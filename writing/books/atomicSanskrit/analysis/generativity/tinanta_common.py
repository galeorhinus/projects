#!/usr/bin/env python3
"""Shared paths, counts, and constructors for the tinanta capacity passes."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

from vidyut.prakriya import Data, Dhatu, Pratipadika, Sanadi


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
CONFIG = HERE / "tinanta_operations.json"
RESTRICTIONS = HERE / "vaidika_base_restrictions.json"
CURRENT_LEXICAL_SUBTOTAL = 12_846_458

SOURCE_LAYERS = (
    ("base", RESULTS / "current_base_assignments.csv"),
    ("one_sanadi", RESULTS / "verbal_derivation_ledger.csv"),
    ("one_upasarga", RESULTS / "upasarga_generation_ledger.csv"),
    ("upasarga_sanadi", RESULTS / "upasarga_sanadi_ledger.csv.gz"),
    ("curadi_true_causative", RESULTS / "curadi_causative_ledger.csv"),
    ("two_upasarga", RESULTS / "two_upasarga_ledger.csv.gz"),
    ("namadhatu", RESULTS / "namadhatu_ledger.csv.gz"),
    ("compound_namadhatu", RESULTS / "compound_stack_ledger.csv"),
)

SANADI_BY_OPERATION = {
    "causative": Sanadi.Ric,
    "desiderative": Sanadi.san,
    "intensive": Sanadi.yaN,
    "intensive_luk": Sanadi.yaNluk,
}
NAMADHATU_SANADI = {
    "self_desire_kyac": Sanadi.kyac,
    "self_desire_kamyac": Sanadi.kAmyac,
    "object_comparison_kyac": Sanadi.kyac,
    "agent_comparison_kyang": Sanadi.kyaN,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_json(path: Path):
    return json.loads(path.read_text())


def csv_rows(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def restricted_source_codes() -> set[str]:
    return {row["source_code"] for row in read_json(RESTRICTIONS)["source_entries"]}


def split_values(value: str, separator: str = ";") -> list[str]:
    return [item for item in value.split(separator) if item]


def is_restricted(row: dict[str, str], field: str = "base_source_codes") -> bool:
    return bool(set(split_values(row.get(field, ""))) & restricted_source_codes())


def load_entries():
    return {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}


def construct_sample_dhatu(row: dict[str, str], entries):
    layer = row["source_layer"]
    codes = split_values(row.get("base_source_codes", ""))
    if layer in {
        "base", "one_sanadi", "one_upasarga", "upasarga_sanadi",
        "curadi_true_causative", "two_upasarga",
    }:
        if not codes:
            raise ValueError(f"No source code for {row['verbal_word_meaning_id']}")
        dhatu = entries[codes[0]].dhatu
        if layer == "one_sanadi":
            dhatu = dhatu.with_sanadi([SANADI_BY_OPERATION[row["operation_id"]]])
        elif layer == "upasarga_sanadi":
            dhatu = dhatu.with_sanadi([SANADI_BY_OPERATION[row["operation_id"]]])
        elif layer == "curadi_true_causative":
            dhatu = dhatu.with_sanadi([Sanadi.Ric, Sanadi.Ric])
        prefixes = split_values(row.get("prefixes_slp1", ""))
        if prefixes:
            dhatu = dhatu.with_prefixes(prefixes)
        return dhatu

    forms = split_values(row["input_forms_slp1"])
    if not forms:
        raise ValueError(f"No nominal input for {row['verbal_word_meaning_id']}")
    operation_id = row["operation_id"]
    constructor = row.get("constructor", "")
    suffix = NAMADHATU_SANADI.get(operation_id)
    if suffix is None and constructor and constructor != "auto":
        suffix = getattr(Sanadi, constructor)
    dhatu = Dhatu.nama(Pratipadika.basic(forms[0]), nama_sanadi=suffix)
    prefixes = split_values(row.get("prefixes_slp1", ""))
    return dhatu.with_prefixes(prefixes) if prefixes else dhatu


def result_paths(results) -> list[dict]:
    return [
        {
            "form_slp1": result.text,
            "steps": [
                {
                    "rule_source": str(step.source),
                    "rule": step.code,
                    "result": list(step.result),
                }
                for step in result.history
            ],
        }
        for result in results
    ]
