#!/usr/bin/env python3
"""
fig_vikarana_examples.py — Ch 11 §11.3 (Building the Kriyā).

Six worked examples of the *dhātu* + *gaṇa-vikaraṇa* + *tiṅ-ending* pipeline,
visualized with the kriyā figure conventions:

    THREE-TIER PROVENANCE (fill color):
        light    #dcdcdc  → original dhātu varṇa (unchanged or in the core slot)
        medium   #888888  → vikaraṇa material, OR vikaraṇa-induced modification
                            of dhātu material (e.g., guṇa, lengthening, redup)
        dark     #555555  → tiṅ-ending material

    THREE-RAIL LAYOUT (vertical position):
        upper    y = -3·HEX_HEIGHT/4   → any vowel that is NOT the dhātu's
                                         original particle still present in the
                                         form (vikaraṇa, ending, reduplicated,
                                         guṇa-replacement, lengthening, etc.)
        middle   y = -HEX_HEIGHT/4     → any consonant
        lower    y = +HEX_HEIGHT/4     → ONLY the dhātu's original vowel,
                                         surviving unchanged in the form

    MĀTRĀ LINE (bottom of strip):
        A horizontal line spanning the strip's mātrā extent, with major ticks
        at every whole mātrā and minor ticks at every half. No labels.
        Convention: C = ½ mātrā, V1 = 1 mātrā, V2 = 2 mātrā.

    CLUSTER COMPRESSION:
        adjacent consonants merge into ONE hexagon (½ mātrā per cell, total
        width = n × EDGE_LENGTH/2), with a vertical divider line between
        cells. Each cell takes its particle's provenance color, so a mixed-
        provenance cluster like s+t in *asti* renders split-color (s light,
        t dark).

Outputs:
    figures/build/building_kriya_vikarana_examples.svg   (composite, all 6)
    figures/building_kriya/output/vikarana_<gana>.svg    (per example)
"""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))

from dhatu_hexagon import (  # noqa: E402
    EDGE_LENGTH,
    HEX_HEIGHT,
    VARNAS,
    is_ayogavaha,
)


# ===========================================================================
# Provenance encoding
# ===========================================================================

PROV_FILL = {
    "original": "#dcdcdc",
    "vikarana": "#888888",
    "ending":   "#555555",
}
PROV_DEV_COLOR = {
    "original": "#1a1a1a",
    "vikarana": "#1a1a1a",
    "ending":   "#f5f5f5",
}
PROV_IAST_COLOR = {
    "original": "#333333",
    "vikarana": "#222222",
    "ending":   "#d8d8d8",
}

STROKE_COLOR = "#1a1a1a"
STROKE_WIDTH = 1.4

DIVIDER_COLOR = "#1a1a1a"
DIVIDER_WIDTH = 0.9
DIVIDER_PAD   = 8

DEV_FONT = ("Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, "
            "Arial Unicode MS, sans-serif")
LATIN_FONT = "Charter, Georgia, Times, serif"


# ===========================================================================
# Three-rail geometry
# ===========================================================================

LOWER_RAIL_Y  =  HEX_HEIGHT / 4         # core dhātu vowels
MIDDLE_RAIL_Y = -HEX_HEIGHT / 4         # consonants
UPPER_RAIL_Y  = -3 * HEX_HEIGHT / 4     # non-core vowels (vikaraṇa, ending, redup)

# ===========================================================================
# Geometry — locked so that each hexagon's midpoint-to-midpoint extent
# equals exactly its mātrā count × MATRA_UNIT
# ===========================================================================
#
# 1 mātrā = 60 px (the midpoint-to-midpoint span of a V1 hexagon).
# Slant length e = EDGE_LENGTH = 40 (kept from the parent module so
# HEX_HEIGHT is unchanged). Top-edge widths are then derived to satisfy
# the midpoint = mātrā × unit identity:
#
#   class   top edge   midpoint extent   mātrā value
#   C       10 px      30 px             0.5
#   V1      40 px      60 px             1.0
#   V2      100 px     120 px            2.0
#
# The C hexagons are visibly shorter — a consonant is a short sound, and
# the geometry matches that. Cluster cells (½ mātrā each) carry 20 px of
# top-edge width inside a 40 px cluster envelope.

WIDTH_C    = 10
WIDTH_V1   = 40
WIDTH_V2   = 100
MATRA_UNIT = 60


