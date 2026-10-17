from __future__ import annotations

import chess

from app.engine.stockfish_engine import ComputerEngine, StockfishEngine


def test_difficulty_settings_are_available():
    settings = ComputerEngine.DIFFICULTY_SETTINGS

    assert set(settings) == {"Easy", "Medium", "Hard"}
    assert settings["Easy"]["skill"] < settings["Medium"]["skill"]
    assert settings["Medium"]["skill"] < settings["Hard"]["skill"]
    assert StockfishEngine.DIFFICULTY_SETTINGS == ComputerEngine.DIFFICULTY_SETTINGS


def test_difficulty_thinking_times_increase():
    settings = ComputerEngine.DIFFICULTY_SETTINGS

    assert settings["Easy"]["time"] < settings["Medium"]["time"]
    assert settings["Medium"]["time"] < settings["Hard"]["time"]


def test_engine_returns_no_move_for_finished_game():
    engine = ComputerEngine.__new__(ComputerEngine)
    board = chess.Board("7k/6Q1/6K1/8/8/8/8/8 b - - 0 1")

    assert board.is_game_over()
    assert engine.get_best_move(board) is None
