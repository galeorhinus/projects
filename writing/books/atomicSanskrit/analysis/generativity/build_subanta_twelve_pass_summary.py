#!/usr/bin/env python3
"""Subanta pass 12: publish the complete report and graph branch."""

from __future__ import annotations

import json
import subprocess
import sys

from subanta_common import HERE, RESULTS, project_path, read_json, sha256


INPUT_NAMES = (
    "subanta_citation_six_pass_summary.json", "subanta_paradigm_capacity.json",
    "subanta_gender_classification.json", "subanta_paradigm_sample.json",
    "subanta_sample_collisions.json", "subanta_capacity_reconciliation.json",
)
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
    complete = [node["id"] for node in graph["nodes"] if node.get("complete_pada") is True and node["id"] == "avyaya_complete_component"]
    lines.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef capacity fill:#f7f5f0,stroke:#5b4a35,stroke-dasharray:5 4,color:#221f1a;",
        f"    class {','.join(base)} base;", f"    class {','.join(capacity)} capacity;",
    ])
    if complete:
        lines.append(f"    class {','.join(complete)} complete;")
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(lines) + "\n")


def main() -> None:
    citation, capacity, gender, sample, collisions, reconciliation = [read_json(RESULTS / name) for name in INPUT_NAMES]
    report = {
        "date": "2026-09-14", "passes_completed": 12,
        "materialized_lexical_word_meaning_subtotal": reconciliation["materialized_lexical_word_meaning_subtotal"],
        "laukika_name_word_meanings": reconciliation["laukika_name_word_meanings"],
        "laukika_complete_unchanging_word_meanings": reconciliation["laukika_complete_unchanging_word_meanings"],
        "citation_semantic_cells": reconciliation["citation_semantic_cells"],
        "full_relation_number_semantic_cells": reconciliation["full_relation_number_semantic_cells"],
        "gender_multiplier": reconciliation["gender_multiplier"],
        "locally_regenerated_citation_sample_cells": reconciliation["locally_regenerated_citation_sample_cells"],
        "locally_regenerated_full_paradigm_sample_cells": reconciliation["locally_regenerated_full_paradigm_sample_cells"],
        "all_inflection_rows_materialized": False,
        "inflectional_cells_added_to_lexical_subtotal": False,
        "remaining_subanta_passes": 0,
        "withheld_extensions": [
            "agreement-driven additional gender forms", "Vedic-domain nominal inflection",
            "meaning-specific restrictions on number usage",
        ],
        "inputs": {project_path(RESULTS / name): sha256(RESULTS / name) for name in INPUT_NAMES},
        "publication_status": "research_capacity_only_not_deployed",
    }
    (RESULTS / "subanta_twelve_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Twelve-Pass नामरूप Capacity Report", "",
        "| Measurement | Result |", "|---|---:|",
        f"| लौकिक name, object, quality, state, and relation meanings | {report['laukika_name_word_meanings']:,} |",
        f"| लौकिक complete unchanging meanings | {report['laukika_complete_unchanging_word_meanings']:,} |",
        f"| Materialized lexical subtotal | {report['materialized_lexical_word_meaning_subtotal']:,} |",
        f"| One citation cell per name meaning | {report['citation_semantic_cells']:,} |",
        f"| Full 8 × 3 relation-number cells | {report['full_relation_number_semantic_cells']:,} |", "",
        "The first three rows describe lexical inventories. The final two describe grammatical views. Citation cells are contained within the full matrix, and neither capacity is added to the lexical subtotal.", "",
        "| Local verification set | Regenerated cells |", "|---|---:|",
        f"| Eight source-backed citation forms | {report['locally_regenerated_citation_sample_cells']:,} |",
        f"| Eight complete 8 × 3 sample paradigms | {report['locally_regenerated_full_paradigm_sample_cells']:,} |", "",
        "Gender is an output attribute rather than an automatic multiplier. Complete unchanging words do not enter the relation-number matrix. Repeated spellings retain every semantic and grammatical coordinate.", "",
    ]
    (RESULTS / "subanta_twelve_pass_summary.md").write_text("\n".join(lines))

    graph = read_json(GRAPH)
    ids = {"subanta_expansion_pending", "laukika_nominal_inventory", "subanta_citation_capacity", "subanta_paradigm_capacity"}
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] not in ids]
    graph["edges"] = [edge for edge in graph["edges"] if edge.get("from") not in ids and edge.get("to") not in ids]
    graph["nodes"].extend([
        {"id": "laukika_nominal_inventory", "stage": 29, "label": "Laukika name-meaning inventory", "reader_label": "Reconciled name, object, quality, state, and relation meanings", "added_count": report["laukika_name_word_meanings"], "cumulative_count": None, "count_unit": "word_meaning_input", "form_class": "virtual_nominal_input_inventory", "complete_pada": False, "count_role": "virtual_input_inventory_not_lexical_subtotal", "included_in_current_research_subtotal": False},
        {"id": "subanta_citation_capacity", "stage": 30, "label": "Name-form citation capacity", "reader_label": "One citation coordinate per name meaning", "added_count": report["citation_semantic_cells"], "cumulative_count": None, "count_unit": "semantic_grammatical_cell", "form_class": "virtual_subanta", "complete_pada": True, "count_role": "grammatical_capacity_not_lexical_subtotal", "included_in_current_research_subtotal": False},
        {"id": "subanta_paradigm_capacity", "stage": 31, "label": "Full name-form capacity", "reader_label": "Eight relations by three number values", "added_count": report["full_relation_number_semantic_cells"], "cumulative_count": None, "count_unit": "semantic_grammatical_cell", "form_class": "virtual_subanta", "complete_pada": True, "count_role": "grammatical_capacity_not_lexical_subtotal", "included_in_current_research_subtotal": False},
    ])
    graph["edges"].extend([
        {"from": "compound_input_stacks", "to": "laukika_nominal_inventory", "operation": "select reconciled laukika name meanings", "added_count": report["laukika_name_word_meanings"], "non_additive_capacity_edge": True},
        {"from": "laukika_nominal_inventory", "to": "subanta_citation_capacity", "operation": "one citation coordinate", "added_count": report["citation_semantic_cells"], "non_additive_capacity_edge": True},
        {"from": "subanta_citation_capacity", "to": "subanta_paradigm_capacity", "operation": "eight relations by three number values", "added_count": report["full_relation_number_semantic_cells"], "non_additive_capacity_edge": True},
    ])
    graph["date"] = "2026-09-14"
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    regenerate_mermaid(graph)
    subprocess.run([sys.executable, str(HERE / "build_wordspace_category_graph.py")], check=True)
    print("Completed twelve name-form passes and updated both graphs.")


if __name__ == "__main__":
    main()
