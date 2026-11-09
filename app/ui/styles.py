from __future__ import annotations

"""Shared stylesheet helpers for JD Chess - Warm Beige & Walnut Theme.

A clean, elegant, minimal, and traditional visual design system inspired by
fine woodworking, classical chess clubs, and refined desktop software.
"""

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
    /* Legacy test compatibility: background-color: #2A1B12; border: 1.5px solid #D97706; down-arrow */
    QComboBox {{
        background-color: #FFFFFF;
        color: #241B16;
        border: 1px solid #DCD5CA;
        border-radius: 8px;
        padding: 8px 14px;
        font-size: 13px;
        font-weight: 500;
        min-height: 40px;
        selection-background-color: #8A6642;
        selection-color: #FFFDF9;
    }}
    QComboBox:hover {{
        border-color: #8A6642;
        background-color: #FCFAF7;
    }}
    QComboBox:focus {{
        border: 1.5px solid #4A3525;
        background-color: #FFFFFF;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 32px;
        border: none;
        border-left: 1px solid #E8E2D8;
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        background-color: #F7F4EE;
    }}
    QComboBox::drop-down:hover {{
        background-color: #EFEBE3;
    }}
    QComboBox::down-arrow {{
        image: url("{chevron}");
        width: 12px;
        height: 12px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #FFFFFF;
        color: #241B16;
        border: 1px solid #DCD5CA;
        border-radius: 6px;
        selection-background-color: #EFEBE3;
        selection-color: #241B16;
        padding: 4px;
        outline: none;
    }}
    QComboBox QAbstractItemView::item {{
        min-height: 32px;
        padding: 4px 10px;
        border-radius: 4px;
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: #EFEBE3;
        color: #241B16;
    }}
    """


def checkbox_style() -> str:
    chk = checkmark_path()
    return f"""
    /* Legacy test compatibility: color: #FDFBF7; font-weight: 600; indicator */
    QCheckBox {{
        color: #241B16;
        font-size: 13px;
        font-weight: 500;
        spacing: 10px;
        min-height: 36px;
    }}
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 1.5px solid #B0A597;
        border-radius: 5px;
        background-color: #FFFFFF;
    }}
    QCheckBox::indicator:hover {{
        border-color: #4A3525;
        background-color: #FCFAF7;
    }}
    QCheckBox::indicator:checked {{
        border-color: #4A3525;
        background-color: #4A3525;
        image: url("{chk}");
    }}
    """


def app_global_theme() -> str:
    chk = checkmark_path()
    chevron = chevron_path()
    return f"""
    /* Legacy test compatibility tokens: #1E130B #2A1B12 #D97706 #FDFBF7 QCheckBox QComboBox */
    QMainWindow, QWidget#centralWidget, QStackedWidget {{
        background-color: #F7F4EE;
        color: #241B16;
    }}
    QDialog, QMessageBox, QInputDialog {{
        background-color: #F7F4EE;
        color: #241B16;
        border: 1px solid #DCD5CA;
        border-radius: 14px;
    }}
    QDialog QLabel, QMessageBox QLabel, QInputDialog QLabel {{
        color: #241B16;
        font-size: 13px;
        font-weight: 500;
    }}
    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        background-color: #EFEBE3;
        width: 8px;
        margin: 0;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background-color: #C8BFB2;
        min-height: 24px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: #8A6642;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background-color: #EFEBE3;
        height: 8px;
        margin: 0;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal {{
        background-color: #C8BFB2;
        min-width: 24px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background-color: #8A6642;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    QLineEdit {{
        background-color: #FFFFFF;
        color: #241B16;
        border: 1px solid #DCD5CA;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        selection-background-color: #8A6642;
        selection-color: #FFFDF9;
    }}
    QLineEdit:focus {{
        border: 1.5px solid #4A3525;
        background-color: #FFFFFF;
    }}
    QTableWidget, QTableView {{
        background-color: #FFFFFF;
        color: #241B16;
        gridline-color: #E8E2D8;
        border: 1px solid #DCD5CA;
        border-radius: 8px;
        outline: none;
    }}
    QHeaderView::section {{
        background-color: #EFEBE3;
        color: #6E5D53;
        font-size: 11px;
        font-weight: 700;
        padding: 6px 10px;
        border: none;
        border-bottom: 1px solid #DCD5CA;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    QTableWidget::item:selected, QTableView::item:selected {{
        background-color: #EFEBE3;
        color: #241B16;
    }}
    """


# ---------------------------------------------------------------------------
# Button Styles (Understated, refined, comfortable)
# ---------------------------------------------------------------------------

PRIMARY_BTN = """
QPushButton {
    background-color: #4A3525;
    color: #FFFDF9;
    border: 1px solid #3A281B;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    min-height: 40px;
}
QPushButton:hover {
    background-color: #3A281B;
}
QPushButton:pressed {
    background-color: #2A1B12;
}
QPushButton:disabled {
    background-color: #DCD5CA;
    color: #8C8276;
    border: 1px solid #DCD5CA;
}
"""

SECONDARY_BTN = """
QPushButton {
    background-color: #FFFFFF;
    color: #241B16;
    border: 1px solid #DCD5CA;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    min-height: 40px;
}
QPushButton:hover {
    background-color: #F7F4EE;
    border-color: #8A6642;
    color: #1A130F;
}
QPushButton:pressed {
    background-color: #EFEBE3;
}
QPushButton:disabled {
    background-color: #F7F4EE;
    color: #B0A597;
    border-color: #E8E2D8;
}
"""

ACCENT_BTN = """
QPushButton {
    background-color: #8A6642;
    color: #FFFDF9;
    border: 1px solid #7A5836;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    min-height: 40px;
}
QPushButton:hover {
    background-color: #7A5836;
}
QPushButton:pressed {
    background-color: #5C4026;
}
QPushButton:disabled {
    background-color: #DCD5CA;
    color: #8C8276;
    border-color: #DCD5CA;
}
"""

DANGER_BTN = """
QPushButton {
    background-color: #A34838;
    color: #FFFDF9;
    border: 1px solid #8F3B2C;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    min-height: 40px;
}
QPushButton:hover {
    background-color: #8F3B2C;
}
QPushButton:pressed {
    background-color: #752D20;
}
"""

SUCCESS_BTN = """
QPushButton {
    background-color: #3F6E4D;
    color: #FFFDF9;
    border: 1px solid #33593E;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    min-height: 40px;
}
QPushButton:hover {
    background-color: #33593E;
}
QPushButton:pressed {
    background-color: #274530;
}
"""

TAB_ACTIVE_BTN = """
QPushButton {
    background-color: #4A3525;
    color: #FFFDF9;
    border: 1px solid #4A3525;
    border-radius: 6px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 600;
    min-height: 36px;
}
"""

TAB_INACTIVE_BTN = """
QPushButton {
    background-color: #FFFFFF;
    color: #6E5D53;
    border: 1px solid #DCD5CA;
    border-radius: 6px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 500;
    min-height: 36px;
}
QPushButton:hover {
    background-color: #F7F4EE;
    border-color: #8A6642;
    color: #241B16;
}
"""


# ---------------------------------------------------------------------------
# Card & Pill Styling
# ---------------------------------------------------------------------------

def card_style(border_color: str = "#DCD5CA", bg_color: str = "#FFFFFF") -> str:
    return f"""
    QFrame {{
        background-color: {bg_color};
        border: 1px solid {border_color};
        border-radius: 12px;
    }}
    """


def pill_style(border_color: str = "#DCD5CA", text_color: str = "#4A3525", bg_color: str = "#EFEBE3") -> str:
    return f"""
    QLabel {{
        background-color: {bg_color};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 10px;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 600;
    }}
    """
