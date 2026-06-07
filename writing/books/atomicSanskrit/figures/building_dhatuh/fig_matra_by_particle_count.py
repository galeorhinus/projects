#!/usr/bin/env python3
"""
fig_matra_by_particle_count.py — Bubble plot of dhātus by (particle count, mātrā).

Each column is one particle-count bucket. Within a column, every distinct
mātrā value that appears is plotted as a bubble whose size scales with the
count of dhātus at that (particles, mātrā) cell. A faint vertical line spans
the column's mātrā range to make the spread visually explicit.

The point the figure carries: same particle budget can produce different
timing shapes. Mātrā is a second distinguishability axis on top of particle
count — that's why the architecture can fit 2,168 distinct semantic atoms
into ~10 dominant scaffolds without collision.

Source: analysis/dhatupatha/data/derived/matra_by_particle_count.csv
"""

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
import matplotlib.pyplot as plt
from _shared.style import setup, savefig, ACCENT, FILL


matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["pdf.fonttype"] = 42


# (particles, mātrā, count) — from
# analysis/dhatupatha/data/derived/matra_by_particle_count.csv
DATA = [
    (1, 1.0,   5),
    (1, 2.0,   2),
    (2, 1.5, 130),
    (2, 2.5, 107),
    (3, 2.0, 884),
    (3, 3.0, 153),
    (3, 3.5,  12),
    (3, 4.5,   3),
    (4, 2.5, 413),
    (4, 3.0,  31),
    (4, 3.5,  47),
    (4, 4.0, 174),
    (4, 5.0,  16),
    (5, 3.0,  47),
    (5, 3.5,  20),
    (5, 4.0,   8),
    (5, 4.5,  76),
    (5, 5.5,   3),
    (5, 6.0,   3),
    (6, 3.5,   1),
    (6, 4.0,   6),
    (6, 4.5,   3),
    (6, 5.0,  10),
    (6, 5.5,   3),
    (6, 6.0,   1),
    (6, 6.5,   1),
    (6, 7.5,   1),
    (7, 4.5,   2),
    (7, 5.0,   1),
    (7, 5.5,   1),
    (7, 6.0,   2),
    (7, 7.0,   1),
    (9, 9.0,   1),
]


def main():
    fig, ax = setup(figsize=(8, 5.2))

    # Organize by particle count.
    by_particles = defaultdict(dict)   # p -> {m: count}
    for (p, m, c) in DATA:
        by_particles[p][m] = c

    all_particles = sorted(by_particles.keys())

    # Draw faint vertical spread line per particle count.
    for p in all_particles:
        ms = sorted(by_particles[p].keys())
        if len(ms) > 1:
            ax.plot([p, p], [min(ms), max(ms)],
                    color="#cccccc", linewidth=1.0, zorder=1)

    # Bubbles.
    max_count = max(c for _, _, c in DATA)
    for (p, m, c) in DATA:
        # sqrt-style scaling so the 884 bubble doesn't drown out the 3-count ones
        size = (c ** 0.62) * 14
        is_big = c >= 100
        ax.scatter(p, m, s=size,
                   alpha=0.85, color=FILL if is_big else ACCENT,
                   edgecolor="#1a1a1a", linewidth=0.6, zorder=2)
        # Count labels for medium and large bubbles
        if c >= 100:
            ax.annotate(str(c), (p, m), fontsize=9,
                        ha="center", va="center",
                        color="white", fontweight="bold", zorder=3)
        elif c >= 25:
            ax.annotate(str(c), (p, m), fontsize=7.5,
                        ha="center", va="center", zorder=3)

    # Spread annotations along the top — "n mātrā spread" for each particle count.
    annot_y = 9.55
    for p in all_particles:
        ms = list(by_particles[p].keys())
        n_buckets = len(ms)
        if n_buckets >= 2:
            span = max(ms) - min(ms)
            ax.text(p, annot_y,
                    f"{n_buckets} buckets\n{span:.1f} mātrā",
                    ha="center", va="bottom", fontsize=7,
                    color="#444", linespacing=1.15)

    ax.set_xlabel("Particle count")
    ax.set_ylabel("Mātrā  (½ · C + 1 · V1 + 2 · V2)")
    ax.set_xticks(all_particles)
    ax.set_xlim(0.4, 9.6)

    # Half-mātrā ticks across the observed range
    y_ticks = [0.5 * i for i in range(2, 19)]   # 1.0 … 9.0
    ax.set_yticks(y_ticks)
    ax.set_ylim(0.7, 10.7)

    ax.grid(True, axis="y", alpha=0.25, linewidth=0.3, zorder=0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    plt.tight_layout()
    savefig("building_dhatuh_matra_by_particle_count")


if __name__ == "__main__":
    main()
