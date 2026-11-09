from __future__ import annotations

"""Custom vector chess piece renderer for JD Chess.

Renders crisp, outlined Staunton chess pieces at any resolution using vector SVGs
and QPainter. White pieces feature an ivory fill with a deep mahogany outline,
while Black pieces feature an obsidian/ebony fill with a radiant royal gold outline.
This ensures optimal contrast and recognisability against all board square colours.
"""

from PySide6.QtCore import QByteArray, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

# Standard Staunton Vector SVG Paths (viewBox 0 0 45 45)
# Custom styled with rich outlines and distinctive fills.
_WHITE_PIECES_SVG = {
    # Pawn
    "P": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z"
        fill="#FDFBF7" stroke="#2B190E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="22.5" cy="13" r="3.2" fill="#FFFFFF" opacity="0.6"/>
  <path d="M12.5 39.5h20" stroke="#D97706" stroke-width="1.8" stroke-linecap="round"/>
</svg>""",

    # Knight
    "N": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FDFBF7" stroke="#2B190E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M22 10c-3 0-5.5 1.5-6.5 4.5-.5 1.5-.5 4.5 1 6.5.5.7.5 1.5 0 2-1 1-3.5 1.5-5 1.5-1.5 0-2.5-.5-3.5-1-.5-.2-1 .2-.9.7.5 3 2.5 5.5 5.5 6.5.8.3 1.4.9 1.4 1.8v2c0 1.5-1.5 3-3 3.5-1 .3-1 1.5 0 1.5h19c1 0 1-1.2 0-1.5-1.5-.5-3-2-3-3.5v-1c0-.8.4-1.5 1-2 3.5-3 6-7 6-12 0-6.5-5-10.5-11-10.5z"/>
    <circle cx="15.5" cy="17" r="1.5" fill="#2B190E"/>
  </g>
  <path d="M11.5 39.5h22" stroke="#D97706" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M20 12c3 1 6 4 7 8" stroke="#D97706" stroke-width="1.2" fill="none"/>
</svg>""",

    # Bishop
    "B": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FDFBF7" stroke="#2B190E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.35.49-2.32.47-3-.5 1.35-1.46 3-2 3-2z"/>
    <path d="M15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2z"/>
    <circle cx="22.5" cy="8" r="2.2" fill="#D97706"/>
  </g>
  <path d="M17.5 26h10M22.5 12v6" stroke="#2B190E" stroke-width="2" stroke-linecap="round"/>
  <path d="M11 39h23" stroke="#D97706" stroke-width="1.8" stroke-linecap="round"/>
</svg>""",

    # Rook
    "R": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FDFBF7" stroke="#2B190E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M9 39h27v-3H9v3zM12 36v-4h21v4H12zM14 32l1.5-14h14L31 32H14zM11 18h23v-5h-4v2h-4v-2h-7v2h-4v-2h-4v5z"/>
  </g>
  <path d="M14 22h17M14 26h17" stroke="#D97706" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M10 40h25" stroke="#D97706" stroke-width="1.8" stroke-linecap="round"/>
</svg>""",

    # Queen
    "Q": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FDFBF7" stroke="#2B190E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M9 26c8.5-1.5 21-1.5 27 0l2-12-7 11-4-14-4.5 14-4.5-14-4 14-7-11 2 12z"/>
    <path d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 20.5 1 27 0 0 0 2-1 .5-2.5 0 0 0-1.5-1.5-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z"/>
    <circle cx="6" cy="12" r="2" fill="#D97706"/>
    <circle cx="13" cy="9" r="2" fill="#D97706"/>
    <circle cx="22.5" cy="8" r="2" fill="#D97706"/>
    <circle cx="32" cy="9" r="2" fill="#D97706"/>
    <circle cx="39" cy="12" r="2" fill="#D97706"/>
  </g>
  <path d="M11 39h23" stroke="#D97706" stroke-width="1.8" stroke-linecap="round"/>
</svg>""",

    # King
    "K": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FDFBF7" stroke="#2B190E" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M22.5 6v6M19.5 9h6"/>
    <path d="M11.5 37c5.5 3.5 15.5 3.5 21 0V34H11.5v3z"/>
    <path d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0"/>
    <path d="M11.5 30c-2.5-4-2.5-10 1-13 3-2.5 7-1 10-1s7-1.5 10 1c3.5 3 3.5 9 1 13"/>
  </g>
  <path d="M22.5 6v6M19.5 9h6" stroke="#D97706" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M10 40h25" stroke="#D97706" stroke-width="1.8" stroke-linecap="round"/>
</svg>""",
}

