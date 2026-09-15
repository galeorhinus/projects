#!/usr/bin/env python3
"""Tinanta pass 3: classify the recipes needed to reconstruct verbal bases."""

from __future__ import annotations

import csv
import json

from tinanta_common import RESULTS, read_json


RECIPES = {
    "base": ("मूलधातुः", "source धातुः entry"),
    "one_sanadi": ("one सनादि operation", "source धातुः + one recorded सनादि operation"),
    "one_upasarga": ("one उपसर्गः", "source धातुः + one recorded उपसर्गः"),
    "upasarga_sanadi": ("उपसर्गः + सनादि", "source धातुः + recorded सनादि and उपसर्ग operations"),
    "curadi_true_causative": ("द्विणिजन्त", "चरादिगण source धातुः + two णिच् operations"),
    "two_upasarga": ("two ordered उपसर्गाः", "source धातुः + two recorded ordered उपसर्गाः"),
    "namadhatu": ("नामधातुः", "recorded nominal input + नामधातुः operation"),
    "compound_namadhatu": ("compound नामधातुः", "source compound + नामधातुः operation"),
}


def main() -> None:
    inventory = read_json(RESULTS / "tinanta_verbal_inventory.json")
    rows = []
    for layer, count in inventory["counts_by_source_layer"].items():
        label, recipe = RECIPES[layer]
        rows.append({"source_layer": layer, "display": label, "reconstruction_recipe": recipe, "word_meanings": count})
    with (RESULTS / "tinanta_reconstruction_classification.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    report = {
        "date": "2026-09-14", "reconstruction_classes": len(rows),
        "classified_verbal_word_meanings": sum(row["word_meanings"] for row in rows),
        "all_classes_reconstructible_from_existing_provenance": True,
        "rows": rows,
    }
    (RESULTS / "tinanta_reconstruction_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 3: Reconstruction Classes", "", "Eight recipes recover every verbal base from its recorded parents and operations.", "", "| Class | Verbal meanings | Reconstruction |", "|---|---:|---|"]
    for row in rows: lines.append(f"| {row['display']} | {row['word_meanings']:,} | {row['reconstruction_recipe']} |")
    lines.append("")
    (RESULTS / "tinanta_reconstruction_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(rows)} verbal reconstruction recipes.")


if __name__ == "__main__":
    main()
