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
    """Compute the comparison metrics on the FULL manner axis.

    Six metrics, two of them asymmetric:

      jaccard       |A ∩ B| / |A ∪ B|                              strict
      dice          2·|A ∩ B| / (|A| + |B|)                        ditto, kinder
      place_overlap |places(A) ∩ places(B)| / |places(A) ∪ places(B)|  anatomy only
      cosine        |A ∩ B| / √(|A|·|B|)                           size-tolerant
      jsd           Jensen-Shannon distance between uniform        info-theoretic
                    distributions on A and B (in nats); bounded
                    [0, ln 2].  Normalised to [0,1] for jsd_sim.
      jsd_sim       1 − jsd/ln 2                                   "JSD similarity"
      cov_a_in_b    |A ∩ B| / |B|   — fraction of B contained in A
      cov_b_in_a    |A ∩ B| / |A|   — fraction of A contained in B

    Cross-pair comparisons of these numbers are directly comparable
    because no compaction is applied here.
    """
    shared = cells_a & cells_b
    union = cells_a | cells_b
    n_a, n_b, n_shared = len(cells_a), len(cells_b), len(shared)
    n_union = len(union)

    jaccard = n_shared / n_union if n_union else 0.0
    dice = 2 * n_shared / (n_a + n_b) if (n_a + n_b) else 0.0
    cosine = (
        n_shared / math.sqrt(n_a * n_b)
        if (n_a and n_b) else 0.0
    )

    places_a = {c[0] for c in cells_a}
    places_b = {c[0] for c in cells_b}
    places_both = places_a & places_b
    places_either = places_a | places_b
    place_overlap = (
        len(places_both) / len(places_either)
        if places_either else 0.0
    )

    # Jensen-Shannon distance between two uniform distributions on
    # their supports.  Treats each filled cell as carrying equal
    # probability mass within its language.
    if n_a == 0 or n_b == 0:
        jsd = 0.0 if (n_a == 0 and n_b == 0) else math.log(2.0)
    else:
        p, q = 1.0 / n_a, 1.0 / n_b
        kl_pm = 0.0
        kl_qm = 0.0
        for cell in union:
            p_x = p if cell in cells_a else 0.0
            q_x = q if cell in cells_b else 0.0
            m_x = 0.5 * (p_x + q_x)
            if p_x > 0:
                kl_pm += p_x * math.log(p_x / m_x)
            if q_x > 0:
                kl_qm += q_x * math.log(q_x / m_x)
        jsd = 0.5 * (kl_pm + kl_qm)
    jsd_sim = 1.0 - jsd / math.log(2.0) if jsd > 0 else 1.0

    cov_a_in_b = n_shared / n_b if n_b else 0.0
    cov_b_in_a = n_shared / n_a if n_a else 0.0

    return {
        "jaccard": jaccard,
        "dice": dice,
        "place_overlap": place_overlap,
        "cosine": cosine,
        "jsd": jsd,
        "jsd_sim": jsd_sim,
        "cov_a_in_b": cov_a_in_b,
        "cov_b_in_a": cov_b_in_a,
        "shared_cells": n_shared,
        "union_cells": n_union,
        "lang_a_cells": n_a,
        "lang_b_cells": n_b,
        "lang_a_places": len(places_a),
        "lang_b_places": len(places_b),
        "places_both": len(places_both),
        "places_either": len(places_either),
    }


STRIP_PRESETS: dict[str, set[str]] = {
    "mahaprana": {"voiceless_asp_stop", "voiced_asp_stop"},
    "voiceless_asp": {"voiceless_asp_stop"},
    "voiced_asp": {"voiced_asp_stop"},
    "sibilants": {"voiceless_fricative", "voiced_fricative"},
}


def strip_cells(
    cells: set[tuple[int, int]],
    preset_names: list[str] | None,
) -> set[tuple[int, int]]:
    """Return cells with selected manner rows removed.

    This supports sensitivity checks such as comparing Sanskrit after
    removing its mahāprāṇa stop rows. Presets remove manner rows after the
    per-language inventory has been harmonised onto the shared 13-row axis.
    """
    if not preset_names:
        return set(cells)
    rows_to_remove: set[int] = set()
    for name in preset_names:
        if name not in STRIP_PRESETS:
            known = ", ".join(sorted(STRIP_PRESETS))
            raise ValueError(f"unknown strip preset {name!r}; known: {known}")
        rows_to_remove.update(MANNERS.index(m) for m in STRIP_PRESETS[name])
    return {(col, row) for (col, row) in cells if row not in rows_to_remove}


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


