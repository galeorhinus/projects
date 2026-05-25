#!/usr/bin/env python3
"""
fig_top_ten_racanas.py — Bar chart of the top 10 racanā scaffolds in the
Dhātupāṭha (which together cover 81.27% of the 2,168-entry corpus).

Y-axis: scaffold ICON (rendered procedurally as a small inline graphic).
        No text labels — the icon IS the label.
X-axis: count of dhātavaḥ in each scaffold.
Per-bar callouts carry structural shorthand + Devanāgarī (IAST) + mātrā.

Source: analysis/dhatupatha/data/derived/template_distribution.csv
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image, ImageDraw
from style import setup, savefig, FILL, ACCENT


# Preserve text as <text> elements in SVG so the renderer (browser / xelatex /
# rsvg) can apply proper Devanagari conjunct shaping at display time.
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["pdf.fonttype"] = 42


# --- Hexagon icon geometry (mirrors figures/icons/build_scaffold_icons.py) ---
ICON_H = 14.0
EDGE = ICON_H / math.sqrt(3)
WIDTH_BY_CLASS = {"C": EDGE / 2, "V1": EDGE, "V2": EDGE * 2}
AMP = ICON_H / 4

PARTICLES_BY_TEMPLATE = {
    "CV1C":   ["C", "V1", "C"],
    "CCV1C":  ["C", "C", "V1", "C"],
    "CV1CC":  ["C", "V1", "C", "C"],
    "CV2C":   ["C", "V2", "C"],
    "CV2":    ["C", "V2"],
    "V1C":    ["V1", "C"],
    "CCV2C":  ["C", "C", "V2", "C"],
    "CV1":    ["C", "V1"],
    "CCV2":   ["C", "C", "V2"],
    "CCV1CC": ["C", "C", "V1", "C", "C"],
    "CV2CV1": ["C", "V2", "C", "V1"],
    "CV1CV2": ["C", "V1", "C", "V2"],
}


def _hex_polygon(cx, cy, w):
    e = EDGE
    return [
        (cx - w / 2,         cy - ICON_H / 2),
        (cx + w / 2,         cy - ICON_H / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2,         cy + ICON_H / 2),
        (cx - w / 2,         cy + ICON_H / 2),
        (cx - w / 2 - e / 2, cy),
    ]


def _hex_layout(particles):
    positions = []
    for i, p in enumerate(particles):
        if i == 0:
            positions.append((0.0, -AMP))
            continue
        prev_w = WIDTH_BY_CLASS[particles[i - 1]]
        w = WIDTH_BY_CLASS[p]
        cx = positions[-1][0] + (prev_w + w) / 2 + EDGE / 2
        cy = -AMP if positions[-1][1] > -AMP else AMP
        positions.append((cx, cy))
    return positions


def render_scaffold_icon(template, color="#1a1a1a", height_px=160):
    """Render a scaffold as RGBA numpy array (transparent background)."""
    particles = PARTICLES_BY_TEMPLATE[template]
    positions = _hex_layout(particles)

    all_xs, all_ys = [], []
    for (cx, cy), p in zip(positions, particles):
        for x, y in _hex_polygon(cx, cy, WIDTH_BY_CLASS[p]):
            all_xs.append(x)
            all_ys.append(y)
    xmin, xmax = min(all_xs), max(all_xs)
    ymin, ymax = min(all_ys), max(all_ys)
    icon_w_data = xmax - xmin
    icon_h_data = ymax - ymin

    aspect = icon_w_data / icon_h_data
    h_px = height_px
    w_px = int(round(height_px * aspect))

    pad = 6
    img = Image.new("RGBA", (w_px + 2 * pad, h_px + 2 * pad), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    color_clean = color.lstrip("#")
    rgb = tuple(int(color_clean[i:i + 2], 16) for i in (0, 2, 4))

    def _to_px(x, y):
        px = (x - xmin) / icon_w_data * w_px + pad
        py = (y - ymin) / icon_h_data * h_px + pad
        return (px, py)

    for (cx, cy), p in zip(positions, particles):
        pts = _hex_polygon(cx, cy, WIDTH_BY_CLASS[p])
        pixel_pts = [_to_px(x, y) for x, y in pts]
        draw.polygon(pixel_pts, fill=rgb + (255,))

    return np.array(img)


# --- Bar chart data ---
# (scaffold, devanagari, iast, mātrā, count, percentage, cumulative)
# Source: analysis/dhatupatha/data/derived/template_distribution.csv
# (regenerated after the Pāṇini-1.3.2 strict anubandha-stripping fix —
# the previous data misclassified anunāsika-vowel-tailed roots).
TEMPLATES = [
    ("CV1C",   "गमादि",    "gamādi",   "2",   926, 42.7, 42.7),
    ("CCV1C",  "स्पदादि",   "spadādi",  "2½",  232, 10.7, 53.4),
    ("CV1CC",  "मन्थादि",   "manthādi", "2½",  216, 10.0, 63.4),
    ("CV2C",   "वाचादि",    "vācādi",   "3",   214,  9.9, 73.3),
    ("CV2",    "धादि",      "dhādi",    "2½",   89,  4.1, 77.4),
    ("V1C",    "इषादि",     "iṣādi",    "1½",   70,  3.2, 80.6),
    ("CCV2C",  "ह्रादादि",   "hrādādi",  "3½",   65,  3.0, 83.6),
    ("CV1",    "क्रादि",    "krādi",    "1½",   64,  3.0, 86.5),
    ("CCV2",   "स्थादि",    "sthādi",   "3",    49,  2.3, 88.8),
    ("CCV1CC", "स्पर्धादि", "spardhādi","3",    48,  2.2, 91.0),
    # 11th bar — the long tail: 59 other racanāḥ outside the top 10.
    # 2,168 − 1,973 (top-10 sum) = 195 dhātavaḥ; mātrā values span 1 to 6.
    ("(tail)", "",         "59 other racanāḥ", "1 to 6", 195, 9.0, 100.0),
]


def main():
    fig, ax = setup(figsize=(12, 9.8))

    counts = [t[4] for t in TEMPLATES]
    pcts = [t[5] for t in TEMPLATES]

    y_positions = list(range(len(TEMPLATES)))
    bars = ax.barh(
        y_positions, counts,
        color=ACCENT, edgecolor="black", linewidth=0.5,
        height=0.95,
        clip_on=False,
    )
    bars[0].set_color(FILL)
    # Tail bar: light-gray fill, no hatch, soft outline — text reads black on it.
    bars[-1].set_color("#e0e0e0")
    bars[-1].set_edgecolor("#bbbbbb")
    bars[-1].set_hatch("")

    ax.set_yticks(y_positions)
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()

    # Y-axis icons (replace tick labels) — gray, integrated with bar palette
    for i, t in enumerate(TEMPLATES):
        template = t[0]
        if template == "(tail)":
            # Tail row's identity is carried by the in-bar label, not a y-axis mark.
            continue
        arr = render_scaffold_icon(template, color="#888888", height_px=160)
        imagebox = OffsetImage(arr, zoom=0.17)
        ab = AnnotationBbox(
            imagebox,
            (0, i),
            xybox=(-12, 0),
            xycoords="data",
            boxcoords="offset points",
            frameon=False,
            box_alignment=(1.0, 0.5),
            pad=0,
        )
        ax.add_artist(ab)

    # Per-bar callouts
    COUNT_TEXT_X_OFFSET = 12
    RACANA_TEXT_X_OFFSET = 170
    INNER_RIGHT_MARGIN = 10  # data-units between count text and bar's right edge
    INNER_LEFT_PAD = 12      # data-units from bar's left edge to in-bar text start

    for i, (bar, count, pct, t) in enumerate(zip(bars, counts, pcts, TEMPLATES)):
        template, deva, iast, matra, _c, _p, _cum = t
        if deva:
            rachana_text = f"{template}  ·  {deva} ({iast})  ·  {matra} mātrā"
        else:
            rachana_text = f"{iast}  ·  {matra} mātrā"
        count_text = f"{count} ({pct:.1f}%)"
        y_center = bar.get_y() + bar.get_height() / 2

        if i == 0:
            # Top bar (gamādi): rachana centered, count right-aligned INSIDE
            # against the bar's right edge so the bar can fill the chart.
            ax.text(
                count / 2, y_center, rachana_text,
                ha="center", va="center",
                fontsize=20, color="white",
            )
            ax.text(
                count - INNER_RIGHT_MARGIN, y_center, count_text,
                ha="right", va="center",
                fontsize=17, color="white",
            )
        elif template == "(tail)":
            # Tail bar shrank with the corrected anubandha-stripping (195 vs
            # the old 406). The bar is now too narrow for in-bar text — keep
            # the lighter fill, but place count + label outside in the empty
            # area, same pattern as the smaller bars.
            ax.text(
                count + COUNT_TEXT_X_OFFSET, y_center, count_text,
                ha="left", va="center", fontsize=17,
            )
            ax.text(
                count + RACANA_TEXT_X_OFFSET, y_center, rachana_text,
                ha="left", va="center", fontsize=18,
                style="italic", color="#555555",
            )
        else:
            # Other bars: count just past bar end, rachana further right
            ax.text(
                count + COUNT_TEXT_X_OFFSET, y_center, count_text,
                ha="left", va="center", fontsize=17,
            )
            ax.text(
                count + RACANA_TEXT_X_OFFSET, y_center, rachana_text,
                ha="left", va="center", fontsize=18,
            )

    ax.set_xlabel("Count in the Dhātupāṭha", fontsize=20)
    ax.set_ylabel("")
    ax.tick_params(axis="x", labelsize=16)
    ax.set_xlim(0, max(counts) + 6)  # bar uses the full chart width
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.xaxis.set_ticks_position("bottom")

    plt.subplots_adjust(left=0.07, right=0.98, top=0.97, bottom=0.08)
    savefig("building_dhatuh_top_ten_racanas")


if __name__ == "__main__":
    main()
