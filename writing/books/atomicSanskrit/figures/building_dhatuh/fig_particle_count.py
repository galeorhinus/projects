"""Particle-count distribution across the 2,168 dhātavaḥ (Ch 11 §11.6).

Bar chart of the particle-count distribution: how many dhātavaḥ (धातवः)
occupy 1, 2, 3, 4, 5, and 6+ particles. The 1-particle floor is Sanskrit's
hydrogen class (V-pattern: √i, √ī, √u, √ṛ, √ṝ — 5 atoms across 7 entries).
The five-particle threshold is the compression-principle prediction;
the modal three-particle bar is the inventory's center of gravity.

Data: Ch 11 §11.6 table (matches analysis/dhatupatha/ scripts).

Run: python3 figures/building_dhatuh/fig_particle_count.py
"""

import sys
from pathlib import Path

# Make figures/style.py importable from this subdirectory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
from style import setup, savefig, FILL, ACCENT


# (label, count, role) — role drives bar shading.
PARTICLE_COUNTS = [
    ("1",  7,    "floor"),
    ("2",  236,  "minimum"),
    ("3",  1051, "modal"),
    ("4",  676,  "high"),
    ("5",  156,  "threshold"),
    ("6+", 42,   "cliff"),
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

    # Floor annotation — entire arrow on the LEFT side of the 1-particle bar
    # so the arrowhead doesn't crash into the centered "7 (0.3%)" count label.
    ax.annotate(
        "structural floor\n(hydrogen class)",
        xy=(-0.35, 30),
        xytext=(-0.4, 380),
        fontsize=7.5,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=0.6),
    )

    # Threshold annotation — vertical arrow at the RIGHT edge of the 5-particle bar
    # so the arrowhead clears the centered "156 (7.2%)" count label.
    ax.annotate(
        "five-particle\nthreshold",
        xy=(4.4, 156),
        xytext=(4.4, 580),
        fontsize=7.5,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=0.6),
    )

    ax.set_xlabel("Particles per dhātuḥ (धातुः)")
    ax.set_ylabel("Count")
    ax.set_ylim(0, 1250)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    plt.tight_layout()
    savefig("building_dhatuh_particle_count")


if __name__ == "__main__":
    main()
