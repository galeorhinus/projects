#!/usr/bin/env python3
"""Subanta pass 3: classify the eight relation and three number coordinates."""

from __future__ import annotations

import csv
import importlib.metadata
import json

from vidyut.prakriya import Vacana, Vibhakti

from subanta_common import ARCHIVE, CONFIG, RESULTS, project_path, read_json, sha256


FIELDS = ("axis", "id", "vidyut", "display", "plain_function", "principal_rule_refs")


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This classification requires Vidyut 0.4.0")
    config = read_json(CONFIG)
    engine_relations = {item.name for item in Vibhakti.choices()}
    engine_numbers = {item.name for item in Vacana.choices()}
    configured_relations = {item["vidyut"] for item in config["relations"]}
    configured_numbers = {item["vidyut"] for item in config["numbers"]}
    if configured_relations != engine_relations or configured_numbers != engine_numbers:
        raise ValueError("Configured relation-number coordinates do not match the pinned engine")
    rule_path = ARCHIVE / "sutrapatha.tsv"
    required_rules = set(config["principal_inventory_rule_refs"])
    for item in config["relations"]:
        required_rules.update(item["principal_rule_refs"])
    with rule_path.open(newline="", encoding="utf-8") as handle:
        available = {row["code"] for row in csv.DictReader(handle, delimiter="\t")}
    if missing := required_rules - available:
        raise ValueError(f"Missing primary rule records: {sorted(missing)}")
    rows = []
    for axis in ("relations", "numbers"):
        for item in config[axis]:
            rows.append({
                "axis": axis[:-1], "id": item["id"], "vidyut": item["vidyut"],
                "display": item["display"], "plain_function": item["plain_function"],
                "principal_rule_refs": ";".join(item.get("principal_rule_refs", [])),
            })
    with (RESULTS / "subanta_coordinate_classification.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    report = {
        "date": "2026-09-14", "passes_completed": 3,
        "engine_relation_coordinates": len(engine_relations),
        "engine_number_coordinates": len(engine_numbers),
        "cells_per_name_meaning": len(engine_relations) * len(engine_numbers),
        "relation_ids": [item["id"] for item in config["relations"]],
        "number_ids": [item["id"] for item in config["numbers"]],
        "primary_rule_records_verified": sorted(required_rules),
        "inputs": {project_path(CONFIG): sha256(CONFIG), project_path(rule_path): sha256(rule_path)},
    }
    (RESULTS / "subanta_coordinate_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 3: Relation-Number Coordinates", "",
        f"The pinned engine exposes **{len(engine_relations)} relation coordinates** and **{len(engine_numbers)} number coordinates**, producing **{report['cells_per_name_meaning']} grammatical cells per eligible meaning**.", "",
        "The eight relation coordinates include direct address. The three number coordinates distinguish one, two, and more than two. Primary records for the inventory and coordinate definitions are present in the archived rule source.", "",
    ]
    (RESULTS / "subanta_coordinate_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(engine_relations)} x {len(engine_numbers)} relation-number coordinates.")


if __name__ == "__main__":
    main()
