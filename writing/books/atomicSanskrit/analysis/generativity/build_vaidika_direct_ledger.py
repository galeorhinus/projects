#!/usr/bin/env python3
"""Generate the direct Vaidika perfect-participle word-meaning layer."""

from __future__ import annotations

from collections import defaultdict
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
CONFIG = HERE / "vaidika_krt_operations.json"
CLASSIFICATION = RESULTS / "vaidika_krt_classification.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def grouped_bases() -> list[dict]:
    grouped = {}
    with ASSIGNMENTS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
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
    operations = {row["operation_id"]: row for row in json.loads(CONFIG.read_text())["operations"]}
    direct_operations = [
        (operations["vedic_perfect_participle_kanac"], "kAnac"),
        (operations["vedic_perfect_participle_kvasu"], "kvasu"),
    ]
    entries = {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(log_steps=False, is_chandasi=True, use_svaras=True, nlp_mode=False)
    engine = {
        (variant, code): sorted({result.text for result in grammar.derive(Pratipadika.krdanta(entry.dhatu, getattr(Krt, variant)))})
        for _, variant in direct_operations for code, entry in entries.items()
    }
    admitted, excluded = [], []
    spellings = defaultdict(set)
    for operation, variant in direct_operations:
        for base in grouped_bases():
            forms = sorted({form for code in base["codes"] for form in engine[(variant, code)]})
            common = {
                "operation_id": operation["operation_id"], "krt_source_variant": variant,
                "base_count_key": base["key"], "base_source_codes": ";".join(sorted(base["codes"])),
                "base_citations_slp1": ";".join(sorted(base["citations"])),
                "base_meaning_slp1": ";".join(sorted(base["meanings"])),
                "base_meaning_display": ";".join(sorted(base["display"])),
                "semantic_branch_id": operation["semantic_branch_id"],
                "semantic_relation": operation["semantic_relation"],
                "rule_refs": ";".join(operation["rule_refs"]),
            }
            if forms:
                word_id = stable_id("vaidika-direct", operation["operation_id"], base["key"])
                admitted.append({
                    "derived_word_meaning_id": word_id, **common,
                    "output_forms_slp1": ";".join(forms), "output_variant_count": str(len(forms)),
                    "admission_basis": "source_defined_vedic_operation_plus_chandasi_engine_output",
                    "count_status": "admitted_vaidika_research_ledger",
                })
                for form in forms:
                    spellings[form].add(word_id)
            else:
                excluded.append({**common, "reason": "No form supplied by the pinned Vedic-mode engine."})
    for name, rows in (("vaidika_direct_ledger.csv", admitted), ("vaidika_direct_exclusions.csv", excluded)):
        fields = list(rows[0]) if rows else list(common) + ["reason"]
        with (RESULTS / name).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    records = {row["filename"]: row for row in manifest["sources"]}
    report = {
        "date": "2026-09-13", "base_word_meanings": len(grouped_bases()),
        "selected_direct_operations": len(direct_operations),
        "admitted_vaidika_direct_word_meanings": len(admitted), "not_admitted_total": len(excluded),
        "vaidika_specific_subtotal": len(admitted),
        "spelling_diagnostics": {
            "distinct_output_spellings": len(spellings),
            "spellings_shared_by_multiple_word_meanings": sum(len(ids) > 1 for ids in spellings.values()),
        },
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": manifest["generator_commit"], "is_chandasi": True, "use_svaras": True},
        "sources": [records[name] for name in ("dhatupatha.tsv", "vidyut-args-krt.rs", "vidyut-krt-basic.rs", "rule-3.2.105.html", "rule-3.2.106.html", "rule-3.2.107.html", "rule-3.2.108.html", "rule-3.2.109.html")],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (ASSIGNMENTS, CONFIG, CLASSIFICATION, MANIFEST, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "vaidika_direct_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "vaidika_direct_summary.md").write_text(
        "# Direct Vaidika Generation\n\n"
        f"The Vedic perfect-participle operations **कानच् (kānac)** and **क्वसु (kvasu)** produced **{len(admitted):,} admitted word-meanings** from {report['base_word_meanings']:,} base meanings. Accent-bearing output forms remain attached to each semantic row; alternate forms do not multiply the meaning count.\n\n"
        f"The pinned engine supplied no output for **{len(excluded):,}** candidates.\n"
    )
    print(f"Admitted {len(admitted)} direct Vaidika word-meanings.")


if __name__ == "__main__":
    main()
