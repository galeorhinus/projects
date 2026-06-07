"""Generate compact icon SVGs for each of the 10 racanā scaffolds.

These icons are filled solid hexagons (no outlines, no text labels), so
the SHAPE of the scaffold reads at small inline sizes — the reader
recognizes the racanā by silhouette. They pair with the outlined
hexagon figures used in §§10.4–10.5 for full pedagogical illustrations.

Use cases:
  * Inline in prose: ![](figures/_shared/icons/scaffold_cv1c_black.svg){height=1em}
  * In chart labels: e.g., x-axis tick of a Ch 11 figure
  * In tables: a column showing the icon next to the structural shorthand
  * In section headings: subtle visual anchor when the section focuses on
    one racanā

Geometry follows the rail tiling of the main hexagon figures
(working/dhatu_hexagons/dhatu_hexagon.py): consonants stay on the upper
rail, vowels stay on the lower rail, and adjacent consonants are grouped
into one split timing envelope. The icons use a small fixed height
(14 SVG units) so they scale cleanly to text em-height.

Outputs (per scaffold, two variants):
  figures/_shared/icons/scaffold_<slug>_black.svg   — for default / dark contexts
  figures/_shared/icons/scaffold_<slug>_gray.svg    — for muted / secondary refs

Slugs are the structural shorthand lowercased (cv1c, ccv1c, cv1cc, etc.).
"""

import math
from pathlib import Path


# (slug, [particle classes], name) for the 10 racanā templates of Ch 10 §10.6
SCAFFOLDS = [
    ("cv1c",    ["C", "V1", "C"],         "gamādi"),
    ("ccv1c",   ["C", "C", "V1", "C"],    "spadādi"),
    ("cv1cc",   ["C", "V1", "C", "C"],    "manthādi"),
    ("cv2c",    ["C", "V2", "C"],         "vācādi"),
    ("cv2",     ["C", "V2"],              "dhādi"),
    ("v1c",     ["V1", "C"],              "iṣādi"),
    ("ccv2c",   ["C", "C", "V2", "C"],    "hrādādi"),
    ("cv1",     ["C", "V1"],              "krādi"),
    ("ccv2",    ["C", "C", "V2"],         "sthādi"),
    ("ccv1cc",  ["C", "C", "V1", "C", "C"], "spardhādi"),
    # Retained from earlier top-10 (now in the long tail but still referenced
    # elsewhere — e.g., §10.4 mātrā-envelope examples and historical figures).
    ("cv2cv1",  ["C", "V2", "C", "V1"],   "bādhrādi"),
    ("cv1cv2",  ["C", "V1", "C", "V2"],   "cityādi"),
]

# Icon geometry — flat-top hexagons; height is fixed, width varies by class.
H = 14.0                          # icon vertical span in SVG units
EDGE = H / math.sqrt(3)           # slanted-edge length

WIDTH_BY_CLASS = {
    "C":  EDGE / 2,               # ½ mātrā — narrow
    "V1": EDGE,                   # 1 mātrā — medium
    "V2": EDGE * 2,               # 2 mātrā — wide
}

# Rail amplitude (matches main hexagon-figure convention, scaled down).
AMP = H / 4

VYANJANA_RAIL_Y = -AMP
SVARA_RAIL_Y = AMP


def hex_points(cx: float, cy: float, w: float) -> str:
    """Return SVG polygon points for a flat-top hexagon centered at (cx, cy)
    with top-edge width w. Slanted-edge length is EDGE; total height is H."""
    e = EDGE
    pts = [
        (cx - w / 2,         cy - H / 2),
        (cx + w / 2,         cy - H / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2,         cy + H / 2),
        (cx - w / 2,         cy + H / 2),
        (cx - w / 2 - e / 2, cy),
    ]
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


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
                units.append({
                    "kind": "cluster",
                    "parts": run,
                    "width": EDGE * len(run) / 2,
                })
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


def layout(particles: list[str]) -> tuple[list[tuple[float, float]], list[dict], tuple[float, float, float, float]]:
    """Compute rail positions for each display unit, plus bounding box."""
    units = display_units(particles)
    positions: list[tuple[float, float]] = []
    for i, unit in enumerate(units):
        cy = unit_rail_y(unit)
        if i == 0:
            positions.append((0.0, cy))
            continue
        prev = units[i - 1]
        prev_w = unit_width(prev)
        prev_cy = positions[-1][1]
        w = unit_width(unit)
        rail_step = EDGE / 2 if prev_cy != cy else EDGE
        cx = positions[-1][0] + (prev_w + w) / 2 + rail_step
        positions.append((cx, cy))

    xmin = ymin = math.inf
    xmax = ymax = -math.inf
    for (px, py), unit in zip(positions, units):
        w = unit_width(unit)
        xmin = min(xmin, px - w / 2 - EDGE / 2)
        xmax = max(xmax, px + w / 2 + EDGE / 2)
        ymin = min(ymin, py - H / 2)
        ymax = max(ymax, py + H / 2)
    return positions, units, (xmin, ymin, xmax, ymax)


def render(particles: list[str], color: str, title: str) -> str:
    positions, units, (xmin, ymin, xmax, ymax) = layout(particles)
    w = xmax - xmin
    h = ymax - ymin

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{xmin:.2f} {ymin:.2f} {w:.2f} {h:.2f}" '
        f'preserveAspectRatio="xMidYMid meet" role="img" aria-label="{title}">',
        f'<title>{title}</title>',
    ]
    for (px, py), unit in zip(positions, units):
        pts = hex_points(px, py, unit_width(unit))
        parts.append(f'<polygon points="{pts}" fill="{color}"/>')
    parts.append('</svg>')
    return "\n".join(parts)


def main():
    out_dir = Path(__file__).resolve().parent
    structural_short = {  # slug → original-case structural shorthand
        "cv1c":   "CV1C",
        "ccv1c":  "CCV1C",
        "cv1cc":  "CV1CC",
        "cv2c":   "CV2C",
        "cv2":    "CV2",
        "v1c":    "V1C",
        "ccv2c":  "CCV2C",
        "cv1":    "CV1",
        "ccv2":   "CCV2",
        "ccv1cc": "CCV1CC",
        "cv2cv1": "CV2CV1",
        "cv1cv2": "CV1CV2",
    }

    for slug, particles, name in SCAFFOLDS:
        title = f"{structural_short[slug]} — {name}"
        for variant, color in [("black", "#1a1a1a"), ("gray", "#888888")]:
            svg = render(particles, color, title)
            path = out_dir / f"scaffold_{slug}_{variant}.svg"
            path.write_text(svg)
            print(f"Wrote {path.relative_to(out_dir.parent.parent)}  ({title})")


if __name__ == "__main__":
    main()
