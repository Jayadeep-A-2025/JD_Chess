from __future__ import annotations

"""Match History & Rating Progression dashboard screen."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
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

from app.services.history_manager import HistoryManager, MatchRecord
from app.ui.styles import SECONDARY_BTN, combo_style


class HistoryScreen(QWidget):
    """Match history view reachable from the Home screen."""

    back_clicked = Signal()

    def __init__(
        self,
        history_manager: HistoryManager,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.history_manager = history_manager
        self.setStyleSheet("QWidget { background-color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- Top bar ---
        top_bar = QFrame()
        top_bar.setStyleSheet("QFrame { background-color: #0F172A; border: none; }")
        top_bar.setFixedHeight(64)
        tb_layout = QHBoxLayout(top_bar)
        tb_layout.setContentsMargins(24, 0, 24, 0)

        back_btn = QPushButton("← Back to Menu")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setMinimumHeight(40)
        back_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                border: 1.5px solid #334155;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #1E293B; color: #F1F5F9; border-color: #64748B; }
            """
        )
        back_btn.clicked.connect(self.back_clicked.emit)
        tb_layout.addWidget(back_btn)

        title_lbl = QLabel("Match History & Player Rating")
        title_lbl.setStyleSheet(
            "font-size: 17px; font-weight: 800; color: #F1F5F9; letter-spacing: 0.3px;"
        )
        tb_layout.addWidget(title_lbl, 1, Qt.AlignmentFlag.AlignCenter)

        # Placeholder to balance centering
        ph = QWidget()
        ph.setFixedWidth(back_btn.sizeHint().width())
        tb_layout.addWidget(ph)

        root.addWidget(top_bar)

        # --- Scrollable content ---
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self._scroll.viewport().setStyleSheet("background: transparent;")

        self._inner = QWidget()
        self._inner.setStyleSheet("background: transparent;")
        self._inner_layout = QVBoxLayout(self._inner)
        self._inner_layout.setContentsMargins(28, 24, 28, 24)
        self._inner_layout.setSpacing(18)

        self._scroll.setWidget(self._inner)
        root.addWidget(self._scroll, 1)

        # Persistent filters state
        self._selected_outcome = "All Outcomes"
        self._selected_mode = "All Modes"

        self.refresh()

    # ------------------------------------------------------------------
    # Public refresh
    # ------------------------------------------------------------------
    def refresh(self) -> None:
        """Re-read history data and rebuild the UI."""
        # Clear existing content
        while self._inner_layout.count():
            item = self._inner_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        rating = self.history_manager.get_rating()
        all_matches = self.history_manager.get_all_matches()

        # 1. Rating card
        self._inner_layout.addWidget(self._build_rating_card(rating, all_matches))

        # 2. Modern Styled Filter Controls
        if all_matches:
            self._inner_layout.addWidget(self._build_filter_bar())

        # 3. Filtered Matches
        filtered_matches = self._filter_matches(all_matches)

        if not all_matches:
            empty_lbl = QLabel(
                "No match history yet.\nPlay your first game to track your rating and analyze growth over time!"
            )
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setWordWrap(True)
            empty_lbl.setStyleSheet(
                "font-size: 14px; color: #94A3B8; margin-top: 40px; font-weight: 500;"
            )
            self._inner_layout.addWidget(empty_lbl)
        elif not filtered_matches:
            no_match_lbl = QLabel("No games match the selected filters.")
            no_match_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_match_lbl.setStyleSheet("font-size: 13px; color: #94A3B8; margin-top: 20px;")
            self._inner_layout.addWidget(no_match_lbl)
        else:
            hist_header = QLabel(f"Past Games Log ({len(filtered_matches)} displayed)")
            hist_header.setStyleSheet(
                "font-size: 14px; font-weight: 800; color: #0F172A; letter-spacing: 0.2px;"
            )
            self._inner_layout.addWidget(hist_header)
            for record in filtered_matches:
                self._inner_layout.addWidget(self._build_match_card(record))

        self._inner_layout.addStretch(1)

    def _build_filter_bar(self) -> QFrame:
        """Bar with modern styled dropdowns to filter matches across modes and outcomes."""
        bar = QFrame()
        bar.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px; }"
        )
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(14)

        lbl = QLabel("Filter Games:")
        lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #1E293B;")
        layout.addWidget(lbl)

        style = combo_style()

        # Outcome combo
        self.outcome_combo = QComboBox()
        self.outcome_combo.setObjectName("historyOutcomeFilter")
        self.outcome_combo.addItems(["All Outcomes", "Wins Only", "Losses Only", "Draws Only"])
        self.outcome_combo.setCurrentText(self._selected_outcome)
        self.outcome_combo.setStyleSheet(style)
        self.outcome_combo.currentTextChanged.connect(self._on_outcome_filter_changed)
        layout.addWidget(self.outcome_combo)

        # Mode combo
        self.mode_combo = QComboBox()
        self.mode_combo.setObjectName("historyModeFilter")
        self.mode_combo.addItems(["All Modes", "Play vs Computer", "Local 2-player"])
        self.mode_combo.setCurrentText(self._selected_mode)
        self.mode_combo.setStyleSheet(style)
        self.mode_combo.currentTextChanged.connect(self._on_mode_filter_changed)
        layout.addWidget(self.mode_combo)

        layout.addStretch(1)
        return bar

    def _on_outcome_filter_changed(self, text: str) -> None:
        self._selected_outcome = text
        self.refresh()

    def _on_mode_filter_changed(self, text: str) -> None:
        self._selected_mode = text
        self.refresh()

    def _filter_matches(self, matches: list[MatchRecord]) -> list[MatchRecord]:
        result = []
        for m in matches:
            if self._selected_outcome == "Wins Only" and m.result != "win":
                continue
            if self._selected_outcome == "Losses Only" and m.result != "loss":
                continue
            if self._selected_outcome == "Draws Only" and m.result != "draw":
                continue
            if self._selected_mode == "Play vs Computer" and m.game_mode != "Play vs Computer":
                continue
            if self._selected_mode == "Local 2-player" and m.game_mode != "Local 2-player":
                continue
            result.append(m)
        return result

    # ------------------------------------------------------------------
    # Card builders
    # ------------------------------------------------------------------
    def _build_rating_card(
        self, rating: int, matches: list[MatchRecord]
    ) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0F172A, stop:1 #1E3A5F);
                border-radius: 16px;
                border: none;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        header_row = QHBoxLayout()

        title = QLabel("⭐  Your Rating & Skill Level")
        title.setStyleSheet("font-size: 15px; font-weight: 700; color: #CBD5E1;")
        header_row.addWidget(title)
        header_row.addStretch(1)
        layout.addLayout(header_row)

        # Big rating number
        rating_lbl = QLabel(str(rating))
        rating_lbl.setStyleSheet(
            "font-size: 54px; font-weight: 900; color: #FFFFFF; letter-spacing: -2px;"
        )
        layout.addWidget(rating_lbl)

        # Win/loss/draw stats
        wins   = sum(1 for m in matches if m.result == "win")
        losses = sum(1 for m in matches if m.result == "loss")
        draws  = sum(1 for m in matches if m.result == "draw")
        total  = len(matches)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(0)

        def _s(label: str, value: str, color: str) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)
            v.setSpacing(2)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vl = QLabel(value)
            vl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vl.setStyleSheet(f"font-size: 22px; font-weight: 900; color: {color};")
            ll = QLabel(label)
            ll.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ll.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 500;")
            v.addWidget(vl)
            v.addWidget(ll)
            return w

        def _vd() -> QFrame:
            f = QFrame()
            f.setFrameShape(QFrame.Shape.VLine)
            f.setStyleSheet("color: rgba(255,255,255,0.1); min-width: 1px; max-width: 1px;")
            return f

        stats_row.addWidget(_s("Wins", str(wins), "#34D399"))
        stats_row.addWidget(_vd())
        stats_row.addWidget(_s("Losses", str(losses), "#F87171"))
        stats_row.addWidget(_vd())
        stats_row.addWidget(_s("Draws", str(draws), "#FBBF24"))
        stats_row.addWidget(_vd())
        stats_row.addWidget(_s("Total Games", str(total), "#93C5FD"))
        layout.addLayout(stats_row)

        # Win-rate progress bar
        if total > 0:
            win_pct = int(wins / total * 100)
            bar_row = QHBoxLayout()
            bar_lbl = QLabel(f"Win Rate  {win_pct}%")
            bar_lbl.setStyleSheet("font-size: 12px; color: #94A3B8; font-weight: 600;")
            bar_row.addWidget(bar_lbl)
            bar_row.addStretch(1)
            layout.addLayout(bar_row)

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(win_pct)
            bar.setTextVisible(False)
            bar.setFixedHeight(8)
            bar.setStyleSheet(
                """
                QProgressBar {
                    background-color: rgba(255,255,255,0.10);
                    border-radius: 4px;
                    border: none;
                }
                QProgressBar::chunk {
                    background-color: #34D399;
                    border-radius: 4px;
                }
                """
            )
            layout.addWidget(bar)

        return card

    def _build_match_card(self, record: MatchRecord) -> QFrame:
        result_colors = {
            "win":  ("#059669", "#D1FAE5", "W"),
            "loss": ("#DC2626", "#FEE2E2", "L"),
            "draw": ("#D97706", "#FEF3C7", "D"),
        }
        fg, bg, letter = result_colors.get(record.result, ("#475569", "#F1F5F9", "?"))

        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 12px;
            }}
            QFrame:hover {{
                border-color: #CBD5E1;
                background-color: #FAFBFC;
            }}
            """
        )
        row = QHBoxLayout(card)
        row.setContentsMargins(16, 14, 16, 14)
        row.setSpacing(16)

        # Result badge
        badge = QLabel(letter)
        badge.setFixedSize(38, 38)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"font-size: 16px; font-weight: 900; color: {fg};"
            f"background-color: {bg}; border-radius: 10px;"
        )
        row.addWidget(badge)

        # Details column
        details = QVBoxLayout()
        details.setSpacing(4)

        result_lbl = QLabel(record.result_label)
        result_lbl.setStyleSheet(
            f"font-size: 13px; font-weight: 700; color: {fg};"
        )
        details.addWidget(result_lbl)

        mode_str = record.game_mode
        if record.game_mode == "Play vs Computer":
            mode_str = f"vs Computer ({record.difficulty})"
        sub_lbl = QLabel(f"{mode_str}  ·  {record.move_count} moves  ·  Playing as {record.player_color}")
        sub_lbl.setStyleSheet("font-size: 12px; color: #64748B;")
        details.addWidget(sub_lbl)

        date_lbl = QLabel(record.played_at_formatted)
        date_lbl.setStyleSheet("font-size: 11px; color: #94A3B8;")
        details.addWidget(date_lbl)

        row.addLayout(details, 1)

        # Right column: rating change + accuracy
        right = QVBoxLayout()
        right.setSpacing(4)
        right.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        delta = record.rating_change
        sign = "+" if delta >= 0 else ""
        delta_color = "#059669" if delta >= 0 else "#DC2626"
        delta_lbl = QLabel(f"{sign}{delta} pts")
        delta_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        delta_lbl.setStyleSheet(
            f"font-size: 14px; font-weight: 800; color: {delta_color};"
        )
        right.addWidget(delta_lbl)

        rating_lbl = QLabel(f"→ {record.rating_after}")
        rating_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        rating_lbl.setStyleSheet("font-size: 11px; color: #94A3B8;")
        right.addWidget(rating_lbl)

        if record.accuracy_score > 0:
            acc_lbl = QLabel(f"Acc {record.accuracy_score}%")
            acc_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            acc_lbl.setStyleSheet("font-size: 11px; color: #0284C7; font-weight: 600;")
            right.addWidget(acc_lbl)

        row.addLayout(right)
        return card
