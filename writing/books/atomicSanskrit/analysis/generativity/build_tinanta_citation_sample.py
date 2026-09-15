#!/usr/bin/env python3
"""Tinanta pass 5: regenerate ten citation coordinates for every recipe class."""

from __future__ import annotations

import csv
import json

from vidyut.prakriya import DhatuPada, Lakara, Pada, Prayoga, Purusha, Vacana, Vyakarana

from tinanta_common import CONFIG, RESULTS, construct_sample_dhatu, load_entries, result_paths


FIELDS = (
    "verbal_word_meaning_id", "source_layer", "lakara_id", "lakara_display",
    "plain_function", "purusha", "vacana", "parasmaipada_forms_slp1",
    "atmanepada_forms_slp1", "all_forms_slp1", "output_variant_count",
    "generation_status", "derivation_paths_json",
)


def derive(grammar, dhatu, lakara, dhatu_pada):
    request = Pada.Tinanta(
        dhatu, Prayoga.Kartari, lakara, Purusha.Prathama, Vacana.Eka,
        dhatu_pada=dhatu_pada,
    )
    results = list(grammar.derive(request))
    return sorted({result.text for result in results}), result_paths(results)


def main() -> None:
    config = json.loads(CONFIG.read_text())
    with (RESULTS / "tinanta_verbal_member_sample.csv").open(newline="", encoding="utf-8") as handle:
        samples = list(csv.DictReader(handle))
    entries = load_entries()
    grammar = Vyakarana(log_steps=True, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for sample in samples:
        dhatu = construct_sample_dhatu(sample, entries)
        for item in config["laukika_lakaras"]:
            lakara = getattr(Lakara, item["vidyut"])
            parasmai, p_paths = derive(grammar, dhatu, lakara, DhatuPada.Parasmaipada)
            atmane, a_paths = derive(grammar, dhatu, lakara, DhatuPada.Atmanepada)
            forms = sorted(set(parasmai) | set(atmane))
            rows.append({
                "verbal_word_meaning_id": sample["verbal_word_meaning_id"],
                "source_layer": sample["source_layer"], "lakara_id": item["id"],
                "lakara_display": item["display"], "plain_function": item["plain_function"],
                "purusha": "Prathama", "vacana": "Eka",
                "parasmaipada_forms_slp1": ";".join(parasmai),
                "atmanepada_forms_slp1": ";".join(atmane),
                "all_forms_slp1": ";".join(forms), "output_variant_count": len(forms),
                "generation_status": "locally_regenerated" if forms else "engine_zero_unresolved",
                "derivation_paths_json": json.dumps({"parasmaipada": p_paths, "atmanepada": a_paths}, ensure_ascii=False),
            })
    with (RESULTS / "tinanta_citation_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    generated = sum(row["generation_status"] == "locally_regenerated" for row in rows)
    report = {
        "date": "2026-09-14", "sample_records": len(samples),
        "sample_reconstruction_classes": len({row["source_layer"] for row in samples}),
        "requested_citation_cells": len(rows), "locally_regenerated_cells": generated,
        "engine_zero_unresolved_cells": len(rows) - generated,
        "pada_output_profile": {
            "parasmaipada_only": sum(bool(row["parasmaipada_forms_slp1"]) and not row["atmanepada_forms_slp1"] for row in rows),
            "atmanepada_only": sum(bool(row["atmanepada_forms_slp1"]) and not row["parasmaipada_forms_slp1"] for row in rows),
            "both": sum(bool(row["parasmaipada_forms_slp1"]) and bool(row["atmanepada_forms_slp1"]) for row in rows),
            "neither": sum(not row["all_forms_slp1"] for row in rows),
        },
        "full_rule_paths_recorded": True,
    }
    (RESULTS / "tinanta_citation_sample.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 5: Citation-Form Sample", "", f"The local pinned engine received **{len(rows)} requests**: ten लकार citation coordinates for one verbal meaning from each of eight reconstruction classes.", "", "| Result | Cells |", "|---|---:|", f"| Locally regenerated | {generated} |", f"| Engine zero, retained as unresolved | {len(rows) - generated} |", "", "Every generated form retains its complete rule path. The sample tests the reconstruction recipes; it does not estimate a surface-form total for all 45 million cells.", ""]
    (RESULTS / "tinanta_citation_sample.md").write_text("\n".join(lines))
    print(f"Regenerated {generated} of {len(rows)} sampled citation cells.")


if __name__ == "__main__":
    main()
