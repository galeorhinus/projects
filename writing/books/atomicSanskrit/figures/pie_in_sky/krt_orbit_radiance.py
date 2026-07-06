#!/usr/bin/env python3
"""Figure B' — the Sun restored: ⟪कृत्⟫, its orbits, and the radiance.

Center: the dhātu ⟪कृत्⟫ (Dhātupāṭha 6.171, tudādi, kṛtī छेदने — "to cut";
present kṛntati; the t is root-final — no "extension" needed).
Inner orbit: Sanskrit śabdas. Middle orbit: living Indic cutting-words
(roman + language tag; native scripts in the hand-edit pass).
Beyond the field boundary: three rays land on the receiving surfaces and
sprout small trees. The s rides only on rays seeded from s+k word
boundaries (saṃ-s-kṛta, namas-kāra, duṣ-kṛta) — the mis-cut bīja.

Orbit word-sets (prune freely):
  inner  : kṛtta कृत्त (cut off) · kartana कर्तनम् (cutting) ·
           kartarī कर्तरी (scissors) · kṛntati कृन्तति (cuts)
  middle : Hindi kāṭnā · Marathi kātarṇe · Bengali kāṭā · Punjabi kaṭṇā ·
           Kannada kattari · Telugu kattera        [VERIFY vs Turner CDIAL]
  rays   : Latin curtus (no s)   → curt, cortex    [kṛtta ↔ curtus]
           PGmc *skurtaz (s + t) → short, shirt, skirt
           PGmc *skeraną (s)     → shear, share, score
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
    ax.text(bx, by, head, ha="center", va="center", fontsize=7.6,
            style="italic", color=FILL,
            bbox=dict(boxstyle="round,pad=0.18",
                      facecolor="#f2f2f2" if dashed_head else "white",
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
    ax.set_ylim(-2.95, 2.34)
    ax.set_aspect("equal")
    ax.axis("off")

    # --- Sun ---
    ax.add_patch(Circle(SUN, 0.40, facecolor="white", edgecolor=EDGE, linewidth=1.1))
    for deg in range(0, 360, 30):
        a = radians(deg)
        ax.plot([SUN[0] + 0.43 * cos(a), SUN[0] + 0.52 * cos(a)],
                [SUN[1] + 0.43 * sin(a), SUN[1] + 0.52 * sin(a)],
                color=EDGE, linewidth=0.7)
    # NOTE: ⟪ ⟫ dhātu marker absent from figure fonts; add in hand-edit pass
    ax.text(SUN[0], SUN[1] + 0.11, "कृत्", ha="center", va="center",
            fontsize=12, color=FILL, fontweight="bold")
    ax.text(SUN[0], SUN[1] - 0.16, "kṛt", ha="center", va="center",
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
        (90, "कृत्त kṛtta"), (162, "कर्तनम् kartana"), (230, "कर्तरी kartarī"),
        (290, "कृन्तति kṛntati"),
    ], fs=6.6)

    # --- middle orbit: living Indic cutting-words ---
    orbit_words(ax, R_MIDDLE, [
        (105, "kāṭnā · Hindi"), (150, "kātarṇe · Marathi"), (198, "kāṭā · Bengali"),
        (255, "kaṭṇā · Punjabi"), (305, "kattari · Kannada"), (55, "kattera · Telugu"),
    ], fs=5.9)

    # --- three rays + sprouting trees ---
    targets = [
        (1.72, 1.35, "curtus", "Latin · kṛtta = curtus",
         ["curt", "cortex"], False, 0.72),
        (1.72, 0.0, "*skurtaz", "PGmc · s + t",
         ["short", "shirt", "skirt"], True, 0.85),
        (1.72, -1.35, "*skeraną", "PGmc · s, no t",
         ["shear", "share", "score"], True, 0.88),
    ]
    for tx, ty, head, sub, leaves, dashed, ldx in targets:
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
    # --- the mis-cut device (schematic): the word before donates its s ---
    # NOTE: lexical s+k flagships (namaskāra, saṃskṛtam) are kṛ-family and live
    # in the Recipe prose, where the kṛ/kṛt distinction is stated; the figure
    # shows the mechanism on this atom schematically.
    ax.text(-0.55, -2.30, "the s rides in from the word before:",
            fontsize=6.2, color=ACCENT, ha="center", style="italic")
    ax.text(-0.55, -2.52, "…s | kṛt-…        (the boundary)",
            fontsize=6.6, color=FILL, ha="center")
    ax.text(-0.55, -2.74, "heard as   … | skṛt-…   --   the seed keeps the s",
            fontsize=6.2, color=ACCENT, ha="center", style="italic")
    ax.text(2.45, -2.52, "the t was always in the atom",
            fontsize=6.4, color=ACCENT, ha="center", style="italic")

    for name in ("krt_orbit_radiance.from-py.svg", "krt_orbit_radiance.svg"):
        fig.savefig(OUT / name, bbox_inches="tight")
    print("wrote", OUT / "krt_orbit_radiance.svg")


if __name__ == "__main__":
    main()
