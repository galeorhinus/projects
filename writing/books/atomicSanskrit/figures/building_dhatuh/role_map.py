"""Role map — onset × coda bubble scatter with inner-cluster as bubble size.

Each consonant is plotted as a bubble. The x-axis is total onset deployment
(atom-start + cluster-joiner-before-vowel); the y-axis is total coda deployment
(cluster-joiner-after-vowel + atom-end). Bubble size encodes inner-cluster
activity (the cluster-joining work). In color mode, color encodes place of
articulation; in gray mode, a single neutral fill is used and the visual
encoding reduces to the position + size dimensions.

Patterns the figure surfaces:
  - Onset specialists (क, व, प, श) far right
  - Coda specialists (ष, ज, स, ल, ट, ड) high up
  - र as the largest bubble — universal bonder, covers all four position-roles
  - ल near the diagonal — structural neutralizer
  - Retroflex closure pattern (ट, ठ, ड, ण high up, low x)

Data source: position-role counts derived from
`analysis/dhatupatha/scripts/analyze_position_roles.py` (single-akṣara atoms,
anubandha-aware). Counts are inlined here to keep the figure script
standalone.

Run: python3 figures/building_dhatuh/role_map.py
Outputs:
  figures/building_dhatuh/role_map_color.from-py.svg
  figures/building_dhatuh/role_map_color.svg
  figures/building_dhatuh/role_map_gray.from-py.svg
  figures/building_dhatuh/role_map_gray.svg
"""

import math
import sys
from pathlib import Path


# Make figures/_shared importable from this subdirectory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _shared.lineage import promote


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

PLACE_OF = {
    "क": "velar", "ख": "velar", "ग": "velar", "घ": "velar", "ङ": "velar",
    "च": "palatal", "छ": "palatal", "ज": "palatal", "झ": "palatal", "ञ": "palatal",
    "ट": "retroflex", "ठ": "retroflex", "ड": "retroflex", "ढ": "retroflex", "ण": "retroflex",
    "त": "dental", "थ": "dental", "द": "dental", "ध": "dental", "न": "dental",
    "प": "labial", "फ": "labial", "ब": "labial", "भ": "labial", "म": "labial",
    "य": "semivowel", "र": "semivowel", "ल": "semivowel", "व": "semivowel",
    "श": "sibilant", "ष": "sibilant", "स": "sibilant", "ह": "sibilant",
}

PLACE_COLOR_COLOR = {
    "velar":     "#2C5F8D",
    "palatal":   "#2C8D8D",
    "retroflex": "#8D2C8D",
    "dental":    "#D97000",
    "labial":    "#A02C2C",
    "semivowel": "#2C8D5F",
    "sibilant":  "#B8860B",
}

# Single neutral gray for all places — print-monochrome mode.
PLACE_COLOR_GRAY = {k: "#888888" for k in PLACE_COLOR_COLOR}

PLACE_LABEL_COMPACT = {
    "velar":     "Velar",
    "palatal":   "Palatal",
    "retroflex": "Retroflex",
    "dental":    "Dental",
    "labial":    "Labial",
    "semivowel": "Semivowel",
    "sibilant":  "Sibilant",
}

# Axis configuration per book design notes
X_MAX = 225   # cut at 225; last labelled tick at 200
Y_MAX = 175   # cut at 175; last labelled tick at 150
X_TICKS = [0, 50, 100, 150, 200]
Y_TICKS = [0, 50, 100, 150]

# The figure is designed for the 4.5 inch trade-book text block. Text sizes
# below are SVG units: at 800 viewBox units over 4.5 inches, 20 units is ~8 pt.
TICK_FONT = 20
AXIS_FONT = 25
LEGEND_HEADER_FONT = 24
LEGEND_FONT = 20
MIN_DEVANAGARI_FONT = 20
LEADER_LINE_WIDTH = 0.8

# Threshold below which a label is rendered outside the bubble with a leader.
INSIDE_RADIUS_THRESHOLD = 16


def compute_points():
    """Return [(ch, onset, coda, inner)] for consonants with non-trivial deployment."""
    out = []
    for ch, (oo, oi, ci, co) in STATS.items():
        onset = oo + oi
        coda = ci + co
        inner = oi + ci
        if onset + coda < 5:
            continue
        out.append((ch, onset, coda, inner))
    return out


