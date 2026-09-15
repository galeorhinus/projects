#!/usr/bin/env python3
"""Verify additional source-conditioned suffix relations with pinned Vidyut."""

from __future__ import annotations

from collections import Counter
import csv
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Pratipadika, Taddhita, Vyakarana

from taddhita_conditioned_common import HERE, RESULTS, sha256


SOURCE = RESULTS / "suffix_conditioned_relations.csv"


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
            generated = sorted({result.text for result in grammar.derive(Pratipadika.taddhitanta(base, suffix))})
        except Exception as exc:
            generated = []
            error = f"{type(exc).__name__}: {exc}"
        missing = sorted(expected - set(generated))
        reproduced = expected.intersection(generated)
        if not reproduced:
            status = "engine_mismatch_not_admitted"
        elif missing:
            status = "verified_relation_partial_variant_coverage"
        else:
            status = "verified"
        rows.append({
            **row,
            "generated_output_forms_slp1": ";".join(generated),
            "missing_expected_forms_slp1": ";".join(missing),
            "additional_engine_forms_slp1": ";".join(sorted(set(generated) - expected)),
            "engine_error": error,
            "verification_status": status,
        })

    output = RESULTS / "suffix_conditioned_verification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["verification_status"] for row in rows)
    verified = counts["verified"] + counts["verified_relation_partial_variant_coverage"]
    report = {
        "date": "2026-09-13",
        "candidate_relations": len(rows),
        "verified_relations": verified,
        "relations_with_partial_variant_coverage": counts["verified_relation_partial_variant_coverage"],
        "engine_mismatches_not_admitted": counts["engine_mismatch_not_admitted"],
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32"},
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (SOURCE, Path(__file__))},
        "publication_status": "research_verification_only_not_deployed",
    }
    (RESULTS / "suffix_conditioned_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "suffix_conditioned_verification.md").write_text(
        "# Additional Suffix Verification\n\n"
        f"Vidyut 0.4.0 reproduces **{verified} of {len(rows)}** source-conditioned relations. "
        f"For {counts['verified_relation_partial_variant_coverage']}, it reproduces the relation but not every source-recorded optional form. "
        f"The remaining {counts['engine_mismatch_not_admitted']} stay outside the count.\n"
    )
    print(f"Verified {verified} of {len(rows)} additional suffix relations.")


if __name__ == "__main__":
    main()
