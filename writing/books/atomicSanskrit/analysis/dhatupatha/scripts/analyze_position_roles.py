#!/usr/bin/env python3
"""
analyze_position_roles.py — extended C₁ / C₂ position-role analysis.

For each consonant in the Dhātupāṭha's single-akṣara atoms, classify its
position by phonological role:
  - onset_outer       (atom-start, the C₁ position)
  - onset_inner       (cluster-joiner before the vowel)
  - coda_inner        (cluster-joiner after the vowel)
  - coda_outer        (atom-end, the C₂ position)

Then aggregate to:
  - C₁ total = onset_outer + onset_inner   (all onset positions)
  - C₂ total = coda_inner + coda_outer     (all coda positions)
  - i/f ratio = C₁ total / C₂ total

This extends the previous CV / VC / CVC analysis to include cluster patterns:
  C₁V, VC₂, C₁VC₂, C₁C₂V, VC₁C₂, C₁C₂VC₃, C₁VC₂C₃, C₁C₂VC₃C₄

Naming convention (per author direction 2026-05-17):
  C₁ = onset position (any consonant before the vowel)
  C₂ = coda position (any consonant after the vowel)
  V  = nucleus vowel

Run: python3 scripts/analyze_position_roles.py
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_dhatupatha import (  # noqa
    strip_anubandhas, strip_markers, classify_phonemes, VOWELS
)
from analyze_internal_structure import DEV, VARGAS, ALL_CONS, PLACE_OF, PLACE_DEV  # noqa

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "dhatupatha.csv"

# Map structural patterns to their new-naming form (single-akṣara only — patterns with exactly one V)
PATTERN_LABELS = {
    "V":      "V",
    "CV":     "C₁V",
    "VC":     "VC₂",
    "CVC":    "C₁VC₂",
    "CCV":    "C₁C₂V",
    "VCC":    "VC₁C₂",
    "CCVC":   "C₁C₂VC₃",
    "CVCC":   "C₁VC₂C₃",
    "CCVCC":  "C₁C₂VC₃C₄",
}


def load_atoms():
    """Read the Dhātupāṭha. Return list of (gana, idx, stripped, pattern)."""
    atoms = []
    with open(DATA_FILE) as fh:
        for line in fh:
            parts = line.strip().split(",")
            if len(parts) < 3: continue
            stripped = strip_anubandhas(strip_markers(parts[2]))
            pat = classify_phonemes(stripped)
            atoms.append((parts[0], parts[1], stripped, pat))
    return atoms


def classify_position_roles(atom: str, pattern: str):
    """For each character in atom, yield (char, role).

    Roles for single-akṣara atoms (exactly one V):
        onset_outer  — first character (atom-start) IF a consonant
        onset_inner  — consonant before the vowel but not at position 0
        coda_inner   — consonant after the vowel but not at last position
        coda_outer   — last character (atom-end) IF a consonant

    Patterns with 0 or 2+ vowels are skipped (intervocalic positions get
    intricate; defer to a future multi-akṣara analysis).
    """
    if pattern.count("V") != 1:
        return  # only single-akṣara atoms
    v_idx = pattern.index("V")
    last_idx = len(pattern) - 1

    for i, ch in enumerate(atom):
        if ch in VOWELS:
            continue
        if i < v_idx:
            role = "onset_outer" if i == 0 else "onset_inner"
        elif i > v_idx:
            role = "coda_outer" if i == last_idx else "coda_inner"
        else:
            continue
        yield ch, role


def main():
    atoms = load_atoms()
    single_akshara = [a for a in atoms if a[3].count("V") == 1]

    print(f"DHĀTUPĀṬHA — EXTENDED POSITION-ROLE ANALYSIS")
    print(f"Total atoms in Dhātupāṭha: {len(atoms)}")
    print(f"Single-akṣara atoms (analyzed here): {len(single_akshara)}")

    # Show pattern breakdown using new naming
    pattern_counts = Counter(a[3] for a in single_akshara)
    print(f"\nSingle-akṣara patterns (new naming → atom count):")
    for pat, n in pattern_counts.most_common():
        label = PATTERN_LABELS.get(pat, pat)
        print(f"  {label:>12s}  ({pat:>5s})  {n:>4d} atoms")

    # Classify position roles
    role_counts = defaultdict(lambda: Counter())
    for gana, idx, stripped, pattern in single_akshara:
        for ch, role in classify_position_roles(stripped, pattern):
            role_counts[ch][role] += 1

    # Display profile per consonant
    print(f"\n{'=' * 88}")
    print(f"PER-CONSONANT POSITION-ROLE PROFILE (extended across all single-akṣara patterns)")
    print(f"{'=' * 88}")
    print(f"  {'cons':<5s} {'onset_outer':>12s} {'onset_inner':>12s} {'coda_inner':>11s} {'coda_outer':>11s}  |  {'C₁ tot':>7s} {'C₂ tot':>7s} {'i/f':>7s}")
    print("  " + "-" * 88)

    # Build summary rows
    rows = []
    for c in ALL_CONS:
        r = role_counts.get(c, Counter())
        oo = r.get("onset_outer", 0)
        oi = r.get("onset_inner", 0)
        ci = r.get("coda_inner", 0)
        co = r.get("coda_outer", 0)
        c1_total = oo + oi
        c2_total = ci + co
        total = c1_total + c2_total
        if total == 0:
            continue
        ratio = c1_total / c2_total if c2_total > 0 else float("inf")
        rows.append((c, oo, oi, ci, co, c1_total, c2_total, ratio, total))

    rows.sort(key=lambda r: -r[8])  # by total productivity
    for c, oo, oi, ci, co, c1, c2, ratio, total in rows:
        ratio_s = f"{ratio:>6.2f}x" if ratio != float("inf") else "    inf"
        print(f"  {DEV[c]:<5s} {oo:>12d} {oi:>12d} {ci:>11d} {co:>11d}  | {c1:>7d} {c2:>7d}  {ratio_s}")

    # Comparison: extended-totals vs old (CV/VC/CVC only) totals
    print(f"\n{'=' * 78}")
    print(f"COMPARISON: extended (clusters) vs three-pattern (single-cons positions only)")
    print(f"{'=' * 78}")
    print(f"  {'cons':<5s} {'ext C₁':>7s} {'ext C₂':>7s} {'ext i/f':>9s}  |  {'3-pat C₁':>9s} {'3-pat C₂':>9s} {'3-pat i/f':>10s}")
    print("  " + "-" * 76)
    # Compute three-pattern totals (CV + VC + CVC only) for comparison
    three_pat_c1 = Counter()
    three_pat_c2 = Counter()
    for gana, idx, stripped, pattern in single_akshara:
        if pattern not in ("CV", "VC", "CVC"):
            continue
        for ch, role in classify_position_roles(stripped, pattern):
            if role.startswith("onset"):
                three_pat_c1[ch] += 1
            elif role.startswith("coda"):
                three_pat_c2[ch] += 1

    for c, oo, oi, ci, co, c1, c2, ratio, total in rows:
        old_c1 = three_pat_c1.get(c, 0)
        old_c2 = three_pat_c2.get(c, 0)
        old_ratio = old_c1 / old_c2 if old_c2 > 0 else (float("inf") if old_c1 > 0 else 0)
        old_ratio_s = f"{old_ratio:>8.2f}x" if old_ratio not in (float("inf"), 0) else ("     inf" if old_c1 > 0 else "       —")
        new_ratio_s = f"{ratio:>7.2f}x" if ratio != float("inf") else "     inf"
        print(f"  {DEV[c]:<5s} {c1:>7d} {c2:>7d} {new_ratio_s}  | {old_c1:>9d} {old_c2:>9d} {old_ratio_s}")

    # Place-of-articulation aggregated analysis
    print(f"\n{'=' * 90}")
    print(f"PLACE-OF-ARTICULATION AGGREGATED (extended across all single-akṣara patterns)")
    print(f"{'=' * 90}")
    print(f"  {'place':<14s} {'oo':>6s} {'oi':>6s} {'ci':>6s} {'co':>6s}  |  {'C₁ tot':>7s} {'C₂ tot':>7s} {'i/f':>7s}  |  {'outer':>6s} {'inner':>6s} {'inner %':>8s}")
    print(f"  {'(Devanagari)':<14s} {'(C₁₀)':>6s} {'(C₁ᵢ)':>6s} {'(C₂ᵢ)':>6s} {'(C₂₀)':>6s}  |")
    print("  " + "-" * 90)

    place_order = ["Velar", "Palatal", "Retroflex", "Dental", "Labial"]
    place_totals = {p: {"oo": 0, "oi": 0, "ci": 0, "co": 0} for p in place_order}

    for c in ALL_CONS:
        place = PLACE_OF.get(c)
        if place is None: continue
        r = role_counts.get(c, Counter())
        place_totals[place]["oo"] += r.get("onset_outer", 0)
        place_totals[place]["oi"] += r.get("onset_inner", 0)
        place_totals[place]["ci"] += r.get("coda_inner", 0)
        place_totals[place]["co"] += r.get("coda_outer", 0)

    for p in place_order:
        t = place_totals[p]
        c1 = t["oo"] + t["oi"]
        c2 = t["ci"] + t["co"]
        outer = t["oo"] + t["co"]
        inner = t["oi"] + t["ci"]
        ratio = c1 / c2 if c2 > 0 else float("inf")
        inner_pct = 100 * inner / (outer + inner) if (outer + inner) > 0 else 0
        ratio_s = f"{ratio:>6.2f}x" if ratio != float("inf") else "    inf"
        print(f"  {PLACE_DEV[p]:<14s} {t['oo']:>6d} {t['oi']:>6d} {t['ci']:>6d} {t['co']:>6d}  | {c1:>7d} {c2:>7d}  {ratio_s}  | {outer:>6d} {inner:>6d}  {inner_pct:>6.1f}%")

    # Compare to CVC-only place-level analysis (from earlier)
    print(f"\nPLACE-LEVEL i/f COMPARISON: extended vs CVC-only")
    print(f"  {'place':<14s} {'CVC-only i/f':>14s}  {'extended i/f':>14s}  {'change':>20s}")
    print("  " + "-" * 70)
    cvc_only_ratios = {
        "Velar":     1.80,
        "Palatal":   1.15,
        "Retroflex": 0.40,
        "Dental":    0.80,
        "Labial":    1.92,
    }
    for p in place_order:
        t = place_totals[p]
        c1 = t["oo"] + t["oi"]
        c2 = t["ci"] + t["co"]
        ext_ratio = c1 / c2 if c2 > 0 else float("inf")
        old_ratio = cvc_only_ratios[p]
        delta = ext_ratio - old_ratio
        sign = "softens" if abs(ext_ratio - 1) < abs(old_ratio - 1) else "sharpens"
        print(f"  {PLACE_DEV[p]:<14s} {old_ratio:>13.2f}x  {ext_ratio:>13.2f}x  {sign:>20s}")


if __name__ == "__main__":
    main()
