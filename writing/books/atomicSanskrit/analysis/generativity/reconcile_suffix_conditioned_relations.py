#!/usr/bin/env python3
"""Remove overlap and admit verified additional suffix word-meanings."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import json
from pathlib import Path

from taddhita_conditioned_common import HERE, RESULTS, sha256


VERIFICATION = RESULTS / "suffix_conditioned_verification.csv"
BROAD = RESULTS / "taddhita_ledger.csv.gz"
CONDITIONED = RESULTS / "conditioned_taddhita_ledger.csv"
PRIOR = RESULTS / "nan_reconciliation.json"


def keys_from(path: Path, compressed: bool = False) -> set[tuple[str, str, str]]:
    opener = gzip.open if compressed else open
    keys = set()
    with opener(path, "rt", newline="", encoding="utf-8") if compressed else opener(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            inputs = row.get("input_forms_slp1", row.get("input_form_slp1", "")).split(";")
            context = row["semantic_context"]
            suffix = row["taddhita_source_variant"]
            keys.update((input_form, context, suffix) for input_form in inputs if input_form)
    return keys


def main() -> None:
    with VERIFICATION.open(newline="", encoding="utf-8") as handle:
        verification_rows = list(csv.DictReader(handle))
    existing = keys_from(BROAD, compressed=True) | keys_from(CONDITIONED)

    admitted = []
    excluded = []
    for row in verification_rows:
        key = (row["input_form_slp1"], row["semantic_context"], row["taddhita_source_variant"])
        if not row["verification_status"].startswith("verified"):
            status = "engine_mismatch_not_admitted"
        elif key in existing:
            status = "existing_relation_overlap_not_added"
        else:
            status = "admitted_additional_conditioned_relation"
        target = admitted if status.startswith("admitted_") else excluded
        target.append({**row, "reconciliation_status": status})

    fields = list(verification_rows[0]) + ["reconciliation_status"]
    for path, rows in (
        (RESULTS / "suffix_conditioned_ledger.csv", admitted),
        (RESULTS / "suffix_conditioned_exclusions.csv", excluded),
    ):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    prior = json.loads(PRIOR.read_text())
    counts = Counter(row["reconciliation_status"] for row in excluded)
    previous = prior["combined_bounded_word_meaning_subtotal"]
    report = {
        "date": "2026-09-13",
        "candidate_relations": len(verification_rows),
        "verified_relations": sum(row["verification_status"].startswith("verified") for row in verification_rows),
        "existing_relation_overlaps_not_added": counts["existing_relation_overlap_not_added"],
        "engine_mismatches_not_admitted": counts["engine_mismatch_not_admitted"],
        "additional_suffix_word_meanings": len(admitted),
        "prior_combined_bounded_word_meaning_subtotal": previous,
        "combined_bounded_word_meaning_subtotal": previous + len(admitted),
        "counting_unit": "one source-conditioned input-meaning-suffix relation; output variants do not multiply it",
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (VERIFICATION, BROAD, CONDITIONED, PRIOR, Path(__file__))},
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "suffix_conditioned_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "suffix_conditioned_reconciliation.md").write_text(
        "# Additional Suffix Reconciliation\n\n"
        f"After engine verification and overlap removal, this pass adds **{len(admitted)} word-meanings**. "
        f"The combined bounded subtotal becomes **{report['combined_bounded_word_meaning_subtotal']:,}**.\n\n"
        "Alternative output forms attached to one input, meaning, and suffix remain variants of one counted relation.\n"
    )
    print(f"Added {len(admitted)} suffix word-meanings; subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
