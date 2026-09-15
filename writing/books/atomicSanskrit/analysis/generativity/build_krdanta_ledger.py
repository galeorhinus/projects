#!/usr/bin/env python3
"""Build a bounded laukika krdanta ledger from original dhatu meanings."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
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
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
CLASSIFICATION = RESULTS / "krt_classification.json"
CONFIG = HERE / "krt_classification.json"
PRIOR_SUMMARY = RESULTS / "two_upasarga_summary.json"
STANDARD = HERE / "admission_standard.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def group_bases(rows: list[dict[str, str]]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for row in rows:
        if row["record_kind"] != "lexical":
            continue
        key = row["normalized_count_key"]
        item = grouped.setdefault(key, {
            "base_count_key": key,
            "source_codes": set(),
            "citations": set(),
            "meanings_slp1": set(),
            "meanings_display": set(),
        })
        item["source_codes"].add(row["source_code"])
        item["citations"].add(row["normalized_citation_slp1"])
        item["meanings_slp1"].add(row["normalized_meaning_slp1"])
        item["meanings_display"].add(row["meaning_display"])
    return [grouped[key] for key in sorted(grouped)]


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")
    classification = json.loads(CLASSIFICATION.read_text())
    config = json.loads(CONFIG.read_text())
    if classification["bounded_laukika_semantic_operations"] != len(config["bounded_laukika_operations"]):
        raise ValueError("Run classify_krt_inventory.py before building the krdanta ledger")

    bases = group_bases(read_csv(ASSIGNMENTS))
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    selected_variants = sorted({row["source_variant"] for row in config["bounded_laukika_operations"]})
    engine: dict[tuple[str, str], set[str]] = {}
    for variant in selected_variants:
        krt = getattr(Krt, variant)
        for entry in entries:
            engine[(variant, entry.code)] = {
                result.text
                for result in grammar.derive(Pratipadika.krdanta(entry.dhatu, krt))
            }

    admitted = []
    excluded = []
    for operation in config["bounded_laukika_operations"]:
        variant = operation["source_variant"]
        for base in bases:
            forms = sorted({form for code in base["source_codes"] for form in engine[(variant, code)]})
            common = {
                "operation_id": operation["operation_id"],
                "krt_source_variant": variant,
                "operation_display": operation["display"],
                "base_count_key": base["base_count_key"],
                "base_source_codes": ";".join(sorted(base["source_codes"])),
                "base_citations_slp1": ";".join(sorted(base["citations"])),
                "base_meaning_slp1": ";".join(sorted(base["meanings_slp1"])),
                "base_meaning_display": ";".join(sorted(base["meanings_display"])),
                "semantic_branch_id": operation["semantic_branch_id"],
                "semantic_relation": operation["semantic_relation"],
                "rule_refs": ";".join(operation["rule_refs"]),
            }
            if not forms:
                excluded.append({
                    **common,
                    "output_forms_slp1": "",
                    "reason": "The selected krt identifier produced no form for any source entry carrying this base meaning; the row is outside this operation, not rejected for lack of attestation.",
                    "count_status": "not_admitted_engine_and_rule_condition_unmet",
                })
                continue
            admitted.append({
                "derived_word_meaning_id": stable_id("krdanta", operation["operation_id"], base["base_count_key"]),
                **common,
                "output_forms_slp1": ";".join(forms),
                "output_variant_count": str(len(forms)),
                "admission_basis": "classified_laukika_semantic_operation_plus_pinned_engine_output",
                "count_status": "admitted_research_ledger",
            })

    admitted.sort(key=lambda row: (row["operation_id"], row["base_count_key"]))
    excluded.sort(key=lambda row: (row["operation_id"], row["base_count_key"]))
    by_operation = Counter(row["operation_id"] for row in admitted)
    excluded_by_operation = Counter(row["operation_id"] for row in excluded)
    spellings: dict[str, set[str]] = defaultdict(set)
    for row in admitted:
        for form in row["output_forms_slp1"].split(";"):
            spellings[form].add(row["derived_word_meaning_id"])
    collisions = {form: ids for form, ids in spellings.items() if len(ids) > 1}
    prior = json.loads(PRIOR_SUMMARY.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    source_names = [
        "vidyut-args-krt.rs", "vidyut-krt-basic.rs", "rule-3.1.96.html",
        "rule-3.1.97.html", "rule-3.1.124.html", "rule-3.1.133.html",
        "rule-3.2.102.html", "rule-3.2.124.html", "rule-3.3.115.html",
        "rule-3.3.117.html", "rule-3.4.67.html", "rule-3.4.70.html",
    ]
    report = {
        "date": "2026-09-13",
        "scope": "Fourteen classified laukika krdanta semantic operations applied directly to the 2,634 original dhatu meanings; no prefixed or sanadi-derived verbal inputs, avyayas, inflection, or taddhita formation.",
        "admission_standard": "A classified semantic operation and successful pinned-engine derivation admit a word-meaning. A missing dictionary or corpus occurrence does not exclude it. Alternative forms remain attached to one operation/base-meaning row.",
        "base_word_meanings": len(bases),
        "selected_krt_identifiers": len(selected_variants),
        "selected_semantic_operations": len(config["bounded_laukika_operations"]),
        "structural_operation_candidates": len(bases) * len(config["bounded_laukika_operations"]),
        "source_entry_operations_tested": len(entries) * len(selected_variants),
        "source_entry_operations_with_output": sum(bool(forms) for forms in engine.values()),
        "source_entry_zero_outputs": sum(not forms for forms in engine.values()),
        "admitted_krdanta_word_meanings": len(admitted),
        "admitted_by_operation": dict(sorted(by_operation.items())),
        "not_admitted_by_operation": dict(sorted(excluded_by_operation.items())),
        "not_admitted_total": len(excluded),
        "spelling_diagnostics": {
            "distinct_output_spellings": len(spellings),
            "spellings_shared_by_multiple_word_meanings": len(collisions),
            "shared_spelling_word_meaning_links": sum(len(ids) for ids in collisions.values()),
            "policy": "The same spelling remains more than one word-meaning when its base meaning or derivational meaning differs.",
        },
        "prior_bounded_verbal_capacity_subtotal": prior["bounded_verbal_capacity_subtotal"],
        "bounded_word_meaning_subtotal": prior["bounded_verbal_capacity_subtotal"] + len(admitted),
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "sources": [records[name] for name in source_names],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (ASSIGNMENTS, CLASSIFICATION, CONFIG, PRIOR_SUMMARY, STANDARD, MANIFEST, Path(__file__))},
    }
    RESULTS.mkdir(exist_ok=True)
    write_csv(RESULTS / "krdanta_ledger.csv", admitted, list(admitted[0]))
    write_csv(RESULTS / "krdanta_exclusions.csv", excluded, list(excluded[0]))
    (RESULTS / "krdanta_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Bounded कृदन्त Generation", "",
        "This pass derives a conservative laukika कृदन्त layer directly from the 2,634 original धातु meanings. It uses twelve engine identifiers carrying fourteen separately stated semantic operations.", "",
        "## Result", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Earlier bounded verbal subtotal | {report['prior_bounded_verbal_capacity_subtotal']:,} |",
        f"| Bounded कृदन्त formations | {len(admitted):,} |",
        f"| **Combined bounded subtotal** | **{report['bounded_word_meaning_subtotal']:,}** |", "",
        "| कृदन्त operation | Admitted | Outside operation |", "|---|---:|---:|",
    ]
    for operation in config["bounded_laukika_operations"]:
        operation_id = operation["operation_id"]
        lines.append(f"| {operation['display']} | {by_operation[operation_id]:,} | {excluded_by_operation[operation_id]:,} |")
    lines.extend([
        "", f"The ledger admits **{len(admitted):,} of {report['structural_operation_candidates']:,} operation/base-meaning candidates**. The rows outside an operation arise where its own grammatical and engine conditions do not supply that formation, chiefly the pada-sensitive present participles and the three complementary -ya obligation formations.", "",
        f"The admitted rows produce **{report['spelling_diagnostics']['distinct_output_spellings']:,} distinct spellings**. A shared spelling does not merge different धातु meanings or different derivational meanings. ल्युट् therefore contributes separate action, instrument, and location entries even when one form carries all three.", "",
        "This is not yet the full कृदन्त space. It excludes Vedic-only formations, अव्ययानि, eighty-seven root- or construction-conditioned identifiers, and कृदन्त derivation from prefixed or सनादि-derived verbal inputs.", "",
    ])
    (RESULTS / "krdanta_summary.md").write_text("\n".join(lines))
    print(f"Admitted {len(admitted)} krdanta word-meanings; combined bounded subtotal {report['bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
