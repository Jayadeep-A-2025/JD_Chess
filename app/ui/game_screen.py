from __future__ import annotations

"""Window 3: Chess Board Game Screen with touch-friendly controls and responsive mobile/desktop layout."""

import chess
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core.chess_game import ChessGame
from app.ui.chessboard_widget import ChessBoardWidget
from app.ui.styles import PRIMARY_BTN, SECONDARY_BTN


class GameScreen(QWidget):
    """Clean, focused chess board screen with player banners and mobile-responsive layout."""

    save_game_clicked = Signal()
    undo_move_clicked = Signal()
    restart_game_clicked = Signal()
    main_menu_clicked = Signal()
    analyze_game_clicked = Signal()

    def __init__(self, game: ChessGame, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.game = game
        self.player_color = chess.BLACK
        self.game_mode = "Play vs Computer"
        self.difficulty = "Medium"
        self._is_narrow_layout = False

        self.setStyleSheet("QWidget { background-color: #F8FAFC; }")

        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(14, 12, 14, 12)
        main_vbox.setSpacing(10)

        # -------------------------------------------------------------
        # TOP BAR: Navigation, Match Info Pill, Quick Actions
        # -------------------------------------------------------------
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.menu_button = QPushButton("← Main Menu")
        self.menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_button.setMinimumHeight(40)
        self.menu_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #334155;
                border: 1.5px solid #CBD5E1;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #F1F5F9; color: #0F172A; }
            """
        )
        self.menu_button.clicked.connect(self.main_menu_clicked.emit)
        top_bar.addWidget(self.menu_button)

        self.match_pill = QLabel("Match in Progress")
        self.match_pill.setWordWrap(True)
        self.match_pill.setStyleSheet(
            "font-size: 12px; font-weight: 700; color: #1E293B; "
            "background-color: #EFF6FF; border: 1px solid #BFDBFE; "
            "border-radius: 12px; padding: 4px 12px;"
        )
        top_bar.addWidget(self.match_pill, 1)

        self.save_button = QPushButton("💾 Save Game")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.setMinimumHeight(40)
        self.save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #10B981;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #059669; }
            """
        )
        self.save_button.clicked.connect(self.save_game_clicked.emit)
        top_bar.addWidget(self.save_button)

        main_vbox.addLayout(top_bar)

        # -------------------------------------------------------------
        # RESPONSIVE SCROLL AREA (Ensures full access on mobile screens)
        # -------------------------------------------------------------
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.scroll_area.viewport().setStyleSheet("background: transparent;")

        self.content_container = QWidget()
        self.content_container.setStyleSheet("background: transparent;")
        self.content_layout = QHBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 4, 0, 4)
        self.content_layout.setSpacing(16)

        # BOARD COLUMN
        self.board_column_widget = QWidget()
        self.board_column_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.board_col_layout = QVBoxLayout(self.board_column_widget)
        self.board_col_layout.setContentsMargins(0, 0, 0, 0)
        self.board_col_layout.setSpacing(8)

        # Top Player Banner (Opponent)
        self.top_banner = self._create_player_banner("top")
        self.board_col_layout.addWidget(self.top_banner["frame"])

        # Chess Board Widget
        self.board_widget = ChessBoardWidget(self.game, parent=self)
        self.board_widget.setMinimumSize(280, 280)
        self.board_col_layout.addWidget(self.board_widget, 1)

        # Bottom Player Banner (User / Player 1)
        self.bottom_banner = self._create_player_banner("bottom")
        self.board_col_layout.addWidget(self.bottom_banner["frame"])

        # SIDEBAR COLUMN
        self.sidebar_panel = QWidget()
        self.sidebar_panel.setMinimumWidth(280)
        self.sidebar_layout = QVBoxLayout(self.sidebar_panel)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(10)

        # Header Title
        title_lbl = QLabel("MATCH CONTROLS")
        title_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #64748B; letter-spacing: 0.5px;"
        )
        self.sidebar_layout.addWidget(title_lbl)

        # STATUS CARD
        status_card = QFrame()
        status_card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1.5px solid #CBD5E1;
                border-radius: 12px;
            }
            """
        )
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(14, 12, 14, 12)
        status_layout.setSpacing(6)

        self.turn_label = QLabel()
        self.turn_label.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        status_layout.addWidget(self.turn_label)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 13px; color: #334155; line-height: 1.4; font-weight: 500;")
        status_layout.addWidget(self.status_label)

        self.sidebar_layout.addWidget(status_card)

        # ACTION BUTTONS ROW (Touch targets min-height 44px)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.new_game_button = QPushButton("New Match")
        self.new_game_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_game_button.setMinimumHeight(44)
        self.new_game_button.setStyleSheet(PRIMARY_BTN)
        self.new_game_button.clicked.connect(self.restart_game_clicked.emit)

        self.undo_button = QPushButton("Undo Move")
        self.undo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.undo_button.setMinimumHeight(44)
        self.undo_button.setStyleSheet(SECONDARY_BTN)
        self.undo_button.clicked.connect(self.undo_move_clicked.emit)

        btn_row.addWidget(self.new_game_button)
        btn_row.addWidget(self.undo_button)
        self.sidebar_layout.addLayout(btn_row)

        self.analyze_button = QPushButton("🔍 Analyze Game & Better Moves")
        self.analyze_button.setObjectName("gameScreenAnalyzeBtn")
        self.analyze_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.analyze_button.setMinimumHeight(44)
        self.analyze_button.setStyleSheet(
            """
            QPushButton {
                background-color: #F8FAFC;
                color: #1D4ED8;
                border: 1.5px solid #93C5FD;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 700;
                min-height: 44px;
            }
            QPushButton:hover { background-color: #EFF6FF; border-color: #2563EB; }
            QPushButton:pressed { background-color: #DBEAFE; }
            """
        )
        self.analyze_button.clicked.connect(self.analyze_game_clicked.emit)
        self.sidebar_layout.addWidget(self.analyze_button)

        # MOVE HISTORY CARD
        history_card = QFrame()
        history_card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1.5px solid #CBD5E1;
                border-radius: 12px;
            }
            """
        )
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(14, 12, 14, 12)
        history_layout.setSpacing(8)

        history_title = QLabel("MOVE HISTORY")
        history_title.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #64748B; letter-spacing: 0.5px;"
        )
        history_layout.addWidget(history_title)

        self.history_scroll = QScrollArea()
        self.history_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.history_scroll.setWidgetResizable(True)
        self.history_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.history_scroll.viewport().setStyleSheet("background: transparent;")

        self.moves_label = QLabel("No moves yet")
        self.moves_label.setWordWrap(True)
        self.moves_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.moves_label.setStyleSheet(
            """
            QLabel {
                background-color: #F8FAFC;
                color: #1E293B;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-family: Menlo, Monaco, "Courier New", monospace;
                min-height: 100px;
            }
            """
        )
        self.history_scroll.setWidget(self.moves_label)
        history_layout.addWidget(self.history_scroll, 1)

        self.sidebar_layout.addWidget(history_card, 1)

        # Add initial layout
        self._set_responsive_layout(is_narrow=False)

        self.scroll_area.setWidget(self.content_container)
        main_vbox.addWidget(self.scroll_area, 1)

        # Expose references for backwards compatibility
        self.white_captured_tray = QLabel("")
        self.black_captured_tray = QLabel("")

    # -------------------------------------------------------------
    # Responsive Layout Switching (Desktop vs Mobile)
    # -------------------------------------------------------------
    def _set_responsive_layout(self, is_narrow: bool) -> None:
        """Dynamically switch between side-by-side (desktop) and stacked (mobile)."""
        self.content_layout.removeWidget(self.board_column_widget)
        self.content_layout.removeWidget(self.sidebar_panel)

        if is_narrow:
            # Recreate as vertical stack on mobile screens
            QWidget().setLayout(self.content_layout)  # clear old layout
            self.content_layout = QVBoxLayout(self.content_container)
            self.content_layout.setContentsMargins(0, 4, 0, 4)
            self.content_layout.setSpacing(14)

            self.sidebar_panel.setMinimumWidth(0)
            self.content_layout.addWidget(self.board_column_widget)
            self.content_layout.addWidget(self.sidebar_panel)
        else:
            # Recreate as horizontal side-by-side on wide/desktop screens
            QWidget().setLayout(self.content_layout)
            self.content_layout = QHBoxLayout(self.content_container)
            self.content_layout.setContentsMargins(0, 4, 0, 4)
            self.content_layout.setSpacing(20)

            self.sidebar_panel.setMinimumWidth(280)
            self.content_layout.addWidget(self.board_column_widget, 3)
            self.content_layout.addWidget(self.sidebar_panel, 1)

        self._is_narrow_layout = is_narrow

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        w = self.width()
        should_be_narrow = (w < 768)
        if should_be_narrow != self._is_narrow_layout:
            self._set_responsive_layout(should_be_narrow)

    def _create_player_banner(self, position: str) -> dict:
        frame = QFrame()
        frame.setObjectName(f"{position}PlayerBanner")
        frame.setFixedHeight(48)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1.5px solid #CBD5E1;
                border-radius: 10px;
            }
            """
        )
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(12)

        # Player Icon & Name
        name_lbl = QLabel(f"Player ({position})")
        name_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #0F172A;")
        layout.addWidget(name_lbl)

        # Turn indicator chip
        turn_chip = QLabel("")
        turn_chip.setStyleSheet(
            "font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 6px;"
        )
        layout.addWidget(turn_chip)

        layout.addStretch(1)

        # Captured pieces label
        captures_title = QLabel("Captures:")
        captures_title.setStyleSheet("font-size: 11px; font-weight: 700; color: #64748B;")
        layout.addWidget(captures_title)

        captures_lbl = QLabel("")
        captures_lbl.setStyleSheet(
            "font-size: 18px; color: #1E293B; font-weight: 600; letter-spacing: 2px;"
        )
        layout.addWidget(captures_lbl)

        return {
            "frame": frame,
            "name": name_lbl,
            "turn_chip": turn_chip,
            "captures_title": captures_title,
            "captures": captures_lbl,
        }

    def update_match_pill(self, game_mode: str, difficulty: str, player_color: chess.Color) -> None:
        self.game_mode = game_mode
        self.difficulty = difficulty
        self.player_color = player_color

        color_str = "White" if player_color == chess.WHITE else "Black"
        if game_mode == "Play vs Computer":
            text = f"⚔️ vs Computer ({difficulty})  •  Playing as {color_str}"
        else:
            text = f"👥 Local 2-Player  •  Perspective: {color_str}"
        self.match_pill.setText(text)

    def update_banners(
        self,
        current_turn: str,
        white_caps: list[str],
        black_caps: list[str],
    ) -> None:
        """Update top and bottom player banner names, turn chips, and captured piece glyphs."""
        white_str = "".join(white_caps)
        black_str = "".join(black_caps)

        is_white_perspective = self.player_color == chess.WHITE
        is_comp = self.game_mode == "Play vs Computer"

        if is_white_perspective:
            top_name = f"Computer ({self.difficulty})" if is_comp else "Black (Player 2)"
            bottom_name = "You (White)" if is_comp else "White (Player 1)"

            top_color = "Black"
            bottom_color = "White"

            # White captures Black pieces -> white_caps belongs to White (bottom)
            top_captured = black_str
            bottom_captured = white_str
        else:
            top_name = "White (Player 1)" if not is_comp else f"Computer (White • {self.difficulty})"
            bottom_name = "You (Black)" if is_comp else "Black (Player 2)"

            top_color = "White"
            bottom_color = "Black"

            top_captured = white_str
            bottom_captured = black_str

        self.top_banner["name"].setText(top_name)
        self.bottom_banner["name"].setText(bottom_name)

        self.top_banner["captures"].setText(top_captured)
        self.bottom_banner["captures"].setText(bottom_captured)

        self.white_captured_tray.setText(white_str)
        self.black_captured_tray.setText(black_str)

        # Update Active Turn Chip
        active_chip_style = (
            "font-size: 11px; font-weight: 700; color: #047857; "
            "background-color: #D1FAE5; border: 1px solid #A7F3D0; "
            "border-radius: 6px; padding: 2px 8px;"
        )

        if current_turn == top_color:
            self.top_banner["turn_chip"].setText("● To Move")
            self.top_banner["turn_chip"].setStyleSheet(active_chip_style)
            self.bottom_banner["turn_chip"].setText("")
            self.bottom_banner["turn_chip"].setStyleSheet("")
        else:
            self.bottom_banner["turn_chip"].setText("● To Move")
            self.bottom_banner["turn_chip"].setStyleSheet(active_chip_style)
            self.top_banner["turn_chip"].setText("")
            self.top_banner["turn_chip"].setStyleSheet("")
