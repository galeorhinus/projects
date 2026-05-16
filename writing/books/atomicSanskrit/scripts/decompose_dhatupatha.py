#!/usr/bin/env python3
"""
decompose_dhatupatha.py — Devanāgarī rendering + varṇa-level decomposition
of the Pāṇinian Dhātupāṭha.

Reads data/dhatupatha.csv (SLP1 with Pāṇinian accent markers), strips
anubandhas per Aṣṭādhyāyī 1.3.2 + 1.3.5 (same logic as
analyze_dhatupatha.py), converts each dhātu to:

  (a) the standard Devanāgarī form (with inherent /a/, vowel diacritics,
      and halants where needed) — e.g.,  कृ, गम्, स्कन्द्
  (b) the varṇa-level decomposition showing each constituent particle
      separately — e.g.,   क् + ऋ,   ग् + अ + म्,   स् + क् + अ + न् + द्

Output: data/derived/dhatupatha_decomposed.md (Devanāgarī markdown,
organized by gaṇa, with one row per dhātu).

The conversion is reproducible: re-running this script regenerates the
markdown from the same source CSV.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "dhatupatha.csv"
OUT_FILE = REPO_ROOT / "data" / "derived" / "dhatupatha_decomposed.md"

# --- SLP1 → Devanāgarī mappings ----------------------------------------

DEV_CONSONANTS = {
    "k": "क", "K": "ख", "g": "ग", "G": "घ", "N": "ङ",
    "c": "च", "C": "छ", "j": "ज", "J": "झ", "Y": "ञ",
    "w": "ट", "W": "ठ", "q": "ड", "Q": "ढ", "R": "ण",
    "t": "त", "T": "थ", "d": "द", "D": "ध", "n": "न",
    "p": "प", "P": "फ", "b": "ब", "B": "भ", "m": "म",
    "y": "य", "r": "र", "l": "ल", "v": "व",
    "S": "श", "z": "ष", "s": "स", "h": "ह",
    "M": "ं", "H": "ः",  # anusvāra, visarga
}

DEV_VOWELS_INDEPENDENT = {
    "a": "अ", "A": "आ", "i": "इ", "I": "ई",
    "u": "उ", "U": "ऊ", "f": "ऋ", "F": "ॠ",
    "x": "ऌ", "X": "ॡ", "e": "ए", "E": "ऐ",
    "o": "ओ", "O": "औ",
}

DEV_VOWEL_DIACRITICS = {
    "a": "",  # inherent — no diacritic
    "A": "ा", "i": "ि", "I": "ी",
    "u": "ु", "U": "ू", "f": "ृ", "F": "ॄ",
    "x": "ॢ", "X": "ॣ", "e": "े", "E": "ै",
    "o": "ो", "O": "ौ",
}

HALANT = "्"

VOWELS = set(DEV_VOWELS_INDEPENDENT.keys())
CONSONANTS = set(DEV_CONSONANTS.keys())

# --- Anubandha stripping (matches analyze_dhatupatha.py) ----------------

SHORT_VOWEL_ANUBANDHAS = set("aiu")
INITIAL_ANUBANDHAS_2CHAR = ("Ji", "wu", "qu")
TRAILING_CONSONANT_ANUBANDHAS = set("YNlSzwq")
ALL_MARKERS = re.compile(r"[~\\^]")


def strip_markers(s: str) -> str:
    return ALL_MARKERS.sub("", s)


def strip_anubandhas(s: str) -> str:
    # 1.3.5 — initial ñi / ṭu / ḍu
    for prefix in INITIAL_ANUBANDHAS_2CHAR:
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    # 1.3.3 — trailing single-consonant anubandha (ñit/ṅit/lit/ṣit etc.)
    # if it sits immediately after a vowel. E.g., qukf\Y → kfY → kf.
    if (len(s) >= 2
            and s[-1] in TRAILING_CONSONANT_ANUBANDHAS
            and s[-2] in VOWELS):
        s = s[:-1]
    # 1.3.2 — final short -a / -i / -u after consonant; only strip if
    # at least one other vowel remains (preserves CV roots like ji, hu).
    if (len(s) >= 2
            and s[-1] in SHORT_VOWEL_ANUBANDHAS
            and s[-2] in CONSONANTS):
        remaining = s[:-1]
        if any(c in VOWELS for c in remaining):
            s = remaining
    return s


# --- SLP1 → Devanāgarī conversions --------------------------------------

def slp1_to_devanagari(s: str) -> str:
    """
    Convert SLP1 to standard Devanāgarī with inherent /a/, vowel
    diacritics, and halant on word-final consonants.
    """
    out: list[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in CONSONANTS:
            out.append(DEV_CONSONANTS[c])
            # Look at next character to decide vowel handling
            if i + 1 < len(s) and s[i + 1] in VOWELS:
                v = s[i + 1]
                if v != "a":  # /a/ is inherent
                    out.append(DEV_VOWEL_DIACRITICS[v])
                i += 2
            else:
                # No following vowel — apply halant
                out.append(HALANT)
                i += 1
        elif c in VOWELS:
            out.append(DEV_VOWELS_INDEPENDENT[c])
            i += 1
        else:
            # Skip unknown character
            i += 1
    return "".join(out)


def slp1_decompose(s: str) -> list[str]:
    """
    Decompose SLP1 into constituent varṇas in Devanāgarī.
    Each consonant gets a halant; each vowel is shown in its
    independent form.
    """
    parts: list[str] = []
    for c in s:
        if c in CONSONANTS:
            parts.append(DEV_CONSONANTS[c] + HALANT)
        elif c in VOWELS:
            parts.append(DEV_VOWELS_INDEPENDENT[c])
    return parts


def classify_pattern(s: str) -> str:
    """Return a C/V pattern string for the SLP1 sequence."""
    return "".join("V" if c in VOWELS else "C" if c in CONSONANTS else ""
                   for c in s)


def count_aksharas(pattern: str) -> int:
    return pattern.count("V")


# --- Main ----------------------------------------------------------------

GANA_NAMES = {
    1: "bhvādi (भ्वादि)",
    2: "adādi (अदादि)",
    3: "juhotyādi (जुहोत्यादि)",
    4: "divādi (दिवादि)",
    5: "svādi (स्वादि)",
    6: "tudādi (तुदादि)",
    7: "rudhādi (रुधादि)",
    8: "tanādi (तनादि)",
    9: "kryādi (क्र्यादि)",
    10: "curādi (चुरादि)",
}


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found at {DATA_FILE}", file=sys.stderr)
        return 1

    # Read and bucket by gaṇa
    by_gana: dict[int, list[tuple[int, str, str, str, str, str, int, int]]] = {}
    # tuple: (position, original_slp1, devanagari_full, decomposition,
    #         pattern, structural_slp1, particle_count, akshara_count)

    with DATA_FILE.open() as fh:
        for row in csv.reader(fh):
            if len(row) < 3 or not row[0].isdigit():
                continue
            gana = int(row[0])
            position = int(row[1]) if row[1].isdigit() else 0
            original = row[2].strip()

            stripped_markers = strip_markers(original)
            structural = strip_anubandhas(stripped_markers)

            if not structural:
                continue

            dev_full = slp1_to_devanagari(structural)
            decomposition = " + ".join(slp1_decompose(structural))
            pattern = classify_pattern(structural)
            particles = len(pattern)
            aksharas = count_aksharas(pattern)

            by_gana.setdefault(gana, []).append((
                position, original, dev_full, decomposition,
                pattern, structural, particles, aksharas,
            ))

    # Ensure output directory
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write markdown
    total = sum(len(v) for v in by_gana.values())

    with OUT_FILE.open("w") as fh:
        fh.write("# Dhātupāṭha — Devanāgarī Decomposition\n\n")
        fh.write("> Source: `data/dhatupatha.csv` "
                 "(github.com/sanskrit/vyakarana)\n>\n")
        fh.write("> Anubandhas stripped per *Aṣṭādhyāyī* 1.3.2 "
                 "(final short -a/-i/-u after consonant in upadeśa) "
                 "and 1.3.5 (initial *ñi*/*ṭu*/*ḍu*).\n>\n")
        fh.write(f"> Total entries (post-stripping): **{total}** "
                 "across the ten gaṇāḥ.\n>\n")
        fh.write("> Generated by `scripts/decompose_dhatupatha.py`.\n\n")
        fh.write("---\n\n")
        fh.write("Each row shows the dhātu in standard Devanāgarī "
                 "(with inherent /a/, vowel diacritics, and halants "
                 "where needed) on the left of the `=`, followed by "
                 "its varṇa-level decomposition (each consonant with "
                 "its halant ् and each vowel in its independent form) "
                 "on the right. Pattern and particle count for each "
                 "in parentheses.\n\n")
        fh.write("---\n\n")

        for gana in sorted(by_gana):
            entries = by_gana[gana]
            name = GANA_NAMES.get(gana, f"gana-{gana}")
            fh.write(f"## Gaṇa {gana} — *{name}* "
                     f"({len(entries)} dhātavaḥ)\n\n")
            for (position, original, dev_full, decomposition,
                 pattern, structural, particles, aksharas) in entries:
                fh.write(
                    f"- **{dev_full}** = {decomposition}  "
                    f"*({pattern}, {particles} part., "
                    f"{aksharas} akṣ.; SLP1 `{original}`)*\n"
                )
            fh.write("\n")

    print(f"Wrote {OUT_FILE} — {total} dhātus across "
          f"{len(by_gana)} gaṇāḥ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
