#!/usr/bin/env python3
"""Generate Vaidika avyaya and source-conditioned krt operations."""

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
CONFIG = HERE / "vaidika_krt_operations.json"
PRIOR = RESULTS / "vaidika_direct_summary.json"


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
            item["codes"].add(row["source_code"]); item["citations"].add(row["normalized_citation_slp1"])
            item["meanings"].add(row["normalized_meaning_slp1"]); item["display"].add(row["meaning_display"])
    return [grouped[key] for key in sorted(grouped)]


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest = json.loads(MANIFEST.read_text())
    operations = {row["operation_id"]: row for row in json.loads(CONFIG.read_text())["operations"]}
    bases = grouped_bases()
    entries = {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(log_steps=False, is_chandasi=True, use_svaras=True, nlp_mode=False)
    engine = {}
    for variant in ("kamul", "kasun"):
        for code, entry in entries.items():
            engine[(variant, code)] = sorted({
                result.text for result in grammar.derive(Pratipadika.krdanta(entry.dhatu, getattr(Krt, variant)))
            })

    admitted, excluded = [], []
    for operation_id, variant in (("vedic_sak_purpose_kamul", "kamul"), ("vedic_bhavalaksana_kasun", "kasun")):
        operation = operations[operation_id]
        eligible = set(operation.get("eligible_source_codes", entries))
        for base in bases:
            codes = sorted(base["codes"] & eligible)
            if not codes:
                continue
            forms = sorted({form for code in codes for form in engine[(variant, code)]})
            common = {
                "operation_id": operation_id, "krt_source_variant": variant,
                "base_count_key": base["key"], "base_source_codes": ";".join(codes),
                "base_citations_slp1": ";".join(sorted(base["citations"])),
                "base_meaning_slp1": ";".join(sorted(base["meanings"])),
                "base_meaning_display": ";".join(sorted(base["display"])),
                "semantic_branch_id": operation["semantic_branch_id"],
                "semantic_relation": operation["semantic_relation"],
                "construction_condition": operation["condition"],
                "rule_refs": ";".join(operation["rule_refs"]),
            }
            if forms:
                admitted.append({
                    "derived_word_meaning_id": stable_id("vaidika-conditioned", operation_id, base["key"]),
                    **common, "output_forms_slp1": ";".join(forms), "output_variant_count": str(len(forms)),
                    "admission_basis": "source_condition_plus_chandasi_engine_output",
                    "count_status": "admitted_vaidika_research_ledger",
                })
            else:
                excluded.append({**common, "reason": "The pinned Vedic-mode engine supplied no output."})
    for name, rows in (("vaidika_conditioned_ledger.csv", admitted), ("vaidika_conditioned_exclusions.csv", excluded)):
        fields = list(rows[0]) if rows else ["operation_id", "reason"]
        with (RESULTS / name).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)

    gaps = []
    for operation in operations.values():
        if operation["engine_strategy"] != "coverage_gap":
            continue
        eligible_codes = set(operation.get("eligible_source_codes", entries))
        candidate_meanings = sum(bool(base["codes"] & eligible_codes) for base in bases)
        gaps.append({
            "operation_id": operation["operation_id"], "identifiers": operation["identifiers"],
            "semantic_candidates": candidate_meanings, "rule_refs": operation["rule_refs"],
            "status": "not_admitted_engine_coverage_gap_not_prohibition",
        })
    prior = json.loads(PRIOR.read_text())["vaidika_specific_subtotal"]
    by_operation = Counter(row["operation_id"] for row in admitted)
    report = {
        "date": "2026-09-13", "admitted_vaidika_conditioned_word_meanings": len(admitted),
        "not_admitted_engine_or_condition_total": len(excluded),
        "admitted_by_operation": dict(sorted(by_operation.items())),
        "coverage_gaps": gaps, "prior_vaidika_specific_subtotal": prior,
        "vaidika_specific_subtotal": prior + len(admitted),
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": manifest["generator_commit"], "is_chandasi": True, "use_svaras": True},
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (ASSIGNMENTS, CONFIG, PRIOR, MANIFEST, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "vaidika_conditioned_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Vaidika Avyaya and Conditioned Generation", "",
        f"The pinned engine and the source conditions admit **{len(admitted):,} word-meanings** in this pass.", "",
        "| Operation | Admitted |", "|---|---:|",
    ]
    for operation_id, count in sorted(by_operation.items()):
        lines.append(f"| {operation_id} | {count:,} |")
    lines.extend(["", "The following capacities remain explicit but uncounted because the pinned engine does not implement their forms:", "", "| Operation | Semantic candidates |", "|---|---:|"])
    for gap in gaps:
        lines.append(f"| {gap['operation_id']} | {gap['semantic_candidates']:,} |")
    lines.extend(["", "No candidate in that table is treated as prohibited. Its contribution is simply zero until a reproducible source-aware generator exists.", ""])
    (RESULTS / "vaidika_conditioned_summary.md").write_text("\n".join(lines))
    print(f"Admitted {len(admitted)} conditioned Vaidika word-meanings; Vaidika-specific subtotal {report['vaidika_specific_subtotal']}.")


if __name__ == "__main__":
    main()
