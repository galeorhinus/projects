#!/usr/bin/env python3
"""Synthesis pass 1: reconcile the complete declared laukika capacity."""

from __future__ import annotations

from capacity_synthesis_common import DATE, RESULTS, project_path, read_json, sha256, write_json


INPUTS = (
    RESULTS / "wordspace_category_graph.json",
    RESULTS / "tinanta_twelve_pass_summary.json",
    RESULTS / "subanta_twelve_pass_summary.json",
)


def main() -> None:
    wordspace, verbs, names = [read_json(path) for path in INPUTS]
    nodes = {node["id"]: node["count"] for node in wordspace["nodes"]}

    action_meanings = verbs["laukika_verbal_word_meanings"]
    name_meanings = names["laukika_name_word_meanings"]
    unchanging = names["laukika_complete_unchanging_word_meanings"]
    action_cells = verbs["full_kartari_person_number_cells"]
    name_cells = names["full_relation_number_semantic_cells"]
    total = action_cells + name_cells + unchanging

    if action_meanings + name_meanings + unchanging != nodes["ordinary_word_meanings"]:
        raise ValueError("The laukika lexical partition does not reconcile")
    if action_cells != action_meanings * 10 * 3 * 3:
        raise ValueError("The action-form matrix does not reconcile")
    if name_cells != name_meanings * 8 * 3:
        raise ValueError("The name-form matrix does not reconcile")

    report = {
        "date": DATE,
        "pass": 1,
        "count_unit": "semantic_grammatical_cell",
        "laukika_lexical_word_meanings": nodes["ordinary_word_meanings"],
        "action_word_meanings": action_meanings,
        "action_cells_per_meaning": 90,
        "action_grammatical_cells": action_cells,
        "name_word_meanings": name_meanings,
        "name_cells_per_meaning": 24,
        "name_grammatical_cells": name_cells,
        "complete_unchanging_word_meanings": unchanging,
        "unchanging_cells_per_meaning": 1,
        "integrated_laukika_grammatical_cells": total,
        "lexical_subtotal_added_to_capacity": False,
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
    }
    write_json(RESULTS / "integrated_grammatical_capacity.json", report)

    lines = [
        "# Synthesis Pass 1: Integrated Laukika Capacity", "",
        "| Meaning class | Lexical meanings | Cells per meaning | Grammatical cells |", "|---|---:|---:|---:|",
        f"| क्रियार्थाः (*kriyārthāḥ*), action and process meanings | {action_meanings:,} | 10 × 3 × 3 | {action_cells:,} |",
        f"| नामार्थाः (*nāmārthāḥ*), names, objects, qualities, states, and relations | {name_meanings:,} | 8 × 3 | {name_cells:,} |",
        f"| अव्ययानि (*avyayāni*), complete words whose forms do not change | {unchanging:,} | 1 | {unchanging:,} |",
        f"| **Complete declared लौकिक capacity** | **{nodes['ordinary_word_meanings']:,}** | — | **{total:,}** |", "",
        f"The exact reconciliation is **{action_cells:,} + {name_cells:,} + {unchanging:,} = {total:,}**. The result counts semantic grammatical cells. It replaces each लौकिक lexical meaning with its declared grammatical matrix; it does not add the {nodes['ordinary_word_meanings']:,} lexical inputs again.", "",
    ]
    (RESULTS / "integrated_grammatical_capacity.md").write_text("\n".join(lines))
    print(f"Reconciled {total:,} laukika grammatical cells.")


if __name__ == "__main__":
    main()
