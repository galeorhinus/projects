"""Sonomer-count distribution across the 2,168 dhātavaḥ (Ch 10 §10.7).

Bar chart of the sonomer-count distribution: how many dhātavaḥ (धातवः)
occupy 1, 2, 3, 4, 5, and 6+ sonomers. The 1-sonomer floor is Sanskrit's
hydrogen class (V-pattern: √i, √ī, √u, √ṛ, √ṝ — 5 atoms across 7 entries).
The five-sonomer threshold is the compression-principle prediction;
the modal three-sonomer bar is the inventory's center of gravity.

Data: Ch 10 §10.7 table (matches analysis/dhatupatha/ scripts).

Run: python3 figures/building_dhatuh/particle_count.py
"""

import sys
from pathlib import Path

# Make figures/_shared/style.py importable from this subdirectory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
from _shared.style import setup, savefig, FILL, ACCENT


# (label, count, role) — role drives bar shading.
# Source: analysis/dhatupatha/data/derived/template_distribution.csv
# (corrected per Yi-fix to the ñi initial anubandha — see commit 9455d07).
PARTICLE_COUNTS = [
    ("1",  7,    "floor"),
    ("2",  237,  "minimum"),
    ("3",  1052, "modal"),
    ("4",  681,  "high"),
    ("5",  157,  "threshold"),
    ("6+", 34,   "cliff"),
]


def main():
    fig, ax = setup(figsize=(4.8, 2.9))

    labels = [row[0] for row in PARTICLE_COUNTS]
    counts = [row[1] for row in PARTICLE_COUNTS]
    total = sum(counts)
    percents = [c / total * 100 for c in counts]

    # Modal bar gets FILL; everything else ACCENT.
    colors = [FILL if row[2] == "modal" else ACCENT for row in PARTICLE_COUNTS]

    bars = ax.bar(labels, counts, color=colors, edgecolor="black", linewidth=0.5)

    # Annotate each bar with count + percentage.
    for bar, count, pct in zip(bars, counts, percents):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 25,
            f"{count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=7.5,
            linespacing=1.1,
        )

    # Earlier versions of this figure carried two annotations — "structural
    # floor (hydrogen class)" on the 1-sonomer bar and "five-sonomer
    # threshold" on the 5-sonomer bar. Both were decorative: the §10.7
    # prose carries the audit signal directly (peak at 3 / heavy at 4 /
    # drop at 5 / cliff at 6+) and the bar counts read the same story.
    # Dropped to let the chart show the distribution without commentary
    # the text does not pick up.

    ax.set_xlabel("Sonomers per dhātuḥ (धातुः)")
    ax.set_ylabel("Count")
    ax.set_ylim(0, 1250)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    plt.tight_layout()
    savefig("particle_count", dir=Path(__file__).resolve().parent)


if __name__ == "__main__":
    main()
