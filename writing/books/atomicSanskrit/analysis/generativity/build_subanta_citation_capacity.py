#!/usr/bin/env python3
"""Subanta pass 4: count one citation cell for each name meaning."""

from __future__ import annotations

import json

from subanta_common import CONFIG, RESULTS, project_path, read_json, sha256


def main() -> None:
    inventory = read_json(RESULTS / "subanta_nominal_inventory.json")
    coordinates = read_json(RESULTS / "subanta_coordinate_classification.json")
    config = read_json(CONFIG)
    count = inventory["laukika_name_word_meanings"]
    report = {
        "date": "2026-09-14", "passes_completed": 4,
        "laukika_name_word_meanings": count,
        "citation_coordinate": config["citation_coordinate"],
        "citation_semantic_cells": count,
        "gender_multiplier_applied": False,
        "surface_variants_counted_as_cells": False,
        "inputs": {
            project_path(RESULTS / "subanta_nominal_inventory.json"): sha256(RESULTS / "subanta_nominal_inventory.json"),
            project_path(RESULTS / "subanta_coordinate_classification.json"): sha256(RESULTS / "subanta_coordinate_classification.json"),
            project_path(CONFIG): sha256(CONFIG),
        },
    }
    if coordinates["cells_per_name_meaning"] != 24:
        raise ValueError("The full coordinate matrix changed")
    (RESULTS / "subanta_citation_capacity.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 4: Citation Capacity", "",
        f"One naming-form coordinate for each of **{count:,}** लौकिक name meanings produces **{count:,} citation cells**.", "",
        "Gender and alternative outputs remain attributes of the cell. Neither creates an automatic multiplier.", "",
    ]
    (RESULTS / "subanta_citation_capacity.md").write_text("\n".join(lines))
    print(f"Counted {count:,} citation cells.")


if __name__ == "__main__":
    main()
