#!/usr/bin/env python3
"""move_annotation.py -- move one of YOUR OWN annotations to a different
Hypothesis group.

Hypothesis has no API to change an annotation's group after creation --
h's own UpdateAnnotationSchema silently drops group/groupid/userid/
references on every PATCH (confirmed against h's source, 2026-08-19). The
only way to actually move one is delete + recreate: POST a new annotation
with the same uri/text/tags/target in the target group, confirm it, then
DELETE the original. This script does exactly that, defaulting to a dry
run so nothing changes until you pass --yes.

Refuses two cases, both because deleting the original would orphan
something that can't be recreated the same way:
  - the annotation IS a reply (has `references`) -- a reply always
    inherits its parent's group and can't be given a different one at
    creation either, so there's nothing to move it TO independent of the
    thread it's in.
  - the annotation HAS replies against it -- those replies' `references`
    point at the original id; deleting it breaks the thread. Move only
    applies to a standalone top-level note with nothing hanging off it.

Usage:
    python3 move_annotation.py <annotation_id> <target_group_id>
    python3 move_annotation.py <annotation_id> <target_group_id> --yes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hypothesis_client import HypothesisClient, HypothesisError  # noqa: E402


def has_replies(client: HypothesisClient, group_id: str, annotation_id: str) -> bool:
    """Only needs to search annotation_id's OWN group -- a reply always
    shares its root's group (Hypothesis assigns it that way; group is
    ignored on a reply POST for exactly this reason), so a reply against
    this annotation can't be sitting in any other group."""
    for a in client.search_all(group_id):
        if annotation_id in (a.get("references") or []):
            return True
    return False


def quote_of(annotation: dict) -> str:
    for t in annotation.get("target", []):
        for s in t.get("selector", []):
            if s.get("type") == "TextQuoteSelector":
                return s.get("exact", "")
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("annotation_id")
    parser.add_argument("target_group_id")
    parser.add_argument("--yes", action="store_true",
                         help="actually perform the move (default is dry-run)")
    args = parser.parse_args()

    client = HypothesisClient()
    try:
        original = client.get_annotation(args.annotation_id)
    except HypothesisError as e:
        print(f"Could not fetch {args.annotation_id}: {e}")
        return 1

    if original.get("references"):
        print("Refusing: this IS a reply, not a top-level annotation -- a reply "
              "always inherits its parent's group and has no independent group "
              "of its own to move.")
        return 1

    if has_replies(client, original["group"], args.annotation_id):
        print("Refusing: this annotation HAS replies against it -- deleting it "
              "would orphan the reply thread (their `references` would point at "
              "a deleted id).")
        return 1

    print(f"Moving {args.annotation_id}")
    print(f"  uri:   {original['uri']}")
    print(f"  quote: {quote_of(original)!r}")
    print(f"  text:  {original.get('text', '')!r}")
    print(f"  tags:  {original.get('tags', [])}")
    print(f"  from group {original['group']} -> {args.target_group_id}")

    if not args.yes:
        print("\nDry run -- nothing changed. Pass --yes to actually move it.")
        return 0

    created = client.create_annotation(
        uri=original["uri"],
        text=original.get("text", ""),
        tags=original.get("tags", []),
        target=original.get("target", []),
        group=args.target_group_id,
        document=original.get("document"),
    )
    print(f"  created {created['id']} in {args.target_group_id}")

    client.delete_annotation(args.annotation_id)
    print(f"  deleted original {args.annotation_id}")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
