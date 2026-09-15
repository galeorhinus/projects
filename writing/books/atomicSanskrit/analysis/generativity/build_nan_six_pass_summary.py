#!/usr/bin/env python3
"""Pass 6: summarize the nan pass and extend the generation-stage graph."""

from __future__ import annotations

import json

from nan_common import RESULTS, project_path, sha256


CLASSIFICATION = RESULTS / "nan_rule_classification.json"
EXAMPLES = RESULTS / "nan_source_examples.json"
ELIGIBILITY = RESULTS / "nan_eligibility.json"
GENERATION = RESULTS / "nan_summary.json"
RECONCILIATION = RESULTS / "nan_reconciliation.json"
GRAPH = RESULTS / "generation_stage_graph.json"


def main() -> None:
    classification = json.loads(CLASSIFICATION.read_text())
    examples = json.loads(EXAMPLES.read_text())
    eligibility = json.loads(ELIGIBILITY.read_text())
    generation = json.loads(GENERATION.read_text())
    reconciliation = json.loads(RECONCILIATION.read_text())
    graph = json.loads(GRAPH.read_text())
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] != "nan_privative"]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["from"] != "nan_privative" and edge["to"] != "nan_privative"
        and not (edge["from"] == "namadhatu" and edge["to"] == "compound_expansion_pending")
    ]
    graph["nodes"].append({
        "id": "nan_privative",
        "stage": 15,
        "label": "Bounded नञ् compounds",
        "reader_label": "Nouns and descriptive meanings generate negative counterparts",
        "added_count": reconciliation["additional_nan_word_meanings"],
        "cumulative_count": reconciliation["combined_bounded_word_meaning_subtotal"],
        "count_unit": "word_meaning",
        "form_class": "derived_nominal_base",
        "complete_pada": False,
        "count_role": "cumulative_subtotal",
        "included_in_current_research_subtotal": True,
        "familiar_example": {"input_slp1": "jYAna", "output_slp1": "ajYAna", "meaning": "absence of knowledge; ignorance"},
        "less_familiar_example": {"input_slp1": "kartftva", "output_slp1": "akartftva", "meaning": "absence or negation of agency"},
    })
    graph["edges"].extend([
        {
            "from": "namadhatu", "to": "nan_privative",
            "operation": "one bounded negative counterpart per current nominal meaning",
            "added_count": reconciliation["additional_nan_word_meanings"],
        },
        {"from": "nan_privative", "to": "compound_expansion_pending", "operation": "other bounded compounds", "added_count": None},
    ])
    graph["date"] = "2026-09-13"
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")

    mermaid = ["flowchart LR"]
    for node in graph["nodes"]:
        count = f"{node['cumulative_count']:,}" if node["cumulative_count"] is not None else (f"{node['added_count']:,}" if node["added_count"] is not None else "count pending")
        mermaid.append(f"    {node['id']}[\"{node['label']}<br/>{count}\"]")
    for edge in graph["edges"]:
        added = f"{edge['added_count']:+,}" if edge["added_count"] is not None and not edge.get("non_additive_component_edge") else (f"contains {edge['added_count']:,}" if edge["added_count"] is not None else "pending")
        mermaid.append(f"    {edge['from']} -->|\"{edge['operation']} · {added}\"| {edge['to']}")
    mermaid.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef pending fill:#f7f5f0,stroke:#777,stroke-dasharray:5 4,color:#444;",
        "    class dhatu_meanings,one_sanadi,one_upasarga,upasarga_sanadi,curadi_causative,two_upasarga,first_krdanta,wider_krdanta,laukika_domain_correction,vaidika_layer,broad_taddhita,conditioned_taddhita,stri,namadhatu,nan_privative base;",
        "    class avyaya_complete_component complete;",
        "    class compound_expansion_pending pending;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(mermaid) + "\n")

    report = {
        "date": "2026-09-13",
        "passes_completed": 6,
        "rules_classified": classification["rules_classified"],
        "source_examples_verified": examples["verified_examples"],
        "eligible_nominal_word_meanings": eligibility["eligible_nominal_word_meanings"],
        "admitted_nan_word_meanings": generation["admitted_nan_word_meanings"],
        "unresolved_candidates": generation["not_admitted_total"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "complete_inflected_words_counted": 0,
        "stage_graph_nodes": len(graph["nodes"]),
        "inputs": {project_path(path): sha256(path) for path in (CLASSIFICATION, EXAMPLES, ELIGIBILITY, GENERATION, RECONCILIATION, GRAPH, __import__("pathlib").Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "nan_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "nan_six_pass_summary.md").write_text("\n".join([
        "# Six-Pass नञ् Expansion", "",
        f"The six passes classify one semantic operation and its two surface outcomes, verify {examples['verified_examples']} source examples, assemble the current nominal input inventory, materialize the ledger, reconcile the count, and extend the generation graph.", "",
        f"One negative counterpart for each of **{eligibility['eligible_nominal_word_meanings']:,}** eligible nominal meanings raises the combined bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,}**.", "",
        "For readers, the operation is simpler than its grammatical label: a noun or descriptive meaning generates its negative counterpart. **ज्ञान** becomes **अज्ञान**; **कर्तृत्व** can become **अकर्तृत्व**. The second example shows capacity beyond the familiar vocabulary.", "",
        "The result remains a lexical subtotal. Other compounds, finite verb conjugation, and nominal declension have not entered it.", "",
    ]))
    print(f"Completed six nan passes; subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
