#!/usr/bin/env python3
"""Capacity pass 1: classify broad and source-conditioned samasa relations."""

from __future__ import annotations

import csv
import json

from samasa_capacity_common import (
    ARGS_SOURCE, CONFIG, IMPLEMENTATION, MANIFEST, RESULTS, RULE_TABLE,
    load_config, project_path, sha256,
)


def main() -> None:
    config = load_config()
    manifest = json.loads(MANIFEST.read_text())
    archived = {row["filename"]: row for row in manifest["sources"]}
    for path in (IMPLEMENTATION, ARGS_SOURCE, RULE_TABLE):
        if sha256(path) != archived[path.name]["sha256"]:
            raise ValueError(f"Pinned source changed: {path}")

    with RULE_TABLE.open(newline="", encoding="utf-8") as handle:
        rules = {row["code"]: row["text"] for row in csv.DictReader(handle, delimiter="\t")}
    source = IMPLEMENTATION.read_text()
    rows = []
    for relation in config["counted_relations"]:
        missing = [rule for rule in relation["rule_refs"] if rule not in rules]
        if missing:
            raise ValueError(f"Rules absent from pinned sūtrapāṭha: {missing}")
        if f'"{relation["rule_refs"][0]}"' not in source:
            raise ValueError(f"Rule absent from pinned compound implementation: {relation['rule_refs'][0]}")
        rows.append({
            "relation_id": relation["relation_id"],
            "display": relation["display"],
            "rule_refs": ";".join(relation["rule_refs"]),
            "pair_model": relation["pair_model"],
            "disposition": "symbolic_capacity_count",
            "meaning_template": relation["meaning_template"],
            "counting_basis": relation["counting_basis"],
        })
    for relation_id in config["conditioned_relations"]:
        rows.append({
            "relation_id": relation_id,
            "display": relation_id.replace("_", " "),
            "rule_refs": "",
            "pair_model": "source_conditioned",
            "disposition": "retain_source_examples_only",
            "meaning_template": "",
            "counting_basis": "The current member inventory does not independently classify the lexical or semantic condition required for a broad multiplier.",
        })

    output = RESULTS / "samasa_capacity_rule_classification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": config["date"],
        "broad_relations_counted": len(config["counted_relations"]),
        "conditioned_relation_families_deferred": len(config["conditioned_relations"]),
        "counted_relation_ids": [row["relation_id"] for row in config["counted_relations"]],
        "conditioned_relation_ids": config["conditioned_relations"],
        "source_example_fixture_relations": 113,
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, MANIFEST, IMPLEMENTATION, ARGS_SOURCE, RULE_TABLE)},
    }
    (RESULTS / "samasa_capacity_rule_classification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "samasa_capacity_rule_classification.md").write_text("\n".join([
        "# समासः Capacity Rule Classification", "",
        "Four relations have a general semantic shape and enter the symbolic depth-one count. Other compound families remain represented by the 113 source-demonstrated examples until their required input classes are independently available.", "",
        "| Relation | Pair model | Disposition |", "|---|---|---|",
        *[f"| {row['display']} | {row['pair_model']} | {row['disposition']} |" for row in rows], "",
    ]))
    print(f"Classified {len(rows)} compound relation families.")


if __name__ == "__main__":
    main()
