#!/usr/bin/env python3
"""Tinanta pass 11: reconcile lexical meanings, citation cells, and paradigms."""

from __future__ import annotations

import json

from tinanta_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, sha256


INPUTS = tuple(RESULTS / name for name in (
    "tinanta_verbal_inventory.json", "tinanta_lakara_classification.json",
    "tinanta_citation_capacity.json", "tinanta_citation_sample.json",
    "tinanta_paradigm_capacity.json", "tinanta_pada_classification.json",
    "tinanta_paradigm_sample.json", "tinanta_sample_collisions.json",
))


def main() -> None:
    inventory, lakaras, citation, citation_sample, paradigm, pada, paradigm_sample, collisions = [json.loads(path.read_text()) for path in INPUTS]
    expected_citation = inventory["laukika_verbal_word_meanings"] * lakaras["counted_laukika_lakaras"]
    expected_full = expected_citation * 9
    if citation["citation_semantic_cells"] != expected_citation:
        raise ValueError("Citation cells do not reconcile")
    if paradigm["full_kartari_tinanta_semantic_cells"] != expected_full:
        raise ValueError("Full paradigm cells do not reconcile")
    report = {
        "date": "2026-09-14", "laukika_verbal_word_meanings": inventory["laukika_verbal_word_meanings"],
        "materialized_lexical_word_meaning_subtotal_unchanged": CURRENT_LEXICAL_SUBTOTAL,
        "third_person_singular_citation_cells": expected_citation,
        "full_kartari_person_number_cells": expected_full,
        "additional_cells_beyond_citation_coordinate": expected_full - expected_citation,
        "citation_is_subset_of_full_matrix": True,
        "pada_multiplier": pada["automatic_pada_multiplier"],
        "locally_regenerated_citation_sample_cells": citation_sample["locally_regenerated_cells"],
        "locally_regenerated_full_paradigm_sample_cells": paradigm_sample["semantic_cells_locally_regenerated"],
        "sample_spelling_collisions": collisions["spellings_shared_across_semantic_cells"],
        "all_inflection_rows_materialized": False,
        "inflectional_cells_added_to_lexical_subtotal": False,
        "domain": "laukika_kartari",
        "withheld": ["Vaidika लेट्", "कर्मणि प्रयोग", "भावे प्रयोग", "meaning-specific पद contrasts", "सुबन्त inflection"],
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
    }
    (RESULTS / "tinanta_capacity_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 11: Reconciliation", "", "| Measurement | Result |", "|---|---:|", f"| Materialized lexical word-meanings | {CURRENT_LEXICAL_SUBTOTAL:,} |", f"| लौकिक verbal word-meanings | {inventory['laukika_verbal_word_meanings']:,} |", f"| Third-person singular citation cells | {expected_citation:,} |", f"| Full कर्तरि person-number cells | {expected_full:,} |", "", "The citation coordinates are part of the full matrix, not an additional layer to add on top of it. Neither inflectional total changes the lexical subtotal. The two पद series and optional outputs remain variants attached to their semantic cells.", ""]
    (RESULTS / "tinanta_capacity_reconciliation.md").write_text("\n".join(lines))
    print("Reconciled lexical, citation, and full tinanta counts.")


if __name__ == "__main__":
    main()
