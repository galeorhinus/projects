#!/usr/bin/env python3
"""Figure B — the Sun restored: ⟪जन्⟫, its orbits, and the radiance.

Center: the dhātu ⟪जन्⟫ (Dhātupāṭha 3.25 janane "to create, procreate";
4.44 prādurbhāve "to be born, come into existence").
Inner orbit: Sanskrit śabdas. Middle orbit: living Indic forms (roman +
language tag; native scripts can be added in the hand-edit pass).
Beyond the field boundary: three rays land on three receiving surfaces
(Latin, Greek, Proto-Germanic) and a small tree sprouts at each landing
point — botany begins exactly where the radiance lands, never at the center.

Orbit word-sets (prune freely):
  inner  : janma जन्म · jāti जाति · jāta जात · jana जन · jananī जननी · prajā प्रजा
  middle : Hindi janam · Marathi janma · Bengali jônmo · Punjabi janam ·
           Telugu janma · Malayalam janmam
  rays   : Latin genus → nation, nature, native, gender
           Greek génos → genesis, gene
           PGmc *kunją → kind, king, kindergarten
"""
import sys
from math import cos, sin, radians
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.style import setup, FILL, ACCENT, EDGE  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

OUT = Path(__file__).resolve().parent

SUN = (-1.55, 0.0)
R_INNER, R_MIDDLE, R_FIELD = 0.94, 1.52, 1.95


def orbit_words(ax, radius, entries, fs, style_italic=True, dy=0.0):
    for angle, text in entries:
        a = radians(angle)
        x = SUN[0] + radius * cos(a)
        y = SUN[1] + radius * sin(a)
        ax.text(x, y + dy, text, ha="center", va="center", fontsize=fs,
                style="italic" if style_italic else "normal", color=FILL,
                bbox=dict(boxstyle="round,pad=0.13", facecolor="white",
                          edgecolor="none", alpha=0.9))


def tree(ax, bx, by, head, head_sub, leaves, dashed_head=False, leaf_dx=0.72):
    # trunk node
    ax.text(bx, by, head, ha="center", va="center", fontsize=7.6,
            style="italic", color=FILL,
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#f2f2f2" if dashed_head else "white",
                      edgecolor=EDGE, linewidth=0.7,
                      linestyle=(0, (3, 2)) if dashed_head else "solid"))
    ax.text(bx, by - 0.21, head_sub, ha="center", va="center",
            fontsize=5.8, color=ACCENT)
    n = len(leaves)
    for i, leaf in enumerate(leaves):
        lx = bx + leaf_dx
        ly = by + (i - (n - 1) / 2) * 0.27
        ax.annotate("", xy=(lx - 0.07, ly), xytext=(bx + leaf_dx - 0.25, by + 0.02),
                    arrowprops=dict(arrowstyle="-", color=ACCENT, linewidth=0.6,
                                    connectionstyle="arc3,rad=0.15"))
        ax.text(lx, ly, leaf, ha="left", va="center", fontsize=6.6, color=FILL)


def main():
    fig, ax = setup(figsize=(4.5, 3.4))
    ax.set_xlim(-3.55, 3.55)
    ax.set_ylim(-2.28, 2.34)
    ax.set_aspect("equal")
    ax.axis("off")

    # --- Sun ---
    ax.add_patch(Circle(SUN, 0.40, facecolor="white", edgecolor=EDGE, linewidth=1.1))
    for deg in range(0, 360, 30):
        a = radians(deg)
        ax.plot([SUN[0] + 0.43 * cos(a), SUN[0] + 0.52 * cos(a)],
                [SUN[1] + 0.43 * sin(a), SUN[1] + 0.52 * sin(a)],
                color=EDGE, linewidth=0.7)
    # NOTE: the ⟪ ⟫ dhātu marker is absent from the figure fonts; add in hand-edit pass if wanted
    ax.text(SUN[0], SUN[1] + 0.11, "जन्", ha="center", va="center",
            fontsize=12, color=FILL, fontweight="bold")
    ax.text(SUN[0], SUN[1] - 0.16, "jan", ha="center", va="center",
            fontsize=6.4, style="italic", color=ACCENT)

    # --- orbit rings + field boundary ---
    for r in (R_INNER, R_MIDDLE):
        ax.add_patch(Circle(SUN, r, fill=False, edgecolor=ACCENT, linewidth=0.6))
    ax.add_patch(Circle(SUN, R_FIELD, fill=False, edgecolor=ACCENT,
                        linewidth=0.7, linestyle=(0, (4, 3))))
    ax.text(SUN[0], SUN[1] + R_FIELD + 0.12, "Sanskritic gravity",
            ha="center", va="bottom", fontsize=6.4, color=ACCENT)

    # --- inner orbit: Sanskrit śabdas ---
    orbit_words(ax, R_INNER, [
        (90, "जन्म janma"), (162, "जाति jāti"), (230, "जन jana"),
        (270, "जननी jananī"), (322, "जात jāta"), (45, "प्रजा prajā"),
    ], fs=6.6)

    # --- middle orbit: living Indic forms (roman; native scripts in hand-edit) ---
    orbit_words(ax, R_MIDDLE, [
        (105, "janam · Hindi"), (150, "janma · Marathi"), (198, "jônmo · Bengali"),
        (255, "janam · Punjabi"), (305, "janma · Telugu"), (55, "janmam · Malayalam"),
    ], fs=5.9)

    # --- three rays + sprouting trees ---
    targets = [
        (1.72, 1.35, "genus · (g)nātus", "Latin",
         ["nation", "nature", "native", "gender"], False, 1.15),
        (1.72, 0.0, "génos", "Greek", ["genesis", "gene"], False, 0.70),
        (1.72, -1.35, "*kunją", "Proto-Germanic",
         ["kind", "king", "kindergarten"], True, 0.85),
    ]
    for tx, ty, head, sub, leaves, dashed, ldx in targets:
        # ray from sun edge to just short of the tree head
        dx, dy_ = tx - SUN[0], ty - SUN[1]
        L = (dx ** 2 + dy_ ** 2) ** 0.5
        ux, uy = dx / L, dy_ / L
        x0, y0 = SUN[0] + 0.55 * ux, SUN[1] + 0.55 * uy
        x1, y1 = tx - 0.62 * ux, ty - 0.62 * uy
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, linewidth=0.9,
                                    linestyle=(0, (5, 3))))
        tree(ax, tx, ty, head, sub, leaves, dashed_head=dashed, leaf_dx=ldx)

    # --- zone labels ---
    ax.text(0.55, 2.02, "radiance", fontsize=6.4, color=ACCENT,
            ha="center", style="italic")
    ax.text(2.45, -2.16, "trees grow where the light lands",
            fontsize=6.4, color=ACCENT, ha="center", style="italic")

    for name in ("jan_orbit_radiance.from-py.svg", "jan_orbit_radiance.svg"):
        fig.savefig(OUT / name, bbox_inches="tight")
    print("wrote", OUT / "jan_orbit_radiance.svg")


if __name__ == "__main__":
    main()
