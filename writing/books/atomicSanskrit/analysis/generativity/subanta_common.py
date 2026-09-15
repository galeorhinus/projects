#!/usr/bin/env python3
"""Shared paths and helpers for the twelve subanta-capacity passes."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

from vidyut.prakriya import Pratipadika


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
CONFIG = HERE / "subanta_operations.json"
CURRENT_LEXICAL_SUBTOTAL = 12_846_458


SAMPLES = (
    {
        "sample_id": "gamana", "display": "गमनम् (gamanam), going",
        "stem_slp1": "gamana", "constructor": "basic", "linga": "Napumsaka",
        "source_file": "krdanta_ledger.csv", "source_id_field": "derived_word_meaning_id",
        "source_word_meaning_id": "7a90db603ab51397148f", "source_form_field": "output_forms_slp1",
        "expected_citation_slp1": "gamanam",
    },
    {
        "sample_id": "kartr", "display": "कर्ता (kartā), doer",
        "stem_slp1": "kartf", "constructor": "basic", "linga": "Pum",
        "source_file": "krdanta_ledger.csv", "source_id_field": "derived_word_meaning_id",
        "source_word_meaning_id": "ebf3acad8cac4eb32dea", "source_form_field": "output_forms_slp1",
        "expected_citation_slp1": "kartA",
    },
    {
        "sample_id": "mitratva", "display": "मित्रत्वम् (mitratvam), friendship",
        "stem_slp1": "mitratva", "constructor": "basic", "linga": "Napumsaka",
        "source_file": "taddhita_ledger.csv.gz", "source_id_field": "derived_word_meaning_id",
        "source_word_meaning_id": "c4dfd65d6035bf5fd9af", "source_form_field": "output_forms_slp1",
        "expected_citation_slp1": "mitratvam",
    },
    {
        "sample_id": "kaunteya", "display": "कौन्तेयः (Kaunteyaḥ), a son or descendant of Kuntī",
        "stem_slp1": "kOnteya", "constructor": "basic", "linga": "Pum",
        "source_file": "taddhita_ledger.csv.gz", "source_id_field": "derived_word_meaning_id",
        "source_word_meaning_id": "b829ae0a686f4e53566a", "source_form_field": "output_forms_slp1",
        "expected_citation_slp1": "kOnteyaH",
    },
    {
        "sample_id": "kartri", "display": "कर्त्री (kartrī), female doer",
        "stem_slp1": "kartrI", "constructor": "nyap", "linga": "Stri",
        "source_file": "stri_generalization_ledger.csv.gz", "source_id_field": "generated_word_meaning_id",
        "source_word_meaning_id": "14e1dfa2790306ebe3bb", "source_form_field": "generated_forms_slp1",
        "expected_citation_slp1": "kartrI",
    },
    {
        "sample_id": "ajnana", "display": "अज्ञानम् (ajñānam), absence of knowledge",
        "stem_slp1": "ajYAna", "constructor": "basic", "linga": "Napumsaka",
        "source_file": "nan_ledger.csv.gz", "source_id_field": "derived_word_meaning_id",
        "source_word_meaning_id": "43acdd0070393388d0f8", "source_form_field": "output_forms_slp1",
        "expected_citation_slp1": "ajYAnam",
    },
    {
        "sample_id": "mahapurusha", "display": "महापुरुषः (mahāpuruṣaḥ), a great person",
        "stem_slp1": "mahApuruza", "constructor": "basic", "linga": "Pum",
        "source_file": "samasa_ledger.csv", "source_id_field": "generated_word_meaning_id",
        "source_word_meaning_id": "f2d107d0d66e1f1f", "source_form_field": "output_forms_slp1",
        "expected_citation_slp1": "mahApuruzaH",
    },
    {
        "sample_id": "mahapurushatva", "display": "महापुरुषत्वम् (mahāpuruṣatvam), the state of being a great person",
        "stem_slp1": "mahApuruzatva", "constructor": "basic", "linga": "Napumsaka",
        "source_file": "compound_stack_ledger.csv", "source_id_field": "derived_word_meaning_id",
        "source_word_meaning_id": "64a320b049c25388fbd0", "source_form_field": "output_forms_slp1",
        "expected_citation_slp1": "mahApuruzatvam",
    },
)


def read_json(path: Path):
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def csv_rows(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def pratipadika_for(sample: dict):
    if sample["constructor"] == "nyap":
        return Pratipadika.nyap(sample["stem_slp1"])
    return Pratipadika.basic(sample["stem_slp1"])


def result_paths(results) -> list[dict]:
    return [
        {
            "form_slp1": result.text,
            "steps": [
                {"rule_source": str(step.source), "rule": step.code, "result": list(step.result)}
                for step in result.history
            ],
        }
        for result in results
    ]
