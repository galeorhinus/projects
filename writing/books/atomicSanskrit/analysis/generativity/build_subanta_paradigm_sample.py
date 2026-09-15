#!/usr/bin/env python3
"""Subanta pass 9: regenerate complete relation-number paradigms for samples."""

from __future__ import annotations

import csv
import json

from vidyut.prakriya import Linga, Pada, Vacana, Vibhakti, Vyakarana

from subanta_common import CONFIG, RESULTS, SAMPLES, pratipadika_for, read_json, result_paths


FIELDS = (
    "sample_id", "display", "source_file", "source_word_meaning_id",
    "stem_slp1", "constructor", "linga", "relation_id", "relation_display",
    "plain_function", "number_id", "number_display", "generated_forms_slp1",
    "output_variant_count", "generation_status", "derivation_paths_json",
)


def main() -> None:
    config = read_json(CONFIG)
    grammar = Vyakarana(log_steps=True, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for sample in SAMPLES:
        stem = pratipadika_for(sample)
        linga = getattr(Linga, sample["linga"])
        for relation in config["relations"]:
            for number in config["numbers"]:
                request = Pada.Subanta(
                    stem, linga, getattr(Vibhakti, relation["vidyut"]),
                    getattr(Vacana, number["vidyut"]),
                )
                results = list(grammar.derive(request))
                forms = sorted({result.text for result in results})
                rows.append({
                    **{key: sample[key] for key in (
                        "sample_id", "display", "source_file", "source_word_meaning_id",
                        "stem_slp1", "constructor", "linga",
                    )},
                    "relation_id": relation["id"], "relation_display": relation["display"],
                    "plain_function": relation["plain_function"],
                    "number_id": number["id"], "number_display": number["display"],
                    "generated_forms_slp1": ";".join(forms), "output_variant_count": len(forms),
                    "generation_status": "locally_regenerated" if forms else "engine_zero_unresolved",
                    "derivation_paths_json": json.dumps(result_paths(results), ensure_ascii=False),
                })
    with (RESULTS / "subanta_paradigm_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    generated = sum(row["generation_status"] == "locally_regenerated" for row in rows)
    report = {
        "date": "2026-09-14", "passes_completed": 9,
        "sample_name_meanings": len(SAMPLES),
        "semantic_cells_requested": len(rows),
        "semantic_cells_locally_regenerated": generated,
        "engine_zero_unresolved_cells": len(rows) - generated,
        "generated_surface_form_links": sum(int(row["output_variant_count"]) for row in rows),
        "full_inflection_rule_paths_recorded": True,
    }
    (RESULTS / "subanta_paradigm_sample.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामरूप Pass 9: Full-Paradigm Sample", "",
        f"The local engine regenerated **{generated} of {len(rows)} semantic cells** across eight source-backed meanings, eight relations, and three number values.", "",
        "The samples include masculine, feminine, and neuter stems as well as regular and less regular ending patterns. Every generated variant retains its inflection rule path from the admitted stem.", "",
    ]
    (RESULTS / "subanta_paradigm_sample.md").write_text("\n".join(lines))
    print(f"Regenerated {generated} of {len(rows)} full-paradigm sample cells.")


if __name__ == "__main__":
    main()
