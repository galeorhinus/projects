#!/usr/bin/env python3
"""Capacity pass 12: publish the complete research report and graph branch."""

from __future__ import annotations

import json

from samasa_capacity_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, sha256


INPUTS = (
    RESULTS / "samasa_capacity_six_pass_summary.json",
    RESULTS / "samasa_reuse_classification.json",
    RESULTS / "samasa_reuse_eligibility.json",
    RESULTS / "recursive_samasa_capacity.json",
    RESULTS / "recursive_samasa_sample.json",
    RESULTS / "samasa_capacity_reconciliation.json",
)
GRAPH = RESULTS / "generation_stage_graph.json"


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
        elif edge.get("non_additive_capacity_edge"):
            added = f"capacity {edge['added_count']:,}"
        else:
            added = f"{edge['added_count']:+,}"
        lines.append(f"    {edge['from']} -->|\"{edge['operation']} · {added}\"| {edge['to']}")
    base_nodes = [
        node["id"] for node in graph["nodes"]
        if node.get("included_in_current_research_subtotal")
        and node["id"] != "avyaya_complete_component"
    ]
    capacity_nodes = [
        node["id"] for node in graph["nodes"]
        if node.get("count_role") in {
            "symbolic_capacity_not_lexical_subtotal",
            "virtual_input_inventory_not_lexical_subtotal",
        }
    ]
    lines.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef capacity fill:#f7f5f0,stroke:#5b4a35,stroke-dasharray:5 4,color:#221f1a;",
        f"    class {','.join(base_nodes)} base;",
        f"    class {','.join(capacity_nodes)} capacity;",
        "    class avyaya_complete_component complete;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(lines) + "\n")


