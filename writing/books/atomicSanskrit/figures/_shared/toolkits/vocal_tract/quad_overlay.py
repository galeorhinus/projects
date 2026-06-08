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
# Layout constants
# ---------------------------------------------------------------------------

CELL = 0.55                # cell side, in
ROW_LABEL_W = 1.10         # row labels stack onto two lines
TITLE_H = 0.32             # bold display title
SUBTITLE_H = 0.26          # italic method-note
COL_HEADER_H = 0.40
GROUP_BAND_H = 0.32
LEGEND_H = 0.42
CAPTION_H = 0.32
TOP_MARGIN = 0.18
BOTTOM_MARGIN = 0.16
LEFT_MARGIN = 0.18
RIGHT_MARGIN = 0.22

# Four-corner offsets — clustered toward the cell centre (each mark
# ~0.10 from centre).  All four are centre-anchored, including the
# Devanāgarī letter.
ROSETTE_TL = (-0.100, -0.100)
ROSETTE_TR = (+0.100, -0.100)
ROSETTE_BL = (-0.100, +0.100)
ROSETTE_BR = (+0.100, +0.100)

# Sanskrit Devanāgarī letter (centre-anchored at ROSETTE_TL).
# 0.149 in × ~60.6 ≈ 9 pt when the figure renders at ~4.5" wide.
DEVANAGARI_FONT_SIZE = 0.149
DEVANAGARI_FONT = (
    "'Adobe Devanagari', 'Noto Sans Devanagari', "
    "'Mangal', 'Kohinoor Devanagari', serif"
)

# Sanskrit cell-tint rounded rectangle, slightly smaller than the cell.
SANSKRIT_BG_SIDE = 0.42
SANSKRIT_BG_RX = 0.06
SANSKRIT_TINT = "#e6e3db"

# Corner-mark sizes
TR_SQUARE_SIDE = 0.082    # hollow square (role "tr")
BL_R = 0.042              # solid circle  (role "bl")
BR_R = 0.042              # hollow ring   (role "br")

# Display-order override for manner rows — nasal hoisted to
# immediately-after-voiced-stop so the matrix reads in varṇamālā
# order (each sparśa-varga closes with its nasal, then affricates,
# then ūṣma).  When the input set carries affricates (External
# Comparison, Mixed Control), the nasal still sits directly under
# the voiced stop rather than being displaced below the affricate row.
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

# Corner key (for the bottom caption)
CORNER_LABEL = {"tl": "top-left", "tr": "top-right",
                "bl": "bottom-left", "br": "bottom-right"}
CORNER_GLYPH = {"tl": "क", "tr": "□", "bl": "●", "br": "○"}


# ---------------------------------------------------------------------------
# Corner renderers (data cells)
# ---------------------------------------------------------------------------

def _render_sanskrit_tint(cx: float, cy: float, highlighted: bool = False) -> str:
    """Rounded-rect tile beneath Sanskrit-lit cells.

    ``highlighted=True`` adds a thin darker outline for Sanskrit-only
    base coordinates that no other language in this overlay covers.
    """
    s = SANSKRIT_BG_SIDE
    stroke_attr = (
        ' stroke="#9a9384" stroke-width="0.013"' if highlighted else ' stroke="none"'
    )
    return (
        f'  <rect x="{cx - s/2:.4f}" y="{cy - s/2:.4f}" '
        f'width="{s}" height="{s}" rx="{SANSKRIT_BG_RX}" '
        f'fill="{SANSKRIT_TINT}"{stroke_attr} />\n'
    )


def _render_sanskrit_letter(cx: float, cy: float, symbol: str, palette: dict) -> str:
    x, y = cx + ROSETTE_TL[0], cy + ROSETTE_TL[1]
    return (
        f'  <text x="{x:.4f}" y="{y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{DEVANAGARI_FONT_SIZE}" '
        f'fill="{palette["data"]}" font-family="{DEVANAGARI_FONT}">'
        f'{_xml_escape(symbol)}</text>\n'
    )


