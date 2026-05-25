#!/usr/bin/env python3
"""
analyze_distinguishability.py — three further analyses on the Dhātupāṭha:

  (A) FEATURE-DISTANCE DISTINGUISHABILITY — quantitative implementation
      of the cost × distinguishability framework.  For each varga
      consonant, compute its mean distance to every other consonant in
      feature space, both via binary Hamming and via perceptually-
      asymmetric weighted distance.  Compute engineering-value =
      distinguishability / (1 + cost) and rank against corpus frequency.

  (B) ONSET-CODA CO-OCCURRENCE — for single-syllable (1-akṣara) dhātus
      with both an initial consonant and a final consonant, look at
      the joint distribution: do initial+final pairs show phonotactic
      harmony, avoidance, or independence?

  (C) CROSS-GAṆA COLUMN DISTRIBUTION — does the column pattern hold
      across all 10 gaṇāḥ, or are there gaṇa-specific signatures?

Reads data/dhatupatha.csv with the standard anubandha-stripping rules.
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

# Varga grid: (place, column)
# Place 1=velar, 2=palatal, 3=retroflex, 4=dental, 5=labial
# Column 1=unv-unasp, 2=unv-asp, 3=voi-unasp, 4=voi-asp, 5=nasal
VARGA_GRID = {
    "k": (1, 1), "K": (1, 2), "g": (1, 3), "G": (1, 4), "N": (1, 5),
    "c": (2, 1), "C": (2, 2), "j": (2, 3), "J": (2, 4), "Y": (2, 5),
    "w": (3, 1), "W": (3, 2), "q": (3, 3), "Q": (3, 4), "R": (3, 5),
    "t": (4, 1), "T": (4, 2), "d": (4, 3), "D": (4, 4), "n": (4, 5),
    "p": (5, 1), "P": (5, 2), "b": (5, 3), "B": (5, 4), "m": (5, 5),
}

NON_VARGA_CONSONANTS = set("yrlv" "SzsH" "h" "M")
CONSONANTS = set(VARGA_GRID.keys()) | NON_VARGA_CONSONANTS

SLP1_TO_IAST = {
    "k": "k", "K": "kh", "g": "g", "G": "gh", "N": "ṅ",
    "c": "c", "C": "ch", "j": "j", "J": "jh", "Y": "ñ",
    "w": "ṭ", "W": "ṭh", "q": "ḍ", "Q": "ḍh", "R": "ṇ",
    "t": "t", "T": "th", "d": "d", "D": "dh", "n": "n",
    "p": "p", "P": "ph", "b": "b", "B": "bh", "m": "m",
    "y": "y", "r": "r", "l": "l", "v": "v",
    "S": "ś", "z": "ṣ", "s": "s", "h": "h",
    "M": "ṃ", "H": "ḥ",
}

# --- Feature vector for each varga consonant ---------------------------

def features(ch: str) -> dict:
    """Return feature dict for a varga consonant."""
    if ch not in VARGA_GRID:
        return None
    place, col = VARGA_GRID[ch]
    # Column 1: unv-unasp; 2: unv-asp; 3: voi-unasp; 4: voi-asp; 5: nasal
    voiced = col in (3, 4, 5)
    aspirated = col in (2, 4)
    nasal = col == 5
    return {
        "place": place,
        "voiced": voiced,
        "aspirated": aspirated,
        "nasal": nasal,
        "column": col,
    }


def hamming_distance(c1: str, c2: str) -> int:
    """Simple binary feature distance: count of features that differ."""
    f1, f2 = features(c1), features(c2)
    if f1 is None or f2 is None:
        return -1
    d = 0
    if f1["place"] != f2["place"]:
        d += 1
    if f1["voiced"] != f2["voiced"]:
        d += 1
    if f1["aspirated"] != f2["aspirated"]:
        d += 1
    if f1["nasal"] != f2["nasal"]:
        d += 1
    return d


def weighted_distance(c1: str, c2: str) -> float:
    """
    Perceptually-weighted feature distance.

    Weights:
      place: 1.0 if different
      voicing: 1.5 if different
      aspiration: 0.5 if both consonants are voiceless (kh vs k is subtle),
                  1.5 if both consonants are voiced (gh vs g — breathy voice
                  is highly salient), 1.0 for cross-voicing comparisons
      nasal: 1.5 if different (nasal coupling is highly salient)
    """
    f1, f2 = features(c1), features(c2)
    if f1 is None or f2 is None:
        return -1.0
    d = 0.0
    if f1["place"] != f2["place"]:
        d += 1.0
    if f1["voiced"] != f2["voiced"]:
        d += 1.5
    if f1["aspirated"] != f2["aspirated"]:
        # Asymmetric: voiced-aspiration is more salient than voiceless-aspiration
        if f1["voiced"] and f2["voiced"]:
            d += 1.5
        elif (not f1["voiced"]) and (not f2["voiced"]):
            d += 0.5
        else:
            d += 1.0
    if f1["nasal"] != f2["nasal"]:
        d += 1.5
    return d


def cost(ch: str) -> float:
    """
    Articulatory cost of producing a consonant — sum of marked features.
      Voicing: 1.5
      Aspiration: 0.5 if voiceless, 1.5 if voiced (asymmetric — breathy voice
                  is articulatorily harder to produce than aspiration alone)
      Nasal: 1.5 if nasal
      Place: 0 (all places equally costly at baseline)
    C1 has cost 0; C5 has cost ~1.5 (nasal only); C4 has cost ~3.0 (voiced + voiced-asp)
    """
    f = features(ch)
    if f is None:
        return -1.0
    c = 0.0
    if f["voiced"] and not f["nasal"]:
        c += 1.5
    if f["aspirated"]:
        c += 1.5 if f["voiced"] else 0.5
    if f["nasal"]:
        c += 1.5
    return c


# --- Anubandha stripping -----------------------------------------------

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


def count_aksharas(s: str) -> int:
    return sum(1 for c in s if c in VOWELS)


def initial_cluster(s: str) -> str:
    out = []
    for ch in s:
        if ch in CONSONANTS:
            out.append(ch)
        else:
            break
    return "".join(out)


def final_cluster(s: str) -> str:
    out = []
    for ch in reversed(s):
        if ch in CONSONANTS:
            out.append(ch)
        else:
            break
    return "".join(reversed(out))


def spearman_correlation(xs: list[float], ys: list[float]) -> float:
    """Compute Spearman rank correlation between two equal-length lists."""
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    rank_x = {v: r for r, v in enumerate(sorted(set(xs)))}
    rank_y = {v: r for r, v in enumerate(sorted(set(ys)))}
    rx = [rank_x[x] for x in xs]
    ry = [rank_y[y] for y in ys]
    n = len(xs)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    var_x = sum((r - mean_rx) ** 2 for r in rx) ** 0.5
    var_y = sum((r - mean_ry) ** 2 for r in ry) ** 0.5
    if var_x == 0 or var_y == 0:
        return 0.0
    return num / (var_x * var_y)


# --- Main analysis -----------------------------------------------------

def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found at {DATA_FILE}", file=sys.stderr)
        return 1

    # Read corpus
    dhatus_all = []   # (gana, structural)
    with DATA_FILE.open() as fh:
        for row in csv.reader(fh):
            if len(row) < 3 or not row[0].isdigit():
                continue
            gana = int(row[0])
            structural = strip_anubandhas(row[2].strip())
            if structural:
                dhatus_all.append((gana, structural))

    # Gaṇa 1 subset for main analysis (the primary engineered class)
    dhatus_g1 = [(g, s) for g, s in dhatus_all if g == 1]

    # --- Consonant frequency in gaṇa 1 ---
    cons_freq = Counter()
    for _, s in dhatus_g1:
        for ch in s:
            if ch in VARGA_GRID:
                cons_freq[ch] += 1
    total_varga_g1 = sum(cons_freq.values())

    # =====================================================================
    # (A) Feature-distance distinguishability
    # =====================================================================
    print("=" * 80)
    print("(A) FEATURE-DISTANCE DISTINGUISHABILITY — quantitative test of")
    print("    cost × distinguishability hypothesis")
    print(f"    (gaṇa 1; {total_varga_g1} varga-consonant occurrences across "
          f"{len(dhatus_g1)} dhātus)")
    print("=" * 80)
    print()

    # For each varga consonant, compute mean distance (binary + weighted)
    # to all 24 OTHER varga consonants
    all_cons = sorted(VARGA_GRID.keys(),
                      key=lambda c: (VARGA_GRID[c][0], VARGA_GRID[c][1]))
    metrics = []  # list of dicts per consonant
    for c in all_cons:
        h_distances = [hamming_distance(c, c2) for c2 in all_cons if c2 != c]
        w_distances = [weighted_distance(c, c2) for c2 in all_cons if c2 != c]
        mean_h = sum(h_distances) / len(h_distances)
        mean_w = sum(w_distances) / len(w_distances)
        min_w = min(w_distances)
        c_cost = cost(c)
        freq = cons_freq.get(c, 0)
        pct = 100 * freq / total_varga_g1 if total_varga_g1 else 0
        # Engineering value = distinguishability / (1 + cost)
        eng_value = mean_w / (1 + c_cost)
        metrics.append({
            "c": c, "iast": SLP1_TO_IAST[c],
            "place": VARGA_GRID[c][0], "col": VARGA_GRID[c][1],
            "cost": c_cost, "mean_h": mean_h, "mean_w": mean_w,
            "min_w": min_w, "eng_value": eng_value,
            "freq": freq, "pct": pct,
        })

    # Print table sorted by frequency
    print(f"{'IAST':>5} {'SLP1':>5} {'Place':>10} {'Col':>4} "
          f"{'Cost':>5} {'MeanH':>6} {'MeanW':>6} {'MinW':>5} "
          f"{'EngVal':>7} {'Freq':>5} {'%':>6}")
    print("-" * 80)
    place_names = {1: "velar", 2: "palatal", 3: "retroflex", 4: "dental",
                   5: "labial"}
    for m in sorted(metrics, key=lambda m: -m["freq"]):
        print(f"{m['iast']:>5} {m['c']:>5} {place_names[m['place']]:>10} "
              f"{m['col']:>4} {m['cost']:>5.1f} {m['mean_h']:>6.2f} "
              f"{m['mean_w']:>6.2f} {m['min_w']:>5.1f} "
              f"{m['eng_value']:>7.2f} {m['freq']:>5} {m['pct']:>5.1f}%")
    print()

    # Spearman rank correlations
    freqs = [m["freq"] for m in metrics]
    cor_eng = spearman_correlation([m["eng_value"] for m in metrics], freqs)
    cor_mw = spearman_correlation([m["mean_w"] for m in metrics], freqs)
    cor_cost = spearman_correlation([m["cost"] for m in metrics], freqs)
    cor_mh = spearman_correlation([m["mean_h"] for m in metrics], freqs)
    print("SPEARMAN RANK CORRELATIONS WITH FREQUENCY")
    print(f"  Engineering value (mean_w / (1 + cost))    ρ = {cor_eng:+.3f}")
    print(f"  Mean weighted distance (distinguishability)  ρ = {cor_mw:+.3f}")
    print(f"  Mean binary Hamming distance                 ρ = {cor_mh:+.3f}")
    print(f"  Cost (negative correlation expected)         ρ = {cor_cost:+.3f}")
    print()
    print("  Interpretation:")
    print("    ρ > +0.3 : moderate-to-strong positive predictor")
    print("    |ρ| < 0.2: weak / unclear predictor")
    print("    Cost ρ should be NEGATIVE if cheap consonants are preferred")
    print()

    # =====================================================================
    # (B) Onset-coda co-occurrence (1-akṣara dhātus with both)
    # =====================================================================
    print("=" * 80)
    print("(B) ONSET-CODA CO-OCCURRENCE in 1-akṣara dhātus")
    print("=" * 80)
    print()

    # For 1-akṣara dhātus only — exclude 2+ akṣara forms
    onset_coda_pairs = []  # (initial_col, final_col, initial_place, final_place)
    for _, s in dhatus_g1:
        if count_aksharas(s) != 1:
            continue
        ini = initial_cluster(s)
        fin = final_cluster(s)
        if not ini or not fin:
            continue
        # Use just the FIRST char of the initial cluster and the LAST of the
        # final cluster (the "outermost" consonants)
        i_ch = ini[0]
        f_ch = fin[-1]
        if i_ch in VARGA_GRID and f_ch in VARGA_GRID:
            i_place, i_col = VARGA_GRID[i_ch]
            f_place, f_col = VARGA_GRID[f_ch]
            onset_coda_pairs.append({
                "initial": i_ch, "final": f_ch,
                "i_place": i_place, "i_col": i_col,
                "f_place": f_place, "f_col": f_col,
            })
    n_pairs = len(onset_coda_pairs)
    print(f"Pairs analyzed: {n_pairs} (1-akṣara dhātus with both initial "
          f"and final varga consonants)")
    print()

    # Place harmony test
    same_place = sum(1 for p in onset_coda_pairs
                     if p["i_place"] == p["f_place"])
    place_pct = 100 * same_place / n_pairs if n_pairs else 0
    # Expected under independence: probability of same place by chance
    place_marginal = Counter(p["i_place"] for p in onset_coda_pairs)
    expected_same_place = sum((c / n_pairs) ** 2 for c in place_marginal.values()) * 100
    print(f"PLACE HARMONY: how often is the initial place = final place?")
    print(f"  Observed: {same_place}/{n_pairs} = {place_pct:.1f}%")
    print(f"  Expected (if independent): ≈ {expected_same_place:.1f}%")
    if place_pct > expected_same_place + 2:
        print(f"  → MODEST HARMONY (place tends to repeat)")
    elif place_pct < expected_same_place - 2:
        print(f"  → AVOIDANCE (place tends to differ)")
    else:
        print(f"  → INDEPENDENCE")
    print()

    # Voicing harmony test
    same_voicing = sum(
        1 for p in onset_coda_pairs
        if features(p["initial"])["voiced"] == features(p["final"])["voiced"]
    )
    voicing_pct = 100 * same_voicing / n_pairs if n_pairs else 0
    # Independence baseline:
    p_init_voiced = sum(1 for p in onset_coda_pairs
                        if features(p["initial"])["voiced"]) / n_pairs
    p_fin_voiced = sum(1 for p in onset_coda_pairs
                       if features(p["final"])["voiced"]) / n_pairs
    expected_voicing = (p_init_voiced * p_fin_voiced
                        + (1 - p_init_voiced) * (1 - p_fin_voiced)) * 100
    print(f"VOICING HARMONY: how often does initial-voicing = final-voicing?")
    print(f"  Observed: {same_voicing}/{n_pairs} = {voicing_pct:.1f}%")
    print(f"  Expected (if independent): ≈ {expected_voicing:.1f}%")
    if voicing_pct > expected_voicing + 2:
        print(f"  → HARMONY (voicing tends to match)")
    elif voicing_pct < expected_voicing - 2:
        print(f"  → AVOIDANCE")
    else:
        print(f"  → INDEPENDENCE")
    print()

    # Column distribution: initial column vs final column
    print("INITIAL COLUMN × FINAL COLUMN MATRIX")
    print("Cell counts; row = initial column, col = final column")
    matrix = Counter()
    row_totals = Counter()
    col_totals = Counter()
    for p in onset_coda_pairs:
        matrix[(p["i_col"], p["f_col"])] += 1
        row_totals[p["i_col"]] += 1
        col_totals[p["f_col"]] += 1
    print(f"{'I↓ F→':>6} {'C1':>6} {'C2':>6} {'C3':>6} {'C4':>6} {'C5':>6} "
          f"{'Total':>7}")
    for ic in (1, 2, 3, 4, 5):
        row_str = f"  {f'C{ic}':>4} "
        for fc in (1, 2, 3, 4, 5):
            row_str += f" {matrix[(ic, fc)]:>5}"
        row_str += f"  {row_totals[ic]:>6}"
        print(row_str)
    totals_row = "  Tot. "
    for fc in (1, 2, 3, 4, 5):
        totals_row += f" {col_totals[fc]:>5}"
    totals_row += f"  {n_pairs:>6}"
    print(totals_row)
    print()

    # =====================================================================
    # (C) Cross-gaṇa column distribution
    # =====================================================================
    print("=" * 80)
    print("(C) CROSS-GAṆA COLUMN DISTRIBUTION")
    print("    Does the column pattern hold across all 10 gaṇāḥ?")
    print("=" * 80)
    print()

    by_gana_cols = {g: Counter() for g in range(1, 11)}
    by_gana_total = Counter()
    by_gana_dhatus = Counter()
    for g, s in dhatus_all:
        by_gana_dhatus[g] += 1
        for ch in s:
            if ch in VARGA_GRID:
                _, col = VARGA_GRID[ch]
                by_gana_cols[g][col] += 1
                by_gana_total[g] += 1

    gana_names = {1: "bhvādi", 2: "adādi", 3: "juhotyādi", 4: "divādi",
                  5: "svādi", 6: "tudādi", 7: "rudhādi", 8: "tanādi",
                  9: "kryādi", 10: "curādi"}

    print(f"{'Gaṇa':>4} {'Class':>12} {'Dhātus':>8} {'Varga':>7} "
          f"{'C1':>6} {'C2':>6} {'C3':>6} {'C4':>6} {'C5':>6}")
    print("-" * 80)
    for g in range(1, 11):
        if by_gana_total[g] == 0:
            continue
        total = by_gana_total[g]
        row_str = (f"  {g:>2} {gana_names[g]:>12} "
                   f"{by_gana_dhatus[g]:>8} {total:>7} ")
        for col in (1, 2, 3, 4, 5):
            cpct = 100 * by_gana_cols[g][col] / total
            row_str += f" {cpct:>5.1f}%"
        print(row_str)
    print()

    # Variance check — how stable is the ordering?
    print("ORDERING CHECK — does C1 > C3 > C5 > C4 > C2 hold across gaṇas?")
    print("-" * 80)
    for g in range(1, 11):
        if by_gana_total[g] == 0:
            continue
        counts = [(col, by_gana_cols[g][col]) for col in (1, 2, 3, 4, 5)]
        counts.sort(key=lambda x: -x[1])
        ordering = " > ".join(f"C{c}" for c, _ in counts)
        matches = ordering.startswith("C1")
        print(f"  Gaṇa {g:>2} ({gana_names[g]:>12}): {ordering} "
              f"{'✓' if matches else '✗ (C1 not first)'}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
