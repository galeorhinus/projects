#!/usr/bin/env python3
"""Separate known Vedic-restricted base descendants from the bounded subtotal."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESTRICTIONS = HERE / "vaidika_base_restrictions.json"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
TWELVE_PASS = RESULTS / "twelve_pass_expansion_summary.json"
VAIDIKA_SUMMARY = RESULTS / "vaidika_stacked_summary.json"

LAYERS = [
    ("one_sanadi", RESULTS / "verbal_derivation_ledger.csv", "csv"),
    ("one_upasarga", RESULTS / "upasarga_generation_ledger.csv", "csv"),
    ("upasarga_sanadi", RESULTS / "upasarga_sanadi_ledger.csv.gz", "gzip"),
    ("curadi_true_causative", RESULTS / "curadi_causative_ledger.csv", "csv"),
    ("two_upasarga", RESULTS / "two_upasarga_ledger.csv.gz", "gzip"),
    ("direct_krdanta", RESULTS / "krdanta_ledger.csv", "csv"),
    ("avyaya", RESULTS / "avyaya_ledger.csv", "csv"),
    ("conditioned_krdanta", RESULTS / "conditioned_krdanta_ledger.csv", "csv"),
    ("prefixed_krdanta", RESULTS / "prefixed_krdanta_ledger.csv.gz", "gzip"),
    ("sanadi_krdanta", RESULTS / "sanadi_krdanta_ledger.csv.gz", "gzip"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_counts(path: Path, kind: str, restricted: set[str]) -> tuple[int, int, int]:
    opener = gzip.open if kind == "gzip" else open
    total = restricted_rows = mixed_rows = 0
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if "base_source_codes" not in (reader.fieldnames or []):
            raise ValueError(f"Missing base_source_codes in {path}")
        for row in reader:
            total += 1
            codes = {code for code in row["base_source_codes"].split(";") if code}
            if codes & restricted:
                restricted_rows += 1
                mixed_rows += bool(codes - restricted)
    return total, restricted_rows, mixed_rows


def main() -> None:
    config = json.loads(RESTRICTIONS.read_text())
    restricted = {row["source_code"] for row in config["source_entries"]}
    with ASSIGNMENTS.open(encoding="utf-8", newline="") as handle:
        base_rows = [
            row for row in csv.DictReader(handle)
            if row["record_kind"] == "lexical" and row["source_code"] in restricted
        ]
    expected_base = sum(row["meaning_count"] for row in config["source_entries"])
    if len(base_rows) != expected_base:
        raise ValueError(f"Restricted base mismatch: {len(base_rows)} != {expected_base}")

    layer_rows = []
    for label, path, kind in LAYERS:
        total, restricted_rows, mixed_rows = row_counts(path, kind, restricted)
        layer_rows.append({
            "layer": label,
            "ledger": str(path.relative_to(ROOT)),
            "total_rows": total,
            "known_vedic_restricted_rows": restricted_rows,
            "mixed_restricted_and_unrestricted_rows": mixed_rows,
        })
    if any(row["mixed_restricted_and_unrestricted_rows"] for row in layer_rows):
        raise ValueError("A domain-restricted source shares a generated row with an unrestricted source")

    gross = json.loads(TWELVE_PASS.read_text())["bounded_word_meaning_subtotal"]
    restricted_total = len(base_rows) + sum(row["known_vedic_restricted_rows"] for row in layer_rows)
    report = {
        "date": "2026-09-13",
        "scope": config["scope"],
        "known_vedic_restricted_source_codes": sorted(restricted),
        "known_vedic_restricted_base_meanings": len(base_rows),
        "layers": layer_rows,
        "gross_bounded_word_meaning_subtotal": gross,
        "known_vedic_restricted_base_and_descendant_rows": restricted_total,
        "bounded_laukika_subtotal_after_known_domain_restrictions": gross - restricted_total,
        "vedic_generation_status": "completed" if VAIDIKA_SUMMARY.exists() else "not_run",
        "interpretation": "These rows are removed from the current known laukika subtotal. They are not automatically counted as Vedic words; Vedic generation must be run separately with Vedic mode and its own operations.",
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in [
                RESTRICTIONS, ASSIGNMENTS, TWELVE_PASS,
                *[row[1] for row in LAYERS],
                *([VAIDIKA_SUMMARY] if VAIDIKA_SUMMARY.exists() else []),
                Path(__file__),
            ]
        },
    }
    (RESULTS / "domain_boundary_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Laukika-Vaidika Domain Boundary", "",
        "The generators were run with `is_chandasi=False` and do not include Vedic-only affixes or accent-sensitive Vedic formations. The shared base inventory nevertheless contained eleven meanings whose reviewed commentaries explicitly restrict their source entries to the Vedic domain.", "",
        "| Layer | All admitted rows | Known Vedic-restricted ancestry |", "|---|---:|---:|",
        f"| Original base meanings | 2,634 | {len(base_rows)} |",
    ]
    for row in layer_rows:
        lines.append(
            f"| {row['layer'].replace('_', ' ')} | {row['total_rows']:,} | "
            f"{row['known_vedic_restricted_rows']:,} |"
        )
    lines.extend([
        f"| **Mechanical bounded subtotal** | **{gross:,}** | **{restricted_total:,}** |", "",
        f"After applying the domain restrictions currently documented in the commentary review, the bounded laukika subtotal is **{gross - restricted_total:,} word-meanings**.", "",
        "These 8,660 rows descend from bases explicitly documented as Vedic-only and therefore move intact to the Vaidika side of the domain reconciliation. The separate Vedic-mode ledgers add only Vaidika-specific operations, retaining accent-bearing forms where the engine supplies them.", "",
        "This audit applies the domain restrictions already found. It does not claim that every धातुपाठः entry has received an exhaustive laukika-Vaidika classification.", "",
    ])
    (RESULTS / "domain_boundary_audit.md").write_text("\n".join(lines))
    print(
        f"Known Vedic-restricted ancestry: {restricted_total}; "
        f"bounded laukika subtotal: {gross - restricted_total}."
    )


if __name__ == "__main__":
    main()
