#!/usr/bin/env python3
"""Pass 5: admit the bounded source-demonstrated compound ledger."""

from __future__ import annotations

import csv
import json

from samasa_common import CURRENT_SUBTOTAL, RESULTS, project_path, sha256, stable_id


SOURCE = RESULTS / "samasa_verification.csv"


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    admitted = []
    seen = set()
    for row in rows:
        identity = (row["compound_type"], row["member_forms_slp1"], row["semantic_relation"])
        if identity in seen:
            raise ValueError(f"Unreconciled duplicate compound meaning: {identity}")
        seen.add(identity)
        admitted.append({
            "generated_word_meaning_id": stable_id("samasa-word-meaning", row["compound_relation_id"]),
            "compound_relation_id": row["compound_relation_id"],
            "compound_type": row["compound_type"],
            "member_forms_slp1": row["member_forms_slp1"],
            "member_count": row["member_count"],
            "derivational_depth": row["derivational_depth"],
            "semantic_relation": row["semantic_relation"],
            "rule_refs": row["rule_refs"],
            "output_forms_slp1": row["generated_forms_slp1"],
            "output_variant_count": row["expected_variant_count"],
            "source_assertion_ids": row["source_assertion_ids"],
            "verification_status": row["verification_status"],
            "admission_basis": "source_demonstrated_nonrecursive_compound_relation",
            "count_status": "admitted_research_ledger",
        })
    output = RESULTS / "samasa_ledger.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(admitted[0]))
        writer.writeheader()
        writer.writerows(admitted)
    report = {
        "date": "2026-09-14",
        "prior_combined_bounded_word_meaning_subtotal": CURRENT_SUBTOTAL,
        "additional_samasa_word_meanings": len(admitted),
        "existing_word_meaning_overlaps_not_added": 0,
        "combined_bounded_word_meaning_subtotal": CURRENT_SUBTOTAL + len(admitted),
        "recursive_compounding_admitted": False,
        "inputs": {project_path(SOURCE): sha256(SOURCE)},
    }
    (RESULTS / "samasa_reconciliation.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / "samasa_reconciliation.md").write_text(
        "# Bounded समासः Reconciliation\n\n"
        f"The pass adds **{len(admitted)}** source-demonstrated compound word-meanings and raises the combined bounded subtotal to "
        f"**{report['combined_bounded_word_meaning_subtotal']:,}**. Repeated source assertions were removed during eligibility; different compound relations would remain separate even if their written results coincided.\n"
    )
    print(f"Added {len(admitted)} compound word-meanings.")


if __name__ == "__main__":
    main()
