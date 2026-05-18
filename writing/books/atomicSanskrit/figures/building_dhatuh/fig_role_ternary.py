"""Role Triangle — ternary plot of release / closure / bonding fractions.

Each consonant occupies a point in the role-triangle whose three vertices are
the pure-role extremes:

  bottom-left  = 100% release  (onset_outer dominant)
  bottom-right = 100% closure  (coda_outer dominant)
  top          = 100% bonding  (inner-cluster activity dominant)

Each consonant's position is its barycentric mix of the three role-fractions.

  r = onset_outer / (onset_outer + coda_outer + inner)
  c = coda_outer  / (onset_outer + coda_outer + inner)
  b = inner       / (onset_outer + coda_outer + inner)    where inner = onset_inner + coda_inner

Expected pattern:
  - र (universal bonder) moves toward the top (high bonding)
  - ट, ड, ष (closure specialists) toward bottom-right
  - क, व, प (release specialists) toward bottom-left
  - ल (neutralizer) near the centroid
  - retroflex stops cluster along the right edge

Color encodes place of articulation (same scheme as the valency scatter).

Data: copied from analysis/dhatupatha/FINDINGS.md §11 (single-akṣara
position-role counts, anubandha-aware).

Run: python3 figures/building_dhatuh/fig_role_ternary.py
"""

import math
from pathlib import Path


STATS = {
    "र": (78, 126, 100, 51),
    "क": (174, 5, 56, 53),
    "ष": (85, 31, 17, 134),
    "ल": (82, 40, 24, 105),
    "व": (129, 56, 2, 48),
    "प": (119, 9, 2, 74),
    "म": (118, 14, 29, 41),
    "स": (73, 4, 15, 86),
    "च": (82, 0, 4, 75),
    "श": (115, 0, 5, 39),
    "द": (70, 0, 2, 86),
    "ज": (53, 0, 7, 97),
    "त": (104, 8, 19, 22),
    "ट": (4, 16, 13, 105),
    "ण": (31, 9, 3, 63),
    "ह": (44, 0, 1, 58),
    "भ": (50, 0, 5, 47),
    "ग": (72, 0, 1, 27),
    "ड": (7, 0, 7, 84),
    "ध": (49, 2, 0, 37),
    "न": (10, 8, 17, 38),
    "य": (19, 30, 1, 21),
    "ब": (38, 1, 3, 27),
    "ख": (32, 3, 1, 27),
    "ठ": (0, 4, 4, 44),
    "घ": (26, 0, 2, 17),
    "थ": (1, 2, 0, 37),
    "फ": (4, 13, 0, 17),
    "ञ": (0, 3, 18, 0),
    # Skip low-deployment: झ, ङ, छ, ढ
}

PLACE_COLOR = {
    "velar":     "#2C5F8D",
    "palatal":   "#2C8D8D",
    "retroflex": "#8D2C8D",
    "dental":    "#D97000",
    "labial":    "#A02C2C",
    "semivowel": "#2C8D5F",
    "sibilant":  "#B8860B",
}

PLACE_LABEL = {
    "velar":     "Velar (कण्ठ्य)",
    "palatal":   "Palatal (तालव्य)",
    "retroflex": "Retroflex (मूर्धन्य)",
    "dental":    "Dental (दन्त्य)",
    "labial":    "Labial (ओष्ठ्य)",
    "semivowel": "Semivowel (अन्तःस्थ)",
    "sibilant":  "Sibilant/Aspirate (ऊष्म)",
}

PLACE_OF = {
    "क": "velar", "ख": "velar", "ग": "velar", "घ": "velar", "ङ": "velar",
    "च": "palatal", "छ": "palatal", "ज": "palatal", "झ": "palatal", "ञ": "palatal",
    "ट": "retroflex", "ठ": "retroflex", "ड": "retroflex", "ढ": "retroflex", "ण": "retroflex",
    "त": "dental", "थ": "dental", "द": "dental", "ध": "dental", "न": "dental",
    "प": "labial", "फ": "labial", "ब": "labial", "भ": "labial", "म": "labial",
    "य": "semivowel", "र": "semivowel", "ल": "semivowel", "व": "semivowel",
    "श": "sibilant", "ष": "sibilant", "स": "sibilant", "ह": "sibilant",
}


