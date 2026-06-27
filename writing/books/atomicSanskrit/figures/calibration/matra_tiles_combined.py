#!/usr/bin/env python3
"""matra_tiles_combined.py — the Virahāṅka / Hemachandra recurrence cascade.

Three columns, eight y-aligned rows. Reading across a row shows the recurrence
B = (one tile) + A and C = (one tile) + B:

    A (left)    predecessor fillings — 1+2 mātrās (rows 1-3, → the 3-mātrā set)
                                       2+3 mātrās (rows 4-8, → the 4-mātrā set)
    B (middle)  3-mātrā (rows 1-3) and 4-mātrā (rows 4-8) fillings
    C (right)   5-mātrā fillings

From-right stagger keeps each shared suffix identical, so every column literally
contains the one to its left as a suffix. Counts cascade: 1+2=3, 2+3=5, 3+5=8.

Composition uses matra_tiles primitives (render_strip / render_ruler / tile), so
geometry and fonts stay in sync with the standalone figures.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BUILD_DIR))
from matra_tiles import (  # noqa: E402
    fillings, render_strip, render_ruler, tile, text,
    BG, GOLD, TEXT, GUIDE, FS_IAST,
    MATRA_UNIT, SLANT, STRIP_HALF, ROW_PITCH, ROW_GAP, RULER_GAP,
)

MARGIN = 16
COL_GAP = 24          # gap between columns (kept small — columns sit close)
LEGEND_H = 40         # top band for the swatch legend
HEAD_H = 26           # column-header band
REF_H_IN = 6.0
N_ROWS = 8


def swatch(token: str, cx: float, cy: float, sc: float = 0.6) -> str:
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({sc})">{tile(token, 0, 0)}</g>'


def main() -> None:
    col_c = fillings(5)                       # 5-mātrā
    col_b = fillings(3) + fillings(4)         # 3-mātrā then 4-mātrā
    col_a = [row[1:] for row in col_b]        # predecessors = B minus its first tile

    columns = [
        {"rows": col_a, "maxn": 3, "head": "1 · 2 · 3 mātrās", "color": TEXT},
        {"rows": col_b, "maxn": 4, "head": "3 · 4 mātrās", "color": TEXT},
        {"rows": col_c, "maxn": 5, "head": "5 mātrās", "color": GOLD},
    ]

    # Horizontal placement: each column left-aligned to its own measure-0.
    measure_x, x = [], MARGIN + SLANT / 2
    for col in columns:
        measure_x.append(x)
        x += col["maxn"] * MATRA_UNIT + SLANT / 2 + COL_GAP
    canvas_w = measure_x[-1] + columns[-1]["maxn"] * MATRA_UNIT + SLANT / 2 + MARGIN

    # Vertical placement: legend band, header band, eight rows, rulers.
    top = MARGIN + LEGEND_H + HEAD_H
    row_cy0 = top + STRIP_HALF
    ruler_y = row_cy0 + (N_ROWS - 1) * ROW_PITCH + STRIP_HALF + RULER_GAP
    canvas_h = ruler_y + 52

    frags: list[str] = []

    # Gridlines first (behind everything).
    for col, mx in zip(columns, measure_x):
        for i in range(col["maxn"] + 1):
            gx = mx + i * MATRA_UNIT
            frags.append(
                f'<line x1="{gx:.1f}" y1="{top - 4:.1f}" x2="{gx:.1f}" '
                f'y2="{ruler_y:.1f}" stroke="{GUIDE}" stroke-width="1" '
                f'stroke-dasharray="3,4"/>'
            )

    # Divider between the 3-set rows (0-2) and the 4-set rows (3-7).
    div_y = row_cy0 + 2 * ROW_PITCH + STRIP_HALF + ROW_GAP / 2
    frags.append(
        f'<line x1="{MARGIN:.1f}" y1="{div_y:.1f}" x2="{canvas_w - MARGIN:.1f}" '
        f'y2="{div_y:.1f}" stroke="{GUIDE}" stroke-width="1"/>'
    )

    # Swatch legend (top-left band).
    ly = MARGIN + LEGEND_H / 2
    frags.append(swatch("L", MARGIN + 16, ly))
    frags.append(text(MARGIN + 42, ly, "laghu · 1 mātrā", FS_IAST, fill=TEXT, anchor="start"))
    frags.append(swatch("G", MARGIN + 200, ly))
    frags.append(text(MARGIN + 240, ly, "guru · 2 mātrās", FS_IAST, fill=TEXT, anchor="start"))

    # Columns: header, rows, ruler.
    for col, mx in zip(columns, measure_x):
        frags.append(text(mx, MARGIN + LEGEND_H + HEAD_H - 9, col["head"],
                          FS_IAST, fill=col["color"], anchor="start", weight="700"))
        for idx, tokens in enumerate(col["rows"]):
            frags.append(render_strip(tokens, mx, row_cy0 + idx * ROW_PITCH))
        frags.append(render_ruler(mx, ruler_y, col["maxn"]))

    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w:.0f}" '
        f'height="{canvas_h:.0f}" viewBox="0 0 {canvas_w:.0f} {canvas_h:.0f}">\n'
        '<title>Mātrā recurrence cascade — 3, 4, 5 mātrās</title>\n'
        f'<rect width="100%" height="100%" fill="{BG}"/>\n'
        + "\n".join(frags) + "\n</svg>\n"
    )
    out = BUILD_DIR / "matra_tiles_combined.svg"
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({canvas_w:.0f}x{canvas_h:.0f}px; "
          f"at {REF_H_IN:.0f}in tall = {canvas_w * REF_H_IN / canvas_h:.2f}in wide)")


if __name__ == "__main__":
    main()
