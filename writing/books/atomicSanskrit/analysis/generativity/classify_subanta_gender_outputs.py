#!/usr/bin/env python3
"""Subanta pass 8: state the gender and output-counting policy."""

from __future__ import annotations

import json

from vidyut.prakriya import Linga

from subanta_common import CONFIG, RESULTS, SAMPLES, project_path, read_json, sha256


def main() -> None:
    config = read_json(CONFIG)
    engine_genders = [item.name for item in Linga.choices()]
    profile = {name: sum(sample["linga"] == name for sample in SAMPLES) for name in engine_genders}
    report = {
        "date": "2026-09-14", "passes_completed": 8,
        "engine_gender_values": engine_genders,
        "sample_gender_profile": profile,
        "automatic_gender_multiplier": 1,
        "gender_is_generation_attribute": True,
        "full_inventory_gender_assignments_materialized": False,
        "agreement_gender_expansion_included": config["agreement_gender_expansion_included"],
        "policy": config["gender_policy"],
        "interpretation": (
            "Each counted name meaning receives one relation-number matrix under its lexical or "
            "contextually selected gender. Agreement across additional genders remains a separate "
            "grammatical expansion and does not create new lexical meanings."
        ),
        "inputs": {project_path(CONFIG): sha256(CONFIG), project_path(RESULTS / "subanta_nominal_member_sample.csv"): sha256(RESULTS / "subanta_nominal_member_sample.csv")},
    }
    (RESULTS / "subanta_gender_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 8: Gender and Output Policy", "",
        "Gender guides the generated form. It does not automatically triple either the lexical meaning or the 24-cell relation-number matrix.", "",
        "The sample includes masculine, feminine, and neuter stems. A later agreement analysis may count additional gender-conditioned forms for words that can modify nouns across genders; that expansion is not included here.", "",
    ]
    (RESULTS / "subanta_gender_classification.md").write_text("\n".join(lines))
    print("Classified gender as an output attribute with no automatic multiplier.")


if __name__ == "__main__":
    main()
