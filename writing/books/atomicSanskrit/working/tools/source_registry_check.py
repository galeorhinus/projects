#!/usr/bin/env python3
"""Validate hidden endnote source IDs against the digital source registry."""

from __future__ import annotations

import re
import sys
from pathlib import Path


BOOK_DIR = Path(__file__).resolve().parents[2]
ENDNOTES = BOOK_DIR / "manuscript" / "as_endnotes.md"
REGISTRY = (
    BOOK_DIR
    / "working"
    / "40_reference"
    / "sources"
    / "as_source_registry.md"
)

BLOCK_RE = re.compile(r"<!--\s*SOURCE-RECORDS\b(.*?)-->", re.DOTALL)
SOURCE_LINE_RE = re.compile(r"^\s*-\s*([a-z0-9_-]+)(?:\s*\||\s*$)")
ENTRY_RE = re.compile(r"^### `([a-z0-9_-]+)`", re.MULTILINE)
REGISTERED_SECTION_RE = re.compile(r"^## Registered Sources\s*$", re.MULTILINE)


def main() -> int:
    if not ENDNOTES.exists() or not REGISTRY.exists():
        print("Missing endnotes or source registry.", file=sys.stderr)
        return 2

    registry_text = REGISTRY.read_text()
    section = REGISTERED_SECTION_RE.search(registry_text)
    registered_text = registry_text[section.end() :] if section else ""
    registered = set(ENTRY_RE.findall(registered_text))

    endnotes_text = ENDNOTES.read_text()
    used: list[tuple[str, str]] = []
    malformed: list[str] = []

    for block in BLOCK_RE.finditer(endnotes_text):
        entry_matches = list(ENTRY_RE.finditer(endnotes_text, 0, block.start()))
        endnote_id = entry_matches[-1].group(1) if entry_matches else "<unknown>"
        for line in block.group(1).splitlines():
            if not line.strip():
                continue
            source = SOURCE_LINE_RE.match(line)
            if source:
                used.append((endnote_id, source.group(1)))
            else:
                malformed.append(f"{endnote_id}: {line.strip()}")

    missing = [(note, source) for note, source in used if source not in registered]

    if malformed:
        print("Malformed SOURCE-RECORDS lines:", file=sys.stderr)
        for item in malformed:
            print(f"  {item}", file=sys.stderr)
    if missing:
        print("Source IDs missing from registry:", file=sys.stderr)
        for note, source in missing:
            print(f"  {note}: {source}", file=sys.stderr)

    if malformed or missing:
        return 1

    print(
        f"Source registry check passed: {len(used)} endnote source links; "
        f"{len(registered)} registered sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
