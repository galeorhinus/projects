#!/usr/bin/env python3
"""check_roster_sync.py -- warn when the groups on Hypothesis and the
groups listed in server/invite_roster.json have drifted apart.

Why this exists: the reader-facing group picker on every book page is
driven entirely by server/invite_roster.json (build_html.py's
groupsAllowlist, injected into <!--GROUPS-ALLOWLIST--> in every rendered
page) -- it is never a live Hypothesis API call. A group created on
hypothes.is but never added to the roster is therefore invisible to
every reader's picker, with no error anywhere to say so. Symmetrically,
a roster entry can go stale silently: a group renamed or deleted on
Hypothesis leaves the roster's cached name and URL looking fine while
no longer matching reality.

This script has no automated fix -- server/invite_roster.json stays a
manually-maintained, git-authoritative file (per its own docstring
convention and hypothesis/README.md) -- it only reports where the two
sides disagree, so the fix can be made by hand.

Live-side caveat: /profile/groups returns only the groups the API
token's own account belongs to (see hypothesis_client.py's
profile_groups() docstring), not literally every group that exists on
Hypothesis. pull_annotations.py already depends on this same assumption
(it fans annotation search out across exactly this set), so a group
this script calls "missing from roster" is scoped to "groups the book's
own Hypothesis account can see" -- if the owner's account was never
added to a group, it won't appear as a live group here even though it
may exist.

Usage:
    python3 check_roster_sync.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from hypothesis_client import HypothesisClient, HypothesisError

ROSTER_PATH = Path(__file__).parent.parent / "server" / "invite_roster.json"

_GROUP_ID_RE = re.compile(r"/groups/([^/?#]+)")


def roster_group_refs() -> dict[str, dict]:
    """group_id -> {"name": recorded name, "readers": [roster keys that
    reference it]}. Mirrors the id-extraction convention shared by
    server/request_access.py, hypothesis/build_dashboard.py, and
    build_html.py's hypothesis_groups_allowlist_json() -- each parses
    invite_roster.json independently for its own reason (see those
    functions' docstrings), so this is a fourth, equally isolated read
    rather than importing any of them."""
    if not ROSTER_PATH.exists():
        print(f"ERROR: no roster at {ROSTER_PATH}", file=sys.stderr)
        sys.exit(1)
    roster = json.loads(ROSTER_PATH.read_text(encoding="utf-8"))

    refs: dict[str, dict] = {}
    for reader_key, record in roster.items():
        groups = record.get("groups")
        if groups is None:  # pre-array roster entry -- see roster_groups()
            url = record.get("hypothesis_group_url")
            groups = [{"url": url, "name": None}] if url else []
        for g in groups:
            m = _GROUP_ID_RE.search(g.get("url") or "")
            if not m:
                continue
            gid = m.group(1)
            entry = refs.setdefault(gid, {"name": g.get("name"), "readers": []})
            entry["readers"].append(reader_key)
            # If two readers recorded different names for the same id,
            # keep the first but note the internal disagreement too --
            # that is itself a sync problem worth surfacing.
            if g.get("name") and entry["name"] and g.get("name") != entry["name"]:
                entry.setdefault("internal_name_conflict", set()).add(g.get("name"))
    return refs


def main() -> int:
    try:
        client = HypothesisClient()
        live_groups = client.profile_groups()
    except HypothesisError as e:
        print(f"ERROR fetching groups from Hypothesis: {e}", file=sys.stderr)
        return 1

    live = {g["id"]: g.get("name", g["id"]) for g in live_groups}
    roster = roster_group_refs()

    live_ids = set(live)
    roster_ids = set(roster)

    missing_from_roster = live_ids - roster_ids
    missing_from_hypothesis = roster_ids - live_ids
    name_mismatches = {
        gid: (roster[gid]["name"], live[gid])
        for gid in (live_ids & roster_ids)
        if roster[gid]["name"] and roster[gid]["name"] != live[gid]
    }
    internal_conflicts = {
        gid: roster[gid]["internal_name_conflict"] | {roster[gid]["name"]}
        for gid in roster
        if roster[gid].get("internal_name_conflict")
    }

    problems = bool(missing_from_roster or missing_from_hypothesis
                     or name_mismatches or internal_conflicts)

    print(f"Live groups on Hypothesis (this account): {len(live_ids)}")
    print(f"Groups referenced in invite_roster.json:  {len(roster_ids)}")
    print()

    if missing_from_roster:
        print(f"⚠ On Hypothesis but NOT in the roster ({len(missing_from_roster)}) "
              f"-- invisible to every reader's group picker until added:")
        for gid in sorted(missing_from_roster):
            print(f"    {live[gid]!r}  (id: {gid})")
        print()

    if missing_from_hypothesis:
        print(f"⚠ In the roster but NOT among this account's live groups "
              f"({len(missing_from_hypothesis)}) -- deleted, renamed away "
              f"from this id, or this account is no longer a member:")
        for gid in sorted(missing_from_hypothesis):
            entry = roster[gid]
            readers = ", ".join(entry["readers"])
            print(f"    {entry['name']!r}  (id: {gid}, readers: {readers})")
        print()

    if name_mismatches:
        print(f"⚠ Same group id, different name on each side ({len(name_mismatches)}) "
              f"-- likely renamed on Hypothesis after the roster was written:")
        for gid, (roster_name, live_name) in sorted(name_mismatches.items()):
            readers = ", ".join(roster[gid]["readers"])
            print(f"    id {gid}: roster says {roster_name!r}, "
                  f"Hypothesis says {live_name!r}  (readers: {readers})")
        print()

    if internal_conflicts:
        print(f"⚠ Roster itself disagrees about one group's name across readers "
              f"({len(internal_conflicts)}):")
        for gid, names in sorted(internal_conflicts.items()):
            readers = ", ".join(roster[gid]["readers"])
            print(f"    id {gid}: {sorted(names)}  (readers: {readers})")
        print()

    if not problems:
        print("✓ In sync -- every live group is in the roster, every roster "
              "group is live, and every name matches.")
        return 0

    print(f"Edit {ROSTER_PATH.relative_to(ROSTER_PATH.parent.parent)} by hand to resolve, "
          f"then rebuild the site so groupsAllowlist picks up the change.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
