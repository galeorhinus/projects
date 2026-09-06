#!/usr/bin/env python3
"""Create and check the Mailgun inbound routes that forward domain mail to Gmail.

Two named addresses are not much clicking, but the UI leaves no record of what
was configured or why, and a route that silently stops matching looks exactly
like mail that nobody sent. This script is the record: run it to create what is
missing, run it again any time to confirm nothing has drifted.

Usage:
    export MAILGUN_API_KEY=...          # the account's private API key
    python mail/setup_routes.py --dry-run
    python mail/setup_routes.py

Set MAILGUN_API_BASE=https://api.eu.mailgun.net for an EU-region account; the
US base is the default and an EU account returns 401 against it, which reads as
a bad key rather than the wrong region.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# Every address this account forwards, and where it goes. Adding a third domain
# means adding a line here and rerunning — the script only creates what is
# missing, so rerunning is safe.
FORWARDS: list[tuple[str, str]] = [
    ("paragtope@secondshanti.org", "paragtope@gmail.com"),
    ("paragtope@atomicsanskrit.org", "paragtope@gmail.com"),
]

DEFAULT_BASE = "https://api.mailgun.net"


def api(path: str, key: str, base: str, *, fields: list[tuple[str, str]] | None = None):
    """One Mailgun API call. POSTs form-encoded when `fields` is given.

    Mailgun takes a route's actions as repeated `action` fields rather than a
    list, so the payload is a list of pairs and not a dict.
    """
    url = f"{base}{path}"
    data = urllib.parse.urlencode(fields).encode() if fields else None
    request = urllib.request.Request(url, data=data)
    token = base64.b64encode(f"api:{key}".encode()).decode()
    request.add_header("Authorization", f"Basic {token}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")[:400]
        if exc.code == 401:
            raise SystemExit(
                "Mailgun rejected the credentials (401).\n"
                "  - MAILGUN_API_KEY must be the account's private API key, not a\n"
                "    domain sending key: the Routes API is account-scoped.\n"
                f"  - An EU-region account needs MAILGUN_API_BASE set; this ran against {base}."
            ) from None
        raise SystemExit(f"Mailgun {exc.code} on {path}: {body}") from None
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not reach {base}: {exc.reason}") from None


def expression_for(address: str) -> str:
    return f'match_recipient("{address}")'


def actions_for(destination: str) -> list[str]:
    # stop() keeps a later, broader route (a catch-all added someday) from
    # forwarding the same message a second time.
    return [f'forward("{destination}")', "stop()"]


def check_domains(key: str, base: str) -> None:
    """Report each domain's state. A route against an unverified domain is
    accepted by the API and then never fires, because mail never arrives."""
    wanted = {address.split("@", 1)[1] for address, _ in FORWARDS}
    try:
        listed = api("/v4/domains?limit=1000", key, base)
    except SystemExit:
        print("  (could not list domains — skipping the verification check)")
        return
    states = {d["name"]: d.get("state", "?") for d in listed.get("items", [])}
    for domain in sorted(wanted):
        state = states.get(domain)
        if state is None:
            print(f"  {domain}: NOT ADDED to this Mailgun account — add it first, "
                  "or mail will never reach the route")
        elif state != "active":
            print(f"  {domain}: state={state} — routes will not fire until the "
                  "DNS records verify")
        else:
            print(f"  {domain}: active")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="show what would be created, change nothing")
    args = parser.parse_args()

    key = os.environ.get("MAILGUN_API_KEY", "").strip()
    if not key:
        print("MAILGUN_API_KEY is not set.\n"
              "  export MAILGUN_API_KEY=...   (Mailgun → Settings → API Keys → "
              "private API key)", file=sys.stderr)
        return 1
    base = os.environ.get("MAILGUN_API_BASE", DEFAULT_BASE).rstrip("/")

    print(f"Mailgun {base}")
    print("Domains:")
    check_domains(key, base)

    existing = api("/v3/routes?limit=1000", key, base).get("items", [])
    by_expression = {route.get("expression", ""): route for route in existing}
    print(f"Routes: {len(existing)} already on the account")

    created = skipped = 0
    for address, destination in FORWARDS:
        expression = expression_for(address)
        actions = actions_for(destination)
        found = by_expression.get(expression)
        if found:
            # Same recipient, different destination, is drift worth naming
            # rather than quietly leaving alone.
            if found.get("actions") != actions:
                print(f"  {address}: EXISTS but forwards elsewhere — "
                      f"{found.get('actions')}")
                print(f"    leave it, or delete route {found.get('id')} and rerun")
            else:
                print(f"  {address} → {destination}: already correct")
            skipped += 1
            continue
        if args.dry_run:
            print(f"  {address} → {destination}: would create")
            created += 1
            continue
        api("/v3/routes", key, base, fields=[
            ("priority", "0"),
            ("description", f"Forward {address} to {destination}"),
            ("expression", expression),
            *[("action", action) for action in actions],
        ])
        print(f"  {address} → {destination}: created")
        created += 1

    verb = "would create" if args.dry_run else "created"
    print(f"{verb} {created}, left alone {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
