#!/usr/bin/env python3
"""Pass 2: extract and semantically label the pinned namadhatu examples."""

from __future__ import annotations

import csv
import json
import re

from namadhatu_common import (
    CORE_MANIFEST, RESULTS, TEST_SOURCE, assertion_calls, project_path,
    rule_from_function, rust_functions, sha256, stable_id,
)


CONFIG = __import__("pathlib").Path(__file__).with_name("namadhatu_operations.json")
STRING_RE = re.compile(r'"([^"]+)"')


def constructor_from(call: str) -> str:
    if "kamyac(" in call:
        return "kAmyac"
    if "kyan(" in call:
        return "kyaN"
    if "kyac(" in call:
        return "kyac"
    return "auto"


def input_from(call: str, function_name: str) -> str:
    matches = re.findall(r'(?:p|nama)\(\s*"([^"]+)"\s*\)', call)
    if matches:
        return matches[-1]
    if function_name == "sutra_3_1_8" and "putriya" in call:
        return "putra"
    return ""


def semantic_relation(config: dict, rule: str, form: str, prefixes: tuple[str, ...]) -> str:
    mapping = config["conditioned_rule_relations"]
    keys = [
        f"{rule}:{':'.join((*prefixes, form))}" if prefixes else f"{rule}:{form}",
        f"{rule}:{form}",
        rule,
    ]
    for key in keys:
        if key in mapping:
            return mapping[key]
    broad = {x["rule_refs"][0]: x["semantic_relation"] for x in config["broad_operations"]}
    return broad.get(rule, "")


def main() -> None:
    config = json.loads(CONFIG.read_text())
    core = json.loads(CORE_MANIFEST.read_text())
    source_record = next(row for row in core["sources"] if row["filename"] == TEST_SOURCE.name)
    if sha256(TEST_SOURCE) != source_record["sha256"]:
        raise ValueError("Pinned Kāśikā 3.1 test source changed")

    raw_rows = []
    for function in rust_functions(TEST_SOURCE):
        rule = rule_from_function(function["name"])
        if not rule or not (8 <= int(rule.split(".")[-1]) <= 21):
            continue
        for call, offset in assertion_calls(function["body"]):
            form = input_from(call, function["name"])
            lists = re.findall(r'&\[([^\]]*)\]', call, re.S)
            prefixes = tuple(STRING_RE.findall(lists[0])) if len(lists) > 1 else ()
            expected = tuple(STRING_RE.findall(lists[-1])) if lists else ()
            if not form or not expected:
                raise ValueError(f"Could not resolve source assertion in {function['name']}: {call}")
            relation = semantic_relation(config, rule, form, prefixes)
            if not relation:
                raise ValueError(f"No semantic relation for {rule} {prefixes} {form}")
            line = function["full_text"].count("\n", 0, function["start"] + offset) + 1
            raw_rows.append({
                "source_example_id": stable_id(TEST_SOURCE.name, function["name"], form, ";".join(prefixes), relation),
                "source_file": TEST_SOURCE.name,
                "source_function": function["name"],
                "source_line": line,
                "rule_ref": rule,
                "input_form_slp1": form,
                "prefixes_slp1": ";".join(prefixes),
                "constructor": constructor_from(call),
                "semantic_relation": relation,
                "expected_present_forms_slp1": ";".join(expected),
                "expected_variant_count": len(expected),
                "source_test_status": "ignored" if function["ignored"] else "active",
                "operation_scope": "broad_example" if int(rule.split(".")[-1]) <= 11 else "conditioned_example",
            })

    # Tense variants and repeated assertions demonstrate one lexical relation only.
    unique = {}
    for row in raw_rows:
        key = (row["rule_ref"], row["input_form_slp1"], row["prefixes_slp1"], row["semantic_relation"])
        if key in unique:
            old = unique[key]
            forms = sorted(set(old["expected_present_forms_slp1"].split(";")) | set(row["expected_present_forms_slp1"].split(";")))
            old["expected_present_forms_slp1"] = ";".join(forms)
            old["expected_variant_count"] = len(forms)
            old["source_test_status"] = "active" if "active" in (old["source_test_status"], row["source_test_status"]) else "ignored"
        else:
            unique[key] = row

    for extra in config["additional_conditioned_relations"]:
        prefixes = tuple(extra["prefixes_slp1"])
        key = (extra["rule_ref"], extra["input_form_slp1"], ";".join(prefixes), extra["semantic_relation"])
        template = next(row for row in unique.values() if row["rule_ref"] == extra["rule_ref"] and row["input_form_slp1"] == extra["input_form_slp1"] and row["prefixes_slp1"] == ";".join(prefixes))
        unique[key] = {
            **template,
            "source_example_id": stable_id("rule-commentary", *key),
            "semantic_relation": extra["semantic_relation"],
            "source_function": "Kāśikā commentary",
            "source_line": "",
        }

    rows = sorted(unique.values(), key=lambda row: (tuple(map(int, row["rule_ref"].split("."))), row["input_form_slp1"], row["semantic_relation"]))
    output = RESULTS / "namadhatu_source_examples.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    active_broad = sum(row["source_test_status"] == "active" and row["operation_scope"] == "broad_example" for row in rows)
    active_conditioned = sum(row["source_test_status"] == "active" and row["operation_scope"] == "conditioned_example" for row in rows)
    ignored = sum(row["source_test_status"] == "ignored" for row in rows)
    report = {
        "date": "2026-09-13",
        "raw_source_assertions": len(raw_rows),
        "unique_source_relations": len(rows),
        "active_broad_examples": active_broad,
        "active_conditioned_relations": active_conditioned,
        "ignored_relations": ignored,
        "duplicates_or_tense_variants_collapsed": len(raw_rows) + len(config["additional_conditioned_relations"]) - len(rows),
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, CORE_MANIFEST, TEST_SOURCE, __import__("pathlib").Path(__file__))},
        "publication_status": "research_source_inventory_only_not_deployed",
    }
    (RESULTS / "namadhatu_source_examples.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "namadhatu_source_examples.md").write_text("\n".join([
        "# नामधातुः Source Examples", "",
        f"The pinned Kāśikā test file supplies {len(raw_rows)} assertions. They collapse to **{len(rows)} lexical relations**: **{active_broad} broad examples**, **{active_conditioned} active conditioned relations**, and **{ignored} ignored relations** retained outside the count.", "",
        "Repeated tense demonstrations do not create new lexical meanings. The second चीवर relation comes directly from the Kāśikā's two stated meanings under 3.1.20.", "",
    ]))
    print(f"Extracted {len(rows)} unique namadhatu source relations.")


if __name__ == "__main__":
    main()
