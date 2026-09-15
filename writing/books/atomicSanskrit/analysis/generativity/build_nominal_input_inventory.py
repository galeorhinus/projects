#!/usr/bin/env python3
"""Build the first sourced laukika nominal word-meaning inventory."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESTRICTIONS = HERE / "vaidika_base_restrictions.json"
PILOT = HERE / "nominal_taddhita_pilot.json"

LAYERS = (
    ("direct_krdanta", RESULTS / "krdanta_ledger.csv", False),
    ("conditioned_krdanta", RESULTS / "conditioned_krdanta_ledger.csv", False),
    ("prefixed_krdanta", RESULTS / "prefixed_krdanta_ledger.csv.gz", True),
    ("sanadi_krdanta", RESULTS / "sanadi_krdanta_ledger.csv.gz", True),
)

FIELDS = (
    "nominal_word_meaning_id", "source_layer", "source_word_meaning_id",
    "source_operation_id", "base_source_codes", "input_forms_slp1",
    "input_variant_count", "constructor", "source_semantic_branch_id",
    "source_semantic_relation", "source_basis", "domain", "count_status",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deterministic_gzip_text(path: Path):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0)
    return raw, zipped, io.TextIOWrapper(zipped, encoding="utf-8", newline="")


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    restricted = {
        row["source_code"]
        for row in json.loads(RESTRICTIONS.read_text())["source_entries"]
    }
    output = RESULTS / "nominal_input_inventory.csv.gz"
    by_layer = Counter()
    excluded_by_layer = Counter()
    unique_forms: set[str] = set()
    total = 0

    raw, zipped, text = deterministic_gzip_text(output)
    try:
        writer = csv.DictWriter(text, fieldnames=FIELDS)
        writer.writeheader()
        for layer, path, compressed in LAYERS:
            opener = gzip.open if compressed else open
            with opener(path, "rt", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    codes = {x for x in row["base_source_codes"].split(";") if x}
                    if codes & restricted:
                        excluded_by_layer[layer] += 1
                        continue
                    forms = sorted({x for x in row["output_forms_slp1"].split(";") if x})
                    if not forms:
                        raise ValueError(f"Nominal row has no form: {row['derived_word_meaning_id']}")
                    writer.writerow({
                        "nominal_word_meaning_id": f"{layer}:{row['derived_word_meaning_id']}",
                        "source_layer": layer,
                        "source_word_meaning_id": row["derived_word_meaning_id"],
                        "source_operation_id": row["operation_id"],
                        "base_source_codes": row["base_source_codes"],
                        "input_forms_slp1": ";".join(forms),
                        "input_variant_count": len(forms),
                        "constructor": "basic",
                        "source_semantic_branch_id": row["semantic_branch_id"],
                        "source_semantic_relation": row["semantic_relation"],
                        "source_basis": str(path.relative_to(ROOT)),
                        "domain": "laukika",
                        "count_status": "admitted_nominal_input",
                    })
                    total += 1
                    by_layer[layer] += 1
                    unique_forms.update(forms)

        pilot = json.loads(PILOT.read_text())
        for row in pilot["nominal_inputs"]:
            form = row["input_slp1"]
            writer.writerow({
                "nominal_word_meaning_id": f"declared:{row['nominal_id']}",
                "source_layer": "declared_pilot_nominal",
                "source_word_meaning_id": row["nominal_id"],
                "source_operation_id": "",
                "base_source_codes": "",
                "input_forms_slp1": form,
                "input_variant_count": 1,
                "constructor": "nyap" if row["nyap"] else "basic",
                "source_semantic_branch_id": row["input_type"],
                "source_semantic_relation": row["display"],
                "source_basis": row["source_basis"],
                "domain": "laukika",
                "count_status": "admitted_nominal_input",
            })
            total += 1
            by_layer["declared_pilot_nominal"] += 1
            unique_forms.add(form)
    finally:
        text.flush()
        text.close()
        raw.close()

    report = {
        "date": "2026-09-13",
        "scope": "Laukika nominal word-meanings already produced by the completed krdanta ledgers, plus the five declared taddhita-pilot nominals. This is not a census of all inherited Sanskrit nominals.",
        "admitted_nominal_word_meanings": total,
        "distinct_input_spellings": len(unique_forms),
        "admitted_by_layer": dict(by_layer),
        "known_vedic_restricted_rows_excluded_by_layer": dict(excluded_by_layer),
        "known_vedic_restricted_rows_excluded": sum(excluded_by_layer.values()),
        "independently_inherited_nominals_in_scope": len(json.loads(PILOT.read_text())["nominal_inputs"]),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (RESTRICTIONS, PILOT, *[x[1] for x in LAYERS], Path(__file__))
        },
    }
    (RESULTS / "nominal_input_inventory_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# First Laukika प्रातिपदिक Input Inventory", "",
        "This pass begins with nominal word-meanings already generated by the completed कृदन्त ledgers. It adds the five independently declared nominals from the earlier तद्धित pilot. It does not import a dictionary or treat every recorded Sanskrit noun as though it descended from the present धातु pipeline.", "",
        "| Source layer | Admitted nominal word-meanings | Known Vedic-restricted rows excluded |", "|---|---:|---:|",
    ]
    for layer, _, _ in LAYERS:
        lines.append(f"| {layer.replace('_', ' ')} | {by_layer[layer]:,} | {excluded_by_layer[layer]:,} |")
    lines.extend([
        f"| Declared pilot nominals | {by_layer['declared_pilot_nominal']:,} | 0 |",
        f"| **Total** | **{total:,}** | **{sum(excluded_by_layer.values()):,}** |", "",
        f"The {total:,} nominal word-meanings contain {len(unique_forms):,} distinct input spellings. Coincident spellings remain separate when their source meanings differ.", "",
        "Still outside this boundary are a general inherited-nominal census, compounds, feminine derivation as a separate operation, Vedic-only nominal inputs, and inflected सुबन्त forms.", "",
    ])
    (RESULTS / "nominal_input_inventory_summary.md").write_text("\n".join(lines))
    print(f"Admitted {total} laukika nominal word-meanings; excluded {sum(excluded_by_layer.values())} known Vedic-restricted rows.")


if __name__ == "__main__":
    main()