def render(mode: str, out_path: Path):
    """Render one SVG. mode is 'color' or 'gray'."""
    assert mode in ("color", "gray")
    place_color = PLACE_COLOR_COLOR if mode == "color" else PLACE_COLOR_GRAY
    show_place_legend = (mode == "color")

    width = 800
    height = 620
    svg_width_in = 4.5
    svg_height_in = svg_width_in * height / width
    pad_l = 48
    pad_r = 18
    pad_t = 36
    pad_b = 84
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    points = compute_points()
    max_inner = max(p[3] for p in points)

    def bubble_r(inner: float) -> float:
        return 6 + 46 * math.sqrt(inner / max_inner)

    def to_screen(x: float, y: float) -> tuple[float, float]:
        sx = pad_l + (x / X_MAX) * plot_w
        sy = pad_t + plot_h - (y / Y_MAX) * plot_h
        return sx, sy

    plot_left   = pad_l
    plot_right  = pad_l + plot_w
    plot_top    = pad_t
    plot_bottom = pad_t + plot_h
    plot_cx, plot_cy = to_screen(X_MAX / 2, Y_MAX / 2)

    bubble_data = []
    for ch, onset, coda, inner in points:
        sx, sy = to_screen(onset, coda)
        r = bubble_r(inner)
        bubble_data.append({
            "ch": ch, "onset": onset, "coda": coda, "inner": inner,
            "sx": sx, "sy": sy, "r": r,
            "place": PLACE_OF.get(ch, "sibilant"),
        })

    # Decide inside-vs-outside labelling. Outside if radius below threshold OR
    # bubble is significantly obscured by a larger bubble.
    bubble_data.sort(key=lambda b: -b["r"])
    for i, b in enumerate(bubble_data):
        if b["r"] < INSIDE_RADIUS_THRESHOLD:
            b["outside"] = True
            continue
        obscured = False
        for j in range(i):
            other = bubble_data[j]
            dist = math.hypot(b["sx"] - other["sx"], b["sy"] - other["sy"])
            if other["r"] > b["r"] and dist + b["r"] * 0.6 < other["r"]:
                obscured = True
                break
        b["outside"] = obscured

    def outside_initial(b: dict) -> tuple[float, float]:
        cx, cy, r = b["sx"], b["sy"], b["r"]
        dx, dy = cx - plot_cx, cy - plot_cy
        dist = math.hypot(dx, dy)
        if dist < 1:
            ux, uy = 1.0, 0.0
        else:
            ux, uy = dx / dist, dy / dist
        offset = r + 16
        lx = cx + offset * ux
        ly = cy + offset * uy
        lx = max(plot_left + 12, min(plot_right - 12, lx))
        ly = max(plot_top + 12, min(plot_bottom - 12, ly))
        return lx, ly

    outside_bubbles = [b for b in bubble_data if b["outside"]]
    label_positions = {}
    for b in outside_bubbles:
        lx, ly = outside_initial(b)
        label_positions[b["ch"]] = {"lx": lx, "ly": ly, "b": b}

    # Iterative repulsion between outside labels to reduce overlap
    label_radius = MIN_DEVANAGARI_FONT * 0.62
    for _ in range(60):
        moved = False
        items = list(label_positions.values())
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, c = items[i], items[j]
                ddx = c["lx"] - a["lx"]
                ddy = c["ly"] - a["ly"]
                d = math.hypot(ddx, ddy)
                if 0.001 < d < 2 * label_radius:
                    push = (2 * label_radius - d) / 2 + 0.4
                    ux, uy = ddx / d, ddy / d
                    a["lx"] -= push * ux
                    a["ly"] -= push * uy
                    c["lx"] += push * ux
                    c["ly"] += push * uy
                    moved = True
        for v in items:
            v["lx"] = max(plot_left + 26, min(plot_right - 12, v["lx"]))
            v["ly"] = max(plot_top + 18, min(plot_bottom - 22, v["ly"]))
        if not moved:
            break

    # Compute leader-line edge points
    for v in label_positions.values():
        b = v["b"]
        cx, cy, r = b["sx"], b["sy"], b["r"]
        bdx, bdy = v["lx"] - cx, v["ly"] - cy
        bdist = math.hypot(bdx, bdy)
        if bdist < 0.001:
            v["ex"], v["ey"] = cx, cy
        else:
            v["ex"] = cx + r * bdx / bdist
            v["ey"] = cy + r * bdy / bdist

    # --- SVG assembly ---
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width_in}in" height="{svg_height_in:.4f}in" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="Charter, &quot;Bitstream Charter&quot;, &quot;DejaVu Serif&quot;, serif">'
    )
    svg.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    ax_y1 = pad_t + plot_h
    ax_x2 = pad_l + plot_w
    ax_y2 = pad_t
    svg.append(f'<line x1="{pad_l}" y1="{ax_y1}" x2="{ax_x2}" y2="{ax_y1}" stroke="black" stroke-width="0.8"/>')
    svg.append(f'<line x1="{pad_l}" y1="{ax_y1}" x2="{pad_l}" y2="{ax_y2}" stroke="black" stroke-width="0.8"/>')

    for tick in X_TICKS:
        sx, _ = to_screen(tick, 0)
        svg.append(
            f'<line x1="{sx}" y1="{ax_y1}" x2="{sx}" y2="{ax_y1 + 5}" '
            f'stroke="black" stroke-width="0.6"/>'
        )
        svg.append(
            f'<text x="{sx}" y="{ax_y1 + 26}" font-size="{TICK_FONT}" text-anchor="middle">{tick}</text>'
        )
    for tick in Y_TICKS:
        _, sy = to_screen(0, tick)
        svg.append(
            f'<line x1="{pad_l - 5}" y1="{sy}" x2="{pad_l}" y2="{sy}" '
            f'stroke="black" stroke-width="0.6"/>'
        )
        svg.append(
            f'<text x="{pad_l - 10}" y="{sy + 7}" font-size="{TICK_FONT}" text-anchor="end">{tick}</text>'
        )

    svg.append(
        f'<text x="{pad_l + plot_w / 2}" y="{height - 22}" '
        f'font-size="{AXIS_FONT}" text-anchor="middle">Onset deployment</text>'
    )

    # Leader lines (under bubbles)
    for v in label_positions.values():
        svg.append(
            f'<line x1="{v["ex"]:.1f}" y1="{v["ey"]:.1f}" '
            f'x2="{v["lx"]:.1f}" y2="{v["ly"]:.1f}" '
            f'stroke="#888" stroke-width="{LEADER_LINE_WIDTH}"/>'
        )

    # Bubbles
    for b in bubble_data:
        color = place_color[b["place"]]
        svg.append(
            f'<circle cx="{b["sx"]:.1f}" cy="{b["sy"]:.1f}" r="{b["r"]:.1f}" '
            f'fill="{color}" fill-opacity="0.55" stroke="#333" stroke-width="0.5"/>'
        )

    # Inside labels — black, bold, scale with radius (min 8pt at 4.5in width)
    for b in bubble_data:
        if b["outside"]:
            continue
        fs = max(MIN_DEVANAGARI_FONT, min(b["r"] * 1.2, 32))
        svg.append(
            f'<text x="{b["sx"]:.1f}" y="{b["sy"]:.1f}" font-size="{fs:.1f}" '
            f'font-weight="bold" fill="#1a1a1a" '
            f'text-anchor="middle" dominant-baseline="central">{b["ch"]}</text>'
        )

    # Outside labels — black, bold, min 8pt at 4.5in width, with white halo for legibility
    for v in label_positions.values():
        svg.append(
            f'<text x="{v["lx"]:.1f}" y="{v["ly"]:.1f}" font-size="{MIN_DEVANAGARI_FONT}" '
            f'font-weight="bold" fill="#1a1a1a" '
            f'text-anchor="middle" dominant-baseline="central" '
            f'stroke="white" stroke-width="3" paint-order="stroke">'
            f'{v["b"]["ch"]}</text>'
        )

    # Legend
    if show_place_legend:
        legend_x = plot_right - 102
        legend_y = pad_t + 154
        row_gap = 22
        legend_rows = ["velar", "palatal", "retroflex", "dental", "labial", "semivowel", "sibilant"]
        svg.append(
            f'<rect x="{legend_x - 16}" y="{legend_y - 30}" width="120" height="184" '
            f'rx="4" fill="white" fill-opacity="0.88" stroke="#dddddd" stroke-width="0.4"/>'
        )
        svg.append(
            f'<text x="{legend_x}" y="{legend_y}" '
            f'font-size="{LEGEND_HEADER_FONT}" font-weight="bold">Place</text>'
        )
        for i, key in enumerate(legend_rows):
            y = legend_y + 27 + i * row_gap
            svg.append(
                f'<circle cx="{legend_x + 8}" cy="{y - 6}" r="7" '
                f'fill="{place_color[key]}" fill-opacity="0.55" '
                f'stroke="#333" stroke-width="0.4"/>'
            )
            svg.append(
                f'<text x="{legend_x + 20}" y="{y}" font-size="{LEGEND_FONT}">{PLACE_LABEL_COMPACT[key]}</text>'
            )
        bs_legend_x = plot_left + 24
        bs_legend_top = plot_top + 32
    else:
        bs_legend_x = plot_left + 24
        bs_legend_top = plot_top + 32

    svg.append(
        f'<text x="{bs_legend_x}" y="{bs_legend_top}" '
        f'font-size="{LEGEND_HEADER_FONT}" font-weight="bold">Inner-cluster size</text>'
    )
    sample_sizes = [50, 150]
    circle_top = bs_legend_top + 24
    for i, s in enumerate(sample_sizes):
        cx = bs_legend_x + 32 + i * 92
        r = bubble_r(s)
        cy = circle_top + r
        svg.append(
            f'<text x="{cx}" y="{circle_top - 8}" font-size="{LEGEND_FONT}" text-anchor="middle">n={s}</text>'
        )
        svg.append(
            f'<circle cx="{cx}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="#888" fill-opacity="0.5" stroke="#333" stroke-width="0.4"/>'
        )

    svg.append("</svg>")
    out_path.write_text("\n".join(svg))
    print(f"Wrote {out_path}")


def main():
    out_dir = Path(__file__).resolve().parent
    color_source = out_dir / "role_map_color.from-py.svg"
    gray_source = out_dir / "role_map_gray.from-py.svg"
    render("color", color_source)
    render("gray", gray_source)
    print(f"Promoted {promote(color_source)}")
    print(f"Promoted {promote(gray_source)}")


if __name__ == "__main__":
    main()
