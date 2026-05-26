#!/usr/bin/env python3
"""
fig_assembly_examples.py — Ch 11 figures: assembling kriyās.

Visualizes the COMPOSITIONAL OPERATION that builds a finite verb form from
its parts (dhātu + vikaraṇa + tiṅ-ending), one figure per gaṇa example.

For each example:

    Destination strip (lower portion of canvas):
        the dhātu's surviving particles drawn as FILLED hexagons (light-gray
        "original" provenance), with any vikaraṇa-induced TRANSFORMATIONS of
        dhātu material rendered as FILLED hexagons in the medium-gray
        "vikarana" provenance color (e.g., ī in dīvyati from dhātu's i; o in
        corayati from guṇa of u). The vikaraṇa's surface particles and the
        tiṅ-ending's surface particles appear as EMPTY (dashed-outline)
        placeholder hexagons to be filled by source-atom arrows.

    Source atoms (upper portion of canvas):
        the vikaraṇa source (if any) and the tiṅ-ending source as labeled
        atomic strips. Surviving particles dark-filled; Pāṇinian anubandhas
        (it-markers) rendered with dashed outline and no fill.

    Arrows:
        from each surviving source-particle (bottom of hex) down to its
        corresponding empty destination slot (top of hex). One-to-many
        fan-out is supported (the curādi ṇic vikaraṇa's single surviving
        'i' surfaces as 'aya' — three destination slots from one source).

Output: figures/build/building_kriya_<slug>_assembly.svg, one per example.
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
# Geometry (Option 2 — matches fig_vikarana_examples.py)
# ===========================================================================

WIDTH_C    = 10
WIDTH_V1   = 40
WIDTH_V2   = 100
MATRA_UNIT = 60

LOWER_RAIL_Y  =  HEX_HEIGHT / 4
MIDDLE_RAIL_Y = -HEX_HEIGHT / 4
UPPER_RAIL_Y  = -3 * HEX_HEIGHT / 4

HALANT = "्"
DEV_FONT = ("Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, "
            "Arial Unicode MS, sans-serif")
LATIN_FONT = "Charter, Georgia, Times, serif"


# ===========================================================================
# Color palette
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

SOURCE_SURVIVING_FILL  = "#1a1a1a"
SOURCE_SURVIVING_DEV   = "#f5f5f5"
SOURCE_SURVIVING_IAST  = "#d8d8d8"

# "Context" — dhātu particle that survives directly into the destination
# (no transformation, no arrow). Rendered with the same light fill the
# destination uses for "original" provenance so the reader links source-atom
# context particle to its in-place destination counterpart.
SOURCE_CONTEXT_FILL  = "#dcdcdc"
SOURCE_CONTEXT_DEV   = "#1a1a1a"
SOURCE_CONTEXT_IAST  = "#333333"

ANUBANDHA_FILL       = "#ffffff"
ANUBANDHA_STROKE     = "#888888"
ANUBANDHA_DASH       = "4,3"
ANUBANDHA_DEV        = "#555555"
ANUBANDHA_IAST       = "#888888"

EMPTY_FILL   = "#ffffff"
EMPTY_STROKE = "#888888"
EMPTY_DASH   = "4,3"

STROKE_COLOR = "#1a1a1a"
STROKE_WIDTH = 1.4

ARROW_COLOR = "#444444"
ARROW_WIDTH = 1.6
ARROW_DASH   = "5,3"
ARROW_LABEL_FILL = "#333333"


# ===========================================================================
# Examples — one entry per gaṇa
# ===========================================================================
#
# Each example carries:
#   slug, form_dev, form_iast — for filename + header
#   header_subtitle — the "dhātu X + vikaraṇa Y + ending Z → form" line
#   destination — list of destination particles; each dict:
#       tok:   token (alias-resolved against VARNAS)
#       prov:  "original" | "vikarana" | "ending"
#       core:  True only for the dhātu's surviving original vowel
#       kind:  "filled" (dhātu material or vikaraṇa-induced transformation)
#              | "empty" (slot to be filled by a source-atom arrow)
#   vikarana_source — None (athematic) or dict:
#       title_dev, title_iast, subtitle
#       particles: list of {tok, role} where role ∈ {"surviving", "anubandha"}
#   ending_source — dict (always तिप् for the cases shown here)

EXAMPLES = [
    {
        "slug": "pacati",
        "form_dev": "पचति", "form_iast": "pacati",
        "header_subtitle": "dhātu पच् + vikaraṇa शप् + ending तिप् → पचति",
        "destination": [
            {"tok": "p", "prov": "original",                  "kind": "filled"},
            {"tok": "a", "prov": "original", "core": True,    "kind": "filled"},
            {"tok": "c", "prov": "original",                  "kind": "filled"},
            {"tok": "a", "prov": "vikarana",                  "kind": "empty"},
            {"tok": "t", "prov": "ending",                    "kind": "empty"},
            {"tok": "i", "prov": "ending",                    "kind": "empty"},
        ],
        "vikarana_source": {
            "title_dev": "शप्", "title_iast": "śap",
            "subtitle": "the bhvādi vikaraṇa",
            "particles": [
                {"tok": "z", "role": "anubandha"},   # ś (alias)
                {"tok": "a", "role": "surviving"},
                {"tok": "p", "role": "anubandha"},
            ],
        },
        "ending_source": {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "particles": [
                {"tok": "t", "role": "surviving"},
                {"tok": "i", "role": "surviving"},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    },
    {
        "slug": "asti",
        "form_dev": "अस्ति", "form_iast": "asti",
        "header_subtitle": "dhātu अस् + ending तिप् → अस्ति  (no surface vikaraṇa)",
        "destination": [
            {"tok": "a", "prov": "original", "core": True, "kind": "filled"},
            {"tok": "s", "prov": "original",               "kind": "filled"},
            {"tok": "t", "prov": "ending",                 "kind": "empty"},
            {"tok": "i", "prov": "ending",                 "kind": "empty"},
        ],
        "vikarana_source": None,
        "ending_source": {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "particles": [
                {"tok": "t", "role": "surviving"},
                {"tok": "i", "role": "surviving"},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    },
    {
        "slug": "divyati",
        "form_dev": "दीव्यति", "form_iast": "dīvyati",
        "header_subtitle": "dhātu दिव् + vikaraṇa श्यन् + ending तिप् → दीव्यति",
        # The dhātu's i is lengthened to ī (vikaraṇa-induced transformation).
        # Shown as an empty slot in the destination; filled by a dashed
        # transformation arrow from the dhātu source atom.
        "destination": [
            {"tok": "d", "prov": "original",                  "kind": "filled"},
            {"tok": "I", "prov": "vikarana",                  "kind": "empty"},   # ī, awaiting transformation arrow
            {"tok": "v", "prov": "original",                  "kind": "filled"},
            {"tok": "y", "prov": "vikarana",                  "kind": "empty"},   # śyaN surface
            {"tok": "a", "prov": "vikarana",                  "kind": "empty"},   # śyaN surface
            {"tok": "t", "prov": "ending",                    "kind": "empty"},
            {"tok": "i", "prov": "ending",                    "kind": "empty"},
        ],
        "dhatu_source": {
            "title_dev": "दिव्", "title_iast": "div",
            "subtitle": "the divādi dhātu",
            "particles": [
                {"tok": "d", "role": "context"},
                {"tok": "i", "role": "surviving", "transforms_to": "I", "label": "lengthened"},
                {"tok": "v", "role": "context"},
            ],
        },
        "vikarana_source": {
            "title_dev": "श्यन्", "title_iast": "śyaN",
            "subtitle": "the divādi vikaraṇa",
            "particles": [
                {"tok": "z", "role": "anubandha"},   # ś
                {"tok": "y", "role": "surviving"},
                {"tok": "a", "role": "surviving"},
                {"tok": "N", "role": "anubandha"},   # ṇ
            ],
        },
        "ending_source": {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "particles": [
                {"tok": "t", "role": "surviving"},
                {"tok": "i", "role": "surviving"},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    },
    {
        "slug": "corayati",
        "form_dev": "चोरयति", "form_iast": "corayati",
        "header_subtitle": "dhātu चुर् + vikaraṇa णिच् + ending तिप् → चोरयति",
        # The dhātu's u is guṇa-replaced by o (now empty in destination; arrow
        # from dhātu source). The ṇic vikaraṇa's single surviving 'i' surfaces
        # as 'aya' via guṇa + sandhi — fan-out from one source to three slots,
        # tagged with a single group label near the source particle.
        "destination": [
            {"tok": "c", "prov": "original",                  "kind": "filled"},
            {"tok": "o", "prov": "vikarana",                  "kind": "empty"},   # awaiting dhātu u → o arrow
            {"tok": "r", "prov": "original",                  "kind": "filled"},
            {"tok": "a", "prov": "vikarana",                  "kind": "empty"},   # first a of aya
            {"tok": "y", "prov": "vikarana",                  "kind": "empty"},   # y of aya
            {"tok": "a", "prov": "vikarana",                  "kind": "empty"},   # second a of aya
            {"tok": "t", "prov": "ending",                    "kind": "empty"},
            {"tok": "i", "prov": "ending",                    "kind": "empty"},
        ],
        "dhatu_source": {
            "title_dev": "चुर्", "title_iast": "cur",
            "subtitle": "the curādi dhātu",
            "particles": [
                {"tok": "c", "role": "context"},
                {"tok": "u", "role": "surviving", "transforms_to": "o", "label": "guṇa"},
                {"tok": "r", "role": "context"},
            ],
        },
        "vikarana_source": {
            "title_dev": "णिच्", "title_iast": "ṇic",
            "subtitle": "the curādi vikaraṇa",
            "particles": [
                {"tok": "N", "role": "anubandha"},   # ṇ
                # Single 'i' that surfaces as 'aya' across three destination slots;
                # fan-out label sits next to this source particle.
                {"tok": "i", "role": "surviving", "group_label": "→ aya"},
                {"tok": "c", "role": "anubandha"},
            ],
        },
        "ending_source": {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "particles": [
                {"tok": "t", "role": "surviving"},
                {"tok": "i", "role": "surviving"},
                {"tok": "p", "role": "anubandha"},
            ],
        },
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


def varna_for(token):
    key = ALIASES.get(token, token)
    if key not in VARNAS:
        raise ValueError(f"Unknown varṇa token: {token!r}")
    return dict(VARNAS[key])


def deva_label(varna):
    if varna["class"] == "C" and not is_ayogavaha(varna):
        return varna["deva"] + HALANT
    return varna["deva"]


# ===========================================================================
# Hexagon geometry helpers
# ===========================================================================

def hex_vertices(cx, cy, w):
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    return [
        (cx - w / 2,         cy - h / 2),
        (cx + w / 2,         cy - h / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2,         cy + h / 2),
        (cx - w / 2,         cy + h / 2),
        (cx - w / 2 - e / 2, cy),
    ]


def width_for(varna):
    if varna["class"] == "C":
        return WIDTH_C
    if varna["class"] == "V1":
        return WIDTH_V1
    if varna["class"] == "V2":
        return WIDTH_V2
    return WIDTH_V1


# ===========================================================================
# Destination strip layout
# ===========================================================================

def destination_layout(particles):
    """Compute (cx, cy, w, kind, varna, prov) for each particle in the
    destination strip. Vowels on LOWER rail if core, UPPER if not."""
    out = []
    cx_running = 0.0
    prev_cy = None
    prev_w = None
    for i, p in enumerate(particles):
        v = varna_for(p["tok"])
        w = width_for(v)
        if v["class"] == "C" or is_ayogavaha(v):
            cy = MIDDLE_RAIL_Y
        else:
            cy = LOWER_RAIL_Y if p.get("core") else UPPER_RAIL_Y

        if i == 0:
            cx = 0.0
        else:
            rail_step = EDGE_LENGTH / 2 if prev_cy != cy else EDGE_LENGTH
            cx = cx_running + (prev_w + w) / 2 + rail_step
        cx_running = cx
        prev_cy = cy
        prev_w = w
        out.append({
            "cx": cx, "cy": cy, "w": w,
            "varna": v, "prov": p["prov"], "kind": p["kind"],
        })
    return out


def destination_extent(positions):
    e = EDGE_LENGTH
    xs = []
    for p in positions:
        xs.extend([p["cx"] - p["w"] / 2 - e / 2, p["cx"] + p["w"] / 2 + e / 2])
    return min(xs), max(xs)


# ===========================================================================
# Source-atom layout — compact 2-rail strip
# ===========================================================================

def source_atom_layout(particles):
    """Each particle gets (cx, cy, w, role, varna, ...). C particles ride the
    upper sub-rail (MIDDLE_RAIL_Y); V particles ride the lower sub-rail
    (LOWER_RAIL_Y). cx values are local to the source atom. Extra particle
    fields (transforms_to, label, group_label) are preserved."""
    out = []
    cx_running = 0.0
    prev_cy = None
    prev_w = None
    for i, p in enumerate(particles):
        v = varna_for(p["tok"])
        w = width_for(v)
        cy = MIDDLE_RAIL_Y if v["class"] == "C" else LOWER_RAIL_Y
        if i == 0:
            cx = 0.0
        else:
            rail_step = EDGE_LENGTH / 2 if prev_cy != cy else EDGE_LENGTH
            cx = cx_running + (prev_w + w) / 2 + rail_step
        cx_running = cx
        prev_cy = cy
        prev_w = w
        out.append({
            **p,
            "cx": cx, "cy": cy, "w": w,
            "varna": v,
        })
    return out


def source_atom_extent(positions):
    e = EDGE_LENGTH
    xs = []
    ys = []
    for p in positions:
        xs.extend([p["cx"] - p["w"] / 2 - e / 2, p["cx"] + p["w"] / 2 + e / 2])
        ys.extend([p["cy"] - HEX_HEIGHT / 2, p["cy"] + HEX_HEIGHT / 2])
    return min(xs), max(xs), min(ys), max(ys)


# ===========================================================================
# Rendering — destination hexagons
# ===========================================================================

def render_filled_destination_hex(p):
    cx, cy, w = p["cx"], p["cy"], p["w"]
    verts = hex_vertices(cx, cy, w)
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts)
    fill = PROV_FILL[p["prov"]]
    dev_color = PROV_DEV_COLOR[p["prov"]]
    iast_color = PROV_IAST_COLOR[p["prov"]]
    out = []
    out.append(
        f'<polygon points="{pts}" fill="{fill}" stroke="{STROKE_COLOR}" '
        f'stroke-width="{STROKE_WIDTH}" stroke-linejoin="round"/>'
    )
    out.append(
        f'<text x="{cx:.1f}" y="{cy + 0.5:.1f}" '
        f'font-family="{DEV_FONT}" font-size="22" font-weight="500" '
        f'text-anchor="middle" dominant-baseline="middle" fill="{dev_color}">'
        f'{deva_label(p["varna"])}</text>'
    )
    out.append(
        f'<text x="{cx:.1f}" y="{cy + 19:.1f}" '
        f'font-family="{LATIN_FONT}" font-size="11" font-style="italic" '
        f'text-anchor="middle" dominant-baseline="middle" fill="{iast_color}">'
        f'{p["varna"]["iast"]}</text>'
    )
    return "\n  ".join(out)


def render_empty_destination_hex(p):
    cx, cy, w = p["cx"], p["cy"], p["w"]
    verts = hex_vertices(cx, cy, w)
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts)
    return (
        f'<polygon points="{pts}" fill="{EMPTY_FILL}" stroke="{EMPTY_STROKE}" '
        f'stroke-width="{STROKE_WIDTH}" stroke-dasharray="{EMPTY_DASH}" '
        f'stroke-linejoin="round"/>'
    )


def render_destination_strip(particles, tx, ty):
    """Render the destination strip; `tx` is the leftmost slant tip x."""
    positions = destination_layout(particles)
    xmin, _ = destination_extent(positions)
    shift_x = tx - xmin

    out = [f'<g transform="translate({shift_x:.1f},{ty:.1f})">']
    for p in positions:
        if p["kind"] == "empty":
            out.append("  " + render_empty_destination_hex(p))
        else:
            out.append("  " + render_filled_destination_hex(p))
    out.append("</g>")
    return "\n".join(out), positions, shift_x


# ===========================================================================
# Rendering — source-atom hexagons
# ===========================================================================

def render_source_hex(p):
    cx, cy, w = p["cx"], p["cy"], p["w"]
    verts = hex_vertices(cx, cy, w)
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts)

    if p["role"] == "surviving":
        fill = SOURCE_SURVIVING_FILL
        stroke = STROKE_COLOR
        dash_attr = ""
        dev_color = SOURCE_SURVIVING_DEV
        iast_color = SOURCE_SURVIVING_IAST
    elif p["role"] == "context":
        fill = SOURCE_CONTEXT_FILL
        stroke = STROKE_COLOR
        dash_attr = ""
        dev_color = SOURCE_CONTEXT_DEV
        iast_color = SOURCE_CONTEXT_IAST
    else:  # anubandha
        fill = ANUBANDHA_FILL
        stroke = ANUBANDHA_STROKE
        dash_attr = f' stroke-dasharray="{ANUBANDHA_DASH}"'
        dev_color = ANUBANDHA_DEV
        iast_color = ANUBANDHA_IAST

    out = []
    out.append(
        f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{STROKE_WIDTH}"{dash_attr} stroke-linejoin="round"/>'
    )
    out.append(
        f'<text x="{cx:.1f}" y="{cy + 0.5:.1f}" '
        f'font-family="{DEV_FONT}" font-size="22" font-weight="500" '
        f'text-anchor="middle" dominant-baseline="middle" fill="{dev_color}">'
        f'{deva_label(p["varna"])}</text>'
    )
    out.append(
        f'<text x="{cx:.1f}" y="{cy + 19:.1f}" '
        f'font-family="{LATIN_FONT}" font-size="11" font-style="italic" '
        f'text-anchor="middle" dominant-baseline="middle" fill="{iast_color}">'
        f'{p["varna"]["iast"]}</text>'
    )
    return "\n  ".join(out)


def render_source_atom(source, tx, ty):
    """Render a source atom centered horizontally at tx, with its midline at
    ty. Returns (svg, canvas_positions, atom_left_x, atom_right_x)."""
    positions = source_atom_layout(source["particles"])
    xmin, xmax, ymin, ymax = source_atom_extent(positions)
    shift_x = tx - (xmin + xmax) / 2   # center horizontally on tx

    canvas_positions = []
    for p in positions:
        canvas_positions.append({
            **p,
            "canvas_cx": p["cx"] + shift_x,
            "canvas_cy": p["cy"] + ty,
        })

    out = []
    out.append(f'<g transform="translate({shift_x:.1f},{ty:.1f})">')
    for p in positions:
        out.append("  " + render_source_hex(p))
    out.append("</g>")

    title_y = ty + ymin - 30
    subtitle_y = ty + ymin - 12
    out.append(
        f'<text x="{tx:.1f}" y="{title_y:.1f}" text-anchor="middle" '
        f'font-family="{LATIN_FONT}" font-size="15" font-weight="700" '
        f'fill="#1a1a1a">'
        f'<tspan font-family="{DEV_FONT}">{source["title_dev"]}</tspan>'
        f' <tspan font-style="italic">({source["title_iast"]})</tspan>'
        f'</text>'
    )
    out.append(
        f'<text x="{tx:.1f}" y="{subtitle_y:.1f}" text-anchor="middle" '
        f'font-family="{LATIN_FONT}" font-size="11" font-style="italic" '
        f'fill="#666">'
        f'{source["subtitle"]}</text>'
    )

    return "\n".join(out), canvas_positions, xmin + shift_x, xmax + shift_x


# ===========================================================================
# Arrows
# ===========================================================================

ARROW_HEAD_MARKER = '''  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="8"
            refX="9" refY="4" orient="auto" markerUnits="strokeWidth">
      <polygon points="0,0 9,4 0,8" fill="''' + ARROW_COLOR + '''"/>
    </marker>
  </defs>'''


def render_arrow(x1, y1, x2, y2, style="solid", label=None):
    """Cubic-Bezier arrow with optional dashed style and midpoint label."""
    dy = y2 - y1
    cy1 = y1 + dy * 0.5
    cy2 = y2 - dy * 0.4

    dash_attr = ""
    if style == "dashed":
        dash_attr = f' stroke-dasharray="{ARROW_DASH}"'

    parts = []
    parts.append(
        f'<path d="M {x1:.1f},{y1:.1f} C {x1:.1f},{cy1:.1f} '
        f'{x2:.1f},{cy2:.1f} {x2:.1f},{y2:.1f}" '
        f'fill="none" stroke="{ARROW_COLOR}" stroke-width="{ARROW_WIDTH}"'
        f'{dash_attr} marker-end="url(#arrowhead)"/>'
    )

    if label:
        # Cubic-Bezier midpoint at t=0.5
        mx = 0.5 * x1 + 0.5 * x2
        my = 0.125 * y1 + 0.375 * cy1 + 0.375 * cy2 + 0.125 * y2
        # White rect behind label to break the dashed line at the label
        rect_w = max(28, len(label) * 6 + 8)
        rect_h = 14
        parts.append(
            f'<rect x="{mx - rect_w / 2:.1f}" y="{my - rect_h / 2:.1f}" '
            f'width="{rect_w:.1f}" height="{rect_h}" fill="white" stroke="none"/>'
        )
        parts.append(
            f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" '
            f'dominant-baseline="middle" '
            f'font-family="{LATIN_FONT}" font-size="10" font-style="italic" '
            f'fill="{ARROW_LABEL_FILL}">{label}</text>'
        )

    return "\n  ".join(parts)


def compute_arrows(dest_positions, source_blocks):
    """Build arrow specs by provenance class:
        dhatu    — match each particle with `transforms_to` to a destination
                   empty slot whose iast equals the transforms_to token's iast.
                   Always dashed (transformation). Label from particle's `label`.
        vikarana — surviving particles → empty vikarana slots, in order.
                   Fan-out if 1 survivor and N empties (N>1).
                   Style: solid when src iast == dst iast, dashed otherwise.
        ending   — same as vikarana but on the ending provenance class.

    Returns list of {src, dst, style, label} dicts.
    """
    arrows = []
    by_prov = {b["prov"]: b["canvas_positions"] for b in source_blocks}

    # Track destination indices claimed by dhātu transformation arrows so they
    # are excluded from later vikaraṇa-class matching.
    dhatu_claimed = set()

    # Dhātu — explicit transforms_to mapping
    if "dhatu" in by_prov:
        for p in by_prov["dhatu"]:
            if p["role"] != "surviving":
                continue
            target_tok = p.get("transforms_to")
            if target_tok is None:
                continue
            target_iast = varna_for(target_tok)["iast"]
            dst_index = next(
                (i for i, d in enumerate(dest_positions)
                 if i not in dhatu_claimed and d["kind"] == "empty"
                 and d["varna"]["iast"] == target_iast),
                None,
            )
            if dst_index is None:
                continue
            dhatu_claimed.add(dst_index)
            arrows.append({
                "src": p, "dst": dest_positions[dst_index],
                "style": "dashed",
                "label": p.get("label"),
            })

    # Vikaraṇa and ending — provenance-class matching with fan-out
    for prov in ("vikarana", "ending"):
        if prov not in by_prov:
            continue
        survivors = [p for p in by_prov[prov] if p["role"] == "surviving"]
        empties = [p for i, p in enumerate(dest_positions)
                   if p["prov"] == prov and p["kind"] == "empty"
                   and i not in dhatu_claimed]
        if not survivors or not empties:
            continue
        if len(survivors) == 1 and len(empties) > 1:
            src = survivors[0]
            for dst in empties:
                style = "solid" if src["varna"]["iast"] == dst["varna"]["iast"] else "dashed"
                arrows.append({
                    "src": src, "dst": dst,
                    "style": style,
                    "label": None,   # group_label is rendered separately
                })
        else:
            for src, dst in zip(survivors, empties):
                style = "solid" if src["varna"]["iast"] == dst["varna"]["iast"] else "dashed"
                arrows.append({
                    "src": src, "dst": dst,
                    "style": style,
                    "label": src.get("label"),
                })
    return arrows


# ===========================================================================
# Cluster merging — for the FINAL strip only
# ===========================================================================
#
# In the intermediate strip, every particle stays as its own hexagon so each
# can be an arrow target. In the final strip, adjacent consonants merge into
# one hexagon with per-cell colors and a two-pass conjunct render (each cell
# clip-paths a copy of the Devanagari conjunct in its own provenance color).

_cluster_id_counter = itertools.count()


def build_units(particles):
    """Group adjacent (non-ayogavāha) consonants into cluster units."""
    units = []
    i = 0
    while i < len(particles):
        cur = particles[i]
        v = varna_for(cur["tok"])
        if v["class"] == "C" and not is_ayogavaha(v):
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


def unit_width(unit):
    if unit["kind"] == "cluster":
        # n × ½ mātrā timing; top-edge = midpoint extent − e/2
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
    if unit.get("core", False):
        return LOWER_RAIL_Y
    return UPPER_RAIL_Y


def layout_units(units):
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


def units_extent(units, positions):
    e = EDGE_LENGTH
    xs = []
    for u, (cx, _cy) in zip(units, positions):
        w = unit_width(u)
        xs.extend([cx - w / 2 - e / 2, cx + w / 2 + e / 2])
    return min(xs), max(xs)


def cluster_cell_polygon(cx, cy, w, n_cells, cell_idx):
    """Polygon vertices for one cell inside a cluster hexagon. Outer cells
    inherit the hexagon's slanted tips; interior boundaries are vertical."""
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    cell_w = w / n_cells
    left_x = cx - w / 2 + cell_idx * cell_w
    right_x = cx - w / 2 + (cell_idx + 1) * cell_w

    pts = [(left_x, cy - h / 2)]
    if cell_idx == n_cells - 1:
        pts.append((right_x, cy - h / 2))
        pts.append((right_x + e / 2, cy))
        pts.append((right_x, cy + h / 2))
    else:
        pts.append((right_x, cy - h / 2))
        pts.append((right_x, cy + h / 2))
    pts.append((left_x, cy + h / 2))
    if cell_idx == 0:
        pts.append((left_x - e / 2, cy))
    return pts


