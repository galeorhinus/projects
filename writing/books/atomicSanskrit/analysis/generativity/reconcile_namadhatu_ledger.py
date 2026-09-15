#!/usr/bin/env python3
"""Pass 5: reconcile namadhatu meanings with the prior bounded subtotal."""

from __future__ import annotations

import csv
import gzip
import json

from namadhatu_common import RESULTS, project_path, sha256


PRIOR = RESULTS / "stri_six_pass_summary.json"
SUMMARY = RESULTS / "namadhatu_summary.json"
LEDGER = RESULTS / "namadhatu_ledger.csv.gz"


def main() -> None:
    prior = json.loads(PRIOR.read_text())
    generated = json.loads(SUMMARY.read_text())
    ids = set()
    by_kind = {}
    ledger_count = 0
    with gzip.open(LEDGER, "rt", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            ledger_count += 1
            identifier = row["derived_word_meaning_id"]
            if identifier in ids:
                raise ValueError(f"Duplicate namadhatu word-meaning ID: {identifier}")
            ids.add(identifier)
            by_kind[row["source_kind"]] = by_kind.get(row["source_kind"], 0) + 1
    if ledger_count != generated["admitted_namadhatu_word_meanings"]:
        raise ValueError("Namadhatu ledger does not reconcile to its summary")

    old_combined = prior["combined_bounded_word_meaning_subtotal"]
    vaidika = json.loads((RESULTS / "vaidika_laukika_reconciliation.json").read_text())["bounded_vaidika_subtotal"]
    old_laukika = old_combined - vaidika
    new_laukika = old_laukika + ledger_count
    combined = new_laukika + vaidika
    report = {
        "date": "2026-09-13",
        "prior_combined_bounded_word_meanings": old_combined,
        "prior_bounded_laukika_word_meanings": old_laukika,
        "bounded_vaidika_subtotal_unchanged": vaidika,
        "additional_namadhatu_word_meanings": ledger_count,
        "additional_by_source_kind": by_kind,
        "bounded_laukika_subtotal_after_namadhatu": new_laukika,
        "combined_bounded_word_meaning_subtotal": combined,
        "complete_inflected_words_counted": 0,
        "form_boundary": "The new rows are derived verbal bases. तिङन्त inflection remains a later and separately reported expansion.",
        "inputs": {project_path(path): sha256(path) for path in (PRIOR, SUMMARY, LEDGER, __import__("pathlib").Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "namadhatu_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "namadhatu_reconciliation.md").write_text("\n".join([
        "# नामधातुः Reconciliation", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Previous combined bounded subtotal | {old_combined:,} |",
        f"| Productive नामधातुः meanings | {by_kind.get('broad_productive_relation', 0):,} |",
        f"| Source-conditioned नामधातुः meanings | {by_kind.get('source_demonstrated_conditioned_relation', 0):,} |",
        f"| **New नामधातुः meanings** | **{ledger_count:,}** |",
        f"| **Bounded लौकिक subtotal** | **{new_laukika:,}** |",
        f"| Bounded वैदिक subtotal | {vaidika:,} |",
        f"| **Combined bounded subtotal** | **{combined:,}** |", "",
        "The count now exceeds 7.9 million lexical word-meanings. It still contains no finite तिङन्त or declined सुबन्त cells.", "",
    ]))
    print(f"Added {ledger_count} namadhatu meanings; combined bounded subtotal {combined}.")


if __name__ == "__main__":
    main()
