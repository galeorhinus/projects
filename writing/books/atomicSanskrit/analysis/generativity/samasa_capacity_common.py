"""Shared inputs and arithmetic for the symbolic samasa-capacity passes."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
CONFIG = ANALYSIS / "samasa_capacity_operations.json"
MANIFEST = ARCHIVE / "samasa_manifest.json"
IMPLEMENTATION = ARCHIVE / "vidyut-samasa.rs"
ARGS_SOURCE = ARCHIVE / "vidyut-args-samasa.rs"
RULE_TABLE = ARCHIVE / "vidyut-sutrapatha.tsv"
VERIFIER = ANALYSIS / "rust/samasa_verifier/target/release/samasa-verifier"
CURRENT_LEXICAL_SUBTOTAL = 12_846_458


SOURCE_PATHS = {
    "first_nominal": RESULTS / "nan_nominal_inventory.csv.gz",
    "nan": RESULTS / "nan_ledger.csv.gz",
    "conditioned_suffix": RESULTS / "suffix_conditioned_ledger.csv",
    "plain_taddhita": RESULTS / "plain_taddhita_ledger.csv",
    "degree": RESULTS / "taddhita_generalization_ledger.csv.gz",
    "lexical_stri": RESULTS / "stri_generalization_ledger.csv.gz",
    "lexical_stri_reconciliation": RESULTS / "stri_generalization_reconciliation.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:20]


def open_csv(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    return opener(path, "rt", encoding="utf-8", newline="")


def split_forms(value: str) -> list[str]:
    return sorted({form for form in value.split(";") if form})


def iter_compoundable_members():
    """Yield one normalized record per admitted nominal word-meaning."""
    with open_csv(SOURCE_PATHS["first_nominal"]) as handle:
        for row in csv.DictReader(handle):
            yield {
                "member_id": f"base:{row['nan_input_word_meaning_id']}",
                "source_layer": f"base:{row['source_layer']}",
                "operation_id": row["source_operation_id"],
                "forms_slp1": row["input_forms_slp1"],
                "semantic_relation": row["source_semantic_relation"],
                "domain": row["domain"],
            }

    with open_csv(SOURCE_PATHS["nan"]) as handle:
        for row in csv.DictReader(handle):
            yield {
                "member_id": f"nan:{row['derived_word_meaning_id']}",
                "source_layer": "nan",
                "operation_id": row["nan_operation_id"],
                "forms_slp1": row["output_forms_slp1"],
                "semantic_relation": row["semantic_relation"],
                "domain": "laukika",
            }

    with open_csv(SOURCE_PATHS["conditioned_suffix"]) as handle:
        for row in csv.DictReader(handle):
            if row["reconciliation_status"] != "admitted_additional_conditioned_relation":
                continue
            yield {
                "member_id": f"conditioned_suffix:{row['relation_id']}",
                "source_layer": "conditioned_suffix",
                "operation_id": row["family_id"],
                "forms_slp1": row["generated_output_forms_slp1"],
                "semantic_relation": row["semantic_relation"],
                "domain": "laukika",
            }

    with open_csv(SOURCE_PATHS["plain_taddhita"]) as handle:
        for row in csv.DictReader(handle):
            if row["reconciliation_status"] != "admitted_additional_plain_relation":
                continue
            if row["output_class"] != "nominal_base":
                continue
            if row["domain"] != "laukika":
                continue
            yield {
                "member_id": f"plain_taddhita:{row['eligible_word_meaning_id']}",
                "source_layer": "plain_taddhita",
                "operation_id": ";".join(split_forms(row["taddhita_source_variants"])),
                "forms_slp1": row["generated_output_forms_slp1"],
                "semantic_relation": row["semantic_relation"],
                "domain": row["domain"],
            }

    with open_csv(SOURCE_PATHS["degree"]) as handle:
        for row in csv.DictReader(handle):
            if row["reconciliation_status"] != "admitted_generalized_relation":
                continue
            yield {
                "member_id": f"degree:{row['derived_word_meaning_id']}",
                "source_layer": "degree",
                "operation_id": row["taddhita_operation_id"],
                "forms_slp1": row["output_forms_slp1"],
                "semantic_relation": row["semantic_relation"],
                "domain": "laukika",
            }

    stri_reconciliation = json.loads(SOURCE_PATHS["lexical_stri_reconciliation"].read_text())
    stri_overlaps = {row["generalized_word_meaning_id"] for row in stri_reconciliation["overlaps"]}
    with open_csv(SOURCE_PATHS["lexical_stri"]) as handle:
        for row in csv.DictReader(handle):
            if row["count_status"] != "admitted_generalized_stri_word_meaning":
                continue
            if row["generated_word_meaning_id"] in stri_overlaps:
                continue
            yield {
                "member_id": f"lexical_stri:{row['generated_word_meaning_id']}",
                "source_layer": "lexical_stri",
                "operation_id": row["source_operation_id"],
                "forms_slp1": row["generated_forms_slp1"],
                "semantic_relation": row["feminine_semantic_relation"],
                "domain": "laukika",
            }


def relation_count(pair_model: str, n: int) -> int:
    if pair_model == "ordered_with_self":
        return n * n
    if pair_model == "ordered_distinct":
        return n * (n - 1)
    if pair_model == "unordered_distinct":
        return n * (n - 1) // 2
    raise ValueError(f"Unknown pair model: {pair_model}")


def load_config() -> dict:
    return json.loads(CONFIG.read_text())
