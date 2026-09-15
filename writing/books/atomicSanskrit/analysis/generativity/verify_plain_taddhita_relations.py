#!/usr/bin/env python3
"""Verify eligible plain taddhita word forms with pinned Vidyut."""

from __future__ import annotations

from collections import Counter
import csv
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Pratipadika, Taddhita, Vyakarana

from taddhita_conditioned_common import HERE, RESULTS, sha256


SOURCE = RESULTS / "plain_taddhita_eligible_relations.csv"


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This verification requires Vidyut 0.4.0")
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))

    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for row in source_rows:
        expected = set(row["expected_output_forms_slp1"].split(";"))
        generated_by_suffix = {}
        errors = []
        for suffix_name in row["taddhita_source_variants"].split(";"):
            try:
                base = Pratipadika.basic(row["input_form_slp1"])
                suffix = getattr(Taddhita, suffix_name)
                generated_by_suffix[suffix_name] = sorted({
                    result.text
                    for result in grammar.derive(Pratipadika.taddhitanta(base, suffix))
                })
            except Exception as exc:
                generated_by_suffix[suffix_name] = []
                errors.append(f"{suffix_name}:{type(exc).__name__}:{exc}")
        generated = {
            form
            for forms in generated_by_suffix.values()
            for form in forms
        }
        reproduced = expected & generated
        missing = expected - generated
        if not reproduced:
            status = "engine_mismatch_not_admitted"
        elif missing:
            status = "verified_relation_partial_variant_coverage"
        else:
            status = "verified"
        rows.append({
            **row,
            "generated_output_forms_slp1": ";".join(sorted(generated)),
            "generated_by_suffix_json": json.dumps(generated_by_suffix, separators=(",", ":")),
            "missing_expected_forms_slp1": ";".join(sorted(missing)),
            "additional_engine_forms_slp1": ";".join(sorted(generated - expected)),
            "engine_errors": " | ".join(errors),
            "verification_status": status,
        })

    output = RESULTS / "plain_taddhita_verification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(row["verification_status"] for row in rows)
    verified = counts["verified"] + counts["verified_relation_partial_variant_coverage"]
    report = {
        "date": "2026-09-13",
        "eligible_relations": len(rows),
        "verified_relations": verified,
        "fully_verified_relations": counts["verified"],
        "relations_with_partial_variant_coverage": counts["verified_relation_partial_variant_coverage"],
        "engine_mismatches_not_admitted": counts["engine_mismatch_not_admitted"],
        "engine": {
            "name": "Vidyut",
            "version": "0.4.0",
            "commit": "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32"
        },
        "verification_boundary": "The engine verifies formation under the named suffix. The archived rule page, not the unconditioned engine call, supplies the semantic relation.",
        "inputs": {
            str(path.relative_to(HERE.parents[1])): sha256(path)
            for path in (SOURCE, Path(__file__))
        },
        "publication_status": "research_verification_only_not_deployed",
    }
    (RESULTS / "plain_taddhita_verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "plain_taddhita_verification.md").write_text(
        "# Plain तद्धित Verification\n\n"
        f"Vidyut 0.4.0 reproduces **{verified} of {len(rows)}** eligible word-meaning relations. "
        f"{counts['verified_relation_partial_variant_coverage']} relations have incomplete optional-variant coverage, and "
        f"{counts['engine_mismatch_not_admitted']} have no reproduced source form and remain outside the count.\n\n"
        "This verifies the formation under the named suffix. The archived rule page supplies the meaning; an unconditioned engine call does not.\n"
    )
    print(f"Verified {verified} of {len(rows)} eligible plain taddhita relations.")


if __name__ == "__main__":
    main()