_BLACK_PIECES_SVG = {
    # Pawn
    "p": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z"
        fill="#1E140C" stroke="#F59E0B" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="22.5" cy="13" r="2.8" fill="#D97706" opacity="0.7"/>
  <path d="M12.5 39.5h20" stroke="#FDFBF7" stroke-width="1.5" stroke-linecap="round"/>
</svg>""",

    # Knight
    "n": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#1E140C" stroke="#F59E0B" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M22 10c-3 0-5.5 1.5-6.5 4.5-.5 1.5-.5 4.5 1 6.5.5.7.5 1.5 0 2-1 1-3.5 1.5-5 1.5-1.5 0-2.5-.5-3.5-1-.5-.2-1 .2-.9.7.5 3 2.5 5.5 5.5 6.5.8.3 1.4.9 1.4 1.8v2c0 1.5-1.5 3-3 3.5-1 .3-1 1.5 0 1.5h19c1 0 1-1.2 0-1.5-1.5-.5-3-2-3-3.5v-1c0-.8.4-1.5 1-2 3.5-3 6-7 6-12 0-6.5-5-10.5-11-10.5z"/>
    <circle cx="15.5" cy="17" r="1.5" fill="#FDFBF7"/>
  </g>
  <path d="M11.5 39.5h22" stroke="#FDFBF7" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M20 12c3 1 6 4 7 8" stroke="#D97706" stroke-width="1.2" fill="none"/>
</svg>""",

    # Bishop
    "b": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#1E140C" stroke="#F59E0B" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.35.49-2.32.47-3-.5 1.35-1.46 3-2 3-2z"/>
    <path d="M15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2z"/>
    <circle cx="22.5" cy="8" r="2.2" fill="#FDFBF7"/>
  </g>
  <path d="M17.5 26h10M22.5 12v6" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
  <path d="M11 39h23" stroke="#FDFBF7" stroke-width="1.5" stroke-linecap="round"/>
</svg>""",

    # Rook
    "r": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#1E140C" stroke="#F59E0B" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M9 39h27v-3H9v3zM12 36v-4h21v4H12zM14 32l1.5-14h14L31 32H14zM11 18h23v-5h-4v2h-4v-2h-7v2h-4v-2h-4v5z"/>
  </g>
  <path d="M14 22h17M14 26h17" stroke="#D97706" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M10 40h25" stroke="#FDFBF7" stroke-width="1.5" stroke-linecap="round"/>
</svg>""",

    # Queen
    "q": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#1E140C" stroke="#F59E0B" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M9 26c8.5-1.5 21-1.5 27 0l2-12-7 11-4-14-4.5 14-4.5-14-4 14-7-11 2 12z"/>
    <path d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 20.5 1 27 0 0 0 2-1 .5-2.5 0 0 0-1.5-1.5-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z"/>
    <circle cx="6" cy="12" r="2" fill="#FDFBF7"/>
    <circle cx="13" cy="9" r="2" fill="#FDFBF7"/>
    <circle cx="22.5" cy="8" r="2" fill="#FDFBF7"/>
    <circle cx="32" cy="9" r="2" fill="#FDFBF7"/>
    <circle cx="39" cy="12" r="2" fill="#FDFBF7"/>
  </g>
  <path d="M11 39h23" stroke="#FDFBF7" stroke-width="1.5" stroke-linecap="round"/>
</svg>""",

    # King
    "k": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#1E140C" stroke="#F59E0B" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">
    <path d="M22.5 6v6M19.5 9h6"/>
    <path d="M11.5 37c5.5 3.5 15.5 3.5 21 0V34H11.5v3z"/>
    <path d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0"/>
    <path d="M11.5 30c-2.5-4-2.5-10 1-13 3-2.5 7-1 10-1s7-1.5 10 1c3.5 3 3.5 9 1 13"/>
  </g>
  <path d="M22.5 6v6M19.5 9h6" stroke="#FDFBF7" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M10 40h25" stroke="#FDFBF7" stroke-width="1.5" stroke-linecap="round"/>
</svg>""",
}

