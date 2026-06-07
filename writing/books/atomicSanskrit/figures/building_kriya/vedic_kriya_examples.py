#!/usr/bin/env python3
"""
fig_vedic_kriya_examples.py — Ch 11 figures: Vedic kriyā assembly before
Pāṇinian notation.

The figures use the same grammar as the later kriyā assembly figures:

    row 1  activation sonomers
    row 2  dhātuḥ atom + dashed destination slots
    row 3  kriyāpada molecule

No Pāṇinian rule names are rendered in the figure. The visual claim is that
the Vedic corpus already shows the sonomer-level procedure running.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))

from dhatu_hexagon import EDGE_LENGTH, HEX_HEIGHT, VARNAS, is_ayogavaha  # noqa: E402


BUILD_DIR = Path(__file__).resolve().parent
HALANT = "्"
DEV_FONT = (
    "Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, "
    "Arial Unicode MS, sans-serif"
)
LATIN_FONT = "Charter, Georgia, Times, serif"
WIDTH_C = 10
WIDTH_V1 = 40
WIDTH_V2 = 100
MATRA_UNIT = 60

LOWER_RAIL_Y = HEX_HEIGHT / 4       # original dhātu vowels
MIDDLE_RAIL_Y = -HEX_HEIGHT / 4     # consonants
UPPER_RAIL_Y = -3 * HEX_HEIGHT / 4  # added / transformed vowels

TOP_BASE_Y = 96
MID_BASE_Y = 220
BOT_BASE_Y = 352
LABEL_X = 184
LEFT_PAD = 222
RIGHT_PAD = 36
TOP_PAD = 22
BOTTOM_PAD = 34

ROLE_FILL = {
    "original": "#dcdcdc",
    "transform": "#888888",
    "activation": "#1a1a1a",
    "ending": "#555555",
}
ROLE_DEV = {
    "original": "#1a1a1a",
    "transform": "#1a1a1a",
    "activation": "#f5f5f5",
    "ending": "#f5f5f5",
}
ROLE_IAST = {
    "original": "#333333",
    "transform": "#222222",
    "activation": "#d8d8d8",
    "ending": "#d8d8d8",
}
STROKE = "#1a1a1a"
EMPTY_STROKE = "#666666"
ARROW = "#555555"

ALIASES = {
    "A": "ā",
    "I": "ī",
    "U": "ū",
    "R": "ṛ",
    "RR": "ṝ",
    "T": "ṭ",
    "Th": "ṭh",
    "D": "ḍ",
    "Dh": "ḍh",
    "N": "ṇ",
    "G": "ṅ",
    "J": "ñ",
    "S": "ṣ",
    "z": "ś",
    "M": "ṃ",
    "H": "ḥ",
}


EXAMPLES = [
    {
        "slug": "eti",
        "title": "eti",
        "bottom_y_shift": HEX_HEIGHT,
        "final": [
            {"tok": "e", "role": "transform"},
            {"tok": "t", "role": "ending"},
            {"tok": "i", "role": "ending"},
        ],
        "dhatu": [
            {"tok": "i", "role": "original", "targets": [0], "core": True},
        ],
        "middle": [
            {"tok": "i", "role": "original", "targets": [0], "core": True},
            {"tok": "t", "role": "ending", "targets": [1], "middle_empty": True},
            {"tok": "i", "role": "ending", "targets": [2], "middle_empty": True},
        ],
        "activation": [
            {"tok": "t", "role": "ending", "targets": [1]},
            {"tok": "i", "role": "ending", "targets": [2]},
        ],
    },
    {
        "slug": "asti",
        "title": "asti",
        "final": [
            {"tok": "a", "role": "original", "core": True},
            {"tok": "s", "role": "original"},
            {"tok": "t", "role": "ending"},
            {"tok": "i", "role": "ending"},
        ],
        "dhatu": [
            {"tok": "a", "role": "original", "targets": [0], "core": True},
            {"tok": "s", "role": "original", "targets": [1]},
        ],
        "middle": [
            {"tok": "a", "role": "original", "targets": [0], "core": True},
            {"tok": "s", "role": "original", "targets": [1]},
            {"tok": "t", "role": "ending", "targets": [2], "middle_empty": True},
            {"tok": "i", "role": "ending", "targets": [3], "middle_empty": True},
        ],
        "activation": [
            {"tok": "t", "role": "ending", "targets": [2]},
            {"tok": "i", "role": "ending", "targets": [3]},
        ],
    },
    {
        "slug": "yajati",
        "title": "yajati",
        "final": [
            {"tok": "y", "role": "original"},
            {"tok": "a", "role": "original", "core": True},
            {"tok": "j", "role": "original"},
            {"tok": "a", "role": "activation"},
            {"tok": "t", "role": "ending"},
            {"tok": "i", "role": "ending"},
        ],
        "dhatu": [
            {"tok": "y", "role": "original", "targets": [0]},
            {"tok": "a", "role": "original", "targets": [1], "core": True},
            {"tok": "j", "role": "original", "targets": [2]},
        ],
        "middle": [
            {"tok": "y", "role": "original", "targets": [0]},
            {"tok": "a", "role": "original", "targets": [1], "core": True},
            {"tok": "j", "role": "original", "targets": [2]},
            {"tok": "a", "role": "activation", "targets": [3], "middle_empty": True},
            {"tok": "t", "role": "ending", "targets": [4], "middle_empty": True},
            {"tok": "i", "role": "ending", "targets": [5], "middle_empty": True},
        ],
        "activation": [
            {"tok": "a", "role": "activation", "targets": [3]},
            {"tok": "t", "role": "ending", "targets": [4]},
            {"tok": "i", "role": "ending", "targets": [5]},
        ],
    },
    {
        "slug": "bhavati",
        "title": "bhavati",
        "final": [
            {"tok": "bh", "role": "original"},
            {"tok": "a", "role": "transform"},
            {"tok": "v", "role": "transform"},
            {"tok": "a", "role": "activation"},
            {"tok": "t", "role": "ending"},
            {"tok": "i", "role": "ending"},
        ],
        "dhatu": [
            {"tok": "bh", "role": "original", "targets": [0]},
            {"tok": "U", "role": "original", "targets": [1, 2], "core": True},
        ],
        "middle": [
            {"tok": "bh", "role": "original", "targets": [0], "y_shift": -HEX_HEIGHT},
            {"tok": "U", "role": "original", "targets": [1, 2], "core": True, "y_shift": -HEX_HEIGHT},
            {"tok": "a", "role": "activation", "targets": [3], "middle_empty": True},
            {"tok": "t", "role": "ending", "targets": [4], "middle_empty": True},
            {"tok": "i", "role": "ending", "targets": [5], "middle_empty": True},
        ],
        "activation": [
            {"tok": "a", "role": "activation", "targets": [3]},
            {"tok": "t", "role": "ending", "targets": [4]},
            {"tok": "i", "role": "ending", "targets": [5]},
        ],
    },
    {
        "slug": "rajati",
        "title": "rājati",
        "final": [
            {"tok": "r", "role": "original"},
            {"tok": "A", "role": "original", "core": True},
            {"tok": "j", "role": "original"},
            {"tok": "a", "role": "activation"},
            {"tok": "t", "role": "ending"},
            {"tok": "i", "role": "ending"},
        ],
        "dhatu": [
            {"tok": "r", "role": "original", "targets": [0]},
            {"tok": "A", "role": "original", "targets": [1], "core": True},
            {"tok": "j", "role": "original", "targets": [2]},
        ],
        "middle": [
            {"tok": "r", "role": "original", "targets": [0]},
            {"tok": "A", "role": "original", "targets": [1], "core": True},
            {"tok": "j", "role": "original", "targets": [2]},
            {"tok": "a", "role": "activation", "targets": [3], "middle_empty": True},
            {"tok": "t", "role": "ending", "targets": [4], "middle_empty": True},
            {"tok": "i", "role": "ending", "targets": [5], "middle_empty": True},
        ],
        "activation": [
            {"tok": "a", "role": "activation", "targets": [3]},
            {"tok": "t", "role": "ending", "targets": [4]},
            {"tok": "i", "role": "ending", "targets": [5]},
        ],
    },
]


def varna_for(token: str) -> dict:
    key = ALIASES.get(token, token)
    if key not in VARNAS:
        raise ValueError(f"Unknown varṇa token: {token!r}")
    return dict(VARNAS[key])


def deva_label(varna: dict, final_cluster: bool = False) -> str:
    if varna["class"] == "C" and not is_ayogavaha(varna) and not final_cluster:
        return varna["deva"] + HALANT
    return varna["deva"]


def width_for_varna(varna: dict) -> float:
    if varna["class"] == "C":
        return WIDTH_C
    if varna["class"] == "V1":
        return WIDTH_V1
    if varna["class"] == "V2":
        return WIDTH_V2
    return WIDTH_V1


def rail_for_particle(particle: dict) -> float:
    varna = particle["varna"]
    if is_ayogavaha(varna):
        return LOWER_RAIL_Y
    if varna["class"] == "C":
        return MIDDLE_RAIL_Y
    if particle.get("core", False):
        return LOWER_RAIL_Y
    return UPPER_RAIL_Y


def hex_vertices(cx: float, cy: float, w: float) -> list[tuple[float, float]]:
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    return [
        (cx - w / 2, cy - h / 2),
        (cx + w / 2, cy - h / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2, cy + h / 2),
        (cx - w / 2, cy + h / 2),
        (cx - w / 2 - e / 2, cy),
    ]


def resolve_particle(particle: dict) -> dict:
    varna = varna_for(particle["tok"])
    return {
        **particle,
        "varna": varna,
        "w": particle.get("w_override", width_for_varna(varna)),
    }


def build_units(
    particles: list[dict],
    *,
    cluster_consonants: bool = True,
) -> tuple[list[dict], dict[int, tuple[float, float]]]:
    units: list[dict] = []
    particle_to_unit: list[tuple[int, int | None]] = []
    i = 0
    while i < len(particles):
        p = resolve_particle(particles[i])
        v = p["varna"]
        if cluster_consonants and v["class"] == "C" and not is_ayogavaha(v):
            cells = [p]
            j = i + 1
            while j < len(particles):
                pj = resolve_particle(particles[j])
                vj = pj["varna"]
                if vj["class"] == "C" and not is_ayogavaha(vj):
                    cells.append(pj)
                    j += 1
                else:
                    break
            if len(cells) > 1:
                unit_index = len(units)
                units.append({"kind": "cluster", "cells": cells})
                for cell_idx in range(len(cells)):
                    particle_to_unit.append((unit_index, cell_idx))
                i = j
                continue
        unit_index = len(units)
        units.append({"kind": "particle", "particle": p})
        particle_to_unit.append((unit_index, None))
        i += 1

    positions = layout_units(units)
    particle_centers: dict[int, tuple[float, float]] = {}
    for particle_idx, (unit_idx, cell_idx) in enumerate(particle_to_unit):
        unit = units[unit_idx]
        cx, cy = positions[unit_idx]
        if unit["kind"] == "cluster":
            n = len(unit["cells"])
            w = unit_width(unit)
            cell_w = w / n
            cell_x = cx - w / 2 + cell_w * (cell_idx + 0.5)
            particle_centers[particle_idx] = (cell_x, cy)
        else:
            particle_centers[particle_idx] = (cx, cy)
    for unit, (x, y) in zip(units, positions):
        unit["x"] = x
        unit["y"] = y
    return units, particle_centers


def unit_width(unit: dict) -> float:
    if unit["kind"] == "cluster":
        n = len(unit["cells"])
        return n * 0.5 * MATRA_UNIT - EDGE_LENGTH / 2
    return unit["particle"]["w"]


def unit_rail_y(unit: dict) -> float:
    if unit["kind"] == "cluster":
        return MIDDLE_RAIL_Y
    return rail_for_particle(unit["particle"])


def layout_units(units: list[dict]) -> list[tuple[float, float]]:
    positions: list[tuple[float, float]] = []
    for i, unit in enumerate(units):
        cy = unit_rail_y(unit)
        if i == 0:
            positions.append((0.0, cy))
            continue
        prev = units[i - 1]
        prev_cy = positions[-1][1]
        prev_w = unit_width(prev)
        w = unit_width(unit)
        rail_step = EDGE_LENGTH / 2 if prev_cy != cy else EDGE_LENGTH
        x = positions[-1][0] + (prev_w + w) / 2 + rail_step
        positions.append((x, cy))
    return positions


def units_extent(units: list[dict]) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for unit in units:
        w = unit_width(unit)
        x = unit["x"]
        y = unit["y"]
        xs.extend([x - w / 2 - EDGE_LENGTH / 2, x + w / 2 + EDGE_LENGTH / 2])
        ys.extend([y - HEX_HEIGHT / 2, y + HEX_HEIGHT / 2])
    return min(xs), max(xs), min(ys), max(ys)


def role_for_slot(particle: dict) -> str:
    if particle["role"] in {"activation", "ending"}:
        return "empty"
    return particle["role"]


def render_particle_cell(
    particle: dict,
    x: float,
    y: float,
    *,
    empty: bool = False,
) -> str:
    varna = particle["varna"]
    w = particle["w"]
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in hex_vertices(x, y, w))
    if empty:
        return (
            f'<polygon points="{pts}" fill="none" stroke="{EMPTY_STROKE}" '
            f'stroke-width="1.35" stroke-dasharray="5 4" stroke-linejoin="round"/>'
        )

    role = particle["role"]
    return "\n".join(
        [
            (
                f'<polygon points="{pts}" fill="{ROLE_FILL[role]}" stroke="{STROKE}" '
                f'stroke-width="1.45" stroke-linejoin="round"/>'
            ),
            (
                f'<text x="{x:.1f}" y="{y + 0.5:.1f}" font-family="{DEV_FONT}" '
                f'font-size="22" font-weight="500" text-anchor="middle" '
                f'dominant-baseline="middle" fill="{ROLE_DEV[role]}">{deva_label(varna)}</text>'
            ),
            (
                f'<text x="{x:.1f}" y="{y + 19:.1f}" font-family="{LATIN_FONT}" '
                f'font-size="11" font-style="italic" text-anchor="middle" '
                f'dominant-baseline="middle" fill="{ROLE_IAST[role]}">{varna["iast"]}</text>'
            ),
        ]
    )


_cluster_ids = itertools.count()


def cluster_cell_polygon(cx: float, cy: float, w: float, n_cells: int, cell_idx: int):
    h = HEX_HEIGHT
    e = EDGE_LENGTH
    cell_w = w / n_cells
    left_x = cx - w / 2 + cell_idx * cell_w
    right_x = cx - w / 2 + (cell_idx + 1) * cell_w

    pts = [(left_x, cy - h / 2)]
    if cell_idx == n_cells - 1:
        pts.extend([(right_x, cy - h / 2), (right_x + e / 2, cy), (right_x, cy + h / 2)])
    else:
        pts.extend([(right_x, cy - h / 2), (right_x, cy + h / 2)])
    pts.append((left_x, cy + h / 2))
    if cell_idx == 0:
        pts.append((left_x - e / 2, cy))
    return pts


def render_cluster(unit: dict, dx: float, dy: float) -> str:
    cells = unit["cells"]
    n = len(cells)
    w = unit_width(unit)
    cx = unit["x"] + dx
    cy = unit["y"] + dy
    cell_w = w / n
    cluster_id = next(_cluster_ids)
    out: list[str] = []

    for i, cell in enumerate(cells):
        pts = " ".join(
            f"{x:.1f},{y:.1f}" for x, y in cluster_cell_polygon(cx, cy, w, n, i)
        )
        out.append(f'<polygon points="{pts}" fill="{ROLE_FILL[cell["role"]]}" stroke="none"/>')

    outer_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in hex_vertices(cx, cy, w))
    out.append(
        f'<polygon points="{outer_pts}" fill="none" stroke="{STROKE}" '
        f'stroke-width="1.45" stroke-linejoin="round"/>'
    )

    defs: list[str] = []
    for i in range(n):
        clip_id = f"vedic-kriya-cluster-{cluster_id}-cell{i}"
        left_x = cx - w / 2 + i * cell_w
        right_x = cx - w / 2 + (i + 1) * cell_w
        if i == 0:
            left_x -= EDGE_LENGTH / 2
        if i == n - 1:
            right_x += EDGE_LENGTH / 2
        defs.append(
            f'<clipPath id="{clip_id}"><rect x="{left_x:.1f}" y="{cy - HEX_HEIGHT:.1f}" '
            f'width="{right_x - left_x:.1f}" height="{2 * HEX_HEIGHT:.1f}"/></clipPath>'
        )
    out.append(f'<defs>{"".join(defs)}</defs>')

    conjunct = HALANT.join(c["varna"]["deva"] for c in cells)
    for i, cell in enumerate(cells):
        clip_id = f"vedic-kriya-cluster-{cluster_id}-cell{i}"
        out.append(
            f'<text x="{cx:.1f}" y="{cy - 2:.1f}" font-family="{DEV_FONT}" '
            f'font-size="20" font-weight="500" text-anchor="middle" '
            f'dominant-baseline="middle" fill="{ROLE_DEV[cell["role"]]}" '
            f'clip-path="url(#{clip_id})">{conjunct}</text>'
        )

    for i, cell in enumerate(cells):
        label_x = cx - w / 2 + cell_w * (i + 0.5)
        out.append(
            f'<text x="{label_x:.1f}" y="{cy + 17:.1f}" font-family="{LATIN_FONT}" '
            f'font-size="9" font-style="italic" text-anchor="middle" '
            f'dominant-baseline="middle" fill="{ROLE_IAST[cell["role"]]}">{cell["varna"]["iast"]}</text>'
        )

    return "\n".join(out)


def render_unit(unit: dict, dx: float, dy: float) -> str:
    if unit["kind"] == "cluster":
        return render_cluster(unit, dx, dy)
    p = unit["particle"]
    return render_particle_cell(p, unit["x"] + dx, unit["y"] + dy)


def render_empty_slot(particle: dict, x: float, y: float) -> str:
    p = resolve_particle(particle)
    return render_particle_cell(p, x, y, empty=True)


def source_x_for_targets(targets: list[int], centers: dict[int, tuple[float, float]]) -> float:
    xs = [centers[idx][0] for idx in targets]
    return sum(xs) / len(xs)


def source_y_for_particle(particle: dict) -> float:
    p = resolve_particle(particle)
    return rail_for_particle(p)


def render_source_particle(particle: dict, centers: dict[int, tuple[float, float]], dx: float, dy: float) -> tuple[str, tuple[float, float]]:
    p = resolve_particle(particle)
    x = source_x_for_targets(particle["targets"], centers) + dx
    y = source_y_for_particle(particle) + dy
    return render_particle_cell(p, x, y), (x, y)


def render_arrow(x1: float, y1: float, x2: float, y2: float, *, dashed: bool = False) -> str:
    if abs(x1 - x2) < 0.1:
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        return (
            f'<path d="M {x1:.1f},{y1:.1f} L {x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{ARROW}" stroke-width="1.35"{dash} marker-end="url(#arrowhead)"/>'
        )
    mid_y = (y1 + y2) / 2
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return (
        f'<path d="M {x1:.1f},{y1:.1f} C {x1:.1f},{mid_y:.1f} '
        f'{x2:.1f},{mid_y:.1f} {x2:.1f},{y2:.1f}" fill="none" '
        f'stroke="{ARROW}" stroke-width="1.35"{dash} marker-end="url(#arrowhead)"/>'
    )


def arrow_target_for_particle(src_x: float, particle: dict, center: tuple[float, float]) -> tuple[float, float]:
    tx, ty = center
    target = resolve_particle(particle)
    if abs(src_x - tx) < 18:
        return tx, ty - HEX_HEIGHT / 2 - 3
    side = -1 if src_x < tx else 1
    return tx + side * (target["w"] / 2 + EDGE_LENGTH / 2 + 2), ty


def render_row_label(text: str, y: float) -> str:
    words = text.split()
    if len(words) >= 2:
        top = " ".join(words[:-1])
        bottom = words[-1]
    else:
        top = text
        bottom = ""
    line_gap = 25
    lines = [
        (
            f'<tspan x="{LABEL_X:.1f}" y="{y - line_gap / 2:.1f}">'
            f'{top}</tspan>'
        )
    ]
    if bottom:
        lines.append(
            (
                f'<tspan x="{LABEL_X:.1f}" y="{y + line_gap / 2:.1f}">'
                f'{bottom}</tspan>'
            )
        )
    return (
        f'<text x="{LABEL_X:.1f}" y="{y:.1f}" font-family="{LATIN_FONT}" '
        f'font-size="21" font-weight="700" text-anchor="end" '
        f'dominant-baseline="middle" fill="#333333">{"".join(lines)}</text>'
    )


def leftmost_unit_center_y(units: list[dict], base_y: float) -> float:
    unit = min(
        units,
        key=lambda item: item["x"] - unit_width(item) / 2 - EDGE_LENGTH / 2,
    )
    return unit["y"] + base_y


def leftmost_cell_center_y(cells: list[dict], base_y: float) -> float:
    cell = min(
        cells,
        key=lambda item: item["x"] - item["w"] / 2 - EDGE_LENGTH / 2,
    )
    return cell["y"] + base_y


def render_example(example: dict) -> str:
    final_units, final_centers = build_units(example["final"])
    middle_units, middle_centers = build_units(example["middle"], cluster_consonants=False)
    target_to_middle_local: dict[int, tuple[float, float]] = {}
    for idx, particle in enumerate(example["middle"]):
        x, y = middle_centers[idx]
        for target_idx in particle["targets"]:
            target_to_middle_local[target_idx] = (x, y)
    xmin, xmax, _, _ = units_extent(final_units)
    mid_xmin, mid_xmax, _, _ = units_extent(middle_units)
    top_cells = []
    for src in example["activation"]:
        p = resolve_particle(src)
        target_positions = [target_to_middle_local[idx] for idx in src["targets"]]
        p["x"] = sum(pos[0] for pos in target_positions) / len(target_positions)
        p["y"] = rail_for_particle(p)
        top_cells.append(p)
    top_xmin = min(cell["x"] - cell["w"] / 2 - EDGE_LENGTH / 2 for cell in top_cells)
    top_xmax = max(cell["x"] + cell["w"] / 2 + EDGE_LENGTH / 2 for cell in top_cells)
    xmin = min(xmin, top_xmin, mid_xmin)
    xmax = max(xmax, top_xmax, mid_xmax)
    dx = LEFT_PAD - xmin
    width = xmax - xmin + LEFT_PAD + RIGHT_PAD
    bot_base_y = BOT_BASE_Y + example.get("bottom_y_shift", 0)
    height = bot_base_y + HEX_HEIGHT / 2 + BOTTOM_PAD

    top_label_y = leftmost_cell_center_y(top_cells, TOP_BASE_Y)
    mid_label_y = leftmost_unit_center_y(middle_units, MID_BASE_Y)
    if example["slug"] == "bhavati":
        mid_label_y += example["middle"][0].get("y_shift", 0)
    bot_label_y = leftmost_unit_center_y(final_units, bot_base_y)

    svg: list[str] = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" '
            f'width="{width:.1f}" height="{height:.1f}">'
        ),
        f"  <title>Vedic kriyāpada assembly: {example['title']}</title>",
        f'  <rect x="0" y="0" width="{width:.1f}" height="{height:.1f}" fill="white"/>',
        "  <defs>",
        (
            '    <marker id="arrowhead" markerWidth="10" markerHeight="8" '
            'refX="9" refY="4" orient="auto" markerUnits="strokeWidth">'
        ),
        f'      <polygon points="0,0 9,4 0,8" fill="{ARROW}"/>',
        "    </marker>",
        "  </defs>",
        "  " + render_row_label("activation sonomers", top_label_y),
        "  " + render_row_label("dhātuḥ atom", mid_label_y),
        "  " + render_row_label("kriyāpada molecule", bot_label_y),
    ]

    # Top row: activation sonomers only.
    top_sources: list[tuple[dict, tuple[float, float]]] = []
    for src, cell in zip(example["activation"], top_cells):
        pos = (cell["x"] + dx, cell["y"] + TOP_BASE_Y)
        top_sources.append((src, pos))
        svg.append(
            "  "
            + render_particle_cell(cell, cell["x"] + dx, cell["y"] + TOP_BASE_Y).replace("\n", "\n  ")
        )

    # Middle row: a coherent placeholder strip. Original dhātu particles remain
    # filled; activation/ending destinations are dashed.
    middle_sources: list[tuple[dict, tuple[float, float]]] = []
    target_to_middle: dict[int, tuple[float, float]] = {}
    target_to_middle_particle: dict[int, dict] = {}
    for idx, particle in enumerate(example["middle"]):
        x, y = middle_centers[idx]
        for target_idx in particle["targets"]:
            target_to_middle[target_idx] = (x + dx, y + MID_BASE_Y)
            target_to_middle_particle[target_idx] = particle
        if particle.get("middle_empty", False):
            svg.append(
                "  " + render_empty_slot(particle, x + dx, y + MID_BASE_Y).replace("\n", "\n  ")
            )
        else:
            p = resolve_particle(particle)
            display_y = rail_for_particle(p) + particle.get("y_shift", 0)
            svg.append("  " + render_particle_cell(p, x + dx, display_y + MID_BASE_Y).replace("\n", "\n  "))
            sx = x + dx
            sy = display_y + MID_BASE_Y
            middle_sources.append((particle, (sx, sy)))

    # Drop activation sonomers into middle-row target slots.
    for src, (sx, sy) in top_sources:
        for target_idx in src["targets"]:
            tx, ty = target_to_middle[target_idx]
            ex, ey = arrow_target_for_particle(sx, target_to_middle_particle[target_idx], (tx, ty))
            svg.append(
                "  "
                + render_arrow(
                    sx,
                    sy + HEX_HEIGHT / 2 + 3,
                    ex,
                    ey,
                )
            )

    # Carry dhātu material down into the finished molecule. Transformation
    # arrows are dashed where one source particle maps to more than one target
    # or changes visible form.
    for src, (sx, sy) in middle_sources:
        for target_idx in src["targets"]:
            tx, ty = final_centers[target_idx]
            final_tok = example["final"][target_idx]["tok"]
            dashed = final_tok != src["tok"] or len(src["targets"]) > 1
            if not dashed:
                continue
            svg.append(
                "  "
                + render_arrow(
                    sx,
                    sy + HEX_HEIGHT / 2 + 3,
                    tx + dx,
                    ty + bot_base_y - HEX_HEIGHT / 2 - 3,
                    dashed=dashed,
                )
            )

    # Finished kriyāpada molecule, with adjacent consonants compressed into
    # split-color cluster cells.
    for unit in final_units:
        svg.append("  " + render_unit(unit, dx, bot_base_y).replace("\n", "\n  "))

    svg.append("</svg>")
    return "\n".join(svg)


def main() -> int:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    for example in EXAMPLES:
        path = BUILD_DIR / f"vedic_{example['slug']}.from-py.svg"
        path.write_text(render_example(example) + "\n", encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
