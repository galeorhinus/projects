#!/usr/bin/env python3
"""Reconcile the bounded Laukika and Vaidika ledgers without double counting."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
DOMAIN = RESULTS / "domain_boundary_audit.json"
DIRECT = RESULTS / "vaidika_direct_summary.json"
CONDITIONED = RESULTS / "vaidika_conditioned_summary.json"
STACKED = RESULTS / "vaidika_stacked_summary.json"

LEDGERS = [
    (RESULTS / "vaidika_direct_ledger.csv", "derived_word_meaning_id", "csv"),
    (RESULTS / "vaidika_conditioned_ledger.csv", "derived_word_meaning_id", "csv"),
    (RESULTS / "vaidika_stacked_ledger.csv.gz", "derived_word_meaning_id", "gzip"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ledger_ids(path: Path, field: str, kind: str) -> list[str]:
    opener = gzip.open if kind == "gzip" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return [row[field] for row in csv.DictReader(handle)]


def main() -> None:
    domain = json.loads(DOMAIN.read_text())
    direct = json.loads(DIRECT.read_text())
    conditioned = json.loads(CONDITIONED.read_text())
    stacked = json.loads(STACKED.read_text())
    expected_specific = (
        direct["admitted_vaidika_direct_word_meanings"]
        + conditioned["admitted_vaidika_conditioned_word_meanings"]
        + stacked["admitted_vaidika_stacked_word_meanings"]
    )
    if expected_specific != stacked["vaidika_specific_subtotal"]:
        raise ValueError("Vaidika-specific subtotal does not equal its materialized layers")
    all_ids = []
    ledger_counts = {}
    for path, field, kind in LEDGERS:
        ids = ledger_ids(path, field, kind)
        ledger_counts[path.name] = len(ids)
        all_ids.extend(ids)
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("A Vaidika word-meaning identifier appears in more than one ledger")
    if len(all_ids) != expected_specific:
        raise ValueError("Materialized Vaidika rows do not match the summary subtotal")

    known_laukika = domain["bounded_laukika_subtotal_after_known_domain_restrictions"]
    reclassified_vedic = domain["known_vedic_restricted_base_and_descendant_rows"]
    gross_prior = domain["gross_bounded_word_meaning_subtotal"]
    if known_laukika + reclassified_vedic != gross_prior:
        raise ValueError("The earlier subtotal does not partition at the known domain boundary")
    vaidika_subtotal = reclassified_vedic + expected_specific
    combined = known_laukika + vaidika_subtotal
    if combined != gross_prior + expected_specific:
        raise ValueError("Combined subtotal double-counts or drops a domain layer")

    report = {
        "date": "2026-09-13",
        "current_bounded_laukika_subtotal_after_known_restrictions": known_laukika,
        "vedic_only_base_and_ordinary_descendant_word_meanings": reclassified_vedic,
        "vaidika_specific_operation_word_meanings": expected_specific,
        "bounded_vaidika_subtotal": vaidika_subtotal,
        "combined_bounded_word_meaning_subtotal": combined,
        "materialized_vaidika_ledger_counts": ledger_counts,
        "unsupported_vaidika_semantic_candidates_not_counted": sum(
            row["semantic_candidates"] for row in conditioned["coverage_gaps"]
        ),
        "partition_policy": "The prior twelve-pass subtotal is split into the current bounded laukika subtotal and rows descending from bases explicitly documented as Vedic-only. Vaidika-specific operations are then added once. Alternative forms and accents remain attributes of one semantic row.",
        "scope_limits": [
            "The 2,623 bases without a restriction in cited evidence are not thereby proved exhaustively laukika.",
            "Unsupported Vaidika suffix families contribute zero rather than being treated as prohibited.",
            "Two-prefix, prefix-plus-sanadi, deeper stacking, nominal expansion, compounds, and inflection remain outside the Vaidika run.",
            "The combined figure is a reproducible research subtotal, not a complete Sanskrit vocabulary total.",
        ],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (DOMAIN, DIRECT, CONDITIONED, STACKED, *[item[0] for item in LEDGERS], Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "vaidika_laukika_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Laukika-Vaidika Reconciliation", "",
        "The two domains are reconciled by semantic row, not by spelling. A Vaidika operation creates a new word-meaning only when a source rule supplies the operation and the pinned Vedic-mode engine supplies its form.", "",
        "| Domain layer | Word-meanings |", "|---|---:|",
        f"| Current bounded laukika subtotal after known restrictions | {known_laukika:,} |",
        f"| Bases documented as Vedic-only and their ordinary-rule descendants | {reclassified_vedic:,} |",
        f"| Vaidika-specific operations materialized in the new ledgers | {expected_specific:,} |",
        f"| **Bounded Vaidika subtotal** | **{vaidika_subtotal:,}** |",
        f"| **Combined bounded subtotal** | **{combined:,}** |", "",
        f"A further **{report['unsupported_vaidika_semantic_candidates_not_counted']:,} semantic candidates** remain uncounted because the pinned engine does not implement their Vedic suffix forms. They are unresolved capacity, not rejected formations.", "",
        "The combined subtotal remains deliberately bounded. It does not include inflection, compounds, deeper operation stacks, or the unsupported Vaidika families, and it is not presented as the complete number of Sanskrit words.", "",
    ]
    (RESULTS / "vaidika_laukika_reconciliation.md").write_text("\n".join(lines))
    print(f"Bounded Vaidika subtotal {vaidika_subtotal}; combined bounded subtotal {combined}.")


if __name__ == "__main__":
    main()
