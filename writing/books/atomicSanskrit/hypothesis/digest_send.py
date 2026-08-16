#!/usr/bin/env python3
"""digest_send.py -- email a summary of annotations new since the last
digest was sent, via the same Gmail SMTP app-password setup
server/request_access.py uses (smtp.gmail.com:587, STARTTLS).

Sends a proper HTML email (with a plain-text fallback for clients that
want it) styled with the same palette and serif type as
secondshanti.org itself -- see templates/landing.html and
server/request_access.py's INVITE_PAGE_TEMPLATE for the source of
truth on the tokens reused here. Each annotation shows its chapter's
real title (linked to the chapter), the highlighted passage in its
surrounding sentence for context, the comment, and a direct
"View on Hypothesis" link -- our own domain plus the Hypothesis
client's #annotations:<id> fragment, not hyp.is (see annotation_link()).

Reads data/annotations.json (run pull_annotations.py and, optionally,
auto_tagger.py first -- this script never hits the Hypothesis or
Anthropic APIs itself). Tracks what it already reported in
digest_state.json (gitignored, local runtime state) so a cron'd run
only ever mails what's genuinely new -- created OR updated since the
last successful send.

Usage:
    python3 digest_send.py              # send if there's anything new
    python3 digest_send.py --dry-run    # write the digest to a local
                                         # .html file to preview, send
                                         # nothing, don't advance state
    python3 digest_send.py --force      # send even if nothing is new
                                         # (e.g. a "still quiet" check-in)
    python3 digest_send.py --to EMAIL   # override the recipient
"""

from __future__ import annotations

import argparse
import html
import json
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

HYPOTHESIS_DIR = Path(__file__).parent
DATA_PATH = HYPOTHESIS_DIR / "data" / "annotations.json"
STATE_PATH = HYPOTHESIS_DIR / "digest_state.json"
SMTP_APP_PASSWORD_PATH = HYPOTHESIS_DIR / "smtp_app_password.txt"
PREVIEW_PATH = HYPOTHESIS_DIR / "digest_preview.html"

# Same account and provider server/request_access.py already uses --
# one Gmail app password, reused rather than provisioning a second one.
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "rhinusgaleo@gmail.com"
DEFAULT_RECIPIENT = "rhinusgaleo@gmail.com"

# The live, self-refreshing dashboard on amrut (owner-only login --
# see the Caddyfile's @dashboard_notowner check), not the Claude
# Artifact -- the Artifact needs a manual republish and can drift
# stale, while this one is reinstalled by run_pipeline.sh on every
# cron run, same data the digest itself was just built from.
DASHBOARD_URL = "https://secondshanti.org/as/private/dashboard/"

# -- site design tokens, matching templates/landing.html / --
# request_access.py's INVITE_PAGE_TEMPLATE. Email clients strip
# webfont <link>/@import reliably enough that pulling in Gentium Book
# Plus isn't worth the risk here -- Georgia is the same serif fallback
# request_access.py's own simpler PAGE_HTML template already uses for
# the plainer pages on the site, so this stays visually "the site,"
# just via the branch of its own type stack built for robustness.
FONT_STACK = "Georgia, 'Charter', 'Iowan Old Style', 'Times New Roman', serif"
C = {
    "field": "#f4f4f3",
    "panel": "#fbf9f4",
    "sand": "#ece4d3",
    "sand2": "#f4efe4",
    "taupe": "#aa9a7a",
    "brown": "#766652",
    "deep": "#4a3f30",
    "gold": "#c19a4e",
    "gold_d": "#9a7833",
    "sun": "#cf8a2e",
    "ink": "#2b2b2d",
    "ink2": "#4a4136",
    "line": "#d8cfbd",
    "line2": "#c3b9a3",
}

# Six semantic clusters (same grouping build_dashboard.py uses) rendered
# in muted, earthy hues that stay inside the site's warm family rather
# than the dashboard's own cooler slate/indigo palette -- the two tools
# have different audiences (a private triage view vs. this personal
# email) and don't need to share a color system, just a family feel.
TAG_CLUSTERS = {
    "typo": "mechanical",
    "factual": "verify",
    "citation-needed": "verify",
    "unclear": "clarify",
    "question": "clarify",
    "structural": "constructive",
    "suggestion": "constructive",
    "translation": "precision",
    "praise": "positive",
}
CLUSTER_COLORS = {
    "mechanical": ("#ece4d3", "#766652"),
    "verify": ("#f3ded0", "#a15226"),
    "clarify": ("#f6ecc9", "#8a6a10"),
    "constructive": ("#dbe6e4", "#3a6b64"),
    "precision": ("#e8dde8", "#6d3f7a"),
    "positive": ("#e1ecd7", "#4a7a2e"),
}


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


def excerpt(text: str, n: int = 220) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def clean_title(title: str) -> str:
    """Strip the trailing site suffix and convert the raw *emphasis*
    markdown some document titles carry (e.g. 'Building the *Dhātuḥ*')
    into real <em> once escaped -- these titles come straight from the
    page's own <title> tag, asterisks and all."""
    return re.sub(r"\s+—\s+Atomic Sanskrit\s*$", "", title).strip()


