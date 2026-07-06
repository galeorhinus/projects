#!/usr/bin/env python3
"""Figure A' — the pyramid's *(s)ker- tree, simplified (the kṛt fraud exhibit).

After the popular "Etymological Tree of Sker" chart: PIE *(s)ker- "to cut"
at the root — with TWO confessed devices in the notation itself:
  (s) — the "s-mobile": a consonant with no source, no rule, no meaning;
  -t- — the "root extension": appended where daughters demand it,
        meaningless by the pyramid's own handbooks.
No Sanskrit appears on the chart. The hidden atom is ⟪कृत्⟫ (kṛtī chedane,
Dhātupāṭha tudādi 6.171, "to cut") — the t is root-final; the s is the
mis-cut word boundary (saṃ-s-kṛta, namas-kāra, duṣ-kṛta).

Word data (from the pyramid's own chart / standard dictionaries):
  root     : *(s)ker- "to cut"                 [dashed]
  Latin    : curtus "short" (no s; t present)  → curt, cortex
  PGmc t   : *skurtaz "short" (s + t)          → short, shirt, skirt
  PGmc     : *skeraną "to shear" (s, no t)     → shear, share, score
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
    ax.set_ylim(-0.45, 4.35)
    ax.axis("off")

    # --- root: the phantom, with both devices in the notation ---
    box(ax, 0.0, 0.25, "*(s)ker-", sub="“to cut”",
        dashed=True, w=1.55, h=0.55, fs=9.0)

    # --- branch-heads ---
    heads = [
        (-2.6, 1.55, "curtus", "Latin — “short” · no s", False),
        (0.0,  1.55, "*skurtaz", "Proto-Germanic — s + t", True),
        (2.6,  1.55, "*skeraną", "Proto-Germanic — s, no t", True),
    ]
    for x, y, t, s, d in heads:
        box(ax, x, y, t, sub=s, dashed=d, w=2.15, h=0.58)
        arrow(ax, 0.0, 0.55, x, y - 0.30)

    # --- leaves (plain text, like the popular chart's outer ring) ---
    leaves = {
        -2.6: ["curt", "cortex"],
        0.0:  ["short", "shirt", "skirt"],
        2.6:  ["shear", "share", "score"],
    }
    for hx, words in leaves.items():
        n = len(words)
        for i, w_ in enumerate(words):
            lx = hx + (i - (n - 1) / 2) * 0.92
            ly = 2.95
            ax.text(lx, ly, w_, ha="center", va="center", fontsize=7.6,
                    style="italic", color=FILL)
            arrow(ax, hx, 1.87, lx, ly - 0.16)

    # --- legend: the confessions ---
    ax.text(-3.9, 4.12, "( ) = the “s-mobile”: a consonant with no source, "
            "no rule, no meaning",
            fontsize=6.6, color=ACCENT, ha="left", va="center")
    ax.text(-3.9, 3.86, "t = a “root extension”: appended where needed; "
            "meaningless by their own account",
            fontsize=6.6, color=ACCENT, ha="left", va="center")
    ax.text(-3.9, 3.60, "dashed = reconstructed; never spoken, never attested "
            "— and no Sanskrit appears on it",
            fontsize=6.6, color=ACCENT, ha="left", va="center")

    # emits ONLY the .from-py.svg staging file; the working .svg is the
    # promoted CD final and must never be overwritten by regeneration.
    fig.savefig(OUT / "sker_pie_tree.from-py.svg", bbox_inches="tight")
    print("wrote", OUT / "sker_pie_tree.from-py.svg")


if __name__ == "__main__":
    main()
