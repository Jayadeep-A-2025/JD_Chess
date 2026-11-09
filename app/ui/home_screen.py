from __future__ import annotations

"""Window 1: Main Home Menu with User Profile, companion CM, and 4 primary options.
Redesigned in Warm Beige & Walnut theme: clean, elegant, minimal, and traditional.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.services.curriculum import get_curriculum
from app.services.history_manager import HistoryManager
from app.services.save_manager import SaveManager
from app.services.user_profile_manager import UserProfileManager
from app.ui.styles import PRIMARY_BTN, SECONDARY_BTN


class EditUsernameDialog(QDialog):
    """Refined, traditional dialog to edit custom username styled in Warm Beige & Walnut."""

    def __init__(self, current_name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Change Username")
        self.setModal(True)
        self.setMinimumWidth(320)
        self.setMaximumWidth(420)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #F7F4EE;
                color: #241B16;
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Edit Player Name")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #241B16;")
        layout.addWidget(title)

        desc = QLabel("Enter your username for companion CM dialogues and match records:")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 12px; color: #6E5D53; font-weight: 400;")
        layout.addWidget(desc)

        self.input_field = QLineEdit()
        self.input_field.setText(current_name)
        self.input_field.selectAll()
        self.input_field.setMinimumHeight(40)
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                background-color: #FFFFFF;
                color: #241B16;
                border: 1px solid #DCD5CA;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: 500;
            }
            QLineEdit:focus {
                border: 1.5px solid #4A3525;
            }
            """
        )
        layout.addWidget(self.input_field)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setMinimumHeight(38)
        self.cancel_btn.setStyleSheet(SECONDARY_BTN)
        self.cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.cancel_btn)

        self.save_btn = QPushButton("Save Name")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setMinimumHeight(38)
        self.save_btn.setStyleSheet(PRIMARY_BTN)
        self.save_btn.clicked.connect(self.accept)
        btn_row.addWidget(self.save_btn)

        self.cancel_button = self.cancel_btn
        self.save_button = self.save_btn

        layout.addLayout(btn_row)

    def get_username(self) -> str:
        username = self.input_field.text().strip()
        return username if username else "Grandmaster"


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
        self._is_mobile_grid = False

        self.setStyleSheet("QWidget { background-color: #F7F4EE; color: #241B16; }")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Scroll area wrapping all home content for small screen / mobile adaptability
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("QScrollArea { background-color: #F7F4EE; border: none; }")
        self.scroll_area.viewport().setStyleSheet("background-color: #F7F4EE;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #F7F4EE;")
        main_layout = QVBoxLayout(self.scroll_content)
        main_layout.setContentsMargins(24, 20, 24, 24)
        main_layout.setSpacing(18)

        # -------------------------------------------------------------
        # TOP BAR: User Profile & Companion CM Greeting
        # -------------------------------------------------------------
        profile_card = self._build_profile_card()
        main_layout.addWidget(profile_card)

        # Centered container for max width aesthetics on desktop
        self.center_container = QWidget()
        self.center_container.setStyleSheet("background: transparent;")
        self.center_container.setMaximumWidth(780)
        center_layout = QVBoxLayout(self.center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(16)

        # HERO HEADER: App Title & Status
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(6)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_lbl = QLabel("JD CHESS")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet(
            "font-size: 26px; font-weight: 800; color: #241B16; letter-spacing: 2px;"
        )
        hero_layout.addWidget(title_lbl)

        sub_lbl = QLabel("A Classical Desktop Chess Studio & Companion")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_lbl.setStyleSheet("font-size: 13px; color: #6E5D53; font-weight: 500;")
        hero_layout.addWidget(sub_lbl)

        # Engine Status Pill
        self.engine_badge = QLabel()
        self.engine_badge.setObjectName("engineStatusPill")
        self.engine_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_engine_status(self.engine_ready, self.engine_path)
        hero_layout.addWidget(self.engine_badge, 0, Qt.AlignmentFlag.AlignCenter)

        center_layout.addLayout(hero_layout)

        # -------------------------------------------------------------
        # 4 PRIMARY CHOICES (Responsive Grid)
        # -------------------------------------------------------------
        self.grid = QGridLayout()
        self.grid.setSpacing(14)

        # 1. NEW GAME
        self.new_game_card = self._create_card(
            title_text="New Game",
            desc_text="Start a fresh match with custom rules, side perspective, and computer difficulty.",
            btn_text="New Game →",
            btn_id="homeNewGameBtn",
            badge_text="Fresh Match",
            badge_color=("#4A3525", "#EFEBE3", "#DCD5CA"),
            on_click=self.new_game_clicked.emit,
            is_primary=True,
        )

        # 2. CONTINUE GAME
        self.continue_game_card, self.save_status_badge, self.continue_btn = (
            self._create_continue_card()
        )

        # 3. LEARN CHESS (with CM)
        self.learn_card, self.learn_badge = self._create_learn_card()

        # 4. MATCH HISTORY & RATING
        self.history_card, self.history_badge = self._create_history_card()

        self._apply_grid_layout(is_mobile=False)
        center_layout.addLayout(self.grid)

        # FOOTER INFO
        footer_lbl = QLabel(
            "AI Companion CM • 3 Active Save Slots • Offline Match Analysis & Elo Rating"
        )
        footer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_lbl.setWordWrap(True)
        footer_lbl.setStyleSheet("font-size: 11px; color: #8C8276; font-weight: 500; margin-top: 8px;")
        center_layout.addWidget(footer_lbl)

        main_layout.addWidget(self.center_container, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_content)
        root_layout.addWidget(self.scroll_area)

        self.update_save_status()
        self.update_profile_ui()

    # -------------------------------------------------------------
    # Responsive Grid Layout for Mobile & Desktop
    # -------------------------------------------------------------
    def _apply_grid_layout(self, is_mobile: bool) -> None:
        """Dynamically re-layout 4 cards into 1 column (mobile) or 2x2 (desktop)."""
        while self.grid.count():
            self.grid.takeAt(0)

        if is_mobile:
            self.grid.addWidget(self.new_game_card, 0, 0)
            self.grid.addWidget(self.continue_game_card, 1, 0)
            self.grid.addWidget(self.learn_card, 2, 0)
            self.grid.addWidget(self.history_card, 3, 0)
        else:
            self.grid.addWidget(self.new_game_card, 0, 0)
            self.grid.addWidget(self.continue_game_card, 0, 1)
            self.grid.addWidget(self.learn_card, 1, 0)
            self.grid.addWidget(self.history_card, 1, 1)

        self._is_mobile_grid = is_mobile
        self._grid_columns = 1 if is_mobile else 2

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        w = self.width()
        should_be_mobile = (w < 640)
        if should_be_mobile != self._is_mobile_grid:
            self._apply_grid_layout(is_mobile=should_be_mobile)

    # -------------------------------------------------------------
    # Profile & CM Header Card
    # -------------------------------------------------------------
    def _build_profile_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            """
        )
        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(14)

        # User avatar & name
        user_avatar = QLabel("👤")
        user_avatar.setStyleSheet("font-size: 22px; background-color: #EFEBE3; border-radius: 16px; padding: 4px;")
        layout.addWidget(user_avatar)

        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        self.username_label = QLabel()
        self.username_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #241B16;")
        user_info.addWidget(self.username_label)

        sub_user = QLabel("Player Profile")
        sub_user.setStyleSheet("font-size: 11px; color: #6E5D53; font-weight: 500;")
        user_info.addWidget(sub_user)
        layout.addLayout(user_info)

        # Edit username button (Touch-friendly 38px height)
        self.edit_user_btn = QPushButton("✏️ Edit Name")
        self.edit_user_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_user_btn.setMinimumHeight(38)
        self.edit_user_btn.setStyleSheet(SECONDARY_BTN)
        self.edit_user_btn.clicked.connect(self._prompt_edit_username)
        layout.addWidget(self.edit_user_btn)

        # Vertical divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.VLine)
        div.setStyleSheet("color: #DCD5CA; max-width: 1px; min-width: 1px;")
        layout.addWidget(div)

        # CM Greeting Pill
        self.cm_greeting_lbl = QLabel()
        self.cm_greeting_lbl.setWordWrap(True)
        self.cm_greeting_lbl.setStyleSheet(
            "font-size: 13px; color: #3D2B1F; font-weight: 500; line-height: 1.4; "
            "background-color: #F7F4EE; border: 1px solid #E8E2D8; border-radius: 8px; padding: 6px 12px;"
        )
        layout.addWidget(self.cm_greeting_lbl, 1)

        return card

    def _prompt_edit_username(self) -> None:
        current_name = self.profile_manager.get_username()
        dlg = EditUsernameDialog(current_name, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_name = dlg.get_username()
            if new_name:
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
        total_lessons = len(get_curriculum())
        completed = len(self.profile_manager.get_profile().completed_lessons)
        self.learn_badge.setText(f"{completed} / {total_lessons} Mastered")

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
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            QFrame#homeCard:hover {
                border-color: #8A6642;
                background-color: #FCFAF7;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        fg, bg, border = badge_color
        top_row = QHBoxLayout()
        badge = QLabel(badge_text)
        badge.setStyleSheet(
            f"font-size: 11px; font-weight: 600; color: {fg}; "
            f"background-color: {bg}; border: 1px solid {border}; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel(title_text)
        card_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #241B16;")
        layout.addWidget(card_title)

        card_desc = QLabel(desc_text)
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #6E5D53; line-height: 1.45; font-weight: 400;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton(btn_text)
        btn.setObjectName(btn_id)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        if is_primary:
            btn.setStyleSheet(PRIMARY_BTN)
        else:
            btn.setStyleSheet(SECONDARY_BTN)
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
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            QFrame#homeCard:hover {
                border-color: #8A6642;
                background-color: #FCFAF7;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        status_badge = QLabel("0 / 3 Slots")
        status_badge.setObjectName("saveStatusBadge")
        status_badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #4A3525; "
            "background-color: #EFEBE3; border: 1px solid #DCD5CA; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(status_badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel("Continue Game")
        card_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #241B16;")
        layout.addWidget(card_title)

        card_desc = QLabel("Resume a saved match where you left off from one of your active slots.")
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #6E5D53; line-height: 1.45; font-weight: 400;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton("Continue Game →")
        btn.setObjectName("homeContinueGameBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(SECONDARY_BTN)
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
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            QFrame#homeCard:hover {
                border-color: #8A6642;
                background-color: #FCFAF7;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        total_lessons = len(get_curriculum())
        badge = QLabel(f"0 / {total_lessons} Mastered")
        badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #3F6E4D; "
            "background-color: #EFEBE3; border: 1px solid #C8D6C7; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel("Learn Chess with CM")
        card_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #241B16;")
        layout.addWidget(card_title)

        card_desc = QLabel("Interactive lessons guided by your AI buddy CM, from piece movements to pro tactics.")
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #6E5D53; line-height: 1.45; font-weight: 400;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton("Start Learning →")
        btn.setObjectName("homeLearnBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(PRIMARY_BTN)
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
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            QFrame#homeCard:hover {
                border-color: #8A6642;
                background-color: #FCFAF7;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        badge = QLabel("⭐ 1200 Rating")
        badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #8A6642; "
            "background-color: #EFEBE3; border: 1px solid #DCD5CA; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        card_title = QLabel("Match History & Analytics")
        card_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #241B16;")
        layout.addWidget(card_title)

        card_desc = QLabel("Review past games, win rates, opening patterns, and track your Elo rating progression.")
        card_desc.setWordWrap(True)
        card_desc.setStyleSheet("font-size: 12px; color: #6E5D53; line-height: 1.45; font-weight: 400;")
        layout.addWidget(card_desc)

        layout.addStretch(1)

        btn = QPushButton("View History →")
        btn.setObjectName("homeHistoryBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(SECONDARY_BTN)
        btn.clicked.connect(self.history_clicked.emit)
        layout.addWidget(btn)

        return card, badge

    def update_save_status(self) -> None:
        """Query SaveManager and update Continue Game card availability."""
        active_count = self.save_manager.active_save_count()
        self.save_status_badge.setText(f"{active_count} / 3 Slots Active")

        if active_count > 0:
            self.continue_btn.setEnabled(True)
            self.continue_btn.setText(f"Continue Game ({active_count} Active) →")
            self.continue_btn.setStyleSheet(PRIMARY_BTN)
        else:
            self.continue_btn.setEnabled(False)
            self.continue_btn.setText("Continue Game")
            self.continue_btn.setStyleSheet(SECONDARY_BTN)

    def set_engine_status(self, ready: bool, path: str | None = None) -> None:
        self.engine_ready = ready
        self.engine_path = path

        if ready:
            self.engine_badge.setText("● Computer Active")
            self.engine_badge.setStyleSheet(
                "color: #3F6E4D; background-color: #EFEBE3; "
                "border: 1px solid #C8D6C7; border-radius: 12px; "
                "font-size: 11px; font-weight: 600; padding: 4px 12px;"
            )
        else:
            self.engine_badge.setText("○ Computer Standby")
            self.engine_badge.setStyleSheet(
                "color: #8C8276; background-color: #EFEBE3; "
                "border: 1px solid #DCD5CA; border-radius: 12px; "
                "font-size: 11px; font-weight: 600; padding: 4px 12px;"
            )
