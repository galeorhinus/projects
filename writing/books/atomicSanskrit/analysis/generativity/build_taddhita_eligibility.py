#!/usr/bin/env python3
"""Declare semantic eligibility for the first broad taddhita expansion."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
CONFIG = HERE / "taddhita_operations.json"
INVENTORY = RESULTS / "nominal_input_inventory.csv.gz"
CLASSIFICATION = RESULTS / "taddhita_identifier_classification.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with gzip.open(INVENTORY, "rt", newline="", encoding="utf-8") as handle:
        nominal_ids = {row["nominal_word_meaning_id"] for row in csv.DictReader(handle)}
    operations = json.loads(CONFIG.read_text())["operations"]
    with CLASSIFICATION.open(newline="", encoding="utf-8") as handle:
        classified = {row["source_variant"]: row for row in csv.DictReader(handle)}

    rows = []
    for operation in operations:
        variant = operation["source_variant"]
        if classified[variant]["count_status"] != "admitted_by_declared_operation":
            raise ValueError(f"Selected operation is not admitted in classification: {variant}")
        if operation["eligibility_scope"] == "all_declared_laukika_nominal_word_meanings":
            candidates = len(nominal_ids)
            listed = ""
        else:
            eligible = operation["eligible_nominal_ids"]
            missing = set(eligible) - nominal_ids
            if missing:
                raise ValueError(f"Unknown eligible nominal IDs: {sorted(missing)}")
            candidates = len(eligible)
            listed = ";".join(eligible)
        rows.append({
            "operation_id": operation["operation_id"],
            "source_variant": variant,
            "semantic_context": operation["semantic_context"],
            "semantic_relation": operation["semantic_relation"],
            "eligibility_scope": operation["eligibility_scope"],
            "eligible_nominal_ids": listed,
            "eligible_candidate_word_meanings": candidates,
            "rule_refs": ";".join(operation["rule_refs"]),
            "count_status": "eligible_for_engine_generation",
        })

    with (RESULTS / "taddhita_eligibility.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": "2026-09-13",
        "scope": json.loads(CONFIG.read_text())["scope"],
        "nominal_word_meanings": len(nominal_ids),
        "selected_semantic_operations": len(rows),
        "eligible_operation_candidates": sum(int(row["eligible_candidate_word_meanings"]) for row in rows),
        "operations": rows,
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (CONFIG, INVENTORY, CLASSIFICATION, Path(__file__))},
    }
    (RESULTS / "taddhita_eligibility.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# First Broad तद्धित Eligibility Pass", "",
        "Eligibility comes from the stated semantic relation, not from multiplying 175 suffix names by every nominal. The pinned engine is used only after that relation has admitted an input.", "",
        "| Operation | Eligible nominal word-meanings | Relation |", "|---|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['operation_id']} | {int(row['eligible_candidate_word_meanings']):,} | {row['semantic_relation']} |")
    lines.extend([
        f"| **Candidate operation relations** | **{report['eligible_operation_candidates']:,}** | Before engine construction |", "",
        "The three general relations are tested against the complete declared nominal inventory. The descent operation remains limited to कुन्ती, सुपर्णा, and विनता. All other तद्धित relations wait for the nominal semantic classes named by their rules.", "",
    ])
    (RESULTS / "taddhita_eligibility.md").write_text("\n".join(lines))
    print(f"Declared {report['eligible_operation_candidates']} eligible operation relations across {len(rows)} semantic operations.")


if __name__ == "__main__":
    main()
