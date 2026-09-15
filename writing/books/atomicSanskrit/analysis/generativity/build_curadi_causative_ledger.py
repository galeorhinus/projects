#!/usr/bin/env python3
"""Build the true causative ledger for curadigana bases with stacked nic."""

from __future__ import annotations

from collections import defaultdict
import csv
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
EXCLUSIONS = RESULTS / "verbal_derivation_exclusions.csv"
PRIOR_SUMMARY = RESULTS / "upasarga_sanadi_summary.json"
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


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")

    candidates = [
        row for row in read_csv(EXCLUSIONS)
        if row["count_status"] == "not_counted_class_forming_nic"
    ]
    entries = {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    engine: dict[str, set[str]] = {}
    tested_codes = sorted({code for row in candidates for code in row["base_source_codes"].split(";") if code})
    for code in tested_codes:
        entry = entries[code]
        if str(entry.dhatu.gana) != "curAdi":
            raise ValueError(f"Expected curadigana source entry: {code}")
        engine[code] = {
            result.text
            for result in grammar.derive(entry.dhatu.with_sanadi([Sanadi.Ric, Sanadi.Ric]))
        }

    admitted = []
    excluded = []
    for row in candidates:
        codes = [value for value in row["base_source_codes"].split(";") if value]
        forms = {form for code in codes for form in engine[code]}
        common = {
            "base_count_key": row["base_count_key"],
            "base_source_codes": row["base_source_codes"],
            "base_citations_slp1": row["base_citations_slp1"],
            "base_meaning_slp1": row["base_meaning_slp1"],
            "base_meaning_display": row["base_meaning_display"],
        }
        if not forms:
            excluded.append({
                **common,
                "output_forms_slp1": "",
                "reason": "Vidyut produced no form from the stacked-nic request; no grammatical prohibition is inferred.",
                "count_status": "not_admitted_engine_zero_unresolved",
            })
            continue
        admitted.append({
            "derived_word_meaning_id": stable_id("curadi-causative", row["base_count_key"]),
            "operation_id": "curadi_true_causative",
            "operation_display": "द्विणिजन्त (dviṇijanta), true causative of a curādigaṇa base",
            **common,
            "semantic_branch_id": "causation",
            "semantic_relation": "cause an independent agent to perform the base action, or bring about the base state",
            "rule_refs": "3.1.25;3.1.26",
            "output_forms_slp1": ";".join(sorted(forms)),
            "output_variant_count": str(len(forms)),
            "admission_basis": "class_forming_nic_plus_causative_nic_plus_pinned_engine_output",
            "count_status": "admitted_research_ledger",
        })

    admitted.sort(key=lambda row: row["base_count_key"])
    excluded.sort(key=lambda row: row["base_count_key"])
    prior = json.loads(PRIOR_SUMMARY.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    source_names = ["rule-3.1.25.html", "rule-3.1.26.html", "vidyut-args-dhatu.rs", "vidyut-sanadi.rs"]
    report = {
        "date": "2026-09-13",
        "scope": "One true causative meaning from each eligible curadigana base meaning, using the class-forming nic followed by causative nic; no upasarga, further sanadi stacking, krdanta, or inflection.",
        "candidate_curadigana_base_meanings": len(candidates),
        "source_entries_tested": len(tested_codes),
        "source_entries_with_output": sum(bool(forms) for forms in engine.values()),
        "source_entry_zero_outputs": sum(not forms for forms in engine.values()),
        "admitted_true_causative_word_meanings": len(admitted),
        "unresolved_word_meanings": len(excluded),
        "prior_bounded_verbal_capacity_subtotal": prior["bounded_verbal_capacity_subtotal"],
        "bounded_verbal_capacity_subtotal": prior["bounded_verbal_capacity_subtotal"] + len(admitted),
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "sources": [records[name] for name in source_names],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (EXCLUSIONS, PRIOR_SUMMARY, STANDARD, MANIFEST, Path(__file__))},
    }
    RESULTS.mkdir(exist_ok=True)
    admitted_fields = list(admitted[0]) if admitted else ["derived_word_meaning_id"]
    excluded_fields = list(excluded[0]) if excluded else [
        "base_count_key", "base_source_codes", "base_citations_slp1", "base_meaning_slp1",
        "base_meaning_display", "output_forms_slp1", "reason", "count_status",
    ]
    write_csv(RESULTS / "curadi_causative_ledger.csv", admitted, admitted_fields)
    write_csv(RESULTS / "curadi_causative_exclusions.csv", excluded, excluded_fields)
    (RESULTS / "curadi_causative_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "curadi_causative_summary.md").write_text("\n".join([
        "# चरादिगणः True-Causative Pass", "",
        "For a चरादिगणः (*curādigaṇaḥ*) base, the first णिच् (*ṇic*) creates the class form under 3.1.25. It does not yet add causation. This pass asks Vidyut for a second णिच् under 3.1.26 and counts the resulting causative meaning.", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Earlier bounded verbal subtotal | {report['prior_bounded_verbal_capacity_subtotal']:,} |",
        f"| चरादिगण true causatives | {len(admitted):,} |",
        f"| **Bounded verbal-capacity subtotal** | **{report['bounded_verbal_capacity_subtotal']:,}** |", "",
        f"All **{len(candidates):,} candidate base meanings** produced a stacked-णिच् form. The ledger counts one new causative meaning per base meaning; alternative forms remain attached to that meaning.", "",
        "This pass does not yet combine these true causatives with prefixes.", "",
    ]))
    print(f"Admitted {len(admitted)} curadigana true causatives; bounded subtotal {report['bounded_verbal_capacity_subtotal']}.")


if __name__ == "__main__":
    main()
