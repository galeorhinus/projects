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

# Make figures/_shared/style.py importable from this subdirectory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
from _shared.style import setup, savefig, FILL, ACCENT


# (label, count, role) — role drives bar shading.
# Source: analysis/dhatupatha/data/derived/matra_distribution.csv
# Refreshed after the Pāṇinian-1.3.2 strict anubandha-stripping correction.
# The earlier "disyllabic" secondary peak at 4 mātrā (188 / 8.7%) was an
# artifact of misclassifying anunāsika-vowel-tailed roots (the bādhṛ /
# gādhṛ family) as CV2CV1; those are now correctly 3-mātrā CV2C, and the
# 4-mātrā bucket is residual.
MATRA_COUNTS = [
    ("1",    7,   "floor"),    # 0.5 mātrā (2) + 1.0 mātrā (5) aggregated
    ("1½", 134,   "low"),
    ("2",  998,   "modal"),
    ("2½", 566,   "high"),
    ("3",  323,   "common"),
    ("3½",  94,   "tail"),
    ("4",   21,   "tail"),
    ("4½",  12,   "tail"),
    ("5+",  13,   "cliff"),    # 5.0 (9) + 5.5 (2) + 6.0 (2) aggregated
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

    # Peak annotation — vertical arrow above the 2-mātrā bar.
    # Label matches the chapter's primary phrasing ("2-mātrā envelope", §10.5).
    ax.annotate(
        "2-mātrā envelope",
        xy=(2, 998),
        xytext=(2.5, 1140),
        fontsize=7.5,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=0.6),
    )

    # NOTE: The earlier annotation marking a "disyllabic family peak" at 4 mātrā
    # was removed after the Pāṇinian-1.3.2 anubandha-stripping correction. The
    # bādhṛ / gādhṛ family that produced the apparent secondary peak is now
    # correctly classified as 3-mātrā CV2C, and the 4-mātrā bucket is residual
    # (21 entries, 1.0%) — no peak to annotate.

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
    ax.set_ylim(0, 1200)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    plt.tight_layout()
    savefig("building_dhatuh_matra_distribution")


if __name__ == "__main__":
    main()
