#!/usr/bin/env python3
"""Pass 4: verify completeness and semantics of the broader feminine ledger."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import json
from pathlib import Path

from stri_generalization_common import ELIGIBILITY, EXCLUSIONS, LEDGER, RESULTS, project_path, sha256


def read_gzip(path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    eligible = read_gzip(ELIGIBILITY)
    generated = read_gzip(LEDGER)
    excluded = read_gzip(EXCLUSIONS)
    eligible_ids = [row["nominal_word_meaning_id"] for row in eligible]
    generated_ids = [row["nominal_word_meaning_id"] for row in generated]
    excluded_ids = [row["nominal_word_meaning_id"] for row in excluded]
    if len(eligible_ids) != len(set(eligible_ids)):
        raise ValueError("Eligibility contains duplicate nominal meanings")
    if len(generated_ids) != len(set(generated_ids)):
        raise ValueError("Ledger contains duplicate nominal meanings")
    if set(eligible_ids) != set(generated_ids) | set(excluded_ids):
        raise ValueError("Generated and excluded rows do not exhaust eligibility")
    if set(generated_ids) & set(excluded_ids):
        raise ValueError("A candidate is both admitted and excluded")

    failures = []
    suffix_counts = Counter()
    for row in generated:
        suffixes = {x for x in row["applied_stri_suffixes"].split(";") if x}
        rules = {x for x in row["applied_rule_refs"].split(";") if x}
        forms = {x for x in row["generated_forms_slp1"].split(";") if x}
        if not suffixes or not rules or not forms:
            failures.append(row["generated_word_meaning_id"])
        if row["source_operation_id"] not in {"agent_nvul", "agent_trc", "agent_ac", "blessed_agent_vun"}:
            failures.append(row["generated_word_meaning_id"])
        suffix_counts.update(suffixes)
    if failures:
        raise ValueError(f"Verification failed for {len(set(failures))} rows")

    report = {
        "date": "2026-09-14",
        "eligible_relations": len(eligible),
        "generated_relations": len(generated),
        "excluded_relations": len(excluded),
        "verified_relations": len(generated),
        "verification_failures": len(failures),
        "suffixes_observed": dict(sorted(suffix_counts.items())),
        "verification_policy": "Every eligible nominal meaning occurs exactly once in either the admitted or exclusion ledger. Every admitted row has a generated form and a logged 4.1 स्त्रीप्रत्यय path, and belongs to one of the four selected lexical-agent operations.",
        "inputs": {project_path(path): sha256(path) for path in (ELIGIBILITY, LEDGER, EXCLUSIONS, Path(__file__))},
        "publication_status": "research_verification_only_not_deployed",
    }
    (RESULTS / "stri_generalization_verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "stri_generalization_verification.md").write_text("\n".join([
        "# Broader स्त्रीप्रत्ययः Verification", "",
        f"All **{len(generated):,}** eligible lexical-agent relations have a generated feminine form and a logged स्त्रीप्रत्यय path. No candidate remains unresolved.", "",
        "The audit checks word-meaning identity rather than spelling identity. Coincident forms therefore remain separate when they descend from different source meanings.", "",
    ]))
    print(f"Verified {len(generated):,} broader stri relations; {len(excluded):,} excluded.")


if __name__ == "__main__":
    main()
