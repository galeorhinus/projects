#!/usr/bin/env python3
"""Pass 6: reconcile and present the bounded compound block."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path

from vidyut.lipi import Scheme, transliterate

from samasa_common import RESULTS, project_path, sha256


INPUTS = (
    RESULTS / "samasa_type_inventory.json",
    RESULTS / "samasa_source_examples.json",
    RESULTS / "samasa_eligibility.json",
    RESULTS / "samasa_verification.json",
    RESULTS / "samasa_reconciliation.json",
)
LEDGER = RESULTS / "samasa_ledger.csv"
GRAPH = RESULTS / "generation_stage_graph.json"


def deva(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Devanagari)


def iast(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Iast)


def display(text: str) -> str:
    return f"{deva(text)} (*{iast(text)}*)"


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
    pending_nodes = [
        node["id"] for node in graph["nodes"]
        if node.get("count_role") == "future_addition"
        and not node.get("complete_pada")
    ]
    lines.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef pending fill:#f7f5f0,stroke:#777,stroke-dasharray:5 4,color:#444;",
        f"    class {','.join(base_nodes)} base;",
        "    class avyaya_complete_component complete;",
        f"    class {','.join(pending_nodes)} pending;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(lines) + "\n")


def main() -> None:
    inventory, source, eligibility, verification, reconciliation = [json.loads(path.read_text()) for path in INPUTS]
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != reconciliation["additional_samasa_word_meanings"]:
        raise ValueError("Ledger and reconciliation counts disagree")
    type_counts = Counter(row["compound_type"] for row in rows)
    examples = []
    wanted = ("rAjapuruza", "mahApuruza", "plakzanyagroDa", "vAktvaca", "grAmagata")
    example_meanings = {
        "rAjapuruza": "the king's man",
        "mahApuruza": "a great person",
        "plakzanyagroDa": "plakṣa and banyan together",
        "vAktvaca": "speech and skin taken as a collection",
        "grAmagata": "gone to the village",
    }
    for form in wanted:
        match = next((row for row in rows if form in row["output_forms_slp1"].split(";")), None)
        if match:
            examples.append(match)

    graph = json.loads(GRAPH.read_text())
    graph["nodes"] = [
        node for node in graph["nodes"]
        if node["id"] not in {"compound_expansion_pending", "source_samasa", "stacked_operations_pending"}
    ]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["from"] not in {"compound_expansion_pending", "source_samasa", "stacked_operations_pending"}
        and edge["to"] not in {"compound_expansion_pending", "source_samasa", "stacked_operations_pending"}
    ]
    graph["nodes"].extend([
        {
            "id": "source_samasa",
            "stage": 20,
            "label": "Source-demonstrated bounded समास relations",
            "reader_label": "Named relations combine words into compounds",
            "added_count": reconciliation["additional_samasa_word_meanings"],
            "cumulative_count": reconciliation["combined_bounded_word_meaning_subtotal"],
            "count_unit": "word_meaning",
            "form_class": "derived_nominal_base",
            "complete_pada": False,
            "count_role": "cumulative_subtotal",
            "included_in_current_research_subtotal": True,
        },
        {
            "id": "stacked_operations_pending",
            "stage": None,
            "label": "Further bounded operation stacks",
            "reader_label": "Completed operations become inputs to later operations",
            "added_count": None,
            "cumulative_count": None,
            "count_unit": "word_meaning",
            "form_class": "derived_base",
            "complete_pada": False,
            "count_role": "future_addition",
            "included_in_current_research_subtotal": False,
        },
    ])
    graph["edges"].extend([
        {
            "from": "generalized_stri",
            "to": "source_samasa",
            "operation": "source-demonstrated compound relations",
            "added_count": reconciliation["additional_samasa_word_meanings"],
        },
        {
            "from": "source_samasa",
            "to": "stacked_operations_pending",
            "operation": "further bounded operation stacks",
            "added_count": None,
        },
        {
            "from": "stacked_operations_pending",
            "to": "subanta_expansion_pending",
            "operation": "declension",
            "added_count": None,
        },
    ])
    graph["date"] = "2026-09-14"
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    regenerate_mermaid(graph)

    report = {
        "date": "2026-09-14",
        "passes_completed": 6,
        "implemented_compound_types": inventory["implemented_type_count"],
        "source_assertions": source["source_assertions"],
        "active_source_assertions": source["active_assertions"],
        "unique_eligible_relations": eligibility["unique_eligible_relations"],
        "relations_asserted_by_pinned_active_tests": verification["relations_asserted_by_pinned_active_tests"],
        "locally_regenerated_relations": verification["locally_regenerated_relations"],
        "additional_samasa_word_meanings": reconciliation["additional_samasa_word_meanings"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "remaining_passes": 18,
        "counts_by_compound_type": dict(sorted(type_counts.items())),
        "maximum_member_count": eligibility["maximum_member_count"],
        "maximum_derivational_depth": eligibility["maximum_derivational_depth"],
        "inputs": {project_path(path): sha256(path) for path in (*INPUTS, LEDGER, GRAPH, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "samasa_six_pass_summary.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = [
        "# Six-Pass Bounded समासः (*samāsaḥ*) Expansion", "",
        "This block counts directly reconstructible compounds in the pinned Kāśikā regression sources. It does not treat compounding as a finite universal multiplier.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | Inventory all {inventory['implemented_type_count']} compound types exposed by pinned Vidyut 0.4.0. |",
        f"| 2 | Extract {source['source_assertions']} assertions: {source['active_assertions']} active and {source['ignored_assertions']} ignored. |",
        f"| 3 | Admit {eligibility['unique_eligible_relations']} unique, directly reconstructible source relations at depth one; collapse {eligibility['duplicate_assertions_collapsed']} repeated assertions. |",
        f"| 4 | Confirm all {verification['relations_asserted_by_pinned_active_tests']} relations as literal active assertions in the pinned engine suite and locally regenerate {verification['locally_regenerated_relations']} of them. |",
        f"| 5 | Add {reconciliation['additional_samasa_word_meanings']} compound word-meanings without collapsing different meanings by spelling. |",
        f"| 6 | Raise the combined bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,} word-meanings**. |", "",
        "## Examples", "", "| Members | Result | Relation |", "|---|---|---|",
    ]
    for row in examples:
        members = " + ".join(display(x) for x in row["member_forms_slp1"].split(";"))
        outputs = ", ".join(display(x) for x in row["output_forms_slp1"].split(";"))
        output = row["output_forms_slp1"].split(";")[0]
        lines.append(f"| {members} | {outputs} | {example_meanings[output]} |")
    lines.extend([
        "", "## Boundary", "",
        "A source example proves one compound relation; it does not license every pair of nominal meanings. Recursive compounds, unrestricted pairwise combination, source examples with constructed members, and broad semantic generalization remain outside this subtotal. The Rust compound API is not exposed in Vidyut 0.4.0's Python binding. The included pinned Rust verifier regenerated the admitted examples locally and retained their rule paths.", "",
    ])
    (RESULTS / "samasa_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six bounded samasa passes complete; subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
