#!/usr/bin/env python3
"""
analyze_extensions.py — three deeper analyses on the Dhātupāṭha:

  (A) CLUSTER ANALYSIS — top initial and final 2-consonant clusters,
      revealing Sanskrit's phonotactic preferences in dhātu construction.

  (B) AKṢARA-COUNT BREAKDOWN — column / place distributions filtered by
      akṣara count (1-akṣara vs. 2-akṣara), testing whether the simplest
      atoms show purest engineering preferences.

  (C) VOWEL × CONSONANT INTERACTION — vowel-frequency distribution and
      consonant-vowel co-occurrence patterns.

Uses the same anubandha-stripping rules as analyze_varga_distribution.py
(Aṣṭādhyāyī 1.3.2 + 1.3.3 + 1.3.5).  Supports gaṇa filtering via CLI arg.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "dhatupatha.csv"

# --- SLP1 phoneme inventory ---------------------------------------------

VOWELS = set("aAiIuUfFxXeEoO")

VARGA_GRID = {
    "k": (1, 1), "K": (1, 2), "g": (1, 3), "G": (1, 4), "N": (1, 5),
    "c": (2, 1), "C": (2, 2), "j": (2, 3), "J": (2, 4), "Y": (2, 5),
    "w": (3, 1), "W": (3, 2), "q": (3, 3), "Q": (3, 4), "R": (3, 5),
    "t": (4, 1), "T": (4, 2), "d": (4, 3), "D": (4, 4), "n": (4, 5),
    "p": (5, 1), "P": (5, 2), "b": (5, 3), "B": (5, 4), "m": (5, 5),
}

NON_VARGA_CONSONANTS = set("yrlv" "SzsH" "h" "M")
CONSONANTS = set(VARGA_GRID.keys()) | NON_VARGA_CONSONANTS

# SLP1 → IAST single-char mapping for display
SLP1_TO_IAST = {
    "a": "a", "A": "ā", "i": "i", "I": "ī", "u": "u", "U": "ū",
    "f": "ṛ", "F": "ṝ", "x": "ḷ", "X": "ḹ",
    "e": "e", "E": "ai", "o": "o", "O": "au",
    "k": "k", "K": "kh", "g": "g", "G": "gh", "N": "ṅ",
    "c": "c", "C": "ch", "j": "j", "J": "jh", "Y": "ñ",
    "w": "ṭ", "W": "ṭh", "q": "ḍ", "Q": "ḍh", "R": "ṇ",
    "t": "t", "T": "th", "d": "d", "D": "dh", "n": "n",
    "p": "p", "P": "ph", "b": "b", "B": "bh", "m": "m",
    "y": "y", "r": "r", "l": "l", "v": "v",
    "S": "ś", "z": "ṣ", "s": "s", "h": "h",
    "M": "ṃ", "H": "ḥ",
}

COLUMN_NAMES_SHORT = {
    1: "C1 (k-type)", 2: "C2 (kh-type)", 3: "C3 (g-type)",
    4: "C4 (gh-type)", 5: "C5 (n-type/nasal)",
}

PLACE_NAMES_SHORT = {
    1: "Velar", 2: "Palatal", 3: "Retroflex", 4: "Dental", 5: "Labial",
}

# --- Anubandha stripping ------------------------------------------------

SHORT_VOWEL_ANUBANDHAS = set("aiu")
INITIAL_ANUBANDHAS_2CHAR = ("Yi", "wu", "qu")
TRAILING_CONSONANT_ANUBANDHAS = set("YNlSzwq")
ALL_MARKERS = re.compile(r"[~\\^]")


def strip_markers(s: str) -> str:
    return ALL_MARKERS.sub("", s)


def strip_anubandhas(s: str) -> str:
    for prefix in INITIAL_ANUBANDHAS_2CHAR:
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    if (len(s) >= 2
            and s[-1] in TRAILING_CONSONANT_ANUBANDHAS
            and s[-2] in VOWELS):
        s = s[:-1]
    if (len(s) >= 2
            and s[-1] in SHORT_VOWEL_ANUBANDHAS
            and s[-2] in CONSONANTS):
        remaining = s[:-1]
        if any(c in VOWELS for c in remaining):
            s = remaining
    return s


def initial_cluster(s: str) -> str:
    """Return contiguous consonants at the start of the structural form."""
    out = []
    for ch in s:
        if ch in CONSONANTS:
            out.append(ch)
        else:
            break
    return "".join(out)


def final_cluster(s: str) -> str:
    """Return contiguous consonants at the end of the structural form."""
    out = []
    for ch in reversed(s):
        if ch in CONSONANTS:
            out.append(ch)
        else:
            break
    return "".join(reversed(out))


def count_aksharas(s: str) -> int:
    return sum(1 for c in s if c in VOWELS)


def slp1_to_iast(s: str) -> str:
    return "".join(SLP1_TO_IAST.get(c, c) for c in s)


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found at {DATA_FILE}", file=sys.stderr)
        return 1

    gana_filter: int | None = None
    if len(sys.argv) > 1:
        try:
            gana_filter = int(sys.argv[1])
        except ValueError:
            print(f"Invalid gaṇa filter: {sys.argv[1]}", file=sys.stderr)
            return 1

    # Buckets
    dhatus = []  # list of (gana, original, structural)
    with DATA_FILE.open() as fh:
        for row in csv.reader(fh):
            if len(row) < 3 or not row[0].isdigit():
                continue
            gana = int(row[0])
            if gana_filter is not None and gana != gana_filter:
                continue
            original = row[2].strip()
            structural = strip_anubandhas(strip_markers(original))
            if not structural:
                continue
            dhatus.append((gana, original, structural))

    total_dhatus = len(dhatus)
    print("=" * 80)
    print("DHĀTUPĀṬHA — DEEPER EXTENSIONS")
    if gana_filter is not None:
        print(f"(FILTERED TO GAṆA {gana_filter} ONLY)")
    print(f"({total_dhatus} dhātus, post-anubandha-stripping)")
    print("=" * 80)
    print()

    # ===== (A) CLUSTER ANALYSIS =====
    print("=" * 80)
    print("(A) CLUSTER ANALYSIS — Initial and final 2-consonant clusters")
    print("=" * 80)
    print()

    initial_clusters_2 = Counter()
    initial_clusters_3 = Counter()  # rare 3-consonant initials
    final_clusters_2 = Counter()
    final_clusters_3 = Counter()
    initial_singletons = Counter()  # dhātus with single initial consonant
    final_singletons = Counter()

    for _, _, structural in dhatus:
        ini = initial_cluster(structural)
        fin = final_cluster(structural)
        if len(ini) == 1:
            initial_singletons[ini] += 1
        elif len(ini) == 2:
            initial_clusters_2[ini] += 1
        elif len(ini) >= 3:
            initial_clusters_3[ini[:3]] += 1
        if len(fin) == 1:
            final_singletons[fin] += 1
        elif len(fin) == 2:
            final_clusters_2[fin] += 1
        elif len(fin) >= 3:
            final_clusters_3[fin[-3:]] += 1

    total_with_initial_2_cluster = sum(initial_clusters_2.values())
    total_with_initial_3_cluster = sum(initial_clusters_3.values())
    total_with_final_2_cluster = sum(final_clusters_2.values())
    total_with_final_3_cluster = sum(final_clusters_3.values())

    print(f"Dhātus with 2-consonant initial cluster (CC-): "
          f"{total_with_initial_2_cluster} "
          f"({100*total_with_initial_2_cluster/total_dhatus:.1f}%)")
    print(f"Dhātus with 3-consonant initial cluster (CCC-): "
          f"{total_with_initial_3_cluster} "
          f"({100*total_with_initial_3_cluster/total_dhatus:.1f}%)")
    print(f"Dhātus with 2-consonant final cluster (-CC): "
          f"{total_with_final_2_cluster} "
          f"({100*total_with_final_2_cluster/total_dhatus:.1f}%)")
    print(f"Dhātus with 3-consonant final cluster (-CCC): "
          f"{total_with_final_3_cluster} "
          f"({100*total_with_final_3_cluster/total_dhatus:.1f}%)")
    print()

    print(f"TOP 20 INITIAL 2-CONSONANT CLUSTERS")
    print(f"{'IAST':>10}  {'SLP1':>10}  {'Count':>7}  {'% of CC-':>9}")
    print("-" * 60)
    for cluster, count in initial_clusters_2.most_common(20):
        iast = slp1_to_iast(cluster)
        pct = 100 * count / total_with_initial_2_cluster
        bar = "#" * int(pct * 0.5)
        print(f"  {iast:>8}-  {cluster:>8}-  {count:>6}  {pct:>7.1f}%  {bar}")
    print()

    if total_with_initial_3_cluster > 0:
        print(f"INITIAL 3-CONSONANT CLUSTERS (rare)")
        for cluster, count in initial_clusters_3.most_common(10):
            iast = slp1_to_iast(cluster)
            print(f"  {iast:>8}-  ({cluster:>4}-)  {count} occurrence(s)")
        print()

    print(f"TOP 20 FINAL 2-CONSONANT CLUSTERS")
    print(f"{'IAST':>10}  {'SLP1':>10}  {'Count':>7}  {'% of -CC':>9}")
    print("-" * 60)
    for cluster, count in final_clusters_2.most_common(20):
        iast = slp1_to_iast(cluster)
        pct = 100 * count / total_with_final_2_cluster
        bar = "#" * int(pct * 0.5)
        print(f"  -{iast:>8}  -{cluster:>8}  {count:>6}  {pct:>7.1f}%  {bar}")
    print()

    if total_with_final_3_cluster > 0:
        print(f"FINAL 3-CONSONANT CLUSTERS (rare)")
        for cluster, count in final_clusters_3.most_common(10):
            iast = slp1_to_iast(cluster)
            print(f"  -{iast:>8}  (-{cluster:>4})  {count} occurrence(s)")
        print()

    # ===== (B) AKṢARA-COUNT BREAKDOWN =====
    print("=" * 80)
    print("(B) AKṢARA-COUNT BREAKDOWN — Column distribution by akṣara count")
    print("=" * 80)
    print()

    # Bucket dhātus by akṣara count
    by_aksh: dict[int, list[str]] = {}
    for _, _, structural in dhatus:
        aksh = count_aksharas(structural)
        by_aksh.setdefault(aksh, []).append(structural)

    print(f"{'Akṣaras':>8}  {'Dhātus':>8}  {'%':>6}  "
          f"{'C1':>6}  {'C2':>6}  {'C3':>6}  {'C4':>6}  {'C5':>6}  "
          f"{'Total varga':>11}")
    print("-" * 80)
    for aksh in sorted(by_aksh):
        cohort = by_aksh[aksh]
        col_counts = Counter()
        total_varga = 0
        for s in cohort:
            for ch in s:
                if ch in VARGA_GRID:
                    _, col = VARGA_GRID[ch]
                    col_counts[col] += 1
                    total_varga += 1
        if total_varga == 0:
            continue
        cohort_pct = 100 * len(cohort) / total_dhatus
        row = (f"  {aksh:>6}  {len(cohort):>8}  {cohort_pct:>5.1f}%  ")
        for col in (1, 2, 3, 4, 5):
            cpct = 100 * col_counts[col] / total_varga
            row += f"  {cpct:>4.1f}%"
        row += f"  {total_varga:>10}"
        print(row)
    print()
    print("Prediction: 1-akṣara cohort should show highest C1 share, "
          "lowest C4 share (purest engineering).")
    print()

    # Place distribution by akṣara count
    print(f"{'Akṣaras':>8}  {'Velar':>8}  {'Palatal':>9}  {'Retroflex':>10}  "
          f"{'Dental':>8}  {'Labial':>8}  {'Total':>8}")
    print("-" * 80)
    for aksh in sorted(by_aksh):
        cohort = by_aksh[aksh]
        place_counts = Counter()
        total_varga = 0
        for s in cohort:
            for ch in s:
                if ch in VARGA_GRID:
                    place, _ = VARGA_GRID[ch]
                    place_counts[place] += 1
                    total_varga += 1
        if total_varga == 0:
            continue
        row = f"  {aksh:>6}  "
        for place in (1, 2, 3, 4, 5):
            ppct = 100 * place_counts[place] / total_varga
            row += f"  {ppct:>6.1f}%"
        row += f"  {total_varga:>8}"
        print(row)
    print()

    # ===== (C) VOWEL × CONSONANT =====
    print("=" * 80)
    print("(C) VOWEL × CONSONANT INTERACTION")
    print("=" * 80)
    print()

    vowel_counts = Counter()
    # For each vowel, count the preceding consonant (or "Ø" if vowel-initial)
    vowel_preceded_by = {v: Counter() for v in VOWELS}

    for _, _, structural in dhatus:
        for idx, ch in enumerate(structural):
            if ch in VOWELS:
                vowel_counts[ch] += 1
                if idx > 0 and structural[idx-1] in CONSONANTS:
                    vowel_preceded_by[ch][structural[idx-1]] += 1
                else:
                    vowel_preceded_by[ch]["Ø"] += 1

    total_vowels = sum(vowel_counts.values())

    print("OVERALL VOWEL DISTRIBUTION")
    print(f"{'IAST':>6}  {'SLP1':>6}  {'Count':>7}  {'% of vowels':>12}")
    print("-" * 60)
    for v, count in vowel_counts.most_common():
        iast = SLP1_TO_IAST.get(v, v)
        pct = 100 * count / total_vowels
        bar = "#" * int(pct * 0.5)
        print(f"  {iast:>4}  {v:>4}  {count:>6}  {pct:>10.1f}%  {bar}")
    print()

    print("TOP CONSONANTS PRECEDING EACH MAJOR VOWEL")
    print("(For each top vowel, what's the top 5 of preceding consonants?)")
    print("-" * 60)
    for v, _ in vowel_counts.most_common(8):
        iast_v = SLP1_TO_IAST.get(v, v)
        total_v = vowel_counts[v]
        if total_v == 0:
            continue
        print(f"\n  Vowel {iast_v} ({v}) — total {total_v}:")
        for preceder, count in vowel_preceded_by[v].most_common(5):
            iast_p = SLP1_TO_IAST.get(preceder, preceder)
            pct = 100 * count / total_v
            print(f"    {iast_p:>5} ({preceder:>2}): {count:>4} "
                  f"({pct:>5.1f}%)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
