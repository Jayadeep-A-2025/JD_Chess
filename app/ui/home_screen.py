from __future__ import annotations

"""Window 1: Main Home Menu with User Profile, CM Greetings, and 4 Primary Paths."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.history_manager import HistoryManager
from app.services.save_manager import SaveManager
from app.services.user_profile_manager import UserProfileManager


class HomeScreen(QWidget):
    """Main Home Menu with User Profile, companion CM, and 4 main options."""

    new_game_clicked = Signal()
    continue_game_clicked = Signal()
    learn_chess_clicked = Signal()
    history_clicked = Signal()
    username_changed = Signal(str)

    def __init__(
        self,
        save_manager: SaveManager,
        profile_manager: UserProfileManager | None = None,
        history_manager: HistoryManager | None = None,
        engine_ready: bool = True,
        engine_path: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.save_manager = save_manager
        self.profile_manager = profile_manager or UserProfileManager()
        self.history_manager = history_manager or HistoryManager()
        self.engine_ready = engine_ready
        self.engine_path = engine_path

        self.setStyleSheet("QWidget { background-color: #F8FAFC; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 24, 32, 28)
        main_layout.setSpacing(20)

        # -------------------------------------------------------------
        # TOP BAR: User Profile & Companion CM Greeting
        # -------------------------------------------------------------
        profile_card = self._build_profile_card()
        main_layout.addWidget(profile_card)

        main_layout.addStretch(1)

        # -------------------------------------------------------------
        # CENTER CONTAINER: Hero Branding & 4 Primary Choice Cards
        # -------------------------------------------------------------
        center_container = QWidget()
        center_container.setMaximumWidth(760)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(22)

        # HERO HEADER
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(8)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        emblem = QLabel("♔")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emblem.setStyleSheet(
            "font-size: 50px; color: #1E293B; background: #FFFFFF; "
            "border: 2px solid #E2E8F0; border-radius: 36px; "
            "min-width: 72px; max-width: 72px; min-height: 72px; max-height: 72px;"
        )
        hero_layout.addWidget(emblem, 0, Qt.AlignmentFlag.AlignCenter)

        title = QLabel("JD CHESS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 34px; font-weight: 900; color: #0F172A; letter-spacing: 1.5px;"
        )
        hero_layout.addWidget(title)

        subtitle = QLabel("Play, learn, and master chess with intelligent offline computer analysis.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")
        hero_layout.addWidget(subtitle)

        # Engine Status Badge
        self.engine_badge = QLabel()
        self.engine_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_engine_status(self.engine_ready, self.engine_path)
        hero_layout.addWidget(self.engine_badge, 0, Qt.AlignmentFlag.AlignCenter)

        center_layout.addLayout(hero_layout)

        # -------------------------------------------------------------
        # 4 PRIMARY CHOICES (2x2 Grid)
        # -------------------------------------------------------------
        grid = QGridLayout()
        grid.setSpacing(16)

        # 1. NEW GAME
        self.new_game_card = self._create_card(
            title_text="New Game",
            desc_text="Start a fresh match with custom rules, side perspective, and computer difficulty.",
            btn_text="New Game →",
            btn_id="homeNewGameBtn",
            badge_text="Fresh Match",
            badge_color=("#2563EB", "#EFF6FF", "#DBEAFE"),
            on_click=self.new_game_clicked.emit,
            is_primary=True,
        )
        grid.addWidget(self.new_game_card, 0, 0)

        # 2. CONTINUE GAME
        self.continue_game_card, self.save_status_badge, self.continue_btn = (
            self._create_continue_card()
        )
        grid.addWidget(self.continue_game_card, 0, 1)

        # 3. LEARN CHESS (with CM)
        self.learn_card, self.learn_badge = self._create_learn_card()
        grid.addWidget(self.learn_card, 1, 0)

        # 4. MATCH HISTORY & RATING
        self.history_card, self.history_badge = self._create_history_card()
        grid.addWidget(self.history_card, 1, 1)

        center_layout.addLayout(grid)

        # FOOTER INFO
        footer_lbl = QLabel(
            "AI Companion CM • 3 Active Save Slots • Offline Match Analysis & Elo Rating"
        )
        footer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        center_layout.addWidget(footer_lbl)

        main_layout.addWidget(center_container, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(2)

        self.update_save_status()
        self.update_profile_ui()

    # -------------------------------------------------------------
    # Profile & CM Header Card
    # -------------------------------------------------------------
    def _build_profile_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 14px;
            }
            """
        )
        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(14)

        # User avatar & name
        user_avatar = QLabel("👤")
        user_avatar.setStyleSheet("font-size: 20px;")
        layout.addWidget(user_avatar)

        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        self.username_label = QLabel()
        self.username_label.setStyleSheet("font-size: 13px; font-weight: 800; color: #0F172A;")
        user_info.addWidget(self.username_label)

        sub_user = QLabel("Player Profile")
        sub_user.setStyleSheet("font-size: 11px; color: #64748B;")
        user_info.addWidget(sub_user)
        layout.addLayout(user_info)

        # Edit username button
        self.edit_user_btn = QPushButton("✏️ Edit Name")
        self.edit_user_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_user_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #F8FAFC;
                color: #334155;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #EFF6FF; border-color: #93C5FD; color: #1D4ED8; }
            """
        )
        self.edit_user_btn.clicked.connect(self._prompt_edit_username)
        layout.addWidget(self.edit_user_btn)

        # Vertical divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.VLine)
        div.setStyleSheet("color: #E2E8F0; max-width: 1px; min-width: 1px;")
        layout.addWidget(div)

        # CM Greeting Pill
        self.cm_greeting_lbl = QLabel()
        self.cm_greeting_lbl.setWordWrap(True)
        self.cm_greeting_lbl.setStyleSheet(
            "font-size: 12px; color: #1E293B; font-weight: 600; line-height: 1.3;"
        )
        layout.addWidget(self.cm_greeting_lbl, 1)

        return card

    def _prompt_edit_username(self) -> None:
        current_name = self.profile_manager.get_username()
        new_name, ok = QInputDialog.getText(
            self,
            "Change Username",
            "Enter your player username:",
            text=current_name,
        )
        if ok and new_name.strip():
            clean = self.profile_manager.set_username(new_name)
            self.update_profile_ui()
            self.username_changed.emit(clean)

    def update_profile_ui(self) -> None:
        """Update username label and CM's personalized greeting."""
        username = self.profile_manager.get_username()
        self.username_label.setText(username)

        # Companion CM addresses the user warmly by name
        self.cm_greeting_lbl.setText(
            f"🤖 CM: \"Hey {username}! Welcome back to JD Chess. Ready to conquer the board or sharpen your tactics?\""
        )

        # Update Learn badge
        completed = len(self.profile_manager.get_profile().completed_lessons)
        self.learn_badge.setText(f"{completed} / 16 Mastered")

        # Update History rating badge
        rating = self.history_manager.get_rating()
        self.history_badge.setText(f"⭐ {rating} Rating")

    # -------------------------------------------------------------
    # Choice Cards
    # -------------------------------------------------------------
    def _create_card(
        self,
        title_text: str,
        desc_text: str,
        btn_text: str,
        btn_id: str,
        badge_text: str,
        badge_color: tuple[str, str, str],
        on_click,
        is_primary: bool = False,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("homeCard")
        card.setStyleSheet(
            """
            QFrame#homeCard {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 14px;
            }
            QFrame#homeCard:hover {
                border-color: #2563EB;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        fg, bg, border = badge_color
        top_row = QHBoxLayout()
        badge = QLabel(badge_text)
        badge.setStyleSheet(
            f"font-size: 11px; font-weight: 700; color: {fg}; "
            f"background-color: {bg}; border: 1px solid {border}; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel(title_text)
        card_title.setStyleSheet("font-size: 17px; font-weight: 800; color: #0F172A;")
        layout.addWidget(card_title)

        card_desc = QLabel(desc_text)
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #64748B; line-height: 1.4;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton(btn_text)
        btn.setObjectName(btn_id)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        if is_primary:
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #2563EB;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 9px;
                    padding: 8px 16px;
                    font-size: 13px;
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
                    border-radius: 9px;
                    padding: 8px 16px;
                    font-size: 13px;
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
        card.setObjectName("homeCard")
        card.setStyleSheet(
            """
            QFrame#homeCard {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 14px;
            }
            QFrame#homeCard:hover {
                border-color: #2563EB;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

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
        card_title.setStyleSheet("font-size: 17px; font-weight: 800; color: #0F172A;")
        layout.addWidget(card_title)

        card_desc = QLabel("Resume a saved match where you left off from one of your active slots.")
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #64748B; line-height: 1.4;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton("Continue Game →")
        btn.setObjectName("homeContinueGameBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #1E293B;
                border: 1.5px solid #CBD5E1;
                border-radius: 9px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #F8FAFC; border-color: #94A3B8; }
            QPushButton:pressed { background-color: #F1F5F9; }
            """
        )
        btn.clicked.connect(self.continue_game_clicked.emit)
        layout.addWidget(btn)

        return card, status_badge, btn

    def _create_learn_card(self) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("homeCard")
        card.setStyleSheet(
            """
            QFrame#homeCard {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 14px;
            }
            QFrame#homeCard:hover {
                border-color: #10B981;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        badge = QLabel("0 / 16 Mastered")
        badge.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #059669; "
            "background-color: #ECFDF5; border: 1px solid #A7F3D0; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel("Learn Chess with CM")
        card_title.setStyleSheet("font-size: 17px; font-weight: 800; color: #0F172A;")
        layout.addWidget(card_title)

        card_desc = QLabel("Interactive lessons guided by your AI buddy CM, from piece movements to pro tactics.")
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #64748B; line-height: 1.4;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton("Start Learning →")
        btn.setObjectName("homeLearnBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #10B981;
                color: #FFFFFF;
                border: none;
                border-radius: 9px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #059669; }
            QPushButton:pressed { background-color: #047857; }
            """
        )
        btn.clicked.connect(self.learn_chess_clicked.emit)
        layout.addWidget(btn)

        return card, badge

    def _create_history_card(self) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("homeCard")
        card.setStyleSheet(
            """
            QFrame#homeCard {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 14px;
            }
            QFrame#homeCard:hover {
                border-color: #8B5CF6;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        badge = QLabel("⭐ 1200 Rating")
        badge.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #7C3AED; "
            "background-color: #F5F3FF; border: 1px solid #DDD6FE; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel("History & Rating")
        card_title.setStyleSheet("font-size: 17px; font-weight: 800; color: #0F172A;")
        layout.addWidget(card_title)

        card_desc = QLabel("Explore past match logs across months, analyze win rates, and monitor Elo rating growth.")
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #64748B; line-height: 1.4;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton("View History →")
        btn.setObjectName("homeHistoryBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #1E293B;
                border: 1.5px solid #CBD5E1;
                border-radius: 9px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #F8FAFC; border-color: #94A3B8; }
            QPushButton:pressed { background-color: #F1F5F9; }
            """
        )
        btn.clicked.connect(self.history_clicked.emit)
        layout.addWidget(btn)

        return card, badge

    # -------------------------------------------------------------
    # State & Engine Badge
    # -------------------------------------------------------------
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
        self.update_profile_ui()