# ---------------------------------------------------------------------------
# Polished print-quality overlay (Claude Design-inspired)
# ---------------------------------------------------------------------------

PLACE_ABBR: dict[int, str] = {
    0: "BIL", 1: "LD",  2: "ID",  3: "DEN",
    4: "ALV", 5: "PA",  6: "RET", 7: "PAL",
    8: "VEL", 9: "UV",  10: "PHA", 11: "GLO",
}

# Column ranges belonging to each articulator family group.
ARTICULATOR_GROUPS: list[tuple[str, set[int]]] = [
    ("LAB",      {0, 1}),                # labial: bilabial, labio-d.
    ("CORONAL",  {2, 3, 4, 5, 6}),       # interdent, dental, alveolar, post-alv, retroflex
    ("DORSAL",   {7, 8}),                # palatal, velar
    ("LARYNGEAL", {9, 10, 11}),          # uvular, pharyngeal, glottal
]


def _polished_color_palette() -> dict[str, str]:
    """Tonal palette extracted from the Claude Design SVGs."""
    return {
        "background":     "#f4f4f3",
        "ribbon_fill":    "#eceae5",
        "ribbon_stroke":  "#cdccc8",
        "detail_dark":    "#cdccc8",
        "detail_light":   "#e3e1db",
        "data":           "#2b2b2d",
        "leader":         "#9a9892",
        "group_arc":      "#8f8d86",
        "pill_fill":      "#ffffff",
    }


