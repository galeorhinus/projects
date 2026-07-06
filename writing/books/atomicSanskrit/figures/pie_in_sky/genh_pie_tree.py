#!/usr/bin/env python3
"""Figure A — the pyramid's own tree, simplified (the PIE fraud exhibit).

A cleaned-down rendering of the popular *ǵenh₁ etymological tree
(after the widely-shared Starkey Comics chart): the starred phantom at
the root, three real branch-heads, a few leaves each — and no Sanskrit
anywhere on the page. Dashed = reconstructed, never attested. The figure
reproduces the pyramid's account faithfully; the caption does the work.

Word data (all from the pyramid's own chart / standard dictionaries):
  root   : *ǵenh₁ "to give birth"           [reconstructed — dashed]
  Latin  : genus "stock, race"; (g)nātus "born"
           → nation, nature, native, gender
  Greek  : génos "stock, race"; génesis
           → genesis, gene
  PGmc   : *kunją [reconstructed — dashed]
           → kind, kin, king, kindergarten
  Celtic : Cóemgen → Kevin  (the smile)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.style import setup, FILL, ACCENT, EDGE  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parent


def box(ax, x, y, text, sub=None, dashed=False, w=1.30, h=0.42, fs=8.0):
    style = dict(boxstyle="round,pad=0.06", linewidth=0.8,
                 edgecolor=EDGE, facecolor="white")
    if dashed:
        style.update(linestyle=(0, (3, 2)), facecolor="#f2f2f2")
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, **style))
    if sub:
        ax.text(x, y + 0.075, text, ha="center", va="center",
                fontsize=fs, style="italic", color=FILL)
        ax.text(x, y - 0.115, sub, ha="center", va="center",
                fontsize=fs - 1.6, color=ACCENT)
    else:
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fs, style="italic", color=FILL)


def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT,
                                linewidth=0.7, shrinkA=2, shrinkB=2))


def main():
    fig, ax = setup(figsize=(4.5, 3.3))
    ax.set_xlim(-4.0, 4.1)
    ax.set_ylim(-0.45, 4.0)
    ax.axis("off")

    # --- root: the phantom ---
    box(ax, 0.0, 0.25, "*ǵenh$_1$", sub="“to give birth”",
        dashed=True, w=1.55, h=0.55, fs=9.0)

    # --- branch-heads ---
    heads = [
        (-2.5, 1.55, "genus · (g)nātus", "Latin — “stock, race” · “born”", False),
        (0.0,  1.55, "génos", "Greek — “stock, race”", False),
        (2.5,  1.55, "*kunją", "Proto-Germanic", True),
    ]
    for x, y, t, s, d in heads:
        box(ax, x, y, t, sub=s, dashed=d, w=2.15, h=0.58)
        arrow(ax, 0.0, 0.55, x, y - 0.30)

    # --- leaves (plain text, like the popular chart's outer ring) ---
    leaves = {
        -2.5: ["nation", "nature", "native"],
        0.0:  ["genesis", "gene"],
        2.5:  ["kind", "king", "kindergarten"],
    }
    for hx, words in leaves.items():
        n = len(words)
        for i, w_ in enumerate(words):
            lx = hx + (i - (n - 1) / 2) * 1.05
            ly = 2.95
            ax.text(lx, ly, w_, ha="center", va="center", fontsize=7.6,
                    style="italic", color=FILL)
            arrow(ax, hx, 1.87, lx, ly - 0.16)

    # --- legend ---
    ax.text(-3.9, 3.75, "dashed = reconstructed; never spoken, never attested",
            fontsize=6.8, color=ACCENT, ha="left", va="center")
    ax.text(-3.9, 3.48, "after the popular etymological tree of *ǵenh$_1$ — "
            "no Sanskrit appears on it",
            fontsize=6.8, color=ACCENT, ha="left", va="center")

    for name in ("genh_pie_tree.from-py.svg", "genh_pie_tree.svg"):
        fig.savefig(OUT / name, bbox_inches="tight")
    print("wrote", OUT / "genh_pie_tree.svg")


if __name__ == "__main__":
    main()
