#!/usr/bin/env python3
"""Capacity pass 3: declare exact depth-one relation formulas."""

from __future__ import annotations

import csv
import json

from samasa_capacity_common import CONFIG, RESULTS, load_config, project_path, relation_count, sha256


MEMBERS = RESULTS / "samasa_capacity_member_inventory.json"
RULES = RESULTS / "samasa_capacity_rule_classification.json"


def main() -> None:
    config = load_config()
    member_report = json.loads(MEMBERS.read_text())
    n = member_report["compoundable_nominal_word_meanings"]
    rows = []
    for relation in config["counted_relations"]:
        rows.append({
            "relation_id": relation["relation_id"],
            "display": relation["display"],
            "member_inventory_size": n,
            "pair_model": relation["pair_model"],
            "formula": {
                "ordered_with_self": "N x N",
                "ordered_distinct": "N x (N - 1)",
                "unordered_distinct": "N x (N - 1) / 2",
            }[relation["pair_model"]],
            "eligible_depth_one_relations": relation_count(relation["pair_model"], n),
            "semantic_relation": relation["meaning_template"],
            "rule_refs": ";".join(relation["rule_refs"]),
        })
    output = RESULTS / "samasa_capacity_eligibility.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    total = sum(row["eligible_depth_one_relations"] for row in rows)
    report = {
        "date": config["date"],
        "member_inventory_size": n,
        "counted_relation_families": len(rows),
        "eligible_depth_one_relation_slots": total,
        "rows": rows,
        "maximum_compound_depth": 1,
        "materialized_all_relations": False,
        "attestation_required": False,
        "context_condition": "Each slot is available when a speaker intends the named relation between its member meanings. The count does not assert that every pair is useful without such a context.",
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, MEMBERS, RULES)},
    }
    (RESULTS / "samasa_capacity_eligibility.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Depth-One समासः Eligibility", "",
        f"The declared inventory contains **{n:,}** nominal word-meanings. Four general compound relations make **{total:,}** depth-one semantic slots available.", "",
        "| Relation | Formula | Eligible semantic slots |", "|---|---:|---:|",
        *[f"| {row['display']} | `{row['formula']}` | {row['eligible_depth_one_relations']:,} |" for row in rows],
        f"| **Total** | | **{total:,}** |", "",
        "These are formal semantic slots at a declared depth. Each becomes available when a speaker intends the named relation between its members. The count does not claim that every pairing is useful without a context, already used, or entered in a dictionary.", "",
    ]
    (RESULTS / "samasa_capacity_eligibility.md").write_text("\n".join(lines))
    print(f"Declared {total:,} depth-one compound relation slots.")


if __name__ == "__main__":
    main()
