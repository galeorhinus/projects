#!/usr/bin/env python3
"""Ch 9 — Subcontinental overlay (polished, 4-language).

The polished overlay idiom from `overlay_sanskrit_vs_tamil_polished.svg`,
extended to four languages.  Mahāprāṇa rows (voiceless aspirated stop,
voiced aspirated stop) are stripped from every language before
rendering — so the chart shows the *natural shared subcontinental
field*, with Sanskrit's engineered mahāprāṇa overlay deliberately
removed for this view.

Four languages, four visual codes (per
`working/inventory_atlas_roadmap.md` §4.1):

  Sanskrit  — filled gray circle    (the engineered selection)
  Tamil     — outlined ring         (southern subcontinental)
  Kurukh    — dashed outline ring   (central forest belt)
  Toda      — small inner dot       (Nilgiri)

At cells where multiple languages light up, the codes layer
concentrically without obscuring each other.  Outside-in draw order:
Kurukh (dashed) → Tamil (outlined) → Sanskrit (filled) → Toda (dot),
so smaller solid codes appear on top.

Reuses the polished-overlay geometry helpers, manner taxonomy,
PLACE_ABBR, ARTICULATOR_GROUPS, mahāprāṇa strip preset, and the
filled-mouth-ribbon visual idiom from
`_shared.toolkits.vocal_tract.overlay`.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.toolkits.vocal_tract.schematics import (
    point_at, build_ribbon_path_d,
)
from _shared.toolkits.vocal_tract.overlay import (
    MANNERS, MANNER_DISPLAY, PLACE_ABBR, ARTICULATOR_GROUPS,
    harmonize, strip_cells,
    _polished_color_palette, _arc_path, _xml_escape,
)
from _shared.toolkits.vocal_tract import CONFIGS_DIR


# ---------------------------------------------------------------------------
# Configuration: which four languages, which visual codes
# ---------------------------------------------------------------------------

# (config slug, display label, visual code).  Listed in HEADER order
# (left-to-right at the top of the chart).
LANGUAGES = [
    ("sanskrit", "Sanskrit", "filled"),
    ("tamil",    "Tamil",    "outlined"),
    ("kurukh",   "Kurukh",   "dashed"),
    ("toda",     "Toda",     "dot"),
]

# Apply mahāprāṇa strip to every language before rendering.  No-op for
# the three that don't natively use it; strips Sanskrit's two
# aspirated stop rows.
STRIP_PRESETS = ["mahaprana"]


# Visual-code radii.  Chosen so codes layer concentrically without
# obscuring each other:  dot (smallest) → filled → outlined → dashed.
CODE_R = {
    "filled":   0.046,
    "outlined": 0.072,
    "dashed":   0.094,
    "dot":      0.022,
}


def visual_code_svg(kind: str, cx: float, cy: float, palette: dict) -> str:
    """SVG fragment for one visual code at (cx, cy)."""
    r = CODE_R[kind]
    if kind == "filled":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r}" '
            f'fill="{palette["data"]}" opacity="0.88" />\n'
        )
    if kind == "outlined":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r}" '
            f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" />\n'
        )
    if kind == "dashed":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r}" '
            f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" '
            f'stroke-dasharray="0.045 0.026" />\n'
        )
    if kind == "dot":
        # Halo stroke (cream) so the dot stays visible whether it sits
        # alone on the background or inside Sanskrit's filled circle.
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r}" '
            f'fill="{palette["data"]}" stroke="{palette["background"]}" '
            f'stroke-width="0.008" />\n'
        )
    raise ValueError(f"unknown visual code: {kind}")


# Order in which codes draw at a shared cell (outside-in so smaller
# solid marks appear on top of larger outlined ones).
DRAW_ORDER = ["dashed", "outlined", "filled", "dot"]


# ---------------------------------------------------------------------------
# Rendering — adapted from render_overlay_polished for N languages
# ---------------------------------------------------------------------------

def render(
    cfgs: list[dict],
    cells_list: list[set[tuple[int, int]]],
    labels: list[str],
    codes: list[str],
) -> str:
    """Render the 4-language polished overlay SVG."""
    palette = _polished_color_palette()
    font = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

    # Use first config's geometry as the shared reference.
    cfg = cfgs[0]
    geometry = cfg["geometry"]
    polished_radius_offset = 0.25
    r1 = float(geometry["r1"]) - polished_radius_offset
    r2 = float(geometry["r2"]) - polished_radius_offset
    w = float(geometry["w"])

    canvas = cfg["canvas"]
    canvas_w = float(canvas["width"])
    canvas_h = float(canvas["height"]) + 0.45    # extra height for legend

    # Column thetas from anatomical distance distribution.
    ar = cfg["scatter"]["angular_range"]
    center = float(ar.get("center", 195.0))
    half = float(ar.get("half_width_deg", 45.0))
    distances = list(ar["distances"])
    d_min, d_max = min(distances), max(distances)
    d_range = d_max - d_min if d_max > d_min else 1.0
    start, end = center - half, center + half
    column_thetas = [
        start + (d - d_min) / d_range * (end - start) for d in distances
    ]
    n_cols = len(column_thetas)

    # Manner-row compaction across all four languages' cells.
    union = set().union(*cells_list)
    rows_used = sorted({m for (_, m) in union})
    n_rows_visible = len(rows_used)
    row_to_visible: dict[int, int] = {m: i for i, m in enumerate(rows_used)}

    delta_r = 0.1
    r_inner = 2.0 - polished_radius_offset
    row_radii = [
        r_inner + (n_rows_visible - 1 - i) * delta_r
        for i in range(n_rows_visible)
    ]

    cols_lit = sorted({c for (c, _) in union})

    body: list[str] = []
    samples: list[tuple[float, float]] = []

    # ----- 1. Filled mouth-ribbon -----
    base = cfg.get("base_ribbon")
    bt1 = float(base.get("t1", 150)) if base else 150.0
    bt2 = float(base.get("t2", 240)) if base else 240.0
    path_d, ribbon_samples = build_ribbon_path_d(r1, r2, w, bt1, bt2)
    body.append(
        f'  <path d="{path_d}" '
        f'fill="{palette["ribbon_fill"]}" stroke="none" />\n'
    )
    upper_arc_r1 = r1 + 0.5 * w
    upper_arc_r2 = r2 + 0.5 * w
    body.append(
        f'  <path d="{_arc_path(upper_arc_r1, upper_arc_r2, bt1, bt2)}" '
        f'fill="none" stroke="{palette["ribbon_stroke"]}" '
        f'stroke-width="0.016" stroke-linecap="round" />\n'
    )
    samples.extend(ribbon_samples)

    # Articulator tick marks at lit columns.
    for col in cols_lit:
        theta = column_thetas[col]
        x_outer, y_outer = point_at(upper_arc_r1, upper_arc_r2, theta)
        x_inner, y_inner = point_at(r1 + 0.05, r2 + 0.05, theta)
        body.append(
            f'  <path d="M {x_outer:.4f} {y_outer:.4f} '
            f'L {x_inner:.4f} {y_inner:.4f}" '
            f'stroke="{palette["detail_dark"]}" stroke-width="0.012" '
            f'stroke-linecap="round" />\n'
        )

    # ----- 2. Data marks: layer all four visual codes at each cell -----
    # Build lookups: which language(s) light each cell?
    lang_idx_by_code = {code: i for i, code in enumerate(codes)}
    cells_by_lang = list(cells_list)

    for code in DRAW_ORDER:
        if code not in lang_idx_by_code:
            continue
        lang_idx = lang_idx_by_code[code]
        for col, manner_row in sorted(cells_by_lang[lang_idx]):
            vrow = row_to_visible[manner_row]
            r = row_radii[vrow]
            theta = column_thetas[col]
            x, y = point_at(r, r, theta)
            body.append(visual_code_svg(code, x, y, palette))
            rad = CODE_R[code]
            samples.append((x - rad, y - rad))
            samples.append((x + rad, y + rad))

    # ----- 3. Leader lines + place-label pill chips -----
    y_pill = -0.32

    def innermost_visible_row(col: int) -> int | None:
        candidates = [row_to_visible[m] for (c, m) in union if c == col]
        return max(candidates) if candidates else None

    pill_x_offset = 0.30 if len(cols_lit) >= 11 else 0.0
    pill_xs: dict[int, float] = {}
    pill_min_gap = 0.34
    if cols_lit:
        sorted_cols = sorted(cols_lit)
        n_lit = len(sorted_cols)
        total_pill_width = (n_lit - 1) * pill_min_gap
        left_pill_x = -0.5 * total_pill_width
        for i, col in enumerate(sorted_cols):
            pill_xs[col] = left_pill_x + i * pill_min_gap + pill_x_offset

    leader_w = 0.007
    pill_w, pill_h, pill_r = 0.32, 0.30, 0.03
    pill_font = 0.125
    pill_top_y = y_pill - 0.5 * pill_h
    r_anchor = r_inner - 0.1
    fan_collect_y = pill_top_y - 0.25

    for col in cols_lit:
        vrow_inner = innermost_visible_row(col)
        if vrow_inner is None:
            continue
        innermost_r = row_radii[vrow_inner]
        theta = column_thetas[col]
        start_r = innermost_r - CODE_R["filled"] - 0.02
        x_start, y_start = point_at(start_r, start_r, theta)
        x_anchor, y_anchor = point_at(r_anchor, r_anchor, theta)
        x_pill = pill_xs[col]
        body.append(
            f'  <path d="M {x_start:.4f} {y_start:.4f} '
            f'L {x_anchor:.4f} {y_anchor:.4f} '
            f'L {x_pill:.4f} {fan_collect_y:.4f} '
            f'L {x_pill:.4f} {pill_top_y:.4f}" '
            f'fill="none" stroke="{palette["leader"]}" '
            f'stroke-width="{leader_w}" stroke-linecap="round" '
            f'stroke-linejoin="round" />\n'
        )
        body.append(
            f'  <rect x="{x_pill - pill_w/2:.4f}" '
            f'y="{y_pill - pill_h/2:.4f}" '
            f'width="{pill_w}" height="{pill_h}" rx="{pill_r}" '
            f'fill="{palette["pill_fill"]}" stroke="none" />\n'
        )
        abbr = PLACE_ABBR.get(col, str(col + 1))
        body.append(
            f'  <text x="{x_pill:.4f}" y="{y_pill:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{pill_font}" letter-spacing="0.012" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'{abbr}</text>\n'
        )
        samples.append((x_pill - pill_w / 2, y_pill - pill_h / 2))
        samples.append((x_pill + pill_w / 2, y_pill + pill_h / 2))

    # ----- 4. Articulator-group headers -----
    group_arc_r = upper_arc_r1 + 0.18
    group_label_r = upper_arc_r1 + 0.30
    for group_name, group_cols in ARTICULATOR_GROUPS:
        intersect = sorted(set(group_cols) & set(cols_lit))
        if not intersect:
            continue
        if group_name == "DORSAL":
            ling_intersect = sorted(set(ARTICULATOR_GROUPS[3][1]) & set(cols_lit))
            display = "DORSAL · LARYNGEAL" if ling_intersect else "DORSAL"
        elif group_name == "LARYNGEAL":
            if set(ARTICULATOR_GROUPS[2][1]) & set(cols_lit):
                continue
            display = "LARYNGEAL"
        else:
            display = group_name

        if group_name == "DORSAL" and (set(ARTICULATOR_GROUPS[3][1]) & set(cols_lit)):
            merged_cols = sorted(
                set(intersect) | (set(ARTICULATOR_GROUPS[3][1]) & set(cols_lit))
            )
            theta_a = column_thetas[merged_cols[0]]
            theta_b = column_thetas[merged_cols[-1]]
        else:
            theta_a = column_thetas[intersect[0]]
            theta_b = column_thetas[intersect[-1]]
        if theta_a == theta_b:
            theta_a -= 1.5; theta_b += 1.5
        else:
            theta_a -= 0.5; theta_b += 0.5

        for theta in (theta_a, theta_b):
            xa, ya = point_at(group_arc_r, group_arc_r, theta)
            xb, yb = point_at(group_arc_r + 0.03, group_arc_r + 0.03, theta)
            body.append(
                f'  <path d="M {xa:.4f} {ya:.4f} L {xb:.4f} {yb:.4f}" '
                f'stroke="{palette["group_arc"]}" stroke-width="0.012" />\n'
            )
        body.append(
            f'  <path d="{_arc_path(group_arc_r, group_arc_r, theta_a, theta_b)}" '
            f'fill="none" stroke="{palette["group_arc"]}" '
            f'stroke-width="0.012" stroke-linecap="round" />\n'
        )
        label_arc_id = f"grplbl_{group_name.lower()}"
        body.append(
            f'  <defs><path id="{label_arc_id}" '
            f'd="{_arc_path(group_label_r, group_label_r, theta_a, theta_b)}" '
            f'fill="none" /></defs>\n'
        )
        body.append(
            f'  <text font-size="0.092" letter-spacing="0.03" '
            f'fill="{palette["group_arc"]}" font-family="{font}">'
            f'<textPath href="#{label_arc_id}" startOffset="50%" '
            f'text-anchor="middle">{_xml_escape(display)}</textPath></text>\n'
        )
        for theta in (theta_a, theta_b):
            x, y = point_at(group_label_r + 0.06, group_label_r + 0.06, theta)
            samples.append((x, y))

    # ----- 5. Header — four language·count entries with legend marks -----
    header_font = 0.115
    header_y = -(group_label_r + 0.35)
    if samples:
        ys = [p[1] for p in samples]
        header_y = min(ys) - 0.18

    # Build labelled chips with the appropriate visual code, evenly spaced.
    n = len(labels)
    chip_gap = 0.10  # space between visual code and text within an entry
    inter_gap = 0.32 # space between entries
    entry_texts = [f"{label} · {len(cells)}"
                   for label, cells in zip(labels, cells_list)]
    entry_widths = [
        2 * CODE_R[codes[i]] + chip_gap + len(entry_texts[i]) * header_font * 0.55
        for i in range(n)
    ]
    total_w = sum(entry_widths) + (n - 1) * inter_gap
    x_cursor = -0.5 * total_w
    for i in range(n):
        # Visual code chip (drawn at the entry's left edge)
        x_chip = x_cursor + CODE_R[codes[i]]
        body.append(visual_code_svg(codes[i], x_chip, header_y, palette))
        # Label text after the chip
        x_text = x_chip + CODE_R[codes[i]] + chip_gap
        body.append(
            f'  <text x="{x_text:.4f}" y="{header_y + 0.04:.4f}" '
            f'font-size="{header_font}" fill="{palette["data"]}" '
            f'font-family="{font}">{_xml_escape(entry_texts[i])}</text>\n'
        )
        x_cursor += entry_widths[i] + inter_gap
    samples.append((-0.5 * total_w - 0.1, header_y - 0.1))
    samples.append((+0.5 * total_w + 0.1, header_y + 0.1))

    # ----- 6. Caption / mahaprana note at the bottom -----
    note_y = y_pill + 0.5 * pill_h + 0.34
    body.append(
        f'  <text x="0" y="{note_y:.4f}" text-anchor="middle" '
        f'font-size="0.105" font-style="italic" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'Mahāprāṇa rows stripped from Sanskrit · the four selections '
        f'overlap on the natural subcontinental field.</text>\n'
    )
    samples.append((-2.0, note_y))
    samples.append((+2.0, note_y))

    # ----- viewBox auto-centring -----
    visual_left_shift = 0.20
    cx_min = min(p[0] for p in samples); cx_max = max(p[0] for p in samples)
    cy_min = min(p[1] for p in samples); cy_max = max(p[1] for p in samples)
    content_cx = 0.5 * (cx_min + cx_max)
    content_cy = 0.5 * (cy_min + cy_max)
    vb_x = content_cx - canvas_w / 2.0 + visual_left_shift
    vb_y = content_cy - canvas_h / 2.0

    svg = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{canvas_w:.4f}in" height="{canvas_h:.4f}in" '
        f'viewBox="{vb_x:.4f} {vb_y:.4f} {canvas_w:.4f} {canvas_h:.4f}">\n',
        f'  <rect x="{vb_x:.4f}" y="{vb_y:.4f}" '
        f'width="{canvas_w:.4f}" height="{canvas_h:.4f}" '
        f'fill="{palette["background"]}" />\n',
    ]
    svg.extend(body)
    svg.append('</svg>\n')
    return "".join(svg)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main() -> int:
    cfgs: list[dict] = []
    cells_list: list[set[tuple[int, int]]] = []
    labels: list[str] = []
    codes: list[str] = []
    for slug, label, code in LANGUAGES:
        cfg = json.loads((CONFIGS_DIR / f"scatter_{slug}.json").read_text())
        cells, _, unc = harmonize(cfg["scatter"]["matrix"])
        if unc:
            print(f"  warn: unclassified symbols in {slug}: {unc[:5]}")
        cells = strip_cells(cells, STRIP_PRESETS)
        cfgs.append(cfg)
        cells_list.append(cells)
        labels.append(label)
        codes.append(code)

    svg = render(cfgs, cells_list, labels, codes)
    out = Path(__file__).resolve().parent / "subcontinental_overlay.from-py.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
