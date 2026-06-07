#!/usr/bin/env python3
"""Figure 7.2 — Language Hotzones Along the Vocal Tract.

Four stacked panels (English / Arabic / Mandarin / Zulu) on a single
4.5 in × 6.0 in canvas.  Each panel collapses the language's
consonant inventory BY PLACE OF ARTICULATION: count the cells at
each of the 12 place columns, draw a single gray circle whose AREA
is proportional to the count.  Larger circle = more sounds selected
in that anatomical region.

The figure is INFORMATIONAL, not polemical.  No Sanskrit, no Indic
languages.  Shows that different languages select different
'hotzones' from the same vocal instrument.

Filenames are distinct from `vocal_tract_hotzones.py` to avoid
collision with parallel work.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vocal_tract_schematics import point_at, build_ribbon_path_d  # noqa: E402


# ---------------------------------------------------------------------------
# Per-language inputs
# ---------------------------------------------------------------------------

PANELS = [
    ("english",  "English",   "front-heavy selection"),
    ("arabic",   "Arabic",    "deep-field / throat-side spread"),
    ("mandarin", "Mandarin",  "coronal-palatal concentration"),
    ("zulu",     "Zulu",      "click-mechanism / expanded contact selection"),
]


# 12-column anatomical place axis — lip-to-place distance (cm)
DISTANCES = [0.0, 0.5, 1.0, 1.5, 2.5, 3.5, 3.8, 5.5, 9.0, 11.5, 13.5, 17.0]
PLACE_ABBR = [
    "BIL", "LD", "ID", "DEN", "ALV", "PA",
    "RET", "PAL", "VEL", "UV", "PHA", "GLO",
]
ANGULAR_RANGE = (150.0, 240.0)


# Per-panel ribbon geometry (smaller than the standalone atlas so a
# whole panel fits comfortably in 1.4 in of vertical space)
R1 = R2 = 1.0
RIBBON_W = 0.18

# Canvas
W = 4.5
H = 6.0
PANEL_H = 1.4
FOOTER_H = H - PANEL_H * len(PANELS)  # 0.4 in for caption


PALETTE = {
    "background":   "#f4f4f3",
    "ribbon_fill":  "#eceae5",
    "ribbon_stroke": "#cdccc8",
    "circle":       "#2b2b2d",
    "label":        "#2b2b2d",
    "muted":        "#9a9892",
    "abbr":         "#6a6a6a",
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
    d_min, d_max = min(DISTANCES), max(DISTANCES)
    start, end = ANGULAR_RANGE
    span = end - start
    return [start + (d - d_min) / (d_max - d_min) * span for d in DISTANCES]


def count_per_column(matrix: list[list[str]]) -> list[int]:
    counts = [0] * 12
    for row in matrix:
        for col_idx, cell in enumerate(row):
            if cell:
                counts[col_idx] += 1
    return counts


def render_panel(
    name: str,
    descr: str,
    counts: list[int],
    n_total: int,
    panel_idx: int,
    radius_scale: float,
) -> list[str]:
    """Render one panel's drawing instructions."""
    body: list[str] = []

    panel_y = panel_idx * PANEL_H

    # ---- 1.  Language name + count (top of panel) ----
    body.append(
        f'  <text x="{W/2:.3f}" y="{panel_y + 0.20:.3f}" '
        f'text-anchor="middle" font-size="0.14" font-weight="bold" '
        f'fill="{PALETTE["label"]}" font-family="{FONT}">'
        f'{_xml_escape(name)} · {n_total} consonants</text>\n'
    )
    body.append(
        f'  <text x="{W/2:.3f}" y="{panel_y + 0.36:.3f}" '
        f'text-anchor="middle" font-size="0.095" font-style="italic" '
        f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
        f'{_xml_escape(descr)}</text>\n'
    )

    # ---- 2.  Ribbon arc + hotzone circles, grouped and translated ----
    # Place the ribbon's outer-edge apex (most-negative y_group) at
    # panel_y + 0.50 so the language name and the hotzone circles
    # never overlap.  Apex y_group = cos(195°) × (R1 + W/2) = −1.053.
    translate_y = panel_y + 0.50 + 1.053
    cx_translate = W / 2

    body.append(
        f'  <g transform="translate({cx_translate:.3f} '
        f'{translate_y:.3f})">\n'
    )

    # 2a.  Ribbon fill
    t1, t2 = ANGULAR_RANGE
    ribbon_d, _ = build_ribbon_path_d(R1, R2, RIBBON_W, t1, t2)
    body.append(
        f'    <path d="{ribbon_d}" '
        f'fill="{PALETTE["ribbon_fill"]}" '
        f'stroke="{PALETTE["ribbon_stroke"]}" stroke-width="0.012" />\n'
    )

    # 2b.  Hotzone circles — one per filled column, area ∝ count
    thetas = column_thetas()
    for col_idx in range(12):
        cnt = counts[col_idx]
        if cnt == 0:
            continue
        r_circle = radius_scale * math.sqrt(cnt)
        cx, cy = point_at(R1, R2, thetas[col_idx])
        body.append(
            f'    <circle cx="{cx:.3f}" cy="{cy:.3f}" '
            f'r="{r_circle:.3f}" fill="{PALETTE["circle"]}" '
            f'opacity="0.78" />\n'
        )

    body.append('  </g>\n')

    # ---- 3.  Place-abbreviation strip along the bottom of the panel ----
    abbr_y = panel_y + PANEL_H - 0.13
    # 12 evenly-spaced positions across the panel's usable width
    strip_left = 0.30
    strip_right = W - 0.30
    strip_w = strip_right - strip_left
    for col_idx in range(12):
        x = strip_left + (col_idx + 0.5) * strip_w / 12
        cnt = counts[col_idx]
        bold = cnt > 0
        weight = "bold" if bold else "normal"
        fill = PALETTE["label"] if bold else PALETTE["abbr"]
        opacity = "1.0" if bold else "0.45"
        body.append(
            f'  <text x="{x:.3f}" y="{abbr_y:.3f}" '
            f'text-anchor="middle" font-size="0.075" font-weight="{weight}" '
            f'fill="{fill}" opacity="{opacity}" '
            f'font-family="{FONT}">'
            f'{_xml_escape(PLACE_ABBR[col_idx])}</text>\n'
        )

    return body