def emphasize(escaped_title: str) -> str:
    """Run on an already-html.escape()'d title: turn *word* into
    <em>word</em>. Safe post-escape since '*' isn't touched by escaping."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped_title)


def annotation_link(annotation_id: str, uri: str) -> str:
    """Deep-link on our own domain via the Hypothesis client's own
    #annotations:<id> fragment convention -- see build_dashboard.py's
    annotation_link() docstring for the full rationale. NOT hyp.is:
    that relay falls back to hypothes.is's "Via" proxy for any browser
    without the extension (most mobile browsers), and Via started
    returning "Access to Via is now restricted" as of 2026-08-16."""
    return f"{uri.rstrip('/')}/#annotations:{annotation_id}"


def chapter_slug(uri: str) -> str:
    return uri.rstrip("/").rsplit("/", 1)[-1]


def cluster_colors(tag: str) -> tuple[str, str]:
    return CLUSTER_COLORS[TAG_CLUSTERS.get(tag, "mechanical")]


# --- plain-text fallback -----------------------------------------------

def format_annotation_text(a: dict) -> str:
    tags = a.get("tags", [])
    suggested = a.get("suggested_tags", [])
    tag_line = ""
    if tags:
        tag_line += f"  tags: {', '.join(tags)}\n"
    if suggested:
        tag_line += f"  suggested (AI, not on Hypothesis): {', '.join(suggested)}\n"

    context = ""
    if a.get("quote"):
        context = (
            f'  context: "…{excerpt(a.get("quote_prefix", ""), 60)}'
            f'[{excerpt(a["quote"], 200)}]'
            f'{excerpt(a.get("quote_suffix", ""), 60)}…"\n'
        )

    reply = " [reply]" if a.get("is_reply") else ""
    return (
        f"- {a['user']} on {clean_title(a['document_title'])} ({a['group_name']}){reply}\n"
        f"  link: {annotation_link(a['id'], a['uri'])}\n"
        f"{context}"
        f'  comment: "{excerpt(a["text"])}"\n'
        f"{tag_line}"
    )


def build_digest_text(new_rows: list[dict], total_count: int) -> str:
    by_chapter: dict[str, list[dict]] = {}
    for a in new_rows:
        by_chapter.setdefault(clean_title(a["document_title"]), []).append(a)

    lines = [
        f"{len(new_rows)} new or updated annotation(s) since the last digest "
        f"({total_count} total across all groups).",
        "",
    ]
    for title in sorted(by_chapter):
        rows = by_chapter[title]
        lines.append(f"== {title} ({len(rows)}) ==")
        lines.append("")
        for a in sorted(rows, key=lambda r: r["created"]):
            lines.append(format_annotation_text(a))
        lines.append("")

    lines.append(f"Full filterable dashboard: {DASHBOARD_URL}")
    return "\n".join(lines)


# --- HTML ----------------------------------------------------------------

def tag_chip_html(tag: str, suggested: bool) -> str:
    bg, fg = cluster_colors(tag)
    style = (
        f"display:inline-block;font-size:11px;font-weight:700;letter-spacing:.02em;"
        f"padding:2px 9px;border-radius:999px;margin:0 6px 6px 0;font-family:{FONT_STACK};"
    )
    if suggested:
        style += f"background:transparent;color:{fg};border:1px dashed {fg};opacity:.85;"
        label = f"{html.escape(tag)} · AI"
    else:
        style += f"background:{bg};color:{fg};"
        label = html.escape(tag)
    return f'<span style="{style}">{label}</span>'


def context_html(a: dict) -> str:
    if not a.get("quote"):
        return ""
    prefix = html.escape(excerpt(a.get("quote_prefix", ""), 80))
    exact = html.escape(excerpt(a["quote"], 260))
    suffix = html.escape(excerpt(a.get("quote_suffix", ""), 80))
    mark_style = f'background:{C["sand"]};color:{C["deep"]};padding:0 2px;border-radius:2px;'
    return f"""<div style="margin:0 0 12px;padding:8px 14px;border-left:3px solid {C['gold']};
      background:{C['sand2']};font-family:{FONT_STACK};font-size:14px;line-height:1.6;
      color:{C['brown']};font-style:italic;">
      …{prefix}<mark style="{mark_style}">{exact}</mark>{suffix}…
    </div>"""


def card_html(a: dict) -> str:
    tag_html = "".join(tag_chip_html(t, False) for t in a.get("tags", [])) + \
               "".join(tag_chip_html(t, True) for t in a.get("suggested_tags", []))
    reply = (
        f'<span style="font-size:11px;color:{C["taupe"]};border:1px solid {C["line2"]};'
        f'border-radius:999px;padding:1px 8px;margin-left:8px;">reply</span>'
        if a.get("is_reply") else ""
    )
    link = annotation_link(a["id"], a["uri"])
    date = a["created"][:10]

    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
      style="margin:0 0 14px;background:#ffffff;border:1px solid {C['line']};border-radius:6px;">
      <tr><td style="padding:16px 18px;">
        <div style="font-family:{FONT_STACK};font-size:13px;color:{C['brown']};margin-bottom:10px;">
          <strong style="color:{C['ink']};">{html.escape(a['user'])}</strong>
          &nbsp;·&nbsp;{html.escape(a['group_name'])}&nbsp;·&nbsp;{date}{reply}
          &nbsp;·&nbsp;<a href="{link}" style="color:{C['gold_d']};text-decoration:none;font-weight:700;">View on Hypothesis →</a>
        </div>
        {context_html(a)}
        <div style="font-family:{FONT_STACK};font-size:15px;line-height:1.55;color:{C['ink2']};margin-bottom:10px;white-space:pre-wrap;">{html.escape(a['text'])}</div>
        <div>{tag_html}</div>
      </td></tr>
    </table>"""


