from __future__ import annotations

"""Chessboard widget with coordinate labels, highlighting, and responsive sizing."""

import chess
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from app.core.chess_game import ChessGame

PIECE_GLYPHS = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}


def compute_captured_pieces(move_stack: list[chess.Move]) -> tuple[list[str], list[str]]:
    """Replay moves on a temporary chess.Board to identify captured pieces in order.

    Returns (white_captures, black_captures) where:
    - white_captures: list of black piece glyphs captured by White
    - black_captures: list of white piece glyphs captured by Black
    """
    temp_board = chess.Board()
    white_captures: list[str] = []
    black_captures: list[str] = []

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


class ChessBoardWidget(QWidget):
    """Clickable chessboard with selectable orientation and coordinate labels."""

    move_made = Signal(str)

    def __init__(self, game: ChessGame, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.game = game
        self.player_color = chess.BLACK
        self.selected_square = None
        self.legal_destinations = set()
        self.last_move_squares = set()
        self.square_buttons: dict[tuple[int, int], QPushButton] = {}
        self.rank_labels: list[QLabel] = []
        self.file_labels: list[QLabel] = []
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

    def minimumSizeHint(self) -> QSize:
        return QSize(160, 160)

    def sizeHint(self) -> QSize:
        return QSize(520, 520)

    def get_rank_labels(self) -> list[str]:
        """Return list of rank coordinate strings from top to bottom."""
        return [lbl.text() for lbl in self.rank_labels]

    def get_file_labels(self) -> list[str]:
        """Return list of file coordinate strings from left to right."""
        return [lbl.text() for lbl in self.file_labels]

    def update_coordinates(self) -> None:
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

    def set_orientation(self, color: chess.Color) -> None:
        self.player_color = color
        self.clear_selection()
        self.update_coordinates()
        self.refresh()

    def visual_to_square(self, row: int, col: int) -> chess.Square:
        if self.player_color == chess.WHITE:
            file_index = col
            rank_index = 7 - row
        else:
            file_index = 7 - col
            rank_index = row
        return chess.square(file_index, rank_index)

    def clear_selection(self) -> None:
        self.selected_square = None
        self.legal_destinations.clear()

    def handle_square_click(self, row: int, col: int) -> None:
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
                    self.move_made.emit(move.uci())
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

    def update_square_geometry(self) -> None:
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

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.update_square_geometry()
        self.refresh()

    def refresh(self) -> None:
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
