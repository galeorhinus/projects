#!/usr/bin/env python3
"""Pass 2: recover and verify nan examples from the pinned source tests."""

from __future__ import annotations

import csv
import json
import re

from nan_common import MANIFEST, RESULTS, TEST_6_3, nan_surface, project_path, sha256, stable_id


ASSERTION = re.compile(
    r'assert_has_avyaya_tatpurusha\("naY",\s*"(?P<input>[^"]+)",\s*&\["(?P<output>[^"]+)"\]\);'
)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    source_record = next(row for row in manifest["sources"] if row["filename"] == TEST_6_3.name)
    if sha256(TEST_6_3) != source_record["sha256"]:
        raise ValueError("Pinned Kāśikā 6.3 test source changed")
    text = TEST_6_3.read_text()
    rows = []
    for match in ASSERTION.finditer(text):
        source = match.group("input")
        expected = match.group("output")
        derived, outcome = nan_surface(source)
        if derived != expected:
            raise ValueError(f"Surface-rule mismatch for {source}: {derived} != {expected}")
        rows.append({
            "source_example_id": stable_id("nan", source, expected),
            "source_file": TEST_6_3.name,
            "source_line": text.count("\n", 0, match.start()) + 1,
            "input_form_slp1": source,
            "expected_output_slp1": expected,
            "derived_output_slp1": derived,
            "surface_outcome": outcome,
            "rule_refs": "2.2.6;6.3.73;6.3.74",
            "verification_status": "matches_pinned_source_test",
        })
    if len(rows) != 5:
        raise ValueError(f"Expected five nan examples, found {len(rows)}")
    output = RESULTS / "nan_source_examples.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": "2026-09-13",
        "verified_examples": len(rows),
        "a_before_consonant": sum(row["surface_outcome"] == "a_before_consonant" for row in rows),
        "an_before_vowel": sum(row["surface_outcome"] == "an_before_vowel" for row in rows),
        "inputs": {project_path(path): sha256(path) for path in (MANIFEST, TEST_6_3, __import__("pathlib").Path(__file__))},
        "publication_status": "research_source_examples_only_not_deployed",
    }
    (RESULTS / "nan_source_examples.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "nan_source_examples.md").write_text("\n".join([
        "# नञ् Source Examples", "",
        "The pinned Kāśikā test source supplies five examples. All five match the directly implemented surface rules.", "",
        "| Input | Output | Surface outcome |", "|---|---|---|",
        *[f"| `{row['input_form_slp1']}` | `{row['derived_output_slp1']}` | {row['surface_outcome']} |" for row in rows], "",
    ]))
    print(f"Verified {len(rows)} nan source examples.")


if __name__ == "__main__":
    main()
