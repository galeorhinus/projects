#!/usr/bin/env python3
"""Shared paths and helpers for the namadhatu passes."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
CORE_MANIFEST = ARCHIVE / "manifest.json"
NAMADHATU_MANIFEST = ARCHIVE / "namadhatu_manifest.json"
TEST_SOURCE = ARCHIVE / "kashika_3_1.rs"
IMPLEMENTATION = ARCHIVE / "vidyut-sanadi.rs"
RULE_TABLE = ARCHIVE / "sutrapatha.tsv"
NOMINAL_INVENTORY = RESULTS / "nominal_input_inventory.csv.gz"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"Unclosed {opening}{closing} block")


def rust_functions(path: Path):
    text = path.read_text()
    pattern = re.compile(
        r"(?P<attrs>(?:[ \t]*#\[[^\]]+\][ \t]*\n)*)"
        r"[ \t]*fn\s+(?P<name>[A-Za-z0-9_]+)\s*\([^)]*\)[^{]*\{"
    )
    for match in pattern.finditer(text):
        brace = text.index("{", match.start())
        end = matching_delimiter(text, brace, "{", "}")
        yield {
            "name": match.group("name"),
            "attrs": match.group("attrs"),
            "ignored": "#[ignore]" in match.group("attrs"),
            "start": brace + 1,
            "body": text[brace + 1:end],
            "full_text": text,
        }


def rule_from_function(name: str) -> str:
    match = re.match(r"sutra_([0-9]+)_([0-9]+)_([0-9]+)", name)
    return ".".join(match.groups()) if match else ""


def assertion_calls(body: str):
    pattern = re.compile(r"assert_has_(?:tip|ta|lat)\s*\(")
    for match in pattern.finditer(body):
        opening = body.index("(", match.start())
        end = matching_delimiter(body, opening, "(", ")")
        yield body[match.start():end + 1], match.start()
