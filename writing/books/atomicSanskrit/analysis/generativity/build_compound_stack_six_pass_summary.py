#!/usr/bin/env python3
"""Pass 6: report the compound-input stacks and extend the stage graph."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from vidyut.lipi import Scheme, transliterate

from compound_stack_common import RESULTS, project_path, read_json, sha256


CLASSIFICATION = RESULTS / "compound_stack_classification.json"
ELIGIBILITY = RESULTS / "compound_stack_eligibility.json"
GENERATION = RESULTS / "compound_stack_generation.json"
VERIFICATION = RESULTS / "compound_stack_verification.json"
RECONCILIATION = RESULTS / "compound_stack_reconciliation.json"
LEDGER = RESULTS / "compound_stack_ledger.csv"
GRAPH = RESULTS / "generation_stage_graph.json"


def display(text: str) -> str:
    deva = transliterate(text, Scheme.Slp1, Scheme.Devanagari)
    iast = transliterate(text, Scheme.Slp1, Scheme.Iast)
    return f"{deva} (*{iast}*)"


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
    base_nodes = [
        node["id"] for node in graph["nodes"]
        if node.get("included_in_current_research_subtotal")
        and node["id"] != "avyaya_complete_component"
    ]
    lines.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        f"    class {','.join(base_nodes)} base;",
        "    class avyaya_complete_component complete;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(lines) + "\n")


def main() -> None:
    classification, eligibility, generation, verification, reconciliation = [
        read_json(path) for path in (CLASSIFICATION, ELIGIBILITY, GENERATION, VERIFICATION, RECONCILIATION)
    ]
    if not (
        eligibility["eligible_relations"]
        == generation["generated_candidate_relations"]
        == verification["verified_relations"]
        == reconciliation["additional_compound_stack_word_meanings"]
    ):
        raise ValueError("The six compound-stack passes do not reconcile")

    graph = read_json(GRAPH)
    graph["nodes"] = [
        node for node in graph["nodes"]
        if node["id"] not in {"stacked_operations_pending", "compound_input_stacks"}
    ]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["from"] not in {"stacked_operations_pending", "compound_input_stacks"}
        and edge["to"] not in {"stacked_operations_pending", "compound_input_stacks"}
    ]
    graph["nodes"].append({
        "id": "compound_input_stacks",
        "stage": 21,
        "label": "One further operation over source compounds",
        "reader_label": "A compound becomes the input to another word-forming operation",
        "added_count": reconciliation["additional_compound_stack_word_meanings"],
        "cumulative_count": reconciliation["combined_bounded_word_meaning_subtotal"],
        "count_unit": "word_meaning",
        "form_class": "mixed_derived_base_inventory",
        "complete_pada": False,
        "count_role": "cumulative_subtotal",
        "included_in_current_research_subtotal": True,
        "derived_nominal_bases": reconciliation["additional_by_output_form_class"]["derived_nominal_base"],
        "derived_verbal_bases": reconciliation["additional_by_output_form_class"]["derived_verbal_base"],
    })
    graph["edges"].extend([
        {
            "from": "source_samasa",
            "to": "compound_input_stacks",
            "operation": "one established operation over each eligible source compound",
            "added_count": reconciliation["additional_compound_stack_word_meanings"],
        },
        {
            "from": "compound_input_stacks",
            "to": "tinanta_expansion_pending",
            "operation": "conjugation of derived verbal meanings",
            "added_count": None,
        },
        {
            "from": "compound_input_stacks",
            "to": "subanta_expansion_pending",
            "operation": "declension of derived nominal meanings",
            "added_count": None,
        },
    ])
    graph["date"] = "2026-09-14"
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    regenerate_mermaid(graph)

    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    wanted = {
        ("mahApuruza", "state_tva"),
        ("mahApuruza", "possession_matup"),
        ("mahApuruza", "nan_privative"),
        ("rAjapuruza", "self_desire_kyac"),
        ("rAjapuruza", "object_comparison_kyac"),
    }
    examples = [
        row for row in rows
        if any(form in {key[0] for key in wanted if key[1] == row["operation_id"]} for form in row["input_forms_slp1"].split(";"))
    ]
    report = {
        "date": "2026-09-14",
        "passes_completed": 6,
        "source_compound_word_meanings": classification["source_compound_word_meanings"],
        "eligible_nominal_compounds": classification["derived_nominal_bases"],
        "complete_indeclinables_not_reopened": classification["complete_avyayibhava_indeclinables"],
        "eligible_operation_relations": eligibility["eligible_relations"],
        "verified_relations": verification["verified_relations"],
        "additional_compound_stack_word_meanings": reconciliation["additional_compound_stack_word_meanings"],
        "additional_by_operation_family": reconciliation["additional_by_operation_family"],
        "additional_by_output_form_class": reconciliation["additional_by_output_form_class"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "remaining_passes": 12,
        "inputs": {project_path(path): sha256(path) for path in (
            CLASSIFICATION, ELIGIBILITY, GENERATION, VERIFICATION, RECONCILIATION,
            LEDGER, GRAPH, Path(__file__),
        )},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "compound_stack_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Six-Pass Compound-Input Operation Stack", "",
        "This block asks what happens when a source-demonstrated compound becomes the input to one more established word-forming operation.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | Classify {classification['derived_nominal_bases']} nominal compound meanings and retain {classification['complete_avyayibhava_indeclinables']} अव्ययीभाव indeclinables as complete words. |",
        f"| 2 | Declare {eligibility['eligible_relations']} depth-two relations under ten already established operations; recursive नञ् remains excluded. |",
        f"| 3 | Generate all {generation['generated_candidate_relations']} candidates: {generation['engine_verified_relations']} through Vidyut and {generation['classified_nan_surface_relations']} through the source-tested नञ् rules. |",
        f"| 4 | Reproduce all {verification['verified_relations']} output sets in a separate verification pass. |",
        f"| 5 | Confirm that none of the source-compound inputs occurred in the earlier broad nominal inventory; preserve {reconciliation['same_spelling_output_groups_not_merged']} repeated-spelling groups as separate meanings where their operations differ. |",
        f"| 6 | Add **{reconciliation['additional_compound_stack_word_meanings']} word-meanings**, raising the bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,}**. |",
        "", "## Examples", "", "| Compound input | Further result | Operation |", "|---|---|---|",
    ]
    for row in examples:
        inputs = ", ".join(display(form) for form in row["input_forms_slp1"].split(";"))
        outputs = ", ".join(display(form) for form in row["output_forms_slp1"].split(";"))
        lines.append(f"| {inputs} | {outputs} | {row['semantic_relation']} |")
    lines.extend([
        "", "## Boundary", "",
        "The block adds exactly one operation after a source-demonstrated nominal compound and stops at derivational depth two. It does not reopen complete अव्ययीभाव compounds, apply नञ् recursively, generate new compounds from these outputs, or infer arbitrary operation sequences. Finite conjugation and nominal declension remain separate.", "",
        "The result remains a research subtotal. It has not changed the manuscript, companion, covers, or published endnotes.", "",
    ])
    (RESULTS / "compound_stack_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six compound-stack passes complete; subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
