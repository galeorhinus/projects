#!/usr/bin/env python3
"""Pass 1: classify source compounds as nominal bases or complete indeclinables."""

from __future__ import annotations

from collections import Counter
import csv
import json

from compound_stack_common import (
    CLASSIFICATION, CLASSIFICATION_ROWS, SOURCE_LEDGER, project_path, read_csv, sha256,
)


FIELDS = (
    "compound_word_meaning_id", "compound_type", "input_forms_slp1",
    "input_semantic_relation", "input_class", "eligible_for_nominal_operations",
)


def main() -> None:
    rows = read_csv(SOURCE_LEDGER)
    if len(rows) != 113:
        raise ValueError(f"Expected 113 source compound meanings, found {len(rows)}")
    counts = Counter()
    with CLASSIFICATION_ROWS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            input_class = "complete_indeclinable" if row["compound_type"] == "avyayibhava" else "derived_nominal_base"
            counts[input_class] += 1
            writer.writerow({
                "compound_word_meaning_id": row["generated_word_meaning_id"],
                "compound_type": row["compound_type"],
                "input_forms_slp1": row["output_forms_slp1"],
                "input_semantic_relation": row["semantic_relation"],
                "input_class": input_class,
                "eligible_for_nominal_operations": str(input_class == "derived_nominal_base").lower(),
            })
    if counts != {"derived_nominal_base": 96, "complete_indeclinable": 17}:
        raise ValueError(f"Unexpected compound classification: {dict(counts)}")
    report = {
        "date": "2026-09-14",
        "source_compound_word_meanings": len(rows),
        "derived_nominal_bases": counts["derived_nominal_base"],
        "complete_avyayibhava_indeclinables": counts["complete_indeclinable"],
        "classification_rule": "Avyayibhava compounds are complete indeclinables. Other admitted source compounds enter this bounded experiment as nominal bases.",
        "inputs": {project_path(SOURCE_LEDGER): sha256(SOURCE_LEDGER)},
    }
    CLASSIFICATION.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (CLASSIFICATION.with_suffix(".md")).write_text("\n".join([
        "# Source-Compound Input Classification", "",
        f"The preceding pass admitted **{len(rows)}** source-demonstrated compound meanings. Of these, **{counts['derived_nominal_base']}** are nominal bases and **{counts['complete_indeclinable']}** are complete अव्ययीभाव (*avyayībhāva*) indeclinables.", "",
        "The indeclinables remain in the lexical subtotal but do not become inputs to the nominal operations in this block.", "",
    ]))
    print(f"Classified {counts['derived_nominal_base']} nominal compounds and {counts['complete_indeclinable']} indeclinables.")


if __name__ == "__main__":
    main()
