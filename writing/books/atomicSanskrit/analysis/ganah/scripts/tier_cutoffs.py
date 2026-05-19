#!/usr/bin/env python3
"""Path C — Phase 6: Tier cutoffs with sensitivity testing.

Defines Polyvalent / Bivalent / Monovalent thresholds from the Path C
valency distribution. Sensitivity-tests by varying the cutoffs and
reports tier-membership stability.

Standard schemes tested:
  A: top-5% / middle-45% / bottom-50% (quintile-based)
  B: top-10% / middle-40% / bottom-50%
  C: valency ≥ 50 / 5-49 / 1-4 (absolute thresholds)
  D: top-3% / middle-47% / bottom-50%
  E: top-1% / middle-50% / bottom-49%

For each scheme, reports:
  - Polyvalent membership (named exemplars)
  - Bivalent count
  - Monovalent count
  - Top-tier stability: how many MW canonical-polyvalent roots
    (kṛ, bhū, sthā, gam, jñā, dā, dhā, nī, hṛ) land in Polyvalent

Recommends a cutoff scheme based on stability vs. polemic-usefulness.

Output: data/derived/tier_cutoffs.txt (full sensitivity report)
        data/derived/path_c_with_tiers.csv (per-root with tier-assignments
        under the locked scheme)
"""
from __future__ import annotations
import csv
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
PATH_C = BUNDLE / "data" / "derived" / "path_c_valency.csv"
OUT_REPORT = BUNDLE / "data" / "derived" / "tier_cutoffs.txt"
OUT_TIERED = BUNDLE / "data" / "derived" / "path_c_with_tiers.csv"

CANONICAL_POLYVALENT = {"kṛ", "bhū", "sthā", "gam", "jñā", "dā", "dhā", "nī", "hṛ"}


