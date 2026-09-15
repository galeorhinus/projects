#!/usr/bin/env python3
"""Subanta pass 7: count the full eight-by-three grammatical capacity."""

from __future__ import annotations

import json

from subanta_common import CONFIG, RESULTS, project_path, read_json, sha256


def main() -> None:
    summary = read_json(RESULTS / "subanta_citation_six_pass_summary.json")
    coordinates = read_json(RESULTS / "subanta_coordinate_classification.json")
    config = read_json(CONFIG)
    per_meaning = coordinates["cells_per_name_meaning"]
    if per_meaning != config["full_matrix"]["cells_per_meaning"]:
        raise ValueError("Configured and classified coordinate matrices differ")
    total = summary["laukika_name_word_meanings"] * per_meaning
    report = {
        "date": "2026-09-14", "passes_completed": 7,
        "laukika_name_word_meanings": summary["laukika_name_word_meanings"],
        "relation_coordinates": coordinates["engine_relation_coordinates"],
        "number_coordinates": coordinates["engine_number_coordinates"],
        "cells_per_name_meaning": per_meaning,
        "full_relation_number_semantic_cells": total,
        "citation_cells_contained_within_full_matrix": summary["citation_semantic_cells"],
        "gender_multiplier_applied": False,
        "all_cells_materialized": False,
        "inputs": {
            project_path(RESULTS / "subanta_citation_six_pass_summary.json"): sha256(RESULTS / "subanta_citation_six_pass_summary.json"),
            project_path(RESULTS / "subanta_coordinate_classification.json"): sha256(RESULTS / "subanta_coordinate_classification.json"),
            project_path(CONFIG): sha256(CONFIG),
        },
    }
    (RESULTS / "subanta_paradigm_capacity.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 7: Full Relation-Number Capacity", "",
        f"**{summary['laukika_name_word_meanings']:,} meanings × {coordinates['engine_relation_coordinates']} relations × {coordinates['engine_number_coordinates']} number values = {total:,} grammatical cells.**", "",
        "The citation cells are contained within this matrix. The total is a formal grammatical capacity, not materialized vocabulary and not an addition to the lexical subtotal.", "",
    ]
    (RESULTS / "subanta_paradigm_capacity.md").write_text("\n".join(lines))
    print(f"Counted {total:,} full relation-number cells.")


if __name__ == "__main__":
    main()
