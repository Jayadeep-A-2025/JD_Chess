from __future__ import annotations

"""Game-over popup with post-game options: Analyze Game and New Game."""

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.ui.styles import DANGER_BTN, PRIMARY_BTN, SECONDARY_BTN, SUCCESS_BTN


class GameOverDialog(QDialog):
    """Styled, mobile-responsive post-game dialog: win/loss/draw result with Analyze and New Game actions."""

    analyze_clicked = Signal()
    new_game_clicked = Signal()

    def __init__(
        self,
        result: str,           # "win" | "loss" | "draw"
        result_label: str,     # e.g. "Checkmate – You Won!"
        move_count: int,
        game_mode: str,
        player_color: str,
        difficulty: str,
        can_analyze: bool = True,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.result = result
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(300)
        self.setMaximumWidth(480)

        # Dialog root layout with responsive padding
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(8, 8, 8, 8)

        # Outer card container
        outer = QFrame(self)
        outer.setObjectName("gameOverOuter")
        outer.setStyleSheet(
            """
            QFrame#gameOverOuter {
                background-color: #FFFFFF;
                border: 2px solid #CBD5E1;
                border-radius: 18px;
            }
            """
        )
        dialog_layout.addWidget(outer)

        main_layout = QVBoxLayout(outer)
        main_layout.setContentsMargins(24, 28, 24, 28)
        main_layout.setSpacing(18)

        # --- Hero section ---
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(8)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Big emoji / icon based on result
        icon_map = {"win": "🏆", "loss": "😔", "draw": "🤝"}
        icon_lbl = QLabel(icon_map.get(result, "♟"))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 48px;")
        hero_layout.addWidget(icon_lbl)

        # Title
        title_map = {
            "win":  "Congratulations!",
            "loss": "Better Luck Next Time!",
            "draw": "Well Played – Draw!",
        }
        title_lbl = QLabel(title_map.get(result, "Game Over"))
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_color = {
            "win": "#059669", "loss": "#DC2626", "draw": "#D97706"
        }.get(result, "#0F172A")
        title_lbl.setStyleSheet(
            f"font-size: 24px; font-weight: 900; color: {title_color}; letter-spacing: 0.3px;"
        )
        hero_layout.addWidget(title_lbl)

        # Subtitle
        sub_lbl = QLabel(result_label)
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_lbl.setStyleSheet("font-size: 14px; color: #334155; font-weight: 600;")
        sub_lbl.setWordWrap(True)
        hero_layout.addWidget(sub_lbl)

        main_layout.addLayout(hero_layout)

        # --- Stats strip ---
        stats_frame = QFrame()
        stats_frame.setStyleSheet(
            "QFrame { background-color: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 10px; }"
        )
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(12, 10, 12, 10)
        stats_layout.setSpacing(0)

        def _stat(label: str, value: str) -> QWidget:
            w = QWidget()
            v = QVBoxLayout(w)
            v.setSpacing(2)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_lbl = QLabel(value)
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600;")
            v.addWidget(val_lbl)
            v.addWidget(lbl)
            return w

        stats_layout.addWidget(_stat("Moves", str(move_count)))
        stats_layout.addWidget(_divider_v())
        mode_abbr = "vs Computer" if game_mode == "Play vs Computer" else "2-Player"
        stats_layout.addWidget(_stat("Mode", mode_abbr))
        stats_layout.addWidget(_divider_v())
        stats_layout.addWidget(_stat("Playing as", player_color))
        if game_mode == "Play vs Computer":
            stats_layout.addWidget(_divider_v())
            stats_layout.addWidget(_stat("Difficulty", difficulty))

        main_layout.addWidget(stats_frame)

        # --- Action buttons (High-contrast, touch-friendly min-height 44px) ---
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)

        if can_analyze:
            self.analyze_btn = QPushButton("🔍  Analyze Game & Better Moves")
            self.analyze_btn.setObjectName("analyzeBtn")
            self.analyze_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.analyze_btn.setMinimumHeight(44)
            self.analyze_btn.setStyleSheet(PRIMARY_BTN)
            self.analyze_btn.clicked.connect(self._on_analyze)
            btn_layout.addWidget(self.analyze_btn)

        self.new_game_btn = QPushButton("♟  New Game")
        self.new_game_btn.setObjectName("postGameNewGameBtn")
        self.new_game_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_game_btn.setMinimumHeight(44)
        self.new_game_btn.setStyleSheet(SECONDARY_BTN)
        self.new_game_btn.clicked.connect(self._on_new_game)
        btn_layout.addWidget(self.new_game_btn)

        self.play_again_button = self.new_game_btn
        self.analyze_button = getattr(self, "analyze_btn", self.new_game_btn)
        self.home_button = self.new_game_btn

        main_layout.addLayout(btn_layout)
        self.setStyleSheet("background: transparent;")

    def _on_analyze(self) -> None:
        self.analyze_clicked.emit()
        self.accept()

    def _on_new_game(self) -> None:
        self.new_game_clicked.emit()
        self.accept()


def _divider_v() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.Shape.VLine)
    f.setStyleSheet("color: #CBD5E1; min-width: 1px; max-width: 1px;")
    return f
