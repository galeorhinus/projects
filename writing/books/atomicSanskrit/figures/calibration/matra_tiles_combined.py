#!/usr/bin/env python3
"""matra_tiles_combined.py — the Virahāṅka / Hemachandra recurrence cascade.

Three columns, eight y-aligned rows. Reading across a row shows the recurrence
B = (one tile) + A and C = (one tile) + B:

    A (left)    predecessor fillings — 1+2 mātrās (rows 1-3, → the 3-mātrā set)
                                       2+3 mātrās (rows 4-8, → the 4-mātrā set)
    B (middle)  3-mātrā (rows 1-3) and 4-mātrā (rows 4-8) fillings
    C (right)   5-mātrā fillings

Each mātrā sub-group sits inside a light rounded-rectangle backer. From-right
stagger keeps each shared suffix identical, so every column contains the one to
its left as a suffix. Counts cascade: 1+2=3, 2+3=5, 3+5=8.

Title/subtitle styling follows figures/fourth_abrahamic (Gentium Book Plus serif).
Output renders at 4.5 in wide.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BUILD_DIR))
from matra_tiles import (  # noqa: E402
    fillings, render_strip, render_ruler, tile, text, width_of,
    BG, GOLD, TEXT, GUIDE, DEV_FONT, FS_IAST,
    MATRA_UNIT, SLANT, STRIP_HALF, ROW_PITCH, RULER_GAP,
)

MARGIN = 16
COL_GAP = 15
N_ROWS = 8

WIDTH_IN = 4.5           # the figure renders at this width

# Title band (the +~0.5 in added on top).
TOP_BAND = 84
HEAD_TXT = 24            # header text height below the rule
HEAD_GAP = 18            # space between column headers and the boxes below

SERIF = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"
FS_TITLE = 18.1          # ≈ 13 pt at 4.5 in wide
FS_SUB = 11.0            # subtitle, fit on one line at 4.5 in wide
TITLE_FILL = "#2b2b2d"
SUB_FILL = "#5f5346"
RULE = "#cccccc"

BLOCK_FILL = "#f3efe6"   # light backer behind each mātrā sub-group
BACK_PAD_H = 7
BACK_PAD_V = 5
BACK_RX = 9


def swatch(token: str, cx: float, cy: float, sc: float = 0.85) -> str:
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({sc})">{tile(token, 0, 0)}</g>'


def main() -> None:
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

    # Vertical placement.
    rule_y = MARGIN + TOP_BAND
    header_y = rule_y + HEAD_TXT
    row_cy0 = header_y + HEAD_GAP + STRIP_HALF
    ruler_y = row_cy0 + (N_ROWS - 1) * ROW_PITCH + STRIP_HALF + RULER_GAP
    canvas_h = ruler_y + 42

    backers: list[str] = []
    gridlines: list[str] = []
    strips: list[str] = []
    chrome: list[str] = []

    for col, mx in zip(columns, measure_x):
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

        for i in range(col["maxn"] + 1):
            gx = mx + i * MATRA_UNIT
            gridlines.append(
                f'<line x1="{gx:.1f}" y1="{header_y + 6:.1f}" x2="{gx:.1f}" '
                f'y2="{ruler_y:.1f}" stroke="{GUIDE}" stroke-width="1" '
                f'stroke-dasharray="3,4"/>'
            )

        chrome.append(text(mx, header_y, col["head"], FS_IAST, fill=col["color"],
                           anchor="start", weight="700"))
        chrome.append(render_ruler(mx, ruler_y, col["maxn"]))

    # --- Title band ---------------------------------------------------------
    chrome.append(text(MARGIN, MARGIN + 30, "Chandas as Mātrā Tiling", FS_TITLE,
                       fill=TITLE_FILL, anchor="start", weight="700", family=SERIF))
    chrome.append(text(MARGIN, MARGIN + 68,
                       "Valid patterns emerge from measured sound.",
                       FS_SUB, fill=SUB_FILL, anchor="start", style="italic", family=SERIF))
    chrome.append(f'<line x1="{MARGIN}" y1="{rule_y:.1f}" x2="{canvas_w - MARGIN:.1f}" '
                  f'y2="{rule_y:.1f}" stroke="{RULE}" stroke-width="1"/>')

    # Legend (right, just above the rule): hexes right-aligned, text right-
    # justified beside them, two rows (laghu, guru) in Devanagari + IAST.
    sw = 0.85

    def hw(token: str) -> float:                 # half-width of a swatch
        return (width_of(token) / 2 + SLANT) * sw

    x_r = canvas_w - MARGIN                       # common right edge of the hexes
    x_t = x_r - 2 * hw("G") - 10                  # common right edge of the text
    lr1_y, lr2_y = rule_y - 42, rule_y - 16
    chrome.append(swatch("L", x_r - hw("L"), lr1_y, sw))
    chrome.append(text(x_t, lr1_y, "लघु laghu · 1 mātrā", FS_IAST, fill=TEXT,
                       anchor="end", family=DEV_FONT))
    chrome.append(swatch("G", x_r - hw("G"), lr2_y, sw))
    chrome.append(text(x_t, lr2_y, "गुरु guru · 2 mātrās", FS_IAST, fill=TEXT,
                       anchor="end", family=DEV_FONT))

    body = "\n".join(backers + gridlines + strips + chrome)
    height_in = canvas_h / canvas_w * WIDTH_IN
    doc = (
        f'<svg viewBox="0 0 {canvas_w:.0f} {canvas_h:.0f}" width="{WIDTH_IN}in" '
        f'height="{height_in:.3f}in" xmlns="http://www.w3.org/2000/svg" '
        f'preserveAspectRatio="xMidYMid meet">\n'
        '<title>Chandas as Mātrā Tiling</title>\n'
        f'<rect width="100%" height="100%" fill="{BG}"/>\n'
        f'{body}\n</svg>\n'
    )
    out = BUILD_DIR / "matra_tiles_combined.svg"
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({canvas_w:.0f}x{canvas_h:.0f}px = "
          f"{WIDTH_IN}in x {height_in:.2f}in)")


if __name__ == "__main__":
    main()
