#!/usr/bin/env python3
"""Reconcile the six completed generativity expansion passes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FILES = {
    "verbal": RESULTS / "verbal_derivation_summary.json",
    "one_upasarga": RESULTS / "upasarga_generation_summary.json",
    "upasarga_sanadi": RESULTS / "upasarga_sanadi_summary.json",
    "curadi": RESULTS / "curadi_causative_summary.json",
    "two_upasarga": RESULTS / "two_upasarga_summary.json",
    "krt_classification": RESULTS / "krt_classification.json",
    "krdanta": RESULTS / "krdanta_summary.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = {name: json.loads(path.read_text()) for name, path in FILES.items()}
    layers = [
        ("Original धातु meanings and one सनादि operation", data["verbal"]["verbal_word_meanings_including_bases"]),
        ("One उपसर्गः from original धातु meanings", data["one_upasarga"]["generated_upasarga_word_meanings"]),
        ("One उपसर्गः plus one सनादि operation", data["upasarga_sanadi"]["admitted_stacked_word_meanings"]),
        ("True चरादिगण causatives", data["curadi"]["admitted_true_causative_word_meanings"]),
        ("Exactly two ordered उपसर्गाः", data["two_upasarga"]["admitted_two_upasarga_word_meanings"]),
        ("Bounded कृदन्त formations from original धातु meanings", data["krdanta"]["admitted_krdanta_word_meanings"]),
    ]
    subtotal = sum(value for _, value in layers)
    expected = data["krdanta"]["bounded_word_meaning_subtotal"]
    if subtotal != expected:
        raise ValueError(f"Six-pass subtotal mismatch: {subtotal} != {expected}")
    if data["krt_classification"]["bounded_laukika_semantic_operations"] != 14:
        raise ValueError("Krt classification no longer exposes fourteen bounded operations")
    report = {
        "date": "2026-09-13",
        "scope": "Six completed bounded expansion passes following the reconciled 2,634 original dhatu meanings; inflection remains separate.",
        "layers": [{"label": label, "word_meanings": value} for label, value in layers],
        "bounded_word_meaning_subtotal": subtotal,
        "not_a_complete_sanskrit_vocabulary_total": True,
        "remaining_major_layers": [
            "three or more upasargas",
            "additional sanadi orderings and depths",
            "krdantas from prefixed and sanadi-derived verbal inputs",
            "laukika avyayas",
            "Vedic-only krt formations",
            "root- and construction-conditioned krt formations",
            "namadhatus from a bounded nominal inventory",
            "taddhitantas, feminine formations, compounds, and other nominal derivations",
            "tin and sup inflection, reported separately from word-meanings"
        ],
        "publication_status": "research_subtotal_only_not_deployed",
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in FILES.values()},
    }
    (RESULTS / "six_pass_expansion_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Six-Pass Generativity Expansion", "",
        "The six completed passes produce a reproducible **bounded subtotal of 1,399,621 word-meanings**. This is not a claim about Sanskrit's complete vocabulary. Each row is tied to a declared semantic operation, an admitted input meaning, a pinned engine construction, and any applicable source restriction.", "",
        "| Completed layer | Word-meanings |", "|---|---:|",
    ]
    for label, value in layers:
        lines.append(f"| {label} | {value:,} |")
    lines.extend([
        f"| **Bounded subtotal** | **{subtotal:,}** |", "",
        "The subtotal counts different words or meanings even when their spellings coincide. It keeps alternative surface forms of one derivation together. It does not use dictionary attestation as a gate where a productive rule licenses a formation, but it honors explicit grammatical and lexical restrictions.", "",
        "## Still Outside the Boundary", "",
    ])
    lines.extend(f"- {item}" for item in report["remaining_major_layers"])
    lines.extend(["", "The manuscript's published calculation remains unchanged until this research subtotal and its next layers are reviewed together.", ""])
    (RESULTS / "six_pass_expansion_summary.md").write_text("\n".join(lines))
    print(f"Reconciled six passes: {subtotal} bounded word-meanings.")


if __name__ == "__main__":
    main()
