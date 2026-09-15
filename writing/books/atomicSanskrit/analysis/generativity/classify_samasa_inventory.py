#!/usr/bin/env python3
"""Pass 1: inventory the compound types implemented by pinned Vidyut."""

import csv
import json
import re

from samasa_common import ARCHIVE, COMMIT, MANIFEST, RESULTS, project_path, sha256


SOURCE = ARCHIVE / "vidyut-args-samasa.rs"
ENUM_RE = re.compile(r"pub enum SamasaType \{(?P<body>.*?)\n\}", re.S)
VARIANT_RE = re.compile(r"^\s*(?P<name>[A-Za-z]+),", re.M)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    source_record = next(row for row in manifest["sources"] if row["filename"] == SOURCE.name)
    if manifest["generator_commit"] != COMMIT or sha256(SOURCE) != source_record["sha256"]:
        raise ValueError("Pinned samasa argument source changed")
    match = ENUM_RE.search(SOURCE.read_text())
    if not match:
        raise ValueError("SamasaType enum not found")
    variants = VARIANT_RE.findall(match.group("body"))
    rows = [{"engine_identifier": name, "disposition": "source_example_only"} for name in variants]
    with (RESULTS / "samasa_type_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "date": "2026-09-14",
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": COMMIT},
        "implemented_type_count": len(variants),
        "identifiers": variants,
        "broad_multiplier_applied": False,
        "reason": "A compound requires a stated semantic relation, and recursive compounding has no natural finite ceiling.",
        "inputs": {project_path(SOURCE): sha256(SOURCE), project_path(MANIFEST): sha256(MANIFEST)},
    }
    (RESULTS / "samasa_type_inventory.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS / "samasa_type_inventory.md").write_text(
        "# समासः Type Inventory\n\n"
        f"Pinned Vidyut 0.4.0 exposes **{len(variants)}** compound types: "
        + ", ".join(f"`{x}`" for x in variants)
        + ".\n\nNo type becomes a multiplier by name alone. Each admitted compound must retain its members, intended relation, member count, and derivational depth.\n"
    )
    print(f"Inventoried {len(variants)} samasa types.")


if __name__ == "__main__":
    main()
