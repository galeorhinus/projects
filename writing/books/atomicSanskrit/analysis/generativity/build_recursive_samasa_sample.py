#!/usr/bin/env python3
"""Capacity pass 10: derive recursive samples with explicit parent records."""

from __future__ import annotations

import csv
import json
import subprocess

from samasa_capacity_common import RESULTS, VERIFIER, load_config, stable_id


DEPTH_ONE_SAMPLE = RESULTS / "samasa_capacity_sample.csv"


def main() -> None:
    if not VERIFIER.exists():
        raise RuntimeError(f"Build the pinned Rust verifier first: {VERIFIER}")
    config = load_config()
    with DEPTH_ONE_SAMPLE.open(newline="", encoding="utf-8") as handle:
        depth_one = list(csv.DictReader(handle))
    parent_by_relation = {}
    for row in depth_one:
        parent_by_relation.setdefault(row["relation_id"], row)
    requests = []
    for relation in config["counted_relations"]:
        parent = parent_by_relation[relation["relation_id"]]
        compound_form = parent["generated_forms_slp1"].split(";")[0]
        for placement in ("compound_first", "compound_second") if relation["pair_model"].startswith("ordered") else ("compound_first",):
            first, second = ((compound_form, "madra") if placement == "compound_first" else ("madra", compound_form))
            sample_id = stable_id("recursive-sample", relation["relation_id"], placement, first, second)
            requests.append({
                "sample_id": sample_id,
                "parent_sample_id": parent["sample_id"],
                "relation_id": relation["relation_id"],
                "vidyut_helper": relation["vidyut_helper"],
                "placement": placement,
                "first_member_slp1": first,
                "second_member_slp1": second,
                "semantic_relation": relation["meaning_template"],
            })
    payload = "".join(
        f"{row['sample_id']}\t{row['vidyut_helper']}\t{row['first_member_slp1']};{row['second_member_slp1']}\n"
        for row in requests
    )
    run = subprocess.run([str(VERIFIER)], input=payload, text=True, capture_output=True, check=True)
    generated = {row["id"]: row for row in map(json.loads, filter(None, run.stdout.splitlines()))}
    rows = []
    for request in requests:
        derivations = generated[request["sample_id"]]["derivations"]
        if not derivations:
            raise ValueError(f"Vidyut generated no recursive form for {request['sample_id']}")
        rows.append({
            **request,
            "generated_forms_slp1": ";".join(row["form_slp1"] for row in derivations),
            "output_variant_count": len(derivations),
            "derivation_paths_json": json.dumps(derivations, ensure_ascii=False, separators=(",", ":")),
            "verification_status": "locally_regenerated_at_pinned_vidyut_commit",
        })
    output = RESULTS / "recursive_samasa_sample.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": "2026-09-14",
        "recursive_sample_relations": len(rows),
        "locally_regenerated_relations": len(rows),
        "zero_output_relations": 0,
        "parent_links_retained": True,
        "derivation_paths_retained": True,
    }
    (RESULTS / "recursive_samasa_sample.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / "recursive_samasa_sample.md").write_text("\n".join([
        "# Recursive समासः Sample", "",
        f"Pinned Vidyut regenerated all **{len(rows)}** depth-two samples. Every record names its depth-one parent and preserves the second compound derivation's complete rule history.", "",
    ]))
    print(f"Regenerated {len(rows)} depth-two sample relations.")


if __name__ == "__main__":
    main()
