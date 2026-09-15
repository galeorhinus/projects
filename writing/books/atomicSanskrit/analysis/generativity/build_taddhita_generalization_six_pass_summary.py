#!/usr/bin/env python3
"""Summarize the six-pass comparative/superlative generalization round."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

from vidyut.lipi import Scheme, transliterate


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
CLASSIFICATION = RESULTS / "taddhita_generalization_classification.json"
ELIGIBILITY = RESULTS / "taddhita_generalization_eligibility.json"
GENERATION = RESULTS / "taddhita_generalization_generation.json"
VERIFICATION = RESULTS / "taddhita_generalization_verification.json"
RECONCILIATION = RESULTS / "taddhita_generalization_reconciliation.json"
LEDGER = RESULTS / "taddhita_generalization_ledger.csv.gz"
GRAPH = RESULTS / "generation_stage_graph.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deva(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Devanagari)


def iast(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Iast)


def regenerate_mermaid(graph: dict) -> None:
    lines = ["flowchart LR"]
    for node in graph["nodes"]:
        count = (
            f"{node['cumulative_count']:,}" if node["cumulative_count"] is not None
            else f"{node['added_count']:,}" if node["added_count"] is not None
            else "count pending"
        )
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
        "    class dhatu_meanings,one_sanadi,one_upasarga,upasarga_sanadi,curadi_causative,two_upasarga,first_krdanta,wider_krdanta,laukika_domain_correction,vaidika_layer,broad_taddhita,conditioned_taddhita,stri,namadhatu,nan_privative,additional_suffix_relations,plain_source_taddhita,generalized_comparison base;",
        "    class avyaya_complete_component complete;",
        "    class compound_expansion_pending pending;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(lines) + "\n")


def main() -> None:
    classification, eligibility, generation, verification, reconciliation = [
        json.loads(path.read_text())
        for path in (CLASSIFICATION, ELIGIBILITY, GENERATION, VERIFICATION, RECONCILIATION)
    ]
    if eligibility["eligible_operation_relations"] != generation["eligible_operation_relations"]:
        raise ValueError("Eligibility and generation disagree")
    if generation["engine_verified_candidate_relations"] != verification["candidate_relations_verified"]:
        raise ValueError("Generation and verification disagree")
    if verification["candidate_relations_verified"] != reconciliation["verified_candidate_relations"]:
        raise ValueError("Verification and reconciliation disagree")

    wanted = {
        ("kartavya", "superlative_tamap"),
        ("kartavya", "comparative_tarap"),
    }
    examples = {}
    with gzip.open(LEDGER, "rt", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            for form in row["input_forms_slp1"].split(";"):
                key = (form, row["taddhita_operation_id"])
                if key in wanted and key not in examples:
                    examples[key] = row
            if len(examples) == len(wanted):
                break
    if set(examples) != wanted:
        raise ValueError(f"Missing summary examples: {sorted(wanted - set(examples))}")

    graph = json.loads(GRAPH.read_text())
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] != "generalized_comparison"]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["from"] != "generalized_comparison"
        and edge["to"] != "generalized_comparison"
        and not (edge["from"] == "plain_source_taddhita" and edge["to"] == "compound_expansion_pending")
    ]
    graph["nodes"].append({
        "id": "generalized_comparison",
        "stage": 18,
        "label": "General comparative and superlative relations",
        "reader_label": "Nominal meanings can express greater and highest degrees under stated semantic conditions",
        "added_count": reconciliation["additional_generalized_word_meanings"],
        "cumulative_count": reconciliation["combined_bounded_word_meaning_subtotal"],
        "count_unit": "word_meaning",
        "form_class": "derived_nominal_base",
        "complete_pada": False,
        "count_role": "cumulative_subtotal",
        "included_in_current_research_subtotal": True,
    })
    graph["edges"].extend([
        {
            "from": "plain_source_taddhita",
            "to": "generalized_comparison",
            "operation": "comparative and superlative relations",
            "added_count": reconciliation["additional_generalized_word_meanings"],
        },
        {
            "from": "generalized_comparison",
            "to": "compound_expansion_pending",
            "operation": "other bounded compounds",
            "added_count": None,
        },
    ])
    graph["date"] = "2026-09-14"
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    regenerate_mermaid(graph)

    report = {
        "date": "2026-09-14",
        "passes_completed": 6,
        "semantic_families_reviewed": classification["semantic_families_reviewed"],
        "selected_semantic_families": classification["selected_families"],
        "nominal_word_meanings": eligibility["nominal_word_meanings"],
        "deferred_gunavacana_operations": eligibility["deferred_gunavacana_operations"],
        "eligible_operation_relations": eligibility["eligible_operation_relations"],
        "engine_verified_candidate_relations": generation["engine_verified_candidate_relations"],
        "engine_zero_or_error_relations": generation["engine_zero_or_error_relations"],
        "existing_word_meaning_overlaps_not_added": reconciliation["existing_word_meaning_overlaps_not_added"],
        "additional_generalized_word_meanings": reconciliation["additional_generalized_word_meanings"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "remaining_passes": 30,
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (CLASSIFICATION, ELIGIBILITY, GENERATION, VERIFICATION, RECONCILIATION, LEDGER, GRAPH, Path(__file__))
        },
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "taddhita_generalization_six_pass_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Six-Pass Comparative and Superlative Expansion", "",
        "This round extends two recovered तद्धित families beyond their source examples. The grammar supplies the relation, the nominal inventory supplies independently recorded meanings and semantic classes, and Vidyut supplies the generated forms.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | Review {classification['semantic_families_reviewed']} recovered semantic families. Comparative and superlative proceed; every other unexpanded family retains a source or semantic-class boundary. |",
        f"| 2 | Admit तमप् and तरप् across {eligibility['nominal_word_meanings']:,} nominal meanings. Keep इष्ठन् and ईयसुन् outside the count because 5.3.58 requires the traditional गुणवचन class, which the present inventory does not independently identify. |",
        f"| 3 | Generate {generation['engine_verified_candidate_relations']:,} candidate word-meanings through pinned Vidyut 0.4.0. |",
        f"| 4 | Verify stable IDs, output-bearing rows, arithmetic, and four independent sample paths. No engine failures occur. |",
        f"| 5 | Remove {reconciliation['existing_word_meaning_overlaps_not_added']} prior source-ledger overlap. |",
        f"| 6 | Add **{reconciliation['additional_generalized_word_meanings']:,}** word-meanings, raising the combined bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,}**. |",
        "", "## Examples", "",
        "| Starting word | Generated word | Operation |", "|---|---|---|",
    ]
    labels = {
        "superlative_tamap": "highest degree with तमप्",
        "comparative_tarap": "greater degree with तरप्",
    }
    for key in sorted(wanted):
        row = examples[key]
        form = key[0]
        output = row["output_forms_slp1"].split(";")[0]
        lines.append(
            f"| {deva(form)} (*{iast(form)}*) | {deva(output)} (*{iast(output)}*) | {labels[key[1]]} |"
        )
    lines.extend([
        "", "## Boundary", "",
        "The count records a grammatical relation that a speaker can intentionally express. It does not require an existing dictionary entry. इष्ठन् and ईयसुन् remain deferred with the narrower families involving descent, geography, materials, measures, times, directions, social roles, and lexical lists because the present inventory does not identify their required input classes.", "",
        "The result remains a research subtotal. It has not changed the manuscript, companion, covers, or published endnotes.", "",
    ])
    (RESULTS / "taddhita_generalization_six_pass_summary.md").write_text("\n".join(lines))
    print(
        "Six comparative/superlative passes complete; "
        f"combined bounded subtotal {report['combined_bounded_word_meaning_subtotal']:,}."
    )


if __name__ == "__main__":
    main()
