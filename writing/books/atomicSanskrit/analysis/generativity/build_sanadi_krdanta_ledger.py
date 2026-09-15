#!/usr/bin/env python3
"""Apply the fourteen bounded krdanta operations to admitted sanadi meanings."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Krt, Pratipadika, Sanadi, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
VERBAL_LEDGER = RESULTS / "verbal_derivation_ledger.csv"
CURADI_LEDGER = RESULTS / "curadi_causative_ledger.csv"
CONFIG = HERE / "krt_classification.json"
PRIOR = RESULTS / "prefixed_krdanta_summary.json"
STANDARD = HERE / "admission_standard.md"

SANADI_STACKS = {
    "causative": [Sanadi.Ric],
    "desiderative": [Sanadi.san],
    "intensive": [Sanadi.yaN],
    "intensive_luk": [Sanadi.yaNluk],
    "curadi_true_causative": [Sanadi.Ric, Sanadi.Ric],
}

LEDGER_FIELDS = [
    "derived_word_meaning_id", "source_sanadi_word_meaning_id",
    "source_sanadi_operation_id", "sanadi_stack", "operation_id",
    "krt_source_variant", "operation_display", "base_count_key",
    "base_source_codes", "base_citations_slp1", "base_meaning_slp1",
    "base_meaning_display", "source_semantic_branch_id",
    "source_semantic_relation", "semantic_branch_id", "semantic_relation",
    "rule_refs", "output_forms_slp1", "output_variant_count",
    "admission_basis", "count_status",
]
EXCLUSION_FIELDS = [
    "source_sanadi_word_meaning_id", "source_sanadi_operation_id",
    "sanadi_stack", "operation_id", "krt_source_variant", "base_count_key",
    "base_source_codes", "reason", "count_status",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def eligible_codes(source: dict[str, str], entries: dict) -> list[str]:
    codes = [code for code in source["base_source_codes"].split(";") if code]
    operation = source["operation_id"]
    if operation == "causative":
        return [code for code in codes if str(entries[code].dhatu.gana) != "curAdi"]
    if operation == "curadi_true_causative":
        return [code for code in codes if str(entries[code].dhatu.gana) == "curAdi"]
    return codes


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")

    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")

    inputs = read_csv(VERBAL_LEDGER) + read_csv(CURADI_LEDGER)
    operations = json.loads(CONFIG.read_text())["bounded_laukika_operations"]
    entries = {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)

    inputs_by_stack: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in inputs:
        if row["operation_id"] not in SANADI_STACKS:
            raise ValueError(f"Unexpected sanadi operation: {row['operation_id']}")
        inputs_by_stack[row["operation_id"]].append(row)

    admitted = excluded = source_trials = source_with_output = 0
    by_source_operation = Counter()
    by_krt_operation = Counter()
    excluded_by_krt_operation = Counter()
    seen_spellings, shared_spellings = set(), set()

    with gzip.open(
        RESULTS / "sanadi_krdanta_ledger.csv.gz", "wt", newline="", encoding="utf-8"
    ) as out, gzip.open(
        RESULTS / "sanadi_krdanta_exclusions.csv.gz", "wt", newline="", encoding="utf-8"
    ) as rejected:
        writer = csv.DictWriter(out, fieldnames=LEDGER_FIELDS)
        reject_writer = csv.DictWriter(rejected, fieldnames=EXCLUSION_FIELDS)
        writer.writeheader()
        reject_writer.writeheader()

        for source_operation, source_rows in sorted(inputs_by_stack.items()):
            stack = SANADI_STACKS[source_operation]
            source_codes = sorted({
                code
                for row in source_rows
                for code in eligible_codes(row, entries)
            })
            engine: dict[tuple[str, str], set[str]] = {}
            for variant in sorted({row["source_variant"] for row in operations}):
                krt = getattr(Krt, variant)
                for code in source_codes:
                    source_trials += 1
                    dhatu = entries[code].dhatu.with_sanadi(stack)
                    forms = {
                        result.text
                        for result in grammar.derive(Pratipadika.krdanta(dhatu, krt))
                    }
                    engine[(variant, code)] = forms
                    source_with_output += bool(forms)

            stack_label = "+".join(str(value) for value in stack)
            for operation in operations:
                variant = operation["source_variant"]
                for source in source_rows:
                    codes = eligible_codes(source, entries)
                    forms = sorted({
                        form
                        for code in codes
                        for form in engine[(variant, code)]
                    })
                    common = {
                        "source_sanadi_word_meaning_id": source["derived_word_meaning_id"],
                        "source_sanadi_operation_id": source_operation,
                        "sanadi_stack": stack_label,
                        "operation_id": operation["operation_id"],
                        "krt_source_variant": variant,
                        "base_count_key": source["base_count_key"],
                        "base_source_codes": ";".join(codes),
                    }
                    if not forms:
                        reject_writer.writerow({
                            **common,
                            "reason": "The selected krt operation produced no form from this admitted sanadi verbal input.",
                            "count_status": "not_admitted_operation_condition_unmet",
                        })
                        excluded += 1
                        excluded_by_krt_operation[operation["operation_id"]] += 1
                        continue

                    writer.writerow({
                        "derived_word_meaning_id": stable_id(
                            "sanadi-krdanta", operation["operation_id"],
                            source["derived_word_meaning_id"],
                        ),
                        **common,
                        "operation_display": operation["display"],
                        "base_citations_slp1": source["base_citations_slp1"],
                        "base_meaning_slp1": source["base_meaning_slp1"],
                        "base_meaning_display": source["base_meaning_display"],
                        "source_semantic_branch_id": source["semantic_branch_id"],
                        "source_semantic_relation": source["semantic_relation"],
                        "semantic_branch_id": operation["semantic_branch_id"],
                        "semantic_relation": (
                            operation["semantic_relation"]
                            + " from the admitted sanadi-derived verbal meaning"
                        ),
                        "rule_refs": ";".join(
                            source["rule_refs"].split(";") + operation["rule_refs"]
                        ),
                        "output_forms_slp1": ";".join(forms),
                        "output_variant_count": str(len(forms)),
                        "admission_basis": "admitted_sanadi_meaning_plus_classified_krt_operation_plus_pinned_engine_output",
                        "count_status": "admitted_research_ledger",
                    })
                    admitted += 1
                    by_source_operation[source_operation] += 1
                    by_krt_operation[operation["operation_id"]] += 1
                    for form in forms:
                        if form in seen_spellings:
                            shared_spellings.add(form)
                        seen_spellings.add(form)

    prior = json.loads(PRIOR.read_text())["bounded_word_meaning_subtotal"]
    records = {row["filename"]: row for row in manifest["sources"]}
    report = {
        "date": "2026-09-13",
        "scope": "Fourteen bounded laukika krdanta semantic operations applied to each admitted one-sanadi meaning and each admitted true curadigana causative; prefixes, further sanadi stacking, Vedic operations, and inflection are excluded.",
        "source_one_sanadi_word_meanings": len(read_csv(VERBAL_LEDGER)),
        "source_curadi_true_causative_word_meanings": len(read_csv(CURADI_LEDGER)),
        "source_sanadi_word_meanings": len(inputs),
        "selected_semantic_operations": len(operations),
        "structural_operation_candidates": len(inputs) * len(operations),
        "source_entry_operations_tested": source_trials,
        "source_entry_operations_with_output": source_with_output,
        "admitted_sanadi_krdanta_word_meanings": admitted,
        "not_admitted_total": excluded,
        "admitted_by_source_sanadi_operation": dict(sorted(by_source_operation.items())),
        "admitted_by_krt_operation": dict(sorted(by_krt_operation.items())),
        "not_admitted_by_krt_operation": dict(sorted(excluded_by_krt_operation.items())),
        "spelling_diagnostics": {
            "distinct_output_spellings": len(seen_spellings),
            "spellings_shared_by_multiple_word_meanings": len(shared_spellings),
            "policy": "Different admitted words or meanings remain separate when their spellings coincide.",
        },
        "prior_bounded_word_meaning_subtotal": prior,
        "bounded_word_meaning_subtotal": prior + admitted,
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "engine": {
            "name": "Vidyut", "version": importlib.metadata.version("vidyut"),
            "commit": manifest["generator_commit"],
        },
        "sources": [
            records[name]
            for name in (
                "dhatupatha.tsv", "vidyut-args-krt.rs", "vidyut-krt-basic.rs",
                "vidyut-sanadi.rs", "rule-3.1.7.html", "rule-3.1.22.html",
                "rule-3.1.23.html", "rule-3.1.24.html", "rule-3.1.25.html",
                "rule-3.1.26.html",
            )
        ],
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                VERBAL_LEDGER, CURADI_LEDGER, CONFIG, PRIOR, STANDARD,
                MANIFEST, Path(__file__),
            )
        },
    }
    (RESULTS / "sanadi_krdanta_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# कृदन्तानि from सनादि Meanings", "",
        f"This pass applies fourteen classified laukika कृदन्त meanings to **{len(inputs):,}** admitted सनादि-derived verbal meanings. That input includes **{report['source_one_sanadi_word_meanings']:,}** one-operation meanings and **{report['source_curadi_true_causative_word_meanings']:,}** true चरादिगणः causatives.", "",
        "| Measure | Count |", "|---|---:|",
        f"| Structural candidates | {report['structural_operation_candidates']:,} |",
        f"| Admitted word-meanings | {admitted:,} |",
        f"| Outside an operation | {excluded:,} |",
        f"| **Bounded subtotal after this pass** | **{report['bounded_word_meaning_subtotal']:,}** |", "",
        "The engine reconstructs each source as a structured धातुः plus its सनादि operation. चरादिगणः true causatives retain both णिच् operations. Coincident spellings do not merge distinct source meanings or semantic operations.", "",
        "The ledger remains laukika. Vedic-only कृदन्त operations are reserved for a separate domain-specific pass.", "",
    ]
    (RESULTS / "sanadi_krdanta_summary.md").write_text("\n".join(lines))
    print(
        f"Admitted {admitted} sanadi-derived krdanta word-meanings; "
        f"bounded subtotal {report['bounded_word_meaning_subtotal']}."
    )


if __name__ == "__main__":
    main()
