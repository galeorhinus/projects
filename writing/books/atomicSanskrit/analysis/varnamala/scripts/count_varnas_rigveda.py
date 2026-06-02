#!/usr/bin/env python3
"""Count varṇa frequencies in the Rigveda Saṃhitā (padapāṭha form).

Source: DCS pada-and-analysis.dat (TSV: book, hymn, stanza, pada, text, lemmata, lexids, refids).
Text is in IAST, padapāṭha-segmented, without accents.

Operations:
1. Tokenize the IAST text of each pada into a sequence of varṇāḥ.
2. Apply Pāṇini 8.4.58 — anusvāra → homorganic nasal before stop consonants.
3. Classify each varṇa as svara / vyañjana / ayogavāha.
4. Aggregate counts by category, place-of-articulation, and individual varṇa.

Writes:
- data/derived/varna_counts.csv      (token counts per varṇa)
- data/derived/category_summary.csv  (per-category totals: svara, vyañjana, ayogavāha)
- data/derived/place_summary.csv     (per place-of-articulation totals for vyañjanāni)
"""
from __future__ import annotations
import csv
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# IAST varṇa inventory + classification
# ---------------------------------------------------------------------------

# Svarāḥ (vowels). Pāṇini's full list (14 svarāḥ) — short + long.
SVARAS = {
    "a": "a (अ)", "ā": "ā (आ)",
    "i": "i (इ)", "ī": "ī (ई)",
    "u": "u (उ)", "ū": "ū (ऊ)",
    "ṛ": "ṛ (ऋ)", "ṝ": "ṝ (ॠ)",
    "ḷ": "ḷ (ऌ)", "ḹ": "ḹ (ॡ)",
    "e": "e (ए)", "ai": "ai (ऐ)",
    "o": "o (ओ)", "au": "au (औ)",
}

# Vyañjanāni (consonants), organized by place-of-articulation (sthāna) + class.
# Classes within each place: unaspirated-voiceless, aspirated-voiceless,
# unaspirated-voiced, aspirated-voiced, nasal.
VYANJANAS = {
    # Kaṇṭhya (velar)
    "k":  ("kaṇṭhya", "stop-unvoiced-unasp"),
    "kh": ("kaṇṭhya", "stop-unvoiced-asp"),
    "g":  ("kaṇṭhya", "stop-voiced-unasp"),
    "gh": ("kaṇṭhya", "stop-voiced-asp"),
    "ṅ":  ("kaṇṭhya", "nasal"),
    # Tālavya (palatal)
    "c":  ("tālavya", "stop-unvoiced-unasp"),
    "ch": ("tālavya", "stop-unvoiced-asp"),
    "j":  ("tālavya", "stop-voiced-unasp"),
    "jh": ("tālavya", "stop-voiced-asp"),
    "ñ":  ("tālavya", "nasal"),
    # Mūrdhanya (retroflex)
    "ṭ":  ("mūrdhanya", "stop-unvoiced-unasp"),
    "ṭh": ("mūrdhanya", "stop-unvoiced-asp"),
    "ḍ":  ("mūrdhanya", "stop-voiced-unasp"),
    "ḍh": ("mūrdhanya", "stop-voiced-asp"),
    "ṇ":  ("mūrdhanya", "nasal"),
    # Dantya (dental)
    "t":  ("dantya", "stop-unvoiced-unasp"),
    "th": ("dantya", "stop-unvoiced-asp"),
    "d":  ("dantya", "stop-voiced-unasp"),
    "dh": ("dantya", "stop-voiced-asp"),
    "n":  ("dantya", "nasal"),
    # Oṣṭhya (labial)
    "p":  ("oṣṭhya", "stop-unvoiced-unasp"),
    "ph": ("oṣṭhya", "stop-unvoiced-asp"),
    "b":  ("oṣṭhya", "stop-voiced-unasp"),
    "bh": ("oṣṭhya", "stop-voiced-asp"),
    "m":  ("oṣṭhya", "nasal"),
    # Antaḥsthāḥ (semivowels)
    "y":  ("tālavya", "antaḥstha"),
    "r":  ("mūrdhanya", "antaḥstha"),
    "l":  ("dantya", "antaḥstha"),
    "v":  ("oṣṭhya", "antaḥstha"),
    # Ūṣmāṇaḥ (sibilants/fricatives)
    "ś":  ("tālavya", "ūṣman"),
    "ṣ":  ("mūrdhanya", "ūṣman"),
    "s":  ("dantya", "ūṣman"),
    "h":  ("kaṇṭhya", "ūṣman"),
}

