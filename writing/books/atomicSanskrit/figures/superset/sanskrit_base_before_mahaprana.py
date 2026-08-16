#!/usr/bin/env python3
"""Figure 8.1 — Sanskrit's 23-cell Base · Mahāprāṇa Rows Set Aside.

Single-language matrix showing Sanskrit's full consonantal inventory
with the ten mahāprāṇa stop cells rendered as set aside (faded tint
gray Devanāgarī letter + dashed outline). Makes Chapter 8's
Sanskrit comparison target clear before the regional surveys begin.

Uses Sanskrit's *sthāna* and *prayatna* categories. The later coverage
figures retain the speech-science grid needed to compare other languages.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.toolkits.vocal_tract.overlay import (
    harmonize, _polished_color_palette, _xml_escape,
)
from _shared.toolkits.vocal_tract import CONFIGS_DIR
from _shared.toolkits.vocal_tract.quad_overlay import (
    OUTER_SCALE, TARGET_CANVAS_W, MAX_CANVAS_H, CELL,
    LEFT_MARGIN, RIGHT_MARGIN, ROW_LABEL_W,
    TOP_MARGIN, BOTTOM_MARGIN,
    TITLE_H, SUBTITLE_H, COL_HEADER_H, GROUP_BAND_H, LEGEND_H, CAPTION_H,
    TITLE_FONT_SIZE, SUBTITLE_FONT_SIZE,
    ROW_FONT_SIZE, CAPTION_FONT_SIZE, BAND_FONT_SIZE,
    SANSKRIT_BG_SIDE, SANSKRIT_BG_RX, SANSKRIT_TINT, DEVANAGARI_FONT,
    _dev_font_in_cell_pt,
)


# The atlas uses six modern place columns for Sanskrit. Figure 8.1 folds
# glottal ह into the traditional kaṇṭhya column and returns to five sthānas.
STHANA_COLUMNS = [
    (8, "कण्ठ्य", "velar"),
    (7, "तालव्य", "palatal"),
    (6, "मूर्धन्य", "retroflex"),
    (3, "दन्त्य", "dental"),
    (0, "ओष्ठ्य", "labial"),
]
PLACE_TO_COLUMN = {place: index for index, (place, _, _) in enumerate(STHANA_COLUMNS)}
PLACE_TO_COLUMN[11] = 0

ROW_ORDER = [
    "alpaprana_aghosa",
    "mahaprana_aghosa",
    "alpaprana_ghosa",
    "mahaprana_ghosa",
    "anunasika",
    "antastha",
    "usman",
]
ROW_LABELS = {
    "alpaprana_aghosa": ("स्पर्श · अल्पप्राण अघोष", "light breath · unvoiced"),
    "mahaprana_aghosa": ("स्पर्श · महाप्राण अघोष", "heavy breath · unvoiced"),
    "alpaprana_ghosa": ("स्पर्श · अल्पप्राण घोष", "light breath · voiced"),
    "mahaprana_ghosa": ("स्पर्श · महाप्राण घोष", "heavy breath · voiced"),
    "anunasika": ("अनुनासिक", "nasal"),
    "antastha": ("अन्तःस्थ", "semivowel"),
    "usman": ("ऊष्मन्", "fricative"),
}
HELD_ROWS = {"mahaprana_aghosa", "mahaprana_ghosa"}


def sanskrit_row(source_manner: int) -> str:
    """Collapse modern manner labels into Sanskrit's seven row categories."""
    return {
        0: "alpaprana_aghosa",
        1: "mahaprana_aghosa",
        2: "alpaprana_ghosa",
        3: "mahaprana_ghosa",
        7: "usman",
        8: "usman",
        9: "anunasika",
        10: "antastha",
        11: "antastha",
        12: "antastha",
    }[source_manner]

# Held-aside tint is a lighter version of the active tint
SANSKRIT_TINT_FADED = "#f0eee8"
LETTER_COLOR_FADED  = "#a8a39a"


