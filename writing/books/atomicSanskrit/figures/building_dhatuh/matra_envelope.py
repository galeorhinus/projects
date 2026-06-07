#!/usr/bin/env python3
"""
fig_matra_envelope.py — Composite SVG of ten dhātu hexagons across the
mātrā envelope (1.0 → 5.5 in half-mātrā steps).

Reuses working/dhatu_hexagons/dhatu_hexagon.py for the per-dhātu geometry
and composes ten dhātu strips into a single 5-row × 2-column grid.
Adjacent consonant clusters render as one split timing envelope:
two half-mātrā vyañjanas become a one-mātrā cluster, three become a
one-and-a-half-mātrā cluster, and so on.

Each cell shows: mātrā label · dhātu title (Devanagari + IAST) · hexagon strip.

Output: figures/building_dhatuh/matra_envelope.svg
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

# Make working/dhatu_hexagons/ importable.
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))

from dhatu_hexagon import (  # noqa: E402
    EDGE_LENGTH,
    HEX_HEIGHT,
    SIMPLE_FILL_CONSONANT,
    SIMPLE_STROKE,
    SIMPLE_STROKE_WIDTH,
    VYANJANA_RAIL_Y,
    WIDTH_BY_CLASS,
    devanagari_label,
    hex_vertices,
    parse_dhatu_string,
    rail_y_for_varna,
    render_hexagon,
)


# (mātrā label, devanagari title, IAST title, dhātu particle-string)
DHATUS = [
    ("1",   "ऋ",        "ṛ",     "R"),
    ("1½",  "कृ",       "kṛ",    "k,R"),
    ("2",   "गम्",      "gam",   "g,a,m"),
    ("2½",  "धा",       "dhā",   "dh,A"),
    ("3",   "वाच्",     "vāc",   "v,A,c"),
    ("3½",  "स्वाद्",   "svād",  "s,v,A,d"),
    ("4",   "बाधृ",     "bādhṛ", "b,A,dh,R"),
    ("4½",  "कुमार्",   "kumār", "k,u,m,A,r"),
    ("5",   "दीपी",     "dīpī",  "d,I,p,I"),
    ("5½",  "ह्लादी",   "hlādī", "h,l,A,d,I"),
]


# --- Layout parameters ---

CELL_W = 420          # column width (px)
CELL_H = 150          # row height (px)
LEFT_MARGIN = 24      # x-offset for strip's left edge inside the cell
TITLE_Y_OFFSET = 32   # y-offset for combined label + title line
HEX_Y_OFFSET = 100    # y-offset for hexagon-strip midline from cell's top edge
BOTTOM_PADDING = 40   # extra whitespace below the last row

# Asymmetric shifts (1 mātrā = EDGE_LENGTH px):
LEFT_COL_HEX_SHIFT   = EDGE_LENGTH   # shift left-column hexagons right by 1 mātrā
RIGHT_COL_TEXT_SHIFT = EDGE_LENGTH   # shift right-column labels left by 1 mātrā


def strip_width(particles):
    """Compute the total horizontal extent of a hexagon strip in geometry units."""
    positions = compute_unit_layout(particles)
    xs = []
    for (cx, _cy), unit in zip(positions, particles):
        w = unit_width(unit)
        xs.extend([cx - w / 2 - EDGE_LENGTH / 2, cx + w / 2 + EDGE_LENGTH / 2])
    return min(xs), max(xs)


def display_units(particles):
    """Group adjacent consonant runs into one split cluster tile.

    A cluster tile keeps the mātrā accounting explicit: each vyañjana
    contributes a half-mātrā, but the whole run occupies one bonded timing
    envelope.
    """
    units = []
    i = 0
    while i < len(particles):
        current = particles[i]
        if current["class"] == "C":
            run = [current]
            j = i + 1
            while j < len(particles) and particles[j]["class"] == "C":
                run.append(particles[j])
                j += 1
            if len(run) > 1:
                cluster_width = EDGE_LENGTH * len(run) / 2
                units.append({
                    "kind": "cluster",
                    "class": "cluster",
                    "width": cluster_width,
                    "parts": run,
                })
                i = j
                continue
            units.append({
                "kind": "particle",
                "class": current["class"],
                "particle": current,
            })
            i += 1
            continue
        units.append({
            "kind": "particle",
            "class": current["class"],
            "particle": current,
        })
        i += 1
    return units


def unit_width(unit):
    """Return the top/bottom edge width for a particle or cluster unit."""
    if unit["kind"] == "cluster":
        return unit["width"]
    return WIDTH_BY_CLASS[unit["class"]]


def unit_rail_y(unit):
    """Return the articulation rail for a display unit."""
    if unit["kind"] == "cluster":
        return VYANJANA_RAIL_Y
    return rail_y_for_varna(unit["particle"])


def compute_unit_layout(units):
    """Compute articulation-rail positions for particle and cluster units."""
    positions = []

    for i, unit in enumerate(units):
        cy = unit_rail_y(unit)
        if i == 0:
            positions.append((0.0, cy))
            continue
        w = unit_width(unit)
        prev = units[i - 1]
        prev_w = unit_width(prev)
        prev_cy = positions[-1][1]
        rail_step = EDGE_LENGTH / 2 if prev_cy != cy else EDGE_LENGTH
        cx_new = positions[-1][0] + (prev_w + w) / 2 + rail_step
        positions.append((cx_new, cy))

    return positions


def render_cluster_hexagon(cx, cy, unit):
    """Render a consonant cluster inside one split timing envelope."""
    w = unit_width(unit)
    verts = hex_vertices(cx, cy, w)
    points_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts)
    cluster_parts = unit["parts"]
    n_parts = len(cluster_parts)
    cell_w = w / n_parts
    divider_pad = 8

    fragments = [
        f'<polygon points="{points_str}" '
        f'fill="{SIMPLE_FILL_CONSONANT}" stroke="{SIMPLE_STROKE}" '
        f'stroke-width="{SIMPLE_STROKE_WIDTH}" stroke-linejoin="round"/>',
    ]

    for divider_i in range(1, n_parts):
        divider_x = cx - w / 2 + divider_i * cell_w
        fragments.append(
            f'<line x1="{divider_x:.1f}" y1="{cy - HEX_HEIGHT / 2 + divider_pad:.1f}" '
            f'x2="{divider_x:.1f}" y2="{cy + HEX_HEIGHT / 2 - divider_pad:.1f}" '
            f'stroke="#777777" stroke-width="0.9" stroke-linecap="round"/>'
        )

    for part_i, particle in enumerate(cluster_parts):
        label_x = cx - w / 2 + cell_w * (part_i + 0.5)
        fragments.extend([
            f'<text x="{label_x:.1f}" y="{cy - 2:.1f}" '
            f'font-family="Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Arial Unicode MS, sans-serif" '
            f'font-size="18" font-weight="500" text-anchor="middle" dominant-baseline="middle" fill="#1a1a1a">'
            f'{devanagari_label(particle)}</text>',
            f'<text x="{label_x:.1f}" y="{cy + 18:.1f}" '
            f'font-family="Charter, Georgia, Times, serif" '
            f'font-size="9" font-style="italic" text-anchor="middle" dominant-baseline="middle" fill="#333">'
            f'{particle["iast"]}</text>',
        ])

    return "\n  ".join(fragments)


def render_cell(col, row, matra, deva, iast, dhatu_str):
    """Render one grid cell with combined label + title on one line and a
    left-aligned hexagon strip below."""
    particles = parse_dhatu_string(dhatu_str)
    units = display_units(particles)
    positions = compute_unit_layout(units)

    xmin_local, _xmax_local = strip_width(units)

    cell_x = col * CELL_W
    cell_y = row * CELL_H

    # Asymmetric column shifts: left column nudges strips right, right column
    # nudges labels left — each by one mātrā.
    strip_offset = LEFT_MARGIN + (LEFT_COL_HEX_SHIFT if col == 0 else 0)
    text_offset  = LEFT_MARGIN - (RIGHT_COL_TEXT_SHIFT if col == 1 else 0)

    # Left-align the strip: its leftmost geometry point lands at cell_x + strip_offset.
    tx = (cell_x + strip_offset) - xmin_local
    ty = cell_y + HEX_Y_OFFSET

    parts = []

    # Combined mātrā label + dhātu title on one line.
    parts.append(
        f'<text x="{cell_x + text_offset}" y="{cell_y + TITLE_Y_OFFSET}" '
        f'font-family="Charter, Georgia, Times, serif" '
        f'font-size="18" font-weight="500" text-anchor="start" fill="#1a1a1a">'
        f'<tspan font-style="italic">{matra} mātrā</tspan>'
        f'  ·  '
        f'<tspan font-family="Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Charter, Georgia, Times, serif">{deva}</tspan>'
        f' — '
        f'<tspan font-style="italic">{iast}</tspan>'
        f'</text>'
    )

    # Hexagon strip (left-aligned to cell_x + LEFT_MARGIN).
    for (cx, cy), unit in zip(positions, units):
        if unit["kind"] == "cluster":
            fragment = render_cluster_hexagon(cx, cy, unit)
        else:
            fragment = render_hexagon(cx, cy, unit["particle"], style="simple")
        parts.append(
            f'<g transform="translate({tx:.1f},{ty:.1f})">'
            f'{fragment}'
            f'</g>'
        )

    return "\n  ".join(parts)


def main():
    # Column-major layout: first 5 dhātus (mātrās 1–3) in the left column,
    # next 5 (mātrās 3½–5½) in the right column.
    n_cols = 2
    n_rows = (len(DHATUS) + n_cols - 1) // n_cols

    total_w = n_cols * CELL_W
    total_h = n_rows * CELL_H + BOTTOM_PADDING

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {total_w} {total_h}" '
        f'width="{total_w}" height="{total_h}">'
    )
    svg_parts.append(f'  <title>Mātrā envelope across ten dhātavaḥ</title>')
    svg_parts.append(
        f'  <rect x="0" y="0" width="{total_w}" height="{total_h}" fill="white"/>'
    )

    for i, (matra, deva, iast, dhatu_str) in enumerate(DHATUS):
        col = i // n_rows
        row = i % n_rows
        svg_parts.append("  " + render_cell(col, row, matra, deva, iast, dhatu_str))

    svg_parts.append("</svg>")

    out_path = REPO_ROOT / "figures" / "build" / "matra_envelope.from-py.svg"
    out_path.write_text("\n".join(svg_parts), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
