#!/usr/bin/env python3
"""Ch 9 — Subcontinental overlay (matrix layout, 4 languages).

The matrix-layout variant of the polished overlay: a rectangular
place × manner grid where four languages stack as concentric visual
codes at each lit cell.  All the styling elements from the
`overlay_sanskrit_vs_tamil_polished.svg` idiom are preserved (cream
background, dark gray data marks, pill chips for place
abbreviations, articulator-group bands, italic caption, header
with language · count entries paired with their visual codes); only
the geometry changes from polar to rectangular.

Columns (left → right):
  BIL · DEN · ALV · PA · RET · PAL · VEL
  (LD, ID, UV, PHA, GLO omitted — none of the four languages
  lights LD/ID/UV/PHA on the place axis, and GLO is dropped per
  the design call to focus on the oral-cavity contact axis.)

Manner rows:
  Only manners used by at least one of the four languages, in
  MANNERS-list order (top → bottom).  After stripping mahāprāṇa
  from Sanskrit this typically reduces to seven rows: voiceless
  and voiced unaspirated stops, nasal, voiceless fricative,
  lateral approximant, approximant / glide, tap or trill.

Visual codes (per inventory_atlas_roadmap.md §4.1):
  Sanskrit  — filled gray circle    (r=0.046, opacity 0.88)
  Tamil     — outlined ring         (r=0.072, stroke 0.011)
  Kurukh    — dashed outline ring   (r=0.094, dashed 0.045 0.026)
  Toda      — small dot with halo   (r=0.022, cream-haloed)

Draw order at each shared cell: outside-in (dashed → outlined →
filled → dot), so smaller solid codes appear on top of larger
outlined ones.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.toolkits.vocal_tract.overlay import (
    MANNERS, MANNER_DISPLAY, PLACE_ABBR, ARTICULATOR_GROUPS,
    harmonize, strip_cells,
    _polished_color_palette, _xml_escape,
)
from _shared.toolkits.vocal_tract import CONFIGS_DIR


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LANGUAGES = [
    ("sanskrit", "Sanskrit", "filled"),
    ("tamil",    "Tamil",    "outlined"),
    ("kurukh",   "Kurukh",   "dashed"),
    ("toda",     "Toda",     "dot"),
]
STRIP_PRESETS = ["mahaprana"]

# Place columns (original atlas column indices) shown in the matrix.
# BIL=0, DEN=3, ALV=4, PA=5, RET=6, PAL=7, VEL=8.
SELECTED_PLACES = [0, 3, 4, 5, 6, 7, 8]


CODE_R = {
    "filled":   0.046,
    "outlined": 0.072,
    "dashed":   0.094,
    "dot":      0.022,
}
DRAW_ORDER = ["dashed", "outlined", "filled", "dot"]


def visual_code_svg(kind: str, cx: float, cy: float, palette: dict) -> str:
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
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r}" '
            f'fill="{palette["data"]}" stroke="{palette["background"]}" '
            f'stroke-width="0.008" />\n'
        )
    raise ValueError(f"unknown visual code: {kind}")


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

CELL = 0.45               # cell side, inches
ROW_LABEL_W = 1.30        # space for manner labels left of the matrix
COL_HEADER_H = 0.34       # space for pill-chip column headers
GROUP_BAND_H = 0.32       # space for LAB / CORONAL / DORSAL bands
LEGEND_H = 0.36           # space for top language-legend row
CAPTION_H = 0.30
TOP_MARGIN = 0.18
BOTTOM_MARGIN = 0.16
LEFT_MARGIN = 0.18
RIGHT_MARGIN = 0.22


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(cells_list: list[set[tuple[int, int]]],
           labels: list[str], codes: list[str]) -> str:
    palette = _polished_color_palette()
    font = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

    # 1. Filter cells to selected places + remap to matrix-column indices.
    place_to_col = {p: i for i, p in enumerate(SELECTED_PLACES)}
    matrix_cells = [
        {(place_to_col[p], m) for (p, m) in cs if p in place_to_col}
        for cs in cells_list
    ]

    # 2. Manner-row compaction across union of all four languages.
    union = set().union(*matrix_cells)
    rows_used = sorted({m for (_, m) in union})
    n_cols = len(SELECTED_PLACES)
    n_rows = len(rows_used)
    row_to_visible = {m: i for i, m in enumerate(rows_used)}

    # 3. Canvas + matrix placement.
    matrix_w = n_cols * CELL
    matrix_h = n_rows * CELL

    canvas_w = LEFT_MARGIN + ROW_LABEL_W + matrix_w + RIGHT_MARGIN
    canvas_h = (TOP_MARGIN + LEGEND_H + GROUP_BAND_H + COL_HEADER_H
                + matrix_h + CAPTION_H + BOTTOM_MARGIN)

    matrix_left = LEFT_MARGIN + ROW_LABEL_W
    matrix_top = (TOP_MARGIN + LEGEND_H + GROUP_BAND_H + COL_HEADER_H)

    def cell_center(matrix_col: int, visible_row: int) -> tuple[float, float]:
        return (matrix_left + (matrix_col + 0.5) * CELL,
                matrix_top + (visible_row + 0.5) * CELL)

    body: list[str] = []

    # ---- Background ----
    body.append(
        f'  <rect x="0" y="0" width="{canvas_w:.4f}" height="{canvas_h:.4f}" '
        f'fill="{palette["background"]}" />\n'
    )

    # ---- Header row: language · count entries with visual codes ----
    legend_y = TOP_MARGIN + LEGEND_H / 2
    header_font = 0.115
    chip_gap = 0.10
    inter_gap = 0.34
    entry_texts = [f"{label} · {len(cells)}"
                   for label, cells in zip(labels, matrix_cells)]
    entry_widths = [
        2 * CODE_R[codes[i]] + chip_gap + len(entry_texts[i]) * header_font * 0.55
        for i in range(len(labels))
    ]
    total_w = sum(entry_widths) + (len(labels) - 1) * inter_gap
    x_cursor = canvas_w / 2 - total_w / 2
    for i in range(len(labels)):
        x_chip = x_cursor + CODE_R[codes[i]]
        body.append(visual_code_svg(codes[i], x_chip, legend_y, palette))
        x_text = x_chip + CODE_R[codes[i]] + chip_gap
        body.append(
            f'  <text x="{x_text:.4f}" y="{legend_y + 0.04:.4f}" '
            f'font-size="{header_font}" fill="{palette["data"]}" '
            f'font-family="{font}">{_xml_escape(entry_texts[i])}</text>\n'
        )
        x_cursor += entry_widths[i] + inter_gap

    # ---- Articulator-group bands (LAB / CORONAL / DORSAL) ----
    band_y_baseline = TOP_MARGIN + LEGEND_H + GROUP_BAND_H * 0.62
    band_line_y = TOP_MARGIN + LEGEND_H + GROUP_BAND_H * 0.88
    for group_name, group_cols in ARTICULATOR_GROUPS:
        spanned = [place_to_col[c] for c in group_cols if c in place_to_col]
        if not spanned:
            continue
        c_lo, c_hi = min(spanned), max(spanned)
        x_lo = matrix_left + c_lo * CELL + 0.06
        x_hi = matrix_left + (c_hi + 1) * CELL - 0.06
        x_mid = (x_lo + x_hi) / 2
        body.append(
            f'  <path d="M {x_lo:.4f} {band_line_y:.4f} '
            f'L {x_hi:.4f} {band_line_y:.4f}" '
            f'stroke="{palette["group_arc"]}" stroke-width="0.012" '
            f'stroke-linecap="round" />\n'
        )
        for x in (x_lo, x_hi):
            body.append(
                f'  <path d="M {x:.4f} {band_line_y:.4f} '
                f'L {x:.4f} {band_line_y - 0.04:.4f}" '
                f'stroke="{palette["group_arc"]}" stroke-width="0.012" />\n'
            )
        body.append(
            f'  <text x="{x_mid:.4f}" y="{band_y_baseline:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="0.092" letter-spacing="0.030" '
            f'fill="{palette["group_arc"]}" font-family="{font}">'
            f'{group_name}</text>\n'
        )

    # ---- Column headers: pill chips with place abbreviations ----
    pill_y = matrix_top - COL_HEADER_H / 2 + 0.02
    pill_w, pill_h, pill_r = 0.32, 0.28, 0.03
    pill_font = 0.122
    for col_orig in SELECTED_PLACES:
        i = place_to_col[col_orig]
        x = matrix_left + (i + 0.5) * CELL
        body.append(
            f'  <rect x="{x - pill_w/2:.4f}" y="{pill_y - pill_h/2:.4f}" '
            f'width="{pill_w}" height="{pill_h}" rx="{pill_r}" '
            f'fill="{palette["pill_fill"]}" stroke="none" />\n'
        )
        abbr = PLACE_ABBR.get(col_orig, str(col_orig + 1))
        body.append(
            f'  <text x="{x:.4f}" y="{pill_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{pill_font}" letter-spacing="0.012" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'{abbr}</text>\n'
        )

    # ---- Grid lines (subtle) ----
    grid_color = "#dcdad4"
    grid_w = 0.005
    grid_left = matrix_left
    grid_right = matrix_left + matrix_w
    grid_top_ = matrix_top
    grid_bot = matrix_top + matrix_h
    for i in range(n_cols + 1):
        x = grid_left + i * CELL
        body.append(
            f'  <line x1="{x:.4f}" y1="{grid_top_:.4f}" '
            f'x2="{x:.4f}" y2="{grid_bot:.4f}" '
            f'stroke="{grid_color}" stroke-width="{grid_w}" />\n'
        )
    for i in range(n_rows + 1):
        y = grid_top_ + i * CELL
        body.append(
            f'  <line x1="{grid_left:.4f}" y1="{y:.4f}" '
            f'x2="{grid_right:.4f}" y2="{y:.4f}" '
            f'stroke="{grid_color}" stroke-width="{grid_w}" />\n'
        )

    # ---- Row labels (manner names) ----
    row_font = 0.108
    for row_idx in rows_used:
        i = row_to_visible[row_idx]
        y = matrix_top + (i + 0.5) * CELL
        manner_name = MANNER_DISPLAY.get(MANNERS[row_idx], MANNERS[row_idx])
        body.append(
            f'  <text x="{matrix_left - 0.14:.4f}" y="{y:.4f}" '
            f'text-anchor="end" dominant-baseline="middle" '
            f'font-size="{row_font}" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'{_xml_escape(manner_name)}</text>\n'
        )

    # ---- Visual codes per cell (layered outside-in) ----
    code_to_lang_idx = {c: i for i, c in enumerate(codes)}
    for code in DRAW_ORDER:
        if code not in code_to_lang_idx:
            continue
        lang_idx = code_to_lang_idx[code]
        for col, manner_row in sorted(matrix_cells[lang_idx]):
            vrow = row_to_visible[manner_row]
            x, y = cell_center(col, vrow)
            body.append(visual_code_svg(code, x, y, palette))

    # ---- Caption ----
    cap_y = matrix_top + matrix_h + CAPTION_H / 2 + 0.10
    body.append(
        f'  <text x="{canvas_w/2:.4f}" y="{cap_y:.4f}" '
        f'text-anchor="middle" font-size="0.098" font-style="italic" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'Mahāprāṇa rows stripped from Sanskrit · '
        f'manner rows shown are the union used by these four languages.'
        f'</text>\n'
    )

    svg = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{canvas_w:.4f}in" height="{canvas_h:.4f}in" '
        f'viewBox="0 0 {canvas_w:.4f} {canvas_h:.4f}">\n'
        + "".join(body)
        + '</svg>\n'
    )
    return svg


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main() -> int:
    cells_list: list[set[tuple[int, int]]] = []
    labels: list[str] = []
    codes: list[str] = []
    for slug, label, code in LANGUAGES:
        cfg = json.loads((CONFIGS_DIR / f"scatter_{slug}.json").read_text())
        cells, _, unc = harmonize(cfg["scatter"]["matrix"])
        if unc:
            print(f"  warn: unclassified symbols in {slug}: {unc[:5]}")
        cells = strip_cells(cells, STRIP_PRESETS)
        cells_list.append(cells)
        labels.append(label)
        codes.append(code)

    svg = render(cells_list, labels, codes)
    out = Path(__file__).resolve().parent / "subcontinental_overlay.from-py.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
