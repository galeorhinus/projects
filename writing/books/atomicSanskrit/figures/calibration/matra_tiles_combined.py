#!/usr/bin/env python3
"""matra_tiles_combined.py — two-column composite of the 3/4/5-mātrā figures.

    Column 1 :  3-mātrā  (top)
                4-mātrā  (bottom)
    Column 2 :  5-mātrā

The 4-mātrā and 5-mātrā panels are bottom-aligned so their mātrā rulers sit on
the same y. Column 1 (3 + gap + 4) is taller than the 5-mātrā panel, so the
5-mātrā carries whitespace above it.

Composition only: each panel is matra_tiles.build(n) verbatim, wrapped in a
<g transform="translate(...)"> on a shared canvas — so every panel is identical
to its standalone figure and stays in sync with matra_tiles.py automatically.

Usage:  python3 figures/calibration/matra_tiles_combined.py
Output: figures/calibration/matra_tiles_combined.svg
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BUILD_DIR))
from matra_tiles import (  # noqa: E402
    build, text, FS_LEGEND, DEV_FONT, MUTED, LEGEND_TEXT,
)

MARGIN = 12          # outer canvas margin
COL_GAP = 8          # horizontal gap between the two columns
STACK_GAP = 12       # vertical gap between the 3- and 4-mātrā panels
REF_H_IN = 6.0       # font-tuned print height; sets the px-per-inch scale
WIDTH_IN = 4.5       # pinned effective print width
COL2_SHIFT_IN = 0.4  # move column 2 (5-mātrā) left by this much (at REF_H_IN scale)


def group(body: str, dx: float, dy: float) -> str:
    return f'<g transform="translate({dx:.1f},{dy:.1f})">\n{body}\n</g>'


def main() -> None:
    # Panels carry no legend; one shared legend goes in the top-right block.
    b3, w3, h3 = build(3, show_ruler=False, show_legend=False)
    b4, w4, h4 = build(4, show_legend=False)
    b5, w5, h5 = build(5, show_legend=False)

    col_w = max(w3, w4, w5)
    col1_x = MARGIN
    col1_h = h3 + STACK_GAP + h4          # taller than h5
    canvas_h = MARGIN + col1_h + MARGIN

    # The figure prints at REF_H_IN tall (height fixed); the column-2 left-shift
    # and right-edge trim below bring the effective width to ~4.5 in.
    px_per_in = canvas_h / REF_H_IN
    col2_x = MARGIN + col_w + COL_GAP - round(COL2_SHIFT_IN * px_per_in)
    # Pin the effective width (smaller title fonts would otherwise shrink it).
    canvas_w = max(round(WIDTH_IN * px_per_in), col2_x + col_w + MARGIN)

    y3 = MARGIN
    y4 = MARGIN + h3 + STACK_GAP
    y5 = (y4 + h4) - h5                   # bottom-align the 5-mātrā with the 4-mātrā

    # One shared legend, centered over column 2 in the empty block above the
    # bottom-aligned 5-mātrā panel.
    legend = text(col2_x + col_w / 2, MARGIN + 42, LEGEND_TEXT, FS_LEGEND,
                  fill=MUTED, family=DEV_FONT)

    body = "\n".join([
        group(b3, col1_x, y3),
        group(b4, col1_x, y4),
        group(b5, col2_x, y5),
        legend,
    ])

    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w:.0f}" '
        f'height="{canvas_h:.0f}" viewBox="0 0 {canvas_w:.0f} {canvas_h:.0f}">\n'
        '<title>Chandas mātrā tiles — 3, 4, 5 mātrās</title>\n'
        '<rect width="100%" height="100%" fill="white"/>\n'
        f'{body}\n</svg>\n'
    )
    out = BUILD_DIR / "matra_tiles_combined.svg"
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({canvas_w:.0f}x{canvas_h:.0f}px; "
          f"at {REF_H_IN:.0f}in tall = {canvas_w * REF_H_IN / canvas_h:.2f}in wide)")


if __name__ == "__main__":
    main()
