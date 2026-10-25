from __future__ import annotations

"""Window 2: Game Setup & Configuration."""

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

from app.ui.styles import checkbox_style, combo_style


class SetupScreen(QWidget):
    """Game Setup screen with mode, side, difficulty selection, and Start Game action."""

    start_game_clicked = Signal()
    back_to_menu_clicked = Signal()

    LOCAL_MODE = "Local 2-player"
    COMPUTER_MODE = "Play vs Computer"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QWidget { background-color: #F8FAFC; }")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Scroll area for seamless mobile scaling
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setStyleSheet("QScrollArea { border: none; background-color: #F8FAFC; }")

        self._scroll_content = QWidget()
        self._scroll_content.setStyleSheet("background-color: #F8FAFC;")
        main_layout = QVBoxLayout(self._scroll_content)
        main_layout.setContentsMargins(20, 20, 20, 30)
        main_layout.setSpacing(20)

        # Top navigation bar
        top_bar = QHBoxLayout()
        self.back_button = QPushButton("← Back to Menu")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setMinimumHeight(44)
        self.back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #334155;
                border: 1.5px solid #CBD5E1;
                border-radius: 8px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #F1F5F9; color: #0F172A; border-color: #94A3B8; }
            """
        )
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

        # SETUP CARD
        setup_card = QFrame()
        setup_card.setObjectName("setupCard")
        setup_card.setStyleSheet(
            """
            QFrame#setupCard {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 16px;
            }
            """
        )
        card_layout = QVBoxLayout(setup_card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(18)

        # Card Title
        card_title = QLabel("Game Configuration")
        card_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #0F172A;")
        card_layout.addWidget(card_title)

        card_desc = QLabel("Set your opponent mode, board orientation, and computer difficulty level.")
        card_desc.setStyleSheet("font-size: 13px; color: #64748B; margin-bottom: 6px;")
        card_desc.setWordWrap(True)
        card_layout.addWidget(card_desc)

        
        style_sheet = combo_style()

        # 1. Mode Selection
        mode_label = QLabel("Game Mode")
        mode_label.setStyleSheet(
            "font-size: 13px; font-weight: 700; color: #1E293B;"
        )
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
        self.color_label.setStyleSheet(
            "font-size: 13px; font-weight: 700; color: #1E293B;"
        )
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
        self.difficulty_label.setStyleSheet(
            "font-size: 13px; font-weight: 700; color: #1E293B;"
        )
        card_layout.addWidget(self.difficulty_label)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.setStyle(QStyleFactory.create("Fusion"))
        self.difficulty_combo.setObjectName("difficultyCombo")
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setCurrentText("Medium")
        self.difficulty_combo.setStyleSheet(style_sheet)
        card_layout.addWidget(self.difficulty_combo)


        self.difficulty_hint = QLabel("(Select 'Play vs Computer' to activate difficulty)")
        self.difficulty_hint.setWordWrap(True)
        self.difficulty_hint.setStyleSheet("font-size: 11px; color: #64748B;")
        card_layout.addWidget(self.difficulty_hint)

        # 4. Preferences & Toggles
        pref_label = QLabel("Match Preferences")
        pref_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #1E293B; margin-top: 4px;")
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
        divider.setStyleSheet("color: #E2E8F0; margin: 6px 0;")
        card_layout.addWidget(divider)

        # Start Game CTA
        self.start_game_button = QPushButton("Start Game →")
        self.start_game_button.setObjectName("setupStartGameBtn")
        self.start_game_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_game_button.setMinimumHeight(48)
        self.start_game_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2563EB;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #1D4ED8; }
            QPushButton:pressed { background-color: #1E40AF; }
            """
        )
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
                "font-size: 13px; font-weight: 700; color: #1E293B;"
            )
            self.difficulty_hint.setText(
                "Skill: Easy (Skill 1) • Medium (Skill 8) • Hard (Skill 20)"
            )
            self.difficulty_hint.setStyleSheet(
                "font-size: 11px; color: #0284C7; font-weight: 500;"
            )
        else:
            self.color_label.setText("Play As (Perspective)")
            self.difficulty_label.setStyleSheet(
                "font-size: 13px; font-weight: 700; color: #94A3B8;"
            )
            self.difficulty_hint.setText(
                "(Select 'Play vs Computer' to activate difficulty)"
            )
            self.difficulty_hint.setStyleSheet(
                "font-size: 11px; color: #64748B;"
            )
