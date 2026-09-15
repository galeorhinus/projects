#!/usr/bin/env python3
"""Generate the source-selected conditioned krdanta subset."""

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
CLASSIFICATION = RESULTS / "conditioned_krt_classification.json"
CONFIG = HERE / "conditioned_krt_operations.json"
PRIOR = RESULTS / "avyaya_summary.json"
STANDARD = HERE / "admission_standard.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def group_bases(rows: list[dict[str, str]]) -> list[dict]:
    grouped = {}
    for row in rows:
        if row["record_kind"] != "lexical":
            continue
        key = row["normalized_count_key"]
        item = grouped.setdefault(key, {"key": key, "codes": set(), "citations": set(), "meanings": set(), "display": set()})
        item["codes"].add(row["source_code"])
        item["citations"].add(row["normalized_citation_slp1"])
        item["meanings"].add(row["normalized_meaning_slp1"])
        item["display"].add(row["meaning_display"])
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
    if classification["selected_semantic_operations"] != len(config["operations"]):
        raise ValueError("Run classify_conditioned_krt.py before generation")
    bases = group_bases(read_csv(ASSIGNMENTS))
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    variants = sorted({row["source_variant"] for row in config["operations"]})
    engine = {}
    for variant in variants:
        for entry in entries:
            engine[(variant, entry.code)] = {
                result.text for result in grammar.derive(Pratipadika.krdanta(entry.dhatu, getattr(Krt, variant)))
            }

    admitted, excluded = [], []
    for operation in config["operations"]:
        variant = operation["source_variant"]
        for base in bases:
            forms = sorted({form for code in base["codes"] for form in engine[(variant, code)]})
            common = {
                "operation_id": operation["operation_id"], "krt_source_variant": variant,
                "operation_display": operation["display"], "base_count_key": base["key"],
                "base_source_codes": ";".join(sorted(base["codes"])),
                "base_citations_slp1": ";".join(sorted(base["citations"])),
                "base_meaning_slp1": ";".join(sorted(base["meanings"])),
                "base_meaning_display": ";".join(sorted(base["display"])),
                "semantic_branch_id": operation["semantic_branch_id"],
                "semantic_relation": operation["semantic_relation"],
                "rule_refs": ";".join(operation["rule_refs"]),
            }
            if forms:
                admitted.append({
                    "derived_word_meaning_id": stable_id("conditioned-krdanta", operation["operation_id"], base["key"]),
                    **common, "output_forms_slp1": ";".join(forms),
                    "output_variant_count": str(len(forms)),
                    "admission_basis": "source_defined_semantic_operation_plus_pinned_engine_output",
                    "count_status": "admitted_research_ledger",
                })
            else:
                excluded.append({
                    **common, "output_forms_slp1": "",
                    "reason": "The selected operation produced no form for a source entry carrying this base meaning.",
                    "count_status": "not_admitted_operation_condition_unmet",
                })
    admitted.sort(key=lambda row: (row["operation_id"], row["base_count_key"]))
    excluded.sort(key=lambda row: (row["operation_id"], row["base_count_key"]))
    for name, rows in (("conditioned_krdanta_ledger.csv", admitted), ("conditioned_krdanta_exclusions.csv", excluded)):
        fields = list(rows[0])
        with (RESULTS / name).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader(); writer.writerows(rows)

    admitted_by_operation = Counter(row["operation_id"] for row in admitted)
    excluded_by_operation = Counter(row["operation_id"] for row in excluded)
    spellings: dict[str, set[str]] = defaultdict(set)
    for row in admitted:
        for form in row["output_forms_slp1"].split(";"):
            spellings[form].add(row["derived_word_meaning_id"])
    prior = json.loads(PRIOR.read_text())["bounded_word_meaning_subtotal"]
    records = {row["filename"]: row for row in manifest["sources"]}
    source_names = [
        "vidyut-args-krt.rs", "vidyut-krt-basic.rs", "rule-3.1.96.html",
        "rule-3.1.134.html", "rule-3.1.150.html", "rule-3.2.129.html",
        "rule-3.3.94.html", "rule-3.3.118.html", "rule-3.3.174.html",
    ]
    report = {
        "date": config["date"], "scope": config["scope"],
        "base_word_meanings": len(bases),
        "selected_identifiers": len(variants),
        "selected_semantic_operations": len(config["operations"]),
        "structural_operation_candidates": len(bases) * len(config["operations"]),
        "admitted_conditioned_krdanta_word_meanings": len(admitted),
        "not_admitted_total": len(excluded),
        "admitted_by_operation": dict(sorted(admitted_by_operation.items())),
        "not_admitted_by_operation": dict(sorted(excluded_by_operation.items())),
        "spelling_diagnostics": {
            "distinct_output_spellings": len(spellings),
            "spellings_shared_by_multiple_word_meanings": sum(len(ids) > 1 for ids in spellings.values()),
        },
        "prior_bounded_word_meaning_subtotal": prior,
        "bounded_word_meaning_subtotal": prior + len(admitted),
        "vocabulary_total": None, "publication_status": "research_subtotal_only_not_deployed",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "sources": [records[name] for name in source_names],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (
            ASSIGNMENTS, CLASSIFICATION, CONFIG, PRIOR, STANDARD, MANIFEST, Path(__file__)
        )},
    }
    (RESULTS / "conditioned_krdanta_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Source-Conditioned कृदन्त Generation", "",
        "This pass admits only the semantic branches explicitly selected in the conditioned कृत्प्रत्यय classification. Engine output alone does not place one of the other deferred identifiers in the count.", "",
        "| Operation | Admitted | Outside operation |", "|---|---:|---:|",
    ]
    for operation in config["operations"]:
        key = operation["operation_id"]
        lines.append(f"| {operation['display']} | {admitted_by_operation[key]:,} | {excluded_by_operation[key]:,} |")
    lines.extend([
        "", f"This pass admits **{len(admitted):,} word-meanings** and brings the bounded subtotal to **{report['bounded_word_meaning_subtotal']:,}**.", "",
        "The remaining conditioned identifiers stay in the classification ledger. They require additional semantic, prefix, उपपद, or construction models and are not treated as prohibited formations.", "",
    ])
    (RESULTS / "conditioned_krdanta_summary.md").write_text("\n".join(lines))
    print(f"Admitted {len(admitted)} conditioned krdanta word-meanings; bounded subtotal {report['bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
