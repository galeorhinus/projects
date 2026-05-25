"""Generate compact icon SVGs for each of the 10 racanā scaffolds.

These icons are filled solid hexagons (no outlines, no text labels), so
the SHAPE of the scaffold reads at small inline sizes — the reader
recognizes the racanā by silhouette. They pair with the outlined
hexagon figures used in §§10.4–10.5 for full pedagogical illustrations.

Use cases:
  * Inline in prose: ![](figures/icons/scaffold_cv1c_black.svg){height=1em}
  * In chart labels: e.g., x-axis tick of a Ch 11 figure
  * In tables: a column showing the icon next to the structural shorthand
  * In section headings: subtle visual anchor when the section focuses on
    one racanā

Geometry follows the zigzag tiling of the main hexagon figures
(working/dhatu_hexagons/dhatu_hexagon.py), but uses a small fixed height
(14 SVG units) so the icons scale cleanly to text em-height.

Outputs (per scaffold, two variants):
  figures/icons/scaffold_<slug>_black.svg   — for default / dark contexts
  figures/icons/scaffold_<slug>_gray.svg    — for muted / secondary refs

Slugs are the structural shorthand lowercased (cv1c, ccv1c, cv1cc, etc.).
"""

import math
from pathlib import Path


# (slug, [particle classes], name) for the 10 racanā templates of Ch 10 §10.6
SCAFFOLDS = [
    ("cv1c",    ["C", "V1", "C"],         "gamādi"),
    ("ccv1c",   ["C", "C", "V1", "C"],    "smarādi"),
    ("cv1cc",   ["C", "V1", "C", "C"],    "kalpādi"),
    ("cv2cv1",  ["C", "V2", "C", "V1"],   "bādhrādi"),
    ("cv2c",    ["C", "V2", "C"],         "vācādi"),
    ("cv2",     ["C", "V2"],              "dhādi"),
    ("v1c",     ["V1", "C"],              "iṣādi"),
    ("cv1",     ["C", "V1"],              "krādi"),
    ("cv1cv2",  ["C", "V1", "C", "V2"],   "cityādi"),
    ("ccv2",    ["C", "C", "V2"],         "sthādi"),
]

# Icon geometry — flat-top hexagons; height is fixed, width varies by class.
H = 14.0                          # icon vertical span in SVG units
EDGE = H / math.sqrt(3)           # slanted-edge length

WIDTH_BY_CLASS = {
    "C":  EDGE / 2,               # ½ mātrā — narrow
    "V1": EDGE,                   # 1 mātrā — medium
    "V2": EDGE * 2,               # 2 mātrā — wide
}

# Zigzag amplitude (matches main hexagon-figure convention)
AMP = H / 4


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


def layout(particles: list[str]) -> tuple[list[tuple[float, float]], tuple[float, float, float, float]]:
    """Compute (cx, cy) for each particle in the zigzag layout, plus the
    overall bounding box (xmin, ymin, xmax, ymax)."""
    positions: list[tuple[float, float]] = []
    for i, p in enumerate(particles):
        if i == 0:
            positions.append((0.0, -AMP))
            continue
        prev_w = WIDTH_BY_CLASS[particles[i - 1]]
        w = WIDTH_BY_CLASS[p]
        cx = positions[-1][0] + (prev_w + w) / 2 + EDGE / 2
        cy = -AMP if positions[-1][1] > -AMP else AMP
        positions.append((cx, cy))

    xmin = ymin = math.inf
    xmax = ymax = -math.inf
    for (px, py), p in zip(positions, particles):
        w = WIDTH_BY_CLASS[p]
        xmin = min(xmin, px - w / 2 - EDGE / 2)
        xmax = max(xmax, px + w / 2 + EDGE / 2)
        ymin = min(ymin, py - H / 2)
        ymax = max(ymax, py + H / 2)
    return positions, (xmin, ymin, xmax, ymax)


def render(particles: list[str], color: str, title: str) -> str:
    positions, (xmin, ymin, xmax, ymax) = layout(particles)
    w = xmax - xmin
    h = ymax - ymin

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{xmin:.2f} {ymin:.2f} {w:.2f} {h:.2f}" '
        f'preserveAspectRatio="xMidYMid meet" role="img" aria-label="{title}">',
        f'<title>{title}</title>',
    ]
    for (px, py), p in zip(positions, particles):
        pts = hex_points(px, py, WIDTH_BY_CLASS[p])
        parts.append(f'<polygon points="{pts}" fill="{color}"/>')
    parts.append('</svg>')
    return "\n".join(parts)


def main():
    out_dir = Path(__file__).resolve().parent
    structural_short = {  # slug → original-case structural shorthand
        "cv1c":   "CV1C",
        "ccv1c":  "CCV1C",
        "cv1cc":  "CV1CC",
        "cv2cv1": "CV2CV1",
        "cv2c":   "CV2C",
        "cv2":    "CV2",
        "v1c":    "V1C",
        "cv1":    "CV1",
        "cv1cv2": "CV1CV2",
        "ccv2":   "CCV2",
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
