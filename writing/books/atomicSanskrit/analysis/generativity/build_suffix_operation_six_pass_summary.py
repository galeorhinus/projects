#!/usr/bin/env python3
"""Build the six-pass suffix-operation report and update reporting artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from vidyut.lipi import Scheme, transliterate

from taddhita_conditioned_common import HERE, RESULTS, sha256


INPUTS = (
    RESULTS / "suffix_semantic_families.json",
    RESULTS / "suffix_productivity_classification.json",
    RESULTS / "suffix_conditioned_relations.json",
    RESULTS / "suffix_conditioned_verification.json",
    RESULTS / "suffix_conditioned_reconciliation.json",
)
LEDGER = RESULTS / "suffix_conditioned_ledger.csv"
GRAPH = RESULTS / "generation_stage_graph.json"


def deva(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Devanagari)


def iast(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Iast)


def main() -> None:
    families, productivity, relations, verification, reconciliation = [json.loads(path.read_text()) for path in INPUTS]
    if relations["eligible_relations"] != verification["candidate_relations"]:
        raise ValueError("Eligibility and verification counts disagree")
    if verification["verified_relations"] != reconciliation["additional_suffix_word_meanings"] + reconciliation["existing_relation_overlaps_not_added"]:
        raise ValueError("Verified relations do not reconcile")
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    selected_keys = {
        ("agnIzoma", "Ca"), ("agnIzoma", "yat"), ("tila", "yat"),
        ("tila", "KaY"), ("tAvat", "kan"),
    }
    selected = {(row["input_form_slp1"], row["taddhita_source_variant"]): row for row in rows if (row["input_form_slp1"], row["taddhita_source_variant"]) in selected_keys}
    if set(selected) != selected_keys:
        raise ValueError(f"Missing examples: {selected_keys - set(selected)}")

    graph = json.loads(GRAPH.read_text())
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] != "additional_suffix_relations"]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["from"] != "additional_suffix_relations" and edge["to"] != "additional_suffix_relations"
        and not (edge["from"] == "nan_privative" and edge["to"] == "compound_expansion_pending")
    ]
    graph["nodes"].append({
        "id": "additional_suffix_relations",
        "stage": 16,
        "label": "Additional source-conditioned तद्धित relations",
        "reader_label": "Named relations hidden inside source helpers add further noun-derived meanings",
        "added_count": reconciliation["additional_suffix_word_meanings"],
        "cumulative_count": reconciliation["combined_bounded_word_meaning_subtotal"],
        "count_unit": "word_meaning",
        "form_class": "derived_nominal_base",
        "complete_pada": False,
        "count_role": "cumulative_subtotal",
        "included_in_current_research_subtotal": True,
    })
    graph["edges"].extend([
        {
            "from": "nan_privative", "to": "additional_suffix_relations",
            "operation": "additional source-conditioned suffix relations",
            "added_count": reconciliation["additional_suffix_word_meanings"],
        },
        {
            "from": "additional_suffix_relations", "to": "compound_expansion_pending",
            "operation": "other bounded compounds", "added_count": None,
        },
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
        "    class dhatu_meanings,one_sanadi,one_upasarga,upasarga_sanadi,curadi_causative,two_upasarga,first_krdanta,wider_krdanta,laukika_domain_correction,vaidika_layer,broad_taddhita,conditioned_taddhita,stri,namadhatu,nan_privative,additional_suffix_relations base;",
        "    class avyaya_complete_component complete;",
        "    class compound_expansion_pending pending;",
        "    class tinanta_expansion_pending,subanta_expansion_pending complete;",
    ])
    (RESULTS / "generation_stage_graph.mmd").write_text("\n".join(mermaid) + "\n")

    report = {
        "date": "2026-09-13",
        "passes_completed": 6,
        "suffix_identifiers_classified": families["suffix_identifiers"],
        "broad_suffix_identifiers": len(productivity["broad_multipliers"]),
        "plain_source_forms_not_counted_as_new_meanings": productivity["plain_source_assertions_outside_count"],
        "new_source_conditioned_candidates": relations["eligible_relations"],
        "verified_relations": verification["verified_relations"],
        "additional_suffix_word_meanings": reconciliation["additional_suffix_word_meanings"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "stage_graph_nodes": len(graph["nodes"]),
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (*INPUTS, LEDGER, GRAPH, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "suffix_operation_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    meanings = {
        "devata_relation": "having the named form as its देवता (*devatā*)",
        "crop_field_relation": "a field in which the named crop grows",
        "purchase_measure_relation": "bought for the named measure or amount",
    }
    lines = [
        "# Six-Pass Suffix-Operation Expansion", "",
        "The letters at the end of a finished word do not identify the operation that formed it. This pass therefore follows each semantic relation from its source condition through its grammatical suffix to the generated form.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | Group all {families['suffix_identifiers']} pinned तद्धित identifiers by the semantic work their rules perform. |",
        f"| 2 | Separate {len(productivity['broad_multipliers'])} already admitted broad operations from conditioned, same-meaning, structural, and unreached suffixes. |",
        f"| 3 | Recover {relations['eligible_relations']} additional meaning-conditioned relations hidden inside local source helpers or constructed inputs. |",
        f"| 4 | Vidyut 0.4.0 reproduces {verification['verified_relations']} of those {verification['candidate_relations']} relations; {verification['relations_with_partial_variant_coverage']} retain incomplete optional-variant coverage. |",
        f"| 5 | Reconcile them against the broad and earlier conditioned ledgers; {reconciliation['additional_suffix_word_meanings']} remain new. |",
        f"| 6 | Add those meanings to reach a combined bounded subtotal of **{reconciliation['combined_bounded_word_meaning_subtotal']:,} word-meanings**. |", "",
        "## What -क and -य Can Hide", "",
        "| Input | Suffix | Output | Meaning |", "|---|---|---|---|",
    ]
    for key in [("agnIzoma", "Ca"), ("agnIzoma", "yat"), ("tila", "yat"), ("tila", "KaY"), ("tAvat", "kan")]:
        row = selected[key]
        outputs = ", ".join(f"{deva(form)} (*{iast(form)}*)" for form in row["expected_output_forms_slp1"].split(";"))
        lines.append(
            f"| {deva(row['input_form_slp1'])} (*{iast(row['input_form_slp1'])}*) | "
            f"{row['taddhita_source_variant']} | {outputs} | {meanings[row['family_id']]} |"
        )
    lines.extend([
        "", "The first two rows express the same relation through different suffixes and therefore produce different words. The two sesame-field forms do the same. In the final row Vidyut reproduces तावत्क (*tāvatka*) but not the optional तावतिक (*tāvatika*) through its generic constructor. The semantic relation still counts once; optional output forms do not multiply it.", "",
        "## Boundary", "",
        f"The pass leaves **{productivity['plain_source_assertions_outside_count']} plain source-recorded forms** outside the word-meaning subtotal. They demonstrate further derivational capacity, but their assertions do not state a distinct meaning. A later pass may admit them only after recovering that semantic condition from the governing rule; spelling alone will not do it.", "",
    ])
    (RESULTS / "suffix_operation_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six suffix-operation passes complete; combined bounded subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
