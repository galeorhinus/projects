#!/usr/bin/env python3
"""Shared paths and helpers for the six-pass capacity synthesis."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
MANUSCRIPT = ROOT / "manuscript"
DATE = "2026-09-15"


def read_json(path: Path):
    return json.loads(path.read_text())


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def extract_paragraph(text: str, phrase: str) -> str:
    matches = [paragraph for paragraph in text.split("\n\n") if phrase in paragraph]
    if len(matches) != 1:
        raise ValueError(f"Expected one paragraph containing {phrase!r}; found {len(matches)}")
    return matches[0]


def extract_section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        raise ValueError(f"Missing section heading {heading!r}")
    end = text.find("\n---", start)
    if end < 0:
        raise ValueError(f"Missing section terminator after {heading!r}")
    return text[start:end].rstrip()
