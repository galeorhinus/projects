#!/usr/bin/env python3
"""Ch 9 — Subcontinental overlay: four languages on one place-axis.

The figure proposed in working/inventory_atlas_roadmap.md §4.1 finally
gets a deployment.  Four languages overlaid on a single shared
12-column place-axis ribbon, each rendered with a distinct visual
code so overlap is legible at a glance:

  Sanskrit  — filled circle      (the engineered selection — protagonist)
  Tamil     — outlined circle    (southern subcontinental parallel)
  Kurukh    — dashed outer ring  (central forest belt parallel)
  Toda      — small inner dot    (Nilgiri parallel)

When multiple languages light the same place column the codes layer
concentrically.  When only one lights a column the lone code stands.

Layout (5.0 × 3.4 in canvas):

  - Wide top ribbon (r=5, W=0.50): the labelled 12-place axis,
    alternating-gray segments, full radial place names inside each
    segment, articulator-group arcs (LAB / CORONAL / DORSAL ·
    LARYNGEAL) above.  Same idiom as the Ch 7 hotzones_panels figure.
  - Single overlay row directly below: r=5, W=0.30, quieter
    alternating-gray segments.  All four languages' visual codes
    drawn at each lit column's anatomical theta.
  - Legend strip at the bottom: the four visual codes mapped to
    language names + total consonant count.

Reads each language's inventory from the shared toolkit configs at
_shared/toolkits/vocal_tract/configs/scatter_<lang>.json — same data
the existing per-language scatter charts and the Sk-vs-X polished
overlays use.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.toolkits.vocal_tract.schematics import point_at  # noqa: E402
from _shared.toolkits.vocal_tract import CONFIGS_DIR  # noqa: E402


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

# (config slug, display label, visual code, code radius in inches)
# Radii chosen so codes layer concentrically without obscuring each other:
# inside-out → dot, filled, outlined, dashed-ring.
LANGUAGES = [
    ("toda",     "Toda",     "dot",      0.026),
    ("sanskrit", "Sanskrit", "filled",   0.064),
    ("tamil",    "Tamil",    "outlined", 0.094),
    ("kurukh",   "Kurukh",   "dashed",   0.118),
]

PLACE_LINES = [
    ("BI-",      "LABIAL"),     # bilabial
    ("LABIO-",   "DENTAL"),     # labio-dental
    ("INTER-",   "DENTAL"),     # interdental
    ("DENTAL",   ""),           # dental
    ("ALVEO-",   "LAR"),        # alveolar
    ("POST-",    "ALV."),       # post-alveolar
    ("RETRO-",   "FLEX"),       # retroflex
    ("PALATAL",  ""),           # palatal
    ("VELAR",    ""),           # velar
    ("UVULAR",   ""),           # uvular
    ("PHAR-",    "YNGEAL"),     # pharyngeal
    ("GLOTTAL",  ""),           # glottal
]

GROUPS = [
    ("LAB",       {0, 1}),
    ("CORONAL",   {2, 3, 4, 5, 6}),
    ("DORSAL",    {7, 8}),
    ("LARYNGEAL", {9, 10, 11}),
]

ANGULAR_RANGE = (155.0, 205.0)
R1 = R2 = 5.00
WIDE_W   = 0.50
OVERLAY_W = 0.32

W = 5.0
H = 3.50

TOP_TRANSLATE_X = W / 2 - (-math.sin(math.radians(180.0)) * R1)
GROUP_ARC_R     = R1 + WIDE_W / 2 + 0.10   # = 5.35
GROUP_LABEL_R   = R1 + WIDE_W / 2 + 0.20   # = 5.45
TOP_TRANSLATE_Y = 0.20 + GROUP_LABEL_R     # = 5.65

WIDE_INNER_R     = R1 - WIDE_W / 2         # 4.75
OVERLAY_OUTER_R  = R1 + OVERLAY_W / 2      # 5.16
OVERLAY_INNER_R  = R1 - OVERLAY_W / 2      # 4.84

WIDE_RIBBON_BOTTOM_Y = TOP_TRANSLATE_Y + (
    math.cos(math.radians(ANGULAR_RANGE[0])) * WIDE_INNER_R
)
OVERLAY_TOP_GAP    = 0.08
OVERLAY_TRANSLATE_Y = (
    WIDE_RIBBON_BOTTOM_Y + OVERLAY_TOP_GAP + OVERLAY_OUTER_R
)
OVERLAY_INNER_ENDPOINT_Y = OVERLAY_TRANSLATE_Y + (
    math.cos(math.radians(ANGULAR_RANGE[0])) * OVERLAY_INNER_R
)

LEGEND_Y       = OVERLAY_INNER_ENDPOINT_Y + 0.36
CAPTION_Y      = LEGEND_Y + 0.40


PALETTE = {
    "background":      "#f4f4f3",
    "segment_light":   "#ece9e2",
    "segment_dark":    "#d4d0c5",
    "overlay_lite":    "#f1efea",
    "overlay_dark":    "#dedbd4",
    "ribbon_stroke":   "#9a9892",
    "narrow_stroke":   "#b8b6b0",
    "segment_text":    "#3a3a3c",
    "group_arc":       "#8f8d86",
    "mark":            "#2b2b2d",
    "label":           "#2b2b2d",
    "muted":           "#8f8d86",
}
FONT = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def column_thetas() -> list[float]:
    start, end = ANGULAR_RANGE
    n = len(PLACE_LINES)
    seg_w = (end - start) / n
    return [start + (i + 0.5) * seg_w for i in range(n)]


def segment_boundaries() -> list[tuple[float, float]]:
    start, end = ANGULAR_RANGE
    n = len(PLACE_LINES)
    seg_w = (end - start) / n
    return [(start + i * seg_w, start + (i + 1) * seg_w) for i in range(n)]


def count_per_column(matrix: list[list[str]]) -> list[int]:
    counts = [0] * 12
    for row in matrix:
        for col_idx, cell in enumerate(row):
            if cell:
                counts[col_idx] += 1
    return counts


def segment_path(r_inner: float, r_outer: float, t1: float, t2: float) -> str:
    x1o, y1o = point_at(r_outer, r_outer, t1)
    x2o, y2o = point_at(r_outer, r_outer, t2)
    x2i, y2i = point_at(r_inner, r_inner, t2)
    x1i, y1i = point_at(r_inner, r_inner, t1)
    return (
        f"M {x1o:.4f} {y1o:.4f} "
        f"A {r_outer:.4f} {r_outer:.4f} 0 0 1 {x2o:.4f} {y2o:.4f} "
        f"L {x2i:.4f} {y2i:.4f} "
        f"A {r_inner:.4f} {r_inner:.4f} 0 0 0 {x1i:.4f} {y1i:.4f} "
        f"Z"
    )


def _arc_path(r: float, t1: float, t2: float) -> str:
    x1, y1 = point_at(r, r, t1)
    x2, y2 = point_at(r, r, t2)
    large = 1 if abs(t2 - t1) > 180 else 0
    sweep = 1 if t2 > t1 else 0
    return (
        f"M {x1:.4f} {y1:.4f} "
        f"A {r:.4f} {r:.4f} 0 {large} {sweep} {x2:.4f} {y2:.4f}"
    )


# ---------------------------------------------------------------------------
# Visual codes — the four marker types
# ---------------------------------------------------------------------------

def visual_code(kind: str, cx: float, cy: float, r: float) -> str:
    """Return SVG for one language's visual code at (cx, cy)."""
    if kind == "filled":
        return (
            f'<circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r:.4f}" '
            f'fill="{PALETTE["mark"]}" opacity="0.85" />'
        )
    if kind == "outlined":
        return (
            f'<circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r:.4f}" '
            f'fill="none" stroke="{PALETTE["mark"]}" stroke-width="0.014" />'
        )
    if kind == "dashed":
        return (
            f'<circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r:.4f}" '
            f'fill="none" stroke="{PALETTE["mark"]}" stroke-width="0.014" '
            f'stroke-dasharray="0.05 0.030" />'
        )
    if kind == "dot":
        return (
            f'<circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r:.4f}" '
            f'fill="{PALETTE["mark"]}" />'
        )
    raise ValueError(f"unknown visual code: {kind}")


