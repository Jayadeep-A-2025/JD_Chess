from __future__ import annotations

"""Interactive post-game analysis window with scorecard, annotations, and suggestions."""

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
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.services.analysis_service import AnalysisResult, MoveAnnotation, analyze_game
from app.ui.styles import PRIMARY_BTN, SECONDARY_BTN, card_style, combo_style


# ---------------------------------------------------------------------------
# Background analysis worker
# ---------------------------------------------------------------------------
class AnalysisWorker(QThread):
    """Run analysis in background thread."""

    finished = Signal(object)   # AnalysisResult
    error = Signal(str)

    def __init__(
        self,
        uci_moves: list[str],
        engine_path: str | None,
        player_color: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.uci_moves = uci_moves
        self.engine_path = engine_path
        self.player_color = player_color

    def run(self) -> None:
        try:
            result = analyze_game(
                self.uci_moves,
                self.engine_path,
                self.player_color,
                depth=14,
                time_limit=0.20,
            )
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Colour palette helpers
# ---------------------------------------------------------------------------
_CLASSIF_COLORS = {
    "best":       ("#059669", "#D1FAE5"),   # green
    "good":       ("#0284C7", "#E0F2FE"),   # blue
    "inaccuracy": ("#D97706", "#FEF3C7"),   # amber
    "mistake":    ("#EA580C", "#FFEDD5"),   # orange
    "blunder":    ("#DC2626", "#FEE2E2"),   # red
}


# ---------------------------------------------------------------------------
# Main Analysis Dialog
# ---------------------------------------------------------------------------
class AnalysisDialog(QDialog):
    """Full post-game analysis window."""

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

        self.setWindowTitle("Game Analysis")
        self.resize(820, 680)
        self.setMinimumSize(640, 500)
        self.setStyleSheet("QDialog { background-color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- Top bar ---
        top_bar = QFrame()
        top_bar.setStyleSheet(
            "QFrame { background-color: #0F172A; border: none; }"
        )
        top_bar.setFixedHeight(60)
        tb_layout = QHBoxLayout(top_bar)
        tb_layout.setContentsMargins(24, 0, 24, 0)

        title_lbl = QLabel("🔍  Post-Game Analysis")
        title_lbl.setStyleSheet(
            "font-size: 17px; font-weight: 800; color: #F1F5F9; letter-spacing: 0.3px;"
        )
        tb_layout.addWidget(title_lbl)
        tb_layout.addStretch(1)

        close_btn = QPushButton("✕  Close")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 5px 14px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #1E293B; color: #F1F5F9; }
            """
        )
        close_btn.clicked.connect(self.reject)
        tb_layout.addWidget(close_btn)

        root.addWidget(top_bar)

        # --- Content area (stacked: loading -> results) ---
        self._content_area = QWidget()
        self._content_layout = QVBoxLayout(self._content_area)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)
        root.addWidget(self._content_area, 1)

        # Run analysis (will use Computer engine or heuristic fallback)
        self._show_loading()
        self._start_analysis()

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
        spinner.setStyleSheet("font-size: 44px;")
        vb.addWidget(spinner)

        msg = QLabel("Analyzing your game…  This may take a moment.")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setStyleSheet("font-size: 14px; color: #64748B; font-weight: 500;")
        vb.addWidget(msg)

        sub = QLabel(f"Reviewing {len(self.uci_moves)} moves")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("font-size: 12px; color: #94A3B8;")
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
        icon.setStyleSheet("font-size: 44px;")
        vb.addWidget(icon)

        msg = QLabel("Computer engine not found.\nInstall Computer engine to enable deep move analysis.")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet("font-size: 14px; color: #64748B; font-weight: 500;")
        vb.addWidget(msg)

        # Show move list fallback
        self._show_move_list_only(vb)

        self._content_layout.addWidget(w)

    def _show_move_list_only(self, parent_layout: QVBoxLayout) -> None:
        if not self.san_moves:
            return
        history_lbl = QLabel("Move List")
        history_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 12px;")
        parent_layout.addWidget(history_lbl)
        pairs = []
        for i in range(0, len(self.san_moves), 2):
            w_m = self.san_moves[i]
            b_m = self.san_moves[i + 1] if i + 1 < len(self.san_moves) else ""
            pairs.append(f"{i//2+1:>2}. {w_m:<8} {b_m}")
        moves_lbl = QLabel("\n".join(pairs))
        moves_lbl.setStyleSheet(
            "font-family: Menlo, Monaco, 'Courier New', monospace; font-size: 12px; color: #334155;"
        )
        parent_layout.addWidget(moves_lbl)

    # ------------------------------------------------------------------
    # Start background analysis
    # ------------------------------------------------------------------
    def _start_analysis(self) -> None:
        self._worker = AnalysisWorker(
            self.uci_moves, self.engine_path, self.player_color, parent=self
        )
        self._worker.finished.connect(self._on_analysis_done)
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
        err = QLabel(f"Analysis failed:\n{msg}")
        err.setAlignment(Qt.AlignmentFlag.AlignCenter)
        err.setWordWrap(True)
        err.setStyleSheet("font-size: 13px; color: #DC2626;")
        vb.addWidget(err)
        self._content_layout.addWidget(w)

    # ------------------------------------------------------------------
    # Results view
    # ------------------------------------------------------------------
    def _show_results(self, result: AnalysisResult) -> None:
        self._clear_content()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        scroll.viewport().setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        vb = QVBoxLayout(container)
        vb.setContentsMargins(24, 24, 24, 24)
        vb.setSpacing(20)

        # --- SCORECARD ---
        vb.addWidget(self._build_scorecard(result))

        # --- PLAYER ANNOTATIONS ---
        player_anns = result.player_annotations(self.player_color)
        if player_anns:
            anns_title = QLabel(f"Your Moves – {self.player_color}")
            anns_title.setStyleSheet(
                "font-size: 14px; font-weight: 800; color: #0F172A; letter-spacing: 0.2px;"
            )
            vb.addWidget(anns_title)

            for ann in player_anns:
                vb.addWidget(self._build_move_card(ann))

        # --- FULL GAME MOVES (ALL) ---
        all_other = [a for a in result.annotations if a.color != self.player_color]
        if all_other:
            opp_color = "Black" if self.player_color == "White" else "White"
            opp_title = QLabel(f"Opponent's Moves – {opp_color}")
            opp_title.setStyleSheet(
                "font-size: 14px; font-weight: 800; color: #0F172A; margin-top: 4px;"
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0F172A, stop:1 #1E293B);
                border-radius: 14px;
                border: none;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        sc_title = QLabel("📊  Performance Scorecard")
        sc_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #F1F5F9;")
        header.addWidget(sc_title)
        header.addStretch(1)
        grade_lbl = QLabel(result.grade)
        grade_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grade_color = {
            "A+": "#34D399", "A": "#34D399", "B": "#60A5FA",
            "C": "#FBBF24", "D": "#F97316", "F": "#F87171",
        }.get(result.grade, "#94A3B8")
        grade_lbl.setStyleSheet(
            f"font-size: 32px; font-weight: 900; color: {grade_color};"
            "min-width: 52px; max-width: 52px; min-height: 52px; max-height: 52px;"
            f"background-color: rgba(255,255,255,0.08); border-radius: 10px;"
        )
        header.addWidget(grade_lbl)
        layout.addLayout(header)

        # Accuracy bar
        acc_row = QHBoxLayout()
        acc_lbl = QLabel(f"Accuracy  {result.accuracy_score}%")
        acc_lbl.setStyleSheet("font-size: 13px; color: #CBD5E1; font-weight: 600;")
        acc_row.addWidget(acc_lbl)
        acc_row.addStretch(1)
        layout.addLayout(acc_row)

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(result.accuracy_score)
        bar.setTextVisible(False)
        bar.setFixedHeight(8)
        bar_color = (
            "#34D399" if result.accuracy_score >= 75
            else "#FBBF24" if result.accuracy_score >= 50
            else "#F87171"
        )
        bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: rgba(255,255,255,0.12);
                border-radius: 4px;
                border: none;
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

        def _s(label: str, value: str, color: str = "#F1F5F9") -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)
            v.setSpacing(2)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val = QLabel(value)
            val.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val.setStyleSheet(f"font-size: 20px; font-weight: 900; color: {color};")
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
            v.addWidget(val)
            v.addWidget(lbl)
            return w

        def _vd() -> QFrame:
            f = QFrame()
            f.setFrameShape(QFrame.Shape.VLine)
            f.setStyleSheet("color: rgba(255,255,255,0.12); min-width: 1px; max-width: 1px;")
            return f

        stats_row.addWidget(_s("Blunders", str(result.blunders), "#F87171"))
        stats_row.addWidget(_vd())
        stats_row.addWidget(_s("Mistakes", str(result.mistakes), "#FBBF24"))
        stats_row.addWidget(_vd())
        stats_row.addWidget(_s("Inaccuracies", str(result.inaccuracies), "#60A5FA"))
        stats_row.addWidget(_vd())
        total_moves = len(result.player_annotations(self.player_color))
        best = sum(
            1 for a in result.player_annotations(self.player_color)
            if a.classification in ("best", "good")
        )
        stats_row.addWidget(_s("Best/Good", str(best), "#34D399"))
        layout.addLayout(stats_row)

        return card

    def _build_move_card(self, ann: MoveAnnotation, muted: bool = False) -> QFrame:
        fg, bg = _CLASSIF_COLORS.get(ann.classification, ("#475569", "#F1F5F9"))
        if muted:
            bg = "#F8FAFC"
            fg = "#94A3B8"

        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {bg};
                border-radius: 10px;
                border: 1px solid {fg}30;
            }}
            """
        )
        row = QHBoxLayout(card)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(14)

        # Move number badge
        num_lbl = QLabel(f"{ann.move_number}.")
        num_lbl.setFixedWidth(30)
        num_lbl.setStyleSheet("font-size: 12px; color: #94A3B8; font-weight: 600;")
        row.addWidget(num_lbl)

        # SAN move played
        san_lbl = QLabel(ann.san)
        san_lbl.setFixedWidth(60)
        san_lbl.setStyleSheet(
            f"font-size: 15px; font-weight: 800; color: {fg};"
            "font-family: Menlo, Monaco, 'Courier New', monospace;"
        )
        row.addWidget(san_lbl)

        # Classification badge
        badge = QLabel(ann.classification.capitalize())
        badge.setStyleSheet(
            f"font-size: 11px; font-weight: 700; color: {fg};"
            f"background-color: {fg}18; border: 1px solid {fg}40;"
            "border-radius: 6px; padding: 2px 8px;"
        )
        row.addWidget(badge)

        # Comment
        comment_lbl = QLabel(ann.comment)
        comment_lbl.setWordWrap(True)
        comment_lbl.setStyleSheet("font-size: 12px; color: #475569;")
        row.addWidget(comment_lbl, 1)

        # Best move suggestion (if different from played)
        if ann.best_uci and ann.best_uci != ann.uci and not muted:
            best_lbl = QLabel(f"→ {ann.best_san}")
            best_lbl.setStyleSheet(
                "font-size: 12px; font-weight: 700; color: #059669;"
                "font-family: Menlo, Monaco, 'Courier New', monospace;"
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
