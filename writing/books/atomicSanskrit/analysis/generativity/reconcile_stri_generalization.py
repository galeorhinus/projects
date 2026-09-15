#!/usr/bin/env python3
"""Pass 5: reconcile broader feminine meanings with the earlier source set."""

from __future__ import annotations

from collections import defaultdict
import csv
import gzip
import json
from pathlib import Path

from stri_generalization_common import LEDGER, RESULTS, project_path, sha256


PRIOR = RESULTS / "taddhita_generalization_six_pass_summary.json"
EARLIER_STRI = RESULTS / "stri_ledger.csv"
CONFIRMED_RELATIONS = {
    ("kartf", "kartrI", "agent_trc"),
    ("hartf", "hartrI", "agent_trc"),
}


def main() -> None:
    with gzip.open(LEDGER, "rt", encoding="utf-8", newline="") as handle:
        broad = list(csv.DictReader(handle))
    with EARLIER_STRI.open(encoding="utf-8", newline="") as handle:
        earlier = list(csv.DictReader(handle))

    index = defaultdict(list)
    for row in broad:
        for source_form in row["input_forms_slp1"].split(";"):
            for feminine_form in row["generated_forms_slp1"].split(";"):
                index[(source_form, feminine_form, row["source_operation_id"])].append(row)
    for rows in index.values():
        rows.sort(key=lambda row: (row["base_count_key"], row["generated_word_meaning_id"]))

    used = set()
    overlaps = []
    surface_matches_not_merged = []
    for old in earlier:
        input_form = old["input_form_slp1"]
        for output_form in old["expected_forms_with_stri_suffix_slp1"].split(";"):
            if not output_form:
                continue
            any_surface = [
                row for (source, output, _), rows in index.items()
                if source == input_form and output == output_form
                for row in rows
            ]
            confirmed = [
                row for operation in {row["source_operation_id"] for row in any_surface}
                if (input_form, output_form, operation) in CONFIRMED_RELATIONS
                for row in index[(input_form, output_form, operation)]
                if row["generated_word_meaning_id"] not in used
            ]
            if confirmed:
                row = confirmed[0]
                used.add(row["generated_word_meaning_id"])
                overlaps.append({
                    "earlier_input_slp1": input_form,
                    "earlier_output_slp1": output_form,
                    "generalized_word_meaning_id": row["generated_word_meaning_id"],
                    "source_operation_id": row["source_operation_id"],
                    "base_count_key": row["base_count_key"],
                    "disposition": "same_agent_feminine_relation_not_added_twice",
                })
            elif any_surface:
                surface_matches_not_merged.append({
                    "earlier_input_slp1": input_form,
                    "earlier_output_slp1": output_form,
                    "generalized_candidate_count": len(any_surface),
                    "source_operations": sorted({row["source_operation_id"] for row in any_surface}),
                    "disposition": "same_spelling_without_same_established_meaning_retained_separately",
                })

    prior = json.loads(PRIOR.read_text())["combined_bounded_word_meaning_subtotal"]
    additional = len(broad) - len(overlaps)
    report = {
        "date": "2026-09-14",
        "generated_generalized_relations": len(broad),
        "confirmed_existing_word_meaning_overlaps_not_added": len(overlaps),
        "same_spelling_cases_not_merged": len(surface_matches_not_merged),
        "additional_generalized_stri_word_meanings": additional,
        "prior_combined_bounded_word_meaning_subtotal": prior,
        "combined_bounded_word_meaning_subtotal": prior + additional,
        "overlaps": overlaps,
        "surface_matches_not_merged": surface_matches_not_merged,
        "reconciliation_policy": "Spelling alone never establishes identity. Only the earlier कर्तृ-कर्त्री and हर्तृ-हर्त्री agent relations are confirmed overlaps. Other coincident forms retain separate meanings because their earlier source example does not establish the same derived-agent sense.",
        "inputs": {project_path(path): sha256(path) for path in (LEDGER, EARLIER_STRI, PRIOR, Path(__file__))},
        "publication_status": "research_reconciliation_only_not_deployed",
    }
    (RESULTS / "stri_generalization_reconciliation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "stri_generalization_reconciliation.md").write_text("\n".join([
        "# Broader स्त्रीप्रत्ययः Reconciliation", "",
        f"The broader ledger contains **{len(broad):,}** generated word-meanings. Two agent relations already counted in the source-demonstrated स्त्रीप्रत्यय set are not added again, leaving **{additional:,} new meanings**.", "",
        f"The resulting bounded subtotal is **{prior + additional:,} word-meanings**.", "",
        "Six surface pairs occur in both ledgers, but four are not merged: shared spelling does not prove shared meaning. This follows the analysis-wide rule that homographs remain separate lexical entries.", "",
    ]))
    print(f"Reconciled {len(overlaps)} overlaps; added {additional:,}; subtotal {prior + additional:,}.")


if __name__ == "__main__":
    main()