# ---------------------------------------------------------------------------
# Wide top ribbon — labelled place-axis (same idiom as hotzones_panels)
# ---------------------------------------------------------------------------

def render_radial_pair(theta: float, lines: tuple[str, str],
                       font_size: float) -> str:
    flip = theta < 180.0
    rotation = theta - 270.0 + (180.0 if flip else 0.0)

    R_rad = math.radians(rotation)
    above_x = math.sin(R_rad)
    above_y = -math.cos(R_rad)

    actual = [line for line in lines if line]
    n = len(actual)
    line_height = font_size * 1.10

    chunks: list[str] = []
    seg_x, seg_y = point_at(R1, R1, theta)
    for i, line in enumerate(actual):
        offset = ((n - 1) / 2 - i) * line_height
        x = seg_x + offset * above_x
        y = seg_y + offset * above_y
        chunks.append(
            f'    <text text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{font_size}" letter-spacing="0.008" '
            f'fill="{PALETTE["segment_text"]}" font-family="{FONT}" '
            f'transform="translate({x:.4f} {y:.4f}) '
            f'rotate({rotation:.4f})">'
            f'{_xml_escape(line)}</text>\n'
        )
    return "".join(chunks)


def render_wide_ribbon(cols_lit_any: set[int]) -> list[str]:
    body: list[str] = []
    r_inner = R1 - WIDE_W / 2
    r_outer = R1 + WIDE_W / 2

    body.append(
        f'  <g transform="translate({TOP_TRANSLATE_X:.4f} '
        f'{TOP_TRANSLATE_Y:.4f})">\n'
    )

    # 1. Alternating-shade segments
    bounds = segment_boundaries()
    for i, (t_lo, t_hi) in enumerate(bounds):
        fill = (PALETTE["segment_light"] if i % 2 == 0
                else PALETTE["segment_dark"])
        body.append(
            f'    <path d="{segment_path(r_inner, r_outer, t_lo, t_hi)}" '
            f'fill="{fill}" stroke="none" />\n'
        )

    # 2. Outline around whole ribbon
    bt1, bt2 = ANGULAR_RANGE
    x1o, y1o = point_at(r_outer, r_outer, bt1)
    x2o, y2o = point_at(r_outer, r_outer, bt2)
    x2i, y2i = point_at(r_inner, r_inner, bt2)
    x1i, y1i = point_at(r_inner, r_inner, bt1)
    body.append(
        f'    <path d="M {x1o:.4f} {y1o:.4f} '
        f'A {r_outer:.4f} {r_outer:.4f} 0 0 1 {x2o:.4f} {y2o:.4f} '
        f'L {x2i:.4f} {y2i:.4f} '
        f'A {r_inner:.4f} {r_inner:.4f} 0 0 0 {x1i:.4f} {y1i:.4f} Z" '
        f'fill="none" stroke="{PALETTE["ribbon_stroke"]}" '
        f'stroke-width="0.012" />\n'
    )

    # 3. Radial place-name labels inside segments
    thetas = column_thetas()
    for i, theta in enumerate(thetas):
        body.append(render_radial_pair(theta, PLACE_LINES[i], 0.085))

    # 4. Group-articulator arcs + labels above the ribbon
    def merge_label(name: str, intersect: set[int]) -> str | None:
        if not intersect:
            return None
        if name == "DORSAL":
            lar = {9, 10, 11} & cols_lit_any
            return "DORSAL · LARYNGEAL" if lar else "DORSAL"
        if name == "LARYNGEAL":
            dor = {7, 8} & cols_lit_any
            return None if dor else "LARYNGEAL"
        return name

    for group_name, group_cols in GROUPS:
        intersect = group_cols & cols_lit_any
        if not intersect:
            continue
        display = merge_label(group_name, intersect)
        if display is None:
            continue
        if group_name == "DORSAL" and ({9, 10, 11} & cols_lit_any):
            merged_cols = intersect | ({9, 10, 11} & cols_lit_any)
        else:
            merged_cols = intersect
        t_a = segment_boundaries()[min(merged_cols)][0] + 0.5
        t_b = segment_boundaries()[max(merged_cols)][1] - 0.5

        for theta in (t_a, t_b):
            xa, ya = point_at(GROUP_ARC_R, GROUP_ARC_R, theta)
            xb, yb = point_at(GROUP_ARC_R + 0.04, GROUP_ARC_R + 0.04, theta)
            body.append(
                f'    <path d="M {xa:.4f} {ya:.4f} L {xb:.4f} {yb:.4f}" '
                f'stroke="{PALETTE["group_arc"]}" stroke-width="0.012" />\n'
            )

        body.append(
            f'    <path d="{_arc_path(GROUP_ARC_R, t_a, t_b)}" '
            f'fill="none" stroke="{PALETTE["group_arc"]}" '
            f'stroke-width="0.012" stroke-linecap="round" />\n'
        )

        arc_id = f"grplbl_{group_name.lower()}"
        body.append(
            f'    <defs><path id="{arc_id}" '
            f'd="{_arc_path(GROUP_LABEL_R, t_a, t_b)}" fill="none" /></defs>\n'
        )
        body.append(
            f'    <text font-size="0.090" letter-spacing="0.030" '
            f'fill="{PALETTE["group_arc"]}" font-family="{FONT}">'
            f'<textPath href="#{arc_id}" startOffset="50%" '
            f'text-anchor="middle">'
            f'{_xml_escape(display)}</textPath></text>\n'
        )

    body.append('  </g>\n')
    return body


