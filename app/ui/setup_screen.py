from __future__ import annotations

"""Window 2: Game Setup & Configuration.
Styled in Royal Gold & Luxury Mahogany theme.
"""

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
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
        self.setStyleSheet("QWidget { background-color: #1E130B; color: #FDFBF7; }")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Scroll area for seamless mobile scaling
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setStyleSheet("QScrollArea { border: none; background-color: #1E130B; }")

        self._scroll_content = QWidget()
        self._scroll_content.setStyleSheet("background-color: #1E130B;")
        main_layout = QVBoxLayout(self._scroll_content)
        main_layout.setContentsMargins(20, 20, 20, 30)
        main_layout.setSpacing(20)

        # Top navigation bar
        top_bar = QHBoxLayout()
        self.back_button = QPushButton("← Back to Menu")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setMinimumHeight(44)
        self.back_button.setStyleSheet(SECONDARY_BTN)
        self.back_button.clicked.connect(self.back_to_menu_clicked.emit)
        top_bar.addWidget(self.back_button)
        top_bar.addStretch(1)
        main_layout.addLayout(top_bar)

        # Centered setup card container
        center_container = QWidget()
        center_container.setMaximumWidth(540)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(20)

        # SETUP CARD - Luxury Mahogany & Royal Gold
        setup_card = QFrame()
        setup_card.setObjectName("setupCard")
        setup_card.setStyleSheet(
            """
            QFrame#setupCard {
                background-color: #2A1B12;
                border: 1.5px solid #D97706;
                border-radius: 18px;
            }
            """
        )
        card_layout = QVBoxLayout(setup_card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(18)

        # Card Title
        card_title = QLabel("Game Configuration")
        card_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #FDFBF7;")
        card_layout.addWidget(card_title)

        card_desc = QLabel("Set your opponent mode, board orientation, and computer difficulty level.")
        card_desc.setStyleSheet("font-size: 13px; color: #D97706; margin-bottom: 6px; font-weight: 500;")
        card_desc.setWordWrap(True)
        card_layout.addWidget(card_desc)

        style_sheet = combo_style()

        # 1. Mode Selection
        mode_label = QLabel("Game Mode")
        mode_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #FDFBF7;")
        card_layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.setStyle(QStyleFactory.create("Fusion"))
        self.mode_combo.setObjectName("modeCombo")
        self.mode_combo.addItems([self.LOCAL_MODE, self.COMPUTER_MODE])
        self.mode_combo.setStyleSheet(style_sheet)
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        card_layout.addWidget(self.mode_combo)

        # 2. Side / Perspective Selection
        self.color_label = QLabel("Play As (Perspective)")
        self.color_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #FDFBF7;")
        card_layout.addWidget(self.color_label)

        self.color_combo = QComboBox()
        self.color_combo.setStyle(QStyleFactory.create("Fusion"))
        self.color_combo.setObjectName("colorCombo")
        self.color_combo.addItems(["White", "Black"])
        self.color_combo.setCurrentText("White")
        self.color_combo.setStyleSheet(style_sheet)
        card_layout.addWidget(self.color_combo)

        # 3. Computer Difficulty
        self.difficulty_label = QLabel("Computer Difficulty")
        self.difficulty_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #FDFBF7;")
        card_layout.addWidget(self.difficulty_label)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.setStyle(QStyleFactory.create("Fusion"))
        self.difficulty_combo.setObjectName("difficultyCombo")
        self.difficulty_combo.addItems(["Novice", "Easy", "Medium", "Hard"])
        self.difficulty_combo.setCurrentText("Novice")
        self.difficulty_combo.setStyleSheet(style_sheet)
        card_layout.addWidget(self.difficulty_combo)

        self.difficulty_hint = QLabel("(Select 'Play vs Computer' to activate difficulty)")
        self.difficulty_hint.setWordWrap(True)
        self.difficulty_hint.setStyleSheet("font-size: 11px; color: #D97706; font-weight: 500;")
        card_layout.addWidget(self.difficulty_hint)

        # 4. Preferences & Toggles
        pref_label = QLabel("Match Preferences")
        pref_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #FDFBF7; margin-top: 4px;")
        card_layout.addWidget(pref_label)

        cb_style = checkbox_style()
        self.sound_checkbox = QCheckBox("Sound Effects & Audio Cues")
        self.sound_checkbox.setObjectName("soundCheckbox")
        self.sound_checkbox.setChecked(True)
        self.sound_checkbox.setStyleSheet(cb_style)
        card_layout.addWidget(self.sound_checkbox)

        self.hints_checkbox = QCheckBox("Highlight Legal Moves & Captures")
        self.hints_checkbox.setObjectName("hintsCheckbox")
        self.hints_checkbox.setChecked(True)
        self.hints_checkbox.setStyleSheet(cb_style)
        card_layout.addWidget(self.hints_checkbox)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: rgba(217, 119, 6, 0.35); margin: 6px 0;")
        card_layout.addWidget(divider)

        # Start Game CTA
        self.start_game_button = QPushButton("Start Game →")
        self.start_game_button.setObjectName("setupStartGameBtn")
        self.start_game_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_game_button.setMinimumHeight(48)
        self.start_game_button.setStyleSheet(PRIMARY_BTN)
        self.start_game_button.clicked.connect(self.start_game_clicked.emit)
        card_layout.addWidget(self.start_game_button)

        center_layout.addWidget(setup_card)
        main_layout.addWidget(center_container, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(2)

        self._scroll.setWidget(self._scroll_content)
        outer_layout.addWidget(self._scroll)

        self._update_controls()

    def _on_mode_changed(self, _) -> None:
        self._update_controls()

    def _update_controls(self) -> None:
        is_comp = self.mode_combo.currentText() == self.COMPUTER_MODE
        self.difficulty_combo.setEnabled(is_comp)
        if is_comp:
            self.color_label.setText("Play As (Your Side)")
            self.difficulty_label.setStyleSheet(
                "font-size: 13px; font-weight: 700; color: #FDFBF7;"
            )
            self.difficulty_hint.setText(
                "Skill: Easy (Skill 1) • Medium (Skill 8) • Hard (Skill 20)"
            )
            self.difficulty_hint.setStyleSheet(
                "font-size: 11px; color: #D97706; font-weight: 600;"
            )
        else:
            self.color_label.setText("Play As (Perspective)")
            self.difficulty_label.setStyleSheet(
                "font-size: 13px; font-weight: 700; color: rgba(253, 251, 247, 0.4);"
            )
            self.difficulty_hint.setText(
                "(Select 'Play vs Computer' to activate difficulty)"
            )
            self.difficulty_hint.setStyleSheet(
                "font-size: 11px; color: rgba(217, 119, 6, 0.5);"
            )
