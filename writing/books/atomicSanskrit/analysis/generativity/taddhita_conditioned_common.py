#!/usr/bin/env python3
"""Shared parsing helpers for the conditioned taddhita example passes."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
ARGS = ARCHIVE / "vidyut-args-taddhita.rs"
TEST_FILES = tuple(
    ARCHIVE / f"kashika_{chapter}_{section}.rs"
    for chapter in (4, 5)
    for section in range(1, 5)
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


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


def strip_line_comments(text: str) -> str:
    """Remove // comments while preserving offsets and line numbers."""
    return "\n".join(re.sub(r"//.*", lambda m: " " * len(m.group()), line) for line in text.split("\n"))


def source_functions(path: Path):
    text = path.read_text()
    clean = strip_line_comments(text)
    function_re = re.compile(r"(?:#\[test\]\s*)?fn\s+([A-Za-z0-9_]+)\s*\([^)]*\)[^{]*\{")
    for match in function_re.finditer(clean):
        brace = clean.index("{", match.start())
        end = matching_brace(clean, brace)
        yield {
            "name": match.group(1),
            "start": brace + 1,
            "end": end,
            "body": clean[brace + 1:end],
            "full_text": text,
        }


def rule_from_function(name: str) -> str:
    match = re.match(r"sutra_([0-9]+)_([0-9]+)_([0-9]+)", name)
    return ".".join(match.groups()) if match else ""


def context_descriptions() -> dict[str, str]:
    text = ARGS.read_text()
    start = text.index("pub enum TaddhitaArtha")
    end = text.index("\n}", start)
    docs: list[str] = []
    result: dict[str, str] = {}
    for line in text[start:end].splitlines()[1:]:
        stripped = line.strip()
        if stripped.startswith("///"):
            docs.append(stripped[3:].strip())
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*),", stripped)
        if match:
            description = " ".join(docs)
            result[match.group(1)] = "" if description == "TODO" else description
            docs = []
    return result
