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
from dhatu_hexagon import EDGE_LENGTH, HEX_HEIGHT  # noqa: E402

# --- Geometry (matches the staggered Ch 10/11/12 hex grammar) --------------

SLANT = EDGE_LENGTH / 2          # horizontal projection of one slanted edge (= 20)
MATRA_UNIT = 60                  # px per mātrā along the measure (vakya value)
UPPER_RAIL = -HEX_HEIGHT / 4     # the two staggered rails, HEX_HEIGHT/2 apart
LOWER_RAIL = HEX_HEIGHT / 4

# --- Palette / type --------------------------------------------------------

LAGHU_FILL = "#dcdcdc"          # lighter weight
GURU_FILL = "#aaaaaa"           # heavier weight
STROKE = "#333333"
TEXT = "#1a1a1a"
MUTED = "#555555"
RULER = "#888888"
GUIDE = "#c8c8c8"

LATIN_FONT = "Charter, Georgia, Times, serif"
DEV_FONT = "Noto Sans Devanagari, Mangal, Devanagari Sangam MN, sans-serif"

# --- Layout ----------------------------------------------------------------

MARGIN = 28
TITLE_H = 66
X0 = MARGIN + 22                       # x where mātrā 0 sits (the measure start)
ROW_GAP = 26
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
    """Every laghu/guru filling of an n-mātrā measure, ordered as in §14.4."""
    out: list[list[str]] = []

    def rec(rem: int, acc: list[str]) -> None:
        if rem == 0:
            out.append(acc[:])
            return
        if rem >= 1:
            acc.append("L"); rec(rem - 1, acc); acc.pop()
        if rem >= 2:
            acc.append("G"); rec(rem - 2, acc); acc.pop()

    rec(n, [])
    out.sort(key=lambda p: (-p.count("G"), "".join(p)))  # 'G' < 'L'
    return out


# --- Rendering -------------------------------------------------------------

def layout(tokens: list[str]) -> list[dict]:
    """Staggered positions (raw, first tile centred at x=0).

    Tiles alternate rails by position, so every gap is one slant; cx advances
    by (prev_w + w)/2 + SLANT — the compute_unit_layout rule.
    """
    out: list[dict] = []
    for i, t in enumerate(tokens):
        w = width_of(t)
        cy = UPPER_RAIL if i % 2 == 0 else LOWER_RAIL
        if i == 0:
            cx = 0.0
        else:
            prev = out[-1]
            cx = prev["cx"] + (prev["w"] + w) / 2 + SLANT
        out.append({"t": t, "cx": cx, "cy": cy, "w": w})
    return out


def render_strip(tokens: list[str], measure_start_x: float, row_cy: float) -> str:
    """One filling as a staggered L/G hex strip, aligned so mātrā 0 = measure_start_x."""
    lay = layout(tokens)
    first = lay[0]
    # Align the first tile's left-vertex midpoint (leftmost vertex + SLANT/2) to the measure start.
    dx = measure_start_x - (first["cx"] - first["w"] / 2 - SLANT / 2)
    polys: list[str] = []
    labels: list[str] = []
    for u in lay:
        cx = u["cx"] + dx
        cy = u["cy"] + row_cy
        w = u["w"]
        fill = GURU_FILL if u["t"] == "G" else LAGHU_FILL
        polys.append(
            f'<polygon points="{hex_points(cx, cy, w)}" fill="{fill}" '
            f'stroke="{STROKE}" stroke-width="1.5" stroke-linejoin="round"/>'
        )
        dev = "गुरु" if u["t"] == "G" else "लघु"
        iast = "guru" if u["t"] == "G" else "laghu"
        labels.append(text(cx, cy - 6, dev, 19, weight="600", family=DEV_FONT, halo=4.0))
        labels.append(text(cx, cy + 16, iast, 12, fill=MUTED, style="italic", halo=3.0))
    return "\n  ".join(polys + labels)


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
            frags.append(text(x, y + 20, f"{i // 2}", 15, fill=MUTED))
    frags.append(text((x_start + end_x) / 2, y + 42, "mātrā", 15, fill=MUTED, style="italic"))
    return "\n  ".join(frags)


def build(n: int) -> tuple[str, float, float]:
    rows = fillings(n)
    count = len(rows)

    measure_end = X0 + n * MATRA_UNIT
    tiles_right = measure_end + SLANT / 2           # rightmost vertex of any strip

    frags: list[str] = []

    measure_word = {4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}.get(n, str(n))
    frags.append(text(MARGIN, 28, f"{measure_word} mātrās — {count} patterns",
                      20, anchor="start", weight="700"))
    frags.append(text(MARGIN, 50, "लघु = 1 mātrā    ·    गुरु = 2 mātrās",
                      14, fill=MUTED, anchor="start", family=DEV_FONT))

    row_cy0 = TITLE_H + STRIP_HALF
    stack_bottom = row_cy0 + (count - 1) * ROW_PITCH + STRIP_HALF
    ruler_y = stack_bottom + RULER_GAP

    # Shared measure-boundary guides (correct: every strip spans the same width).
    for gx in (X0, measure_end):
        frags.append(
            f'<line x1="{gx:.1f}" y1="{TITLE_H - 4:.1f}" x2="{gx:.1f}" '
            f'y2="{ruler_y:.1f}" stroke="{GUIDE}" stroke-width="1" '
            f'stroke-dasharray="3,4"/>'
        )

    for idx, tokens in enumerate(rows):
        cy = row_cy0 + idx * ROW_PITCH
        frags.append(render_strip(tokens, X0, cy))

    frags.append(render_ruler(X0, ruler_y, n))

    width = tiles_right + RIGHT_PAD
    height = ruler_y + 56
    return "\n  ".join(frags), width, height


def write_svg(n: int) -> None:
    body, width, height = build(n)
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">\n'
        f'<title>Chandas mātrā tiles — {n} mātrās</title>\n'
        '<rect width="100%" height="100%" fill="white"/>\n'
        f'{body}\n</svg>\n'
    )
    out = BUILD_DIR / f"matra_tiles_{n}.svg"
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({len(fillings(n))} patterns)")


def main() -> None:
    args = sys.argv[1:]
    measures = [int(a) for a in args] if args else [4, 5]
    for n in measures:
        write_svg(n)


if __name__ == "__main__":
    main()
