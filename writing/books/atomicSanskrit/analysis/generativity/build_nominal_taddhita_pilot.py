#!/usr/bin/env python3
"""Build a bounded nominal-input inventory and taddhita pilot ledger."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Pratipadika, Taddhita, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
CONFIG = HERE / "nominal_taddhita_pilot.json"
PRIOR = RESULTS / "sanadi_krdanta_summary.json"
STANDARD = HERE / "admission_standard.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
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

    config = json.loads(CONFIG.read_text())
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    admitted = []
    excluded = []
    candidates = 0
    for nominal in config["nominal_inputs"]:
        base = (
            Pratipadika.nyap(nominal["input_slp1"])
            if nominal["nyap"]
            else Pratipadika.basic(nominal["input_slp1"])
        )
        for operation in config["operations"]:
            if nominal["input_type"] != operation["eligible_input_type"]:
                continue
            candidates += 1
            forms = sorted({
                result.text
                for result in grammar.derive(Pratipadika.taddhitanta(
                    base, getattr(Taddhita, operation["source_variant"])
                ))
            })
            common = {
                "nominal_id": nominal["nominal_id"],
                "nominal_input_slp1": nominal["input_slp1"],
                "nominal_display": nominal["display"],
                "nominal_input_type": nominal["input_type"],
                "nominal_input_source_basis": nominal["source_basis"],
                "operation_id": operation["operation_id"],
                "taddhita_source_variant": operation["source_variant"],
                "operation_display": operation["display"],
                "semantic_branch_id": operation["semantic_branch_id"],
                "semantic_relation": operation["semantic_relation"],
                "rule_refs": ";".join(operation["rule_refs"]),
            }
            if forms:
                admitted.append({
                    "derived_word_meaning_id": stable_id(
                        "taddhita-pilot", nominal["nominal_id"], operation["operation_id"]
                    ),
                    **common,
                    "output_forms_slp1": ";".join(forms),
                    "output_variant_count": str(len(forms)),
                    "admission_basis": "bounded_nominal_input_plus_sourced_semantic_operation_plus_pinned_engine_output",
                    "count_status": "admitted_research_pilot",
                })
            else:
                excluded.append({
                    **common,
                    "output_forms_slp1": "",
                    "reason": "The selected taddhita operation produced no form from this declared nominal input.",
                    "count_status": "not_admitted_engine_zero_unresolved",
                })

    prior = json.loads(PRIOR.read_text())["bounded_word_meaning_subtotal"]
    records = {row["filename"]: row for row in manifest["sources"]}
    by_operation = Counter(row["operation_id"] for row in admitted)
    report = {
        "date": "2026-09-13",
        "scope": config["scope"],
        "nominal_input_count": len(config["nominal_inputs"]),
        "selected_taddhita_semantic_operations": len(config["operations"]),
        "eligible_operation_candidates": candidates,
        "admitted_taddhita_word_meanings": len(admitted),
        "not_admitted_total": len(excluded),
        "admitted_by_operation": dict(sorted(by_operation.items())),
        "prior_bounded_word_meaning_subtotal": prior,
        "bounded_word_meaning_subtotal_including_pilot": prior + len(admitted),
        "vocabulary_total": None,
        "publication_status": "bounded_pilot_only_not_a_nominal_inventory_total",
        "engine": {
            "name": "Vidyut", "version": importlib.metadata.version("vidyut"),
            "commit": manifest["generator_commit"],
        },
        "sources": [
            records[name]
            for name in (
                "vidyut-args-taddhita.rs", "rule-4.1.92.html",
                "rule-4.1.120.html", "rule-5.1.119.html", "kashika_4_1.rs",
            )
        ],
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (CONFIG, PRIOR, STANDARD, MANIFEST, Path(__file__))
        },
    }
    RESULTS.mkdir(exist_ok=True)
    write_csv(
        RESULTS / "nominal_input_inventory.csv",
        [{
            "nominal_id": row["nominal_id"],
            "input_slp1": row["input_slp1"],
            "display": row["display"],
            "input_type": row["input_type"],
            "nyap": str(row["nyap"]).lower(),
            "source_basis": row["source_basis"],
        } for row in config["nominal_inputs"]],
        ["nominal_id", "input_slp1", "display", "input_type", "nyap", "source_basis"],
    )
    admitted_fields = list(admitted[0]) if admitted else ["derived_word_meaning_id"]
    excluded_fields = list(excluded[0]) if excluded else ["nominal_id"]
    write_csv(RESULTS / "taddhita_pilot_ledger.csv", admitted, admitted_fields)
    write_csv(RESULTS / "taddhita_pilot_exclusions.csv", excluded, excluded_fields)
    (RESULTS / "taddhita_pilot_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Bounded तद्धितान्त Pilot", "",
        "This pass declares five nominal inputs before applying any operation. It then tests two sourced relations: अपत्यम् (*apatyam*), descent or offspring, and भावः (*bhāvaḥ*), state or defining quality.", "",
        "| Measure | Count |", "|---|---:|",
        f"| Declared nominal inputs | {report['nominal_input_count']} |",
        f"| Eligible operation candidates | {candidates} |",
        f"| Admitted तद्धित word-meanings | {len(admitted)} |",
        f"| Not admitted | {len(excluded)} |",
        f"| **Bounded subtotal including this pilot** | **{report['bounded_word_meaning_subtotal_including_pilot']:,}** |", "",
        "The five inputs are not presented as a Sanskrit nominal inventory. They keep the experiment reproducible while demonstrating why a defensible full तद्धित count must first establish a bounded, sourced inventory of nominal bases and their grammatical properties.", "",
        "The pilot remains laukika. It does not extrapolate five inputs across all 175 taddhita identifiers exposed by the engine.", "",
    ]
    (RESULTS / "taddhita_pilot_summary.md").write_text("\n".join(lines))
    print(
        f"Admitted {len(admitted)} taddhita pilot word-meanings from "
        f"{len(config['nominal_inputs'])} declared nominal inputs."
    )


if __name__ == "__main__":
    main()
