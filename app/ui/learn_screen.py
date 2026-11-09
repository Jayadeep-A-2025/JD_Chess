from __future__ import annotations

"""Window: Learn Chess Module featuring AI companion 'CM' (Chess Mate) with responsive mobile layout,
interactive learning modes (Practice Challenge, Grandmaster Theory, Guided Demonstration),
multi-tier progressive hints, rich move explanations, and structured curriculum navigation.
Styled in Warm Beige & Walnut theme: clean, elegant, minimal, and traditional.
"""

import chess
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
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
    """Interactive learning module guided step-by-step by companion CM."""

    main_menu_clicked = Signal()

    def __init__(
        self,
        profile_manager: UserProfileManager,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.profile_manager = profile_manager
        self.curriculum = get_curriculum()

        # Dedicated isolated game instance for interactive puzzles
        self.game = ChessGame()
        self.current_lesson: Lesson = self._initial_lesson()
        self.is_lesson_solved: bool = False
        self._is_narrow_layout = False
        self._hint_tier: int = 0
        self._current_mode: str = "challenge"  # "challenge" | "theory" | "demo"

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
        self.back_button.setMinimumHeight(40)
        self.back_button.setStyleSheet(SECONDARY_BTN)
        self.back_button.clicked.connect(self.main_menu_clicked.emit)
        top_bar.addWidget(self.back_button)

        title_lbl = QLabel("Learn Chess with CM")
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

        # --- LEFT COLUMN: Mode Tabs, CM Dialogue, Board, Actions, Theory ---
        self.left_col = QWidget()
        self.left_col_layout = QVBoxLayout(self.left_col)
        self.left_col_layout.setContentsMargins(0, 0, 0, 0)
        self.left_col_layout.setSpacing(10)

        # Mode Selection Bar (Challenge vs Theory vs Demonstration)
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

        # Action bar under board (Hint, Demo, Reset, Prev, Next)
        actions_bar = QHBoxLayout()
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

        self.left_col_layout.addLayout(actions_bar)

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

            self.right_sidebar.setMinimumWidth(300)
            self.content_layout.addWidget(self.left_col, 3)
            self.content_layout.addWidget(self.right_sidebar, 1)

        self._is_narrow_layout = is_narrow

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        w = self.width()
        should_be_narrow = (w < 820)
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
        self.cm_name_lbl = QLabel("CM (Chess Mate) • AI Companion")
        self.cm_name_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #4A3525;")
        top_row.addWidget(self.cm_name_lbl)

        self.lesson_badge = QLabel("Lesson 1")
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
            "font-size: 12px; font-weight: 600; color: #8A6642; margin-top: 4px;"
        )
        text_col.addWidget(self.cm_objective_lbl)

        layout.addLayout(text_col, 1)
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
        sb_title = QLabel(f"Course Curriculum ({len(self.curriculum)} Lessons)")
        sb_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #241B16;")
        layout.addWidget(sb_title)

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
        current_cat = ""

        for lesson in self.curriculum:
            if lesson.category != current_cat:
                current_cat = lesson.category
                cat_row = QHBoxLayout()
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

                self.lesson_list_layout.addLayout(cat_row)

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

    # -------------------------------------------------------------
    # Interactive Modes (Challenge / Theory / Demonstration)
    # -------------------------------------------------------------
    def _set_learning_mode(self, mode: str) -> None:
        self._current_mode = mode
        self._update_mode_buttons_ui()

        username = self.profile_manager.get_username()

        if mode == "theory":
            self.theory_mode_badge.setText("Theory Mode")
            self.theory_mode_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #3F6E4D; "
                "background-color: #EFEBE3; border: 1px solid #C8D6C7; border-radius: 6px; padding: 2px 8px;"
            )
            # Display deep dive theory
            self.note_header.setText(f"📖 Grandmaster Theory: {self.current_lesson.title}")
            self.note_text.setText(self.current_lesson.educational_note)
            if self.current_lesson.theory_detail:
                self.theory_deep_dive_lbl.setText(f"💡 Key Strategy:\n{self.current_lesson.theory_detail}")
                self.theory_deep_dive_lbl.setVisible(True)
            else:
                self.theory_deep_dive_lbl.setVisible(False)

            self.cm_dialogue_lbl.setText(
                f"📖 Concept & Theory Study for {username}:\n"
                f"Carefully examine this position and the strategic concepts below. "
                f"Understanding the core principles helps you discover the move intuitively!"
            )
            self.cm_objective_lbl.setText(f"🎯 Principle: {self.current_lesson.objective}")

        elif mode == "demo":
            self.theory_mode_badge.setText("Demonstration")
            self.theory_mode_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #8A6642; "
                "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
            )
            self.theory_deep_dive_lbl.setVisible(False)
            self._demonstrate_move()

        else:  # "challenge"
            self.theory_mode_badge.setText("Practice Mode")
            self.theory_mode_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #8A6642; "
                "background-color: #EFEBE3; border: 1px solid #DCD5CA; border-radius: 6px; padding: 2px 8px;"
            )
            self.note_header.setText("📖 Grandmaster Insight & Strategy")
            self.note_text.setText(self.current_lesson.educational_note)
            self.theory_deep_dive_lbl.setVisible(False)

            # Reset board for student challenge
            self.game.board.set_fen(self.current_lesson.fen)
            self.game._move_history.clear()
            self.board_widget.clear_selection()
            self.board_widget.refresh()

            cm_intro_text = self.current_lesson.cm_intro.format(username=username)
            self.cm_dialogue_lbl.setText(cm_intro_text)
            self.cm_objective_lbl.setText(f"🎯 Objective: {self.current_lesson.objective}")

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
        self.lesson_badge.setText(lesson.category)
        self.turn_badge.setText(f"{lesson.player_color} to Move")

        # Update educational note
        self.note_header.setText("📖 Grandmaster Insight & Strategy")
        self.note_text.setText(lesson.educational_note)
        self.theory_deep_dive_lbl.setVisible(False)

        # Reset hint button
        self.hint_btn.setText("💡 Ask CM for Hint")

        # Reset mode to challenge
        self._current_mode = "challenge"
        self._update_mode_buttons_ui()

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
            self.profile_manager.mark_lesson_completed(self.current_lesson.id)

            success_text = self.current_lesson.cm_success.format(username=username)
            if self.current_lesson.feedback_correct:
                fb = self.current_lesson.feedback_correct
                if "{username}" in fb:
                    fb = fb.format(username=username)
                success_text = f"{success_text} {fb}"

            self.cm_dialogue_lbl.setText(f"🎉 {success_text}")
            self.cm_objective_lbl.setText("✨ Objective Complete! Well done!")

            self._refresh_progress_ui()
        else:
            hint_text = self.current_lesson.cm_hint
            if self.current_lesson.feedback_incorrect:
                fb = self.current_lesson.feedback_incorrect
                if "{username}" in fb:
                    fb = fb.format(username=username)
                hint_text = f"{fb} Hint: {hint_text}"

            self.cm_dialogue_lbl.setText(
                f"🤔 Not quite, {username}! That move doesn't achieve our objective.\n"
                f"{hint_text}"
            )
            self.cm_objective_lbl.setText(
                "Click '↺ Reset Board' to try the position again."
            )

    def _show_hint(self) -> None:
        """Cycle through multi-tier progressive hints."""
        username = self.profile_manager.get_username()
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

    def _refresh_progress_ui(self) -> None:
        """Update sidebar checkmarks, category counts, progress bar, and top badges."""
        completed = self.profile_manager.get_profile().completed_lessons
        total = len(self.curriculum)
        done_count = len(completed)

        self.progress_bar.setValue(done_count)
        self.progress_pill.setText(f"🏆 {done_count} / {total} Completed")

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
