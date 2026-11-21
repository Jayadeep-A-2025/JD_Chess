from __future__ import annotations

"""Window: Learn Chess Module featuring AI companion 'CM' (Chess Mate) with responsive mobile layout,
interactive learning modes (Practice Challenge, Grandmaster Theory, Guided Demonstration, Concept Assessment),
multi-tier progressive hints, rich mistake analysis, threat detection, and structured 7-level curriculum navigation.
Styled in Warm Beige & Walnut theme: clean, elegant, minimal, and traditional.
"""

import chess
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

from app.core.chess_game import ChessGame
from app.services.curriculum import (
    CURRICULUM,
    Lesson,
    get_curriculum,
    get_lesson_by_id,
    get_next_lesson,
    get_prev_lesson,
)
from app.services.user_profile_manager import UserProfileManager
from app.ui.chessboard_widget import ChessBoardWidget
from app.ui.styles import (
    ACCENT_BTN,
    PRIMARY_BTN,
    SECONDARY_BTN,
    TAB_ACTIVE_BTN,
    TAB_INACTIVE_BTN,
)


class LearnScreen(QWidget):
    """Interactive learning academy guided step-by-step by companion CM."""

    main_menu_clicked = Signal()

    def __init__(
        self,
        profile_manager: UserProfileManager,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.profile_manager = profile_manager
        self.profile_manager.migrate_progress()
        self.curriculum = get_curriculum()

        # Dedicated isolated game instance for interactive puzzles
        self.game = ChessGame()
        self.current_lesson: Lesson = self._initial_lesson()
        self.is_lesson_solved: bool = False
        self._is_narrow_layout = False
        self._hint_tier: int = 0
        self._current_mode: str = "challenge"  # "challenge" | "theory" | "demo" | "assessment"
        self._selected_level_filter: int = 0   # 0 = All Levels, 1..7 = Level 1..7

        self.setStyleSheet("QWidget { background-color: #F7F4EE; color: #241B16; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Main scrollable area for mobile responsiveness
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("QScrollArea { background-color: #F7F4EE; border: none; }")
        self.scroll_area.viewport().setStyleSheet("background-color: #F7F4EE;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #F7F4EE;")
        main_vbox = QVBoxLayout(self.scroll_content)
        main_vbox.setContentsMargins(16, 14, 16, 16)
        main_vbox.setSpacing(12)

        # -------------------------------------------------------------
        # 1. TOP BAR
        # -------------------------------------------------------------
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.back_button = QPushButton("← Main Menu")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setMinimumHeight(38)
        self.back_button.setStyleSheet(SECONDARY_BTN)
        self.back_button.clicked.connect(self.main_menu_clicked.emit)
        top_bar.addWidget(self.back_button)

        title_lbl = QLabel("JD Chess Academy")
        title_lbl.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #241B16; letter-spacing: 0.3px;"
        )
        top_bar.addWidget(title_lbl)

        self.cm_status_pill = QLabel("🤖 CM: Online")
        self.cm_status_pill.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #3F6E4D; "
            "background-color: #EFEBE3; border: 1px solid #C8D6C7; "
            "border-radius: 10px; padding: 4px 10px;"
        )
        top_bar.addWidget(self.cm_status_pill)

        self.accuracy_pill = QLabel("🎯 Accuracy: 100%")
        self.accuracy_pill.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #5C4A3E; "
            "background-color: #EFEBE3; border: 1px solid #DCD5CA; "
            "border-radius: 10px; padding: 4px 10px;"
        )
        top_bar.addWidget(self.accuracy_pill)

        top_bar.addStretch(1)

        self.progress_pill = QLabel()
        self.progress_pill.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #4A3525; "
            "background-color: #EFEBE3; border: 1px solid #DCD5CA; "
            "border-radius: 10px; padding: 4px 12px;"
        )
        top_bar.addWidget(self.progress_pill)

        main_vbox.addLayout(top_bar)

        # -------------------------------------------------------------
        # 2. MAIN SPLIT LAYOUT (Left: Board + CM, Right: Curriculum Sidebar)
        # -------------------------------------------------------------
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background: transparent;")
        self.content_layout = QHBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 4, 0, 4)
        self.content_layout.setSpacing(16)

        # --- LEFT COLUMN: Mode Tabs, CM Dialogue, Board / Quiz, Actions, Theory ---
        self.left_col = QWidget()
        self.left_col_layout = QVBoxLayout(self.left_col)
        self.left_col_layout.setContentsMargins(0, 0, 0, 0)
        self.left_col_layout.setSpacing(10)

        # Mode Selection Bar (Challenge vs Theory vs Demonstration vs Assessment)
        mode_bar = QHBoxLayout()
        mode_bar.setSpacing(8)

        self.mode_challenge_btn = QPushButton("🎯 Practice Challenge")
        self.mode_challenge_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_challenge_btn.setMinimumHeight(36)
        self.mode_challenge_btn.clicked.connect(lambda: self._set_learning_mode("challenge"))
        mode_bar.addWidget(self.mode_challenge_btn)

        self.mode_theory_btn = QPushButton("📖 Grandmaster Theory")
        self.mode_theory_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_theory_btn.setMinimumHeight(36)
        self.mode_theory_btn.clicked.connect(lambda: self._set_learning_mode("theory"))
        mode_bar.addWidget(self.mode_theory_btn)

        self.mode_demo_btn = QPushButton("🎬 Guided Demonstration")
        self.mode_demo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_demo_btn.setMinimumHeight(36)
        self.mode_demo_btn.clicked.connect(lambda: self._set_learning_mode("demo"))
        mode_bar.addWidget(self.mode_demo_btn)

        self.mode_assessment_btn = QPushButton("📝 Concept Assessment")
        self.mode_assessment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_assessment_btn.setMinimumHeight(36)
        self.mode_assessment_btn.clicked.connect(lambda: self._set_learning_mode("assessment"))
        mode_bar.addWidget(self.mode_assessment_btn)

        mode_bar.addStretch(1)
        self.left_col_layout.addLayout(mode_bar)

        # CM Companion Speech Card
        self.cm_card = self._build_cm_speech_card()
        self.left_col_layout.addWidget(self.cm_card)

        # Interactive Board Container
        self.board_container = QWidget()
        self.board_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        board_box = QVBoxLayout(self.board_container)
        board_box.setContentsMargins(0, 0, 0, 0)

        self.board_widget = ChessBoardWidget(game=self.game, parent=self)
        self.board_widget.setMinimumSize(280, 280)
        self.board_widget.move_made.connect(self._on_user_board_move)
        board_box.addWidget(self.board_widget)
        self.left_col_layout.addWidget(self.board_container, 1)

        # Conceptual Assessment Quiz Container (Used in Assessment Mode)
        self.quiz_card = self._build_quiz_card()
        self.quiz_card.setVisible(False)
        self.left_col_layout.addWidget(self.quiz_card, 1)

        # Action bar under board (Hint, Demo, Reset, Prev, Next)
        self.actions_bar_widget = QWidget()
        actions_bar = QHBoxLayout(self.actions_bar_widget)
        actions_bar.setContentsMargins(0, 0, 0, 0)
        actions_bar.setSpacing(8)

        self.hint_btn = QPushButton("💡 Ask CM for Hint")
        self.hint_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hint_btn.setMinimumHeight(40)
        self.hint_btn.setStyleSheet(SECONDARY_BTN)
        self.hint_btn.clicked.connect(self._show_hint)
        actions_bar.addWidget(self.hint_btn)

        self.action_demo_btn = QPushButton("🎬 Demonstrate")
        self.action_demo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_demo_btn.setMinimumHeight(40)
        self.action_demo_btn.setStyleSheet(ACCENT_BTN)
        self.action_demo_btn.clicked.connect(self._demonstrate_move)
        actions_bar.addWidget(self.action_demo_btn)

        self.reset_btn = QPushButton("↺ Reset Board")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setMinimumHeight(40)
        self.reset_btn.setStyleSheet(SECONDARY_BTN)
        self.reset_btn.clicked.connect(self._reset_current_lesson)
        actions_bar.addWidget(self.reset_btn)

        actions_bar.addStretch(1)

        self.prev_btn = QPushButton("← Prev")
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.setMinimumHeight(40)
        self.prev_btn.setStyleSheet(SECONDARY_BTN)
        self.prev_btn.clicked.connect(self._go_prev_lesson)
        actions_bar.addWidget(self.prev_btn)

        self.next_btn = QPushButton("Next →")
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setMinimumHeight(40)
        self.next_btn.setStyleSheet(PRIMARY_BTN)
        self.next_btn.clicked.connect(self._go_next_lesson)
        actions_bar.addWidget(self.next_btn)

        self.left_col_layout.addWidget(self.actions_bar_widget)

        # Grandmaster Educational Theory Note
        self.note_card = QFrame()
        self.note_card.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border: 1px solid #DCD5CA; border-radius: 12px; }"
        )
        note_layout = QVBoxLayout(self.note_card)
        note_layout.setContentsMargins(16, 12, 16, 12)
        note_layout.setSpacing(6)

        note_top_row = QHBoxLayout()
        self.note_header = QLabel("📖 Grandmaster Insight & Strategy")
        self.note_header.setStyleSheet("font-size: 13px; font-weight: 700; color: #4A3525;")
        note_top_row.addWidget(self.note_header)
        note_top_row.addStretch(1)

        self.theory_mode_badge = QLabel("Practice Mode")
        self.theory_mode_badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #8A6642; "
            "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
        )
        note_top_row.addWidget(self.theory_mode_badge)
        note_layout.addLayout(note_top_row)

        self.note_text = QLabel()
        self.note_text.setWordWrap(True)
        self.note_text.setStyleSheet("font-size: 12px; color: #241B16; line-height: 1.45; font-weight: 400;")
        note_layout.addWidget(self.note_text)

        self.theory_deep_dive_lbl = QLabel()
        self.theory_deep_dive_lbl.setWordWrap(True)
        self.theory_deep_dive_lbl.setStyleSheet(
            "font-size: 12px; color: #241B16; line-height: 1.45; font-weight: 400; "
            "background-color: #F7F4EE; border-left: 3px solid #8A6642; padding: 8px 12px; border-radius: 4px;"
        )
        self.theory_deep_dive_lbl.setVisible(False)
        note_layout.addWidget(self.theory_deep_dive_lbl)

        self.real_app_lbl = QLabel()
        self.real_app_lbl.setWordWrap(True)
        self.real_app_lbl.setStyleSheet(
            "font-size: 11px; color: #3F6E4D; font-style: italic; line-height: 1.4; "
            "background-color: #F0F4EE; border: 1px solid #D2E0CE; padding: 6px 10px; border-radius: 6px; margin-top: 4px;"
        )
        self.real_app_lbl.setVisible(False)
        note_layout.addWidget(self.real_app_lbl)

        self.left_col_layout.addWidget(self.note_card)

        # --- RIGHT COLUMN: Curriculum Navigation Sidebar ---
        self.right_sidebar = self._build_curriculum_sidebar()

        self._set_responsive_layout(is_narrow=False)

        main_vbox.addWidget(self.content_container, 1)
        self.scroll_area.setWidget(self.scroll_content)
        root.addWidget(self.scroll_area)

        # Set default challenge mode buttons styling
        self._update_mode_buttons_ui()

        # Load initial lesson
        self.load_lesson(self.current_lesson)

    # -------------------------------------------------------------
    # Responsive Layout Switching (Desktop vs Mobile)
    # -------------------------------------------------------------
    def _set_responsive_layout(self, is_narrow: bool) -> None:
        self.content_layout.removeWidget(self.left_col)
        self.content_layout.removeWidget(self.right_sidebar)

        if is_narrow:
            QWidget().setLayout(self.content_layout)
            self.content_layout = QVBoxLayout(self.content_container)
            self.content_layout.setContentsMargins(0, 0, 0, 0)
            self.content_layout.setSpacing(14)

            self.right_sidebar.setMinimumWidth(0)
            self.content_layout.addWidget(self.left_col)
            self.content_layout.addWidget(self.right_sidebar)
        else:
            QWidget().setLayout(self.content_layout)
            self.content_layout = QHBoxLayout(self.content_container)
            self.content_layout.setContentsMargins(0, 0, 0, 0)
            self.content_layout.setSpacing(18)

            self.right_sidebar.setMinimumWidth(320)
            self.content_layout.addWidget(self.left_col, 3)
            self.content_layout.addWidget(self.right_sidebar, 1)

        self._is_narrow_layout = is_narrow

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        w = self.width()
        should_be_narrow = (w < 840)
        if should_be_narrow != self._is_narrow_layout:
            self._set_responsive_layout(should_be_narrow)

    # -------------------------------------------------------------
    # UI Component Builders
    # -------------------------------------------------------------
    def _build_cm_speech_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("cmSpeechCard")
        card.setStyleSheet(
            """
            QFrame#cmSpeechCard {
                background-color: #FFFFFF;
                border: 1px solid #DCD5CA;
                border-radius: 12px;
            }
            """
        )
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(14)

        # Avatar
        avatar = QLabel("🤖")
        avatar.setFixedSize(44, 44)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "font-size: 22px; background-color: #EFEBE3; "
            "border: 1px solid #DCD5CA; border-radius: 22px;"
        )
        layout.addWidget(avatar, 0, Qt.AlignmentFlag.AlignTop)

        # Text column
        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        top_row = QHBoxLayout()
        self.cm_name_lbl = QLabel("CM (Chess Mate) • Academy Coach")
        self.cm_name_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #4A3525;")
        top_row.addWidget(self.cm_name_lbl)

        self.lesson_badge = QLabel("Level 1")
        self.lesson_badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #6E5D53; "
            "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(self.lesson_badge)

        self.turn_badge = QLabel("White to Move")
        self.turn_badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #241B16; "
            "background-color: #F7F4EE; border: 1px solid #E8E2D8; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(self.turn_badge)

        top_row.addStretch(1)
        text_col.addLayout(top_row)

        self.cm_dialogue_lbl = QLabel()
        self.cm_dialogue_lbl.setWordWrap(True)
        self.cm_dialogue_lbl.setStyleSheet("font-size: 13px; color: #241B16; line-height: 1.45;")
        text_col.addWidget(self.cm_dialogue_lbl)

        self.cm_objective_lbl = QLabel()
        self.cm_objective_lbl.setWordWrap(True)
        self.cm_objective_lbl.setStyleSheet(
            "font-size: 12px; font-weight: 600; color: #8A6642; margin-top: 2px;"
        )
        text_col.addWidget(self.cm_objective_lbl)

        # Threat Detection Pill
        self.cm_threat_lbl = QLabel()
        self.cm_threat_lbl.setWordWrap(True)
        self.cm_threat_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #8A3822; "
            "background-color: #FDF3E8; border: 1px solid #E6D0BE; "
            "border-radius: 6px; padding: 4px 8px; margin-top: 3px;"
        )
        self.cm_threat_lbl.setVisible(False)
        text_col.addWidget(self.cm_threat_lbl)

        layout.addLayout(text_col, 1)
        return card

    def _build_quiz_card(self) -> QFrame:
        """Card for conceptual assessment questions with interactive choice options."""
        card = QFrame()
        card.setObjectName("quizCard")
        card.setStyleSheet(
            """
            QFrame#quizCard {
                background-color: #FFFFFF;
                border: 1px solid #DCD5CA;
                border-radius: 12px;
                padding: 16px;
            }
            """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        quiz_title = QLabel("📝 Conceptual Academy Assessment")
        quiz_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #4A3525;")
        header_row.addWidget(quiz_title)
        header_row.addStretch(1)

        self.quiz_status_badge = QLabel("Active Quiz")
        self.quiz_status_badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #3F6E4D; "
            "background-color: #EFEBE3; border: 1px solid #C8D6C7; border-radius: 6px; padding: 2px 8px;"
        )
        header_row.addWidget(self.quiz_status_badge)
        layout.addLayout(header_row)

        self.quiz_question_lbl = QLabel()
        self.quiz_question_lbl.setWordWrap(True)
        self.quiz_question_lbl.setStyleSheet(
            "font-size: 13px; font-weight: 600; color: #241B16; line-height: 1.45; "
            "background-color: #F7F4EE; border-left: 3px solid #8A6642; padding: 10px 14px; border-radius: 6px;"
        )
        layout.addWidget(self.quiz_question_lbl)

        self.quiz_options_layout = QVBoxLayout()
        self.quiz_options_layout.setSpacing(8)
        self.quiz_option_buttons: list[QPushButton] = []

        for i in range(4):
            btn = QPushButton()
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFFFFF;
                    color: #241B16;
                    border: 1px solid #DCD5CA;
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-size: 12px;
                    font-weight: 500;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #F7F4EE;
                    border-color: #8A6642;
                }
                """
            )
            btn.clicked.connect(lambda _, idx=i: self._on_quiz_option_selected(idx))
            self.quiz_option_buttons.append(btn)
            self.quiz_options_layout.addWidget(btn)

        layout.addLayout(self.quiz_options_layout)

        self.quiz_feedback_lbl = QLabel()
        self.quiz_feedback_lbl.setWordWrap(True)
        self.quiz_feedback_lbl.setStyleSheet(
            "font-size: 12px; line-height: 1.4; padding: 8px 12px; border-radius: 6px;"
        )
        self.quiz_feedback_lbl.setVisible(False)
        layout.addWidget(self.quiz_feedback_lbl)

        layout.addStretch(1)
        return card

    def _build_curriculum_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border: 1px solid #DCD5CA; border-radius: 12px; }"
        )
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Header
        sb_title = QLabel(f"Academy Curriculum ({len(self.curriculum)} Lessons)")
        sb_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #241B16;")
        layout.addWidget(sb_title)

        # Level Selector Dropdown
        self.level_combo = QComboBox()
        self.level_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #F7F4EE;
                border: 1px solid #DCD5CA;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
                font-weight: 600;
                color: #4A3525;
            }
            QComboBox:hover {
                border-color: #8A6642;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            """
        )
        self.level_combo.addItems([
            "All Academy Levels (42 Lessons)",
            "Level 1: Beginner Foundations",
            "Level 2: Chess Tactics",
            "Level 3: Opening Mastery",
            "Level 4: Middlegame Strategy",
            "Level 5: Advanced Calculation",
            "Level 6: Endgame Mastery",
            "Level 7: Competitive Chess",
        ])
        self.level_combo.currentIndexChanged.connect(self._on_level_filter_changed)
        layout.addWidget(self.level_combo)

        # Smart Recommendation Card
        self.rec_card = QFrame()
        self.rec_card.setStyleSheet(
            "QFrame { background-color: #F7F4EE; border: 1px solid #E0D6CB; border-radius: 8px; padding: 8px; }"
        )
        rec_box = QVBoxLayout(self.rec_card)
        rec_box.setContentsMargins(6, 6, 6, 6)
        rec_box.setSpacing(4)

        self.rec_title_lbl = QLabel("💡 Smart Recommendation")
        self.rec_title_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #6E5D53;")
        rec_box.addWidget(self.rec_title_lbl)

        self.rec_desc_lbl = QLabel()
        self.rec_desc_lbl.setWordWrap(True)
        self.rec_desc_lbl.setStyleSheet("font-size: 11px; color: #241B16;")
        rec_box.addWidget(self.rec_desc_lbl)

        self.rec_btn = QPushButton("Practice Recommendation →")
        self.rec_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rec_btn.setStyleSheet(PRIMARY_BTN)
        self.rec_btn.setMinimumHeight(30)
        self.rec_btn.clicked.connect(self._on_rec_clicked)
        rec_box.addWidget(self.rec_btn)
        layout.addWidget(self.rec_card)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(self.curriculum))
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #EFEBE3;
                border-radius: 3px;
                border: 1px solid #DCD5CA;
            }
            QProgressBar::chunk {
                background-color: #3F6E4D;
                border-radius: 3px;
            }
            """
        )
        layout.addWidget(self.progress_bar)

        # Scroll area with categorized lesson buttons
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        scroll.viewport().setStyleSheet("background: transparent;")

        self.lesson_list_container = QWidget()
        self.lesson_list_layout = QVBoxLayout(self.lesson_list_container)
        self.lesson_list_layout.setContentsMargins(0, 0, 0, 0)
        self.lesson_list_layout.setSpacing(6)

        self.lesson_buttons: dict[str, QPushButton] = {}
        self.category_pills: dict[str, QLabel] = {}
        self.category_headers: dict[str, QWidget] = {}
        current_cat = ""

        for lesson in self.curriculum:
            if lesson.category != current_cat:
                current_cat = lesson.category
                header_widget = QWidget()
                cat_row = QHBoxLayout(header_widget)
                cat_row.setContentsMargins(0, 8, 0, 2)
                cat_row.setSpacing(6)

                cat_lbl = QLabel(current_cat)
                cat_lbl.setStyleSheet(
                    "font-size: 11px; font-weight: 700; color: #6E5D53; "
                    "text-transform: uppercase; letter-spacing: 0.5px;"
                )
                cat_row.addWidget(cat_lbl)
                cat_row.addStretch(1)

                cat_badge = QLabel("0/0")
                cat_badge.setStyleSheet(
                    "font-size: 10px; font-weight: 600; color: #6E5D53; "
                    "background-color: #EFEBE3; border: 1px solid #DCD5CA; "
                    "border-radius: 4px; padding: 1px 6px;"
                )
                self.category_pills[current_cat] = cat_badge
                cat_row.addWidget(cat_badge)

                self.category_headers[current_cat] = header_widget
                self.lesson_list_layout.addWidget(header_widget)

            btn = QPushButton()
            btn.setObjectName(f"lesson_btn_{lesson.id}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(38)
            btn.clicked.connect(lambda _, lid=lesson.id: self.select_lesson_by_id(lid))
            self.lesson_buttons[lesson.id] = btn
            self.lesson_list_layout.addWidget(btn)

        self.lesson_list_layout.addStretch(1)
        scroll.setWidget(self.lesson_list_container)
        layout.addWidget(scroll, 1)

        return sidebar

    def _on_level_filter_changed(self, index: int) -> None:
        """Filter sidebar curriculum list by selected tier level."""
        self._selected_level_filter = index
        self._update_sidebar_visibility()

    def _update_sidebar_visibility(self) -> None:
        lvl = self._selected_level_filter
        # Category headers visibility
        cats_in_level: set[str] = set()
        for lesson in self.curriculum:
            if lvl == 0 or lesson.level_number == lvl:
                cats_in_level.add(lesson.category)

        for cat, header in self.category_headers.items():
            header.setVisible(cat in cats_in_level)

        for lesson in self.curriculum:
            btn = self.lesson_buttons.get(lesson.id)
            if btn:
                btn.setVisible(lvl == 0 or lesson.level_number == lvl)

    # -------------------------------------------------------------
    # Interactive Modes (Challenge / Theory / Demonstration / Assessment)
    # -------------------------------------------------------------
    def _set_learning_mode(self, mode: str) -> None:
        self._current_mode = mode
        self._update_mode_buttons_ui()

        username = self.profile_manager.get_username()

        if mode == "theory":
            self.board_container.setVisible(True)
            self.quiz_card.setVisible(False)
            self.actions_bar_widget.setVisible(True)

            self.theory_mode_badge.setText("Theory Mode")
            self.theory_mode_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #3F6E4D; "
                "background-color: #EFEBE3; border: 1px solid #C8D6C7; border-radius: 6px; padding: 2px 8px;"
            )
            self.note_header.setText(f"📖 Grandmaster Theory: {self.current_lesson.title}")
            self.note_text.setText(self.current_lesson.educational_note)
            if self.current_lesson.theory_detail:
                self.theory_deep_dive_lbl.setText(f"💡 Key Strategy:\n{self.current_lesson.theory_detail}")
                self.theory_deep_dive_lbl.setVisible(True)
            else:
                self.theory_deep_dive_lbl.setVisible(False)

            if self.current_lesson.real_application:
                self.real_app_lbl.setText(f"🏆 Master Game Application:\n{self.current_lesson.real_application}")
                self.real_app_lbl.setVisible(True)
            else:
                self.real_app_lbl.setVisible(False)

            self.cm_dialogue_lbl.setText(
                f"📖 Concept & Theory Study for {username}:\n"
                f"Carefully examine this position and the strategic concepts below. "
                f"Understanding the core principles helps you discover the move intuitively!"
            )
            self.cm_objective_lbl.setText(f"🎯 Principle: {self.current_lesson.objective}")
            self.cm_threat_lbl.setVisible(False)

        elif mode == "demo":
            self.board_container.setVisible(True)
            self.quiz_card.setVisible(False)
            self.actions_bar_widget.setVisible(True)

            self.theory_mode_badge.setText("Demonstration")
            self.theory_mode_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #8A6642; "
                "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
            )
            self.theory_deep_dive_lbl.setVisible(False)
            self.real_app_lbl.setVisible(False)
            self.cm_threat_lbl.setVisible(False)
            self._demonstrate_move()

        elif mode == "assessment":
            self.board_container.setVisible(False)
            self.quiz_card.setVisible(True)
            self.actions_bar_widget.setVisible(False)

            self.theory_mode_badge.setText("Assessment Quiz")
            self.theory_mode_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #6E5D53; "
                "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
            )
            self.cm_dialogue_lbl.setText(
                f"📝 Academy Assessment for {username}:\n"
                f"Put your conceptual understanding to the test! Answer the question below to confirm your mastery."
            )
            self.cm_objective_lbl.setText("🎯 Select the most accurate chess principle below:")
            self.cm_threat_lbl.setVisible(False)
            self._load_quiz_ui()

        else:  # "challenge"
            self.board_container.setVisible(True)
            self.quiz_card.setVisible(False)
            self.actions_bar_widget.setVisible(True)

            self.theory_mode_badge.setText("Practice Mode")
            self.theory_mode_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #8A6642; "
                "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
            )
            self.note_header.setText("📖 Grandmaster Insight & Strategy")
            self.note_text.setText(self.current_lesson.educational_note)
            self.theory_deep_dive_lbl.setVisible(False)
            self.real_app_lbl.setVisible(False)

            # Reset board for student challenge
            self.game.board.set_fen(self.current_lesson.fen)
            self.game._move_history.clear()
            self.board_widget.clear_selection()
            self.board_widget.refresh()

            cm_intro_text = self.current_lesson.cm_intro.format(username=username)
            self.cm_dialogue_lbl.setText(cm_intro_text)
            self.cm_objective_lbl.setText(f"🎯 Objective: {self.current_lesson.objective}")
            if self.current_lesson.opponent_threat:
                self.cm_threat_lbl.setText(f"⚠️ Opponent Threat: {self.current_lesson.opponent_threat}")
                self.cm_threat_lbl.setVisible(True)
            else:
                self.cm_threat_lbl.setVisible(False)

    def _update_mode_buttons_ui(self) -> None:
        self.mode_challenge_btn.setStyleSheet(
            TAB_ACTIVE_BTN if self._current_mode == "challenge" else TAB_INACTIVE_BTN
        )
        self.mode_theory_btn.setStyleSheet(
            TAB_ACTIVE_BTN if self._current_mode == "theory" else TAB_INACTIVE_BTN
        )
        self.mode_demo_btn.setStyleSheet(
            TAB_ACTIVE_BTN if self._current_mode == "demo" else TAB_INACTIVE_BTN
        )
        self.mode_assessment_btn.setStyleSheet(
            TAB_ACTIVE_BTN if self._current_mode == "assessment" else TAB_INACTIVE_BTN
        )

    # -------------------------------------------------------------
    # Conceptual Assessment Quiz Handling
    # -------------------------------------------------------------
    def _load_quiz_ui(self) -> None:
        lesson = self.current_lesson
        self.quiz_question_lbl.setText(lesson.assessment_question)
        self.quiz_feedback_lbl.setVisible(False)
        self.quiz_status_badge.setText("Active Quiz")
        self.quiz_status_badge.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #4A3525; "
            "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
        )

        for i, btn in enumerate(self.quiz_option_buttons):
            if i < len(lesson.assessment_options):
                btn.setText(f"{chr(65 + i)}.  {lesson.assessment_options[i]}")
                btn.setEnabled(True)
                btn.setVisible(True)
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #FFFFFF;
                        color: #241B16;
                        border: 1px solid #DCD5CA;
                        border-radius: 8px;
                        padding: 8px 14px;
                        font-size: 12px;
                        font-weight: 500;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #F7F4EE;
                        border-color: #8A6642;
                    }
                    """
                )
            else:
                btn.setVisible(False)

    def _on_quiz_option_selected(self, option_index: int) -> None:
        lesson = self.current_lesson
        is_correct = (option_index == lesson.assessment_answer_index)
        self.profile_manager.record_exercise_attempt(
            lesson.id, lesson.topic, is_correct, hints_used=0
        )

        # Update styling of options
        for i, btn in enumerate(self.quiz_option_buttons):
            if i == lesson.assessment_answer_index:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #EBF4EC;
                        color: #2E5C38;
                        border: 2px solid #3F6E4D;
                        border-radius: 8px;
                        padding: 8px 14px;
                        font-size: 12px;
                        font-weight: 700;
                        text-align: left;
                    }
                    """
                )
            elif i == option_index and not is_correct:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #FBEBEB;
                        color: #A32D2D;
                        border: 2px solid #D9534F;
                        border-radius: 8px;
                        padding: 8px 14px;
                        font-size: 12px;
                        font-weight: 600;
                        text-align: left;
                    }
                    """
                )

        if is_correct:
            self.quiz_status_badge.setText("Passed ✓")
            self.quiz_status_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #3F6E4D; "
                "background-color: #EFEBE3; border: 1px solid #C8D6C7; border-radius: 6px; padding: 2px 8px;"
            )
            self.quiz_feedback_lbl.setText(f"🎉 Correct! {lesson.assessment_explanation}")
            self.quiz_feedback_lbl.setStyleSheet(
                "font-size: 12px; line-height: 1.4; color: #2E5C38; "
                "background-color: #EBF4EC; border: 1px solid #C8D6C7; padding: 10px 14px; border-radius: 6px;"
            )
            self.quiz_feedback_lbl.setVisible(True)
        else:
            self.quiz_status_badge.setText("Review Required")
            self.quiz_status_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #A32D2D; "
                "background-color: #FDF0F0; border: 1px solid #F3C4C4; border-radius: 6px; padding: 2px 8px;"
            )
            self.quiz_feedback_lbl.setText(f"🤔 Not quite. {lesson.assessment_explanation}")
            self.quiz_feedback_lbl.setStyleSheet(
                "font-size: 12px; line-height: 1.4; color: #A32D2D; "
                "background-color: #FDF0F0; border: 1px solid #F3C4C4; padding: 10px 14px; border-radius: 6px;"
            )
            self.quiz_feedback_lbl.setVisible(True)

        self._refresh_progress_ui()

    # -------------------------------------------------------------
    # Lesson Management & State
    # -------------------------------------------------------------
    def _initial_lesson(self) -> Lesson:
        saved_id = self.profile_manager.get_current_lesson_id()
        lesson = get_lesson_by_id(saved_id)
        return lesson or self.curriculum[0]

    def load_lesson(self, lesson: Lesson) -> None:
        """Load a specific lesson onto the board and update CM dialogue."""
        self.current_lesson = lesson
        self.is_lesson_solved = False
        self._hint_tier = 0
        self.profile_manager.set_current_lesson_id(lesson.id)

        # Setup isolated board with lesson FEN
        self.game.board.set_fen(lesson.fen)
        self.game._move_history.clear()

        # Update board orientation
        color = chess.WHITE if lesson.player_color == "White" else chess.BLACK
        self.board_widget.set_orientation(color)
        self.board_widget.clear_selection()
        self.board_widget.refresh()

        # Update CM dialogue with username
        username = self.profile_manager.get_username()
        cm_intro_text = lesson.cm_intro.format(username=username)
        self.cm_dialogue_lbl.setText(cm_intro_text)
        self.cm_objective_lbl.setText(f"🎯 Objective: {lesson.objective}")
        self.lesson_badge.setText(f"Level {lesson.level_number}: {lesson.level_name}")
        self.turn_badge.setText(f"{lesson.player_color} to Move")

        # Update threat pill
        if lesson.opponent_threat:
            self.cm_threat_lbl.setText(f"⚠️ Opponent Threat: {lesson.opponent_threat}")
            self.cm_threat_lbl.setVisible(self._current_mode == "challenge")
        else:
            self.cm_threat_lbl.setVisible(False)

        # Update educational note
        self.note_header.setText("📖 Grandmaster Insight & Strategy")
        self.note_text.setText(lesson.educational_note)
        self.theory_deep_dive_lbl.setVisible(False)
        self.real_app_lbl.setVisible(False)

        # Reset hint button
        self.hint_btn.setText("💡 Ask CM for Hint")

        # Reset mode to challenge
        self._current_mode = "challenge"
        self._update_mode_buttons_ui()

        # Ensure board and actions are visible
        self.board_container.setVisible(True)
        self.quiz_card.setVisible(False)
        self.actions_bar_widget.setVisible(True)

        # Button states
        has_prev = get_prev_lesson(lesson.id) is not None
        has_next = get_next_lesson(lesson.id) is not None
        self.prev_btn.setEnabled(has_prev)
        self.next_btn.setEnabled(has_next)

        self._refresh_progress_ui()

    def select_lesson_by_id(self, lesson_id: str) -> None:
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            self.load_lesson(lesson)

    def _demonstrate_move(self) -> None:
        """Execute guided demonstration move on the board and explain it."""
        username = self.profile_manager.get_username()
        self.game.board.set_fen(self.current_lesson.fen)
        self.game._move_history.clear()

        if self.current_lesson.guided_move:
            try:
                self.game.make_move(self.current_lesson.guided_move)
            except Exception:
                pass

        self.board_widget.refresh()

        explanation = self.current_lesson.feedback_correct or (
            "Notice how this piece move targets key squares, follows core principles, "
            "and achieves the strategic objective flawlessly."
        )
        if "{username}" in explanation:
            explanation = explanation.format(username=username)

        self.cm_dialogue_lbl.setText(
            f"🎬 Guided Demonstration for {username}:\n"
            f"Watch the board — CM executed '{self.current_lesson.guided_move}'.\n"
            f"{explanation}\n\n"
            f"Click '↺ Reset Board' to practice playing this move yourself!"
        )
        self.cm_objective_lbl.setText("✨ Move demonstrated! Click '↺ Reset Board' to practice.")

    def _on_user_board_move(self, uci_move: str) -> None:
        """Called whenever the user makes a move on the board widget."""
        username = self.profile_manager.get_username()

        if uci_move in self.current_lesson.expected_moves:
            self.is_lesson_solved = True
            self.profile_manager.record_exercise_attempt(
                self.current_lesson.id,
                self.current_lesson.topic,
                True,
                hints_used=self._hint_tier,
            )

            success_text = self.current_lesson.cm_success.format(username=username)
            if self.current_lesson.feedback_correct:
                fb = self.current_lesson.feedback_correct
                if "{username}" in fb:
                    fb = fb.format(username=username)
                success_text = f"{success_text} {fb}"

            if self.current_lesson.real_application:
                success_text += f"\n\n🏆 Master Application: {self.current_lesson.real_application}"

            self.cm_dialogue_lbl.setText(f"🎉 {success_text}")
            self.cm_objective_lbl.setText("✨ Objective Complete! Well done!")

            self._refresh_progress_ui()
        else:
            self.profile_manager.record_exercise_attempt(
                self.current_lesson.id,
                self.current_lesson.topic,
                False,
                hints_used=self._hint_tier,
            )

            why_failed = self.current_lesson.why_mistakes_fail.get(uci_move)
            if why_failed:
                if "{username}" in why_failed:
                    why_failed = why_failed.format(username=username)
                cm_msg = (
                    f"🤔 Not quite, {username}!\n"
                    f"⚠️ Tactical Analysis: {why_failed}\n\n"
                    f"💡 Hint: {self.current_lesson.cm_hint}"
                )
            else:
                hint_text = self.current_lesson.cm_hint
                if self.current_lesson.feedback_incorrect:
                    fb = self.current_lesson.feedback_incorrect
                    if "{username}" in fb:
                        fb = fb.format(username=username)
                    hint_text = f"{fb} Hint: {hint_text}"

                cm_msg = (
                    f"🤔 Not quite, {username}! That move doesn't achieve our objective.\n"
                    f"{hint_text}"
                )

            self.cm_dialogue_lbl.setText(cm_msg)
            self.cm_objective_lbl.setText(
                "Click '↺ Reset Board' to try the position again."
            )

    def _show_hint(self) -> None:
        """Cycle through multi-tier progressive hints."""
        username = self.profile_manager.get_username()
        self.profile_manager.record_hint_used(self.current_lesson.id, self.current_lesson.topic)
        hints = self.current_lesson.hints

        if hints and len(hints) > 0:
            total = len(hints)
            idx = self._hint_tier % total
            self._hint_tier += 1

            tier_names = ["Strategic Direction", "Target Piece & Square", "Concrete Move Instruction"]
            tier_name = tier_names[idx] if idx < len(tier_names) else f"Step {idx + 1}"

            hint_text = hints[idx]
            if "{username}" in hint_text:
                hint_text = hint_text.format(username=username)

            self.cm_dialogue_lbl.setText(
                f"💡 CM's Hint ({idx + 1}/{total} • {tier_name}) for {username}:\n{hint_text}"
            )
            next_idx = (self._hint_tier % total) + 1
            self.hint_btn.setText(f"💡 Hint ({next_idx}/{total})")
        else:
            # Fallback to single cm_hint
            self.cm_dialogue_lbl.setText(
                f"💡 CM's Hint for {username}:\n{self.current_lesson.cm_hint}"
            )

    def _reset_current_lesson(self) -> None:
        self.load_lesson(self.current_lesson)

    def _go_prev_lesson(self) -> None:
        prev = get_prev_lesson(self.current_lesson.id)
        if prev:
            self.load_lesson(prev)

    def _go_next_lesson(self) -> None:
        nxt = get_next_lesson(self.current_lesson.id)
        if nxt:
            self.load_lesson(nxt)

    def _on_rec_clicked(self) -> None:
        rec_id = self.profile_manager.get_recommended_lesson_id()
        if rec_id:
            self.select_lesson_by_id(rec_id)

    def _refresh_progress_ui(self) -> None:
        """Update sidebar checkmarks, category counts, progress bar, accuracy, and recommendations."""
        completed = self.profile_manager.get_profile().completed_lessons
        total = len(self.curriculum)
        done_count = len(completed)

        self.progress_bar.setValue(done_count)
        self.progress_pill.setText(f"🏆 {done_count} / {total} Completed")

        # Accuracy
        acc = self.profile_manager.get_accuracy_rate()
        self.accuracy_pill.setText(f"🎯 Accuracy: {acc}%")

        # Smart Recommendation
        rec_id = self.profile_manager.get_recommended_lesson_id()
        rec_lesson = get_lesson_by_id(rec_id)
        if rec_lesson:
            weak_topics = [t for t, _ in self.profile_manager.get_weak_topics()]
            reason = "Focus Area" if rec_lesson.topic in weak_topics else "Next Challenge"
            self.rec_desc_lbl.setText(f"[{reason}] {rec_lesson.title}")

        # Update category badges
        cat_counts: dict[str, list[int]] = {}  # cat -> [done, total]
        for lesson in self.curriculum:
            if lesson.category not in cat_counts:
                cat_counts[lesson.category] = [0, 0]
            cat_counts[lesson.category][1] += 1
            if lesson.id in completed:
                cat_counts[lesson.category][0] += 1

        for cat, (d, t) in cat_counts.items():
            pill = self.category_pills.get(cat)
            if pill:
                pill.setText(f"{d}/{t}")
                if d == t and t > 0:
                    pill.setStyleSheet(
                        "font-size: 10px; font-weight: 600; color: #3F6E4D; "
                        "background-color: #EFEBE3; border: 1px solid #C8D6C7; "
                        "border-radius: 4px; padding: 1px 6px;"
                    )
                else:
                    pill.setStyleSheet(
                        "font-size: 10px; font-weight: 600; color: #6E5D53; "
                        "background-color: #EFEBE3; border: 1px solid #DCD5CA; "
                        "border-radius: 4px; padding: 1px 6px;"
                    )

        # Update lesson buttons
        for lesson in self.curriculum:
            btn = self.lesson_buttons.get(lesson.id)
            if not btn:
                continue

            is_active = (lesson.id == self.current_lesson.id)
            is_done = (lesson.id in completed)
            is_unlocked = self.profile_manager.is_level_unlocked(lesson.level_number)

            if not is_unlocked:
                btn.setText(f"🔒 {lesson.title}")
            else:
                icon = "✓ " if is_done else "• "
                btn.setText(f"{icon}{lesson.title}")

            if is_active:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #EFEBE3;
                        color: #4A3525;
                        border: 1.5px solid #4A3525;
                        border-radius: 6px;
                        padding: 7px 12px;
                        font-size: 12px;
                        font-weight: 700;
                        text-align: left;
                        min-height: 38px;
                    }
                    """
                )
            elif is_done:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #FFFFFF;
                        color: #3F6E4D;
                        border: 1px solid #C8D6C7;
                        border-radius: 6px;
                        padding: 7px 12px;
                        font-size: 12px;
                        font-weight: 500;
                        text-align: left;
                        min-height: 38px;
                    }
                    QPushButton:hover { background-color: #F7F4EE; }
                    """
                )
            elif not is_unlocked:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #F4F1EA;
                        color: #A0968E;
                        border: 1px dashed #DCD5CA;
                        border-radius: 6px;
                        padding: 7px 12px;
                        font-size: 12px;
                        font-weight: 400;
                        text-align: left;
                        min-height: 38px;
                    }
                    """
                )
            else:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #FFFFFF;
                        color: #241B16;
                        border: 1px solid #E8E2D8;
                        border-radius: 6px;
                        padding: 7px 12px;
                        font-size: 12px;
                        font-weight: 400;
                        text-align: left;
                        min-height: 38px;
                    }
                    QPushButton:hover { background-color: #F7F4EE; border-color: #8A6642; }
                    """
                )

        self._update_sidebar_visibility()
