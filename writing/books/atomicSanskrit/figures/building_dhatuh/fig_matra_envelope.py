#!/usr/bin/env python3
"""
fig_matra_envelope.py — Composite SVG of ten dhātu hexagons across the
mātrā envelope (1.0 → 5.5 in half-mātrā steps).

Reuses working/dhatu_hexagons/dhatu_hexagon.py for the per-dhātu geometry
and composes ten dhātu strips into a single 5-row × 2-column grid.

Each cell shows: mātrā label · dhātu title (Devanagari + IAST) · hexagon strip.

Output: figures/build/building_dhatuh_matra_envelope.svg
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

# Make working/dhatu_hexagons/ importable.
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))

from dhatu_hexagon import (  # noqa: E402
    EDGE_LENGTH,
    HEX_HEIGHT,
    WIDTH_BY_CLASS,
    compute_layout,
    parse_dhatu_string,
    render_hexagon,
)


# (mātrā label, devanagari title, IAST title, dhātu particle-string)
DHATUS = [
    ("1",   "ऋ",        "ṛ",     "R"),
    ("1½",  "कृ",       "kṛ",    "k,R"),
    ("2",   "गम्",      "gam",   "g,a,m"),
    ("2½",  "धा",       "dhā",   "dh,A"),
    ("3",   "वाच्",     "vāc",   "v,A,c"),
    ("3½",  "स्वाद्",   "svād",  "s,v,A,d"),
    ("4",   "बाधृ",     "bādhṛ", "b,A,dh,R"),
    ("4½",  "कुमार्",   "kumār", "k,u,m,A,r"),
    ("5",   "दीपी",     "dīpī",  "d,I,p,I"),
    ("5½",  "ह्लादी",   "hlādī", "h,l,A,d,I"),
]


# --- Layout parameters ---

CELL_W = 420          # column width (px)
CELL_H = 150          # row height (px)
LEFT_MARGIN = 24      # x-offset for strip's left edge inside the cell
TITLE_Y_OFFSET = 32   # y-offset for combined label + title line
HEX_Y_OFFSET = 100    # y-offset for hexagon-strip midline from cell's top edge
BOTTOM_PADDING = 40   # extra whitespace below the last row

# Asymmetric shifts (1 mātrā = EDGE_LENGTH px):
LEFT_COL_HEX_SHIFT   = EDGE_LENGTH   # shift left-column hexagons right by 1 mātrā
RIGHT_COL_TEXT_SHIFT = EDGE_LENGTH   # shift right-column labels left by 1 mātrā


def strip_width(particles):
    """Compute the total horizontal extent of a hexagon strip in geometry units."""
    positions = compute_layout(particles)
    xs = []
    for (cx, _cy), v in zip(positions, particles):
        w = WIDTH_BY_CLASS[v["class"]]
        xs.extend([cx - w / 2 - EDGE_LENGTH / 2, cx + w / 2 + EDGE_LENGTH / 2])
    return min(xs), max(xs)


def render_cell(col, row, matra, deva, iast, dhatu_str):
    """Render one grid cell with combined label + title on one line and a
    left-aligned hexagon strip below."""
    particles = parse_dhatu_string(dhatu_str)
    positions = compute_layout(particles)

    xmin_local, _xmax_local = strip_width(particles)

    cell_x = col * CELL_W
    cell_y = row * CELL_H

    # Asymmetric column shifts: left column nudges strips right, right column
    # nudges labels left — each by one mātrā.
    strip_offset = LEFT_MARGIN + (LEFT_COL_HEX_SHIFT if col == 0 else 0)
    text_offset  = LEFT_MARGIN - (RIGHT_COL_TEXT_SHIFT if col == 1 else 0)

    # Left-align the strip: its leftmost geometry point lands at cell_x + strip_offset.
    tx = (cell_x + strip_offset) - xmin_local
    ty = cell_y + HEX_Y_OFFSET

    parts = []

    # Combined mātrā label + dhātu title on one line.
    parts.append(
        f'<text x="{cell_x + text_offset}" y="{cell_y + TITLE_Y_OFFSET}" '
        f'font-family="Charter, Georgia, Times, serif" '
        f'font-size="18" font-weight="500" text-anchor="start" fill="#1a1a1a">'
        f'<tspan font-style="italic">{matra} mātrā</tspan>'
        f'  ·  '
        f'<tspan font-family="Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Charter, Georgia, Times, serif">{deva}</tspan>'
        f' — '
        f'<tspan font-style="italic">{iast}</tspan>'
        f'</text>'
    )

    # Hexagon strip (left-aligned to cell_x + LEFT_MARGIN).
    for (cx, cy), v in zip(positions, particles):
        parts.append(
            f'<g transform="translate({tx:.1f},{ty:.1f})">'
            f'{render_hexagon(cx, cy, v, style="simple")}'
            f'</g>'
        )

    return "\n  ".join(parts)


def main():
    # Column-major layout: first 5 dhātus (mātrās 1–3) in the left column,
    # next 5 (mātrās 3½–5½) in the right column.
    n_cols = 2
    n_rows = (len(DHATUS) + n_cols - 1) // n_cols

    total_w = n_cols * CELL_W
    total_h = n_rows * CELL_H + BOTTOM_PADDING

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {total_w} {total_h}" '
        f'width="{total_w}" height="{total_h}">'
    )
    svg_parts.append(f'  <title>Mātrā envelope across ten dhātavaḥ</title>')
    svg_parts.append(
        f'  <rect x="0" y="0" width="{total_w}" height="{total_h}" fill="white"/>'
    )

    for i, (matra, deva, iast, dhatu_str) in enumerate(DHATUS):
        col = i // n_rows
        row = i % n_rows
        svg_parts.append("  " + render_cell(col, row, matra, deva, iast, dhatu_str))

    svg_parts.append("</svg>")

    out_path = REPO_ROOT / "figures" / "build" / "building_dhatuh_matra_envelope.svg"
    out_path.write_text("\n".join(svg_parts), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
