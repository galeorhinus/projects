#!/usr/bin/env python3
"""Capacity pass 4: reconcile symbolic capacity with the lexical subtotal."""

from __future__ import annotations

import json

from samasa_capacity_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, sha256


ELIGIBILITY = RESULTS / "samasa_capacity_eligibility.json"
SOURCE_FIXTURE = RESULTS / "samasa_verification.json"


def main() -> None:
    eligibility = json.loads(ELIGIBILITY.read_text())
    fixture = json.loads(SOURCE_FIXTURE.read_text())
    report = {
        "date": "2026-09-14",
        "current_materialized_lexical_word_meanings": CURRENT_LEXICAL_SUBTOTAL,
        "symbolic_depth_one_compound_slots": eligibility["eligible_depth_one_relation_slots"],
        "source_demonstrated_fixture_relations": fixture["relations_asserted_by_pinned_active_tests"],
        "locally_regenerated_fixture_relations": fixture["locally_regenerated_relations"],
        "source_fixture_added_to_symbolic_capacity": False,
        "symbolic_capacity_added_to_materialized_lexical_subtotal": False,
        "count_boundary": "The lexical subtotal counts materialized word-meaning records. Compound capacity counts licensed semantic slots at a declared depth. They are reported beside one another and are not summed.",
        "inputs": {project_path(path): sha256(path) for path in (ELIGIBILITY, SOURCE_FIXTURE)},
    }
    (RESULTS / "samasa_capacity_counts.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / "samasa_capacity_counts.md").write_text("\n".join([
        "# समासः Count Boundary", "",
        f"The materialized lexical ledger remains at **{CURRENT_LEXICAL_SUBTOTAL:,} word-meanings**.", "",
        f"The depth-one compound model exposes **{eligibility['eligible_depth_one_relation_slots']:,} formal semantic slots**. The 113 source examples validate the mechanism; they are not added again to that symbolic number.", "",
        "The two numbers answer different questions and must not be summed.", "",
    ]))
    print("Reconciled symbolic capacity without changing the lexical subtotal.")


if __name__ == "__main__":
    main()
