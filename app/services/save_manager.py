from __future__ import annotations

"""Game state persistence and slot management."""

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class SaveSlot:
    """Represents one of the 3 available game save slots."""

    slot_id: int
    is_active: bool = False
    saved_at: str = ""
    saved_at_formatted: str = ""
    game_mode: str = "Local 2-player"
    player_color: str = "White"  # Perspective / Human color ("White" or "Black")
    difficulty: str = "Medium"
    moves: list[str] = field(default_factory=list)  # UCI moves
    move_count: int = 0
    fen: str = ""
    turn: str = "White"
    status_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SaveSlot:
        slot_id = data.get("slot_id", 1)
        moves = data.get("moves") or []
        return cls(
            slot_id=slot_id,
            is_active=data.get("is_active", False),
            saved_at=data.get("saved_at", ""),
            saved_at_formatted=data.get("saved_at_formatted", ""),
            game_mode=data.get("game_mode", "Local 2-player"),
            player_color=data.get("player_color", "White"),
            difficulty=data.get("difficulty", "Medium"),
            moves=list(moves),
            move_count=data.get("move_count", len(moves)),
            fen=data.get("fen", ""),
            turn=data.get("turn", "White"),
            status_text=data.get("status_text", ""),
        )


class SaveManager:
    """Manages saving, loading, and deleting up to 3 game slots."""

    MAX_SLOTS: int = 3

    def __init__(self, storage_path: str | Path | None = None) -> None:
        if storage_path is not None:
            self.storage_path = Path(storage_path)
        else:
            env_path = os.environ.get("JD_CHESS_SAVES_PATH")
            if env_path:
                self.storage_path = Path(env_path)
            else:
                self.storage_path = Path.home() / ".jd_chess" / "saved_games.json"

    def _ensure_dir(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def _read_data(self) -> dict[str, Any]:
        if not self.storage_path.is_file():
            return {}
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_data(self, data: dict[str, Any]) -> None:
        self._ensure_dir()
        temp_dir = self.storage_path.parent if self.storage_path.parent.exists() else None
        
        # Write to temporary file then replace to prevent partial writes
        try:
            with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
                json.dump(data, tf, indent=2)
                temp_name = tf.name
            os.replace(temp_name, str(self.storage_path))
        except Exception:
            # Fallback direct write
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    def get_slots(self) -> list[SaveSlot]:
        """Return list of all 3 slots (slot_id 1 to 3)."""
        data = self._read_data()
        slots: list[SaveSlot] = []

        for slot_id in range(1, self.MAX_SLOTS + 1):
            key = str(slot_id)
            if key in data and isinstance(data[key], dict) and data[key].get("is_active"):
                slots.append(SaveSlot.from_dict(data[key]))
            else:
                slots.append(SaveSlot(slot_id=slot_id, is_active=False))

        return slots

    def get_slot(self, slot_id: int) -> SaveSlot | None:
        """Return slot by ID, or None if out of range."""
        if slot_id < 1 or slot_id > self.MAX_SLOTS:
            return None
        slots = self.get_slots()
        return slots[slot_id - 1]

    def has_active_saves(self) -> bool:
        """Check if any slot contains saved data."""
        return any(slot.is_active for slot in self.get_slots())

    def active_save_count(self) -> int:
        """Return number of currently active save slots."""
        return sum(1 for slot in self.get_slots() if slot.is_active)

    def save_game(
        self,
        slot_id: int,
        game_mode: str,
        player_color: str,
        difficulty: str,
        moves: list[str],
        fen: str,
        turn: str,
        status_text: str = "",
    ) -> SaveSlot:
        """Save game state to the designated slot (1 to 3)."""
        if slot_id < 1 or slot_id > self.MAX_SLOTS:
            raise ValueError(f"Invalid slot ID: {slot_id}. Must be 1 to {self.MAX_SLOTS}.")

        now = datetime.now()
        saved_at_iso = now.isoformat()
        saved_at_formatted = now.strftime("%b %d, %Y • %I:%M %p")

        slot = SaveSlot(
            slot_id=slot_id,
            is_active=True,
            saved_at=saved_at_iso,
            saved_at_formatted=saved_at_formatted,
            game_mode=game_mode,
            player_color=player_color,
            difficulty=difficulty,
            moves=list(moves),
            move_count=len(moves),
            fen=fen,
            turn=turn,
            status_text=status_text,
        )

        data = self._read_data()
        data[str(slot_id)] = slot.to_dict()
        self._write_data(data)

        return slot

    def delete_slot(self, slot_id: int) -> bool:
        """Clear the designated slot."""
        if slot_id < 1 or slot_id > self.MAX_SLOTS:
            return False

        data = self._read_data()
        key = str(slot_id)
        if key in data:
            del data[key]
            self._write_data(data)
            return True
        return False
