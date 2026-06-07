#!/usr/bin/env python3
"""Figure 7.2 — Language Hotzones Along the Vocal Tract.

Layout (revised, 4.5 in × ~4.0 in):

  - Top section: single ribbon (the same anatomical arc used in the
    standalone atlas), with PLACE-OF-ARTICULATION labels (BIL, LD,
    ID, …, GLO) arranged radially just outside the ribbon's outer
    edge, plus articulator-group headers (LAB / CORONAL / DORSAL /
    LARYNGEAL) on arcs further outside.
  - Continuous dashed vertical guides drop from each lit column's
    ribbon position down through ALL four hotzone panels.
  - Four hotzone panels (English / Arabic / Mandarin / Zulu) stacked
    with 0.1 in vertical gaps.  Each panel: a single horizontal row
    of grayscale hotzone circles (one per lit column, AREA ∝ count),
    with the language name + total consonant count on the left,
    BELOW the row of circles.
  - Caption at the bottom.

Informational, not polemical.  No Sanskrit, no Indic languages.

Filenames are distinct from `vocal_tract_hotzones.py` to avoid
collision with parallel Codex work on the same figure brief.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vocal_tract_schematics import point_at, build_ribbon_path_d  # noqa: E402


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

PANELS = [
    ("english",  "English",   "front-heavy selection"),
    ("arabic",   "Arabic",    "deep-field / throat-side spread"),
    ("mandarin", "Mandarin",  "coronal-palatal concentration"),
    ("zulu",     "Zulu",      "click-mechanism / expanded contact selection"),
]

# 12 anatomical place columns, lip-to-place distance (cm).
DISTANCES = [0.0, 0.5, 1.0, 1.5, 2.5, 3.5, 3.8, 5.5, 9.0, 11.5, 13.5, 17.0]
PLACE_ABBR = [
    "BIL", "LD", "ID", "DEN", "ALV", "PA",
    "RET", "PAL", "VEL", "UV", "PHA", "GLO",
]
# Articulator-family grouping (column indices, 0-based)
GROUPS = [
    ("LAB",       {0, 1}),
    ("CORONAL",   {2, 3, 4, 5, 6}),
    ("DORSAL",    {7, 8}),
    ("LARYNGEAL", {9, 10, 11}),
]

ANGULAR_RANGE = (160.0, 200.0)

# Top-ribbon geometry.  Large radius (r = 4.0) gives a shallow
# almost-horizontal arc at the top of the figure; the 40° angular
# spread keeps the column positions concentrated near the top of
# the canvas; the 0.5-in band is visually prominent.
R1 = R2 = 4.00
RIBBON_W = 0.50

# Canvas
W = 4.5
H = 4.0

# Top-section translate.  X: the angular range (160°–200°) is
# symmetric around 180° so the apex naturally centres when the
# group is translated to (W/2, ·).  Y: tuned so the topmost feature
# (the group-arc apex at y_group = -(R1 + W/2 + 0.32)) sits about
# 0.05 in below the canvas top.
TOP_TRANSLATE_X = W / 2 - (-math.sin(math.radians(180.0)) * R1)
TOP_TRANSLATE_Y = 4.62  # group-arc apex lands at y_screen ≈ 0.05

# Per-panel geometry below the ribbon
PANEL_H = 0.50
PANEL_GAP = 0.10
N_PANELS = len(PANELS)

# Y where the panels start (right under the ribbon).  The visual
# bottom of the ribbon — the lowest point on screen, i.e. the
# highest y_screen — is on the ribbon's INNER edge at the
# endpoint (theta = 160° or 200°), because the inner ring is
# closer to origin and the ribbon slopes downward toward its
# endpoints.  Using (R1 - W/2) for the bottom y prevents the
# panels overlapping the ribbon.
RIBBON_BOTTOM_Y = TOP_TRANSLATE_Y + (
    math.cos(math.radians(160.0)) * (R1 - RIBBON_W / 2)
)
PANELS_TOP_Y = RIBBON_BOTTOM_Y + 0.12  # small margin under ribbon

# Footer caption strip
CAPTION_Y = (
    PANELS_TOP_Y
    + N_PANELS * PANEL_H
    + (N_PANELS - 1) * PANEL_GAP
    + 0.18
)


PALETTE = {
    "background":     "#f4f4f3",
    "ribbon_fill":    "#eceae5",
    "ribbon_stroke":  "#cdccc8",
    "circle":         "#2b2b2d",
    "label":          "#2b2b2d",
    "muted":          "#9a9892",
    "group_arc":      "#8f8d86",
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
    """Even angular spacing across the 12 place columns.

    The standalone atlases use anatomical distance (lip-to-place in
    cm) to drive the angular spread; this figure uses uniform
    spacing instead so the 12 columns lay out evenly across the
    new 40° arc, with no front-of-mouth crowding.
    """
    start, end = ANGULAR_RANGE
    n = len(PLACE_ABBR)
    return [start + i * (end - start) / (n - 1) for i in range(n)]


def count_per_column(matrix: list[list[str]]) -> list[int]:
    counts = [0] * 12
    for row in matrix:
        for col_idx, cell in enumerate(row):
            if cell:
                counts[col_idx] += 1
    return counts


def _arc_path(r: float, t1: float, t2: float) -> str:
    """SVG path-data for a circular arc from t1 to t2 at radius r."""
    x1, y1 = point_at(r, r, t1)
    x2, y2 = point_at(r, r, t2)
    large = 1 if abs(t2 - t1) > 180 else 0
    sweep = 1 if t2 > t1 else 0
    return (
        f"M {x1:.4f} {y1:.4f} "
        f"A {r:.4f} {r:.4f} 0 {large} {sweep} {x2:.4f} {y2:.4f}"
    )


def render_top_ribbon(cols_lit_any: set[int]) -> list[str]:
    """Render the top ribbon + radial place labels + group arcs.

    Only the columns lit by AT LEAST ONE language receive labels
    and dashed guides; the remaining columns are ignored visually.
    """
    body: list[str] = []
    thetas = column_thetas()

    body.append(
        f'  <g transform="translate({TOP_TRANSLATE_X:.4f} '
        f'{TOP_TRANSLATE_Y:.4f})">\n'
    )

    # Ribbon body
    t1, t2 = ANGULAR_RANGE
    ribbon_d, _ = build_ribbon_path_d(R1, R2, RIBBON_W, t1, t2)
    body.append(
        f'    <path d="{ribbon_d}" '
        f'fill="{PALETTE["ribbon_fill"]}" '
        f'stroke="{PALETTE["ribbon_stroke"]}" stroke-width="0.014" />\n'
    )

    # Radial place labels: horizontal text at r = r_outer + 0.16,
    # positioned at each lit column's theta.  Plain horizontal text
    # (not rotated) keeps the labels readable across the arc.
    r_label = R1 + RIBBON_W / 2 + 0.16
    for col_idx in cols_lit_any:
        theta = thetas[col_idx]
        x, y = point_at(r_label, r_label, theta)
        body.append(
            f'    <text x="{x:.4f}" y="{y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="0.085" letter-spacing="0.010" '
            f'fill="{PALETTE["label"]}" '
            f'font-family="{FONT}">'
            f'{_xml_escape(PLACE_ABBR[col_idx])}</text>\n'
        )

    # Articulator-group arcs + labels, positioned just outside the
    # place-label ring.
    r_group_arc = R1 + RIBBON_W / 2 + 0.32

    def merge_labels(group_name: str, intersect: set[int]) -> str | None:
        if not intersect:
            return None
        # Special case: collapse DORSAL · LARYNGEAL when both present.
        if group_name == "DORSAL":
            laryngeal_lit = {9, 10, 11} & cols_lit_any
            return "DORSAL · LARYNGEAL" if laryngeal_lit else "DORSAL"
        if group_name == "LARYNGEAL":
            dorsal_lit = {7, 8} & cols_lit_any
            return None if dorsal_lit else "LARYNGEAL"
        return group_name

    for group_name, group_cols in GROUPS:
        intersect = group_cols & cols_lit_any
        if not intersect:
            continue
        display = merge_labels(group_name, intersect)
        if display is None:
            continue
        if group_name == "DORSAL" and ({9, 10, 11} & cols_lit_any):
            merged = intersect | ({9, 10, 11} & cols_lit_any)
            theta_a = thetas[min(merged)]
            theta_b = thetas[max(merged)]
        else:
            theta_a = thetas[min(intersect)]
            theta_b = thetas[max(intersect)]
        # Small breathing room on each end
        theta_a -= 1.0
        theta_b += 1.0
        # Tick marks at each end of the arc
        for theta in (theta_a, theta_b):
            xa, ya = point_at(r_group_arc, r_group_arc, theta)
            xb, yb = point_at(r_group_arc + 0.03, r_group_arc + 0.03, theta)
            body.append(
                f'    <path d="M {xa:.4f} {ya:.4f} L {xb:.4f} {yb:.4f}" '
                f'stroke="{PALETTE["group_arc"]}" stroke-width="0.010" />\n'
            )
        # The arc itself
        body.append(
            f'    <path d="{_arc_path(r_group_arc, theta_a, theta_b)}" '
            f'fill="none" stroke="{PALETTE["group_arc"]}" '
            f'stroke-width="0.010" stroke-linecap="round" />\n'
        )
        # Group label along the arc (textPath at a slightly larger r)
        arc_id = f"grplbl_{group_name.lower()}"
        body.append(
            f'    <defs><path id="{arc_id}" '
            f'd="{_arc_path(r_group_arc + 0.07, theta_a, theta_b)}" '
            f'fill="none" /></defs>\n'
        )
        body.append(
            f'    <text font-size="0.078" letter-spacing="0.025" '
            f'fill="{PALETTE["group_arc"]}" font-family="{FONT}">'
            f'<textPath href="#{arc_id}" startOffset="50%" '
            f'text-anchor="middle">'
            f'{_xml_escape(display)}</textPath></text>\n'
        )

    body.append('  </g>\n')
    return body


def render_guides(cols_lit_any: set[int]) -> list[str]:
    """Continuous vertical dashed lines from below the ribbon down
    through all four panels."""
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
        # Ribbon-inner-edge x at this column theta becomes the
        # guide's x throughout the figure.
        x_local, y_local = point_at(r_inner, r_inner, theta)
        x_screen = TOP_TRANSLATE_X + x_local
        y_top = TOP_TRANSLATE_Y + y_local + 0.04  # just below the ribbon
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
    # Row of circles centered around y_row
    y_row = panel_y_top + 0.18
    # Language name below the row of circles, left-aligned
    y_name = panel_y_top + 0.42

    # Circles
    for col_idx in range(12):
        cnt = counts[col_idx]
        if cnt == 0:
            continue
        r_circle = radius_scale * math.sqrt(cnt)
        theta = thetas[col_idx]
        # Use the same x as the dashed guides, so circles land on
        # the dashed columns.
        x_local, _ = point_at(r_inner, r_inner, theta)
        x_screen = TOP_TRANSLATE_X + x_local
        body.append(
            f'  <circle cx="{x_screen:.4f}" cy="{y_row:.4f}" '
            f'r="{r_circle:.4f}" fill="{PALETTE["circle"]}" '
            f'opacity="0.80" />\n'
        )

    # Language name + count (left-aligned, below the row of circles)
    body.append(
        f'  <text x="0.30" y="{y_name:.4f}" '
        f'text-anchor="start" font-size="0.105" font-weight="bold" '
        f'fill="{PALETTE["label"]}" font-family="{FONT}">'
        f'{_xml_escape(name)} · {n_total} consonants</text>\n'
    )
    body.append(
        f'  <text x="0.30" y="{y_name + 0.14:.4f}" '
        f'text-anchor="start" font-size="0.085" font-style="italic" '
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

    r_max_inches = 0.16
    radius_scale = (
        r_max_inches / math.sqrt(global_max) if global_max > 0 else 0.0
    )

    body: list[str] = []
    body.append(
        f'  <rect x="0" y="0" width="{W:.4f}" height="{H:.4f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    # Top ribbon + radial labels
    body.extend(render_top_ribbon(cols_lit_any))

    # Continuous dashed vertical guides
    body.extend(render_guides(cols_lit_any))

    # The four hotzone panels (circles on top of the dashed guides)
    for i, (name, descr, counts, n_total) in enumerate(panel_data):
        body.extend(render_panel(i, name, descr, counts, n_total, radius_scale))

    # Caption footer
    body.append(
        f'  <text x="{W/2:.4f}" y="{CAPTION_Y:.4f}" '
        f'text-anchor="middle" font-size="0.085" font-style="italic" '
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