# ---------------------------------------------------------------------------
# The 4-language overlay row
# ---------------------------------------------------------------------------

def render_overlay_row(per_lang_counts: dict[str, list[int]]) -> list[str]:
    body: list[str] = []
    body.append(
        f'  <g transform="translate({TOP_TRANSLATE_X:.4f} '
        f'{OVERLAY_TRANSLATE_Y:.4f})">\n'
    )

    # Alternating-shade overlay-row segments (quieter than the place axis)
    bounds = segment_boundaries()
    for i, (t_lo, t_hi) in enumerate(bounds):
        fill = (PALETTE["overlay_lite"] if i % 2 == 0
                else PALETTE["overlay_dark"])
        body.append(
            f'    <path d="{segment_path(OVERLAY_INNER_R, OVERLAY_OUTER_R, t_lo, t_hi)}" '
            f'fill="{fill}" stroke="none" />\n'
        )

    # Thin outline around overlay row
    bt1, bt2 = ANGULAR_RANGE
    x1o, y1o = point_at(OVERLAY_OUTER_R, OVERLAY_OUTER_R, bt1)
    x2o, y2o = point_at(OVERLAY_OUTER_R, OVERLAY_OUTER_R, bt2)
    x2i, y2i = point_at(OVERLAY_INNER_R, OVERLAY_INNER_R, bt2)
    x1i, y1i = point_at(OVERLAY_INNER_R, OVERLAY_INNER_R, bt1)
    body.append(
        f'    <path d="M {x1o:.4f} {y1o:.4f} '
        f'A {OVERLAY_OUTER_R:.4f} {OVERLAY_OUTER_R:.4f} 0 0 1 {x2o:.4f} {y2o:.4f} '
        f'L {x2i:.4f} {y2i:.4f} '
        f'A {OVERLAY_INNER_R:.4f} {OVERLAY_INNER_R:.4f} 0 0 0 {x1i:.4f} {y1i:.4f} Z" '
        f'fill="none" stroke="{PALETTE["narrow_stroke"]}" '
        f'stroke-width="0.010" />\n'
    )

    # Visual codes per language at lit columns, drawn inside-out so larger
    # codes don't obscure smaller ones (dot first, dashed-ring last).
    thetas = column_thetas()
    for slug, label, kind, r_code in LANGUAGES:
        counts = per_lang_counts[slug]
        for col_idx in range(12):
            if counts[col_idx] == 0:
                continue
            cx, cy = point_at(R1, R1, thetas[col_idx])
            body.append(f'    {visual_code(kind, cx, cy, r_code)}\n')

    body.append('  </g>\n')
    return body


