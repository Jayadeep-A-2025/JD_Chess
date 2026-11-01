from __future__ import annotations

"""Computer UCI engine integration."""

import os
import shutil
import sys
import threading

import chess
import chess.engine


class ComputerEngine:
    """Manage a Computer chess engine process and request computer moves."""

    DIFFICULTY_SETTINGS = {
    "Novice": {"time": 0.05, "skill": 0},
    "Easy":   {"time": 0.15, "skill": 3},
    "Medium": {"time": 0.50, "skill": 8},
    "Hard":   {"time": 1.20, "skill": 20},
}

    def __init__(self, engine_path: str | None = None) -> None:
        self.engine_path = engine_path or self.find_engine()
        if not self.engine_path:
            raise FileNotFoundError(
                "Computer engine was not found. Install it or set COMPUTER_PATH or STOCKFISH_PATH."
            )

        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        # Protects engine access from concurrent get_best_move / cancel calls
        self._lock = threading.Lock()
        self._searching = False

    @staticmethod
    def find_engine() -> str | None:
        """Find a configured, bundled, or system chess engine."""
        configured_path = (
            os.environ.get("COMPUTER_PATH")
            or os.environ.get("STOCKFISH_PATH")
        )
        if configured_path and os.path.isfile(configured_path):
            return configured_path

        executable_dir = os.path.dirname(os.path.abspath(sys.executable))
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        bundle_dir = getattr(sys, "_MEIPASS", None)

        candidates = []

        # PyInstaller one-file bundle.
        if bundle_dir:
            candidates.extend([
                os.path.join(bundle_dir, "assets", "stockfish"),
                os.path.join(bundle_dir, "assets", "stockfish.exe"),
            ])

        # Executable-relative assets.
        candidates.extend([
            os.path.join(executable_dir, "assets", "stockfish"),
            os.path.join(executable_dir, "assets", "stockfish.exe"),
            os.path.join(executable_dir, "stockfish"),
            os.path.join(executable_dir, "stockfish.exe"),
        ])

        # macOS app: JD_Chess.app/Contents/Resources/assets/
        macos_resources = os.path.abspath(
            os.path.join(executable_dir, "..", "Resources")
        )
        candidates.extend([
            os.path.join(macos_resources, "assets", "stockfish"),
            os.path.join(macos_resources, "assets", "stockfish.exe"),
        ])

        # Development checkout.
        candidates.extend([
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

        with self._lock:
            if "Skill Level" in engine.options:
                engine.configure({"Skill Level": settings["skill"]})

            # If it's Easy mode, introduce a chance to make a random amateur move (e.g., 35% of the time)
            if difficulty == "Easy":
                import random
                legal_moves = list(board.legal_moves)
                # 35% chance to play a completely random move, simulating a beginner blunder
                if legal_moves and random.random() < 0.35:
                    return random.choice(legal_moves).uci()

            self._searching = True
            try:
                result = engine.play(
                    board,
                    chess.engine.Limit(time=settings["time"]),
                )
            finally:
                self._searching = False

        return result.move.uci() if result.move else None

    def cancel_search(self) -> None:
        """Send a stop command to the engine subprocess if a search is in progress.

        chess.engine.SimpleEngine runs the engine process asynchronously under
        asyncio.  The cleanest cross-thread way to interrupt an in-progress
        ``engine.play()`` call is to write ``stop\\n`` directly to the engine
        process's stdin.  This causes the engine to return its best move so far
        immediately, which lets the blocking ``engine.play()`` call return
        quickly on the background thread without requiring us to call any
        asyncio internals.
        """
        engine = getattr(self, "engine", None)
        if engine is None or not self._searching:
            return
        try:
            # Access the underlying transport's stdin to send a UCI stop command.
            proc = getattr(engine, "_transport", None) or getattr(engine, "transport", None)
            if proc is not None:
                stdin = getattr(proc, "stdin", None) or getattr(proc, "_stdin", None)
                if stdin is not None and not getattr(stdin, "closed", True):
                    stdin.write(b"stop\n")
                    stdin.flush()
        except Exception:
            pass

    def close(self) -> None:
        with self._lock:
            if self.engine is not None:
                try:
                    self.engine.quit()
                except Exception:
                    pass
                self.engine = None


# Backward-compatible alias
StockfishEngine = ComputerEngine
