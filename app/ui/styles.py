from __future__ import annotations

"""Shared stylesheet helpers for modern controls, high-contrast dialogs, and mobile-responsive styling."""

from pathlib import Path


def _chevron_path() -> str:
    icons_dir = (
        Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
    )
    return (icons_dir / "chevron-down.svg").as_posix()


def _checkmark_path() -> str:
    icons_dir = (
        Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
    )
    return (icons_dir / "checkmark.svg").as_posix()


# ---------------------------------------------------------------------------
# Modern Combo-box / Dropdown Style (touch-friendly 40px+ height)
# ---------------------------------------------------------------------------

def combo_style() -> str:
    chevron = _chevron_path()
    return f"""
        QComboBox {{
            background-color: #FFFFFF;
            color: #0F172A;
            border: 2px solid #CBD5E1;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 14px;
            font-weight: 600;
            min-height: 40px;
            selection-background-color: #DBEAFE;
        }}

        QComboBox:hover {{
            border-color: #3B82F6;
            background-color: #F8FAFC;
        }}

        QComboBox:focus {{
            border: 2px solid #2563EB;
            background-color: #FFFFFF;
        }}

        QComboBox:disabled {{
            background-color: #F1F5F9;
            color: #94A3B8;
            border-color: #E2E8F0;
        }}

        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 36px;
            border: none;
            border-left: 1px solid #E2E8F0;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background-color: #F8FAFC;
        }}

        QComboBox::drop-down:hover {{
            background-color: #EFF6FF;
        }}

        QComboBox::down-arrow {{
            image: url("{chevron}");
            width: 14px;
            height: 14px;
        }}

        QComboBox QAbstractItemView {{
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            padding: 4px;
            outline: 0;
            font-size: 14px;
            font-weight: 500;
            selection-background-color: #2563EB;
            selection-color: #FFFFFF;
        }}

        QComboBox QAbstractItemView::item {{
            min-height: 36px;
            padding: 8px 12px;
            border-radius: 5px;
            color: #0F172A;
            background-color: transparent;
        }}

        QComboBox QAbstractItemView::item:hover {{
            background-color: #EFF6FF;
            color: #1D4ED8;
        }}

        QComboBox QAbstractItemView::item:selected {{
            background-color: #2563EB;
            color: #FFFFFF;
        }}
    """


# ---------------------------------------------------------------------------
# Modern Checkbox & Toggle Style
# ---------------------------------------------------------------------------
def checkbox_style() -> str:
    chk = _checkmark_path()
    return f"""
        QCheckBox {{
            color: #0F172A;
            font-size: 14px;
            font-weight: 600;
            spacing: 10px;
            min-height: 32px;
        }}
        QCheckBox::indicator {{
            width: 22px;
            height: 22px;
            border: 2px solid #CBD5E1;
            border-radius: 6px;
            background-color: #FFFFFF;
        }}
        QCheckBox::indicator:hover {{
            border-color: #2563EB;
            background-color: #F8FAFC;
        }}
        QCheckBox::indicator:checked {{
            border-color: #2563EB;
            background-color: #2563EB;
            image: url("{chk}");
        }}
        QCheckBox::indicator:checked:hover {{
            background-color: #1D4ED8;
            border-color: #1D4ED8;
        }}
        QCheckBox::indicator:disabled {{
            border-color: #E2E8F0;
            background-color: #F1F5F9;
        }}
    """


