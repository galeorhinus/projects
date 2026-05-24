#!/usr/bin/env python3
"""
fig_top_ten_racanas.py — Bar chart of the top 10 racanā templates in the
Dhātupāṭha (which together cover 81.27% of the 2,168-entry corpus).

X-axis: template shorthand (CV1C, CCV1C, ...).
Y-axis: count of dhātavaḥ in each template.
On top of each bar: count and corpus percent.
Callouts: each bar is annotated with an arrow pointing to a text showing
the racanā name (Devanagari + Roman) and its mātrā value.

Source: analysis/dhatupatha/data/derived/template_distribution.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
import matplotlib.pyplot as plt
from style import setup, savefig, FILL, ACCENT


# Preserve text as <text> elements in SVG so the renderer (browser / xelatex /
# rsvg) can apply proper Devanagari conjunct shaping at display time — matplotlib
# itself doesn't run an OpenType shaper, so baking glyphs into paths breaks
# conjuncts like ध्र, त्य, स्म.
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["pdf.fonttype"] = 42


# (template, devanagari, iast, mātrā, count, percentage, cumulative)
# Same ordering as the §10.6 table — descending count.
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
    # 11th bar — the long tail: the 59 racanāḥ outside the top 10.
    # 2,168 − 1,762 (top-10 sum) = 406 dhātavaḥ; mātrā values span 1 to 9.
    ("(tail)", "",         "59 other racanāḥ", "1 to 9", 406, 18.73, 100.00),
]


def main():
    fig, ax = setup(figsize=(9, 5.2))

    counts = [t[4] for t in TEMPLATES]
    pcts = [t[5] for t in TEMPLATES]
    template_labels = [t[0] for t in TEMPLATES]

    y_positions = list(range(len(TEMPLATES)))
    bars = ax.barh(y_positions, counts, color=ACCENT,
                   edgecolor="black", linewidth=0.5,
                   clip_on=False)
    bars[0].set_color(FILL)  # gamādi gets the dark FILL highlight
    # The last bar is the long-tail aggregate — hatch it to mark it as a
    # summary bar rather than a single named racanā.
    bars[-1].set_hatch("///")
    bars[-1].set_edgecolor("#555555")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(template_labels, fontsize=12)
    ax.invert_yaxis()  # put the longest bar (gamādi) at the top

    # Offsets within the data axis (xlim = 800).
    COUNT_TEXT_X_OFFSET  = 10
    RACANA_TEXT_X_OFFSET = 120

    for i, (bar, count, pct, t) in enumerate(zip(bars, counts, pcts, TEMPLATES)):
        template, deva, iast, matra, _c, _p, _cum = t
        # Use a non-breaking space + middle-dot separator pattern that
        # survives matplotlib's font-switching between Devanagari and Latin.
        if deva:
            rachana_text = f"{deva} ({iast}) · {matra} mātrā"
        else:
            rachana_text = f"{iast} · {matra} mātrā"
        count_text = f"{count} ({pct:.2f}%)"
        y_center = bar.get_y() + bar.get_height() / 2

        if i == 0:
            # gamādi (longest bar): rachana label INSIDE the bar, centered.
            ax.text(
                count / 2, y_center, rachana_text,
                ha="center", va="center",
                fontsize=11, color="white",
            )
            ax.text(
                count + COUNT_TEXT_X_OFFSET, y_center, count_text,
                ha="left", va="center", fontsize=10,
            )
        else:
            # Other bars: count/% just past bar end, rachana label further right.
            ax.text(
                count + COUNT_TEXT_X_OFFSET, y_center, count_text,
                ha="left", va="center", fontsize=10,
            )
            ax.text(
                count + RACANA_TEXT_X_OFFSET, y_center, rachana_text,
                ha="left", va="center", fontsize=11,
            )

    ax.set_xlabel("Count in the Dhātupāṭha", fontsize=11)
    ax.set_ylabel("Racanā template", fontsize=11)
    ax.tick_params(axis="x", labelsize=10)
    ax.set_xlim(0, 800)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    plt.tight_layout()
    savefig("building_dhatuh_top_ten_racanas")


if __name__ == "__main__":
    main()
