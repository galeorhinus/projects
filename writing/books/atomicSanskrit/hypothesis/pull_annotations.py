#!/usr/bin/env python3
"""pull_annotations.py -- fetch every annotation across every Hypothesis
group the token's account belongs to, and write a normalized snapshot to
hypothesis/data/annotations.json.

Usage:
    python3 pull_annotations.py

Re-run any time; this always does a full pull (the volume here -- a
handful of readers on one book -- doesn't need incremental fetching).
digest_send.py tracks its own "what's new since last digest" state
separately, on top of whatever this script last wrote.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from hypothesis_client import HypothesisClient, HypothesisError

DATA_DIR = Path(__file__).parent / "data"
ANNOTATIONS_PATH = DATA_DIR / "annotations.json"
GROUPS_PATH = DATA_DIR / "groups.json"

_USER_RE = re.compile(r"^acct:([^@]+)@")


def clean_user(user_id: str) -> str:
    """'acct:jsmith@hypothes.is' -> 'jsmith'. Falls back to the raw id if
    it doesn't match the expected acct: shape (defensive, not expected)."""
    m = _USER_RE.match(user_id or "")
    return m.group(1) if m else (user_id or "")


def extract_quote_context(annotation: dict) -> tuple[str, str, str]:
    """(prefix, exact, suffix) -- the text the reader highlighted, plus
    the surrounding sentence fragment Hypothesis already captures on
    either side (its own anchoring context, typically ~30-40 chars each
    way). Note-only annotations with no selection return ("", "", "")."""
    for target in annotation.get("target", []):
        for selector in target.get("selector", []):
            if selector.get("type") == "TextQuoteSelector":
                return (
                    selector.get("prefix", ""),
                    selector.get("exact", ""),
                    selector.get("suffix", ""),
                )
    return "", "", ""


def normalize(annotation: dict, group_name: str) -> dict:
    prefix, exact, suffix = extract_quote_context(annotation)
    return {
        "id": annotation.get("id"),
        "created": annotation.get("created"),
        "updated": annotation.get("updated"),
        "user": clean_user(annotation.get("user", "")),
        "user_id": annotation.get("user"),
        "group_id": annotation.get("group"),
        "group_name": group_name,
        "tags": annotation.get("tags", []),
        "text": annotation.get("text", ""),
        "quote": exact,
        "quote_prefix": prefix,
        "quote_suffix": suffix,
        "uri": annotation.get("uri", ""),
        "document_title": (annotation.get("document", {}).get("title") or [""])[0],
        "is_reply": bool(annotation.get("references")),
    }


def main() -> int:
    try:
        client = HypothesisClient()
    except HypothesisError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        groups = client.profile_groups()
    except HypothesisError as e:
        print(f"ERROR fetching groups: {e}", file=sys.stderr)
        return 1

    if not groups:
        print("No groups found for this token's account.", file=sys.stderr)
        return 1

    print(f"Found {len(groups)} group(s):")
    all_annotations: list[dict] = []
    group_index = {}
    for g in groups:
        gid = g["id"]
        gname = g.get("name", gid)
        group_index[gid] = gname
        try:
            rows = client.search_all(gid)
        except HypothesisError as e:
            print(f"  ⚠ {gname} ({gid}): {e}", file=sys.stderr)
            continue
        print(f"  {gname} ({gid}): {len(rows)} annotation(s)")
        all_annotations.extend(normalize(a, gname) for a in rows)

    all_annotations.sort(key=lambda a: a["created"])

    DATA_DIR.mkdir(exist_ok=True)
    ANNOTATIONS_PATH.write_text(
        json.dumps(all_annotations, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    GROUPS_PATH.write_text(
        json.dumps(group_index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\nWrote {len(all_annotations)} annotation(s) -> {ANNOTATIONS_PATH.relative_to(Path.cwd()) if ANNOTATIONS_PATH.is_relative_to(Path.cwd()) else ANNOTATIONS_PATH}")
    untagged = sum(1 for a in all_annotations if not a["tags"])
    print(f"{untagged} untagged (candidates for auto_tagger.py)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