# ===========================================================================
# Examples — six gaṇas
# ===========================================================================
#
# Each particle dict:
#   tok:  Harvard-Kyoto or IAST token (resolved against VARNAS)
#   prov: "original" | "vikarana" | "ending"
#   core: True if this vowel occupies the dhātu's core vowel slot (lower rail).
#         Omit (or False) for consonants and for non-core vowels (upper rail).

EXAMPLES = [
    {
        "slug": "bhvadi",
        "gana": "bhvādi",
        "gana_dev": "भ्वादि",
        "vikarana": "śap (a)",
        "dhatu_dev": "पच्",
        "dhatu_iast": "pac",
        "form_dev": "पचति",
        "form_iast": "pacati",
        "particles": [
            {"tok": "p", "prov": "original"},
            {"tok": "a", "prov": "original", "core": True},
            {"tok": "c", "prov": "original"},
            {"tok": "a", "prov": "vikarana"},
            {"tok": "t", "prov": "ending"},
            {"tok": "i", "prov": "ending"},
        ],
    },
    {
        "slug": "adadi",
        "gana": "adādi",
        "gana_dev": "अदादि",
        "vikarana": "zero (athematic)",
        "dhatu_dev": "अस्",
        "dhatu_iast": "as",
        "form_dev": "अस्ति",
        "form_iast": "asti",
        "particles": [
            {"tok": "a", "prov": "original", "core": True},
            {"tok": "s", "prov": "original"},
            {"tok": "t", "prov": "ending"},
            {"tok": "i", "prov": "ending"},
        ],
    },
    {
        "slug": "juhotyadi",
        "gana": "juhotyādi",
        "gana_dev": "जुहोत्यादि",
        "vikarana": "ślu (reduplication)",
        "dhatu_dev": "हु",
        "dhatu_iast": "hu",
        "form_dev": "जुहोति",
        "form_iast": "juhoti",
        "particles": [
            {"tok": "j", "prov": "vikarana"},  # reduplicated h → j (palatalization)
            {"tok": "u", "prov": "vikarana"},  # reduplicated vowel
            {"tok": "h", "prov": "original"},
            {"tok": "o", "prov": "vikarana"},  # guṇa-replaces u; original u is gone, so NEW → upper rail
            {"tok": "t", "prov": "ending"},
            {"tok": "i", "prov": "ending"},
        ],
    },
    {
        "slug": "divadi",
        "gana": "divādi",
        "gana_dev": "दिवादि",
        "vikarana": "śyan (ya)",
        "dhatu_dev": "दिव्",
        "dhatu_iast": "div",
        "form_dev": "दीव्यति",
        "form_iast": "dīvyati",
        "particles": [
            {"tok": "d", "prov": "original"},
            {"tok": "I", "prov": "vikarana"},   # i lengthened to ī; original i is gone, so NEW → upper rail
            {"tok": "v", "prov": "original"},
            {"tok": "y", "prov": "vikarana"},   # śyan
            {"tok": "a", "prov": "vikarana"},   # śyan thematic vowel
            {"tok": "t", "prov": "ending"},
            {"tok": "i", "prov": "ending"},
        ],
    },
    {
        "slug": "tanadi",
        "gana": "tanādi",
        "gana_dev": "तनादि",
        "vikarana": "u/o",
        "dhatu_dev": "कृ",
        "dhatu_iast": "kṛ",
        "form_dev": "करोति",
        "form_iast": "karoti",
        "particles": [
            {"tok": "k", "prov": "original"},
            {"tok": "a", "prov": "vikarana"},   # guṇa half of ṛ; original ṛ is gone, so NEW → upper rail
            {"tok": "r", "prov": "vikarana"},   # consonant from ṛ guṇa — intermediate (vikaraṇa-induced)
            {"tok": "o", "prov": "vikarana"},   # tanādi u/o
            {"tok": "t", "prov": "ending"},
            {"tok": "i", "prov": "ending"},
        ],
    },
    {
        "slug": "curadi",
        "gana": "curādi",
        "gana_dev": "चुरादि",
        "vikarana": "ṇic (aya)",
        "dhatu_dev": "चुर्",
        "dhatu_iast": "cur",
        "form_dev": "चोरयति",
        "form_iast": "corayati",
        "particles": [
            {"tok": "c", "prov": "original"},
            {"tok": "o", "prov": "vikarana"},    # guṇa-replaces u; original u is gone, so NEW → upper rail
            {"tok": "r", "prov": "original"},
            {"tok": "a", "prov": "vikarana"},
            {"tok": "y", "prov": "vikarana"},
            {"tok": "a", "prov": "vikarana"},
            {"tok": "t", "prov": "ending"},
            {"tok": "i", "prov": "ending"},
        ],
    },
]


