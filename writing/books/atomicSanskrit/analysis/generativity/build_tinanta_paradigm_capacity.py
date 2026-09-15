#!/usr/bin/env python3
"""Tinanta pass 7: expand citation coordinates to the 3 x 3 matrix."""

from __future__ import annotations

import csv
import json

from tinanta_common import CONFIG, RESULTS, read_json


def main() -> None:
    config = read_json(CONFIG)
    citation = read_json(RESULTS / "tinanta_citation_capacity.json")
    purushas = config["full_person_number_matrix"]["purushas"]
    vacanas = config["full_person_number_matrix"]["vacanas"]
    rows = []
    for purusha in purushas:
        for vacana in vacanas:
            rows.append({
                "purusha": purusha, "vacana": vacana,
                "cells_across_all_verbal_meanings_and_lakaras": citation["citation_semantic_cells"],
            })
    total = citation["citation_semantic_cells"] * len(rows)
    with (RESULTS / "tinanta_paradigm_capacity.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    report = {
        "date": "2026-09-14", "citation_semantic_cells": citation["citation_semantic_cells"],
        "person_number_cells_per_lakara": len(rows),
        "full_kartari_tinanta_semantic_cells": total,
        "formula": "V x 10 lakaras x 3 purushas x 3 vacanas",
        "pada_series_multiplier_applied": False,
        "surface_forms_materialized": False,
    }
    (RESULTS / "tinanta_paradigm_capacity.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 7: Full Person-Number Capacity", "", "Each citation coordinate expands into three पुरुषाः and three वचनानि.", "", "| Calculation | Semantic grammatical cells |", "|---|---:|", f"| {citation['citation_semantic_cells']:,} × 3 × 3 | **{total:,}** |", "", "This is the कर्तरि person-number capacity. कर्मणि and भावे प्रयोग remain separate, as does the Vaidika लेट् domain.", ""]
    (RESULTS / "tinanta_paradigm_capacity.md").write_text("\n".join(lines))
    print(f"Counted {total} full kartari tinanta cells.")


if __name__ == "__main__":
    main()
