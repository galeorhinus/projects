#!/usr/bin/env python3
"""Pass 1: classify the broad and conditioned namadhatu operations."""

from __future__ import annotations

import csv
import json

from namadhatu_common import (
    CORE_MANIFEST, IMPLEMENTATION, NAMADHATU_MANIFEST, RESULTS, RULE_TABLE,
    project_path, sha256,
)


CONFIG = __import__("pathlib").Path(__file__).with_name("namadhatu_operations.json")


def verified_manifest(path):
    manifest = json.loads(path.read_text())
    archive = path.parent
    for row in manifest["sources"]:
        source = archive / row["filename"]
        if sha256(source) != row["sha256"]:
            raise ValueError(f"Archived source changed: {source}")
    return manifest


def main() -> None:
    core = verified_manifest(CORE_MANIFEST)
    source_manifest = verified_manifest(NAMADHATU_MANIFEST)
    core_records = {row["filename"]: row for row in core["sources"]}
    for source in (IMPLEMENTATION, RULE_TABLE):
        if sha256(source) != core_records[source.name]["sha256"]:
            raise ValueError(f"Pinned source changed: {source}")

    config = json.loads(CONFIG.read_text())
    with RULE_TABLE.open(newline="", encoding="utf-8") as handle:
        rules = {row["code"]: row["text"] for row in csv.DictReader(handle, delimiter="\t")}
    implementation = IMPLEMENTATION.read_text()
    rows = []
    for operation in config["broad_operations"]:
        rule = operation["rule_refs"][0]
        constructor = operation["constructor"]
        if f'Some({constructor})' not in implementation and f'Some(Sanadi::{constructor})' not in implementation:
            raise ValueError(f"Constructor not found in pinned implementation: {constructor}")
        rows.append({
            "operation_id": operation["operation_id"],
            "operation_scope": "productive_broad_relation",
            "constructor": constructor,
            "rule_ref": rule,
            "rule_text_slp1": rules[rule],
            "semantic_relation": operation["semantic_relation"],
            "count_status": "admitted_for_eligibility_pass",
        })
    for rule in (f"3.1.{number}" for number in range(12, 22)):
        rows.append({
            "operation_id": f"conditioned_{rule.replace('.', '_')}",
            "operation_scope": "source_conditioned_relation",
            "constructor": "rule_supplied_or_source_selected",
            "rule_ref": rule,
            "rule_text_slp1": rules[rule],
            "semantic_relation": "one or more relations restricted by the rule's named inputs and conditions",
            "count_status": "requires_source_example_eligibility",
        })

    output = RESULTS / "namadhatu_operation_classification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": "2026-09-13",
        "rules_classified": len(rows),
        "productive_broad_relations": len(config["broad_operations"]),
        "conditioned_rule_groups": 10,
        "exposed_general_constructors": ["kyac", "kAmyac", "kyaN"],
        "classification_boundary": "Rules 3.1.8-3.1.11 supply four broad meaning-relations. Rules 3.1.12-3.1.21 remain tied to named sets, stated conditions, or source-demonstrated examples.",
        "sources": source_manifest["sources"],
        "inputs": {project_path(path): sha256(path) for path in (
            CONFIG, CORE_MANIFEST, NAMADHATU_MANIFEST, IMPLEMENTATION, RULE_TABLE, __import__("pathlib").Path(__file__)
        )},
        "publication_status": "research_classification_only_not_deployed",
    }
    (RESULTS / "namadhatu_operation_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "namadhatu_operation_classification.md").write_text("\n".join([
        "# नामधातुः Operation Classification", "",
        "The first four relations are productive: two ways to express desire, conduct toward an object by comparison, and conduct of an agent by comparison. They are semantic operations, not three suffix names used as automatic multipliers.", "",
        "Rules 3.1.12-3.1.21 add narrower operations. Their named inputs and meanings enter only through the source-demonstrated route; they do not authorize multiplication across the nominal inventory.", "",
    ]))
    print(f"Classified {len(rows)} namadhatu rule groups.")


if __name__ == "__main__":
    main()