def chapter_section_html(title: str, uri: str, rows: list[dict]) -> str:
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:26px 0 10px;">
      <tr><td style="border-bottom:2px solid {C['gold']};padding-bottom:6px;">
        <a href="{html.escape(uri)}" style="font-family:{FONT_STACK};font-size:18px;font-weight:700;
          color:{C['gold_d']};text-decoration:none;">{emphasize(html.escape(title))}</a>
        <span style="font-family:{FONT_STACK};font-size:13px;color:{C['taupe']};margin-left:8px;">({len(rows)})</span>
      </td></tr>
    </table>""" + "".join(card_html(a) for a in sorted(rows, key=lambda r: r["created"]))


def build_digest_html(new_rows: list[dict], total_count: int) -> str:
    by_title: dict[str, tuple[str, list[dict]]] = {}
    for a in new_rows:
        title = clean_title(a["document_title"])
        uri = a["uri"]
        by_title.setdefault(title, (uri, []))[1].append(a)

    sections = "".join(
        chapter_section_html(title, uri, rows)
        for title, (uri, rows) in sorted(by_title.items())
    )

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:0;background:{C['field']};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{C['field']};">
<tr><td align="center" style="padding:28px 14px;">
<table role="presentation" width="640" cellpadding="0" cellspacing="0"
  style="max-width:640px;width:100%;background:{C['panel']};border:1px solid {C['line']};border-radius:8px;overflow:hidden;">
  <tr><td style="background:{C['deep']};padding:22px 26px;">
    <div style="font-family:{FONT_STACK};font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:{C['gold']};font-weight:700;">Atomic Sanskrit</div>
    <div style="font-family:{FONT_STACK};font-size:22px;color:{C['sand2']};margin-top:4px;font-weight:700;">Reader Digest</div>
  </tr></td>
  <tr><td style="padding:22px 26px 4px;">
    <p style="font-family:{FONT_STACK};font-size:15px;color:{C['ink2']};margin:0;">
      <strong>{len(new_rows)}</strong> new or updated annotation{"s" if len(new_rows) != 1 else ""} since the last digest
      &mdash; {total_count} total across all reading groups.
    </p>
  </td></tr>
  <tr><td style="padding:0 26px 22px;">
    {sections}
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;border-top:1px solid {C['line']};">
      <tr><td style="padding-top:16px;font-family:{FONT_STACK};font-size:13px;color:{C['brown']};line-height:1.6;">
        <a href="{DASHBOARD_URL}" style="color:{C['gold_d']};font-weight:700;text-decoration:none;">Open the full filterable dashboard →</a><br>
        Tags shown with a dashed outline are AI-suggested only &mdash; the annotation's author didn't tag it and this
        token can't write tags to another reader's annotation, so they exist only here and in the dashboard, not on Hypothesis itself.
      </td></tr>
    </table>
  </td></tr>
</table>
</td></tr>
</table>
</body></html>"""


def send_email(subject: str, text_body: str, html_body: str, recipient: str) -> None:
    password = load_smtp_password()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = recipient
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, password)
        server.send_message(msg)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="write digest_preview.html, send nothing")
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
        text_body = build_digest_text(new_rows, len(annotations))
        html_body = build_digest_html(new_rows, len(annotations))
        subject = f"Atomic Sanskrit reader digest -- {len(new_rows)} new"
    else:
        text_body = f"No new annotations since the last digest ({len(annotations)} total).\n\nDashboard: {DASHBOARD_URL}"
        html_body = build_digest_html([], len(annotations))
        subject = "Atomic Sanskrit reader digest -- nothing new"

    if args.dry_run:
        PREVIEW_PATH.write_text(html_body, encoding="utf-8")
        print(f"Subject: {subject}\n")
        print(text_body)
        print(f"\n(dry run -- not sent, digest_state.json not advanced; HTML preview written to {PREVIEW_PATH})")
        return 0

    try:
        send_email(subject, text_body, html_body, args.to)
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
