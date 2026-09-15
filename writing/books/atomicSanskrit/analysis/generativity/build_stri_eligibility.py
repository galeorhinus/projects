#!/usr/bin/env python3
"""Pass 3: build a deduplicated source-demonstrated stri input inventory."""

from __future__ import annotations

from collections import defaultdict
import csv
import json

from stri_common import RESULTS, project_path, sha256, stable_id


SOURCE = RESULTS / "stri_source_examples.csv"


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    admitted_source = [row for row in source_rows if row["source_test_status"] == "active" and row["input_form_slp1"]]
    excluded_source = [row for row in source_rows if row not in admitted_source]

    grouped = defaultdict(list)
    for row in admitted_source:
        grouped[row["input_form_slp1"]].append(row)
    candidates = []
    for input_form, rows in sorted(grouped.items()):
        outputs = sorted({form for row in rows for form in row["expected_nominative_forms_slp1"].split(";") if form})
        rules = sorted({row["rule_ref"] for row in rows if row["rule_ref"]})
        candidates.append({
            "stri_relation_id": stable_id("stri-source-relation", input_form),
            "input_form_slp1": input_form,
            "semantic_relation": "feminine counterpart of the demonstrated nominal base",
            "expected_nominative_forms_slp1": ";".join(outputs),
            "expected_variant_count": len(outputs),
            "source_rule_refs": ";".join(rules),
            "source_assertion_ids": ";".join(sorted(row["source_example_id"] for row in rows)),
            "source_assertion_count": len(rows),
            "eligibility_status": "source_demonstrated_candidate",
        })

    output = RESULTS / "stri_eligible_inputs.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(candidates[0]))
        writer.writeheader()
        writer.writerows(candidates)
    report = {
        "date": "2026-09-13",
        "active_resolved_assertions": len(admitted_source),
        "unique_source_demonstrated_inputs": len(candidates),
        "duplicate_assertions_collapsed": len(admitted_source) - len(candidates),
        "ignored_or_unresolved_assertions_excluded": len(excluded_source),
        "eligibility_policy": "Only an active, source-located feminine assertion creates a candidate. Repeated assertions for one input collapse into one feminine word-meaning relation; alternative forms remain variants of that relation.",
        "broad_nominal_multiplier_applied": False,
        "inputs": {project_path(SOURCE): sha256(SOURCE)},
        "publication_status": "research_eligibility_only_not_deployed",
    }
    (RESULTS / "stri_eligibility.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "stri_eligibility.md").write_text("\n".join([
        "# स्त्रीप्रत्ययः Eligibility", "",
        f"The {len(admitted_source)} active, resolved assertions collapse to **{len(candidates)} source-demonstrated nominal inputs**. Repetition contributes no additional word-meaning, and alternative forms stay attached to one relation.", "",
        "This pass does not multiply a feminine operation across the full nominal ledger. The grammatical sources choose the suffix according to the base, and some feminine inputs require no new suffix at all.", "",
    ]))
    print(f"Built {len(candidates)} eligible source-demonstrated stri inputs.")


if __name__ == "__main__":
    main()
