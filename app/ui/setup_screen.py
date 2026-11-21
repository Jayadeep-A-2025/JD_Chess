from __future__ import annotations

"""Window 2: Game Setup & Configuration.
Styled in Warm Beige & Walnut theme: clean, elegant, minimal, and traditional.
"""

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QListView,
    QStyleFactory,
)

from app.ui.styles import PRIMARY_BTN, SECONDARY_BTN, checkbox_style, combo_style


class SetupScreen(QWidget):
    """Game Setup screen with mode, side, difficulty selection, and Start Game action."""

    start_game_clicked = Signal()
    back_to_menu_clicked = Signal()

    LOCAL_MODE = "Local 2-player"
    COMPUTER_MODE = "Play vs Computer"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QWidget { background-color: #F7F4EE; color: #241B16; }")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Scroll area for seamless mobile scaling
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setStyleSheet("QScrollArea { border: none; background-color: #F7F4EE; }")

        self._scroll_content = QWidget()
        self._scroll_content.setStyleSheet("background-color: #F7F4EE;")
        main_layout = QVBoxLayout(self._scroll_content)
        main_layout.setContentsMargins(18, 12, 18, 16)
        main_layout.setSpacing(10)

        # Top navigation bar
        top_bar = QHBoxLayout()
        self.back_button = QPushButton("← Back to Menu")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setMinimumHeight(40)
        self.back_button.setStyleSheet(SECONDARY_BTN)
        self.back_button.clicked.connect(self.back_to_menu_clicked.emit)
        top_bar.addWidget(self.back_button)
        top_bar.addStretch(1)
        main_layout.addLayout(top_bar)

        # Centered setup card container
        self.center_container = QWidget()
        self.center_container.setMaximumWidth(640)
        center_layout = QVBoxLayout(self.center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(10)

        # SETUP CARD - Warm Beige & Walnut
        self.setup_card = QFrame()
        self.setup_card.setObjectName("setupCard")
        self.setup_card.setStyleSheet(
            """
            QFrame#setupCard {
                background-color: #FFFFFF;
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            """
        )
        self.card_layout = QVBoxLayout(self.setup_card)
        self.card_layout.setContentsMargins(22, 16, 22, 16)
        self.card_layout.setSpacing(10)

        # Card Title
        card_title = QLabel("Game Configuration")
        card_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #241B16;")
        self.card_layout.addWidget(card_title)

        card_desc = QLabel("Set your opponent mode, board orientation, and computer difficulty level.")
        card_desc.setStyleSheet("font-size: 12px; color: #6E5D53; margin-bottom: 2px; font-weight: 400;")
        card_desc.setWordWrap(True)
        self.card_layout.addWidget(card_desc)

        style_sheet = combo_style()

        # 1. Mode Selection
        self.mode_label = QLabel("Game Mode")
        self.mode_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #241B16;")

        self.mode_combo = QComboBox()
        self.mode_combo.setStyle(QStyleFactory.create("Fusion"))
        self.mode_combo.setObjectName("modeCombo")
        self.mode_combo.setMinimumHeight(40)
        self.mode_combo.addItems([self.LOCAL_MODE, self.COMPUTER_MODE])
        self.mode_combo.setStyleSheet(style_sheet)
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)

        # 2. Side / Perspective Selection
        self.color_label = QLabel("Play As (Perspective)")
        self.color_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #241B16;")

        self.color_combo = QComboBox()
        self.color_combo.setStyle(QStyleFactory.create("Fusion"))
        self.color_combo.setObjectName("colorCombo")
        self.color_combo.setMinimumHeight(40)
        self.color_combo.addItems(["White", "Black"])
        self.color_combo.setCurrentText("White")
        self.color_combo.setStyleSheet(style_sheet)

        # 3. Computer Difficulty
        self.difficulty_label = QLabel("Computer Difficulty")
        self.difficulty_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #241B16;")

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.setStyle(QStyleFactory.create("Fusion"))
        self.difficulty_combo.setObjectName("difficultyCombo")
        self.difficulty_combo.setMinimumHeight(40)
        self.difficulty_combo.addItems(["Novice", "Easy", "Medium", "Hard"])
        self.difficulty_combo.setCurrentText("Novice")
        self.difficulty_combo.setStyleSheet(style_sheet)

        self.difficulty_hint = QLabel("(Select 'Play vs Computer' to activate difficulty)")
        self.difficulty_hint.setWordWrap(True)
        self.difficulty_hint.setStyleSheet("font-size: 11px; color: #8A6642; font-weight: 500;")

        # 4. Preferences & Toggles
        self.pref_label = QLabel("Match Preferences")
        self.pref_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #241B16;")

        cb_style = checkbox_style()
        self.sound_checkbox = QCheckBox("Sound Effects & Audio Cues")
        self.sound_checkbox.setObjectName("soundCheckbox")
        self.sound_checkbox.setChecked(True)
        self.sound_checkbox.setStyleSheet(cb_style)

        self.hints_checkbox = QCheckBox("Highlight Legal Moves & Captures")
        self.hints_checkbox.setObjectName("hintsCheckbox")
        self.hints_checkbox.setChecked(True)
        self.hints_checkbox.setStyleSheet(cb_style)

        # Form grid layout for responsive 2-column or 1-column adaptation
        self.form_grid = QGridLayout()
        self.form_grid.setSpacing(10)
        self._is_narrow_form = False
        self._build_form_layout(is_narrow=False)
        self.card_layout.addLayout(self.form_grid)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #E8E2D8; margin: 2px 0;")
        self.card_layout.addWidget(divider)

        # Start Game CTA
        self.start_game_button = QPushButton("Start Game →")
        self.start_game_button.setObjectName("setupStartGameBtn")
        self.start_game_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_game_button.setMinimumHeight(44)
        self.start_game_button.setStyleSheet(PRIMARY_BTN)
        self.start_game_button.clicked.connect(self.start_game_clicked.emit)
        self.card_layout.addWidget(self.start_game_button)

        center_layout.addWidget(self.setup_card)
        main_layout.addWidget(self.center_container, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(1)

        self._scroll.setWidget(self._scroll_content)
        outer_layout.addWidget(self._scroll)

        self._update_controls()

    def _build_form_layout(self, is_narrow: bool) -> None:
        """Arrange form into clean 2-column layout (desktop) or stacked (mobile)."""
        while self.form_grid.count():
            self.form_grid.takeAt(0)

        if is_narrow:
            self.form_grid.addWidget(self.mode_label, 0, 0)
            self.form_grid.addWidget(self.mode_combo, 1, 0)
            self.form_grid.addWidget(self.color_label, 2, 0)
            self.form_grid.addWidget(self.color_combo, 3, 0)
            self.form_grid.addWidget(self.difficulty_label, 4, 0)
            self.form_grid.addWidget(self.difficulty_combo, 5, 0)
            self.form_grid.addWidget(self.difficulty_hint, 6, 0)
            self.form_grid.addWidget(self.pref_label, 7, 0)
            self.form_grid.addWidget(self.sound_checkbox, 8, 0)
            self.form_grid.addWidget(self.hints_checkbox, 9, 0)
        else:
            # Row 0: Mode & Color labels
            self.form_grid.addWidget(self.mode_label, 0, 0)
            self.form_grid.addWidget(self.color_label, 0, 1)
            # Row 1: Mode & Color combos
            self.form_grid.addWidget(self.mode_combo, 1, 0)
            self.form_grid.addWidget(self.color_combo, 1, 1)
            # Row 2: Difficulty label & hint
            self.form_grid.addWidget(self.difficulty_label, 2, 0)
            self.form_grid.addWidget(self.difficulty_hint, 2, 1)
            # Row 3: Difficulty combo
            self.form_grid.addWidget(self.difficulty_combo, 3, 0)
            # Row 4: Preferences checkboxes side-by-side
            self.form_grid.addWidget(self.sound_checkbox, 4, 0)
            self.form_grid.addWidget(self.hints_checkbox, 4, 1)

        self._is_narrow_form = is_narrow

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        should_be_narrow = (self.width() < 560)
        if should_be_narrow != self._is_narrow_form:
            self._build_form_layout(is_narrow=should_be_narrow)

    def _on_mode_changed(self, _) -> None:
        self._update_controls()

    def _update_controls(self) -> None:
        is_comp = self.mode_combo.currentText() == self.COMPUTER_MODE
        self.difficulty_combo.setEnabled(is_comp)
        if is_comp:
            self.color_label.setText("Play As (Your Side)")
            self.difficulty_label.setStyleSheet(
                "font-size: 13px; font-weight: 600; color: #241B16;"
            )
            self.difficulty_hint.setText(
                "Skill: Easy (Skill 1) • Medium (Skill 8) • Hard (Skill 20)"
            )
            self.difficulty_hint.setStyleSheet(
                "font-size: 11px; color: #8A6642; font-weight: 500;"
            )
        else:
            self.color_label.setText("Play As (Perspective)")
            self.difficulty_label.setStyleSheet(
                "font-size: 13px; font-weight: 600; color: #A3907C;"
            )
            self.difficulty_hint.setText(
                "(Select 'Play vs Computer' to activate difficulty)"
            )
            self.difficulty_hint.setStyleSheet(
                "font-size: 11px; color: #B0A597;"
            )
