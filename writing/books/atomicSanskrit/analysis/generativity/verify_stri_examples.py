#!/usr/bin/env python3
"""Pass 4: verify source-demonstrated feminine derivations through Vidyut."""

from __future__ import annotations

from collections import Counter
import csv
import importlib.metadata
import json

from vidyut.prakriya import Linga, Pada, Pratipadika, Vacana, Vibhakti, Vyakarana

from stri_common import RESULTS, project_path, sha256


SOURCE = RESULTS / "stri_eligible_inputs.csv"
INVENTORY = RESULTS / "stri_suffix_inventory.csv"


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This verification requires Vidyut 0.4.0")
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    with INVENTORY.open(newline="", encoding="utf-8") as handle:
        suffixes = {row["engine_identifier"] for row in csv.DictReader(handle)}

    grammar = Vyakarana(log_steps=True, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for row in source_rows:
        expected = set(row["expected_nominative_forms_slp1"].split(";"))
        generated = {}
        error = ""
        try:
            argument = Pada.Subanta(
                Pratipadika.basic(row["input_form_slp1"]),
                Linga.Stri,
                Vibhakti.Prathama,
                Vacana.Eka,
            )
            for result in grammar.derive(argument):
                applied_suffixes = set()
                applied_rules = set()
                for step in result.history:
                    terms = set(step.result)
                    found = suffixes.intersection(terms)
                    if found and step.code.startswith("4.1"):
                        applied_suffixes.update(found)
                        applied_rules.add(step.code)
                generated[result.text] = {
                    "suffixes": sorted(applied_suffixes),
                    "rules": sorted(applied_rules),
                }
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"

        actual = set(generated)
        missing = sorted(expected - actual)
        expected_with_suffix = sorted(form for form in expected.intersection(actual) if generated[form]["suffixes"])
        applied_suffixes = sorted({suffix for form in expected_with_suffix for suffix in generated[form]["suffixes"]})
        applied_rules = sorted({rule for form in expected_with_suffix for rule in generated[form]["rules"]})
        if missing:
            status = "engine_mismatch_not_admitted"
        elif not expected_with_suffix:
            status = "inflection_only_no_stri_derivation"
        else:
            status = "verified_stri_derivation"
        rows.append({
            **row,
            "generated_nominative_forms_slp1": ";".join(sorted(actual)),
            "generated_variant_count": len(actual),
            "missing_expected_forms_slp1": ";".join(missing),
            "expected_forms_with_stri_suffix_slp1": ";".join(expected_with_suffix),
            "applied_stri_suffixes": ";".join(applied_suffixes),
            "applied_rule_refs": ";".join(applied_rules),
            "engine_error": error,
            "verification_status": status,
        })

    output = RESULTS / "stri_verification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["verification_status"] for row in rows)
    report = {
        "date": "2026-09-13",
        "candidate_relations": len(rows),
        "verified_stri_derivations": counts["verified_stri_derivation"],
        "inflection_only_relations_not_admitted": counts["inflection_only_no_stri_derivation"],
        "engine_mismatches_not_admitted": counts["engine_mismatch_not_admitted"],
        "suffixes_observed": sorted({suffix for row in rows for suffix in row["applied_stri_suffixes"].split(";") if suffix}),
        "verification_policy": "The expected nominative forms must be reproduced by Vidyut 0.4.0, and at least one expected path must show an inserted स्त्रीप्रत्यय. Nominative inflection without a feminine derivation does not create a lexical row.",
        "engine": {"name": "Vidyut", "version": "0.4.0"},
        "inputs": {project_path(path): sha256(path) for path in (SOURCE, INVENTORY)},
        "publication_status": "research_verification_only_not_deployed",
    }
    (RESULTS / "stri_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "stri_verification.md").write_text("\n".join([
        "# स्त्रीप्रत्ययः Engine Verification", "",
        f"Vidyut 0.4.0 verifies **{counts['verified_stri_derivation']}** source-demonstrated feminine derivations. **{counts['inflection_only_no_stri_derivation']}** inputs merely decline in the feminine without adding a स्त्रीप्रत्यय, and **{counts['engine_mismatch_not_admitted']}** source expectations are not reproduced through the generic Python constructor. Both groups remain outside the lexical subtotal.", "",
    ]))
    print(f"Verified {counts['verified_stri_derivation']} stri derivations; {counts['inflection_only_no_stri_derivation']} inflection-only and {counts['engine_mismatch_not_admitted']} mismatches excluded.")


if __name__ == "__main__":
    main()
