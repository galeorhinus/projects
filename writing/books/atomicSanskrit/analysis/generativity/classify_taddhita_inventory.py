#!/usr/bin/env python3
"""Classify all pinned taddhita identifiers without making them multipliers."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
PILOT_MANIFEST = ARCHIVE / "manifest.json"
TADDHITA_MANIFEST = ARCHIVE / "taddhita_manifest.json"
CONFIG = HERE / "taddhita_operations.json"
ARGS = ARCHIVE / "vidyut-args-taddhita.rs"

MODULES = tuple(sorted(ARCHIVE.glob("vidyut-taddhita-*.rs")))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matching_brace(text: str, start: int) -> int:
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unclosed context block")


def context_descriptions() -> dict[str, str]:
    text = ARGS.read_text()
    start = text.index("pub enum TaddhitaArtha")
    end = text.index("\n}", start)
    docs: list[str] = []
    result = {}
    for line in text[start:end].splitlines()[1:]:
        stripped = line.strip()
        if stripped.startswith("///"):
            docs.append(stripped[3:].strip())
        else:
            match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*),", stripped)
            if match:
                result[match.group(1)] = " ".join(docs)
                docs = []
    return result


def source_usage() -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    contexts: dict[str, set[str]] = defaultdict(set)
    rules: dict[str, set[str]] = defaultdict(set)
    files: dict[str, set[str]] = defaultdict(set)
    context_re = re.compile(r"tp\.with_context\(([A-Za-z][A-Za-z0-9_]*),\s*\|tp\|\s*\{")
    suffix_re = re.compile(
        r"(?:optional_)?try_add(?:_with)?\("
        r"[^,\n]+,\s*(?:P::)?([A-Za-z][A-Za-z0-9_]*)"
    )
    direct_rule_re = re.compile(
        r"(?:optional_)?try_add(?:_with)?\("
        r"(?:Rule::Kashika\()?\"([0-9]+\.[0-9]+\.[0-9]+(?:\.[a-z])?)\"\)?"
        r"\s*,\s*(?:P::)?([A-Za-z][A-Za-z0-9_]*)"
    )
    for path in MODULES:
        text = path.read_text()
        for variant in suffix_re.findall(text):
            files[variant].add(path.name)
        for match in context_re.finditer(text):
            block_start = text.index("{", match.start())
            block = text[block_start:matching_brace(text, block_start) + 1]
            for variant in suffix_re.findall(block):
                contexts[variant].add(match.group(1))
        for rule, variant in direct_rule_re.findall(text):
            rules[variant].add(rule)
    return contexts, rules, files


def main() -> None:
    records = {}
    for manifest_path in (PILOT_MANIFEST, TADDHITA_MANIFEST):
        manifest = json.loads(manifest_path.read_text())
        records.update({row["filename"]: row for row in manifest["sources"]})
    for path in (ARGS, *MODULES):
        if sha256(path) != records[path.name]["sha256"]:
            raise ValueError(f"Archived source changed: {path.name}")

    with (RESULTS / "operation_inventory.csv").open(newline="", encoding="utf-8") as handle:
        inventory = [row for row in csv.DictReader(handle) if row["family"] == "taddhita"]
    if len(inventory) != 175:
        raise ValueError(f"Expected 175 taddhita identifiers, found {len(inventory)}")

    selected = {
        row["source_variant"]: row for row in json.loads(CONFIG.read_text())["operations"]
    }
    descriptions = context_descriptions()
    contexts, rules, files = source_usage()
    rows = []
    for row in inventory:
        variant = row["source_variant"]
        found_contexts = sorted(contexts.get(variant, set()))
        source_files = sorted(files.get(variant, set()))
        if variant in {"tva", "tal", "matup"}:
            disposition = "admitted_general_relation"
        elif variant == "Qak":
            disposition = "admitted_listed_examples_only"
        elif source_files == ["vidyut-taddhita-samasanta.rs"]:
            disposition = "compound_only_deferred"
        elif found_contexts:
            disposition = "conditioned_semantic_relation_deferred"
        elif source_files:
            disposition = "self_meaning_or_structural_relation_deferred"
        else:
            disposition = "engine_identifier_not_reached_in_archived_implementation"
        rows.append({
            "catalog_id": row["catalog_id"],
            "engine_id": row["engine_id"],
            "source_variant": variant,
            "visible_suffix": row["visible_suffix"],
            "semantic_contexts": ";".join(found_contexts),
            "semantic_descriptions": " | ".join(
                descriptions.get(x, "") for x in found_contexts if descriptions.get(x)
            ),
            "direct_rule_refs": ";".join(sorted(rules.get(variant, set()))),
            "implementation_files": ";".join(source_files),
            "selected_operation_id": selected.get(variant, {}).get("operation_id", ""),
            "classification_disposition": disposition,
            "count_status": "admitted_by_declared_operation" if variant in selected else "not_admitted",
        })

    with (RESULTS / "taddhita_identifier_classification.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    by_disposition = Counter(row["classification_disposition"] for row in rows)
    report = {
        "date": "2026-09-13",
        "scope": "Classification of all 175 taddhita identifiers exposed by the pinned engine. Classification does not itself admit a word-meaning.",
        "identifier_count": len(rows),
        "identifiers_with_semantic_contexts": sum(bool(row["semantic_contexts"]) for row in rows),
        "identifiers_selected_by_declared_operations": sum(row["count_status"] == "admitted_by_declared_operation" for row in rows),
        "by_disposition": dict(by_disposition),
        "semantic_context_count": len(descriptions),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (PILOT_MANIFEST, TADDHITA_MANIFEST, ARGS, CONFIG, RESULTS / "operation_inventory.csv", *MODULES, Path(__file__))
        },
    }
    (RESULTS / "taddhita_identifier_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# तद्धित Identifier Classification", "",
        "All 175 identifiers exposed by the pinned engine have a recorded disposition. This is an inventory classification, not a claim that every suffix can multiply every nominal base.", "",
        "| Disposition | Identifiers |", "|---|---:|",
    ]
    for key, value in sorted(by_disposition.items()):
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend([
        "", f"The archived implementation places {report['identifiers_with_semantic_contexts']} identifiers inside at least one explicit तद्धित semantic context. The first broad count admits only त्व, तल्, and मतुप् as general relations. ढक् remains limited to the three source examples already used by the pilot.", "",
        "All other identifiers retain their mapped contexts and source files for later conditioned passes.", "",
    ])
    (RESULTS / "taddhita_identifier_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(rows)} taddhita identifiers; selected {report['identifiers_selected_by_declared_operations']} source variants.")


if __name__ == "__main__":
    main()
