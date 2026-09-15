#!/usr/bin/env python3
"""Shared source and path helpers for the stri-pratyaya passes."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
CORE_MANIFEST = ARCHIVE / "manifest.json"
STRI_MANIFEST = ARCHIVE / "stri_manifest.json"
TEST_SOURCE = ARCHIVE / "kashika_4_1.rs"
IMPLEMENTATION = ARCHIVE / "vidyut-stritva.rs"
INTERNAL_ARGS = ARCHIVE / "vidyut-args-internal.rs"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def matching_brace(text: str, start: int) -> int:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("Unclosed Rust function block")


def rust_functions(path: Path):
    text = path.read_text()
    pattern = re.compile(
        r"(?P<attrs>(?:[ \t]*#\[[^\]]+\][ \t]*\n)*)"
        r"[ \t]*fn\s+(?P<name>[A-Za-z0-9_]+)\s*\([^)]*\)[^{]*\{"
    )
    for match in pattern.finditer(text):
        brace = text.index("{", match.start())
        end = matching_brace(text, brace)
        yield {
            "name": match.group("name"),
            "attrs": match.group("attrs"),
            "ignored": "#[ignore]" in match.group("attrs"),
            "start": brace + 1,
            "end": end,
            "body": text[brace + 1:end],
            "full_text": text,
        }


def rule_from_function(name: str) -> str:
    match = re.match(r"sutra_([0-9]+)_([0-9]+)_([0-9]+)", name)
    return ".".join(match.groups()) if match else ""