def render_overlay_polished(
    cfg_a: dict, cfg_b: dict,
    cells_a: set[tuple[int, int]],
    cells_b: set[tuple[int, int]],
    metrics: dict[str, float | int],
    label_a: str, label_b: str,
) -> str:
    """Build the print-quality overlay SVG.

    Visual conventions (extracted from the Claude Design SVGs):

    - Cream background (#f4f4f3)
    - Ribbon arc rendered as a filled mouth-cross-section with subtle
      articulator detail lines along the upper boundary
    - Header line at the top: "Sanskrit · 33   Tamil · 18" with a
      filled dot beside language A and an outlined ring beside B
    - Articulator group headers (LAB / CORONAL / DORSAL / LARYNGEAL)
      drawn as labeled arcs above the ribbon, grouping the place
      columns by articulator family
    - Place-column labels as white pill chips at the bottom of the
      chart with 3-letter abbreviations (BIL / DEN / ALV / RET / etc.)
    - Leader lines from data dots down to the pill labels
    - Metric panel at the very bottom with Jaccard / Dice / Cosine /
      Place-overlap / asymmetric coverage values

    Both languages share the harmonised 13-row manner axis; only
    rows used by either language are rendered (compaction).
    """
    palette = _polished_color_palette()

    # Polished overlay shrinks the standalone atlas geometry by
    # 0.25 in radially so the chart fits the canvas more snugly.
    # The standalone atlas configs are left alone; this is purely
    # a polished-overlay layout choice.
    geometry = cfg_a["geometry"]
    polished_radius_offset = 0.25
    r1 = float(geometry["r1"]) - polished_radius_offset
    r2 = float(geometry["r2"]) - polished_radius_offset
    w = float(geometry["w"])

    canvas_w = 4.5
    canvas_h = 4.0

    # Column thetas from anatomical-distance distribution.
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

    # Compact manner-rows to only those used.
    rows_used = sorted({m for (_, m) in cells_a | cells_b})
    n_rows_visible = len(rows_used)
    row_to_visible: dict[int, int] = {m: i for i, m in enumerate(rows_used)}

    # Pull r_inner inward by the same polished_radius_offset so dots
    # stay aligned with the (now smaller) ribbon, straddling its
    # centerline as before.
    delta_r = 0.1
    r_inner = 2.0 - polished_radius_offset
    row_radii = [
        r_inner + (n_rows_visible - 1 - i) * delta_r
        for i in range(n_rows_visible)
    ]

    cols_lit = sorted({c for (c, _) in cells_a | cells_b})

    body: list[str] = []
    samples: list[tuple[float, float]] = []
    font = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

    # ----- 1. Filled mouth-ribbon -----
    base = cfg_a.get("base_ribbon")
    bt1 = float(base.get("t1", 150)) if base else 150.0
    bt2 = float(base.get("t2", 240)) if base else 240.0
    path_d, ribbon_samples = build_ribbon_path_d(r1, r2, w, bt1, bt2)
    body.append(
        f'  <path d="{path_d}" '
        f'fill="{palette["ribbon_fill"]}" stroke="none" />\n'
    )
    # The upper edge of the ribbon, with a slightly thicker stroke.
    upper_arc_r1 = r1 + 0.5 * w
    upper_arc_r2 = r2 + 0.5 * w
    body.append(
        f'  <path d="{_arc_path(upper_arc_r1, upper_arc_r2, bt1, bt2)}" '
        f'fill="none" stroke="{palette["ribbon_stroke"]}" '
        f'stroke-width="0.016" stroke-linecap="round" />\n'
    )
    samples.extend(ribbon_samples)

    # Articulator-detail tick marks along the upper edge, lit-column-aligned.
    # The book's polemic move is anatomical; these tick marks reinforce that
    # each place corresponds to a real articulator-contact zone.
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

    # ----- 2. Data dots: A filled, B outlined -----
    r_filled = 0.046
    r_outlined = 0.072
    for col, manner_row in cells_a:
        vrow = row_to_visible[manner_row]
        r = row_radii[vrow]
        theta = column_thetas[col]
        x, y = point_at(r, r, theta)
        body.append(
            f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{r_filled}" '
            f'fill="{palette["data"]}" />\n'
        )
        samples.append((x - r_filled, y - r_filled))
        samples.append((x + r_filled, y + r_filled))
    for col, manner_row in cells_b:
        vrow = row_to_visible[manner_row]
        r = row_radii[vrow]
        theta = column_thetas[col]
        x, y = point_at(r, r, theta)
        body.append(
            f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{r_outlined}" '
            f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" />\n'
        )
        samples.append((x - r_outlined, y - r_outlined))
        samples.append((x + r_outlined, y + r_outlined))

    # ----- 3. Leader lines + place-label pill chips -----
    # Layout (3-segment leader, no criss-crossing):
    #
    #   (a) RADIAL — from just below each column's innermost dot
    #       INWARD along the column's theta to a UNIFORM anchor
    #       radius (r_anchor = r_inner - 0.1, so 0.1 in from the
    #       global innermost dot row).  Anchor points all sit on
    #       a common arc below the data.
    #   (b) ANGLED — from the anchor point to (pill_x, fan_collect_y)
    #       where fan_collect_y is a SINGLE constant y = 0.25 in
    #       above the pill tops.  All angled segments converge to
    #       this horizontal "fan-collect line."
    #   (c) VERTICAL — straight drop from (pill_x, fan_collect_y)
    #       to (pill_x, pill_top_y) — every column ends with this
    #       same short vertical, giving a clean horizontal shelf
    #       above the pill row.
    #
    # Because anchor x and pill x are both monotonic in column-theta
    # order, the angled segments fan outward symmetrically without
    # crossing.
    y_pill = -0.32

    def innermost_visible_row(col: int) -> int | None:
        candidates = [
            row_to_visible[m] for (c, m) in (cells_a | cells_b) if c == col
        ]
        return max(candidates) if candidates else None

    # Wide-pill charts (>= 11 lit columns — Arabic, Brahui) need
    # the pill row nudged rightward to avoid clipping at the left
    # canvas edge after the global leftward shift applied below.
    n_lit_total = len(cols_lit)
    pill_x_offset = 0.30 if n_lit_total >= 11 else 0.0

    pill_xs: dict[int, float] = {}
    pill_min_gap = 0.34
    if cols_lit:
        sorted_cols_for_pills = sorted(cols_lit)
        n_lit = len(sorted_cols_for_pills)
        total_pill_width = (n_lit - 1) * pill_min_gap
        left_pill_x = -0.5 * total_pill_width
        for i, col in enumerate(sorted_cols_for_pills):
            pill_xs[col] = left_pill_x + i * pill_min_gap + pill_x_offset

    leader_w = 0.007
    pill_w, pill_h, pill_r = 0.32, 0.30, 0.03
    pill_font = 0.125
    pill_top_y = y_pill - 0.5 * pill_h

    # Uniform anchor radius: 0.1 in inside the global innermost dot row.
    r_anchor = r_inner - 0.1
    # Fan-collect y: 0.25 in above the pill top row.
    fan_collect_y = pill_top_y - 0.25

    for col in cols_lit:
        vrow_inner = innermost_visible_row(col)
        if vrow_inner is None:
            continue
        innermost_r = row_radii[vrow_inner]
        theta = column_thetas[col]
        # (a) Radial from just below the column's innermost dot edge,
        #     inward to the uniform anchor radius.
        start_r = innermost_r - r_filled - 0.02
        x_start, y_start = point_at(start_r, start_r, theta)
        x_anchor, y_anchor = point_at(r_anchor, r_anchor, theta)
        # (b) Angled connector to (pill_x, fan_collect_y).
        x_pill = pill_xs[col]
        # (c) Vertical drop from fan_collect_y to pill_top.
        body.append(
            f'  <path d="M {x_start:.4f} {y_start:.4f} '
            f'L {x_anchor:.4f} {y_anchor:.4f} '
            f'L {x_pill:.4f} {fan_collect_y:.4f} '
            f'L {x_pill:.4f} {pill_top_y:.4f}" '
            f'fill="none" stroke="{palette["leader"]}" '
            f'stroke-width="{leader_w}" stroke-linecap="round" '
            f'stroke-linejoin="round" />\n'
        )
        # White pill chip
        body.append(
            f'  <rect x="{x_pill - pill_w/2:.4f}" '
            f'y="{y_pill - pill_h/2:.4f}" '
            f'width="{pill_w}" height="{pill_h}" rx="{pill_r}" '
            f'fill="{palette["pill_fill"]}" stroke="none" />\n'
        )
        # Place abbreviation text
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

    # ----- 4. Articulator-group headers (LAB / CORONAL / DORSAL / LARYNGEAL) -----
    # Each group's arc covers the angular extent of its constituent lit columns.
    group_arc_r = upper_arc_r1 + 0.18
    group_label_r = upper_arc_r1 + 0.30
    for group_name, group_cols in ARTICULATOR_GROUPS:
        intersect = sorted(set(group_cols) & set(cols_lit))
        if not intersect:
            continue
        # Special-case: if DORSAL and LARYNGEAL both fire, merge label.
        if group_name == "DORSAL":
            ling_intersect = sorted(set(ARTICULATOR_GROUPS[3][1]) & set(cols_lit))
            if ling_intersect:
                # Merge label; emit only DORSAL's arc here over its own cols
                display = "DORSAL · LARYNGEAL"
            else:
                display = "DORSAL"
        elif group_name == "LARYNGEAL":
            # If DORSAL also fires, skip this iteration (already merged above)
            if set(ARTICULATOR_GROUPS[2][1]) & set(cols_lit):
                continue
            display = "LARYNGEAL"
        else:
            display = group_name

        # Determine arc theta range from the leftmost to rightmost lit column
        # in this group; widen slightly for visual breathing room.
        if group_name == "DORSAL" and (set(ARTICULATOR_GROUPS[3][1]) & set(cols_lit)):
            # Merged DORSAL · LARYNGEAL — arc spans both groups' lit cols
            merged_cols = sorted(
                set(intersect) | (set(ARTICULATOR_GROUPS[3][1]) & set(cols_lit))
            )
            theta_a = column_thetas[merged_cols[0]]
            theta_b = column_thetas[merged_cols[-1]]
        else:
            theta_a = column_thetas[intersect[0]]
            theta_b = column_thetas[intersect[-1]]
        if theta_a == theta_b:
            theta_a -= 1.5
            theta_b += 1.5
        else:
            theta_a -= 0.5
            theta_b += 0.5

        # Arc path for textPath
        arc_id = f"grp_{group_name.lower()}"
        body.append(
            f'  <defs><path id="{arc_id}" '
            f'd="{_arc_path(group_arc_r, group_arc_r, theta_a, theta_b)}" '
            f'fill="none" /></defs>\n'
        )
        # Arc tick at each end
        for theta in (theta_a, theta_b):
            xa, ya = point_at(group_arc_r, group_arc_r, theta)
            xb, yb = point_at(group_arc_r + 0.03, group_arc_r + 0.03, theta)
            body.append(
                f'  <path d="M {xa:.4f} {ya:.4f} L {xb:.4f} {yb:.4f}" '
                f'stroke="{palette["group_arc"]}" stroke-width="0.012" />\n'
            )
        # Arc body
        body.append(
            f'  <path d="{_arc_path(group_arc_r, group_arc_r, theta_a, theta_b)}" '
            f'fill="none" stroke="{palette["group_arc"]}" '
            f'stroke-width="0.012" stroke-linecap="round" />\n'
        )
        # Group label along the arc
        # Build a fresh slightly-larger arc for the text positioning
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
        # Sample the label-arc extent for canvas auto-centring
        for theta in (theta_a, theta_b):
            x, y = point_at(group_label_r + 0.06, group_label_r + 0.06, theta)
            samples.append((x, y))

    # ----- 5. Header line at the top -----
    # "Sanskrit · 33   <legend dot>  Tamil · 18  <legend ring>"
    header_y_top = group_label_r + 0.18
    header_y = -(header_y_top)  # most-negative y, top of chart
    if samples:
        ys = [p[1] for p in samples]
        # Place header slightly above the current topmost content sample
        header_y = min(ys) - 0.16
    header_font = 0.135
    n_a = len(cells_a)
    n_b = len(cells_b)
    text_a = f"{label_a} · {n_a}"
    text_b = f"{label_b} · {n_b}"
    a_text_w = max(len(text_a), 1) * header_font * 0.55
    b_text_w = max(len(text_b), 1) * header_font * 0.55
    gap = 0.35
    total_w = a_text_w + b_text_w + gap + 2 * 0.07  # 0.07 = legend dot radius
    x0 = -0.5 * total_w
    body.append(
        f'  <circle cx="{x0:.4f}" cy="{header_y:.4f}" r="0.05" '
        f'fill="{palette["data"]}" />\n'
    )
    body.append(
        f'  <text x="{x0 + 0.105:.4f}" y="{header_y + 0.05:.4f}" '
        f'font-size="{header_font}" fill="{palette["data"]}" '
        f'font-family="{font}">{_xml_escape(text_a)}</text>\n'
    )
    x_b_dot = x0 + 0.105 + a_text_w + gap
    body.append(
        f'  <circle cx="{x_b_dot:.4f}" cy="{header_y:.4f}" r="0.062" '
        f'fill="none" stroke="{palette["data"]}" stroke-width="0.011" />\n'
    )
    body.append(
        f'  <text x="{x_b_dot + 0.12:.4f}" y="{header_y + 0.05:.4f}" '
        f'font-size="{header_font}" fill="{palette["data"]}" '
        f'font-family="{font}">{_xml_escape(text_b)}</text>\n'
    )
    samples.append((x0 - 0.1, header_y - 0.1))
    samples.append((x0 + total_w + 0.1, header_y + 0.1))

    # ----- 6. Metric panel at the bottom -----
    metric_y_base = y_pill + 0.5 * pill_h + 0.30
    metric_font = 0.115
    line_spacing = 0.18

    line1 = (
        f"shared {metrics['shared_cells']} of {metrics['union_cells']} cells"
        f"   ·   Jaccard {metrics['jaccard']:.2f}"
        f"   ·   Dice {metrics['dice']:.2f}"
        f"   ·   Cosine {metrics['cosine']:.2f}"
    )
    line2 = f"Place-overlap {metrics['place_overlap']:.2f}"
    line3 = (
        f"{label_a} ⊇ {label_b}  {metrics['cov_a_in_b']:.2f}"
        f"      {label_b} ⊇ {label_a}  {metrics['cov_b_in_a']:.2f}"
    )
    for i, line in enumerate((line1, line2, line3)):
        body.append(
            f'  <text x="0" y="{metric_y_base + i*line_spacing:.4f}" '
            f'text-anchor="middle" font-size="{metric_font}" '
            f'fill="{palette["data"]}" font-family="{font}">'
            f'{_xml_escape(line)}</text>\n'
        )
    samples.append((-2.0, metric_y_base + 3 * line_spacing))
    samples.append((2.0, metric_y_base + 3 * line_spacing))

    # ----- viewBox auto-centring -----
    # Apply a small global leftward shift so the asymmetric mouth
    # arc (which leans visually right because theta range is 150°-
    # 240°) sits a bit left of canvas centre.
    visual_left_shift = 0.20
    cx_min = min(p[0] for p in samples)
    cx_max = max(p[0] for p in samples)
    cy_min = min(p[1] for p in samples)
    cy_max = max(p[1] for p in samples)
    content_cx = 0.5 * (cx_min + cx_max)
    content_cy = 0.5 * (cy_min + cy_max)
    vb_x = content_cx - canvas_w / 2.0 + visual_left_shift
    vb_y = content_cy - canvas_h / 2.0

    svg = [
        f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',
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


def _arc_path(r1: float, r2: float, t1: float, t2: float) -> str:
    """SVG path-data for the elliptical arc from t1 to t2 at radii (r1, r2)."""
    x1, y1 = point_at(r1, r2, t1)
    x2, y2 = point_at(r1, r2, t2)
    large = 1 if abs(t2 - t1) > 180 else 0
    sweep = 1 if t2 > t1 else 0
    return (
        f"M {x1:.4f} {y1:.4f} "
        f"A {r1:.4f} {r2:.4f} 0 {large} {sweep} {x2:.4f} {y2:.4f}"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config_a", type=Path)
    ap.add_argument("config_b", type=Path)
    ap.add_argument("--output", "-o", type=Path)
    ap.add_argument("--label-a", default=None,
                    help="Display label for the FIRST language "
                         "(default: derived from config name)")
    ap.add_argument("--label-b", default=None)
    ap.add_argument(
        "--strip-a",
        action="append",
        choices=sorted(STRIP_PRESETS),
        default=[],
        help="Remove a manner-row preset from the FIRST language before "
             "metrics/rendering. Can be repeated.",
    )
    ap.add_argument(
        "--strip-b",
        action="append",
        choices=sorted(STRIP_PRESETS),
        default=[],
        help="Remove a manner-row preset from the SECOND language before "
             "metrics/rendering. Can be repeated.",
    )
    ap.add_argument(
        "--strip",
        action="append",
        choices=sorted(STRIP_PRESETS),
        default=[],
        help="Remove a manner-row preset from BOTH languages before "
             "metrics/rendering. Can be repeated.",
    )
    ap.add_argument(
        "--style", choices=("technical", "polished"), default="technical",
        help="'technical' (default): debug layout; 'polished': print-quality "
             "Claude-Design-style layout for book figures",
    )
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
    strip_a = list(args.strip) + list(args.strip_a)
    strip_b = list(args.strip) + list(args.strip_b)
    cells_a = strip_cells(cells_a, strip_a)
    cells_b = strip_cells(cells_b, strip_b)

    if unk_a:
        print(f"warning: unclassified symbols in {label_a}: {sorted(set(unk_a))}",
              file=sys.stderr)
    if unk_b:
        print(f"warning: unclassified symbols in {label_b}: {sorted(set(unk_b))}",
              file=sys.stderr)

    metrics = compute_metrics(cells_a, cells_b)

    if strip_a:
        print(f"  Strip {label_a}: {', '.join(strip_a)}")
    if strip_b:
        print(f"  Strip {label_b}: {', '.join(strip_b)}")
    print(
        f"{label_a} ({metrics['lang_a_cells']} cells, "
        f"{metrics['lang_a_places']} places)  vs  "
        f"{label_b} ({metrics['lang_b_cells']} cells, "
        f"{metrics['lang_b_places']} places)"
    )
    print(
        f"  Jaccard           {metrics['jaccard']:.3f}  "
        f"({metrics['shared_cells']} shared / "
        f"{metrics['union_cells']} union)"
    )
    print(f"  Dice              {metrics['dice']:.3f}")
    print(
        f"  Place-overlap     {metrics['place_overlap']:.3f}  "
        f"({metrics['places_both']} places in both / "
        f"{metrics['places_either']} in either)"
    )
    print(f"  Cosine similarity {metrics['cosine']:.3f}")
    print(
        f"  JSD               {metrics['jsd']:.3f}  "
        f"(similarity {metrics['jsd_sim']:.3f})"
    )
    print(
        f"  Coverage  {label_a}→{label_b}: {metrics['cov_a_in_b']:.3f}  "
        f"({metrics['shared_cells']} of {metrics['lang_b_cells']} cells "
        f"in {label_b} are also in {label_a})"
    )
    print(
        f"  Coverage  {label_b}→{label_a}: {metrics['cov_b_in_a']:.3f}  "
        f"({metrics['shared_cells']} of {metrics['lang_a_cells']} cells "
        f"in {label_a} are also in {label_b})"
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
        suffix = "_polished" if args.style == "polished" else ""
        out_path = out_dir / f"overlay_{a_slug}_vs_{b_slug}{suffix}.svg"

    if args.style == "polished":
        svg = render_overlay_polished(
            cfg_a, cfg_b, cells_a, cells_b, metrics, label_a, label_b
        )
    else:
        svg = render_overlay(
            cfg_a, cfg_b, cells_a, cells_b, metrics, label_a, label_b
        )
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
