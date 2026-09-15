#!/usr/bin/env python3
"""Pass 6: summarize the broader lexical स्त्रीप्रत्ययः round."""

from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path

from vidyut.lipi import Scheme, transliterate

from stri_generalization_common import LEDGER, RESULTS, ROOT, project_path, sha256


CLASSIFICATION = RESULTS / "stri_generalization_classification.json"
ELIGIBILITY = RESULTS / "stri_generalization_eligibility.json"
GENERATION = RESULTS / "stri_generalization_generation.json"
VERIFICATION = RESULTS / "stri_generalization_verification.json"
RECONCILIATION = RESULTS / "stri_generalization_reconciliation.json"
GRAPH = RESULTS / "generation_stage_graph.json"


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
    base_nodes = [
        node["id"] for node in graph["nodes"]
        if node.get("included_in_current_research_subtotal")
        and node["id"] != "avyaya_complete_component"
    ]
    lines.extend([
        "    classDef base fill:#eadfca,stroke:#5b4a35,color:#221f1a;",
        "    classDef complete fill:#fff,stroke:#9f6b20,stroke-width:2px,color:#221f1a;",
        "    classDef pending fill:#f7f5f0,stroke:#777,stroke-dasharray:5 4,color:#444;",
        f"    class {','.join(base_nodes)} base;",
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
    if eligibility["eligible_lexical_agent_meanings"] != generation["eligible_candidates"]:
        raise ValueError("Eligibility and generation disagree")
    if generation["engine_verified_relations"] != verification["verified_relations"]:
        raise ValueError("Generation and verification disagree")
    if generation["engine_verified_relations"] != reconciliation["generated_generalized_relations"]:
        raise ValueError("Generation and reconciliation disagree")

    wanted = {"kartf", "dAtf", "rakzitf"}
    examples = {}
    with gzip.open(LEDGER, "rt", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            for form in row["input_forms_slp1"].split(";"):
                if form in wanted and form not in examples:
                    examples[form] = row
            if len(examples) == len(wanted):
                break
    if set(examples) != wanted:
        raise ValueError(f"Missing examples: {sorted(wanted - set(examples))}")

    graph = json.loads(GRAPH.read_text())
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] != "generalized_stri"]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["from"] != "generalized_stri"
        and edge["to"] != "generalized_stri"
        and not (edge["from"] == "generalized_comparison" and edge["to"] == "compound_expansion_pending")
    ]
    graph["nodes"].append({
        "id": "generalized_stri",
        "stage": 19,
        "label": "Lexical feminine agent relations",
        "reader_label": "Agent nouns generate feminine counterparts",
        "added_count": reconciliation["additional_generalized_stri_word_meanings"],
        "cumulative_count": reconciliation["combined_bounded_word_meaning_subtotal"],
        "count_unit": "word_meaning",
        "form_class": "derived_nominal_base",
        "complete_pada": False,
        "count_role": "cumulative_subtotal",
        "included_in_current_research_subtotal": True,
    })
    graph["edges"].extend([
        {
            "from": "generalized_comparison",
            "to": "generalized_stri",
            "operation": "lexical feminine counterparts of agent nouns",
            "added_count": reconciliation["additional_generalized_stri_word_meanings"],
        },
        {
            "from": "generalized_stri",
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
        "selected_semantic_operations": classification["selected_semantic_operations"],
        "eligible_lexical_agent_meanings": eligibility["eligible_lexical_agent_meanings"],
        "engine_verified_relations": generation["engine_verified_relations"],
        "engine_exclusions": generation["engine_zero_or_no_stri_suffix_relations"],
        "confirmed_prior_overlaps": reconciliation["confirmed_existing_word_meaning_overlaps_not_added"],
        "same_spelling_cases_not_merged": reconciliation["same_spelling_cases_not_merged"],
        "additional_generalized_stri_word_meanings": reconciliation["additional_generalized_stri_word_meanings"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "remaining_passes": 24,
        "inputs": {
            project_path(path): sha256(path)
            for path in (CLASSIFICATION, ELIGIBILITY, GENERATION, VERIFICATION, RECONCILIATION, LEDGER, GRAPH, Path(__file__))
        },
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "stri_generalization_six_pass_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Six-Pass Lexical स्त्रीप्रत्ययः Expansion", "",
        "This round extends feminine derivation across nominal meanings already classified as agents. It counts the additional meaning 'female agent,' while keeping ordinary feminine agreement outside the lexical subtotal.", "",
        "| Pass | Result |", "|---:|---|",
        "| 1 | Select four agent-producing source operations and defer participles, verbal adjectives, and non-agent nominals. |",
        f"| 2 | Recover source construction metadata for {eligibility['eligible_lexical_agent_meanings']:,} eligible agent meanings. |",
        f"| 3 | Reconstruct their धातुः, कृदन्त, उपसर्गः, and सनादि paths and generate {generation['engine_verified_relations']:,} feminine relations through Vidyut 0.4.0. |",
        f"| 4 | Verify every candidate has a generated form and an inserted स्त्रीप्रत्यय; {generation['engine_zero_or_no_stri_suffix_relations']:,} remain unresolved. |",
        f"| 5 | Remove {reconciliation['confirmed_existing_word_meaning_overlaps_not_added']} confirmed earlier agent-feminine overlaps without merging {reconciliation['same_spelling_cases_not_merged']} merely homographic cases. |",
        f"| 6 | Add **{reconciliation['additional_generalized_stri_word_meanings']:,}** meanings, raising the bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,}**. |",
        "", "## Examples", "",
        "| Agent noun | Feminine counterpart | Meaning added |", "|---|---|---|",
    ]
    for form in ("kartf", "dAtf", "rakzitf"):
        row = examples[form]
        output = row["generated_forms_slp1"].split(";")[0]
        lines.append(
            f"| {deva(form)} (*{iast(form)}*) | {deva(output)} (*{iast(output)}*) | female agent performing the source action |"
        )
    lines.extend([
        "", "## Boundary", "",
        "The count does not multiply grammatical gender across every noun or adjective. It uses only source meanings already classified as agents and reconstructs the grammatical operation that produced each one. Feminine participles and obligation forms remain for the later inflectional analysis.", "",
        "The result remains a research subtotal. It has not changed the manuscript, companion, covers, or published endnotes.", "",
    ])
    (RESULTS / "stri_generalization_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six broader stri passes complete; subtotal {report['combined_bounded_word_meaning_subtotal']:,}.")


if __name__ == "__main__":
    main()
