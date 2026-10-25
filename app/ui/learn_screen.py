from __future__ import annotations

"""Window: Learn Chess Module featuring AI companion 'CM' (Chess Mate)."""

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
from app.ui.styles import PRIMARY_BTN, SECONDARY_BTN, SUCCESS_BTN


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

        self.setStyleSheet("QWidget { background-color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(14)

        # -------------------------------------------------------------
        # 1. TOP BAR
        # -------------------------------------------------------------
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)

        self.back_button = QPushButton("← Main Menu")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #475569;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #F1F5F9; color: #0F172A; }
            """
        )
        self.back_button.clicked.connect(self.main_menu_clicked.emit)
        top_bar.addWidget(self.back_button)

        title_lbl = QLabel("Learn Chess with CM")
        title_lbl.setStyleSheet(
            "font-size: 17px; font-weight: 800; color: #0F172A; letter-spacing: 0.3px;"
        )
        top_bar.addWidget(title_lbl)

        self.cm_status_pill = QLabel("🤖 CM: Online & Ready")
        self.cm_status_pill.setStyleSheet(
            "font-size: 12px; font-weight: 700; color: #1D4ED8; "
            "background-color: #EFF6FF; border: 1px solid #BFDBFE; "
            "border-radius: 12px; padding: 4px 14px;"
        )
        top_bar.addWidget(self.cm_status_pill)

        top_bar.addStretch(1)

        self.progress_pill = QLabel()
        self.progress_pill.setStyleSheet(
            "font-size: 12px; font-weight: 700; color: #065F46; "
            "background-color: #D1FAE5; border: 1px solid #A7F3D0; "
            "border-radius: 12px; padding: 4px 14px;"
        )
        top_bar.addWidget(self.progress_pill)

        root.addLayout(top_bar)

        # -------------------------------------------------------------
        # 2. MAIN SPLIT LAYOUT (Left: Board + CM, Right: Curriculum Sidebar)
        # -------------------------------------------------------------
        content_row = QHBoxLayout()
        content_row.setSpacing(20)

        # --- LEFT COLUMN: CM Dialogue & Board ---
        left_col = QVBoxLayout()
        left_col.setSpacing(12)

        # CM Companion Speech Card
        self.cm_card = self._build_cm_speech_card()
        left_col.addWidget(self.cm_card)

        # Interactive Board Container
        self.board_container = QWidget()
        self.board_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        board_box = QVBoxLayout(self.board_container)
        board_box.setContentsMargins(0, 0, 0, 0)

        self.board_widget = ChessBoardWidget(game=self.game, parent=self)
        self.board_widget.move_made.connect(self._on_user_board_move)
        board_box.addWidget(self.board_widget)
        left_col.addWidget(self.board_container, 1)

        # Action bar under board (Hint, Reset, Prev, Next)
        actions_bar = QHBoxLayout()
        actions_bar.setSpacing(10)

        self.hint_btn = QPushButton("💡 Ask CM for Hint")
        self.hint_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hint_btn.setStyleSheet(SECONDARY_BTN)
        self.hint_btn.clicked.connect(self._show_hint)
        actions_bar.addWidget(self.hint_btn)

        self.reset_btn = QPushButton("↺ Reset Board")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setStyleSheet(SECONDARY_BTN)
        self.reset_btn.clicked.connect(self._reset_current_lesson)
        actions_bar.addWidget(self.reset_btn)

        actions_bar.addStretch(1)

        self.prev_btn = QPushButton("← Prev Lesson")
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.setStyleSheet(SECONDARY_BTN)
        self.prev_btn.clicked.connect(self._go_prev_lesson)
        actions_bar.addWidget(self.prev_btn)

        self.next_btn = QPushButton("Next Lesson →")
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setStyleSheet(PRIMARY_BTN)
        self.next_btn.clicked.connect(self._go_next_lesson)
        actions_bar.addWidget(self.next_btn)

        left_col.addLayout(actions_bar)

        # Grandmaster Educational Theory Note
        self.note_card = QFrame()
        self.note_card.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px; }"
        )
        note_layout = QVBoxLayout(self.note_card)
        note_layout.setContentsMargins(16, 12, 16, 12)
        note_layout.setSpacing(4)

        self.note_header = QLabel("📖 Grandmaster Insight")
        self.note_header.setStyleSheet("font-size: 12px; font-weight: 800; color: #1E293B;")
        note_layout.addWidget(self.note_header)

        self.note_text = QLabel()
        self.note_text.setWordWrap(True)
        self.note_text.setStyleSheet("font-size: 12px; color: #475569; line-height: 1.4;")
        note_layout.addWidget(self.note_text)

        left_col.addWidget(self.note_card)

        content_row.addLayout(left_col, 3)

        # --- RIGHT COLUMN: Curriculum Navigation Sidebar ---
        right_sidebar = self._build_curriculum_sidebar()
        content_row.addWidget(right_sidebar, 1)

        root.addLayout(content_row, 1)

        # Load initial lesson
        self.load_lesson(self.current_lesson)

    # -------------------------------------------------------------
    # UI Component Builders
    # -------------------------------------------------------------
    def _build_cm_speech_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("cmSpeechCard")
        card.setStyleSheet(
            """
            QFrame#cmSpeechCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0F172A, stop:1 #1E293B);
                border: 1px solid #334155;
                border-radius: 14px;
            }
            """
        )
        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(16)

        # Avatar
        avatar = QLabel("🤖")
        avatar.setFixedSize(48, 48)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "font-size: 28px; background-color: #2563EB; "
            "border: 2px solid #60A5FA; border-radius: 24px;"
        )
        layout.addWidget(avatar, 0, Qt.AlignmentFlag.AlignTop)

        # Text column
        text_col = QVBoxLayout()
        text_col.setSpacing(6)

        top_row = QHBoxLayout()
        self.cm_name_lbl = QLabel("CM (Chess Mate) • AI Coach")
        self.cm_name_lbl.setStyleSheet("font-size: 12px; font-weight: 800; color: #60A5FA;")
        top_row.addWidget(self.cm_name_lbl)

        self.lesson_badge = QLabel("Lesson 1")
        self.lesson_badge.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #94A3B8; "
            "background-color: rgba(255,255,255,0.08); border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(self.lesson_badge)
        top_row.addStretch(1)
        text_col.addLayout(top_row)

        self.cm_dialogue_lbl = QLabel()
        self.cm_dialogue_lbl.setWordWrap(True)
        self.cm_dialogue_lbl.setStyleSheet("font-size: 13px; color: #F1F5F9; line-height: 1.4;")
        text_col.addWidget(self.cm_dialogue_lbl)

        self.cm_objective_lbl = QLabel()
        self.cm_objective_lbl.setWordWrap(True)
        self.cm_objective_lbl.setStyleSheet(
            "font-size: 12px; font-weight: 700; color: #34D399; margin-top: 4px;"
        )
        text_col.addWidget(self.cm_objective_lbl)

        layout.addLayout(text_col, 1)
        return card

    def _build_curriculum_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 14px; }"
        )
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        sb_title = QLabel("Course Curriculum")
        sb_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        layout.addWidget(sb_title)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(self.curriculum))
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #F1F5F9;
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #10B981;
                border-radius: 4px;
            }
            """
        )
        layout.addWidget(self.progress_bar)

        # Scroll area with lesson buttons
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
        current_cat = ""

        for lesson in self.curriculum:
            if lesson.category != current_cat:
                current_cat = lesson.category
                cat_lbl = QLabel(current_cat)
                cat_lbl.setStyleSheet(
                    "font-size: 11px; font-weight: 800; color: #64748B; "
                    "text-transform: uppercase; letter-spacing: 0.5px; margin-top: 8px; margin-bottom: 2px;"
                )
                self.lesson_list_layout.addWidget(cat_lbl)

            btn = QPushButton()
            btn.setObjectName(f"lesson_btn_{lesson.id}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, lid=lesson.id: self.select_lesson_by_id(lid))
            self.lesson_buttons[lesson.id] = btn
            self.lesson_list_layout.addWidget(btn)

        self.lesson_list_layout.addStretch(1)
        scroll.setWidget(self.lesson_list_container)
        layout.addWidget(scroll, 1)

        return sidebar

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

        # Update educational note
        self.note_text.setText(lesson.educational_note)

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

    def _on_user_board_move(self, uci_move: str) -> None:
        """Called whenever the user makes a move on the board widget."""
        username = self.profile_manager.get_username()

        # Check if the played move matches an expected solution
        if uci_move in self.current_lesson.expected_moves:
            self.is_lesson_solved = True
            self.profile_manager.mark_lesson_completed(self.current_lesson.id)

            success_text = self.current_lesson.cm_success.format(username=username)
            self.cm_dialogue_lbl.setText(f"🎉 {success_text}")
            self.cm_objective_lbl.setText("✨ Objective Complete! Well done!")

            self._refresh_progress_ui()
        else:
            hint_text = self.current_lesson.cm_hint
            self.cm_dialogue_lbl.setText(
                f"🤔 Not quite, {username}! That move doesn't achieve our objective.\n"
                f"Hint: {hint_text}"
            )
            self.cm_objective_lbl.setText(
                "Click '↺ Reset Board' to try the position again."
            )

    def _show_hint(self) -> None:
        username = self.profile_manager.get_username()
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
        """Update sidebar checkmarks, progress bar, and top badges."""
        completed = self.profile_manager.get_profile().completed_lessons
        total = len(self.curriculum)
        done_count = len(completed)

        self.progress_bar.setValue(done_count)
        self.progress_pill.setText(f"🏆 {done_count} / {total} Completed")

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
                        background-color: #EFF6FF;
                        color: #1D4ED8;
                        border: 1.5px solid #3B82F6;
                        border-radius: 8px;
                        padding: 8px 10px;
                        font-size: 12px;
                        font-weight: 700;
                        text-align: left;
                    }
                    """
                )
            elif is_done:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #F0FDF4;
                        color: #15803D;
                        border: 1px solid #BBF7D0;
                        border-radius: 8px;
                        padding: 8px 10px;
                        font-size: 12px;
                        font-weight: 600;
                        text-align: left;
                    }
                    QPushButton:hover { background-color: #DCFCE7; }
                    """
                )
            else:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #FFFFFF;
                        color: #475569;
                        border: 1px solid #E2E8F0;
                        border-radius: 8px;
                        padding: 8px 10px;
                        font-size: 12px;
                        font-weight: 500;
                        text-align: left;
                    }
                    QPushButton:hover { background-color: #F8FAFC; border-color: #CBD5E1; }
                    """
                )
