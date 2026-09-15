#!/usr/bin/env python3
"""Subanta pass 10: record repeated spellings without merging coordinates."""

from __future__ import annotations

from collections import defaultdict
import csv
import json

from subanta_common import RESULTS


FIELDS = ("form_slp1", "semantic_cell_count", "semantic_cells")


def main() -> None:
    form_cells = defaultdict(set)
    with (RESULTS / "subanta_paradigm_sample.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        cell = f"{row['sample_id']}:{row['relation_id']}:{row['number_id']}"
        for form in row["generated_forms_slp1"].split(";"):
            if form:
                form_cells[form].add(cell)
    collisions = [
        {"form_slp1": form, "semantic_cell_count": len(cells), "semantic_cells": ";".join(sorted(cells))}
        for form, cells in sorted(form_cells.items()) if len(cells) > 1
    ]
    with (RESULTS / "subanta_sample_collisions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(collisions)
    links = sum(len(cells) for cells in form_cells.values())
    collision_links = sum(row["semantic_cell_count"] for row in collisions)
    report = {
        "date": "2026-09-14", "passes_completed": 10,
        "sample_semantic_cells": len(rows),
        "generated_form_coordinate_links": links,
        "distinct_sample_spellings": len(form_cells),
        "spellings_shared_across_semantic_cells": len(collisions),
        "shared_spelling_coordinate_links": collision_links,
        "semantic_cells_merged": 0,
        "policy": "Repeated spellings retain every word-meaning and relation-number coordinate they realize.",
    }
    (RESULTS / "subanta_sample_collisions.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 10: Repeated-Spelling Diagnostic", "",
        f"The sample produced **{len(form_cells)} distinct spellings** across **{links} form-to-cell links**. **{len(collisions)} spellings** occur in more than one semantic cell.", "",
        "A repeated form does not erase the relation or number distinction that produced it. The sample records these collisions but does not project its collision rate over the full capacity.", "",
    ]
    (RESULTS / "subanta_sample_collisions.md").write_text("\n".join(lines))
    print(f"Found {len(collisions)} repeated spellings; retained every grammatical coordinate.")


if __name__ == "__main__":
    main()
