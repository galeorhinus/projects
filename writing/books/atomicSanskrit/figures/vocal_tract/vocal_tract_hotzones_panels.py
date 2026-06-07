#!/usr/bin/env python3
"""Figure 7.2 — Language Hotzones Along the Vocal Tract.

Top section: a single wide ribbon (r = 5.0, w = 0.5, arc 150°-210°)
divided into 12 ALTERNATING-GRAY SEGMENTS, one per place column.
Inside each segment, the full place name is rendered as a 2-LINE
radial label.  Labels on the left half (theta < 180°) are flipped
180° so they read in the same head-tilt direction as the right half.
Above the ribbon, four ARTICULATOR-GROUP ARCS (LAB · CORONAL ·
DORSAL · LARYNGEAL) curve along the chart top.

Below: continuous dashed vertical guides drop from each segment
down through four hotzone panels (English / Arabic / Mandarin /
Zulu) stacked with 0.1 in gaps.  Each panel: a row of grayscale
hotzone circles, AREA ∝ count; language name + total count on the
LEFT, BELOW the row of circles.

Informational, not polemical.  No Sanskrit, no Indic languages.

Filenames distinct from `vocal_tract_hotzones.py` to avoid collision
with parallel Codex work.
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

# 12 place columns rendered as 2-line radial labels.  Tuple format:
# (line1, line2).  Short single-word names get a small second line
# of empty string so the layout stays consistent; using ("name", "")
# keeps all labels at the same radial extent.
PLACE_LINES = [
    ("bi-",      "labial"),     # bilabial
    ("labio-",   "dental"),     # labio-dental
    ("inter-",   "dental"),     # interdental
    ("dental",   ""),           # dental
    ("alveo-",   "lar"),        # alveolar
    ("post-",    "alv."),       # post-alveolar
    ("retro-",   "flex"),       # retroflex
    ("palatal",  ""),           # palatal
    ("velar",    ""),           # velar
    ("uvular",   ""),           # uvular
    ("pharyn-",  "geal"),       # pharyngeal
    ("glottal",  ""),           # glottal
]

# Articulator-family groupings shown as labelled arcs above the
# ribbon (the "circumferential" labels the user asked to bring back).
GROUPS = [
    ("LAB",       {0, 1}),
    ("CORONAL",   {2, 3, 4, 5, 6}),
    ("DORSAL",    {7, 8}),
    ("LARYNGEAL", {9, 10, 11}),
]

ANGULAR_RANGE = (150.0, 210.0)

# Top-ribbon geometry.
R1 = R2 = 5.00
RIBBON_W = 0.50

# Canvas — sized to fit the larger ribbon + group arcs + 4 panels +
# caption without cropping at the top.
W = 6.0
H = 5.0

# Top-section translate.  X: angular range symmetric around 180°
# so the apex centres naturally on (W/2, ·).  Y: tuned so the
# group-arc apex (y_group = -(R1 + W/2 + 0.30)) sits about 0.10 in
# below the canvas top.
TOP_TRANSLATE_X = W / 2 - (-math.sin(math.radians(180.0)) * R1)
GROUP_ARC_R     = R1 + RIBBON_W / 2 + 0.30   # = 5.55
GROUP_LABEL_R   = R1 + RIBBON_W / 2 + 0.40   # = 5.65
TOP_TRANSLATE_Y = 0.10 + GROUP_LABEL_R       # group-label apex at y_screen ≈ 0.10

# Per-panel layout
PANEL_H = 0.50
PANEL_GAP = 0.10
N_PANELS = len(PANELS)

RIBBON_BOTTOM_Y = TOP_TRANSLATE_Y + (
    math.cos(math.radians(ANGULAR_RANGE[0])) * (R1 - RIBBON_W / 2)
)
PANELS_TOP_Y = RIBBON_BOTTOM_Y + 0.18

CAPTION_Y = (
    PANELS_TOP_Y
    + N_PANELS * PANEL_H
    + (N_PANELS - 1) * PANEL_GAP
    + 0.22
)


PALETTE = {
    "background":     "#f4f4f3",
    "segment_light":  "#ece9e2",
    "segment_dark":   "#d4d0c5",
    "ribbon_stroke":  "#9a9892",
    "segment_text":   "#3a3a3c",
    "group_arc":      "#8f8d86",
    "circle":         "#2b2b2d",
    "label":          "#2b2b2d",
    "muted":          "#8f8d86",
    "guide_dash":     "#cdccc8",
}

FONT = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def column_thetas() -> list[float]:
    """Each column at the centre of its segment (even angular spacing)."""
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


def render_radial_pair(
    theta: float,
    lines: tuple[str, str],
    font_size: float,
) -> str:
    """Render a 1- or 2-line radial label centred on the segment.

    Convention:
      - Right half (theta ≥ 180°): rotation = theta - 270°, so text
        reads OUTWARD from the chart's centre.  Line 1 (first read)
        is INNER, line 2 (second read) is OUTER.
      - Left half (theta < 180°): the rotation is flipped by 180°
        (rotation = theta - 90°), so the text reads in the opposite
        direction.  Symmetric head-tilt across the two halves.
        Line 1 (first read) is OUTER, line 2 is INNER.
    """
    flip = theta < 180.0
    rotation = theta - 270.0 + (180.0 if flip else 0.0)

    out_x = -math.sin(math.radians(theta))
    out_y = math.cos(math.radians(theta))

    actual_lines = [line for line in lines if line]
    n = len(actual_lines)
    line_height = font_size * 1.18

    chunks: list[str] = []
    for i, line in enumerate(actual_lines):
        # Offset along the outward radial axis.  Sign depends on
        # reading direction so the first-read line sits at the side
        # the reader's eye lands first.
        if flip:
            # Inward reading: line 0 at OUTER offset
            offset = ((n - 1) / 2 - i) * line_height
        else:
            # Outward reading: line 0 at INNER offset
            offset = (i - (n - 1) / 2) * line_height
        # Apply along the outward unit vector (out_x, out_y).
        x_local, _ = point_at(R1, R1, theta)
        _, y_local = point_at(R1, R1, theta)
        x = x_local + offset * out_x
        y = y_local + offset * out_y
        chunks.append(
            f'    <text text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{font_size}" letter-spacing="0.008" '
            f'fill="{PALETTE["segment_text"]}" font-family="{FONT}" '
            f'transform="translate({x:.4f} {y:.4f}) '
            f'rotate({rotation:.4f})">'
            f'{_xml_escape(line)}</text>\n'
        )
    return "".join(chunks)


def render_top_ribbon(cols_lit_any: set[int]) -> list[str]:
    body: list[str] = []
    r_inner = R1 - RIBBON_W / 2
    r_outer = R1 + RIBBON_W / 2

    body.append(
        f'  <g transform="translate({TOP_TRANSLATE_X:.4f} '
        f'{TOP_TRANSLATE_Y:.4f})">\n'
    )

    # ---- 1. Alternating-shade segment fills ----
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

    # Single thin outline around the whole ribbon
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

    # ---- 2. Radial 2-line labels inside each segment ----
    thetas = column_thetas()
    label_font_size = 0.105  # slightly larger than the previous 0.085
    for i, theta in enumerate(thetas):
        body.append(render_radial_pair(theta, PLACE_LINES[i], label_font_size))

    # ---- 3. Group-articulator arcs + labels above the ribbon ----
    bounds_for_group = column_thetas()  # column theta = segment centre

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
        # Compute the angular extent of the group based on segment
        # boundaries (not column centres) so the arc covers all
        # segments in the group.
        if group_name == "DORSAL" and ({9, 10, 11} & cols_lit_any):
            merged_cols = intersect | ({9, 10, 11} & cols_lit_any)
        else:
            merged_cols = intersect
        t_a = segment_boundaries()[min(merged_cols)][0]
        t_b = segment_boundaries()[max(merged_cols)][1]
        # Small breathing room
        t_a += 0.5
        t_b -= 0.5

        # End-tick marks
        for theta in (t_a, t_b):
            xa, ya = point_at(GROUP_ARC_R, GROUP_ARC_R, theta)
            xb, yb = point_at(GROUP_ARC_R + 0.04, GROUP_ARC_R + 0.04, theta)
            body.append(
                f'    <path d="M {xa:.4f} {ya:.4f} L {xb:.4f} {yb:.4f}" '
                f'stroke="{PALETTE["group_arc"]}" stroke-width="0.012" />\n'
            )

        # Arc body
        body.append(
            f'    <path d="{_arc_path(GROUP_ARC_R, t_a, t_b)}" '
            f'fill="none" stroke="{PALETTE["group_arc"]}" '
            f'stroke-width="0.012" stroke-linecap="round" />\n'
        )

        # Text along arc (slightly larger label radius)
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


def render_guides(cols_lit_any: set[int]) -> list[str]:
    body: list[str] = []
    thetas = column_thetas()
    r_inner = R1 - RIBBON_W / 2

    last_panel_bottom = (
        PANELS_TOP_Y
        + N_PANELS * PANEL_H
        + (N_PANELS - 1) * PANEL_GAP
    )

    for col_idx in cols_lit_any:
        theta = thetas[col_idx]
        x_local, y_local = point_at(r_inner, r_inner, theta)
        x_screen = TOP_TRANSLATE_X + x_local
        y_top = TOP_TRANSLATE_Y + y_local + 0.06
        body.append(
            f'  <line x1="{x_screen:.4f}" y1="{y_top:.4f}" '
            f'x2="{x_screen:.4f}" y2="{last_panel_bottom - 0.04:.4f}" '
            f'stroke="{PALETTE["guide_dash"]}" stroke-width="0.005" '
            f'stroke-dasharray="0.04 0.04" />\n'
        )
    return body


def render_panel(
    panel_idx: int,
    name: str,
    descr: str,
    counts: list[int],
    n_total: int,
    radius_scale: float,
) -> list[str]:
    body: list[str] = []
    thetas = column_thetas()
    r_inner = R1 - RIBBON_W / 2

    panel_y_top = PANELS_TOP_Y + panel_idx * (PANEL_H + PANEL_GAP)
    y_row = panel_y_top + 0.18
    y_name = panel_y_top + 0.42

    for col_idx in range(12):
        cnt = counts[col_idx]
        if cnt == 0:
            continue
        r_circle = radius_scale * math.sqrt(cnt)
        theta = thetas[col_idx]
        x_local, _ = point_at(r_inner, r_inner, theta)
        x_screen = TOP_TRANSLATE_X + x_local
        body.append(
            f'  <circle cx="{x_screen:.4f}" cy="{y_row:.4f}" '
            f'r="{r_circle:.4f}" fill="{PALETTE["circle"]}" '
            f'opacity="0.80" />\n'
        )

    body.append(
        f'  <text x="0.35" y="{y_name:.4f}" '
        f'text-anchor="start" font-size="0.115" font-weight="bold" '
        f'fill="{PALETTE["label"]}" font-family="{FONT}">'
        f'{_xml_escape(name)} · {n_total} consonants</text>\n'
    )
    body.append(
        f'  <text x="0.35" y="{y_name + 0.15:.4f}" '
        f'text-anchor="start" font-size="0.095" font-style="italic" '
        f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
        f'{_xml_escape(descr)}</text>\n'
    )

    return body


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

    r_max_inches = 0.18
    radius_scale = (
        r_max_inches / math.sqrt(global_max) if global_max > 0 else 0.0
    )

    body: list[str] = []
    body.append(
        f'  <rect x="0" y="0" width="{W:.4f}" height="{H:.4f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    body.extend(render_top_ribbon(cols_lit_any))
    body.extend(render_guides(cols_lit_any))

    for i, (name, descr, counts, n_total) in enumerate(panel_data):
        body.extend(render_panel(i, name, descr, counts, n_total, radius_scale))

    body.append(
        f'  <text x="{W/2:.4f}" y="{CAPTION_Y:.4f}" '
        f'text-anchor="middle" font-size="0.095" font-style="italic" '
        f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
        f'Languages select different hotzones from the same vocal '
        f'instrument.</text>\n'
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
