#!/usr/bin/env python3
"""Build the bounded one-upasarga generated-capacity ledger."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
INVENTORY = HERE / "upasarga_inventory.csv"
CONFLICTS = HERE / "upasarga_conflicts.json"
STANDARD = HERE / "admission_standard.md"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
PRIOR_SUMMARY = RESULTS / "verbal_derivation_summary.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def verify_inputs() -> tuple[dict, list[dict[str, str]], dict]:
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")
    inventory = read_csv(INVENTORY)
    if len(inventory) != 20 or len({row["upasarga_id"] for row in inventory}) != 20:
        raise ValueError("The normalized upasarga inventory must contain exactly 20 identities")
    conflicts = json.loads(CONFLICTS.read_text())
    restrictions_path = HERE / "upasarga_restrictions.json"
    restrictions_key = str(restrictions_path.relative_to(ROOT))
    if conflicts.get("inputs", {}).get(restrictions_key) != sha256(restrictions_path):
        raise ValueError("Run audit_upasarga_restrictions.py before rebuilding the upasarga ledger")
    lexical_source = conflicts.get("reviewed_lexical_source", {})
    if lexical_source.get("sha256") != next(
        row["sha256"] for row in manifest["sources"]
        if row["filename"] == lexical_source.get("filename")
    ):
        raise ValueError("The upasarga restriction source does not match the archive manifest")
    return manifest, inventory, conflicts


def lexical_assignments() -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    rows = [row for row in read_csv(ASSIGNMENTS) if row["record_kind"] == "lexical"]
    by_code: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_code[row["source_code"]].append(row)
    return rows, by_code


def run_engine(entries, inventory: list[dict[str, str]]) -> list[dict[str, str]]:
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for prefix in inventory:
        for entry in entries:
            outputs = sorted({
                result.text
                for result in grammar.derive(entry.dhatu.with_prefixes([prefix["engine_input_slp1"]]))
            })
            rows.append({
                "upasarga_id": prefix["upasarga_id"],
                "upasarga_order": prefix["order"],
                "source_forms_slp1": prefix["source_forms_slp1"],
                "engine_input_slp1": prefix["engine_input_slp1"],
                "source_code": entry.code,
                "gana": str(entry.dhatu.gana),
                "aupadeshika_slp1": entry.dhatu.aupadeshika,
                "source_artha_slp1": entry.artha,
                "engine_status": "generated" if outputs else "zero_output_unresolved",
                "output_forms_slp1": ";".join(outputs),
                "output_variant_count": str(len(outputs)),
            })
    return rows


def conflict_index(conflicts: dict) -> dict[tuple[str, str], dict]:
    index = {}
    for row in conflicts["exclusions"]:
        key = (row["upasarga_id"], row["base_count_key"])
        if key in index:
            raise ValueError(f"Duplicate upasarga conflict: {key}")
        index[key] = row
    return index


def build_ledgers(
    engine_rows: list[dict[str, str]],
    assignments_by_code: dict[str, list[dict[str, str]]],
    conflicts: dict,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    grouped: dict[tuple[str, str], dict] = {}
    zero_by_pair: set[tuple[str, str]] = set()
    for generated in engine_rows:
        outputs = {value for value in generated["output_forms_slp1"].split(";") if value}
        for base in assignments_by_code.get(generated["source_code"], []):
            key = (generated["upasarga_id"], base["normalized_count_key"])
            if not outputs:
                zero_by_pair.add(key)
                continue
            item = grouped.setdefault(key, {
                "upasarga_id": generated["upasarga_id"],
                "upasarga_order": generated["upasarga_order"],
                "upasarga_source_forms_slp1": generated["source_forms_slp1"],
                "base_count_key": base["normalized_count_key"],
                "base_source_codes": set(),
                "base_citations_slp1": set(),
                "base_meaning_slp1": set(),
                "base_meaning_display": set(),
                "output_forms_slp1": set(),
            })
            item["base_source_codes"].add(base["source_code"])
            item["base_citations_slp1"].add(base["normalized_citation_slp1"])
            item["base_meaning_slp1"].add(base["normalized_meaning_slp1"])
            item["base_meaning_display"].add(base["meaning_display"])
            item["output_forms_slp1"].update(outputs)

    blocked = conflict_index(conflicts)
    admitted = []
    excluded = []
    for key, item in grouped.items():
        flat = {
            field: ";".join(sorted(value)) if isinstance(value, set) else value
            for field, value in item.items()
        }
        forms = sorted(item["output_forms_slp1"])
        if key in blocked:
            excluded.append({
                **flat,
                "output_variant_count": str(len(forms)),
                "reason": blocked[key]["reason"],
                "rule_refs": ";".join(blocked[key]["rule_refs"]),
                "count_status": "not_counted_documented_conflict",
            })
            continue
        admitted.append({
            "generated_word_meaning_id": stable_id("upasarga", key[0], key[1]),
            **flat,
            "semantic_relation": "the upasarga modifies the base action; exact contextual gloss remains open",
            "semantic_status": "generated_meaning_open",
            "known_gloss": "",
            "rule_refs": "1.4.58;1.4.59",
            "output_variant_count": str(len(forms)),
            "admission_basis": "productive_upasarga_operation_plus_pinned_engine_output",
            "count_status": "admitted_generated_capacity",
        })

    engine_index = {
        (row["upasarga_id"], row["source_code"]): row
        for row in engine_rows
    }
    inventory_by_id = {row["upasarga_id"]: row for row in read_csv(INVENTORY)}
    for enrichment in conflicts["prefixed_meaning_enrichments"]:
        source_code = enrichment["source_code"]
        source_bases = assignments_by_code[source_code]
        citations = sorted({row["normalized_citation_slp1"] for row in source_bases})
        for upasarga_id in enrichment["resolved_upasarga_ids"]:
            generated = engine_index[(upasarga_id, source_code)]
            forms = sorted(value for value in generated["output_forms_slp1"].split(";") if value)
            if not forms:
                raise ValueError(f"No engine output for enriched meaning: {upasarga_id} {source_code}")
            base_key = json.dumps(
                [source_code, enrichment["meaning_id"]],
                ensure_ascii=True,
                separators=(", ", ": "),
            )
            prefix = inventory_by_id[upasarga_id]
            admitted.append({
                "generated_word_meaning_id": stable_id("upasarga-enrichment", upasarga_id, base_key),
                "upasarga_id": upasarga_id,
                "upasarga_order": prefix["order"],
                "upasarga_source_forms_slp1": prefix["source_forms_slp1"],
                "base_count_key": base_key,
                "base_source_codes": source_code,
                "base_citations_slp1": ";".join(citations),
                "base_meaning_slp1": enrichment["meaning_slp1"],
                "base_meaning_display": enrichment["meaning_display"],
                "output_forms_slp1": ";".join(forms),
                "semantic_relation": enrichment["semantic_relation"],
                "semantic_status": "source_attested_prefixed_meaning",
                "known_gloss": enrichment["meaning_display"],
                "rule_refs": enrichment["source_locator"],
                "output_variant_count": str(len(forms)),
                "admission_basis": "source_attested_prefixed_meaning_plus_pinned_engine_output",
                "count_status": "admitted_generated_capacity",
            })

    for upasarga_id, base_key in sorted(zero_by_pair - set(grouped)):
        excluded.append({
            "upasarga_id": upasarga_id,
            "upasarga_order": "",
            "upasarga_source_forms_slp1": "",
            "base_count_key": base_key,
            "base_source_codes": "",
            "base_citations_slp1": "",
            "base_meaning_slp1": "",
            "base_meaning_display": "",
            "output_forms_slp1": "",
            "output_variant_count": "0",
            "reason": "Vidyut produced no form; no grammatical prohibition is inferred.",
            "rule_refs": "1.4.58;1.4.59",
            "count_status": "not_admitted_engine_zero_unresolved",
        })

    admitted.sort(key=lambda row: (int(row["upasarga_order"]), row["base_count_key"]))
    excluded.sort(key=lambda row: (row["upasarga_id"], row["base_count_key"]))
    return admitted, excluded


def build_report(
    manifest: dict,
    inventory: list[dict[str, str]],
    conflicts: dict,
    assignments: list[dict[str, str]],
    engine_rows: list[dict[str, str]],
    admitted: list[dict[str, str]],
    excluded: list[dict[str, str]],
) -> dict:
    prior = json.loads(PRIOR_SUMMARY.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    source_names = [
        "dhatupatha.tsv", "rule-1.4.58.html", "rule-1.4.59.html", "rule-1.4.60.html",
        "sutrapatha.tsv", "vidyut-args-dhatu.rs", "dhatupatha-sanskritdocuments.html",
    ]
    spellings: dict[str, set[str]] = defaultdict(set)
    for row in admitted:
        for form in row["output_forms_slp1"].split(";"):
            if form:
                spellings[form].add(row["generated_word_meaning_id"])
    collisions = {form: ids for form, ids in spellings.items() if len(ids) > 1}
    by_prefix = Counter(row["upasarga_id"] for row in admitted)
    base_total = len({row["normalized_count_key"] for row in assignments})
    return {
        "date": "2026-09-13",
        "scope": "One normalized upasarga plus one original dhatu meaning; no sanadi operation, multiple upasargas, nominal derivation, or inflection.",
        "counting_standard": "A productive upasarga operation plus successful construction enters generated capacity. An exact conventional gloss or corpus attestation is not required. Explicit grammatical conflicts override generation.",
        "engine": {
            "name": "Vidyut",
            "version": importlib.metadata.version("vidyut"),
            "commit": manifest["generator_commit"],
        },
        "original_base_word_meanings": base_total,
        "normalized_upasarga_identities": len(inventory),
        "source_entry_operations_tested": len(engine_rows),
        "source_entry_operations_with_output": sum(row["engine_status"] == "generated" for row in engine_rows),
        "source_entry_zero_outputs": sum(row["engine_status"] != "generated" for row in engine_rows),
        "generated_upasarga_word_meanings": len(admitted),
        "generated_by_upasarga": dict(sorted(by_prefix.items(), key=lambda item: next(int(row["order"]) for row in inventory if row["upasarga_id"] == item[0]))),
        "documented_pair_conflicts": sum(row["count_status"] == "not_counted_documented_conflict" for row in excluded),
        "unresolved_zero_output_pairs": sum(row["count_status"] == "not_admitted_engine_zero_unresolved" for row in excluded),
        "meaning_status": {
            "generated_meaning_open": sum(row["semantic_status"] == "generated_meaning_open" for row in admitted),
            "source_attested_prefixed_meanings": sum(row["semantic_status"] == "source_attested_prefixed_meaning" for row in admitted),
            "known_glosses_attached": sum(bool(row["known_gloss"]) for row in admitted),
            "policy": "Known glosses enrich rows and independently supported additional meanings add rows; unattested status does not subtract a generated formation.",
        },
        "spelling_diagnostics": {
            "distinct_output_spellings": len(spellings),
            "spellings_shared_by_multiple_generated_word_meanings": len(collisions),
            "shared_spelling_word_meaning_links": sum(len(ids) for ids in collisions.values()),
            "policy": "Spelling identity does not merge different words or meanings.",
        },
        "prior_verbal_subtotal_including_bases": prior["verbal_word_meanings_including_bases"],
        "bounded_verbal_capacity_subtotal": prior["verbal_word_meanings_including_bases"] + len(admitted),
        "conflict_register_status": conflicts["status"],
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "sources": [records[name] for name in source_names],
        "manifest_source_count": len(manifest["sources"]),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                INVENTORY, CONFLICTS, HERE / "upasarga_restrictions.json", STANDARD,
                ASSIGNMENTS, PRIOR_SUMMARY, MANIFEST, Path(__file__),
            )
        },
    }


def write_markdown(report: dict) -> None:
    lines = [
        "# One-उपसर्गः (*Upasargaḥ*) Generated-Capacity Ledger", "",
        "This pass tests each of the twenty normalized उपसर्ग identities against every one of the 2,634 original धातु meanings. It counts Sanskrit's rule-licensed generative capacity, not the contents of a dictionary or corpus.", "",
        "## Result", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Earlier verbal subtotal, including original bases and one सनादि operation | {report['prior_verbal_subtotal_including_bases']:,} |",
        f"| One-उपसर्गः formations from original bases | {report['generated_upasarga_word_meanings']:,} |",
        f"| **Bounded verbal-capacity subtotal** | **{report['bounded_verbal_capacity_subtotal']:,}** |", "",
        f"Vidyut tested **{report['source_entry_operations_tested']:,} source-entry operations** and constructed at least one form for all **{report['source_entry_operations_with_output']:,}**. Reconciliation against distinct base meanings, followed by the source-level restriction and enrichment audit, produced **{report['generated_upasarga_word_meanings']:,} generated word-meanings**.", "",
        "## Meaning Status", "",
        f"Of the admitted rows, **{report['meaning_status']['generated_meaning_open']:,}** have a known base meaning and a rule-licensed उपसर्ग operation while their exact prefixed gloss remains open. The धातुपाठः directly supplies **{report['meaning_status']['source_attested_prefixed_meanings']} additional prefixed meanings**. That openness is part of the capacity being measured: Sanskrit can generate the word before a dictionary records how a particular speaker uses it.", "",
        "Attested usage can later replace an open gloss with an established one. If one generated word carries several independently supported meanings, those meanings add separate entries. Lack of attestation does not remove the generated word.", "",
        "## Exclusions", "",
        f"The general-rule review found no pair-level prohibition. The root-specific धातुपाठः audit found **{report['documented_pair_conflicts']} meaning/prefix conflicts**, and the engine produced **{report['source_entry_zero_outputs']} zero outputs**. Each exclusion records the restricted meaning, the affected prefix, and the exact source clause in `upasarga_conflicts.json`.", "",
        "## Spelling Is Not the Count", "",
        f"The ledger contains **{report['spelling_diagnostics']['distinct_output_spellings']:,} distinct generated spellings**. **{report['spelling_diagnostics']['spellings_shared_by_multiple_generated_word_meanings']:,} spellings** serve more than one generated word-meaning. Those entries remain separate because the governing distinction is a different word or meaning, not a different spelling.", "",
        "## Boundary", "",
        "This subtotal includes one उपसर्गः attached to an original धातु meaning. It excludes multiple उपसर्गाः, उपसर्ग + सनादि stacking, कृदन्तानि, तद्धितान्तानि, other nominal formations, and inflection. It remains a research subtotal and does not change the manuscript's published calculation.", "",
    ]
    (RESULTS / "upasarga_generation_summary.md").write_text("\n".join(lines))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest, inventory, conflicts = verify_inputs()
    assignments, by_code = lexical_assignments()
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    engine_rows = run_engine(entries, inventory)
    admitted, excluded = build_ledgers(engine_rows, by_code, conflicts)
    report = build_report(manifest, inventory, conflicts, assignments, engine_rows, admitted, excluded)
    write_csv(RESULTS / "upasarga_engine_results.csv", engine_rows, list(engine_rows[0]))
    write_csv(RESULTS / "upasarga_generation_ledger.csv", admitted, list(admitted[0]))
    exclusion_fields = [
        "upasarga_id", "upasarga_order", "upasarga_source_forms_slp1", "base_count_key",
        "base_source_codes", "base_citations_slp1", "base_meaning_slp1", "base_meaning_display",
        "output_forms_slp1", "output_variant_count", "reason", "rule_refs", "count_status",
    ]
    write_csv(RESULTS / "upasarga_generation_exclusions.csv", excluded, exclusion_fields)
    (RESULTS / "upasarga_generation_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_markdown(report)
    print(
        f"Admitted {len(admitted)} one-upasarga generated word-meanings; "
        f"bounded verbal capacity subtotal: {report['bounded_verbal_capacity_subtotal']}."
    )


if __name__ == "__main__":
    main()
