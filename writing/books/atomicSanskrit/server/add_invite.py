#!/usr/bin/env python3
"""add_invite.py — add or update a roster entry without hand-editing JSON.

Run this LOCALLY against the repo (not on the server) — the roster is
git-tracked and deploy.sh installs it to the server read-only. Commit and
push after running this, then deploy, for the new/updated invite to take
effect. See server/README.md for the full workflow.

Usage:
    python3 add_invite.py <slug> "<Full Name>" <hypothesis_group_url> [email]

Example:
    python3 add_invite.py jk "JK" https://hypothes.is/groups/AbC123x/reading-group jk@example.com
    python3 add_invite.py rm "R. Kumar" https://hypothes.is/groups/DeF456y/reading-group

If email is omitted, the invite page will ask the visitor for one and
auto-whitelist whatever they submit on first use, then lock the slug to
that email — see request_access.py's module docstring for what happens
if a different email shows up at the same link afterward.

The group NAME shown on the page is derived from the URL's last path
segment unless overridden with --group-name.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

# Relative to this script's own location (server/), not the CWD, so it
# works the same whether invoked as `python3 add_invite.py` from inside
# server/ or `python3 server/add_invite.py` from the repo root. Git-
# tracked — commit and push after running this script.
ROSTER_PATH = Path(__file__).resolve().parent / "invite_roster.json"


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

    ROSTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    roster = {}
    if ROSTER_PATH.exists():
        raw = ROSTER_PATH.read_text(encoding="utf-8").strip()
        roster = json.loads(raw) if raw else {}

    if args.slug in roster:
        print(f"Note: '{args.slug}' already exists, overwriting name/group/email.")

    record = roster.get(args.slug, {})
    record.update({
        "name": args.name,
        "hypothesis_group_url": args.group_url,
        "hypothesis_group_name": args.group_name or derive_group_name(args.group_url),
        "email": args.email,
    })
    roster[args.slug] = record

    ROSTER_PATH.write_text(json.dumps(roster, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added/updated '{args.slug}' -> {record['name']} <{args.email or '(no email on file)'}>")
    print(f"Invite link: https://secondshanti.org/as/invite/{args.slug}")
    print("Don't forget: commit, push, and deploy for this to take effect on the server.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
