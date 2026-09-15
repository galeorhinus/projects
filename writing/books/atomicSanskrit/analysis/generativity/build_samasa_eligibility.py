#!/usr/bin/env python3
"""Pass 3: deduplicate directly reconstructible compound relations."""

from __future__ import annotations

from collections import defaultdict
import csv
import json

from samasa_common import RESULTS, project_path, sha256, stable_id


SOURCE = RESULTS / "samasa_source_examples.csv"


def render_meaning(template: str, members: list[str]) -> str:
    if len(members) >= 2:
        return template.format(a=members[0], b=members[1], members=" and ".join(members))
    return template.format(a="first member", b="second member", members="the members")


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    grouped = defaultdict(list)
    exclusions = []
    for row in source_rows:
        if row["source_test_status"] != "active" or row["input_resolution"] != "literal_members":
            exclusions.append({**row, "exclusion_reason": (
                "ignored_source_test" if row["source_test_status"] != "active"
                else "constructed_member_not_reconstructed_in_this_pass"
            )})
            continue
        key = (row["compound_type"], row["member_forms_slp1"])
        grouped[key].append(row)

    eligible = []
    for (compound_type, member_string), group in sorted(grouped.items()):
        members = member_string.split(";")
        outputs = sorted({x for row in group for x in row["expected_forms_slp1"].split(";") if x})
        rules = sorted({row["rule_ref"] for row in group if row["rule_ref"]})
        template = group[0]["semantic_template"]
        eligible.append({
            "compound_relation_id": stable_id("samasa", compound_type, member_string),
            "compound_type": compound_type,
            "member_forms_slp1": member_string,
            "member_count": len(members),
            "derivational_depth": 1,
            "semantic_relation": render_meaning(template, members),
            "rule_refs": ";".join(rules),
            "source_assertion_ids": ";".join(sorted(row["source_example_id"] for row in group)),
            "source_assertion_count": len(group),
            "expected_forms_slp1": ";".join(outputs),
            "expected_variant_count": len(outputs),
            "eligibility_status": "source_demonstrated_two_or_three_member_relation",
        })

    for name, rows in (("samasa_eligible_relations.csv", eligible), ("samasa_exclusions.csv", exclusions)):
        with (RESULTS / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    report = {
        "date": "2026-09-14",
        "active_reconstructible_assertions": sum(len(x) for x in grouped.values()),
        "unique_eligible_relations": len(eligible),
        "duplicate_assertions_collapsed": sum(len(x) - 1 for x in grouped.values()),
        "excluded_assertions": len(exclusions),
        "maximum_member_count": max(int(row["member_count"]) for row in eligible),
        "maximum_derivational_depth": 1,
        "recursive_compounding_admitted": False,
        "nominal_square_multiplier_applied": False,
        "inputs": {project_path(SOURCE): sha256(SOURCE)},
    }
    (RESULTS / "samasa_eligibility.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / "samasa_eligibility.md").write_text(
        "# Bounded समासः Eligibility\n\n"
        f"The pass admits **{len(eligible)}** unique source-demonstrated relations at depth one. "
        f"It collapses {report['duplicate_assertions_collapsed']} repeated assertions and retains {len(exclusions)} ignored or unreconstructed assertions outside the count.\n\n"
        "No Cartesian product of the nominal inventory is used.\n"
    )
    print(f"Prepared {len(eligible)} eligible compound relations.")


if __name__ == "__main__":
    main()
