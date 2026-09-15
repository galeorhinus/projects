#!/usr/bin/env python3
"""Extract literal, meaning-conditioned taddhita examples from pinned tests."""

from __future__ import annotations

from collections import Counter
import csv
import json
import re

from taddhita_conditioned_common import HERE, RESULTS, TEST_FILES, rule_from_function, sha256, source_functions, stable_id


CALL_RE = re.compile(
    r'assert_has_artha_taddhita\(\s*"([^"]+)"\s*,\s*'
    r'([A-Za-z][A-Za-z0-9_]*)\s*,\s*T::([A-Za-z][A-Za-z0-9_]*)\s*,\s*'
    r'&\[([^\]]*)\]\s*\)',
    re.S,
)
LET_RE = re.compile(r"let\s+([A-Za-z][A-Za-z0-9_]*)(?:\s*:[^=;]+)?\s*=\s*([A-Za-z][A-Za-z0-9_]*)\s*;")
STRING_RE = re.compile(r'"([^"]+)"')


def main() -> None:
    extracted = []
    direct_call_count = 0
    for path in TEST_FILES:
        for function in source_functions(path):
            variables = dict(LET_RE.findall(function["body"]))
            for match in CALL_RE.finditer(function["body"]):
                direct_call_count += 1
                base, context, suffix, output_source = match.groups()
                context = variables.get(context, context)
                outputs = sorted(set(STRING_RE.findall(output_source)))
                absolute = function["start"] + match.start()
                line = function["full_text"].count("\n", 0, absolute) + 1
                extracted.append({
                    "example_id": stable_id(path.name, function["name"], str(line), base, context, suffix),
                    "source_file": path.name,
                    "source_function": function["name"],
                    "source_line": line,
                    "rule_ref": rule_from_function(function["name"]),
                    "input_form_slp1": base,
                    "semantic_context": context,
                    "taddhita_source_variant": suffix,
                    "expected_output_forms_slp1": ";".join(outputs),
                    "expected_output_variant_count": len(outputs),
                    "source_assertion_status": "positive" if outputs else "negative",
                })

    fields = list(extracted[0])
    output = RESULTS / "conditioned_taddhita_source_examples.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(extracted)

    report = {
        "date": "2026-09-13",
        "scope": "Literal assert_has_artha_taddhita examples in the pinned Kāśikā integration tests for Aṣṭādhyāyī 4.1-5.4. Helper-generated and nonliteral constructions remain outside this pass.",
        "test_files": len(TEST_FILES),
        "literal_conditioned_assertions": len(extracted),
        "positive_source_examples": sum(row["source_assertion_status"] == "positive" for row in extracted),
        "negative_source_examples": sum(row["source_assertion_status"] == "negative" for row in extracted),
        "distinct_semantic_context_tokens": len({row["semantic_context"] for row in extracted}),
        "distinct_suffix_identifiers": len({row["taddhita_source_variant"] for row in extracted}),
        "by_source_file": dict(Counter(row["source_file"] for row in extracted)),
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (*TEST_FILES, __import__("pathlib").Path(__file__))},
        "publication_status": "research_inventory_only_not_deployed",
    }
    (RESULTS / "conditioned_taddhita_source_examples.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Conditioned तद्धित Source Examples", "",
        "This pass extracts only literal, meaning-conditioned assertions from the pinned Kāśikā integration tests. A positive source example supplies a nominal base, a तद्धित semantic context, a suffix identifier, a rule-located test, and one or more expected forms.", "",
        f"The eight source files contain **{report['positive_source_examples']:,} positive** and **{report['negative_source_examples']:,} negative** literal conditioned assertions across {report['distinct_semantic_context_tokens']} context tokens and {report['distinct_suffix_identifiers']} suffix identifiers.", "",
        "Helper-generated examples, compound tests, स्त्रीप्रत्यय tests, inflection tests, and assertions whose input is constructed through a local Rust expression remain outside this extraction. Negative assertions document exclusions and do not enter the count.", "",
    ]
    (RESULTS / "conditioned_taddhita_source_examples.md").write_text("\n".join(lines))
    print(f"Extracted {len(extracted)} literal conditioned assertions: {report['positive_source_examples']} positive, {report['negative_source_examples']} negative.")


if __name__ == "__main__":
    main()
