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
    "CV2CV1": ["C", "V2", "C", "V1"],
    "CV2C":   ["C", "V2", "C"],
    "CV2":    ["C", "V2"],
    "V1C":    ["V1", "C"],
    "CV1":    ["C", "V1"],
    "CV1CV2": ["C", "V1", "C", "V2"],
    "CCV2":   ["C", "C", "V2"],
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
# Same ordering as the §10.6 roster table — descending count.
TEMPLATES = [
    ("CV1C",   "गमादि",    "gamādi",   "2",   819, 37.78, 37.78),
    ("CCV1C",  "स्मरादि",   "smarādi",  "2½",  209,  9.64, 47.42),
    ("CV1CC",  "कल्पादि",   "kalpādi",  "2½",  203,  9.36, 56.78),
    ("CV2CV1", "बाध्रादि",  "bādhrādi", "4",   105,  4.84, 61.62),
    ("CV2C",   "वाचादि",    "vācādi",   "3",   101,  4.66, 66.28),
    ("CV2",    "धादि",      "dhādi",    "2½",   88,  4.06, 70.34),
    ("V1C",    "इषादि",     "iṣādi",    "1½",   65,  3.00, 73.34),
    ("CV1",    "क्रादि",    "krādi",    "1½",   65,  3.00, 76.34),
    ("CV1CV2", "चित्यादि",  "cityādi",  "4",    58,  2.68, 79.01),
    ("CCV2",   "स्थादि",    "sthādi",   "3",    49,  2.26, 81.27),
    # 11th bar — the long tail: 59 racanāḥ outside the top 10.
    # 2,168 − 1,762 (top-10 sum) = 406 dhātavaḥ; mātrā values span 1 to 9.
    ("(tail)", "",         "59 other racanāḥ", "1 to 9", 406, 18.73, 100.00),
]


def main():
    fig, ax = setup(figsize=(12, 9.8))

    counts = [t[4] for t in TEMPLATES]
    pcts = [t[5] for t in TEMPLATES]

    y_positions = list(range(len(TEMPLATES)))
    bars = ax.barh(
        y_positions, counts,
        color=ACCENT, edgecolor="black", linewidth=0.5,
        height=0.95,  # bars ~1.3x thicker than the previous 0.86 (combined with the taller figsize)
        clip_on=False,
    )
    bars[0].set_color(FILL)
    bars[-1].set_hatch("///")
    bars[-1].set_edgecolor("#555555")

    ax.set_yticks(y_positions)
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()

    # Y-axis icons (replace tick labels) — gray, ~70% of the prior size
    for i, t in enumerate(TEMPLATES):
        template = t[0]
        if template == "(tail)":
            ax.text(
                -0.012, i, "tail",
                ha="right", va="center",
                fontsize=15, color="#888888",
                style="italic",
                transform=ax.get_yaxis_transform(),
                clip_on=False,
            )
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

    # Per-bar callouts: count(%) and structural · Devanāgarī (IAST) · mātrā
    COUNT_TEXT_X_OFFSET = 12
    RACANA_TEXT_X_OFFSET = 160
    for i, (bar, count, pct, t) in enumerate(zip(bars, counts, pcts, TEMPLATES)):
        template, deva, iast, matra, _c, _p, _cum = t
        if deva:
            rachana_text = f"{template}  ·  {deva} ({iast})  ·  {matra} mātrā"
        else:
            rachana_text = f"{iast}  ·  {matra} mātrā"
        count_text = f"{count} ({pct:.2f}%)"
        y_center = bar.get_y() + bar.get_height() / 2

        if i == 0:
            ax.text(
                count / 2, y_center, rachana_text,
                ha="center", va="center",
                fontsize=18, color="white",
            )
            ax.text(
                count + COUNT_TEXT_X_OFFSET, y_center, count_text,
                ha="left", va="center", fontsize=15,
            )
        else:
            ax.text(
                count + COUNT_TEXT_X_OFFSET, y_center, count_text,
                ha="left", va="center", fontsize=15,
            )
            ax.text(
                count + RACANA_TEXT_X_OFFSET, y_center, rachana_text,
                ha="left", va="center", fontsize=16,
            )

    ax.set_xlabel("Count in the Dhātupāṭha", fontsize=17)
    ax.set_ylabel("")
    ax.tick_params(axis="x", labelsize=14)
    ax.set_xlim(0, 850)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.xaxis.set_ticks_position("bottom")

    plt.subplots_adjust(left=0.10, right=0.97, top=0.97, bottom=0.08)
    savefig("building_dhatuh_top_ten_racanas")


if __name__ == "__main__":
    main()
