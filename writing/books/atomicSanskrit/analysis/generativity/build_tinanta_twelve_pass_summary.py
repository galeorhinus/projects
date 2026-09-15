#!/usr/bin/env python3
"""Tinanta pass 12: publish the complete report and graph branch."""

from __future__ import annotations

import json

from tinanta_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, sha256


INPUTS = tuple(RESULTS / name for name in (
    "tinanta_citation_six_pass_summary.json", "tinanta_paradigm_capacity.json",
    "tinanta_pada_classification.json", "tinanta_paradigm_sample.json",
    "tinanta_sample_collisions.json", "tinanta_capacity_reconciliation.json",
))
GRAPH = RESULTS / "generation_stage_graph.json"


def regenerate_mermaid(graph: dict) -> None:
    lines = ["flowchart LR"]
    for node in graph["nodes"]:
        count = node.get("cumulative_count") if node.get("cumulative_count") is not None else node.get("added_count")
        text = f"{count:,}" if count is not None else "count pending"
        lines.append(f"    {node['id']}[\"{node['label']}<br/>{text}\"]")
    for edge in graph["edges"]:
        count = edge.get("added_count")
        if count is None:
            amount = "pending"
        elif edge.get("non_additive_component_edge"):
            amount = f"contains {count:,}"
        elif edge.get("non_additive_capacity_edge"):
            amount = f"capacity {count:,}"
        else:
            amount = f"{count:+,}"
        lines.append(f"    {edge['from']} -->|\"{edge['operation']} · {amount}\"| {edge['to']}")
    base = [node["id"] for node in graph["nodes"] if node.get("included_in_current_research_subtotal") and node["id"] != "avyaya_complete_component"]
    capacity = [node["id"] for node in graph["nodes"] if not node.get("included_in_current_research_subtotal") and node.get("added_count") is not None and node["id"] != "avyaya_complete_component"]
    complete = [node["id"] for node in graph["nodes"] if node["id"] == "avyaya_complete_component"]
    pending = [node["id"] for node in graph["nodes"] if node["id"].endswith("_pending")]
    lines.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef capacity fill:#f7f5f0,stroke:#5b4a35,stroke-dasharray:5 4,color:#221f1a;",
        f"    class {','.join(base)} base;", f"    class {','.join(capacity)} capacity;",
    ])
    if complete or pending:
        lines.append(f"    class {','.join(complete + pending)} complete;")
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(lines) + "\n")