# ---------------------------------------------------------------------------
# Legend at the bottom — visual code → language + consonant count
# ---------------------------------------------------------------------------

def render_legend(per_lang_totals: dict[str, int]) -> list[str]:
    """Four legend entries, horizontally distributed across the canvas."""
    body: list[str] = []
    entries = list(LANGUAGES)              # display order: Toda, Sk, Tamil, Kurukh
    n = len(entries)
    # Even horizontal spacing across the canvas; leave outer margins
    inner_left = 0.55
    inner_right = W - 0.55
    span = inner_right - inner_left
    step = span / (n - 1) if n > 1 else 0

    for idx, (slug, label, kind, r_code) in enumerate(entries):
        cx = inner_left + idx * step
        # Visual code centred on cx
        body.append(f'  {visual_code(kind, cx, LEGEND_Y, r_code)}\n')
        # Label below the code
        body.append(
            f'  <text x="{cx:.4f}" y="{LEGEND_Y + 0.22:.4f}" '
            f'text-anchor="middle" font-size="0.090" font-weight="bold" '
            f'fill="{PALETTE["label"]}" font-family="{FONT}">'
            f'{_xml_escape(label)}</text>\n'
        )
        body.append(
            f'  <text x="{cx:.4f}" y="{LEGEND_Y + 0.34:.4f}" '
            f'text-anchor="middle" font-size="0.078" font-style="italic" '
            f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
            f'{per_lang_totals[slug]} consonants</text>\n'
        )
    return body


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_figure() -> str:
    per_lang_counts: dict[str, list[int]] = {}
    per_lang_totals: dict[str, int] = {}
    cols_lit_any: set[int] = set()
    for slug, label, kind, _r in LANGUAGES:
        cfg = json.loads((CONFIGS_DIR / f"scatter_{slug}.json").read_text())
        counts = count_per_column(cfg["scatter"]["matrix"])
        per_lang_counts[slug] = counts
        per_lang_totals[slug] = sum(counts)
        for i, c in enumerate(counts):
            if c > 0:
                cols_lit_any.add(i)

    body: list[str] = []
    body.append(
        f'  <rect x="0" y="0" width="{W:.4f}" height="{H:.4f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    body.extend(render_wide_ribbon(cols_lit_any))
    body.extend(render_overlay_row(per_lang_counts))
    body.extend(render_legend(per_lang_totals))

    body.append(
        f'  <text x="{W/2:.4f}" y="{CAPTION_Y:.4f}" '
        f'text-anchor="middle" font-size="0.090" font-style="italic" '
        f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
        f'Four subcontinental selections from the same vocal instrument.'
        f'</text>\n'
    )

    svg = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W:.4f}in" height="{H:.4f}in" '
        f'viewBox="0 0 {W:.4f} {H:.4f}">\n'
        + "".join(body)
        + '</svg>\n'
    )
    return svg


def main() -> int:
    svg = build_figure()
    out = Path(__file__).resolve().parent / "subcontinental_overlay.from-py.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
