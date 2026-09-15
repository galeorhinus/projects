#!/usr/bin/env python3
"""Tinanta pass 10: measure repeated spellings in the full-paradigm sample."""

from __future__ import annotations

from collections import defaultdict
import csv
import json

from tinanta_common import RESULTS


def main() -> None:
    with (RESULTS / "tinanta_paradigm_sample.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    coordinates = defaultdict(set)
    variant_links = 0
    for row in rows:
        coordinate = ":".join((row["sample_id"], row["lakara_id"], row["purusha"], row["vacana"]))
        for form in {item for item in row["all_forms_slp1"].split(";") if item}:
            coordinates[form].add(coordinate); variant_links += 1
    collisions = [
        {"form_slp1": form, "coordinate_count": len(cells), "coordinates_json": json.dumps(sorted(cells))}
        for form, cells in sorted(coordinates.items()) if len(cells) > 1
    ]
    with (RESULTS / "tinanta_sample_collisions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("form_slp1", "coordinate_count", "coordinates_json"))
        writer.writeheader(); writer.writerows(collisions)
    report = {
        "date": "2026-09-14", "sample_semantic_cells": len(rows),
        "generated_form_coordinate_links": variant_links,
        "distinct_sample_spellings": len(coordinates),
        "spellings_shared_across_semantic_cells": len(collisions),
        "shared_spelling_coordinate_links": sum(row["coordinate_count"] for row in collisions),
        "counting_policy": "Repeated spelling never merges distinct lakara-person-number semantic cells.",
        "scope": "sample diagnostic, not an extrapolated collision rate",
    }
    (RESULTS / "tinanta_sample_collisions.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 10: Repeated-Spelling Diagnostic", "", f"The three-धातुः sample produced **{len(coordinates):,} distinct spellings** across **{variant_links:,} form-to-cell links**. **{len(collisions):,} spellings** occur in more than one semantic cell.", "", "A repeated surface form does not erase the grammatical distinction that produced it. This sample records collisions but does not project its collision rate over the full capacity.", ""]
    (RESULTS / "tinanta_sample_collisions.md").write_text("\n".join(lines))
    print(f"Found {len(collisions)} repeated spellings in the paradigm sample.")


if __name__ == "__main__":
    main()
