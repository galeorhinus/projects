#!/usr/bin/env python3
"""Capacity pass 9: count exactly one additional binary compound layer."""

from __future__ import annotations

import csv
import json

from samasa_capacity_common import CONFIG, RESULTS, load_config, project_path, sha256


DEPTH_ONE = RESULTS / "samasa_capacity_eligibility.json"


def main() -> None:
    config = load_config()
    depth_one = json.loads(DEPTH_ONE.read_text())
    n = depth_one["member_inventory_size"]
    c1 = depth_one["eligible_depth_one_relation_slots"]
    rows = []
    for relation in config["counted_relations"]:
        if relation["pair_model"].startswith("ordered"):
            multiplier = 2
            formula = "2 x C1 x N"
        else:
            multiplier = 1
            formula = "C1 x N"
        rows.append({
            "relation_id": relation["relation_id"],
            "display": relation["display"],
            "formula": formula,
            "placement_multiplier": multiplier,
            "eligible_depth_two_relations": multiplier * c1 * n,
            "rule_refs": ";".join(relation["rule_refs"]),
        })
    total = sum(row["eligible_depth_two_relations"] for row in rows)
    output = RESULTS / "recursive_samasa_capacity.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": config["date"],
        "original_nominal_meanings": n,
        "depth_one_compound_meaning_slots": c1,
        "depth_two_compound_relation_slots": total,
        "rows": rows,
        "maximum_compound_depth": 2,
        "one_compound_plus_one_original_member_only": True,
        "two_depth_one_compounds_as_members": False,
        "materialized_all_relations": False,
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, DEPTH_ONE)},
    }
    (RESULTS / "recursive_samasa_capacity.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Depth-Two समासः Capacity", "",
        "Exactly one depth-one compound and one original nominal meaning enter one further compound operation.", "",
        "| Relation | Formula | Depth-two slots |", "|---|---:|---:|",
        *[f"| {row['display']} | `{row['formula']}` | {row['eligible_depth_two_relations']:,} |" for row in rows],
        f"| **Total** | | **{total:,}** |", "",
        "The count stops here. Joining two compounds or reopening these outputs would begin another explicitly declared depth.", "",
    ]
    (RESULTS / "recursive_samasa_capacity.md").write_text("\n".join(lines))
    print(f"Declared {total:,} compound slots at depth two.")


if __name__ == "__main__":
    main()
