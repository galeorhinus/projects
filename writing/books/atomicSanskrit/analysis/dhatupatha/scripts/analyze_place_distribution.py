#!/usr/bin/env python3
"""
analyze_place_distribution.py — place-of-articulation (sthāna) ×
position analysis of the Dhātupāṭha, plus specific-consonant
frequency rankings.

For each varga consonant occurrence:
  - Identify its sthāna (place): velar, palatal, retroflex,
    dental, or labial.
  - Identify its position in the dhātu: initial / medial / final.
  - Identify its varga column (1-5) too for cross-tab.

Reports:
  - Overall place distribution.
  - Place × position breakdown.
  - Top-frequency specific consonants.
  - Place × column cross-tab (which (row, col) cells are populated
    most heavily).

Supports gaṇa-filtering via CLI arg (e.g., `python ... 1`).
Reuses the anubandha-stripping logic from analyze_varga_distribution.py.
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

# Map each varga consonant to (place, column)
# Places: 1=velar (kaṇṭhya), 2=palatal (tālavya), 3=retroflex (mūrdhanya),
#         4=dental (dantya), 5=labial (oṣṭhya)
# Columns: 1=unv-unasp, 2=unv-asp, 3=voi-unasp, 4=voi-asp, 5=nasal
VARGA_GRID = {
    # ka-varga (velar)
    "k": (1, 1), "K": (1, 2), "g": (1, 3), "G": (1, 4), "N": (1, 5),
    # ca-varga (palatal)
    "c": (2, 1), "C": (2, 2), "j": (2, 3), "J": (2, 4), "Y": (2, 5),
    # ṭa-varga (retroflex)
    "w": (3, 1), "W": (3, 2), "q": (3, 3), "Q": (3, 4), "R": (3, 5),
    # ta-varga (dental)
    "t": (4, 1), "T": (4, 2), "d": (4, 3), "D": (4, 4), "n": (4, 5),
    # pa-varga (labial)
    "p": (5, 1), "P": (5, 2), "b": (5, 3), "B": (5, 4), "m": (5, 5),
}

NON_VARGA_CONSONANTS = set("yrlv" "SzsH" "h" "M")
CONSONANTS = set(VARGA_GRID.keys()) | NON_VARGA_CONSONANTS

PLACE_NAMES = {
    1: "Velar (kaṇṭhya — k, kh, g, gh, ṅ)",
    2: "Palatal (tālavya — c, ch, j, jh, ñ)",
    3: "Retroflex (mūrdhanya — ṭ, ṭh, ḍ, ḍh, ṇ)",
    4: "Dental (dantya — t, th, d, dh, n)",
    5: "Labial (oṣṭhya — p, ph, b, bh, m)",
}

SLP1_TO_IAST = {
    "k": "k", "K": "kh", "g": "g", "G": "gh", "N": "ṅ",
    "c": "c", "C": "ch", "j": "j", "J": "jh", "Y": "ñ",
    "w": "ṭ", "W": "ṭh", "q": "ḍ", "Q": "ḍh", "R": "ṇ",
    "t": "t", "T": "th", "d": "d", "D": "dh", "n": "n",
    "p": "p", "P": "ph", "b": "b", "B": "bh", "m": "m",
}

# --- Anubandha stripping (matches analyze_varga_distribution.py) --------

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


def position_in_dhatu(idx: int, length: int) -> str:
    if idx == 0:
        return "initial"
    if idx == length - 1:
        return "final"
    return "medial"


# --- Analysis -----------------------------------------------------------

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

    # Counters
    place_counts = Counter()  # by place
    place_position_counts = Counter()  # by (place, position)
    place_column_counts = Counter()    # by (place, column) — 5x5 grid
    specific_consonant_counts = Counter()  # SLP1 char → count
    specific_consonant_position = Counter()  # (SLP1 char, position) → count

    total_dhatus = 0
    total_varga = 0

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
                if ch not in VARGA_GRID:
                    continue
                place, column = VARGA_GRID[ch]
                pos = position_in_dhatu(idx, length)
                place_counts[place] += 1
                place_position_counts[(place, pos)] += 1
                place_column_counts[(place, column)] += 1
                specific_consonant_counts[ch] += 1
                specific_consonant_position[(ch, pos)] += 1
                total_varga += 1

    # --- Report ---
    print("=" * 80)
    print("DHĀTUPĀṬHA — PLACE × POSITION + SPECIFIC CONSONANT ANALYSIS")
    if gana_filter is not None:
        print(f"(FILTERED TO GAṆA {gana_filter} ONLY)")
    print(f"({total_dhatus} dhātus; {total_varga} varga consonant occurrences)")
    print("=" * 80)
    print()

    # P1 — Overall place distribution
    print("PREDICTION 1 — All 5 places roughly comparable (~20% each); "
          "retroflex slightly under.")
    print("-" * 80)
    print(f"{'Place':<48} {'Count':>7} {'% of varga':>11}")
    for place in (1, 2, 3, 4, 5):
        count = place_counts[place]
        pct = 100 * count / total_varga
        bar = "#" * int(pct * 0.5)
        print(f"  {PLACE_NAMES[place]:<46} {count:>7} {pct:>10.1f}%  {bar}")
    print()

    # Place × position breakdown
    print("PLACE × POSITION BREAKDOWN")
    print("For each place, what % of its consonants sit in initial / medial / final?")
    print("-" * 80)
    print(f"{'Place':<48} {'Initial':>8} {'Medial':>8} {'Final':>7}")
    for place in (1, 2, 3, 4, 5):
        total_place = place_counts[place]
        if total_place == 0:
            continue
        ini = place_position_counts[(place, "initial")]
        med = place_position_counts[(place, "medial")]
        fin = place_position_counts[(place, "final")]
        print(f"  {PLACE_NAMES[place]:<46} "
              f"{100*ini/total_place:>7.1f}% "
              f"{100*med/total_place:>7.1f}% "
              f"{100*fin/total_place:>6.1f}%")
    print()

    # Place distribution within each position
    print("PLACE DISTRIBUTION WITHIN EACH POSITION")
    print("Of all initial varga consonants, what % is each place? (etc.)")
    print("-" * 80)
    print(f"{'Position':<10} {'Velar':>8} {'Palatal':>9} {'Retroflex':>10} "
          f"{'Dental':>8} {'Labial':>8}   N")
    for pos in ("initial", "medial", "final"):
        total_pos = sum(place_position_counts[(p, pos)] for p in (1, 2, 3, 4, 5))
        if total_pos == 0:
            continue
        row_str = f"  {pos:<8}"
        for place in (1, 2, 3, 4, 5):
            pct = 100 * place_position_counts[(place, pos)] / total_pos
            row_str += f"  {pct:>6.1f}%"
        row_str += f"   {total_pos}"
        print(row_str)
    print()

    # Verdicts
    print("=" * 80)
    print("VERDICTS")
    print("=" * 80)
    print()
    place_pct = {p: 100 * place_counts[p] / total_varga for p in (1, 2, 3, 4, 5)}
    print("P1 — Place uniformity (~20% each); retroflex slightly under?")
    print(f"  Velar {place_pct[1]:.1f}% | Palatal {place_pct[2]:.1f}% | "
          f"Retroflex {place_pct[3]:.1f}% | Dental {place_pct[4]:.1f}% | "
          f"Labial {place_pct[5]:.1f}%")
    print()

    # P2 — Retroflex initial avoidance
    retro_initial = place_position_counts[(3, "initial")]
    retro_total = place_counts[3]
    retro_initial_share = 100 * retro_initial / retro_total if retro_total else 0
    # Compare to other places' initial share
    print("P2 — Retroflex depleted in initial position?")
    print(f"  Retroflex % in initial: {retro_initial_share:.1f}%")
    for place in (1, 2, 3, 4, 5):
        tot = place_counts[place]
        ini = place_position_counts[(place, "initial")]
        if tot:
            share = 100 * ini / tot
            label = "Retroflex" if place == 3 else PLACE_NAMES[place][:8]
            print(f"    {label} → initial: {share:.1f}%")
    print()

    # P3 — Dentals and labials overrepresented in final
    print("P3 — Dentals + Labials overrepresented in final position?")
    print(f"  (Of all final varga consonants, what % is each place?)")
    total_final = sum(place_position_counts[(p, "final")] for p in (1, 2, 3, 4, 5))
    for place in (1, 2, 3, 4, 5):
        fin = place_position_counts[(place, "final")]
        if total_final:
            share = 100 * fin / total_final
            print(f"    {PLACE_NAMES[place][:30]}: {share:.1f}%")
    expected_uniform = 20.0
    print(f"    [if uniform: {expected_uniform:.0f}% each]")
    print()

    # P4 — Palatals depleted in final
    print("P4 — Palatals depleted in final position?")
    palatal_final = place_position_counts[(2, "final")]
    palatal_total = place_counts[2]
    palatal_final_share = (100 * palatal_final / palatal_total
                           if palatal_total else 0)
    print(f"  Palatal % in final: {palatal_final_share:.1f}%")
    for place in (1, 2, 3, 4, 5):
        tot = place_counts[place]
        fin = place_position_counts[(place, "final")]
        if tot:
            share = 100 * fin / tot
            label = "Palatal" if place == 2 else PLACE_NAMES[place][:8]
            print(f"    {label} → final: {share:.1f}%")
    print()

    # Full 5×5 grid: place × column heatmap
    print("=" * 80)
    print("FULL VARGA GRID — counts and % of varga total")
    print("=" * 80)
    print()
    print(f"{'Place':<14} {'C1':>10} {'C2':>10} {'C3':>10} {'C4':>10} {'C5':>10} "
          f"{'Total':>10}")
    print("-" * 80)
    for place in (1, 2, 3, 4, 5):
        row_str = f"{PLACE_NAMES[place][:13]:<14}"
        place_total = place_counts[place]
        for col in (1, 2, 3, 4, 5):
            cnt = place_column_counts[(place, col)]
            pct = 100 * cnt / total_varga
            row_str += f"  {cnt:>4} ({pct:>3.1f}%)"
        pct = 100 * place_total / total_varga
        row_str += f"  {place_total:>4} ({pct:>3.1f}%)"
        print(row_str)
    print()

    # Top specific consonants
    print("=" * 80)
    print("TOP-FREQUENCY SPECIFIC CONSONANTS")
    print("=" * 80)
    print(f"{'Rank':>4} {'IAST':>8} {'SLP1':>6} {'Count':>7} "
          f"{'% varga':>8}  Position breakdown (I/M/F)")
    print("-" * 80)
    for rank, (ch, count) in enumerate(
            specific_consonant_counts.most_common(15), 1):
        iast = SLP1_TO_IAST.get(ch, ch)
        pct = 100 * count / total_varga
        i_cnt = specific_consonant_position[(ch, "initial")]
        m_cnt = specific_consonant_position[(ch, "medial")]
        f_cnt = specific_consonant_position[(ch, "final")]
        ipct = 100 * i_cnt / count
        mpct = 100 * m_cnt / count
        fpct = 100 * f_cnt / count
        print(f"  {rank:>2}.   {iast:>5}   {ch:>4}  {count:>6}  {pct:>6.1f}%  "
              f"{ipct:>4.1f}% / {mpct:>4.1f}% / {fpct:>4.1f}%")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
