from __future__ import annotations

"""Staunton Vector Piece Theme & Proportional Scaler for JD Chess (Warm Beige & Walnut).

Renders classical, elegant Staunton chess pieces calibrated to occupy ~70-75% of
each square with refined line weights, balanced negative space, and traditional aesthetics.
White pieces feature a warm ivory fill with a crisp espresso-walnut contour line.
Black pieces feature a deep espresso-walnut fill with an ivory contour line for optimal contrast.
"""

from PySide6.QtCore import QByteArray, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

import app.ui.piece_renderer as pr
from app.ui.piece_renderer import PieceRenderer

# ---------------------------------------------------------------------------
# Classical Staunton Vector SVG Definitions (viewBox 0 0 45 45)
# Sized and centered for balanced 70-75% square proportions
# ---------------------------------------------------------------------------

_STAUNTON_WHITE_SVG = {
    # Pawn
    "P": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <path d="m 22.5,9 c -2.21,0 -4,1.79 -4,4 0,0.89 0.29,1.71 0.78,2.38 C 17.33,16.5 16,18.59 16,21 c 0,2.03 0.94,3.84 2.41,5.03 C 15.41,27.09 11,31.58 11,39.5 l 23,0 c 0,-7.92 -4.41,-12.41 -7.41,-13.47 1.47,-1.19 2.41,-3 2.41,-5.03 0,-2.41 -1.33,-4.5 -3.28,-5.62 c 0.49,-0.67 0.78,-1.49 0.78,-2.38 0,-2.21 -1.79,-4 -4,-4 z"
        fill="#FFFDF9" stroke="#3D2B1F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    # Knight
    "N": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FFFDF9" stroke="#3D2B1F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 22,10 c -3,0 -5.5,1.5 -6.5,4.5 -0.5,1.5 -0.5,4.5 1,6.5 0.5,0.7 0.5,1.5 0,2 -1,1 -3.5,1.5 -5,1.5 -1.5,0 -2.5,-0.5 -3.5,-1 -0.5,-0.2 -1,0.2 -0.9,0.7 0.5,3 2.5,5.5 5.5,6.5 0.8,0.3 1.4,0.9 1.4,1.8 l 0,2 c 0,1.5 -1.5,3 -3,3.5 -1,0.3 -1,1.5 0,1.5 l 19,0 c 1,0 1,-1.2 0,-1.5 -1.5,-0.5 -3,-2 -3,-3.5 l 0,-1 c 0,-0.8 0.4,-1.5 1,-2 3.5,-3 6,-7 6,-12 0,-6.5 -5,-10.5 -11,-10.5 z"/>
    <path d="m 24,18 c 0.38,2.91 -5.55,7.37 -8,9 -3,2 -2.82,4.34 -5,4 -1.04,-0.94 -1.41,-3.04 0,-3 1,0 0.19,1.23 -1,2 -1,0 -4.09,0.31 -4,-4 0,-2 4.09,-0.75 4,-2 0,0 -1,-0.5 -1,-1 0.77,-1.39 3,-2 4,-1 1.76,0.32 2.11,-0.58 2,-2 -0.45,-1.37 -2.48,-1.7 -3,-3 -0.22,-0.56 0.29,-1.21 1,-1 2.45,0.73 4.14,2.57 6,2 1.34,-0.41 1.63,-1.93 2,-3 0.28,-0.82 1.5,-0.78 2,-0.5 0.53,0.3 0.87,0.9 1,1.5 z" fill="#FFFDF9" stroke="#3D2B1F" stroke-width="1"/>
    <circle cx="15" cy="17" r="1.2" fill="#3D2B1F"/>
  </g>
</svg>""",

    # Bishop
    "B": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FFFDF9" stroke="#3D2B1F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 9,36 c 3.39,-0.97 10.11,0.43 13.5,-2 3.39,2.43 10.11,1.03 13.5,2 0,0 1.65,0.54 3,2 -0.68,0.97 -1.65,0.99 -3,0.5 -3.39,-0.97 -10.11,0.46 -13.5,-1 -3.39,1.46 -10.11,0.03 -13.5,1 -1.35,0.49 -2.32,0.47 -3,-0.5 1.35,-1.46 3,-2 3,-2 z"/>
    <path d="m 15,32 c 2.5,2.5 12.5,2.5 15,0 0.5,-1.5 0,-2 0,-2 0,-2.5 -2.5,-4 -2.5,-4 5.5,-1.5 6,-11.5 -5,-15.5 -11,4 -10.5,14 -5,15.5 0,0 -2.5,1.5 -2.5,4 0,0 -0.5,0.5 0,2 z"/>
    <circle cx="22.5" cy="8" r="2.2"/>
    <path d="m 17.5,26 10,0 M 22.5,12 22.5,18" stroke-width="1.5"/>
  </g>
</svg>""",

    # Rook
    "R": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FFFDF9" stroke="#3D2B1F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 9,39 27,0 0,-3 -27,0 0,3 z m 3,-3 0,-4 21,0 0,4 -21,0 z m 2,-4 1.5,-14 14,0 1.5,14 -17,0 z m -3,-14 23,0 0,-5 -4,0 0,2 -4,0 0,-2 -7,0 0,2 -4,0 0,-2 -4,0 0,5 z"/>
    <path d="m 14,22 17,0 M 14,26 17,26" stroke-width="1.2"/>
  </g>
</svg>""",

    # Queen
    "Q": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FFFDF9" stroke="#3D2B1F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 9,26 c 8.5,-1.5 21,-1.5 27,0 l 2,-12 -7,11 -4,-14 -4.5,14 -4.5,-14 -4,14 -7,-11 2,12 z"/>
    <path d="m 9,26 c 0,2 1.5,2 2.5,4 1,1.5 1,1 0.5,3.5 -1.5,1 -1.5,2.5 -1.5,2.5 -1.5,1.5 0.5,2.5 0.5,2.5 6.5,1 20.5,1 27,0 0,0 2,-1 0.5,-2.5 0,0 0,-1.5 -1.5,-2.5 -0.5,-2.5 -0.5,-2 0.5,-3.5 1,-2 2.5,-2 2.5,-4 -8.5,-1.5 -18.5,-1.5 -27,0 z"/>
    <circle cx="6" cy="12" r="2"/>
    <circle cx="13" cy="9" r="2"/>
    <circle cx="22.5" cy="8" r="2"/>
    <circle cx="32" cy="9" r="2"/>
    <circle cx="39" cy="12" r="2"/>
    <path d="m 11,38.5 23,0" stroke-width="1.5"/>
  </g>
</svg>""",

    # King
    "K": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#FFFDF9" stroke="#3D2B1F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 22.5,6 0,6 M 19.5,9 25.5,9" stroke-width="1.6"/>
    <path d="m 11.5,37 c 5.5,3.5 15.5,3.5 21,0 l 0,-3 -21,0 0,3 z"/>
    <path d="m 11.5,30 c 5.5,-3 15.5,-3 21,0 m -21,3.5 c 5.5,-3 15.5,-3 21,0"/>
    <path d="m 11.5,30 c -2.5,-4 -2.5,-10 1,-13 3,-2.5 7,-1 10,-1 3,0 7,-1.5 10,1 3.5,3 3.5,9 1,13"/>
  </g>
</svg>""",
}

_STAUNTON_BLACK_SVG = {
    # Pawn
    "p": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <path d="m 22.5,9 c -2.21,0 -4,1.79 -4,4 0,0.89 0.29,1.71 0.78,2.38 C 17.33,16.5 16,18.59 16,21 c 0,2.03 0.94,3.84 2.41,5.03 C 15.41,27.09 11,31.58 11,39.5 l 23,0 c 0,-7.92 -4.41,-12.41 -7.41,-13.47 1.47,-1.19 2.41,-3 2.41,-5.03 0,-2.41 -1.33,-4.5 -3.28,-5.62 c 0.49,-0.67 0.78,-1.49 0.78,-2.38 0,-2.21 -1.79,-4 -4,-4 z"
        fill="#2E2017" stroke="#EADECA" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="22.5" cy="13" r="2.5" fill="none" stroke="#EADECA" stroke-width="1" opacity="0.6"/>
  <path d="M 14,37.5 31,37.5" stroke="#EADECA" stroke-width="1" stroke-linecap="round"/>
</svg>""",

    # Knight
    "n": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#2E2017" stroke="#EADECA" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 22,10 c -3,0 -5.5,1.5 -6.5,4.5 -0.5,1.5 -0.5,4.5 1,6.5 0.5,0.7 0.5,1.5 0,2 -1,1 -3.5,1.5 -5,1.5 -1.5,0 -2.5,-0.5 -3.5,-1 -0.5,-0.2 -1,0.2 -0.9,0.7 0.5,3 2.5,5.5 5.5,6.5 0.8,0.3 1.4,0.9 1.4,1.8 l 0,2 c 0,1.5 -1.5,3 -3,3.5 -1,0.3 -1,1.5 0,1.5 l 19,0 c 1,0 1,-1.2 0,-1.5 -1.5,-0.5 -3,-2 -3,-3.5 l 0,-1 c 0,-0.8 0.4,-1.5 1,-2 3.5,-3 6,-7 6,-12 0,-6.5 -5,-10.5 -11,-10.5 z"/>
    <path d="m 24,18 c 0.38,2.91 -5.55,7.37 -8,9 -3,2 -2.82,4.34 -5,4 -1.04,-0.94 -1.41,-3.04 0,-3 1,0 0.19,1.23 -1,2 -1,0 -4.09,0.31 -4,-4 0,-2 4.09,-0.75 4,-2 0,0 -1,-0.5 -1,-1 0.77,-1.39 3,-2 4,-1 1.76,0.32 2.11,-0.58 2,-2 -0.45,-1.37 -2.48,-1.7 -3,-3 -0.22,-0.56 0.29,-1.21 1,-1 2.45,0.73 4.14,2.57 6,2 1.34,-0.41 1.63,-1.93 2,-3 0.28,-0.82 1.5,-0.78 2,-0.5 0.53,0.3 0.87,0.9 1,1.5 z" fill="#2E2017" stroke="#EADECA" stroke-width="1"/>
    <circle cx="15" cy="17" r="1.2" fill="#EADECA"/>
  </g>
</svg>""",

    # Bishop
    "b": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#2E2017" stroke="#EADECA" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 9,36 c 3.39,-0.97 10.11,0.43 13.5,-2 3.39,2.43 10.11,1.03 13.5,2 0,0 1.65,0.54 3,2 -0.68,0.97 -1.65,0.99 -3,0.5 -3.39,-0.97 -10.11,0.46 -13.5,-1 -3.39,1.46 -10.11,0.03 -13.5,1 -1.35,0.49 -2.32,0.47 -3,-0.5 1.35,-1.46 3,-2 3,-2 z"/>
    <path d="m 15,32 c 2.5,2.5 12.5,2.5 15,0 0.5,-1.5 0,-2 0,-2 0,-2.5 -2.5,-4 -2.5,-4 5.5,-1.5 6,-11.5 -5,-15.5 -11,4 -10.5,14 -5,15.5 0,0 -2.5,1.5 -2.5,4 0,0 -0.5,0.5 0,2 z"/>
    <circle cx="22.5" cy="8" r="2.2" fill="#EADECA" stroke="none"/>
    <path d="m 17.5,26 10,0 M 22.5,12 22.5,18" stroke-width="1.4" stroke="#EADECA"/>
  </g>
</svg>""",

    # Rook
    "r": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#2E2017" stroke="#EADECA" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 9,39 27,0 0,-3 -27,0 0,3 z m 3,-3 0,-4 21,0 0,4 -21,0 z m 2,-4 1.5,-14 14,0 1.5,14 -17,0 z m -3,-14 23,0 0,-5 -4,0 0,2 -4,0 0,-2 -7,0 0,2 -4,0 0,-2 -4,0 0,5 z"/>
    <path d="m 14,22 17,0 M 14,26 17,26" stroke-width="1" stroke="#EADECA"/>
  </g>
</svg>""",

    # Queen
    "q": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#2E2017" stroke="#EADECA" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 9,26 c 8.5,-1.5 21,-1.5 27,0 l 2,-12 -7,11 -4,-14 -4.5,14 -4.5,-14 -4,14 -7,-11 2,12 z"/>
    <path d="m 9,26 c 0,2 1.5,2 2.5,4 1,1.5 1,1 0.5,3.5 -1.5,1 -1.5,2.5 -1.5,2.5 -1.5,1.5 0.5,2.5 0.5,2.5 6.5,1 20.5,1 27,0 0,0 2,-1 0.5,-2.5 0,0 0,-1.5 -1.5,-2.5 -0.5,-2.5 -0.5,-2 0.5,-3.5 1,-2 2.5,-2 2.5,-4 -8.5,-1.5 -18.5,-1.5 -27,0 z"/>
    <circle cx="6" cy="12" r="2" fill="#EADECA" stroke="none"/>
    <circle cx="13" cy="9" r="2" fill="#EADECA" stroke="none"/>
    <circle cx="22.5" cy="8" r="2" fill="#EADECA" stroke="none"/>
    <circle cx="32" cy="9" r="2" fill="#EADECA" stroke="none"/>
    <circle cx="39" cy="12" r="2" fill="#EADECA" stroke="none"/>
    <path d="m 11,38.5 23,0" stroke-width="1.2" stroke="#EADECA"/>
  </g>
</svg>""",

    # King
    "k": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45">
  <g fill="#2E2017" stroke="#EADECA" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="m 22.5,6 0,6 M 19.5,9 25.5,9" stroke-width="1.5" stroke="#EADECA"/>
    <path d="m 11.5,37 c 5.5,3.5 15.5,3.5 21,0 l 0,-3 -21,0 0,3 z"/>
    <path d="m 11.5,30 c 5.5,-3 15.5,-3 21,0 m -21,3.5 c 5.5,-3 15.5,-3 21,0"/>
    <path d="m 11.5,30 c -2.5,-4 -2.5,-10 1,-13 3,-2.5 7,-1 10,-1 3,0 7,-1.5 10,1 3.5,3 3.5,9 1,13"/>
  </g>
</svg>""",
}

STAUNTON_SVGS = {**_STAUNTON_WHITE_SVG, **_STAUNTON_BLACK_SVG}


class StauntonPieceRenderer(PieceRenderer):
    """Refined Staunton piece renderer with calibrated 70-75% square proportions."""

    def __init__(self) -> None:
        super().__init__()
        self._staunton_renderers: dict[str, QSvgRenderer] = {}
        for sym, svg_str in STAUNTON_SVGS.items():
            renderer = QSvgRenderer(QByteArray(svg_str.encode("utf-8")))
            if renderer.isValid():
                self._staunton_renderers[sym] = renderer

    def get_piece_pixmap(self, symbol: str, size: int) -> QPixmap:
        """Return a rendered piece pixmap scaled to ~72% of square dimension with centered margins."""
        key = (f"staunton_{symbol}", size)
        if key in self._pixmap_cache:
            return self._pixmap_cache[key]

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        renderer = self._staunton_renderers.get(symbol) or self._renderers.get(symbol)
        if renderer and renderer.isValid():
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Sizing calibration:
            # chessboard_widget passes icon_size = int(square_size * 0.82)
            # To achieve ~72% of square width for visible piece, scale factor is (0.72 / 0.82) = ~0.88
            target_scale = 0.88
            piece_w = size * target_scale
            piece_h = size * target_scale
            offset_x = (size - piece_w) / 2.0
            offset_y = (size - piece_h) / 2.0

            renderer.render(painter, QRectF(offset_x, offset_y, piece_w, piece_h))
            painter.end()

        self._pixmap_cache[key] = pixmap
        return pixmap

    def get_piece_icon(self, symbol: str, size: int) -> QIcon:
        pixmap = self.get_piece_pixmap(symbol, size)
        return QIcon(pixmap)

    def get_move_dot_pixmap(self, size: int) -> QPixmap:
        """Subtle, traditional translucent walnut dot for legal move destinations."""
        key = ("staunton_dot", size)
        if key in self._marker_cache:
            return self._marker_cache[key]

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dot_radius = max(3.5, size * 0.13)
        center = size / 2.0

        # Outer subtle walnut halo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(61, 43, 31, 40))
        painter.drawEllipse(QRectF(center - dot_radius - 2, center - dot_radius - 2, (dot_radius + 2) * 2, (dot_radius + 2) * 2))

        # Main walnut core
        painter.setBrush(QColor(74, 53, 37, 180))
        painter.drawEllipse(QRectF(center - dot_radius, center - dot_radius, dot_radius * 2, dot_radius * 2))

        painter.end()
        self._marker_cache[key] = pixmap
        return pixmap

    def get_capture_target_pixmap(self, symbol: str, size: int) -> QPixmap:
        """Render piece with subtle, elegant terracotta-walnut capture corner indicators."""
        key = (f"staunton_cap_{symbol}", size)
        if key in self._marker_cache:
            return self._marker_cache[key]

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Subtle, understated capture frame
        pad = max(2.0, size * 0.05)
        ring_rect = QRectF(pad, pad, size - pad * 2, size - pad * 2)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(168, 68, 48, 40))
        painter.drawRoundedRect(ring_rect, 6, 6)

        pen = painter.pen()
        pen.setColor(QColor(168, 68, 48, 180))
        pen.setWidthF(max(1.5, size * 0.04))
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(ring_rect, 6, 6)

        # 2. Render piece inside with same ~72% proportion
        renderer = self._staunton_renderers.get(symbol) or self._renderers.get(symbol)
        if renderer and renderer.isValid():
            target_scale = 0.88
            piece_w = size * target_scale
            piece_h = size * target_scale
            offset_x = (size - piece_w) / 2.0
            offset_y = (size - piece_h) / 2.0
            renderer.render(painter, QRectF(offset_x, offset_y, piece_w, piece_h))

        painter.end()
        self._marker_cache[key] = pixmap
        return pixmap


def install_staunton_theme() -> StauntonPieceRenderer:
    """Activate StauntonPieceRenderer as the global renderer for all chessboard widgets."""
    renderer = StauntonPieceRenderer()
    pr._GLOBAL_RENDERER = renderer
    return renderer