# ===========================================================================
# Token resolution
# ===========================================================================

ALIASES = {
    "A": "ā", "I": "ī", "U": "ū", "R": "ṛ", "RR": "ṝ",
    "T": "ṭ", "Th": "ṭh", "D": "ḍ", "Dh": "ḍh", "N": "ṇ",
    "G": "ṅ", "J": "ñ", "S": "ṣ", "z": "ś", "M": "ṃ", "H": "ḥ",
}

HALANT = "्"


def varna_for(token):
    key = ALIASES.get(token, token)
    if key not in VARNAS:
        raise ValueError(f"Unknown varṇa token: {token!r}")
    return dict(VARNAS[key])


def deva_label(varna):
    """Devanagari label with halant for pure consonants."""
    if varna["class"] == "C" and not is_ayogavaha(varna):
        return varna["deva"] + HALANT
    return varna["deva"]


# ===========================================================================
# Unit grouping — adjacent consonants compress to a cluster
# ===========================================================================

def build_units(particles):
    """Group adjacent consonant runs into cluster units.

    A unit is a dict:
        {"kind": "particle", "varna": ..., "prov": ..., "core": ...}
        {"kind": "cluster",  "cells": [{"varna":..., "prov":...}, ...]}
    """
    units = []
    i = 0
    while i < len(particles):
        cur = particles[i]
        v = varna_for(cur["tok"])
        if v["class"] == "C" and not is_ayogavaha(v):
            # gather a run of consonants
            run = [(v, cur["prov"])]
            j = i + 1
            while j < len(particles):
                vj = varna_for(particles[j]["tok"])
                if vj["class"] == "C" and not is_ayogavaha(vj):
                    run.append((vj, particles[j]["prov"]))
                    j += 1
                else:
                    break
            if len(run) > 1:
                units.append({
                    "kind": "cluster",
                    "cells": [{"varna": vv, "prov": pp} for (vv, pp) in run],
                })
                i = j
                continue
        units.append({
            "kind": "particle",
            "varna": v,
            "prov": cur["prov"],
            "core": cur.get("core", False),
        })
        i += 1
    return units


# ===========================================================================
# Layout — three-rail with slanted-edge sharing
# ===========================================================================

def unit_width(unit):
    if unit["kind"] == "cluster":
        # Cluster of n cells = n × ½ mātrā in timing. Total midpoint extent =
        # n × ½ × MATRA_UNIT. Top-edge width = midpoint extent − e/2.
        n = len(unit["cells"])
        return n * 0.5 * MATRA_UNIT - EDGE_LENGTH / 2
    v = unit["varna"]
    if v["class"] == "C":
        return WIDTH_C
    if v["class"] == "V1":
        return WIDTH_V1
    if v["class"] == "V2":
        return WIDTH_V2
    return WIDTH_V1


def unit_rail_y(unit):
    if unit["kind"] == "cluster":
        return MIDDLE_RAIL_Y
    v = unit["varna"]
    if is_ayogavaha(v):
        return LOWER_RAIL_Y
    if v["class"] == "C":
        return MIDDLE_RAIL_Y
    # Vowel — split by core/non-core
    if unit.get("core", False):
        return LOWER_RAIL_Y
    return UPPER_RAIL_Y


def layout_units(units):
    """Compute (cx, cy) for each unit. Adjacent rails share slanted edges."""
    positions = []
    for i, u in enumerate(units):
        cy = unit_rail_y(u)
        if i == 0:
            positions.append((0.0, cy))
            continue
        prev = units[i - 1]
        prev_cy = positions[-1][1]
        prev_w = unit_width(prev)
        w = unit_width(u)
        rail_step = EDGE_LENGTH / 2 if prev_cy != cy else EDGE_LENGTH
        cx_new = positions[-1][0] + (prev_w + w) / 2 + rail_step
        positions.append((cx_new, cy))
    return positions


# ===========================================================================
# Hexagon geometry
# ===========================================================================

