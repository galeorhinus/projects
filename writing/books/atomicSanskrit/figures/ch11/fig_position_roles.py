"""Inner vs outer position roles per consonant across single-akṣara dhātus.

For each of the 33 consonants in the varṇamālā, shows how its deployment
breaks down across the four position-roles:

  C₁ₒ — onset_outer (atom-start)
  C₁ᵢ — onset_inner (cluster-joiner before vowel)
  C₂ᵢ — coda_inner  (cluster-joiner after vowel)
  C₂ₒ — coda_outer  (atom-end)

Data: analysis/dhatupatha/ — single-akṣara atoms (~1,852 atoms),
classified via analyze_position_roles.py.

Run: python3 figures/ch11/fig_position_roles.py
"""

import sys
from collections import Counter, defaultdict
from pathlib import Path

# Make figures/style.py importable from this subdirectory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Make analysis scripts importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "analysis" / "dhatupatha" / "scripts"))

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from style import setup, savefig

from analyze_dhatupatha import strip_anubandhas, strip_markers, classify_phonemes, VOWELS
from analyze_internal_structure import DEV, ALL_CONS
from analyze_position_roles import load_atoms, classify_position_roles


# Color palette — onset shades blue, coda shades red, outer darker, inner lighter
COLOR_ONSET_OUTER = "#1F4E79"  # dark blue
COLOR_ONSET_INNER = "#5B9BD5"  # light blue
COLOR_CODA_INNER  = "#C6989B"  # light red
COLOR_CODA_OUTER  = "#822529"  # dark red


def main():
    atoms = load_atoms()
    single = [a for a in atoms if a[3].count("V") == 1]

    role_counts = defaultdict(lambda: Counter())
    for gana, idx, stripped, pattern in single:
        for ch, role in classify_position_roles(stripped, pattern):
            role_counts[ch][role] += 1

    # Build rows for each consonant with role counts; sort by total productivity
    rows = []
    for c in ALL_CONS:
        r = role_counts.get(c, Counter())
        oo = r.get("onset_outer", 0)
        oi = r.get("onset_inner", 0)
        ci = r.get("coda_inner", 0)
        co = r.get("coda_outer", 0)
        total = oo + oi + ci + co
        if total > 0:
            rows.append((c, oo, oi, ci, co, total))
    rows.sort(key=lambda r: -r[5])

    cons_labels = [DEV[r[0]] for r in rows]
    oo_vals = [r[1] for r in rows]
    oi_vals = [r[2] for r in rows]
    ci_vals = [r[3] for r in rows]
    co_vals = [r[4] for r in rows]
    totals = [r[5] for r in rows]

    n = len(rows)
    fig, ax = setup(figsize=(6.5, 0.22 * n + 1.5))

    y = list(range(n))[::-1]  # most-productive at top

    # Horizontal stacked bars
    left = [0] * n
    ax.barh(y, oo_vals, left=left, color=COLOR_ONSET_OUTER, edgecolor="black", linewidth=0.3, label="C₁₀ onset-outer")
    left = [a + b for a, b in zip(left, oo_vals)]
    ax.barh(y, oi_vals, left=left, color=COLOR_ONSET_INNER, edgecolor="black", linewidth=0.3, label="C₁ᵢ onset-inner")
    left = [a + b for a, b in zip(left, oi_vals)]
    ax.barh(y, ci_vals, left=left, color=COLOR_CODA_INNER, edgecolor="black", linewidth=0.3, label="C₂ᵢ coda-inner")
    left = [a + b for a, b in zip(left, ci_vals)]
    ax.barh(y, co_vals, left=left, color=COLOR_CODA_OUTER, edgecolor="black", linewidth=0.3, label="C₂₀ coda-outer")

    ax.set_yticks(y)
    ax.set_yticklabels(cons_labels, fontsize=10)
    ax.set_xlabel("Position-role deployment count (single-akṣara atoms)")
    ax.set_xlim(0, max(totals) * 1.08)

    # Total count annotation at end of each bar
    for yi, total in zip(y, totals):
        ax.text(total + 5, yi, str(total), va="center", fontsize=7.5)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    # Legend — manually controlled order (subscripts avoided due to font glyph gaps)
    legend_handles = [
        Patch(facecolor=COLOR_ONSET_OUTER, edgecolor="black", linewidth=0.3, label="C1-outer — onset (atom-start)"),
        Patch(facecolor=COLOR_ONSET_INNER, edgecolor="black", linewidth=0.3, label="C1-inner — onset cluster-joiner"),
        Patch(facecolor=COLOR_CODA_INNER,  edgecolor="black", linewidth=0.3, label="C2-inner — coda cluster-joiner"),
        Patch(facecolor=COLOR_CODA_OUTER,  edgecolor="black", linewidth=0.3, label="C2-outer — coda (atom-end)"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=7.5, frameon=False)

    plt.tight_layout()
    savefig("ch11_position_roles")


if __name__ == "__main__":
    main()
