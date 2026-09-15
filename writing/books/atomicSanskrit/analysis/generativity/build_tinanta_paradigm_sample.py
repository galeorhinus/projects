#!/usr/bin/env python3
"""Tinanta pass 9: regenerate full ten-lakara paradigms for three dhatus."""

from __future__ import annotations

import csv
import json

from vidyut.prakriya import DhatuPada, Lakara, Pada, Prayoga, Purusha, Vacana, Vyakarana

from tinanta_common import CONFIG, RESULTS, load_entries, result_paths


SAMPLES = (
    ("bhu", "01.0001", "⟪भू⟫ (bhū), to be or become"),
    ("kr", "08.0010", "⟪कृ⟫ (kṛ), to do or make"),
    ("edh", "01.0002", "⟪एध्⟫ (edh), to grow or prosper"),
)
FIELDS = (
    "sample_id", "source_code", "sample_display", "lakara_id", "lakara_display",
    "plain_function", "purusha", "vacana", "parasmaipada_forms_slp1",
    "atmanepada_forms_slp1", "all_forms_slp1", "output_variant_count",
    "generation_status", "derivation_paths_json",
)


def derive(grammar, dhatu, lakara, purusha, vacana, dhatu_pada):
    request = Pada.Tinanta(
        dhatu, Prayoga.Kartari, lakara, purusha, vacana,
        dhatu_pada=dhatu_pada,
    )
    results = list(grammar.derive(request))
    return sorted({result.text for result in results}), result_paths(results)


def main() -> None:
    config = json.loads(CONFIG.read_text())
    entries = load_entries()
    grammar = Vyakarana(log_steps=True, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for sample_id, source_code, display in SAMPLES:
        dhatu = entries[source_code].dhatu
        for item in config["laukika_lakaras"]:
            lakara = getattr(Lakara, item["vidyut"])
            for purusha_name in config["full_person_number_matrix"]["purushas"]:
                purusha = getattr(Purusha, purusha_name)
                for vacana_name in config["full_person_number_matrix"]["vacanas"]:
                    vacana = getattr(Vacana, vacana_name)
                    parasmai, p_paths = derive(grammar, dhatu, lakara, purusha, vacana, DhatuPada.Parasmaipada)
                    atmane, a_paths = derive(grammar, dhatu, lakara, purusha, vacana, DhatuPada.Atmanepada)
                    forms = sorted(set(parasmai) | set(atmane))
                    rows.append({
                        "sample_id": sample_id, "source_code": source_code,
                        "sample_display": display, "lakara_id": item["id"],
                        "lakara_display": item["display"], "plain_function": item["plain_function"],
                        "purusha": purusha_name, "vacana": vacana_name,
                        "parasmaipada_forms_slp1": ";".join(parasmai),
                        "atmanepada_forms_slp1": ";".join(atmane),
                        "all_forms_slp1": ";".join(forms), "output_variant_count": len(forms),
                        "generation_status": "locally_regenerated" if forms else "engine_zero_unresolved",
                        "derivation_paths_json": json.dumps({"parasmaipada": p_paths, "atmanepada": a_paths}, ensure_ascii=False),
                    })
    with (RESULTS / "tinanta_paradigm_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    generated = sum(row["generation_status"] == "locally_regenerated" for row in rows)
    report = {
        "date": "2026-09-14", "sample_dhatus": len(SAMPLES),
        "semantic_cells_requested": len(rows), "semantic_cells_locally_regenerated": generated,
        "engine_zero_unresolved_cells": len(rows) - generated,
        "engine_requests_including_two_pada_series": len(rows) * 2,
        "generated_surface_variants": sum(row["output_variant_count"] for row in rows),
        "full_rule_paths_recorded": True,
    }
    (RESULTS / "tinanta_paradigm_sample.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 9: Full-Paradigm Sample", "", f"The local engine regenerated **{generated} of {len(rows)} semantic cells** across भू, कृ, and एध्: ten लकाराः, three पुरुषाः, and three वचनानि for each धातुः.", "", "भू supplies a familiar परस्मैपदम् example, एध् supplies an आत्मनेपदम् example, and कृ demonstrates a wider output range. Every generated variant retains its rule path.", ""]
    (RESULTS / "tinanta_paradigm_sample.md").write_text("\n".join(lines))
    print(f"Regenerated {generated} of {len(rows)} full-paradigm sample cells.")


if __name__ == "__main__":
    main()
