#!/usr/bin/env python3
"""racana_scaffold.py — one CV1C scaffold, four fillings.

Left column: four CV1C dhātavaḥ (गम्, नम्, पच्, वद्) at a small scale, filled in
the warm calibration palette. Right: one large empty CV1C scaffold (outline
only) with slot labels C · V1 · C. Arrows fan from each filling to the shared
scaffold — distinct fillings, one dhāturacanā.

Both sides are 2-mātrā strips (C½ + V1 + C½). A mātrā ruler under each side
spans 0–2; the two rulers are physically different widths because the two sides
are drawn at different scales — the same measure, two magnifications.

Style (palette, fonts, ruler, hexes, labels) comes from
figures/_shared/matra_style.py; varṇa data from dhatu_hexagon.py.

The figure sits at width=100% in the trade layout (4.75 in text width); fonts
are sized to land in the 9–11 pt band there.

Output: figures/build/racana_scaffold.from-py.svg
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))
sys.path.insert(0, str(REPO_ROOT / "figures" / "_shared"))

import matra_style as ms  # noqa: E402
from dhatu_hexagon import (  # noqa: E402
    EDGE_LENGTH as EDGE_BASE,
    HEX_HEIGHT as HEX_BASE,
    devanagari_label,
    parse_dhatu_string,
)

EXAMPLES = [
    ("गम्", "gam", "g,a,m"),
    ("नम्", "nam", "n,a,m"),
    ("पच्", "pac", "p,a,c"),
    ("वद्", "vad", "v,a,d"),
]

# --- Two scales: small fillings (left), large scaffold (right) --------------

SCALE_L = 0.6                                 # 20% larger than the envelope scale
EDGE_L, HEX_L, SLANT_L, MU_L = (EDGE_BASE * SCALE_L, HEX_BASE * SCALE_L,
                                EDGE_BASE * SCALE_L / 2, 72 * SCALE_L)
SCALE_R = 1.3
EDGE_R, HEX_R, SLANT_R, MU_R = (EDGE_BASE * SCALE_R, HEX_BASE * SCALE_R,
                                EDGE_BASE * SCALE_R / 2, 72 * SCALE_R)

# --- Horizontal layout ------------------------------------------------------

MARGIN = 18
LABEL_W = 110                                 # room for "गम् — gam"; nudges dhātus right
MEASURE_L = MARGIN + LABEL_W + SLANT_L / 2    # mātrā-0 of the left strips
LEFT_RIGHT = MEASURE_L + 2 * MU_L + SLANT_L / 2
ARROW_GAP = 66                                # shorter arrows; pulls scaffold ~0.25in left
MEASURE_R = LEFT_RIGHT + ARROW_GAP + SLANT_R / 2   # mātrā-0 of the scaffold
CANVAS_W = MEASURE_R + 2 * MU_R + SLANT_R / 2 + MARGIN

# --- Vertical layout --------------------------------------------------------

STRIP_HALF_L = 3 * HEX_L / 4
STRIP_HALF_R = 3 * HEX_R / 4
TOP = 18
HEADER_Y = TOP + 13
ROW_CY0 = HEADER_Y + 32 + STRIP_HALF_L
PITCH_L = 2 * STRIP_HALF_L + 28
LAST_CY = ROW_CY0 + (len(EXAMPLES) - 1) * PITCH_L
SCAFFOLD_CY = (ROW_CY0 + LAST_CY) / 2
RULER_Y = max(LAST_CY + STRIP_HALF_L, SCAFFOLD_CY + STRIP_HALF_R) + 26
CANVAS_H = RULER_Y + 52   # room below the "mātrā" axis label

# --- Fonts (px → pt at the 4.5 in rendered width) ---------------------------

TW = 4.5
FS_HEADER = ms.pt_to_px(11.0, CANVAS_W, TW)
FS_LABEL = ms.pt_to_px(10.5, CANVAS_W, TW)
FS_DEV = ms.pt_to_px(9.5, CANVAS_W, TW)
FS_IAST = ms.pt_to_px(9.0, CANVAS_W, TW)
FS_SLOT = ms.pt_to_px(11.0, CANVAS_W, TW)
FS_RULER = ms.pt_to_px(9.5, CANVAS_W, TW)

ARROW = ms.MUTED


def cv1c_layout(mu, slant, hexh):
    """Staggered positions for a C-V1-C strip (C upper rail, V1 lower)."""
    slots = [("C", 0.5, False), ("V1", 1.0, True), ("C", 0.5, False)]
    up, lo = -hexh / 4, hexh / 4
    out = []
    for i, (cls, m, isv) in enumerate(slots):
        w = ms.matra_width(m, matra_unit=mu, slant=slant)
        cy = lo if isv else up
        cx = 0.0 if i == 0 else out[-1][1] + (out[-1][3] + w) / 2 + slant
        out.append((cls, cx, cy, w))
    return out


def tspan_label(x, y, deva, iast, size, *, anchor):
    """Devanagari — italic IAST, on one line (for the left-column labels)."""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{ms.LATIN_FONT}" '
        f'font-size="{size}" text-anchor="{anchor}" dominant-baseline="middle" '
        f'fill="{ms.TEXT}"><tspan font-family="{ms.DEV_FONT}">{deva}</tspan>'
        f' — <tspan font-style="italic">{iast}</tspan></text>'
    )


def render_example(row_cy, dhatu_str):
    particles = parse_dhatu_string(dhatu_str)
    lay = cv1c_layout(MU_L, SLANT_L, HEX_L)
    dx = MEASURE_L - (lay[0][1] - lay[0][3] / 2 - SLANT_L / 2)
    parts, right = [], 0.0
    for (cls, cx, cy, w), p in zip(lay, particles):
        X, Y = cx + dx, cy + row_cy
        is_v = cls.startswith("V")
        fill = ms.LIGHT_FILL if is_v else ms.DARK_FILL
        ink = ms.INK_DARK if is_v else ms.INK_LIGHT
        parts.append(
            f'<polygon points="{ms.hex_points(X, Y, w, slant=SLANT_L, hex_height=HEX_L)}" '
            f'fill="{fill}" stroke="{ms.STROKE}" stroke-width="{ms.STROKE_W}" stroke-linejoin="round"/>'
        )
        parts.append(ms.varna_label(X, Y, devanagari_label(p), p["iast"],
                                    ink=ink, fs_dev=FS_DEV, fs_iast=FS_IAST))
        right = max(right, X + w / 2 + SLANT_L / 2)
    return "\n  ".join(parts), right


def render_scaffold(cy0):
    lay = cv1c_layout(MU_R, SLANT_R, HEX_R)
    dx = MEASURE_R - (lay[0][1] - lay[0][3] / 2 - SLANT_R / 2)
    parts, left = [], 1e9
    for cls, cx, cy, w in lay:
        X, Y = cx + dx, cy + cy0
        parts.append(
            f'<polygon points="{ms.hex_points(X, Y, w, slant=SLANT_R, hex_height=HEX_R)}" '
            f'fill="none" stroke="{ms.STROKE}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        parts.append(ms.text(X, Y, cls, FS_SLOT, fill=ms.MUTED, style="italic"))
        left = min(left, X - w / 2 - SLANT_R / 2)
    return "\n  ".join(parts), left


def main():
    body = []

    # Column headers.
    left_cx = MEASURE_L + MU_L
    right_cx = MEASURE_R + MU_R
    body.append(
        f'<text x="{left_cx:.1f}" y="{HEADER_Y:.1f}" font-family="{ms.LATIN_FONT}" '
        f'font-size="{FS_HEADER}" font-weight="600" text-anchor="middle" '
        f'fill="{ms.TEXT}">filled <tspan font-style="italic">dhātavaḥ</tspan></text>'
    )
    body.append(
        f'<text x="{CANVAS_W - MARGIN:.1f}" y="{HEADER_Y:.1f}" font-family="{ms.LATIN_FONT}" '
        f'font-size="{FS_HEADER}" font-weight="600" text-anchor="end" '
        f'dominant-baseline="middle" fill="{ms.TEXT}">'
        f'<tspan font-family="{ms.DEV_FONT}">गमादि</tspan> '
        f'(<tspan font-style="italic">gamādi</tspan>) / CV1C scaffold</text>'
    )

    # Left fillings + their labels; collect arrow start anchors.
    anchors = []
    for i, (deva, iast, dstr) in enumerate(EXAMPLES):
        cy = ROW_CY0 + i * PITCH_L
        body.append(tspan_label(MEASURE_L - SLANT_L / 2 - 10, cy, deva, iast,
                                FS_LABEL, anchor="end"))
        strip, right = render_example(cy, dstr)
        body.append(strip)
        anchors.append((right, cy))

    # Scaffold.
    scaffold, scaffold_left = render_scaffold(SCAFFOLD_CY)
    body.append(scaffold)

    # Arrows fan from each filling to the scaffold's left V-edge.
    v_center = SCAFFOLD_CY - HEX_R / 4
    spread = HEX_R * 0.8
    step = spread / (len(anchors) - 1)
    for i, (ex_right, ex_cy) in enumerate(anchors):
        x2 = scaffold_left - 14
        y2 = v_center - spread / 2 + i * step
        body.append(
            f'<line x1="{ex_right + 12:.1f}" y1="{ex_cy:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{ARROW}" stroke-width="1.4" marker-end="url(#arrowhead)"/>'
        )

    # A 0–2 mātrā ruler under each side — same measure, two scales.
    body.append(ms.render_ruler(MEASURE_L, RULER_Y, 2, matra_unit=MU_L,
                                fs_num=FS_RULER, fs_label=FS_RULER))
    body.append(ms.render_ruler(MEASURE_R, RULER_Y, 2, matra_unit=MU_R,
                                fs_num=FS_RULER, fs_label=FS_RULER))

    defs = (
        '<defs><marker id="arrowhead" markerWidth="10" markerHeight="8" refX="9" '
        f'refY="4" orient="auto" markerUnits="strokeWidth"><polygon points="0,0 9,4 0,8" '
        f'fill="{ARROW}"/></marker></defs>'
    )
    doc = ms.svg(CANVAS_W, CANVAS_H, defs + "\n" + "\n".join(body),
                 title="One CV1C scaffold, four fillings", width_in=TW)

    out = REPO_ROOT / "figures" / "build" / "racana_scaffold.from-py.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({CANVAS_W:.0f}x{CANVAS_H:.0f}px = "
          f"{TW}in x {CANVAS_H / CANVAS_W * TW:.2f}in)")


if __name__ == "__main__":
    main()
