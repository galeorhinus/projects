#!/usr/bin/env python3
"""Capacity pass 11: reconcile counting, domain, collision, and storage boundaries."""

from __future__ import annotations

import csv
import json

from samasa_capacity_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, sha256


INPUTS = (
    RESULTS / "samasa_capacity_member_inventory.json",
    RESULTS / "samasa_capacity_eligibility.json",
    RESULTS / "samasa_capacity_sample.csv",
    RESULTS / "samasa_reuse_eligibility.json",
    RESULTS / "recursive_samasa_capacity.json",
    RESULTS / "recursive_samasa_sample.csv",
)


def collision_groups(path):
    forms = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            for form in row["generated_forms_slp1"].split(";"):
                forms.setdefault(form, set()).add(row["relation_id"])
    return {form: sorted(relations) for form, relations in forms.items() if len(relations) > 1}


def main() -> None:
    members = json.loads(INPUTS[0].read_text())
    depth_one = json.loads(INPUTS[1].read_text())
    reuse = json.loads(INPUTS[3].read_text())
    depth_two = json.loads(INPUTS[4].read_text())
    collisions = collision_groups(INPUTS[2])
    recursive_collisions = collision_groups(INPUTS[5])
    report = {
        "date": "2026-09-14",
        "materialized_lexical_word_meaning_subtotal": CURRENT_LEXICAL_SUBTOTAL,
        "compoundable_laukika_nominal_meanings": members["compoundable_nominal_word_meanings"],
        "symbolic_depth_one_compound_slots": depth_one["eligible_depth_one_relation_slots"],
        "symbolic_post_compound_derivational_slots": reuse["post_compound_derivational_slots"],
        "symbolic_depth_two_compound_slots": depth_two["depth_two_compound_relation_slots"],
        "symbolic_counts_added_to_lexical_subtotal": False,
        "vaidika_inputs_admitted": False,
        "same_spelling_depth_one_sample_groups": collisions,
        "same_spelling_depth_two_sample_groups": recursive_collisions,
        "same_spelling_meanings_collapsed": False,
        "storage_policy": {
            "store": [
                "canonical nominal word-meaning records in their existing ledgers",
                "relation definitions and exact capacity formulas",
                "verification fixtures and sampled derivation paths",
            ],
            "generate_on_demand": [
                "arbitrary depth-one compound forms",
                "post-compound descendants",
                "depth-two compound forms",
            ],
        },
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
    }
    (RESULTS / "samasa_capacity_reconciliation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "samasa_capacity_reconciliation.md").write_text("\n".join([
        "# समासः Capacity Reconciliation", "",
        "The materialized lexical subtotal, symbolic compound capacity, and inflectional cells remain three separate measurements.", "",
        "The database stores the existing canonical meanings, relation formulas, fixtures, and sampled paths. It generates arbitrary compounds on demand. Same spelling never merges different member meanings or different compound relations.", "",
        "This capacity run is laukika. Vedic compounds and Vedic inflection remain separate.", "",
    ]))
    print("Reconciled compound capacity, domain, collisions, and storage policy.")


if __name__ == "__main__":
    main()
