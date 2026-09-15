#!/usr/bin/env python3
"""Pass 4: materialize one bounded nan meaning per eligible nominal meaning."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import io
import json

from nan_common import RESULTS, nan_surface, project_path, sha256, stable_id


CONFIG = __import__("pathlib").Path(__file__).with_name("nan_operations.json")
ELIGIBILITY = RESULTS / "nan_eligibility.json"
INVENTORY = RESULTS / "nan_nominal_inventory.csv.gz"
SOURCE_EXAMPLES = RESULTS / "nan_source_examples.csv"
LEDGER = RESULTS / "nan_ledger.csv.gz"
FIELDS = (
    "derived_word_meaning_id", "nan_input_word_meaning_id", "source_layer",
    "source_word_meaning_id", "source_operation_id", "input_forms_slp1",
    "nan_operation_id", "semantic_relation", "source_semantic_relation",
    "rule_refs", "output_forms_slp1", "output_variant_count",
    "surface_outcomes", "admission_basis", "count_status",
)


def deterministic_writer(path):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0)
    text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
    writer = csv.DictWriter(text, fieldnames=FIELDS)
    writer.writeheader()
    return raw, text, writer


def main() -> None:
    config = json.loads(CONFIG.read_text())
    eligibility = json.loads(ELIGIBILITY.read_text())
    counts = Counter()
    surface_counts = Counter()
    output_variants = 0
    output_spellings = Counter()
    raw, text, writer = deterministic_writer(LEDGER)
    try:
        with gzip.open(INVENTORY, "rt", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                outputs = set()
                outcomes = set()
                for form in row["input_forms_slp1"].split(";"):
                    output, outcome = nan_surface(form)
                    outputs.add(output)
                    outcomes.add(outcome)
                forms = sorted(outputs)
                writer.writerow({
                    "derived_word_meaning_id": stable_id("nan", row["nan_input_word_meaning_id"]),
                    "nan_input_word_meaning_id": row["nan_input_word_meaning_id"],
                    "source_layer": row["source_layer"],
                    "source_word_meaning_id": row["source_word_meaning_id"],
                    "source_operation_id": row["source_operation_id"],
                    "input_forms_slp1": row["input_forms_slp1"],
                    "nan_operation_id": config["operation_id"],
                    "semantic_relation": config["semantic_relation"],
                    "source_semantic_relation": row["source_semantic_relation"],
                    "rule_refs": ";".join([config["compound_rule"], *config["surface_rules"]]),
                    "output_forms_slp1": ";".join(forms),
                    "output_variant_count": len(forms),
                    "surface_outcomes": ";".join(sorted(outcomes)),
                    "admission_basis": "admitted_nominal_word_meaning_plus_nan_compound_rule_plus_explicit_surface_rules",
                    "count_status": "admitted_research_ledger",
                })
                counts[row["source_layer"]] += 1
                surface_counts.update(outcomes)
                output_variants += len(forms)
                output_spellings.update(forms)
    finally:
        text.flush()
        text.close()
        raw.close()

    admitted = sum(counts.values())
    if admitted != eligibility["candidate_nan_word_meanings"]:
        raise ValueError(f"Eligibility mismatch: {admitted} != {eligibility['candidate_nan_word_meanings']}")
    collisions = sum(count - 1 for count in output_spellings.values() if count > 1)
    report = {
        "date": "2026-09-13",
        "eligible_nan_word_meanings": eligibility["candidate_nan_word_meanings"],
        "admitted_nan_word_meanings": admitted,
        "not_admitted_total": 0,
        "admitted_by_source_layer": dict(counts),
        "word_meanings_by_surface_outcome": dict(surface_counts),
        "generated_output_variants": output_variants,
        "distinct_output_spellings": len(output_spellings),
        "coincident_output_spellings_beyond_first": collisions,
        "collision_policy": "Coincident spellings do not merge different source meanings. One source word-meaning plus the nan relation remains one generated word-meaning.",
        "implementation": "The pinned Python API exposes no compound constructor. This ledger applies the three classified rules directly after verifying both surface outcomes against five pinned source tests.",
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, ELIGIBILITY, INVENTORY, SOURCE_EXAMPLES, __import__("pathlib").Path(__file__))},
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "nan_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "nan_summary.md").write_text("\n".join([
        "# Bounded नञ् Generation", "",
        f"The pass admits **{admitted:,}** negative word-meanings from the current nominal inventory. The two visible beginnings, **अ-** and **अन्-**, are phonetic outcomes of one operation.", "",
        "| Input layer | Added negative meanings |", "|---|---:|",
        *[f"| {layer} | {count:,} |" for layer, count in counts.items()],
        f"| **Total** | **{admitted:,}** |", "",
        f"The ledger contains {output_variants:,} output variants and {len(output_spellings):,} distinct spellings. Its {collisions:,} repeated spellings do not collapse different meanings.", "",
        "No dictionary-attestation gate was applied. The operation is admitted because the grammar licenses it and the declared surface rules form it.", "",
    ]))
    print(f"Admitted {admitted} nan word-meanings.")


if __name__ == "__main__":
    main()