# ---------------------------------------------------------------------------
# Global Application Theme (Ensures high contrast on all dialogs, modals, popups)
# ---------------------------------------------------------------------------
def app_global_theme() -> str:
    chk = _checkmark_path()
    return f"""
        /* Base Dialog & Window Styling */
        QDialog, QMessageBox, QInputDialog {{
            background-color: #FFFFFF;
            color: #0F172A;
        }}
        QDialog QLabel, QMessageBox QLabel, QInputDialog QLabel {{
            color: #0F172A;
            font-size: 14px;
            font-weight: 500;
        }}

        /* Input Fields: High contrast, clearly readable */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: #FFFFFF;
            color: #0F172A;
            border: 2px solid #CBD5E1;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 14px;
            font-weight: 500;
            selection-background-color: #2563EB;
            selection-color: #FFFFFF;
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border-color: #2563EB;
            background-color: #FFFFFF;
        }}

        /* Dialog & Modal PushButtons (High contrast, touch-friendly min-height) */
        QDialogButtonBox QPushButton,
        QMessageBox QPushButton,
        QInputDialog QPushButton {{
            background-color: #2563EB;
            color: #FFFFFF;
            border: 1.5px solid #1D4ED8;
            border-radius: 8px;
            padding: 9px 20px;
            font-size: 14px;
            font-weight: 700;
            min-height: 40px;
            min-width: 80px;
        }}
        QDialogButtonBox QPushButton:hover,
        QMessageBox QPushButton:hover,
        QInputDialog QPushButton:hover {{
            background-color: #1D4ED8;
            border-color: #1E40AF;
        }}
        QDialogButtonBox QPushButton:pressed,
        QMessageBox QPushButton:pressed,
        QInputDialog QPushButton:pressed {{
            background-color: #1E40AF;
        }}

        /* Specific secondary buttons in dialogs (e.g. Cancel, No, Close) */
        QDialogButtonBox QPushButton[text="Cancel"],
        QDialogButtonBox QPushButton[text="&Cancel"],
        QDialogButtonBox QPushButton[text="No"],
        QDialogButtonBox QPushButton[text="&No"],
        QDialogButtonBox QPushButton[text="Close"],
        QMessageBox QPushButton[text="Cancel"],
        QMessageBox QPushButton[text="&Cancel"],
        QMessageBox QPushButton[text="No"],
        QMessageBox QPushButton[text="&No"] {{
            background-color: #F8FAFC;
            color: #334155;
            border: 1.5px solid #CBD5E1;
        }}
        QDialogButtonBox QPushButton[text="Cancel"]:hover,
        QDialogButtonBox QPushButton[text="&Cancel"]:hover,
        QDialogButtonBox QPushButton[text="No"]:hover,
        QDialogButtonBox QPushButton[text="&No"]:hover,
        QMessageBox QPushButton[text="Cancel"]:hover,
        QMessageBox QPushButton[text="No"]:hover {{
            background-color: #EFF6FF;
            color: #1D4ED8;
            border-color: #93C5FD;
        }}

        /* Scrollbars (touch-friendly smooth scroll) */
        QScrollBar:vertical {{
            border: none;
            background: #F1F5F9;
            width: 10px;
            border-radius: 5px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: #CBD5E1;
            min-height: 24px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: #94A3B8;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """


# ---------------------------------------------------------------------------
# Thin horizontal divider
# ---------------------------------------------------------------------------
DIVIDER_STYLE = "background-color: #E2E8F0; max-height: 1px; min-height: 1px;"


# ---------------------------------------------------------------------------
# Card frame
# ---------------------------------------------------------------------------
def card_style(object_name: str = "") -> str:
    sel = f"QFrame#{object_name}" if object_name else "QFrame"
    return f"""
        {sel} {{
            background-color: #FFFFFF;
            border: 1.5px solid #E2E8F0;
            border-radius: 14px;
        }}
    """


# ---------------------------------------------------------------------------
# Action Buttons (Touch-scaled with min-height >= 44px)
# ---------------------------------------------------------------------------
PRIMARY_BTN = """
    QPushButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 700;
        min-height: 44px;
        letter-spacing: 0.2px;
    }
    QPushButton:hover { background-color: #1D4ED8; }
    QPushButton:pressed { background-color: #1E40AF; }
    QPushButton:disabled { background-color: #BFDBFE; color: #EFF6FF; }
"""

SECONDARY_BTN = """
    QPushButton {
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1.5px solid #CBD5E1;
        border-radius: 10px;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 600;
        min-height: 44px;
    }
    QPushButton:hover { background-color: #F8FAFC; border-color: #93C5FD; color: #1D4ED8; }
    QPushButton:pressed { background-color: #EFF6FF; }
"""

DANGER_BTN = """
    QPushButton {
        background-color: #FEF2F2;
        color: #DC2626;
        border: 1.5px solid #FECACA;
        border-radius: 10px;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 600;
        min-height: 44px;
    }
    QPushButton:hover { background-color: #FEE2E2; border-color: #F87171; }
    QPushButton:pressed { background-color: #FCA5A5; color: #7F1D1D; }
"""

SUCCESS_BTN = """
    QPushButton {
        background-color: #10B981;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 700;
        min-height: 44px;
    }
    QPushButton:hover { background-color: #059669; }
    QPushButton:pressed { background-color: #047857; }
"""
