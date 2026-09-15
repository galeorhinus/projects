#!/usr/bin/env python3
"""Shared helpers for the broader lexical स्त्रीप्रत्ययः pass."""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
CONFIG = HERE / "stri_generalization_operations.json"
NOMINAL = RESULTS / "nominal_input_inventory.csv.gz"
ELIGIBILITY = RESULTS / "stri_generalization_eligibility.csv.gz"
LEDGER = RESULTS / "stri_generalization_ledger.csv.gz"
EXCLUSIONS = RESULTS / "stri_generalization_exclusions.csv.gz"

SOURCE_LEDGERS = {
    "direct_krdanta": (RESULTS / "krdanta_ledger.csv", False),
    "conditioned_krdanta": (RESULTS / "conditioned_krdanta_ledger.csv", False),
    "prefixed_krdanta": (RESULTS / "prefixed_krdanta_ledger.csv.gz", True),
    "sanadi_krdanta": (RESULTS / "sanadi_krdanta_ledger.csv.gz", True),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_csv(path: Path, compressed: bool = False):
    opener = gzip.open if compressed else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def deterministic_gzip_writer(path: Path, fields: list[str]):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0)
    text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
    writer = csv.DictWriter(text, fieldnames=fields)
    writer.writeheader()
    return raw, text, writer


def close_gzip_writer(raw, text) -> None:
    text.flush()
    text.close()
    raw.close()
