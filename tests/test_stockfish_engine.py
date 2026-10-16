import chess

from app.engine.stockfish_engine import StockfishEngine


def test_difficulty_settings_are_available():
    settings = StockfishEngine.DIFFICULTY_SETTINGS

    assert set(settings) == {"Easy", "Medium", "Hard"}
    assert settings["Easy"]["skill"] < settings["Medium"]["skill"]
    assert settings["Medium"]["skill"] < settings["Hard"]["skill"]


def test_difficulty_thinking_times_increase():
    settings = StockfishEngine.DIFFICULTY_SETTINGS

    assert settings["Easy"]["time"] < settings["Medium"]["time"]
    assert settings["Medium"]["time"] < settings["Hard"]["time"]


def test_engine_returns_no_move_for_finished_game():
    engine = StockfishEngine.__new__(StockfishEngine)
    board = chess.Board("7k/6Q1/6K1/8/8/8/8/8 b - - 0 1")

    assert board.is_game_over()
    assert engine.get_best_move(board) is None