def render_cluster(cx, cy, unit):
    """Two-pass conjunct render: per-cell colored backgrounds, single outer
    outline, then one clipped copy of the Devanagari conjunct per cell so each
    half of the conjunct uses its own cell's provenance text color."""
    cells = unit["cells"]
    n = len(cells)
    w = unit_width(unit)
    h = HEX_HEIGHT
    e = EDGE_LENGTH
    cell_w = w / n

    cluster_id = next(_cluster_id_counter)

    out = []

    # 1) Per-cell colored polygons (no stroke)
    for i, cell in enumerate(cells):
        cell_pts = cluster_cell_polygon(cx, cy, w, n, i)
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in cell_pts)
        out.append(
            f'<polygon points="{pts}" fill="{PROV_FILL[cell["prov"]]}" '
            f'stroke="none"/>'
        )

    # 2) Outer hexagon outline only
    outer = hex_vertices(cx, cy, w)
    outer_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in outer)
    out.append(
        f'<polygon points="{outer_pts}" fill="none" stroke="{STROKE_COLOR}" '
        f'stroke-width="{STROKE_WIDTH}" stroke-linejoin="round"/>'
    )

    # 3) Per-cell clip-paths
    defs_parts = []
    for i in range(n):
        clip_id = f"kriya-assembly-cluster-{cluster_id}-cell{i}"
        left_x = cx - w / 2 + i * cell_w
        right_x = cx - w / 2 + (i + 1) * cell_w
        if i == 0:
            left_x -= e / 2
        if i == n - 1:
            right_x += e / 2
        defs_parts.append(
            f'<clipPath id="{clip_id}"><rect x="{left_x:.1f}" y="{cy - h:.1f}" '
            f'width="{right_x - left_x:.1f}" height="{2 * h:.1f}"/></clipPath>'
        )
    out.append(f'<defs>{"".join(defs_parts)}</defs>')

    # 4) Conjunct rendered N times, each clipped to its cell's strip
    conjunct = HALANT.join(c["varna"]["deva"] for c in cells)
    for i, cell in enumerate(cells):
        clip_id = f"kriya-assembly-cluster-{cluster_id}-cell{i}"
        text_color = PROV_DEV_COLOR[cell["prov"]]
        out.append(
            f'<text x="{cx:.1f}" y="{cy - 2:.1f}" '
            f'font-family="{DEV_FONT}" font-size="20" font-weight="500" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'fill="{text_color}" clip-path="url(#{clip_id})">'
            f'{conjunct}</text>'
        )

    # 5) Per-cell roman labels
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


