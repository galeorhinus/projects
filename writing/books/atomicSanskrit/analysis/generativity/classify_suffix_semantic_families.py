#!/usr/bin/env python3
"""Group the taddhita inventory by semantic work rather than visible ending."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path

from taddhita_conditioned_common import HERE, RESULTS, sha256


SOURCE = RESULTS / "taddhita_identifier_classification.csv"

CATEGORY_CONTEXTS = {
    "descent_identity_community": {
        "TasyaApatyam", "Gotra", "Jatau", "Janapada", "TasyaSamuha",
        "AyudhaJiviSangha",
    },
    "place_origin_association": {
        "Caturarthika", "TatraJata", "TatraKrtaLabdhaKritaKushala",
        "TatraPrayabhava", "TatraSambhute", "TatraBhava", "TataAgata",
        "AsyaNivasa", "TasyaVishayoDeshe", "TatraVasi", "Vasati",
        "DigDeshaKala",
    },
    "material_transformation_preparation": {
        "TenaRaktam", "SamskrtamBhaksha", "TasyaVikara", "TenaSamskrtam",
        "TenaNirvrtte", "TenaSamsrshte", "TenaUpasikte", "Nirmita",
        "TadarthamVikrtehPrakrtau", "Krta", "Nimana", "TatPrakrtaVacane",
        "AbhutaTadbhava",
    },
    "possession_state_measure": {
        "TasyaIdam", "TasyaDharmyam", "Mati", "Shilam", "TadAsyaTadAsminSyat",
        "TadAsyaParimanam", "TasyaBhava", "TadAsyaSamjatam", "TadAsyaPramanam",
        "Parimana", "Avasana", "Purana", "TadAsyaAstiAsmin",
    },
    "purpose_suitability_value": {
        "HitamBhaksha", "TadAsmaiDiyateNiyuktam", "Priya", "TasmaiHitam",
        "TasyaNimittamSamyogotpattau", "TadArhati", "AbhigamanamArhati",
        "AlamGami", "Tadarthye",
    },
    "action_occupation_instrument": {
        "TenaDivyatiJayatiJitam", "TenaTarati", "TenaCarati", "TenaJivati",
        "TenaHarati", "PrayacchatiGarhyam", "Unchati", "TadRakshati", "Karoti",
        "Hanti", "Grhnati", "Carati", "Eti", "Samavaiti", "Pashyati",
        "TadAsyaPanyam", "Praharanam", "Shilpam", "KarmaAdhyayaneVrttam",
        "Niyuktam", "Vyavaharati", "TadVahati", "TadVidhyati", "TatraSadhu",
        "TenaKritam", "TasyaVapa", "TadDharatiVahatiAvahati",
        "SambhavatiAharatiPacati", "TadVartayati", "Gacchati", "Ahrtam",
        "TenaNirvrttam", "TatraKushala", "Hari", "Karin", "Anvicchati",
    },
    "knowledge_devotion_relation": {
        "SaAsyaDevata", "TadAdhiteTadVeda", "Bhakti", "TenaProktam", "TenaKrte",
    },
    "evaluation_comparison_degree": {
        "Prashamsa", "Kutsite", "Avakshepane", "Anukampayam", "Tanutve",
        "Alpe", "Hrasve", "IvePratikrtau", "PrakaraVacane", "AnatyantaGati",
        "Acchadana",
    },
    "time_quantity_repetition": {
        "TamAdhisteBhrtoBhutoBhavi", "Vayasi", "EkahaGama", "TasyaPakamula",
        "KriyaAbhyavrttiGanana", "DvayorEka", "BahunamEka",
    },
}


def categories(contexts: list[str]) -> list[str]:
    matched = [name for name, members in CATEGORY_CONTEXTS.items() if set(contexts) & members]
    categorized = set().union(*(CATEGORY_CONTEXTS[name] for name in matched)) if matched else set()
    if set(contexts) - categorized:
        matched.append("other_conditioned_relation")
    return matched


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))

    rows = []
    for row in source_rows:
        contexts = [value for value in row["semantic_contexts"].split(";") if value]
        if contexts:
            groups = categories(contexts)
        elif row["classification_disposition"] == "self_meaning_or_structural_relation_deferred":
            groups = ["same_meaning_or_structural"]
        elif row["classification_disposition"] == "engine_identifier_not_reached_in_archived_implementation":
            groups = ["unreached_in_pinned_implementation"]
        else:
            groups = ["declared_operation"]
        rows.append({**row, "semantic_families": ";".join(groups)})

    output = RESULTS / "suffix_semantic_families.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    family_counts = Counter(family for row in rows for family in row["semantic_families"].split(";"))
    visible_counts = Counter(row["visible_suffix"] or "zero_or_replacement" for row in rows)
    report = {
        "date": "2026-09-13",
        "suffix_identifiers": len(rows),
        "semantic_family_assignments": dict(sorted(family_counts.items())),
        "most_common_visible_endings": dict(visible_counts.most_common(20)),
        "principle": "A visible ending is not an operation. Different grammatical suffixes can converge on the same visible form, and one suffix can serve several semantic relations.",
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (SOURCE, Path(__file__))},
        "publication_status": "research_classification_only_not_deployed",
    }
    (RESULTS / "suffix_semantic_families.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Suffix Semantic Families", "",
        "The pinned inventory contains **175 तद्धित suffix identifiers**. They are grouped here by the work they perform, not by the letters visible at the end of the finished word.", "",
        "A visible **-क (-ka)** or **-य (-ya)** is not one operation. Several underlying suffixes can produce either ending, and the same underlying suffix can express different relations under different rules.", "",
        "| Semantic family | Suffix identifiers assigned |", "|---|---:|",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(f"| {family.replace('_', ' ')} | {count} |")
    lines.extend(["", "One suffix can appear in more than one row because its rules can perform more than one kind of semantic work.", ""])
    (RESULTS / "suffix_semantic_families.md").write_text("\n".join(lines))
    print(f"Grouped {len(rows)} suffix identifiers into {len(family_counts)} semantic families.")


if __name__ == "__main__":
    main()
