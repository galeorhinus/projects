#!/usr/bin/env python3
"""Pass 4: reproduce every generated compound-input stack row in a separate run."""

from __future__ import annotations

import csv
import json

from vidyut.prakriya import Vyakarana

from build_compound_stack_ledger import derive_forms
from compound_stack_common import RESULTS, project_path, read_csv, sha256


LEDGER = RESULTS / "compound_stack_candidates.csv"
VERIFICATION = RESULTS / "compound_stack_verification.csv"
FIELDS = (
    "derived_word_meaning_id", "operation_id", "expected_forms_slp1",
    "regenerated_forms_slp1", "verification_status",
)


def main() -> None:
    rows = read_csv(LEDGER)
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    verified = 0
    with VERIFICATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            regenerated = derive_forms(grammar, row)
            expected = tuple(row["output_forms_slp1"].split(";"))
            status = "verified" if regenerated == expected else "mismatch"
            writer.writerow({
                "derived_word_meaning_id": row["derived_word_meaning_id"],
                "operation_id": row["operation_id"],
                "expected_forms_slp1": ";".join(expected),
                "regenerated_forms_slp1": ";".join(regenerated),
                "verification_status": status,
            })
            verified += status == "verified"
    if verified != len(rows):
        raise ValueError(f"Only {verified} of {len(rows)} stack relations reproduced")
    report = {
        "date": "2026-09-14",
        "candidate_relations": len(rows),
        "verified_relations": verified,
        "mismatches": len(rows) - verified,
        "verification_scope": "Separate exact output-set regeneration from every admitted source compound and declared second operation.",
        "inputs": {project_path(path): sha256(path) for path in (LEDGER, VERIFICATION, __import__("pathlib").Path(__file__))},
    }
    (RESULTS / "compound_stack_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "compound_stack_verification.md").write_text("\n".join([
        "# Compound-Input Stack Verification", "",
        f"A separate verification pass reproduces the recorded output sets for all **{verified}** candidate relations. The तद्धित and नामधातुः rows use Vidyut 0.4.0; the नञ् rows use the already source-tested surface rules.", "",
    ]))
    print(f"Verified {verified} compound-input stack relations.")


if __name__ == "__main__":
    main()
