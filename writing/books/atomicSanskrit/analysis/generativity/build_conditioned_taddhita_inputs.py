#!/usr/bin/env python3
"""Reconcile source examples into unique conditioned taddhita inputs."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

from taddhita_conditioned_common import HERE, RESULTS, sha256, stable_id


SOURCE = RESULTS / "conditioned_taddhita_semantic_classification.csv"


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        candidates = [row for row in csv.DictReader(handle) if row["semantic_disposition"] == "source_conditioned_candidate"]

    grouped = defaultdict(list)
    for row in candidates:
        key = (
            row["input_form_slp1"], row["semantic_context"],
            row["taddhita_source_variant"],
        )
        grouped[key].append(row)

    rows = []
    for key, source_rows in sorted(grouped.items()):
        base, context, suffix = key
        output_forms = sorted({
            form
            for row in source_rows
            for form in row["expected_output_forms_slp1"].split(";")
            if form
        })
        outputs = ";".join(output_forms)
        rules = sorted({row["rule_ref"] for row in source_rows if row["rule_ref"]})
        locators = sorted({f"{row['source_file']}:{row['source_line']}" for row in source_rows})
        rows.append({
            "conditioned_candidate_id": stable_id("conditioned-taddhita", *key),
            "input_form_slp1": base,
            "semantic_context": context,
            "semantic_description": next((row["semantic_description"] for row in source_rows if row["semantic_description"]), ""),
            "taddhita_source_variant": suffix,
            "expected_output_forms_slp1": outputs,
            "expected_output_variant_count": len(output_forms),
            "rule_refs": ";".join(rules),
            "source_locators": ";".join(locators),
            "collapsed_duplicate_assertions": len(source_rows) - 1,
            "input_status": "source_conditioned_relation_not_independent_nominal_count",
        })

    output = RESULTS / "conditioned_taddhita_inputs.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "date": "2026-09-13",
        "candidate_source_assertions": len(candidates),
        "unique_conditioned_relations": len(rows),
        "duplicate_assertions_collapsed": len(candidates) - len(rows),
        "distinct_input_forms": len({row["input_form_slp1"] for row in rows}),
        "distinct_input_context_pairs": len({(row["input_form_slp1"], row["semantic_context"]) for row in rows}),
        "by_chapter": dict(Counter(rule.split(".")[0] for row in rows for rule in row["rule_refs"].split(";") if rule)),
        "input_count_policy": "The source nominal is an input to a proven conditioned relation. It is not added separately to the lexical subtotal without a distinct nominal-meaning record.",
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (SOURCE, Path(__file__))},
        "publication_status": "research_inventory_only_not_deployed",
    }
    (RESULTS / "conditioned_taddhita_inputs.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Conditioned तद्धित Input Reconciliation", "",
        f"The {report['candidate_source_assertions']:,} positive assertions resolve to **{report['unique_conditioned_relations']:,} unique conditioned relations** after {report['duplicate_assertions_collapsed']:,} exact duplicate assertions are collapsed.", "",
        f"These relations use {report['distinct_input_forms']:,} written input forms across {report['distinct_input_context_pairs']:,} base-context pairs. The input form does not enter the lexical subtotal by itself: this pass counts the derivative relation established by the test, not an otherwise unglossed inherited noun.", "",
    ]
    (RESULTS / "conditioned_taddhita_inputs.md").write_text("\n".join(lines))
    print(f"Reconciled {len(candidates)} assertions into {len(rows)} unique conditioned relations.")


if __name__ == "__main__":
    main()
