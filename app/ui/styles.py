from __future__ import annotations
"""Shared stylesheet helpers for Royal Gold & Luxury Mahogany Theme."""

from pathlib import Path


def chevron_path() -> str:
    icons_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
    return (icons_dir / "chevron-down.svg").as_posix()


def checkmark_path() -> str:
    icons_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
    return (icons_dir / "checkmark.svg").as_posix()


def combo_style() -> str:
    chevron = chevron_path()
    return f"""
    QComboBox {{
        background-color: #2A1B12;
        color: #FDFBF7;
        border: 1.5px solid #D97706;
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 14px;
        font-weight: 600;
        min-height: 44px;
        selection-background-color: #D97706;
        selection-color: #1E130B;
    }}
    QComboBox:hover {{
        border-color: #B45309;
        background-color: #352317;
    }}
    QComboBox:focus {{
        border: 2px solid #D97706;
        background-color: #2A1B12;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 38px;
        border: none;
        border-left: 1.5px solid #D97706;
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        background-color: #352317;
    }}
    QComboBox::drop-down:hover {{
        background-color: #D97706;
    }}
    QComboBox::down-arrow {{
        image: url("{chevron}");
        width: 14px;
        height: 14px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #1E130B;
        color: #FDFBF7;
        border: 1.5px solid #D97706;
        border-radius: 10px;
        padding: 6px;
        outline: 0;
        font-size: 14px;
        font-weight: 500;
        selection-background-color: #D97706;
        selection-color: #1E130B;
    }}
    QComboBox QAbstractItemView::item {{
        min-height: 40px;
        padding: 8px 12px;
        border-radius: 6px;
        color: #FDFBF7;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: #2A1B12;
        color: #D97706;
    }}
    """


def checkbox_style() -> str:
    chk = checkmark_path()
    return f"""
    QCheckBox {{
        color: #FDFBF7;
        font-size: 14px;
        font-weight: 600;
        spacing: 12px;
        min-height: 36px;
    }}
    QCheckBox::indicator {{
        width: 22px;
        height: 22px;
        border: 2px solid #D97706;
        border-radius: 6px;
        background-color: #2A1B12;
    }}
    QCheckBox::indicator:hover {{
        border-color: #B45309;
        background-color: #352317;
    }}
    QCheckBox::indicator:checked {{
        border-color: #D97706;
        background-color: #D97706;
        image: url("{chk}");
    }}
    """


