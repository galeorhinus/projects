#!/usr/bin/env python3
"""Reconcile verified plain taddhita relations against all earlier taddhita ledgers."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
import json
from pathlib import Path

from taddhita_conditioned_common import HERE, RESULTS, sha256


SOURCE = RESULTS / "plain_taddhita_verification.csv"
PRIOR = RESULTS / "suffix_conditioned_reconciliation.json"
EXISTING = {
    "broad_taddhita": RESULTS / "taddhita_ledger.csv.gz",
    "taddhita_pilot": RESULTS / "taddhita_pilot_ledger.csv",
    "conditioned_taddhita": RESULTS / "conditioned_taddhita_ledger.csv",
    "suffix_conditioned": RESULTS / "suffix_conditioned_ledger.csv",
}


def context_for(source_name: str, row: dict[str, str]) -> str:
    if source_name == "taddhita_pilot":
        return {
            "apatyam": "TasyaApatyam",
            "bhava": "TasyaBhava",
            "possession": "TadAsyaAstiAsmin",
        }.get(row["semantic_branch_id"], row["semantic_branch_id"])
    return row.get("semantic_context", "")


def outputs_for(source_name: str, row: dict[str, str]) -> list[str]:
    if source_name == "conditioned_taddhita":
        value = row["generated_output_forms_slp1"] or row["expected_output_forms_slp1"]
    elif source_name == "suffix_conditioned":
        value = row["generated_output_forms_slp1"] or row["expected_output_forms_slp1"]
    else:
        value = row["output_forms_slp1"]
    return [part for part in value.split(";") if part]


def source_rows(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        candidates = list(csv.DictReader(handle))
    verified = [
        row for row in candidates
        if row["verification_status"] in {"verified", "verified_relation_partial_variant_coverage"}
    ]

    wanted = {
        (row["semantic_context"], output)
        for row in verified
        for output in row["expected_output_forms_slp1"].split(";")
    }
    overlaps: dict[tuple[str, str], set[str]] = defaultdict(set)
    for source_name, path in EXISTING.items():
        for row in source_rows(path):
            context = context_for(source_name, row)
            for output in outputs_for(source_name, row):
                key = (context, output)
                if key in wanted:
                    overlaps[key].add(source_name)

    rows = []
    for row in candidates:
        found = {
            source_name
            for output in row["expected_output_forms_slp1"].split(";")
            for source_name in overlaps.get((row["semantic_context"], output), set())
        }
        if row["verification_status"] == "engine_mismatch_not_admitted":
            status = "engine_mismatch_not_admitted"
        elif found:
            status = "existing_word_meaning_overlap_not_added"
        else:
            status = "admitted_additional_plain_relation"
        rows.append({
            **row,
            "existing_ledger_overlaps": ";".join(sorted(found)),
            "reconciliation_status": status,
        })

    output = RESULTS / "plain_taddhita_ledger.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    admitted = [row for row in rows if row["reconciliation_status"] == "admitted_additional_plain_relation"]
    prior = json.loads(PRIOR.read_text())
    prior_total = prior["combined_bounded_word_meaning_subtotal"]
    report = {
        "date": "2026-09-13",
        "verified_candidate_relations": len(verified),
        "existing_word_meaning_overlaps_not_added": sum(
            row["reconciliation_status"] == "existing_word_meaning_overlap_not_added"
            for row in rows
        ),
        "engine_mismatches_not_admitted": sum(
            row["reconciliation_status"] == "engine_mismatch_not_admitted"
            for row in rows
        ),
        "additional_plain_taddhita_word_meanings": len(admitted),
        "additional_nominal_bases": sum(row["output_class"] == "nominal_base" for row in admitted),
        "additional_complete_avyayas": sum(row["output_class"] == "complete_avyaya" for row in admitted),
        "additional_same_referent_or_lexical_derivatives": sum(
            row["relation_class"] == "same_referent_or_lexical_derivative" for row in admitted
        ),
        "prior_combined_bounded_word_meaning_subtotal": prior_total,
        "combined_bounded_word_meaning_subtotal": prior_total + len(admitted),
        "counting_unit": "one source-defined word-meaning; optional outputs and alternative derivational paths do not multiply it",
        "overlaps_by_ledger": dict(Counter(
            source_name
            for row in rows
            for source_name in row["existing_ledger_overlaps"].split(";")
            if source_name
        )),
        "inputs": {
            str(path.relative_to(HERE.parents[1])): sha256(path)
            for path in (SOURCE, PRIOR, *EXISTING.values(), Path(__file__))
        },
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "plain_taddhita_reconciliation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "plain_taddhita_reconciliation.md").write_text(
        "# Plain तद्धित Reconciliation\n\n"
        f"Of {len(verified)} verified source-defined relations, **{report['existing_word_meaning_overlaps_not_added']}** "
        f"already occur in an earlier तद्धित ledger. The remaining **{len(admitted)}** enter as additional "
        f"word-meanings: {report['additional_nominal_bases']} nominal bases and {report['additional_complete_avyayas']} complete अव्यय words.\n\n"
        f"The combined bounded subtotal becomes **{report['combined_bounded_word_meaning_subtotal']:,} word-meanings**.\n"
    )
    print(
        f"Admitted {len(admitted)} new plain taddhita word-meanings; "
        f"subtotal {report['combined_bounded_word_meaning_subtotal']:,}."
    )


if __name__ == "__main__":
    main()
