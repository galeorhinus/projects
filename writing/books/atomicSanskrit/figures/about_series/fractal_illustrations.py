"""Stdlib-only SVG generator for the About-the-Series three-fractals
triptych.

Produces eight SVGs into ``figures/build/about_series/``:

  - prakṛti — about_series_prakrti_tree.svg
  - prakṛti — about_series_prakrti_fern.svg
  - vikṛti — about_series_vikrti_pyramid_simple.svg
  - vikṛti — about_series_vikrti_pyramid_sierpinski.svg
  - vikṛti — about_series_vikrti_pyramid_nested.svg
  - saṃskṛti — about_series_samskrti_swastika_simple.svg
  - saṃskṛti — about_series_samskrti_swastika_fractal.svg
  - saṃskṛti — about_series_samskrti_swastika_tessellated.svg

No matplotlib / numpy dependency — pure Python.
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

FILL = "#222222"
WHITE = "#ffffff"

# --- SVG primitives ----------------------------------------------------------


def svg_open(width: float, height: float, view: tuple[float, float, float, float]):
    minx, miny, w, h = view
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="{minx} {miny} {w} {h}">\n'
    )


def svg_close() -> str:
    return "</svg>\n"


def line(x1, y1, x2, y2, stroke=FILL, lw=1.0, linecap="round"):
    return (
        f'  <line x1="{x1:.4f}" y1="{y1:.4f}" x2="{x2:.4f}" y2="{y2:.4f}" '
        f'stroke="{stroke}" stroke-width="{lw}" stroke-linecap="{linecap}" />\n'
    )


def polyline(points: Iterable[tuple[float, float]], stroke=FILL, lw=1.0,
             linecap="butt", linejoin="miter"):
    pts = " ".join(f"{x:.4f},{y:.4f}" for x, y in points)
    return (
        f'  <polyline points="{pts}" fill="none" stroke="{stroke}" '
        f'stroke-width="{lw}" stroke-linecap="{linecap}" '
        f'stroke-linejoin="{linejoin}" />\n'
    )


def polygon(points: Iterable[tuple[float, float]], fill=FILL, stroke="none",
            lw=0.0):
    pts = " ".join(f"{x:.4f},{y:.4f}" for x, y in points)
    sw = f' stroke-width="{lw}"' if stroke != "none" else ""
    return (
        f'  <polygon points="{pts}" fill="{fill}" stroke="{stroke}"{sw} />\n'
    )


def rect(x, y, w, h, fill=FILL):
    return f'  <rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" fill="{fill}" />\n'


def write(name: str, body: str, *, width=350, height=350, view=None,
          white_background=False):
    if view is None:
        view = (-1.4, -1.4, 2.8, 2.8)
    path = OUT_DIR / f"{name}.svg"
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_open(width, height, view))
        if white_background:
            minx, miny, w, h = view
            f.write(
                f'  <rect x="{minx}" y="{miny}" width="{w}" height="{h}" '
                f'fill="#ffffff" />\n'
            )
        f.write(body)
        f.write(svg_close())
    print(f"Wrote {path.relative_to(PROJECT_ROOT)}")


# --- Helpers ----------------------------------------------------------------
# SVG y axis is positive downward.  All figures below are written in
# "math" coordinates (y up) and flipped at output time per view.


def flip_y(points: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    """No-op stub: viewBox handles axis orientation via negative scales when
    needed.  In practice we use SVG-native coordinates throughout."""
    return list(points)


# --- 1. prakṛti: fractal tree (binary L-system) ------------------------------


def render_tree() -> str:
    body = []

    def draw(x, y, angle, length, depth, lw):
        if depth == 0 or length < 0.01:
            return
        x2 = x + length * math.cos(angle)
        y2 = y - length * math.sin(angle)  # SVG y is down; tree grows up
        body.append(line(x, y, x2, y2, stroke=FILL, lw=lw))
        new_length = length * 0.72
        new_lw = max(lw * 0.7, 0.4)
        spread = math.radians(28)
        draw(x2, y2, angle + spread, new_length, depth - 1, new_lw)
        draw(x2, y2, angle - spread, new_length, depth - 1, new_lw)

    # Tree base at (0, 0) growing upward (angle = π/2)
    draw(0, 0, math.pi / 2, 1.0, 9, 4.5)
    return "".join(body)


# --- 2. prakṛti: Barnsley fern ----------------------------------------------


def render_fern() -> str:
    """Barnsley fern via iterated function system."""
    transforms = [
        (0.00, 0.00, 0.00, 0.16, 0.00, 0.00, 0.01),  # stem
        (0.85, 0.04, -0.04, 0.85, 0.00, 1.60, 0.85),
        (0.20, -0.26, 0.23, 0.22, 0.00, 1.60, 0.07),
        (-0.15, 0.28, 0.26, 0.24, 0.00, 0.44, 0.07),
    ]
    cum_probs = []
    cum = 0.0
    for t in transforms:
        cum += t[6]
        cum_probs.append(cum)

    random.seed(0)
    x, y = 0.0, 0.0
    n_points = 7000
    # Single <path> with many tiny subpath line-strokes, far more compact
    # than per-point <rect>/<circle> elements.  Each subpath:
    #   "M X,Y h 0.01 "   ~ 18 chars at 3-decimal precision.
    parts = []
    for _ in range(n_points):
        r = random.random()
        for i, cp in enumerate(cum_probs):
            if r <= cp:
                a, b, c, d, e, f, _ = transforms[i]
                x, y = a * x + b * y + e, c * x + d * y + f
                break
        parts.append(f"M{x:.3f},{-y:.3f}h0.012")
    d_attr = "".join(parts)
    return (
        f'  <path d="{d_attr}" stroke="{FILL}" stroke-width="0.018" '
        f'fill="none" stroke-linecap="round" />\n'
    )


# --- 3. vikṛti: simple stepped pyramid --------------------------------------


def render_pyramid_simple() -> str:
    apex = (0.0, -1.0)
    base_left = (-1.0, 0.0)
    base_right = (1.0, 0.0)
    body = [polygon([apex, base_right, base_left], fill=FILL)]
    # Horizontal strata
    n_strata = 6
    for i in range(1, n_strata):
        y_norm = i / n_strata  # 0 at apex, 1 at base — invert for SVG
        # In SVG coords: apex at y = -1, base at y = 0.
        y_svg = -1.0 + i / n_strata
        half_width = i / n_strata
        body.append(
            line(
                -half_width, y_svg, half_width, y_svg,
                stroke=WHITE, lw=0.012, linecap="butt"
            )
        )
    return "".join(body)


# --- 4. vikṛti: canonical Sierpinski triangle -------------------------------


def render_pyramid_sierpinski() -> str:
    """Equilateral Sierpinski triangle, filled triangles in dark."""
    # Equilateral triangle: apex at top, base on bottom
    apex = (0.0, -1.0)
    base_left = (-1.0, 0.732)  # tan(60°) gives height = √3 ≈ 1.732 from apex
    base_right = (1.0, 0.732)
    # Adjust to a unit-bounded square
    apex = (0.0, -1.0)
    base_left = (-1.0, 0.155)
    base_right = (1.0, 0.155)
    body = []

    def mid(p, q):
        return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

    def sierp(A, B, C, depth):
        if depth == 0:
            body.append(polygon([A, B, C], fill=FILL))
            return
        AB = mid(A, B)
        BC = mid(B, C)
        CA = mid(C, A)
        sierp(A, AB, CA, depth - 1)
        sierp(AB, B, BC, depth - 1)
        sierp(CA, BC, C, depth - 1)

    sierp(apex, base_right, base_left, depth=5)
    return "".join(body)


# --- 5. vikṛti: nested pyramid (no negative space) --------------------------


def render_pyramid_nested() -> str:
    """Nested-pyramid recursion, no holes.  Each level darkens."""
    apex = (0.0, -1.0)
    base_left = (-1.0, 0.155)
    base_right = (1.0, 0.155)
    body = []

    def mid(p, q):
        return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

    def gray_hex(value: float) -> str:
        v = max(0, min(255, int(value * 255)))
        return f"#{v:02x}{v:02x}{v:02x}"

    def nested(A, B, C, depth, gray):
        body.append(
            polygon([A, B, C], fill=gray_hex(gray), stroke=WHITE, lw=0.006)
        )
        if depth == 0:
            return
        AB = mid(A, B)
        BC = mid(B, C)
        CA = mid(C, A)
        next_gray = max(gray - 0.18, 0.05)
        nested(A, AB, CA, depth - 1, next_gray)
        nested(AB, B, BC, depth - 1, next_gray)
        nested(CA, BC, C, depth - 1, next_gray)

    nested(apex, base_right, base_left, depth=3, gray=0.65)
    return "".join(body)


# --- 6. saṃskṛti: simple svastika -------------------------------------------


def svastika(cx: float, cy: float, size: float, lw: float, stroke=FILL,
             bend_ratio: float = 0.55) -> str:
    """Single Indic right-facing (clockwise dharmic) svastika.

    SVG y is positive downward.  Indic right-facing svastika geometry:
      - top arm: center → up → bend right
      - right arm: center → right → bend down
      - bottom arm: center → down → bend left
      - left arm: center → left → bend up

    bend_ratio controls how far each arm's bent tip extends as a fraction
    of the arm length.  Default 0.55 (matches the canonical icon); set to
    1.0 for an equal-arm-and-bend svastika ("full-length edge").
    """
    h = size
    b = size * bend_ratio
    # In SVG coords (y-down):
    #   up    → cy - h
    #   down  → cy + h
    #   right → cx + h or cx + b
    #   left  → cx - h or cx - b
    arms = [
        # top arm: down→up at center, then bend right at top
        [(cx, cy), (cx, cy - h), (cx + b, cy - h)],
        # right arm: center → right, then bend down
        [(cx, cy), (cx + h, cy), (cx + h, cy + b)],
        # bottom arm: center → down, then bend left
        [(cx, cy), (cx, cy + h), (cx - b, cy + h)],
        # left arm: center → left, then bend up
        [(cx, cy), (cx - h, cy), (cx - h, cy - b)],
    ]
    return "".join(
        polyline(arm, stroke=stroke, lw=lw, linecap="butt", linejoin="miter")
        for arm in arms
    )


def render_swastika_simple() -> str:
    return svastika(cx=0.0, cy=0.0, size=1.0, lw=0.22)


# --- 7. saṃskṛti: fractal svastika ------------------------------------------


def render_swastika_fractal() -> str:
    """Central svastika with smaller svastikas at arm-tips, recursing 2 levels."""
    body = []

    def draw(cx, cy, size, lw, depth):
        body.append(svastika(cx, cy, size, lw))
        if depth == 0:
            return
        h = size
        b = size * 0.55
        # Arm-tip positions (the bent ends, SVG coords y-down):
        tips = [
            (cx + b, cy - h),  # top
            (cx + h, cy + b),  # right
            (cx - b, cy + h),  # bottom
            (cx - h, cy - b),  # left
        ]
        smaller_size = size * 0.32
        smaller_lw = max(lw * 0.55, 0.025)
        for tx, ty in tips:
            draw(tx, ty, smaller_size, smaller_lw, depth - 1)

    draw(0.0, 0.0, 1.0, 0.20, depth=2)
    return "".join(body)


# --- 8. saṃskṛti: tessellated svastika --------------------------------------


def render_swastika_tessellated() -> str:
    body = []
    n = 5
    size = 0.36
    spacing = 1.0
    lw = 0.07
    for i in range(n):
        for j in range(n):
            cx = (i - (n - 1) / 2.0) * spacing
            cy = (j - (n - 1) / 2.0) * spacing
            body.append(svastika(cx, cy, size, lw))
    return "".join(body)


# --- 9. saṃskṛti: distributive tessellation (no apex) -----------------------
# Each svastika links to its neighbors via thin connector segments running
# between bend-tips.  Geometry: arm length a = 1, bend length b = 0.55
# (matches the simple-svastika icon).  Step vectors in SVG (y-down) coords:
#   Step A (top-bend → bottom-bend via horizontal connector):
#       (2b + c, -2a) = (1.1 + c, -2)
#   Step B (right-bend → left-bend via vertical connector):
#       (2a, 2b + c) = (2, 1.1 + c)
# c = 0.5 matches the sketch's proportions; c = 1.0 yields the closer-to-
# symmetric (2.1, ±2) tile.  The pattern reads as distributive — no svastika
# is privileged as a center, the same shape repeats across space, the
# tessellation continues beyond whatever frame the figure crops to.


def connector(x1: float, y1: float, x2: float, y2: float,
              lw: float = 0.08, stroke: str = "#888888") -> str:
    return (
        f'  <line x1="{x1:.4f}" y1="{y1:.4f}" '
        f'x2="{x2:.4f}" y2="{y2:.4f}" '
        f'stroke="{stroke}" stroke-width="{lw}" stroke-linecap="butt" />\n'
    )


def _tessellated_positions(c_length: float, grid_extent: int
                           ) -> list[tuple[float, float]]:
    """Generate svastika center positions on the tessellation lattice."""
    step_a = (1.1 + c_length, -2.0)   # top → bottom, horizontal connector
    step_b = (2.0, 1.1 + c_length)    # right → left, vertical connector
    positions = []
    for i in range(-grid_extent, grid_extent + 1):
        for j in range(-grid_extent, grid_extent + 1):
            cx = i * step_a[0] + j * step_b[0]
            cy = i * step_a[1] + j * step_b[1]
            positions.append((cx, cy))
    return positions


def render_swastika_distributive(c_length: float, grid_extent: int,
                                 svastika_lw: float = 0.20,
                                 connector_lw: float = 0.08,
                                 svastika_color: str = FILL,
                                 connector_color: str = "#aaaaaa"
                                 ) -> tuple[str, tuple[float, float, float, float]]:
    """Render a distributive tessellation of svastikas with thin connectors.

    Returns (svg_body, viewbox) where viewbox = (xmin, ymin, width, height).
    """
    a = 1.0
    b = 0.55
    c = c_length
    step_a = (1.1 + c, -2.0)
    step_b = (2.0, 1.1 + c)
    positions = _tessellated_positions(c, grid_extent)

    body = []

    # Connectors first (so svastikas overlay them where they cross).
    pos_set = {(round(px, 3), round(py, 3)) for px, py in positions}
    for cx, cy in positions:
        # Step-A neighbor: top bend → next svastika's bottom bend.
        nx, ny = cx + step_a[0], cy + step_a[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + b, cy - a,
                cx + b + c, cy - a,
                lw=connector_lw, stroke=connector_color,
            ))
        # Step-B neighbor: right bend → next svastika's left bend.
        nx, ny = cx + step_b[0], cy + step_b[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + a, cy + b,
                cx + a, cy + b + c,
                lw=connector_lw, stroke=connector_color,
            ))

    # Svastikas on top.
    for cx, cy in positions:
        body.append(svastika(cx, cy, a, svastika_lw, svastika_color))

    # Bounding box: include svastika reach (±a) plus a small margin.
    pad = 0.15
    xmin = min(cx for cx, _ in positions) - a - pad
    xmax = max(cx for cx, _ in positions) + a + pad
    ymin = min(cy for _, cy in positions) - a - pad
    ymax = max(cy for _, cy in positions) + a + pad
    return "".join(body), (xmin, ymin, xmax - xmin, ymax - ymin)


def render_swastika_distributive_full_edge(c_length: float, bend_ratio: float,
                                           grid_extent: int,
                                           svastika_lw: float = 0.20,
                                           connector_lw: float = 0.08,
                                           svastika_color: str = FILL,
                                           connector_color: str = "#aaaaaa"
                                           ) -> tuple[str, tuple[float, float, float, float]]:
    """Distributive tessellation, parameterized bend_ratio.

    Geometry preserves the (2b + c, -2a) / (2a, 2b + c) step vectors.  Use
    bend_ratio > 0.55 with a smaller c to keep the lattice spacing constant
    while making the svastika's edge longer relative to the connector.
    """
    a = 1.0
    b = a * bend_ratio
    c = c_length
    step_a = (2 * b + c, -2 * a)
    step_b = (2 * a, 2 * b + c)

    positions = []
    for i in range(-grid_extent, grid_extent + 1):
        for j in range(-grid_extent, grid_extent + 1):
            cx = i * step_a[0] + j * step_b[0]
            cy = i * step_a[1] + j * step_b[1]
            positions.append((cx, cy))

    body = []
    pos_set = {(round(px, 3), round(py, 3)) for px, py in positions}
    for cx, cy in positions:
        nx, ny = cx + step_a[0], cy + step_a[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + b, cy - a,
                cx + b + c, cy - a,
                lw=connector_lw, stroke=connector_color,
            ))
        nx, ny = cx + step_b[0], cy + step_b[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + a, cy + b,
                cx + a, cy + b + c,
                lw=connector_lw, stroke=connector_color,
            ))

    for cx, cy in positions:
        body.append(svastika(cx, cy, a, svastika_lw, svastika_color,
                             bend_ratio=bend_ratio))

    pad = 0.15
    xmin = min(cx for cx, _ in positions) - a - pad
    xmax = max(cx for cx, _ in positions) + a + pad
    ymin = min(cy for _, cy in positions) - a - pad
    ymax = max(cy for _, cy in positions) + a + pad
    return "".join(body), (xmin, ymin, xmax - xmin, ymax - ymin)


def render_swastika_distributive_rect_diagonal(dx_length: float, dy_length: float,
                                               grid_extent: int,
                                               svastika_lw: float = 0.20,
                                               connector_lw: float = 0.08,
                                               svastika_color: str = FILL,
                                               connector_color: str = "#aaaaaa"
                                               ) -> tuple[str, tuple[float, float, float, float]]:
    """Distributive tessellation with rectangular-slope diagonal connectors.

    Connector A has horizontal extent dx and vertical extent dy (going up-right
    from the top bend tip).  Connector B mirrors at the right bend tip going
    down-right.

    Step vectors:
      Step A = (1.1 + dx, -2 - dy)
      Step B = (2 + dx, 1.1 + dy)

    For ratio dx:dy = 2:1, the steps are not perpendicular but are linearly
    independent — the lattice still tiles cleanly.
    """
    a = 1.0
    b = 0.55
    step_a = (2 * b + dx_length, -2 * a - dy_length)
    step_b = (2 * a + dx_length, 2 * b + dy_length)

    positions = []
    for i in range(-grid_extent, grid_extent + 1):
        for j in range(-grid_extent, grid_extent + 1):
            cx = i * step_a[0] + j * step_b[0]
            cy = i * step_a[1] + j * step_b[1]
            positions.append((cx, cy))

    body = []
    pos_set = {(round(px, 3), round(py, 3)) for px, py in positions}
    for cx, cy in positions:
        nx, ny = cx + step_a[0], cy + step_a[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + b, cy - a,
                cx + b + dx_length, cy - a - dy_length,
                lw=connector_lw, stroke=connector_color,
            ))
        nx, ny = cx + step_b[0], cy + step_b[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + a, cy + b,
                cx + a + dx_length, cy + b + dy_length,
                lw=connector_lw, stroke=connector_color,
            ))

    for cx, cy in positions:
        body.append(svastika(cx, cy, a, svastika_lw, svastika_color))

    pad = 0.15
    xmin = min(cx for cx, _ in positions) - a - pad
    xmax = max(cx for cx, _ in positions) + a + pad
    ymin = min(cy for _, cy in positions) - a - pad
    ymax = max(cy for _, cy in positions) + a + pad
    return "".join(body), (xmin, ymin, xmax - xmin, ymax - ymin)


def render_swastika_distributive_diagonal(d_length: float, grid_extent: int,
                                          svastika_lw: float = 0.20,
                                          connector_lw: float = 0.08,
                                          svastika_color: str = FILL,
                                          connector_color: str = "#aaaaaa"
                                          ) -> tuple[str, tuple[float, float, float, float]]:
    """Render distributive tessellation with 45-degree connectors.

    Geometry:
      Step A vector = (1.1 + d, -2 - d)   — top-bend → bottom-bend, diagonal up-right
      Step B vector = (2 + d, 1.1 + d)    — right-bend → left-bend, diagonal down-right
    The two step vectors are always perpendicular (dot product = 0), so the
    tessellation is a square grid rotated by some angle that depends on d.
    Larger d ⇒ rotation angle approaches 45°.
    """
    a = 1.0
    b = 0.55
    d = d_length
    step_a = (1.1 + d, -2.0 - d)
    step_b = (2.0 + d, 1.1 + d)

    positions = []
    for i in range(-grid_extent, grid_extent + 1):
        for j in range(-grid_extent, grid_extent + 1):
            cx = i * step_a[0] + j * step_b[0]
            cy = i * step_a[1] + j * step_b[1]
            positions.append((cx, cy))

    body = []
    pos_set = {(round(px, 3), round(py, 3)) for px, py in positions}
    for cx, cy in positions:
        # Step-A: top bend tip → diagonal up-right by (d, -d).
        nx, ny = cx + step_a[0], cy + step_a[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + b, cy - a,
                cx + b + d, cy - a - d,
                lw=connector_lw, stroke=connector_color,
            ))
        # Step-B: right bend tip → diagonal down-right by (d, d).
        nx, ny = cx + step_b[0], cy + step_b[1]
        if (round(nx, 3), round(ny, 3)) in pos_set:
            body.append(connector(
                cx + a, cy + b,
                cx + a + d, cy + b + d,
                lw=connector_lw, stroke=connector_color,
            ))

    for cx, cy in positions:
        body.append(svastika(cx, cy, a, svastika_lw, svastika_color))

    pad = 0.15
    xmin = min(cx for cx, _ in positions) - a - pad
    xmax = max(cx for cx, _ in positions) + a + pad
    ymin = min(cy for _, cy in positions) - a - pad
    ymax = max(cy for _, cy in positions) + a + pad
    return "".join(body), (xmin, ymin, xmax - xmin, ymax - ymin)


# --- Main -------------------------------------------------------------------


def main():
    # Each figure uses a 350×350 px canvas; viewBox is the math frame.
    write(
        "about_series_prakrti_tree",
        render_tree(),
        view=(-1.4, -2.5, 2.8, 2.8),
    )
    write(
        "about_series_prakrti_fern",
        render_fern(),
        view=(-3.0, -10.5, 6.0, 11.0),
    )
    write(
        "about_series_vikrti_pyramid_simple",
        render_pyramid_simple(),
        view=(-1.15, -1.1, 2.3, 1.3),
    )
    write(
        "about_series_vikrti_pyramid_sierpinski",
        render_pyramid_sierpinski(),
        view=(-1.15, -1.1, 2.3, 1.4),
    )
    write(
        "about_series_vikrti_pyramid_nested",
        render_pyramid_nested(),
        view=(-1.15, -1.1, 2.3, 1.4),
    )
    write(
        "about_series_samskrti_swastika_simple",
        render_swastika_simple(),
        view=(-1.3, -1.3, 2.6, 2.6),
    )
    write(
        "about_series_samskrti_swastika_fractal",
        render_swastika_fractal(),
        view=(-1.7, -1.7, 3.4, 3.4),
    )
    write(
        "about_series_samskrti_swastika_tessellated",
        render_swastika_tessellated(),
        view=(-2.8, -2.8, 5.6, 5.6),
    )

    # Distributive tessellation variants — no apex, equal svastikas, thin
    # subordinate connectors, explicit white background.
    for name, c_length, grid_extent in [
        ("about_series_samskrti_swastika_distributive_c05_cluster",
         0.5, 1),
        ("about_series_samskrti_swastika_distributive_c10_cluster",
         1.0, 1),
        ("about_series_samskrti_swastika_distributive_c05_extended",
         0.5, 2),
        ("about_series_samskrti_swastika_distributive_c10_extended",
         1.0, 2),
        # Longer orthogonal connector — proves the tessellation still works.
        ("about_series_samskrti_swastika_distributive_c20_extended",
         2.0, 2),
    ]:
        body, view = render_swastika_distributive(
            c_length=c_length, grid_extent=grid_extent,
        )
        write(name, body, width=500, height=500, view=view,
              white_background=True)

    # 45-degree (diagonal) connector variants — perpendicular step vectors,
    # so the tessellation is a square grid rotated by some angle.  Three d
    # lengths show the geometric progression from short to long connectors.
    for name, d_length, grid_extent in [
        ("about_series_samskrti_swastika_distributive_d05_extended",
         0.5, 2),
        ("about_series_samskrti_swastika_distributive_d10_extended",
         1.0, 2),
        ("about_series_samskrti_swastika_distributive_d15_extended",
         1.5, 2),
    ]:
        body, view = render_swastika_distributive_diagonal(
            d_length=d_length, grid_extent=grid_extent,
        )
        write(name, body, width=500, height=500, view=view,
              white_background=True)

    # c20 redo: same spacing as c20_extended, but bend_ratio=1.0 (svastika
    # edge as long as the arm) and c reduced so 2b + c stays at 3.1.
    body, view = render_swastika_distributive_full_edge(
        c_length=1.1, bend_ratio=1.0, grid_extent=2,
    )
    write("about_series_samskrti_swastika_distributive_c20_fulledge",
          body, width=500, height=500, view=view, white_background=True)

    # Rectangular-slope diagonal connectors (dx:dy = 2:1).  Two magnitudes:
    # small (dx=1, dy=0.5) and larger (dx=2, dy=1).
    for name, dx, dy, grid_extent in [
        ("about_series_samskrti_swastika_distributive_xy21_short",
         1.0, 0.5, 2),
        ("about_series_samskrti_swastika_distributive_xy21_long",
         2.0, 1.0, 2),
    ]:
        body, view = render_swastika_distributive_rect_diagonal(
            dx_length=dx, dy_length=dy, grid_extent=grid_extent,
        )
        write(name, body, width=500, height=500, view=view,
              white_background=True)


if __name__ == "__main__":
    main()
