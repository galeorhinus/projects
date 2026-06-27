#!/usr/bin/env python3
"""matra_tiles_combined.py — the Virahāṅka / Hemachandra recurrence cascade.

Three columns, eight y-aligned rows. Reading across a row shows the recurrence
B = (one tile) + A and C = (one tile) + B:

    A (left)    predecessor fillings — 1+2 mātrās (rows 1-3, → the 3-mātrā set)
                                       2+3 mātrās (rows 4-8, → the 4-mātrā set)
    B (middle)  3-mātrā (rows 1-3) and 4-mātrā (rows 4-8) fillings
    C (right)   5-mātrā fillings

Each mātrā sub-group (1, 2, 3, … ) sits inside a light rounded-rectangle backer.
From-right stagger keeps each shared suffix identical, so every column literally
contains the one to its left as a suffix. Counts cascade: 1+2=3, 2+3=5, 3+5=8.
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
    MATRA_UNIT, SLANT, STRIP_HALF, ROW_PITCH, RULER_GAP,
)

MARGIN = 16
COL_GAP = 24
LEGEND_H = 40
HEAD_H = 26
REF_H_IN = 6.0
N_ROWS = 8

BLOCK_FILL = "#f3efe6"   # light backer behind each mātrā sub-group
BACK_PAD_H = 7
BACK_PAD_V = 5
BACK_RX = 9


def swatch(token: str, cx: float, cy: float, sc: float = 0.7) -> str:
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({sc})">{tile(token, 0, 0)}</g>'


def main() -> None:
    # Each column is a list of (mātrā, fillings) sub-blocks.
    columns = [
        {"blocks": [(1, fillings(1)), (2, fillings(2)), (2, fillings(2)), (3, fillings(3))],
         "maxn": 3, "head": "1 · 2 · 3 mātrās", "color": TEXT},
        {"blocks": [(3, fillings(3)), (4, fillings(4))],
         "maxn": 4, "head": "3 · 4 mātrās", "color": TEXT},
        {"blocks": [(5, fillings(5))],
         "maxn": 5, "head": "5 mātrās", "color": GOLD},
    ]

    # Horizontal placement: each column left-aligned to its own measure-0.
    measure_x, x = [], MARGIN + SLANT / 2 + BACK_PAD_H
    for col in columns:
        measure_x.append(x)
        x += col["maxn"] * MATRA_UNIT + SLANT / 2 + BACK_PAD_H + COL_GAP
    canvas_w = measure_x[-1] + columns[-1]["maxn"] * MATRA_UNIT + SLANT / 2 + BACK_PAD_H + MARGIN

    # Vertical placement: legend band, header band, eight rows, rulers.
    top = MARGIN + LEGEND_H + HEAD_H
    row_cy0 = top + STRIP_HALF
    ruler_y = row_cy0 + (N_ROWS - 1) * ROW_PITCH + STRIP_HALF + RULER_GAP
    canvas_h = ruler_y + 52

    backers: list[str] = []
    gridlines: list[str] = []
    strips: list[str] = []
    chrome: list[str] = []

    for col, mx in zip(columns, measure_x):
        # Sub-group backers + the strips inside them.
        r = 0
        for n, rows in col["blocks"]:
            ry0 = row_cy0 + r * ROW_PITCH - STRIP_HALF - BACK_PAD_V
            ry1 = row_cy0 + (r + len(rows) - 1) * ROW_PITCH + STRIP_HALF + BACK_PAD_V
            rx0 = mx - SLANT / 2 - BACK_PAD_H
            rw = n * MATRA_UNIT + SLANT + 2 * BACK_PAD_H
            backers.append(
                f'<rect x="{rx0:.1f}" y="{ry0:.1f}" width="{rw:.1f}" '
                f'height="{ry1 - ry0:.1f}" rx="{BACK_RX}" fill="{BLOCK_FILL}"/>'
            )
            for tokens in rows:
                strips.append(render_strip(tokens, mx, row_cy0 + r * ROW_PITCH))
                r += 1

        # Gridlines at every major mātrā tick.
        for i in range(col["maxn"] + 1):
            gx = mx + i * MATRA_UNIT
            gridlines.append(
                f'<line x1="{gx:.1f}" y1="{top - 4:.1f}" x2="{gx:.1f}" '
                f'y2="{ruler_y:.1f}" stroke="{GUIDE}" stroke-width="1" '
                f'stroke-dasharray="3,4"/>'
            )

        # Header + ruler.
        chrome.append(text(mx, MARGIN + LEGEND_H + HEAD_H - 9, col["head"],
                           FS_IAST, fill=col["color"], anchor="start", weight="700"))
        chrome.append(render_ruler(mx, ruler_y, col["maxn"]))

    # Swatch legend (top-left band).
    ly = MARGIN + LEGEND_H / 2
    chrome.append(swatch("L", MARGIN + 14, ly))
    chrome.append(text(MARGIN + 36, ly, "laghu · 1 mātrā", FS_IAST, fill=TEXT, anchor="start"))
    chrome.append(swatch("G", MARGIN + 190, ly))
    chrome.append(text(MARGIN + 226, ly, "guru · 2 mātrās", FS_IAST, fill=TEXT, anchor="start"))

    body = "\n".join(backers + gridlines + strips + chrome)
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w:.0f}" '
        f'height="{canvas_h:.0f}" viewBox="0 0 {canvas_w:.0f} {canvas_h:.0f}">\n'
        '<title>Mātrā recurrence cascade — 3, 4, 5 mātrās</title>\n'
        f'<rect width="100%" height="100%" fill="{BG}"/>\n'
        f'{body}\n</svg>\n'
    )
    out = BUILD_DIR / "matra_tiles_combined.svg"
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({canvas_w:.0f}x{canvas_h:.0f}px; "
          f"at {REF_H_IN:.0f}in tall = {canvas_w * REF_H_IN / canvas_h:.2f}in wide)")


if __name__ == "__main__":
    main()
