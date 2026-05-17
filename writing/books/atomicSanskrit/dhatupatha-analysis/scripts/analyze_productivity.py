#!/usr/bin/env python3
"""
analyze_productivity.py — productivity vs. structural complexity.

For a curated sample of ~120 representative dhātus, correlates productivity
(count of primary derivatives per dhātu, estimated from Monier-Williams entries)
against structural features (particle count, akṣara count, structural pattern).

The compression-principle prediction: simpler atoms generate larger vocabularies.
The minimum-particle CV pattern should dominate the top of the productivity
ranking; the maximum-particle CCVCC pattern should sit at the bottom.

DATA SOURCE NOTE
================

The productivity counts in `data/dhatu_productivity.csv` are *approximate
estimates* of the count of primary derivatives (kṛdanta nominals, upasarga-
prefixed verbs and their derivatives, agentive / instrumental / abstract
nominals) per dhātu, drawn from canonical Sanskrit reference dictionaries:

  - Monier-Williams Sanskrit-English Dictionary (1899) — primary source
  - V. S. Apte, The Practical Sanskrit-English Dictionary (1890)

The estimates are *order-of-magnitude correct* (the top-tier dhātus generate
60-80 primary derivatives; the bottom-tier 2-8). The relative ranking is
the load-bearing claim, not the precise count.

The sample of ~120 dhātus is selected to span the Dhātupāṭha's structural
pattern space (CV, VC, CVC, CCV, CCVC, CVCC, CCVCC) with multiple dhātus
in each category. The sample is *illustrative*, not exhaustive; it
documents the engineering pattern visible in the standard reference
dictionaries.

Spearman rank correlation is used because the productivity estimates are
ordinal-reliable but not interval-precise.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "dhatu_productivity.csv"


def spearman(xs: list[float], ys: list[float]) -> float:
    """Spearman rank correlation between two equal-length lists."""
    n = len(xs)
    if n < 2:
        return 0.0

    def rank(values: list[float]) -> list[float]:
        sorted_idx = sorted(range(n), key=lambda i: values[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and values[sorted_idx[j + 1]] == values[sorted_idx[i]]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[sorted_idx[k]] = avg_rank
            i = j + 1
        return ranks

    rx = rank(xs)
    ry = rank(ys)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    den_x = sum((rx[i] - mean_rx) ** 2 for i in range(n)) ** 0.5
    den_y = sum((ry[i] - mean_ry) ** 2 for i in range(n)) ** 0.5
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found at {DATA_FILE}")
        return 1

    rows: list[dict] = []
    with DATA_FILE.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                derivatives = int(row["mw_derivatives"])
            except (KeyError, ValueError):
                continue
            if derivatives <= 0:
                continue
            try:
                particles = int(row["particles"])
                aksharas = int(row["aksharas"])
            except (KeyError, ValueError):
                continue
            rows.append({
                "slp1": row["slp1"],
                "iast": row["iast"],
                "devanagari": row["devanagari"],
                "gloss": row["gloss"],
                "pattern": row["particle_pattern"],
                "particles": particles,
                "aksharas": aksharas,
                "productivity": derivatives,
            })

    n = len(rows)
    print("=" * 72)
    print("DHĀTUPĀṬHA PRODUCTIVITY ANALYSIS")
    print("=" * 72)
    print()
    print(f"Sample size: {n} dhātus")
    print(f"Productivity proxy: estimated primary-derivative count from")
    print(f"  Monier-Williams Sanskrit-English Dictionary (1899)")
    print(f"  and V. S. Apte's Practical Sanskrit-English Dictionary (1890).")
    print()

    productivities = [r["productivity"] for r in rows]
    print(f"Productivity range: {min(productivities)}  →  {max(productivities)}")
    print(f"Productivity mean:  {mean(productivities):.1f}")
    print(f"Productivity median: {median(productivities):.1f}")
    print()

    # ----- Top and bottom -----
    print("-" * 72)
    print("TOP 15 dhātus by productivity (load-bearing atoms):")
    print("-" * 72)
    print(f"{'rank':<5}{'iast':<8}{'dev':<6}{'pattern':<8}{'parts':>6}{'akṣ':>5}{'prod':>6}  gloss")
    sorted_top = sorted(rows, key=lambda r: -r["productivity"])
    for i, r in enumerate(sorted_top[:15], 1):
        print(f"{i:<5}{r['iast']:<8}{r['devanagari']:<6}{r['pattern']:<8}"
              f"{r['particles']:>6}{r['aksharas']:>5}{r['productivity']:>6}  {r['gloss']}")
    print()

    print("-" * 72)
    print("BOTTOM 15 dhātus by productivity:")
    print("-" * 72)
    print(f"{'rank':<5}{'iast':<8}{'dev':<6}{'pattern':<8}{'parts':>6}{'akṣ':>5}{'prod':>6}  gloss")
    sorted_bot = sorted(rows, key=lambda r: r["productivity"])
    for i, r in enumerate(sorted_bot[:15], 1):
        print(f"{i:<5}{r['iast']:<8}{r['devanagari']:<6}{r['pattern']:<8}"
              f"{r['particles']:>6}{r['aksharas']:>5}{r['productivity']:>6}  {r['gloss']}")
    print()

    # ----- Stratified by particle count -----
    print("-" * 72)
    print("PRODUCTIVITY × PARTICLE COUNT:")
    print("-" * 72)
    by_particles = defaultdict(list)
    for r in rows:
        by_particles[r["particles"]].append(r["productivity"])

    print(f"{'particles':<12}{'n':>5}{'mean':>9}{'median':>9}{'max':>7}{'min':>6}")
    for p in sorted(by_particles.keys()):
        vals = by_particles[p]
        print(f"{p:<12}{len(vals):>5}{mean(vals):>9.1f}"
              f"{median(vals):>9.1f}{max(vals):>7}{min(vals):>6}")
    print()

    # ----- Stratified by pattern -----
    print("-" * 72)
    print("PRODUCTIVITY × STRUCTURAL PATTERN:")
    print("-" * 72)
    by_pattern = defaultdict(list)
    for r in rows:
        by_pattern[r["pattern"]].append(r["productivity"])

    print(f"{'pattern':<10}{'n':>5}{'mean':>9}{'median':>9}{'max':>7}{'min':>6}")
    pattern_order = ["V", "CV", "VC", "CCV", "VCC", "CVC", "CCVC", "CVCC", "CCVCC"]
    for pat in pattern_order:
        if pat in by_pattern:
            vals = by_pattern[pat]
            print(f"{pat:<10}{len(vals):>5}{mean(vals):>9.1f}"
                  f"{median(vals):>9.1f}{max(vals):>7}{min(vals):>6}")
    print()

    # ----- Correlations -----
    print("-" * 72)
    print("RANK CORRELATIONS (Spearman ρ):")
    print("-" * 72)
    rho_particles = spearman(
        [r["particles"] for r in rows],
        [r["productivity"] for r in rows],
    )
    rho_aksharas = spearman(
        [r["aksharas"] for r in rows],
        [r["productivity"] for r in rows],
    )
    print(f"  productivity vs. particle count : ρ = {rho_particles:+.3f}")
    print(f"  productivity vs. akṣara count  : ρ = {rho_aksharas:+.3f}")
    print()
    print("Interpretation: negative ρ means *simpler atoms are more productive*")
    print("— the compression principle's prediction.")
    print()

    # ----- Top-10 pattern composition -----
    print("-" * 72)
    print("PATTERN COMPOSITION OF TOP 20 vs. BOTTOM 20:")
    print("-" * 72)
    top20 = sorted_top[:20]
    bot20 = sorted_bot[:20]
    top_patterns = Counter(r["pattern"] for r in top20)
    bot_patterns = Counter(r["pattern"] for r in bot20)
    print(f"{'pattern':<10}{'top 20':>10}{'bottom 20':>13}")
    all_patterns = sorted(set(top_patterns) | set(bot_patterns))
    for pat in all_patterns:
        print(f"{pat:<10}{top_patterns.get(pat, 0):>10}{bot_patterns.get(pat, 0):>13}")
    print()

    # ----- Mean particle count in top vs bottom -----
    mean_top_parts = mean(r["particles"] for r in top20)
    mean_bot_parts = mean(r["particles"] for r in bot20)
    print(f"Mean particle count, top 20:    {mean_top_parts:.2f}")
    print(f"Mean particle count, bottom 20: {mean_bot_parts:.2f}")
    print(f"Compression signature ratio:    {mean_bot_parts / mean_top_parts:.2f}×")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
