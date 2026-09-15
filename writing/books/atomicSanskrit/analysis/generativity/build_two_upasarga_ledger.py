#!/usr/bin/env python3
"""Build the bounded ledger for exactly two ordered upasargas."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
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
STACKING_MANIFEST = ARCHIVE / "upasarga_stacking_manifest.json"
INVENTORY = HERE / "upasarga_inventory.csv"
RESTRICTIONS = HERE / "upasarga_restrictions.json"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
PRIOR_SUMMARY = RESULTS / "curadi_causative_summary.json"
STANDARD = HERE / "admission_standard.md"

LEDGER_FIELDS = [
    "generated_word_meaning_id", "outer_upasarga_id", "inner_upasarga_id",
    "upasarga_sequence_slp1", "base_count_key", "base_source_codes",
    "base_citations_slp1", "base_meaning_slp1", "base_meaning_display",
    "semantic_relation", "semantic_status", "known_gloss", "rule_refs",
    "output_forms_slp1", "output_variant_count", "admission_basis", "count_status",
]
EXCLUSION_FIELDS = [
    "outer_upasarga_id", "inner_upasarga_id", "base_count_key", "base_source_codes",
    "base_meaning_slp1", "reason", "rule_refs", "count_status",
]


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


def restriction_index(config: dict, assignments: list[dict[str, str]]) -> dict[str, set[str]]:
    index = {}
    for restriction in config["restrictions"]:
        matches = [
            row for row in assignments
            if row["record_kind"] == "lexical"
            and row["source_code"] == restriction["source_code"]
            and row["normalized_meaning_slp1"] == restriction["meaning_slp1"]
        ]
        if len(matches) != 1:
            raise ValueError(f"Restriction did not resolve uniquely: {restriction['source_locator']}")
        index[matches[0]["normalized_count_key"]] = set(restriction["allowed_upasarga_ids"])
    return index


def enrichment_records(config: dict, bases_by_code: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for item in config["prefixed_meaning_enrichments"]:
        sources = bases_by_code[item["source_code"]]
        rows.append({
            "base_count_key": json.dumps([item["source_code"], item["meaning_id"]], separators=(", ", ": ")),
            "source_codes": {item["source_code"]},
            "citations": {citation for source in sources for citation in source["citations"]},
            "meanings_slp1": {item["meaning_slp1"]},
            "meanings_display": {item["meaning_display"]},
            "allowed_upasarga_ids": item["allowed_upasarga_ids"],
            "semantic_relation": item["semantic_relation"],
            "source_locator": item["source_locator"],
        })
    return rows


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")
    stacking_manifest = json.loads(STACKING_MANIFEST.read_text())
    for record in stacking_manifest["sources"]:
        if sha256(ARCHIVE / record["filename"]) != record["sha256"]:
            raise ValueError(f"Archived source changed: {record['filename']}")
    inventory = read_csv(INVENTORY)
    if len(inventory) != 20:
        raise ValueError("Expected twenty normalized upasarga identities")
    config = json.loads(RESTRICTIONS.read_text())
    assignments = read_csv(ASSIGNMENTS)
    bases = group_bases(assignments)
    bases_by_code: dict[str, list[dict]] = defaultdict(list)
    for base in bases:
        for code in base["source_codes"]:
            bases_by_code[code].append(base)
    restrictions = restriction_index(config, assignments)
    enrichments = enrichment_records(config, bases_by_code)
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)

    admitted_count = excluded_count = enrichment_count = source_operations = source_zero = 0
    excluded_by_reason = Counter()
    admitted_by_inner = Counter()
    distinct_spellings = set()
    ledger_path = RESULTS / "two_upasarga_ledger.csv.gz"
    exclusions_path = RESULTS / "two_upasarga_exclusions.csv.gz"
    with gzip.open(ledger_path, "wt", newline="", encoding="utf-8") as ledger_handle, gzip.open(exclusions_path, "wt", newline="", encoding="utf-8") as exclusion_handle:
        ledger_writer = csv.DictWriter(ledger_handle, fieldnames=LEDGER_FIELDS)
        exclusion_writer = csv.DictWriter(exclusion_handle, fieldnames=EXCLUSION_FIELDS)
        ledger_writer.writeheader()
        exclusion_writer.writeheader()
        for outer in inventory:
            for inner in inventory:
                sequence = [outer["engine_input_slp1"], inner["engine_input_slp1"]]
                outputs_by_code = {}
                for entry in entries:
                    source_operations += 1
                    forms = sorted({result.text for result in grammar.derive(entry.dhatu.with_prefixes(sequence))})
                    outputs_by_code[entry.code] = forms
                    if not forms:
                        source_zero += 1

                for base in bases:
                    allowed = restrictions.get(base["base_count_key"])
                    if allowed is not None and inner["upasarga_id"] not in allowed:
                        reason = "The recorded base meaning requires a different immediately preceding upasarga or no upasarga."
                        exclusion_writer.writerow({
                            "outer_upasarga_id": outer["upasarga_id"],
                            "inner_upasarga_id": inner["upasarga_id"],
                            "base_count_key": base["base_count_key"],
                            "base_source_codes": ";".join(sorted(base["source_codes"])),
                            "base_meaning_slp1": ";".join(sorted(base["meanings_slp1"])),
                            "reason": reason,
                            "rule_refs": "Dhatupatha prefix condition",
                            "count_status": "not_counted_documented_base_meaning_conflict",
                        })
                        excluded_count += 1
                        excluded_by_reason["not_counted_documented_base_meaning_conflict"] += 1
                        continue
                    forms = sorted({form for code in base["source_codes"] for form in outputs_by_code[code]})
                    if not forms:
                        exclusion_writer.writerow({
                            "outer_upasarga_id": outer["upasarga_id"],
                            "inner_upasarga_id": inner["upasarga_id"],
                            "base_count_key": base["base_count_key"],
                            "base_source_codes": ";".join(sorted(base["source_codes"])),
                            "base_meaning_slp1": ";".join(sorted(base["meanings_slp1"])),
                            "reason": "Vidyut produced no form; no grammatical prohibition is inferred.",
                            "rule_refs": "1.4.58;1.4.59;1.4.80;6.4.96",
                            "count_status": "not_admitted_engine_zero_unresolved",
                        })
                        excluded_count += 1
                        excluded_by_reason["not_admitted_engine_zero_unresolved"] += 1
                        continue
                    word_id = stable_id("two-upasarga", outer["upasarga_id"], inner["upasarga_id"], base["base_count_key"])
                    ledger_writer.writerow({
                        "generated_word_meaning_id": word_id,
                        "outer_upasarga_id": outer["upasarga_id"],
                        "inner_upasarga_id": inner["upasarga_id"],
                        "upasarga_sequence_slp1": "+".join(sequence),
                        "base_count_key": base["base_count_key"],
                        "base_source_codes": ";".join(sorted(base["source_codes"])),
                        "base_citations_slp1": ";".join(sorted(base["citations"])),
                        "base_meaning_slp1": ";".join(sorted(base["meanings_slp1"])),
                        "base_meaning_display": ";".join(sorted(base["meanings_display"])),
                        "semantic_relation": "the ordered pair of upasargas modifies the base action; exact contextual gloss remains open",
                        "semantic_status": "generated_meaning_open",
                        "known_gloss": "",
                        "rule_refs": "1.4.58;1.4.59;1.4.80;6.4.96",
                        "output_forms_slp1": ";".join(forms),
                        "output_variant_count": str(len(forms)),
                        "admission_basis": "two_ordered_productive_upasargas_plus_pinned_engine_output",
                        "count_status": "admitted_generated_capacity",
                    })
                    admitted_count += 1
                    admitted_by_inner[inner["upasarga_id"]] += 1
                    distinct_spellings.update(forms)

                for enrichment in enrichments:
                    allowed = enrichment["allowed_upasarga_ids"]
                    if allowed != "all" and inner["upasarga_id"] not in allowed:
                        continue
                    forms = sorted({form for code in enrichment["source_codes"] for form in outputs_by_code[code]})
                    if not forms:
                        raise ValueError(f"No output for enriched two-prefix meaning: {outer['upasarga_id']} {inner['upasarga_id']} {enrichment['base_count_key']}")
                    word_id = stable_id("two-upasarga-enrichment", outer["upasarga_id"], inner["upasarga_id"], enrichment["base_count_key"])
                    ledger_writer.writerow({
                        "generated_word_meaning_id": word_id,
                        "outer_upasarga_id": outer["upasarga_id"],
                        "inner_upasarga_id": inner["upasarga_id"],
                        "upasarga_sequence_slp1": "+".join(sequence),
                        "base_count_key": enrichment["base_count_key"],
                        "base_source_codes": ";".join(sorted(enrichment["source_codes"])),
                        "base_citations_slp1": ";".join(sorted(enrichment["citations"])),
                        "base_meaning_slp1": ";".join(sorted(enrichment["meanings_slp1"])),
                        "base_meaning_display": ";".join(sorted(enrichment["meanings_display"])),
                        "semantic_relation": enrichment["semantic_relation"],
                        "semantic_status": "source_attested_prefixed_meaning",
                        "known_gloss": ";".join(sorted(enrichment["meanings_display"])),
                        "rule_refs": enrichment["source_locator"],
                        "output_forms_slp1": ";".join(forms),
                        "output_variant_count": str(len(forms)),
                        "admission_basis": "source_attested_prefixed_meaning_plus_two_prefix_engine_output",
                        "count_status": "admitted_generated_capacity",
                    })
                    admitted_count += 1
                    enrichment_count += 1
                    admitted_by_inner[inner["upasarga_id"]] += 1
                    distinct_spellings.update(forms)

    prior = json.loads(PRIOR_SUMMARY.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    source_names = ["dhatupatha.tsv", "dhatupatha-sanskritdocuments.html", "sutrapatha.tsv", "rule-1.4.58.html", "rule-1.4.59.html", "vidyut-args-dhatu.rs"]
    report = {
        "date": "2026-09-13",
        "scope": "Exactly two ordered normalized upasargas applied to each original dhatu meaning, plus source-attested prefix-conditioned meaning enrichments; no sanadi, krdanta, or inflection. Two positions are a declared computational bound, not a grammatical maximum.",
        "sequence_policy": "Aṣṭādhyāyī 1.4.80 places upasargas before the dhatu in laukika use, and 6.4.96 expressly recognizes a two-upasarga environment. The inventory contains 20 upasarga identities and therefore 400 ordered two-prefix sequences, including repetition. Rows record outer upasarga, then inner upasarga, then dhatu. For a meaning requiring a named upasarga, that upasarga must be the inner member immediately before the dhatu. An anupasarga-only meaning admits no sequence.",
        "base_word_meanings": len(bases),
        "ordered_upasarga_sequences": len(inventory) ** 2,
        "structural_base_candidates": len(bases) * len(inventory) ** 2,
        "source_entry_operations_tested": source_operations,
        "source_entry_zero_outputs": source_zero,
        "documented_base_meaning_conflicts": excluded_by_reason["not_counted_documented_base_meaning_conflict"],
        "unresolved_zero_output_meanings": excluded_by_reason["not_admitted_engine_zero_unresolved"],
        "source_attested_enrichment_meanings": enrichment_count,
        "admitted_two_upasarga_word_meanings": admitted_count,
        "admitted_by_inner_upasarga": dict(sorted(admitted_by_inner.items())),
        "distinct_output_spellings_diagnostic": len(distinct_spellings),
        "prior_bounded_verbal_capacity_subtotal": prior["bounded_verbal_capacity_subtotal"],
        "bounded_verbal_capacity_subtotal": prior["bounded_verbal_capacity_subtotal"] + admitted_count,
        "vocabulary_total": None,
        "publication_status": "research_subtotal_only_not_deployed",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "sources": [records[name] for name in source_names],
        "stacking_commentary_sources": stacking_manifest["sources"],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (INVENTORY, RESTRICTIONS, ASSIGNMENTS, PRIOR_SUMMARY, STANDARD, MANIFEST, STACKING_MANIFEST, Path(__file__))},
    }
    (RESULTS / "two_upasarga_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "two_upasarga_summary.md").write_text("\n".join([
        "# Two-उपसर्गः Generated-Capacity Ledger", "",
        "This pass applies exactly two ordered उपसर्गाः (*upasargāḥ*) to each original धातु meaning. Aṣṭādhyāyī 1.4.80 places the उपसर्गाः before the धातुः in लौकिक use, while 6.4.96 expressly recognizes a two-उपसर्ग environment. With twenty normalized prefix identities, the declared two-position experiment contains 400 ordered sequences. The grammar does not make two a general maximum.", "",
        "## Result", "",
        "| Layer | Word-meanings |", "|---|---:|",
        f"| Earlier bounded verbal subtotal | {report['prior_bounded_verbal_capacity_subtotal']:,} |",
        f"| Exactly two ordered उपसर्गाः | {admitted_count:,} |",
        f"| **Bounded verbal-capacity subtotal** | **{report['bounded_verbal_capacity_subtotal']:,}** |", "",
        f"The original base meanings yield **{report['structural_base_candidates']:,} structural candidates**. The धातुपाठ conditions exclude **{report['documented_base_meaning_conflicts']:,}** of them. Its two prefix-conditioned enrichment clauses add **{report['source_attested_enrichment_meanings']:,} word-meanings**. Vidyut produced no unresolved meaning-level failures.", "",
        "Each row records the sequence from outside inward: outer उपसर्गः + inner उपसर्गः + धातुः. For a meaning that requires a named prefix, the required prefix must stand directly beside the धातुः. Thus an outer prefix may precede आङ् or अधि, but another inner prefix cannot displace the required one. The meaning expressly marked अनुपसर्गात् remains unavailable to every prefixed sequence.", "",
        "Repeated prefix identities remain in scope because this pass measures rule-licensed generative capacity rather than dictionary inventory. Coincident spellings do not merge meanings or ordered operations.", "",
        "This bounded research subtotal excludes three or more prefixes, सनादि stacking, कृदन्तानि, inflection, and nominal formation.", "",
    ]))
    print(f"Admitted {admitted_count} two-upasarga word-meanings; bounded subtotal {report['bounded_verbal_capacity_subtotal']}.")


if __name__ == "__main__":
    main()
