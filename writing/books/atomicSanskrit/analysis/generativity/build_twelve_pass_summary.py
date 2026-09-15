#!/usr/bin/env python3
"""Reconcile the original and second six-pass generativity expansions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FILES = {
    "first_six": RESULTS / "six_pass_expansion_summary.json",
    "avyaya": RESULTS / "avyaya_summary.json",
    "conditioned_classification": RESULTS / "conditioned_krt_classification.json",
    "conditioned_krdanta": RESULTS / "conditioned_krdanta_summary.json",
    "prefixed_krdanta": RESULTS / "prefixed_krdanta_summary.json",
    "sanadi_krdanta": RESULTS / "sanadi_krdanta_summary.json",
    "taddhita_pilot": RESULTS / "taddhita_pilot_summary.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = {name: json.loads(path.read_text()) for name, path in FILES.items()}
    first_subtotal = data["first_six"]["bounded_word_meaning_subtotal"]
    additions = [
        ("Laukika अव्ययानि", data["avyaya"]["admitted_avyaya_word_meanings"]),
        (
            "Selected conditioned कृदन्त formations from original धातु meanings",
            data["conditioned_krdanta"]["admitted_conditioned_krdanta_word_meanings"],
        ),
        (
            "Fourteen कृदन्त operations from one-उपसर्गः meanings",
            data["prefixed_krdanta"]["admitted_prefixed_krdanta_word_meanings"],
        ),
        (
            "Fourteen कृदन्त operations from सनादि-derived meanings",
            data["sanadi_krdanta"]["admitted_sanadi_krdanta_word_meanings"],
        ),
        (
            "Bounded तद्धित pilot",
            data["taddhita_pilot"]["admitted_taddhita_word_meanings"],
        ),
    ]
    subtotal = first_subtotal + sum(value for _, value in additions)
    expected = data["taddhita_pilot"]["bounded_word_meaning_subtotal_including_pilot"]
    if subtotal != expected:
        raise ValueError(f"Twelve-pass subtotal mismatch: {subtotal} != {expected}")
    if data["conditioned_classification"]["deferred_identifiers_classified"] != 87:
        raise ValueError("The conditioned-krt pass no longer accounts for all 87 identifiers")

    report = {
        "date": "2026-09-13",
        "scope": "Twelve bounded research passes following the reconciled 2,634 original dhatu meanings; operations run in laukika engine mode, with inflection separate.",
        "first_six_pass_subtotal": first_subtotal,
        "second_six_passes": [
            {
                "pass": 7,
                "label": additions[0][0],
                "word_meanings": additions[0][1],
            },
            {
                "pass": 8,
                "label": "Classification of 87 conditioned krt identifiers",
                "word_meanings": 0,
                "note": "Classification pass; it admits no words by itself.",
            },
            *[
                {"pass": number, "label": label, "word_meanings": value}
                for number, (label, value) in enumerate(additions[1:], start=9)
            ],
        ],
        "bounded_word_meaning_subtotal": subtotal,
        "not_a_complete_sanskrit_vocabulary_total": True,
        "domain": "laukika_generation_mode_over_current_base_inventory",
        "vedic_boundary": "Nineteen Vedic-only krt identifiers and accent-sensitive formations remain reserved for a separate is_chandasi=True ledger. A separate domain audit removes descendants of eleven base meanings already documented as Vedic-only from the current known laukika subtotal.",
        "remaining_major_layers": [
            "Vedic-only and accent-sensitive formations in a separate domain ledger",
            "the remaining conditioned krt operations after source-level semantic classification",
            "three or more upasargas and other bounded operation orderings",
            "a sourced Sanskrit nominal-base inventory and broader taddhita classification",
            "namadhatus, feminine formations, compounds, and further nominal derivations",
            "tin and sup inflection, reported separately from word-meanings",
        ],
        "publication_status": "research_subtotal_only_not_deployed",
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in FILES.values()},
    }
    (RESULTS / "twelve_pass_expansion_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# Twelve-Pass Generativity Expansion", "",
        f"The first six passes established **{first_subtotal:,}** bounded word-meanings. The next six classify the remaining ordinary कृत्प्रत्यय identifiers, add four wider कृदन्त and अव्यय layers, and establish a small तद्धित pilot. Together they produce **{subtotal:,} bounded word-meanings under laukika generation mode**.", "",
        "| Pass | Completed layer | Added word-meanings |", "|---:|---|---:|",
    ]
    for row in report["second_six_passes"]:
        lines.append(f"| {row['pass']} | {row['label']} | {row['word_meanings']:,} |")
    lines.extend([
        f"|  | **Twelve-pass bounded subtotal** | **{subtotal:,}** |", "",
        "This is not a complete Sanskrit vocabulary total. It counts distinct admitted words or meanings under declared operations. It does not merge homographs, multiply alternative surface forms, or use dictionary attestation as a gate where a productive rule licenses a formation.", "",
        "## Domain Boundary", "",
        "The nineteen Vedic-only कृत्प्रत्यय identifiers remain outside this run. The shared base inventory does, however, contain eleven meanings already documented as Vedic-only. The separate [domain-boundary audit](domain_boundary_audit.md) removes those meanings and all of their unmixed descendants from the current known laukika subtotal. A later Vedic pass must use the engine's Vedic mode, retain accent where relevant, and report its results separately before any combined figure is considered.", "",
        "## Still Outside the Boundary", "",
    ])
    lines.extend(f"- {item}" for item in report["remaining_major_layers"])
    lines.extend(["", "The manuscript's published calculation remains unchanged pending author review.", ""])
    (RESULTS / "twelve_pass_expansion_summary.md").write_text("\n".join(lines))
    print(f"Reconciled twelve passes: {subtotal} bounded word-meanings under laukika generation mode.")


if __name__ == "__main__":
    main()
