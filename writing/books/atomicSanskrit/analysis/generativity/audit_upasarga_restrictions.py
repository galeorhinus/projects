#!/usr/bin/env python3
"""Build the source-checked register of upasarga/dhatu meaning restrictions."""

from __future__ import annotations

import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
INVENTORY = HERE / "upasarga_inventory.csv"
RESTRICTIONS = HERE / "upasarga_restrictions.json"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
CONFLICTS = HERE / "upasarga_conflicts.json"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def source_text(path: Path) -> str:
    parser = TextExtractor()
    parser.feed(path.read_text())
    return " ".join(" ".join(parser.parts).split())


def normalized_devanagari(value: str) -> str:
    return value.translate(str.maketrans("०१२३४५६७८९", "0123456789"))


def main() -> None:
    config = json.loads(RESTRICTIONS.read_text())
    manifest = json.loads(MANIFEST.read_text())
    inventory = read_csv(INVENTORY)
    assignments = [
        row for row in read_csv(ASSIGNMENTS) if row["record_kind"] == "lexical"
    ]
    source_path = ARCHIVE / config["source_filename"]
    source_record = next(
        row for row in manifest["sources"] if row["filename"] == config["source_filename"]
    )
    if sha256(source_path) != source_record["sha256"]:
        raise ValueError("Archived Dhatupatha witness changed")
    text = normalized_devanagari(source_text(source_path))

    upasarga_ids = [row["upasarga_id"] for row in inventory]
    exclusions = []
    restriction_rows = []
    for restriction in config["restrictions"]:
        quote = restriction["source_quote_devanagari"]
        if quote not in text:
            raise ValueError(f"Source quotation not found: {quote}")
        matches = [
            row for row in assignments
            if row["source_code"] == restriction["source_code"]
            and row["normalized_meaning_slp1"] == restriction["meaning_slp1"]
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Expected one base meaning for {restriction['source_code']} "
                f"{restriction['meaning_slp1']}; found {len(matches)}"
            )
        base = matches[0]
        allowed = set(restriction["allowed_upasarga_ids"])
        if not allowed.issubset(upasarga_ids):
            raise ValueError(f"Unknown allowed upasarga in {restriction['source_locator']}")
        blocked_ids = [value for value in upasarga_ids if value not in allowed]
        restriction_rows.append({
            **restriction,
            "base_count_key": base["normalized_count_key"],
            "base_citation_slp1": base["normalized_citation_slp1"],
            "blocked_upasarga_ids": blocked_ids,
            "exclusion_count": len(blocked_ids),
        })
        for upasarga_id in blocked_ids:
            exclusions.append({
                "upasarga_id": upasarga_id,
                "base_count_key": base["normalized_count_key"],
                "source_code": restriction["source_code"],
                "base_citation_slp1": base["normalized_citation_slp1"],
                "base_meaning_slp1": base["normalized_meaning_slp1"],
                "reason": restriction["reason"],
                "rule_refs": [restriction["source_locator"]],
                "source_filename": config["source_filename"],
                "source_quote": restriction["source_quote_devanagari"],
            })

    for annotation in config["non_subtractive_annotations"]:
        quote = annotation["source_quote_devanagari"]
        if quote not in text:
            raise ValueError(f"Source quotation not found: {quote}")

    enrichment_rows = []
    known_codes = {row["source_code"] for row in assignments}
    for enrichment in config["prefixed_meaning_enrichments"]:
        quote = enrichment["source_quote_devanagari"]
        if quote not in text:
            raise ValueError(f"Source quotation not found: {quote}")
        if enrichment["source_code"] not in known_codes:
            raise ValueError(f"Unknown source code in enrichment: {enrichment['source_code']}")
        allowed = enrichment["allowed_upasarga_ids"]
        if allowed == "all":
            resolved = upasarga_ids
        else:
            if not set(allowed).issubset(upasarga_ids):
                raise ValueError(f"Unknown upasarga in {enrichment['source_locator']}")
            resolved = allowed
        enrichment_rows.append({**enrichment, "resolved_upasarga_ids": resolved})

    exclusions.sort(key=lambda row: (upasarga_ids.index(row["upasarga_id"]), row["base_count_key"]))
    conflicts = {
        "date": config["date"],
        "scope": "Explicit conflicts that prevent a named original dhatu meaning from being inherited by one normalized upasarga in the bounded laukika run.",
        "reviewed_general_rules": ["1.4.58", "1.4.59", "1.4.60", "1.4.80"],
        "reviewed_lexical_source": source_record,
        "restriction_groups": restriction_rows,
        "non_subtractive_annotations": config["non_subtractive_annotations"],
        "prefixed_meaning_enrichments": enrichment_rows,
        "exclusions": exclusions,
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (RESTRICTIONS, INVENTORY, ASSIGNMENTS, MANIFEST, source_path, Path(__file__))
        },
        "status": f"Root-specific Dhatupatha restriction sweep complete: {len(exclusions)} meaning/prefix conflicts documented. Missing attestation is never an exclusion.",
    }
    CONFLICTS.write_text(json.dumps(conflicts, ensure_ascii=False, indent=2) + "\n")

    report = {
        "date": config["date"],
        "source": source_record,
        "restriction_groups": len(restriction_rows),
        "pair_exclusions": len(exclusions),
        "non_subtractive_annotations": len(config["non_subtractive_annotations"]),
        "prefixed_meaning_enrichments": len(enrichment_rows),
        "enriched_word_meanings": sum(len(row["resolved_upasarga_ids"]) for row in enrichment_rows),
        "restrictions": restriction_rows,
        "annotations": config["non_subtractive_annotations"],
        "enrichments": enrichment_rows,
        "inputs": conflicts["inputs"],
    }
    (RESULTS / "upasarga_restriction_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )

    lines = [
        "# Upasarga-Dhatu Restriction Audit",
        "",
        "This pass checks explicit prefix conditions in the archived Paninian Dhatupatha witness. It does not use dictionary or corpus attestation as an admission test.",
        "",
        "## Result",
        "",
        f"Seven source clauses produce **{len(exclusions)} exact meaning/prefix exclusions**. Four meanings require आङ् (*āṅ*), two require अधि (*adhi*), and one movement meaning is expressly limited to the unprefixed root.",
        "",
        "| Entry | Meaning | Permitted prefix | Excluded pairs | Source |",
        "|---|---|---|---:|---|",
    ]
    for row in restriction_rows:
        allowed = ", ".join(row["allowed_upasarga_ids"]) or "none"
        lines.append(
            f"| `{row['source_code']}` `{row['base_citation_slp1']}` | `{row['meaning_slp1']}` | {allowed} | {row['exclusion_count']} | {row['source_locator']} |"
        )
    lines.extend([
        "",
        "## Non-Subtractive Findings",
        "",
    ])
    for row in config["non_subtractive_annotations"]:
        lines.append(f"- **{row['source_locator']}:** {row['disposition']}")
    lines.extend([
        "",
        "## Prefixed Meaning Enrichment",
        "",
        f"Two source clauses add **{sum(len(row['resolved_upasarga_ids']) for row in enrichment_rows)} word-meanings** to the one-prefix ledger: twenty lengthening meanings from prefixed `tanu` and one longing meaning from `ut + kaṭhi`.",
    ])
    lines.extend([
        "",
        "The exclusions concern inheritance of a particular recorded meaning. They do not assert that the engine cannot spell a prefixed form, nor do they reject a combination merely because no dictionary records it.",
        "",
    ])
    (RESULTS / "upasarga_restriction_audit.md").write_text("\n".join(lines))
    print(f"Recorded {len(exclusions)} exact upasarga/dhatu meaning conflicts.")


if __name__ == "__main__":
    main()
