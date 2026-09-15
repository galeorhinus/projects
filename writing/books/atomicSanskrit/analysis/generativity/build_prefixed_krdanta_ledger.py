#!/usr/bin/env python3
"""Apply the fourteen bounded krdanta operations to one-upasarga meanings."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Krt, Pratipadika, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
INPUT_LEDGER = RESULTS / "upasarga_generation_ledger.csv"
UPASARGAS = HERE / "upasarga_inventory.csv"
CONFIG = HERE / "krt_classification.json"
PRIOR = RESULTS / "conditioned_krdanta_summary.json"
STANDARD = HERE / "admission_standard.md"

LEDGER_FIELDS = [
    "derived_word_meaning_id", "source_prefixed_word_meaning_id", "upasarga_id",
    "operation_id", "krt_source_variant", "operation_display", "base_count_key",
    "base_source_codes", "base_citations_slp1", "base_meaning_slp1",
    "base_meaning_display", "semantic_branch_id", "semantic_relation", "rule_refs",
    "output_forms_slp1", "output_variant_count", "admission_basis", "count_status",
]
EXCLUSION_FIELDS = [
    "source_prefixed_word_meaning_id", "upasarga_id", "operation_id",
    "krt_source_variant", "base_count_key", "base_source_codes", "reason", "count_status",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")
    inputs = read_csv(INPUT_LEDGER)
    inventory = read_csv(UPASARGAS)
    prefix_engine = {row["upasarga_id"]: row["engine_input_slp1"] for row in inventory}
    operations = json.loads(CONFIG.read_text())["bounded_laukika_operations"]
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    entries_by_code = {entry.code: entry for entry in entries}
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    inputs_by_prefix = {row["upasarga_id"]: [] for row in inventory}
    for row in inputs:
        inputs_by_prefix[row["upasarga_id"]].append(row)

    admitted = excluded = source_trials = source_with_output = 0
    by_operation = Counter()
    excluded_by_operation = Counter()
    seen_spellings, shared_spellings = set(), set()
    with gzip.open(RESULTS / "prefixed_krdanta_ledger.csv.gz", "wt", newline="", encoding="utf-8") as out, gzip.open(RESULTS / "prefixed_krdanta_exclusions.csv.gz", "wt", newline="", encoding="utf-8") as rejected:
        writer = csv.DictWriter(out, fieldnames=LEDGER_FIELDS); writer.writeheader()
        reject_writer = csv.DictWriter(rejected, fieldnames=EXCLUSION_FIELDS); reject_writer.writeheader()
        for prefix in inventory:
            prefix_id = prefix["upasarga_id"]
            engine_prefix = prefix_engine[prefix_id]
            engine = {}
            for variant in sorted({row["source_variant"] for row in operations}):
                krt = getattr(Krt, variant)
                for entry in entries:
                    source_trials += 1
                    dhatu = entry.dhatu.with_prefixes([engine_prefix])
                    forms = {result.text for result in grammar.derive(Pratipadika.krdanta(dhatu, krt))}
                    engine[(variant, entry.code)] = forms
                    source_with_output += bool(forms)
            for operation in operations:
                variant = operation["source_variant"]
                for source in inputs_by_prefix[prefix_id]:
                    codes = [code for code in source["base_source_codes"].split(";") if code]
                    forms = sorted({form for code in codes for form in engine[(variant, code)]})
                    if not forms:
                        reject_writer.writerow({
                            "source_prefixed_word_meaning_id": source["generated_word_meaning_id"],
                            "upasarga_id": prefix_id, "operation_id": operation["operation_id"],
                            "krt_source_variant": variant, "base_count_key": source["base_count_key"],
                            "base_source_codes": source["base_source_codes"],
                            "reason": "The selected krt operation produced no form from this prefixed verbal input.",
                            "count_status": "not_admitted_operation_condition_unmet",
                        })
                        excluded += 1; excluded_by_operation[operation["operation_id"]] += 1
                        continue
                    word_id = stable_id("prefixed-krdanta", operation["operation_id"], source["generated_word_meaning_id"])
                    writer.writerow({
                        "derived_word_meaning_id": word_id,
                        "source_prefixed_word_meaning_id": source["generated_word_meaning_id"],
                        "upasarga_id": prefix_id, "operation_id": operation["operation_id"],
                        "krt_source_variant": variant, "operation_display": operation["display"],
                        "base_count_key": source["base_count_key"],
                        "base_source_codes": source["base_source_codes"],
                        "base_citations_slp1": source["base_citations_slp1"],
                        "base_meaning_slp1": source["base_meaning_slp1"],
                        "base_meaning_display": source["base_meaning_display"],
                        "semantic_branch_id": operation["semantic_branch_id"],
                        "semantic_relation": operation["semantic_relation"] + " from the prefixed verbal meaning",
                        "rule_refs": ";".join(operation["rule_refs"]),
                        "output_forms_slp1": ";".join(forms), "output_variant_count": str(len(forms)),
                        "admission_basis": "admitted_one_prefix_meaning_plus_classified_krt_operation_plus_pinned_engine_output",
                        "count_status": "admitted_research_ledger",
                    })
                    admitted += 1; by_operation[operation["operation_id"]] += 1
                    for form in forms:
                        if form in seen_spellings: shared_spellings.add(form)
                        seen_spellings.add(form)

    prior = json.loads(PRIOR.read_text())["bounded_word_meaning_subtotal"]
    records = {row["filename"]: row for row in manifest["sources"]}
    report = {
        "date": "2026-09-13",
        "scope": "Fourteen previously classified laukika krdanta semantic operations applied to every admitted one-upasarga verbal meaning; conditioned krt operations, avyayas, sanadi stacking, and inflection are excluded.",
        "source_prefixed_word_meanings": len(inputs),
        "selected_semantic_operations": len(operations),
        "structural_operation_candidates": len(inputs) * len(operations),
        "source_entry_operations_tested": source_trials,
        "source_entry_operations_with_output": source_with_output,
        "admitted_prefixed_krdanta_word_meanings": admitted,
        "not_admitted_total": excluded,
        "admitted_by_operation": dict(sorted(by_operation.items())),
        "not_admitted_by_operation": dict(sorted(excluded_by_operation.items())),
        "spelling_diagnostics": {"distinct_output_spellings": len(seen_spellings), "spellings_shared_by_multiple_word_meanings": len(shared_spellings)},
        "prior_bounded_word_meaning_subtotal": prior,
        "bounded_word_meaning_subtotal": prior + admitted,
        "vocabulary_total": None, "publication_status": "research_subtotal_only_not_deployed",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "sources": [records[name] for name in ("dhatupatha.tsv", "vidyut-args-krt.rs", "vidyut-krt-basic.rs")],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (INPUT_LEDGER, UPASARGAS, CONFIG, PRIOR, STANDARD, MANIFEST, Path(__file__))},
    }
    (RESULTS / "prefixed_krdanta_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# कृदन्तानि from One-उपसर्गः Meanings", "",
        f"This pass applies fourteen classified laukika कृदन्त meanings to **{len(inputs):,}** admitted one-prefix verbal meanings. Every admitted result is materialized in the compressed ledger.", "",
        "| Measure | Count |", "|---|---:|",
        f"| Structural candidates | {report['structural_operation_candidates']:,} |",
        f"| Admitted word-meanings | {admitted:,} |",
        f"| Outside an operation | {excluded:,} |",
        f"| **Bounded subtotal after this pass** | **{report['bounded_word_meaning_subtotal']:,}** |", "",
        "The exclusions chiefly reflect the pada-sensitive present participles and the complementary obligation suffixes. Missing dictionary attestation is not used as an exclusion.", "",
    ]
    (RESULTS / "prefixed_krdanta_summary.md").write_text("\n".join(lines))
    print(f"Admitted {admitted} one-prefix krdanta word-meanings; bounded subtotal {report['bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
