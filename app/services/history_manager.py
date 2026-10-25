from __future__ import annotations

"""Match history and player rating tracking service."""

import json
import math
import os
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Rating system helpers (simplified Elo)
# ---------------------------------------------------------------------------
_DEFAULT_RATING = 1200
_K_FACTOR = 32


def _expected_score(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))


def compute_rating_change(
    player_rating: float,
    opponent_rating: float,
    result: str,  # "win" | "loss" | "draw"
) -> int:
    """Return the integer Elo delta for the player."""
    actual = {"win": 1.0, "draw": 0.5, "loss": 0.0}.get(result, 0.5)
    expected = _expected_score(player_rating, opponent_rating)
    return int(round(_K_FACTOR * (actual - expected)))


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class MatchRecord:
    """Single completed game record stored in history."""

    match_id: str
    played_at: str          # ISO timestamp
    played_at_formatted: str
    game_mode: str          # "Local 2-player" | "Play vs Computer"
    player_color: str       # "White" | "Black"
    difficulty: str         # "Easy" | "Medium" | "Hard" | "N/A"
    result: str             # "win" | "loss" | "draw"
    result_label: str       # human-readable e.g. "Checkmate – You Won"
    moves: list[str]        # UCI move list
    move_count: int
    rating_before: int
    rating_after: int
    rating_change: int
    accuracy_score: int     # 0-100 computed from analysis
    blunders: int
    mistakes: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> MatchRecord:
        return cls(
            match_id=d.get("match_id", ""),
            played_at=d.get("played_at", ""),
            played_at_formatted=d.get("played_at_formatted", ""),
            game_mode=d.get("game_mode", ""),
            player_color=d.get("player_color", "White"),
            difficulty=d.get("difficulty", "N/A"),
            result=d.get("result", "draw"),
            result_label=d.get("result_label", "Draw"),
            moves=list(d.get("moves") or []),
            move_count=d.get("move_count", 0),
            rating_before=d.get("rating_before", _DEFAULT_RATING),
            rating_after=d.get("rating_after", _DEFAULT_RATING),
            rating_change=d.get("rating_change", 0),
            accuracy_score=d.get("accuracy_score", 0),
            blunders=d.get("blunders", 0),
            mistakes=d.get("mistakes", 0),
        )


# ---------------------------------------------------------------------------
# HistoryManager
# ---------------------------------------------------------------------------
class HistoryManager:
    """Persists match records and player rating across sessions."""

    def __init__(self, storage_path: str | Path | None = None) -> None:
        if storage_path is not None:
            self.storage_path = Path(storage_path)
        else:
            env_path = os.environ.get("JD_CHESS_HISTORY_PATH")
            if env_path:
                self.storage_path = Path(env_path)
            else:
                self.storage_path = Path.home() / ".jd_chess" / "match_history.json"

    # ------------------------------------------------------------------
    # Private IO helpers
    # ------------------------------------------------------------------
    def _ensure_dir(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def _read_data(self) -> dict[str, Any]:
        if not self.storage_path.is_file():
            return {"rating": _DEFAULT_RATING, "matches": []}
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Ensure keys exist
            data.setdefault("rating", _DEFAULT_RATING)
            data.setdefault("matches", [])
            return data
        except Exception:
            return {"rating": _DEFAULT_RATING, "matches": []}

    def _write_data(self, data: dict[str, Any]) -> None:
        self._ensure_dir()
        temp_dir = (
            self.storage_path.parent if self.storage_path.parent.exists() else None
        )
        try:
            with tempfile.NamedTemporaryFile(
                "w", dir=temp_dir, delete=False, encoding="utf-8", suffix=".json"
            ) as tf:
                json.dump(data, tf, indent=2)
                temp_name = tf.name
            os.replace(temp_name, str(self.storage_path))
        except Exception:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_rating(self) -> int:
        return int(self._read_data().get("rating", _DEFAULT_RATING))

    def get_all_matches(self) -> list[MatchRecord]:
        data = self._read_data()
        records = []
        for item in reversed(data.get("matches", [])):  # newest first
            try:
                records.append(MatchRecord.from_dict(item))
            except Exception:
                pass
        return records

    def get_matches_count(self) -> int:
        return len(self._read_data().get("matches", []))

    def record_match(
        self,
        game_mode: str,
        player_color: str,
        difficulty: str,
        result: str,
        result_label: str,
        moves: list[str],
        accuracy_score: int = 0,
        blunders: int = 0,
        mistakes: int = 0,
    ) -> MatchRecord:
        """Append a new match result and update the player rating."""
        data = self._read_data()
        current_rating = int(data.get("rating", _DEFAULT_RATING))

        # Opponent rating is based on difficulty (for Computer mode)
        if game_mode == "Play vs Computer":
            opponent_rating = {"Easy": 800, "Medium": 1200, "Hard": 1600}.get(
                difficulty, 1200
            )
        else:
            opponent_rating = current_rating  # local: symmetric change

        delta = compute_rating_change(current_rating, opponent_rating, result)
        new_rating = max(100, current_rating + delta)

        now = datetime.now()
        match_id = now.strftime("%Y%m%d_%H%M%S_%f")

        record = MatchRecord(
            match_id=match_id,
            played_at=now.isoformat(),
            played_at_formatted=now.strftime("%b %d, %Y  %I:%M %p"),
            game_mode=game_mode,
            player_color=player_color,
            difficulty=difficulty if game_mode == "Play vs Computer" else "N/A",
            result=result,
            result_label=result_label,
            moves=list(moves),
            move_count=len(moves),
            rating_before=current_rating,
            rating_after=new_rating,
            rating_change=delta,
            accuracy_score=accuracy_score,
            blunders=blunders,
            mistakes=mistakes,
        )

        data["rating"] = new_rating
        data["matches"].append(record.to_dict())
        self._write_data(data)
        return record
