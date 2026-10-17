from pathlib import Path

import chess

from PySide6.QtCore import QSize, Qt, QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core.chess_game import ChessGame
from app.engine.stockfish_engine import StockfishEngine


PIECE_GLYPHS = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}


def compute_captured_pieces(move_stack):
    """Replay moves on a temporary chess.Board to identify captured pieces in order.

    Returns (white_captures, black_captures) where:
    - white_captures: list of black piece glyphs captured by White
    - black_captures: list of white piece glyphs captured by Black
    """
    temp_board = chess.Board()
    white_captures = []
    black_captures = []

    for move in move_stack:
        captured_glyph = None
        if temp_board.is_en_passant(move):
            cap_square = chess.square(
                chess.square_file(move.to_square),
                chess.square_rank(move.from_square),
            )
            cap_piece = temp_board.piece_at(cap_square)
            if cap_piece:
                captured_glyph = PIECE_GLYPHS.get(cap_piece.symbol(), "")
        elif temp_board.is_capture(move):
            cap_piece = temp_board.piece_at(move.to_square)
            if cap_piece:
                captured_glyph = PIECE_GLYPHS.get(cap_piece.symbol(), "")

        if captured_glyph:
            if temp_board.turn == chess.WHITE:
                white_captures.append(captured_glyph)
            else:
                black_captures.append(captured_glyph)

        temp_board.push(move)

    return white_captures, black_captures


