"""Valency Map — onset × coda scatter with inner-cluster as bubble size.

Each consonant is plotted as a bubble. The x-axis is total onset deployment
(atom-start + cluster-joiner-before-vowel); the y-axis is total coda deployment
(cluster-joiner-after-vowel + atom-end). Bubble size encodes inner-cluster
activity (the cluster-joining work). Color encodes place of articulation.

Expected patterns:
  - Onset specialists (क, व, प, त, श) far right
  - Coda specialists (ट, ज, स, ड) high up
  - Balanced consonants near the diagonal
  - र as a huge bubble (universal bonder)
  - ल near the diagonal (structural neutralizer)
  - Retroflex closure pattern (ट, ठ, ड, ण high up, low x)

Data: copied from analysis/dhatupatha/FINDINGS.md §11 (single-akṣara
position-role counts, anubandha-aware).

Run: python3 figures/building_dhatuh/fig_valency_scatter.py
"""

import math
from pathlib import Path


# Per-consonant position-role counts: (onset_outer, onset_inner, coda_inner, coda_outer)
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
    "झ": (8, 0, 0, 2),
    "ङ": (1, 0, 3, 0),
    "छ": (0, 0, 0, 1),
    "ढ": (0, 0, 1, 0),
}

# Place of articulation → color
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
    width = 760
    height = 600
    pad_l, pad_r, pad_t, pad_b = 100, 230, 50, 90  # right margin for legend
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    # Compute onset/coda/inner per consonant
    points = []
    for ch, (oo, oi, ci, co) in STATS.items():
        onset = oo + oi
        coda = ci + co
        inner = oi + ci
        if onset + coda < 5:
            continue  # skip near-zero deployment
        points.append((ch, onset, coda, inner))

    max_x = max(p[1] for p in points)
    max_y = max(p[2] for p in points)
    max_inner = max(p[3] for p in points)

    # Round up axes
    def round_up_to_50(v):
        return ((int(v) // 50) + 1) * 50
    x_max = round_up_to_50(max_x)
    y_max = round_up_to_50(max_y)

    # Bubble radius scaling: 2x previous range (min 6, max 52)
    def bubble_r(inner):
        if max_inner == 0:
            return 10
        # square-root scaling so area is proportional to count
        return 6 + 46 * math.sqrt(inner / max_inner)

    # Audiograph font size proportional to bubble radius (capped for legibility)
    def label_font(r):
        return max(7, min(r * 1.0, 36))

    def to_screen(x, y):
        sx = pad_l + (x / x_max) * plot_w
        sy = pad_t + plot_h - (y / y_max) * plot_h
        return sx, sy

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="Charter, &quot;Bitstream Charter&quot;, &quot;DejaVu Serif&quot;, serif">'
    )
    svg.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    # Axes
    ax_x1, ax_y1 = pad_l, pad_t + plot_h
    ax_x2 = pad_l + plot_w
    ax_y2 = pad_t
    svg.append(f'<line x1="{pad_l}" y1="{ax_y1}" x2="{ax_x2}" y2="{ax_y1}" stroke="black" stroke-width="0.8"/>')
    svg.append(f'<line x1="{pad_l}" y1="{ax_y1}" x2="{pad_l}" y2="{ax_y2}" stroke="black" stroke-width="0.8"/>')

    # Tick marks + labels (axis-number font 1.5x larger: 9 -> 14)
    n_ticks = 5
    for i in range(n_ticks + 1):
        # X ticks
        x_val = (x_max / n_ticks) * i
        sx, _ = to_screen(x_val, 0)
        svg.append(
            f'<line x1="{sx}" y1="{ax_y1}" x2="{sx}" y2="{ax_y1 + 5}" '
            f'stroke="black" stroke-width="0.6"/>'
        )
        svg.append(
            f'<text x="{sx}" y="{ax_y1 + 22}" font-size="14" text-anchor="middle">{int(x_val)}</text>'
        )
        # Y ticks
        y_val = (y_max / n_ticks) * i
        _, sy = to_screen(0, y_val)
        svg.append(
            f'<line x1="{pad_l - 5}" y1="{sy}" x2="{pad_l}" y2="{sy}" '
            f'stroke="black" stroke-width="0.6"/>'
        )
        svg.append(
            f'<text x="{pad_l - 10}" y="{sy + 5}" font-size="14" text-anchor="end">{int(y_val)}</text>'
        )

    # Axis labels (axis-description font 2x bigger: 11 -> 22)
    svg.append(
        f'<text x="{pad_l + plot_w / 2}" y="{height - 22}" '
        f'font-size="22" text-anchor="middle">Onset deployment</text>'
    )
    svg.append(
        f'<text x="30" y="{pad_t + plot_h / 2}" '
        f'font-size="22" text-anchor="middle" '
        f'transform="rotate(-90 30 {pad_t + plot_h / 2})">'
        f'Coda deployment</text>'
    )

    # Diagonal y=x line (for balanced reference)
    diag_max = min(x_max, y_max)
    dx1, dy1 = to_screen(0, 0)
    dx2, dy2 = to_screen(diag_max, diag_max)
    svg.append(
        f'<line x1="{dx1}" y1="{dy1}" x2="{dx2}" y2="{dy2}" '
        f'stroke="#cccccc" stroke-width="0.5" stroke-dasharray="3,3"/>'
    )
    svg.append(
        f'<text x="{dx2 - 6}" y="{dy2 + 16}" font-size="12" fill="#888" '
        f'text-anchor="end">onset = coda</text>'
    )

    # Bubbles drawn largest-first (so smaller bubbles overlap on top)
    for ch, onset, coda, inner in sorted(points, key=lambda p: -p[3]):
        sx, sy = to_screen(onset, coda)
        r = bubble_r(inner)
        place = PLACE_OF.get(ch, "sibilant")
        color = PLACE_COLOR[place]
        svg.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" '
            f'fill="{color}" fill-opacity="0.55" stroke="black" stroke-width="0.5"/>'
        )

    # Audiograph labels INSIDE bubbles, font size proportional to radius
    for ch, onset, coda, inner in sorted(points, key=lambda p: -p[3]):
        sx, sy = to_screen(onset, coda)
        r = bubble_r(inner)
        fs = label_font(r)
        svg.append(
            f'<text x="{sx:.1f}" y="{sy:.1f}" font-size="{fs:.1f}" '
            f'font-weight="bold" fill="white" '
            f'text-anchor="middle" dominant-baseline="central">{ch}</text>'
        )

    # Legend (right side) — fonts 1.5x bigger: 10 -> 15 (header), 9 -> 14 (entries)
    legend_x = pad_l + plot_w + 30
    legend_y = pad_t + 10
    svg.append(
        f'<text x="{legend_x}" y="{legend_y - 4}" '
        f'font-size="15" font-weight="bold">Place</text>'
    )
    for i, key in enumerate(["velar", "palatal", "retroflex", "dental", "labial", "semivowel", "sibilant"]):
        y = legend_y + 18 + i * 26
        svg.append(
            f'<circle cx="{legend_x + 9}" cy="{y - 5}" r="9" '
            f'fill="{PLACE_COLOR[key]}" fill-opacity="0.6" '
            f'stroke="black" stroke-width="0.4"/>'
        )
        svg.append(
            f'<text x="{legend_x + 24}" y="{y - 1}" font-size="14">{PLACE_LABEL[key]}</text>'
        )

    # Bubble-size legend (representative sizes, scaled down from plot scale)
    bs_y = legend_y + 18 + 7 * 26 + 22
    svg.append(
        f'<text x="{legend_x}" y="{bs_y}" font-size="15" font-weight="bold">Inner-cluster size</text>'
    )
    sample_sizes = [50, 150, max_inner]
    for i, s in enumerate(sample_sizes):
        cx = legend_x + 22 + i * 60
        cy = bs_y + 42
        # Use the actual plot-scale bubble_r so legend matches plot
        r = bubble_r(s)
        svg.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" '
            f'fill="#888" fill-opacity="0.5" stroke="black" stroke-width="0.4"/>'
        )
        svg.append(
            f'<text x="{cx}" y="{cy + r + 14}" font-size="12" text-anchor="middle">n={s}</text>'
        )

    svg.append("</svg>")

    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "building_dhatuh_valency_scatter.svg"
    out_path.write_text("\n".join(svg))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
