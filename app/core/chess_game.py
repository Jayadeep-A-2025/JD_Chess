"""Core chess game model using python-chess."""

from dataclasses import dataclass
from typing import Optional

import chess


@dataclass(frozen=True)
class GameStatus:
    turn: str
    is_check: bool
    is_checkmate: bool
    is_stalemate: bool
    is_game_over: bool
    result: str
    termination: str


class ChessGame:
    """Manage chess rules and state independently of the GUI."""

    def __init__(self) -> None:
        self.board = chess.Board()
        self._move_history = []

    def new_game(self) -> None:
        """Reset the board and move history."""
        self.board.reset()
        self._move_history.clear()

    def make_move(self, uci_move: str) -> str:
        """Make a legal UCI move and return SAN notation."""
        try:
            move = chess.Move.from_uci(uci_move)
        except ValueError as exc:
            raise ValueError("Invalid move format.") from exc

        if move not in self.board.legal_moves:
            raise ValueError(f"Illegal move: {uci_move}")

        san = self.board.san(move)
        self.board.push(move)
        self._move_history.append(san)
        return san

    def undo_move(self) -> Optional[str]:
        """Undo the last move, if one exists."""
        if not self.board.move_stack:
            return None

        self.board.pop()
        return self._move_history.pop()

    def get_legal_moves(self, square_name: str) -> list:
        """Return legal destination squares for a piece."""
        try:
            square = chess.parse_square(square_name)
        except ValueError as exc:
            raise ValueError(f"Invalid square: {square_name}") from exc

        return [
            chess.square_name(move.to_square)
            for move in self.board.legal_moves
            if move.from_square == square
        ]

    def get_piece(self, square_name: str) -> Optional[str]:
        """Return a piece symbol, or None for an empty square."""
        try:
            square = chess.parse_square(square_name)
        except ValueError as exc:
            raise ValueError(f"Invalid square: {square_name}") from exc

        piece = self.board.piece_at(square)
        return piece.symbol() if piece else None

    def get_move_history(self) -> list:
        """Return a copy of the move history."""
        return self._move_history.copy()

    def get_status(self) -> GameStatus:
        """Report whose turn it is and whether the game has ended."""
        outcome = self.board.outcome()

        if outcome is None:
            result = "*"
            termination = "In progress"
        else:
            result = outcome.result()
            termination = outcome.termination.name.replace(
                "_", " "
            ).title()

        return GameStatus(
            turn="White" if self.board.turn == chess.WHITE else "Black",
            is_check=self.board.is_check(),
            is_checkmate=self.board.is_checkmate(),
            is_stalemate=self.board.is_stalemate(),
            is_game_over=self.board.is_game_over(),
            result=result,
            termination=termination,
        )
