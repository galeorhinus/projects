#!/usr/bin/env python3
"""Remove broad-ledger overlap from verified conditioned taddhita relations."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import json
from pathlib import Path

from taddhita_conditioned_common import HERE, RESULTS, sha256


VERIFICATION = RESULTS / "conditioned_taddhita_verification.csv"
BROAD_LEDGER = RESULTS / "taddhita_ledger.csv.gz"
PRIOR = RESULTS / "taddhita_reconciliation.json"


def main() -> None:
    with VERIFICATION.open(newline="", encoding="utf-8") as handle:
        verification_rows = list(csv.DictReader(handle))
    verified = [row for row in verification_rows if row["verification_status"] == "verified"]

    candidate_forms = {row["input_form_slp1"] for row in verified}
    existing_keys: set[tuple[str, str, str]] = set()
    existing_outputs: dict[tuple[str, str, str], set[str]] = {}
    with gzip.open(BROAD_LEDGER, "rt", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            matching_inputs = candidate_forms.intersection(row["input_forms_slp1"].split(";"))
            for input_form in matching_inputs:
                key = (input_form, row["semantic_context"], row["taddhita_source_variant"])
                existing_keys.add(key)
                existing_outputs.setdefault(key, set()).update(row["output_forms_slp1"].split(";"))

    admitted = []
    exclusions = []
    for row in verification_rows:
        if row["verification_status"] != "verified":
            exclusions.append({**row, "reconciliation_status": "engine_mismatch_not_admitted"})
            continue
        key = (row["input_form_slp1"], row["semantic_context"], row["taddhita_source_variant"])
        expected = set(row["expected_output_forms_slp1"].split(";"))
        if key in existing_keys:
            status = "existing_broad_relation_overlap_not_added"
            if not expected.intersection(existing_outputs.get(key, set())):
                status = "existing_relation_key_overlap_not_added_output_differs"
            exclusions.append({**row, "reconciliation_status": status})
        else:
            admitted.append({**row, "reconciliation_status": "admitted_conditioned_addition"})

    fields = list(verification_rows[0]) + ["reconciliation_status"]
    admitted_path = RESULTS / "conditioned_taddhita_ledger.csv"
    excluded_path = RESULTS / "conditioned_taddhita_reconciliation_exclusions.csv"
    for path, rows in ((admitted_path, admitted), (excluded_path, exclusions)):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    prior = json.loads(PRIOR.read_text())
    exclusion_counts = Counter(row["reconciliation_status"] for row in exclusions)
    report = {
        "date": "2026-09-13",
        "candidate_relations": len(verification_rows),
        "engine_verified_relations": len(verified),
        "engine_mismatches_not_admitted": exclusion_counts["engine_mismatch_not_admitted"],
        "existing_broad_relation_overlaps_not_added": sum(value for key, value in exclusion_counts.items() if key.startswith("existing_")),
        "additional_conditioned_taddhita_word_meanings": len(admitted),
        "prior_combined_bounded_word_meaning_subtotal": prior["combined_bounded_word_meaning_subtotal"],
        "combined_bounded_word_meaning_subtotal": prior["combined_bounded_word_meaning_subtotal"] + len(admitted),
        "exclusions_by_status": dict(exclusion_counts),
        "overlap_policy": "An exact input-form, semantic-context, and suffix match already represented in the broad taddhita ledger is not added again. Different word-meaning inputs sharing a spelling remain distinguishable inside the broad ledger, but the source test does not identify which such input meaning it intends.",
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (VERIFICATION, BROAD_LEDGER, PRIOR, Path(__file__))},
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "conditioned_taddhita_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Conditioned तद्धित Reconciliation", "",
        f"Of {report['engine_verified_relations']:,} engine-verified conditioned relations, {report['existing_broad_relation_overlaps_not_added']:,} already have the same input form, semantic context, and suffix in the broad तद्धित ledger. The pass therefore adds **{report['additional_conditioned_taddhita_word_meanings']:,} conditioned word-meanings**.", "",
        f"The combined bounded subtotal becomes **{report['combined_bounded_word_meaning_subtotal']:,} word-meanings**. The {report['engine_mismatches_not_admitted']:,} Python-binding mismatches remain available in the exclusion ledger and do not enter this subtotal.", "",
    ]
    (RESULTS / "conditioned_taddhita_reconciliation.md").write_text("\n".join(lines))
    print(f"Added {len(admitted)} conditioned taddhita word-meanings; subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