def render_final_particle(cx, cy, varna, prov):
    if varna["class"] == "C":
        w = WIDTH_C
    elif varna["class"] == "V1":
        w = WIDTH_V1
    elif varna["class"] == "V2":
        w = WIDTH_V2
    else:
        w = WIDTH_V1
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


def render_unit(cx, cy, unit):
    if unit["kind"] == "cluster":
        return render_cluster(cx, cy, unit)
    return render_final_particle(cx, cy, unit["varna"], unit["prov"])


def render_final_strip(particles, canvas_w, ty):
    """Render the final assembled strip with consonant clusters merged.
    The strip is centered horizontally on canvas_w."""
    units = build_units(particles)
    positions = layout_units(units)
    xmin, xmax = units_extent(units, positions)
    strip_w = xmax - xmin
    tx = (canvas_w - strip_w) / 2          # leftmost slant tip x
    shift_x = tx - xmin

    out = [f'<g transform="translate({shift_x:.1f},{ty:.1f})">']
    for u, (cx, cy) in zip(units, positions):
        out.append("  " + render_unit(cx, cy, u))
    out.append("</g>")
    return "\n".join(out)


# ===========================================================================
# Layout — adaptive canvas width per example
# ===========================================================================
#
# Source atoms are packed left-to-right with SOURCE_GAP between them; the
# packed row is centered horizontally on the canvas. Destination strips
# (intermediate + final) are also centered horizontally. Canvas width is
# whichever of (source row, destination strip) is wider, plus padding.

