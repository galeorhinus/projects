#!/usr/bin/env python3
"""Synthesis pass 2: keep the Vaidika inventory outside laukika inflection."""

from __future__ import annotations

from capacity_synthesis_common import DATE, RESULTS, project_path, read_json, sha256, write_json


INPUTS = (
    RESULTS / "wordspace_category_graph.json",
    RESULTS / "integrated_grammatical_capacity.json",
)


def main() -> None:
    wordspace, integrated = [read_json(path) for path in INPUTS]
    nodes = {node["id"]: node["count"] for node in wordspace["nodes"]}
    vaidika = nodes["vedic_word_meanings"]
    laukika = nodes["ordinary_word_meanings"]
    lexical_total = nodes["all_word_meanings"]
    if vaidika + laukika != lexical_total:
        raise ValueError("The Vaidika-laukika lexical partition does not reconcile")

    report = {
        "date": DATE,
        "pass": 2,
        "bounded_lexical_word_meanings": lexical_total,
        "vaidika_lexical_word_meanings": vaidika,
        "laukika_lexical_word_meanings": laukika,
        "laukika_grammatical_cells": integrated["integrated_laukika_grammatical_cells"],
        "vaidika_inflection_modeled": False,
        "mixed_unit_grand_total_published": False,
        "reason": "The Vaidika number counts lexical meanings, while the laukika number counts grammatical cells. Adding them would mix units.",
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
    }
    write_json(RESULTS / "vaidika_capacity_boundary.json", report)
    lines = [
        "# Synthesis Pass 2: Vaidika Boundary", "",
        f"The bounded lexical inventory contains **{lexical_total:,} word-meanings**: **{laukika:,} लौकिक** and **{vaidika:,} वैदिक**.", "",
        f"Only the लौकिक partition enters the present grammatical expansion, producing **{report['laukika_grammatical_cells']:,} semantic grammatical cells**. The {vaidika:,} Vedic meanings remain a separate lexical inventory until a Vedic inflection model has been declared and tested.", "",
        "No combined grand total is reported. Adding the Vedic lexical count to the लौकिक grammatical-cell count would mix two different units.", "",
    ]
    (RESULTS / "vaidika_capacity_boundary.md").write_text("\n".join(lines))
    print("Separated the Vaidika lexical inventory from laukika grammatical capacity.")


if __name__ == "__main__":
    main()
