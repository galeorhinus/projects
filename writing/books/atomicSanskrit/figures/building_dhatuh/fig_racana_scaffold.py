#!/usr/bin/env python3
"""
fig_racana_scaffold.py — One CV1C scaffold, four fillings.

Left column: four CV1C dhātavaḥ (गम्, नम्, पच्, वद्) rendered at the same
hex size as the mātrā-envelope figure.
Right column: one largish empty CV1C scaffold with slot labels C / V1 / C.
Arrows fan from each example to the scaffold, illustrating that distinct
fillings inhabit a shared dhāturacanā.

Output: figures/build/building_dhatuh_racana_scaffold.svg
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))

from dhatu_hexagon import (  # noqa: E402
    EDGE_LENGTH,
    HEX_HEIGHT,
    WIDTH_BY_CLASS,
    SIMPLE_FILL_CONSONANT,
    SIMPLE_FILL_VOWEL,
    SIMPLE_STROKE,
    SIMPLE_STROKE_WIDTH,
    compute_layout,
    parse_dhatu_string,
    render_hexagon,
)


# Template hex fill colors — match the example-row "simple" palette.
TEMPLATE_FILL_BY_CLASS = {
    "C":  SIMPLE_FILL_CONSONANT,
    "V1": SIMPLE_FILL_VOWEL,
    "V2": SIMPLE_FILL_VOWEL,
}


# Four CV1C dhātus on the left.
EXAMPLES = [
    ("गम्",  "gam", "g,a,m"),
    ("नम्",  "nam", "n,a,m"),
    ("पच्",  "pac", "p,a,c"),
    ("वद्",  "vad", "v,a,d"),
]

# Right-column scaffold — CV1C with slot labels.
TEMPLATE_SLOTS = [
    ("C",  "C"),
    ("V1", "V1"),
    ("C",  "C"),
]


# --- Layout parameters ---

CANVAS_W = 900
CANVAS_H = 540

LABEL_X       = 24     # x-position of example label (left of strip)
LEFT_COL_X    = 140    # left column strip's leftmost canvas-x
ROW_H         = 120    # vertical pitch between example rows
FIRST_ROW_TY  = 90     # strip-midline y of the first (top) example row

TEMPLATE_SCALE     = 1.8
TEMPLATE_EDGE      = EDGE_LENGTH * TEMPLATE_SCALE
TEMPLATE_HEX_H     = TEMPLATE_EDGE * math.sqrt(3)
TEMPLATE_WIDTH_BY_CLASS = {
    "C":  TEMPLATE_EDGE / 2,
    "V1": TEMPLATE_EDGE,
    "V2": TEMPLATE_EDGE * 2,
}
RIGHT_COL_X   = 540    # template's leftmost canvas-x


def strip_extent(particles):
    positions = compute_layout(particles)
    xs = []
    for (cx, _cy), v in zip(positions, particles):
        w = WIDTH_BY_CLASS[v["class"]]
        xs.extend([cx - w / 2 - EDGE_LENGTH / 2, cx + w / 2 + EDGE_LENGTH / 2])
    return min(xs), max(xs)


def render_example(row, deva, iast, dhatu_str):
    """Render one example dhātu strip with a title above it. Returns
    (svg fragment, right-edge canvas x, strip-midline canvas y)."""
    particles = parse_dhatu_string(dhatu_str)
    positions = compute_layout(particles)
    xmin_local, xmax_local = strip_extent(particles)

    ty = FIRST_ROW_TY + row * ROW_H
    tx = LEFT_COL_X - xmin_local

    parts = []

    # Label to the left of the strip, vertically centered at strip midline.
    parts.append(
        f'<text x="{LABEL_X}" y="{ty + 6}" '
        f'font-family="Charter, Georgia, Times, serif" '
        f'font-size="18" font-weight="500" text-anchor="start" fill="#1a1a1a">'
        f'<tspan font-family="Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Charter, Georgia, Times, serif">{deva}</tspan>'
        f' — '
        f'<tspan font-style="italic">{iast}</tspan>'
        f'</text>'
    )

    for (cx, cy), v in zip(positions, particles):
        parts.append(
            f'<g transform="translate({tx:.1f},{ty:.1f})">'
            f'{render_hexagon(cx, cy, v, style="simple")}'
            f'</g>'
        )

    right_edge_x = tx + xmax_local
    return "\n  ".join(parts), right_edge_x, ty


def template_hex_vertices(cx, cy, w):
    e = TEMPLATE_EDGE
    h = TEMPLATE_HEX_H
    return [
        (cx - w/2,         cy - h/2),
        (cx + w/2,         cy - h/2),
        (cx + w/2 + e/2,   cy),
        (cx + w/2,         cy + h/2),
        (cx - w/2,         cy + h/2),
        (cx - w/2 - e/2,   cy),
    ]


def template_layout():
    """Same zigzag logic as compute_layout, but with TEMPLATE_EDGE scaling."""
    e = TEMPLATE_EDGE
    h = TEMPLATE_HEX_H
    positions = []
    cx_running = 0.0
    cy_init = -h / 4
    for i, (cls, _label) in enumerate(TEMPLATE_SLOTS):
        w = TEMPLATE_WIDTH_BY_CLASS[cls]
        if i == 0:
            positions.append((cx_running, cy_init))
            continue
        prev_cls, _ = TEMPLATE_SLOTS[i - 1]
        prev_w = TEMPLATE_WIDTH_BY_CLASS[prev_cls]
        cx_new = positions[-1][0] + (prev_w + w) / 2 + e / 2
        cy_new = (-h/4) if positions[-1][1] > -h/4 else (h/4)
        positions.append((cx_new, cy_new))
    return positions


def render_template(template_cy):
    positions = template_layout()
    e = TEMPLATE_EDGE

    xs = []
    for (cx, _cy), (cls, _label) in zip(positions, TEMPLATE_SLOTS):
        w = TEMPLATE_WIDTH_BY_CLASS[cls]
        xs.extend([cx - w/2 - e/2, cx + w/2 + e/2])
    xmin_local, xmax_local = min(xs), max(xs)

    tx = RIGHT_COL_X - xmin_local
    ty = template_cy

    parts = []

    for (cx, cy), (cls, label) in zip(positions, TEMPLATE_SLOTS):
        w = TEMPLATE_WIDTH_BY_CLASS[cls]
        verts = template_hex_vertices(cx, cy, w)
        points_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts)
        fill = TEMPLATE_FILL_BY_CLASS[cls]
        parts.append(
            f'<g transform="translate({tx:.1f},{ty:.1f})">'
            f'<polygon points="{points_str}" fill="{fill}" '
            f'stroke="{SIMPLE_STROKE}" stroke-width="{SIMPLE_STROKE_WIDTH}" '
            f'stroke-linejoin="round"/>'
            f'<text x="{cx:.1f}" y="{cy + 7:.1f}" '
            f'font-family="Charter, Georgia, Times, serif" '
            f'font-size="22" font-weight="500" font-style="italic" '
            f'text-anchor="middle" fill="#1a1a1a">'
            f'{label}</text>'
            f'</g>'
        )

    # Label below the scaffold — "the gamādi atomic scaffold".
    # Position: centered horizontally over the scaffold's x-extent, below its bottom.
    template_canvas_cx = tx + (xmin_local + xmax_local) / 2
    template_bottom_y = ty + max(cy for (cx, cy) in positions) + TEMPLATE_HEX_H / 2
    label_y = template_bottom_y + 30
    parts.append(
        f'<text x="{template_canvas_cx:.1f}" y="{label_y:.1f}" '
        f'font-family="Charter, Georgia, Times, serif" '
        f'font-size="18" font-weight="500" text-anchor="middle" fill="#1a1a1a">'
        f'the <tspan font-family="Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Charter, Georgia, Times, serif">गमादि</tspan>'
        f' (<tspan font-style="italic">gamādi</tspan>) atomic scaffold</text>'
    )

    left_edge_x = tx + xmin_local
    return "\n  ".join(parts), left_edge_x


def main():
    # Place the template's vertical center at the midline of the example rows.
    n_rows = len(EXAMPLES)
    first_ty = FIRST_ROW_TY
    last_ty = FIRST_ROW_TY + (n_rows - 1) * ROW_H
    template_cy = (first_ty + last_ty) / 2

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'width="{CANVAS_W}" height="{CANVAS_H}">'
    )
    svg_parts.append('  <title>One CV1C scaffold, four fillings</title>')
    svg_parts.append(
        f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="white"/>'
    )
    svg_parts.append('  <defs>')
    svg_parts.append(
        '    <marker id="arrowhead" markerWidth="10" markerHeight="8" '
        'refX="9" refY="4" orient="auto" markerUnits="strokeWidth">'
        '<polygon points="0,0 9,4 0,8" fill="#555"/>'
        '</marker>'
    )
    svg_parts.append('  </defs>')
    svg_parts.append(
        '  <text x="205" y="32" '
        'font-family="Charter, Georgia, Times, serif" '
        'font-size="18" font-weight="600" text-anchor="middle" fill="#1a1a1a">'
        'filled <tspan font-style="italic">dhātavaḥ</tspan></text>'
    )
    svg_parts.append(
        '  <text x="684" y="142" '
        'font-family="Charter, Georgia, Times, serif" '
        'font-size="18" font-weight="600" text-anchor="middle" fill="#1a1a1a">'
        'shared CV1C scaffold</text>'
    )

    # Render the 4 example strips, collect arrow start anchors.
    example_anchors = []
    for i, (deva, iast, dhatu_str) in enumerate(EXAMPLES):
        ex_svg, right_x, ty = render_example(i, deva, iast, dhatu_str)
        svg_parts.append("  " + ex_svg)
        example_anchors.append((right_x, ty))

    # Render the template, collect arrow end anchor.
    tpl_svg, tpl_left_x = render_template(template_cy)
    svg_parts.append("  " + tpl_svg)

    # Draw arrows from each example to the template, with arrowheads
    # spread vertically along the first hex's left V-shape (no point-convergence).
    # The first hex's leftmost-point P6 is at template_cy - TEMPLATE_HEX_H / 4;
    # P1 (top corner) and P5 (bottom corner) are h/2 above and below it
    # respectively. Spread the arrow tips evenly inside that vertical range.
    n = len(example_anchors)
    v_center_y = template_cy - TEMPLATE_HEX_H / 4
    arrow_spread = TEMPLATE_HEX_H * 0.8   # ~100 px for TEMPLATE_HEX_H ≈ 125
    step = arrow_spread / (n - 1) if n > 1 else 0
    for i, (ex_right, ex_cy) in enumerate(example_anchors):
        x1 = ex_right + 12
        y1 = ex_cy
        x2 = tpl_left_x - 14
        y2 = v_center_y - arrow_spread / 2 + i * step
        svg_parts.append(
            f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#555" stroke-width="1.4" marker-end="url(#arrowhead)"/>'
        )

    svg_parts.append("</svg>")

    out_path = REPO_ROOT / "figures" / "build" / "building_dhatuh_racana_scaffold.svg"
    out_path.write_text("\n".join(svg_parts), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
