#!/usr/bin/env python3
"""Build the pinned engine-affix census without treating it as a multiplier."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
RESULTS = HERE / "results"
MANIFEST = ARCHIVE / "manifest.json"

SOURCES = {
    "sanadi": ("vidyut-args-dhatu.rs", "Sanadi"),
    "krt": ("vidyut-args-krt.rs", "BaseKrt"),
    "taddhita": ("vidyut-args-taddhita.rs", "Taddhita"),
}
EXPECTED_COUNTS = {"sanadi": 7, "krt": 122, "taddhita": 175}

TADDHITA_IDS = {"Qak", "tva", "tal", "aR", "matup"}
NAMA_SANADI = {"kAmyac", "kyaN", "kyac"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_records() -> dict[str, dict]:
    data = json.loads(MANIFEST.read_text())
    return {row["filename"]: row for row in data["sources"]}


def enum_block(text: str, enum_name: str) -> str:
    marker = f"pub enum {enum_name} {{"
    start = text.index(marker) + len(marker)
    end = text.index("\n}", start)
    return text[start:end]


def macro_mapping(text: str, enum_name: str) -> dict[str, str]:
    marker = f"sanskrit_enum!({enum_name}, {{"
    start = text.index(marker) + len(marker)
    end = text.index("\n});", start)
    block = text[start:end]
    return dict(re.findall(r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*=>\s*"([^"]+)",', block, re.M))


def parse_enum(path: Path, enum_name: str) -> list[dict[str, str]]:
    text = path.read_text()
    block = enum_block(text, enum_name)
    mapping = macro_mapping(text, enum_name)
    rows = []
    comments: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("///"):
            comments.append(stripped[3:].strip())
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*),", stripped)
        if match:
            variant = match.group(1)
            description = " ".join(part for part in comments if part)
            surface_match = re.search(r"(?:^|`)\-([^` ,.)]+)", description)
            rows.append({
                "source_variant": variant,
                "engine_id": mapping[variant],
                "source_description": description,
                "visible_suffix": surface_match.group(1) if surface_match else "",
            })
            comments = []
        elif stripped and not stripped.startswith("#"):
            comments = []
    return rows


def curated_rows() -> list[dict[str, str]]:
    with (HERE / "operations.csv").open() as handle:
        return list(csv.DictReader(handle))


def curated_family(row: dict[str, str]) -> str | None:
    affix = row["affix_slp1"]
    if not affix:
        return None
    if row["stage"] == "verbal_base":
        return "sanadi"
    if row["stage"] == "indeclinable":
        return "krt"
    if row["stage"] == "nominal_base":
        return "taddhita" if affix in TADDHITA_IDS else "krt"
    return None


def build_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    manifest = source_records()
    curated = curated_rows()
    links: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in curated:
        family = curated_family(row)
        if family:
            # operations.csv uses the familiar enum spelling without embedded
            # anubandha markers, so match it to the Rust source variant.
            links.setdefault((family, row["affix_slp1"]), []).append(row)

    inventory = []
    unmatched = set(links)
    for family, (filename, enum_name) in SOURCES.items():
        path = ARCHIVE / filename
        record = manifest[filename]
        if sha256(path) != record["sha256"]:
            raise ValueError(f"Archived source changed: {path}")
        parsed = parse_enum(path, enum_name)
        if len(parsed) != EXPECTED_COUNTS[family]:
            raise ValueError(f"Expected {EXPECTED_COUNTS[family]} {family} entries, found {len(parsed)}")
        for item in parsed:
            matches = links.get((family, item["source_variant"]), [])
            unmatched.discard((family, item["source_variant"]))
            inventory.append({
                "catalog_id": f"{family}:{item['engine_id']}",
                "family": family,
                "engine_id": item["engine_id"],
                "source_variant": item["source_variant"],
                "visible_suffix": item["visible_suffix"],
                "input_domain": "nominal_base" if family == "taddhita" or item["source_variant"] in NAMA_SANADI else "verbal_base",
                "output_domain": "derived_verbal_base" if family == "sanadi" else "derived_word_or_base",
                "curated_operation_ids": ";".join(row["id"] for row in matches),
                "semantic_status": "seeded" if matches else "pending",
                "eligibility_status": "example_scope_only" if matches else "pending",
                "count_status": "not_admitted",
                "source_description": item["source_description"],
                "source_file": filename,
                "source_url": record["url"],
                "source_sha256": record["sha256"],
            })
    if unmatched:
        raise ValueError(f"Curated affixes missing from pinned engine inventory: {sorted(unmatched)}")
    return inventory, curated


def write_csv(rows: list[dict[str, str]]) -> None:
    path = RESULTS / "operation_inventory.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict[str, str]], curated: list[dict[str, str]]) -> None:
    manifest = source_records()
    source_files = [SOURCES[family][0] for family in SOURCES]
    payload = {
        "scope": "Pinned engine identifier census; not a Sanskrit word count or an eligibility claim.",
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": json.loads(MANIFEST.read_text())["generator_commit"]},
        "counts": {
            "total_identifiers": len(rows),
            "by_family": {family: sum(row["family"] == family for row in rows) for family in SOURCES},
            "identifiers_with_curated_seed": sum(bool(row["curated_operation_ids"]) for row in rows),
            "curated_semantic_operations": len(curated),
            "curated_affix_operations": sum(bool(row["affix_slp1"]) for row in curated),
            "curated_non_affix_operations": sum(not row["affix_slp1"] for row in curated),
            "admitted_to_count": 0,
        },
        "source_records": [manifest[name] for name in source_files],
        "input_hashes": {
            "operations.csv": sha256(HERE / "operations.csv"),
            "operation_families.csv": sha256(HERE / "operation_families.csv"),
        },
        "inventory": rows,
    }
    (RESULTS / "operation_inventory.json").write_text(json.dumps(payload, indent=2) + "\n")


def write_markdown(rows: list[dict[str, str]], curated: list[dict[str, str]]) -> None:
    counts = {family: sum(row["family"] == family for row in rows) for family in SOURCES}
    seeded = [row for row in rows if row["curated_operation_ids"]]
    pending = [row for row in rows if not row["curated_operation_ids"]]
    lines = [
        "# Formation Operation Inventory", "",
        "This is a census of the derivational identifiers exposed by the pinned Vidyut 0.4.0 engine. It is not a Sanskrit vocabulary total. An identifier enters a future count only after its meaning, input conditions, and base-level eligibility are established.", "",
        "## Boundary", "",
        f"The engine exposes **{len(rows)} identifiers**: **{counts['sanadi']} sanadi**, **{counts['krt']} ordinary krt**, and **{counts['taddhita']} taddhita**. The existing pilot contains **{len(curated)} semantic-operation rows**. Twenty-eight name an affix; the other **{sum(not row['affix_slp1'] for row in curated)}** describe identity, prefixing, feminine formation, inflection, or compounding.", "",
        f"The curated pilot touches **{len(seeded)} distinct engine identifiers**. The remaining **{len(pending)} identifiers** are inventoried but semantically unclassified. All {len(rows)} rows therefore remain `not_admitted`; no multiplier has been applied to the 2,634 provisional base meanings.", "",
        "A suffix identifier is not always one semantic operation. The pilot already records three meanings for `lyu~w`: action, instrument, and location. Conversely, a grammatical operation can surface through a replacement while the engine request retains the original identifier, as with prefixed `ktvA` producing the `lyap` form. The next pass must therefore classify meaning-bearing operations, not merely suffix names.", "",
        "## Family Architecture", "",
        "| Family | Role | Current boundary |", "|---|---|---|",
    ]
    with (HERE / "operation_families.csv").open() as handle:
        for row in csv.DictReader(handle):
            lines.append(f"| {row['label']} | {row['lexical_role']} | {row['current_status']} |")
    lines.extend(["", "## Engine Census", "", "| Family | Identifiers | Seeded by pilot | Pending semantic classification |", "|---|---:|---:|---:|"])
    for family in SOURCES:
        family_rows = [row for row in rows if row["family"] == family]
        family_seeded = sum(bool(row["curated_operation_ids"]) for row in family_rows)
        lines.append(f"| {family} | {len(family_rows)} | {family_seeded} | {len(family_rows) - family_seeded} |")
    lines.extend(["", "## What Comes Next", "", "1. Split identifiers that carry several semantic relations into separate meaning-bearing operations.", "2. For each operation, state the eligible input class and record exclusions, required prefixes, and construction conditions.", "3. Test those rules against a bounded sample of the current 2,634 base meanings.", "4. Enumerate derived verbal, nominal, and indeclinable meanings separately. Inflection follows only after those base inventories are fixed.", "", "The full row-level census is in `operation_inventory.csv`; `operation_inventory.json` carries the same rows with source URLs, checksums, and input hashes.", ""])
    (RESULTS / "operation_inventory.md").write_text("\n".join(lines))


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows, curated = build_rows()
    write_csv(rows)
    write_json(rows, curated)
    write_markdown(rows, curated)
    print(f"Wrote {len(rows)} engine identifiers; none admitted to a vocabulary count.")


if __name__ == "__main__":
    main()