def hex_vertices(cx, cy, w):
    """Six vertices of a hexagon centered at (cx, cy) with top/bottom edge w."""
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    return [
        (cx - w / 2,         cy - h / 2),   # top-left
        (cx + w / 2,         cy - h / 2),   # top-right
        (cx + w / 2 + e / 2, cy),           # rightmost
        (cx + w / 2,         cy + h / 2),   # bottom-right
        (cx - w / 2,         cy + h / 2),   # bottom-left
        (cx - w / 2 - e / 2, cy),           # leftmost
    ]


def cluster_cell_polygon(cx, cy, w, n_cells, cell_idx):
    """Return polygon vertices for one cell inside a cluster hexagon.

    The hexagon is centred at (cx, cy) with total top/bottom edge width w
    and slanted left/right side-tips at ±(w/2 + e/2). Cells slice the
    hexagon by vertical lines at x = cx - w/2 + k * cell_w for k in 1..n-1.
    """
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    cell_w = w / n_cells
    left_x = cx - w / 2 + cell_idx * cell_w
    right_x = cx - w / 2 + (cell_idx + 1) * cell_w

    pts = []
    # Top-left
    if cell_idx == 0:
        pts.append((left_x, cy - h / 2))
    else:
        pts.append((left_x, cy - h / 2))
    # Top-right
    if cell_idx == n_cells - 1:
        pts.append((right_x, cy - h / 2))
        # Add rightmost slanted tip
        pts.append((right_x + e / 2, cy))
        pts.append((right_x, cy + h / 2))
    else:
        pts.append((right_x, cy - h / 2))
        pts.append((right_x, cy + h / 2))
    # Bottom-left
    pts.append((left_x, cy + h / 2))
    if cell_idx == 0:
        pts.append((left_x - e / 2, cy))
    return pts


# ===========================================================================
# Rendering
# ===========================================================================

def render_particle(cx, cy, varna, prov):
    w = unit_width({"kind": "particle", "varna": varna, "prov": prov})
    verts = hex_vertices(cx, cy, w)
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts)

    fill = PROV_FILL[prov]
    dev_color = PROV_DEV_COLOR[prov]
    iast_color = PROV_IAST_COLOR[prov]

    out = [
        f'<polygon points="{pts}" fill="{fill}" stroke="{STROKE_COLOR}" '
        f'stroke-width="{STROKE_WIDTH}" stroke-linejoin="round"/>',
        f'<text x="{cx:.1f}" y="{cy + 0.5:.1f}" '
        f'font-family="{DEV_FONT}" font-size="22" font-weight="500" '
        f'text-anchor="middle" dominant-baseline="middle" fill="{dev_color}">'
        f'{deva_label(varna)}</text>',
        f'<text x="{cx:.1f}" y="{cy + 19:.1f}" '
        f'font-family="{LATIN_FONT}" font-size="11" font-style="italic" '
        f'text-anchor="middle" dominant-baseline="middle" fill="{iast_color}">'
        f'{varna["iast"]}</text>',
    ]
    return "\n  ".join(out)


# Global counter for cluster clip-path IDs — needs to be unique across each SVG
_cluster_id_counter = itertools.count()


