import chess
import pytest

from app.core.chess_game import ChessGame


def test_initial_position():
    game = ChessGame()
    assert game.board == chess.Board()
    assert game.get_status().turn == "White"


def test_legal_move_switches_turn():
    game = ChessGame()
    assert game.make_move("e2e4") == "e4"
    assert game.get_status().turn == "Black"


def test_illegal_move_is_rejected():
    game = ChessGame()
    with pytest.raises(ValueError):
        game.make_move("e2e5")
    assert game.board == chess.Board()


def test_legal_destinations():
    game = ChessGame()
    assert set(game.get_legal_moves("e2")) == {"e3", "e4"}


def test_undo_move():
    game = ChessGame()
    game.make_move("e2e4")
    assert game.undo_move() == "e4"
    assert game.board == chess.Board()
    assert game.get_move_history() == []
