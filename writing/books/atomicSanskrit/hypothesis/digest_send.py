#!/usr/bin/env python3
"""digest_send.py -- email a summary of annotations new since the last
digest was sent, via the same Gmail SMTP app-password setup
server/request_access.py uses (smtp.gmail.com:587, STARTTLS).

Reads data/annotations.json (run pull_annotations.py and, optionally,
auto_tagger.py first -- this script never hits the Hypothesis or
Anthropic APIs itself). Tracks what it already reported in
digest_state.json (gitignored, local runtime state) so a cron'd run
only ever mails what's genuinely new -- created OR updated since the
last successful send.

Usage:
    python3 digest_send.py              # send if there's anything new
    python3 digest_send.py --dry-run    # print the digest, send nothing,
                                         # don't advance digest_state.json
    python3 digest_send.py --force      # send even if nothing is new
                                         # (e.g. a "still quiet" check-in)
    python3 digest_send.py --to EMAIL   # override the recipient
"""

from __future__ import annotations

import argparse
import json
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path

HYPOTHESIS_DIR = Path(__file__).parent
DATA_PATH = HYPOTHESIS_DIR / "data" / "annotations.json"
STATE_PATH = HYPOTHESIS_DIR / "digest_state.json"
SMTP_APP_PASSWORD_PATH = HYPOTHESIS_DIR / "smtp_app_password.txt"

# Same account and provider server/request_access.py already uses --
# one Gmail app password, reused rather than provisioning a second one.
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "rhinusgaleo@gmail.com"
DEFAULT_RECIPIENT = "rhinusgaleo@gmail.com"

DASHBOARD_NOTE = (
    "Full filterable view (search, tag/reader/chapter filters): "
    "see the Reader Margins artifact -- republish dashboard.html to get "
    "a fresh link if this one has gone stale."
)


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"last_seen_updated": ""}
    return json.loads(STATE_PATH.read_text())


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def load_smtp_password() -> str:
    if not SMTP_APP_PASSWORD_PATH.exists() or not SMTP_APP_PASSWORD_PATH.read_text().strip():
        raise RuntimeError(
            f"No password at {SMTP_APP_PASSWORD_PATH}. Create a Gmail app password "
            f"(https://myaccount.google.com/apppasswords) for {SMTP_USER} and paste "
            f"it as the only line in that file -- see hypothesis/README.md. "
            f"(Reuse the same app password server/request_access.py already has on "
            f"amrut, at /etc/secondshanti/smtp-app-password, if you have it handy --  "
            f"just copy the value, not the file.)"
        )
    return SMTP_APP_PASSWORD_PATH.read_text(encoding="utf-8").strip()


def excerpt(text: str, n: int = 160) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def format_annotation(a: dict) -> str:
    tags = a.get("tags", [])
    suggested = a.get("suggested_tags", [])
    tag_line = ""
    if tags:
        tag_line += f"  tags: {', '.join(tags)}\n"
    if suggested:
        tag_line += f"  suggested (AI, not on Hypothesis): {', '.join(suggested)}\n"

    quote = f'  quote: "{excerpt(a["quote"])}"\n' if a.get("quote") else ""
    chapter = a["uri"].rstrip("/").rsplit("/", 1)[-1]
    reply = " [reply]" if a.get("is_reply") else ""

    return (
        f"- {a['user']} on {chapter} ({a['group_name']}){reply}\n"
        f"{quote}"
        f'  comment: "{excerpt(a["text"])}"\n'
        f"{tag_line}"
    )


def build_digest_body(new_rows: list[dict], total_count: int) -> str:
    by_chapter: dict[str, list[dict]] = {}
    for a in new_rows:
        chapter = a["uri"].rstrip("/").rsplit("/", 1)[-1]
        by_chapter.setdefault(chapter, []).append(a)

    lines = [
        f"{len(new_rows)} new or updated annotation(s) since the last digest "
        f"({total_count} total across all groups).",
        "",
    ]
    for chapter in sorted(by_chapter):
        rows = by_chapter[chapter]
        lines.append(f"== {chapter} ({len(rows)}) ==")
        lines.append("")
        for a in sorted(rows, key=lambda r: r["created"]):
            lines.append(format_annotation(a))
        lines.append("")

    lines.append(DASHBOARD_NOTE)
    return "\n".join(lines)


def send_email(subject: str, body: str, recipient: str) -> None:
    password = load_smtp_password()
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = recipient

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, password)
        server.send_message(msg)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="print the digest, send nothing")
    parser.add_argument("--force", action="store_true", help="send even if nothing is new")
    parser.add_argument("--to", default=DEFAULT_RECIPIENT, help="override the recipient email")
    args = parser.parse_args()

    if not DATA_PATH.exists():
        print(f"No {DATA_PATH} -- run pull_annotations.py first.", file=sys.stderr)
        return 1

    annotations = json.loads(DATA_PATH.read_text())
    state = load_state()
    last_seen = state.get("last_seen_updated", "")

    # "updated" (not just "created") so a reader editing an old annotation,
    # or auto_tagger.py adding tags to one, both count as "new" for the
    # next digest -- not just brand-new annotations.
    new_rows = [a for a in annotations if a["updated"] > last_seen]
    new_rows.sort(key=lambda a: a["updated"])

    if not new_rows and not args.force:
        print("Nothing new since the last digest -- not sending.")
        return 0

    if new_rows:
        body = build_digest_body(new_rows, len(annotations))
        subject = f"Atomic Sanskrit reader digest -- {len(new_rows)} new"
    else:
        body = f"No new annotations since the last digest ({len(annotations)} total).\n\n{DASHBOARD_NOTE}"
        subject = "Atomic Sanskrit reader digest -- nothing new"

    if args.dry_run:
        print(f"Subject: {subject}\n")
        print(body)
        print("\n(dry run -- not sent, digest_state.json not advanced)")
        return 0

    try:
        send_email(subject, body, args.to)
    except Exception as e:
        print(f"ERROR sending digest: {e}", file=sys.stderr)
        return 1

    if new_rows:
        newest_updated = max(a["updated"] for a in new_rows)
        save_state({"last_seen_updated": newest_updated})

    print(f"Sent digest ({len(new_rows)} new) to {args.to}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