def render_cluster(cx, cy, unit):
    """Render a consonant cluster: one hexagon, n cells with per-cell fills,
    a single Devanagari conjunct centered on the cluster (two-pass rendered
    so each cell-half of the conjunct uses its own cell's text color via
    SVG clip-paths), and per-cell roman labels at the bottom."""
    cells = unit["cells"]
    n = len(cells)
    w = unit_width(unit)     # mātrā-locked width matching the layout
    h = HEX_HEIGHT
    e = EDGE_LENGTH
    cell_w = w / n

    cluster_id = next(_cluster_id_counter)

    out = []

    # 1) Per-cell colored polygons (no stroke; outer hexagon stroke comes next)
    for i, cell in enumerate(cells):
        cell_pts = cluster_cell_polygon(cx, cy, w, n, i)
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in cell_pts)
        out.append(
            f'<polygon points="{pts}" fill="{PROV_FILL[cell["prov"]]}" '
            f'stroke="none"/>'
        )

    # 2) Outer hexagon outline (stroke only)
    outer = hex_vertices(cx, cy, w)
    outer_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in outer)
    out.append(
        f'<polygon points="{outer_pts}" fill="none" stroke="{STROKE_COLOR}" '
        f'stroke-width="{STROKE_WIDTH}" stroke-linejoin="round"/>'
    )

    # 3) (No internal divider line — the per-cell background colors carry
    #    the cluster boundary visually; an explicit black divider was cutting
    #    through the conjunct character.)

    # 4) Define clip-paths — one per cell — for two-pass conjunct rendering.
    # Each clip is a vertical strip covering the cell's region (extended to
    # the slant tips on the outer edges so glyph extents outside the top edge
    # are not visually truncated).
    defs_parts = []
    for i in range(n):
        clip_id = f"kriya-cluster-{cluster_id}-cell{i}"
        left_x = cx - w / 2 + i * cell_w
        right_x = cx - w / 2 + (i + 1) * cell_w
        if i == 0:
            left_x -= e / 2          # include leftmost slant tip
        if i == n - 1:
            right_x += e / 2         # include rightmost slant tip
        defs_parts.append(
            f'<clipPath id="{clip_id}"><rect x="{left_x:.1f}" y="{cy - h:.1f}" '
            f'width="{right_x - left_x:.1f}" height="{2 * h:.1f}"/></clipPath>'
        )
    out.append(f'<defs>{"".join(defs_parts)}</defs>')

    # 5) Render the Devanagari conjunct n times — once per cell — each
    # rendering clipped to its cell's vertical strip and using that cell's
    # provenance-appropriate text color. The conjunct is built by joining
    # consonant bases with HALANT (no trailing halant; the next hexagon's
    # vowel attaches implicitly in the larger word context).
    conjunct = HALANT.join(c["varna"]["deva"] for c in cells)
    for i, cell in enumerate(cells):
        clip_id = f"kriya-cluster-{cluster_id}-cell{i}"
        text_color = PROV_DEV_COLOR[cell["prov"]]
        out.append(
            f'<text x="{cx:.1f}" y="{cy - 2:.1f}" '
            f'font-family="{DEV_FONT}" font-size="20" font-weight="500" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'fill="{text_color}" clip-path="url(#{clip_id})">'
            f'{conjunct}</text>'
        )

    # 6) Per-cell roman labels at the bottom, each in its own provenance color
    for i, cell in enumerate(cells):
        v = cell["varna"]
        prov = cell["prov"]
        label_x = cx - w / 2 + cell_w * (i + 0.5)
        out.append(
            f'<text x="{label_x:.1f}" y="{cy + 17:.1f}" '
            f'font-family="{LATIN_FONT}" font-size="9" font-style="italic" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'fill="{PROV_IAST_COLOR[prov]}">'
            f'{v["iast"]}</text>'
        )

    return "\n  ".join(out)


def render_unit(cx, cy, unit):
    if unit["kind"] == "cluster":
        return render_cluster(cx, cy, unit)
    return render_particle(cx, cy, unit["varna"], unit["prov"])


# ===========================================================================
# Strip layout + composition
# ===========================================================================

def strip_extent(units, positions):
    e = EDGE_LENGTH
    xs = []
    ys = []
    h = HEX_HEIGHT
    for u, (cx, cy) in zip(units, positions):
        w = unit_width(u)
        xs.extend([cx - w / 2 - e / 2, cx + w / 2 + e / 2])
        ys.extend([cy - h / 2, cy + h / 2])
    return min(xs), max(xs), min(ys), max(ys)


def total_matras(units):
    """Total mātrā count for a unit list. C = ½, V1 = 1, V2 = 2.
    Cluster of n consonants = n × ½."""
    total = 0.0
    for u in units:
        if u["kind"] == "cluster":
            total += 0.5 * len(u["cells"])
        else:
            v = u["varna"]
            if v["class"] == "C":
                total += 0.5
            elif v["class"] == "V1":
                total += 1.0
            elif v["class"] == "V2":
                total += 2.0
    return total


def render_matra_line(tx, line_y, n_matras):
    """Horizontal ruler with ticks. `tx` is the canvas x of the strip's
    leftmost slant tip; `line_y` is the absolute canvas y of the ruler line.
    First tick lands at the leftmost particle's left-side midpoint (e/4 inside
    the slant-tip overhang). Major ticks at every whole mātrā, minor at every
    half mātrā. No labels."""
    if n_matras <= 0:
        return ""
    start_x = tx + EDGE_LENGTH / 4   # left-side midpoint of leftmost hexagon
    line_len = n_matras * MATRA_UNIT
    end_x = start_x + line_len

    color = "#888"
    out = []
    out.append(
        f'<line x1="{start_x:.1f}" y1="{line_y:.1f}" '
        f'x2="{end_x:.1f}" y2="{line_y:.1f}" '
        f'stroke="{color}" stroke-width="1.2"/>'
    )

    # Half-mātrā steps; major ticks at integer steps, minor at half steps.
    # Ticks go UPWARD from the line (toward the strip).
    n_half_steps = int(round(n_matras * 2))
    for i in range(n_half_steps + 1):
        x = start_x + i * MATRA_UNIT / 2
        is_major = (i % 2 == 0)
        tick_len = 8 if is_major else 4
        tick_w = 1.2 if is_major else 1.0
        out.append(
            f'<line x1="{x:.1f}" y1="{line_y:.1f}" '
            f'x2="{x:.1f}" y2="{line_y - tick_len:.1f}" '
            f'stroke="{color}" stroke-width="{tick_w}"/>'
        )
    return "\n  ".join(out)


