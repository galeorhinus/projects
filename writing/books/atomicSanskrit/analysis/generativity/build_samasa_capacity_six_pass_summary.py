#!/usr/bin/env python3
"""Capacity pass 6: summarize the depth-one compound-capacity model."""

from __future__ import annotations

import json

from samasa_capacity_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, sha256


INPUTS = (
    RESULTS / "samasa_capacity_rule_classification.json",
    RESULTS / "samasa_capacity_member_inventory.json",
    RESULTS / "samasa_capacity_eligibility.json",
    RESULTS / "samasa_capacity_counts.json",
    RESULTS / "samasa_capacity_sample.json",
)


def main() -> None:
    rules, members, eligibility, counts, sample = [json.loads(path.read_text()) for path in INPUTS]
    total = eligibility["eligible_depth_one_relation_slots"]
    report = {
        "date": "2026-09-14",
        "passes_completed": 6,
        "compoundable_nominal_word_meanings": members["compoundable_nominal_word_meanings"],
        "broad_relation_families_counted": rules["broad_relations_counted"],
        "source_conditioned_families_deferred": rules["conditioned_relation_families_deferred"],
        "symbolic_depth_one_compound_slots": total,
        "locally_regenerated_source_fixture_relations": counts["locally_regenerated_fixture_relations"],
        "locally_regenerated_capacity_sample_relations": sample["locally_regenerated_relations"],
        "materialized_lexical_word_meaning_subtotal": CURRENT_LEXICAL_SUBTOTAL,
        "symbolic_slots_added_to_lexical_subtotal": False,
        "remaining_samasa_capacity_passes": 6,
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
        "publication_status": "research_capacity_only_not_deployed",
    }
    output = RESULTS / "samasa_capacity_six_pass_summary.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Six-Pass Depth-One समासः Capacity", "",
        f"The current **{members['compoundable_nominal_word_meanings']:,}** nominal meanings support **{total:,}** formal semantic slots under four broad compound relations at depth one.", "",
        "| Pass | Result |", "|---:|---|",
        "| 1 | Classify four broad relations and retain ten other families as source-conditioned. |",
        f"| 2 | Build a normalized virtual inventory of {members['compoundable_nominal_word_meanings']:,} nominal meanings without duplicating its rows. |",
        f"| 3 | State exact ordered and unordered pair formulas, producing {total:,} eligible slots. |",
        f"| 4 | Keep the {CURRENT_LEXICAL_SUBTOTAL:,} materialized lexical subtotal separate from symbolic capacity. |",
        f"| 5 | Regenerate {sample['locally_regenerated_relations']} stratified sample relations through pinned Vidyut and retain complete rule paths. |",
        "| 6 | Reconcile the model as capacity at depth one, not as an attested dictionary. |", "",
        "The next six passes measure one further operation over each depth-one compound and exactly one additional compound layer without materializing the resulting space.", "",
    ]
    (RESULTS / "samasa_capacity_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Completed six depth-one capacity passes: {total:,} formal slots.")


if __name__ == "__main__":
    main()
