#!/usr/bin/env python3
"""Tinanta pass 4: count ten third-person singular citation coordinates."""

from __future__ import annotations

import csv
import json

from tinanta_common import CONFIG, RESULTS, read_json


def main() -> None:
    inventory = read_json(RESULTS / "tinanta_verbal_inventory.json")
    classification = read_json(RESULTS / "tinanta_lakara_classification.json")
    config = read_json(CONFIG)
    meanings = inventory["laukika_verbal_word_meanings"]
    rows = []
    for item in config["laukika_lakaras"]:
        rows.append({
            "lakara_id": item["id"], "display": item["display"],
            "plain_function": item["plain_function"],
            "verbal_word_meanings": meanings, "citation_semantic_cells": meanings,
        })
    total = sum(row["citation_semantic_cells"] for row in rows)
    with (RESULTS / "tinanta_citation_capacity.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    report = {
        "date": "2026-09-14", "verbal_word_meanings": meanings,
        "laukika_lakaras": classification["counted_laukika_lakaras"],
        "citation_coordinate": "प्रथमपुरुष-एकवचनम् (third-person singular)",
        "citation_semantic_cells": total, "surface_forms_materialized": False,
        "pada_series_multiplier_applied": False,
        "formula": "V x 10",
    }
    (RESULTS / "tinanta_citation_capacity.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 4: Citation-Form Capacity", "", f"Each of **{meanings:,}** verbal word-meanings receives one third-person singular coordinate in each of ten लौकिक लकाराः.", "", "| Calculation | Semantic grammatical cells |", "|---|---:|", f"| {meanings:,} × 10 | **{total:,}** |", "", "The result counts grammatical functions, not unique spellings. Alternative forms and the two पद series remain attached to a cell rather than multiplying it.", ""]
    (RESULTS / "tinanta_citation_capacity.md").write_text("\n".join(lines))
    print(f"Counted {total} third-person singular citation cells.")


if __name__ == "__main__":
    main()
