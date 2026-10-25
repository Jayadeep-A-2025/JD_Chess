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


def test_find_engine_in_pyinstaller_bundle(monkeypatch, tmp_path):
    import sys

    bundle_dir = tmp_path / "bundle"
    engine_path = bundle_dir / "assets" / "stockfish"
    engine_path.parent.mkdir(parents=True)
    engine_path.write_text("fake engine")

    monkeypatch.setattr(sys, "_MEIPASS", str(bundle_dir), raising=False)
    monkeypatch.setattr(
        "app.engine.stockfish_engine.shutil.which",
        lambda name: None,
    )

    assert ComputerEngine.find_engine() == str(engine_path)


def test_find_engine_in_macos_app_resources(monkeypatch, tmp_path):
    import sys

    executable_dir = tmp_path / "JD_Chess.app" / "Contents" / "MacOS"
    executable_dir.mkdir(parents=True)

    engine_path = (
        tmp_path / "JD_Chess.app" / "Contents"
        / "Resources" / "assets" / "stockfish"
    )
    engine_path.parent.mkdir(parents=True)
    engine_path.write_text("fake engine")

    monkeypatch.setattr(sys, "executable", str(executable_dir / "JD_Chess"))
    monkeypatch.delattr(sys, "_MEIPASS", raising=False)

    # Prevent this test from finding Stockfish installed on the host Mac.
    monkeypatch.setattr(
        "app.engine.stockfish_engine.shutil.which",
        lambda name: None,
    )
    monkeypatch.setattr(
        "app.engine.stockfish_engine.os.path.isfile",
        lambda path: str(path) == str(engine_path),
    )

    assert ComputerEngine.find_engine() == str(engine_path)
