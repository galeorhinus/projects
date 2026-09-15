#!/usr/bin/env python3
"""Separate broad suffix operations from restricted and unresolved ones."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path
import re

from taddhita_conditioned_common import HERE, RESULTS, TEST_FILES, sha256, source_functions


SOURCE = RESULTS / "suffix_semantic_families.csv"
PLAIN_CALL_RE = re.compile(
    r'assert_has_taddhita\(\s*"[^"]+"\s*,\s*T::[A-Za-z][A-Za-z0-9_]*\s*,\s*&\[([^\]]*)\]\s*\)',
    re.S,
)


def decision(row: dict[str, str]) -> tuple[str, str]:
    disposition = row["classification_disposition"]
    if disposition == "admitted_general_relation":
        return "broad_declared_operation", "already admitted across the declared nominal inventory"
    if disposition == "admitted_listed_examples_only":
        return "listed_inputs_only", "already admitted only for named source-backed inputs"
    if disposition == "conditioned_semantic_relation_deferred":
        return "conditioned_inputs_only", "requires an input satisfying the rule's named semantic condition"
    if disposition == "self_meaning_or_structural_relation_deferred":
        return "form_capacity_not_new_meaning", "a new form is not counted without evidence of a distinct meaning"
    return "unreached_not_counted", "the pinned implementation does not establish an operation here"


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    rows = []
    for row in source_rows:
        productivity, reason = decision(row)
        rows.append({**row, "productivity_class": productivity, "counting_decision": reason})

    output = RESULTS / "suffix_productivity_classification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(row["productivity_class"] for row in rows)
    positive_plain_assertions = 0
    for path in TEST_FILES:
        for function in source_functions(path):
            positive_plain_assertions += sum('"' in match.group(1) for match in PLAIN_CALL_RE.finditer(function["body"]))
    report = {
        "date": "2026-09-13",
        "suffix_identifiers": len(rows),
        "by_productivity_class": dict(counts),
        "broad_multipliers": [row["source_variant"] for row in rows if row["productivity_class"] == "broad_declared_operation"],
        "plain_source_assertions_outside_count": positive_plain_assertions,
        "plain_assertion_reason": "These positive source assertions record forms but do not by themselves establish a distinct word-meaning. They therefore remain evidence of formation capacity rather than additions to a meaning count.",
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (SOURCE, *TEST_FILES, Path(__file__))},
        "publication_status": "research_classification_only_not_deployed",
    }
    (RESULTS / "suffix_productivity_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Suffix Productivity Classification", "",
        "Only a declared semantic relation can enlarge the word-meaning count. Engine generation proves that a form can be built; it does not prove that every generated spelling contributes another meaning.", "",
        "| Class | Suffix identifiers | Counting treatment |", "|---|---:|---|",
        f"| Broad declared operation | {counts['broad_declared_operation']} | Already counted over the eligible nominal inventory |",
        f"| Listed inputs only | {counts['listed_inputs_only']} | Already counted only for named inputs |",
        f"| Conditioned inputs only | {counts['conditioned_inputs_only']} | Count only source-backed or independently classified eligible inputs |",
        f"| Same-meaning or structural | {counts['form_capacity_not_new_meaning']} | Preserve as formation evidence; do not add merely for a new spelling |",
        f"| Unreached | {counts['unreached_not_counted']} | Do not count |", "",
        f"The **{positive_plain_assertions} positive plain assertions** in the pinned tests remain outside the word-meaning total. They record further formations, including many -क and -य forms, but the assertions do not state a distinct semantic relation.", "",
    ]
    (RESULTS / "suffix_productivity_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(rows)} suffix identifiers by productivity and counting treatment.")


if __name__ == "__main__":
    main()
