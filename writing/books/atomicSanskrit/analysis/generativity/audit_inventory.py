#!/usr/bin/env python3
"""Audit source entries and spellings, without treating either as word counts."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "analysis/dhatupatha/data/dhatupatha.csv"
NORMALIZER = ROOT / "analysis/dhatupatha/scripts/decompose_dhatupatha.py"


def audit(source: Path) -> dict:
    spec = importlib.util.spec_from_file_location("dhatu_decomposition", NORMALIZER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    entries = []
    excluded = 0
    seen = set()
    with source.open(encoding="utf-8", newline="") as handle:
        for line, row in enumerate(csv.reader(handle), 1):
            if not row or not any(cell.strip() for cell in row):
                continue
            if row[0].lstrip().startswith("#"):
                excluded += 1
                continue
            if len(row) != 3 or not row[2].strip():
                raise ValueError(f"Line {line}: expected gana, position, citation form")
            gana, position = int(row[0]), int(row[1])
            if not 1 <= gana <= 10 or position < 1:
                raise ValueError(f"Line {line}: invalid entry identifier")
            key = (gana, position)
            if key in seen:
                raise ValueError(f"Line {line}: duplicate entry identifier {key}")
            seen.add(key)
            entries.append((gana, position, row[2].strip()))

    raw = Counter(entry[2] for entry in entries)
    normalized = Counter(module.strip_anubandhas(entry[2]) for entry in entries)
    return {
        "source_name": source.name,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "normalizer_sha256": hashlib.sha256(NORMALIZER.read_bytes()).hexdigest(),
        "active_entries": len(entries),
        "commented_rows_excluded": excluded,
        "distinct_citation_spellings": len(raw),
        "distinct_normalized_spellings": len(normalized),
        "empty_normalized_entries": normalized.get("", 0),
        "entries_by_gana": dict(sorted(Counter(e[0] for e in entries).items())),
        "repeated_normalized_spellings": sum(n > 1 for n in normalized.values()),
        "interpretation": (
            "Spelling groups do not establish lexical or semantic identity. "
            "Normalization reuses the existing structural-analysis helper, "
            "not a validated lexical-identity resolver. No word total is calculated."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    print(json.dumps(audit(args.source), indent=2))


if __name__ == "__main__":
    main()
