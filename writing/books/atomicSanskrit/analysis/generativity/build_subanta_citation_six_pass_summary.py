#!/usr/bin/env python3
"""Subanta pass 6: consolidate the citation-stage findings."""

from __future__ import annotations

import json

from subanta_common import RESULTS, project_path, read_json, sha256


INPUT_NAMES = (
    "subanta_word_class_reconciliation.json", "subanta_nominal_inventory.json",
    "subanta_coordinate_classification.json", "subanta_citation_capacity.json",
    "subanta_citation_sample.json",
)


def main() -> None:
    partition, inventory, coordinates, capacity, sample = [read_json(RESULTS / name) for name in INPUT_NAMES]
    if capacity["citation_semantic_cells"] != inventory["laukika_name_word_meanings"]:
        raise ValueError("Citation capacity no longer matches the name-meaning inventory")
    report = {
        "date": "2026-09-14", "passes_completed": 6,
        "laukika_name_word_meanings": inventory["laukika_name_word_meanings"],
        "complete_unchanging_meanings_excluded": inventory["complete_unchanging_meanings_excluded"],
        "citation_semantic_cells": capacity["citation_semantic_cells"],
        "relation_coordinates": coordinates["engine_relation_coordinates"],
        "number_coordinates": coordinates["engine_number_coordinates"],
        "sample_citation_cells_regenerated": sample["locally_regenerated_cells"],
        "expected_citation_forms_recovered": sample["expected_citation_forms_recovered"],
        "gender_multiplier_applied": False,
        "citation_cells_added_to_lexical_subtotal": False,
        "former_reader_graph_residual": partition["former_unresolved_reader_graph_residual"],
        "remaining_passes": 6,
        "inputs": {project_path(RESULTS / name): sha256(RESULTS / name) for name in INPUT_NAMES},
    }
    (RESULTS / "subanta_citation_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Six-Pass नामरूप Citation Summary", "",
        "| Measurement | Result |", "|---|---:|",
        f"| Declinable name meanings | {report['laukika_name_word_meanings']:,} |",
        f"| Complete unchanging meanings excluded | {report['complete_unchanging_meanings_excluded']:,} |",
        f"| Citation cells | {report['citation_semantic_cells']:,} |",
        f"| Sample citation cells regenerated | {report['sample_citation_cells_regenerated']:,} |", "",
        "The citation cell is a grammatical view of an existing lexical meaning. It is not another word-meaning and does not raise the lexical subtotal.", "",
    ]
    (RESULTS / "subanta_citation_six_pass_summary.md").write_text("\n".join(lines))
    print("Completed six name-form citation passes.")


if __name__ == "__main__":
    main()
