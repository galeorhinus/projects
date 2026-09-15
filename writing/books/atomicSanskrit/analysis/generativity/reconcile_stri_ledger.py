#!/usr/bin/env python3
"""Pass 5: materialize the source-demonstrated stri word-meaning ledger."""

from __future__ import annotations

from collections import Counter
import csv
import json

from stri_common import RESULTS, project_path, sha256, stable_id


SOURCE = RESULTS / "stri_verification.csv"
PRIOR = RESULTS / "conditioned_taddhita_reconciliation.json"


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    admitted = []
    excluded = []
    for row in rows:
        if row["verification_status"] == "verified_stri_derivation":
            admitted.append({
                **row,
                "generated_word_meaning_id": stable_id("stri-word-meaning", row["stri_relation_id"]),
                "count_status": "admitted_source_demonstrated_stri_word_meaning",
            })
        else:
            excluded.append({**row, "count_status": "not_counted_" + row["verification_status"]})

    fields = list(rows[0]) + ["generated_word_meaning_id", "count_status"]
    with (RESULTS / "stri_ledger.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(admitted)
    exclusion_fields = list(rows[0]) + ["count_status"]
    with (RESULTS / "stri_exclusions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=exclusion_fields)
        writer.writeheader()
        writer.writerows(excluded)

    prior = json.loads(PRIOR.read_text())
    excluded_by_status = Counter(row["verification_status"] for row in excluded)
    report = {
        "date": "2026-09-13",
        "verified_candidates": len(admitted),
        "additional_stri_word_meanings": len(admitted),
        "excluded_by_status": dict(excluded_by_status),
        "prior_combined_bounded_word_meaning_subtotal": prior["combined_bounded_word_meaning_subtotal"],
        "combined_bounded_word_meaning_subtotal": prior["combined_bounded_word_meaning_subtotal"] + len(admitted),
        "counting_policy": "One source-demonstrated input-to-feminine relation contributes one word-meaning. Alternative nominative forms and alternative suffix paths remain variants of that relation. No grammatical case or number cell is counted here.",
        "inputs": {project_path(path): sha256(path) for path in (SOURCE, PRIOR)},
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "stri_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "stri_reconciliation.md").write_text("\n".join([
        "# स्त्रीप्रत्ययः Reconciliation", "",
        f"The source-demonstrated pass adds **{len(admitted)} feminine word-meanings**. The combined bounded subtotal becomes **{report['combined_bounded_word_meaning_subtotal']:,} word-meanings**.", "",
        "Each row is one feminine semantic relation. Its nominative forms provide reproducible evidence but do not add inflectional cells to this lexical subtotal.", "",
    ]))
    print(f"Added {len(admitted)} stri word-meanings; subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
