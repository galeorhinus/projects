#!/usr/bin/env python3
"""
analyze_varga_distribution.py — varga-column + positional analysis of
the Pāṇinian Dhātupāṭha.

For each consonant in each (anubandha-stripped) dhātu, determine:

  (a) Its varga column — C1 (unvoiced unaspirated), C2 (unvoiced
      aspirated), C3 (voiced unaspirated), C4 (voiced aspirated),
      C5 (nasal); or "non-varga" for semivowels, sibilants, h.
  (b) Its position in the dhātu — initial (first char), final
      (last char), or medial (in between).

Outputs:
  - Overall column distribution (Prediction 1 — articulatory
    simplicity gradient: C1 > C2 ≈ C3 > C4).
  - Position-specific column distribution (Prediction 2 — nasals
    cluster in final position; Prediction 3 — initial position
    favors C1).
  - For each column, the position breakdown (where does C1 most
    often appear? where do nasals?).

Reads data/dhatupatha.csv with the same anubandha-stripping rules as
analyze_dhatupatha.py (Aṣṭādhyāyī 1.3.2 + 1.3.3 + 1.3.5).
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

# Varga columns — mapped from SLP1 char to (varga-row, column-number)
# Column 1: unvoiced unaspirated (k, c, ṭ, t, p)
# Column 2: unvoiced aspirated   (K, C, W, T, P)
# Column 3: voiced unaspirated   (g, j, q, d, b)
# Column 4: voiced aspirated     (G, J, Q, D, B)
# Column 5: nasal                (N, Y, R, n, m)

VARGA_COLUMNS = {
    # ka-varga
    "k": 1, "K": 2, "g": 3, "G": 4, "N": 5,
    # ca-varga
    "c": 1, "C": 2, "j": 3, "J": 4, "Y": 5,
    # ṭa-varga (retroflex)
    "w": 1, "W": 2, "q": 3, "Q": 4, "R": 5,
    # ta-varga (dental)
    "t": 1, "T": 2, "d": 3, "D": 4, "n": 5,
    # pa-varga (labial)
    "p": 1, "P": 2, "b": 3, "B": 4, "m": 5,
}

NON_VARGA_CONSONANTS = set("yrlv" "SzsH" "h" "M")

COLUMN_NAMES = {
    1: "C1 (unvoiced unaspirated — k, c, ṭ, t, p)",
    2: "C2 (unvoiced aspirated — kh, ch, ṭh, th, ph)",
    3: "C3 (voiced unaspirated — g, j, ḍ, d, b)",
    4: "C4 (voiced aspirated — gh, jh, ḍh, dh, bh)",
    5: "C5 (nasal — ṅ, ñ, ṇ, n, m)",
}

# --- Anubandha stripping (matches analyze_dhatupatha.py) ----------------

# Anubandha-stripping logic lives in decompose_dhatupatha.py (single source
# of truth). Re-exported here so callers downstream get the corrected
# `~`-marker-aware implementation automatically.
import importlib.util as _ilu
_dpath = Path(__file__).resolve().parent / "decompose_dhatupatha.py"
_spec = _ilu.spec_from_file_location("_decompose", _dpath)
_decompose = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_decompose)
strip_markers = _decompose.strip_markers
strip_anubandhas = _decompose.strip_anubandhas
SHORT_VOWEL_ANUBANDHAS = _decompose.SHORT_VOWEL_ANUBANDHAS
INITIAL_ANUBANDHAS_2CHAR = _decompose.INITIAL_ANUBANDHAS_2CHAR
TRAILING_CONSONANT_ANUBANDHAS = _decompose.TRAILING_CONSONANT_ANUBANDHAS
ALL_MARKERS = _decompose.ALL_MARKERS


# --- Analysis -----------------------------------------------------------

def classify_consonant(c: str) -> int | None:
    """Return varga column 1-5, or None for non-varga consonant."""
    return VARGA_COLUMNS.get(c)


def position_in_dhatu(idx: int, length: int) -> str:
    """Return 'initial', 'final', or 'medial' for the char at idx."""
    if idx == 0:
        return "initial"
    if idx == length - 1:
        return "final"
    return "medial"


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found at {DATA_FILE}", file=sys.stderr)
        return 1

    # Optional gaṇa filter from CLI arg (e.g. `python ... 1` for gaṇa 1 only,
    # `python ... 10` for gaṇa 10 only). No arg → all gaṇas.
    gana_filter: int | None = None
    if len(sys.argv) > 1:
        try:
            gana_filter = int(sys.argv[1])
        except ValueError:
            print(f"Invalid gaṇa filter: {sys.argv[1]}", file=sys.stderr)
            return 1

    # Collect every (column, position) tuple for every varga consonant
    column_counts = Counter()
    position_counts = Counter()  # by (column, position)
    initial_consonant_counts = Counter()  # consonants in position 0
    final_consonant_counts = Counter()    # consonants at last position
    medial_consonant_counts = Counter()
    non_varga_counts = Counter()  # SLP1 char -> count of non-varga consonants

    total_dhatus = 0
    total_consonants = 0
    total_varga_consonants = 0
    total_non_varga_consonants = 0

    with DATA_FILE.open() as fh:
        for row in csv.reader(fh):
            if len(row) < 3 or not row[0].isdigit():
                continue
            gana = int(row[0])
            if gana_filter is not None and gana != gana_filter:
                continue
            original = row[2].strip()
            structural = strip_anubandhas(original)
            if not structural:
                continue
            total_dhatus += 1

            length = len(structural)
            for idx, ch in enumerate(structural):
                if ch in VOWELS:
                    continue
                if ch in CONSONANTS:
                    total_consonants += 1
                    pos = position_in_dhatu(idx, length)
                    col = classify_consonant(ch)
                    if col is not None:
                        total_varga_consonants += 1
                        column_counts[col] += 1
                        position_counts[(col, pos)] += 1
                        if pos == "initial":
                            initial_consonant_counts[col] += 1
                        elif pos == "final":
                            final_consonant_counts[col] += 1
                        else:
                            medial_consonant_counts[col] += 1
                    else:
                        total_non_varga_consonants += 1
                        non_varga_counts[ch] += 1

    # --- Report ---
    print("=" * 75)
    print("DHĀTUPĀṬHA — VARGA-COLUMN + POSITIONAL ANALYSIS")
    if gana_filter is not None:
        print(f"(FILTERED TO GAṆA {gana_filter} ONLY)")
    print(f"({total_dhatus} dhātus; {total_consonants} consonant occurrences; "
          f"{total_varga_consonants} are varga, "
          f"{total_non_varga_consonants} non-varga)")
    print("=" * 75)
    print()

    # --- Overall column distribution (Prediction 1) ---
    print("PREDICTION 1 — Articulatory simplicity gradient")
    print("Expected: C1 > C2 ≈ C3 > C4; C5 separate.")
    print("-" * 75)
    print(f"{'Column':<55} {'Count':>7} {'% of varga':>10}")
    for col in (1, 2, 3, 4, 5):
        count = column_counts[col]
        pct = 100 * count / total_varga_consonants
        bar = "#" * int(pct * 0.6)
        print(f"  {COLUMN_NAMES[col]:<53} {count:>7} {pct:>9.1f}%  {bar}")
    print()

    # --- Position breakdown by column (Predictions 2 + 3) ---
    print("POSITION BREAKDOWN BY COLUMN")
    print("For each column, what % of its consonants sit in initial / "
          "medial / final position?")
    print("-" * 75)
    print(f"{'Column':<55} {'Initial':>8} {'Medial':>8} {'Final':>7}")
    for col in (1, 2, 3, 4, 5):
        total_col = column_counts[col]
        if total_col == 0:
            continue
        ini = position_counts[(col, "initial")]
        med = position_counts[(col, "medial")]
        fin = position_counts[(col, "final")]
        print(f"  {COLUMN_NAMES[col]:<53} "
              f"{100*ini/total_col:>7.1f}% "
              f"{100*med/total_col:>7.1f}% "
              f"{100*fin/total_col:>6.1f}%")
    print()

    # --- Column distribution within each position ---
    print("COLUMN DISTRIBUTION WITHIN EACH POSITION")
    print("Of all initial varga consonants, what % is each column? "
          "(Same for medial / final.)")
    print("-" * 75)
    print(f"{'Position':<10} {'C1':>7} {'C2':>7} {'C3':>7} "
          f"{'C4':>7} {'C5':>7}   N")
    for pos, counter in (("initial", initial_consonant_counts),
                         ("medial", medial_consonant_counts),
                         ("final", final_consonant_counts)):
        total_pos = sum(counter.values())
        if total_pos == 0:
            continue
        row = f"  {pos:<8}"
        for col in (1, 2, 3, 4, 5):
            pct = 100 * counter[col] / total_pos
            row += f"  {pct:>5.1f}%"
        row += f"   {total_pos}"
        print(row)
    print()

    # --- Headline predictions check ---
    print("=" * 75)
    print("HEADLINE COMPARISON TO PREDICTIONS")
    print("=" * 75)

    c1 = column_counts[1]
    c2 = column_counts[2]
    c3 = column_counts[3]
    c4 = column_counts[4]
    c5 = column_counts[5]
    pct = lambda n: 100 * n / total_varga_consonants

    print()
    print("PREDICTION 1 — C1 should dominate; C4 should be rarest.")
    ranking = sorted(((c1, "C1"), (c2, "C2"), (c3, "C3"),
                      (c4, "C4"), (c5, "C5")), reverse=True)
    print(f"  Actual ranking (most → least common):")
    for n, label in ranking:
        print(f"    {label}: {n} ({pct(n):.1f}%)")
    print(f"  → C1 most common? {ranking[0][1] == 'C1'}")
    print(f"  → C4 rarest? {ranking[-1][1] == 'C4'}")
    print()

    # Prediction 2 — nasals in final position
    nasal_total = column_counts[5]
    nasal_final = position_counts[(5, "final")]
    print("PREDICTION 2 — Nasals (C5) should cluster in final position.")
    if nasal_total > 0:
        print(f"  Of all nasal consonants ({nasal_total} total):")
        print(f"    Initial: {position_counts[(5, 'initial')]} "
              f"({100*position_counts[(5,'initial')]/nasal_total:.1f}%)")
        print(f"    Medial:  {position_counts[(5, 'medial')]} "
              f"({100*position_counts[(5,'medial')]/nasal_total:.1f}%)")
        print(f"    Final:   {nasal_final} ({100*nasal_final/nasal_total:.1f}%)")
    total_final = sum(final_consonant_counts.values())
    if total_final > 0:
        print(f"  Of all final-position varga consonants ({total_final}):")
        for col in (1, 2, 3, 4, 5):
            print(f"    {COLUMN_NAMES[col][:30]}: "
                  f"{final_consonant_counts[col]} "
                  f"({100*final_consonant_counts[col]/total_final:.1f}%)")
    print()

    # Prediction 3 — initial position favors C1
    total_initial = sum(initial_consonant_counts.values())
    print("PREDICTION 3 — Initial position should favor C1; avoid C4.")
    if total_initial > 0:
        print(f"  Of all initial-position varga consonants ({total_initial}):")
        for col in (1, 2, 3, 4, 5):
            print(f"    {COLUMN_NAMES[col][:30]}: "
                  f"{initial_consonant_counts[col]} "
                  f"({100*initial_consonant_counts[col]/total_initial:.1f}%)")
    print()

    # --- Non-varga consonants (for completeness) ---
    print("NON-VARGA CONSONANTS (semivowels / sibilants / h / anusvara)")
    print("-" * 75)
    for ch, count in non_varga_counts.most_common():
        names = {
            "y": "y (palatal semivowel)", "r": "r (retroflex semivowel)",
            "l": "l (dental semivowel)", "v": "v (labial semivowel)",
            "S": "ś (palatal sibilant)", "z": "ṣ (retroflex sibilant)",
            "s": "s (dental sibilant)", "h": "h (aspirate)",
            "M": "ṃ (anusvāra)", "H": "ḥ (visarga)",
        }
        name = names.get(ch, ch)
        pct = 100 * count / total_non_varga_consonants
        print(f"  {name:<35} {count:>5} ({pct:>5.1f}%)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
