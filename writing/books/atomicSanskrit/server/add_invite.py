#!/usr/bin/env python3
"""add_invite.py — add or update a roster entry without hand-editing JSON.

Run this LOCALLY against the repo (not on the server) — the roster is
git-tracked and deploy.sh installs it to the server read-only. Commit and
push after running this, then deploy, for the new/updated invite to take
effect. See server/README.md for the full workflow.

Usage:
    python3 add_invite.py <slug> "<Full Name>" <hypothesis_group_url> [email]
    python3 add_invite.py <slug> "<Full Name>" <hypothesis_group_url> --add-group

Example:
    python3 add_invite.py jk "JK" https://hypothes.is/groups/AbC123x/reading-group jk@example.com
    python3 add_invite.py rm "R. Kumar" https://hypothes.is/groups/DeF456y/reading-group

If email is omitted, the invite page will ask the visitor for one and
auto-whitelist whatever they submit on first use, then lock the slug to
that email — see request_access.py's module docstring for what happens
if a different email shows up at the same link afterward.

The group NAME shown on the page is derived from the URL's last path
segment unless overridden with --group-name.

A reader may belong to more than one group, so `groups` is an array.
By default this script REPLACES the array with the single group given.
Pass --add-group to append instead, keeping the existing ones.

Adding beats moving. A Hypothesis annotation's group is fixed at creation
and cannot be changed afterwards (the API silently drops `group` on PATCH),
so replacing a reader's group orphans every note they have already written:
it stays in the old group and vanishes from their dashboard. Use --add-group
unless you actually intend to cut them off from their own history.
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


def group_id(url: str) -> str | None:
    """The immutable id out of https://hypothes.is/groups/<id>/<slug>."""
    parts = [p for p in urlparse(url).path.split("/") if p]
    return parts[1] if len(parts) >= 2 and parts[0] == "groups" else None


def existing_groups(record: dict) -> list[dict]:
    """This reader's current groups, migrating a pre-array record on read."""
    if "groups" in record:
        return list(record["groups"])
    url, name = record.get("hypothesis_group_url"), record.get("hypothesis_group_name")
    return [{"url": url, "name": name}] if (url or name) else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="URL slug, e.g. 'jk' for /as/invite/jk")
    parser.add_argument("name", help="Display name, e.g. 'JK'")
    parser.add_argument("group_url", help="Hypothesis group join link")
    parser.add_argument("email", nargs="?", default=None, help="Known email, if you have it")
    parser.add_argument("--group-name", default=None, help="Override the displayed group name")
    parser.add_argument("--add-group", action="store_true",
                        help="Append this group to the reader's existing groups "
                             "instead of replacing them")
    args = parser.parse_args()

    ROSTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    roster = {}
    if ROSTER_PATH.exists():
        raw = ROSTER_PATH.read_text(encoding="utf-8").strip()
        roster = json.loads(raw) if raw else {}

    if args.slug in roster:
        what = "adding a group to" if args.add_group else "overwriting name/group/email for"
        print(f"Note: '{args.slug}' already exists, {what} it.")

    record = roster.get(args.slug, {})
    new_group = {
        "url": args.group_url,
        "name": args.group_name or derive_group_name(args.group_url),
    }

    if args.add_group:
        groups = existing_groups(record)
        new_id = group_id(args.group_url)
        already = any(
            (new_id is not None and group_id(g.get("url", "")) == new_id)
            or g.get("url") == args.group_url
            for g in groups
        )
        if already:
            print(f"'{args.slug}' is already in that group — nothing to add.")
            return 0
        groups.append(new_group)
    else:
        groups = [new_group]

    # --add-group is for an existing reader; don't blank their email just
    # because the positional argument was omitted on this invocation.
    email = record.get("email") if (args.email is None and args.add_group) else args.email

    # Rebuild in canonical field order so the file stays readable, carrying
    # any fields this script does not manage (e.g. hypothesis_username).
    rebuilt = {"name": args.name, "groups": groups, "email": email}
    for k, v in record.items():
        if k not in rebuilt and k not in ("hypothesis_group_url", "hypothesis_group_name"):
            rebuilt[k] = v
    roster[args.slug] = record = rebuilt

    ROSTER_PATH.write_text(json.dumps(roster, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added/updated '{args.slug}' -> {record['name']} <{record['email'] or '(no email on file)'}>")
    print(f"  groups: {', '.join(g['name'] for g in record['groups'])}")
    print(f"Invite link: https://secondshanti.org/as/invite/{args.slug}")
    print("Don't forget: commit, push, and deploy for this to take effect on the server.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
