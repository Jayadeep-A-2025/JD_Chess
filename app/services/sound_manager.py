from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt, QUrl
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QAbstractButton


class SoundManager(QObject):
    """Centralized, optional sound effects for JD Chess."""

    SOUND_FILES = {
        "click": "click.wav",
        "move": "move.wav",
        "capture": "capture.wav",
        "success": "success.wav",
        "game_over": "game_over.wav",
    }

    def __init__(self, enabled: bool = True, parent=None):
        super().__init__(parent)
        self.enabled = bool(enabled)
        self.effects: dict[str, QSoundEffect] = {}

        # Support both development and PyInstaller builds.
        if getattr(sys, "_MEIPASS", None):
            asset_root = Path(sys._MEIPASS)
        else:
            asset_root = Path(__file__).resolve().parents[2]

        sound_dir = asset_root / "assets" / "sounds"

        for name, filename in self.SOUND_FILES.items():
            path = sound_dir / filename
            if not path.is_file():
                continue

            try:
                effect = QSoundEffect(self)
                effect.setSource(QUrl.fromLocalFile(str(path.resolve())))
                effect.setLoopCount(1)
                effect.setVolume(0.20)
                self.effects[name] = effect
            except Exception:
                # Audio must never prevent the chess app from starting.
                continue

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)

    def play(self, name: str) -> None:
        if not self.enabled:
            return

        effect = self.effects.get(name)
        if effect is not None:
            try:
                effect.play()
            except Exception:
                pass

    def eventFilter(self, watched, event) -> bool:
        """Play clicks for UI buttons, excluding disabled controls."""
        if not self.enabled or not isinstance(watched, QAbstractButton):
            return False

        if not watched.isEnabled():
            return False

        if event.type() == QEvent.Type.MouseButtonRelease:
            self.play("click")
        elif event.type() == QEvent.Type.KeyRelease and event.key() in (
            Qt.Key.Key_Space,
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter,
        ):
            self.play("click")

        return False
