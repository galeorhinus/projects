#!/usr/bin/env python3
"""
analyze_scaffold_distinguishability.py

Summarize distinguishability signals inside each mātrā budget.

The analysis starts from `template_distribution.csv`, where each observed
dhātu-racanā scaffold has already been counted. It asks a narrower question:
inside a fixed timing envelope, which scaffold choices dominate?

Outputs:
  data/derived/scaffold_distinguishability_by_matra.csv
  data/derived/scaffold_distinguishability_by_matra.md
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_IN = REPO_ROOT / "data" / "derived" / "template_distribution.csv"
CSV_OUT = REPO_ROOT / "data" / "derived" / "scaffold_distinguishability_by_matra.csv"
MD_OUT = REPO_ROOT / "data" / "derived" / "scaffold_distinguishability_by_matra.md"


def tokens(scaffold: str) -> list[str]:
    return re.findall(r"V[12]|C", scaffold)


def matra_value(parts: list[str]) -> float:
    total = 0.0
    for part in parts:
        if part == "C":
            total += 0.5
        elif part == "V1":
            total += 1.0
        elif part == "V2":
            total += 2.0
    return total


def has_bracketed_short_vowel(parts: list[str]) -> bool:
    for i, part in enumerate(parts):
        if part != "V1":
            continue
        if i > 0 and i < len(parts) - 1 and parts[i - 1] == "C" and parts[i + 1] == "C":
            return True
    return False


def scaffold_stats(scaffold: str) -> dict[str, object]:
    parts = tokens(scaffold)
    consonants = sum(1 for part in parts if part == "C")
    matra = matra_value(parts)
    return {
        "parts": parts,
        "matra": matra,
        "particles": len(parts),
        "consonants": consonants,
        "contacts_per_matra": consonants / matra if matra else 0.0,
        "has_v1": "V1" in parts,
        "has_v2": "V2" in parts,
        "bracketed_v1": has_bracketed_short_vowel(parts),
    }


def fmt_scaffolds(rows: list[dict[str, object]], limit: int = 3) -> str:
    return "; ".join(
        f"{row['scaffold']} ({row['count']})"
        for row in rows[:limit]
    )


def main() -> int:
    if not CSV_IN.exists():
        raise SystemExit(f"Missing input: {CSV_IN}. Run analyze_shells.py first.")

    buckets: dict[float, list[dict[str, object]]] = defaultdict(list)
    grand_total = 0

    with CSV_IN.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            scaffold = row["template"]
            count = int(row["count"])
            stats = scaffold_stats(scaffold)
            item = {
                "scaffold": scaffold,
                "count": count,
                **stats,
            }
            buckets[stats["matra"]].append(item)
            grand_total += count

    rows_out = []
    for matra in sorted(buckets):
        rows = sorted(buckets[matra], key=lambda row: -int(row["count"]))
        total = sum(int(row["count"]) for row in rows)
        top = rows[0]
        top_two_count = sum(int(row["count"]) for row in rows[:2])
        top_three_count = sum(int(row["count"]) for row in rows[:3])
        bracketed_count = sum(int(row["count"]) for row in rows if row["bracketed_v1"])
        short_count = sum(int(row["count"]) for row in rows if row["has_v1"])
        long_count = sum(int(row["count"]) for row in rows if row["has_v2"])
        weighted_contacts = sum(
            int(row["count"]) * float(row["contacts_per_matra"])
            for row in rows
        ) / total
        rows_out.append({
            "matra": matra,
            "total": total,
            "distinct_scaffolds": len(rows),
            "top_scaffold": top["scaffold"],
            "top_count": top["count"],
            "top_pct": 100 * int(top["count"]) / total,
            "top_two": fmt_scaffolds(rows, 2),
            "top_two_pct": 100 * top_two_count / total,
            "top_three": fmt_scaffolds(rows, 3),
            "top_three_pct": 100 * top_three_count / total,
            "bracketed_v1_count": bracketed_count,
            "bracketed_v1_pct": 100 * bracketed_count / total,
            "short_vowel_count": short_count,
            "short_vowel_pct": 100 * short_count / total,
            "long_vowel_count": long_count,
            "long_vowel_pct": 100 * long_count / total,
            "weighted_contacts_per_matra": weighted_contacts,
        })

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "matra",
            "total",
            "distinct_scaffolds",
            "top_scaffold",
            "top_count",
            "top_pct",
            "top_two",
            "top_two_pct",
            "top_three",
            "top_three_pct",
            "bracketed_v1_count",
            "bracketed_v1_pct",
            "short_vowel_count",
            "short_vowel_pct",
            "long_vowel_count",
            "long_vowel_pct",
            "weighted_contacts_per_matra",
        ])
        writer.writeheader()
        for row in rows_out:
            writer.writerow({
                **row,
                "matra": f"{row['matra']:.1f}",
                "top_pct": f"{row['top_pct']:.2f}",
                "top_two_pct": f"{row['top_two_pct']:.2f}",
                "top_three_pct": f"{row['top_three_pct']:.2f}",
                "bracketed_v1_pct": f"{row['bracketed_v1_pct']:.2f}",
                "short_vowel_pct": f"{row['short_vowel_pct']:.2f}",
                "long_vowel_pct": f"{row['long_vowel_pct']:.2f}",
                "weighted_contacts_per_matra": f"{row['weighted_contacts_per_matra']:.3f}",
            })

    with MD_OUT.open("w") as fh:
        fh.write("# Dhātupāṭha — Scaffold Distinguishability by Mātrā\n\n")
        fh.write(f"> Source: `template_distribution.csv` ({grand_total} dhātus).\n>\n")
        fh.write("> Generated by `scripts/analyze_scaffold_distinguishability.py`.\n\n")
        fh.write("This table asks which scaffold choices dominate inside each fixed timing envelope.\n\n")
        fh.write("| Mātrā | Count | Distinct scaffolds | Top scaffold | Top share | Top three | Top three share | Bracketed V1 share | Avg consonantal contacts per mātrā |\n")
        fh.write("|---:|---:|---:|---|---:|---|---:|---:|---:|\n")
        for row in rows_out:
            fh.write(
                f"| {row['matra']:.1f} | {row['total']} | {row['distinct_scaffolds']} | "
                f"**{row['top_scaffold']}** ({row['top_count']}) | {row['top_pct']:.2f}% | "
                f"{row['top_three']} | {row['top_three_pct']:.2f}% | "
                f"{row['bracketed_v1_pct']:.2f}% | {row['weighted_contacts_per_matra']:.3f} |\n"
            )

    print(f"Wrote {CSV_OUT}")
    print(f"Wrote {MD_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