def app_global_theme() -> str:
    chk = checkmark_path()
    chevron = chevron_path()
    return f"""
    QMainWindow, QWidget#centralWidget, QStackedWidget {{
        background-color: #1E130B;
        color: #FDFBF7;
    }}
    QDialog, QMessageBox, QInputDialog {{
        background-color: #1E130B;
        color: #FDFBF7;
        border: 1.5px solid #D97706;
        border-radius: 16px;
    }}
    QDialog QLabel, QMessageBox QLabel, QInputDialog QLabel {{
        color: #FDFBF7;
        font-size: 14px;
        font-weight: 500;
    }}
    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        background-color: #1E130B;
        width: 10px;
        margin: 0;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background-color: #352317;
        border: 1px solid #D97706;
        min-height: 24px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: #D97706;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background-color: #1E130B;
        height: 10px;
        margin: 0;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal {{
        background-color: #352317;
        border: 1px solid #D97706;
        min-width: 24px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background-color: #D97706;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    QCheckBox {{
        color: #FDFBF7;
        font-size: 14px;
        font-weight: 600;
        spacing: 12px;
        min-height: 36px;
    }}
    QCheckBox::indicator {{
        width: 22px;
        height: 22px;
        border: 2px solid #D97706;
        border-radius: 6px;
        background-color: #2A1B12;
    }}
    QCheckBox::indicator:hover {{
        border-color: #B45309;
        background-color: #352317;
    }}
    QCheckBox::indicator:checked {{
        border-color: #D97706;
        background-color: #D97706;
        image: url("{chk}");
    }}
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: #2A1B12;
        color: #FDFBF7;
        border: 1.5px solid #D97706;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 14px;
        font-weight: 500;
        selection-background-color: #D97706;
        selection-color: #1E130B;
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid #D97706;
        background-color: #352317;
    }}
    QComboBox {{
        background-color: #2A1B12;
        color: #FDFBF7;
        border: 1.5px solid #D97706;
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 14px;
        font-weight: 600;
        min-height: 44px;
        selection-background-color: #D97706;
        selection-color: #1E130B;
    }}
    QComboBox:hover {{
        border-color: #B45309;
        background-color: #352317;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 38px;
        border: none;
        border-left: 1.5px solid #D97706;
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        background-color: #352317;
    }}
    QComboBox::drop-down:hover {{
        background-color: #D97706;
    }}
    QComboBox::down-arrow {{
        image: url("{chevron}");
        width: 14px;
        height: 14px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #1E130B;
        color: #FDFBF7;
        border: 1.5px solid #D97706;
        border-radius: 10px;
        padding: 6px;
        outline: 0;
        font-size: 14px;
        font-weight: 500;
        selection-background-color: #D97706;
        selection-color: #1E130B;
    }}
    QComboBox QAbstractItemView::item {{
        min-height: 40px;
        padding: 8px 12px;
        border-radius: 6px;
        color: #FDFBF7;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: #2A1B12;
        color: #D97706;
    }}
    QDialogButtonBox QPushButton,
    QMessageBox QPushButton,
    QInputDialog QPushButton {{
        background-color: #D97706;
        color: #1E130B;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 800;
        min-height: 44px;
        min-width: 90px;
    }}
    QDialogButtonBox QPushButton:hover,
    QMessageBox QPushButton:hover,
    QInputDialog QPushButton:hover {{
        background-color: #B45309;
        color: #FDFBF7;
    }}
    """


def card_style(object_name: str = "") -> str:
    sel = f"QFrame#{object_name}" if object_name else "QFrame"
    return f"""
    {sel} {{
        background-color: #2A1B12;
        border: 1.5px solid #D97706;
        border-radius: 16px;
    }}
    """


def stats_frame_style(object_name: str = "") -> str:
    sel = f"QFrame#{object_name}" if object_name else "QFrame"
    return f"""
    {sel} {{
        background-color: #2A1B12;
        border: 1.5px solid #D97706;
        border-radius: 16px;
    }}
    """


PRIMARY_BTN = """
QPushButton {
    background-color: #D97706;
    color: #1E130B;
    border: none;
    border-radius: 10px;
    padding: 12px 22px;
    font-size: 14px;
    font-weight: 800;
    min-height: 44px;
}
QPushButton:hover {
    background-color: #B45309;
    color: #FDFBF7;
}
QPushButton:pressed {
    background-color: #92400E;
    color: #FDFBF7;
}
"""

SECONDARY_BTN = """
QPushButton {
    background-color: #2A1B12;
    color: #FDFBF7;
    border: 1.5px solid #D97706;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 700;
    min-height: 44px;
}
QPushButton:hover {
    background-color: #352317;
    border-color: #B45309;
    color: #D97706;
}
QPushButton:pressed {
    background-color: #1E130B;
    color: #FDFBF7;
}
"""

DANGER_BTN = """
QPushButton {
    background-color: #7F1D1D;
    color: #FDFBF7;
    border: 1.5px solid #DC2626;
    border-radius: 10px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 700;
    min-height: 44px;
}
QPushButton:hover {
    background-color: #991B1B;
    border-color: #EF4444;
}
QPushButton:pressed {
    background-color: #581C87;
}
"""

SUCCESS_BTN = """
QPushButton {
    background-color: #065F46;
    color: #FDFBF7;
    border: 1.5px solid #10B981;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 700;
    min-height: 44px;
}
QPushButton:hover {
    background-color: #047857;
}
QPushButton:pressed {
    background-color: #064E3B;
}
"""
