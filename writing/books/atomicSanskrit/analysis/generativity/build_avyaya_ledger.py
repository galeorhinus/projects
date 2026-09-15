#!/usr/bin/env python3
"""Build the bounded laukika krt-derived avyaya ledger."""

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
CONFIG = HERE / "avyaya_krt_operations.json"
PRIOR = RESULTS / "six_pass_expansion_summary.json"
STANDARD = HERE / "admission_standard.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


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
    primary = classification["classification_counts"]
    if primary.get("laukika_avyaya_deferred") != len(config["operations"]):
        raise ValueError("The source-corrected laukika avyaya classification is stale")

    bases = group_bases(read_csv(ASSIGNMENTS))
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    variants = sorted({row["source_variant"] for row in config["operations"]})
    engine = {}
    for variant in variants:
        for entry in entries:
            engine[(variant, entry.code)] = {
                result.text
                for result in grammar.derive(Pratipadika.krdanta(entry.dhatu, getattr(Krt, variant)))
            }

    admitted = []
    excluded = []
    for operation in config["operations"]:
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
                    "reason": "The pinned engine supplied no form; no prohibition is inferred.",
                    "count_status": "not_admitted_engine_zero_unresolved",
                })
            else:
                admitted.append({
                    "derived_word_meaning_id": stable_id("avyaya", operation["operation_id"], base["base_count_key"]),
                    **common,
                    "output_forms_slp1": ";".join(forms),
                    "output_variant_count": str(len(forms)),
                    "admission_basis": "source_classified_laukika_avyaya_operation_plus_pinned_engine_output",
                    "count_status": "admitted_research_ledger",
                })

    admitted.sort(key=lambda row: (row["operation_id"], row["base_count_key"]))
    excluded.sort(key=lambda row: (row["operation_id"], row["base_count_key"]))
    for name, rows in (("avyaya_ledger.csv", admitted), ("avyaya_exclusions.csv", excluded)):
        fields = list(rows[0]) if rows else [
            "derived_word_meaning_id", "operation_id", "krt_source_variant",
            "base_count_key", "reason", "count_status",
        ]
        with (RESULTS / name).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    by_operation = Counter(row["operation_id"] for row in admitted)
    spellings: dict[str, set[str]] = defaultdict(set)
    for row in admitted:
        for form in row["output_forms_slp1"].split(";"):
            spellings[form].add(row["derived_word_meaning_id"])
    prior = json.loads(PRIOR.read_text())["bounded_word_meaning_subtotal"]
    records = {row["filename"]: row for row in manifest["sources"]}
    source_names = [
        "vidyut-args-krt.rs", "vidyut-krt-basic.rs", "rule-3.3.10.html",
        "rule-3.4.9.html", "rule-3.4.12.html", "rule-3.4.21.html",
        "rule-3.4.22.html", "rule-7.1.37.html",
    ]
    report = {
        "date": config["date"],
        "scope": config["scope"] + " Prefixed ktva-to-lyap formations remain for a later derived-base pass.",
        "base_word_meanings": len(bases),
        "selected_laukika_avyaya_identifiers": len(variants),
        "selected_semantic_operations": len(config["operations"]),
        "structural_operation_candidates": len(bases) * len(config["operations"]),
        "admitted_avyaya_word_meanings": len(admitted),
        "not_admitted_total": len(excluded),
        "admitted_by_operation": dict(sorted(by_operation.items())),
        "deferred_or_excluded_identifiers": config["deferred_or_excluded"],
        "spelling_diagnostics": {
            "distinct_output_spellings": len(spellings),
            "spellings_shared_by_multiple_word_meanings": sum(len(ids) > 1 for ids in spellings.values()),
        },
        "prior_bounded_word_meaning_subtotal": prior,
        "bounded_word_meaning_subtotal": prior + len(admitted),
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "sources": [records[name] for name in source_names],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (
            ASSIGNMENTS, CLASSIFICATION, CONFIG, PRIOR, STANDARD, MANIFEST, Path(__file__)
        )},
    }
    (RESULTS / "avyaya_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Bounded लौकिक अव्ययाणि", "",
        "This pass separates indeclinable verbal derivatives from nominal कृदन्त formations. It admits three general laukika operations and does not apply nominal case-number inflection to their results.", "",
        "| Operation | Word-meanings |", "|---|---:|",
    ]
    for operation in config["operations"]:
        lines.append(f"| {operation['display']} | {by_operation[operation['operation_id']]:,} |")
    lines.extend([
        f"| **अव्यय subtotal** | **{len(admitted):,}** |", "",
        f"The earlier bounded subtotal was **{prior:,}**. Including these indeclinables produces **{report['bounded_word_meaning_subtotal']:,} word-meanings**.", "",
        "णमुल् expresses repetition only when the derived form is repeated in the construction, as in भोजं भोजम्. The ledger counts the derived word-meaning once rather than counting its two token occurrences as two words.", "",
        "कमुल्, कसे, and कसेन् remain outside this laukika subtotal because their governing rules continue the Vedic-domain condition. The last two also have no ordinary output in Vidyut 0.4.0, and कसेन् is a near-duplicate of कसे except for accent.", "",
    ])
    (RESULTS / "avyaya_summary.md").write_text("\n".join(lines))
    print(f"Admitted {len(admitted)} laukika avyaya word-meanings; bounded subtotal {report['bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
