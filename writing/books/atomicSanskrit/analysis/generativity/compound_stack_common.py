"""Shared paths and helpers for operations applied to source compounds."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
SOURCE_LEDGER = RESULTS / "samasa_ledger.csv"
CLASSIFICATION = RESULTS / "compound_stack_classification.json"
CLASSIFICATION_ROWS = RESULTS / "compound_stack_classification.csv"
ELIGIBILITY = RESULTS / "compound_stack_eligibility.json"
ELIGIBILITY_ROWS = RESULTS / "compound_stack_eligible_relations.csv"
CONFIG = HERE / "compound_stack_operations.json"
CURRENT_SUBTOTAL = 12_845_500


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path):
    return json.loads(path.read_text())
