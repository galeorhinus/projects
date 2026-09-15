#!/usr/bin/env python3
"""Capacity pass 7: classify one post-compound operation and one recursive layer."""

from __future__ import annotations

import json

from samasa_capacity_common import ANALYSIS, CONFIG, RESULTS, load_config, project_path, sha256


STACK_CONFIG = ANALYSIS / "compound_stack_operations.json"


def main() -> None:
    config = load_config()
    stack = json.loads(STACK_CONFIG.read_text())
    operations = {row["operation_id"]: row for row in stack["operations"]}
    expected = config["post_compound_operations"]
    missing = [operation for operation in expected if operation not in operations]
    if missing:
        raise ValueError(f"Post-compound operations absent from established stack: {missing}")
    report = {
        "date": config["date"],
        "post_compound_operation_count": len(expected),
        "post_compound_operations": [operations[operation] for operation in expected],
        "recursive_compound_relation_count": len(config["counted_relations"]),
        "recursive_compound_relations": [row["relation_id"] for row in config["counted_relations"]],
        "maximum_compound_depth": config["depth_two_boundary"]["maximum_compound_depth"],
        "two_compounds_as_members": config["depth_two_boundary"]["two_depth_one_compounds_as_members"],
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, STACK_CONFIG)},
    }
    (RESULTS / "samasa_reuse_classification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "samasa_reuse_classification.md").write_text("\n".join([
        "# Post-Compound and Recursive Classification", "",
        f"The next layer permits **{len(expected)}** already established operations after a depth-one compound. It also permits one compound to join one original nominal meaning under the same four broad compound relations.", "",
        "It does not join two compounds, reopen the result again, or claim unrestricted recursion.", "",
    ]))
    print(f"Classified {len(expected)} post-compound operations and one recursive layer.")


if __name__ == "__main__":
    main()
