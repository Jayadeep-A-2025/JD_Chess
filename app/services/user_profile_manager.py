from __future__ import annotations

"""User profile and learning progress persistence manager."""

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

_DEFAULT_USERNAME = "Grandmaster"


@dataclass
class UserProfile:
    """Stores user preferences, username, and learning curriculum progress."""

    username: str = _DEFAULT_USERNAME
    completed_lessons: list[str] = field(default_factory=list)
    current_lesson_id: str = "beginner_pawn"
    sound_enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserProfile:
        return cls(
            username=str(data.get("username", _DEFAULT_USERNAME)).strip() or _DEFAULT_USERNAME,
            completed_lessons=list(data.get("completed_lessons", [])),
            current_lesson_id=str(data.get("current_lesson_id", "beginner_pawn")),
            sound_enabled=bool(data.get("sound_enabled", True)),
        )


class UserProfileManager:
    """Manages reading and writing user profile & lesson progress to disk."""

    def __init__(self, storage_path: str | Path | None = None) -> None:
        if storage_path is not None:
            self.storage_path = Path(storage_path)
        else:
            env_path = os.environ.get("JD_CHESS_PROFILE_PATH")
            if env_path:
                self.storage_path = Path(env_path)
            else:
                self.storage_path = Path.home() / ".jd_chess" / "user_profile.json"

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
        temp_dir = (
            self.storage_path.parent
            if self.storage_path.parent.exists()
            else None
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

    def get_profile(self) -> UserProfile:
        return UserProfile.from_dict(self._read_data())

    def save_profile(self, profile: UserProfile) -> None:
        self._write_data(profile.to_dict())

    def get_username(self) -> str:
        return self.get_profile().username

    def set_username(self, name: str) -> str:
        clean_name = str(name).strip() or _DEFAULT_USERNAME
        prof = self.get_profile()
        prof.username = clean_name
        self.save_profile(prof)
        return clean_name

    def is_lesson_completed(self, lesson_id: str) -> bool:
        return lesson_id in self.get_profile().completed_lessons

    def mark_lesson_completed(self, lesson_id: str) -> None:
        prof = self.get_profile()
        if lesson_id not in prof.completed_lessons:
            prof.completed_lessons.append(lesson_id)
            self.save_profile(prof)

    def get_current_lesson_id(self) -> str:
        return self.get_profile().current_lesson_id

    def set_current_lesson_id(self, lesson_id: str) -> None:
        prof = self.get_profile()
        prof.current_lesson_id = lesson_id
        self.save_profile(prof)
