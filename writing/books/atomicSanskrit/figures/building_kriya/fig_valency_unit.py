"""Ch 11 §11.4 — Valency unit illustration (two figures).

Figure A — Abstract bonding diagram:
  one head zone + one atom zone + one tail zone, three shades of gray,
  no sonomer labels.  Shows what one valency unit IS at the shape level.

Figure B — Applied to the kṛ dhātuḥ:
  multiple rows of [head][kṛ][tail] configurations, each captioned with
  the resulting Sanskrit word.  Makes "1,062 distinct configurations"
  legible as a picture.

Geometry inherits the hexagon-rail tiling from
``figures/_shared/icons/build_scaffold_icons.py`` (same hexagon dimensions, same
upper-rail/lower-rail convention, same flat-top hexagons).  No matplotlib
dependency — pure stdlib SVG generation.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

# --- Geometry (copied verbatim from figures/_shared/icons/build_scaffold_icons.py) ---

H = 14.0
EDGE = H / math.sqrt(3)
AMP = H / 4

WIDTH_BY_CLASS = {
    "C": EDGE / 2,
    "V1": EDGE,
    "V2": EDGE * 2,
}

VYANJANA_RAIL_Y = -AMP
SVARA_RAIL_Y = AMP

# --- Color palette ---------------------------------------------------------
# Three distinct shades; atom-as-lightest so the reader's eye reads the
# atom as the center the bonds attach to.

ATOM_FILL = "#888888"  # scaffold-gray (matches existing icons)
HEAD_FILL = "#555555"  # medium-dark
TAIL_FILL = "#333333"  # darkest

# Caption / label colors
LABEL_COLOR = "#222222"
SUBLABEL_COLOR = "#777777"

OUT_DIR = Path(__file__).resolve().parents[1] / "build"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# --- Hexagon primitives ---------------------------------------------------


def hex_points(cx: float, cy: float, w: float) -> str:
    e = EDGE
    pts = [
        (cx - w / 2, cy - H / 2),
        (cx + w / 2, cy - H / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2, cy + H / 2),
        (cx - w / 2, cy + H / 2),
        (cx - w / 2 - e / 2, cy),
    ]
    return " ".join(f"{x:.3f},{y:.3f}" for x, y in pts)


def display_units(particles: list[str]) -> list[dict]:
    """Group adjacent consonants into one upper-rail cluster unit."""
    units: list[dict] = []
    i = 0
    while i < len(particles):
        p = particles[i]
        if p == "C":
            run = [p]
            j = i + 1
            while j < len(particles) and particles[j] == "C":
                run.append(particles[j])
                j += 1
            if len(run) > 1:
                units.append(
                    {
                        "kind": "cluster",
                        "parts": run,
                        "width": EDGE * len(run) / 2,
                    }
                )
                i = j
                continue
        units.append({"kind": "particle", "class": p})
        i += 1
    return units


def unit_width(unit: dict) -> float:
    if unit["kind"] == "cluster":
        return unit["width"]
    return WIDTH_BY_CLASS[unit["class"]]


def unit_rail_y(unit: dict) -> float:
    if unit["kind"] == "cluster":
        return VYANJANA_RAIL_Y
    return VYANJANA_RAIL_Y if unit["class"] == "C" else SVARA_RAIL_Y


def layout_zone(
    particles: list[str], start_x: float, start_cy_override: float | None = None
) -> tuple[list[tuple[float, float]], list[dict], float, float]:
    """Lay out one chain of particles starting at start_x.

    Returns positions, units, the leftmost x extent, the rightmost x extent.
    If start_cy_override is given, the first unit goes on the rail that
    smoothly continues from the previous zone's last rail.
    """
    units = display_units(particles)
    positions: list[tuple[float, float]] = []

    for i, unit in enumerate(units):
        cy = unit_rail_y(unit)
        if i == 0:
            cx = start_x + unit_width(unit) / 2 + EDGE / 2
            positions.append((cx, cy))
            continue
        prev = units[i - 1]
        prev_w = unit_width(prev)
        prev_cy = positions[-1][1]
        w = unit_width(unit)
        rail_step = EDGE / 2 if prev_cy != cy else EDGE
        cx = positions[-1][0] + (prev_w + w) / 2 + rail_step
        positions.append((cx, cy))

    if not positions:
        return positions, units, start_x, start_x

    left = positions[0][0] - unit_width(units[0]) / 2 - EDGE / 2
    last_w = unit_width(units[-1])
    right = positions[-1][0] + last_w / 2 + EDGE / 2
    return positions, units, left, right


def chain_layout(
    zones: list[tuple[list[str], str]]
) -> tuple[list[list[tuple[float, float]]], list[list[dict]], float, float]:
    """Lay out a chain of zones, each zone being (particles, fill).

    Adjacent zones tile continuously — the second zone starts where the
    first ended, with rail continuity preserved.
    Returns: per-zone positions list, per-zone units list, xmin, xmax.
    """
    all_positions: list[list[tuple[float, float]]] = []
    all_units: list[list[dict]] = []
    current_x = -EDGE / 2  # so first unit's left edge sits at x=0
    overall_left = math.inf
    overall_right = -math.inf
    prev_last_cy: float | None = None

    for zone_particles, _ in zones:
        if not zone_particles:
            all_positions.append([])
            all_units.append([])
            continue
        units = display_units(zone_particles)
        positions: list[tuple[float, float]] = []
        for i, unit in enumerate(units):
            cy = unit_rail_y(unit)
            w = unit_width(unit)
            if not positions and prev_last_cy is None:
                # First unit of the whole chain.
                cx = current_x + w / 2 + EDGE / 2
            else:
                if positions:
                    prev = units[i - 1]
                    prev_w = unit_width(prev)
                    prev_cy = positions[-1][1]
                    rail_step = EDGE / 2 if prev_cy != cy else EDGE
                    cx = positions[-1][0] + (prev_w + w) / 2 + rail_step
                else:
                    # First unit of this zone, but not first of chain.
                    # Continue tiling from the previous zone's last unit.
                    rail_step = EDGE / 2 if prev_last_cy != cy else EDGE
                    cx = (
                        current_x
                        + prev_last_w / 2  # type: ignore[name-defined]
                        + w / 2
                        + rail_step
                    )
            positions.append((cx, cy))
        all_positions.append(positions)
        all_units.append(units)

        for (px, _), unit in zip(positions, units):
            w = unit_width(unit)
            overall_left = min(overall_left, px - w / 2 - EDGE / 2)
            overall_right = max(overall_right, px + w / 2 + EDGE / 2)

        # Track tail for the next zone.
        last_unit = units[-1]
        prev_last_w = unit_width(last_unit)  # noqa: F841
        prev_last_cy = positions[-1][1]
        current_x = positions[-1][0]

    return all_positions, all_units, overall_left, overall_right


def render_chain_svg(
    zones: list[tuple[list[str], str]],
    *,
    width_px: int = 540,
    margin: float = 4.0,
) -> tuple[str, float, float]:
    """Render one chain of zones into an SVG fragment.

    Returns: (svg_string, xmin, xmax) — the SVG element and the chain's
    horizontal extent so callers can place labels relative to it.
    """
    positions_per_zone, units_per_zone, xmin, xmax = chain_layout(zones)
    parts = []
    for (positions, units), (_, fill) in zip(
        zip(positions_per_zone, units_per_zone), zones
    ):
        for (px, py), unit in zip(positions, units):
            pts = hex_points(px, py, unit_width(unit))
            parts.append(f'<polygon points="{pts}" fill="{fill}"/>')
    return "\n".join(parts), xmin, xmax


# --- Figure A: abstract valency unit --------------------------------------


def figure_a():
    """One row: [head]-[atom]-[tail], no labels on hexagons, captions below."""
    # Head: CV1  (one consonant + one short vowel — e.g., vi-)
    # Atom: CV1C (three particles — the canonical gamādi shape)
    # Tail: CV1  (one consonant + one short vowel — e.g., -ti)
    zones = [
        (["C", "V1"], HEAD_FILL),
        (["C", "V1", "C"], ATOM_FILL),
        (["C", "V1"], TAIL_FILL),
    ]
    chain_svg, xmin, xmax = render_chain_svg(zones)

    # Compute per-zone centers for the zone labels.
    positions_per_zone, units_per_zone, _, _ = chain_layout(zones)
    zone_centers = []
    for positions, units in zip(positions_per_zone, units_per_zone):
        if not positions:
            zone_centers.append(0.0)
            continue
        first = positions[0]
        last = positions[-1]
        zone_centers.append((first[0] + last[0]) / 2.0)

    # Compute the visual center of each zone — average of its hex centers.
    zone_centers = []
    for positions in positions_per_zone:
        if not positions:
            zone_centers.append(0.0)
            continue
        zone_centers.append(sum(p[0] for p in positions) / len(positions))

    label_y = H / 2 + 8.0
    summary_y = label_y + 10.0

    zone_labels = [
        "upasarga (head)",
        "dhātuḥ (atom)",
        "pratyaya (tail)",
    ]

    label_svgs = []
    for cx, label in zip(zone_centers, zone_labels):
        label_svgs.append(
            f'<text x="{cx:.3f}" y="{label_y:.3f}" '
            f'text-anchor="middle" font-family="Charter, serif" '
            f'font-style="italic" font-size="6" fill="{LABEL_COLOR}">{label}</text>'
        )
    brackets_svg = "\n".join(label_svgs)

    summary_text = (
        f'<text x="{(xmin + xmax) / 2:.3f}" y="{summary_y:.3f}" '
        f'text-anchor="middle" font-family="Charter, serif" '
        f'font-size="6" fill="{LABEL_COLOR}">'
        f'one distinct (head, tail) pairing = 1 valency unit'
        f'</text>'
    )

    viewbox_x = xmin - 8.0
    viewbox_y = -H / 2 - 2.0
    viewbox_h = summary_y + 4.0 - viewbox_y
    viewbox_w = xmax - xmin + 16.0

    svg = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{viewbox_x:.3f} {viewbox_y:.3f} '
        f'{viewbox_w:.3f} {viewbox_h:.3f}" '
        f'preserveAspectRatio="xMidYMid meet" '
        f'role="img" aria-label="Valency unit (schematic)">\n'
        f'<title>Valency unit — head + atom + tail</title>\n'
        f'{chain_svg}\n'
        f'{brackets_svg}\n'
        f'{summary_text}\n'
        f'</svg>\n'
    )
    out_path = OUT_DIR / "ch11_valency_unit_schematic.svg"
    out_path.write_text(svg)
    print(f"Wrote {out_path.relative_to(out_path.parents[3])}")


# --- Figure B: kṛ applied --------------------------------------------------


# Each row: (head_particles or None, tail_particles or None, label).
# kṛ itself is the krādi scaffold = CV1 (one consonant + one short vowel).
# Head and tail shapes are schematic — chosen for visual variety, not
# strict morphological derivation.  The chapter's prose carries the
# morphological detail (vṛddhi, sandhi, vikaraṇa insertion).
KR_ROWS = [
    # (head, tail, result-word)
    (None, ["C", "V1"], "kṛti — कृति"),
    (None, ["C", "V2"], "kāra — कार"),
    (None, ["C", "V1", "C", "V1"], "kartṛ — कर्तृ"),
    (["C", "V1"], ["C", "V1"], "prakṛti — प्रकृति"),
    (["C", "V1"], ["C", "V1"], "vikṛti — विकृति"),
    (["C", "V1", "C"], ["C", "V1"], "saṃskṛta — संस्कृत"),
    (["C", "V1", "C"], ["C", "V2", "C", "V1"], "saṃskāra — संस्कार"),
    (["V1", "C"], ["C", "V1"], "utkṛta — उत्कृत"),
]

ATOM_PARTICLES = ["C", "V1"]  # kṛ = krādi (CV1)


def figure_b():
    """Vertical stack: every row is one [head]?-[atom]-[tail] configuration."""

    # Layout strategy: align all rows on a common atom-center x.
    # Compute the atom's "natural" left position when there is no head,
    # and the maximum head-width across rows; align so the atom-block sits
    # at the same x in every row.

    # First, compute the head widths so we can pick the alignment offset.
    head_widths = []
    for head, _, _ in KR_ROWS:
        if head is None:
            head_widths.append(0.0)
        else:
            zones = [(head, HEAD_FILL)]
            positions_per_zone, units_per_zone, l, r = chain_layout(zones)
            head_widths.append(r - l)

    max_head_width = max(head_widths)

    # Now lay out each row with the atom anchored at the same x.
    # We compute each row's chain layout separately, then translate so the
    # atom block's leftmost x lines up at the same column.

    row_svgs = []
    row_height = H + 12.0  # H=14 hex height + 12 units of breathing room
    label_x_offset = 14.0  # gap between right end of chain and the word label

    overall_xmin = math.inf
    overall_xmax = -math.inf
    overall_ymin = -row_height * len(KR_ROWS) / 2
    overall_ymax = row_height * len(KR_ROWS) / 2

    for i, (head, tail, label) in enumerate(KR_ROWS):
        zones: list[tuple[list[str], str]] = []
        if head is not None:
            zones.append((head, HEAD_FILL))
        zones.append((ATOM_PARTICLES, ATOM_FILL))
        if tail is not None:
            zones.append((tail, TAIL_FILL))
        positions_per_zone, units_per_zone, row_xmin, row_xmax = chain_layout(zones)

        # Find the atom zone's leftmost x in this row.
        atom_zone_idx = 1 if head is not None else 0
        atom_positions = positions_per_zone[atom_zone_idx]
        atom_units = units_per_zone[atom_zone_idx]
        atom_left = (
            atom_positions[0][0]
            - unit_width(atom_units[0]) / 2
            - EDGE / 2
        )

        # Translate so the atom-left sits at x = max_head_width + 2.0
        target_atom_left = max_head_width + 2.0
        dx = target_atom_left - atom_left

        row_y = -overall_ymin - (i + 0.5) * row_height + overall_ymin
        # Equivalent: place row i centered at y_i = i * row_height + row_height/2 - total_h/2
        # We'll just stack downward starting at the top:
        row_y = i * row_height + H / 2 - row_height * len(KR_ROWS) / 2 + 2.0

        parts = []
        for (positions, units), (_, fill) in zip(
            zip(positions_per_zone, units_per_zone), zones
        ):
            for (px, py), unit in zip(positions, units):
                pts = hex_points(px + dx, py + row_y, unit_width(unit))
                parts.append(f'<polygon points="{pts}" fill="{fill}"/>')

        # Label to the right of the chain
        label_x = row_xmax + dx + label_x_offset
        parts.append(
            f'<text x="{label_x:.3f}" y="{row_y + 2:.3f}" '
            f'text-anchor="start" font-family="Charter, serif" '
            f'font-size="6.5" fill="{LABEL_COLOR}">{label}</text>'
        )

        # Update bounds
        overall_xmin = min(overall_xmin, row_xmin + dx - 2.0)
        overall_xmax = max(overall_xmax, label_x + 60.0)

        row_svgs.append("\n".join(parts))

    # Final "...and 1,054 more" line
    n_rows = len(KR_ROWS)
    total_h = n_rows * row_height
    overall_ymin = -row_height * n_rows / 2 - 2.0
    overall_ymax = row_height * n_rows / 2 + 2.0

    final_y = overall_ymax + 4.0
    overall_ymax = final_y + 8.0

    summary_x = (overall_xmin + overall_xmax) / 2
    summary = (
        f'<text x="{summary_x:.3f}" y="{final_y:.3f}" '
        f'text-anchor="middle" font-family="Charter, serif" '
        f'font-style="italic" font-size="6.5" fill="{SUBLABEL_COLOR}">'
        f'… 1,054 more such configurations measured in the parsed Sanskrit corpus.'
        f'</text>'
    )

    viewbox_x = overall_xmin
    viewbox_y = overall_ymin
    viewbox_w = overall_xmax - overall_xmin
    viewbox_h = overall_ymax - overall_ymin

    svg = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{viewbox_x:.3f} {viewbox_y:.3f} '
        f'{viewbox_w:.3f} {viewbox_h:.3f}" '
        f'preserveAspectRatio="xMidYMid meet" '
        f'role="img" aria-label="kṛ valency configurations">\n'
        f'<title>kṛ — sample valency configurations</title>\n'
        + "\n".join(row_svgs)
        + "\n"
        + summary
        + "\n"
        + "</svg>\n"
    )
    out_path = OUT_DIR / "ch11_valency_kr_configurations.svg"
    out_path.write_text(svg)
    print(f"Wrote {out_path.relative_to(out_path.parents[3])}")


def main():
    figure_a()
    figure_b()


if __name__ == "__main__":
    main()
