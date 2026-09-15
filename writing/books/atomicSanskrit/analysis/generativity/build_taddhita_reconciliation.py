#!/usr/bin/env python3
"""Replace the seven-row taddhita pilot with the broad taddhita ledger."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
PRIOR = RESULTS / "vaidika_laukika_reconciliation.json"
PILOT = RESULTS / "taddhita_pilot_ledger.csv"
SUMMARY = RESULTS / "taddhita_summary.json"
LEDGER = RESULTS / "taddhita_ledger.csv.gz"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    prior = json.loads(PRIOR.read_text())
    generated = json.loads(SUMMARY.read_text())
    with PILOT.open(newline="", encoding="utf-8") as handle:
        pilot_rows = list(csv.DictReader(handle))
    expected_overlap = {
        (f"declared:{row['nominal_id']}", row["operation_id"])
        for row in pilot_rows
    }
    actual_overlap = set()
    ledger_count = 0
    with gzip.open(LEDGER, "rt", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            ledger_count += 1
            key = (row["nominal_word_meaning_id"], row["taddhita_operation_id"])
            if key in expected_overlap:
                actual_overlap.add(key)
    if ledger_count != generated["admitted_taddhita_word_meanings"]:
        raise ValueError("Taddhita ledger does not reconcile to its summary")
    if actual_overlap != expected_overlap:
        raise ValueError(f"Pilot overlap mismatch: {len(actual_overlap)} != {len(expected_overlap)}")

    overlap = len(expected_overlap)
    additional = ledger_count - overlap
    old_laukika = prior["current_bounded_laukika_subtotal_after_known_restrictions"]
    vaidika = prior["bounded_vaidika_subtotal"]
    new_laukika = old_laukika + additional
    combined = new_laukika + vaidika
    report = {
        "date": "2026-09-13",
        "prior_combined_bounded_word_meanings": prior["combined_bounded_word_meaning_subtotal"],
        "prior_taddhita_pilot_word_meanings_already_counted": overlap,
        "broad_taddhita_ledger_word_meanings": ledger_count,
        "additional_taddhita_word_meanings": additional,
        "bounded_laukika_subtotal_after_taddhita_expansion": new_laukika,
        "bounded_vaidika_subtotal_unchanged": vaidika,
        "combined_bounded_word_meaning_subtotal": combined,
        "unsupported_vaidika_semantic_candidates_not_counted": prior["unsupported_vaidika_semantic_candidates_not_counted"],
        "scope_limits": [
            "The nominal input boundary contains generated laukika krdanta meanings plus five declared pilot nominals, not every inherited Sanskrit nominal.",
            "Only three general taddhita relations and three listed descendant examples are admitted.",
            "Conditioned taddhita relations, feminine formations, nominally derived verbs, compounds, deeper stacks, and inflection remain outside the subtotal.",
        ],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (PRIOR, PILOT, SUMMARY, LEDGER, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "taddhita_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Broad तद्धित Reconciliation", "",
        "The earlier combined subtotal already contained seven pilot तद्धित word-meanings. This reconciliation replaces that pilot with the broad ledger and adds only the newly materialized rows.", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Previous combined bounded subtotal | {prior['combined_bounded_word_meaning_subtotal']:,} |",
        f"| Broad तद्धित ledger | {ledger_count:,} |",
        f"| Pilot rows already present | -{overlap:,} |",
        f"| **New तद्धित word-meanings added** | **{additional:,}** |",
        f"| **Bounded लौकिक subtotal** | **{new_laukika:,}** |",
        f"| Bounded वैदिक subtotal | {vaidika:,} |",
        f"| **Combined bounded subtotal** | **{combined:,}** |", "",
        "This remains a bounded word-meaning subtotal. तिङन्त and सुबन्त grammatical cells have not entered it.", "",
    ]
    (RESULTS / "taddhita_reconciliation.md").write_text("\n".join(lines))
    print(f"Added {additional} taddhita word-meanings; combined bounded subtotal {combined}.")


if __name__ == "__main__":
    main()