def strip_vertical_extent(units):
    """Return (top_rel, bottom_rel) — the y extent of the strip's hexagons
    relative to the strip midline. Used to compute dynamic title and mātrā
    line positions."""
    rails = set()
    for u in units:
        if u["kind"] == "cluster":
            rails.add(MIDDLE_RAIL_Y)
        else:
            rails.add(unit_rail_y(u))
    if not rails:
        return 0.0, 0.0
    top = min(rail - HEX_HEIGHT / 2 for rail in rails)
    bottom = max(rail + HEX_HEIGHT / 2 for rail in rails)
    return top, bottom


def render_strip(particles, tx, ty):
    """Render just the hexagon strip (no mātrā line — render_example_block
    handles that separately so the line can sit at a dynamic y)."""
    units = build_units(particles)
    positions = layout_units(units)
    xmin, xmax, _ymin, _ymax = strip_extent(units, positions)
    shift_x = tx - xmin

    out = []
    for u, (cx, cy) in zip(units, positions):
        out.append(
            f'<g transform="translate({shift_x:.1f},{ty:.1f})">'
            f'{render_unit(cx, cy, u)}'
            f'</g>'
        )

    return "\n  ".join(out), xmax - xmin


# Vertical padding (text baseline / line position to nearest strip-hex edge)
STRIP_PAD = 15
# Baseline-to-baseline spacing between title and vikaraṇa note
TITLE_NOTE_GAP = 22


def render_example_block(example, tx, ty):
    """Header (gaṇa, dhātu → form, vikaraṇa note) + hexagon strip + mātrā ruler.
    Title and ruler are positioned DYNAMICALLY based on the strip's actual
    vertical extent — 15 px padding above topmost hex and below bottommost hex,
    regardless of which rails the strip uses."""
    units = build_units(example["particles"])
    strip_top_rel, strip_bottom_rel = strip_vertical_extent(units)

    # Dynamic y positions
    note_y = ty + strip_top_rel - STRIP_PAD
    title_y = note_y - TITLE_NOTE_GAP
    matra_y = ty + strip_bottom_rel + STRIP_PAD

    out = []
    out.append(
        f'<text x="{tx:.1f}" y="{title_y:.1f}" '
        f'font-family="{LATIN_FONT}" font-size="16" font-weight="600" '
        f'fill="#1a1a1a">'
        f'<tspan font-family="{DEV_FONT}">{example["gana_dev"]}</tspan>'
        f' <tspan font-style="italic">({example["gana"]})</tspan>'
        f'  ·  <tspan font-family="{DEV_FONT}">{example["dhatu_dev"]}</tspan>'
        f' <tspan font-style="italic">({example["dhatu_iast"]})</tspan>'
        f' → <tspan font-family="{DEV_FONT}" font-weight="700">'
        f'{example["form_dev"]}</tspan>'
        f' <tspan font-style="italic">({example["form_iast"]})</tspan>'
        f'</text>'
    )
    out.append(
        f'<text x="{tx:.1f}" y="{note_y:.1f}" '
        f'font-family="{LATIN_FONT}" font-size="12" font-style="italic" '
        f'fill="#555">'
        f'vikaraṇa: {example["vikarana"]}'
        f'</text>'
    )

    strip_svg, strip_w = render_strip(example["particles"], tx, ty)
    out.append(strip_svg)

    n_matras = total_matras(units)
    out.append(render_matra_line(tx, matra_y, n_matras))

    return "\n  ".join(out), strip_w