def main():
    # Figure dimensions
    width = 640
    height = 560
    # Triangle layout
    tri_w = 420   # base width
    tri_h = tri_w * math.sqrt(3) / 2  # equilateral

    # Vertex coordinates (in SVG y-down coords)
    margin_top = 60
    margin_left = 70

    v_release = (margin_left, margin_top + tri_h)            # bottom-left
    v_closure = (margin_left + tri_w, margin_top + tri_h)    # bottom-right
    v_bonding = (margin_left + tri_w / 2, margin_top)        # top

    def to_xy(r_frac, c_frac, b_frac):
        """Convert barycentric (release, closure, bonding) to SVG coords."""
        x = r_frac * v_release[0] + c_frac * v_closure[0] + b_frac * v_bonding[0]
        y = r_frac * v_release[1] + c_frac * v_closure[1] + b_frac * v_bonding[1]
        return x, y

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="Charter, &quot;Bitstream Charter&quot;, &quot;DejaVu Serif&quot;, serif">'
    )
    svg.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    # Draw triangle
    svg.append(
        f'<polygon points="'
        f'{v_release[0]:.1f},{v_release[1]:.1f} '
        f'{v_closure[0]:.1f},{v_closure[1]:.1f} '
        f'{v_bonding[0]:.1f},{v_bonding[1]:.1f}" '
        f'fill="none" stroke="black" stroke-width="0.8"/>'
    )

    # Gridlines (lines parallel to each edge at 25/50/75% positions)
    for frac in [0.25, 0.50, 0.75]:
        # Line parallel to release-closure edge (bottom) at height b=frac
        x1, y1 = to_xy(1 - frac, 0, frac)
        x2, y2 = to_xy(0, 1 - frac, frac)
        svg.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#dddddd" stroke-width="0.4"/>'
        )
        # Line parallel to closure-bonding edge (right) at r=frac
        x1, y1 = to_xy(frac, 1 - frac, 0)
        x2, y2 = to_xy(frac, 0, 1 - frac)
        svg.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#dddddd" stroke-width="0.4"/>'
        )
        # Line parallel to release-bonding edge (left) at c=frac
        x1, y1 = to_xy(0, frac, 1 - frac)
        x2, y2 = to_xy(1 - frac, frac, 0)
        svg.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#dddddd" stroke-width="0.4"/>'
        )

    # Vertex labels
    svg.append(
        f'<text x="{v_release[0] - 6}" y="{v_release[1] + 16}" '
        f'font-size="11" font-weight="bold" text-anchor="end">RELEASE</text>'
    )
    svg.append(
        f'<text x="{v_release[0] - 6}" y="{v_release[1] + 30}" '
        f'font-size="9" text-anchor="end" fill="#666">atom-start dominant</text>'
    )
    svg.append(
        f'<text x="{v_closure[0] + 6}" y="{v_closure[1] + 16}" '
        f'font-size="11" font-weight="bold" text-anchor="start">CLOSURE</text>'
    )
    svg.append(
        f'<text x="{v_closure[0] + 6}" y="{v_closure[1] + 30}" '
        f'font-size="9" text-anchor="start" fill="#666">atom-end dominant</text>'
    )
    svg.append(
        f'<text x="{v_bonding[0]}" y="{v_bonding[1] - 14}" '
        f'font-size="11" font-weight="bold" text-anchor="middle">BONDING</text>'
    )
    svg.append(
        f'<text x="{v_bonding[0]}" y="{v_bonding[1] - 2}" '
        f'font-size="9" text-anchor="middle" fill="#666">inner-cluster dominant</text>'
    )

    # Plot consonants
    bubble_r = 7
    points = []
    for ch, (oo, oi, ci, co) in STATS.items():
        inner = oi + ci
        total = oo + co + inner
        if total < 5:
            continue
        r_frac = oo / total
        c_frac = co / total
        b_frac = inner / total
        x, y = to_xy(r_frac, c_frac, b_frac)
        place = PLACE_OF.get(ch, "sibilant")
        color = PLACE_COLOR[place]
        points.append((ch, x, y, color))

    # Bubbles
    for ch, x, y, color in points:
        svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{bubble_r}" '
            f'fill="{color}" fill-opacity="0.65" stroke="black" stroke-width="0.4"/>'
        )

    # Labels (Devanagari, positioned to top-right of bubble)
    for ch, x, y, color in points:
        lx = x + bubble_r + 2
        ly = y - 1
        svg.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="12" '
            f'font-weight="bold">{ch}</text>'
        )

    # Legend
    legend_x = margin_left + tri_w + 30
    legend_y = margin_top + 20
    svg.append(
        f'<text x="{legend_x}" y="{legend_y - 6}" '
        f'font-size="10" font-weight="bold">Place</text>'
    )
    for i, key in enumerate(["velar", "palatal", "retroflex", "dental", "labial", "semivowel", "sibilant"]):
        y = legend_y + 14 + i * 18
        svg.append(
            f'<circle cx="{legend_x + 6}" cy="{y - 4}" r="6" '
            f'fill="{PLACE_COLOR[key]}" fill-opacity="0.65" '
            f'stroke="black" stroke-width="0.4"/>'
        )
        svg.append(
            f'<text x="{legend_x + 18}" y="{y - 1}" font-size="9">{PLACE_LABEL[key]}</text>'
        )

    svg.append("</svg>")

    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "building_dhatuh_role_ternary.svg"
    out_path.write_text("\n".join(svg))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
