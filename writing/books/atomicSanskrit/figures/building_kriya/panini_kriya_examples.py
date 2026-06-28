#!/usr/bin/env python3
"""
fig_panini_kriya_examples.py — Ch 11 figures: the same five Vedic
kriyāpada assemblies, now with Pāṇini's notation layer named.

The geometry intentionally mirrors fig_vedic_kriya_examples.py:

    row 1  named operation sonomers
    row 2  dhātuḥ atom — the activated intermediate
    row 3  kriyāpada molecule

The visual action stays the same as the Vedic-first figures. The only new
material is the notation layer: gaṇa, vikaraṇa / zero operation, transformation,
and tiṅ-ending labels.
"""

from __future__ import annotations

from vedic_kriya_examples import (  # noqa: E402
    ARROW,
    BUILD_DIR,
    DEV_FONT,
    EDGE_LENGTH,
    EMPTY_STROKE,
    EXAMPLES,
    HEX_HEIGHT,
    LABEL_COL_RIGHT,
    LATIN_FONT,
    LEADER_GAP,
    RIGHT_PAD,
    ROLE_FILL,
    ROLE_DEV,
    ROLE_IAST,
    STROKE,
    WIDTH_IN,
    build_units,
    configure_fonts,
    deva_label,
    ms,
    rail_for_particle,
    render_arrow,
    render_empty_slot,
    render_leader,
    render_particle_cell,
    render_unit,
    resolve_particle,
    units_extent,
)

# Panini-layer font sizes (px) — set by configure_panini() so the notation layer
# lands 9–11 pt at the 4.5in render width. P_COMMON_W pads the set to one width.
P_COMMON_W = 0.0
P_FS_TITLE = 20.0
P_FS_FORMULA = 20.0
P_FS_GROUP = 15.0
P_FS_GROUP_SUB = 11.0
P_FS_DEVA = 22.0
P_FS_IAST = 17.0
P_FS_LABEL = 21.0


def configure_panini(common_w: float) -> None:
    """Size the notation layer + share the width with the vedic engine so the
    whole panini set renders at one uniform scale, 9–11 pt at 4.5in."""
    global P_COMMON_W, P_FS_TITLE, P_FS_FORMULA, P_FS_GROUP, P_FS_GROUP_SUB
    global P_FS_DEVA, P_FS_IAST, P_FS_LABEL
    P_COMMON_W = common_w
    P_FS_TITLE = ms.pt_to_px(11.0, common_w, WIDTH_IN)
    P_FS_FORMULA = ms.pt_to_px(11.0, common_w, WIDTH_IN)
    P_FS_GROUP = ms.pt_to_px(10.0, common_w, WIDTH_IN)
    P_FS_GROUP_SUB = ms.pt_to_px(9.0, common_w, WIDTH_IN)
    P_FS_DEVA = ms.pt_to_px(11.0, common_w, WIDTH_IN)
    P_FS_IAST = ms.pt_to_px(9.0, common_w, WIDTH_IN)
    P_FS_LABEL = ms.pt_to_px(11.0, common_w, WIDTH_IN)
    configure_fonts(common_w)        # share width with the vedic hex renderer

P_TOP_BASE_Y = 236              # pushed down to clear the group headings above
P_MID_BASE_Y = 388
P_BOT_BASE_Y = 552
GROUP_HEADING_Y = 96            # absolute y of the adādi/tip group titles
P_LABEL_X = LABEL_COL_RIGHT     # labels right-justify in the left column
P_BOTTOM_PAD = 34
ARROW_STROKE_WIDTH = 1.45
ARROW_TIP_ADVANCE = 9 * ARROW_STROKE_WIDTH
# Near-horizontal drop arrows get an S-wave (down → up → down) instead of a flat
# line, so the shaft does not run straight into the arrowhead.
NEAR_HORIZ_THRESHOLD = 55
NEAR_HORIZ_SWING = 18


