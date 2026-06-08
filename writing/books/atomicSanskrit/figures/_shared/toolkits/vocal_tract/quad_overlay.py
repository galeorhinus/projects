"""Quad-overlay — four-language place × manner-union matrix.

Each lit cell uses its four corners — one language per corner — so the
four inventories co-exist in one cell without obscuring each other:

  Sanskrit (role "tl")  — TOP-LEFT     · cell-tint tile + Devanāgarī letter
  Second   (role "tr")  — TOP-RIGHT    · hollow outlined square
  Third    (role "bl")  — BOTTOM-LEFT  · solid filled circle
  Fourth   (role "br")  — BOTTOM-RIGHT · hollow outlined ring

Sanskrit always sits at "tl"; the other three languages are
interchangeable in the spec but the shape-coding stays constant
(square / dot / ring) across every figure that uses this idiom.

Used by Ch 8 subcontinental sound-field figures (filename format
``sk_<l2>_<l3>_<l4>.py`` — Sanskrit is always the constant tl
language so it stays implicit in the filename's ``sk_`` prefix):

  - sk_tamil_toda_kurukh.py            Southern Survey
  - sk_korku_mundari_santali.py        Munda Survey
  - sk_korku_mundari_ho.py             Forest-Belt Survey
  - sk_korku_mundari_burushaski.py     Mixed Control
  - sk_sora_khasi_nicobarese.py        Dispersed Survey
  - sk_english_arabic_farsi.py         External Comparison

The figure self-titles using the spec's ``set_name`` plus the
dynamically computed "{covered} of {total} Sanskrit Base Coordinates"
count, and self-subtitles with the actual unfilled Devanāgarī letters.

Two layout formats — auto-selected by column count:
  - INDIC  (≤7 place columns) — 5.35″ intrinsic, 0.55″ cells, scales
    to 4.5″ at display (× 0.841).  All subcontinental surveys.
  - COMPACT (>7 place columns) — 4.5″ intrinsic (no scaling at display),
    cell width auto-sized to fit, outer fonts × 0.841 so the rendered
    pt sizes match the Indic figures' rendered pt sizes when both are
    displayed at 4.5″ wide.  All external / Iranian / Caucasus /
    Central-Asian surveys.

The auto-detect keeps every figure rendering at consistent pt sizes
when embedded at 4.5″ wide in the manuscript.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from _shared.toolkits.vocal_tract.overlay import (
    MANNERS, MANNER_DISPLAY, PLACE_ABBR, ARTICULATOR_GROUPS,
    harmonize, strip_cells,
    _polished_color_palette, _xml_escape,
)
from _shared.toolkits.vocal_tract import CONFIGS_DIR


# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------

@dataclass
class QuadOverlaySpec:
    set_name: str                              # e.g. "Southern Survey"
    languages: list[tuple[str, str, str]]      # (slug, display_label, role)
    strip_presets: list[str] = field(default_factory=lambda: ["mahaprana"])
    selected_places: list[int] | None = None   # None → auto-detect from data


# ---------------------------------------------------------------------------
# INDIC-FORMAT BASELINE CONSTANTS
# ---------------------------------------------------------------------------
# These are the dimensions for a 7-column figure rendering at 5.35″
# intrinsic width.  Compact-format figures are computed by scaling the
# outer dimensions by OUTER_COMPACT_SCALE and shrinking the cell to fit
# the 4.5″ target canvas; cell internals scale with cell-vs-baseline.

# Cell geometry
CELL = 0.55                # cell side, in — baseline (Indic format)

# Margins / row label
ROW_LABEL_W = 1.10
TITLE_H = 0.32
SUBTITLE_H = 0.26
COL_HEADER_H = 0.40
GROUP_BAND_H = 0.32
LEGEND_H = 0.42
CAPTION_H = 0.32
TOP_MARGIN = 0.18
BOTTOM_MARGIN = 0.16
LEFT_MARGIN = 0.18
RIGHT_MARGIN = 0.22

# Four-corner cell-content offsets — baseline (clustered toward centre)
ROSETTE_TL = (-0.100, -0.100)
ROSETTE_TR = (+0.100, -0.100)
ROSETTE_BL = (-0.100, +0.100)
ROSETTE_BR = (+0.100, +0.100)

# Sanskrit Devanāgarī letter — baseline font size
DEVANAGARI_FONT_SIZE = 0.149
DEVANAGARI_FONT = (
    "'Adobe Devanagari', 'Noto Sans Devanagari', "
    "'Mangal', 'Kohinoor Devanagari', serif"
)

# Sanskrit cell-tint rounded rectangle — baseline dimensions
SANSKRIT_BG_SIDE = 0.42
SANSKRIT_BG_RX = 0.06
SANSKRIT_TINT = "#e6e3db"

# Corner-mark sizes — baseline
TR_SQUARE_SIDE = 0.082
BL_R = 0.042
BR_R = 0.042

# Outer font sizes — baseline (9 pt at 4.5″ display)
TITLE_FONT_SIZE = 0.180
SUBTITLE_FONT_SIZE = 0.132
HEADER_FONT_SIZE = 0.132
PILL_FONT_SIZE = 0.149
ROW_FONT_SIZE = 0.149
CAPTION_FONT_SIZE = 0.122
BAND_FONT_SIZE = 0.108

# Pill (column header) dimensions — baseline
PILL_H = 0.32
PILL_RX = 0.035

# Stroke widths — baseline
TR_STROKE_WIDTH = 0.012
BR_STROKE_WIDTH = 0.011
SANSKRIT_OUTLINE_STROKE = 0.013

# Display-order override for manner rows — nasal hoisted to
# immediately-after-voiced-stop so the matrix reads in varṇamālā
# order (each sparśa-varga closes with its nasal, then affricates,
# then ūṣma).
MANNER_DISPLAY_ORDER = {
    0: 0,                  # voiceless_unasp_stop
    1: 1,                  # voiceless_asp_stop  (stripped via mahāprāṇa)
    2: 2,                  # voiced_unasp_stop
    3: 3,                  # voiced_asp_stop     (stripped via mahāprāṇa)
    9: 4,                  # nasal — hoisted immediately below voiced stop
    4: 5,                  # ejective_stop
    5: 6,                  # voiceless_affricate
    6: 7,                  # voiced_affricate
    7: 8,                  # voiceless_fricative
    8: 9,                  # voiced_fricative
    10: 10, 11: 11, 12: 12,
}

# Canvas layout — every figure ships at 4.5" intrinsic width.
# Row height stays at the baseline (CELL × OUTER_SCALE) so cells become
# tall rectangles when columns get tight; only if the natural canvas
# height would exceed MAX_CANVAS_H does the row height compress to fit.
INDIC_CANVAS_W = 5.35              # baseline 7-col canvas (legacy reference)
TARGET_CANVAS_W = 4.5              # every figure renders at exactly this width
MAX_CANVAS_H    = 6.5              # cap on canvas height — compress rows beyond this
OUTER_SCALE     = TARGET_CANVAS_W / INDIC_CANVAS_W   # ≈ 0.841 — used to pre-scale
                                                    # outer fonts + margins so the
                                                    # rendered pt sizes match the
                                                    # original Indic look at 4.5"

# In-cell Devanāgarī font, in pt, by column count.  Editorial choice —
# the natural proportional scaling makes the 12-column letters
# unreadably small; these values trade strict proportionality for
# legibility while still shrinking as columns crowd.  Since canvas is
# 4.5" intrinsic = 4.5" embedded, SVG inches and rendered inches are
# the same here (pt = SVG-inch × 72).
DEV_FONT_PT_BY_NCOLS: dict[int, float] = {
    7:  11.0,
    9:  10.0,
    10:  9.5,
    11:  9.5,
}


def _dev_font_in_cell_pt(n_cols: int) -> float:
    """Return the in-cell Devanāgarī font size in pt for ``n_cols``.

    Exact match from DEV_FONT_PT_BY_NCOLS when present; otherwise
    linear interpolation between bracketing entries, clamped at the
    endpoints of the table.
    """
    if n_cols in DEV_FONT_PT_BY_NCOLS:
        return DEV_FONT_PT_BY_NCOLS[n_cols]
    keys = sorted(DEV_FONT_PT_BY_NCOLS.keys())
    if n_cols <= keys[0]:
        return DEV_FONT_PT_BY_NCOLS[keys[0]]
    if n_cols >= keys[-1]:
        return DEV_FONT_PT_BY_NCOLS[keys[-1]]
    for lo, hi in zip(keys, keys[1:]):
        if lo <= n_cols <= hi:
            y0 = DEV_FONT_PT_BY_NCOLS[lo]
            y1 = DEV_FONT_PT_BY_NCOLS[hi]
            return y0 + (y1 - y0) * (n_cols - lo) / (hi - lo)
    return DEV_FONT_PT_BY_NCOLS[keys[-1]]    # unreachable, but typed-safe


# Mark-to-font proportions — preserve the baseline ratio so the square
# and circles keep visual parity with the Devanāgarī letter regardless
# of column count.
MARK_TO_DEV_RATIO_TR = TR_SQUARE_SIDE / DEVANAGARI_FONT_SIZE   # ≈ 0.55
MARK_TO_DEV_RATIO_BL = (2 * BL_R) / DEVANAGARI_FONT_SIZE       # ≈ 0.56 (diameter / font)
MARK_TO_DEV_RATIO_BR = (2 * BR_R) / DEVANAGARI_FONT_SIZE       # ≈ 0.56


# ---------------------------------------------------------------------------
# Row-label split helper
# ---------------------------------------------------------------------------

def _split_row_label(text: str) -> list[str]:
    if " (" in text:
        head, _, tail = text.partition(" ")
        return [head, tail]
    if " / " in text:
        a, b = text.split(" / ", 1)
        return [a, "/ " + b]
    if " " in text:
        head, _, tail = text.partition(" ")
        return [head, tail]
    return [text]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _load_language_data(spec: QuadOverlaySpec):
    """Returns (cells_list, labels, roles, sanskrit_symbols)."""
    cells_list: list[set[tuple[int, int]]] = []
    labels: list[str] = []
    roles: list[str] = []
    sanskrit_symbols: dict[tuple[int, int], str] = {}
    for slug, label, role in spec.languages:
        cfg = json.loads((CONFIGS_DIR / f"scatter_{slug}.json").read_text())
        cells, symbols, unc = harmonize(cfg["scatter"]["matrix"])
        if unc:
            print(f"  warn: unclassified symbols in {slug}: {unc[:5]}")
        cells = strip_cells(cells, spec.strip_presets)
        cells_list.append(cells)
        labels.append(label)
        roles.append(role)
        if slug == "sanskrit":
            sanskrit_symbols = {key: sym for key, sym in symbols.items()
                                if key in cells}
    return cells_list, labels, roles, sanskrit_symbols


def _resolve_selected_places(cells_list, override) -> list[int]:
    if override is not None:
        return list(override)
    return sorted({p for cs in cells_list for (p, _) in cs})


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------

def render_quad_overlay(spec: QuadOverlaySpec) -> str:
    cells_list, labels, roles, sanskrit_symbols = _load_language_data(spec)
    selected_places = _resolve_selected_places(cells_list, spec.selected_places)
    return _render_svg(spec, cells_list, labels, roles,
                       sanskrit_symbols, selected_places)


def _render_svg(spec: QuadOverlaySpec,
                cells_list: list[set[tuple[int, int]]],
                labels: list[str],
                roles: list[str],
                sanskrit_symbols: dict[tuple[int, int], str],
                selected_places: list[int]) -> str:
    palette = _polished_color_palette()
    font = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

    # ---- Filter cells to selected places + remap columns ----
    place_to_col = {p: i for i, p in enumerate(selected_places)}
    matrix_cells = [
        {(place_to_col[p], m) for (p, m) in cs if p in place_to_col}
        for cs in cells_list
    ]

    # ---- Manner-row compaction ----
    union = set().union(*matrix_cells)
    rows_used = sorted(
        {m for (_, m) in union},
        key=lambda m: MANNER_DISPLAY_ORDER.get(m, m),
    )
    n_cols = len(selected_places)
    n_rows = len(rows_used)
    row_to_visible = {m: i for i, m in enumerate(rows_used)}

    # ---- Layout: always 4.5" wide; cells become tall rectangles when
    # columns are tight; rows compress only if canvas would exceed 6.5".
    outer_scale = OUTER_SCALE
    scaled_left = LEFT_MARGIN * outer_scale
    scaled_right = RIGHT_MARGIN * outer_scale
    scaled_row_label_w = ROW_LABEL_W * outer_scale

    # Cell width fits the matrix into 4.5" canvas
    matrix_w_target = TARGET_CANVAS_W - scaled_left - scaled_row_label_w - scaled_right
    cell_w = matrix_w_target / n_cols

    # Row height — baseline equals the Indic cell at 4.5"-rendered size
    # (0.55 × outer_scale).  Compress only if the natural canvas height
    # would exceed MAX_CANVAS_H.
    cell_h_baseline = CELL * outer_scale

    # Outer vertical overhead (everything above + below the matrix)
    outer_v_overhead = (TOP_MARGIN + TITLE_H + SUBTITLE_H + LEGEND_H
                        + GROUP_BAND_H + COL_HEADER_H + CAPTION_H
                        + BOTTOM_MARGIN) * outer_scale
    max_matrix_h = MAX_CANVAS_H - outer_v_overhead
    cell_h = min(cell_h_baseline, max_matrix_h / n_rows)

    # Independent x and y inner-scale factors — let cells be rectangular.
    inner_scale_w = cell_w / CELL
    inner_scale_h = cell_h / CELL
    inner_scale_min = min(inner_scale_w, inner_scale_h)   # for circles / squares
                                                          # that must stay round

    # Scaled outer layout dimensions
    title_h_s      = TITLE_H * outer_scale
    subtitle_h_s   = SUBTITLE_H * outer_scale
    legend_h_s     = LEGEND_H * outer_scale
    band_h_s       = GROUP_BAND_H * outer_scale
    col_header_h_s = COL_HEADER_H * outer_scale
    caption_h_s    = CAPTION_H * outer_scale
    top_margin_s   = TOP_MARGIN * outer_scale
    bottom_margin_s = BOTTOM_MARGIN * outer_scale

    # Scaled outer font sizes
    title_font    = TITLE_FONT_SIZE * outer_scale
    subtitle_font = SUBTITLE_FONT_SIZE * outer_scale
    header_font   = HEADER_FONT_SIZE * outer_scale
    pill_font     = PILL_FONT_SIZE * outer_scale
    row_font      = ROW_FONT_SIZE * outer_scale
    caption_font  = CAPTION_FONT_SIZE * outer_scale
    band_font     = BAND_FONT_SIZE * outer_scale

    # Pill dimensions — height scales with outer; width tied to cell_w
    # so the pill aligns with its column without overflowing.
    pill_h = PILL_H * outer_scale
    pill_rx = PILL_RX * outer_scale
    pill_w = min(0.42 * outer_scale, cell_w * 0.85)

    # Cell-internal sizes.  Devanāgarī uses an explicit per-n_cols
    # lookup (editorial — strict proportional shrink makes the 12-col
    # letter unreadably small).  Marks (square, dot, ring) scale from
    # Devanāgarī via the baseline ratios so the visual parity between
    # letter and marks holds across every figure.  Tint matches cell
    # aspect (rectangular when cell is tall); rosette offsets split x
    # by inner_scale_w, y by inner_scale_h so corners spread evenly
    # inside the (possibly rectangular) cell.
    dev_font_in_cell = _dev_font_in_cell_pt(n_cols) / 72       # SVG inches
    mark_scale = dev_font_in_cell / DEVANAGARI_FONT_SIZE       # vs baseline 0.149

    sans_bg_w = SANSKRIT_BG_SIDE * inner_scale_w
    sans_bg_h = SANSKRIT_BG_SIDE * inner_scale_h
    sans_bg_rx = SANSKRIT_BG_RX * inner_scale_min
    tr_side = MARK_TO_DEV_RATIO_TR * dev_font_in_cell
    bl_r    = (MARK_TO_DEV_RATIO_BL * dev_font_in_cell) / 2
    br_r    = (MARK_TO_DEV_RATIO_BR * dev_font_in_cell) / 2
    ros_tl = (ROSETTE_TL[0] * inner_scale_w, ROSETTE_TL[1] * inner_scale_h)
    ros_tr = (ROSETTE_TR[0] * inner_scale_w, ROSETTE_TR[1] * inner_scale_h)
    ros_bl = (ROSETTE_BL[0] * inner_scale_w, ROSETTE_BL[1] * inner_scale_h)
    ros_br = (ROSETTE_BR[0] * inner_scale_w, ROSETTE_BR[1] * inner_scale_h)
    tr_stroke = TR_STROKE_WIDTH * mark_scale
    br_stroke = BR_STROKE_WIDTH * mark_scale
    sans_outline = SANSKRIT_OUTLINE_STROKE * inner_scale_min

    # ---- Coverage statistics (drives dynamic title + subtitle) ----
    sanskrit_idx = roles.index("tl")
    other_union: set[tuple[int, int]] = set()
    for idx, role in enumerate(roles):
        if role != "tl":
            other_union |= matrix_cells[idx]
    unfilled = matrix_cells[sanskrit_idx] - other_union
    total_sanskrit = len(matrix_cells[sanskrit_idx])
    covered = total_sanskrit - len(unfilled)

    unfilled_letters: list[str] = []
    for col, manner_row in sorted(
        unfilled, key=lambda c: (MANNER_DISPLAY_ORDER.get(c[1], c[1]), c[0])
    ):
        orig_col = selected_places[col]
        sym = sanskrit_symbols.get((orig_col, manner_row), "")
        if sym:
            unfilled_letters.append(sym)

    title_text = (
        f"{spec.set_name}: {covered} of {total_sanskrit} "
        f"Sanskrit Base Coordinates"
    )

    # ---- Canvas + matrix placement ----
    matrix_w = n_cols * cell_w
    matrix_h = n_rows * cell_h
    canvas_w = scaled_left + scaled_row_label_w + matrix_w + scaled_right
    canvas_h = (top_margin_s + title_h_s + subtitle_h_s + legend_h_s
                + band_h_s + col_header_h_s + matrix_h
                + caption_h_s + bottom_margin_s)
    matrix_left = scaled_left + scaled_row_label_w
    matrix_top = (top_margin_s + title_h_s + subtitle_h_s + legend_h_s
                  + band_h_s + col_header_h_s)

    def cell_center(matrix_col: int, visible_row: int) -> tuple[float, float]:
        return (matrix_left + (matrix_col + 0.5) * cell_w,
                matrix_top + (visible_row + 0.5) * cell_h)

    # ---- Inline cell-content renderers (capture scaled values) ----

    def render_sanskrit_tint(cx, cy, highlighted=False):
        w, h = sans_bg_w, sans_bg_h
        stroke_attr = (
            f' stroke="#9a9384" stroke-width="{sans_outline:.4f}"'
            if highlighted else ' stroke="none"'
        )
        return (
            f'  <rect x="{cx - w/2:.4f}" y="{cy - h/2:.4f}" '
            f'width="{w:.4f}" height="{h:.4f}" rx="{sans_bg_rx:.4f}" '
            f'fill="{SANSKRIT_TINT}"{stroke_attr} />\n'
        )

    def render_sanskrit_letter(cx, cy, symbol):
        x = cx + ros_tl[0]
        y = cy + ros_tl[1]
        return (
            f'  <text x="{x:.4f}" y="{y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{dev_font_in_cell:.4f}" '
            f'fill="{palette["data"]}" font-family="{DEVANAGARI_FONT}">'
            f'{_xml_escape(symbol)}</text>\n'
        )

    def render_tr_vertex(cx, cy):
        x = cx + ros_tr[0]
        y = cy + ros_tr[1]
        s = tr_side
        return (
            f'  <rect x="{x - s/2:.4f}" y="{y - s/2:.4f}" '
            f'width="{s:.4f}" height="{s:.4f}" '
            f'fill="none" stroke="{palette["data"]}" '
            f'stroke-width="{tr_stroke:.4f}" />\n'
        )

    def render_bl_vertex(cx, cy):
        x = cx + ros_bl[0]
        y = cy + ros_bl[1]
        return (
            f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{bl_r:.4f}" '
            f'fill="{palette["data"]}" />\n'
        )

    def render_br_vertex(cx, cy):
        x = cx + ros_br[0]
        y = cy + ros_br[1]
        return (
            f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{br_r:.4f}" '
            f'fill="none" stroke="{palette["data"]}" '
            f'stroke-width="{br_stroke:.4f}" />\n'
        )

    role_renderers = {
        "tr": render_tr_vertex,
        "bl": render_bl_vertex,
        "br": render_br_vertex,
    }

    # Legend chip — uses OUTER scaling (it's part of header / chrome,
    # not cell content).  Chip dimensions, glyph sizes, and the
    # Devanāgarī sample letter all scale with outer_scale.
    leg_chip_w = 0.26 * outer_scale
    leg_chip_h = 0.22 * outer_scale
    leg_chip_rx = 0.045 * outer_scale
    leg_chip_dev_font = DEVANAGARI_FONT_SIZE * outer_scale
    leg_tr_side = TR_SQUARE_SIDE * outer_scale
    leg_bl_r = BL_R * outer_scale
    leg_br_r = BR_R * outer_scale
    leg_tr_stroke = TR_STROKE_WIDTH * outer_scale
    leg_br_stroke = BR_STROKE_WIDTH * outer_scale

    def render_legend_chip(role, cx, cy):
        if role == "tl":
            return (
                f'  <rect x="{cx - leg_chip_w/2:.4f}" y="{cy - leg_chip_h/2:.4f}" '
                f'width="{leg_chip_w:.4f}" height="{leg_chip_h:.4f}" '
                f'rx="{leg_chip_rx:.4f}" '
                f'fill="{SANSKRIT_TINT}" stroke="none" />\n'
                f'  <text x="{cx:.4f}" y="{cy:.4f}" '
                f'text-anchor="middle" dominant-baseline="middle" '
                f'font-size="{leg_chip_dev_font:.4f}" '
                f'fill="{palette["data"]}" font-family="{DEVANAGARI_FONT}">'
                f'क</text>\n'
            )
        if role == "tr":
            return (
                f'  <rect x="{cx - leg_tr_side/2:.4f}" y="{cy - leg_tr_side/2:.4f}" '
                f'width="{leg_tr_side:.4f}" height="{leg_tr_side:.4f}" '
                f'fill="none" stroke="{palette["data"]}" '
                f'stroke-width="{leg_tr_stroke:.4f}" />\n'
            )
        if role == "bl":
            return (
                f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{leg_bl_r:.4f}" '
                f'fill="{palette["data"]}" />\n'
            )
        if role == "br":
            return (
                f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{leg_br_r:.4f}" '
                f'fill="none" stroke="{palette["data"]}" '
                f'stroke-width="{leg_br_stroke:.4f}" />\n'
            )
        raise ValueError(f"unknown legend role: {role}")

    def chip_extent(role):
        if role == "tl":   return leg_chip_w
        if role == "tr":   return leg_tr_side
        if role == "bl":   return 2 * leg_bl_r
        if role == "br":   return 2 * leg_br_r
        return 0.1

    # ============================================================
    # BUILD SVG BODY
    # ============================================================
    body: list[str] = []

    # ---- Background ----
    body.append(
        f'  <rect x="0" y="0" width="{canvas_w:.4f}" height="{canvas_h:.4f}" '
        f'fill="{palette["background"]}" />\n'
    )

    # ---- Title + subtitle ----
    title_y = top_margin_s + title_h_s / 2 + 0.04 * outer_scale
    body.append(
        f'  <text x="{canvas_w/2:.4f}" y="{title_y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{title_font:.4f}" font-weight="700" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'{_xml_escape(title_text)}</text>\n'
    )
    subtitle_y = top_margin_s + title_h_s + subtitle_h_s / 2 + 0.02 * outer_scale
    if unfilled_letters:
        unfilled_str = " · ".join(unfilled_letters)
        body.append(
            f'  <text x="{canvas_w/2:.4f}" y="{subtitle_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{subtitle_font:.4f}" font-style="italic" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'Mahāprāṇa rows held aside · Unfilled: '
            f'<tspan font-style="normal" font-family="{DEVANAGARI_FONT}">'
            f'{_xml_escape(unfilled_str)}</tspan></text>\n'
        )
    else:
        body.append(
            f'  <text x="{canvas_w/2:.4f}" y="{subtitle_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{subtitle_font:.4f}" font-style="italic" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'Mahāprāṇa rows held aside · '
            f'All Sanskrit base coordinates covered.</text>\n'
        )

    # ---- Sanskrit cell tints (below grid + corner marks) ----
    for col, manner_row in sorted(matrix_cells[sanskrit_idx]):
        vrow = row_to_visible[manner_row]
        cx, cy = cell_center(col, vrow)
        body.append(
            render_sanskrit_tint(
                cx, cy, highlighted=(col, manner_row) in unfilled
            )
        )

    # ---- Legend chips + labels ----
    legend_y = top_margin_s + title_h_s + subtitle_h_s + legend_h_s / 2
    chip_gap = 0.12 * outer_scale
    inter_gap = 0.30 * outer_scale
    entry_texts = [
        (f"{label} base shell" if role == "tl" else label)
        for label, role in zip(labels, roles)
    ]
    entry_widths = [
        chip_extent(roles[i]) + chip_gap + len(entry_texts[i]) * header_font * 0.55
        for i in range(len(labels))
    ]
    total_w = sum(entry_widths) + (len(labels) - 1) * inter_gap
    x_cursor = canvas_w / 2 - total_w / 2
    for i in range(len(labels)):
        ext = chip_extent(roles[i])
        x_chip = x_cursor + ext / 2
        body.append(render_legend_chip(roles[i], x_chip, legend_y))
        x_text = x_chip + ext / 2 + chip_gap
        body.append(
            f'  <text x="{x_text:.4f}" y="{legend_y + 0.046 * outer_scale:.4f}" '
            f'font-size="{header_font:.4f}" fill="{palette["data"]}" '
            f'font-family="{font}">{_xml_escape(entry_texts[i])}</text>\n'
        )
        x_cursor += entry_widths[i] + inter_gap

    # ---- Articulator-group bands ----
    band_top = top_margin_s + title_h_s + subtitle_h_s + legend_h_s
    band_y_baseline = band_top + band_h_s * 0.62
    band_line_y = band_top + band_h_s * 0.88
    band_stroke_w = 0.012 * outer_scale
    band_margin = 0.06 * outer_scale
    band_tick_h = 0.04 * outer_scale
    for group_name, group_cols in ARTICULATOR_GROUPS:
        spanned = [place_to_col[c] for c in group_cols if c in place_to_col]
        if not spanned:
            continue
        c_lo, c_hi = min(spanned), max(spanned)
        x_lo = matrix_left + c_lo * cell_w + band_margin
        x_hi = matrix_left + (c_hi + 1) * cell_w - band_margin
        x_mid = (x_lo + x_hi) / 2
        body.append(
            f'  <path d="M {x_lo:.4f} {band_line_y:.4f} '
            f'L {x_hi:.4f} {band_line_y:.4f}" '
            f'stroke="{palette["group_arc"]}" stroke-width="{band_stroke_w:.4f}" '
            f'stroke-linecap="round" />\n'
        )
        for x in (x_lo, x_hi):
            body.append(
                f'  <path d="M {x:.4f} {band_line_y:.4f} '
                f'L {x:.4f} {band_line_y - band_tick_h:.4f}" '
                f'stroke="{palette["group_arc"]}" stroke-width="{band_stroke_w:.4f}" />\n'
            )
        body.append(
            f'  <text x="{x_mid:.4f}" y="{band_y_baseline:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{band_font:.4f}" letter-spacing="{0.030 * outer_scale:.4f}" '
            f'fill="{palette["group_arc"]}" font-family="{font}">'
            f'{group_name}</text>\n'
        )

    # ---- Column headers: pill chips with place abbreviations ----
    pill_y = matrix_top - col_header_h_s / 2 + 0.02 * outer_scale
    # Pill font shrinks to fit pill_w if necessary (3-char abbreviation
    # needs roughly char_count × font × 0.55 ≤ pill_w with margin).
    pill_text_max = pill_w / (3.5 * 0.55)   # margin for 3-char abbreviations
    pill_font_eff = min(pill_font, pill_text_max)
    for col_orig in selected_places:
        i = place_to_col[col_orig]
        x = matrix_left + (i + 0.5) * cell_w
        body.append(
            f'  <rect x="{x - pill_w/2:.4f}" y="{pill_y - pill_h/2:.4f}" '
            f'width="{pill_w:.4f}" height="{pill_h:.4f}" rx="{pill_rx:.4f}" '
            f'fill="{palette["pill_fill"]}" stroke="none" />\n'
        )
        abbr = PLACE_ABBR.get(col_orig, str(col_orig + 1))
        body.append(
            f'  <text x="{x:.4f}" y="{pill_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{pill_font_eff:.4f}" letter-spacing="{0.012 * outer_scale:.4f}" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'{abbr}</text>\n'
        )

    # ---- Grid lines ----
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

    # ---- Row labels (manner names) ----
    line_offset = 0.092 * outer_scale
    label_x = matrix_left - 0.12 * outer_scale
    for row_idx in rows_used:
        i = row_to_visible[row_idx]
        y = matrix_top + (i + 0.5) * cell_h
        manner_name = MANNER_DISPLAY.get(MANNERS[row_idx], MANNERS[row_idx])
        lines = _split_row_label(manner_name)
        if len(lines) == 1:
            body.append(
                f'  <text x="{label_x:.4f}" y="{y:.4f}" '
                f'text-anchor="end" dominant-baseline="middle" '
                f'font-size="{row_font:.4f}" '
                f'fill="{palette["data"]}" font-family="{font}">'
                f'{_xml_escape(lines[0])}</text>\n'
            )
        else:
            for k, line in enumerate(lines):
                y_line = y + (k - 0.5) * 2 * line_offset
                body.append(
                    f'  <text x="{label_x:.4f}" y="{y_line:.4f}" '
                    f'text-anchor="end" dominant-baseline="middle" '
                    f'font-size="{row_font:.4f}" '
                    f'fill="{palette["data"]}" font-family="{font}">'
                    f'{_xml_escape(line)}</text>\n'
                )

    # ---- Corner marks (Sanskrit letter last, on top) ----
    for role in ("bl", "br", "tr"):
        try:
            lang_idx = roles.index(role)
        except ValueError:
            continue
        renderer = role_renderers[role]
        for col, manner_row in sorted(matrix_cells[lang_idx]):
            vrow = row_to_visible[manner_row]
            cx, cy = cell_center(col, vrow)
            body.append(renderer(cx, cy))

    for col, manner_row in sorted(matrix_cells[sanskrit_idx]):
        vrow = row_to_visible[manner_row]
        cx, cy = cell_center(col, vrow)
        orig_col = selected_places[col]
        symbol = sanskrit_symbols.get((orig_col, manner_row), "")
        if symbol:
            body.append(render_sanskrit_letter(cx, cy, symbol))

    # ---- Caption (corner key) ----
    role_to_label = {role: label for _, label, role in spec.languages}
    cap_y = matrix_top + matrix_h + caption_h_s / 2 + 0.10 * outer_scale
    caption_open = (
        f'  <text x="{canvas_w/2:.4f}" y="{cap_y:.4f}" '
        f'text-anchor="middle" font-size="{caption_font:.4f}" font-style="italic" '
        f'fill="{palette["data"]}" font-family="{font}">'
    )
    top_part = (
        f'Top row: {role_to_label.get("tl", "?")} '
        f'<tspan font-style="normal" font-family="{DEVANAGARI_FONT}">क</tspan>'
        f' · {role_to_label.get("tr", "?")} □'
    )
    bottom_part = (
        f'  ·  Bottom row: {role_to_label.get("bl", "?")} ●'
        f' · {role_to_label.get("br", "?")} ○.'
    )
    body.append(caption_open + top_part + bottom_part + '</text>\n')

    svg = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{canvas_w:.4f}in" height="{canvas_h:.4f}in" '
        f'viewBox="0 0 {canvas_w:.4f} {canvas_h:.4f}">\n'
        + "".join(body)
        + '</svg>\n'
    )
    return svg


def build_and_write(spec: QuadOverlaySpec, output_path: Path) -> int:
    """Render ``spec`` and write the SVG to ``output_path``.  Returns 0."""
    svg = render_quad_overlay(spec)
    output_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {output_path} ({len(svg)} bytes)")
    return 0
