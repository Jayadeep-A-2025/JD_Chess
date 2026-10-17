from __future__ import annotations

"""Computer UCI engine integration."""

import os
import shutil
import sys

import chess
import chess.engine


class ComputerEngine:
    """Manage a Computer chess engine process and request computer moves."""

    DIFFICULTY_SETTINGS = {
        "Easy": {"time": 0.15, "skill": 1},
        "Medium": {"time": 0.50, "skill": 8},
        "Hard": {"time": 1.20, "skill": 20},
    }

    def __init__(self, engine_path: str | None = None) -> None:
        self.engine_path = engine_path or self.find_engine()
        if not self.engine_path:
            raise FileNotFoundError(
                "Computer engine was not found. Install it or set COMPUTER_PATH or STOCKFISH_PATH."
            )

        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)

    @staticmethod
    def find_engine() -> str | None:
        """Find Computer engine in configured, bundled, or system locations."""
        configured_path = os.environ.get("COMPUTER_PATH") or os.environ.get("STOCKFISH_PATH")
        if configured_path and os.path.isfile(configured_path):
            return configured_path

        bundle_dir = getattr(sys, "_MEIPASS", None)
        executable_dir = os.path.dirname(os.path.abspath(sys.executable))
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        candidates = []

        if bundle_dir:
            candidates.extend([
                os.path.join(bundle_dir, "assets", "stockfish"),
                os.path.join(bundle_dir, "assets", "stockfish.exe"),
            ])

        candidates.extend([
            os.path.join(executable_dir, "assets", "stockfish"),
            os.path.join(executable_dir, "assets", "stockfish.exe"),
            os.path.join(executable_dir, "stockfish"),
            os.path.join(executable_dir, "stockfish.exe"),
            os.path.join(project_root, "assets", "stockfish"),
            os.path.join(project_root, "assets", "stockfish.exe"),
        ])

        for candidate in candidates:
            if os.path.isfile(candidate):
                return candidate

        discovered = shutil.which("stockfish")
        if discovered:
            return discovered

        if os.name == "nt":
            discovered = shutil.which("stockfish.exe")
            if discovered:
                return discovered

        for candidate in (
            "/opt/homebrew/bin/stockfish",
            "/usr/local/bin/stockfish",
            "/usr/bin/stockfish",
            "/usr/games/stockfish",
        ):
            if os.path.isfile(candidate):
                return candidate

        return None

    def get_best_move(self, board: chess.Board, difficulty: str = "Medium") -> str | None:
        engine = getattr(self, "engine", None)
        if engine is None or board.is_game_over():
            return None
        settings = self.DIFFICULTY_SETTINGS.get(
            difficulty, self.DIFFICULTY_SETTINGS["Medium"]
        )

        if "Skill Level" in engine.options:
            engine.configure({"Skill Level": settings["skill"]})

        result = engine.play(
            board,
            chess.engine.Limit(time=settings["time"]),
        )

        return result.move.uci() if result.move else None

    def close(self) -> None:
        if self.engine is not None:
            self.engine.quit()
            self.engine = None


# Backward-compatible alias
StockfishEngine = ComputerEngine
