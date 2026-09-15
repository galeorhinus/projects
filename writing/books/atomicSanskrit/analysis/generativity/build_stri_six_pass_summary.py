#!/usr/bin/env python3
"""Pass 6: reconcile and present the six stri-pratyaya passes."""

from __future__ import annotations

import csv
import json

from vidyut.lipi import Scheme, transliterate

from stri_common import RESULTS, project_path, sha256


INPUTS = (
    RESULTS / "stri_suffix_inventory.json",
    RESULTS / "stri_source_examples.json",
    RESULTS / "stri_eligibility.json",
    RESULTS / "stri_verification.json",
    RESULTS / "stri_reconciliation.json",
)
LEDGER = RESULTS / "stri_ledger.csv"
SUFFIX_DISPLAY = {
    "cAp": "चाप् (*cāp*)",
    "wAp": "टाप् (*ṭāp*)",
    "qAp": "डाप् (*ḍāp*)",
    "NIn": "ङीन् (*ṅīn*)",
    "NIp": "ङीप् (*ṅīp*)",
    "NIz": "ङीष् (*ṅīṣ*)",
    "UN": "ऊङ् (*ūṅ*)",
}


def deva(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Devanagari)


def iast(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Iast)


def main() -> None:
    inventory, source, eligibility, verification, reconciliation = [json.loads(path.read_text()) for path in INPUTS]
    if eligibility["unique_source_demonstrated_inputs"] != verification["candidate_relations"]:
        raise ValueError("Eligibility and verification counts disagree")
    if verification["verified_stri_derivations"] != reconciliation["additional_stri_word_meanings"]:
        raise ValueError("Verification and reconciliation counts disagree")
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    by_input = {row["input_form_slp1"]: row for row in rows}
    wanted = [form for form in ("aja", "kartf", "gOra", "indra", "SvaSura") if form in by_input]

    report = {
        "date": "2026-09-13",
        "passes_completed": 6,
        "pinned_suffix_identifiers": inventory["pinned_suffix_identifiers"],
        "active_source_assertions": source["active_assertions"],
        "unique_source_demonstrated_inputs": eligibility["unique_source_demonstrated_inputs"],
        "verified_stri_derivations": verification["verified_stri_derivations"],
        "inflection_only_relations_not_admitted": verification["inflection_only_relations_not_admitted"],
        "engine_mismatches_not_admitted": verification["engine_mismatches_not_admitted"],
        "additional_stri_word_meanings": reconciliation["additional_stri_word_meanings"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "inputs": {project_path(path): sha256(path) for path in (*INPUTS, LEDGER)},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "stri_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Six-Pass स्त्रीप्रत्ययः Expansion", "",
        "This block counts source-demonstrated feminine derivations without treating grammatical gender as a universal multiplier.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | Inventory all {inventory['pinned_suffix_identifiers']} स्त्रीप्रत्यय identifiers exposed by the pinned engine. |",
        f"| 2 | Extract {source['active_assertions']} active assertions and retain {source['ignored_assertions']} ignored assertions outside the candidate set. |",
        f"| 3 | Collapse repetition into {eligibility['unique_source_demonstrated_inputs']} unique source-demonstrated nominal inputs. |",
        f"| 4 | Verify {verification['verified_stri_derivations']} actual feminine derivations through Vidyut; separate {verification['inflection_only_relations_not_admitted']} inflection-only inputs and {verification['engine_mismatches_not_admitted']} generic-constructor mismatches. |",
        f"| 5 | Admit {reconciliation['additional_stri_word_meanings']} feminine word-meanings without counting their nominative evidence as inflection. |",
        f"| 6 | Raise the combined bounded subtotal to **{reconciliation['combined_bounded_word_meaning_subtotal']:,} word-meanings**. |", "",
        "## Examples", "",
        "| Input | Feminine nominative evidence | Suffix path |", "|---|---|---|",
    ]
    for form in wanted:
        row = by_input[form]
        outputs = ", ".join(f"{deva(x)} (*{iast(x)}*)" for x in row["expected_nominative_forms_slp1"].split(";"))
        suffix_display = ", ".join(SUFFIX_DISPLAY[x] for x in row["applied_stri_suffixes"].split(";") if x)
        lines.append(f"| {deva(form)} (*{iast(form)}*) | {outputs} | {suffix_display} |")
    lines.extend([
        "", "## Boundary", "",
        "The subtotal is deliberately narrow. It does not multiply स्त्रीप्रत्ययः across the 794,078-meaning nominal inventory, infer lexical eligibility from spelling, count already-feminine bases again, count ignored tests, or count case and number forms. A later broader pass would require semantic classes for the nominal inputs rather than a mechanical gender switch.", "",
    ])
    (RESULTS / "stri_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six stri passes complete; combined bounded subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()
