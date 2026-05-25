#!/usr/bin/env python3
"""Join Dhātupāṭha scaffold features with Path C corpus reactivity.

Creates one row per Dhātupāṭha entry, using the same stripping and scaffold
classification logic as the Ch10 dhāturacanā analysis, then joins DCS Path C
valency/token fields by normalized IAST root.

Output:
  data/derived/dhatu_scaffold_path_c_join.csv
  data/derived/dhatu_scaffold_path_c_join_summary.txt
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
BOOK = BUNDLE.parent.parent
DHATUPATHA = BOOK / "analysis" / "dhatupatha"

sys.path.insert(0, str(DHATUPATHA / "scripts"))
from decompose_dhatupatha import (  # noqa: E402
    CONSONANTS,
    VOWELS,
    strip_markers,
    strip_anubandhas,
    slp1_to_devanagari,
)
from analyze_shells import classify_shell, count_particles  # noqa: E402
from analyze_matra_distribution import template_to_matra  # noqa: E402

DHATUPATHA_CSV = DHATUPATHA / "data" / "dhatupatha.csv"
PATH_C_VALENCY = BUNDLE / "data" / "derived" / "path_c_valency.csv"
OUT_CSV = BUNDLE / "data" / "derived" / "dhatu_scaffold_path_c_join.csv"
OUT_SUMMARY = BUNDLE / "data" / "derived" / "dhatu_scaffold_path_c_join_summary.txt"

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


def slp1_to_iast(s: str) -> str:
    return "".join(SLP1_TO_IAST.get(ch, ch) for ch in s)


def cv_pattern(s: str) -> str:
    return "".join("V" if ch in VOWELS else "C" if ch in CONSONANTS else "" for ch in s)


def count_aksharas(pattern: str) -> int:
    return pattern.count("V")


def load_path_c() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with PATH_C_VALENCY.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out[row["root"]] = row
    return out


def main() -> int:
    if not DHATUPATHA_CSV.exists():
        print(f"ERROR: missing {DHATUPATHA_CSV}", file=sys.stderr)
        return 1
    if not PATH_C_VALENCY.exists():
        print(f"ERROR: missing {PATH_C_VALENCY}", file=sys.stderr)
        return 1

    path_c = load_path_c()
    rows: list[dict[str, object]] = []
    matched = 0
    duplicate_key_counts = Counter()

    with DHATUPATHA_CSV.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        for raw in reader:
            if len(raw) < 3 or not raw[0].isdigit():
                continue

            gana = int(raw[0])
            position = int(raw[1]) if raw[1].isdigit() else 0
            original_slp1 = raw[2].strip()
            structural_slp1 = strip_anubandhas(original_slp1)
            if not structural_slp1:
                continue

            root_iast = slp1_to_iast(structural_slp1)
            duplicate_key_counts[root_iast] += 1
            dev = slp1_to_devanagari(structural_slp1)
            pattern = cv_pattern(structural_slp1)
            racana = classify_shell(structural_slp1)
            pc = path_c.get(root_iast)

            if pc:
                matched += 1

            rows.append({
                "dhatu_id": f"{gana}.{position}",
                "gana": gana,
                "position": position,
                "original_slp1": original_slp1,
                "clean_sound_form_slp1": structural_slp1,
                "dhatu_iast": root_iast,
                "dhatu_devanagari": dev,
                "cv_pattern": pattern,
                "particle_count": count_particles(racana),
                "akshara_count": count_aksharas(pattern),
                "matra_count": f"{template_to_matra(racana):.1f}",
                "racana_scaffold": racana,
                "attested_in_dcs": "yes" if pc else "no",
                "path_c_valency": pc["valency_path_c"] if pc else "0",
                "path_c_token_count": pc["total_tokens"] if pc else "0",
                "path_c_distinct_preverbs": pc["distinct_preverbs"] if pc else "0",
                "path_c_distinct_pratyayas": pc["distinct_pratyayas"] if pc else "0",
            })

    for row in rows:
        row["dhatu_iast_row_count"] = duplicate_key_counts[str(row["dhatu_iast"])]

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "dhatu_id",
        "gana",
        "position",
        "original_slp1",
        "clean_sound_form_slp1",
        "dhatu_iast",
        "dhatu_devanagari",
        "cv_pattern",
        "particle_count",
        "akshara_count",
        "matra_count",
        "racana_scaffold",
        "attested_in_dcs",
        "path_c_valency",
        "path_c_token_count",
        "path_c_distinct_preverbs",
        "path_c_distinct_pratyayas",
        "dhatu_iast_row_count",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    unmatched = total - matched
    attested_roots = len({r["dhatu_iast"] for r in rows if r["attested_in_dcs"] == "yes"})
    duplicate_keys = sum(1 for _key, count in duplicate_key_counts.items() if count > 1)
    top_unmatched = [r["dhatu_iast"] for r in rows if r["attested_in_dcs"] == "no"][:40]

    with OUT_SUMMARY.open("w", encoding="utf-8") as f:
        f.write("Dhātupāṭha scaffold × Path C join summary\n")
        f.write("=" * 52 + "\n\n")
        f.write(f"Dhātupāṭha rows: {total}\n")
        f.write(f"Rows matched to Path C: {matched} ({matched / total:.1%})\n")
        f.write(f"Rows unmatched to Path C: {unmatched} ({unmatched / total:.1%})\n")
        f.write(f"Distinct attested Dhātupāṭha roots: {attested_roots}\n")
        f.write(f"IAST keys with multiple Dhātupāṭha rows: {duplicate_keys}\n")
        f.write("\nCaution: this is a row-level join. For reactivity sums by scaffold,\n")
        f.write("deduplicate by dhatu_iast (or by dhatu_iast + racana_scaffold) before\n")
        f.write("summing Path C valency/token fields, otherwise repeated entries across\n")
        f.write("gaṇas will inflate the corpus-derived columns.\n")
        f.write("\nCanonicalization caveat: this first-pass join uses the same structural\n")
        f.write("anubandha-stripping as the Ch10 scaffold analysis. Some high-value Path C\n")
        f.write("roots may still require Dhātupāṭha-to-corpus canonicalization before final\n")
        f.write("reactivity conclusions are drawn from this table.\n")
        f.write("\nColumns written:\n")
        for name in fieldnames:
            f.write(f"- {name}\n")
        f.write("\nFirst 40 unmatched IAST keys:\n")
        f.write(", ".join(top_unmatched) + "\n")

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_SUMMARY}")
    print(f"Dhātupāṭha rows: {total}")
    print(f"Rows matched to Path C: {matched} ({matched / total:.1%})")
    print(f"Rows unmatched to Path C: {unmatched} ({unmatched / total:.1%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
