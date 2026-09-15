#!/usr/bin/env python3
"""Subanta pass 2: build the virtual name-meaning inventory and source samples."""

from __future__ import annotations

import csv
import json

from subanta_common import RESULTS, SAMPLES, csv_rows, project_path, read_json, sha256


FIELDS = (
    "sample_id", "display", "stem_slp1", "constructor", "linga",
    "source_file", "source_id_field", "source_word_meaning_id",
    "source_form_field", "expected_citation_slp1",
)


def main() -> None:
    partition = read_json(RESULTS / "subanta_word_class_reconciliation.json")
    samples_by_file = {}
    for sample in SAMPLES:
        samples_by_file.setdefault(sample["source_file"], []).append(sample)
    for filename, expected in samples_by_file.items():
        remaining = {row["source_word_meaning_id"]: row for row in expected}
        for source_row in csv_rows(RESULTS / filename):
            matched = [
                key for key, sample in remaining.items()
                if source_row[sample["source_id_field"]] == key
            ]
            for key in matched:
                sample = remaining.pop(key)
                if sample["stem_slp1"] not in source_row[sample["source_form_field"]].split(";"):
                    raise ValueError(f"Sample form missing from {filename}: {sample['stem_slp1']}")
            if not remaining:
                break
        if remaining:
            raise ValueError(f"Sample IDs missing from {filename}: {sorted(remaining)}")
    with (RESULTS / "subanta_nominal_member_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(SAMPLES)
    report = {
        "date": "2026-09-14", "passes_completed": 2,
        "laukika_name_word_meanings": partition["laukika_name_meanings"],
        "counts_by_source_layer": partition["nominal_counts_by_source_layer"],
        "complete_unchanging_meanings_excluded": partition["laukika_unchanging_meanings"],
        "inventory_storage": "normalized virtual view over completed source ledgers",
        "full_inventory_duplicated": False,
        "materialized_sample_records": len(SAMPLES),
        "sample_source_ledgers_verified": len(samples_by_file),
        "inputs": {
            project_path(path): sha256(path)
            for path in [RESULTS / "subanta_word_class_reconciliation.json", *[RESULTS / name for name in samples_by_file]]
        },
        "publication_status": "research_inventory_not_deployed",
    }
    (RESULTS / "subanta_nominal_inventory.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 2: Name-Meaning Inventory", "",
        f"The current ledgers contain **{report['laukika_name_word_meanings']:,} लौकिक name, object, quality, state, and relation meanings** available to the relation-number model.", "",
        f"The **{report['complete_unchanging_meanings_excluded']:,}** complete unchanging meanings remain in the lexical subtotal but do not enter this inventory. The full inventory remains a virtual view; this pass materializes only {len(SAMPLES)} provenance-rich samples.", "",
    ]
    (RESULTS / "subanta_nominal_inventory.md").write_text("\n".join(lines))
    print(f"Built virtual inventory of {report['laukika_name_word_meanings']:,} name meanings.")


if __name__ == "__main__":
    main()