PANINI_LABELS = {
    "eti": {
        "title": "adādi: i → e; tip → ti",
        "formula": "इ → ए + ति → एति",
    },
    "asti": {
        "title": "adādi: zero operation; tip → ti",
        "formula": "अस् + ति → अस्ति",
    },
    "yajati": {
        "title": "bhvādi: śap → a; tip → ti",
        "formula": "यज् + अ + ति → यजति",
    },
    "bhavati": {
        "title": "bhvādi: bhū → bhav; śap → a; tip → ti",
        "formula": "भू → भव् + अ + ति → भवति",
    },
    "rajati": {
        "title": "bhvādi: śap → a; tip → ti",
        "formula": "राज् + अ + ति → राजति",
    },
}

PANINI_SOURCE_GROUPS = {
    "eti": [
        {
            "title_dev": "अदादि", "title_iast": "adādi",
            "subtitle": "i → e operation",
            "anchor_targets": [0],
            "x_shift": -58,
            "particles": [],
        },
        {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "x_shift": 44,
            "particles": [
                {"tok": "t", "role": "surviving", "fill_role": "ending", "targets": [1]},
                {"tok": "i", "role": "surviving", "fill_role": "ending", "targets": [2], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    ],
    "asti": [
        {
            "title_dev": "अदादि", "title_iast": "adādi",
            "subtitle": "zero operation",
            "anchor_targets": [1],
            "x_shift": -58,
            "particles": [],
        },
        {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "x_shift": 44,
            "particles": [
                {"tok": "t", "role": "surviving", "fill_role": "ending", "targets": [2]},
                {"tok": "i", "role": "surviving", "fill_role": "ending", "targets": [3], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    ],
    "yajati": [
        {
            "title_dev": "शप्", "title_iast": "śap",
            "subtitle": "the bhvādi vikaraṇa",
            "x_shift": -62,
            "particles": [
                {"tok": "z", "role": "anubandha"},
                {"tok": "a", "role": "surviving", "fill_role": "activation", "targets": [3], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
        {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "x_shift": 52,
            "particles": [
                {"tok": "t", "role": "surviving", "fill_role": "ending", "targets": [4]},
                {"tok": "i", "role": "surviving", "fill_role": "ending", "targets": [5], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    ],
    "bhavati": [
        {
            "title_dev": "शप्", "title_iast": "śap",
            "subtitle": "the bhvādi vikaraṇa",
            "x_shift": -62,
            "particles": [
                {"tok": "z", "role": "anubandha"},
                {"tok": "a", "role": "surviving", "fill_role": "activation", "targets": [3], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
        {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "x_shift": 52,
            "particles": [
                {"tok": "t", "role": "surviving", "fill_role": "ending", "targets": [4]},
                {"tok": "i", "role": "surviving", "fill_role": "ending", "targets": [5], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    ],
    "rajati": [
        {
            "title_dev": "शप्", "title_iast": "śap",
            "subtitle": "the bhvādi vikaraṇa",
            "x_shift": -62,
            "particles": [
                {"tok": "z", "role": "anubandha"},
                {"tok": "a", "role": "surviving", "fill_role": "activation", "targets": [3], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
        {
            "title_dev": "तिप्", "title_iast": "tip",
            "subtitle": "the 3sg present ending",
            "x_shift": 52,
            "particles": [
                {"tok": "t", "role": "surviving", "fill_role": "ending", "targets": [4]},
                {"tok": "i", "role": "surviving", "fill_role": "ending", "targets": [5], "core": True},
                {"tok": "p", "role": "anubandha"},
            ],
        },
    ],
}


def source_y_for_particle(particle: dict) -> float:
    return rail_for_particle(resolve_particle(particle))


def source_x_for_targets(targets: list[int], centers: dict[int, tuple[float, float]]) -> float:
    xs = [centers[idx][0] for idx in targets]
    return sum(xs) / len(xs)


def render_panini_label(text: str, x: float, y: float, *, anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{LATIN_FONT}" '
        f'font-size="{P_FS_TITLE:.1f}" font-weight="700" text-anchor="{anchor}" '
        f'dominant-baseline="middle" fill="{ms.TEXT}">{text}</text>'
    )


def render_formula_label(text: str, x: float, y: float) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{DEV_FONT}" '
        f'font-size="{P_FS_FORMULA:.1f}" font-weight="500" text-anchor="middle" '
        f'dominant-baseline="middle" fill="{ms.MUTED}">{text}</text>'
    )


def render_source_title(group: dict, x: float, y: float) -> str:
    return "\n".join(
        [
            (
                f'<text x="{x:.1f}" y="{y:.1f}" font-family="{LATIN_FONT}" '
                f'font-size="{P_FS_GROUP:.1f}" font-weight="700" text-anchor="middle" '
                f'dominant-baseline="middle" fill="{ms.TEXT}">'
                f'<tspan font-family="{DEV_FONT}">{group["title_dev"]}</tspan> '
                f'<tspan font-style="italic">'
                f'({group["title_iast"]})</tspan></text>'
            ),
            (
                f'<text x="{x:.1f}" y="{y + 1.6 * P_FS_GROUP_SUB:.1f}" font-family="{LATIN_FONT}" '
                f'font-size="{P_FS_GROUP_SUB:.1f}" font-style="italic" text-anchor="middle" '
                f'dominant-baseline="middle" fill="{ms.MUTED}">{group["subtitle"]}</text>'
            ),
        ]
    )


def render_local_row_label(text: str, y: float) -> str:
    words = text.split()
    if len(words) >= 2:
        top = " ".join(words[:-1])
        bottom = words[-1]
    else:
        top = text
        bottom = ""
    line_gap = P_FS_LABEL * 1.2
    lines = [
        (
            f'<tspan x="{P_LABEL_X:.1f}" y="{y - line_gap / 2:.1f}">'
            f'{top}</tspan>'
        )
    ]
    if bottom:
        lines.append(
            (
                f'<tspan x="{P_LABEL_X:.1f}" y="{y + line_gap / 2:.1f}">'
                f'{bottom}</tspan>'
            )
        )
    return (
        f'<text x="{P_LABEL_X:.1f}" y="{y:.1f}" font-family="{LATIN_FONT}" '
        f'font-size="{P_FS_LABEL:.1f}" font-weight="700" text-anchor="end" '
        f'dominant-baseline="middle" fill="{ms.TEXT}">{"".join(lines)}</text>'
    )


def render_source_particle_cell(particle: dict, x: float, y: float) -> str:
    if particle["role"] != "anubandha":
        display_particle = {**particle, "role": particle.get("fill_role", "activation")}
        return render_particle_cell(display_particle, x, y)

    varna = particle["varna"]
    pts = " ".join(
        f"{px:.1f},{py:.1f}"
        for px, py in [
            (x - particle["w"] / 2, y - HEX_HEIGHT / 2),
            (x + particle["w"] / 2, y - HEX_HEIGHT / 2),
            (x + particle["w"] / 2 + EDGE_LENGTH / 2, y),
            (x + particle["w"] / 2, y + HEX_HEIGHT / 2),
            (x - particle["w"] / 2, y + HEX_HEIGHT / 2),
            (x - particle["w"] / 2 - EDGE_LENGTH / 2, y),
        ]
    )
    return "\n".join(
        [
            (
                f'<polygon points="{pts}" fill="{ms.BG}" stroke="{EMPTY_STROKE}" '
                f'stroke-width="1.35" stroke-dasharray="5 4" stroke-linejoin="round"/>'
            ),
            (
                f'<text x="{x:.1f}" y="{y - 0.18 * P_FS_DEVA:.1f}" font-family="{DEV_FONT}" '
                f'font-size="{P_FS_DEVA:.1f}" font-weight="500" text-anchor="middle" '
                f'dominant-baseline="middle" fill="{ms.MUTED}">{deva_label(varna)}</text>'
            ),
            (
                f'<text x="{x:.1f}" y="{y + 0.62 * P_FS_DEVA:.1f}" font-family="{LATIN_FONT}" '
                f'font-size="{P_FS_IAST:.1f}" font-style="italic" text-anchor="middle" '
                f'dominant-baseline="middle" fill="{ms.MUTED}">{varna["iast"]}</text>'
            ),
        ]
    )


def source_group_layout(
    group: dict,
    target_to_middle_local: dict[int, tuple[float, float]],
) -> dict:
    if not group["particles"]:
        anchor_targets = group.get("anchor_targets", [])
        if anchor_targets:
            anchor_x = sum(target_to_middle_local[idx][0] for idx in anchor_targets) / len(anchor_targets)
        else:
            anchor_x = 0.0
        x = anchor_x + group.get("x_shift", 0.0)
        return {
            "group": group,
            "units": [],
            "centers": {},
            "x_offset": x,
            "xmin": x - 58,
            "xmax": x + 58,
            "label_x": x,
        }

    units, centers = build_units(group["particles"], cluster_consonants=False)
    target_particles = [
        (idx, particle)
        for idx, particle in enumerate(group["particles"])
        if particle.get("role") != "anubandha" and particle.get("targets")
    ]
    target_x = sum(
        target_to_middle_local[target_idx][0]
        for _, particle in target_particles
        for target_idx in particle["targets"]
    ) / sum(len(particle["targets"]) for _, particle in target_particles)
    source_x = sum(centers[idx][0] for idx, _ in target_particles) / len(target_particles)
    x_offset = target_x - source_x + group.get("x_shift", 0.0)
    xmin, xmax, _, _ = units_extent(units)
    return {
        "group": group,
        "units": units,
        "centers": centers,
        "x_offset": x_offset,
        "xmin": xmin + x_offset,
        "xmax": xmax + x_offset,
        "label_x": (xmin + xmax) / 2 + x_offset,
    }


def arrow_target_for_particle(src_x: float, particle: dict, center: tuple[float, float]) -> tuple[float, float]:
    tx, ty = center
    return tx, ty - HEX_HEIGHT / 2 - 3


def render_drop_arrow(x1: float, y1: float, x2: float, y2: float, *, dashed: bool = False) -> str:
    """Short drop-and-turn arrow, used for source-form-to-slot motion.

    The path follows the visual convention sketched in the markup: descend
    almost vertically from the source particle, then make a short turn into
    the destination slot instead of drawing a broad sweeping curve.
    """
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    end_y = y2 - ARROW_TIP_ADVANCE if y2 >= y1 else y2 + ARROW_TIP_ADVANCE
    if abs(x1 - x2) < 10:
        d = f"M {x1:.1f},{y1:.1f} L {x2:.1f},{end_y:.1f}"
    elif abs(end_y - y1) < NEAR_HORIZ_THRESHOLD:
        # Near-horizontal: S-wave — leave the start going straight down, swing
        # back up, then come down into the arrowhead.
        sw = NEAR_HORIZ_SWING
        d = (
            f"M {x1:.1f},{y1:.1f} "
            f"C {x1:.1f},{y1 + sw:.1f} {x2:.1f},{end_y - sw:.1f} {x2:.1f},{end_y:.1f}"
        )
    else:
        span = end_y - y1
        c1_y = y1 + span * 0.45
        c2_y = y1 + span * 0.78
        d = (
            f"M {x1:.1f},{y1:.1f} "
            f"C {x1:.1f},{c1_y:.1f} {x2:.1f},{c2_y:.1f} {x2:.1f},{end_y:.1f}"
        )
    return (
        f'<path d="{d}" fill="none" stroke="{ARROW}" stroke-width="{ARROW_STROKE_WIDTH}"{dash} '
        f'marker-end="url(#arrowhead)"/>'
    )


def unit_width(unit: dict) -> float:
    if unit["kind"] == "cluster":
        n = len(unit["cells"])
        return n * 0.5 * 60 - EDGE_LENGTH / 2
    return unit["particle"]["w"]


def leftmost_unit_center_y(units: list[dict], base_y: float) -> float:
    unit = min(
        units,
        key=lambda item: item["x"] - unit_width(item) / 2 - EDGE_LENGTH / 2,
    )
    return unit["y"] + base_y


def leftmost_source_center_y(source_groups: list[dict], base_y: float) -> float:
    candidates: list[tuple[float, float]] = []
    for group_layout in source_groups:
        for unit in group_layout["units"]:
            if unit["kind"] != "particle":
                continue
            x = unit["x"] + group_layout["x_offset"]
            w = unit_width(unit)
            candidates.append((x - w / 2 - EDGE_LENGTH / 2, unit["y"] + base_y))
    if not candidates:
        return base_y
    return min(candidates, key=lambda item: item[0])[1]


def leftmost_middle_center_y(
    particles: list[dict],
    centers: dict[int, tuple[float, float]],
    base_y: float,
) -> float:
    candidates: list[tuple[float, float]] = []
    for idx, particle in enumerate(particles):
        p = resolve_particle(particle)
        x, _y = centers[idx]
        display_y = rail_for_particle(p) + particle.get("y_shift", 0)
        candidates.append((x - p["w"] / 2 - EDGE_LENGTH / 2, display_y + base_y))
    return min(candidates, key=lambda item: item[0])[1]


def render_example(example: dict) -> str:
    labels = PANINI_LABELS[example["slug"]]
    groups = PANINI_SOURCE_GROUPS[example["slug"]]

    final_units, final_centers = build_units(example["final"])
    middle_units, middle_centers = build_units(example["middle"], cluster_consonants=False)

    target_to_middle_local: dict[int, tuple[float, float]] = {}
    for idx, particle in enumerate(example["middle"]):
        x, y = middle_centers[idx]
        for target_idx in particle["targets"]:
            target_to_middle_local[target_idx] = (x, y)

    final_xmin, xmax, _, _ = units_extent(final_units)
    mid_xmin, mid_xmax, _, _ = units_extent(middle_units)
    source_groups = [source_group_layout(group, target_to_middle_local) for group in groups]
    top_xmin = min(group["xmin"] for group in source_groups)
    top_xmax = max(group["xmax"] for group in source_groups)
    xmin = min(final_xmin, top_xmin, mid_xmin)
    xmax = max(xmax, top_xmax, mid_xmax)

    natural_w = LABEL_COL_RIGHT + LEADER_GAP + (xmax - xmin) + RIGHT_PAD
    canvas_w = P_COMMON_W if P_COMMON_W else natural_w
    dx = (canvas_w - RIGHT_PAD) - xmax            # right-align the illustration
    height = P_BOT_BASE_Y + HEX_HEIGHT / 2 + P_BOTTOM_PAD
    height_in = height / canvas_w * WIDTH_IN
    center_x = (xmin + xmax) / 2 + dx             # centre title/formula on the illustration
    top_label_y = leftmost_source_center_y(source_groups, P_TOP_BASE_Y)
    mid_label_y = leftmost_middle_center_y(example["middle"], middle_centers, P_MID_BASE_Y)
    bot_label_y = leftmost_unit_center_y(final_units, P_BOT_BASE_Y)

    svg: list[str] = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w:.1f} {height:.1f}" '
            f'width="{WIDTH_IN}in" height="{height_in:.3f}in">'
        ),
        f"  <title>Pāṇinian kriyāpada assembly: {example['title']}</title>",
        f'  <rect x="0" y="0" width="{canvas_w:.1f}" height="{height:.1f}" fill="{ms.BG}"/>',
        "  <defs>",
        (
            '    <marker id="arrowhead" markerWidth="10" markerHeight="8" '
            'refX="0" refY="4" orient="auto" markerUnits="strokeWidth">'
        ),
        f'      <polygon points="0,0 9,4 0,8" fill="{ARROW}"/>',
        "    </marker>",
        "  </defs>",
        "  " + render_panini_label(labels["title"], center_x, 24),
        "  " + render_formula_label(labels["formula"], center_x, 54),
        "  " + render_local_row_label("activation sonomers", top_label_y),
        "  " + render_local_row_label("dhātuḥ atom", mid_label_y),
        "  " + render_local_row_label("kriyāpada molecule", bot_label_y),
    ]

    # Leader lines: each row label across to that row's leftmost hex.
    svg.append("  " + render_leader(top_label_y, top_xmin + dx))
    svg.append("  " + render_leader(mid_label_y, mid_xmin + dx))
    svg.append("  " + render_leader(bot_label_y, final_xmin + dx))

    # Top row: Pāṇini's named source forms. Anubandhas are dashed and do
    # not drop into the dhātuḥ atom.
    top_sources: list[tuple[dict, tuple[float, float]]] = []
    for group_layout in source_groups:
        group = group_layout["group"]
        label_x = group_layout["label_x"] + dx
        svg.append("  " + render_source_title(group, label_x, GROUP_HEADING_Y).replace("\n", "\n  "))
        for unit_index, unit in enumerate(group_layout["units"]):
            if unit["kind"] != "particle":
                continue
            particle = unit["particle"]
            x = unit["x"] + group_layout["x_offset"] + dx
            y = unit["y"] + P_TOP_BASE_Y
            svg.append("  " + render_source_particle_cell(particle, x, y).replace("\n", "\n  "))
            if particle.get("role") != "anubandha":
                top_sources.append((particle, (x, y)))

    # Middle row: the activated dhātuḥ atom. The original dhātu material is
    # visible; the named-operation slots are dashed until the source sonomers
    # enter them.
    middle_sources: list[tuple[dict, tuple[float, float]]] = []
    target_to_middle: dict[int, tuple[float, float]] = {}
    target_to_middle_particle: dict[int, dict] = {}
    for idx, particle in enumerate(example["middle"]):
        x, y = middle_centers[idx]
        for target_idx in particle["targets"]:
            target_to_middle[target_idx] = (x + dx, y + P_MID_BASE_Y)
            target_to_middle_particle[target_idx] = particle
        if particle.get("middle_empty", False):
            svg.append(
                "  " + render_empty_slot(particle, x + dx, y + P_MID_BASE_Y).replace("\n", "\n  ")
            )
        else:
            p = resolve_particle(particle)
            display_y = rail_for_particle(p) + particle.get("y_shift", 0)
            svg.append(
                "  "
                + render_particle_cell(p, x + dx, display_y + P_MID_BASE_Y).replace("\n", "\n  ")
            )
            middle_sources.append((particle, (x + dx, display_y + P_MID_BASE_Y)))

    # Drop named operation sonomers into the dhātuḥ atom's empty slots.
    for src, (sx, sy) in top_sources:
        for target_idx in src["targets"]:
            tx, ty = target_to_middle[target_idx]
            ex, ey = arrow_target_for_particle(sx, target_to_middle_particle[target_idx], (tx, ty))
            svg.append(
                "  "
                + render_drop_arrow(
                    sx,
                    sy + HEX_HEIGHT / 2 + 3,
                    ex,
                    ey,
                )
            )

    # Carry the activated intermediate into the final molecule.
    for src, (sx, sy) in middle_sources:
        for target_idx in src["targets"]:
            tx, ty = final_centers[target_idx]
            final_tok = example["final"][target_idx]["tok"]
            dashed = final_tok != src["tok"] or len(src["targets"]) > 1
            if not dashed:
                continue
            svg.append(
                "  "
                + render_drop_arrow(
                    sx,
                    sy + HEX_HEIGHT / 2 + 3,
                    tx + dx,
                    ty + P_BOT_BASE_Y - HEX_HEIGHT / 2 - 3,
                    dashed=dashed,
                )
            )

    for unit in final_units:
        svg.append("  " + render_unit(unit, dx, P_BOT_BASE_Y).replace("\n", "\n  "))

    svg.append("</svg>")
    return "\n".join(svg), natural_w


def main() -> int:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    widths = [render_example(example)[1] for example in EXAMPLES]
    configure_panini(max(widths))
    for example in EXAMPLES:
        path = BUILD_DIR / f"panini_{example['slug']}.from-py.svg"
        path.write_text(render_example(example)[0] + "\n", encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
