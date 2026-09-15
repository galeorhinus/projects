#!/usr/bin/env python3
"""Reconcile the six nominal and taddhita passes into one readable report."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

INPUTS = (
    RESULTS / "nominal_input_inventory_summary.json",
    RESULTS / "taddhita_identifier_classification.json",
    RESULTS / "taddhita_eligibility.json",
    RESULTS / "taddhita_summary.json",
    RESULTS / "taddhita_reconciliation.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    nominal, classification, eligibility, generation, reconciliation = [json.loads(path.read_text()) for path in INPUTS]
    if eligibility["eligible_operation_candidates"] != generation["eligible_operation_candidates"]:
        raise ValueError("Eligibility and generation candidate counts disagree")
    if generation["admitted_taddhita_word_meanings"] + generation["not_admitted_total"] != generation["eligible_operation_candidates"]:
        raise ValueError("Generation does not partition eligible candidates")

    report = {
        "date": "2026-09-13",
        "passes_completed": 6,
        "nominal_input_word_meanings": nominal["admitted_nominal_word_meanings"],
        "taddhita_identifiers_classified": classification["identifier_count"],
        "semantic_operations_selected": eligibility["selected_semantic_operations"],
        "eligible_operation_candidates": eligibility["eligible_operation_candidates"],
        "admitted_taddhita_word_meanings": generation["admitted_taddhita_word_meanings"],
        "unresolved_candidates": generation["not_admitted_total"],
        "additional_word_meanings_after_pilot_overlap": reconciliation["additional_taddhita_word_meanings"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (*INPUTS, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "nominal_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Six-Pass Nominal and तद्धित Expansion", "",
        "The six passes establish the nominal input boundary, classify every pinned तद्धित identifier, declare semantic eligibility, materialize admitted word-meanings, reconcile the previous pilot, and preserve the new incremental subtotal.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | {nominal['admitted_nominal_word_meanings']:,} लौकिक nominal word-meanings admitted as inputs; {nominal['known_vedic_restricted_rows_excluded']:,} known Vedic-restricted rows held outside. |",
        f"| 2 | All {classification['identifier_count']} pinned तद्धित identifiers assigned a classification disposition. |",
        f"| 3 | {eligibility['selected_semantic_operations']} sourced semantic operations admit {eligibility['eligible_operation_candidates']:,} candidate relations. |",
        f"| 4 | The pinned engine materializes {generation['admitted_taddhita_word_meanings']:,} तद्धित word-meanings and leaves {generation['not_admitted_total']:,} unresolved. |",
        f"| 5 | The seven earlier pilot rows are removed from the addition, yielding {reconciliation['additional_taddhita_word_meanings']:,} newly counted meanings. |",
        f"| 6 | The combined bounded subtotal becomes **{reconciliation['combined_bounded_word_meaning_subtotal']:,} word-meanings**. |", "",
        "## Boundary", "",
        "This expansion follows the existing धातु-derived nominal architecture. It does not claim to inventory every independently inherited Sanskrit noun. It admits त्व and तल् for state or defining quality, मतुप् for possession, and three listed ढक् descent examples. Narrower तद्धित relations remain classified but uncounted until their required nominal classes are established.", "",
        "Feminine formations, नामधातवः, compounds, deeper operation stacks, finite verbs, and nominal declension remain outside the subtotal.", "",
    ]
    (RESULTS / "nominal_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six nominal passes complete; combined bounded subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
