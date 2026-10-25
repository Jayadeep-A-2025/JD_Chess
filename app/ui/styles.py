from __future__ import annotations

"""Shared stylesheet helpers for consistent, modern dropdown/combo-box styling."""

from pathlib import Path


def _chevron_path() -> str:
    icons_dir = (
        Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
    )
    return (icons_dir / "chevron-down.svg").as_posix()


# ---------------------------------------------------------------------------
# Combo-box style  (call once, cache the result)
# ---------------------------------------------------------------------------
def combo_style() -> str:
    chevron = _chevron_path()
    return f"""
        QComboBox {{
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1.5px solid #CBD5E1;
            border-radius: 10px;
            padding: 9px 14px;
            font-size: 13px;
            font-weight: 600;
            min-height: 30px;
            selection-background-color: #EFF6FF;
        }}
        QComboBox:hover {{
            border-color: #93C5FD;
            background-color: #F8FAFC;
        }}
        QComboBox:focus {{
            border-color: #2563EB;
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
            width: 34px;
            border-left: 1.5px solid #E2E8F0;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            background-color: #F8FAFC;
        }}
        QComboBox::drop-down:hover {{
            background-color: #EFF6FF;
        }}
        QComboBox::down-arrow {{
            image: url("{chevron}");
            width: 13px;
            height: 13px;
        }}
        QComboBox QAbstractItemView {{
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1.5px solid #CBD5E1;
            border-radius: 10px;
            selection-background-color: #2563EB;
            selection-color: #FFFFFF;
            padding: 6px;
            outline: none;
            font-size: 13px;
            font-weight: 500;
        }}
        QComboBox QAbstractItemView::item {{
            padding: 6px 10px;
            border-radius: 6px;
            min-height: 26px;
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: #EFF6FF;
            color: #1D4ED8;
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
# Primary CTA button (blue)
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
        letter-spacing: 0.2px;
    }
    QPushButton:hover { background-color: #1D4ED8; }
    QPushButton:pressed { background-color: #1E40AF; }
    QPushButton:disabled { background-color: #BFDBFE; color: #EFF6FF; }
"""

# Secondary / ghost button
SECONDARY_BTN = """
    QPushButton {
        background-color: #FFFFFF;
        color: #334155;
        border: 1.5px solid #CBD5E1;
        border-radius: 10px;
        padding: 9px 18px;
        font-size: 13px;
        font-weight: 600;
    }
    QPushButton:hover { background-color: #F8FAFC; border-color: #93C5FD; }
    QPushButton:pressed { background-color: #EFF6FF; }
"""

# Danger / destructive button (red)
DANGER_BTN = """
    QPushButton {
        background-color: transparent;
        color: #DC2626;
        border: 1.5px solid #FECACA;
        border-radius: 10px;
        padding: 9px 18px;
        font-size: 13px;
        font-weight: 600;
    }
    QPushButton:hover { background-color: #FEF2F2; }
    QPushButton:pressed { background-color: #FEE2E2; }
"""

# Success button (green)
SUCCESS_BTN = """
    QPushButton {
        background-color: #10B981;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 700;
    }
    QPushButton:hover { background-color: #059669; }
    QPushButton:pressed { background-color: #047857; }
"""
