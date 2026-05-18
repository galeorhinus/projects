"""Subatomic periodicity grid — varṇamālā colored by position-role behavior.

Generates an SVG directly (no matplotlib dependency) so the figure builds
regardless of the local Python environment's numpy/matplotlib state.

For each of the 33 consonants in the varṇamālā, classify its dominant
position-role from the Dhātupāṭha corpus and color the cell accordingly:

  BLUE   — onset / release specialist     (onset-deployment ≥ 65% of total)
  RED    — coda / closure specialist      (coda-deployment ≥ 65% of total)
  GREEN  — cluster-joiner / bonder        (inner-cluster ≥ 25% of total)
  GOLD   — balanced / neutralizer         (no strong lean; multi-role)
  GRAY   — low deployment                 (total < 15)

Data: copied from analysis/dhatupatha/FINDINGS.md §11 (single-akṣara
position-role counts, anubandha-aware).

Run: python3 figures/building_dhatuh/fig_subatomic_periodicity.py
"""

from pathlib import Path


# ---- Data: per-consonant position-role counts (FINDINGS.md §11) ----
# Format: char -> (onset_outer, onset_inner, coda_inner, coda_outer)
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


# ---- Colors ----
COLOR_ONSET = "#1F4E79"    # dark blue — release/onset specialist
COLOR_CODA = "#822529"     # dark red — closure/coda specialist
COLOR_BONDER = "#2D6A4F"   # dark green — cluster-joiner/bonder
COLOR_NEUTRAL = "#B8860B"  # dark goldenrod — balanced/neutralizer
COLOR_LOW = "#BBBBBB"      # light gray — low deployment


# ---- Canonical varṇamālā layout ----
GRID = [
    ("कण्ठ्य", "velar", ["क", "ख", "ग", "घ", "ङ"]),
    ("तालव्य", "palatal", ["च", "छ", "ज", "झ", "ञ"]),
    ("मूर्धन्य", "retroflex", ["ट", "ठ", "ड", "ढ", "ण"]),
    ("दन्त्य", "dental", ["त", "थ", "द", "ध", "न"]),
    ("ओष्ठ्य", "labial", ["प", "फ", "ब", "भ", "म"]),
    ("अन्तःस्थाः", "semivowels", ["य", "र", "ल", "व", None]),
    ("ऊष्माणः", "sibilants", ["श", "ष", "स", "ह", None]),
]
COLUMNS = [
    ("C1", "unv-unasp"),
    ("C2", "unv-asp"),
    ("C3", "voi-unasp"),
    ("C4", "voi-asp"),
    ("C5", "nasal"),
]


def classify(ch):
    """Return color + category for a consonant from its position-role stats."""
    stats = STATS.get(ch)
    if not stats:
        return COLOR_LOW, "low"

    oo, oi, ci, co = stats
    total = oo + oi + ci + co
    if total < 15:
        return COLOR_LOW, "low"

    onset = oo + oi
    coda = ci + co
    inner = oi + ci

    inner_pct = inner / total
    onset_pct = onset / total
    coda_pct = coda / total

    # Strong cluster-joiner: 25%+ inner activity
    if inner_pct >= 0.25:
        return COLOR_BONDER, "bonder"

    # Strong onset specialist
    if onset_pct >= 0.65:
        return COLOR_ONSET, "onset"

    # Strong coda specialist
    if coda_pct >= 0.65:
        return COLOR_CODA, "coda"

    # Otherwise balanced
    return COLOR_NEUTRAL, "balanced"


def main():
    # Geometry (SVG units = points-ish, set width/height for trade-book column)
    cell_w = 60
    cell_h = 60
    place_w = 110     # left margin for place labels
    col_label_h = 30  # top margin for column labels
    legend_h = 130

    n_cols = 5
    n_rows = len(GRID)

    width = place_w + n_cols * cell_w + 20
    height = col_label_h + n_rows * cell_h + legend_h + 20

    svg = []
    svg.append(f'<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="Charter, &quot;Bitstream Charter&quot;, &quot;DejaVu Serif&quot;, serif">'
    )

    # Background
    svg.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    # Column labels (top)
    for c, (col, sub) in enumerate(COLUMNS):
        x = place_w + c * cell_w + cell_w / 2
        y_top = col_label_h - 14
        y_bot = col_label_h - 2
        svg.append(
            f'<text x="{x}" y="{y_top}" font-size="10" font-weight="bold" '
            f'text-anchor="middle">{col}</text>'
        )
        svg.append(
            f'<text x="{x}" y="{y_bot}" font-size="8" fill="#666" '
            f'text-anchor="middle">{sub}</text>'
        )

    # Rows
    for r, (dev_label, eng_label, cells) in enumerate(GRID):
        y = col_label_h + r * cell_h

        # Place label (left)
        label_x = place_w - 10
        ly1 = y + cell_h / 2 - 6
        ly2 = y + cell_h / 2 + 8
        svg.append(
            f'<text x="{label_x}" y="{ly1}" font-size="11" '
            f'text-anchor="end">{dev_label}</text>'
        )
        svg.append(
            f'<text x="{label_x}" y="{ly2}" font-size="8" fill="#666" '
            f'text-anchor="end">({eng_label})</text>'
        )

        # Cells
        for c, ch in enumerate(cells):
            if ch is None:
                continue
            x = place_w + c * cell_w
            color, cat = classify(ch)
            total = sum(STATS.get(ch, (0, 0, 0, 0)))

            svg.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
                f'fill="{color}" stroke="black" stroke-width="0.5"/>'
            )
            # Devanagari character
            svg.append(
                f'<text x="{x + cell_w/2}" y="{y + cell_h*0.55}" '
                f'font-size="28" font-weight="bold" fill="white" '
                f'text-anchor="middle" dominant-baseline="middle">{ch}</text>'
            )
            # Count
            if total > 0:
                svg.append(
                    f'<text x="{x + cell_w/2}" y="{y + cell_h - 8}" '
                    f'font-size="8" fill="white" text-anchor="middle">'
                    f'n={total}</text>'
                )

    # Legend
    legend_y = col_label_h + n_rows * cell_h + 30
    entries = [
        (COLOR_ONSET, "Onset / release specialist (≥65% onset)"),
        (COLOR_CODA, "Coda / closure specialist (≥65% coda)"),
        (COLOR_BONDER, "Cluster-joiner / bonder (≥25% inner)"),
        (COLOR_NEUTRAL, "Balanced / neutralizer (no strong lean)"),
        (COLOR_LOW, "Low deployment (n&lt;15)"),
    ]
    box_w = 14
    box_h = 14
    row_h = 19
    col_x = [20, 280]
    for i, (color, label) in enumerate(entries):
        col = i // 3
        row = i % 3
        x = col_x[col]
        y = legend_y + row * row_h
        svg.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" '
            f'fill="{color}" stroke="black" stroke-width="0.4"/>'
        )
        svg.append(
            f'<text x="{x + box_w + 6}" y="{y + box_h - 3}" '
            f'font-size="9.5">{label}</text>'
        )

    svg.append("</svg>")

    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "building_dhatuh_subatomic_periodicity.svg"
    out_path.write_text("\n".join(svg))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
