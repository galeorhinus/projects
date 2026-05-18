#!/usr/bin/env python3
"""
analyze_internal_structure.py — internal-structure matrices for CV / VC / CVC dhātus.

For each of the three highest-deployment patterns, builds the (consonant × vowel)
or (consonant × vowel × consonant) deployment matrix from the Dhātupāṭha and
reports which combinations the architects engineered vs. which they left empty.

The polemical move: structural patterns in the deployment matrix reveal the
engineering classification axis the architects actually used.

Run: python3 scripts/analyze_internal_structure.py
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

# Import the existing anubandha-aware classifier
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_dhatupatha import strip_anubandhas, strip_markers, classify_phonemes  # noqa

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "dhatupatha.csv"

# SLP1 inventory
VARGAS = [
    ("Velar",     ["k", "K", "g", "G", "N"]),
    ("Palatal",   ["c", "C", "j", "J", "Y"]),
    ("Retroflex", ["w", "W", "q", "Q", "R"]),
    ("Dental",    ["t", "T", "d", "D", "n"]),
    ("Labial",    ["p", "P", "b", "B", "m"]),
]
VARGA_CONS = [c for _, row in VARGAS for c in row]  # 25 ordered
OTHER_CONS = ["y", "r", "l", "v", "S", "z", "s", "h"]  # 8
ALL_CONS = VARGA_CONS + OTHER_CONS  # 33

VOWELS = ["a", "A", "i", "I", "u", "U", "f", "F", "x", "X", "e", "E", "o", "O"]  # 14

# Devanagari display (bare consonant forms — without virama — for table readability)
DEV = {
    # Vowels (standalone forms)
    "a": "अ", "A": "आ", "i": "इ", "I": "ई", "u": "उ", "U": "ऊ",
    "f": "ऋ", "F": "ॠ", "x": "ऌ", "X": "ॡ",
    "e": "ए", "E": "ऐ", "o": "ओ", "O": "औ",
    # Consonants (citation form — inherent vowel implicit per Sanskrit grammatical tradition)
    "k": "क", "K": "ख", "g": "ग", "G": "घ", "N": "ङ",
    "c": "च", "C": "छ", "j": "ज", "J": "झ", "Y": "ञ",
    "w": "ट", "W": "ठ", "q": "ड", "Q": "ढ", "R": "ण",
    "t": "त", "T": "थ", "d": "द", "D": "ध", "n": "न",
    "p": "प", "P": "फ", "b": "ब", "B": "भ", "m": "म",
    "y": "य", "r": "र", "l": "ल", "v": "व",
    "S": "श", "z": "ष", "s": "स", "h": "ह",
}

# Internal-frame varga names (Sanskrit anchor)
VARGA_DEV = {
    "Velar": "कवर्ग",
    "Palatal": "चवर्ग",
    "Retroflex": "टवर्ग",
    "Dental": "तवर्ग",
    "Labial": "पवर्ग",
}

VARGA_OF = {}
for v_name, v_cons in VARGAS:
    for c in v_cons:
        VARGA_OF[c] = v_name

# Full phonetic place-of-articulation map (all 33 consonants), per
# Pāṇinian / Prātiśākhya tradition (Aṣṭādhyāyī 1.1.9 / Pāṇinīya Śikṣā).
# Extends VARGA_OF to include semivowels, sibilants, and h.
PLACE_OF = {
    # Velar / kaṇṭhya (back of mouth + glottis)
    "k": "Velar", "K": "Velar", "g": "Velar", "G": "Velar", "N": "Velar",
    "h": "Velar",
    # Palatal / tālavya (hard palate, mid-mouth)
    "c": "Palatal", "C": "Palatal", "j": "Palatal", "J": "Palatal", "Y": "Palatal",
    "y": "Palatal", "S": "Palatal",
    # Retroflex / mūrdhanya (top of mouth, tongue curled)
    "w": "Retroflex", "W": "Retroflex", "q": "Retroflex", "Q": "Retroflex", "R": "Retroflex",
    "r": "Retroflex", "z": "Retroflex",
    # Dental / dantya (teeth, tongue at upper teeth)
    "t": "Dental", "T": "Dental", "d": "Dental", "D": "Dental", "n": "Dental",
    "l": "Dental", "s": "Dental",
    # Labial / oṣṭhya (lips, front of mouth)
    "p": "Labial", "P": "Labial", "b": "Labial", "B": "Labial", "m": "Labial",
    "v": "Labial",
}

PLACE_DEV = {
    "Velar":     "कण्ठ्य",
    "Palatal":   "तालव्य",
    "Retroflex": "मूर्धन्य",
    "Dental":    "दन्त्य",
    "Labial":    "ओष्ठ्य",
}


def load_dhatus():
    """Read the Dhātupāṭha and group bare forms by structural pattern."""
    by_pattern = defaultdict(list)
    with open(DATA_FILE) as fh:
        for line in fh:
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            gana, idx, slp1 = parts[0], parts[1], parts[2]
            stripped = strip_anubandhas(strip_markers(slp1))
            pat = classify_phonemes(stripped)
            by_pattern[pat].append((gana, idx, stripped))
    return by_pattern


def print_2d_matrix(title, atoms, row_keys, col_keys, row_label, col_label,
                    row_dev=None, col_dev=None, group_rows=None,
                    group_dev=None):
    """Print a row × col deployment matrix in Devanagari."""
    counts = Counter()
    for atom in atoms:
        if len(atom) < 2:
            continue
        r, c = atom[0], atom[1]
        if r in row_keys and c in col_keys:
            counts[(r, c)] += 1

    total = sum(counts.values())
    deployed = len({k for k, v in counts.items() if v > 0})
    space = len(row_keys) * len(col_keys)

    print(f"\n{'=' * 78}")
    print(f"{title}")
    print(f"Atoms in pattern: {len(atoms)}  |  Combinatorial space: {space}")
    print(f"Deployed cells:   {deployed}  ({100 * deployed / space:.1f}% of space)")
    print(f"Total occurrences (incl. duplicates): {total}")
    print(f"{'=' * 78}")

    # Column header (Devanagari)
    col_disp = col_dev or {c: c for c in col_keys}
    print(f"  {row_label:<7s}", end="")
    for c in col_keys:
        print(f" {col_disp[c]:>3s}", end="")
    print("  | row tot")

    def print_row(r):
        rd = row_dev.get(r, r) if row_dev else r
        print(f"  {rd:<7s}", end="")
        row_total = 0
        for c in col_keys:
            n = counts.get((r, c), 0)
            row_total += n
            cell = f"{n:>3d}" if n else "  ."
            print(f" {cell}", end="")
        print(f"  | {row_total:>4d}")

    if group_rows:
        for group_name, group_members in group_rows:
            display_name = (group_dev or {}).get(group_name, group_name)
            print(f"  -- {display_name} --")
            for r in group_members:
                if r in row_keys:
                    print_row(r)
    else:
        for r in row_keys:
            print_row(r)

    # Column totals
    print(f"  {'col tot':<7s}", end="")
    for c in col_keys:
        ct = sum(counts.get((r, c), 0) for r in row_keys)
        print(f" {ct:>3d}", end="")
    print(f"  | {total:>4d}")


def print_cvc_marginals(atoms):
    """For CVC atoms, print marginal distributions in Devanagari."""
    print(f"\n{'=' * 78}")
    print(f"CVC PATTERN — MARGINAL DISTRIBUTIONS")
    print(f"Atoms: {len(atoms)}  |  Combinatorial space: 25 × 14 × 25 = 8,750")
    print(f"{'=' * 78}")

    c1_counter = Counter()
    c2_counter = Counter()
    v_counter = Counter()
    c1c2_counter = Counter()
    varga1_varga2_counter = Counter()

    for atom in atoms:
        if len(atom) < 3:
            continue
        c1, v, c2 = atom[0], atom[1], atom[2]
        c1_counter[c1] += 1
        c2_counter[c2] += 1
        v_counter[v] += 1
        c1c2_counter[(c1, c2)] += 1
        if c1 in VARGA_OF and c2 in VARGA_OF:
            varga1_varga2_counter[(VARGA_OF[c1], VARGA_OF[c2])] += 1

    # C1 distribution
    print("\nInitial consonant (C1) distribution — top 15:")
    for c, n in c1_counter.most_common(15):
        bar = "#" * (n // 5)
        print(f"  {DEV[c]:3s} {n:>4d}  {bar}")

    # C2 distribution
    print("\nFinal consonant (C2) distribution — top 15:")
    for c, n in c2_counter.most_common(15):
        bar = "#" * (n // 5)
        print(f"  {DEV[c]:3s} {n:>4d}  {bar}")

    # Vowel distribution
    print("\nVowel distribution:")
    for v in VOWELS:
        n = v_counter[v]
        bar = "#" * (n // 5)
        if n:
            print(f"  {DEV[v]:3s} {n:>4d}  {bar}")

    # Varga × Varga matrix (compressed 5x5 from 25x25)
    print("\nC1-varga × C2-varga matrix (5x5 compression of C1×C2):")
    varga_names = ["Velar", "Palatal", "Retroflex", "Dental", "Labial"]
    print(f"  {'C1\\C2':<10s}", end="")
    for vn in varga_names:
        dev_name = VARGA_DEV[vn]
        print(f" {dev_name:>7s}", end="")
    print("  | row tot")
    for v1 in varga_names:
        dev1 = VARGA_DEV[v1]
        print(f"  {dev1:<10s}", end="")
        row_tot = 0
        for v2 in varga_names:
            n = varga1_varga2_counter.get((v1, v2), 0)
            row_tot += n
            cell = f"{n:>3d}" if n else "  ."
            print(f"     {cell}", end="")
        print(f"  | {row_tot:>4d}")
    print(f"  {'col tot':<10s}", end="")
    for v2 in varga_names:
        ct = sum(varga1_varga2_counter.get((v1, v2), 0) for v1 in varga_names)
        print(f"     {ct:>3d}", end="")
    print(f"  | {sum(varga1_varga2_counter.values()):>4d}")


def print_2particle_summary(cv_atoms, vc_atoms):
    """Quick comparative summary of the 2-particle patterns."""
    print(f"\n{'=' * 78}")
    print(f"2-PARTICLE PATTERN COMPARISON")
    print(f"{'=' * 78}")
    print(f"  CV:  {len(cv_atoms):>4d} atoms / 350 cells = {100*len(cv_atoms)/350:.1f}% deployed (cells filled may be lower with duplicates)")
    print(f"  VC:  {len(vc_atoms):>4d} atoms / 350 cells = {100*len(vc_atoms)/350:.1f}% deployed")

    cv_cells = len({(a[0], a[1]) for a in cv_atoms if len(a) >= 2})
    vc_cells = len({(a[0], a[1]) for a in vc_atoms if len(a) >= 2})
    print(f"\n  Unique CV cells filled: {cv_cells} / 350 = {100*cv_cells/350:.1f}%")
    print(f"  Unique VC cells filled: {vc_cells} / 350 = {100*vc_cells/350:.1f}%")
    print(f"\n  CV/VC asymmetry: CV is {len(cv_atoms)/max(1,len(vc_atoms)):.2f}× more deployed than VC.")


def main():
    by_pattern = load_dhatus()

    # Extract bare forms
    cv_atoms = [a[2] for a in by_pattern.get("CV", [])]
    vc_atoms = [a[2] for a in by_pattern.get("VC", [])]
    cvc_atoms = [a[2] for a in by_pattern.get("CVC", [])]

    print(f"DHĀTUPĀṬHA INTERNAL-STRUCTURE ANALYSIS")
    print(f"Anubandha-aware classifier from analyze_dhatupatha.py")

    # 2-particle summary
    print_2particle_summary(cv_atoms, vc_atoms)

    # CV matrix
    print_2d_matrix(
        title="CV MATRIX (initial consonant × vowel)",
        atoms=cv_atoms,
        row_keys=ALL_CONS,
        col_keys=VOWELS,
        row_label="व्यञ्जन",
        col_label="स्वर",
        row_dev=DEV,
        col_dev=DEV,
        group_rows=VARGAS + [("Other (य र ल व श ष स ह)", OTHER_CONS)],
        group_dev={**VARGA_DEV, "Other (य र ल व श ष स ह)": "अन्य"},
    )

    # VC matrix
    print_2d_matrix(
        title="VC MATRIX (vowel × final consonant)",
        atoms=vc_atoms,
        row_keys=VOWELS,
        col_keys=ALL_CONS,
        row_label="स्वर",
        col_label="व्यञ्जन",
        row_dev=DEV,
        col_dev=DEV,
    )

    # CVC marginals
    print_cvc_marginals(cvc_atoms)

    # CVC full place-of-articulation matrix (all 33 consonants grouped by place)
    print_cvc_place_matrix(cvc_atoms)


def print_cvc_place_matrix(atoms):
    """C1-place × C2-place matrix using the full phonetic-place classification.

    Unlike the varga-only matrix (25 stops + nasals), this includes all 33
    consonants by their Pāṇinian place-of-articulation:
      Velar / kaṇṭhya: क ख ग घ ङ + ह
      Palatal / tālavya: च छ ज झ ञ + य + श
      Retroflex / mūrdhanya: ट ठ ड ढ ण + र + ष
      Dental / dantya: त थ द ध न + ल + स
      Labial / oṣṭhya: प फ ब भ म + व
    """
    place_names = ["Velar", "Palatal", "Retroflex", "Dental", "Labial"]
    place_counter = Counter()
    c1_place_counter = Counter()
    c2_place_counter = Counter()
    total = 0

    for atom in atoms:
        if len(atom) < 3:
            continue
        c1, v, c2 = atom[0], atom[1], atom[2]
        if c1 in PLACE_OF and c2 in PLACE_OF:
            place_counter[(PLACE_OF[c1], PLACE_OF[c2])] += 1
            c1_place_counter[PLACE_OF[c1]] += 1
            c2_place_counter[PLACE_OF[c2]] += 1
            total += 1

    print(f"\n{'=' * 78}")
    print(f"CVC PATTERN — FULL PHONETIC-PLACE MATRIX (all 33 consonants)")
    print(f"Total CVC atoms classified by place: {total} / {len(atoms)}")
    print(f"{'=' * 78}")

    # Matrix
    print(f"\nC1-place × C2-place matrix:")
    print(f"  {'C1 \\ C2':<14s}", end="")
    for pn in place_names:
        print(f" {PLACE_DEV[pn]:>10s}", end="")
    print("  | row tot")
    print(f"  {'':<14s}", end="")
    for pn in place_names:
        print(f" {'(' + pn[:6] + ')':>10s}", end="")
    print()
    for p1 in place_names:
        print(f"  {PLACE_DEV[p1]:<14s}", end="")
        row_tot = 0
        for p2 in place_names:
            n = place_counter.get((p1, p2), 0)
            row_tot += n
            cell = f"{n:>5d}" if n else "    ."
            print(f"      {cell}", end="")
        print(f"  | {row_tot:>5d}")
    print(f"  {'col tot':<14s}", end="")
    for p2 in place_names:
        ct = sum(place_counter.get((p1, p2), 0) for p1 in place_names)
        print(f"      {ct:>5d}", end="")
    print(f"  | {total:>5d}")

    # Asymmetry ratios per place
    print(f"\nC1 / C2 asymmetry per phonetic place:")
    print(f"  {'Place':<14s} {'C1 tot':>8s} {'C2 tot':>8s} {'C1/C2':>8s}  Preference")
    print(f"  {'-' * 60}")
    for p in place_names:
        c1 = c1_place_counter[p]
        c2 = c2_place_counter[p]
        ratio = c1 / c2 if c2 else float("inf")
        if ratio >= 1.5:
            pref = "strongly INITIAL"
        elif ratio >= 1.15:
            pref = "moderately INITIAL"
        elif ratio <= 1 / 1.5:
            pref = "strongly FINAL"
        elif ratio <= 1 / 1.15:
            pref = "moderately FINAL"
        else:
            pref = "balanced"
        print(f"  {PLACE_DEV[p]:<14s} {c1:>8d} {c2:>8d} {ratio:>8.2f}x  {pref}")


if __name__ == "__main__":
    main()