def main() -> None:
    citation, paradigm, pada, sample, collisions, reconciliation = [json.loads(path.read_text()) for path in INPUTS]
    report = {
        "date": "2026-09-14", "passes_completed": 12,
        "laukika_verbal_word_meanings": reconciliation["laukika_verbal_word_meanings"],
        "materialized_lexical_word_meaning_subtotal": CURRENT_LEXICAL_SUBTOTAL,
        "third_person_singular_citation_cells": reconciliation["third_person_singular_citation_cells"],
        "full_kartari_person_number_cells": reconciliation["full_kartari_person_number_cells"],
        "pada_multiplier": reconciliation["pada_multiplier"],
        "locally_regenerated_citation_sample_cells": reconciliation["locally_regenerated_citation_sample_cells"],
        "locally_regenerated_full_paradigm_sample_cells": reconciliation["locally_regenerated_full_paradigm_sample_cells"],
        "all_inflection_rows_materialized": False,
        "inflectional_cells_added_to_lexical_subtotal": False,
        "remaining_tinanta_passes": 0,
        "next_stage": "सुबन्त eight-case-by-three-number expansion",
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
        "publication_status": "research_capacity_only_not_deployed",
    }
    (RESULTS / "tinanta_twelve_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Twelve-Pass तिङन्त Capacity Report", "",
        "| Measurement | Result |", "|---|---:|",
        f"| लौकिक verbal word-meanings | {report['laukika_verbal_word_meanings']:,} |",
        f"| Materialized lexical subtotal | {CURRENT_LEXICAL_SUBTOTAL:,} |",
        f"| Ten-लकार third-person singular citation cells | {report['third_person_singular_citation_cells']:,} |",
        f"| Full कर्तरि 10 × 3 × 3 cells | {report['full_kartari_person_number_cells']:,} |", "",
        "The first two numbers count lexical inventories. The final two count grammatical cells. Citation cells are already contained within the full matrix, and neither inflectional capacity is added to the lexical subtotal.", "",
        "| Local verification set | Regenerated cells |", "|---|---:|",
        f"| Eight construction classes plus an आत्मनेपदम् control across ten citation coordinates | {report['locally_regenerated_citation_sample_cells']:,} |",
        f"| भू, कृ, and एध् across all ten 3 × 3 paradigms | {report['locally_regenerated_full_paradigm_sample_cells']:,} |", "",
        "परस्मैपदम् and आत्मनेपदम् outputs remain attached to one semantic cell. Repeated spellings remain attached to every grammatical coordinate they realize. वैदिक लेट्, कर्मणि, भावे, and सुबन्त inflection remain separate.", "",
        "The next analytical stage is the सुबन्त eight-case-by-three-number matrix.", "",
    ]
    (RESULTS / "tinanta_twelve_pass_summary.md").write_text("\n".join(lines))

    graph = json.loads(GRAPH.read_text())
    ids = {"tinanta_expansion_pending", "laukika_verbal_inventory", "tinanta_citation_capacity", "tinanta_paradigm_capacity"}
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] not in ids]
    graph["edges"] = [edge for edge in graph["edges"] if edge.get("from") not in ids and edge.get("to") not in ids]
    graph["nodes"].extend([
        {"id": "laukika_verbal_inventory", "stage": 26, "label": "Laukika verbal-meaning inventory", "reader_label": "Reconciled verbal meanings available for inflection", "added_count": report["laukika_verbal_word_meanings"], "cumulative_count": None, "count_unit": "word_meaning_input", "form_class": "virtual_verbal_input_inventory", "complete_pada": False, "count_role": "virtual_input_inventory_not_lexical_subtotal", "included_in_current_research_subtotal": False},
        {"id": "tinanta_citation_capacity", "stage": 27, "label": "Ten-lakara citation capacity", "reader_label": "Third-person singular in ten laukika lakaras", "added_count": report["third_person_singular_citation_cells"], "cumulative_count": None, "count_unit": "semantic_grammatical_cell", "form_class": "virtual_tinanta", "complete_pada": True, "count_role": "grammatical_capacity_not_lexical_subtotal", "included_in_current_research_subtotal": False},
        {"id": "tinanta_paradigm_capacity", "stage": 28, "label": "Full kartari tinanta capacity", "reader_label": "Ten lakaras by three persons by three numbers", "added_count": report["full_kartari_person_number_cells"], "cumulative_count": None, "count_unit": "semantic_grammatical_cell", "form_class": "virtual_tinanta", "complete_pada": True, "count_role": "grammatical_capacity_not_lexical_subtotal", "included_in_current_research_subtotal": False},
    ])
    graph["edges"].extend([
        {"from": "compound_input_stacks", "to": "laukika_verbal_inventory", "operation": "select reconciled laukika verbal meanings", "added_count": report["laukika_verbal_word_meanings"], "non_additive_capacity_edge": True},
        {"from": "laukika_verbal_inventory", "to": "tinanta_citation_capacity", "operation": "ten third-person singular lakara coordinates", "added_count": report["third_person_singular_citation_cells"], "non_additive_capacity_edge": True},
        {"from": "tinanta_citation_capacity", "to": "tinanta_paradigm_capacity", "operation": "three purushas by three vacanas", "added_count": report["full_kartari_person_number_cells"], "non_additive_capacity_edge": True},
    ])
    graph["date"] = "2026-09-14"
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    regenerate_mermaid(graph)
    print("Completed twelve tinanta passes and updated the stage graph.")


if __name__ == "__main__":
    main()