def render() -> str:
    palette = _polished_color_palette()
    font = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

    # ---- Load Sanskrit data ----
    cfg = json.loads((CONFIGS_DIR / "scatter_sanskrit.json").read_text())
    cells, symbols, unc = harmonize(cfg["scatter"]["matrix"])
    if unc:
        print(f"  warn: unclassified symbols in sanskrit: {unc[:5]}")

    # ---- Re-map the atlas inventory into Sanskrit's five sthānas ----
    matrix_cells: set[tuple[int, str]] = set()
    matrix_symbols: dict[tuple[int, str], str] = {}
    for (p, m), sym in symbols.items():
        if p not in PLACE_TO_COLUMN:
            continue
        cell = (PLACE_TO_COLUMN[p], sanskrit_row(m))
        matrix_cells.add(cell)
        matrix_symbols[cell] = sym

    rows_used = [row for row in ROW_ORDER if any(r == row for _, r in matrix_cells)]
    n_cols = len(STHANA_COLUMNS)
    n_rows = len(rows_used)
    row_to_visible = {row: i for i, row in enumerate(rows_used)}

    # ---- Counts ----
    held_cells = {c for c in matrix_cells if c[1] in HELD_ROWS}
    base_cells = matrix_cells - held_cells
    n_base = len(base_cells)
    n_held = len(held_cells)
    n_total = n_base + n_held

    # ---- Layout (matches quad_overlay's auto-format) ----
    outer_scale = OUTER_SCALE
    scaled_left = LEFT_MARGIN * outer_scale
    scaled_right = RIGHT_MARGIN * outer_scale
    # Sanskrit names for the four stop rows need a wider label lane than
    # the speech-science labels used by the comparison figures.
    scaled_row_label_w = (ROW_LABEL_W + 0.45) * outer_scale
    matrix_w_target = TARGET_CANVAS_W - scaled_left - scaled_row_label_w - scaled_right
    cell_w = matrix_w_target / n_cols

    cell_h_baseline = CELL * outer_scale
    outer_v_overhead = (TOP_MARGIN + TITLE_H + SUBTITLE_H + LEGEND_H
                        + GROUP_BAND_H + COL_HEADER_H + CAPTION_H
                        + BOTTOM_MARGIN) * outer_scale
    max_matrix_h = MAX_CANVAS_H - outer_v_overhead
    cell_h = min(cell_h_baseline, max_matrix_h / n_rows)

    inner_scale_w = cell_w / CELL
    inner_scale_h = cell_h / CELL
    inner_scale_min = min(inner_scale_w, inner_scale_h)

    # Outer scaled dims
    title_h_s      = TITLE_H * outer_scale
    subtitle_h_s   = SUBTITLE_H * outer_scale
    legend_h_s     = LEGEND_H * outer_scale
    band_h_s       = GROUP_BAND_H * outer_scale
    col_header_h_s = COL_HEADER_H * outer_scale
    caption_h_s    = CAPTION_H * outer_scale
    top_margin_s   = TOP_MARGIN * outer_scale
    bottom_margin_s = BOTTOM_MARGIN * outer_scale

    # Outer fonts
    title_font    = TITLE_FONT_SIZE * outer_scale
    subtitle_font = SUBTITLE_FONT_SIZE * outer_scale
    row_font      = ROW_FONT_SIZE * outer_scale
    caption_font  = CAPTION_FONT_SIZE * outer_scale
    band_font     = BAND_FONT_SIZE * outer_scale

    # Cell-internal sizes
    dev_font_in_cell = _dev_font_in_cell_pt(n_cols) / 72
    sans_bg_w = SANSKRIT_BG_SIDE * inner_scale_w
    sans_bg_h = SANSKRIT_BG_SIDE * inner_scale_h
    sans_bg_rx = SANSKRIT_BG_RX * inner_scale_min
    held_stroke_w = 0.013 * inner_scale_min

    # Canvas
    matrix_w = n_cols * cell_w
    matrix_h = n_rows * cell_h
    canvas_w = scaled_left + scaled_row_label_w + matrix_w + scaled_right
    canvas_h = (top_margin_s + title_h_s + subtitle_h_s + legend_h_s
                + band_h_s + col_header_h_s + matrix_h
                + caption_h_s + bottom_margin_s)
    matrix_left = scaled_left + scaled_row_label_w
    matrix_top = (top_margin_s + title_h_s + subtitle_h_s + legend_h_s
                  + band_h_s + col_header_h_s)

    def cell_center(col: int, vrow: int) -> tuple[float, float]:
        return (matrix_left + (col + 0.5) * cell_w,
                matrix_top + (vrow + 0.5) * cell_h)

    body: list[str] = []

    # ---- Background ----
    body.append(
        f'  <rect x="0" y="0" width="{canvas_w:.4f}" height="{canvas_h:.4f}" '
        f'fill="{palette["background"]}" />\n'
    )

    # ---- Title + subtitle ----
    title_text = f"Sanskrit's {n_base}-cell Base · Mahāprāṇa Rows Set Aside"
    title_y = top_margin_s + title_h_s / 2 + 0.04 * outer_scale
    body.append(
        f'  <text x="{canvas_w/2:.4f}" y="{title_y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{title_font:.4f}" font-weight="700" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'{_xml_escape(title_text)}</text>\n'
    )

    subtitle_y = top_margin_s + title_h_s + subtitle_h_s / 2 + 0.02 * outer_scale
    body.append(
        f'  <text x="{canvas_w/2:.4f}" y="{subtitle_y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{subtitle_font:.4f}" font-style="italic" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'<tspan font-family="{DEVANAGARI_FONT}" font-style="normal">महाप्राण</tspan> '
        f'rows set aside (faded) for the chapter’s comparison — '
        f'<tspan font-style="normal" font-family="{DEVANAGARI_FONT}">'
        f'ख · छ · ठ · थ · फ and घ · झ · ढ · ध · भ</tspan></text>\n'
    )

    # ---- Legend chips: active vs held-aside ----
    legend_y = top_margin_s + title_h_s + subtitle_h_s + legend_h_s / 2
    chip_w = 0.26 * outer_scale
    chip_h = 0.22 * outer_scale
    chip_rx = 0.045 * outer_scale
    chip_dev_font = 0.149 * outer_scale
    chip_gap = 0.12 * outer_scale
    inter_gap = 0.40 * outer_scale

    # Build the two chip+text entries
    entry_active_text = f"Base cells · {n_base}"
    entry_held_text   = f"Set aside · {n_held}"
    header_font = SUBTITLE_FONT_SIZE * outer_scale
    width_active = chip_w + chip_gap + len(entry_active_text) * header_font * 0.55
    width_held   = chip_w + chip_gap + len(entry_held_text) * header_font * 0.55
    total_w = width_active + width_held + inter_gap
    x_cursor = canvas_w / 2 - total_w / 2

    for is_held, label_text in ((False, entry_active_text), (True, entry_held_text)):
        ext = chip_w
        x_chip = x_cursor + ext / 2
        tint = SANSKRIT_TINT_FADED if is_held else SANSKRIT_TINT
        stroke_attr = (
            f' stroke="#9a9384" stroke-width="{0.011 * outer_scale:.4f}" '
            f'stroke-dasharray="{0.040 * outer_scale:.4f} {0.030 * outer_scale:.4f}"'
            if is_held else ' stroke="none"'
        )
        letter_color = LETTER_COLOR_FADED if is_held else palette["data"]
        body.append(
            f'  <rect x="{x_chip - chip_w/2:.4f}" y="{legend_y - chip_h/2:.4f}" '
            f'width="{chip_w:.4f}" height="{chip_h:.4f}" rx="{chip_rx:.4f}" '
            f'fill="{tint}"{stroke_attr} />\n'
            f'  <text x="{x_chip:.4f}" y="{legend_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{chip_dev_font:.4f}" '
            f'fill="{letter_color}" font-family="{DEVANAGARI_FONT}">'
            f'क</text>\n'
        )
        x_text = x_chip + ext / 2 + chip_gap
        body.append(
            f'  <text x="{x_text:.4f}" y="{legend_y + 0.046 * outer_scale:.4f}" '
            f'font-size="{header_font:.4f}" fill="{palette["data"]}" '
            f'font-family="{font}">{_xml_escape(label_text)}</text>\n'
        )
        x_cursor += (width_active if not is_held else width_held) + inter_gap

    # ---- Sanskrit heading for the place axis ----
    band_top = top_margin_s + title_h_s + subtitle_h_s + legend_h_s
    body.append(
        f'  <text x="{matrix_left + matrix_w / 2:.4f}" '
        f'y="{band_top + band_h_s * 0.58:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{band_font:.4f}" fill="{palette["group_arc"]}" '
        f'font-family="{font}"><tspan font-family="{DEVANAGARI_FONT}">स्थान</tspan> '
        f'<tspan font-style="italic">(sthāna)</tspan> · where the sound is made</text>\n'
    )

    # ---- Column headers: Sanskrit place first, English translation below ----
    header_y = matrix_top - col_header_h_s / 2 + 0.02 * outer_scale
    body.append(
        f'  <text x="{matrix_left - 0.12 * outer_scale:.4f}" '
        f'y="{header_y - 0.052 * outer_scale:.4f}" '
        f'text-anchor="end" dominant-baseline="middle" '
        f'font-size="{row_font:.4f}" fill="{palette["data"]}" '
        f'font-family="{DEVANAGARI_FONT}">प्रयत्न</text>\n'
        f'  <text x="{matrix_left - 0.12 * outer_scale:.4f}" '
        f'y="{header_y + 0.070 * outer_scale:.4f}" '
        f'text-anchor="end" dominant-baseline="middle" '
        f'font-size="{caption_font:.4f}" fill="{palette["group_arc"]}" '
        f'font-family="{font}">prayatna</text>\n'
    )
    for i, (_, devanagari, english) in enumerate(STHANA_COLUMNS):
        x = matrix_left + (i + 0.5) * cell_w
        body.append(
            f'  <text x="{x:.4f}" y="{header_y - 0.052 * outer_scale:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{row_font:.4f}" fill="{palette["data"]}" '
            f'font-family="{DEVANAGARI_FONT}">{devanagari}</text>\n'
            f'  <text x="{x:.4f}" y="{header_y + 0.070 * outer_scale:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{caption_font:.4f}" fill="{palette["group_arc"]}" '
            f'font-family="{font}">{english}</text>\n'
        )

    # ---- Cell tints (active + faded) ----
    for col, manner_row in sorted(matrix_cells):
        vrow = row_to_visible[manner_row]
        cx, cy = cell_center(col, vrow)
        is_held = manner_row in HELD_ROWS
        tint = SANSKRIT_TINT_FADED if is_held else SANSKRIT_TINT
        stroke_attr = (
            f' stroke="#9a9384" stroke-width="{held_stroke_w:.4f}" '
            f'stroke-dasharray="{0.040 * inner_scale_min:.4f} {0.030 * inner_scale_min:.4f}"'
            if is_held else ' stroke="none"'
        )
        body.append(
            f'  <rect x="{cx - sans_bg_w/2:.4f}" y="{cy - sans_bg_h/2:.4f}" '
            f'width="{sans_bg_w:.4f}" height="{sans_bg_h:.4f}" rx="{sans_bg_rx:.4f}" '
            f'fill="{tint}"{stroke_attr} />\n'
        )

    # ---- Grid lines (subtle) ----
    grid_color = "#dcdad4"
    grid_w = 0.005 * outer_scale
    for i in range(n_cols + 1):
        x = matrix_left + i * cell_w
        body.append(
            f'  <line x1="{x:.4f}" y1="{matrix_top:.4f}" '
            f'x2="{x:.4f}" y2="{matrix_top + matrix_h:.4f}" '
            f'stroke="{grid_color}" stroke-width="{grid_w:.4f}" />\n'
        )
    for i in range(n_rows + 1):
        y = matrix_top + i * cell_h
        body.append(
            f'  <line x1="{matrix_left:.4f}" y1="{y:.4f}" '
            f'x2="{matrix_left + matrix_w:.4f}" y2="{y:.4f}" '
            f'stroke="{grid_color}" stroke-width="{grid_w:.4f}" />\n'
        )

    # ---- Row labels: Sanskrit prayatna categories, then English gloss ----
    label_x = matrix_left - 0.12 * outer_scale
    for row_key in rows_used:
        i = row_to_visible[row_key]
        y = matrix_top + (i + 0.5) * cell_h
        devanagari, english = ROW_LABELS[row_key]
        is_held_row = row_key in HELD_ROWS
        label_color = LETTER_COLOR_FADED if is_held_row else palette["data"]
        body.append(
            f'  <text x="{label_x:.4f}" y="{y - 0.057 * outer_scale:.4f}" '
            f'text-anchor="end" dominant-baseline="middle" '
            f'font-size="{row_font:.4f}" fill="{label_color}" '
            f'font-family="{DEVANAGARI_FONT}">{devanagari}</text>\n'
            f'  <text x="{label_x:.4f}" y="{y + 0.073 * outer_scale:.4f}" '
            f'text-anchor="end" dominant-baseline="middle" '
            f'font-size="{caption_font:.4f}" fill="{label_color}" '
            f'font-family="{font}">{english}</text>\n'
        )

    # ---- Devanāgarī letters in cells ----
    for (col, manner_row), sym in sorted(matrix_symbols.items()):
        if (col, manner_row) not in matrix_cells:
            continue
        vrow = row_to_visible[manner_row]
        cx, cy = cell_center(col, vrow)
        is_held = manner_row in HELD_ROWS
        letter_color = LETTER_COLOR_FADED if is_held else palette["data"]
        body.append(
            f'  <text x="{cx:.4f}" y="{cy:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{dev_font_in_cell:.4f}" '
            f'fill="{letter_color}" font-family="{DEVANAGARI_FONT}">'
            f'{_xml_escape(sym)}</text>\n'
        )

    # ---- Caption ----
    cap_y = matrix_top + matrix_h + caption_h_s / 2 + 0.10 * outer_scale
    body.append(
        f'  <text x="{canvas_w/2:.4f}" y="{cap_y:.4f}" '
        f'text-anchor="middle" font-size="{caption_font:.4f}" font-style="italic" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'Filled tile = reusable base cell; faded tile + dashed outline = '
        f'<tspan font-family="{DEVANAGARI_FONT}" font-style="normal">महाप्राण</tspan> set aside for §8.7.</text>\n'
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


def main() -> int:
    svg = render()
    out = Path(__file__).resolve().parent / "sanskrit_base_before_mahaprana.from-py.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
