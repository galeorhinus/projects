#!/usr/bin/env python3
"""Tinanta pass 1: declare the ten-lakara laukika inflection boundary."""

from __future__ import annotations

import csv
import importlib.metadata
import json

from vidyut.prakriya import Lakara

from tinanta_common import CONFIG, RESULTS, project_path, sha256


def main() -> None:
    config = json.loads(CONFIG.read_text())
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("The tinanta analysis requires Vidyut 0.4.0")
    engine = {repr(item).split(".")[-1] for item in Lakara.choices()}
    configured = {item["vidyut"] for item in config["laukika_lakaras"]}
    withheld = config["vaidika_lakara_withheld"]["vidyut"]
    if len(configured) != 10 or configured | {withheld} != engine:
        raise ValueError("The ten-lakara boundary does not reconcile to Vidyut's Lakara enum")

    fields = ("id", "vidyut", "display", "plain_function", "principal_rule_refs", "disposition")
    rows = []
    for item in config["laukika_lakaras"]:
        rows.append({**item, "principal_rule_refs": ";".join(item["principal_rule_refs"]), "disposition": "counted_laukika"})
    item = config["vaidika_lakara_withheld"]
    rows.append({
        "id": item["id"], "vidyut": item["vidyut"], "display": item["display"],
        "plain_function": "Vaidika verbal resource", "principal_rule_refs": "",
        "disposition": "withheld_vaidika_domain",
    })
    with (RESULTS / "tinanta_lakara_classification.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    report = {
        "date": "2026-09-14", "engine_lakaras": len(engine),
        "counted_laukika_lakaras": len(configured), "withheld_vaidika_lakaras": 1,
        "citation_cells_per_word_meaning": len(configured),
        "full_person_number_cells_per_word_meaning": len(configured) * 9,
        "prayoga": config["prayoga"], "pada_multiplier": 1,
        "input": {project_path(CONFIG): sha256(CONFIG)},
    }
    (RESULTS / "tinanta_lakara_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# तिङन्त Pass 1: लकार Boundary", "",
        "The लौकिक capacity uses ten लकाराः. वैदिक लेट् remains in its own domain.", "",
        "| लकारः | Plain function | Disposition |", "|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['display']} | {row['plain_function']} | {row['disposition']} |")
    lines.extend(["", "The count uses कर्तरि प्रयोग. Each लकार first contributes one third-person singular citation coordinate and later expands to nine person-number cells. The two पद series remain alternative forms within those cells.", ""])
    (RESULTS / "tinanta_lakara_classification.md").write_text("\n".join(lines))
    print("Classified ten laukika lakaras and withheld Vaidika let.")


if __name__ == "__main__":
    main()