def _render_tr_vertex(cx: float, cy: float, palette: dict) -> str:
    x, y = cx + ROSETTE_TR[0], cy + ROSETTE_TR[1]
    s = TR_SQUARE_SIDE
    return (
        f'  <rect x="{x - s/2:.4f}" y="{y - s/2:.4f}" '
        f'width="{s}" height="{s}" '
        f'fill="none" stroke="{palette["data"]}" stroke-width="0.012" />\n'
    )


def _render_bl_vertex(cx: float, cy: float, palette: dict) -> str:
    x, y = cx + ROSETTE_BL[0], cy + ROSETTE_BL[1]
    return (
        f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{BL_R}" '
        f'fill="{palette["data"]}" />\n'
    )


def _render_br_vertex(cx: float, cy: float, palette: dict) -> str:
    x, y = cx + ROSETTE_BR[0], cy + ROSETTE_BR[1]
    return (
        f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{BR_R}" '
        f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" />\n'
    )


_ROLE_RENDERERS = {
    "tl": None,                # special-cased — needs per-cell symbol
    "tr": _render_tr_vertex,
    "bl": _render_bl_vertex,
    "br": _render_br_vertex,
}


# ---------------------------------------------------------------------------
# Legend chip renderers
# ---------------------------------------------------------------------------

def _render_legend_chip(role: str, cx: float, cy: float, palette: dict) -> str:
    if role == "tl":
        w, h, rx = 0.26, 0.22, 0.045
        return (
            f'  <rect x="{cx - w/2:.4f}" y="{cy - h/2:.4f}" '
            f'width="{w}" height="{h}" rx="{rx}" '
            f'fill="{SANSKRIT_TINT}" stroke="none" />\n'
            f'  <text x="{cx:.4f}" y="{cy:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{DEVANAGARI_FONT_SIZE}" '
            f'fill="{palette["data"]}" font-family="{DEVANAGARI_FONT}">'
            f'क</text>\n'
        )
    if role == "tr":
        s = TR_SQUARE_SIDE
        return (
            f'  <rect x="{cx - s/2:.4f}" y="{cy - s/2:.4f}" '
            f'width="{s}" height="{s}" '
            f'fill="none" stroke="{palette["data"]}" stroke-width="0.012" />\n'
        )
    if role == "bl":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{BL_R}" '
            f'fill="{palette["data"]}" />\n'
        )
    if role == "br":
        return (
            f'  <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{BR_R}" '
            f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" />\n'
        )
    raise ValueError(f"unknown legend role: {role}")


def _chip_extent(role: str) -> float:
    if role == "tl":   return 0.26       # Sanskrit tile (tint + क)
    if role == "tr":   return TR_SQUARE_SIDE
    if role == "bl":   return 2 * BL_R
    if role == "br":   return 2 * BR_R
    return 0.1


# ---------------------------------------------------------------------------
# Row-label split helper (manner names render on up to two lines)
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
    # Auto: union of place columns lit by any of the four languages.
    return sorted({p for cs in cells_list for (p, _) in cs})


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------

