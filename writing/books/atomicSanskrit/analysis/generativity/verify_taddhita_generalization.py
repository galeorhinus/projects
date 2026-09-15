#!/usr/bin/env python3
"""Verify the generalized comparative/superlative candidate ledger."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Pratipadika, Taddhita, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
LEDGER = RESULTS / "taddhita_generalization_candidates.csv.gz"
EXCLUSIONS = RESULTS / "taddhita_generalization_exclusions.csv.gz"
GENERATION = RESULTS / "taddhita_generalization_generation.json"
ELIGIBILITY = RESULTS / "taddhita_generalization_eligibility.json"
CONFIG = HERE / "taddhita_generalization_operations.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This verification requires Vidyut 0.4.0")
    generation = json.loads(GENERATION.read_text())
    eligibility = json.loads(ELIGIBILITY.read_text())
    config = json.loads(CONFIG.read_text())
    ids: set[str] = set()
    counts: Counter[str] = Counter()
    malformed = 0
    sample_rows: dict[tuple[str, str], dict[str, str]] = {}
    sample_inputs = {"darSanIya", "vezanIya", "Bavana"}
    with gzip.open(LEDGER, "rt", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row_id = row["derived_word_meaning_id"]
            if row_id in ids:
                raise ValueError(f"Duplicate derived word-meaning ID: {row_id}")
            ids.add(row_id)
            counts[row["taddhita_operation_id"]] += 1
            if not row["output_forms_slp1"] or int(row["output_variant_count"]) < 1:
                malformed += 1
            for form in row["input_forms_slp1"].split(";"):
                if form in sample_inputs:
                    sample_rows.setdefault((form, row["taddhita_source_variant"]), row)

    exclusion_count = 0
    with gzip.open(EXCLUSIONS, "rt", newline="", encoding="utf-8") as handle:
        for _ in csv.DictReader(handle):
            exclusion_count += 1
    if sum(counts.values()) != generation["engine_verified_candidate_relations"]:
        raise ValueError("Candidate ledger count differs from generation report")
    if exclusion_count != generation["engine_zero_or_error_relations"]:
        raise ValueError("Exclusion ledger count differs from generation report")
    if sum(counts.values()) + exclusion_count != eligibility["eligible_operation_relations"]:
        raise ValueError("Generated and excluded relations do not exhaust eligibility")
    if malformed:
        raise ValueError(f"Malformed output rows: {malformed}")

    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    expected = {
        ("darSanIya", "tamap"): "darSanIyatama",
        ("darSanIya", "tarap"): "darSanIyatara",
        ("Bavana", "tamap"): "Bavanatama",
        ("Bavana", "tarap"): "Bavanatara",
    }
    sample_checks = []
    for (base, suffix_name), wanted in expected.items():
        outputs = sorted({
            result.text
            for result in grammar.derive(
                Pratipadika.taddhitanta(
                    Pratipadika.basic(base), getattr(Taddhita, suffix_name)
                )
            )
        })
        ledger_row = sample_rows.get((base, suffix_name))
        present = ledger_row is not None and wanted in ledger_row["output_forms_slp1"].split(";")
        if wanted not in outputs or not present:
            raise ValueError(f"Sample verification failed: {base} + {suffix_name} -> {wanted}")
        sample_checks.append({"input_slp1": base, "suffix": suffix_name, "expected_slp1": wanted})

    report = {
        "date": "2026-09-14",
        "candidate_relations_verified": sum(counts.values()),
        "excluded_relations_verified": exclusion_count,
        "verified_by_operation": dict(counts),
        "unique_stable_ids": len(ids),
        "deferred_gunavacana_operations": config["deferred_operations"],
        "malformed_output_rows": malformed,
        "sample_engine_and_ledger_checks": sample_checks,
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (LEDGER, EXCLUSIONS, GENERATION, ELIGIBILITY, CONFIG, Path(__file__))
        },
        "verification_status": "passed",
        "publication_status": "verified_candidate_ledger_not_yet_reconciled",
    }
    (RESULTS / "taddhita_generalization_verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "taddhita_generalization_verification.md").write_text(
        "# Comparative and Superlative Verification\n\n"
        f"All **{sum(counts.values()):,}** generated candidate relations have unique stable IDs and at least one pinned-engine output. "
        f"The **{exclusion_count:,}** engine-zero or error records are preserved separately. The two operations restricted by 5.3.58 remain outside this ledger.\n\n"
        f"Four familiar and generated sample paths were independently rerun through Vidyut 0.4.0. Verification passed.\n"
    )
    print(f"Verified {sum(counts.values()):,} candidate relations; all integrity checks passed.")


if __name__ == "__main__":
    main()
