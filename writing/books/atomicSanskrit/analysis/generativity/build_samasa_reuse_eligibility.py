#!/usr/bin/env python3
"""Capacity pass 8: count one established operation over each depth-one compound."""

from __future__ import annotations

import json

from samasa_capacity_common import RESULTS, project_path, sha256


DEPTH_ONE = RESULTS / "samasa_capacity_eligibility.json"
CLASSIFICATION = RESULTS / "samasa_reuse_classification.json"


def main() -> None:
    depth_one = json.loads(DEPTH_ONE.read_text())
    classification = json.loads(CLASSIFICATION.read_text())
    compounds = depth_one["eligible_depth_one_relation_slots"]
    operations = classification["post_compound_operation_count"]
    total = compounds * operations
    report = {
        "date": "2026-09-14",
        "depth_one_compound_meaning_slots": compounds,
        "operations_per_compound": operations,
        "post_compound_derivational_slots": total,
        "formula": "C1 x O",
        "maximum_compound_depth": 1,
        "maximum_following_operations": 1,
        "materialized_all_outputs": False,
        "inputs": {project_path(path): sha256(path) for path in (DEPTH_ONE, CLASSIFICATION)},
    }
    (RESULTS / "samasa_reuse_eligibility.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / "samasa_reuse_eligibility.md").write_text("\n".join([
        "# One Operation After a Compound", "",
        f"Each of the **{compounds:,}** depth-one compound slots can become the input to **{operations}** already established operations under the declared model.", "",
        f"This creates **{total:,} post-compound derivational slots**. The result is symbolic and is not materialized as a multi-petabyte ledger.", "",
    ]))
    print(f"Declared {total:,} post-compound derivational slots.")


if __name__ == "__main__":
    main()