def build_figure() -> str:
    cfg_dir = Path(__file__).resolve().parent / "configs"

    # Load each language's matrix and compute counts.
    panel_data: list[tuple[str, str, list[int], int]] = []
    global_max = 0
    for slug, name, descr in PANELS:
        cfg = json.loads((cfg_dir / f"scatter_{slug}.json").read_text())
        counts = count_per_column(cfg["scatter"]["matrix"])
        n_total = sum(counts)
        panel_data.append((name, descr, counts, n_total))
        for c in counts:
            if c > global_max:
                global_max = c

    # Set the largest circle to 0.18 in radius; smaller circles scale
    # by sqrt(count) so AREA is proportional to count.
    r_max_inches = 0.18
    radius_scale = (
        r_max_inches / math.sqrt(global_max) if global_max > 0 else 0.0
    )

    body: list[str] = []
    body.append(
        f'  <rect x="0" y="0" width="{W:.3f}" height="{H:.3f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    for i, (name, descr, counts, n_total) in enumerate(panel_data):
        body.extend(render_panel(name, descr, counts, n_total, i, radius_scale))

    # Subtle dividers between panels
    for i in range(1, len(panel_data)):
        y = i * PANEL_H
        body.append(
            f'  <line x1="0.30" y1="{y:.3f}" '
            f'x2="{W - 0.30:.3f}" y2="{y:.3f}" '
            f'stroke="{PALETTE["ribbon_stroke"]}" stroke-width="0.006" '
            f'opacity="0.55" />\n'
        )

    # Caption footer
    caption_y = H - 0.18
    body.append(
        f'  <text x="{W/2:.3f}" y="{caption_y:.3f}" '
        f'text-anchor="middle" font-size="0.095" font-style="italic" '
        f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
        f'Languages select different hotzones from the same vocal '
        f'instrument.</text>\n'
    )

    svg = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W:.3f}in" height="{H:.3f}in" '
        f'viewBox="0 0 {W:.3f} {H:.3f}">\n'
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
