#!/usr/bin/env python3
"""matra_tiles.py — Chandas mātrā-tile figures for Chapter 14 §14.4.

Visualizes the laghu / guru filling of a fixed metrical measure with the
book's staggered hex-tile grammar (Ch 10/11/12).

    L (laghu) = 1-mātrā tile      G (guru) = 2-mātrā tile

Geometry (the calculation the earlier scripts use — see
figures/building_vakya/vakya_figures.py and working/dhatu_hexagons):

  * A tile's flat-top width is  mātrā · MATRA_UNIT − SLANT, so its mātrā
    *footprint* (flat top + one slanted edge) is exactly mātrā · MATRA_UNIT.
    With WIDTH constants matching vakya: laghu = 40 px, guru = 100 px.
  * Tiles are staggered on two rails (±HEX_HEIGHT/4); every gap is one slant
    (EDGE_LENGTH/2), so the slanted edges interlock diagonally.
  * The mātrā measure starts at the x-midpoint of a tile's left-most vertex
    and its two next vertices, i.e. leftmost_vertex + EDGE_LENGTH/4.

Because the per-tile footprints sum to mātrā · MATRA_UNIT and every gap is one
slant, *every* filling of n mātrās spans an identical width — so all patterns
align to one shared measure and a single ruler reads true for the whole stack.

Usage:
    python3 figures/calibration/matra_tiles.py          # n = 4 and 5 (§14.4)
    python3 figures/calibration/matra_tiles.py 4 5 6    # any measures

Output: figures/calibration/matra_tiles_<n>.svg
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))
from dhatu_hexagon import EDGE_LENGTH as _EDGE_BASE, HEX_HEIGHT as _HH_BASE  # noqa: E402

# --- Geometry (matches the staggered Ch 10/11/12 hex grammar) --------------

TILE_SCALE = 0.72                # shrink the tiles for a less crowded page
EDGE_LENGTH = _EDGE_BASE * TILE_SCALE
HEX_HEIGHT = _HH_BASE * TILE_SCALE
SLANT = EDGE_LENGTH / 2          # horizontal projection of one slanted edge
MATRA_UNIT = 72 * TILE_SCALE     # px per mātrā along the measure
UPPER_RAIL = -HEX_HEIGHT / 4     # the two staggered rails, HEX_HEIGHT/2 apart
LOWER_RAIL = HEX_HEIGHT / 4

# --- Palette / type --------------------------------------------------------

# Warm palette drawn from the reference design.
BG = "#ffffff"                  # white background
LAGHU_FILL = "#d8c7a3"          # tan — the lighter weight (1 mātrā)
GURU_FILL = "#4a3a28"           # dark brown — the heavier weight (2 mātrās)
STROKE = "#5c4830"              # tile outline
GURU_TEXT = "#f4eedd"           # mark colour on the dark guru tile
LAGHU_TEXT = "#3d2f1f"          # mark colour on the tan laghu tile
GOLD = "#a8842c"                # accent (the 5-mātrā result column)
TEXT = "#3d2f1f"                # default dark-brown ink (titles)
MUTED = "#6b563a"               # secondary brown (subtitle, ruler labels)
RULER = "#7a6647"               # ruler line + ticks
GUIDE = "#cdbf9e"               # dashed major-tick gridlines

LATIN_FONT = "Charter, Georgia, Times, serif"
DEV_FONT = "Noto Sans Devanagari, Mangal, Devanagari Sangam MN, sans-serif"

# --- Font sizes (px) -------------------------------------------------------
# Tuned so the COMBINED cascade (matra_tiles_combined.py, 869 px tall) prints its
# text at these point sizes at 6 in tall: title 11 / legend 10 / IAST 8 / ruler
# numbers 9.5 / mātrā label 9.5.  (px = pt × 869 / 432.)

FS_TITLE = 22.1
FS_LEGEND = 20.1
FS_DEV = 22.1
FS_IAST = 16.1
FS_RULER_NUM = 19.1
FS_MATRA_LABEL = 19.1

# --- Layout ----------------------------------------------------------------

MARGIN = 28
TITLE_H = 102                          # top chrome with the legend line
TITLE_H_NO_LEGEND = 66                 # top chrome with the title only
LEGEND_TEXT = "| = laghu (1 mātrā)    ·    || = guru (2)"
X0 = MARGIN + 22                       # x where mātrā 0 sits (the measure start)
ROW_GAP = 16
RIGHT_PAD = 28
RULER_GAP = 24

STRIP_HALF = 3 * HEX_HEIGHT / 4        # half-height of a staggered strip
ROW_PITCH = 2 * STRIP_HALF + ROW_GAP


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x: float, y: float, content: str, size: float, *, fill: str = TEXT,
         anchor: str = "middle", weight: str = "400", style: str = "normal",
         family: str = LATIN_FONT, halo: float = 0.0) -> str:
    halo_attr = (
        f'paint-order="stroke" stroke="#ffffff" stroke-width="{halo}" '
        f'stroke-linejoin="round" ' if halo else ""
    )
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" '
        f'dominant-baseline="middle" {halo_attr}fill="{fill}">{esc(content)}</text>'
    )


def hex_points(cx: float, cy: float, w: float) -> str:
    """Flat-top hexagon, flat-width w, slant projection SLANT each side."""
    h = HEX_HEIGHT
    pts = [
        (cx - w / 2, cy - h / 2),
        (cx + w / 2, cy - h / 2),
        (cx + w / 2 + SLANT, cy),
        (cx + w / 2, cy + h / 2),
        (cx - w / 2, cy + h / 2),
        (cx - w / 2 - SLANT, cy),
    ]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


# --- Combinatorics ---------------------------------------------------------

def matra_of(token: str) -> int:
    return 2 if token == "G" else 1


def width_of(token: str) -> float:
    return matra_of(token) * MATRA_UNIT - SLANT   # L → 40, G → 100


def fillings(n: int) -> list[list[str]]:
    """Every laghu/guru filling of an n-mātrā measure, in *recurrence* order.

    A filling is either guru + a filling of (n−2) or laghu + a filling of (n−1):
    the guru-first block comes first, then the laghu-first block. So the rows of
    consecutive measures correspond — the guru-first rows of n match the rows of
    (n−2), the laghu-first rows match (n−1) — the visual form of the Virahāṅka /
    Hemachandra recurrence, count(n) = count(n−1) + count(n−2).
    """
    if n == 0:
        return [[]]
    if n == 1:
        return [["L"]]
    guru_first = [["G"] + p for p in fillings(n - 2)]
    laghu_first = [["L"] + p for p in fillings(n - 1)]
    return guru_first + laghu_first


# --- Rendering -------------------------------------------------------------

def layout(tokens: list[str]) -> list[dict]:
    """Staggered positions (raw, first tile centred at x=0).

    Tiles alternate rails by position, so every gap is one slant; cx advances
    by (prev_w + w)/2 + SLANT — the compute_unit_layout rule.
    """
    out: list[dict] = []
    n_tiles = len(tokens)
    for i, t in enumerate(tokens):
        w = width_of(t)
        # Rails assigned from the RIGHT, so a shared suffix keeps its stagger:
        # the matching sub-pattern (e.g. the "GL" inside "GGL") sits identically
        # to its standalone row. Last tile on the lower rail.
        cy = LOWER_RAIL if (n_tiles - 1 - i) % 2 == 0 else UPPER_RAIL
        if i == 0:
            cx = 0.0
        else:
            prev = out[-1]
            cx = prev["cx"] + (prev["w"] + w) / 2 + SLANT
        out.append({"t": t, "cx": cx, "cy": cy, "w": w})
    return out


# --- Scansion marks: laghu = | (one pipe), guru = || (two pipes) -----------

PIPE_HALF = HEX_HEIGHT * 0.21    # half-height of a pipe mark
PIPE_GAP = EDGE_LENGTH * 0.16    # half-gap between the two guru pipes
PIPE_WIDTH = 2.6


def tile_hex(token: str, cx: float, cy: float) -> str:
    fill = GURU_FILL if token == "G" else LAGHU_FILL
    return (
        f'<polygon points="{hex_points(cx, cy, width_of(token))}" fill="{fill}" '
        f'stroke="{STROKE}" stroke-width="1.5" stroke-linejoin="round"/>'
    )


def tile_marks(token: str, cx: float, cy: float) -> str:
    guru = token == "G"
    ink = GURU_TEXT if guru else LAGHU_TEXT
    offsets = (-PIPE_GAP, PIPE_GAP) if guru else (0.0,)
    return "\n  ".join(
        f'<line x1="{cx + off:.1f}" y1="{cy - PIPE_HALF:.1f}" '
        f'x2="{cx + off:.1f}" y2="{cy + PIPE_HALF:.1f}" stroke="{ink}" '
        f'stroke-width="{PIPE_WIDTH}" stroke-linecap="round"/>'
        for off in offsets
    )


def tile(token: str, cx: float, cy: float) -> str:
    """A complete hex tile with its scansion mark — for isolated / legend use."""
    return tile_hex(token, cx, cy) + "\n  " + tile_marks(token, cx, cy)


def render_strip(tokens: list[str], measure_start_x: float, row_cy: float) -> str:
    """One filling as a staggered hex strip, aligned so mātrā 0 = measure_start_x.

    Two passes (all hexes, then all marks) so an interlocking neighbour never
    clips a tile's pipe.
    """
    lay = layout(tokens)
    first = lay[0]
    dx = measure_start_x - (first["cx"] - first["w"] / 2 - SLANT / 2)
    hexes = [tile_hex(u["t"], u["cx"] + dx, u["cy"] + row_cy) for u in lay]
    marks = [tile_marks(u["t"], u["cx"] + dx, u["cy"] + row_cy) for u in lay]
    return "\n  ".join(hexes + marks)


def render_ruler(x_start: float, y: float, n: int) -> str:
    """Half-mātrā ruler spanning the shared measure [x_start, x_start + n·MATRA_UNIT]."""
    end_x = x_start + n * MATRA_UNIT
    frags = [
        f'<line x1="{x_start:.1f}" y1="{y:.1f}" x2="{end_x:.1f}" y2="{y:.1f}" '
        f'stroke="{RULER}" stroke-width="2.6"/>'
    ]
    for i in range(n * 2 + 1):
        x = x_start + i * MATRA_UNIT / 2
        major = i % 2 == 0
        tick = 12 if major else 6
        frags.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - tick:.1f}" '
            f'stroke="{RULER}" stroke-width="{2.4 if major else 1.5}"/>'
        )
        if major:
            frags.append(text(x, y + 26, f"{i // 2}", FS_RULER_NUM, fill=MUTED))
    frags.append(text((x_start + end_x) / 2, y + 56, "mātrā", FS_MATRA_LABEL, fill=MUTED, style="italic"))
    return "\n  ".join(frags)


def build(n: int, show_ruler: bool = True, show_legend: bool = True,
          title_color: str = TEXT) -> tuple[str, float, float]:
    rows = fillings(n)
    count = len(rows)

    measure_end = X0 + n * MATRA_UNIT
    tiles_right = measure_end + SLANT / 2           # rightmost vertex of any strip

    frags: list[str] = []

    title_text = f"{n} mātrās · {count}"
    frags.append(text(MARGIN, 42, title_text, FS_TITLE, fill=title_color,
                      anchor="start", weight="700"))
    if show_legend:
        frags.append(text(MARGIN, 78, LEGEND_TEXT,
                          FS_LEGEND, fill=MUTED, anchor="start"))

    top = TITLE_H if show_legend else TITLE_H_NO_LEGEND
    row_cy0 = top + STRIP_HALF
    stack_bottom = row_cy0 + (count - 1) * ROW_PITCH + STRIP_HALF
    guide_bottom = stack_bottom + (RULER_GAP if show_ruler else 10)

    # Dashed gridlines at every major (integer) mātrā tick, behind the tiles.
    for i in range(n + 1):
        gx = X0 + i * MATRA_UNIT
        frags.append(
            f'<line x1="{gx:.1f}" y1="{top - 4:.1f}" x2="{gx:.1f}" '
            f'y2="{guide_bottom:.1f}" stroke="{GUIDE}" stroke-width="1" '
            f'stroke-dasharray="3,4"/>'
        )

    for idx, tokens in enumerate(rows):
        cy = row_cy0 + idx * ROW_PITCH
        frags.append(render_strip(tokens, X0, cy))

    if show_ruler:
        ruler_y = stack_bottom + RULER_GAP
        frags.append(render_ruler(X0, ruler_y, n))
        height = ruler_y + 78
    else:
        height = stack_bottom + 26

    title_w = len(title_text) * FS_TITLE * 0.56     # rough advance-width estimate
    width = max(tiles_right + RIGHT_PAD, MARGIN + title_w + MARGIN)
    return "\n  ".join(frags), width, height


def write_svg(n: int) -> None:
    body, width, height = build(n)
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">\n'
        f'<title>Chandas mātrā tiles — {n} mātrās</title>\n'
        f'<rect width="100%" height="100%" fill="{BG}"/>\n'
        f'{body}\n</svg>\n'
    )
    out = BUILD_DIR / f"matra_tiles_{n}.svg"
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({len(fillings(n))} patterns)")


def main() -> None:
    args = sys.argv[1:]
    measures = [int(a) for a in args] if args else [3, 4, 5]
    for n in measures:
        write_svg(n)


if __name__ == "__main__":
    main()