class StockfishWorker(QThread):
    """Background worker that queries Stockfish without blocking the Qt UI thread."""

    move_ready = Signal(int, object)  # (request_id, uci_move_or_None)
    error_occurred = Signal(int, str)  # (request_id, error_message)

    def __init__(self, engine, board_copy, difficulty, request_id, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.board_copy = board_copy
        self.difficulty = difficulty
        self.request_id = request_id

    def run(self):
        try:
            uci_move = self.engine.get_best_move(
                self.board_copy, self.difficulty
            )
            self.move_ready.emit(self.request_id, uci_move)
        except Exception as exc:
            self.error_occurred.emit(self.request_id, str(exc))


class ChessBoardWidget(QWidget):
    """Clickable chessboard with selectable orientation and coordinate labels."""

    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.game = game
        self.player_color = chess.BLACK
        self.selected_square = None
        self.legal_destinations = set()
        self.last_move_squares = set()
        self.square_buttons = {}
        self.rank_labels = []
        self.file_labels = []
        self.coord_margin = 22
        self.outer_margin = 10
        self.square_size = 50

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        # Frame enclosing the 8x8 chessboard and its rank/file coordinates
        self.board_frame = QFrame(self)
        self.board_frame.setObjectName("boardFrame")
        self.board_frame.setStyleSheet(
            """
            QFrame#boardFrame {
                background-color: #E2E8F0;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
            }
            """
        )

        # 8 rank coordinate labels on the left (aligned with rows)
        for row in range(8):
            lbl = QLabel(self.board_frame)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(
                "color: #64748B; font-size: 11px; font-weight: 700;"
            )
            self.rank_labels.append(lbl)

        # 8 file coordinate labels on the bottom (aligned with columns)
        for col in range(8):
            lbl = QLabel(self.board_frame)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(
                "color: #64748B; font-size: 11px; font-weight: 700;"
            )
            self.file_labels.append(lbl)

        # 64 chess squares
        for row in range(8):
            for col in range(8):
                button = QPushButton(self.board_frame)
                button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                button.setMinimumSize(0, 0)
                button.clicked.connect(
                    lambda checked=False, r=row, c=col:
                    self.handle_square_click(r, c)
                )
                self.square_buttons[(row, col)] = button

        self.update_coordinates()
        self.update_square_geometry()
        self.refresh()

    def minimumSizeHint(self):
        return QSize(160, 160)

    def sizeHint(self):
        return QSize(520, 520)

    def get_rank_labels(self):
        """Return list of rank coordinate strings from top to bottom."""
        return [lbl.text() for lbl in self.rank_labels]

    def get_file_labels(self):
        """Return list of file coordinate strings from left to right."""
        return [lbl.text() for lbl in self.file_labels]

    def update_coordinates(self):
        """Update file and rank labels depending on board orientation."""
        if self.player_color == chess.WHITE:
            rank_texts = ["8", "7", "6", "5", "4", "3", "2", "1"]
            file_texts = ["a", "b", "c", "d", "e", "f", "g", "h"]
        else:
            rank_texts = ["1", "2", "3", "4", "5", "6", "7", "8"]
            file_texts = ["h", "g", "f", "e", "d", "c", "b", "a"]

        for i, text in enumerate(rank_texts):
            self.rank_labels[i].setText(text)

        for i, text in enumerate(file_texts):
            self.file_labels[i].setText(text)

    def set_orientation(self, color):
        self.player_color = color
        self.clear_selection()
        self.update_coordinates()
        self.refresh()

    def visual_to_square(self, row, col):
        if self.player_color == chess.WHITE:
            file_index = col
            rank_index = 7 - row
        else:
            file_index = 7 - col
            rank_index = row
        return chess.square(file_index, rank_index)

    def clear_selection(self):
        self.selected_square = None
        self.legal_destinations.clear()

    def handle_square_click(self, row, col):
        window = self.window()

        is_human_turn = getattr(window, "is_human_turn", None)
        if callable(is_human_turn) and not is_human_turn():
            return

        square = self.visual_to_square(row, col)
        piece = self.game.board.piece_at(square)

        if self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            selected_piece = self.game.board.piece_at(self.selected_square)

            if (
                selected_piece is not None
                and selected_piece.piece_type == chess.PAWN
                and chess.square_rank(square) in (0, 7)
            ):
                move = chess.Move(
                    self.selected_square, square, promotion=chess.QUEEN
                )

            if move in self.game.board.legal_moves:
                try:
                    self.game.make_move(move.uci())
                except ValueError:
                    pass
                else:
                    self.clear_selection()
                    self.refresh()
                    on_human_move = getattr(window, "on_human_move_made", None)
                    if callable(on_human_move):
                        on_human_move()
                    return

        if piece is not None and piece.color == self.game.board.turn:
            self.selected_square = square
            self.legal_destinations = set(
                self.game.get_legal_moves(chess.square_name(square))
            )
        else:
            self.clear_selection()

        self.refresh()

    def update_square_geometry(self):
        """Fit square grid and coordinates perfectly within available space."""
        w = self.width()
        h = self.height()
        if w <= 0 or h <= 0:
            w, h = 500, 500

        margin_left = self.coord_margin + self.outer_margin
        margin_right = self.outer_margin
        margin_top = self.outer_margin
        margin_bottom = self.coord_margin + self.outer_margin

        avail_w_for_squares = max(40, w - margin_left - margin_right)
        avail_h_for_squares = max(40, h - margin_top - margin_bottom)

        self.square_size = max(5, min(avail_w_for_squares // 8, avail_h_for_squares // 8))

        grid_pixel_size = self.square_size * 8
        frame_w = margin_left + grid_pixel_size + margin_right
        frame_h = margin_top + grid_pixel_size + margin_bottom

        frame_x = max(0, (w - frame_w) // 2)
        frame_y = max(0, (h - frame_h) // 2)

        self.board_frame.setGeometry(frame_x, frame_y, frame_w, frame_h)

        squares_x = margin_left
        squares_y = margin_top

        # Position rank labels on left (aligned with each row)
        for row in range(8):
            y = squares_y + row * self.square_size
            self.rank_labels[row].setGeometry(
                self.outer_margin, y, self.coord_margin, self.square_size
            )

        # Position file labels on bottom (aligned with each column)
        for col in range(8):
            x = squares_x + col * self.square_size
            self.file_labels[col].setGeometry(
                x, squares_y + grid_pixel_size, self.square_size, self.coord_margin
            )

        # Position 64 square buttons
        for row in range(8):
            for col in range(8):
                btn = self.square_buttons[(row, col)]
                x = squares_x + col * self.square_size
                y = squares_y + row * self.square_size
                btn.setGeometry(x, y, self.square_size, self.square_size)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_square_geometry()
        self.refresh()

    def refresh(self):
        font_size = max(10, int(self.square_size * 0.58))
        last_move = (
            self.game.board.peek() if self.game.board.move_stack else None
        )
        self.last_move_squares = (
            {last_move.from_square, last_move.to_square}
            if last_move
            else set()
        )

        for (row, col), button in self.square_buttons.items():
            square = self.visual_to_square(row, col)
            square_name = chess.square_name(square)
            piece = self.game.board.piece_at(square)

            background = (
                "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
            )

            if square == self.selected_square:
                background = "#BBCB45"
            elif square_name in self.legal_destinations:
                background = "#B86B3A"
            elif square in self.last_move_squares:
                background = "#E6C657"

            button.setText(PIECE_GLYPHS.get(piece.symbol(), "") if piece else "")
            
            # High-contrast piece coloring: crisp dark tone for white coins to ensure 100% visibility
            piece_color = "#1E293B" if piece and piece.color == chess.WHITE else "#0F172A"
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {background};
                    color: {piece_color};
                    border: none;
                    border-radius: 0px;
                    font-size: {font_size}px;
                    font-weight: bold;
                    padding: 0px;
                }}
                QPushButton:hover {{
                    border: 2px solid #667085;
                }}
                """
            )


class MainWindow(QMainWindow):
    """Main application window."""

    LOCAL_MODE = "Local 2-player"
    COMPUTER_MODE = "Play vs Stockfish"
    POST_THINKING_DELAY_MS: int = 1500

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JD Chess")
        self.resize(1040, 740)
        self.setMinimumSize(600, 450)

        self.game = ChessGame()
        self.engine = None
        self.engine_error = None
        self.player_color = chess.BLACK

        # Async Stockfish worker and post-thinking delay state
        self._computer_request_id = 0
        self._stockfish_worker = None
        self._pending_computer_move = None
        self._shutting_down = False
        self._computer_delay_timer = QTimer(self)
        self._computer_delay_timer.setSingleShot(True)
        self._computer_delay_timer.timeout.connect(
            self._on_computer_delay_timeout
        )

        # Captured pieces lists
        self.white_captured_pieces = []
        self.black_captured_pieces = []

        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(24)

        # Board container with top and bottom captured-piece trays
        self.board_container = QWidget()
        self.board_column = QVBoxLayout(self.board_container)
        self.board_column.setContentsMargins(0, 0, 0, 0)
        self.board_column.setSpacing(8)

        self.white_tray_frame, self.white_captured_tray = (
            self._create_capture_tray(
                "White Captures:",
                "whiteCapturedTray",
                "Black pieces captured by White",
            )
        )
        self.black_tray_frame, self.black_captured_tray = (
            self._create_capture_tray(
                "Black Captures:",
                "blackCapturedTray",
                "White pieces captured by Black",
            )
        )

        self.board_widget = ChessBoardWidget(self.game)
        self.update_tray_layout()
        root_layout.addWidget(self.board_container, 3)

        side_panel = QWidget()
        side_panel.setMinimumWidth(280)
        side_layout = QVBoxLayout(side_panel)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(12)

        # Header Title and Engine status
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        title = QLabel("JD CHESS")
        title.setStyleSheet(
            "font-size: 26px; font-weight: 800; color: #0F172A; letter-spacing: 0.5px;"
        )
        header_layout.addWidget(title)

        detected_engine = StockfishEngine.find_engine()
        if detected_engine:
            self.engine_badge = QLabel("● Stockfish Ready")
            self.engine_badge.setToolTip(f"Engine path: {detected_engine}")
            self.engine_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #15803D; "
                "background-color: #DCFCE7; border: 1px solid #86EFAC; "
                "border-radius: 10px; padding: 2px 10px; max-width: 140px;"
            )
        else:
            self.engine_badge = QLabel("⚠ Stockfish Not Found")
            self.engine_badge.setToolTip("Install Stockfish to play against the computer.")
            self.engine_badge.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #B91C1C; "
                "background-color: #FEE2E2; border: 1px solid #FCA5A5; "
                "border-radius: 10px; padding: 2px 10px; max-width: 155px;"
            )
        header_layout.addWidget(self.engine_badge)
        side_layout.addLayout(header_layout)

        # Styling for combo boxes and labels
        icons_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
        chevron_path = (icons_dir / "chevron-down.svg").as_posix()
        combo_style = f"""
            QComboBox {{
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1.5px solid #CBD5E1;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
                font-weight: 500;
                min-height: 24px;
            }}
            QComboBox:hover {{
                border-color: #94A3B8;
            }}
            QComboBox:focus {{
                border-color: #2563EB;
            }}
            QComboBox:disabled {{
                background-color: #F1F5F9;
                color: #94A3B8;
                border-color: #E2E8F0;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border-left: 1px solid #E2E8F0;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
            QComboBox::down-arrow {{
                image: url("{chevron_path}");
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                selection-background-color: #2563EB;
                selection-color: #FFFFFF;
                padding: 4px;
                outline: none;
            }}
        """

        # MATCH SETUP CARD
        setup_card = QFrame()
        setup_card.setObjectName("setupCard")
        setup_card.setStyleSheet(
            """
            QFrame#setupCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            """
        )
        setup_layout = QVBoxLayout(setup_card)
        setup_layout.setContentsMargins(14, 14, 14, 14)
        setup_layout.setSpacing(10)

        setup_title = QLabel("MATCH SETUP")
        setup_title.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #64748B; letter-spacing: 0.5px;"
        )
        setup_layout.addWidget(setup_title)

        # Mode Selection
        self.mode_label = QLabel("Game Mode")
        self.mode_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #1E293B;")
        setup_layout.addWidget(self.mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([self.LOCAL_MODE, self.COMPUTER_MODE])
        self.mode_combo.setStyleSheet(combo_style)
        setup_layout.addWidget(self.mode_combo)

        # Color Selection
        self.color_label = QLabel("Play As (Perspective)")
        self.color_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #1E293B;")
        setup_layout.addWidget(self.color_label)

        self.color_combo = QComboBox()
        self.color_combo.addItems(["Black", "White"])
        self.color_combo.setCurrentText("Black")
        self.color_combo.setStyleSheet(combo_style)
        setup_layout.addWidget(self.color_combo)

        # Difficulty Selection
        self.difficulty_label = QLabel("Computer Difficulty")
        self.difficulty_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #1E293B;")
        setup_layout.addWidget(self.difficulty_label)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setCurrentText("Medium")
        self.difficulty_combo.setStyleSheet(combo_style)
        setup_layout.addWidget(self.difficulty_combo)

        self.difficulty_hint = QLabel("(Select 'Play vs Stockfish' above to play against AI)")
        self.difficulty_hint.setWordWrap(True)
        self.difficulty_hint.setStyleSheet("font-size: 11px; color: #64748B;")
        setup_layout.addWidget(self.difficulty_hint)

        side_layout.addWidget(setup_card)

        # GAME STATUS CARD
        status_card = QFrame()
        status_card.setObjectName("statusCard")
        status_card.setStyleSheet(
            """
            QFrame#statusCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            """
        )
        status_card_layout = QVBoxLayout(status_card)
        status_card_layout.setContentsMargins(14, 14, 14, 14)
        status_card_layout.setSpacing(6)

        self.turn_label = QLabel()
        self.turn_label.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #0F172A;"
        )
        status_card_layout.addWidget(self.turn_label)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 13px; color: #475569; line-height: 1.4;")
        status_card_layout.addWidget(self.status_label)

        side_layout.addWidget(status_card)

        # ACTION BUTTONS
        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        self.new_game_button = QPushButton("New Game")
        self.undo_button = QPushButton("Undo Move")

        self.new_game_button.setMinimumHeight(38)
        self.new_game_button.setCursor(Qt.CursorShape.PointingHandCursor)
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

        self.undo_button.setMinimumHeight(38)
        self.undo_button.setCursor(Qt.CursorShape.PointingHandCursor)
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

        self.new_game_button.clicked.connect(self.start_new_game)
        self.undo_button.clicked.connect(self.undo_move)

        button_row.addWidget(self.new_game_button)
        button_row.addWidget(self.undo_button)
        side_layout.addLayout(button_row)

        # MOVE HISTORY
        history_card = QFrame()
        history_card.setObjectName("historyCard")
        history_card.setStyleSheet(
            """
            QFrame#historyCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            """
        )
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(14, 14, 14, 14)
        history_layout.setSpacing(8)

        moves_title = QLabel("MOVE HISTORY")
        moves_title.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #64748B; letter-spacing: 0.5px;"
        )
        history_layout.addWidget(moves_title)

        self.moves_label = QLabel("No moves yet")
        self.moves_label.setWordWrap(True)
        self.moves_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
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
            }
            """
        )
        history_layout.addWidget(self.moves_label)
        side_layout.addWidget(history_card)

        side_layout.addStretch(1)

        sidebar_scroll = QScrollArea()
        sidebar_scroll.setWidget(side_panel)
        sidebar_scroll.setWidgetResizable(True)
        sidebar_scroll.setMinimumWidth(280)
        sidebar_scroll.setFrameShape(QFrame.Shape.NoFrame)
        sidebar_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        sidebar_scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
        )
        sidebar_scroll.viewport().setStyleSheet("background: transparent;")
        root_layout.addWidget(sidebar_scroll, 1)

        self.setStyleSheet("QMainWindow { background-color: #F8FAFC; }")

        self.mode_combo.currentTextChanged.connect(self.change_mode)
        self.color_combo.currentTextChanged.connect(self.change_color)
        self.difficulty_combo.currentTextChanged.connect(
            self.update_game_info
        )

        self.update_mode_controls()
        self.update_game_info()

    def _create_capture_tray(self, title_text: str, object_name: str, tooltip: str):
        """Create a styled captured-piece tray frame with label."""
        tray_frame = QFrame()
        tray_frame.setObjectName(f"{object_name}Frame")
        tray_frame.setFixedHeight(36)
        tray_frame.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
            """
        )
        layout = QHBoxLayout(tray_frame)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)

        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #64748B; letter-spacing: 0.5px;"
        )
        layout.addWidget(title_lbl)

        glyphs_lbl = QLabel("")
        glyphs_lbl.setObjectName(object_name)
        glyphs_lbl.setToolTip(tooltip)
        glyphs_lbl.setStyleSheet(
            "font-size: 19px; color: #1E293B; font-weight: 600; letter-spacing: 2px;"
        )
        layout.addWidget(glyphs_lbl, 1)

        return tray_frame, glyphs_lbl

    def update_tray_layout(self):
        """Arrange capture trays to reflect board perspective."""
        self.board_column.removeWidget(self.white_tray_frame)
        self.board_column.removeWidget(self.board_widget)
        self.board_column.removeWidget(self.black_tray_frame)

        if self.player_color == chess.WHITE:
            # When playing as White: Black's captures at top, White's at bottom
            self.board_column.addWidget(self.black_tray_frame)
            self.board_column.addWidget(self.board_widget, 1)
            self.board_column.addWidget(self.white_tray_frame)
        else:
            # When playing as Black: White's captures at top, Black's at bottom
            self.board_column.addWidget(self.white_tray_frame)
            self.board_column.addWidget(self.board_widget, 1)
            self.board_column.addWidget(self.black_tray_frame)

    def get_captured_pieces(self):
        """Return tuple of (white_captured_glyphs, black_captured_glyphs)."""
        return list(self.white_captured_pieces), list(self.black_captured_pieces)

    def update_mode_controls(self):
        is_comp = self.is_computer_mode()
        self.difficulty_combo.setEnabled(is_comp)
        if is_comp:
            self.color_label.setText("Play As (Human Color)")
            self.difficulty_label.setStyleSheet(
                "font-size: 13px; font-weight: 600; color: #1E293B;"
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
                "font-size: 13px; font-weight: 600; color: #94A3B8;"
            )
            self.difficulty_hint.setText(
                "(Select 'Play vs Stockfish' above to play against AI)"
            )
            self.difficulty_hint.setStyleSheet(
                "font-size: 11px; color: #64748B;"
            )

    def is_computer_mode(self):
        return self.mode_combo.currentText() == self.COMPUTER_MODE

    def is_computer_thinking_or_pending(self):
        """Return True if Stockfish is currently calculating or delay timer is active."""
        worker_running = (
            self._stockfish_worker is not None
            and self._stockfish_worker.isRunning()
        )
        timer_running = self._computer_delay_timer.isActive()
        return worker_running or timer_running

    def is_human_turn(self):
        if not self.is_computer_mode():
            return True
        if self.is_computer_thinking_or_pending():
            return False
        return self.game.board.turn == self.player_color

    def cancel_pending_computer_move(self):
        """Cancel any in-flight search, delay timer, or queued move."""
        self._computer_request_id += 1
        self._pending_computer_move = None
        if self._computer_delay_timer.isActive():
            self._computer_delay_timer.stop()

    def change_mode(self, mode):
        self.cancel_pending_computer_move()
        if mode == self.COMPUTER_MODE and self.engine is None:
            try:
                self.engine = StockfishEngine()
                self.engine_error = None
            except Exception as exc:
                self.engine_error = str(exc)
                QMessageBox.warning(
                    self,
                    "Stockfish unavailable",
                    "JD Chess could not start Stockfish.\n\n"
                    f"{exc}\n\n"
                    "Install Stockfish and try again.",
                )
                self.mode_combo.blockSignals(True)
                self.mode_combo.setCurrentText(self.LOCAL_MODE)
                self.mode_combo.blockSignals(False)
                self.update_mode_controls()
                self.update_game_info()
                return

        if mode == self.LOCAL_MODE:
            self.close_engine()

        self.update_mode_controls()
        self.start_new_game()

    def change_color(self, color_name):
        self.cancel_pending_computer_move()
        self.player_color = (
            chess.WHITE if color_name == "White" else chess.BLACK
        )
        self.board_widget.set_orientation(self.player_color)
        self.update_tray_layout()
        self.start_new_game()

    def close_engine(self):
        self.cancel_pending_computer_move()

        worker = self._stockfish_worker
        if worker is not None and worker.isRunning():
            # Never close the engine while its worker is using it.
            # This waits for the current search to finish safely.
            worker.wait()

        self._stockfish_worker = None

        if self.engine is not None:
            try:
                self.engine.close()
            except Exception:
                pass
            self.engine = None

    def start_new_game(self):
        self.cancel_pending_computer_move()
        self.game.new_game()
        self.board_widget.clear_selection()
        self.board_widget.set_orientation(self.player_color)
        self.board_widget.refresh()
        self.update_game_info()

        if (
            self.is_computer_mode()
            and self.player_color == chess.BLACK
        ):
            self.make_computer_move()

    def on_human_move_made(self):
        self.update_game_info()

        if self.is_computer_mode() and not self.game.board.is_game_over():
            self.make_computer_move()

    def make_computer_move(self):
        if self.engine is None or self.game.board.is_game_over():
            self.update_game_info()
            return

        if self.game.board.turn == self.player_color:
            self.update_game_info()
            return

        if self.is_computer_thinking_or_pending():
            return

        self._computer_request_id += 1
        req_id = self._computer_request_id

        # Pass a copy of the board to the background worker to protect live state
        board_copy = self.game.board.copy()
        difficulty = self.difficulty_combo.currentText()

        self.status_label.setText("Stockfish is thinking...")

        self._stockfish_worker = StockfishWorker(
            self.engine, board_copy, difficulty, req_id, parent=self
        )
        self._stockfish_worker.move_ready.connect(self._on_computer_move_ready)
        self._stockfish_worker.error_occurred.connect(self._on_computer_error)
        self._stockfish_worker.finished.connect(
            self._on_stockfish_worker_finished
        )
        self._stockfish_worker.start()

    def _on_stockfish_worker_finished(self):
        worker = self.sender()

        # Ignore callbacks from workers that have already been retired.
        if worker is not self._stockfish_worker:
            return

        worker_req_id = getattr(worker, "request_id", None)
        request_was_stale = (
            worker_req_id != self._computer_request_id
        )
        self._stockfish_worker = None

        if self._shutting_down or not request_was_stale:
            return

        # A restart, undo, or other state change invalidated the old search.
        # If the current board still needs a computer move, search again.
        if (
            self.is_computer_mode()
            and not self.game.board.is_game_over()
            and self.game.board.turn != self.player_color
            and self._pending_computer_move is None
            and not self._computer_delay_timer.isActive()
        ):
            self.make_computer_move()

    def _on_computer_move_ready(self, req_id, uci_move):
        # Ignore stale results from previous/cancelled requests
        if req_id != self._computer_request_id:
            return

        if not self.is_computer_mode() or self.game.board.is_game_over():
            return

        if uci_move is None:
            self.update_game_info()
            return

        self._pending_computer_move = uci_move
        delay = getattr(self, "POST_THINKING_DELAY_MS", 2000)
        if delay <= 0:
            self._on_computer_delay_timeout()
        else:
            self.status_label.setText("Stockfish is thinking...")
            self._computer_delay_timer.start(delay)

    def _on_computer_delay_timeout(self):
        if self._pending_computer_move is None:
            return

        uci_move = self._pending_computer_move
        self._pending_computer_move = None

        if not self.is_computer_mode() or self.game.board.is_game_over():
            self.update_game_info()
            return

        if self.game.board.turn == self.player_color:
            self.update_game_info()
            return

        try:
            move = chess.Move.from_uci(uci_move)
            if move in self.game.board.legal_moves:
                self.game.make_move(uci_move)
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Computer move failed",
                f"Stockfish move was invalid:\n{exc}",
            )

        self.board_widget.clear_selection()
        self.update_game_info()

    def _on_computer_error(self, req_id, error_msg):
        if req_id != self._computer_request_id:
            return

        self._pending_computer_move = None
        QMessageBox.warning(
            self,
            "Computer move failed",
            f"Stockfish could not make a move:\n{error_msg}",
        )
        self.board_widget.clear_selection()
        self.update_game_info()

    def update_game_info(self, *_):
        status = self.game.get_status()

        if status.is_game_over:
            if status.is_checkmate:
                message = f"Checkmate! {status.turn} has no legal move."
            elif status.is_stalemate:
                message = "Draw by stalemate."
            else:
                message = f"Game over: {status.termination}."
        elif status.is_check:
            message = f"⚠ {status.turn} is in check!"
        elif self.is_computer_mode() and not self.is_human_turn():
            message = "Stockfish is thinking..."
        elif self.is_computer_mode():
            color_text = "White" if self.player_color == chess.WHITE else "Black"
            diff_text = self.difficulty_combo.currentText()
            message = f"Your turn ({color_text}) vs Stockfish ({diff_text})."
        else:
            message = "Select a piece to see its legal moves."

        turn_symbol = "⚪" if status.turn == "White" else "⚫"
        self.turn_label.setText(f"{turn_symbol} {status.turn} to move")
        self.status_label.setText(message)

        history = self.game.get_move_history()
        if not history:
            self.moves_label.setText("No moves yet")
        else:
            formatted = []
            for index in range(0, len(history), 2):
                white_move = history[index]
                black_move = (
                    history[index + 1] if index + 1 < len(history) else ""
                )
                formatted.append(
                    f"{index // 2 + 1}. {white_move}  {black_move}"
                )
            self.moves_label.setText("\n".join(formatted))

        # Reconstruct captured pieces without mutating the live game board
        white_caps, black_caps = compute_captured_pieces(
            self.game.board.move_stack
        )
        self.white_captured_pieces = white_caps
        self.black_captured_pieces = black_caps
        self.white_captured_tray.setText(" ".join(white_caps))
        self.black_captured_tray.setText(" ".join(black_caps))

        self.board_widget.refresh()

    def undo_move(self):
        computer_mode = self.is_computer_mode()
        human_turn_before_undo = (
            self.game.board.turn == self.player_color
        )
        move_count = len(self.game.board.move_stack)

        # Invalidate any search or delayed move before changing the board.
        self.cancel_pending_computer_move()

        if computer_mode:
            if human_turn_before_undo:
                # Normally undo the computer's move and the previous human move.
                # If only the computer's opening exists, undo just that move.
                moves_to_undo = 2 if move_count >= 2 else move_count
            else:
                # The human just moved and the computer is thinking or responding.
                moves_to_undo = 1 if move_count else 0

            for _ in range(moves_to_undo):
                if self.game.board.move_stack:
                    self.game.undo_move()
        elif self.game.board.move_stack:
            self.game.undo_move()

        self.board_widget.clear_selection()
        self.update_game_info()

        # If undo leaves the computer to move, request a fresh search.
        # An active stale worker will trigger this when it finishes.
        if (
            computer_mode
            and not self.game.board.is_game_over()
            and self.game.board.turn != self.player_color
        ):
            self.make_computer_move()

    def closeEvent(self, event):
        self._shutting_down = True
        self.close_engine()
        event.accept()