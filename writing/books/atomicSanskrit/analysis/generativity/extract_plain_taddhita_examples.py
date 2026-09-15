#!/usr/bin/env python3
"""Extract literal plain taddhita assertions from the pinned Kāśikā tests."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path
import re

from taddhita_conditioned_common import HERE, RESULTS, TEST_FILES, matching_brace, sha256, stable_id, strip_line_comments


CORE_MANIFEST = HERE.parents[1] / "working/40_reference/sources/archive/documents/generativity-pilot/manifest.json"
TADDHITA_MANIFEST = HERE.parents[1] / "working/40_reference/sources/archive/documents/generativity-pilot/taddhita_manifest.json"

FUNCTION_RE = re.compile(
    r"(?P<attributes>(?:#\[[^\]]+\]\s*)*)"
    r"fn\s+(?P<name>sutra_[A-Za-z0-9_]+)\s*\([^)]*\)[^{]*\{"
)
ASSERTION_RE = re.compile(
    r"assert_has_taddhita\(\s*"
    r'"(?P<input>[^"]+)"\s*,\s*'
    r"T::(?P<suffix>[A-Za-z0-9_]+)\s*,\s*"
    r"&\[(?P<outputs>[^\]]*)\]\s*\)"
)


def parse_rule(name: str) -> str:
    match = re.match(r"sutra_(\d+)_(\d+)_(\d+)", name)
    return ".".join(match.groups()) if match else ""


def source_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in TEST_FILES:
        text = path.read_text()
        clean = strip_line_comments(text)
        for function in FUNCTION_RE.finditer(clean):
            brace = clean.index("{", function.start())
            end = matching_brace(clean, brace)
            ignored = "#[ignore]" in function.group("attributes")
            rule = parse_rule(function.group("name"))
            body = clean[brace + 1:end]
            for assertion in ASSERTION_RE.finditer(body):
                outputs = re.findall(r'"([^"]+)"', assertion.group("outputs"))
                line = clean.count("\n", 0, brace + 1 + assertion.start()) + 1
                status = "positive" if outputs else "negative"
                execution = "ignored_test" if ignored else "active_test"
                rows.append({
                    "assertion_id": stable_id(
                        "plain-taddhita",
                        path.name,
                        str(line),
                        assertion.group("input"),
                        assertion.group("suffix"),
                    ),
                    "source_file": path.name,
                    "source_line": line,
                    "test_function": function.group("name"),
                    "governing_rule": rule,
                    "input_form_slp1": assertion.group("input"),
                    "taddhita_source_variant": assertion.group("suffix"),
                    "expected_output_forms_slp1": ";".join(outputs),
                    "expected_output_variant_count": len(outputs),
                    "assertion_status": status,
                    "test_status": execution,
                })
    return rows


def main() -> None:
    records = {}
    for manifest in (CORE_MANIFEST, TADDHITA_MANIFEST):
        records.update({row["filename"]: row for row in json.loads(manifest.read_text())["sources"]})
    for path in TEST_FILES:
        if sha256(path) != records[path.name]["sha256"]:
            raise ValueError(f"Archived source changed: {path.name}")

    rows = source_rows()
    output = RESULTS / "plain_taddhita_source_assertions.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    positive = [row for row in rows if row["assertion_status"] == "positive"]
    active_positive = [row for row in positive if row["test_status"] == "active_test"]
    report = {
        "date": "2026-09-13",
        "literal_plain_assertions": len(rows),
        "positive_assertions": len(positive),
        "negative_assertions": len(rows) - len(positive),
        "active_positive_assertions": len(active_positive),
        "ignored_positive_assertions": len(positive) - len(active_positive),
        "active_governing_rules": len({row["governing_rule"] for row in active_positive}),
        "active_suffix_identifiers": len({row["taddhita_source_variant"] for row in active_positive}),
        "by_source_file": dict(Counter(row["source_file"] for row in active_positive)),
        "inputs": {
            str(path.relative_to(HERE.parents[1])): sha256(path)
            for path in (CORE_MANIFEST, TADDHITA_MANIFEST, *TEST_FILES, Path(__file__))
        },
        "publication_status": "research_inventory_only_not_deployed",
    }
    (RESULTS / "plain_taddhita_source_assertions.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "plain_taddhita_source_assertions.md").write_text(
        "# Plain तद्धित Source Assertions\n\n"
        f"The pinned Kāśikā integration sources contain **{len(rows)} literal plain assertions**: "
        f"{len(positive)} positive and {len(rows) - len(positive)} negative. Of the positive rows, "
        f"**{len(active_positive)} are active tests** and **{len(positive) - len(active_positive)} are marked ignored**.\n\n"
        "An expected spelling is not yet a counted word-meaning. Each active positive row must first be "
        "attached to the semantic work of its governing rule. Ignored rows remain recorded but unadmitted.\n"
    )
    print(
        f"Extracted {len(rows)} literal assertions: {len(active_positive)} active positive, "
        f"{len(positive) - len(active_positive)} ignored positive."
    )


if __name__ == "__main__":
    main()
