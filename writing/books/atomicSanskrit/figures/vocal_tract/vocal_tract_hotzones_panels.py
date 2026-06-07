#!/usr/bin/env python3
"""Figure 7.2 — Language Hotzones Along the Vocal Tract.

Top section: a single ribbon with r = 5.0, w = 0.5, arc 150°–210°
divided into 12 alternating-gray SEGMENTS, one per place column.
The full place name (bilabial, labio-dent., …, glottal) sits INSIDE
each segment, oriented radially (text reads outward from origin).
Above the ribbon is reserved space so nothing clips at the canvas top.

Below: continuous dashed vertical guides drop from each segment
down through four hotzone panels (English / Arabic / Mandarin /
Zulu) stacked with 0.1 in gaps.  Each panel: a row of grayscale
hotzone circles, AREA ∝ count.  Language name + total consonant
count sits on the LEFT, BELOW the row of circles.

The figure is informational, not polemical.  No Sanskrit, no Indic
languages.

Filenames are distinct from `vocal_tract_hotzones.py` to avoid
collision with parallel Codex work on the same brief.
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

# 12 place columns — full names rendered radially inside each
# alternating-gray segment.  Two longer compounds shortened so they
# fit the 0.5-in radial band cleanly.
PLACE_FULL = [
    "bilabial",
    "labio-dent.",
    "interdental",
    "dental",
    "alveolar",
    "post-alv.",
    "retroflex",
    "palatal",
    "velar",
    "uvular",
    "pharyngeal",
    "glottal",
]

# Top-ribbon geometry.  Large radius + 60° arc gives a very
# shallow band across the top of the figure; even angular spacing
# (see column_thetas) gives uniform horizontal step between columns.
R1 = R2 = 5.00
RIBBON_W = 0.50
ANGULAR_RANGE = (150.0, 210.0)

# Canvas — widened both directions so the larger ribbon fits without
# horizontal cropping and so the top-section has breathing room.
W = 6.0
H = 5.0

# Top-section translate.  X: the angular range is symmetric around
# 180°, so the apex naturally centres when the group is translated
# to (W/2, ·).  Y: tuned so the ribbon-outer apex
# (y_group = -(R1 + W/2)) sits about 0.15 in below the canvas top.
TOP_TRANSLATE_X = W / 2 - (-math.sin(math.radians(180.0)) * R1)
TOP_TRANSLATE_Y = 0.15 + (R1 + RIBBON_W / 2)

# Per-panel layout (unchanged from previous version)
PANEL_H = 0.50
PANEL_GAP = 0.10
N_PANELS = len(PANELS)

# Y where panels start — just under the ribbon's lowest visible
# point (inner edge at the endpoint).
RIBBON_BOTTOM_Y = TOP_TRANSLATE_Y + (
    math.cos(math.radians(ANGULAR_RANGE[0])) * (R1 - RIBBON_W / 2)
)
PANELS_TOP_Y = RIBBON_BOTTOM_Y + 0.15  # margin under ribbon

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
    """Even angular spacing — each column at the centre of one of
    twelve equal-width segments dividing the 60° arc."""
    start, end = ANGULAR_RANGE
    n = len(PLACE_FULL)
    seg_w = (end - start) / n
    return [start + (i + 0.5) * seg_w for i in range(n)]


def segment_boundaries() -> list[tuple[float, float]]:
    """Return (theta_lo, theta_hi) for each of the 12 segments."""
    start, end = ANGULAR_RANGE
    n = len(PLACE_FULL)
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
    """SVG path for a single annular segment between angles t1 and t2."""
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


def render_top_ribbon(cols_lit_any: set[int]) -> list[str]:
    """Render twelve alternating-gray segments with radial place
    labels inside each."""
    body: list[str] = []
    r_inner = R1 - RIBBON_W / 2
    r_outer = R1 + RIBBON_W / 2

    body.append(
        f'  <g transform="translate({TOP_TRANSLATE_X:.4f} '
        f'{TOP_TRANSLATE_Y:.4f})">\n'
    )

    bounds = segment_boundaries()
    thetas = column_thetas()

    # 1. Alternating-shade segment fills + thin separator strokes.
    for i, (t_lo, t_hi) in enumerate(bounds):
        fill = (
            PALETTE["segment_light"] if i % 2 == 0
            else PALETTE["segment_dark"]
        )
        d = segment_path(r_inner, r_outer, t_lo, t_hi)
        body.append(
            f'    <path d="{d}" fill="{fill}" stroke="none" />\n'
        )

    # 2. Single outline around the whole ribbon (outer arc only)
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

    # 3. Radial labels — full place names at the radial mid-line of
    # each segment, baseline along the radius (text reads outward
    # from origin).  SVG rotation = (theta − 270°) makes the text
    # baseline align with the outward radial vector at theta.
    label_r = R1  # ribbon centerline
    for i, theta in enumerate(thetas):
        if i not in cols_lit_any:
            # Still draw the label even if no language uses this
            # column; the segment is part of the place axis.
            pass
        x, y = point_at(label_r, label_r, theta)
        rotation = theta - 270.0
        body.append(
            f'    <text text-anchor="middle" dominant-baseline="middle" '
            f'font-size="0.085" letter-spacing="0.010" '
            f'fill="{PALETTE["segment_text"]}" font-family="{FONT}" '
            f'transform="translate({x:.4f} {y:.4f}) '
            f'rotate({rotation:.4f})">'
            f'{_xml_escape(PLACE_FULL[i])}</text>\n'
        )

    body.append('  </g>\n')
    return body


def render_guides(cols_lit_any: set[int]) -> list[str]:
    """Continuous dashed vertical guides from below the ribbon down
    through all hotzone panels."""
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
        y_top = TOP_TRANSLATE_Y + y_local + 0.05
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

    # Language name + count + descriptor on the left below the row
    body.append(
        f'  <text x="0.35" y="{y_name:.4f}" '
        f'text-anchor="start" font-size="0.110" font-weight="bold" '
        f'fill="{PALETTE["label"]}" font-family="{FONT}">'
        f'{_xml_escape(name)} · {n_total} consonants</text>\n'
    )
    body.append(
        f'  <text x="0.35" y="{y_name + 0.14:.4f}" '
        f'text-anchor="start" font-size="0.090" font-style="italic" '
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
        f'text-anchor="middle" font-size="0.090" font-style="italic" '
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
