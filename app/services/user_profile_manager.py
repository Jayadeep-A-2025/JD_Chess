from __future__ import annotations

"""User profile and learning progress persistence manager."""

import json
import logging
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_USERNAME = "Grandmaster"


@dataclass
class UserProfile:
    """Stores user preferences, username, and learning curriculum progress."""

    username: str = _DEFAULT_USERNAME
    completed_lessons: list[str] = field(default_factory=list)
    current_lesson_id: str = "beginner_pawn"
    sound_enabled: bool = True
    exercise_attempts: int = 0
    exercise_correct: int = 0
    hint_usage_count: int = 0
    topic_attempts: dict[str, int] = field(default_factory=dict)
    topic_correct: dict[str, int] = field(default_factory=dict)
    topic_mistakes: dict[str, int] = field(default_factory=dict)
    lesson_history: dict[str, dict[str, Any]] = field(default_factory=dict)
    unlocked_level: int = 1

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UserProfile:
        return cls(
            username=str(data.get("username", _DEFAULT_USERNAME)).strip() or _DEFAULT_USERNAME,
            completed_lessons=list(data.get("completed_lessons", [])),
            current_lesson_id=str(data.get("current_lesson_id", "beginner_pawn")),
            sound_enabled=bool(data.get("sound_enabled", True)),
            exercise_attempts=int(data.get("exercise_attempts", 0)),
            exercise_correct=int(data.get("exercise_correct", 0)),
            hint_usage_count=int(data.get("hint_usage_count", 0)),
            topic_attempts=dict(data.get("topic_attempts", {})),
            topic_correct=dict(data.get("topic_correct", {})),
            topic_mistakes=dict(data.get("topic_mistakes", {})),
            lesson_history=dict(data.get("lesson_history", {})),
            unlocked_level=int(data.get("unlocked_level", 1)),
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
        self._cached_profile: UserProfile | None = None
        self._cached_mtime: float | None = None

    def _ensure_dir(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            logger.warning(
                "UserProfileManager: could not create storage directory %s: %s",
                self.storage_path.parent,
                exc,
            )

    def _read_data(self) -> dict[str, Any]:
        if not self.storage_path.is_file():
            return {}
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as exc:
            logger.error(
                "UserProfileManager: profile file %s is corrupt (%s). "
                "Starting with default profile.",
                self.storage_path,
                exc,
            )
            return {}
        except OSError as exc:
            logger.error(
                "UserProfileManager: could not read profile file %s: %s. "
                "Starting with default profile.",
                self.storage_path,
                exc,
            )
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
        except OSError as exc:
            logger.error(
                "UserProfileManager: atomic write failed for %s (%s). "
                "Attempting direct write as fallback.",
                self.storage_path,
                exc,
            )
            try:
                with open(self.storage_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
            except OSError as exc2:
                raise RuntimeError(
                    f"UserProfileManager: failed to write profile to "
                    f"{self.storage_path}: {exc2}"
                ) from exc2

    def get_profile(self) -> UserProfile:
        try:
            if self.storage_path.is_file():
                mtime = self.storage_path.stat().st_mtime
                if self._cached_profile is not None and self._cached_mtime == mtime:
                    return UserProfile.from_dict(self._cached_profile.to_dict())
                data = self._read_data()
                prof = UserProfile.from_dict(data)
                self._cached_profile = prof
                self._cached_mtime = mtime
                return UserProfile.from_dict(prof.to_dict())
        except OSError:
            pass
        data = self._read_data()
        prof = UserProfile.from_dict(data)
        self._cached_profile = prof
        return prof

    def save_profile(self, profile: UserProfile) -> None:
        self._write_data(profile.to_dict())
        self._cached_profile = profile
        try:
            if self.storage_path.is_file():
                self._cached_mtime = self.storage_path.stat().st_mtime
        except OSError:
            self._cached_mtime = None

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

    def get_sound_enabled(self) -> bool:
        """Return whether sound effects are enabled."""
        return self.get_profile().sound_enabled

    def set_sound_enabled(self, enabled: bool) -> None:
        """Set and persist sound effects preference."""
        prof = self.get_profile()
        prof.sound_enabled = bool(enabled)
        self.save_profile(prof)

    # -------------------------------------------------------------------------
    # Learning Academy Metrics & Smart Progress Tracking
    # -------------------------------------------------------------------------
    def record_exercise_attempt(
        self,
        lesson_id: str,
        topic: str,
        is_correct: bool,
        hints_used: int = 0,
    ) -> None:
        """Record an interactive attempt on a lesson exercise or assessment."""
        prof = self.get_profile()
        prof.exercise_attempts += 1
        if is_correct:
            prof.exercise_correct += 1
            if lesson_id not in prof.completed_lessons:
                prof.completed_lessons.append(lesson_id)

        clean_topic = topic.strip() if topic else "general"
        prof.topic_attempts[clean_topic] = prof.topic_attempts.get(clean_topic, 0) + 1
        if is_correct:
            prof.topic_correct[clean_topic] = prof.topic_correct.get(clean_topic, 0) + 1
        else:
            prof.topic_mistakes[clean_topic] = prof.topic_mistakes.get(clean_topic, 0) + 1

        if hints_used > 0:
            prof.hint_usage_count += hints_used

        entry = prof.lesson_history.get(lesson_id, {
            "attempts": 0,
            "correct": 0,
            "hints_used": 0,
            "completed": False,
        })
        entry["attempts"] = entry.get("attempts", 0) + 1
        if is_correct:
            entry["correct"] = entry.get("correct", 0) + 1
            entry["completed"] = True
        entry["hints_used"] = entry.get("hints_used", 0) + hints_used
        prof.lesson_history[lesson_id] = entry

        # Update unlocked level dynamically
        prof.unlocked_level = max(prof.unlocked_level, self._calc_max_unlocked_level(prof.completed_lessons))
        self.save_profile(prof)

    def record_hint_used(self, lesson_id: str, topic: str = "") -> None:
        """Increment hint usage counter."""
        prof = self.get_profile()
        prof.hint_usage_count += 1
        if lesson_id in prof.lesson_history:
            prof.lesson_history[lesson_id]["hints_used"] = (
                prof.lesson_history[lesson_id].get("hints_used", 0) + 1
            )
        self.save_profile(prof)

    def get_accuracy_rate(self, topic: str | None = None) -> float:
        """Return percentage of correct attempts (0.0 to 100.0)."""
        prof = self.get_profile()
        if topic:
            clean_topic = topic.strip()
            attempts = prof.topic_attempts.get(clean_topic, 0)
            correct = prof.topic_correct.get(clean_topic, 0)
        else:
            attempts = prof.exercise_attempts
            correct = prof.exercise_correct

        if attempts <= 0:
            return 100.0
        return round((correct / attempts) * 100.0, 1)

    def get_weak_topics(self, limit: int = 3) -> list[tuple[str, float]]:
        """Identify topics with low accuracy or high mistake counts."""
        prof = self.get_profile()
        topics_stats: list[tuple[str, float, int]] = []
        for topic, attempts in prof.topic_attempts.items():
            if attempts > 0:
                correct = prof.topic_correct.get(topic, 0)
                acc = (correct / attempts) * 100.0
                mistakes = prof.topic_mistakes.get(topic, 0)
                topics_stats.append((topic, round(acc, 1), mistakes))

        # Sort primarily by lowest accuracy, secondarily by highest mistakes
        topics_stats.sort(key=lambda item: (item[1], -item[2]))
        weak = [(topic, acc) for topic, acc, _ in topics_stats if acc < 85.0]
        return weak[:limit]

    def get_recommended_lesson_id(self) -> str:
        """Return the next best lesson ID based on topic weaknesses or progression."""
        from app.services.curriculum import get_curriculum

        prof = self.get_profile()
        curriculum = get_curriculum()
        completed_set = set(prof.completed_lessons)

        # 1. Look for uncompleted lessons in the player's weakest topics
        weak_topics = [t for t, _ in self.get_weak_topics()]
        for topic in weak_topics:
            for lesson in curriculum:
                if lesson.topic == topic and lesson.id not in completed_set:
                    return lesson.id

        # 2. Look for the next uncompleted lesson in the curriculum
        for lesson in curriculum:
            if lesson.id not in completed_set:
                return lesson.id

        # 3. If all completed, return first lesson
        return curriculum[0].id if curriculum else "beginner_pawn"

    def _calc_max_unlocked_level(self, completed_lessons: list[str]) -> int:
        """Determine highest unlocked level based on prerequisite completion."""
        from app.services.curriculum import get_curriculum

        curriculum = get_curriculum()
        comp_set = set(completed_lessons)
        max_level = 1

        # Check each level from 1 to 6 to see if level + 1 unlocks
        for lvl in range(1, 7):
            level_lessons = [l for l in curriculum if l.level_number == lvl]
            if not level_lessons:
                continue
            done = sum(1 for l in level_lessons if l.id in comp_set)
            # Unlock next level if at least 4 of 6 (or 60%) are completed
            threshold = min(4, len(level_lessons))
            if done >= threshold:
                max_level = lvl + 1
            else:
                break
        return min(max_level, 7)

    def is_level_unlocked(self, level_number: int) -> bool:
        """Check whether a level (1-7) is accessible to the player."""
        if level_number <= 1:
            return True
        prof = self.get_profile()
        calculated = self._calc_max_unlocked_level(prof.completed_lessons)
        return max(prof.unlocked_level, calculated) >= level_number

    def get_level_progress(self, level_number: int) -> tuple[int, int]:
        """Return (completed_count, total_count) for a specific level."""
        from app.services.curriculum import get_curriculum

        curriculum = get_curriculum()
        level_lessons = [l for l in curriculum if l.level_number == level_number]
        if not level_lessons:
            return (0, 0)
        comp_set = set(self.get_profile().completed_lessons)
        done = sum(1 for l in level_lessons if l.id in comp_set)
        return (done, len(level_lessons))

    def migrate_progress(self) -> None:
        """Safely migrate any legacy progress data to the Academy schema."""
        prof = self.get_profile()
        # Clean up any duplicated lesson IDs while preserving order
        seen = set()
        cleaned_lessons = []
        for lid in prof.completed_lessons:
            if lid not in seen:
                seen.add(lid)
                cleaned_lessons.append(lid)
        prof.completed_lessons = cleaned_lessons
        prof.unlocked_level = max(prof.unlocked_level, self._calc_max_unlocked_level(prof.completed_lessons))
        self.save_profile(prof)
