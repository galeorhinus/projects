#!/usr/bin/env python3
"""Pass 5: reconcile the bounded nan ledger with the prior subtotal."""

from __future__ import annotations

import csv
import gzip
import json

from nan_common import RESULTS, project_path, sha256


PRIOR = RESULTS / "namadhatu_reconciliation.json"
SUMMARY = RESULTS / "nan_summary.json"
LEDGER = RESULTS / "nan_ledger.csv.gz"
VAIDIKA = RESULTS / "vaidika_laukika_reconciliation.json"


def main() -> None:
    prior = json.loads(PRIOR.read_text())
    generated = json.loads(SUMMARY.read_text())
    identifiers = set()
    ledger_count = 0
    with gzip.open(LEDGER, "rt", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            ledger_count += 1
            identifier = row["derived_word_meaning_id"]
            if identifier in identifiers:
                raise ValueError(f"Duplicate nan word-meaning ID: {identifier}")
            identifiers.add(identifier)
    if ledger_count != generated["admitted_nan_word_meanings"]:
        raise ValueError("Nan ledger does not reconcile to its summary")

    old_combined = prior["combined_bounded_word_meaning_subtotal"]
    vaidika = json.loads(VAIDIKA.read_text())["bounded_vaidika_subtotal"]
    old_laukika = old_combined - vaidika
    new_laukika = old_laukika + ledger_count
    combined = new_laukika + vaidika
    report = {
        "date": "2026-09-13",
        "prior_combined_bounded_word_meanings": old_combined,
        "prior_bounded_laukika_word_meanings": old_laukika,
        "bounded_vaidika_subtotal_unchanged": vaidika,
        "additional_nan_word_meanings": ledger_count,
        "bounded_laukika_subtotal_after_nan": new_laukika,
        "combined_bounded_word_meaning_subtotal": combined,
        "complete_inflected_words_counted": 0,
        "counting_boundary": "One nonrecursive nan relation per eligible nominal word-meaning. The a-/an- surface distinction does not multiply meanings.",
        "remaining_layers": ["other bounded compounds", "finite verb conjugation", "nominal declension"],
        "inputs": {project_path(path): sha256(path) for path in (PRIOR, SUMMARY, LEDGER, VAIDIKA, __import__("pathlib").Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "nan_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "nan_reconciliation.md").write_text("\n".join([
        "# नञ् Reconciliation", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Previous combined bounded subtotal | {old_combined:,} |",
        f"| One negative counterpart for each eligible nominal meaning | {ledger_count:,} |",
        f"| **Bounded लौकिक subtotal** | **{new_laukika:,}** |",
        f"| Bounded वैदिक subtotal | {vaidika:,} |",
        f"| **Combined bounded subtotal** | **{combined:,}** |", "",
        "This subtotal still excludes recursive negation, other compounds, finite verb conjugation, and nominal declension.", "",
    ]))
    print(f"Added {ledger_count} nan meanings; combined bounded subtotal {combined}.")


if __name__ == "__main__":
    main()