ALL_SVGS = {**_WHITE_PIECES_SVG, **_BLACK_PIECES_SVG}


class PieceRenderer:
    """Renders custom vector chess pieces and move markers with high-performance caching."""

    def __init__(self) -> None:
        self._renderers: dict[str, QSvgRenderer] = {}
        self._pixmap_cache: dict[tuple[str, int], QPixmap] = {}
        self._marker_cache: dict[tuple[str, int], QPixmap] = {}

        for sym, svg_str in ALL_SVGS.items():
            renderer = QSvgRenderer(QByteArray(svg_str.encode("utf-8")))
            if renderer.isValid():
                self._renderers[sym] = renderer

    def get_piece_pixmap(self, symbol: str, size: int) -> QPixmap:
        """Return a rendered piece pixmap at specified pixel dimension."""
        key = (symbol, size)
        if key in self._pixmap_cache:
            return self._pixmap_cache[key]

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        renderer = self._renderers.get(symbol)
        if renderer and renderer.isValid():
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            renderer.render(painter, QRectF(0, 0, size, size))
            painter.end()

        self._pixmap_cache[key] = pixmap
        return pixmap

    def get_piece_icon(self, symbol: str, size: int) -> QIcon:
        """Return a QIcon containing the rendered piece pixmap."""
        pixmap = self.get_piece_pixmap(symbol, size)
        return QIcon(pixmap)

    def get_move_dot_pixmap(self, size: int) -> QPixmap:
        """Return a clean, centered translucent golden dot for empty legal move destinations."""
        key = ("dot", size)
        if key in self._marker_cache:
            return self._marker_cache[key]

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dot_radius = max(4.0, size * 0.16)
        center = size / 2.0

        # Outer subtle golden glow
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(217, 119, 6, 80))
        painter.drawEllipse(QRectF(center - dot_radius - 2, center - dot_radius - 2, (dot_radius + 2) * 2, (dot_radius + 2) * 2))

        # Main solid gold core
        painter.setBrush(QColor(245, 158, 11, 230))
        painter.drawEllipse(QRectF(center - dot_radius, center - dot_radius, dot_radius * 2, dot_radius * 2))

        painter.end()
        self._marker_cache[key] = pixmap
        return pixmap

    def get_capture_target_pixmap(self, symbol: str, size: int) -> QPixmap:
        """Render piece with a striking capture ring and corner brackets."""
        key = (f"cap_{symbol}", size)
        if key in self._marker_cache:
            return self._marker_cache[key]

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Draw subtle red/gold capture background ring
        pad = max(2.0, size * 0.04)
        ring_rect = QRectF(pad, pad, size - pad * 2, size - pad * 2)

        # Outer pulsing danger halo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(239, 68, 68, 60))
        painter.drawRoundedRect(ring_rect, 8, 8)

        # Capture border ring
        pen = painter.pen()
        pen.setColor(QColor(239, 68, 68, 220))
        pen.setWidthF(max(2.0, size * 0.05))
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(ring_rect, 8, 8)

        # 2. Render piece inside
        renderer = self._renderers.get(symbol)
        if renderer and renderer.isValid():
            piece_pad = max(4.0, size * 0.08)
            piece_rect = QRectF(piece_pad, piece_pad, size - piece_pad * 2, size - piece_pad * 2)
            renderer.render(painter, piece_rect)

        painter.end()
        self._marker_cache[key] = pixmap
        return pixmap


# Global singleton instance for efficient sharing across widgets
_GLOBAL_RENDERER: PieceRenderer | None = None


def get_piece_renderer() -> PieceRenderer:
    global _GLOBAL_RENDERER
    if _GLOBAL_RENDERER is None:
        _GLOBAL_RENDERER = PieceRenderer()
    return _GLOBAL_RENDERER
