#!/usr/bin/env python3
"""Pass 6: summarize the namadhatu passes and refresh the stage graph."""

from __future__ import annotations

import json

from namadhatu_common import RESULTS, project_path, sha256


CLASSIFICATION = RESULTS / "namadhatu_operation_classification.json"
EXAMPLES = RESULTS / "namadhatu_source_examples.json"
ELIGIBILITY = RESULTS / "namadhatu_eligibility.json"
GENERATION = RESULTS / "namadhatu_summary.json"
RECONCILIATION = RESULTS / "namadhatu_reconciliation.json"
GRAPH = RESULTS / "generation_stage_graph.json"


STAGES = [
    (1, "dhatu_meanings", "Reconciled धातुः meanings", 2634, 2634),
    (2, "one_sanadi", "One सनादि operation", 12522, 15156),
    (3, "one_upasarga", "One उपसर्गः", 52567, 67723),
    (4, "upasarga_sanadi", "One उपसर्गः plus one सनादि operation", 250040, 317763),
    (5, "curadi_causative", "True चरादिगण causatives", 522, 318285),
    (6, "two_upasarga", "Exactly two ordered उपसर्गाः", 1051340, 1369625),
    (7, "first_krdanta", "First कृदन्त layer", 29996, 1399621),
    (8, "wider_krdanta", "Wider अव्यय and कृदन्त layers plus तद्धित pilot", 775100, 2174721),
    (9, "laukika_domain_correction", "Known लौकिक-वैदिक domain correction", -8660, 2166061),
    (10, "vaidika_layer", "वैदिक-only bases, descendants, and operations", 213398, 2379459),
    (11, "broad_taddhita", "Broad तद्धित relations", 2382230, 4761689),
    (12, "conditioned_taddhita", "Conditioned तद्धित relations", 975, 4762664),
    (13, "stri", "Source-demonstrated स्त्रीप्रत्ययः formations", 50, 4762714),
]

READER_LABELS = {
    "dhatu_meanings": "Recorded verbal atoms and their meanings",
    "one_sanadi": "Verbal transformations for causation, desire, repetition, and intensity",
    "one_upasarga": "One prefix redirects the action",
    "upasarga_sanadi": "A prefix combines with a verbal transformation",
    "curadi_causative": "A separate causative operation",
    "two_upasarga": "Two ordered prefixes redirect the action",
    "first_krdanta": "Verbs become actions, agents, instruments, qualities, and obligations",
    "wider_krdanta": "Those derivatives extend across prefixed and transformed verbs",
    "laukika_domain_correction": "Vedic-only formations move to the Vedic count",
    "vaidika_layer": "Vedic formations are counted in their own domain",
    "broad_taddhita": "Nouns generate words for quality, state, and possession",
    "conditioned_taddhita": "Nouns express descent, origin, use, measure, and other specific relations",
    "stri": "Eligible nouns generate feminine counterparts",
    "namadhatu": "Nouns become verbs",
}


