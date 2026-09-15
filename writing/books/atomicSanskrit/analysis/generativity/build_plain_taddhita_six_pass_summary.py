#!/usr/bin/env python3
"""Summarize the plain-taddhita passes and extend the reporting graph."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from vidyut.lipi import Scheme, transliterate

from taddhita_conditioned_common import HERE, RESULTS, sha256


INVENTORY = RESULTS / "plain_taddhita_source_assertions.json"
CLASSIFICATION = RESULTS / "plain_taddhita_semantic_classification.json"
ELIGIBILITY = RESULTS / "plain_taddhita_eligibility.json"
VERIFICATION = RESULTS / "plain_taddhita_verification.json"
RECONCILIATION = RESULTS / "plain_taddhita_reconciliation.json"
LEDGER = RESULTS / "plain_taddhita_ledger.csv"
GRAPH = RESULTS / "generation_stage_graph.json"


def deva(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Devanagari)


def iast(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Iast)


def regenerate_mermaid(graph: dict) -> None:
    lines = ["flowchart LR"]
    for node in graph["nodes"]:
        if node["cumulative_count"] is not None:
            count = f"{node['cumulative_count']:,}"
        elif node["added_count"] is not None:
            count = f"{node['added_count']:,}"
        else:
            count = "count pending"
        lines.append(f"    {node['id']}[\"{node['label']}<br/>{count}\"]")
    for edge in graph["edges"]:
        if edge["added_count"] is None:
            added = "pending"
        elif edge.get("non_additive_component_edge"):
            added = f"contains {edge['added_count']:,}"
        else:
            added = f"{edge['added_count']:+,}"
        lines.append(f"    {edge['from']} -->|\"{edge['operation']} · {added}\"| {edge['to']}")
    lines.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef pending fill:#f7f5f0,stroke:#777,stroke-dasharray:5 4,color:#444;",
        "    class dhatu_meanings,one_sanadi,one_upasarga,upasarga_sanadi,curadi_causative,two_upasarga,first_krdanta,wider_krdanta,laukika_domain_correction,vaidika_layer,broad_taddhita,conditioned_taddhita,stri,namadhatu,nan_privative,additional_suffix_relations,plain_source_taddhita base;",
        "    class avyaya_complete_component complete;",
        "    class compound_expansion_pending pending;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(lines) + "\n")


def main() -> None:
    inventory, classification, eligibility, verification, reconciliation = [
        json.loads(path.read_text())
        for path in (INVENTORY, CLASSIFICATION, ELIGIBILITY, VERIFICATION, RECONCILIATION)
    ]
    if classification["classified_positive_assertions"] != inventory["positive_assertions"]:
        raise ValueError("Source inventory and semantic classification disagree")
    if eligibility["eligible_word_meaning_relations"] != verification["eligible_relations"]:
        raise ValueError("Eligibility and verification counts disagree")
    if verification["verified_relations"] != reconciliation["verified_candidate_relations"]:
        raise ValueError("Verification and reconciliation counts disagree")
    if reconciliation["verified_candidate_relations"] != (
        reconciliation["additional_plain_taddhita_word_meanings"]
        + reconciliation["existing_word_meaning_overlaps_not_added"]
    ):
        raise ValueError("Verified relations do not reconcile")

    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    admitted = [
        row for row in rows
        if row["reconciliation_status"] == "admitted_additional_plain_relation"
    ]
    example_keys = [
        ("vayas", "vayasya", "VayasaTulyah"),
        ("mUla", "mUlya", "MulenaSamam"),
        ("anna", "annamaya", "TatPrakrtaVacane"),
        ("vAc", "vAcika", "VyahrtaArtha"),
        ("pawu", "pawizWa", "AtishayanaSuperlative"),
        ("kim", "kaTam", "Prakara"),
        ("tad", "tatra", "DigDeshaKalaLocative"),
        ("vEyAkaraRa", "vEyAkaraRapASa", "Yapya"),
    ]
    by_key = {
        (row["input_form_slp1"], row["expected_output_forms_slp1"], row["semantic_context"]): row
        for row in admitted
    }
    missing = [key for key in example_keys if key not in by_key]
    if missing:
        raise ValueError(f"Missing admitted examples: {missing}")

    graph = json.loads(GRAPH.read_text())
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] != "plain_source_taddhita"]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["from"] != "plain_source_taddhita"
        and edge["to"] != "plain_source_taddhita"
        and not (
            edge["from"] == "additional_suffix_relations"
            and edge["to"] == "compound_expansion_pending"
        )
    ]
    graph["nodes"].append({
        "id": "plain_source_taddhita",
        "stage": 17,
        "label": "Source-defined plain तद्धित relations",
        "reader_label": "Governing rules recover meanings behind further source-listed forms",
        "added_count": reconciliation["additional_plain_taddhita_word_meanings"],
        "cumulative_count": reconciliation["combined_bounded_word_meaning_subtotal"],
        "count_unit": "word_meaning",
        "form_class": "mixed_lexical_inventory",
        "complete_pada": "mixed",
        "count_role": "cumulative_subtotal",
        "included_in_current_research_subtotal": True,
        "nominal_bases": reconciliation["additional_nominal_bases"],
        "complete_avyayas": reconciliation["additional_complete_avyayas"],
    })
    graph["edges"].extend([
        {
            "from": "additional_suffix_relations",
            "to": "plain_source_taddhita",
            "operation": "source-defined plain तद्धित relations",
            "added_count": reconciliation["additional_plain_taddhita_word_meanings"],
        },
        {
            "from": "plain_source_taddhita",
            "to": "compound_expansion_pending",
            "operation": "other bounded compounds",
            "added_count": None,
        },
    ])
    graph["date"] = "2026-09-13"
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    regenerate_mermaid(graph)

    report = {
        "date": "2026-09-13",
        "passes_completed": 6,
        "literal_plain_assertions": inventory["literal_plain_assertions"],
        "positive_assertions": inventory["positive_assertions"],
        "active_positive_assertions": inventory["active_positive_assertions"],
        "ignored_positive_assertions_not_admitted": inventory["ignored_positive_assertions"],
        "active_semantic_rows": classification["active_semantic_rows"],
        "eligible_word_meaning_relations": eligibility["eligible_word_meaning_relations"],
        "duplicate_assertions_collapsed": eligibility["duplicate_assertions_collapsed"],
        "verified_relations": verification["verified_relations"],
        "existing_word_meaning_overlaps_not_added": reconciliation["existing_word_meaning_overlaps_not_added"],
        "additional_plain_taddhita_word_meanings": reconciliation["additional_plain_taddhita_word_meanings"],
        "additional_nominal_bases": reconciliation["additional_nominal_bases"],
        "additional_complete_avyayas": reconciliation["additional_complete_avyayas"],
        "additional_same_referent_or_lexical_derivatives": reconciliation["additional_same_referent_or_lexical_derivatives"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "stage_graph_nodes": len(graph["nodes"]),
        "inputs": {
            str(path.relative_to(HERE.parents[1])): sha256(path)
            for path in (
                INVENTORY, CLASSIFICATION, ELIGIBILITY, VERIFICATION,
                RECONCILIATION, LEDGER, GRAPH, Path(__file__),
            )
        },
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "plain_taddhita_six_pass_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )

    lines = [
        "# Six-Pass Plain तद्धित Expansion", "",
        "The earlier pass set these source assertions aside because the generic engine call supplied a form but not its meaning. This pass returns each active assertion to its governing rule. The rule supplies the semantic relation; Vidyut verifies the formation.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | Inventory {inventory['literal_plain_assertions']} literal assertions: {inventory['positive_assertions']} positive and {inventory['negative_assertions']} negative. Of the positive assertions, {inventory['active_positive_assertions']} are active and {inventory['ignored_positive_assertions']} occur only in ignored tests. |",
        f"| 2 | Attach all {classification['classified_positive_assertions']} positive assertions to archived rule pages and classify their semantic work. The active assertions produce {classification['active_semantic_rows']} semantic rows because one form, मूल्य (*mūlya*), carries two source-defined meanings. |",
        f"| 3 | Collapse {eligibility['duplicate_assertions_collapsed']} repeated assertions, leaving {eligibility['eligible_word_meaning_relations']} eligible relations: {eligibility['by_output_class']['nominal_base']} nominal bases and {eligibility['by_output_class']['complete_avyaya']} complete indeclinables. |",
        f"| 4 | Vidyut 0.4.0 reproduces all {verification['verified_relations']} eligible relations under their named suffixes. |",
        f"| 5 | Reconciliation finds {reconciliation['existing_word_meaning_overlaps_not_added']} word-meanings already present in earlier तद्धित ledgers. The remaining {reconciliation['additional_plain_taddhita_word_meanings']} are new. |",
        f"| 6 | Add {reconciliation['additional_nominal_bases']} nominal bases and {reconciliation['additional_complete_avyayas']} complete indeclinables, raising the combined bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,} word-meanings**. |",
        "", "## Examples", "",
        "| Starting point | Generated word | Meaning | Form class |",
        "|---|---|---|---|",
    ]
    for key in example_keys:
        row = by_key[key]
        lines.append(
            f"| {deva(row['input_form_slp1'])} (*{iast(row['input_form_slp1'])}*) | "
            f"{deva(row['expected_output_forms_slp1'])} (*{iast(row['expected_output_forms_slp1'])}*) | "
            f"{row['semantic_relation']} | {row['output_class'].replace('_', ' ')} |"
        )
    lines.extend([
        "", "The two meanings of मूल्य (*mūlya*) count separately because the governing rule states both relations. A single spelling does not collapse two meanings. By contrast, repeated assertions and alternative output forms do not create additional word-meanings.", "",
        "## Boundary", "",
        f"The {inventory['ignored_positive_assertions']} positive assertions found only in ignored engine tests remain documented but unadmitted. The {reconciliation['additional_same_referent_or_lexical_derivatives']} same-referent or lexical derivatives are reported separately inside the admitted total. This is a bounded source-example count, not a multiplier across every nominal base.", "",
        "The result remains a research subtotal. It has not changed the manuscript, companion, covers, or published endnotes.", "",
    ])
    (RESULTS / "plain_taddhita_six_pass_summary.md").write_text("\n".join(lines))
    print(
        "Six plain-taddhita passes complete; "
        f"combined bounded subtotal {report['combined_bounded_word_meaning_subtotal']:,}."
    )


if __name__ == "__main__":
    main()
