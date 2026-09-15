#!/usr/bin/env python3
"""Pass 3: declare broad and source-conditioned namadhatu eligibility."""

from __future__ import annotations

import csv
import gzip
import json

from namadhatu_common import NOMINAL_INVENTORY, RESULTS, project_path, sha256


HERE = __import__("pathlib").Path(__file__).resolve().parent
CONFIG = HERE / "namadhatu_operations.json"
CLASSIFICATION = RESULTS / "namadhatu_operation_classification.json"
EXAMPLES = RESULTS / "namadhatu_source_examples.csv"


def main() -> None:
    with gzip.open(NOMINAL_INVENTORY, "rt", newline="", encoding="utf-8") as handle:
        nominal_count = sum(1 for _ in csv.DictReader(handle))
    config = json.loads(CONFIG.read_text())
    classification = json.loads(CLASSIFICATION.read_text())
    if classification["productive_broad_relations"] != len(config["broad_operations"]):
        raise ValueError("Operation classification does not match configuration")
    with EXAMPLES.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    conditioned = [row for row in source_rows if row["source_test_status"] == "active" and row["operation_scope"] == "conditioned_example"]

    broad_rows = [{
        "operation_id": operation["operation_id"],
        "constructor": operation["constructor"],
        "semantic_relation": operation["semantic_relation"],
        "eligibility_scope": operation["eligibility_scope"],
        "eligible_candidate_word_meanings": nominal_count,
        "rule_refs": ";".join(operation["rule_refs"]),
        "count_status": "eligible_for_engine_generation",
    } for operation in config["broad_operations"]]
    output = RESULTS / "namadhatu_eligibility.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(broad_rows[0]))
        writer.writeheader()
        writer.writerows(broad_rows)
    report = {
        "date": "2026-09-13",
        "declared_laukika_nominal_word_meanings": nominal_count,
        "broad_semantic_operations": len(broad_rows),
        "broad_candidate_relations": nominal_count * len(broad_rows),
        "active_conditioned_source_relations": len(conditioned),
        "total_candidate_relations": nominal_count * len(broad_rows) + len(conditioned),
        "ignored_source_relations_not_eligible": sum(row["source_test_status"] == "ignored" for row in source_rows),
        "policy": "Productive rules 3.1.8-3.1.11 apply to every admitted nominal word-meaning because the operation supplies the desire or comparison context. Rules 3.1.12-3.1.21 remain limited to active source-demonstrated relations.",
        "inputs": {project_path(path): sha256(path) for path in (NOMINAL_INVENTORY, CONFIG, CLASSIFICATION, EXAMPLES, __import__("pathlib").Path(__file__))},
        "publication_status": "research_eligibility_only_not_deployed",
    }
    (RESULTS / "namadhatu_eligibility.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामधातुः Eligibility", "",
        f"Four productive relations apply to the declared inventory of {nominal_count:,} nominal word-meanings, producing **{report['broad_candidate_relations']:,} broad candidates** before engine construction.", "",
        f"The narrower rules add **{len(conditioned):,} source-demonstrated candidates**. Their examples establish their own relations but do not multiply across the nominal inventory.", "",
    ]
    (RESULTS / "namadhatu_eligibility.md").write_text("\n".join(lines))
    print(f"Declared {report['total_candidate_relations']} namadhatu candidate relations.")


if __name__ == "__main__":
    main()
