#!/usr/bin/env python3
"""Pass 2: extract compound assertions from the pinned Kāśikā tests."""

from __future__ import annotations

from collections import Counter
import csv
import json
import re

from samasa_common import HELPERS, MANIFEST, RESULTS, SOURCE_FILES, project_path, sha256, stable_id
from stri_common import rule_from_function, rust_functions


BINARY_RE = re.compile(
    r'(?P<helper>assert_has_[a-z_]+)\(\s*"(?P<a>[^"]+)"\s*,\s*"(?P<b>[^"]+)"\s*,\s*&\[(?P<outputs>[^]]*)\]\s*\)'
)
ARRAY_RE = re.compile(
    r'(?P<helper>assert_has_(?:samahara_)?dvandva)\(\s*&\[(?P<members>[^]]*)\]\s*,\s*&\[(?P<outputs>[^]]*)\]\s*\)'
)
STRING_RE = re.compile(r'"([^"]+)"')


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    rows = []
    for path in SOURCE_FILES:
        if sha256(path) != records[path.name]["sha256"]:
            raise ValueError(f"Pinned source changed: {path}")
        for function in rust_functions(path):
            for offset, line_text in enumerate(function["body"].splitlines()):
                if "assert_has_" not in line_text or line_text.lstrip().startswith("//"):
                    continue
                helper_match = re.search(r"(assert_has_[a-z_]+)", line_text)
                if not helper_match or helper_match.group(1) not in HELPERS:
                    continue
                helper = helper_match.group(1)
                binary = BINARY_RE.search(line_text)
                array = ARRAY_RE.search(line_text)
                if binary:
                    members = [binary.group("a"), binary.group("b")]
                    outputs = STRING_RE.findall(binary.group("outputs"))
                    resolution = "literal_members"
                elif array:
                    members = STRING_RE.findall(array.group("members"))
                    outputs = STRING_RE.findall(array.group("outputs"))
                    resolution = "literal_members"
                else:
                    members = []
                    outputs_match = re.search(r'&\[(?P<outputs>[^]]*)\]\s*\)\s*;?$', line_text)
                    outputs = STRING_RE.findall(outputs_match.group("outputs")) if outputs_match else []
                    resolution = "constructed_or_unresolved_member"
                line = function["full_text"].count("\n", 0, function["start"]) + offset + 1
                compound_type, template = HELPERS[helper]
                rows.append({
                    "source_example_id": stable_id(path.name, function["name"], str(line), helper, ";".join(members)),
                    "source_file": path.name,
                    "source_function": function["name"],
                    "source_line": line,
                    "rule_ref": rule_from_function(function["name"]),
                    "source_test_status": "ignored" if function["ignored"] else "active",
                    "helper": helper,
                    "compound_type": compound_type,
                    "member_forms_slp1": ";".join(members),
                    "member_count": len(members),
                    "input_resolution": resolution,
                    "semantic_template": template,
                    "expected_forms_slp1": ";".join(sorted(set(outputs))),
                    "expected_variant_count": len(set(outputs)),
                })

    output = RESULTS / "samasa_source_examples.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    statuses = Counter(row["source_test_status"] for row in rows)
    resolutions = Counter(row["input_resolution"] for row in rows)
    report = {
        "date": "2026-09-14",
        "source_assertions": len(rows),
        "active_assertions": statuses["active"],
        "ignored_assertions": statuses["ignored"],
        "reconstructible_assertions": resolutions["literal_members"],
        "constructed_or_unresolved_assertions": resolutions["constructed_or_unresolved_member"],
        "scope": "All recognized compound assertions in pinned Kāśikā 2.1 and 2.2 tests; ignored and locally constructed inputs remain visible.",
        "inputs": {project_path(path): sha256(path) for path in (*SOURCE_FILES, MANIFEST)},
    }
    (RESULTS / "samasa_source_examples.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / "samasa_source_examples.md").write_text(
        "# समासः Source Examples\n\n"
        f"The pinned tests contain **{len(rows)}** recognized compound assertions: **{statuses['active']} active** and **{statuses['ignored']} ignored**. "
        f"The extractor can reconstruct {resolutions['literal_members']} directly from literal members; {resolutions['constructed_or_unresolved_member']} use locally constructed inputs and remain explicit exclusions in this bounded pass.\n"
    )
    print(f"Extracted {len(rows)} compound assertions.")


if __name__ == "__main__":
    main()
