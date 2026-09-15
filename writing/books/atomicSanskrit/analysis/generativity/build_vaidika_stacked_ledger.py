#!/usr/bin/env python3
"""Apply engine-supported Vaidika operations to admitted prefixed and sanadi meanings."""

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
PREFIX_INPUT = RESULTS / "upasarga_generation_ledger.csv"
SANADI_INPUT = RESULTS / "verbal_derivation_ledger.csv"
CURADI_INPUT = RESULTS / "curadi_causative_ledger.csv"
UPASARGAS = HERE / "upasarga_inventory.csv"
CONFIG = HERE / "vaidika_krt_operations.json"
PRIOR = RESULTS / "vaidika_conditioned_summary.json"

SANADI_STACKS = {
    "causative": [Sanadi.Ric], "desiderative": [Sanadi.san],
    "intensive": [Sanadi.yaN], "intensive_luk": [Sanadi.yaNluk],
    "curadi_true_causative": [Sanadi.Ric, Sanadi.Ric],
}
VARIANTS = {
    "vedic_perfect_participle_kanac": "kAnac",
    "vedic_perfect_participle_kvasu": "kvasu",
    "vedic_sak_purpose_kamul": "kamul",
}
LEDGER_FIELDS = [
    "derived_word_meaning_id", "source_kind", "source_word_meaning_id",
    "source_operation_id", "vaidika_operation_id", "krt_source_variant",
    "upasarga_id", "sanadi_stack", "base_count_key", "base_source_codes",
    "base_citations_slp1", "base_meaning_slp1", "base_meaning_display",
    "source_semantic_relation", "semantic_relation", "construction_condition",
    "rule_refs", "output_forms_slp1", "output_variant_count", "admission_basis",
    "count_status",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def eligible_codes(source: dict[str, str], entries: dict) -> list[str]:
    codes = [code for code in source["base_source_codes"].split(";") if code]
    operation = source["operation_id"]
    if operation == "causative":
        return [code for code in codes if str(entries[code].dhatu.gana) != "curAdi"]
    if operation == "curadi_true_causative":
        return [code for code in codes if str(entries[code].dhatu.gana) == "curAdi"]
    return codes


def write_row(writer, source_kind, source, source_id, source_operation, upasarga_id,
              sanadi_stack, operation, variant, codes, forms):
    writer.writerow({
        "derived_word_meaning_id": stable_id("vaidika-stacked", source_kind, source_id, operation["operation_id"]),
        "source_kind": source_kind, "source_word_meaning_id": source_id,
        "source_operation_id": source_operation, "vaidika_operation_id": operation["operation_id"],
        "krt_source_variant": variant, "upasarga_id": upasarga_id,
        "sanadi_stack": sanadi_stack, "base_count_key": source["base_count_key"],
        "base_source_codes": ";".join(codes),
        "base_citations_slp1": source["base_citations_slp1"],
        "base_meaning_slp1": source["base_meaning_slp1"],
        "base_meaning_display": source["base_meaning_display"],
        "source_semantic_relation": source["semantic_relation"],
        "semantic_relation": operation["semantic_relation"] + " from the admitted " + source_kind + " meaning",
        "construction_condition": operation["condition"],
        "rule_refs": ";".join(source["rule_refs"].split(";") + operation["rule_refs"]),
        "output_forms_slp1": ";".join(forms), "output_variant_count": str(len(forms)),
        "admission_basis": "admitted_source_meaning_plus_source_defined_vedic_operation_plus_chandasi_engine_output",
        "count_status": "admitted_vaidika_research_ledger",
    })


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")
    operations = {row["operation_id"]: row for row in json.loads(CONFIG.read_text())["operations"]}
    entries = {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(log_steps=False, is_chandasi=True, use_svaras=True, nlp_mode=False)
    prefixes = {row["upasarga_id"]: row["engine_input_slp1"] for row in read_csv(UPASARGAS)}
    prefix_rows = read_csv(PREFIX_INPUT)
    sanadi_rows = read_csv(SANADI_INPUT) + read_csv(CURADI_INPUT)
    by_prefix = defaultdict(list)
    for row in prefix_rows:
        by_prefix[row["upasarga_id"]].append(row)
    by_sanadi = defaultdict(list)
    for row in sanadi_rows:
        by_sanadi[row["operation_id"]].append(row)

    admitted = excluded = 0
    by_source_kind = Counter(); by_operation = Counter(); excluded_by_operation = Counter()
    ledger_path = RESULTS / "vaidika_stacked_ledger.csv.gz"
    exclusion_path = RESULTS / "vaidika_stacked_exclusions.csv.gz"
    with gzip.open(ledger_path, "wt", encoding="utf-8", newline="") as out, gzip.open(exclusion_path, "wt", encoding="utf-8", newline="") as rejected:
        writer = csv.DictWriter(out, fieldnames=LEDGER_FIELDS); writer.writeheader()
        reject_fields = ["source_kind", "source_word_meaning_id", "vaidika_operation_id", "base_count_key", "base_source_codes", "reason"]
        reject_writer = csv.DictWriter(rejected, fieldnames=reject_fields); reject_writer.writeheader()

        for prefix_id, rows in sorted(by_prefix.items()):
            engine = {}
            for operation_id, variant in VARIANTS.items():
                for code, entry in entries.items():
                    dhatu = entry.dhatu.with_prefixes([prefixes[prefix_id]])
                    engine[(operation_id, code)] = sorted({
                        result.text for result in grammar.derive(Pratipadika.krdanta(dhatu, getattr(Krt, variant)))
                    })
            for operation_id, variant in VARIANTS.items():
                operation = operations[operation_id]
                for source in rows:
                    codes = [code for code in source["base_source_codes"].split(";") if code]
                    forms = sorted({form for code in codes for form in engine[(operation_id, code)]})
                    if not forms:
                        reject_writer.writerow({"source_kind": "one_upasarga", "source_word_meaning_id": source["generated_word_meaning_id"], "vaidika_operation_id": operation_id, "base_count_key": source["base_count_key"], "base_source_codes": ";".join(codes), "reason": "No Vedic-mode engine output."})
                        excluded += 1; excluded_by_operation[operation_id] += 1; continue
                    write_row(writer, "one_upasarga", source, source["generated_word_meaning_id"], source["upasarga_id"], prefix_id, "", operation, variant, codes, forms)
                    admitted += 1; by_source_kind["one_upasarga"] += 1; by_operation[operation_id] += 1

        for source_operation, rows in sorted(by_sanadi.items()):
            stack = SANADI_STACKS[source_operation]
            stack_label = "+".join(str(value) for value in stack)
            codes_needed = sorted({code for source in rows for code in eligible_codes(source, entries)})
            engine = {}
            for operation_id, variant in VARIANTS.items():
                for code in codes_needed:
                    dhatu = entries[code].dhatu.with_sanadi(stack)
                    engine[(operation_id, code)] = sorted({
                        result.text for result in grammar.derive(Pratipadika.krdanta(dhatu, getattr(Krt, variant)))
                    })
            for operation_id, variant in VARIANTS.items():
                operation = operations[operation_id]
                for source in rows:
                    codes = eligible_codes(source, entries)
                    forms = sorted({form for code in codes for form in engine[(operation_id, code)]})
                    if not forms:
                        reject_writer.writerow({"source_kind": "one_sanadi", "source_word_meaning_id": source["derived_word_meaning_id"], "vaidika_operation_id": operation_id, "base_count_key": source["base_count_key"], "base_source_codes": ";".join(codes), "reason": "No Vedic-mode engine output."})
                        excluded += 1; excluded_by_operation[operation_id] += 1; continue
                    write_row(writer, "one_sanadi", source, source["derived_word_meaning_id"], source_operation, "", stack_label, operation, variant, codes, forms)
                    admitted += 1; by_source_kind["one_sanadi"] += 1; by_operation[operation_id] += 1

    prior = json.loads(PRIOR.read_text())["vaidika_specific_subtotal"]
    report = {
        "date": "2026-09-13", "source_one_upasarga_word_meanings": len(prefix_rows),
        "source_one_sanadi_word_meanings": len(sanadi_rows),
        "selected_vedic_operations": len(VARIANTS),
        "structural_operation_candidates": (len(prefix_rows) + len(sanadi_rows)) * len(VARIANTS),
        "admitted_vaidika_stacked_word_meanings": admitted, "not_admitted_total": excluded,
        "admitted_by_source_kind": dict(sorted(by_source_kind.items())),
        "admitted_by_operation": dict(sorted(by_operation.items())),
        "not_admitted_by_operation": dict(sorted(excluded_by_operation.items())),
        "prior_vaidika_specific_subtotal": prior, "vaidika_specific_subtotal": prior + admitted,
        "scope": "The engine-supported Vedic perfect participle and sak-conditioned purpose operation applied separately to one-prefix and one-sanadi meanings. No two-prefix, prefix-plus-sanadi, inflectional, or unsupported Vedic suffix layer enters this pass.",
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": manifest["generator_commit"], "is_chandasi": True, "use_svaras": True},
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (PREFIX_INPUT, SANADI_INPUT, CURADI_INPUT, UPASARGAS, CONFIG, PRIOR, MANIFEST, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "vaidika_stacked_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Vaidika Operations over Prefixed and सनादि Meanings", "",
        f"This pass tests two engine-supported Vaidika operations over **{len(prefix_rows):,} one-prefix** and **{len(sanadi_rows):,} one-सनादि** meanings.", "",
        "| Source layer | Admitted word-meanings |", "|---|---:|",
    ]
    for kind, count in sorted(by_source_kind.items()):
        lines.append(f"| {kind.replace('_', ' ')} | {count:,} |")
    lines.extend([
        f"| **Total** | **{admitted:,}** |", "",
        f"The Vaidika-specific subtotal after this pass is **{report['vaidika_specific_subtotal']:,} word-meanings**. The compressed ledger materializes every admitted row.", "",
        "The pass does not infer that every possible further stack is authorized. It stops at the two already admitted input layers named above.", "",
    ])
    (RESULTS / "vaidika_stacked_summary.md").write_text("\n".join(lines))
    print(f"Admitted {admitted} stacked Vaidika word-meanings; Vaidika-specific subtotal {report['vaidika_specific_subtotal']}.")


if __name__ == "__main__":
    main()
