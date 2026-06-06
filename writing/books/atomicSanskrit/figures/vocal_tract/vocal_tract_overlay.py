#!/usr/bin/env python3
"""Two-language consonant inventory OVERLAY + similarity metrics.

Renders two language inventories on a shared (12 place columns x N
manner rows) coordinate system, with the second language drawn as
outlined rings around the first language's filled dots so that
overlap is visually unmistakable.

Also computes three similarity measures and renders them inline at
the bottom of the SVG:

  Jaccard       — fraction of (place, manner) cells filled in BOTH
                  out of cells filled in EITHER.  Strict measure.
  Dice          — 2 * shared / (|A| + |B|).  Slightly more generous.
  Place-overlap — fraction of places-of-articulation used in BOTH
                  out of places used in EITHER.  Generous; ignores
                  manner.

The metric set is computed on the FULL 13-row manner axis (not
on the compacted visible axis), so cross-pair comparisons are
directly comparable.

Usage:

  python3 vocal_tract_overlay.py configs/scatter_sanskrit.json \\
        configs/scatter_tamil.json [-o output.svg]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# Geometry primitives from the shared schematics module.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vocal_tract_schematics import point_at, build_ribbon_path_d  # noqa: E402


# 13 standardized manner rows (outermost row of the chart = index 0).
MANNERS: list[str] = [
    "voiceless_unasp_stop",   # 0
    "voiceless_asp_stop",     # 1
    "voiced_unasp_stop",      # 2
    "voiced_asp_stop",        # 3
    "ejective_stop",          # 4
    "voiceless_affricate",    # 5
    "voiced_affricate",       # 6
    "voiceless_fricative",    # 7
    "voiced_fricative",       # 8
    "nasal",                  # 9
    "lateral",                # 10
    "tap_or_trill",           # 11
    "approximant",            # 12
]

MANNER_DISPLAY: dict[str, str] = {
    "voiceless_unasp_stop":   "stop (voiceless)",
    "voiceless_asp_stop":     "stop (voiceless aspirated)",
    "voiced_unasp_stop":      "stop (voiced)",
    "voiced_asp_stop":        "stop (voiced aspirated)",
    "ejective_stop":          "stop (ejective)",
    "voiceless_affricate":    "affricate (voiceless)",
    "voiced_affricate":       "affricate (voiced)",
    "voiceless_fricative":    "fricative (voiceless)",
    "voiced_fricative":       "fricative (voiced)",
    "nasal":                  "nasal",
    "lateral":                "lateral approximant",
    "tap_or_trill":           "tap or trill",
    "approximant":            "approximant / glide",
}


# Symbol -> manner-class lookup.  Devanagari + Tamil + commonly-used
# IPA symbols across the 34 atlas languages.
SYMBOL_TO_MANNER: dict[str, str] = {
    # Devanagari (Sanskrit, Hindi, the loan rows used in southern/
    # Munda configs).
    "क": "voiceless_unasp_stop",
    "ख": "voiceless_asp_stop",
    "ग": "voiced_unasp_stop",
    "घ": "voiced_asp_stop",
    "ङ": "nasal",
    "च": "voiceless_unasp_stop",
    "छ": "voiceless_asp_stop",
    "ज": "voiced_unasp_stop",
    "झ": "voiced_asp_stop",
    "ञ": "nasal",
    "ट": "voiceless_unasp_stop",
    "ठ": "voiceless_asp_stop",
    "ड": "voiced_unasp_stop",
    "ढ": "voiced_asp_stop",
    "ण": "nasal",
    "त": "voiceless_unasp_stop",
    "थ": "voiceless_asp_stop",
    "द": "voiced_unasp_stop",
    "ध": "voiced_asp_stop",
    "न": "nasal",
    "प": "voiceless_unasp_stop",
    "फ": "voiceless_asp_stop",
    "ब": "voiced_unasp_stop",
    "भ": "voiced_asp_stop",
    "म": "nasal",
    "य": "approximant",
    "र": "tap_or_trill",
    "ल": "lateral",
    "व": "approximant",
    "श": "voiceless_fricative",
    "ष": "voiceless_fricative",
    "स": "voiceless_fricative",
    "ह": "voiceless_fricative",

    # Tamil
    "ப": "voiceless_unasp_stop",
    "ம": "nasal",
    "வ": "approximant",
    "ல": "lateral",
    "ள": "lateral",
    "ர": "tap_or_trill",
    "ழ": "approximant",
    "ற": "voiceless_unasp_stop",
    "ன": "nasal",
    "ட": "voiceless_unasp_stop",
    "ண": "nasal",
    "ச": "voiceless_unasp_stop",
    "ஞ": "nasal",
    "க": "voiceless_unasp_stop",
    "ங": "nasal",
    "த": "voiceless_unasp_stop",
    "ந": "nasal",
    "ய": "approximant",

    # Korean Hangul (basic; full inventory would expand)
    "ㅂ": "voiceless_unasp_stop",
    "ㄷ": "voiceless_unasp_stop",
    "ㄱ": "voiceless_unasp_stop",
    "ㅍ": "voiceless_asp_stop",
    "ㅌ": "voiceless_asp_stop",
    "ㅋ": "voiceless_asp_stop",
    "ㅃ": "voiceless_unasp_stop",  # "tensed" — classified as voiceless here
    "ㄸ": "voiceless_unasp_stop",
    "ㄲ": "voiceless_unasp_stop",
    "ㅈ": "voiceless_affricate",
    "ㅊ": "voiceless_affricate",
    "ㅉ": "voiceless_affricate",
    "ㅁ": "nasal",
    "ㄴ": "nasal",
    "ㅇ": "nasal",
    "ㄹ": "lateral",
    "ㅅ": "voiceless_fricative",
    "ㅆ": "voiceless_fricative",
    "ㅎ": "voiceless_fricative",

    # Arabic (basic)
    "ت": "voiceless_unasp_stop",
    "ك": "voiceless_unasp_stop",
    "ق": "voiceless_unasp_stop",
    "ء": "voiceless_unasp_stop",
    "ط": "voiceless_unasp_stop",
    "ب": "voiced_unasp_stop",
    "د": "voiced_unasp_stop",
    "ض": "voiced_unasp_stop",
    "ج": "voiced_affricate",
    "م": "nasal",
    "ن": "nasal",
    "ر": "tap_or_trill",
    "ل": "lateral",
    "و": "approximant",
    "ي": "approximant",
    "ف": "voiceless_fricative",
    "ث": "voiceless_fricative",
    "س": "voiceless_fricative",
    "ش": "voiceless_fricative",
    "خ": "voiceless_fricative",
    "ح": "voiceless_fricative",
    "ه": "voiceless_fricative",
    "ذ": "voiced_fricative",
    "ز": "voiced_fricative",
    "غ": "voiced_fricative",
    "ع": "voiced_fricative",
    "ظ": "voiced_fricative",
    "ص": "voiceless_fricative",

    # IPA — voiceless stops
    "p":   "voiceless_unasp_stop",
    "t":   "voiceless_unasp_stop",
    "t̪":  "voiceless_unasp_stop",
    "ʈ":   "voiceless_unasp_stop",
    "c":   "voiceless_unasp_stop",
    "k":   "voiceless_unasp_stop",
    "q":   "voiceless_unasp_stop",
    "ʔ":   "voiceless_unasp_stop",
    "kʷ":  "voiceless_unasp_stop",

    # IPA — voiceless aspirated stops
    "pʰ":  "voiceless_asp_stop",
    "tʰ":  "voiceless_asp_stop",
    "t̪ʰ": "voiceless_asp_stop",
    "ʈʰ":  "voiceless_asp_stop",
    "cʰ":  "voiceless_asp_stop",
    "kʰ":  "voiceless_asp_stop",
    "qʰ":  "voiceless_asp_stop",
    "ph":  "voiceless_asp_stop",
    "th":  "voiceless_asp_stop",
    "kh":  "voiceless_asp_stop",
    "qh":  "voiceless_asp_stop",

    # IPA — voiced stops
    "b":   "voiced_unasp_stop",
    "d":   "voiced_unasp_stop",
    "d̪":  "voiced_unasp_stop",
    "ɖ":   "voiced_unasp_stop",
    "ɟ":   "voiced_unasp_stop",
    "g":   "voiced_unasp_stop",
    "ɢ":   "voiced_unasp_stop",
    "ɓ":   "voiced_unasp_stop",

    # IPA — voiced aspirated stops
    "bʰ":  "voiced_asp_stop",
    "bʱ":  "voiced_asp_stop",
    "dʰ":  "voiced_asp_stop",
    "dʱ":  "voiced_asp_stop",
    "ɖʰ":  "voiced_asp_stop",
    "ɖʱ":  "voiced_asp_stop",
    "ɟʰ":  "voiced_asp_stop",
    "ɟʱ":  "voiced_asp_stop",
    "gʰ":  "voiced_asp_stop",
    "gʱ":  "voiced_asp_stop",

    # IPA — ejective stops
    "p'":  "ejective_stop",
    "t'":  "ejective_stop",
    "k'":  "ejective_stop",
    "q'":  "ejective_stop",
    "pʼ":  "ejective_stop",
    "tʼ":  "ejective_stop",
    "kʼ":  "ejective_stop",
    "qʼ":  "ejective_stop",

    # IPA — affricates
    "ts":  "voiceless_affricate",
    "tʃ":  "voiceless_affricate",
    "tɕ":  "voiceless_affricate",
    "tʂ":  "voiceless_affricate",
    "tɬ":  "voiceless_affricate",
    "tsh": "voiceless_affricate",
    "tʂh": "voiceless_affricate",
    "tɕh": "voiceless_affricate",
    "dz":  "voiced_affricate",
    "dʒ":  "voiced_affricate",
    "dʑ":  "voiced_affricate",
    "ɖʐ":  "voiced_affricate",

    # IPA — voiceless fricatives
    "f":   "voiceless_fricative",
    "θ":   "voiceless_fricative",
    "s":   "voiceless_fricative",
    "ʃ":   "voiceless_fricative",
    "ʂ":   "voiceless_fricative",
    "ɕ":   "voiceless_fricative",
    "x":   "voiceless_fricative",
    "χ":   "voiceless_fricative",
    "ħ":   "voiceless_fricative",
    "h":   "voiceless_fricative",
    "ɸ":   "voiceless_fricative",
    "ɬ":   "lateral",          # voiceless lateral fricative — classed as lateral
    "sʼ":  "voiceless_fricative",

    # IPA — voiced fricatives
    "v":   "voiced_fricative",
    "ð":   "voiced_fricative",
    "z":   "voiced_fricative",
    "ʒ":   "voiced_fricative",
    "ʐ":   "voiced_fricative",
    "ɣ":   "voiced_fricative",
    "ʁ":   "voiced_fricative",
    "ʕ":   "voiced_fricative",
    "ɦ":   "voiced_fricative",
    "β":   "voiced_fricative",

    # IPA — nasals
    "m":   "nasal",
    "n":   "nasal",
    "n̪":  "nasal",
    "ɳ":   "nasal",
    "ɲ":   "nasal",
    "ŋ":   "nasal",

    # IPA — laterals
    "l":   "lateral",
    "ɭ":   "lateral",
    "ʎ":   "lateral",

    # IPA — taps and trills
    "r":   "tap_or_trill",
    "ɾ":   "tap_or_trill",
    "ɽ":   "tap_or_trill",
    "r̥":  "tap_or_trill",

    # IPA — approximants
    "w":   "approximant",
    "j":   "approximant",
    "ʋ":   "approximant",
    "ɥ":   "approximant",
    "ɻ":   "approximant",
    "y":   "approximant",

    # Click consonants — classed as voiceless stop for metric purposes
    "ǀ":   "voiceless_unasp_stop",
    "ǁ":   "voiceless_unasp_stop",
    "ǃ":   "voiceless_unasp_stop",
}


def classify(symbol: str) -> str | None:
    """Map a single IPA / native-script symbol to its manner row.

    Returns None when the symbol is not recognised — caller is
    expected to surface unknowns.
    """
    if not symbol:
        return None
    s = symbol.strip()
    if s in SYMBOL_TO_MANNER:
        return SYMBOL_TO_MANNER[s]
    # Fallback — try a few simple suffix strips for unknown variants.
    for suffix in ("ʰ", "ʱ", "ʼ", "'", "ʷ"):
        if s.endswith(suffix) and s[:-len(suffix)] in SYMBOL_TO_MANNER:
            base = SYMBOL_TO_MANNER[s[:-len(suffix)]]
            if suffix in ("ʰ", "h") and base == "voiceless_unasp_stop":
                return "voiceless_asp_stop"
            if suffix in ("ʱ",) and base == "voiced_unasp_stop":
                return "voiced_asp_stop"
            if suffix in ("ʼ", "'") and base == "voiceless_unasp_stop":
                return "ejective_stop"
            return base
    return None


def harmonize(matrix: list[list[str]]) -> tuple[
    set[tuple[int, int]], dict[tuple[int, int], str], list[str]
]:
    """Convert a per-language matrix to a set of (place_col, manner_row) cells.

    Returns:
      cells          — set of (col_idx, manner_row_idx) tuples
      cell_symbols   — dict mapping each cell to the source symbol (for debug)
      unclassified   — list of source symbols the classifier did not recognise
    """
    cells: set[tuple[int, int]] = set()
    cell_symbols: dict[tuple[int, int], str] = {}
    unclassified: list[str] = []
    for row in matrix:
        for col_idx, symbol in enumerate(row):
            if not symbol:
                continue
            manner = classify(symbol)
            if manner is None:
                unclassified.append(symbol)
                continue
            manner_row = MANNERS.index(manner)
            cells.add((col_idx, manner_row))
            cell_symbols[(col_idx, manner_row)] = symbol
    return cells, cell_symbols, unclassified


def compute_metrics(
    cells_a: set[tuple[int, int]],
    cells_b: set[tuple[int, int]],
) -> dict[str, float | int]:
    """Compute the three comparison metrics on the FULL manner axis.

    Cross-pair comparisons of these numbers are directly comparable
    because no compaction is applied here.
    """
    shared = cells_a & cells_b
    union = cells_a | cells_b
    jaccard = len(shared) / len(union) if union else 0.0
    dice = (
        2 * len(shared) / (len(cells_a) + len(cells_b))
        if (cells_a or cells_b) else 0.0
    )
    places_a = {c[0] for c in cells_a}
    places_b = {c[0] for c in cells_b}
    places_both = places_a & places_b
    places_either = places_a | places_b
    place_overlap = (
        len(places_both) / len(places_either)
        if places_either else 0.0
    )
    return {
        "jaccard": jaccard,
        "dice": dice,
        "place_overlap": place_overlap,
        "shared_cells": len(shared),
        "union_cells": len(union),
        "lang_a_cells": len(cells_a),
        "lang_b_cells": len(cells_b),
        "lang_a_places": len(places_a),
        "lang_b_places": len(places_b),
        "places_both": len(places_both),
        "places_either": len(places_either),
    }


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def render_overlay(
    cfg_a: dict, cfg_b: dict,
    cells_a: set[tuple[int, int]],
    cells_b: set[tuple[int, int]],
    metrics: dict[str, float | int],
    label_a: str, label_b: str,
) -> str:
    """Build the overlay SVG string.

    Uses cfg_a's geometry / angular_range / canvas as the shared
    layout reference; expects cfg_b to use the same.  Manner-rows
    are COMPACTED to only rows used by either language so the chart
    stays vertically compact.
    """
    geometry = cfg_a["geometry"]
    r1, r2, w = float(geometry["r1"]), float(geometry["r2"]), float(geometry["w"])

    canvas = cfg_a["canvas"]
    canvas_w = float(canvas["width"])
    canvas_h = float(canvas["height"])

    # Column thetas from the anatomical distance distribution.
    ar = cfg_a["scatter"]["angular_range"]
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

    # Visible (compacted) rows = union of manner rows used by either language.
    rows_used = sorted({m for (_, m) in cells_a | cells_b})
    n_rows_visible = len(rows_used)
    row_to_visible: dict[int, int] = {m: i for i, m in enumerate(rows_used)}

    # Outermost = visible index 0; innermost = visible index n-1.
    delta_r = 0.1
    r_inner = 2.0
    row_radii = [
        r_inner + (n_rows_visible - 1 - i) * delta_r
        for i in range(n_rows_visible)
    ]

    body: list[str] = []
    samples: list[tuple[float, float]] = []

    # 1. Base ribbon.
    base = cfg_a.get("base_ribbon")
    if base is not None:
        bt1 = float(base.get("t1", 150))
        bt2 = float(base.get("t2", 240))
        path_d, ribbon_samples = build_ribbon_path_d(r1, r2, w, bt1, bt2)
        body.append(
            f'  <path d="{path_d}" '
            f'fill="none" stroke="#bbbbbb" stroke-width="0.01" '
            f'opacity="0.7" stroke-linejoin="miter" stroke-linecap="butt" />\n'
        )
        samples.extend(ribbon_samples)

    # 2a. Language A dots — FILLED, gray.
    circle_radius_a = 0.05
    fill_a = "#666666"
    fill_opacity_a = 0.5
    for col, manner_row in cells_a:
        vrow = row_to_visible[manner_row]
        r = row_radii[vrow]
        theta = column_thetas[col]
        x, y = point_at(r, r, theta)
        body.append(
            f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{circle_radius_a}" '
            f'fill="{fill_a}" opacity="{fill_opacity_a}" />\n'
        )
        samples.append((x - circle_radius_a, y - circle_radius_a))
        samples.append((x + circle_radius_a, y + circle_radius_a))

    # 2b. Language B dots — OUTLINED, slightly larger so that overlap with
    # an A-dot reads as 'filled with a ring around it'.
    circle_radius_b = 0.075
    stroke_b = "#222222"
    stroke_w_b = 0.015
    for col, manner_row in cells_b:
        vrow = row_to_visible[manner_row]
        r = row_radii[vrow]
        theta = column_thetas[col]
        x, y = point_at(r, r, theta)
        body.append(
            f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{circle_radius_b}" '
            f'fill="none" stroke="{stroke_b}" stroke-width="{stroke_w_b}" />\n'
        )
        samples.append((x - circle_radius_b, y - circle_radius_b))
        samples.append((x + circle_radius_b, y + circle_radius_b))

    # 3. Leader lines + number callouts for columns lit in either language.
    cols_lit = sorted({c for (c, _) in cells_a | cells_b})

    leader_inner_r = 1.9
    leader_gap = 0.1
    label_gap = 0.05
    font_size = 0.1528
    bottom_margin = 0.7  # leaves room for the metrics text block

    # Most-negative y of any rendered dot (used for dynamic y_label).
    chart_y_top = 0.0
    for col, manner_row in cells_a | cells_b:
        vrow = row_to_visible[manner_row]
        r = row_radii[vrow]
        theta = column_thetas[col]
        y = math.cos(math.radians(theta)) * r
        if y < chart_y_top:
            chart_y_top = y
    y_label = (
        chart_y_top + label_gap + font_size
        + (canvas_h - 2.0 * bottom_margin)
    )

    leader_color = "#888888"
    leader_w = 0.005

    def innermost_visible_row(col: int) -> int | None:
        candidates: list[int] = []
        for (c, m) in cells_a | cells_b:
            if c == col:
                candidates.append(row_to_visible[m])
        if not candidates:
            return None
        # Largest visible-row index = smallest r = innermost on chart.
        return max(candidates)

    for col in cols_lit:
        vrow_innermost = innermost_visible_row(col)
        if vrow_innermost is None:
            continue
        innermost_r = row_radii[vrow_innermost]
        start_r = innermost_r - leader_gap
        theta = column_thetas[col]
        x_start, y_start = point_at(start_r, start_r, theta)
        x_inner, y_inner = point_at(leader_inner_r, leader_inner_r, theta)
        body.append(
            f'  <path d="M {x_start:.4f} {y_start:.4f} '
            f'L {x_inner:.4f} {y_inner:.4f} '
            f'L {x_inner:.4f} {y_label:.4f}" '
            f'fill="none" stroke="{leader_color}" '
            f'stroke-width="{leader_w}" stroke-linecap="round" />\n'
        )
        label_text = str(col + 1)
        text_y = y_label + label_gap + font_size * 0.5
        body.append(
            f'  <text x="{x_inner:.4f}" y="{text_y:.4f}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="{font_size}" fill="#222222" '
            f'font-family="Gentium Book Plus, Charter, Charis SIL, Georgia, serif">'
            f'{label_text}</text>\n'
        )
        samples.append((x_start, y_start))
        samples.append((x_inner, y_inner))
        samples.append((x_inner, text_y + font_size * 0.6))

    # 4. Metric text block at the bottom of the canvas.
    metrics_y_top = y_label + label_gap + font_size + 0.18
    legend_y = metrics_y_top
    header_y = metrics_y_top + 0.20
    metric_y = metrics_y_top + 0.36

    legend_text_a = f"●  {label_a}"
    legend_text_b = f"○  {label_b}"
    legend_font = 0.13
    metric_font = 0.13
    header_font = 0.13

    legend_x_a = -1.7
    legend_x_b = 0.7

    body.append(
        f'  <text x="{legend_x_a:.4f}" y="{legend_y:.4f}" '
        f'text-anchor="start" dominant-baseline="middle" '
        f'font-size="{legend_font}" fill="#222222" '
        f'font-family="Gentium Book Plus, Charter, Charis SIL, Georgia, serif">'
        f'{_xml_escape(legend_text_a)}</text>\n'
    )
    body.append(
        f'  <text x="{legend_x_b:.4f}" y="{legend_y:.4f}" '
        f'text-anchor="start" dominant-baseline="middle" '
        f'font-size="{legend_font}" fill="#222222" '
        f'font-family="Gentium Book Plus, Charter, Charis SIL, Georgia, serif">'
        f'{_xml_escape(legend_text_b)}</text>\n'
    )

    header = f"{label_a.upper()}  —  {label_b.upper()}"
    body.append(
        f'  <text x="0" y="{header_y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{header_font}" fill="#222222" font-weight="bold" '
        f'font-family="Gentium Book Plus, Charter, Charis SIL, Georgia, serif">'
        f'{_xml_escape(header)}</text>\n'
    )

    metric_line = (
        f"shared {metrics['shared_cells']} of {metrics['union_cells']} cells  "
        f"•  Jaccard {metrics['jaccard']:.2f}  "
        f"•  Dice {metrics['dice']:.2f}  "
        f"•  Places {metrics['place_overlap']:.2f}"
    )
    body.append(
        f'  <text x="0" y="{metric_y:.4f}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{metric_font}" fill="#222222" '
        f'font-family="Gentium Book Plus, Charter, Charis SIL, Georgia, serif">'
        f'{_xml_escape(metric_line)}</text>\n'
    )

    # Sample bounding-box anchors for the bottom text block.
    samples.append((-2.0, header_y))
    samples.append((2.0, metric_y + 0.2))

    # ViewBox: auto-centred on content (mirrors vocal_tract_scatter.py).
    cx_min = min(p[0] for p in samples)
    cx_max = max(p[0] for p in samples)
    cy_min = min(p[1] for p in samples)
    cy_max = max(p[1] for p in samples)
    content_cx = 0.5 * (cx_min + cx_max)
    content_cy = 0.5 * (cy_min + cy_max)
    vb_x = content_cx - canvas_w / 2.0
    vb_y = content_cy - canvas_h / 2.0

    svg = [
        f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{canvas_w:.4f}in" height="{canvas_h:.4f}in" '
        f'viewBox="{vb_x:.4f} {vb_y:.4f} {canvas_w:.4f} {canvas_h:.4f}">\n',
        f'  <rect x="{vb_x:.4f}" y="{vb_y:.4f}" '
        f'width="{canvas_w:.4f}" height="{canvas_h:.4f}" fill="white" />\n',
    ]
    svg.extend(body)
    svg.append('</svg>\n')
    return "".join(svg)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config_a", type=Path)
    ap.add_argument("config_b", type=Path)
    ap.add_argument("--output", "-o", type=Path)
    ap.add_argument("--label-a", default=None,
                    help="Display label for the FIRST language "
                         "(default: derived from config name)")
    ap.add_argument("--label-b", default=None)
    args = ap.parse_args(argv)

    cfg_a = json.loads(args.config_a.read_text(encoding="utf-8"))
    cfg_b = json.loads(args.config_b.read_text(encoding="utf-8"))

    def derive_label(cfg: dict, path: Path) -> str:
        name = cfg.get("name", path.stem)
        if name.startswith("scatter_"):
            name = name[len("scatter_"):]
        return name.replace("_", " ").title()

    label_a = args.label_a or derive_label(cfg_a, args.config_a)
    label_b = args.label_b or derive_label(cfg_b, args.config_b)

    cells_a, _, unk_a = harmonize(cfg_a["scatter"]["matrix"])
    cells_b, _, unk_b = harmonize(cfg_b["scatter"]["matrix"])

    if unk_a:
        print(f"warning: unclassified symbols in {label_a}: {sorted(set(unk_a))}",
              file=sys.stderr)
    if unk_b:
        print(f"warning: unclassified symbols in {label_b}: {sorted(set(unk_b))}",
              file=sys.stderr)

    metrics = compute_metrics(cells_a, cells_b)

    print(
        f"{label_a} ({metrics['lang_a_cells']} cells, "
        f"{metrics['lang_a_places']} places)  vs  "
        f"{label_b} ({metrics['lang_b_cells']} cells, "
        f"{metrics['lang_b_places']} places)"
    )
    print(
        f"  Jaccard       {metrics['jaccard']:.3f}  "
        f"({metrics['shared_cells']} shared / "
        f"{metrics['union_cells']} union)"
    )
    print(f"  Dice          {metrics['dice']:.3f}")
    print(
        f"  Place-overlap {metrics['place_overlap']:.3f}  "
        f"({metrics['places_both']} places in both / "
        f"{metrics['places_either']} in either)"
    )

    out_path: Path
    if args.output:
        out_path = args.output
    else:
        out_dir = (
            Path(__file__).resolve().parent.parent / "build" / "vocal_tract"
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        a_slug = label_a.replace(" ", "_").lower()
        b_slug = label_b.replace(" ", "_").lower()
        out_path = out_dir / f"overlay_{a_slug}_vs_{b_slug}.svg"

    svg = render_overlay(cfg_a, cfg_b, cells_a, cells_b, metrics, label_a, label_b)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