def main() -> None:
    classification = json.loads(CLASSIFICATION.read_text())
    examples = json.loads(EXAMPLES.read_text())
    eligibility = json.loads(ELIGIBILITY.read_text())
    generation = json.loads(GENERATION.read_text())
    reconciliation = json.loads(RECONCILIATION.read_text())
    stages = STAGES + [(
        14, "namadhatu", "नामधातुः from the first nominal inventory",
        reconciliation["additional_namadhatu_word_meanings"],
        reconciliation["combined_bounded_word_meaning_subtotal"],
    )]
    nodes = [{
        "id": identifier,
        "stage": stage,
        "label": label,
        "reader_label": READER_LABELS[identifier],
        "added_count": added,
        "cumulative_count": cumulative,
        "count_unit": "word_meaning",
        "form_class": "derived_verbal_base_inventory" if stage <= 6 else "mixed_lexical_inventory",
        "complete_pada": False if stage <= 6 else "mixed",
        "count_role": "cumulative_subtotal",
        "included_in_current_research_subtotal": True,
    } for stage, identifier, label, added, cumulative in stages]
    nodes.extend([
        {
            "id": "avyaya_complete_component", "stage": 8,
            "label": "Complete अव्यय word-meanings already inside Stage 8",
            "added_count": 7902, "cumulative_count": None,
            "count_unit": "word_meaning",
            "form_class": "complete_indeclinable_word", "complete_pada": True,
            "count_role": "component_already_included_in_stage_8",
            "included_in_current_research_subtotal": True,
        },
        {
            "id": "compound_expansion_pending", "stage": None,
            "label": "Bounded समास expansion", "added_count": None,
            "cumulative_count": None, "count_unit": "word_meaning",
            "form_class": "derived_nominal_base", "complete_pada": False,
            "count_role": "future_addition",
            "included_in_current_research_subtotal": False,
        },
        {
            "id": "tinanta_expansion_pending", "stage": None,
            "label": "तिङन्त grammatical expansion", "added_count": None,
            "cumulative_count": None, "count_unit": "inflected_grammatical_cell",
            "form_class": "complete_inflected_word", "complete_pada": True,
            "count_role": "future_addition",
            "included_in_current_research_subtotal": False,
        },
        {
            "id": "subanta_expansion_pending", "stage": None,
            "label": "सुबन्त grammatical expansion", "added_count": None,
            "cumulative_count": None, "count_unit": "inflected_grammatical_cell",
            "form_class": "complete_inflected_word", "complete_pada": True,
            "count_role": "future_addition",
            "included_in_current_research_subtotal": False,
        },
    ])
    edges = [{
        "from": stages[index - 1][1], "to": stages[index][1],
        "operation": stages[index][2], "added_count": stages[index][3],
    } for index in range(1, len(stages))]
    edges.extend([
        {"from": "wider_krdanta", "to": "avyaya_complete_component", "operation": "contains complete indeclinables", "added_count": 7902, "non_additive_component_edge": True},
        {"from": "namadhatu", "to": "compound_expansion_pending", "operation": "bounded compounds", "added_count": None},
        {"from": "namadhatu", "to": "tinanta_expansion_pending", "operation": "conjugation", "added_count": None},
        {"from": "compound_expansion_pending", "to": "subanta_expansion_pending", "operation": "declension", "added_count": None},
    ])
    graph = {
        "date": "2026-09-13",
        "purpose": "Machine-readable source for a future figure showing how each operation enlarges the count while distinguishing derivational bases from complete inflected words.",
        "visual_encoding": {
            "derived_verbal_base_inventory": "solid warm fill",
            "mixed_lexical_inventory": "solid warm fill with mixed-form marker",
            "complete_indeclinable_word": "outlined accent fill",
            "derived_nominal_base": "solid light fill",
            "complete_inflected_word": "outlined accent fill",
            "pending_count": "dashed border",
            "edge_label": "operation and added count",
            "node_number": "cumulative count",
        },
        "count_warning": "Do not add cumulative node totals together. Added counts belong on edges; cumulative counts belong in nodes.",
        "nodes": nodes,
        "edges": edges,
    }
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")

    mermaid = ["flowchart LR"]
    for node in nodes:
        count = f"{node['cumulative_count']:,}" if node["cumulative_count"] is not None else (f"{node['added_count']:,}" if node["added_count"] is not None else "count pending")
        shape = f"{node['id']}[\"{node['label']}<br/>{count}\"]"
        mermaid.append(f"    {shape}")
    for edge in edges:
        added = f"{edge['added_count']:+,}" if edge["added_count"] is not None and not edge.get("non_additive_component_edge") else (f"contains {edge['added_count']:,}" if edge["added_count"] is not None else "pending")
        mermaid.append(f"    {edge['from']} -->|\"{edge['operation']} · {added}\"| {edge['to']}")
    mermaid.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef pending fill:#f7f5f0,stroke:#777,stroke-dasharray:5 4,color:#444;",
        "    class dhatu_meanings,one_sanadi,one_upasarga,upasarga_sanadi,curadi_causative,two_upasarga,first_krdanta,wider_krdanta,laukika_domain_correction,vaidika_layer,broad_taddhita,conditioned_taddhita,stri,namadhatu base;",
        "    class avyaya_complete_component complete;",
        "    class compound_expansion_pending pending;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(mermaid) + "\n")

    report = {
        "date": "2026-09-13",
        "passes_completed": 6,
        "rules_classified": classification["rules_classified"],
        "unique_source_relations": examples["unique_source_relations"],
        "broad_candidate_relations": eligibility["broad_candidate_relations"],
        "conditioned_candidate_relations": eligibility["active_conditioned_source_relations"],
        "admitted_namadhatu_word_meanings": generation["admitted_namadhatu_word_meanings"],
        "unresolved_candidates": generation["not_admitted_total"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "complete_inflected_words_counted": 0,
        "stage_graph_nodes": len(nodes),
        "inputs": {project_path(path): sha256(path) for path in (
            CLASSIFICATION, EXAMPLES, ELIGIBILITY, GENERATION,
            RECONCILIATION, GRAPH, __import__("pathlib").Path(__file__)
        )},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "namadhatu_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "namadhatu_six_pass_summary.md").write_text("\n".join([
        "# Six-Pass नामधातुः Expansion", "",
        "The six passes classify the rule family, recover its source examples, declare semantic eligibility, materialize generated bases, reconcile the subtotal, and preserve the process as graph data.", "",
        f"Four productive relations contribute **{eligibility['broad_candidate_relations']:,}** meanings. The narrower rules contribute **{eligibility['active_conditioned_source_relations']:,}** source-demonstrated meanings. All **{generation['admitted_namadhatu_word_meanings']:,}** candidates generated, raising the combined bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,}**.", "",
        "Every new row is a derived verbal base. The graph marks तिङन्त and सुबन्त expansion separately because those operations produce complete inflected words rather than new lexical bases.", "",
        "The JSON graph is the source of truth; the Mermaid file is a working visualization. A publication figure should be drawn only after the remaining lexical and inflectional layers are complete.", "",
    ]))
    print(f"Completed six namadhatu passes; subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
