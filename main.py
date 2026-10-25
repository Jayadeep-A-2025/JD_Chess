from __future__ import annotations

"""Application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("JD Chess")

    from app.ui.styles import app_global_theme
    app.setStyleSheet(app_global_theme())

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
