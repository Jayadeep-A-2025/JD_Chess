from __future__ import annotations

"""Interactive post-game analysis window with scorecard, annotations, and suggestions.
Styled in Royal Gold & Luxury Mahogany theme.
"""

import chess
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.services.analysis_service import AnalysisResult, MoveAnnotation, analyze_game
from app.ui.styles import PRIMARY_BTN, SECONDARY_BTN


# ---------------------------------------------------------------------------
# Background analysis worker
# ---------------------------------------------------------------------------
class AnalysisWorker(QThread):
    """Run analysis in background thread without shadowing QThread.finished.

    Supports cooperative cancellation via the _cancelled flag. The analysis
    service is invoked in full, but the worker checks _cancelled before
    emitting signals so a stopping dialog never receives results for a dead
    parent and never leaves signals connected to a destroyed widget.
    """

    analysis_completed = Signal(object)  # Emits AnalysisResult
    error = Signal(str)

    def __init__(
        self,
        uci_moves: list[str],
        engine_path: str | None,
        player_color: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._cancelled: bool = False
        self.uci_moves = uci_moves
        self.engine_path = engine_path
        self.player_color = player_color

    def cancel(self) -> None:
        """Signal the worker to suppress result/error emission."""
        self._cancelled = True

    def run(self) -> None:
        try:
            result = analyze_game(
                self.uci_moves,
                self.engine_path,
                self.player_color,
                depth=14,
                time_limit=0.20,
            )
            if not self._cancelled:
                self.analysis_completed.emit(result)
        except Exception as exc:
            if not self._cancelled:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Classification palette helpers (tailored for dark mahogany background)
# ---------------------------------------------------------------------------
_CLASSIF_COLORS = {
    "best":       ("#10B981", "rgba(16, 185, 129, 0.15)"),  # Emerald
    "good":       ("#38BDF8", "rgba(56, 189, 248, 0.15)"),  # Sky Blue
    "inaccuracy": ("#FBBF24", "rgba(251, 191, 36, 0.15)"),  # Amber
    "mistake":    ("#FB923C", "rgba(251, 146, 60, 0.15)"),  # Orange
    "blunder":    ("#EF4444", "rgba(239, 68, 68, 0.15)"),   # Red
}


# ---------------------------------------------------------------------------
# Main Analysis Dialog
# ---------------------------------------------------------------------------
class AnalysisDialog(QDialog):
    """Full post-game analysis window in Royal Gold & Luxury Mahogany theme."""

    def __init__(
        self,
        uci_moves: list[str],
        san_moves: list[str],
        player_color: str,
        engine_path: str | None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.uci_moves = uci_moves
        self.san_moves = san_moves
        self.player_color = player_color
        self.engine_path = engine_path
        self._result: AnalysisResult | None = None
        self._worker: AnalysisWorker | None = None

        self.setWindowTitle("Game Analysis")
        self.resize(840, 700)
        self.setMinimumSize(640, 520)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #1E130B;
                color: #FDFBF7;
            }
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- Top bar ---
        top_bar = QFrame()
        top_bar.setStyleSheet(
            """
            QFrame {
                background-color: #1E130B;
                border-bottom: 1.5px solid #D97706;
            }
            """
        )
        top_bar.setFixedHeight(64)
        tb_layout = QHBoxLayout(top_bar)
        tb_layout.setContentsMargins(24, 0, 24, 0)

        title_lbl = QLabel("🔍  Post-Game Analysis")
        title_lbl.setStyleSheet(
            "font-size: 18px; font-weight: 800; color: #FDFBF7; letter-spacing: 0.4px;"
        )
        tb_layout.addWidget(title_lbl)
        tb_layout.addStretch(1)

        close_btn = QPushButton("✕  Close")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2A1B12;
                color: #FDFBF7;
                border: 1.5px solid #D97706;
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: 700;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: #352317;
                color: #D97706;
                border-color: #B45309;
            }
            """
        )
        close_btn.clicked.connect(self.reject)
        tb_layout.addWidget(close_btn)

        root.addWidget(top_bar)

        # --- Content area (stacked: loading -> results) ---
        self._content_area = QWidget()
        self._content_area.setStyleSheet("background-color: #1E130B;")
        self._content_layout = QVBoxLayout(self._content_area)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)
        root.addWidget(self._content_area, 1)

        # Run analysis (uses Computer engine or heuristic fallback)
        self._show_loading()
        self._start_analysis()

    # ------------------------------------------------------------------
    # Worker lifecycle & cleanup
    # ------------------------------------------------------------------
    def _stop_worker(self) -> None:
        """Gracefully cancel and detach the analysis worker thread.

        Strategy:
          1. Call worker.cancel() so the run() loop suppresses any pending
             signal emissions — this eliminates the "signal fired into a
             destroyed parent" crash.
          2. Disconnect all signals immediately to ensure no Qt-queued
             invocations can sneak through before the thread exits.
          3. Ask the thread's event loop to exit (quit()), then wait up to
             5 seconds for a clean join.  5 s is conservative; the analysis
             engine time-limit per move is 0.20 s and the total game is
             bounded, so this always succeeds well within the limit.
          4. If the wait times out (should be impossible in practice), the
             thread is terminated forcibly as a last resort to prevent the
             OS-level dangling thread.
        """
        worker = self._worker
        self._worker = None
        if worker is None:
            return

        # Mark cancelled so run() won't emit after we return.
        worker.cancel()

        # Disconnect signals before waiting to prevent queued callbacks
        # firing on a partially-destroyed dialog.
        for sig in (worker.analysis_completed, worker.error):
            try:
                sig.disconnect()
            except Exception:
                pass
        # Only disconnect QThread.finished if the thread was ever started.
        if worker.isRunning() or worker.isFinished():
            try:
                worker.finished.disconnect()
            except Exception:
                pass

        if worker.isRunning():
            worker.quit()
            if not worker.wait(5_000):
                # Absolute last resort — avoid OS zombie thread
                worker.terminate()
                worker.wait(1_000)

    def closeEvent(self, event) -> None:
        self._stop_worker()
        super().closeEvent(event)

    def reject(self) -> None:
        self._stop_worker()
        super().reject()

    # ------------------------------------------------------------------
    # Loading state
    # ------------------------------------------------------------------
    def _show_loading(self) -> None:
        self._clear_content()
        w = QWidget()
        vb = QVBoxLayout(w)
        vb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vb.setSpacing(16)

        spinner = QLabel("⏳")
        spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spinner.setStyleSheet("font-size: 48px;")
        vb.addWidget(spinner)

        msg = QLabel("Analyzing your game…  This may take a moment.")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setStyleSheet("font-size: 15px; color: #FDFBF7; font-weight: 700;")
        vb.addWidget(msg)

        sub = QLabel(f"Reviewing {len(self.uci_moves)} moves with engine precision")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("font-size: 13px; color: #D97706; font-weight: 600;")
        vb.addWidget(sub)

        self._content_layout.addWidget(w)

    def _show_no_engine(self) -> None:
        self._clear_content()
        w = QWidget()
        vb = QVBoxLayout(w)
        vb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vb.setSpacing(16)

        icon = QLabel("⚠️")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 48px;")
        vb.addWidget(icon)

        msg = QLabel("Computer engine not found.\nInstall Computer engine to enable deep move analysis.")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet("font-size: 14px; color: #FDFBF7; font-weight: 600;")
        vb.addWidget(msg)

        self._show_move_list_only(vb)
        self._content_layout.addWidget(w)

    def _show_move_list_only(self, parent_layout: QVBoxLayout) -> None:
        if not self.san_moves:
            return
        history_lbl = QLabel("Move List")
        history_lbl.setStyleSheet(
            "font-size: 14px; font-weight: 800; color: #D97706; margin-top: 14px;"
        )
        parent_layout.addWidget(history_lbl)
        pairs = []
        for i in range(0, len(self.san_moves), 2):
            w_m = self.san_moves[i]
            b_m = self.san_moves[i + 1] if i + 1 < len(self.san_moves) else ""
            pairs.append(f"{i//2+1:>2}. {w_m:<8} {b_m}")
        moves_lbl = QLabel("\n".join(pairs))
        moves_lbl.setStyleSheet(
            "font-family: Menlo, Monaco, 'Courier New', monospace; font-size: 13px; color: #FDFBF7;"
        )
        parent_layout.addWidget(moves_lbl)

    # ------------------------------------------------------------------
    # Start background analysis
    # ------------------------------------------------------------------
    def _start_analysis(self) -> None:
        self._worker = AnalysisWorker(
            self.uci_moves, self.engine_path, self.player_color, parent=self
        )
        self._worker.analysis_completed.connect(self._on_analysis_done)
        self._worker.error.connect(self._on_analysis_error)
        self._worker.start()

    def _on_analysis_done(self, result: AnalysisResult) -> None:
        self._result = result
        self._show_results(result)

    def _on_analysis_error(self, msg: str) -> None:
        self._show_error(msg)

    def _show_error(self, msg: str) -> None:
        self._clear_content()
        w = QWidget()
        vb = QVBoxLayout(w)
        vb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vb.setContentsMargins(24, 24, 24, 24)

        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #2A1B12;
                border: 1.5px solid #EF4444;
                border-radius: 14px;
                padding: 24px;
            }
            """
        )
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        err_title = QLabel("⚠️  Analysis Notice")
        err_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #EF4444;")
        card_layout.addWidget(err_title)

        err = QLabel(f"Unable to complete full engine analysis:\n{msg}")
        err.setWordWrap(True)
        err.setStyleSheet("font-size: 13px; color: #FDFBF7; font-weight: 500;")
        card_layout.addWidget(err)

        vb.addWidget(card)
        self._content_layout.addWidget(w)

    # ------------------------------------------------------------------
    # Results view
    # ------------------------------------------------------------------
    def _show_results(self, result: AnalysisResult) -> None:
        self._clear_content()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: #1E130B; border: none; }")
        scroll.viewport().setStyleSheet("background-color: #1E130B;")

        container = QWidget()
        container.setStyleSheet("background-color: #1E130B;")
        vb = QVBoxLayout(container)
        vb.setContentsMargins(24, 24, 24, 24)
        vb.setSpacing(20)

        # Incomplete analysis alert if any
        if not result.is_complete and result.error:
            notice = QFrame()
            notice.setStyleSheet(
                """
                QFrame {
                    background-color: #2A1B12;
                    border: 1.5px solid #D97706;
                    border-radius: 12px;
                }
                """
            )
            n_layout = QHBoxLayout(notice)
            n_layout.setContentsMargins(16, 12, 16, 12)
            n_lbl = QLabel(f"ℹ️  Partial Analysis: {result.error}")
            n_lbl.setStyleSheet("color: #FDFBF7; font-size: 13px; font-weight: 600;")
            n_lbl.setWordWrap(True)
            n_layout.addWidget(n_lbl)
            vb.addWidget(notice)

        # --- SCORECARD ---
        vb.addWidget(self._build_scorecard(result))

        # --- PLAYER ANNOTATIONS ---
        player_anns = result.player_annotations(self.player_color)
        if player_anns:
            anns_title = QLabel(f"Your Moves – {self.player_color}")
            anns_title.setStyleSheet(
                "font-size: 16px; font-weight: 800; color: #FDFBF7; letter-spacing: 0.3px; margin-top: 6px;"
            )
            vb.addWidget(anns_title)

            for ann in player_anns:
                vb.addWidget(self._build_move_card(ann))

        # --- OPPONENT ANNOTATIONS ---
        all_other = [a for a in result.annotations if a.color != self.player_color]
        if all_other:
            opp_color = "Black" if self.player_color == "White" else "White"
            opp_title = QLabel(f"Opponent's Moves – {opp_color}")
            opp_title.setStyleSheet(
                "font-size: 16px; font-weight: 800; color: #FDFBF7; letter-spacing: 0.3px; margin-top: 12px;"
            )
            vb.addWidget(opp_title)
            for ann in all_other:
                vb.addWidget(self._build_move_card(ann, muted=True))

        vb.addStretch(1)
        scroll.setWidget(container)
        self._content_layout.addWidget(scroll)

    def _build_scorecard(self, result: AnalysisResult) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #2A1B12;
                border: 1.5px solid #D97706;
                border-radius: 16px;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)

        header = QHBoxLayout()
        sc_title = QLabel("📊  Performance Scorecard")
        sc_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #FDFBF7;")
        header.addWidget(sc_title)
        header.addStretch(1)

        grade_lbl = QLabel(result.grade)
        grade_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grade_color = {
            "A+": "#10B981", "A": "#10B981", "B": "#38BDF8",
            "C": "#FBBF24", "D": "#FB923C", "F": "#EF4444",
        }.get(result.grade, "#D97706")
        grade_lbl.setStyleSheet(
            f"font-size: 30px; font-weight: 900; color: {grade_color};"
            "min-width: 52px; max-width: 52px; min-height: 52px; max-height: 52px;"
            "background-color: #1E130B; border: 1.5px solid #D97706; border-radius: 10px;"
        )
        header.addWidget(grade_lbl)
        layout.addLayout(header)

        # Accuracy bar
        acc_row = QHBoxLayout()
        acc_lbl = QLabel(f"Overall Accuracy:  {result.accuracy_score}%")
        acc_lbl.setStyleSheet("font-size: 13px; color: #FDFBF7; font-weight: 700;")
        acc_row.addWidget(acc_lbl)
        acc_row.addStretch(1)
        layout.addLayout(acc_row)

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(result.accuracy_score)
        bar.setTextVisible(False)
        bar.setFixedHeight(10)
        bar_color = (
            "#10B981" if result.accuracy_score >= 75
            else "#FBBF24" if result.accuracy_score >= 50
            else "#EF4444"
        )
        bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: #1E130B;
                border-radius: 5px;
                border: 1px solid rgba(217, 119, 6, 0.4);
            }}
            QProgressBar::chunk {{
                background-color: {bar_color};
                border-radius: 4px;
            }}
            """
        )
        layout.addWidget(bar)

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(0)

        def _s(label: str, value: str, color: str = "#FDFBF7") -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)
            v.setSpacing(2)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val = QLabel(value)
            val.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val.setStyleSheet(f"font-size: 22px; font-weight: 900; color: {color};")
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 11px; color: #D97706; font-weight: 700; letter-spacing: 0.3px;")
            v.addWidget(val)
            v.addWidget(lbl)
            return w

        def _vd() -> QFrame:
            f = QFrame()
            f.setFrameShape(QFrame.Shape.VLine)
            f.setStyleSheet("color: rgba(217, 119, 6, 0.3); min-width: 1px; max-width: 1px;")
            return f

        stats_row.addWidget(_s("Blunders", str(result.blunders), "#EF4444"))
        stats_row.addWidget(_vd())
        stats_row.addWidget(_s("Mistakes", str(result.mistakes), "#FB923C"))
        stats_row.addWidget(_vd())
        stats_row.addWidget(_s("Inaccuracies", str(result.inaccuracies), "#FBBF24"))
        stats_row.addWidget(_vd())
        best = sum(
            1 for a in result.player_annotations(self.player_color)
            if a.classification in ("best", "good")
        )
        stats_row.addWidget(_s("Best/Good", str(best), "#10B981"))
        layout.addLayout(stats_row)

        return card

    def _build_move_card(self, ann: MoveAnnotation, muted: bool = False) -> QFrame:
        fg, bg = _CLASSIF_COLORS.get(ann.classification, ("#D97706", "rgba(217, 119, 6, 0.15)"))
        card = QFrame()
        card_border = "#D97706" if not muted else "rgba(217, 119, 6, 0.4)"
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: #2A1B12;
                border-radius: 12px;
                border: 1.5px solid {card_border};
            }}
            """
        )
        row = QHBoxLayout(card)
        row.setContentsMargins(16, 12, 16, 12)
        row.setSpacing(14)

        # Move number
        num_lbl = QLabel(f"{ann.move_number}.")
        num_lbl.setFixedWidth(32)
        num_lbl.setStyleSheet("font-size: 13px; color: #D97706; font-weight: 700;")
        row.addWidget(num_lbl)

        # SAN move played
        san_lbl = QLabel(ann.san)
        san_lbl.setFixedWidth(64)
        san_lbl.setStyleSheet(
            "font-size: 15px; font-weight: 800; color: #FDFBF7;"
            "font-family: Menlo, Monaco, 'Courier New', monospace;"
        )
        row.addWidget(san_lbl)

        # Classification badge
        badge = QLabel(ann.classification.capitalize())
        badge.setStyleSheet(
            f"font-size: 11px; font-weight: 700; color: {fg};"
            f"background-color: {bg}; border: 1.5px solid {fg};"
            "border-radius: 6px; padding: 3px 8px;"
        )
        row.addWidget(badge)

        # Comment
        comment_lbl = QLabel(ann.comment)
        comment_lbl.setWordWrap(True)
        comment_lbl.setStyleSheet("font-size: 13px; color: #FDFBF7; font-weight: 500;")
        row.addWidget(comment_lbl, 1)

        # Best move suggestion (if different from played)
        if ann.best_uci and ann.best_uci != ann.uci and not muted:
            best_lbl = QLabel(f"Better: {ann.best_san}")
            best_lbl.setStyleSheet(
                "font-size: 12px; font-weight: 800; color: #10B981;"
                "font-family: Menlo, Monaco, 'Courier New', monospace;"
                "background-color: rgba(16, 185, 129, 0.15); border: 1px solid #10B981;"
                "border-radius: 6px; padding: 2px 8px;"
            )
            row.addWidget(best_lbl)

        return card

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _clear_content(self) -> None:
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
