from __future__ import annotations

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


def test_new_game_resets_history():
    game = ChessGame()
    game.make_move("e2e4")
    game.new_game()

    assert game.board == chess.Board()
    assert game.get_move_history() == []


def test_castling():
    game = ChessGame()

    for move in [
        "e2e4", "e7e5",
        "g1f3", "b8c6",
        "f1c4", "g8f6",
    ]:
        game.make_move(move)

    game.make_move("e1g1")

    assert game.get_piece("g1") == "K"
    assert game.get_piece("f1") == "R"


def test_en_passant():
    game = ChessGame()

    for move in ["e2e4", "a7a6", "e4e5", "d7d5", "e5d6"]:
        game.make_move(move)

    assert game.get_piece("d6") == "P"
    assert game.get_piece("d5") is None


def test_pawn_promotion():
    game = ChessGame()
    game.board.set_fen("7k/P7/8/8/8/8/8/7K w - - 0 1")

    game.make_move("a7a8q")

    assert game.get_piece("a8") == "Q"


def test_checkmate():
    game = ChessGame()

    for move in ["f2f3", "e7e5", "g2g4", "d8h4"]:
        game.make_move(move)

    assert game.get_status().is_checkmate
    assert game.get_status().result == "0-1"


def test_stalemate():
    game = ChessGame()
    game.board.set_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")

    status = game.get_status()

    assert status.is_stalemate
    assert status.result == "1/2-1/2"
    