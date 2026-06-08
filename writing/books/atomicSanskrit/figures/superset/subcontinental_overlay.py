#!/usr/bin/env python3
"""Ch 9 — Subcontinental overlay (matrix layout with cell rosette, 4 langs).

Eight-column place × manner-union matrix.  Each lit cell carries a
rosette of up to four language marks arranged so the four can co-
exist in one cell without obscuring each other:

  Sanskrit  — cell-tint background     (rounded shaded rectangle
                                        filling the cell when
                                        Sanskrit lights it)
  Tamil     — TOP vertex of triangle    (solid filled circle)
  Toda      — BOTTOM-LEFT vertex        (smaller solid dot)
  Kurukh    — BOTTOM-RIGHT vertex       (dashed outline ring)

The three corner marks form a triangle within the cell.  Position
disambiguates the three solid/dashed variants; the Sanskrit tint
is a separate visual channel (cell fill, not corner mark).

Columns (8):  BIL · DEN · ALV · PA · RET · PAL · VEL · GLO
Manners:      union used by the four languages after mahāprāṇa strip
Mahāprāṇa rows are stripped from Sanskrit before render.

Other styling preserved from the polished overlay idiom: cream
background, dark gray data marks, pill chips with place
abbreviations, articulator-group bands LAB / CORONAL / DORSAL ·
LARYNGEAL, italic caption, language-legend header row.
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

# (slug, label, role).  Roles drive the visual code:
#   "tint"    — cell-background rounded rectangle (Sanskrit)
#   "top"     — top-vertex solid filled circle    (Tamil)
#   "left"    — bottom-left small solid dot       (Toda)
#   "right"   — bottom-right dashed outline ring  (Kurukh)
LANGUAGES = [
    ("sanskrit", "Sanskrit", "tint"),
    ("tamil",    "Tamil",    "top"),
    ("toda",     "Toda",     "left"),
    ("kurukh",   "Kurukh",   "right"),
]
STRIP_PRESETS = ["mahaprana"]

# 8 place columns: BIL=0, DEN=3, ALV=4, PA=5, RET=6, PAL=7, VEL=8, GLO=11.
SELECTED_PLACES = [0, 3, 4, 5, 6, 7, 8, 11]


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

CELL = 0.55                # cell side, in
ROW_LABEL_W = 1.30
COL_HEADER_H = 0.34
GROUP_BAND_H = 0.32
LEGEND_H = 0.40
CAPTION_H = 0.30
TOP_MARGIN = 0.18
BOTTOM_MARGIN = 0.16
LEFT_MARGIN = 0.18
RIGHT_MARGIN = 0.22

# Rosette geometry inside a cell (cell centre at origin).
# Equilateral-ish triangle inscribed in the cell, centred on the
# cell midpoint.
ROSETTE_TOP    = (0.000, -0.115)
ROSETTE_LEFT   = (-0.108, +0.062)
ROSETTE_RIGHT  = (+0.108, +0.062)

# Sanskrit cell-tint rectangle parameters
SANSKRIT_BG_INSET = 0.05    # how far from cell edge the rect sits
SANSKRIT_BG_RX = 0.07       # corner radius

# Corner-mark radii
R_TOP    = 0.046            # Tamil top vertex
R_LEFT   = 0.030            # Toda bottom-left (smaller — disambiguates Tamil)
R_RIGHT  = 0.046            # Kurukh bottom-right

# Sanskrit tint shade (lighter than data dark; reads as a soft fill)
SANSKRIT_TINT = "#e6e3db"


# ---------------------------------------------------------------------------
# Visual codes
# ---------------------------------------------------------------------------

def render_sanskrit_tint(cx: float, cy: float) -> str:
    """Rounded rounded-rect background filling a cell when Sanskrit lights it."""
    side = CELL - 2 * SANSKRIT_BG_INSET
    return (
        f'  <rect x="{cx - side/2:.4f}" y="{cy - side/2:.4f}" '
        f'width="{side:.4f}" height="{side:.4f}" rx="{SANSKRIT_BG_RX}" '
        f'fill="{SANSKRIT_TINT}" stroke="none" />\n'
    )


def render_top_vertex(cx: float, cy: float, palette: dict) -> str:
    """Tamil — solid filled circle at top vertex."""
    x, y = cx + ROSETTE_TOP[0], cy + ROSETTE_TOP[1]
    return (
        f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{R_TOP}" '
        f'fill="{palette["data"]}" />\n'
    )


def render_left_vertex(cx: float, cy: float, palette: dict) -> str:
    """Toda — smaller solid dot at bottom-left vertex (cream halo for legibility
    inside Sanskrit's tinted cell)."""
    x, y = cx + ROSETTE_LEFT[0], cy + ROSETTE_LEFT[1]
    return (
        f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{R_LEFT}" '
        f'fill="{palette["data"]}" stroke="{palette["background"]}" '
        f'stroke-width="0.008" />\n'
    )


def render_right_vertex(cx: float, cy: float, palette: dict) -> str:
    """Kurukh — dashed outline ring at bottom-right vertex."""
    x, y = cx + ROSETTE_RIGHT[0], cy + ROSETTE_RIGHT[1]
    return (
        f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{R_RIGHT}" '
        f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" '
        f'stroke-dasharray="0.045 0.026" />\n'
    )


ROLE_RENDERERS = {
    "tint":  None,                # special-cased: render first, below corner marks
    "top":   render_top_vertex,
    "left":  render_left_vertex,
    "right": render_right_vertex,
}


# Legend-chip renderers — mini versions positioned at a freestanding point.
def render_legend_chip(role: str, cx: float, cy: float, palette: dict) -> str:
    if role == "tint":
        # Show a small rounded rect — the "tile" idiom — next to "Sanskrit · N"
        w, h, rx = 0.20, 0.13, 0.025
        return (
            f'  <rect x="{cx - w/2:.4f}" y="{cy - h/2:.4f}" '
            f'width="{w}" height="{h}" rx="{rx}" '
            f'fill="{SANSKRIT_TINT}" stroke="none" />\n'
        )
    if role == "top":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{R_TOP}" '
            f'fill="{palette["data"]}" />\n'
        )
    if role == "left":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{R_LEFT}" '
            f'fill="{palette["data"]}" stroke="{palette["background"]}" '
            f'stroke-width="0.008" />\n'
        )
    if role == "right":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{R_RIGHT}" '
            f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" '
            f'stroke-dasharray="0.045 0.026" />\n'
        )
    raise ValueError(f"unknown legend role: {role}")


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(cells_list: list[set[tuple[int, int]]],
           labels: list[str], roles: list[str]) -> str:
    palette = _polished_color_palette()
    font = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

    # 1. Filter cells to selected places + remap to matrix-column indices.
    place_to_col = {p: i for i, p in enumerate(SELECTED_PLACES)}
    matrix_cells = [
        {(place_to_col[p], m) for (p, m) in cs if p in place_to_col}
        for cs in cells_list
    ]

    # 2. Manner-row compaction across union of all four languages' cells.
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

    # ---- Sanskrit cell-tint backgrounds (BEFORE everything else so corner
    # marks land on top) ----
    sanskrit_idx = roles.index("tint")
    for col, manner_row in sorted(matrix_cells[sanskrit_idx]):
        vrow = row_to_visible[manner_row]
        cx, cy = cell_center(col, vrow)
        body.append(render_sanskrit_tint(cx, cy))

    # ---- Header row: language · count entries with legend chips ----
    legend_y = TOP_MARGIN + LEGEND_H / 2
    header_font = 0.115
    chip_gap = 0.12
    inter_gap = 0.34

    # Estimate chip widths (varies by role)
    def chip_extent(role: str) -> float:
        if role == "tint":   return 0.20
        if role == "top":    return 2 * R_TOP
        if role == "left":   return 2 * R_LEFT
        if role == "right":  return 2 * R_RIGHT
        return 0.1

    entry_texts = [f"{label} · {len(cells)}"
                   for label, cells in zip(labels, matrix_cells)]
    entry_widths = [
        chip_extent(roles[i]) + chip_gap + len(entry_texts[i]) * header_font * 0.55
        for i in range(len(labels))
    ]
    total_w = sum(entry_widths) + (len(labels) - 1) * inter_gap
    x_cursor = canvas_w / 2 - total_w / 2
    for i in range(len(labels)):
        ext = chip_extent(roles[i])
        x_chip = x_cursor + ext / 2
        body.append(render_legend_chip(roles[i], x_chip, legend_y, palette))
        x_text = x_chip + ext / 2 + chip_gap
        body.append(
            f'  <text x="{x_text:.4f}" y="{legend_y + 0.04:.4f}" '
            f'font-size="{header_font}" fill="{palette["data"]}" '
            f'font-family="{font}">{_xml_escape(entry_texts[i])}</text>\n'
        )
        x_cursor += entry_widths[i] + inter_gap

    # ---- Articulator-group bands ----
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
    pill_w, pill_h, pill_r = 0.34, 0.28, 0.03
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
    for i in range(n_cols + 1):
        x = matrix_left + i * CELL
        body.append(
            f'  <line x1="{x:.4f}" y1="{matrix_top:.4f}" '
            f'x2="{x:.4f}" y2="{matrix_top + matrix_h:.4f}" '
            f'stroke="{grid_color}" stroke-width="{grid_w}" />\n'
        )
    for i in range(n_rows + 1):
        y = matrix_top + i * CELL
        body.append(
            f'  <line x1="{matrix_left:.4f}" y1="{y:.4f}" '
            f'x2="{matrix_left + matrix_w:.4f}" y2="{y:.4f}" '
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

    # ---- Corner marks for Tamil / Toda / Kurukh ----
    # Render order: Toda (small) → Tamil (medium) → Kurukh (medium dashed).
    # Stable order with no overlap; smallest first keeps them all visible
    # whether or not Sanskrit's tint is underneath.
    for role in ("left", "top", "right"):
        lang_idx = roles.index(role)
        renderer = ROLE_RENDERERS[role]
        for col, manner_row in sorted(matrix_cells[lang_idx]):
            vrow = row_to_visible[manner_row]
            cx, cy = cell_center(col, vrow)
            body.append(renderer(cx, cy, palette))

    # ---- Caption ----
    cap_y = matrix_top + matrix_h + CAPTION_H / 2 + 0.10
    body.append(
        f'  <text x="{canvas_w/2:.4f}" y="{cap_y:.4f}" '
        f'text-anchor="middle" font-size="0.098" font-style="italic" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'Mahāprāṇa rows stripped from Sanskrit · '
        f'rosette positions in each cell: Tamil ▲ top, Toda ◣ bottom-left, '
        f'Kurukh ◥ bottom-right.</text>\n'
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
    roles: list[str] = []
    for slug, label, role in LANGUAGES:
        cfg = json.loads((CONFIGS_DIR / f"scatter_{slug}.json").read_text())
        cells, _, unc = harmonize(cfg["scatter"]["matrix"])
        if unc:
            print(f"  warn: unclassified symbols in {slug}: {unc[:5]}")
        cells = strip_cells(cells, STRIP_PRESETS)
        cells_list.append(cells)
        labels.append(label)
        roles.append(role)

    svg = render(cells_list, labels, roles)
    out = Path(__file__).resolve().parent / "subcontinental_overlay.from-py.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