CANVAS_H        = 660
PADDING_X       = 40
SOURCE_GAP      = 60
SOURCE_TY       = 160
INTERMEDIATE_TY = 400
FINAL_TY        = 570


def source_atom_width(source):
    positions = source_atom_layout(source["particles"])
    xmin, xmax, _, _ = source_atom_extent(positions)
    return xmax - xmin


def compute_layout(example):
    """Returns canvas_w, source_centers, dest_tx, dest_w."""
    source_widths = []
    if example.get("dhatu_source"):
        source_widths.append(source_atom_width(example["dhatu_source"]))
    if example.get("vikarana_source"):
        source_widths.append(source_atom_width(example["vikarana_source"]))
    source_widths.append(source_atom_width(example["ending_source"]))

    source_row_w = sum(source_widths) + (len(source_widths) - 1) * SOURCE_GAP

    dest_positions = destination_layout(example["destination"])
    dxmin, dxmax = destination_extent(dest_positions)
    dest_w = dxmax - dxmin

    canvas_w = max(source_row_w, dest_w) + 2 * PADDING_X

    # Pack source atoms left-to-right, row centered on canvas midline
    source_centers = []
    x = (canvas_w - source_row_w) / 2
    for w in source_widths:
        source_centers.append((x + w / 2, SOURCE_TY))
        x += w + SOURCE_GAP

    dest_tx = (canvas_w - dest_w) / 2
    return canvas_w, source_centers, dest_tx, dest_w


