#!/usr/bin/env python3
"""Tinanta pass 6: reconcile the citation-form half of the analysis."""

from __future__ import annotations

import json

from tinanta_common import RESULTS, project_path, sha256


INPUTS = tuple(RESULTS / name for name in (
    "tinanta_lakara_classification.json", "tinanta_verbal_inventory.json",
    "tinanta_reconstruction_classification.json", "tinanta_citation_capacity.json",
    "tinanta_citation_sample.json",
))


def main() -> None:
    classification, inventory, reconstruction, capacity, sample = [json.loads(path.read_text()) for path in INPUTS]
    expected = inventory["laukika_verbal_word_meanings"] * classification["counted_laukika_lakaras"]
    if capacity["citation_semantic_cells"] != expected:
        raise ValueError("Citation capacity does not reconcile")
    report = {
        "date": "2026-09-14", "passes_completed": 6,
        "laukika_verbal_word_meanings": inventory["laukika_verbal_word_meanings"],
        "laukika_lakaras": classification["counted_laukika_lakaras"],
        "citation_semantic_cells": expected,
        "sampled_recipe_classes": reconstruction["reconstruction_classes"],
        "locally_regenerated_sample_cells": sample["locally_regenerated_cells"],
        "engine_zero_unresolved_sample_cells": sample["engine_zero_unresolved_cells"],
        "surface_forms_materialized_for_full_capacity": False,
        "capacity_added_to_lexical_subtotal": False,
        "remaining_tinanta_passes": 6,
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
    }
    (RESULTS / "tinanta_citation_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Six-Pass तिङन्त Citation Report", "",
        f"The first six passes identify **{inventory['laukika_verbal_word_meanings']:,}** verbal meanings and ten लौकिक लकाराः. Their third-person singular coordinates provide **{expected:,} semantic grammatical cells**.", "",
        "The capacity is formulaic, while the local sample verifies every reconstruction class through the pinned engine and stores full rule paths. परस्मैपदम् and आत्मनेपदम् forms remain alternatives attached to a cell. No citation cell is added to the lexical word-meaning subtotal.", "",
    ]
    (RESULTS / "tinanta_citation_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six citation passes complete; capacity {expected}.")


if __name__ == "__main__":
    main()
