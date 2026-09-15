#!/usr/bin/env python3
"""Pass 1: inventory the pinned engine's stri-pratyaya identifiers."""

from __future__ import annotations

import csv
import json
import re

from stri_common import IMPLEMENTATION, INTERNAL_ARGS, RESULTS, STRI_MANIFEST, project_path, sha256


DISPLAY = {
    "cAp": "चाप् (cāp)",
    "wAp": "टाप् (ṭāp)",
    "qAp": "डाप् (ḍāp)",
    "NIn": "ङीन् (ṅīn)",
    "NIp": "ङीप् (ṅīp)",
    "NIz": "ङीष् (ṅīṣ)",
    "UN": "ऊङ् (ūṅ)",
}


def main() -> None:
    manifest = json.loads(STRI_MANIFEST.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    for path in (IMPLEMENTATION, INTERNAL_ARGS):
        if sha256(path) != records[path.name]["sha256"]:
            raise ValueError(f"Archived source changed: {path.name}")

    text = INTERNAL_ARGS.read_text()
    block = re.search(r"internal_term!\(Stri,\s*\{(.*?)\}\);", text, re.S)
    if not block:
        raise ValueError("Could not locate the Stri enum")
    identifiers = re.findall(r'^\s*([A-Za-z][A-Za-z0-9]*)\s*=>\s*"([^"]+)"', block.group(1), re.M)
    rows = [{
        "engine_identifier": name,
        "aupadeshika_slp1": value,
        "display": DISPLAY[name],
        "family": "Ap" if value.endswith("Ap") else "NI" if value.startswith("NI") else "UN",
        "operation_role": "forms a feminine nominal base under Aṣṭādhyāyī 4.1.3-4.1.75",
    } for name, value in identifiers]
    if set(DISPLAY) != {row["engine_identifier"] for row in rows}:
        raise ValueError("Pinned स्त्रीप्रत्यय inventory changed")

    output = RESULTS / "stri_suffix_inventory.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": "2026-09-13",
        "pinned_suffix_identifiers": len(rows),
        "identifiers": [row["engine_identifier"] for row in rows],
        "rule_scope": "4.1.3-4.1.75",
        "classification": "derivational feminine-base operations, subject to base-specific rules; not a universal gender multiplier",
        "inputs": {project_path(path): sha256(path) for path in (IMPLEMENTATION, INTERNAL_ARGS, STRI_MANIFEST)},
        "publication_status": "research_inventory_only_not_deployed",
    }
    (RESULTS / "stri_suffix_inventory.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "stri_suffix_inventory.md").write_text("\n".join([
        "# स्त्रीप्रत्ययः Inventory", "",
        "The pinned engine exposes **seven** feminine suffix identifiers: " + ", ".join(row["display"] for row in rows) + ".", "",
        "Aṣṭādhyāyī 4.1.3 supplies the स्त्रियाम् scope, and rules 4.1.4-4.1.75 determine which suffix, if any, a particular nominal base receives. The inventory therefore records possible operations, not seven automatic multipliers.", "",
    ]))
    print(f"Inventoried {len(rows)} stri-pratyaya identifiers.")


if __name__ == "__main__":
    main()
