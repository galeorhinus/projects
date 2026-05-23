#!/usr/bin/env python3
"""
fig_matra_distribution.py — Bar chart of the mātrā-count distribution
of the Dhātupāṭha.

Companion to fig_particle_count.py. Same corpus (Dhātupāṭha 2,168 entries)
but aggregated by total mātrā (½·C + 1·V1 + 2·V2) rather than particle count.

Source: analysis/dhatupatha/data/derived/matra_distribution.csv
Run:    python3 figures/building_dhatuh/fig_matra_distribution.py
"""

import sys
from pathlib import Path

# Make figures/style.py importable from this subdirectory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
from style import setup, savefig, FILL, ACCENT


# (label, count, role) — role drives bar shading.
# Source: analysis/dhatupatha/data/derived/matra_distribution.csv
# (corrected per Yi-fix to the ñi initial anubandha — see commit 9455d07).
MATRA_COUNTS = [
    ("1",    5,   "floor"),
    ("1½", 130,   "low"),
    ("2",  886,   "modal"),
    ("2½", 520,   "high"),
    ("3",  231,   "common"),
    ("3½",  80,   "tail"),
    ("4",  188,   "disyllabic"),
    ("4½",  84,   "tail"),
    ("5+",  44,   "cliff"),
]


def main():
    fig, ax = setup(figsize=(5.6, 3.0))

    labels = [row[0] for row in MATRA_COUNTS]
    counts = [row[1] for row in MATRA_COUNTS]
    total = sum(counts)
    percents = [c / total * 100 for c in counts]

    # Modal bar gets FILL; everything else ACCENT.
    colors = [FILL if row[2] == "modal" else ACCENT for row in MATRA_COUNTS]

    bars = ax.bar(labels, counts, color=colors, edgecolor="black", linewidth=0.5)

    # Annotate each bar with count + percentage.
    for bar, count, pct in zip(bars, counts, percents):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 18,
            f"{count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=7,
            linespacing=1.1,
        )

    # Mode annotation — vertical arrow above the 2-mātrā bar
    ax.annotate(
        "modal envelope\n2 mātrās",
        xy=(2, 886),
        xytext=(2.5, 1030),
        fontsize=7.5,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=0.6),
    )

    # Disyllabic peak annotation — pointing to the 4-mātrā bar
    ax.annotate(
        "disyllabic\nfamily peak",
        xy=(6.4, 188),
        xytext=(7.0, 480),
        fontsize=7.5,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=0.6),
    )

    # Floor annotation — on the left of the 1-mātrā bar to avoid the count label.
    ax.annotate(
        "1-mātrā floor\n(bare-vowel\ndhātus)",
        xy=(-0.35, 30),
        xytext=(-0.4, 320),
        fontsize=7.5,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=0.6),
    )

    ax.set_xlabel("Total mātrās per dhātuḥ (धातुः)")
    ax.set_ylabel("Count")
    ax.set_ylim(0, 1080)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    plt.tight_layout()
    savefig("building_dhatuh_matra_distribution")


if __name__ == "__main__":
    main()
