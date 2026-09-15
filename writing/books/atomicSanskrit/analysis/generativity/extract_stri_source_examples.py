#!/usr/bin/env python3
"""Pass 2: extract active and ignored stri examples from pinned tests."""

from __future__ import annotations

from collections import Counter
import csv
import json
import re

from stri_common import CORE_MANIFEST, RESULTS, TEST_SOURCE, project_path, rule_from_function, rust_functions, sha256, stable_id


CALL_RE = re.compile(
    r'assert_has_stri\(\s*(?P<input>"[^"]+"|&?[A-Za-z][A-Za-z0-9_]*)\s*,\s*'
    r'&\[(?P<outputs>[^\]]*)\]\s*\)',
    re.S,
)
CONSTRUCTOR_RE = re.compile(
    r'let\s+(?P<name>[A-Za-z][A-Za-z0-9_]*)[^=;]*=\s*'
    r'create_[A-Za-z0-9_]+\(\s*"(?P<form>[^"]+)"',
    re.S,
)
STRING_RE = re.compile(r'"([^"]+)"')


def main() -> None:
    manifest = json.loads(CORE_MANIFEST.read_text())
    record = next(row for row in manifest["sources"] if row["filename"] == TEST_SOURCE.name)
    if sha256(TEST_SOURCE) != record["sha256"]:
        raise ValueError("Pinned Kāśikā 4.1 test source changed")

    rows = []
    for function in rust_functions(TEST_SOURCE):
        variables = {match.group("name"): match.group("form") for match in CONSTRUCTOR_RE.finditer(function["body"])}
        for match in CALL_RE.finditer(function["body"]):
            token = match.group("input")
            if token.startswith('"'):
                input_form = token.strip('"')
                input_kind = "literal"
            else:
                variable = token.lstrip("&")
                input_form = variables.get(variable, "")
                input_kind = "constructed_variable" if input_form else "unresolved_variable"
            outputs = sorted(set(STRING_RE.findall(match.group("outputs"))))
            absolute = function["start"] + match.start()
            line = function["full_text"].count("\n", 0, absolute) + 1
            rows.append({
                "source_example_id": stable_id(TEST_SOURCE.name, function["name"], str(line), input_form, ";".join(outputs)),
                "source_file": TEST_SOURCE.name,
                "source_function": function["name"],
                "source_line": line,
                "rule_ref": rule_from_function(function["name"]),
                "source_test_status": "ignored" if function["ignored"] else "active",
                "input_expression": token,
                "input_resolution": input_kind,
                "input_form_slp1": input_form,
                "expected_nominative_forms_slp1": ";".join(outputs),
                "expected_variant_count": len(outputs),
            })

    output = RESULTS / "stri_source_examples.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    statuses = Counter(row["source_test_status"] for row in rows)
    resolutions = Counter(row["input_resolution"] for row in rows)
    report = {
        "date": "2026-09-13",
        "source_assertions": len(rows),
        "active_assertions": statuses["active"],
        "ignored_assertions": statuses["ignored"],
        "literal_inputs": resolutions["literal"],
        "constructed_inputs_resolved": resolutions["constructed_variable"],
        "unresolved_inputs": resolutions["unresolved_variable"],
        "scope": "All assert_has_stri calls in the pinned Kāśikā 4.1 integration file; ignored tests and unresolved inputs remain explicit exclusions.",
        "inputs": {project_path(path): sha256(path) for path in (TEST_SOURCE, CORE_MANIFEST)},
        "publication_status": "research_source_inventory_only_not_deployed",
    }
    (RESULTS / "stri_source_examples.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "stri_source_examples.md").write_text("\n".join([
        "# स्त्रीप्रत्ययः Source Examples", "",
        f"The pinned Kāśikā 4.1 test file contains **{len(rows)}** feminine assertions: **{statuses['active']} active** and **{statuses['ignored']} ignored**. The extractor resolves {resolutions['literal']} literal inputs and {resolutions['constructed_variable']} locally constructed inputs; {resolutions['unresolved_variable']} remain unresolved.", "",
        "An ignored assertion records useful research material but does not enter the candidate inventory. The expected strings are nominative singular evidence, not independently counted inflected cells.", "",
    ]))
    print(f"Extracted {len(rows)} stri assertions: {statuses['active']} active, {statuses['ignored']} ignored.")


if __name__ == "__main__":
    main()
