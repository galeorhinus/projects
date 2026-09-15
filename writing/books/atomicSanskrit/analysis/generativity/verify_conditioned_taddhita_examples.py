#!/usr/bin/env python3
"""Verify source-conditioned taddhita examples with pinned Vidyut."""

from __future__ import annotations

from collections import Counter
import csv
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Pratipadika, Taddhita, Vyakarana

from taddhita_conditioned_common import HERE, RESULTS, sha256, stable_id


SOURCE = RESULTS / "conditioned_taddhita_inputs.csv"


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This verification requires Vidyut 0.4.0")
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))

    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for row in source_rows:
        expected = set(row["expected_output_forms_slp1"].split(";"))
        error = ""
        try:
            base = Pratipadika.basic(row["input_form_slp1"])
            suffix = getattr(Taddhita, row["taddhita_source_variant"])
            generated = sorted({
                result.text
                for result in grammar.derive(Pratipadika.taddhitanta(base, suffix))
            })
        except Exception as exc:
            generated = []
            error = f"{type(exc).__name__}: {exc}"
        missing = sorted(expected - set(generated))
        extra = sorted(set(generated) - expected)
        status = "verified" if not missing else "engine_mismatch_not_admitted"
        rows.append({
            **row,
            "generated_output_forms_slp1": ";".join(generated),
            "generated_output_variant_count": len(generated),
            "missing_expected_forms_slp1": ";".join(missing),
            "additional_unconditioned_engine_forms_slp1": ";".join(extra),
            "engine_error": error,
            "verification_status": status,
            "verified_word_meaning_id": stable_id(
                "verified-conditioned-taddhita", row["input_form_slp1"],
                row["semantic_context"], row["taddhita_source_variant"],
                row["expected_output_forms_slp1"],
            ) if status == "verified" else "",
        })

    output = RESULTS / "conditioned_taddhita_verification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    by_status = Counter(row["verification_status"] for row in rows)
    report = {
        "date": "2026-09-13",
        "candidate_relations": len(rows),
        "verified_relations": by_status["verified"],
        "engine_mismatches_not_admitted": by_status["engine_mismatch_not_admitted"],
        "relations_with_additional_unconditioned_engine_forms": sum(bool(row["additional_unconditioned_engine_forms_slp1"]) for row in rows),
        "verification_policy": "The expected forms recorded by the pinned Kāśikā test must be a subset of the forms produced by Vidyut 0.4.0 without an artha filter. Extra forms are diagnostics, not extra word-meanings.",
        "engine": {"name": "Vidyut", "version": "0.4.0"},
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (SOURCE, Path(__file__))},
        "publication_status": "research_verification_only_not_deployed",
    }
    (RESULTS / "conditioned_taddhita_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Conditioned तद्धित Engine Verification", "",
        f"Vidyut 0.4.0 reproduces the source-recorded form set for **{report['verified_relations']:,} of {report['candidate_relations']:,}** unique conditioned relations. The remaining {report['engine_mismatches_not_admitted']:,} stay outside the count.", "",
        "The Python binding does not pass the semantic-context enum into the derivation. The test's expected form must therefore appear among the engine's unrestricted outputs. Any additional unrestricted output remains a diagnostic variant and does not create another word-meaning.", "",
    ]
    (RESULTS / "conditioned_taddhita_verification.md").write_text("\n".join(lines))
    print(f"Verified {report['verified_relations']} of {report['candidate_relations']} conditioned relations; {report['engine_mismatches_not_admitted']} mismatches remain outside.")


if __name__ == "__main__":
    main()
