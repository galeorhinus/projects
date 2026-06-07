#!/usr/bin/env python3
"""
fig_periodic_table.py — Mendeleev-style periodic table of dhātus.

Each dhātu is positioned by its (varga column, inherent vowel) cell.
Axes:
  X — varga column (C1 unvoiced-unaspirate → C5 nasal, plus non-varga
      semivowel / sibilant / glottal / vowel-initial)
  Y — inherent vowel (a / ā / i / ī / u / ū / ṛ / ṝ / e / ai / o / au)

Marker size and color encode reactivity tier (Path C valency):
  Polyvalent (≥ 50)   — dark FILL, large
  Bivalent (5 – 49)   — ACCENT gray, medium
  Monovalent (1 – 4)  — light gray, small

The canonical-9 (kṛ, bhū, sthā, gam, jñā, dā, dhā, nī, hṛ) are labeled
in bold. All other polyvalent dhātus are labeled in regular weight.
Source: analysis/ganah/data/derived/column_axes_per_root.csv (3,839
corpus-attested dhātus).
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
import matplotlib.pyplot as plt
from _shared.style import setup, savefig, FILL, ACCENT

matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["pdf.fonttype"] = 42


CSV_IN = (Path(__file__).resolve().parent.parent.parent /
          "analysis" / "ganah" / "data" / "derived" /
          "column_axes_per_root.csv")

# Varga column labels in display order (left → right)
VARGA_ORDER = [
    "C1 (unvoiced unaspirate)",
    "C2 (unvoiced aspirate)",
    "C3 (voiced unaspirate)",
    "C4 (voiced aspirate)",
    "C5 (nasal)",
    "non-varga (semivowel)",
    "non-varga (sibilant)",
    "non-varga (glottal)",
    "non-varga (vowel-initial)",
]
VARGA_SHORT = ["C1", "C2", "C3", "C4", "C5", "semi-\nvowel", "sibi-\nlant", "h", "vowel-\ninitial"]
VARGA_X = {name: i for i, name in enumerate(VARGA_ORDER)}

# Vowel rows top → bottom
VOWEL_ORDER = ["a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "e", "ai", "o", "au"]
VOWEL_Y = {v: i for i, v in enumerate(VOWEL_ORDER)}

CANONICAL_9 = {"kṛ", "bhū", "sthā", "gam", "jñā", "dā", "dhā", "nī", "hṛ"}

# Tier visual encoding
TIER_STYLE = {
    "polyvalent": {"color": FILL,    "size": 220, "edge": "#1a1a1a", "ew": 0.5, "alpha": 0.95, "zorder": 4},
    "bivalent":   {"color": ACCENT,  "size":  80, "edge": "#555555", "ew": 0.3, "alpha": 0.7,  "zorder": 3},
    "monovalent": {"color": "#dcdcdc","size":  14, "edge": "none",   "ew": 0,   "alpha": 0.5,  "zorder": 2},
}


def tier_of(v: int) -> str:
    if v >= 50:
        return "polyvalent"
    if v >= 5:
        return "bivalent"
    return "monovalent"


def jitter(name: str, scale: float = 0.32) -> tuple[float, float]:
    """Deterministic jitter inside a cell from a hash of the root."""
    h = abs(hash(name))
    dx = ((h % 1000) / 1000 - 0.5) * scale
    dy = (((h // 1000) % 1000) / 1000 - 0.5) * scale
    return dx, dy


def main():
    rows = []
    with CSV_IN.open() as fh:
        for r in csv.DictReader(fh):
            v = int(r["valency"])
            vowel = r["vowel"]
            varga = r["varga_column"]
            if vowel not in VOWEL_Y or varga not in VARGA_X:
                continue
            rows.append({
                "root": r["root"],
                "valency": v,
                "tokens": int(r["tokens"]),
                "varga": varga,
                "vowel": vowel,
                "tier": tier_of(v),
            })

    fig, ax = setup(figsize=(11, 7.5))

    # Background cell grid
    for x in range(len(VARGA_ORDER)):
        for y in range(len(VOWEL_ORDER)):
            ax.add_patch(plt.Rectangle((x - 0.48, y - 0.48), 0.96, 0.96,
                                       facecolor="white",
                                       edgecolor="#e8e8e8", linewidth=0.5,
                                       zorder=1))

    # Highlight the "compact-vowel" reading region: a / ā / ṛ rows
    for vowel in ("a", "ā", "ṛ"):
        y = VOWEL_Y[vowel]
        ax.axhspan(y - 0.5, y + 0.5,
                   facecolor="#f7f3e8", alpha=0.5, zorder=0)

    # Plot dhātus, tier by tier (monovalent first so polyvalent ends on top)
    for tier_name in ("monovalent", "bivalent", "polyvalent"):
        xs, ys = [], []
        for d in rows:
            if d["tier"] != tier_name:
                continue
            jx, jy = jitter(d["root"])
            xs.append(VARGA_X[d["varga"]] + jx)
            ys.append(VOWEL_Y[d["vowel"]] + jy)
        st = TIER_STYLE[tier_name]
        ax.scatter(xs, ys, s=st["size"], color=st["color"],
                   edgecolor=st["edge"], linewidth=st["ew"],
                   alpha=st["alpha"], zorder=st["zorder"])

    # Labels: polyvalent dhātus
    for d in rows:
        if d["tier"] != "polyvalent":
            continue
        jx, jy = jitter(d["root"])
        x = VARGA_X[d["varga"]] + jx
        y = VOWEL_Y[d["vowel"]] + jy
        canonical = d["root"] in CANONICAL_9
        ax.annotate(
            d["root"],
            (x, y),
            xytext=(7 if canonical else 5, 0),
            textcoords="offset points",
            ha="left", va="center",
            fontsize=8.5 if canonical else 7,
            fontweight="bold" if canonical else "normal",
            color="#1a1a1a" if canonical else "#444",
            zorder=5,
        )

    # X-axis
    ax.set_xticks(range(len(VARGA_ORDER)))
    ax.set_xticklabels(VARGA_SHORT, fontsize=9)
    ax.set_xlim(-0.6, len(VARGA_ORDER) - 0.4)

    # Y-axis: invert so 'a' is at top
    ax.set_yticks(range(len(VOWEL_ORDER)))
    ax.set_yticklabels(VOWEL_ORDER, fontsize=10)
    ax.set_ylim(len(VOWEL_ORDER) - 0.5, -0.5)

    # Axis labels
    ax.set_xlabel("Varga column (initial consonant class)", fontsize=10, labelpad=10)
    ax.set_ylabel("Inherent vowel", fontsize=10, labelpad=8)

    # Title
    ax.set_title("Periodic table of dhātavaḥ — corpus-attested inventory positioned\n"
                 "by varga column × inherent vowel, sized by Path C reactivity",
                 fontsize=11, pad=14)

    # Legend
    legend_handles = []
    for tier_name, label in [("polyvalent", "Polyvalent (valency ≥ 50)"),
                             ("bivalent",   "Bivalent (5 – 49)"),
                             ("monovalent", "Monovalent (1 – 4)")]:
        st = TIER_STYLE[tier_name]
        legend_handles.append(
            plt.scatter([], [], s=st["size"], color=st["color"],
                        edgecolor=st["edge"], linewidth=st["ew"],
                        alpha=st["alpha"], label=label)
        )
    ax.legend(handles=legend_handles, loc="upper right",
              fontsize=8, frameon=True, framealpha=0.95,
              edgecolor="#bbb")

    # Spines: keep light
    for spine in ax.spines.values():
        spine.set_color("#888")
        spine.set_linewidth(0.6)
    ax.tick_params(colors="#444")

    # Footer note
    fig.text(0.02, 0.015,
             "Source: analysis/ganah (Path C, 3,839 corpus-attested dhātavaḥ); "
             "Canonical-9 (kṛ, bhū, sthā, gam, jñā, dā, dhā, nī, hṛ) in bold.",
             fontsize=7, color="#555", style="italic")

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    savefig("periodic_table", dir=Path(__file__).resolve().parent)


if __name__ == "__main__":
    main()
