#!/usr/bin/env python3
"""Path C — Phase 5: Spearman rank correlation between Path A and Path C.

Path A: MW-derivative count from analysis/dhatupatha/data/dhatu_productivity.csv
        (144 curated dhātus, derivative-count estimates from Monier-Williams 1899
        and Apte 1890).
Path C: corpus-attested combinatorial valency from data/derived/path_c_valency.csv
        (3,839 roots, count of distinct (preverb, pratyaya_class) pairs in DCS).

Match on IAST root name. Reports:
  - Number of MW-sample roots matched in the corpus
  - Spearman rank correlation ρ
  - Pearson product-moment correlation r (secondary)
  - Top-tier agreement (top-N MW vs top-N corpus)
  - Where the two paths disagree most (the polemically interesting cases)

Output: data/derived/path_a_vs_path_c.csv (per-root comparison)
         + console summary written to data/derived/spearman_summary.txt
"""
from __future__ import annotations
import csv
import math
from collections import defaultdict
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
PATH_A = BUNDLE.parent / "dhatupatha" / "data" / "dhatu_productivity.csv"
PATH_C = BUNDLE / "data" / "derived" / "path_c_valency.csv"
OUT_COMPARE = BUNDLE / "data" / "derived" / "path_a_vs_path_c.csv"
OUT_SUMMARY = BUNDLE / "data" / "derived" / "spearman_summary.txt"


def spearman(xs, ys):
    """Spearman rank correlation. Handles ties via average ranks."""
    n = len(xs)
    if n < 2:
        return 0.0
    # Rank both arrays (average rank for ties)
    def ranks(vals):
        sorted_indexed = sorted(enumerate(vals), key=lambda iv: iv[1])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and sorted_indexed[j + 1][1] == sorted_indexed[i][1]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[sorted_indexed[k][0]] = avg_rank
            i = j + 1
        return r
    rx = ranks(xs)
    ry = ranks(ys)
    mean_x = sum(rx) / n
    mean_y = sum(ry) / n
    num = sum((rx[i] - mean_x) * (ry[i] - mean_y) for i in range(n))
    den_x = math.sqrt(sum((rx[i] - mean_x) ** 2 for i in range(n)))
    den_y = math.sqrt(sum((ry[i] - mean_y) ** 2 for i in range(n)))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = math.sqrt(sum((xs[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ys[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def main():
    # Load Path A (MW)
    path_a: dict[str, dict] = {}
    with open(PATH_A, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            iast = row["iast"]
            path_a[iast] = {
                "particles": int(row["particles"]),
                "mw_derivatives": int(row["mw_derivatives"]),
                "pattern": row["particle_pattern"],
            }

    # Load Path C (corpus)
    path_c: dict[str, dict] = {}
    with open(PATH_C, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            path_c[row["root"]] = {
                "valency_path_c": int(row["valency_path_c"]),
                "total_tokens": int(row["total_tokens"]),
            }

    # Match: for each MW root, look up in corpus.
    matched = []
    unmatched_a = []
    for root, a_data in path_a.items():
        c_data = path_c.get(root)
        if c_data:
            matched.append({
                "root": root,
                "particles": a_data["particles"],
                "pattern": a_data["pattern"],
                "mw_derivatives": a_data["mw_derivatives"],
                "valency_path_c": c_data["valency_path_c"],
                "tokens": c_data["total_tokens"],
            })
        else:
            unmatched_a.append(root)

    # Sort by MW rank for stable output
    matched.sort(key=lambda r: -r["mw_derivatives"])

    # Compute correlations on matched subset
    mw_vals = [r["mw_derivatives"] for r in matched]
    c_vals = [r["valency_path_c"] for r in matched]
    rho_mw_vs_c = spearman(mw_vals, c_vals)
    r_mw_vs_c = pearson(mw_vals, c_vals)

    # Also re-verify the Path A claim: ρ(productivity, particle_count) = -0.485
    particles = [r["particles"] for r in matched]
    rho_mw_vs_particles = spearman(mw_vals, particles)

    # And new: ρ(Path C, particle_count) — does corpus valency show the same inverse?
    rho_c_vs_particles = spearman(c_vals, particles)

    # Top-tier overlap: top-20 by MW vs top-20 by Path C
    top20_mw = set(r["root"] for r in sorted(matched,
        key=lambda r: -r["mw_derivatives"])[:20])
    top20_c = set(r["root"] for r in sorted(matched,
        key=lambda r: -r["valency_path_c"])[:20])
    overlap_top20 = top20_mw & top20_c

    # Write per-root comparison
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_COMPARE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "root", "particles", "pattern", "mw_derivatives",
            "valency_path_c", "tokens",
        ])
        w.writeheader()
        for row in matched:
            w.writerow(row)

    # Write summary
    summary_lines = [
        "Path C Phase 5 — Spearman baseline (Path A vs Path C)",
        "=" * 56,
        "",
        f"MW sample size (Path A): {len(path_a)}",
        f"Roots matched in corpus: {len(matched)}",
        f"Unmatched MW roots: {len(unmatched_a)}",
        "",
        "Correlations on matched subset:",
        f"  Spearman ρ (MW vs Path C):           {rho_mw_vs_c:+.4f}",
        f"  Pearson  r (MW vs Path C):           {r_mw_vs_c:+.4f}",
        f"  Spearman ρ (MW vs particles):        {rho_mw_vs_particles:+.4f}  [chapter cites −0.485]",
        f"  Spearman ρ (Path C vs particles):    {rho_c_vs_particles:+.4f}  [parallel test]",
        "",
        f"Top-20 overlap (MW top-20 ∩ Path C top-20): {len(overlap_top20)}/20",
        f"  Common: {sorted(overlap_top20)}",
        f"  MW-only top-20: {sorted(top20_mw - top20_c)}",
        f"  Path-C-only top-20: {sorted(top20_c - top20_mw)}",
        "",
    ]
    if unmatched_a:
        summary_lines.append(f"Unmatched MW roots (no corpus attestation): {sorted(unmatched_a)}")
    summary_text = "\n".join(summary_lines)
    print(summary_text)
    OUT_SUMMARY.write_text(summary_text)
    print(f"\nWrote {OUT_COMPARE.relative_to(BUNDLE)}")
    print(f"Wrote {OUT_SUMMARY.relative_to(BUNDLE)}")


if __name__ == "__main__":
    main()