# ===========================================================================
# Composition
# ===========================================================================


def build_svg(example):
    canvas_w, source_centers, dest_tx, dest_w = compute_layout(example)
    canvas_h = CANVAS_H

    # Intermediate destination (with empty placeholders for arrows to land in)
    inter_svg, inter_positions, inter_shift_x = render_destination_strip(
        example["destination"], dest_tx, INTERMEDIATE_TY
    )
    for p in inter_positions:
        p["canvas_cx"] = p["cx"] + inter_shift_x
        p["canvas_cy"] = p["cy"] + INTERMEDIATE_TY
        p["canvas_top_y"] = p["canvas_cy"] - HEX_HEIGHT / 2

    # Final destination — every particle filled, adjacent consonants merged
    # into clusters with per-cell colors and two-pass conjunct rendering.
    final_svg = render_final_strip(example["destination"], canvas_w, FINAL_TY)

    # Source atoms in L-to-R reading order:
    #   dhātu (if transformation case) → vikaraṇa (if present) → ending
    source_specs = []
    if example.get("dhatu_source"):
        source_specs.append(("dhatu", example["dhatu_source"]))
    if example.get("vikarana_source"):
        source_specs.append(("vikarana", example["vikarana_source"]))
    source_specs.append(("ending", example["ending_source"]))

    source_svgs = []
    source_blocks = []
    for (prov, source_data), (cx, cy) in zip(source_specs, source_centers):
        svg, canvas_positions, _, _ = render_source_atom(source_data, cx, cy)
        source_svgs.append(svg)
        source_blocks.append({"prov": prov, "canvas_positions": canvas_positions})

    # Arrows from sources to the intermediate destination's empty slots
    arrow_specs = compute_arrows(inter_positions, source_blocks)
    arrow_svgs = []
    for spec in arrow_specs:
        src, dst = spec["src"], spec["dst"]
        src_x = src["canvas_cx"]
        src_y = src["canvas_cy"] + HEX_HEIGHT / 2 + 2
        dst_x = dst["canvas_cx"]
        dst_y = dst["canvas_top_y"] - 4
        arrow_svgs.append(render_arrow(
            src_x, src_y, dst_x, dst_y,
            style=spec["style"], label=spec["label"],
        ))

    # Group labels next to source particles (for fan-out groups whose
    # individual arrows are unlabeled — currently ṇic's i → aya)
    group_label_svgs = []
    for block in source_blocks:
        for p in block["canvas_positions"]:
            if p.get("role") != "surviving":
                continue
            group_label = p.get("group_label")
            if not group_label:
                continue
            lx = p["canvas_cx"] + p["w"] / 2 + EDGE_LENGTH / 2 + 8
            ly = p["canvas_cy"] + HEX_HEIGHT / 2 + 14
            group_label_svgs.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="start" '
                f'font-family="{LATIN_FONT}" font-size="11" font-style="italic" '
                f'fill="{ARROW_LABEL_FILL}">{group_label}</text>'
            )

    # Header
    header_y = 32
    subheader_y = 56
    header_svg = (
        f'  <text x="{canvas_w / 2:.1f}" y="{header_y}" text-anchor="middle" '
        f'font-family="{LATIN_FONT}" font-size="20" font-weight="700" '
        f'fill="#1a1a1a">Assembling <tspan font-style="italic">{example["form_iast"]}</tspan></text>'
        f'\n  <text x="{canvas_w / 2:.1f}" y="{subheader_y}" text-anchor="middle" '
        f'font-family="{LATIN_FONT}" font-size="13" font-style="italic" '
        f'fill="#555">{example["header_subtitle"]}</text>'
    )

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" '
        f'width="{canvas_w}" height="{canvas_h}">'
    )
    parts.append(f'  <title>Assembling {example["form_iast"]}</title>')
    parts.append(
        f'  <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" fill="white"/>'
    )
    parts.append(ARROW_HEAD_MARKER)
    parts.append(header_svg)
    for svg in source_svgs:
        parts.append("  " + svg)
    for label_svg in group_label_svgs:
        parts.append("  " + label_svg)
    for asvg in arrow_svgs:
        parts.append("  " + asvg)
    parts.append("  " + inter_svg)
    parts.append("  " + final_svg)
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    build_dir = REPO_ROOT / "figures" / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    for example in EXAMPLES:
        out_path = build_dir / f"building_kriya_{example['slug']}_assembly.svg"
        out_path.write_text(build_svg(example), encoding="utf-8")
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