def render_legend(cx, cy):
    out = []
    sw, sh = 28, 18
    cell_pad = 28
    items = [
        ("original", "original dhātu"),
        ("vikarana", "vikaraṇa"),
        ("ending",   "tiṅ-ending"),
    ]
    # Compute label widths approximately
    item_widths = [180, 130, 140]
    total = sum(item_widths) + cell_pad * len(items)
    x = cx - total / 2

    out.append(
        f'<text x="{x - 10:.1f}" y="{cy + 2:.1f}" '
        f'font-family="{LATIN_FONT}" font-size="12" font-weight="600" '
        f'fill="#1a1a1a" text-anchor="end">provenance:</text>'
    )
    cur_x = x
    for (prov, label), w_item in zip(items, item_widths):
        out.append(
            f'<rect x="{cur_x:.1f}" y="{cy - sh / 2:.1f}" '
            f'width="{sw}" height="{sh}" fill="{PROV_FILL[prov]}" '
            f'stroke="{STROKE_COLOR}" stroke-width="1.2"/>'
        )
        out.append(
            f'<text x="{cur_x + sw + 6:.1f}" y="{cy + 4:.1f}" '
            f'font-family="{LATIN_FONT}" font-size="12" fill="#1a1a1a">'
            f'{label}</text>'
        )
        cur_x += w_item + cell_pad
    return "\n  ".join(out)


# ===========================================================================
# Composite + per-example output
# ===========================================================================

def render_composite():
    margin_left = 60
    margin_top = 50
    row_height = 220
    canvas_w = 1200
    canvas_h = margin_top + 100 + len(EXAMPLES) * row_height + 40

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" '
        f'width="{canvas_w}" height="{canvas_h}">'
    )
    out.append('  <title>Vikaraṇa operations — six examples</title>')
    out.append(
        f'  <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" fill="white"/>'
    )

    # Title
    out.append(
        f'  <text x="{canvas_w / 2:.1f}" y="32" text-anchor="middle" '
        f'font-family="{LATIN_FONT}" font-size="20" font-weight="700" '
        f'fill="#1a1a1a">The Vikaraṇa Operation — Six Worked Examples</text>'
    )

    # Legend
    out.append("  " + render_legend(canvas_w / 2, margin_top + 30))

    strip_top = margin_top + 130
    for i, ex in enumerate(EXAMPLES):
        ty = strip_top + i * row_height
        block_svg, _ = render_example_block(ex, margin_left, ty)
        out.append("  " + block_svg)

    out.append("</svg>")
    return "\n".join(out)


def render_single(example):
    """Render one example as a standalone SVG, with canvas dimensions sized
    to the actual block (so each example is as tight or as tall as it needs)."""
    units = build_units(example["particles"])
    positions = layout_units(units)
    xmin, xmax, _, _ = strip_extent(units, positions)
    strip_top_rel, strip_bottom_rel = strip_vertical_extent(units)

    # Block vertical extent relative to strip midline
    block_top_rel = strip_top_rel - STRIP_PAD - TITLE_NOTE_GAP - 6  # 6 = title text top-of-glyph above baseline
    block_bottom_rel = strip_bottom_rel + STRIP_PAD + 10            # 10 = tick + small gap

    margin_top = 20
    margin_bottom = 20

    canvas_h = int(margin_top + (block_bottom_rel - block_top_rel) + margin_bottom)
    ty = margin_top - block_top_rel   # so block_top_rel + ty = margin_top

    canvas_w = int(xmax - xmin + 120)
    tx = 60

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" '
        f'width="{canvas_w}" height="{canvas_h}">'
    )
    out.append(f'  <title>{example["dhatu_iast"]} → {example["form_iast"]}</title>')
    out.append(
        f'  <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" fill="white"/>'
    )
    block_svg, _ = render_example_block(example, tx, ty)
    out.append("  " + block_svg)
    out.append("</svg>")
    return "\n".join(out)


def main():
    indiv_dir = REPO_ROOT / "figures" / "building_kriya" / "output"
    indiv_dir.mkdir(parents=True, exist_ok=True)
    build_dir = REPO_ROOT / "figures" / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    composite = render_composite()
    out_path = build_dir / "building_kriya_vikarana_examples.svg"
    out_path.write_text(composite, encoding="utf-8")
    print(f"Wrote {out_path}")

    for ex in EXAMPLES:
        svg = render_single(ex)
        p = indiv_dir / f"vikarana_{ex['slug']}.svg"
        p.write_text(svg, encoding="utf-8")
        print(f"Wrote {p}")


if __name__ == "__main__":
    main()
