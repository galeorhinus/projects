#!/usr/bin/env python3
"""Capacity pass 5: locally derive a stratified sample and retain rule histories."""

from __future__ import annotations

import csv
import json
import subprocess

from samasa_capacity_common import RESULTS, VERIFIER, load_config, stable_id


PAIRS = (
    ("kuntI", "vatsa"),
    ("madra", "suparRA"),
    ("vinatA", "kuntI"),
    ("vatsa", "madra"),
)


def main() -> None:
    if not VERIFIER.exists():
        raise RuntimeError(f"Build the pinned Rust verifier first: {VERIFIER}")
    config = load_config()
    requests = []
    for relation in config["counted_relations"]:
        for first, second in PAIRS:
            request_id = stable_id("capacity-sample", relation["relation_id"], first, second)
            requests.append({
                "sample_id": request_id,
                "relation_id": relation["relation_id"],
                "vidyut_helper": relation["vidyut_helper"],
                "first_member_slp1": first,
                "second_member_slp1": second,
                "semantic_relation": relation["meaning_template"],
                "rule_refs": ";".join(relation["rule_refs"]),
            })
    payload = "".join(
        f"{row['sample_id']}\t{row['vidyut_helper']}\t{row['first_member_slp1']};{row['second_member_slp1']}\n"
        for row in requests
    )
    run = subprocess.run([str(VERIFIER)], input=payload, text=True, capture_output=True, check=True)
    generated = {row["id"]: row for row in map(json.loads, filter(None, run.stdout.splitlines()))}
    rows = []
    for request in requests:
        record = generated[request["sample_id"]]
        if not record["derivations"]:
            raise ValueError(f"Vidyut generated no form for {request['sample_id']}")
        rows.append({
            **request,
            "generated_forms_slp1": ";".join(x["form_slp1"] for x in record["derivations"]),
            "output_variant_count": len(record["derivations"]),
            "derivation_paths_json": json.dumps(record["derivations"], ensure_ascii=False, separators=(",", ":")),
            "verification_status": "locally_regenerated_at_pinned_vidyut_commit",
        })
    output = RESULTS / "samasa_capacity_sample.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    by_form = {}
    for row in rows:
        for form in row["generated_forms_slp1"].split(";"):
            by_form.setdefault(form, set()).add(row["relation_id"])
    collisions = {form: sorted(relations) for form, relations in by_form.items() if len(relations) > 1}
    report = {
        "date": "2026-09-14",
        "sample_relations": len(rows),
        "locally_regenerated_relations": len(rows),
        "zero_output_relations": 0,
        "same_spelling_relation_groups": len(collisions),
        "same_spelling_relations": collisions,
        "derivation_paths_retained": True,
    }
    (RESULTS / "samasa_capacity_sample.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "samasa_capacity_sample.md").write_text("\n".join([
        "# समासः Capacity Sample", "",
        f"Pinned Vidyut regenerated all **{len(rows)}** sampled relations. Each output retains its complete rule history.", "",
        f"The sample contains **{len(collisions)}** written-form groups shared by more than one compound relation. Those relations remain separate meanings.", "",
    ]))
    print(f"Regenerated {len(rows)} depth-one sample relations.")


if __name__ == "__main__":
    main()
