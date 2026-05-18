#!/usr/bin/env python3
"""
analyze_dhatupatha.py — structural classification of the Dhātupāṭha.

Reads data/dhatupatha.csv (3 columns: gaṇa-number, position-in-gaṇa,
dhātu-in-SLP1) and produces a structural breakdown by:
  - total count
  - distribution by gaṇa
  - distribution by syllable / akṣara count
  - distribution by phoneme pattern (CV, CVC, CCV, CVCC, CCVC, CCVCC, etc.)
  - distribution by particle count (number of varṇāḥ)

Source: github.com/sanskrit/vyakarana — data/dhatupatha.csv

SLP1 encoding reference:
  Vowels: a A i I u U f F x X e E o O
          (A=ā, I=ī, U=ū, f=ṛ, F=ṝ, x=ḷ, X=ḹ, E=ai, O=au)
  Velar:  k K g G N      (K=kh, G=gh, N=ṅ)
  Palatal: c C j J Y     (C=ch, J=jh, Y=ñ)
  Retroflex: w W q Q R   (w=ṭ, W=ṭh, q=ḍ, Q=ḍh, R=ṇ)
  Dental: t T d D n      (T=th, D=dh)
  Labial: p P b B m      (P=ph, B=bh)
  Semivowels: y r l v
  Sibilants: S z s       (S=ś, z=ṣ)
  Aspirate: h
  Visarga: H   Anusvara: M

Pāṇinian anubandhas (indicatory markers stripped before structural analysis):
  ~ \\ ^ — accent markers (udātta, anudātta, svarita)
  Trailing -a: the inherent vowel carrying the citation form for
               consonant-ending dhātus (so 'gama~' = gam-CVC, not CVCV)
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "dhatupatha.csv"

# SLP1 vowels (single-character codes)
VOWELS = set("aAiIuUfFxXeEoO")

# SLP1 consonants
CONSONANTS = set(
    "kKgGN"     # velar
    "cCjJY"     # palatal
    "wWqQR"     # retroflex
    "tTdDn"     # dental
    "pPbBm"     # labial
    "yrlv"      # semivowel
    "SzsH"      # sibilant + visarga
    "h"         # aspirate
    "M"         # anusvara (treated as consonant for syllable-count purposes)
)

# Strip these accent / indicatory markers before structural analysis
ACCENT_MARKERS = re.compile(r"[~\\^]+$")
ALL_MARKERS = re.compile(r"[~\\^]")


def strip_markers(slp1: str) -> str:
    """Remove accent and indicatory markers from a SLP1 dhātu form."""
    return ALL_MARKERS.sub("", slp1)


# Anubandhas (citation-only markers) per Pāṇini 1.3.2 + 1.3.5.
# Short -a, -i, -u after a consonant are anunāsika in the upadeśa
# tradition and thus anubandhas (1.3.2 — *upadeśe 'janunāsika it*).
# Long vowels and syllabic liquids are root-final and stay.
SHORT_VOWEL_ANUBANDHAS = set("aiu")
ROOT_FINAL_VOWELS = set("AIUfFxXeEoO")  # long ā ī ū, ṛ ṝ ḷ ḹ, e ai o au

# Initial dhātu anubandhas per 1.3.5 (ādir ñiṭuḍavaḥ)
# SLP1: ñi=Ji, ṭu=wu, ḍu=qu
INITIAL_ANUBANDHAS_2CHAR = ("Ji", "wu", "qu")

# Trailing single-consonant anubandhas per 1.3.3 (halantyam) — the
# standard ñit / ṅit / lit / ṣit etc. markers that signal grammatical
# properties (ātmanepadī, vowel-shift behavior, etc.) when they appear
# after a root-final vowel.
TRAILING_CONSONANT_ANUBANDHAS = set("YNlSzwq")


def strip_anubandhas(slp1: str) -> str:
    """
    Apply Pāṇinian it-saṃjñā stripping (1.3.2 + 1.3.5) to the
    accent-stripped SLP1 dhātu citation form.

      - Initial Ji / wu / qu (= ñi / ṭu / ḍu) stripped per 1.3.5
      - Final short -a / -i / -u after consonant stripped per 1.3.2
      - Long / diphthong / syllabic-liquid finals retained (root-final)
    """
    s = slp1

    # Strip initial 2-char anubandhas per 1.3.5
    for prefix in INITIAL_ANUBANDHAS_2CHAR:
        if s.startswith(prefix):
            s = s[len(prefix):]
            break

    # Strip trailing single-consonant anubandha if it sits immediately
    # after a vowel (per 1.3.3 + Pāṇinian-tradition convention for
    # ñit/ṅit/lit/ṣit markers). E.g., qukf\Y → kfY → kf.
    if (len(s) >= 2
            and s[-1] in TRAILING_CONSONANT_ANUBANDHAS
            and s[-2] in VOWELS):
        s = s[:-1]

    # Strip trailing short -a / -i / -u after a consonant per 1.3.2 —
    # BUT only if the remaining form has at least one other vowel.
    # If stripping would leave a consonant-only stem, the short vowel
    # IS the root vowel (e.g., ji, hu, sru, ki, du, ru, yu — all CV roots).
    if (len(s) >= 2
            and s[-1] in SHORT_VOWEL_ANUBANDHAS
            and s[-2] in CONSONANTS):
        remaining = s[:-1]
        if any(c in VOWELS for c in remaining):
            s = remaining

    return s


def classify_phonemes(slp1: str) -> str:
    """
    Return a structural pattern string: 'C' for each consonant,
    'V' for each vowel. Examples:
      'BU'    -> 'CV'      (bhū)
      'gam'   -> 'CVC'     (gam)
      'kfp'   -> 'CVC'     (kṛp)
      'spand' -> 'CCVCC'   (spand)
      'skand' -> 'CCVCC'   (skand)
    """
    pattern = []
    for char in slp1:
        if char in VOWELS:
            pattern.append("V")
        elif char in CONSONANTS:
            pattern.append("C")
        # else: unknown / marker — skip
    return "".join(pattern)


def count_aksharas(pattern: str) -> int:
    """
    Count akṣaras (syllables) = count of V groups, since one akṣara
    has exactly one vowel-nucleus with any number of surrounding
    consonants.
    """
    return pattern.count("V")


def particle_count(pattern: str) -> int:
    """Number of phonemic particles (varṇāḥ) in the dhātu's structural form."""
    return len(pattern)


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found at {DATA_FILE}", file=sys.stderr)
        return 1

    entries: list[tuple[int, int, str, str, str]] = []
    # tuple: (gana, position, original_slp1, stripped_slp1, structural_form)

    with DATA_FILE.open() as fh:
        reader = csv.reader(fh)
        for row in reader:
            if len(row) < 3:
                continue
            try:
                gana = int(row[0])
            except ValueError:
                continue
            position = int(row[1]) if row[1].isdigit() else 0
            original = row[2].strip()
            stripped = strip_markers(original)
            structural = strip_anubandhas(stripped)
            entries.append((gana, position, original, stripped, structural))

    total = len(entries)

    # Distribution by gaṇa
    gana_counts = Counter(e[0] for e in entries)
    gana_names = {
        1: "bhvādi", 2: "adādi", 3: "juhotyādi", 4: "divādi",
        5: "svādi", 6: "tudādi", 7: "rudhādi", 8: "tanādi",
        9: "kryādi", 10: "curādi",
    }

    # Compute pattern + akṣara + particle stats
    patterns = []
    akshara_counts = []
    particle_counts = []
    for gana, pos, orig, strip, struct in entries:
        pat = classify_phonemes(struct)
        patterns.append(pat)
        akshara_counts.append(count_aksharas(pat))
        particle_counts.append(particle_count(pat))

    pattern_dist = Counter(patterns)
    akshara_dist = Counter(akshara_counts)
    particle_dist = Counter(particle_counts)

    # Output report
    print("=" * 70)
    print("DHĀTUPĀṬHA STRUCTURAL ANALYSIS")
    print("Source: github.com/sanskrit/vyakarana — data/dhatupatha.csv")
    print("=" * 70)
    print()

    print(f"TOTAL DHĀTUS: {total}")
    print()

    print("DISTRIBUTION BY GAṆA")
    print("-" * 70)
    for gana in sorted(gana_counts):
        name = gana_names.get(gana, f"gana-{gana}")
        count = gana_counts[gana]
        pct = 100 * count / total
        print(f"  Gana {gana:>2} ({name:<10}): {count:>4} dhātus ({pct:>5.1f}%)")
    print()

    print("DISTRIBUTION BY AKṢARA COUNT (number of vowel-nuclei)")
    print("-" * 70)
    for n in sorted(akshara_dist):
        count = akshara_dist[n]
        pct = 100 * count / total
        bar = "#" * int(pct * 0.6)
        print(f"  {n} akṣara{'s' if n != 1 else ' '}: {count:>4} dhātus ({pct:>5.1f}%) {bar}")
    print()

    print("DISTRIBUTION BY PARTICLE (VARṆA) COUNT")
    print("-" * 70)
    for n in sorted(particle_dist):
        count = particle_dist[n]
        pct = 100 * count / total
        bar = "#" * int(pct * 0.6)
        print(f"  {n} particles: {count:>4} dhātus ({pct:>5.1f}%) {bar}")
    print()

    print("TOP 15 STRUCTURAL PATTERNS")
    print("-" * 70)
    for pat, count in pattern_dist.most_common(15):
        pct = 100 * count / total
        bar = "#" * int(pct * 0.6)
        print(f"  {pat:<10}: {count:>4} dhātus ({pct:>5.1f}%) {bar}")
    print()

    # Summary block — the prose-ready numbers
    print("PROSE-READY SUMMARY")
    print("-" * 70)
    one_akshara = akshara_dist[1]
    two_akshara = akshara_dist[2]
    three_plus = sum(c for n, c in akshara_dist.items() if n >= 3)
    cv_count = pattern_dist.get("CV", 0)
    cvc_count = pattern_dist.get("CVC", 0)
    ccv_count = pattern_dist.get("CCV", 0)
    cvcc_count = pattern_dist.get("CVCC", 0)
    ccvc_count = pattern_dist.get("CCVC", 0)
    ccvcc_count = pattern_dist.get("CCVCC", 0)
    one_part = particle_dist.get(1, 0)
    two_part = particle_dist.get(2, 0)
    three_part = particle_dist.get(3, 0)
    four_part = particle_dist.get(4, 0)
    five_part = particle_dist.get(5, 0)
    six_plus = sum(c for n, c in particle_dist.items() if n >= 6)
    v_count = pattern_dist.get("V", 0)

    print(f"  Total dhātus in the Dhātupāṭha: {total}")
    print(f"  Single-akṣara dhātus: {one_akshara} ({100*one_akshara/total:.1f}%)")
    print(f"  Two-akṣara dhātus:    {two_akshara} ({100*two_akshara/total:.1f}%)")
    print(f"  Three+ akṣara dhātus: {three_plus} ({100*three_plus/total:.1f}%)")
    print()
    print(f"  One-particle dhātus (V):         {one_part} ({100*one_part/total:.1f}%)")
    print(f"  Two-particle dhātus (CV / VC):   {two_part} ({100*two_part/total:.1f}%)")
    print(f"  Three-particle dhātus (CVC etc): {three_part} ({100*three_part/total:.1f}%)")
    print(f"  Four-particle dhātus:            {four_part} ({100*four_part/total:.1f}%)")
    print(f"  Five-particle dhātus:            {five_part} ({100*five_part/total:.1f}%)")
    print(f"  Six+ particle dhātus:            {six_plus} ({100*six_plus/total:.1f}%)")
    print()
    print(f"  V pattern (e.g. इ, ऋ):    {v_count} ({100*v_count/total:.1f}%)")
    print(f"  CV pattern (e.g. कृ, भू):   {cv_count} ({100*cv_count/total:.1f}%)")
    print(f"  CVC pattern (e.g. गम्):     {cvc_count} ({100*cvc_count/total:.1f}%)")
    print(f"  CCV pattern (e.g. स्था):    {ccv_count} ({100*ccv_count/total:.1f}%)")
    print(f"  CVCC pattern (e.g. कल्प्):  {cvcc_count} ({100*cvcc_count/total:.1f}%)")
    print(f"  CCVC pattern (e.g. स्वप्):  {ccvc_count} ({100*ccvc_count/total:.1f}%)")
    print(f"  CCVCC pattern (e.g. स्कन्द्): {ccvcc_count} ({100*ccvcc_count/total:.1f}%)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
