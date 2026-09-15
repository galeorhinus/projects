#!/usr/bin/env python3
"""Shared paths and helpers for the bounded nan-compound passes."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "nan_manifest.json"
RULE_TABLE = ARCHIVE / "sutrapatha.tsv"
TEST_2_2 = ARCHIVE / "kashika_2_2.rs"
TEST_6_3 = ARCHIVE / "kashika_6_3.rs"
IMPLEMENTATION = ARCHIVE / "vidyut-samasa.rs"
NOMINAL_INVENTORY = RESULTS / "nominal_input_inventory.csv.gz"
VOWELS = frozenset("aAiIuUfFxXeEoO")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def nan_surface(form: str) -> tuple[str, str]:
    """Derive the ordinary laukika surface outcome licensed by 6.3.73-74:
    n-loss yields a- before a consonant; nuṭ yields an- before a vowel.
    """
    if not form:
        raise ValueError("Cannot prefix an empty nominal form")
    if form[0] in VOWELS:
        return "an" + form, "an_before_vowel"
    return "a" + form, "a_before_consonant"
