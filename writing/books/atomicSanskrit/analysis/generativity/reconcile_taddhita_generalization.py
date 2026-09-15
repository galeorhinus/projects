#!/usr/bin/env python3
"""Reconcile generalized comparative/superlative meanings with prior ledgers."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
CANDIDATES = RESULTS / "taddhita_generalization_candidates.csv.gz"
VERIFICATION = RESULTS / "taddhita_generalization_verification.json"
PRIOR_LEDGER = RESULTS / "plain_taddhita_ledger.csv"
PRIOR_TOTAL = RESULTS / "plain_taddhita_reconciliation.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deterministic_writer(path: Path, fields: list[str]):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0)
    text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
    writer = csv.DictWriter(text, fieldnames=fields)
    writer.writeheader()
    return raw, text, writer


def main() -> None:
    verification = json.loads(VERIFICATION.read_text())
    prior_total = json.loads(PRIOR_TOTAL.read_text())

    prior_by_key: dict[tuple[str, str], list[str]] = defaultdict(list)
    with PRIOR_LEDGER.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["reconciliation_status"] not in {
                "admitted_additional_plain_relation", "existing_word_meaning_overlap_not_added"
            }:
                continue
            if row["semantic_context"] not in {"AtishayanaSuperlative", "AtishayanaComparative"}:
                continue
            for output in row["expected_output_forms_slp1"].split(";"):
                if output:
                    prior_by_key[(row["semantic_context"], output)].append(row["eligible_word_meaning_id"])

    used_prior: set[str] = set()
    overlaps: Counter[str] = Counter()
    admitted: Counter[str] = Counter()
    output = RESULTS / "taddhita_generalization_ledger.csv.gz"
    with gzip.open(CANDIDATES, "rt", newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or []) + ["prior_overlap_id", "reconciliation_status"]
        raw, text, writer = deterministic_writer(output, fields)
        try:
            for row in reader:
                prior_id = ""
                for candidate_output in row["output_forms_slp1"].split(";"):
                    for possible in prior_by_key.get((row["semantic_context"], candidate_output), []):
                        if possible not in used_prior:
                            prior_id = possible
                            break
                    if prior_id:
                        break
                if prior_id:
                    used_prior.add(prior_id)
                    status = "existing_word_meaning_overlap_not_added"
                    overlaps[row["taddhita_operation_id"]] += 1
                else:
                    status = "admitted_generalized_relation"
                    admitted[row["taddhita_operation_id"]] += 1
                writer.writerow({**row, "prior_overlap_id": prior_id, "reconciliation_status": status})
        finally:
            text.flush(); text.close(); raw.close()

    verified = verification["candidate_relations_verified"]
    if sum(admitted.values()) + sum(overlaps.values()) != verified:
        raise ValueError("Generalized relations do not reconcile with verified candidate count")
    prior = prior_total["combined_bounded_word_meaning_subtotal"]
    added = sum(admitted.values())
    report = {
        "date": "2026-09-14",
        "verified_candidate_relations": verified,
        "existing_word_meaning_overlaps_not_added": sum(overlaps.values()),
        "overlaps_by_operation": dict(overlaps),
        "additional_generalized_word_meanings": added,
        "additional_by_operation": dict(admitted),
        "prior_combined_bounded_word_meaning_subtotal": prior,
        "combined_bounded_word_meaning_subtotal": prior + added,
        "counting_unit": "one nominal input meaning under one comparative or superlative operation; alternative outputs remain variants of that relation",
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (CANDIDATES, VERIFICATION, PRIOR_LEDGER, PRIOR_TOTAL, Path(__file__))
        },
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "taddhita_generalization_reconciliation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "taddhita_generalization_reconciliation.md").write_text(
        "# Comparative and Superlative Reconciliation\n\n"
        f"The pass verifies **{verified:,}** candidate relations. **{sum(overlaps.values()):,}** already {'occurs' if sum(overlaps.values()) == 1 else 'occur'} in the plain-source तद्धित ledger and is not added again. "
        f"The remaining **{added:,}** word-meanings raise the combined bounded subtotal from **{prior:,}** to **{prior + added:,}**.\n"
    )
    print(f"Added {added:,} generalized meanings; subtotal {prior + added:,}.")


if __name__ == "__main__":
    main()