# Ayogavāhāḥ — non-classifiable carriers.
# Anusvāra written as ṁ (overdot, U+1E41) or ṃ (underdot, U+1E43) in IAST.
ANUSVARA_CHARS = {"ṁ", "ṃ"}
VISARGA = "ḥ"
ANUSVARA_RESOLVED = "anusvāra (ं)"          # when not resolved to homorganic nasal
ANUSVARA_AYOGAVAHA = ANUSVARA_RESOLVED      # alias for clarity

# Anusvāra → homorganic nasal map (Pāṇini 8.4.58, parasavarṇa rule).
# Index by following consonant's place.
HOMORGANIC_BY_PLACE = {
    "kaṇṭhya":  "ṅ",
    "tālavya":  "ñ",
    "mūrdhanya": "ṇ",
    "dantya":   "n",
    "oṣṭhya":   "m",
}

# Multi-character varṇāḥ — the IAST digraphs that must be read as a single varṇa.
# These are checked greedily in the tokenizer.
DIGRAPHS = ("kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh", "ai", "au")

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

def tokenize_iast(text: str) -> list[str]:
    """Split an IAST string into varṇa-tokens. Greedy match on digraphs.

    Returns a list of varṇa-strings (e.g., ['a', 'g', 'n', 'i', 'm']).
    Spaces and any non-varṇa characters are skipped.
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        # Skip whitespace and any other non-varṇa
        if ch.isspace():
            i += 1
            continue
        # Anusvāra (either encoding)
        if ch in ANUSVARA_CHARS:
            out.append("ṃ")  # normalize encoding internally to ṃ
            i += 1
            continue
        # Visarga
        if ch == VISARGA:
            out.append(VISARGA)
            i += 1
            continue
        # Try digraph
        if i + 1 < n:
            two = text[i:i+2]
            if two in DIGRAPHS:
                out.append(two)
                i += 2
                continue
        # Single-character varṇa
        if ch in SVARAS or ch in VYANJANAS:
            out.append(ch)
            i += 1
            continue
        # Unknown character — record as is, skip
        # (could be punctuation, digit, etc.)
        i += 1
    return out


def resolve_anusvara(tokens: list[str]) -> list[str]:
    """Apply Pāṇini 8.4.58: ṃ → homorganic nasal before a stop or nasal.

    Before semivowels (y/r/l/v), sibilants (ś/ṣ/s), and h, anusvāra
    remains as ayogavāha.
    """
    out: list[str] = []
    n = len(tokens)
    for i, tok in enumerate(tokens):
        if tok == "ṃ":
            # Look at the next non-svara token; in padapāṭha form,
            # the next token is the next varṇa in the same word OR
            # crosses a word-boundary. We only resolve if the next
            # token is a stop/nasal consonant.
            if i + 1 < n:
                nxt = tokens[i + 1]
                if nxt in VYANJANAS:
                    place, cls = VYANJANAS[nxt]
                    # Resolve before stops + nasals
                    if cls.startswith("stop") or cls == "nasal":
                        out.append(HOMORGANIC_BY_PLACE[place])
                        continue
            # Word-final or before semivowel/sibilant/h → ayogavāha
            out.append("ayogavāha-anusvāra")
        else:
            out.append(tok)
    return out


# ---------------------------------------------------------------------------
# Categorization
# ---------------------------------------------------------------------------

def classify(varna: str) -> tuple[str, str | None, str | None]:
    """Return (category, place, class) for a varṇa.

    category in {'svara', 'vyañjana', 'ayogavāha'}.
    place is set only for vyañjanāni.
    class is set only for vyañjanāni.
    """
    if varna in SVARAS:
        return "svara", None, None
    if varna in VYANJANAS:
        place, cls = VYANJANAS[varna]
        return "vyañjana", place, cls
    if varna in ("ayogavāha-anusvāra", VISARGA):
        return "ayogavāha", None, None
    return "unknown", None, None


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

REPO = Path("/Users/paragtope/projects/writing/books/atomicSanskrit")
DCS_DAT = REPO / "analysis/ganah/data/raw/dcs/dcs/data/rigveda/pada-and-analysis.dat"
DERIVED = REPO / "analysis/varnamala/data/derived"
DERIVED.mkdir(parents=True, exist_ok=True)


def main() -> None:
    counts: Counter[str] = Counter()
    cat_counts: Counter[str] = Counter()
    place_counts: Counter[str] = Counter()
    total_padas = 0
    total_words = 0
    total_varnas = 0

    with DCS_DAT.open() as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            text = row.get("text", "")
            if not text:
                continue
            total_padas += 1
            total_words += len(text.split())
            tokens = tokenize_iast(text)
            tokens = resolve_anusvara(tokens)
            for t in tokens:
                counts[t] += 1
                cat, place, _ = classify(t)
                cat_counts[cat] += 1
                if place:
                    place_counts[place] += 1
                total_varnas += 1

    # ---- varna_counts.csv ----
    out_varna = DERIVED / "varna_counts.csv"
    with out_varna.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["varna", "category", "place", "class", "count", "share_of_total"])
        for varna, cnt in counts.most_common():
            cat, place, cls = classify(varna)
            share = cnt / total_varnas if total_varnas else 0
            w.writerow([varna, cat, place or "", cls or "", cnt, f"{share:.6f}"])

    # ---- category_summary.csv ----
    out_cat = DERIVED / "category_summary.csv"
    with out_cat.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["category", "count", "share_of_total"])
        for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
            share = cnt / total_varnas if total_varnas else 0
            w.writerow([cat, cnt, f"{share:.6f}"])

    # ---- place_summary.csv ----
    out_place = DERIVED / "place_summary.csv"
    with out_place.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["place", "vyanjana_count", "share_of_vyanjanas"])
        vy_total = cat_counts.get("vyañjana", 0)
        for place, cnt in sorted(place_counts.items(), key=lambda x: -x[1]):
            share = cnt / vy_total if vy_total else 0
            w.writerow([place, cnt, f"{share:.6f}"])

    # ---- Report to stdout ----
    print(f"Total padas processed:  {total_padas:,}")
    print(f"Total words (tokens):   {total_words:,}")
    print(f"Total varṇāḥ counted:   {total_varnas:,}")
    print()
    print("=== Category breakdown ===")
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        share = cnt / total_varnas if total_varnas else 0
        print(f"  {cat:<14s}  {cnt:>9,d}   {share:>7.2%}")
    print()
    print("=== Top 10 svarāḥ ===")
    for varna, cnt in counts.most_common():
        cat, _, _ = classify(varna)
        if cat == "svara":
            share = cnt / total_varnas
            print(f"  {SVARAS.get(varna, varna):<10s}  {cnt:>9,d}   {share:>7.2%}")
    print()
    print("=== Top 15 vyañjanāni ===")
    shown = 0
    for varna, cnt in counts.most_common():
        cat, place, cls = classify(varna)
        if cat == "vyañjana":
            share = cnt / total_varnas
            print(f"  {varna:<4s} ({place:<10s} {cls:<20s})  {cnt:>9,d}   {share:>7.2%}")
            shown += 1
            if shown >= 15:
                break
    print()
    print("=== Place-of-articulation distribution (vyañjanāni only) ===")
    vy_total = cat_counts.get("vyañjana", 0)
    for place, cnt in sorted(place_counts.items(), key=lambda x: -x[1]):
        share = cnt / vy_total if vy_total else 0
        print(f"  {place:<14s}  {cnt:>9,d}   {share:>7.2%}")
    print()
    print(f"Output: {out_varna}")
    print(f"Output: {out_cat}")
    print(f"Output: {out_place}")


if __name__ == "__main__":
    main()
