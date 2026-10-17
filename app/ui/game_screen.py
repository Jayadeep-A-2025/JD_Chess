from __future__ import annotations

"""Window 3: Chess Board Game Screen with optimized layout, banners, and sidebar."""

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


class GameScreen(QWidget):
    """Clean, focused chess board screen with player banners and sidebar history."""

    save_game_clicked = Signal()
    undo_move_clicked = Signal()
    restart_game_clicked = Signal()
    main_menu_clicked = Signal()

    def __init__(self, game: ChessGame, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.game = game
        self.player_color = chess.BLACK
        self.game_mode = "Play vs Computer"
        self.difficulty = "Medium"

        self.setStyleSheet("QWidget { background-color: #F8FAFC; }")

        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(20, 16, 20, 16)
        main_vbox.setSpacing(14)

        # TOP BAR: Navigation, Match Info Pill, Quick Actions
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)

        self.menu_button = QPushButton("← Main Menu")
        self.menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_button.setStyleSheet(
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
        self.menu_button.clicked.connect(self.main_menu_clicked.emit)
        top_bar.addWidget(self.menu_button)

        self.match_pill = QLabel("Match in Progress")
        self.match_pill.setStyleSheet(
            "font-size: 12px; font-weight: 700; color: #1E293B; "
            "background-color: #EFF6FF; border: 1px solid #BFDBFE; "
            "border-radius: 12px; padding: 4px 14px;"
        )
        top_bar.addWidget(self.match_pill)

        top_bar.addStretch(1)

        self.save_button = QPushButton("💾 Save Game")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #10B981;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #059669; }
            """
        )
        self.save_button.clicked.connect(self.save_game_clicked.emit)
        top_bar.addWidget(self.save_button)

        main_vbox.addLayout(top_bar)

        # MAIN CONTENT ROW: Board Column (3) + Sidebar (1)
        content_row = QHBoxLayout()
        content_row.setSpacing(24)

        # BOARD COLUMN
        self.board_column_widget = QWidget()
        board_col_layout = QVBoxLayout(self.board_column_widget)
        board_col_layout.setContentsMargins(0, 0, 0, 0)
        board_col_layout.setSpacing(10)

        # Top Player Banner (Opponent)
        self.top_banner = self._create_player_banner("top")
        board_col_layout.addWidget(self.top_banner["frame"])

        # Chess Board Widget
        self.board_widget = ChessBoardWidget(self.game, parent=self)
        board_col_layout.addWidget(self.board_widget, 1)

        # Bottom Player Banner (User / Player 1)
        self.bottom_banner = self._create_player_banner("bottom")
        board_col_layout.addWidget(self.bottom_banner["frame"])

        content_row.addWidget(self.board_column_widget, 3)

        # SIDEBAR COLUMN
        sidebar_panel = QWidget()
        sidebar_panel.setMinimumWidth(280)
        sidebar_layout = QVBoxLayout(sidebar_panel)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(12)

        # Header Title
        title_lbl = QLabel("MATCH CONTROLS")
        title_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #64748B; letter-spacing: 0.5px;"
        )
        sidebar_layout.addWidget(title_lbl)

        # STATUS CARD
        status_card = QFrame()
        status_card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            """
        )
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(14, 14, 14, 14)
        status_layout.setSpacing(6)

        self.turn_label = QLabel()
        self.turn_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #0F172A;")
        status_layout.addWidget(self.turn_label)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 13px; color: #475569; line-height: 1.4;")
        status_layout.addWidget(self.status_label)

        sidebar_layout.addWidget(status_card)

        # ACTION BUTTONS ROW
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.new_game_button = QPushButton("New Match")
        self.new_game_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_game_button.setMinimumHeight(38)
        self.new_game_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2563EB;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #1D4ED8; }
            QPushButton:pressed { background-color: #1E40AF; }
            """
        )
        self.new_game_button.clicked.connect(self.restart_game_clicked.emit)

        self.undo_button = QPushButton("Undo Move")
        self.undo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.undo_button.setMinimumHeight(38)
        self.undo_button.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #334155;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #F8FAFC; border-color: #94A3B8; }
            QPushButton:pressed { background-color: #F1F5F9; }
            """
        )
        self.undo_button.clicked.connect(self.undo_move_clicked.emit)

        btn_row.addWidget(self.new_game_button)
        btn_row.addWidget(self.undo_button)
        sidebar_layout.addLayout(btn_row)

        # MOVE HISTORY CARD
        history_card = QFrame()
        history_card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            """
        )
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(14, 14, 14, 14)
        history_layout.setSpacing(8)

        history_title = QLabel("MOVE HISTORY")
        history_title.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #64748B; letter-spacing: 0.5px;"
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
                color: #334155;
                border: 1px solid #F1F5F9;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                font-family: Menlo, Monaco, "Courier New", monospace;
                min-height: 120px;
            }
            """
        )
        self.history_scroll.setWidget(self.moves_label)
        history_layout.addWidget(self.history_scroll, 1)

        sidebar_layout.addWidget(history_card, 1)

        content_row.addWidget(sidebar_panel, 1)
        main_vbox.addLayout(content_row, 1)

        # Expose references for backwards compatibility
        self.white_captured_tray = QLabel("")
        self.black_captured_tray = QLabel("")

    def _create_player_banner(self, position: str) -> dict:
        frame = QFrame()
        frame.setObjectName(f"{position}PlayerBanner")
        frame.setFixedHeight(48)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
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
            "font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 6px;"
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
        white_captures: list[str],
        black_captures: list[str],
    ) -> None:
        """Update top and bottom banners based on perspective and current turn."""
        is_comp = self.game_mode == "Play vs Computer"
        
        # When player is White:
        # Top banner = Black (Opponent/Computer), displays Black captures (White pieces captured by Black)
        # Bottom banner = White (Player 1), displays White captures (Black pieces captured by White)
        # When player is Black:
        # Top banner = White (Opponent/Computer), displays White captures
        # Bottom banner = Black (Player 1), displays Black captures

        if self.player_color == chess.WHITE:
            top_color_str = "Black"
            top_name = "🤖 Computer (Black)" if is_comp else "👥 Player 2 (Black)"
            top_caps = black_captures

            bottom_color_str = "White"
            bottom_name = "👤 You (White)" if is_comp else "👤 Player 1 (White)"
            bottom_caps = white_captures
        else:
            top_color_str = "White"
            top_name = "🤖 Computer (White)" if is_comp else "👥 Player 2 (White)"
            top_caps = white_captures

            bottom_color_str = "Black"
            bottom_name = "👤 You (Black)" if is_comp else "👤 Player 1 (Black)"
            bottom_caps = black_captures

        # Top Banner update
        self.top_banner["name"].setText(top_name)
        self.top_banner["captures"].setText(" ".join(top_caps))
        if current_turn == top_color_str:
            self.top_banner["turn_chip"].setText("● To Move")
            self.top_banner["turn_chip"].setStyleSheet(
                "font-size: 11px; font-weight: 700; color: #2563EB; "
                "background-color: #EFF6FF; border: 1px solid #BFDBFE; "
                "border-radius: 6px; padding: 2px 8px;"
            )
            self.top_banner["frame"].setStyleSheet(
                "QFrame { background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 10px; }"
            )
        else:
            self.top_banner["turn_chip"].setText("")
            self.top_banner["frame"].setStyleSheet(
                "QFrame { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; }"
            )

        # Bottom Banner update
        self.bottom_banner["name"].setText(bottom_name)
        self.bottom_banner["captures"].setText(" ".join(bottom_caps))
        if current_turn == bottom_color_str:
            self.bottom_banner["turn_chip"].setText("● To Move")
            self.bottom_banner["turn_chip"].setStyleSheet(
                "font-size: 11px; font-weight: 700; color: #2563EB; "
                "background-color: #EFF6FF; border: 1px solid #BFDBFE; "
                "border-radius: 6px; padding: 2px 8px;"
            )
            self.bottom_banner["frame"].setStyleSheet(
                "QFrame { background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 10px; }"
            )
        else:
            self.bottom_banner["turn_chip"].setText("")
            self.bottom_banner["frame"].setStyleSheet(
                "QFrame { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; }"
            )

        # Synchronize backward-compatible tray labels
        self.white_captured_tray.setText(" ".join(white_captures))
        self.black_captured_tray.setText(" ".join(black_captures))
