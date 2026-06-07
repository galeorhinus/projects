#!/usr/bin/env python3
"""
fig_canonical_rank_trajectory.py — Visualizes the canonical-9 polyvalent
core's rank across DCS sub-corpora to land the empirical invariance claim.

Y-axis: rank by verb-token count within each sub-corpus (inverted so #1
sits at the top). X-axis: sub-corpora ordered by total verb tokens, with
the small *Aṣṭāvakragīta* sample at the right as a tight stress test.

One line per canonical dhātu (kṛ, bhū, sthā, gam, jñā, dā, dhā, nī, hṛ).
A flat line near the top = the dhātu stays in the top-N across the corpus
shift. A diving line = the dhātu drops out of the top in that corpus.

Source: analysis/ganah/data/derived/per_corpus_productivity.csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

# Make figures/_shared/style.py importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
import matplotlib.pyplot as plt
from _shared.style import setup, savefig, FILL, ACCENT

matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["pdf.fonttype"] = 42


CSV_IN = (Path(__file__).resolve().parent.parent.parent /
          "analysis" / "ganah" / "data" / "derived" /
          "per_corpus_productivity.csv")

CANONICAL = ["kṛ", "bhū", "sthā", "gam", "jñā", "dā", "dhā", "nī", "hṛ"]

# Order sub-corpora left-to-right; place AṣG last as the small-sample stress.
CORPUS_ORDER = [
    "Ṛgveda",
    "Atharvaveda (Śaunaka)",
    "Mahābhārata",
    "Rāmāyaṇa",
    "Aṣṭāvakragīta",
]

CORPUS_LABEL_OVERRIDE = {
    "Atharvaveda (Śaunaka)": "Atharvaveda",
    "Aṣṭāvakragīta": "Aṣṭāvakragītā",
}


def load_ranks():
    """Return {root: {corpus: rank}} from the per-corpus CSV."""
    ranks = {root: {} for root in CANONICAL}
    with CSV_IN.open() as fh:
        for row in csv.DictReader(fh):
            corpus = row["corpus"]
            root = row["root"]
            if root in CANONICAL and corpus in CORPUS_ORDER:
                ranks[root][corpus] = int(row["rank"])
    return ranks


def main():
    ranks = load_ranks()

    fig, ax = setup(figsize=(8.5, 5.2))

    # X-axis: integer positions for each corpus
    x = list(range(len(CORPUS_ORDER)))
    x_labels = [CORPUS_LABEL_OVERRIDE.get(c, c) for c in CORPUS_ORDER]

    # Color cycle that prints cleanly in monochrome — vary line style instead
    line_styles = ["-", "--", "-.", ":"]
    markers = ["o", "s", "D", "^", "v", "P", "X", "*", "h"]

    for i, root in enumerate(CANONICAL):
        ys = []
        for c in CORPUS_ORDER:
            r = ranks[root].get(c)
            ys.append(r if r is not None else None)

        # Split into segments at None (root not in top-50 of that corpus)
        xs_drawn = [x[j] for j in range(len(ys)) if ys[j] is not None]
        ys_drawn = [ys[j] for j in range(len(ys)) if ys[j] is not None]

        ls = line_styles[i % len(line_styles)]
        marker = markers[i % len(markers)]

        ax.plot(xs_drawn, ys_drawn,
                linestyle=ls, marker=marker, markersize=7,
                color=FILL if root == "kṛ" else ACCENT,
                linewidth=1.4 if root == "kṛ" else 1.1,
                alpha=0.85, label=root,
                zorder=3 if root == "kṛ" else 2)

        # Label the line at the rightmost data point
        if xs_drawn:
            ax.annotate(root,
                        xy=(xs_drawn[-1], ys_drawn[-1]),
                        xytext=(xs_drawn[-1] + 0.12, ys_drawn[-1]),
                        fontsize=9, va="center",
                        fontweight="bold" if root == "kṛ" else "normal")

    # Y-axis: ranks 1–50, inverted so #1 is at top
    ax.set_yscale("log")
    ax.set_yticks([1, 2, 3, 5, 10, 20, 50, 100])
    ax.set_yticklabels(["1", "2", "3", "5", "10", "20", "50", "100"])
    ax.set_ylim(120, 0.8)   # inverted; rank 1 at top
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=10)
    ax.set_xlim(-0.3, len(x) - 0.4)
    ax.set_ylabel("Rank by verb-token count (within sub-corpus)", fontsize=10)

    # Reference band at top — "top 10" zone
    ax.axhspan(0.8, 10.5, color="#f0f0f0", zorder=1)
    ax.text(len(x) - 0.55, 1.2, "top 10",
            fontsize=8, va="center", ha="right", color="#666", style="italic")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", which="major", alpha=0.25, linewidth=0.3)

    ax.set_title("Canonical-9 dhātu rank across DCS sub-corpora",
                 fontsize=11, pad=12)

    plt.tight_layout()
    savefig("ganah_canonical_rank_trajectory")


if __name__ == "__main__":
    main()
