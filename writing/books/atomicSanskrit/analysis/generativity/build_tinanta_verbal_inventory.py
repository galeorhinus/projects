#!/usr/bin/env python3
"""Tinanta pass 2: normalize the current laukika verbal meaning inventory."""

from __future__ import annotations

from collections import Counter
import csv
import json

from tinanta_common import (
    RESULTS, SOURCE_LAYERS, csv_rows, is_restricted, project_path, sha256,
    split_values, stable_id,
)


SAMPLE_FIELDS = (
    "verbal_word_meaning_id", "source_layer", "base_source_codes",
    "base_citations_slp1", "meaning", "input_forms_slp1", "prefixes_slp1",
    "operation_id", "constructor", "output_base_forms_slp1",
)


def normalized_row(layer: str, row: dict[str, str], word_id: str) -> dict[str, str]:
    prefixes = ""
    operation = ""
    constructor = ""
    input_forms = ""
    outputs = ""
    meaning = row.get("semantic_relation") or row.get("meaning_display") or row.get("base_meaning_display", "")
    if layer == "base":
        outputs = row["normalized_citation_slp1"]
    elif layer == "one_sanadi":
        operation = row["operation_id"]; outputs = row["output_forms_slp1"]
    elif layer == "one_upasarga":
        prefixes = row["upasarga_source_forms_slp1"]; outputs = row["output_forms_slp1"]
    elif layer == "upasarga_sanadi":
        prefixes = row["upasarga_source_forms_slp1"]; operation = row["operation_id"]; outputs = row["output_forms_slp1"]
    elif layer == "curadi_true_causative":
        operation = row["operation_id"]; outputs = row["output_forms_slp1"]
    elif layer == "two_upasarga":
        prefixes = ";".join(split_values(row["upasarga_sequence_slp1"], "+")); outputs = row["output_forms_slp1"]
    elif layer == "namadhatu":
        prefixes = row["prefixes_slp1"]; operation = row["namadhatu_operation_id"]
        constructor = row["constructor"]; input_forms = row["input_forms_slp1"]
        outputs = row["output_base_forms_slp1"]
    elif layer == "compound_namadhatu":
        operation = row["operation_id"]; constructor = {
            "self_desire_kyac": "kyac", "self_desire_kamyac": "kAmyac",
            "object_comparison_kyac": "kyac", "agent_comparison_kyang": "kyaN",
        }.get(operation, "")
        input_forms = row["input_forms_slp1"]; outputs = row["output_forms_slp1"]
    return {
        "verbal_word_meaning_id": word_id, "source_layer": layer,
        "base_source_codes": row.get("base_source_codes", row.get("source_code", "")),
        "base_citations_slp1": row.get("base_citations_slp1", row.get("normalized_citation_slp1", "")),
        "meaning": meaning, "input_forms_slp1": input_forms,
        "prefixes_slp1": prefixes, "operation_id": operation,
        "constructor": constructor, "output_base_forms_slp1": outputs,
    }


def main() -> None:
    counts = Counter()
    excluded = Counter()
    samples: dict[str, dict[str, str]] = {}
    inputs = {}
    for layer, path in SOURCE_LAYERS:
        inputs[project_path(path)] = sha256(path)
        if layer == "base":
            groups: dict[str, list[dict[str, str]]] = {}
            for row in csv_rows(path):
                if row["record_kind"] == "lexical":
                    groups.setdefault(row["normalized_count_key"], []).append(row)
            for key, rows in groups.items():
                codes = {row["source_code"] for row in rows}
                representative = dict(rows[0])
                representative["source_code"] = ";".join(sorted(codes))
                if is_restricted(representative, "source_code"):
                    excluded[layer] += 1; continue
                word_id = "base:" + stable_id(key)
                counts[layer] += 1
                samples.setdefault(layer, normalized_row(layer, representative, word_id))
                if "01.0002" in codes:
                    samples.setdefault("base_atmanepada_example", normalized_row(layer, representative, word_id))
            continue

        for row in csv_rows(path):
            if layer == "compound_namadhatu" and row["output_form_class"] != "derived_verbal_base":
                continue
            if layer not in {"namadhatu", "compound_namadhatu"} and is_restricted(row):
                excluded[layer] += 1; continue
            id_field = {
                "one_sanadi": "derived_word_meaning_id",
                "one_upasarga": "generated_word_meaning_id",
                "upasarga_sanadi": "stacked_word_meaning_id",
                "curadi_true_causative": "derived_word_meaning_id",
                "two_upasarga": "generated_word_meaning_id",
                "namadhatu": "derived_word_meaning_id",
                "compound_namadhatu": "derived_word_meaning_id",
            }[layer]
            word_id = f"{layer}:{row[id_field]}"
            counts[layer] += 1
            samples.setdefault(layer, normalized_row(layer, row, word_id))

    total = sum(counts.values())
    expected = {
        "base": 2623, "one_sanadi": 12480, "one_upasarga": 52347,
        "upasarga_sanadi": 249200, "curadi_true_causative": 522,
        "two_upasarga": 1046940, "namadhatu": 3176352,
        "compound_namadhatu": 384,
    }
    if dict(counts) != expected:
        raise ValueError(f"Verbal inventory mismatch: {dict(counts)}")

    with (RESULTS / "tinanta_verbal_member_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SAMPLE_FIELDS)
        writer.writeheader(); writer.writerows(samples.values())
    report = {
        "date": "2026-09-14", "laukika_verbal_word_meanings": total,
        "counts_by_source_layer": dict(counts),
        "known_vaidika_restricted_meanings_excluded_by_layer": dict(excluded),
        "inventory_storage": "normalized virtual view over existing reconciled ledgers",
        "full_inventory_duplicated": False, "materialized_sample_records": len(samples),
        "inputs": inputs,
    }
    (RESULTS / "tinanta_verbal_inventory.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 2: Verbal Meaning Inventory", "", "The current ledgers contain **{:,} लौकिक verbal word-meanings** available to the ten-लकार model. They remain a virtual view; this pass does not copy four million rows.".format(total), "", "| Source layer | Verbal meanings |", "|---|---:|"]
    for layer, count in counts.items(): lines.append(f"| {layer} | {count:,} |")
    lines.extend([f"| **Total** | **{total:,}** |", "", "Rows descending from the eleven documented Vedic-only base meanings remain outside this लौकिक inventory. लेट् and Vedic inflection require their own domain pass.", ""])
    (RESULTS / "tinanta_verbal_inventory.md").write_text("\n".join(lines))
    print(f"Built virtual inventory of {total} laukika verbal word-meanings.")


if __name__ == "__main__":
    main()
