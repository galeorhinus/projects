#!/usr/bin/env python3
"""Attach plain taddhita assertions to their source-defined semantic work."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path

from taddhita_conditioned_common import ARCHIVE, HERE, RESULTS, sha256, stable_id


SOURCE = RESULTS / "plain_taddhita_source_assertions.csv"
CONFIG = HERE / "plain_taddhita_operations.json"
RULE_MANIFEST = ARCHIVE / "plain_taddhita_rule_manifest.json"


def operation_for(config: dict, rule: str, suffix: str) -> dict:
    candidates = []
    for operation in config["rule_operations"]:
        if rule not in operation["rules"]:
            continue
        suffixes = operation.get("suffixes")
        if suffixes and suffix not in suffixes:
            continue
        candidates.append(operation)
    if len(candidates) != 1:
        raise ValueError(f"Expected one operation for {rule}/{suffix}; found {len(candidates)}")
    return candidates[0]


def main() -> None:
    config = json.loads(CONFIG.read_text())
    manifest = json.loads(RULE_MANIFEST.read_text())
    rule_sources = {row["rule"]: row for row in manifest["sources"]}
    for rule, record in rule_sources.items():
        path = ARCHIVE / record["filename"]
        if sha256(path) != record["sha256"]:
            raise ValueError(f"Archived rule source changed: {path.name}")

    with SOURCE.open(newline="", encoding="utf-8") as handle:
        assertions = list(csv.DictReader(handle))

    overrides: dict[tuple[str, str], list[dict]] = {}
    for row in config["input_relations"]:
        overrides.setdefault((row["rule"], row["input_form_slp1"]), []).append(row)
    domains = {row["rule"]: row["domain"] for row in config["domain_overrides"]}

    rows = []
    classified_assertions = set()
    for assertion in assertions:
        if assertion["assertion_status"] == "negative":
            rows.append({
                **assertion,
                "semantic_row_id": stable_id("plain-taddhita-semantic", assertion["assertion_id"], "negative"),
                "semantic_rule_ref": "",
                "semantic_context": "",
                "semantic_relation": "",
                "semantic_family": "",
                "output_class": "",
                "relation_class": "",
                "domain": "",
                "rule_source_file": "",
                "rule_source_url": "",
                "semantic_status": "negative_assertion_not_admitted",
            })
            continue

        rule = assertion["governing_rule"]
        operation = operation_for(config, rule, assertion["taddhita_source_variant"])
        relations = overrides.get((rule, assertion["input_form_slp1"]), [operation])
        classified_assertions.add(assertion["assertion_id"])
        for index, relation in enumerate(relations, 1):
            semantic_rule = operation.get("canonical_rule", rule)
            source = rule_sources[semantic_rule]
            status = (
                "ignored_test_not_admitted"
                if assertion["test_status"] == "ignored_test"
                else "semantic_relation_recovered"
            )
            rows.append({
                **assertion,
                "semantic_row_id": stable_id(
                    "plain-taddhita-semantic",
                    assertion["assertion_id"],
                    relation["semantic_context"],
                    str(index),
                ),
                "semantic_rule_ref": semantic_rule,
                "semantic_context": relation["semantic_context"],
                "semantic_relation": relation["semantic_relation"],
                "semantic_family": relation["semantic_family"],
                "output_class": operation["output_class"],
                "relation_class": operation["relation_class"],
                "domain": domains.get(rule, "laukika"),
                "rule_source_file": source["filename"],
                "rule_source_url": source["url"],
                "semantic_status": status,
            })

    positive_assertions = {
        row["assertion_id"] for row in assertions if row["assertion_status"] == "positive"
    }
    if classified_assertions != positive_assertions:
        missing = sorted(positive_assertions - classified_assertions)
        raise ValueError(f"Unclassified positive assertions: {missing}")

    output = RESULTS / "plain_taddhita_semantic_classification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    active = [row for row in rows if row["semantic_status"] == "semantic_relation_recovered"]
    report = {
        "date": "2026-09-13",
        "source_assertions": len(assertions),
        "classified_positive_assertions": len(classified_assertions),
        "active_semantic_rows": len(active),
        "extra_semantic_rows_from_polysemy": len(active) - sum(
            row["assertion_status"] == "positive" and row["test_status"] == "active_test"
            for row in assertions
        ),
        "ignored_positive_assertions_not_admitted": sum(
            row["assertion_status"] == "positive" and row["test_status"] == "ignored_test"
            for row in assertions
        ),
        "by_output_class": dict(Counter(row["output_class"] for row in active)),
        "by_relation_class": dict(Counter(row["relation_class"] for row in active)),
        "by_semantic_family": dict(Counter(row["semantic_family"] for row in active)),
        "inputs": {
            str(path.relative_to(HERE.parents[1])): sha256(path)
            for path in (SOURCE, CONFIG, RULE_MANIFEST, Path(__file__))
        },
        "publication_status": "research_classification_only_not_deployed",
    }
    (RESULTS / "plain_taddhita_semantic_classification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Plain तद्धित Semantic Classification",
        "",
        f"All **{len(classified_assertions)} positive assertions** now have a governing semantic rule and an archived rule page. "
        f"The {report['ignored_positive_assertions_not_admitted']} ignored assertions remain outside the count.",
        "",
        f"The {len(active)} active semantic rows include {report['extra_semantic_rows_from_polysemy']} additional row supplied by an explicitly polysemous rule. "
        "The classification does not multiply optional output forms.",
        "",
        "| Output class | Active semantic rows |",
        "|---|---:|",
    ]
    for key, value in sorted(report["by_output_class"].items()):
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "| Relation class | Active semantic rows |", "|---|---:|"])
    for key, value in sorted(report["by_relation_class"].items()):
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.append("")
    (RESULTS / "plain_taddhita_semantic_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(classified_assertions)} positive assertions into {len(active)} active semantic rows.")


if __name__ == "__main__":
    main()
