#!/usr/bin/env python3
"""Pass 2: declare one additional operation over eligible source compounds."""

from __future__ import annotations

from collections import Counter
import csv
import json

from compound_stack_common import (
    CLASSIFICATION, CLASSIFICATION_ROWS, CONFIG, ELIGIBILITY, ELIGIBILITY_ROWS,
    project_path, read_csv, read_json, sha256, stable_id,
)


FIELDS = (
    "candidate_relation_id", "compound_word_meaning_id", "compound_type",
    "input_forms_slp1", "input_semantic_relation", "operation_family",
    "operation_id", "source_variant", "semantic_context", "semantic_branch_id",
    "semantic_relation", "rule_refs", "derivational_depth",
)
EXCLUSION_FIELDS = FIELDS + ("reason",)


def main() -> None:
    classification = read_json(CLASSIFICATION)
    rows = read_csv(CLASSIFICATION_ROWS)
    operations = read_json(CONFIG)["operations"]
    admitted = Counter()
    excluded = Counter()
    exclusions_path = ELIGIBILITY_ROWS.with_name("compound_stack_exclusions.csv")
    with ELIGIBILITY_ROWS.open("w", newline="", encoding="utf-8") as good, exclusions_path.open("w", newline="", encoding="utf-8") as bad:
        writer = csv.DictWriter(good, fieldnames=FIELDS)
        exclusion_writer = csv.DictWriter(bad, fieldnames=EXCLUSION_FIELDS)
        writer.writeheader()
        exclusion_writer.writeheader()
        for row in rows:
            for operation in operations:
                common = {
                    "candidate_relation_id": stable_id("compound-stack", row["compound_word_meaning_id"], operation["operation_id"]),
                    "compound_word_meaning_id": row["compound_word_meaning_id"],
                    "compound_type": row["compound_type"],
                    "input_forms_slp1": row["input_forms_slp1"],
                    "input_semantic_relation": row["input_semantic_relation"],
                    "operation_family": operation["family"],
                    "operation_id": operation["operation_id"],
                    "source_variant": operation["source_variant"],
                    "semantic_context": operation["semantic_context"],
                    "semantic_branch_id": operation["semantic_branch_id"],
                    "semantic_relation": operation["semantic_relation"],
                    "rule_refs": ";".join(operation["rule_refs"]),
                    "derivational_depth": "2",
                }
                if row["input_class"] != "derived_nominal_base":
                    exclusion_writer.writerow({**common, "reason": "The compound is already a complete avyayibhava indeclinable, not a nominal input in this block."})
                    excluded["complete_indeclinable"] += 1
                    continue
                if row["compound_type"] in operation.get("exclude_compound_types", []):
                    exclusion_writer.writerow({**common, "reason": "Recursive nan over an already negative compound is outside the declared boundary."})
                    excluded["recursive_nan"] += 1
                    continue
                writer.writerow(common)
                admitted[operation["operation_id"]] += 1
    total = sum(admitted.values())
    if total != 958:
        raise ValueError(f"Expected 958 eligible relations, found {total}")
    report = {
        "date": "2026-09-14",
        "source_nominal_compounds": classification["derived_nominal_bases"],
        "operation_count": len(operations),
        "eligible_relations": total,
        "eligible_by_operation": dict(admitted),
        "excluded_operation_relations": sum(excluded.values()),
        "excluded_by_reason": dict(excluded),
        "maximum_derivational_depth": 2,
        "recursive_nan_admitted": False,
        "recursive_compounding_admitted": False,
        "inputs": {project_path(path): sha256(path) for path in (CLASSIFICATION, CLASSIFICATION_ROWS, CONFIG)},
    }
    ELIGIBILITY.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Compound-Input Stack Eligibility", "",
        f"Nine established nominal operations apply to all **{classification['derived_nominal_bases']}** nominal compounds. The नञ् operation applies to **{admitted['nan_privative']}**, excluding the two source compounds that are already negative.", "",
        "| Operation | Eligible meanings |", "|---|---:|",
        *[f"| {key} | {value} |" for key, value in admitted.items()],
        f"| **Total** | **{total}** |", "",
        "The block adds one operation after the source compound and stops at derivational depth two.", "",
    ]
    ELIGIBILITY.with_suffix(".md").write_text("\n".join(lines))
    print(f"Declared {total} compound-input operation relations.")


if __name__ == "__main__":
    main()
