#!/usr/bin/env python3
"""matra_style.py — shared palette + mātrā-tile style for the hex figures.

Single source of truth for the warm colour scheme, stroke weights, fonts, and
the mātrā ruler / gridline / SVG helpers used across the calibration-style hex
figures (matra_tiles, matra_envelope, …). Change a colour here and every figure
that imports it updates — no need to touch each script.

What lives here:        the *style* — colours, fonts, stroke, and the chrome
                        helpers (text / ruler / gridlines / svg), parameterised
                        by each figure's own scale and font sizes.
What stays per-figure:   geometry choices (TILE_SCALE, MATRA_UNIT), font sizes,
                        and layout.  The varṇa *data* lives in dhatu_hexagon.py.

The geometry convention `matra_width = mātrā · unit − slant` makes a strip's
mātrā footprint exactly `mātrā · unit`, so a single ruler aligns with the tiles.
"""

from __future__ import annotations

import math

# --- Palette (the single source of truth for colour) -----------------------

BG          = "#ffffff"   # background
LIGHT_FILL  = "#d8c7a3"   # tan — the lighter weight (1-mātrā / laghu / vowel)
DARK_FILL   = "#4a3a28"   # dark brown — the heavier weight (2-mātrā / guru / consonant)
STROKE      = "#5c4830"   # tile outline
INK_LIGHT   = "#f4eedd"   # ink on dark fills (cream)
INK_DARK    = "#3d2f1f"   # ink on light fills (dark brown)
GOLD        = "#a8842c"   # accent (e.g. the result column)
TEXT        = "#3d2f1f"   # default dark-brown ink (titles)
MUTED       = "#6b563a"   # secondary brown (subtitles, labels, ruler text)
RULER       = "#7a6647"   # ruler line + ticks
GUIDE       = "#cdbf9e"   # dashed major-tick gridlines

# Aliases for the matra_tiles vocabulary (laghu/guru).
LAGHU_FILL  = LIGHT_FILL
GURU_FILL   = DARK_FILL
GURU_TEXT   = INK_LIGHT
LAGHU_TEXT  = INK_DARK

STROKE_W    = 1.0         # default stroke width (hex outlines, ruler)

# --- Fonts -----------------------------------------------------------------

LATIN_FONT  = "Charter, Georgia, Times, serif"
DEV_FONT    = "Noto Sans Devanagari, Mangal, Devanagari Sangam MN, sans-serif"
SERIF_TITLE = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

WIDTH_IN    = 4.5         # figures render at this width


# --- Generic helpers -------------------------------------------------------

def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pt_to_px(pt: float, viewbox_w: float, width_in: float = WIDTH_IN) -> float:
    """px (user units) for a target point size when rendered at width_in wide."""
    return pt * viewbox_w / (width_in * 72.0)


def text(x: float, y: float, content: str, size: float, *, fill: str = TEXT,
         anchor: str = "middle", weight: str = "400", style: str = "normal",
         family: str = LATIN_FONT, halo: float = 0.0) -> str:
    halo_attr = (
        f'paint-order="stroke" stroke="{BG}" stroke-width="{halo}" '
        f'stroke-linejoin="round" ' if halo else ""
    )
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" '
        f'dominant-baseline="middle" {halo_attr}fill="{fill}">{esc(content)}</text>'
    )


# --- Mātrā geometry --------------------------------------------------------

def matra_width(matra: float, *, matra_unit: float, slant: float) -> float:
    """Flat-top width whose mātrā footprint (flat + one slant) is matra·unit."""
    return matra * matra_unit - slant


def hex_points(cx: float, cy: float, w: float, *, slant: float, hex_height: float) -> str:
    """Flat-top hexagon: flat-width w, slant projection `slant` each side."""
    h = hex_height
    pts = [
        (cx - w / 2, cy - h / 2),
        (cx + w / 2, cy - h / 2),
        (cx + w / 2 + slant, cy),
        (cx + w / 2, cy + h / 2),
        (cx - w / 2, cy + h / 2),
        (cx - w / 2 - slant, cy),
    ]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def varna_label(cx: float, cy: float, deva: str, iast: str, *, ink: str,
                fs_dev: float, fs_iast: float, dev_weight: str = "600",
                family_dev: str = DEV_FONT) -> str:
    """Stacked varṇa label: Devanagari centred, IAST tucked just beneath it.

    Offsets scale with the font sizes so the pairing reads the same in every
    figure — the single place that fixes Devanagari ↔ IAST spacing.
    """
    dev_y = cy - 0.30 * fs_dev
    iast_y = dev_y + 0.5 * fs_dev + 0.5 * fs_iast + 1.0
    return (
        text(cx, dev_y, deva, fs_dev, fill=ink, weight=dev_weight, family=family_dev)
        + "\n  "
        + text(cx, iast_y, iast, fs_iast, fill=ink, style="italic")
    )


# --- Chrome: ruler + gridlines ---------------------------------------------

def render_ruler(x_start: float, y: float, n: int, *, matra_unit: float,
                 fs_num: float, fs_label: float, label: str = "mātrā",
                 num_dy: float = 16, label_dy: float | None = None,
                 color: str = RULER, line_w: float = STROKE_W) -> str:
    """Half-mātrā ruler from x_start spanning n mātrās (ticks 0..n)."""
    end_x = x_start + n * matra_unit
    frags = [
        f'<line x1="{x_start:.1f}" y1="{y:.1f}" x2="{end_x:.1f}" y2="{y:.1f}" '
        f'stroke="{color}" stroke-width="{line_w}"/>'
    ]
    for i in range(int(round(n * 2)) + 1):
        x = x_start + i * matra_unit / 2
        major = i % 2 == 0
        tick = 11 if major else 6
        frags.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - tick:.1f}" '
            f'stroke="{color}" stroke-width="{line_w}"/>'
        )
        if major:
            frags.append(text(x, y + num_dy, f"{i // 2}", fs_num, fill=MUTED))
    if label:
        ly = y + (label_dy if label_dy is not None else num_dy + fs_label + 2)
        frags.append(text((x_start + end_x) / 2, ly, label, fs_label,
                          fill=MUTED, style="italic"))
    return "\n  ".join(frags)


def gridlines(x0: float, n: int, y_top: float, y_bottom: float, *,
              matra_unit: float, color: str = GUIDE) -> str:
    """Vertical dashed gridlines at every major (integer) mātrā tick, 0..n."""
    out = []
    for i in range(n + 1):
        gx = x0 + i * matra_unit
        out.append(
            f'<line x1="{gx:.1f}" y1="{y_top:.1f}" x2="{gx:.1f}" y2="{y_bottom:.1f}" '
            f'stroke="{color}" stroke-width="1" stroke-dasharray="3,4"/>'
        )
    return "\n  ".join(out)


def svg(viewbox_w: float, viewbox_h: float, body: str, *, title: str = "",
        width_in: float = WIDTH_IN, bg: str = BG) -> str:
    """Wrap body in an SVG that renders at width_in wide (height keeps aspect)."""
    height_in = viewbox_h / viewbox_w * width_in
    return (
        f'<svg viewBox="0 0 {viewbox_w:.0f} {viewbox_h:.0f}" width="{width_in}in" '
        f'height="{height_in:.3f}in" xmlns="http://www.w3.org/2000/svg" '
        f'preserveAspectRatio="xMidYMid meet">\n'
        f'<title>{esc(title)}</title>\n'
        f'<rect width="100%" height="100%" fill="{bg}"/>\n'
        f'{body}\n</svg>\n'
    )
