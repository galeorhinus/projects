#!/usr/bin/env python3
"""Collapse duplicate plain assertions into eligible lexical word-meaning relations."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

from taddhita_conditioned_common import HERE, RESULTS, sha256, stable_id


SOURCE = RESULTS / "plain_taddhita_semantic_classification.csv"


def joined(values) -> str:
    return ";".join(sorted({value for value in values if value}))


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = [
            row for row in csv.DictReader(handle)
            if row["semantic_status"] == "semantic_relation_recovered"
        ]

    # First collapse repeated tests of the same grammatical operation. This joins
    # replacement rules such as 5.3.44-46 back to their semantic attachment rule.
    operation_groups: dict[tuple[str, ...], list[dict]] = defaultdict(list)
    for row in source_rows:
        key = (
            row["input_form_slp1"],
            row["taddhita_source_variant"],
            row["semantic_context"],
            row["semantic_relation"],
            row["output_class"],
            row["relation_class"],
            row["domain"],
        )
        operation_groups[key].append(row)

    operation_rows = []
    for key, group in operation_groups.items():
        outputs = {
            output
            for row in group
            for output in row["expected_output_forms_slp1"].split(";")
            if output
        }
        operation_rows.append({
            "input_form_slp1": key[0],
            "taddhita_source_variants": key[1],
            "semantic_context": key[2],
            "semantic_relation": key[3],
            "output_class": key[4],
            "relation_class": key[5],
            "domain": key[6],
            "expected_output_forms_slp1": ";".join(sorted(outputs)),
            "semantic_rule_refs": joined(row["semantic_rule_ref"] for row in group),
            "source_test_rules": joined(row["governing_rule"] for row in group),
            "source_locators": joined(f"{row['source_file']}:{row['source_line']}" for row in group),
            "collapsed_duplicate_assertions": len(group) - 1,
        })

    # Then collapse alternative grammatical paths only when they produce the same
    # word with the same meaning. Different outputs remain different words even if
    # their semantic relation is shared.
    lexical_groups: dict[tuple[str, ...], list[dict]] = defaultdict(list)
    for row in operation_rows:
        key = (
            row["input_form_slp1"],
            row["semantic_context"],
            row["semantic_relation"],
            row["expected_output_forms_slp1"],
            row["output_class"],
            row["relation_class"],
            row["domain"],
        )
        lexical_groups[key].append(row)

    rows = []
    for key, group in lexical_groups.items():
        suffixes = {
            suffix
            for row in group
            for suffix in row["taddhita_source_variants"].split(";")
            if suffix
        }
        rows.append({
            "eligible_word_meaning_id": stable_id("plain-taddhita-word-meaning", *key),
            "input_form_slp1": key[0],
            "semantic_context": key[1],
            "semantic_relation": key[2],
            "expected_output_forms_slp1": key[3],
            "expected_output_variant_count": len(key[3].split(";")),
            "output_class": key[4],
            "relation_class": key[5],
            "domain": key[6],
            "taddhita_source_variants": ";".join(sorted(suffixes)),
            "semantic_rule_refs": joined(row["semantic_rule_refs"] for row in group),
            "source_test_rules": joined(row["source_test_rules"] for row in group),
            "source_locators": joined(row["source_locators"] for row in group),
            "collapsed_duplicate_assertions": sum(int(row["collapsed_duplicate_assertions"]) for row in group),
            "collapsed_alternative_derivations": len(group) - 1,
            "eligibility_status": "source_semantic_relation_recovered",
        })
    rows.sort(key=lambda row: (
        tuple(map(int, row["semantic_rule_refs"].split(";")[0].split("."))),
        row["input_form_slp1"],
        row["semantic_context"],
        row["taddhita_source_variants"],
    ))

    output = RESULTS / "plain_taddhita_eligible_relations.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "date": "2026-09-13",
        "active_semantic_rows": len(source_rows),
        "eligible_word_meaning_relations": len(rows),
        "duplicate_assertions_collapsed": sum(int(row["collapsed_duplicate_assertions"]) for row in rows),
        "alternative_derivations_collapsed": sum(int(row["collapsed_alternative_derivations"]) for row in rows),
        "by_output_class": dict(Counter(row["output_class"] for row in rows)),
        "by_relation_class": dict(Counter(row["relation_class"] for row in rows)),
        "inputs": {
            str(path.relative_to(HERE.parents[1])): sha256(path)
            for path in (SOURCE, Path(__file__))
        },
        "publication_status": "research_eligibility_only_not_deployed",
    }
    (RESULTS / "plain_taddhita_eligibility.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "plain_taddhita_eligibility.md").write_text(
        "# Plain तद्धित Eligibility\n\n"
        f"The {len(source_rows)} active semantic rows collapse to **{len(rows)} eligible word-meaning relations**. "
        f"This removes {report['duplicate_assertions_collapsed']} repeated assertions and "
        f"{report['alternative_derivations_collapsed']} alternative derivational paths that produce the same word with the same meaning.\n\n"
        f"The eligible set contains **{report['by_output_class'].get('nominal_base', 0)} nominal bases** and "
        f"**{report['by_output_class'].get('complete_avyaya', 0)} complete अव्यय word-meanings**. "
        "Neither class has yet been reconciled against earlier ledgers.\n"
    )
    print(f"Collapsed {len(source_rows)} semantic rows to {len(rows)} eligible relations.")


if __name__ == "__main__":
    main()
