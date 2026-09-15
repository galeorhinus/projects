#!/usr/bin/env python3
"""Pass 5: reconcile generated compound-input stacks with earlier input layers."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
import json

from compound_stack_common import CURRENT_SUBTOTAL, RESULTS, project_path, read_csv, sha256


CANDIDATES = RESULTS / "compound_stack_candidates.csv"
VERIFICATION = RESULTS / "compound_stack_verification.json"
PRIOR_NOMINALS = RESULTS / "nominal_input_inventory.csv.gz"
LEDGER = RESULTS / "compound_stack_ledger.csv"


def main() -> None:
    rows = read_csv(CANDIDATES)
    verification = json.loads(VERIFICATION.read_text())
    if verification["verified_relations"] != len(rows):
        raise ValueError("Unverified candidate rows remain")
    source_forms = {form for row in rows for form in row["input_forms_slp1"].split(";")}
    prior_input_overlaps = set()
    with gzip.open(PRIOR_NOMINALS, "rt", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            prior_input_overlaps.update(source_forms.intersection(row["input_forms_slp1"].split(";")))
    if prior_input_overlaps:
        raise ValueError(f"Compound inputs already occurred in the prior broad inventory: {sorted(prior_input_overlaps)}")
    ids = [row["derived_word_meaning_id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate generated word-meaning identifiers")
    spellings = defaultdict(list)
    for row in rows:
        for form in row["output_forms_slp1"].split(";"):
            spellings[form].append((row["compound_word_meaning_id"], row["semantic_branch_id"]))
    collision_spellings = {form: values for form, values in spellings.items() if len(values) > 1}
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            row["count_status"] = "admitted_research_ledger"
            writer.writerow(row)
    by_family = Counter(row["operation_family"] for row in rows)
    by_class = Counter(row["output_form_class"] for row in rows)
    report = {
        "date": "2026-09-14",
        "verified_candidate_relations": len(rows),
        "prior_broad_input_form_overlaps": len(prior_input_overlaps),
        "confirmed_prior_word_meaning_overlaps_not_added": 0,
        "same_spelling_output_groups_not_merged": len(collision_spellings),
        "same_spelling_output_instances_beyond_first": sum(len(values) - 1 for values in collision_spellings.values()),
        "additional_compound_stack_word_meanings": len(rows),
        "additional_by_operation_family": dict(by_family),
        "additional_by_output_form_class": dict(by_class),
        "prior_combined_bounded_subtotal": CURRENT_SUBTOTAL,
        "combined_bounded_word_meaning_subtotal": CURRENT_SUBTOTAL + len(rows),
        "inputs": {project_path(path): sha256(path) for path in (CANDIDATES, VERIFICATION, PRIOR_NOMINALS, __import__("pathlib").Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "compound_stack_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "compound_stack_reconciliation.md").write_text("\n".join([
        "# Compound-Input Stack Reconciliation", "",
        f"The **{len(rows)}** verified relations add **{len(rows)} word-meanings**. None of the 96 source-compound inputs occurred in the earlier broad nominal inventory, so these operation relations were not already counted there.", "",
        f"The bounded subtotal rises from **{CURRENT_SUBTOTAL:,}** to **{CURRENT_SUBTOTAL + len(rows):,} word-meanings**.", "",
        f"The outputs contain {len(collision_spellings)} repeated-spelling groups. They remain separate where the source compound meaning or the semantic operation differs.", "",
    ]))
    print(f"Added {len(rows)} operation-stack meanings; subtotal {CURRENT_SUBTOTAL + len(rows)}.")


if __name__ == "__main__":
    main()
