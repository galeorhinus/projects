#!/usr/bin/env python3
"""Pass 3: build the current nominal inventory and declare nan eligibility."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import io
import json

from nan_common import NOMINAL_INVENTORY, RESULTS, project_path, sha256


CONFIG = __import__("pathlib").Path(__file__).with_name("nan_operations.json")
TADDHITA = RESULTS / "taddhita_ledger.csv.gz"
CONDITIONED = RESULTS / "conditioned_taddhita_ledger.csv"
STRI = RESULTS / "stri_ledger.csv"
OUTPUT = RESULTS / "nan_nominal_inventory.csv.gz"
FIELDS = (
    "nan_input_word_meaning_id", "source_layer", "source_word_meaning_id",
    "source_operation_id", "input_forms_slp1", "input_variant_count",
    "source_semantic_relation", "domain", "eligibility_status",
)


def deterministic_writer(path):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0)
    text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
    writer = csv.DictWriter(text, fieldnames=FIELDS)
    writer.writeheader()
    return raw, text, writer


def write_row(writer, *, identifier, layer, source_id, operation, forms, relation):
    variants = sorted(set(filter(None, forms.split(";"))))
    if not variants:
        raise ValueError(f"No input form for {identifier}")
    writer.writerow({
        "nan_input_word_meaning_id": identifier,
        "source_layer": layer,
        "source_word_meaning_id": source_id,
        "source_operation_id": operation,
        "input_forms_slp1": ";".join(variants),
        "input_variant_count": len(variants),
        "source_semantic_relation": relation,
        "domain": "laukika",
        "eligibility_status": "eligible_for_one_nan_privative_relation",
    })


def main() -> None:
    config = json.loads(CONFIG.read_text())
    counts = Counter()
    identifiers = set()
    raw, text, writer = deterministic_writer(OUTPUT)
    try:
        with gzip.open(NOMINAL_INVENTORY, "rt", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                identifier = f"first_nominal:{row['nominal_word_meaning_id']}"
                if identifier in identifiers:
                    raise ValueError(f"Duplicate nan input: {identifier}")
                identifiers.add(identifier)
                write_row(
                    writer, identifier=identifier, layer=row["source_layer"],
                    source_id=row["nominal_word_meaning_id"], operation=row["source_operation_id"],
                    forms=row["input_forms_slp1"], relation=row["source_semantic_relation"],
                )
                counts["first_nominal_inventory"] += 1
        with gzip.open(TADDHITA, "rt", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                identifier = f"broad_taddhita:{row['derived_word_meaning_id']}"
                if identifier in identifiers:
                    raise ValueError(f"Duplicate nan input: {identifier}")
                identifiers.add(identifier)
                write_row(
                    writer, identifier=identifier, layer="broad_taddhita",
                    source_id=row["derived_word_meaning_id"], operation=row["taddhita_operation_id"],
                    forms=row["output_forms_slp1"], relation=row["semantic_relation"],
                )
                counts["broad_taddhita"] += 1
        with CONDITIONED.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["reconciliation_status"] != "admitted_conditioned_addition":
                    continue
                identifier = f"conditioned_taddhita:{row['verified_word_meaning_id']}"
                if identifier in identifiers:
                    raise ValueError(f"Duplicate nan input: {identifier}")
                identifiers.add(identifier)
                write_row(
                    writer, identifier=identifier, layer="conditioned_taddhita",
                    source_id=row["verified_word_meaning_id"], operation=row["taddhita_source_variant"],
                    forms=row["generated_output_forms_slp1"], relation=row["semantic_description"],
                )
                counts["conditioned_taddhita"] += 1
        with STRI.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["count_status"] != "admitted_source_demonstrated_stri_word_meaning":
                    continue
                identifier = f"stri:{row['generated_word_meaning_id']}"
                if identifier in identifiers:
                    raise ValueError(f"Duplicate nan input: {identifier}")
                identifiers.add(identifier)
                write_row(
                    writer, identifier=identifier, layer="stri",
                    source_id=row["generated_word_meaning_id"], operation=row["applied_stri_suffixes"],
                    forms=row["generated_nominative_forms_slp1"], relation=row["semantic_relation"],
                )
                counts["stri"] += 1
    finally:
        text.flush()
        text.close()
        raw.close()

    total = sum(counts.values())
    report = {
        "date": "2026-09-13",
        "eligible_nominal_word_meanings": total,
        "eligible_by_source_layer": dict(counts),
        "semantic_operations_per_input": 1,
        "candidate_nan_word_meanings": total,
        "eligibility_scope": config["eligibility_scope"],
        "exclusions": config["exclusions"],
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, NOMINAL_INVENTORY, TADDHITA, CONDITIONED, STRI, __import__("pathlib").Path(__file__))},
        "publication_status": "research_eligibility_only_not_deployed",
    }
    (RESULTS / "nan_eligibility.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "nan_eligibility.md").write_text("\n".join([
        "# नञ् Eligibility", "",
        "This pass collects the current bounded लौकिक nominal inventory. Every admitted nominal word-meaning receives one negative counterpart. **अ-** and **अन्-** remain surface variants of that one relation.", "",
        "| Input layer | Eligible meanings |", "|---|---:|",
        *[f"| {layer} | {count:,} |" for layer, count in counts.items()],
        f"| **Total candidate नञ् meanings** | **{total:,}** |", "",
        "The pass does not apply नञ् recursively to its own output and does not count inflected compound forms.", "",
    ]))
    print(f"Declared {total} nominal meanings eligible for one nan relation.")


if __name__ == "__main__":
    main()