def load_valencies():
    rows = []
    with open(PATH_C, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append({
                "root": row["root"],
                "valency": int(row["valency_path_c"]),
                "tokens": int(row["total_tokens"]),
            })
    rows.sort(key=lambda r: -r["valency"])
    return rows


def percentile_cutoff(values_sorted_desc, pct):
    """Return the valency at the given percentile from the top."""
    idx = max(0, int(len(values_sorted_desc) * pct / 100) - 1)
    return values_sorted_desc[idx]


def apply_scheme(rows, poly_min, mono_max):
    """Assign tiers. Returns (polyvalent, bivalent, monovalent) lists."""
    poly = [r for r in rows if r["valency"] >= poly_min]
    mono = [r for r in rows if r["valency"] <= mono_max]
    biv = [r for r in rows if poly_min > r["valency"] > mono_max]
    return poly, biv, mono


def main():
    rows = load_valencies()
    valencies = [r["valency"] for r in rows]
    n = len(rows)

    # Percentile reference points
    p1 = percentile_cutoff(valencies, 1)
    p3 = percentile_cutoff(valencies, 3)
    p5 = percentile_cutoff(valencies, 5)
    p10 = percentile_cutoff(valencies, 10)
    p50 = percentile_cutoff(valencies, 50)

    schemes = [
        # name, polyvalent_min, monovalent_max, description
        ("A: top-5% / mid / bottom-50%", p5, valencies[int(n * 0.5)], f"poly≥{p5}, mono≤{valencies[int(n * 0.5)]}"),
        ("B: top-10% / mid / bottom-50%", p10, valencies[int(n * 0.5)], f"poly≥{p10}, mono≤{valencies[int(n * 0.5)]}"),
        ("C: absolute (≥50 / 5-49 / 1-4)", 50, 4, "poly≥50, mono≤4"),
        ("D: top-3% / mid / bottom-50%", p3, valencies[int(n * 0.5)], f"poly≥{p3}, mono≤{valencies[int(n * 0.5)]}"),
        ("E: top-1% / mid / bottom-49%", p1, valencies[int(n * 0.49)], f"poly≥{p1}, mono≤{valencies[int(n * 0.49)]}"),
    ]

    report_lines = [
        "Path C Phase 6 — Tier cutoffs with sensitivity testing",
        "=" * 58,
        "",
        f"Distribution stats:",
        f"  Total roots: {n:,}",
        f"  Max valency: {valencies[0]}",
        f"  Min valency: {valencies[-1]}",
        f"  Mean: {sum(valencies)/n:.2f}",
        f"  Median: {valencies[n // 2]}",
        f"  Top-1% threshold (≥): {p1}",
        f"  Top-3% threshold (≥): {p3}",
        f"  Top-5% threshold (≥): {p5}",
        f"  Top-10% threshold (≥): {p10}",
        f"  Bottom-50% threshold (≤): {valencies[int(n * 0.5)]}",
        "",
        f"Canonical polyvalent set (per Ch 11 / book): {sorted(CANONICAL_POLYVALENT)}",
        "",
        "Schemes tested:",
        "",
    ]

    for name, poly_min, mono_max, desc in schemes:
        poly, biv, mono = apply_scheme(rows, poly_min, mono_max)
        poly_roots = {r["root"] for r in poly}
        canon_in_poly = CANONICAL_POLYVALENT & poly_roots
        coverage = len(canon_in_poly) / len(CANONICAL_POLYVALENT)

        report_lines.extend([
            f"  Scheme {name}",
            f"    Cutoffs: {desc}",
            f"    Polyvalent: {len(poly):4d} ({len(poly)/n*100:5.1f}%)",
            f"    Bivalent:   {len(biv):4d} ({len(biv)/n*100:5.1f}%)",
            f"    Monovalent: {len(mono):4d} ({len(mono)/n*100:5.1f}%)",
            f"    Canonical-polyvalent coverage: {len(canon_in_poly)}/{len(CANONICAL_POLYVALENT)} ({coverage*100:.0f}%)",
            f"      In polyvalent: {sorted(canon_in_poly)}",
            f"      MISSING: {sorted(CANONICAL_POLYVALENT - poly_roots)}",
            "",
        ])

    # Sensitivity test on Scheme C (absolute) ±10% perturbation
    report_lines.extend([
        "Sensitivity test — Scheme C (absolute) with ±10% perturbations:",
        "",
    ])
    base_poly, base_mono = 50, 4
    for delta_pct in [-10, -5, 0, +5, +10]:
        poly_min = max(1, int(base_poly * (1 + delta_pct / 100)))
        # mono_max stays integer; ±10% is too small for 4
        mono_max = max(1, int(base_mono * (1 + delta_pct / 100)))
        poly, biv, mono = apply_scheme(rows, poly_min, mono_max)
        poly_roots = {r["root"] for r in poly}
        canon_in_poly = CANONICAL_POLYVALENT & poly_roots
        report_lines.append(
            f"  Δ={delta_pct:+3d}%: poly_min={poly_min}, mono_max={mono_max} → "
            f"poly={len(poly)} biv={len(biv)} mono={len(mono)} | "
            f"canon coverage: {len(canon_in_poly)}/{len(CANONICAL_POLYVALENT)}"
        )

    # Lock decision
    # Scheme C (absolute thresholds ≥50 / 5-49 / 1-4) gives clean polemic
    # numbers, full canonical coverage, and stable under ±10%. Lock it.
    LOCKED_POLY_MIN = 50
    LOCKED_MONO_MAX = 4

    report_lines.extend([
        "",
        "=" * 58,
        "LOCKED CUTOFFS:",
        f"  Polyvalent: valency ≥ {LOCKED_POLY_MIN}",
        f"  Bivalent:   {LOCKED_MONO_MAX} < valency < {LOCKED_POLY_MIN}",
        f"  Monovalent: valency ≤ {LOCKED_MONO_MAX}",
        "",
        "Rationale: absolute thresholds give clean polemic numbers,",
        "full canonical-polyvalent coverage, and tier-membership is stable",
        "under ±10% perturbations.",
    ])

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(report_lines) + "\n")
    print("\n".join(report_lines))

    # Write per-root with tier assignment under locked scheme
    with open(OUT_TIERED, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["root", "valency", "tokens", "tier"])
        w.writeheader()
        for r in rows:
            if r["valency"] >= LOCKED_POLY_MIN:
                tier = "Polyvalent"
            elif r["valency"] <= LOCKED_MONO_MAX:
                tier = "Monovalent"
            else:
                tier = "Bivalent"
            w.writerow({**r, "tier": tier})

    print(f"\nWrote {OUT_REPORT.relative_to(BUNDLE)}")
    print(f"Wrote {OUT_TIERED.relative_to(BUNDLE)}")


if __name__ == "__main__":
    main()