def render_quad_overlay(spec: QuadOverlaySpec) -> str:
    """Build and return the SVG for ``spec``."""
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

    # 1. Filter cells to selected places + remap to matrix-column indices.
    place_to_col = {p: i for i, p in enumerate(selected_places)}
    matrix_cells = [
        {(place_to_col[p], m) for (p, m) in cs if p in place_to_col}
        for cs in cells_list
    ]

    # 2. Manner-row compaction across union of all four languages' cells.
    union = set().union(*matrix_cells)
    rows_used = sorted(
        {m for (_, m) in union},
        key=lambda m: MANNER_DISPLAY_ORDER.get(m, m),
    )
    n_cols = len(selected_places)
    n_rows = len(rows_used)
    row_to_visible = {m: i for i, m in enumerate(rows_used)}

    # 3. Coverage statistics (drives dynamic title + subtitle).
    sanskrit_idx = roles.index("tl")
    other_union: set[tuple[int, int]] = set()
    for idx, role in enumerate(roles):
        if role != "tl":
            other_union |= matrix_cells[idx]
    unfilled = matrix_cells[sanskrit_idx] - other_union
    total_sanskrit = len(matrix_cells[sanskrit_idx])
    covered = total_sanskrit - len(unfilled)

    # Devanāgarī letters for unfilled cells, in MANNER_DISPLAY_ORDER then
    # place-column order — so the subtitle reads in a sensible sequence.
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

    # 4. Canvas + matrix placement.
    matrix_w = n_cols * CELL
    matrix_h = n_rows * CELL
    canvas_w = LEFT_MARGIN + ROW_LABEL_W + matrix_w + RIGHT_MARGIN
    canvas_h = (TOP_MARGIN + TITLE_H + SUBTITLE_H + LEGEND_H
                + GROUP_BAND_H + COL_HEADER_H + matrix_h
                + CAPTION_H + BOTTOM_MARGIN)
    matrix_left = LEFT_MARGIN + ROW_LABEL_W
    matrix_top = (TOP_MARGIN + TITLE_H + SUBTITLE_H + LEGEND_H
                  + GROUP_BAND_H + COL_HEADER_H)

    def cell_center(matrix_col: int, visible_row: int) -> tuple[float, float]:
        return (matrix_left + (matrix_col + 0.5) * CELL,
                matrix_top + (visible_row + 0.5) * CELL)

    body: list[str] = []

    # ---- Background ----
    body.append(
        f'  <rect x="0" y="0" width="{canvas_w:.4f}" height="{canvas_h:.4f}" '
        f'fill="{palette["background"]}" />\n'
    )

    # ---- Title + subtitle ----
    title_y = TOP_MARGIN + TITLE_H / 2 + 0.04
    body.append(
        f'  <text x="{canvas_w/2:.4f}" y="{title_y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="0.180" font-weight="700" '
        f'fill="{palette["data"]}" font-family="{font}">'
        f'{_xml_escape(title_text)}</text>\n'
    )
    subtitle_y = TOP_MARGIN + TITLE_H + SUBTITLE_H / 2 + 0.02
    if unfilled_letters:
        # Mixed Latin + Devanāgarī.  The Devanāgarī letters need an
        # explicit Devanāgarī-aware font via a tspan so they render
        # correctly even when the serif primary lacks the script.
        unfilled_str = " · ".join(unfilled_letters)
        body.append(
            f'  <text x="{canvas_w/2:.4f}" y="{subtitle_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="0.132" font-style="italic" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'Mahāprāṇa rows held aside · Unfilled: '
            f'<tspan font-style="normal" font-family="{DEVANAGARI_FONT}">'
            f'{_xml_escape(unfilled_str)}</tspan></text>\n'
        )
    else:
        body.append(
            f'  <text x="{canvas_w/2:.4f}" y="{subtitle_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="0.132" font-style="italic" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'Mahāprāṇa rows held aside · '
            f'All Sanskrit base coordinates covered.</text>\n'
        )

    # ---- Sanskrit cell tints ----
    for col, manner_row in sorted(matrix_cells[sanskrit_idx]):
        vrow = row_to_visible[manner_row]
        cx, cy = cell_center(col, vrow)
        body.append(
            _render_sanskrit_tint(
                cx, cy, highlighted=(col, manner_row) in unfilled
            )
        )

    # ---- Header row: language chips + labels ----
    legend_y = TOP_MARGIN + TITLE_H + SUBTITLE_H + LEGEND_H / 2
    header_font = 0.132
    chip_gap = 0.12
    inter_gap = 0.30
    entry_texts = [
        (f"{label} base shell" if role == "tl" else label)
        for label, role in zip(labels, roles)
    ]
    entry_widths = [
        _chip_extent(roles[i]) + chip_gap + len(entry_texts[i]) * header_font * 0.55
        for i in range(len(labels))
    ]
    total_w = sum(entry_widths) + (len(labels) - 1) * inter_gap
    x_cursor = canvas_w / 2 - total_w / 2
    for i in range(len(labels)):
        ext = _chip_extent(roles[i])
        x_chip = x_cursor + ext / 2
        body.append(_render_legend_chip(roles[i], x_chip, legend_y, palette))
        x_text = x_chip + ext / 2 + chip_gap
        body.append(
            f'  <text x="{x_text:.4f}" y="{legend_y + 0.046:.4f}" '
            f'font-size="{header_font}" fill="{palette["data"]}" '
            f'font-family="{font}">{_xml_escape(entry_texts[i])}</text>\n'
        )
        x_cursor += entry_widths[i] + inter_gap

    # ---- Articulator-group bands ----
    band_top = TOP_MARGIN + TITLE_H + SUBTITLE_H + LEGEND_H
    band_y_baseline = band_top + GROUP_BAND_H * 0.62
    band_line_y = band_top + GROUP_BAND_H * 0.88
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
            f'font-size="0.108" letter-spacing="0.030" '
            f'fill="{palette["group_arc"]}" font-family="{font}">'
            f'{group_name}</text>\n'
        )

    # ---- Column headers: pill chips with place abbreviations ----
    pill_y = matrix_top - COL_HEADER_H / 2 + 0.02
    pill_w, pill_h, pill_r = 0.42, 0.32, 0.035
    pill_font = 0.149
    for col_orig in selected_places:
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

    # ---- Row labels (manner names) — two-line stacked ----
    row_font = 0.149
    line_offset = 0.092
    label_x = matrix_left - 0.12
    for row_idx in rows_used:
        i = row_to_visible[row_idx]
        y = matrix_top + (i + 0.5) * CELL
        manner_name = MANNER_DISPLAY.get(MANNERS[row_idx], MANNERS[row_idx])
        lines = _split_row_label(manner_name)
        if len(lines) == 1:
            body.append(
                f'  <text x="{label_x:.4f}" y="{y:.4f}" '
                f'text-anchor="end" dominant-baseline="middle" '
                f'font-size="{row_font}" '
                f'fill="{palette["data"]}" font-family="{font}">'
                f'{_xml_escape(lines[0])}</text>\n'
            )
        else:
            for k, line in enumerate(lines):
                y_line = y + (k - 0.5) * 2 * line_offset
                body.append(
                    f'  <text x="{label_x:.4f}" y="{y_line:.4f}" '
                    f'text-anchor="end" dominant-baseline="middle" '
                    f'font-size="{row_font}" '
                    f'fill="{palette["data"]}" font-family="{font}">'
                    f'{_xml_escape(line)}</text>\n'
                )

    # ---- Corner marks ----
    # Render order: bl → br → tr, then Sanskrit letter last so it lands
    # on top of any grid-line crossings inside the cluster slot.
    for role in ("bl", "br", "tr"):
        try:
            lang_idx = roles.index(role)
        except ValueError:
            continue
        renderer = _ROLE_RENDERERS[role]
        for col, manner_row in sorted(matrix_cells[lang_idx]):
            vrow = row_to_visible[manner_row]
            cx, cy = cell_center(col, vrow)
            body.append(renderer(cx, cy, palette))

    for col, manner_row in sorted(matrix_cells[sanskrit_idx]):
        vrow = row_to_visible[manner_row]
        cx, cy = cell_center(col, vrow)
        orig_col = selected_places[col]
        symbol = sanskrit_symbols.get((orig_col, manner_row), "")
        if symbol:
            body.append(_render_sanskrit_letter(cx, cy, symbol, palette))

    # ---- Caption (corner key derived from the spec) ----
    # "Top: Sanskrit क · L2 □  ·  Bottom: L3 ● · L4 ○."
    role_to_label = {role: label for _, label, role in spec.languages}
    cap_y = matrix_top + matrix_h + CAPTION_H / 2 + 0.10
    # Use a tspan for the Sanskrit क so it renders in the Devanāgarī
    # font even when the serif primary lacks the script.
    caption_open = (
        f'  <text x="{canvas_w/2:.4f}" y="{cap_y:.4f}" '
        f'text-anchor="middle" font-size="0.122" font-style="italic" '
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
