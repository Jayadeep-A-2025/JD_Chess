from __future__ import annotations

"""Window 1: Main Home Menu."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.save_manager import SaveManager


class HomeScreen(QWidget):
    """Main Home Menu screen with 'New Game' and 'Continue Game' options."""

    new_game_clicked = Signal()
    continue_game_clicked = Signal()

    def __init__(
        self,
        save_manager: SaveManager,
        engine_ready: bool = True,
        engine_path: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.save_manager = save_manager
        self.engine_ready = engine_ready
        self.engine_path = engine_path

        self.setStyleSheet("QWidget { background-color: #F8FAFC; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(32)

        main_layout.addStretch(1)

        # Centered container for max width control and polish
        center_container = QWidget()
        center_container.setMaximumWidth(680)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(28)

        # HERO HEADER
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(8)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Crown icon / emblem
        emblem = QLabel("♔")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emblem.setStyleSheet(
            "font-size: 54px; color: #1E293B; background: #FFFFFF; "
            "border: 2px solid #E2E8F0; border-radius: 40px; "
            "min-width: 80px; max-width: 80px; min-height: 80px; max-height: 80px;"
        )
        hero_layout.addWidget(emblem, 0, Qt.AlignmentFlag.AlignCenter)

        # Main Title
        title = QLabel("JD CHESS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 36px; font-weight: 900; color: #0F172A; "
            "letter-spacing: 1.5px;"
        )
        hero_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Master the board with intelligent offline computer analysis.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #64748B; font-weight: 500;")
        hero_layout.addWidget(subtitle)

        # Engine Status Badge
        self.engine_badge = QLabel()
        self.engine_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_engine_status(self.engine_ready, self.engine_path)
        hero_layout.addWidget(self.engine_badge, 0, Qt.AlignmentFlag.AlignCenter)

        center_layout.addLayout(hero_layout)

        # PRIMARY CHOICES CONTAINER (Cards for New Game & Continue Game)
        choices_layout = QHBoxLayout()
        choices_layout.setSpacing(20)

        # 1. NEW GAME CARD
        self.new_game_card = self._create_hero_card(
            title_text="New Game",
            desc_text="Start a fresh match with custom rules, side perspective, and computer difficulty.",
            btn_text="New Game →",
            btn_id="homeNewGameBtn",
            is_primary=True,
            badge_text="Fresh Match",
            on_click=self.new_game_clicked.emit,
        )
        choices_layout.addWidget(self.new_game_card)

        # 2. CONTINUE GAME CARD
        self.continue_game_card, self.save_status_badge, self.continue_btn = (
            self._create_continue_card()
        )
        choices_layout.addWidget(self.continue_game_card)

        center_layout.addLayout(choices_layout)

        # FOOTER INFO
        footer_lbl = QLabel("3 Save Slots Supported • Local Two-Player & Computer Play Modes")
        footer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        center_layout.addWidget(footer_lbl)

        main_layout.addWidget(center_container, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(2)

        self.update_save_status()

    def set_engine_status(self, ready: bool, path: str | None = None) -> None:
        self.engine_ready = ready
        self.engine_path = path
        if ready:
            self.engine_badge.setText("● Computer Ready")
            self.engine_badge.setToolTip(f"Engine available: {path or 'System Engine'}")
            self.engine_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #15803D; "
                "background-color: #DCFCE7; border: 1px solid #86EFAC; "
                "border-radius: 12px; padding: 4px 14px;"
            )
        else:
            self.engine_badge.setText("⚠ Computer Not Found")
            self.engine_badge.setToolTip("Install Computer chess engine to play against AI.")
            self.engine_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #B91C1C; "
                "background-color: #FEE2E2; border: 1px solid #FCA5A5; "
                "border-radius: 12px; padding: 4px 14px;"
            )

    def _create_hero_card(
        self,
        title_text: str,
        desc_text: str,
        btn_text: str,
        btn_id: str,
        is_primary: bool,
        badge_text: str,
        on_click,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("heroCard")
        card.setStyleSheet(
            """
            QFrame#heroCard {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 16px;
            }
            QFrame#heroCard:hover {
                border-color: #2563EB;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        top_row = QHBoxLayout()
        badge = QLabel(badge_text)
        badge.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #2563EB; "
            "background-color: #EFF6FF; border: 1px solid #DBEAFE; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel(title_text)
        card_title.setStyleSheet("font-size: 19px; font-weight: 800; color: #0F172A;")
        layout.addWidget(card_title)

        card_desc = QLabel(desc_text)
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 13px; color: #64748B; line-height: 1.4;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton(btn_text)
        btn.setObjectName(btn_id)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(44)
        if is_primary:
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #2563EB;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 10px;
                    padding: 8px 18px;
                    font-size: 14px;
                    font-weight: 700;
                }
                QPushButton:hover { background-color: #1D4ED8; }
                QPushButton:pressed { background-color: #1E40AF; }
                """
            )
        else:
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFFFFF;
                    color: #1E293B;
                    border: 1.5px solid #CBD5E1;
                    border-radius: 10px;
                    padding: 8px 18px;
                    font-size: 14px;
                    font-weight: 700;
                }
                QPushButton:hover { background-color: #F8FAFC; border-color: #94A3B8; }
                QPushButton:pressed { background-color: #F1F5F9; }
                """
            )
        btn.clicked.connect(on_click)
        layout.addWidget(btn)

        return card

    def _create_continue_card(self) -> tuple[QFrame, QLabel, QPushButton]:
        card = QFrame()
        card.setObjectName("continueCard")
        card.setStyleSheet(
            """
            QFrame#continueCard {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 16px;
            }
            QFrame#continueCard:hover {
                border-color: #2563EB;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        top_row = QHBoxLayout()
        status_badge = QLabel("0 / 3 Slots")
        status_badge.setObjectName("saveStatusBadge")
        status_badge.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #475569; "
            "background-color: #F1F5F9; border: 1px solid #E2E8F0; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(status_badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel("Continue Game")
        card_title.setStyleSheet("font-size: 19px; font-weight: 800; color: #0F172A;")
        layout.addWidget(card_title)

        card_desc = QLabel("Resume a saved match where you left off from one of your active slots.")
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 13px; color: #64748B; line-height: 1.4;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton("Continue Game →")
        btn.setObjectName("homeContinueGameBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(44)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #1E293B;
                border: 1.5px solid #CBD5E1;
                border-radius: 10px;
                padding: 8px 18px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #F8FAFC; border-color: #94A3B8; }
            QPushButton:pressed { background-color: #F1F5F9; }
            """
        )
        btn.clicked.connect(self.continue_game_clicked.emit)
        layout.addWidget(btn)

        return card, status_badge, btn

    def update_save_status(self) -> None:
        """Update badge showing count of active saved games."""
        count = self.save_manager.active_save_count()
        if count > 0:
            self.save_status_badge.setText(f"{count} / 3 Active Saves")
            self.save_status_badge.setStyleSheet(
                "font-size: 11px; font-weight: 700; color: #047857; "
                "background-color: #D1FAE5; border: 1px solid #A7F3D0; "
                "border-radius: 6px; padding: 2px 8px;"
            )
        else:
            self.save_status_badge.setText("No Active Saves")
            self.save_status_badge.setStyleSheet(
                "font-size: 11px; font-weight: 700; color: #64748B; "
                "background-color: #F1F5F9; border: 1px solid #E2E8F0; "
                "border-radius: 6px; padding: 2px 8px;"
            )
