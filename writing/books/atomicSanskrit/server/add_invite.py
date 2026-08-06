#!/usr/bin/env python3
"""add_invite.py — add or update a named invite without hand-editing JSON.

Usage:
    python3 add_invite.py <slug> "<Full Name>" <hypothesis_group_url> [email]

Example:
    python3 add_invite.py jk "JK" https://hypothes.is/groups/AbC123x/reading-group jk@example.com
    python3 add_invite.py rm "R. Kumar" https://hypothes.is/groups/DeF456y/reading-group

If email is omitted, the invite page will ask the visitor for one and
auto-whitelist whatever they submit (no email on file to compare against).

The group NAME shown on the page is derived from the URL's last path
segment unless overridden with --group-name.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

INVITES_PATH = Path("/etc/secondshanti/invites.json")


def derive_group_name(url: str) -> str:
    slug = urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
    return slug.replace("-", " ").replace("_", " ").title() or "your group"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="URL slug, e.g. 'jk' for /as/invite/jk")
    parser.add_argument("name", help="Display name, e.g. 'JK'")
    parser.add_argument("group_url", help="Hypothesis group join link")
    parser.add_argument("email", nargs="?", default=None, help="Known email, if you have it")
    parser.add_argument("--group-name", default=None, help="Override the displayed group name")
    args = parser.parse_args()

    INVITES_PATH.parent.mkdir(parents=True, exist_ok=True)
    invites = {}
    if INVITES_PATH.exists():
        raw = INVITES_PATH.read_text(encoding="utf-8").strip()
        invites = json.loads(raw) if raw else {}

    if args.slug in invites:
        print(f"Note: '{args.slug}' already exists, overwriting name/group/email "
              f"(preserving status/submitted_email/hypothesis_username if present).")

    record = invites.get(args.slug, {})
    record.update({
        "name": args.name,
        "hypothesis_group_url": args.group_url,
        "hypothesis_group_name": args.group_name or derive_group_name(args.group_url),
        "email": args.email,
        "status": record.get("status", "invited"),
    })
    invites[args.slug] = record

    INVITES_PATH.write_text(json.dumps(invites, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Added/updated '{args.slug}' -> {record['name']} <{args.email or '(no email on file)'}>")
    print(f"Invite link: https://secondshanti.org/as/invite/{args.slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
