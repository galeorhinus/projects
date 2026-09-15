#!/usr/bin/env python3
"""Build semantic eligibility for the comparative/superlative expansion."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
INVENTORY = RESULTS / "nominal_input_inventory.csv.gz"
CLASSIFICATION = RESULTS / "taddhita_generalization_classification.json"
CONFIG = HERE / "taddhita_generalization_operations.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    config = json.loads(CONFIG.read_text())
    classification = json.loads(CLASSIFICATION.read_text())
    if classification["selected_families"] != ["comparative", "superlative"]:
        raise ValueError("Generalization classification does not select the expected families")

    total = 0
    with gzip.open(INVENTORY, "rt", newline="", encoding="utf-8") as handle:
        for _row in csv.DictReader(handle):
            total += 1

    rows = []
    for operation in config["operations"]:
        scope = operation["eligibility_scope"]
        if scope != "all_declared_laukika_nominal_word_meanings":
            raise ValueError(f"Unsupported generalization scope: {scope}")
        rows.append({
            **operation,
            "eligible_semantic_branches": "",
            "eligible_candidate_word_meanings": total,
            "count_status": "eligible_for_engine_generation",
        })

    output = RESULTS / "taddhita_generalization_eligibility.csv"
    fields = [
        "operation_id", "source_variant", "operation_display", "semantic_context",
        "semantic_branch_id", "semantic_relation", "eligibility_scope",
        "eligible_semantic_branches", "eligible_candidate_word_meanings",
        "rule_refs", "count_status",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["rule_refs"] = ";".join(row["rule_refs"])
            writer.writerow({field: row[field] for field in fields})

    report = {
        "date": "2026-09-14",
        "nominal_word_meanings": total,
        "deferred_gunavacana_operations": config["deferred_operations"],
        "operations": rows,
        "eligible_operation_relations": sum(row["eligible_candidate_word_meanings"] for row in rows),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (INVENTORY, CLASSIFICATION, CONFIG, Path(__file__))
        },
        "publication_status": "research_eligibility_not_deployed",
    }
    (RESULTS / "taddhita_generalization_eligibility.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Comparative and Superlative Eligibility", "",
        f"The nominal inventory contains **{total:,}** लौकिक word-meanings. Rules 5.3.55 and 5.3.57 admit the general तमप् and तरप् relations across that inventory when a speaker intends comparison. Rule 5.3.58 limits इष्ठन् and ईयसुन् to the traditional गुणवचन class. The present inventory does not independently identify that class, so those two operations remain outside the count.", "",
        "| Operation | Eligible relations |", "|---|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['operation_id']} | {row['eligible_candidate_word_meanings']:,} |")
    lines.extend([
        f"| **Total** | **{report['eligible_operation_relations']:,}** |", "",
        "Eligibility records a meaning that the grammar can express. It does not require prior dictionary attestation, and it does not admit the narrower तद्धित families whose input classes remain unidentified.", "",
    ])
    (RESULTS / "taddhita_generalization_eligibility.md").write_text("\n".join(lines))
    print(f"Declared {report['eligible_operation_relations']:,} comparative/superlative relations.")


if __name__ == "__main__":
    main()
