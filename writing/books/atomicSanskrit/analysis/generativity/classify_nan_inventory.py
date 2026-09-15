#!/usr/bin/env python3
"""Pass 1: classify the rules and counting boundary for bounded nan compounds."""

from __future__ import annotations

import csv
import json

from nan_common import (
    IMPLEMENTATION, MANIFEST, RESULTS, RULE_TABLE, project_path, sha256,
)


CONFIG = __import__("pathlib").Path(__file__).with_name("nan_operations.json")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    archived = {row["filename"]: row for row in manifest["sources"]}
    for name, record in archived.items():
        path = MANIFEST.parent / name
        if sha256(path) != record["sha256"]:
            raise ValueError(f"Archived source changed: {path}")
    with RULE_TABLE.open(newline="", encoding="utf-8") as handle:
        rules = {row["code"]: row["text"] for row in csv.DictReader(handle, delimiter="\t")}
    config = json.loads(CONFIG.read_text())
    refs = [config["compound_rule"], *config["surface_rules"]]
    missing = [ref for ref in refs if ref not in rules]
    if missing:
        raise ValueError(f"Rules absent from pinned sūtrapāṭha: {missing}")
    implementation = IMPLEMENTATION.read_text()
    if 'purva.has_u("naY")' not in implementation:
        raise ValueError("Pinned compound implementation does not contain its nan branch")
    rows = [
        {
            "rule_ref": config["compound_rule"],
            "rule_text_slp1": rules[config["compound_rule"]],
            "role": "licenses the nan compound",
            "count_effect": "one semantic operation",
        },
        {
            "rule_ref": config["surface_rules"][0],
            "rule_text_slp1": rules[config["surface_rules"][0]],
            "role": "removes the n of nan before the following member",
            "count_effect": "surface form only",
        },
        {
            "rule_ref": config["surface_rules"][1],
            "rule_text_slp1": rules[config["surface_rules"][1]],
            "role": "restores n before a vowel-initial following member",
            "count_effect": "surface form only",
        },
    ]
    output = RESULTS / "nan_rule_classification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": "2026-09-13",
        "rules_classified": len(rows),
        "semantic_operations": 1,
        "surface_allomorphs": 2,
        "counting_boundary": config["counting_rule"],
        "attestation_boundary": config["attestation_rule"],
        "rules": rows,
        "sources": manifest["sources"],
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, MANIFEST, RULE_TABLE, IMPLEMENTATION, __import__("pathlib").Path(__file__))},
        "publication_status": "research_classification_only_not_deployed",
    }
    (RESULTS / "nan_rule_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "nan_rule_classification.md").write_text("\n".join([
        "# नञ् Rule Classification", "",
        "The grammar licenses one negative compound relation. Two later rules determine whether its visible beginning is **अ-** or **अन्-**. Those are two pronunciations of the same operation, not two new meanings.", "",
        "| Rule | Work performed | Count effect |", "|---|---|---|",
        *[f"| {row['rule_ref']} | {row['role']} | {row['count_effect']} |" for row in rows], "",
    ]))
    print("Classified one nan operation and its two surface outcomes.")


if __name__ == "__main__":
    main()
