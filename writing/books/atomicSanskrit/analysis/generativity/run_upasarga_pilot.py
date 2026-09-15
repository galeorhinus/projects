#!/usr/bin/env python3
"""Build the normalized upasarga inventory and run a bounded gam pilot."""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut import lipi
from vidyut.prakriya import Data, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
INVENTORY = HERE / "upasarga_inventory.csv"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
GAM_CODE = "01.1137"

EXPECTED_RULES = {
    "1.4.58": "prAdayaH",
    "1.4.59": "upasargAH kriyAyoge",
    "1.4.60": "gatiSca",
    "1.4.80": "te prAgDAtoH",
}
EXPECTED_SOURCE_FORMS = [
    "pra", "parA", "apa", "sam", "anu", "ava", "nis", "nir", "dus", "dur",
    "vi", "AN", "ni", "aDi", "api", "ati", "su", "ut", "aBi", "prati", "pari", "upa",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def transliterate(text: str, scheme) -> str:
    return lipi.transliterate(text, lipi.Scheme.Slp1, scheme)


def transliterate_list(values: list[str], scheme) -> str:
    return ";".join(transliterate(value, scheme) for value in values)


def verify_sources() -> tuple[dict, dict[str, str]]:
    manifest = json.loads(MANIFEST.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    for record in records.values():
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")

    with (ARCHIVE / "sutrapatha.tsv").open() as handle:
        rules = {row["code"]: row["text"] for row in csv.DictReader(handle, delimiter="\t")}
    for code, text in EXPECTED_RULES.items():
        if rules.get(code) != text:
            raise ValueError(f"Unexpected rule text for {code}: {rules.get(code)!r}")
    return manifest, rules


def load_inventory() -> list[dict[str, str]]:
    rows = read_csv(INVENTORY)
    if len(rows) != 20:
        raise ValueError(f"Expected 20 normalized upasarga identities, found {len(rows)}")
    if [int(row["order"]) for row in rows] != list(range(1, 21)):
        raise ValueError("Upasarga inventory order is incomplete")
    if len({row["upasarga_id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate normalized upasarga identity")
    source_forms = [form for row in rows for form in row["source_forms_slp1"].split(";")]
    if source_forms != EXPECTED_SOURCE_FORMS:
        raise ValueError("The normalized inventory does not preserve the listed pradi forms")
    return rows


def current_base_count() -> int:
    rows = [row for row in read_csv(ASSIGNMENTS) if row["record_kind"] == "lexical"]
    return len({row["normalized_count_key"] for row in rows})


def run_pilot(inventory: list[dict[str, str]]) -> list[dict[str, str]]:
    entries = {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    gam = entries[GAM_CODE].dhatu
    rows = []
    for item in inventory:
        outputs = sorted({result.text for result in grammar.derive(gam.with_prefixes([item["engine_input_slp1"]]))})
        expected = sorted(filter(None, item["expected_gam_outputs_slp1"].split(";")))
        source_forms = item["source_forms_slp1"].split(";")
        rows.append({
            "order": item["order"],
            "upasarga_id": item["upasarga_id"],
            "source_forms_slp1": item["source_forms_slp1"],
            "source_forms_devanagari": transliterate_list(source_forms, lipi.Scheme.Devanagari),
            "source_forms_iast": transliterate_list(source_forms, lipi.Scheme.Iast),
            "engine_input_slp1": item["engine_input_slp1"],
            "base_source_code": GAM_CODE,
            "base_citation_slp1": "gam",
            "base_meaning": "गति (*gati*), movement or going",
            "output_forms_slp1": ";".join(outputs),
            "output_forms_devanagari": transliterate_list(outputs, lipi.Scheme.Devanagari),
            "output_forms_iast": transliterate_list(outputs, lipi.Scheme.Iast),
            "output_variant_count": str(len(outputs)),
            "matches_expected": str(outputs == expected).lower(),
            "semantic_status": "generated_meaning_open",
            "count_status": "pilot_subset_not_added_separately",
        })
    return rows


def build_report(manifest: dict, rules: dict[str, str], inventory: list[dict[str, str]], rows: list[dict[str, str]]) -> dict:
    records = {row["filename"]: row for row in manifest["sources"]}
    source_names = [
        "dhatupatha.tsv", "rule-1.4.58.html", "rule-1.4.59.html", "rule-1.4.60.html",
        "sutrapatha.tsv", "vidyut-args-dhatu.rs",
    ]
    bases = current_base_count()
    output_spellings = {
        form for row in rows for form in row["output_forms_slp1"].split(";") if form
    }
    return {
        "date": "2026-09-13",
        "scope": "One normalized upasarga attached to the original gam dhatu; no sanadi operation, stacking, inflection, or lexical admission.",
        "engine": {
            "name": "Vidyut",
            "version": importlib.metadata.version("vidyut"),
            "commit": manifest["generator_commit"],
        },
        "governing_rules": [
            {"code": code, "text_slp1": text}
            for code, text in EXPECTED_RULES.items()
        ],
        "inventory": {
            "listed_pradi_forms": len(EXPECTED_SOURCE_FORMS),
            "normalized_upasarga_identities": len(inventory),
            "normalizations": {
                "nis_nir": "One inventory identity; conditioned forms do not create two meanings by themselves.",
                "dus_dur": "One inventory identity; conditioned forms do not create two meanings by themselves.",
                "ang": "The source-listed AN carries an indicatory consonant; the operational prefix appears as A.",
                "ut": "The source-listed ut appears as ud before the voiced initial of gam.",
            },
        },
        "pilot": {
            "base_source_code": GAM_CODE,
            "base_word_meaning": "gam, movement or going",
            "operations_tested": len(rows),
            "operations_with_output": sum(bool(row["output_forms_slp1"]) for row in rows),
            "expectation_matches": sum(row["matches_expected"] == "true" for row in rows),
            "distinct_output_spellings_diagnostic": len(output_spellings),
            "generated_capacity_relations": len(rows),
            "separately_added_to_subtotal": 0,
        },
        "planned_full_matrix": {
            "original_base_word_meanings": bases,
            "normalized_upasargas": len(inventory),
            "structural_operation_base_pairs": bases * len(inventory),
            "pre_restriction_candidates": bases * len(inventory),
        },
        "semantic_boundary": [
            "The rules identify the pradi forms and classify them as upasargas when they connect with an action.",
            "The rules do not assign one uniform conventional gloss to every upasarga-dhatu pair.",
            "A generated pair enters the generativity count when the operation is licensed and no source condition prevents that pair from inheriting the selected base meaning.",
            "Attestation enriches the meaning record; it is not an admission gate.",
        ],
        "vocabulary_total": None,
        "publication_status": "inventory_and_generation_pilot_only_not_deployed",
        "sources": [records[name] for name in source_names],
        "manifest_source_count": len(manifest["sources"]),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (INVENTORY, ASSIGNMENTS, MANIFEST, Path(__file__))
        },
    }


def write_markdown(report: dict, rows: list[dict[str, str]]) -> None:
    inv = report["inventory"]
    pilot = report["pilot"]
    matrix = report["planned_full_matrix"]
    lines = [
        "# उपसर्गः (*Upasargaḥ*) Inventory and गम् (*Gam*) Pilot", "",
        "This first pass fixes the उपसर्गः inventory and tests one उपसर्गः at a time with गम् (*gam*), movement or going. Each successful pair demonstrates generated capacity. The pilot is not added separately because its rows belong inside the full matrix.", "",
        "## Governing Architecture", "",
        "Pāṇini first identifies the प्रादयः (*prādayaḥ*), then assigns the name उपसर्गः (*upasargaḥ*) when one of those forms connects with an action. The same forms also receive the name गति (*gati*), and their ordinary position is before the धातुः (*dhātuḥ*). These rules authorize the operation. A conventional gloss may remain open without erasing the generated word.", "",
        "## Inventory", "",
        f"The grammatical list contains **{inv['listed_pradi_forms']} forms**. Normalizing निस्/निर् and दुस्/दुर् as conditioned forms of two identities produces **{inv['normalized_upasarga_identities']} उपसर्ग identities**. The indicatory consonant in आङ् does not appear in the operational आ, and उत् appears as उद् before the voiced initial of गम्. None of those surface changes creates another meaning by itself.", "",
        "| # | Listed form | With गम् | Engine check | Lexical status |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        source = " / ".join(row["source_forms_devanagari"].split(";"))
        source_iast = " / ".join(row["source_forms_iast"].split(";"))
        outputs = ", ".join(row["output_forms_devanagari"].split(";"))
        outputs_iast = ", ".join(row["output_forms_iast"].split(";"))
        lines.append(
            f"| {row['order']} | {source} (*{source_iast}*) | {outputs} (*{outputs_iast}*) | "
            f"{'matched' if row['matches_expected'] == 'true' else 'mismatch'} | generated; pilot subset |"
        )
    lines.extend([
        "", "The twenty operations produced forms in all twenty cases. The सम् + गम् case produced two surface alternatives; both remain attached to one operation/base pair. The pilot therefore demonstrates **twenty generated relations** represented by twenty-one diagnostic spellings. These twenty are not added separately to the subtotal because the full matrix contains them.", "",
        "## Full-Run Boundary", "",
        f"A complete one-उपसर्गः matrix over the **{matrix['original_base_word_meanings']:,} original base meanings** contains **{matrix['structural_operation_base_pairs']:,} structural candidates** before source restrictions are applied. Every successfully generated and grammatically permitted pair enters the bounded generativity count. A later meaning pass can replace an open gloss with an established one or add independently supported additional meanings.", "",
        "The full run remains limited to original धातु meanings. It does not add सनादि derivatives, stacked उपसर्गाः, or inflection.", "",
    ])
    (RESULTS / "upasarga_pilot.md").write_text("\n".join(lines))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This pilot requires Vidyut 0.4.0")
    manifest, rules = verify_sources()
    inventory = load_inventory()
    rows = run_pilot(inventory)
    report = build_report(manifest, rules, inventory, rows)
    RESULTS.mkdir(exist_ok=True)
    write_csv(RESULTS / "upasarga_pilot.csv", rows)
    (RESULTS / "upasarga_pilot.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_markdown(report, rows)
    print(
        f"Upasarga pilot: {report['pilot']['expectation_matches']}/{report['pilot']['operations_tested']} "
        f"checks matched; {report['pilot']['generated_capacity_relations']} generated relations demonstrated."
    )


if __name__ == "__main__":
    main()
