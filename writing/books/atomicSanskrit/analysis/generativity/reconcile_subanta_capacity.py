#!/usr/bin/env python3
"""Subanta pass 11: reconcile citation, full-matrix, gender, and sample results."""

from __future__ import annotations

import json

from subanta_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, read_json, sha256


INPUT_NAMES = (
    "subanta_word_class_reconciliation.json", "subanta_citation_six_pass_summary.json",
    "subanta_paradigm_capacity.json", "subanta_gender_classification.json",
    "subanta_paradigm_sample.json", "subanta_sample_collisions.json",
)


def main() -> None:
    partition, citation, capacity, gender, sample, collisions = [read_json(RESULTS / name) for name in INPUT_NAMES]
    names = partition["laukika_name_meanings"]
    if citation["citation_semantic_cells"] != names:
        raise ValueError("Citation cells do not reconcile to name meanings")
    if capacity["full_relation_number_semantic_cells"] != names * 24:
        raise ValueError("Full relation-number capacity does not reconcile")
    if sample["semantic_cells_locally_regenerated"] != sample["semantic_cells_requested"]:
        raise ValueError("The full sample contains unresolved cells")
    if gender["automatic_gender_multiplier"] != 1 or collisions["semantic_cells_merged"] != 0:
        raise ValueError("Gender or collision policy changed")
    report = {
        "date": "2026-09-14", "passes_completed": 11,
        "materialized_lexical_word_meaning_subtotal": CURRENT_LEXICAL_SUBTOTAL,
        "laukika_name_word_meanings": names,
        "laukika_complete_unchanging_word_meanings": partition["laukika_unchanging_meanings"],
        "citation_semantic_cells": citation["citation_semantic_cells"],
        "full_relation_number_semantic_cells": capacity["full_relation_number_semantic_cells"],
        "gender_multiplier": gender["automatic_gender_multiplier"],
        "locally_regenerated_citation_sample_cells": citation["sample_citation_cells_regenerated"],
        "locally_regenerated_full_paradigm_sample_cells": sample["semantic_cells_locally_regenerated"],
        "sample_repeated_spellings": collisions["spellings_shared_across_semantic_cells"],
        "all_inflection_rows_materialized": False,
        "inflectional_cells_added_to_lexical_subtotal": False,
        "inputs": {project_path(RESULTS / name): sha256(RESULTS / name) for name in INPUT_NAMES},
    }
    (RESULTS / "subanta_capacity_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 11: Capacity Reconciliation", "",
        f"The exact name-meaning inventory is **{names:,}**. Its citation view contains the same number of cells. The complete 8 × 3 matrix contains **{report['full_relation_number_semantic_cells']:,} grammatical cells**.", "",
        "Gender supplies the form used within a cell and contributes no automatic multiplier. Repeated spellings retain every coordinate. Neither grammatical total is added to the lexical subtotal.", "",
    ]
    (RESULTS / "subanta_capacity_reconciliation.md").write_text("\n".join(lines))
    print("Reconciled the complete name-form capacity model.")


if __name__ == "__main__":
    main()
