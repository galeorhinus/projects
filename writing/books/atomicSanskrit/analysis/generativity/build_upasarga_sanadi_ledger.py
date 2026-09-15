#!/usr/bin/env python3
"""Build the bounded one-upasarga plus one-sanadi word-meaning ledger."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Sanadi, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
INVENTORY = HERE / "upasarga_inventory.csv"
CONFLICTS = HERE / "upasarga_conflicts.json"
VERBAL_LEDGER = RESULTS / "verbal_derivation_ledger.csv"
PRIOR_SUMMARY = RESULTS / "upasarga_generation_summary.json"
STANDARD = HERE / "admission_standard.md"

SANADI_BY_OPERATION = {
    "causative": Sanadi.Ric,
    "desiderative": Sanadi.san,
    "intensive": Sanadi.yaN,
    "intensive_luk": Sanadi.yaNluk,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_gzip_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with gzip.open(path, "wt", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def verify_inputs() -> tuple[dict, list[dict[str, str]], dict]:
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")
    inventory = read_csv(INVENTORY)
    conflicts = json.loads(CONFLICTS.read_text())
    if len(inventory) != 20:
        raise ValueError("Expected twenty normalized upasarga identities")
    return manifest, inventory, conflicts


def run_engine(entries, inventory: list[dict[str, str]]) -> tuple[dict[tuple[str, str, str], set[str]], dict]:
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    index: dict[tuple[str, str, str], set[str]] = {}
    tested = generated = 0
    zero_by_operation = Counter()
    for prefix in inventory:
        prefix_id = prefix["upasarga_id"]
        engine_prefix = prefix["engine_input_slp1"]
        for operation_id, sanadi in SANADI_BY_OPERATION.items():
            for entry in entries:
                tested += 1
                dhatu = entry.dhatu.with_prefixes([engine_prefix]).with_sanadi([sanadi])
                outputs = {result.text for result in grammar.derive(dhatu)}
                index[(prefix_id, operation_id, entry.code)] = outputs
                if outputs:
                    generated += 1
                else:
                    zero_by_operation[operation_id] += 1
    return index, {
        "source_entry_operations_tested": tested,
        "source_entry_operations_with_output": generated,
        "source_entry_zero_outputs": tested - generated,
        "zero_outputs_by_operation": dict(sorted(zero_by_operation.items())),
    }


def build_ledgers(
    verbal_rows: list[dict[str, str]],
    inventory: list[dict[str, str]],
    conflicts: dict,
    entries_by_code: dict,
    engine: dict[tuple[str, str, str], set[str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    blocked = {
        (row["upasarga_id"], row["base_count_key"]): row
        for row in conflicts["exclusions"]
    }
    admitted = []
    excluded = []
    for prefix in inventory:
        prefix_id = prefix["upasarga_id"]
        for row in verbal_rows:
            block = blocked.get((prefix_id, row["base_count_key"]))
            if block:
                excluded.append({
                    "upasarga_id": prefix_id,
                    "derived_word_meaning_id": row["derived_word_meaning_id"],
                    "operation_id": row["operation_id"],
                    "base_count_key": row["base_count_key"],
                    "reason": block["reason"],
                    "rule_refs": ";".join(block["rule_refs"]),
                    "count_status": "not_counted_documented_base_meaning_conflict",
                })
                continue

            codes = [value for value in row["base_source_codes"].split(";") if value]
            if row["operation_id"] == "causative":
                codes = [code for code in codes if str(entries_by_code[code].dhatu.gana) != "curAdi"]
            forms = {
                form
                for code in codes
                for form in engine[(prefix_id, row["operation_id"], code)]
            }
            if not forms:
                excluded.append({
                    "upasarga_id": prefix_id,
                    "derived_word_meaning_id": row["derived_word_meaning_id"],
                    "operation_id": row["operation_id"],
                    "base_count_key": row["base_count_key"],
                    "reason": "Vidyut produced no form; no grammatical prohibition is inferred.",
                    "rule_refs": row["rule_refs"],
                    "count_status": "not_admitted_engine_zero_unresolved",
                })
                continue

            admitted.append({
                "stacked_word_meaning_id": stable_id(
                    "upasarga-sanadi", prefix_id, row["derived_word_meaning_id"]
                ),
                "upasarga_id": prefix_id,
                "upasarga_order": prefix["order"],
                "upasarga_source_forms_slp1": prefix["source_forms_slp1"],
                "sanadi_word_meaning_id": row["derived_word_meaning_id"],
                "operation_id": row["operation_id"],
                "operation_display": row["operation_display"],
                "base_count_key": row["base_count_key"],
                "base_source_codes": row["base_source_codes"],
                "base_citations_slp1": row["base_citations_slp1"],
                "base_meaning_slp1": row["base_meaning_slp1"],
                "base_meaning_display": row["base_meaning_display"],
                "semantic_branch_id": row["semantic_branch_id"],
                "semantic_relation": f"{row['semantic_relation']} with the action modified by {prefix_id}",
                "rule_refs": "1.4.58;1.4.59;" + row["rule_refs"],
                "output_forms_slp1": ";".join(sorted(forms)),
                "output_variant_count": str(len(forms)),
                "admission_basis": "admitted_sanadi_meaning_plus_productive_upasarga_plus_pinned_engine_output",
                "count_status": "admitted_generated_capacity",
            })
    admitted.sort(key=lambda row: (int(row["upasarga_order"]), row["operation_id"], row["base_count_key"], row["semantic_branch_id"]))
    excluded.sort(key=lambda row: (row["upasarga_id"], row["operation_id"], row["base_count_key"]))
    return admitted, excluded


def build_report(
    manifest: dict,
    inventory: list[dict[str, str]],
    engine_report: dict,
    admitted_sanadi_meanings: int,
    admitted: list[dict[str, str]],
    excluded: list[dict[str, str]],
) -> dict:
    prior = json.loads(PRIOR_SUMMARY.read_text())
    by_operation = Counter(row["operation_id"] for row in admitted)
    by_status = Counter(row["count_status"] for row in excluded)
    source_names = [
        "dhatupatha.tsv", "dhatupatha-sanskritdocuments.html", "vidyut-args-dhatu.rs",
        "vidyut-sanadi.rs", "rule-1.4.58.html", "rule-1.4.59.html",
        "rule-2.4.74.html", "rule-3.1.7.html", "rule-3.1.22.html",
        "rule-3.1.23.html", "rule-3.1.24.html", "rule-3.1.25.html", "rule-3.1.26.html",
    ]
    records = {row["filename"]: row for row in manifest["sources"]}
    spellings: dict[str, set[str]] = defaultdict(set)
    for row in admitted:
        for form in row["output_forms_slp1"].split(";"):
            spellings[form].add(row["stacked_word_meaning_id"])
    collisions = {form: ids for form, ids in spellings.items() if len(ids) > 1}
    return {
        "date": "2026-09-13",
        "scope": "Exactly one normalized upasarga and one already admitted sanadi semantic branch applied to an original dhatu meaning; no second upasarga, second sanadi, krdanta, or inflection.",
        "admission_standard": "The sanadi meaning must already be admitted, the upasarga operation must be productive, the pinned engine must construct a form, and an explicit base-meaning restriction overrides generation. Attestation is not required.",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "normalized_upasarga_identities": len(inventory),
        "admitted_one_sanadi_meanings": admitted_sanadi_meanings,
        **engine_report,
        "admitted_stacked_word_meanings": len(admitted),
        "admitted_by_sanadi_operation": dict(sorted(by_operation.items())),
        "not_admitted_by_status": dict(sorted(by_status.items())),
        "spelling_diagnostics": {
            "distinct_output_spellings": len(spellings),
            "spellings_shared_by_multiple_word_meanings": len(collisions),
            "policy": "Shared spelling does not merge different words or meanings.",
        },
        "prior_bounded_verbal_capacity_subtotal": prior["bounded_verbal_capacity_subtotal"],
        "bounded_verbal_capacity_subtotal": prior["bounded_verbal_capacity_subtotal"] + len(admitted),
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "sources": [records[name] for name in source_names],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (
            INVENTORY, CONFLICTS, VERBAL_LEDGER, PRIOR_SUMMARY, STANDARD, MANIFEST, Path(__file__)
        )},
    }


def write_markdown(report: dict) -> None:
    status = report["not_admitted_by_status"]
    op = report["admitted_by_sanadi_operation"]
    lines = [
        "# One-उपसर्गः Plus One-सनादि Generated-Capacity Ledger", "",
        "This pass combines exactly one normalized उपसर्गः (*upasargaḥ*) with one already admitted सनादि (*sanādi*) semantic branch. The prefix modifies the action; the सनादि operation then supplies causation, desire, repetition, intensity, crooked movement, or disparaged action.", "",
        "## Result", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Earlier bounded verbal subtotal | {report['prior_bounded_verbal_capacity_subtotal']:,} |",
        f"| One उपसर्गः + one सनादि operation | {report['admitted_stacked_word_meanings']:,} |",
        f"| **Bounded verbal-capacity subtotal** | **{report['bounded_verbal_capacity_subtotal']:,}** |", "",
        "The stacked layer contains:", "",
        f"- {op.get('causative', 0):,} causative meanings;",
        f"- {op.get('desiderative', 0):,} desiderative meanings;",
        f"- {op.get('intensive', 0):,} यङन्त meanings; and",
        f"- {op.get('intensive_luk', 0):,} यङ्लुगन्त meanings.", "",
        f"The source restrictions exclude **{status.get('not_counted_documented_base_meaning_conflict', 0):,}** combinations. Vidyut leaves **{status.get('not_admitted_engine_zero_unresolved', 0):,}** otherwise eligible combinations without an output; these remain unresolved and are not treated as grammatical prohibitions.", "",
        "The detailed admitted and excluded ledgers are gzip-compressed CSV files. Coincident spellings remain separate when they carry different base meanings or different सनादि semantic branches.", "",
        "This is a bounded research subtotal. It excludes prefix-conditioned enrichment meanings, a second prefix, a second सनादि operation, कृदन्तानि, inflection, and nominal operations.", "",
    ]
    (RESULTS / "upasarga_sanadi_summary.md").write_text("\n".join(lines))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest, inventory, conflicts = verify_inputs()
    verbal_rows = read_csv(VERBAL_LEDGER)
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    entries_by_code = {entry.code: entry for entry in entries}
    engine, engine_report = run_engine(entries, inventory)
    admitted, excluded = build_ledgers(verbal_rows, inventory, conflicts, entries_by_code, engine)
    report = build_report(
        manifest,
        inventory,
        engine_report,
        len(verbal_rows),
        admitted,
        excluded,
    )
    write_gzip_csv(RESULTS / "upasarga_sanadi_ledger.csv.gz", admitted)
    write_gzip_csv(RESULTS / "upasarga_sanadi_exclusions.csv.gz", excluded)
    (RESULTS / "upasarga_sanadi_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_markdown(report)
    print(f"Admitted {len(admitted)} stacked word-meanings; bounded subtotal {report['bounded_verbal_capacity_subtotal']}.")


if __name__ == "__main__":
    main()
