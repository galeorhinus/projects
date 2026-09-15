#!/usr/bin/env python3
"""Subanta pass 1: reconcile the current lexical subtotal by broad word class."""

from __future__ import annotations

import json

from subanta_common import CURRENT_LEXICAL_SUBTOTAL, RESULTS, project_path, read_json, sha256


INPUT_NAMES = (
    "nominal_input_inventory_summary.json", "taddhita_pilot_summary.json",
    "taddhita_reconciliation.json", "conditioned_taddhita_reconciliation.json",
    "stri_reconciliation.json", "nan_reconciliation.json",
    "suffix_conditioned_reconciliation.json", "plain_taddhita_reconciliation.json",
    "taddhita_generalization_reconciliation.json", "stri_generalization_reconciliation.json",
    "compound_stack_classification.json", "compound_stack_reconciliation.json",
    "domain_boundary_audit.json", "vaidika_laukika_reconciliation.json",
    "tinanta_verbal_inventory.json",
)


def main() -> None:
    data = {name: read_json(RESULTS / name) for name in INPUT_NAMES}
    first = data["nominal_input_inventory_summary.json"]
    initial_generated_nominals = sum(
        count for layer, count in first["admitted_by_layer"].items()
        if layer != "declared_pilot_nominal"
    )
    nominal_layers = {
        "initial_laukika_derived_nominals": initial_generated_nominals,
        "bounded_taddhita_pilot_outputs": data["taddhita_pilot_summary.json"]["admitted_taddhita_word_meanings"],
        "additional_broad_taddhita": data["taddhita_reconciliation.json"]["additional_taddhita_word_meanings"],
        "conditioned_taddhita": data["conditioned_taddhita_reconciliation.json"]["additional_conditioned_taddhita_word_meanings"],
        "source_demonstrated_feminines": data["stri_reconciliation.json"]["additional_stri_word_meanings"],
        "negative_counterparts": data["nan_reconciliation.json"]["additional_nan_word_meanings"],
        "conditioned_suffix_relations": data["suffix_conditioned_reconciliation.json"]["additional_suffix_word_meanings"],
        "plain_taddhita_nominals": data["plain_taddhita_reconciliation.json"]["additional_nominal_bases"],
        "comparatives_and_superlatives": data["taddhita_generalization_reconciliation.json"]["additional_generalized_word_meanings"],
        "lexical_feminine_agents": data["stri_generalization_reconciliation.json"]["additional_generalized_stri_word_meanings"],
        "source_compound_nominals": data["compound_stack_classification.json"]["derived_nominal_bases"],
        "post_compound_nominals": data["compound_stack_reconciliation.json"]["additional_by_output_form_class"]["derived_nominal_base"],
    }
    nominal_total = sum(nominal_layers.values())
    restricted_avyaya = next(
        row["known_vedic_restricted_rows"]
        for row in data["domain_boundary_audit.json"]["layers"] if row["layer"] == "avyaya"
    )
    initial_avyaya = next(
        row["total_rows"] for row in data["domain_boundary_audit.json"]["layers"] if row["layer"] == "avyaya"
    ) - restricted_avyaya
    unchanging_layers = {
        "initial_laukika_avyayas": initial_avyaya,
        "plain_taddhita_avyayas": data["plain_taddhita_reconciliation.json"]["additional_complete_avyayas"],
        "source_compound_avyayibhavas": data["compound_stack_classification.json"]["complete_avyayibhava_indeclinables"],
    }
    unchanging_total = sum(unchanging_layers.values())
    vaidika_total = data["vaidika_laukika_reconciliation.json"]["bounded_vaidika_subtotal"]
    ordinary_total = CURRENT_LEXICAL_SUBTOTAL - vaidika_total
    verbal_total = data["tinanta_verbal_inventory.json"]["laukika_verbal_word_meanings"]
    if ordinary_total != verbal_total + nominal_total + unchanging_total:
        raise ValueError("The ordinary-domain word classes do not reconcile")
    previous_nominal_view = read_json(RESULTS / "samasa_capacity_member_inventory.json")["compoundable_nominal_word_meanings"]
    report = {
        "date": "2026-09-14", "passes_completed": 1,
        "combined_lexical_word_meanings": CURRENT_LEXICAL_SUBTOTAL,
        "vaidika_word_meanings": vaidika_total,
        "laukika_word_meanings": ordinary_total,
        "laukika_action_meanings": verbal_total,
        "laukika_name_meanings": nominal_total,
        "laukika_unchanging_meanings": unchanging_total,
        "nominal_counts_by_source_layer": nominal_layers,
        "unchanging_counts_by_source_layer": unchanging_layers,
        "previous_compound_member_view": previous_nominal_view,
        "difference_from_previous_compound_member_view": nominal_total - previous_nominal_view,
        "former_unresolved_reader_graph_residual": ordinary_total - verbal_total - previous_nominal_view,
        "unresolved_reader_graph_residual_after_reconciliation": 0,
        "inputs": {project_path(RESULTS / name): sha256(RESULTS / name) for name in INPUT_NAMES},
        "publication_status": "research_partition_not_deployed",
    }
    (RESULTS / "subanta_word_class_reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 1: Lexical-Class Reconciliation", "",
        "| Current class | Word-meanings |", "|---|---:|",
        f"| वैदिक domain | {vaidika_total:,} |",
        f"| लौकिक action and process meanings | {verbal_total:,} |",
        f"| लौकिक name, object, quality, state, and relation meanings | {nominal_total:,} |",
        f"| लौकिक complete unchanging meanings | {unchanging_total:,} |",
        f"| **Combined lexical subtotal** | **{CURRENT_LEXICAL_SUBTOTAL:,}** |", "",
        f"The earlier compound-member view counted {previous_nominal_view:,} possible nominal members. It was built for compounding, not as a complete lexical-class partition. Reconstructing every added stage raises the current declinable name-meaning inventory by **{nominal_total - previous_nominal_view:,}** and resolves the former **{report['former_unresolved_reader_graph_residual']:,}** reader-graph remainder.", "",
    ]
    (RESULTS / "subanta_word_class_reconciliation.md").write_text("\n".join(lines))
    print(f"Reconciled {nominal_total:,} name meanings and {unchanging_total:,} complete unchanging meanings.")


if __name__ == "__main__":
    main()
