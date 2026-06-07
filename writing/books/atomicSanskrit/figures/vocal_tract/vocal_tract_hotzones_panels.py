#!/usr/bin/env python3
"""Figure 7.2 — Language Hotzones Along the Vocal Tract.

Top section: ONE WIDE ribbon (r=5, W=0.50, arc 155°-205°) carrying
the labelled place-axis: 12 alternating-gray segments, full radial
place names inside each segment, articulator-group arcs above
(LAB · CORONAL · DORSAL · LARYNGEAL).

Below: EACH LANGUAGE GETS ITS OWN NARROW RIBBON of the same
curvature — r=5, W=0.10, arc 155°-205° — stacked vertically with
its own TRANSLATE_Y.  Each language ribbon carries:
  - 12 alternating-gray segments (a quieter version of the top
    ribbon's segments, so the column-axis stays legible per
    language)
  - hotzone circles ON the band at the column centres, AREA ∝
    count for that language
  - language name + total consonant count CENTERED below the
    ribbon

Twelve dashed vertical guides drop from the inner edge of the top
ribbon all the way through the four language ribbons.  Because
every ribbon shares the same r and the same arc, the column x-
positions are identical across all five ribbons — the guides drop
straight down without any bending.

The angular range tightened from 60° to 50° to make room for four
extra ribbons in the vertical budget.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vocal_tract_schematics import point_at  # noqa: E402


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

PANELS = [
    ("english",  "English",   "front-heavy selection"),
    ("arabic",   "Arabic",    "deep-field / throat-side spread"),
    ("mandarin", "Mandarin",  "coronal-palatal concentration"),
    ("zulu",     "Zulu",      "click-mechanism / expanded contact selection"),
]

PLACE_LINES = [
    ("bi-",      "labial"),
    ("labio-",   "dental"),
    ("inter-",   "dental"),
    ("dental",   ""),
    ("alveo-",   "lar"),
    ("post-",    "alv."),
    ("retro-",   "flex"),
    ("palatal",  ""),
    ("velar",    ""),
    ("uvular",   ""),
    ("phar-",    "yngeal"),
    ("glottal",  ""),
]

GROUPS = [
    ("LAB",       {0, 1}),
    ("CORONAL",   {2, 3, 4, 5, 6}),
    ("DORSAL",    {7, 8}),
    ("LARYNGEAL", {9, 10, 11}),
]

# Angle tightened from 60° → 50° to compress the vertical budget so
# the wide ribbon + four language ribbons fit comfortably.
ANGULAR_RANGE = (155.0, 205.0)

# Shared radius across the wide top ribbon and the four narrow
# language ribbons — keeps column x-positions identical so the
# dashed guides drop straight down through every ribbon.
R1 = R2 = 5.00

WIDE_W   = 0.50   # wide top ribbon (carries the labelled place-axis)
NARROW_W = 0.25   # per-language ribbons (was 0.10)

# Canvas trimmed laterally — the chart's actual horizontal footprint
# is ~4.5 in, so 5.0 in width leaves ~0.13 in of breathing room each
# side without burning the previous 1.0 in of dead margin.
W = 5.0
H = 5.25

# Top-section translate.  Wide ribbon's outer-apex sits near the
# top of the canvas; group-arc apex lands at y_screen ≈ 0.10.
TOP_TRANSLATE_X = W / 2 - (-math.sin(math.radians(180.0)) * R1)
GROUP_ARC_R     = R1 + WIDE_W / 2 + 0.42     # = 5.67
GROUP_LABEL_R   = R1 + WIDE_W / 2 + 0.52     # = 5.77
# Top margin raised 0.10 → 0.15 so the group labels don't kiss the
# canvas edge once horizontal margins are trimmed.
TOP_TRANSLATE_Y = 0.15 + GROUP_LABEL_R       # = 5.92


# y_screen at the wide ribbon's inner endpoint (where panels begin)
WIDE_INNER_R           = R1 - WIDE_W / 2     # 4.75
WIDE_RIBBON_BOTTOM_Y   = TOP_TRANSLATE_Y + (
    math.cos(math.radians(ANGULAR_RANGE[0])) * WIDE_INNER_R
)
NARROW_INNER_R         = R1 - NARROW_W / 2   # 4.95
NARROW_OUTER_R         = R1 + NARROW_W / 2   # 5.05

# Narrow-ribbon vertical extent in screen coords:
#   outer apex y_screen      = TRANSLATE_Y - NARROW_OUTER_R
#   inner endpoint y_screen  = TRANSLATE_Y + cos(t_start) * NARROW_INNER_R
# extent = inner − outer = NARROW_OUTER_R + cos(t_start)*NARROW_INNER_R
# At t_start = 155°, cos is negative, so this collapses to ~0.565.
NARROW_RIBBON_EXT = NARROW_OUTER_R + (
    math.cos(math.radians(ANGULAR_RANGE[0])) * NARROW_INNER_R
)

LABEL_FONT_SIZE  = 0.090
# Labels now sit INSIDE the curve's bowl rather than below the band.
# Concretely: label centre = inner endpoint y_screen − LABEL_INSIDE_OFFSET.
# Net effect vs the previous "label below the band" placement is +0.25 in
# upward shift (was inner + 0.13; now inner − 0.12).
LABEL_INSIDE_OFFSET = 0.27
LANG_TOP_GAP        = 0.10
LANG_INTER_GAP      = 0.10

# Pre-compute TRANSLATE_Y for each language ribbon.  Each ribbon
# starts a small gap below the previous ribbon's inner endpoint;
# the label lives inside the bowl, so the gap doesn't carry label
# height anymore.
LANG_TRANSLATE_Y: list[float] = []
prev_inner_endpoint_y = WIDE_RIBBON_BOTTOM_Y
for _i in range(len(PANELS)):
    gap = LANG_TOP_GAP if _i == 0 else LANG_INTER_GAP
    outer_apex_y = prev_inner_endpoint_y + gap
    translate_y = outer_apex_y + NARROW_OUTER_R
    LANG_TRANSLATE_Y.append(translate_y)
    prev_inner_endpoint_y = (
        translate_y + math.cos(math.radians(ANGULAR_RANGE[0])) * NARROW_INNER_R
    )

CAPTION_Y = prev_inner_endpoint_y + 0.18

N_PANELS = len(PANELS)


PALETTE = {
    "background":      "#f4f4f3",
    "segment_light":   "#ece9e2",
    "segment_dark":    "#d4d0c5",
    "segment_lt_lite": "#f1efea",   # softer light shade for narrow ribbons
    "segment_lt_dark": "#dedbd4",
    "ribbon_stroke":   "#9a9892",
    "narrow_stroke":   "#b8b6b0",
    "segment_text":    "#3a3a3c",
    "group_arc":       "#8f8d86",
    "circle":          "#2b2b2d",
    "label":           "#2b2b2d",
    "muted":           "#8f8d86",
    "guide_dash":      "#cdccc8",
}

FONT = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"


# ---------------------------------------------------------------------------
# Geometry helpers
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
# Wide top ribbon
# ---------------------------------------------------------------------------

def render_radial_pair(theta: float, lines: tuple[str, str],
                       font_size: float) -> str:
    """Two-line radial label centred on the wide-ribbon segment.

    Lines stack TANGENTIALLY (perpendicular to the radial reading
    direction).  Left half is flipped 180° for symmetric head-tilt.
    """
    flip = theta < 180.0
    rotation = theta - 270.0 + (180.0 if flip else 0.0)

    R_rad = math.radians(rotation)
    above_x = math.sin(R_rad)
    above_y = -math.cos(R_rad)

    actual_lines = [line for line in lines if line]
    n = len(actual_lines)
    line_height = font_size * 1.10

    chunks: list[str] = []
    seg_x, seg_y = point_at(R1, R1, theta)

    for i, line in enumerate(actual_lines):
        above_offset = ((n - 1) / 2 - i) * line_height
        x = seg_x + above_offset * above_x
        y = seg_y + above_offset * above_y
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

    bounds = segment_boundaries()
    for i, (t_lo, t_hi) in enumerate(bounds):
        fill = (
            PALETTE["segment_light"] if i % 2 == 0
            else PALETTE["segment_dark"]
        )
        d = segment_path(r_inner, r_outer, t_lo, t_hi)
        body.append(
            f'    <path d="{d}" fill="{fill}" stroke="none" />\n'
        )

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

    thetas = column_thetas()
    label_font_size = 0.095
    for i, theta in enumerate(thetas):
        body.append(render_radial_pair(theta, PLACE_LINES[i], label_font_size))

    # Group-articulator arcs
    def merge_label(name: str, intersect: set[int]) -> str | None:
        if not intersect:
            return None
        if name == "DORSAL":
            laryngeal_lit = {9, 10, 11} & cols_lit_any
            return "DORSAL · LARYNGEAL" if laryngeal_lit else "DORSAL"
        if name == "LARYNGEAL":
            dorsal_lit = {7, 8} & cols_lit_any
            return None if dorsal_lit else "LARYNGEAL"
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
        t_a = segment_boundaries()[min(merged_cols)][0]
        t_b = segment_boundaries()[max(merged_cols)][1]
        t_a += 0.5
        t_b -= 0.5

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
            f'd="{_arc_path(GROUP_LABEL_R, t_a, t_b)}" '
            f'fill="none" /></defs>\n'
        )
        body.append(
            f'    <text font-size="0.095" letter-spacing="0.030" '
            f'fill="{PALETTE["group_arc"]}" font-family="{FONT}">'
            f'<textPath href="#{arc_id}" startOffset="50%" '
            f'text-anchor="middle">'
            f'{_xml_escape(display)}</textPath></text>\n'
        )

    body.append('  </g>\n')
    return body


# ---------------------------------------------------------------------------
# Narrow per-language ribbons
# ---------------------------------------------------------------------------

def render_language_ribbon(
    panel_idx: int,
    name: str,
    counts: list[int],
    n_total: int,
    radius_scale: float,
) -> list[str]:
    body: list[str] = []
    translate_y = LANG_TRANSLATE_Y[panel_idx]
    r_inner = NARROW_INNER_R
    r_outer = NARROW_OUTER_R

    body.append(
        f'  <g transform="translate({TOP_TRANSLATE_X:.4f} '
        f'{translate_y:.4f})">\n'
    )

    # Alternating-shade narrow segments — quieter palette so the
    # circles read against them without competing.
    bounds = segment_boundaries()
    for i, (t_lo, t_hi) in enumerate(bounds):
        fill = (
            PALETTE["segment_lt_lite"] if i % 2 == 0
            else PALETTE["segment_lt_dark"]
        )
        d = segment_path(r_inner, r_outer, t_lo, t_hi)
        body.append(
            f'    <path d="{d}" fill="{fill}" stroke="none" />\n'
        )

    # Thin outline around the narrow ribbon
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
        f'fill="none" stroke="{PALETTE["narrow_stroke"]}" '
        f'stroke-width="0.008" />\n'
    )

    # Hotzone circles on the band centreline (r = R1).
    thetas = column_thetas()
    for col_idx in range(12):
        cnt = counts[col_idx]
        if cnt == 0:
            continue
        r_circle = radius_scale * math.sqrt(cnt)
        theta = thetas[col_idx]
        cx, cy = point_at(R1, R1, theta)
        body.append(
            f'    <circle cx="{cx:.4f}" cy="{cy:.4f}" '
            f'r="{r_circle:.4f}" fill="{PALETTE["circle"]}" '
            f'opacity="0.82" />\n'
        )

    body.append('  </g>\n')

    # Language label centred INSIDE the curve's bowl, sitting
    # LABEL_INSIDE_OFFSET above the ribbon's inner endpoint
    # (i.e. 0.25 in higher than the previous below-the-band
    # placement).  At this y_screen, the curve's inner edge has
    # opened wide enough that "Language · N consonants" fits
    # comfortably between the two endpoints of the arc.
    inner_endpoint_y_screen = translate_y + (
        math.cos(math.radians(ANGULAR_RANGE[0])) * r_inner
    )
    label_y = inner_endpoint_y_screen - LABEL_INSIDE_OFFSET
    body.append(
        f'  <text x="{W/2:.4f}" y="{label_y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{LABEL_FONT_SIZE}" font-weight="bold" '
        f'fill="{PALETTE["label"]}" font-family="{FONT}">'
        f'{_xml_escape(name)} · {n_total} consonants</text>\n'
    )

    return body


# ---------------------------------------------------------------------------
# Dashed guides
# ---------------------------------------------------------------------------

def render_guides(cols_lit_any: set[int]) -> list[str]:
    body: list[str] = []
    thetas = column_thetas()

    # Guide top: just below the wide ribbon's inner edge.
    # Guide bottom: just above the last language ribbon's outer apex.
    last_outer_apex_y = LANG_TRANSLATE_Y[-1] - NARROW_OUTER_R

    for col_idx in cols_lit_any:
        theta = thetas[col_idx]
        x_local, y_local_wide = point_at(WIDE_INNER_R, WIDE_INNER_R, theta)
        x_screen = TOP_TRANSLATE_X + x_local
        y_top = TOP_TRANSLATE_Y + y_local_wide + 0.05
        # Bottom guide: just above the last language ribbon's outer apex
        # at this column (each language ribbon's outer apex at this
        # column has y_local_narrow_outer; we extend the guide so it
        # threads through every language ribbon).
        y_bot = LANG_TRANSLATE_Y[-1] + math.cos(math.radians(theta)) * NARROW_OUTER_R
        # Pull bottom a hair further down so the guide ends inside the
        # last ribbon's band rather than just kissing its outer edge.
        y_bot += 0.04
        body.append(
            f'  <line x1="{x_screen:.4f}" y1="{y_top:.4f}" '
            f'x2="{x_screen:.4f}" y2="{y_bot:.4f}" '
            f'stroke="{PALETTE["guide_dash"]}" stroke-width="0.005" '
            f'stroke-dasharray="0.04 0.04" />\n'
        )
    return body


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_figure() -> str:
    cfg_dir = Path(__file__).resolve().parent / "configs"

    panel_data: list[tuple[str, str, list[int], int]] = []
    global_max = 0
    cols_lit_any: set[int] = set()
    for slug, name, descr in PANELS:
        cfg = json.loads((cfg_dir / f"scatter_{slug}.json").read_text())
        counts = count_per_column(cfg["scatter"]["matrix"])
        n_total = sum(counts)
        panel_data.append((name, descr, counts, n_total))
        for i, c in enumerate(counts):
            if c > 0:
                cols_lit_any.add(i)
            if c > global_max:
                global_max = c

    # Cap the per-circle radius so circles don't overflow too far
    # past the narrow-ribbon band edges.
    r_max_inches = 0.13
    radius_scale = (
        r_max_inches / math.sqrt(global_max) if global_max > 0 else 0.0
    )

    body: list[str] = []
    body.append(
        f'  <rect x="0" y="0" width="{W:.4f}" height="{H:.4f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    body.extend(render_wide_ribbon(cols_lit_any))
    body.extend(render_guides(cols_lit_any))

    for i, (name, _descr, counts, n_total) in enumerate(panel_data):
        body.extend(render_language_ribbon(i, name, counts, n_total, radius_scale))

    body.append(
        f'  <text x="{W/2:.4f}" y="{CAPTION_Y:.4f}" '
        f'text-anchor="middle" font-size="0.095" font-style="italic" '
        f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
        f'One shared place-axis (wide ribbon); each language carries '
        f'its hotzones on its own narrow ribbon below.</text>\n'
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
    out = (
        Path(__file__).resolve().parent.parent / "build" / "vocal_tract"
        / "hotzones_panels.svg"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