def main() -> None:
    first, classification, reuse, recursive, sample, reconciliation = [json.loads(path.read_text()) for path in INPUTS]
    report = {
        "date": "2026-09-14",
        "passes_completed": 12,
        "compoundable_nominal_word_meanings": first["compoundable_nominal_word_meanings"],
        "materialized_lexical_word_meaning_subtotal": CURRENT_LEXICAL_SUBTOTAL,
        "symbolic_depth_one_compound_slots": first["symbolic_depth_one_compound_slots"],
        "symbolic_post_compound_derivational_slots": reuse["post_compound_derivational_slots"],
        "symbolic_depth_two_compound_slots": recursive["depth_two_compound_relation_slots"],
        "locally_regenerated_source_fixture_relations": first["locally_regenerated_source_fixture_relations"],
        "locally_regenerated_depth_one_samples": first["locally_regenerated_capacity_sample_relations"],
        "locally_regenerated_depth_two_samples": sample["locally_regenerated_relations"],
        "maximum_compound_depth": 2,
        "all_capacity_rows_materialized": False,
        "symbolic_counts_added_to_lexical_subtotal": False,
        "remaining_samasa_capacity_passes": 0,
        "next_stage": "तिङन्त citation forms and inflectional matrices",
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
        "publication_status": "research_capacity_only_not_deployed",
    }
    (RESULTS / "samasa_capacity_twelve_pass_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Twelve-Pass समासः Capacity Report", "",
        "| Measurement | Result |", "|---|---:|",
        f"| Canonical compoundable nominal meanings | {first['compoundable_nominal_word_meanings']:,} |",
        f"| Materialized lexical subtotal | {CURRENT_LEXICAL_SUBTOTAL:,} |",
        f"| Formal depth-one compound slots | {first['symbolic_depth_one_compound_slots']:,} |",
        f"| One of ten established operations after a depth-one compound | {reuse['post_compound_derivational_slots']:,} |",
        f"| Formal depth-two compound slots | {recursive['depth_two_compound_relation_slots']:,} |", "",
        "The first number is an inventory. The final three are capacities at declared depths. They are not added to the materialized lexical subtotal and are not claims about dictionary attestation.", "",
        "| Local verification set | Regenerated relations |", "|---|---:|",
        f"| Source fixtures | {first['locally_regenerated_source_fixture_relations']:,} |",
        f"| Depth-one capacity samples | {first['locally_regenerated_capacity_sample_relations']:,} |",
        f"| Depth-two capacity samples | {sample['locally_regenerated_relations']:,} |", "",
        "## What the Twelve Passes Establish", "",
        "1. Vidyut's compound API accepts supplied members, their relation, and a compound class; it does not discover meaningful pairs.",
        "2. The existing 113 source examples are a validation fixture. The local pinned engine now regenerates all of them and retains their rule paths.",
        "3. Four broad semantic relations can be counted over the current nominal inventory without claiming that the remaining conditioned classes are universal multipliers.",
        "4. Compound recursion changes the scale so rapidly that a complete row-by-row database is neither necessary nor informative.",
        "5. The application should store canonical meanings and relation rules, then generate requested compound branches on demand.", "",
        "The next analytical stage is तिङन्त inflection. Its grammatical cells will remain separate from lexical word-meanings and compound-capacity slots.", "",
    ]
    (RESULTS / "samasa_capacity_twelve_pass_summary.md").write_text("\n".join(lines))

    graph = json.loads(GRAPH.read_text())
    additions = [
        {
            "id": "samasa_member_inventory", "stage": 22,
            "label": "Compoundable nominal inventory",
            "reader_label": "Reconciled nominal meanings available as compound members",
            "added_count": first["compoundable_nominal_word_meanings"], "cumulative_count": None,
            "count_unit": "word_meaning_input", "form_class": "virtual_nominal_input_inventory",
            "complete_pada": False, "count_role": "virtual_input_inventory_not_lexical_subtotal",
            "included_in_current_research_subtotal": False,
        },
        {
            "id": "samasa_depth_one_capacity", "stage": 23,
            "label": "Depth-one समासः capacity",
            "reader_label": "Nominal meanings enter four broad compound relations",
            "added_count": first["symbolic_depth_one_compound_slots"], "cumulative_count": None,
            "count_unit": "formal_semantic_slot", "form_class": "virtual_derived_nominal_base",
            "complete_pada": False, "count_role": "symbolic_capacity_not_lexical_subtotal",
            "included_in_current_research_subtotal": False,
        },
        {
            "id": "post_compound_capacity", "stage": 24,
            "label": "One operation after a compound",
            "reader_label": "A compound becomes the input to one established operation",
            "added_count": reuse["post_compound_derivational_slots"], "cumulative_count": None,
            "count_unit": "formal_derivational_slot", "form_class": "virtual_mixed_derived_base",
            "complete_pada": False, "count_role": "symbolic_capacity_not_lexical_subtotal",
            "included_in_current_research_subtotal": False,
        },
        {
            "id": "samasa_depth_two_capacity", "stage": 25,
            "label": "Depth-two समासः capacity",
            "reader_label": "One compound joins one original nominal meaning",
            "added_count": recursive["depth_two_compound_relation_slots"], "cumulative_count": None,
            "count_unit": "formal_semantic_slot", "form_class": "virtual_derived_nominal_base",
            "complete_pada": False, "count_role": "symbolic_capacity_not_lexical_subtotal",
            "included_in_current_research_subtotal": False,
        },
    ]
    replaced_ids = {item["id"] for item in additions} | {"stacked_operations_pending"}
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] not in replaced_ids] + additions
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge.get("from") not in replaced_ids and edge.get("to") not in replaced_ids
    ]
    compound_edge = {
        "from": "source_samasa", "to": "compound_input_stacks",
        "operation": "one established operation over each eligible source compound",
        "added_count": 958,
    }
    if not any(
        edge.get("from") == compound_edge["from"] and edge.get("to") == compound_edge["to"]
        for edge in graph["edges"]
    ):
        graph["edges"].append(compound_edge)
    graph["edges"].extend([
        {"from": "compound_input_stacks", "to": "samasa_member_inventory", "operation": "reconcile compoundable nominal inputs", "added_count": first["compoundable_nominal_word_meanings"], "non_additive_capacity_edge": True},
        {"from": "samasa_member_inventory", "to": "samasa_depth_one_capacity", "operation": "four broad compound relations", "added_count": first["symbolic_depth_one_compound_slots"], "non_additive_capacity_edge": True},
        {"from": "samasa_depth_one_capacity", "to": "post_compound_capacity", "operation": "one established operation", "added_count": reuse["post_compound_derivational_slots"], "non_additive_capacity_edge": True},
        {"from": "samasa_depth_one_capacity", "to": "samasa_depth_two_capacity", "operation": "one compound plus one original nominal member", "added_count": recursive["depth_two_compound_relation_slots"], "non_additive_capacity_edge": True},
    ])
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    regenerate_mermaid(graph)
    print("Completed twelve samasa-capacity passes and updated the stage graph.")


if __name__ == "__main__":
    main()
