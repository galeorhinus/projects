#!/usr/bin/env python3
"""Build the admitted one-sanadi verbal word-meaning ledger."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path

from review_yan_semantics import RULE_3124_CODES


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
CANDIDATES = RESULTS / "sanadi_candidate_meanings.csv"
ENGINE = RESULTS / "sanadi_engine_results.csv"
MOVEMENT = RESULTS / "yan_movement_classification.csv"
APPROVALS = HERE / "approved_yan_semantics.json"
STANDARD = HERE / "admission_standard.md"

ANABHIDHANA_CODES = {"01.0847", "06.0046"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def stable_id(*parts: str) -> str:
    payload = "\x1f".join(parts).encode()
    return hashlib.sha256(payload).hexdigest()[:20]


def source_codes(row: dict[str, str]) -> set[str]:
    return {value for value in row["base_source_codes"].split(";") if value}


def engine_index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["operation_id"], row["source_code"]): row for row in rows}


def base_fields(candidate: dict[str, str]) -> dict[str, str]:
    return {
        "base_count_key": candidate["base_count_key"],
        "base_source_codes": candidate["base_source_codes"],
        "base_citations_slp1": candidate["base_citations_slp1"],
        "base_meaning_slp1": candidate["base_meaning_slp1"],
        "base_meaning_display": candidate["base_meaning_display"],
    }


def admitted_row(
    candidate: dict[str, str],
    operation_id: str,
    operation_display: str,
    branch_id: str,
    relation: str,
    rule_refs: str,
    output_forms: set[str] | None = None,
) -> dict[str, str]:
    forms = sorted(output_forms if output_forms is not None else set(candidate["output_forms_slp1"].split(";")))
    return {
        "derived_word_meaning_id": stable_id(operation_id, candidate["base_count_key"], branch_id),
        "operation_id": operation_id,
        "operation_display": operation_display,
        **base_fields(candidate),
        "semantic_branch_id": branch_id,
        "semantic_relation": relation,
        "rule_refs": rule_refs,
        "output_forms_slp1": ";".join(value for value in forms if value),
        "output_variant_count": str(len([value for value in forms if value])),
        "admission_basis": "productive_rule_plus_pinned_engine_output",
        "count_status": "admitted_research_ledger",
    }


def excluded_row(candidate: dict[str, str], operation: str, reason: str, status: str) -> dict[str, str]:
    return {
        "operation_id": operation,
        **base_fields(candidate),
        "output_forms_slp1": candidate["output_forms_slp1"],
        "reason": reason,
        "count_status": status,
    }


def build_ledgers(
    candidates: list[dict[str, str]],
    engine_rows: list[dict[str, str]],
    movement_rows: list[dict[str, str]],
    assignments: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    engine = engine_index(engine_rows)
    movement = {row["base_count_key"]: row["classification"] for row in movement_rows}
    admitted = []
    excluded = []

    for candidate in candidates:
        operation = candidate["operation_id"]
        codes = source_codes(candidate)

        if operation == "causative":
            non_curadi_codes = {
                code for code in codes if engine[(operation, code)]["gana"] != "curAdi"
            }
            if not non_curadi_codes:
                excluded.append(excluded_row(
                    candidate,
                    operation,
                    "The first nic is class-forming under 3.1.25 for this curadigana base; a true causative requires a later stacked-nic pass.",
                    "not_counted_class_forming_nic",
                ))
                continue
            forms = {
                form
                for code in non_curadi_codes
                for form in engine[(operation, code)]["output_forms_slp1"].split(";")
                if form
            }
            admitted.append(admitted_row(
                candidate,
                operation,
                "णिजन्त (ṇijanta), causative",
                "causation",
                "cause an independent agent to perform the base action, or bring about the base state",
                "3.1.26",
                forms,
            ))
            continue

        if operation == "desiderative":
            admitted.append(admitted_row(
                candidate,
                operation,
                "सन्नन्त (sannanta), desiderative",
                "same_agent_desire",
                "desire to perform or undergo the base action or state, with the desirer as its agent",
                "3.1.7",
            ))
            continue

        if operation not in {"intensive", "intensive_luk"}:
            raise ValueError(f"Unexpected operation: {operation}")

        if codes & ANABHIDHANA_CODES:
            excluded.append(excluded_row(
                candidate,
                operation,
                "The Kashika under 3.1.22 explicitly excludes the shobh and ruc formations through anabhidhana.",
                "not_counted_anabhidhana",
            ))
            continue

        display = "यङन्त (yaṅanta)" if operation == "intensive" else "यङ्लुगन्त (yaṅluganta)"
        extra_rule = "" if operation == "intensive" else ";2.4.74"
        inherited = "" if operation == "intensive" else " through the separate yaN-luk derived word"

        if codes & RULE_3124_CODES:
            admitted.append(admitted_row(
                candidate,
                operation,
                display,
                "disparaged_action",
                "perform the base action in a manner that disparages the action itself" + inherited,
                "3.1.24" + extra_rule,
            ))
        elif movement.get(candidate["base_count_key"]) == "direct_movement":
            admitted.append(admitted_row(
                candidate,
                operation,
                display,
                "crooked_movement",
                "perform the base movement crookedly" + inherited,
                "3.1.23" + extra_rule,
            ))
        else:
            for branch, relation in (
                ("repetition", "perform the base action repeatedly"),
                ("intensity", "perform the base action intensely"),
            ):
                admitted.append(admitted_row(
                    candidate,
                    operation,
                    display,
                    branch,
                    relation + inherited,
                    "3.1.22" + extra_rule,
                ))

    # Preserve base meanings for which Vidyut produced no yaN/yaN-luk output.
    lexical = [row for row in assignments if row["record_kind"] == "lexical"]
    generated_keys = {
        (row["operation_id"], row["base_count_key"])
        for row in candidates
        if row["operation_id"] in {"intensive", "intensive_luk"}
    }
    base_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lexical:
        base_by_key[row["normalized_count_key"]].append(row)
    for operation in ("intensive", "intensive_luk"):
        for key, rows in base_by_key.items():
            if (operation, key) in generated_keys:
                continue
            excluded.append({
                "operation_id": operation,
                "base_count_key": key,
                "base_source_codes": ";".join(sorted({row["source_code"] for row in rows})),
                "base_citations_slp1": ";".join(sorted({row["normalized_citation_slp1"] for row in rows})),
                "base_meaning_slp1": ";".join(sorted({row["normalized_meaning_slp1"] for row in rows})),
                "base_meaning_display": ";".join(sorted({row["meaning_display"] for row in rows})),
                "output_forms_slp1": "",
                "reason": "Vidyut 0.4.0 produced no form in the bounded one-operation run; no grammatical prohibition is inferred.",
                "count_status": "not_admitted_engine_zero_unresolved",
            })

    admitted.sort(key=lambda row: (row["operation_id"], row["base_count_key"], row["semantic_branch_id"]))
    excluded.sort(key=lambda row: (row["operation_id"], row["count_status"], row["base_count_key"]))

    spellings: dict[str, set[str]] = defaultdict(set)
    for row in admitted:
        for form in row["output_forms_slp1"].split(";"):
            if form:
                spellings[form].add(row["derived_word_meaning_id"])
    collisions = {form: ids for form, ids in spellings.items() if len(ids) > 1}
    diagnostics = {
        "distinct_output_spellings": len(spellings),
        "spellings_shared_by_multiple_word_meanings": len(collisions),
        "shared_spelling_word_meaning_links": sum(len(ids) for ids in collisions.values()),
        "policy": "Shared spelling does not merge different words or meanings.",
    }
    return admitted, excluded, diagnostics


def build_report(admitted: list[dict[str, str]], excluded: list[dict[str, str]], diagnostics: dict) -> dict:
    manifest = json.loads(MANIFEST.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    for record in records.values():
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")

    by_operation = Counter(row["operation_id"] for row in admitted)
    by_branch = Counter((row["operation_id"], row["semantic_branch_id"]) for row in admitted)
    excluded_by_status = Counter(row["count_status"] for row in excluded)
    source_files = [
        "rule-2.4.74.html", "rule-3.1.7.html", "rule-3.1.22.html",
        "rule-3.1.23.html", "rule-3.1.24.html", "rule-3.1.25.html",
        "rule-3.1.26.html", "vidyut-sanadi.rs",
    ]
    base_total = 2634
    derived_total = len(admitted)
    return {
        "date": "2026-09-13",
        "scope": "One verbal-base sanadi operation, no upasarga, laukika engine mode; inflection and stacked operations excluded.",
        "admission_standard": "A productive rule licenses the word-meaning; the pinned engine constructs its form; explicit restrictions override generation; dictionary attestation is not required.",
        "base_word_meanings": base_total,
        "admitted_derived_word_meanings": derived_total,
        "verbal_word_meanings_including_bases": base_total + derived_total,
        "admitted_by_operation": dict(sorted(by_operation.items())),
        "admitted_by_operation_and_branch": {
            f"{operation}:{branch}": count
            for (operation, branch), count in sorted(by_branch.items())
        },
        "not_admitted_by_status": dict(sorted(excluded_by_status.items())),
        "formation_findings": {
            "causative": "The bounded first-nic run admits non-curadigana causatives. For curadigana-only bases, that nic is class-forming under 3.1.25; their causatives require a stacked-nic run.",
            "desiderative": "Rule 3.1.7 licenses one same-agent desire meaning for each admitted base word-meaning in the bounded run.",
            "yaN": "General 3.1.22 contributes separate repetition and intensity meanings; 3.1.23 and 3.1.24 replace them in their semantic domains.",
            "yaNluk": "A separate derived verbal word inherits the licensed yaN branch and adds no semantic multiplier.",
        },
        "spelling_diagnostics": diagnostics,
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "sources": [records[name] for name in source_files],
        "manifest_source_count": len(manifest["sources"]),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (ASSIGNMENTS, CANDIDATES, ENGINE, MOVEMENT, APPROVALS, STANDARD, MANIFEST, Path(__file__))
        },
    }


def write_markdown(report: dict) -> None:
    op = report["admitted_by_operation"]
    status = report["not_admitted_by_status"]
    branch = report["admitted_by_operation_and_branch"]
    lines = [
        "# Verbal Derivation Ledger: First सनादि (Sanādi) Subtotal", "",
        "This report completes the six-pass verbal-derivation stage. It counts rule-licensed word-meanings produced by one सनादिप्रत्ययः (*sanādipratyayaḥ*) without an उपसर्गः (*upasargaḥ*). It does not count तिङन्तानि (*tiṅantāni*), stacked operations, or nominal formations.", "",
        "## Admission Standard", "",
        "A productive grammatical rule provides positive authorization for a word-meaning. Vidyut supplies a reproducible construction of its form. Dictionary or corpus attestation is not required. An explicit semantic restriction or **अनभिधानम् (*anabhidhānam*)** overrides engine output.", "",
        "## Admitted Word-Meanings", "",
        "| Layer | Word-meanings |",
        "|---|---:|",
        f"| Reconciled base धातु meanings | {report['base_word_meanings']:,} |",
        f"| णिजन्त (*ṇijanta*), causative | {op['causative']:,} |",
        f"| सन्नन्त (*sannanta*), desiderative | {op['desiderative']:,} |",
        f"| यङन्त (*yaṅanta*) | {op['intensive']:,} |",
        f"| यङ्लुगन्त (*yaṅluganta*) | {op['intensive_luk']:,} |",
        f"| **Derived subtotal** | **{report['admitted_derived_word_meanings']:,}** |",
        f"| **Verbal word-meanings including bases** | **{report['verbal_word_meanings_including_bases']:,}** |", "",
        "The यङन्त and यङ्लुगन्त subtotals each contain:", "",
        f"- {branch['intensive:repetition']:,} repetition meanings and {branch['intensive:intensity']:,} intensity meanings under 3.1.22;",
        f"- {branch['intensive:crooked_movement']:,} crooked-movement meanings under 3.1.23; and",
        f"- {branch['intensive:disparaged_action']:,} disparaged-action meanings under 3.1.24.", "",
        "The corresponding यङ्लुगन्त figures are identical because it creates a separate derived verbal word while inheriting the same semantic branch.", "",
        "## What Did Not Enter", "",
        f"- **{status['not_counted_class_forming_nic']:,}** चरादिगणः (*curādigaṇaḥ*) base meanings: the first णिच् (*ṇic*) is class-forming under 3.1.25, not a causative derivation. Their causatives require a later stacked-णिच् run.",
        f"- **{status['not_counted_anabhidhana']:,}** operation/base rows: the Kāśikā explicitly excludes *śobh* and *ruc* from the general यङन्त operation; the exclusion also blocks their यङ्लुगन्त descendants.",
        f"- **{status['not_admitted_engine_zero_unresolved']:,}** operation/base rows: Vidyut returned no यङन्त or यङ्लुगन्त form. These remain unresolved rather than being called grammatically impossible.", "",
        "## Reconciliation", "",
        f"The admitted ledger contains **{report['spelling_diagnostics']['distinct_output_spellings']:,} distinct generated spellings**. **{report['spelling_diagnostics']['spellings_shared_by_multiple_word_meanings']:,} spellings** serve more than one admitted word-meaning. They remain separate because spelling identity does not erase a difference of word or meaning.", "",
        "Every admitted row has one stable derived-word-meaning ID, one base counting key, one operation, one semantic branch, its generated forms, and its governing rule. No duplicate derived-word-meaning IDs remain.", "",
        "## Status", "",
        "This is the first reproducible verbal derivation subtotal, not a replacement Sanskrit vocabulary total. उपसर्गाः (*upasargāḥ*), stacked operations, कृदन्तानि (*kṛdantāni*), तद्धितान्तानि (*taddhitāntāni*), other nominal formations, and inflection remain outside it. The manuscript and its existing published number remain unchanged.", "",
    ]
    (RESULTS / "verbal_derivation_summary.md").write_text("\n".join(lines))


def main() -> None:
    approvals = json.loads(APPROVALS.read_text())
    if approvals["approved_proposal_ids"] != ["YAN-P1", "YAN-P2", "YAN-P3", "YAN-P4", "YAN-P5"]:
        raise ValueError("The five yaN semantic decisions are not approved")
    admitted, excluded, diagnostics = build_ledgers(
        read_csv(CANDIDATES), read_csv(ENGINE), read_csv(MOVEMENT), read_csv(ASSIGNMENTS)
    )
    report = build_report(admitted, excluded, diagnostics)
    write_csv(RESULTS / "verbal_derivation_ledger.csv", admitted, list(admitted[0]))
    write_csv(RESULTS / "verbal_derivation_exclusions.csv", excluded, list(excluded[0]))
    (RESULTS / "verbal_derivation_summary.json").write_text(json.dumps(report, indent=2) + "\n")
    write_markdown(report)
    print(
        f"Admitted {len(admitted)} derived word-meanings; verbal subtotal with {report['base_word_meanings']} bases: {report['verbal_word_meanings_including_bases']}."
    )


if __name__ == "__main__":
    main()
