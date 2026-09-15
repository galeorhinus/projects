#!/usr/bin/env python3
"""Pass 2: recover lexical-agent candidates with constructor provenance."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import json
from pathlib import Path

from stri_generalization_common import (
    CONFIG, ELIGIBILITY, NOMINAL, RESULTS, SOURCE_LEDGERS,
    close_gzip_writer, deterministic_gzip_writer, project_path, read_csv, sha256,
)


FIELDS = [
    "nominal_word_meaning_id", "source_layer", "source_word_meaning_id",
    "source_operation_id", "krt_source_variant", "base_count_key",
    "base_source_codes", "input_forms_slp1", "source_semantic_branch_id",
    "source_semantic_relation", "feminine_semantic_relation", "upasarga_id",
    "source_sanadi_operation_id", "sanadi_stack", "rule_refs",
    "eligibility_status",
]


def main() -> None:
    config = json.loads(CONFIG.read_text())
    operations = {row["source_operation_id"]: row for row in config["selected_operations"]}
    with gzip.open(NOMINAL, "rt", encoding="utf-8", newline="") as handle:
        nominal_rows = [
            row for row in csv.DictReader(handle)
            if row["source_operation_id"] in operations
        ]
    nominal_index = {
        (row["source_layer"], row["source_word_meaning_id"]): row
        for row in nominal_rows
    }

    recovered = {}
    for layer, (path, compressed) in SOURCE_LEDGERS.items():
        for source in read_csv(path, compressed):
            key = (layer, source["derived_word_meaning_id"])
            nominal = nominal_index.get(key)
            if not nominal:
                continue
            operation = operations[source["operation_id"]]
            row = {
                "nominal_word_meaning_id": nominal["nominal_word_meaning_id"],
                "source_layer": layer,
                "source_word_meaning_id": source["derived_word_meaning_id"],
                "source_operation_id": source["operation_id"],
                "krt_source_variant": source["krt_source_variant"],
                "base_count_key": source["base_count_key"],
                "base_source_codes": source["base_source_codes"],
                "input_forms_slp1": source["output_forms_slp1"],
                "source_semantic_branch_id": source["semantic_branch_id"],
                "source_semantic_relation": source["semantic_relation"],
                "feminine_semantic_relation": operation["feminine_relation"],
                "upasarga_id": source.get("upasarga_id", ""),
                "source_sanadi_operation_id": source.get("source_sanadi_operation_id", ""),
                "sanadi_stack": source.get("sanadi_stack", ""),
                "rule_refs": ";".join(operation["rule_refs"]),
                "eligibility_status": "admitted_lexical_agent_candidate",
            }
            recovered[key] = row

    missing = sorted(set(nominal_index) - set(recovered))
    if missing:
        raise ValueError(f"Could not recover constructor provenance for {len(missing)} rows")

    rows = [recovered[key] for key in sorted(recovered)]
    raw, text, writer = deterministic_gzip_writer(ELIGIBILITY, FIELDS)
    try:
        writer.writerows(rows)
    finally:
        close_gzip_writer(raw, text)

    by_operation = Counter(row["source_operation_id"] for row in rows)
    by_layer = Counter(row["source_layer"] for row in rows)
    report = {
        "date": config["date"],
        "eligible_lexical_agent_meanings": len(rows),
        "eligible_by_operation": dict(sorted(by_operation.items())),
        "eligible_by_source_layer": dict(sorted(by_layer.items())),
        "constructor_provenance_recovered": len(recovered),
        "constructor_provenance_missing": len(missing),
        "eligibility_policy": "Only nominal meanings already classified as agents enter. Every candidate retains the original dhatu codes, krt suffix, prefix or sanadi stack, and source semantic relation needed to reconstruct the derivation.",
        "inputs": {
            project_path(path): sha256(path)
            for path in (CONFIG, NOMINAL, *[value[0] for value in SOURCE_LEDGERS.values()], Path(__file__))
        },
        "publication_status": "research_eligibility_only_not_deployed",
    }
    (RESULTS / "stri_generalization_eligibility.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Broader स्त्रीप्रत्ययः Eligibility", "",
        f"The nominal inventory contains **{len(rows):,} lexical agent meanings** whose source construction can be reconstructed.", "",
        "| Source operation | Eligible meanings |", "|---|---:|",
    ]
    for operation, count in sorted(by_operation.items()):
        lines.append(f"| {operation} | {count:,} |")
    lines.extend(["", "No candidate enters through spelling alone. Each row retains the grammatical operation that produced its source agent noun.", ""])
    (RESULTS / "stri_generalization_eligibility.md").write_text("\n".join(lines))
    print(f"Recovered {len(rows):,} lexical-agent candidates with constructor provenance.")


if __name__ == "__main__":
    main()
