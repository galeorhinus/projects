#!/usr/bin/env python3
"""request_access.py — loopback-only access-request handler, two flows.

1. Generic form at "/" (Caddy: /as/request-access) — for strangers you
   don't know. Every submission needs manual review; see README.

2. Named invites at "/<slug>" (Caddy: /as/invite/<slug>) — for people you
   deliberately invited by name. Creating the invites.json entry IS the
   approval, so submissions here are handled by trust tier:
     - no email on file for that slug         -> auto-whitelist whatever
                                                   they submit
     - submitted email matches the one on file -> auto-whitelist
     - submitted email differs from the one on
       file                                    -> falls back to the same
                                                   manual-review path as
                                                   the generic form

Neither flow grants access on its own beyond the trust rules above — the
"different email" case always needs a human. See server/README.md for the
full deployment and review workflow.

Pure standard library, deliberately — no pip install on the server.
"""

from __future__ import annotations

import fcntl
import html
import json
import re
import smtplib
import subprocess
import time
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

# --- Configuration — adjust for your deployment -----------------------------

BIND_HOST = "127.0.0.1"
BIND_PORT = 8090

# Append-only request log, outside the web root, never git-tracked.
LOG_PATH = Path("/var/lib/secondshanti/access-requests.log")

# Named-invite records — one JSON object keyed by slug. See
# server/invites.example.json for the schema. Never git-tracked (contains
# real names/emails); lives only on the server.
INVITES_PATH = Path("/etc/secondshanti/invites.json")

# oauth2-proxy's email whitelist. Auto-whitelisting appends here directly.
WHITELIST_PATH = Path("/etc/oauth2-proxy/authenticated-emails.txt")

# Optional command run after appending to the whitelist, e.g. to make
# oauth2-proxy pick up the change. Leave as None to skip (and reload
# manually) unless you've confirmed oauth2-proxy needs a nudge and have
# granted the service user narrow, passwordless sudo for exactly this:
#   WHITELIST_RELOAD_COMMAND = ["sudo", "/bin/systemctl", "restart", "oauth2-proxy"]
WHITELIST_RELOAD_COMMAND: list[str] | None = None

OWNER_EMAIL = "rhinusgaleo@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "rhinusgaleo@gmail.com"
# One line, no trailing newline, chmod 600, owned by the service user.
SMTP_APP_PASSWORD_FILE = Path("/etc/secondshanti/smtp-app-password")

# Per-IP throttle: at most one submission every RATE_LIMIT_SECONDS.
RATE_LIMIT_SECONDS = 60
_last_submission_by_ip: dict[str, float] = {}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# --- Shared page chrome ------------------------------------------------------

PAGE_HTML = """<!doctype html>
<html><head><meta charset="utf-8">
<title>{title} &mdash; Atomic Sanskrit</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/as/favicon.svg?v=2" type="image/svg+xml">
<link rel="icon" href="/as/favicon.ico" sizes="any">
<style>
  body {{ font-family: Georgia, 'Charter', serif; max-width: 32em; margin: 4em auto;
         padding: 0 1.5em; color: #2b2b2d; line-height: 1.5; }}
  h1 {{ font-size: 1.4em; }}
  .kicker {{ display: flex; align-items: center; gap: 0.8em; margin-bottom: 0.3em; }}
  .kicker-icon svg {{ display: block; width: 40px; height: 40px; }}
  .kicker-title {{ font-size: 0.95em; font-weight: bold; letter-spacing: 0.02em; color: #9a7833; }}
  .kicker-subtitle {{ font-size: 0.8em; color: #666; font-style: italic; margin-top: 0.1em; }}
  .action {{ font-size: 1.05em; }}
  label {{ display: block; margin-top: 1.2em; font-weight: bold; }}
  input[type=text], input[type=email], textarea {{
    width: 100%; padding: 0.5em; font-size: 1em; margin-top: 0.3em;
    box-sizing: border-box; font-family: inherit; border: 1px solid #999;
  }}
  button {{
    margin-top: 1.5em; padding: 0.6em 1.4em; font-size: 1em; cursor: pointer;
    background: #2b2b2d; color: #f4f4f3; border: none;
  }}
  a.group-link {{
    display: inline-block; margin-top: 0.5em; padding: 0.6em 1.2em;
    background: #9a7833; color: #fff; text-decoration: none; border-radius: 4px;
  }}
  .hp {{ position: absolute; left: -9999px; }}
  p.note {{ color: #666; font-size: 0.9em; }}
  .explainer {{
    background: #f2ede2; border: 1px solid #e2dac9; border-radius: 4px;
    padding: 0.6em 1.2em; margin-top: 1.2em;
  }}
  .explainer summary {{ cursor: pointer; font-weight: bold; padding: 0.2em 0; }}
  .explainer[open] summary {{ margin-bottom: 0.4em; }}
  .explainer p {{ margin: 0.4em 0; }}
</style>
</head><body>
<h1>{heading}</h1>
{body}
</body></html>
"""


def page(title: str, heading: str, body: str) -> str:
    return PAGE_HTML.format(title=title, heading=heading, body=body)


# Book identity kicker — used on the named-invite pages, where a bare
# "Welcome, {name}" carries no visual sign of which book this is for.
# Title/subtitle match as_book.yaml exactly; not user input, so no
# html.escape() needed. The icon is inlined (not linked) so this page
# never depends on the static site's build state or asset paths — read
# once at import time, with a graceful empty fallback if the repo layout
# ever changes, since a missing icon shouldn't be able to take the whole
# service down.
_ICON_PATH = Path(__file__).parent.parent / "figures/_shared/icons/ic-engineered.svg"
try:
    _ENGINEERED_ICON_SVG = _ICON_PATH.read_text(encoding="utf-8")
except OSError:
    _ENGINEERED_ICON_SVG = ""

BOOK_KICKER = f"""<div class="kicker">
  <div class="kicker-icon">{_ENGINEERED_ICON_SVG}</div>
  <div class="kicker-text">
    <div class="kicker-title">Atomic Sanskrit</div>
    <div class="kicker-subtitle">The Radiant, Calibrant, and Fractal Architecture of Sanātan</div>
  </div>
</div>
"""


# --- Shared plumbing (logging, email, whitelist) ----------------------------


def send_notification_email(subject: str, body: str, reply_to: str) -> None:
    password = SMTP_APP_PASSWORD_FILE.read_text().strip()
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = OWNER_EMAIL
    msg["Reply-To"] = reply_to

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, password)
        server.send_message(msg)


def log_request(name: str, email: str, note: str, ip: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "name": name,
        "email": email,
        "note": note,
        "ip": ip,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _with_invites_lock(fn):
    """Run fn(invites_dict) -> invites_dict under an flock, then persist
    the returned dict. Simple advisory locking — traffic here is low
    enough that this is about correctness under rare concurrent hits,
    not throughput."""
    INVITES_PATH.parent.mkdir(parents=True, exist_ok=True)
    INVITES_PATH.touch(exist_ok=True)
    with INVITES_PATH.open("r+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            raw = f.read().strip()
            invites = json.loads(raw) if raw else {}
            invites = fn(invites)
            f.seek(0)
            f.truncate()
            json.dump(invites, f, indent=2, ensure_ascii=False)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    return invites


def load_invites() -> dict:
    if not INVITES_PATH.exists():
        return {}
    with INVITES_PATH.open(encoding="utf-8") as f:
        raw = f.read().strip()
    return json.loads(raw) if raw else {}


def update_invite(slug: str, **fields) -> dict:
    def apply(invites: dict) -> dict:
        record = invites.get(slug, {})
        record.update(fields)
        invites[slug] = record
        return invites

    return _with_invites_lock(apply)[slug]


def add_to_whitelist(email: str) -> None:
    WHITELIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if WHITELIST_PATH.exists():
        existing = {
            line.strip().lower()
            for line in WHITELIST_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    if email.strip().lower() in existing:
        return
    with WHITELIST_PATH.open("a", encoding="utf-8") as f:
        f.write(email.strip() + "\n")
    if WHITELIST_RELOAD_COMMAND:
        subprocess.run(WHITELIST_RELOAD_COMMAND, check=False)


# --- Flow 1: generic request-access form ("/") ------------------------------

GENERIC_FORM = """<p>{message}</p>
<form method="post">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required>

  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>

  <label for="note">How did you hear about this, or who invited you? (optional)</label>
  <textarea id="note" name="note" rows="3"></textarea>

  <div class="hp" aria-hidden="true">
    <label for="website">Website</label>
    <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
  </div>

  <button type="submit">Request access</button>
</form>
<p class="note">Requests are reviewed individually; you'll hear back by email.</p>
"""


def render_generic(message: str, show_form: bool = True) -> str:
    body = GENERIC_FORM.format(message=message) if show_form else f"<p>{message}</p>"
    return page("Request access", "Request access to <em>Atomic Sanskrit</em>", body)


def handle_generic_get() -> tuple[int, str]:
    return 200, render_generic("Fill in your details below.")


def handle_generic_post(fields: dict, ip: str) -> tuple[int, str]:
    if fields.get("website"):  # honeypot
        return 200, render_generic("Thanks — your request has been received.", show_form=False)

    name = fields.get("name", "").strip()
    email = fields.get("email", "").strip()
    note = fields.get("note", "").strip()

    if not name or not EMAIL_RE.match(email):
        return 400, render_generic("Please provide your name and a valid email address.")

    if _rate_limited(ip):
        return 429, render_generic("Please wait a moment before submitting again.")

    try:
        log_request(name, email, note, ip)
    except Exception as exc:
        print(f"request_access: log_request failed: {exc}")
        return 500, render_generic(
            "Something went wrong on our end — please try again in a few minutes, "
            "or email rhinusgaleo@gmail.com directly."
        )

    try:
        send_notification_email(
            f"Access request: {name} <{email}>",
            "New access request for Atomic Sanskrit\n\n"
            f"Name:  {name}\nEmail: {email}\nNote:  {note or '(none)'}\n"
            f"IP:    {ip}\nTime:  {time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n",
            reply_to=email,
        )
    except Exception as exc:
        print(f"request_access: email send failed: {exc}")

    return 200, render_generic(
        f"Thanks, {html.escape(name)} — your request has been received. "
        "You'll hear back by email once it's reviewed.",
        show_form=False,
    )


# --- Flow 2: named invites ("/<slug>") --------------------------------------

INVITE_FORM = """<p>{message}</p>

<p class="action"><strong>Before you start reading Atomic Sanskrit:</strong>
create a free account on Hypothesis, or sign in if you already have one —
it's how you'll annotate the book as you read.</p>

<p><a class="group-link" href="{group_url}" target="_blank" rel="noopener">
  Join your reading group on Hypothesis: {group_name}
</a></p>

<p class="note">New to Hypothesis? Clicking the button above will let you
create a free account on the spot — no extension or software to
install.</p>

<details class="explainer">
  <summary>What is Hypothesis?</summary>
  <p>It's a free tool for annotating directly on the book's pages as you
  read — highlight a passage, leave a note or a question, and see what
  others in your group have flagged. Nothing you write is public; it's
  visible only within your private group and to the author. Joining
  takes you straight into your private reading group — no separate
  approval step on their end.</p>
</details>

<p class="action">Once you've joined, come back here and confirm your
email below so we can set up your reading access on our side.</p>

<form method="post">
  <label for="email">Email</label>
  <input type="email" id="email" name="email" value="{email_value}" required>

  <label for="hypothesis_username">Your Hypothesis username (recommended)</label>
  <input type="text" id="hypothesis_username" name="hypothesis_username">

  <div class="hp" aria-hidden="true">
    <label for="website">Website</label>
    <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
  </div>

  <button type="submit">Continue</button>
</form>
"""


def render_invite_form(name: str, record: dict, message: str) -> str:
    body = BOOK_KICKER + INVITE_FORM.format(
        message=message,
        group_url=html.escape(record.get("hypothesis_group_url", "")),
        group_name=html.escape(record.get("hypothesis_group_name", "your group")),
        email_value=html.escape(record.get("email") or ""),
    )
    return page(f"Welcome, {name}", f"Welcome, {html.escape(name)}", body)


def render_invite_result(name: str, message: str) -> str:
    body = BOOK_KICKER + f"<p>{message}</p>"
    return page(f"Welcome, {name}", f"Welcome, {html.escape(name)}", body)


def render_not_found() -> str:
    return page(
        "Not found",
        "Invite link not recognized",
        "<p>This invite link isn't recognized. Please double-check the URL, "
        "or use the <a href=\"/as/request-access\">general request-access form</a> instead.</p>",
    )


def handle_invite_get(slug: str) -> tuple[int, str]:
    invites = load_invites()
    record = invites.get(slug)
    if not record:
        return 404, render_not_found()
    name = record.get("name", slug)
    return 200, render_invite_form(
        name, record, "Thank you for taking the time — glad to have you reading along."
    )


def handle_invite_post(slug: str, fields: dict, ip: str) -> tuple[int, str]:
    invites = load_invites()
    record = invites.get(slug)
    if not record:
        return 404, render_not_found()
    name = record.get("name", slug)

    if fields.get("website"):  # honeypot
        return 200, render_invite_result(name, "Thanks — you're all set.")

    email = fields.get("email", "").strip()
    hyp_username = fields.get("hypothesis_username", "").strip()

    if not EMAIL_RE.match(email):
        return 400, render_invite_form(name, record, "Please enter a valid email address.")

    if _rate_limited(ip):
        return 429, render_invite_form(name, record, "Please wait a moment before submitting again.")

    known_email = (record.get("email") or "").strip().lower()
    matches_known = (not known_email) or (email.lower() == known_email)

    update_invite(
        slug,
        submitted_email=email,
        hypothesis_username=hyp_username,
        submitted_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        status="whitelisted" if matches_known else "pending_review",
    )

    if matches_known:
        try:
            add_to_whitelist(email)
        except Exception as exc:
            print(f"request_access: add_to_whitelist failed for {slug}: {exc}")
            return 500, render_invite_form(
                name, record,
                "Something went wrong granting access — please try again shortly, "
                "or email rhinusgaleo@gmail.com directly.",
            )
        try:
            send_notification_email(
                f"Auto-approved: {name} ({slug})",
                f"{name} (invite '{slug}') confirmed their email and was auto-whitelisted.\n\n"
                f"Email:               {email}\n"
                f"Hypothesis username: {hyp_username or '(not given)'}\n"
                f"IP:                  {ip}\n"
                f"Time:                {time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n\n"
                "No action needed unless oauth2-proxy needs a manual reload "
                "to pick up the new whitelist entry.\n",
                reply_to=email,
            )
        except Exception as exc:
            print(f"request_access: notification email failed: {exc}")
        return 200, render_invite_result(
            name,
            "Thank you for joining us — you're all set. "
            '<a href="/as/book/">Head to the book here</a>.',
        )

    # Different email than expected: same manual-review path as the
    # generic form, just with clearer framing on what's odd about it.
    try:
        log_request(
            name, email,
            f"INVITE '{slug}' — different email than on file (expected {known_email})",
            ip,
        )
    except Exception as exc:
        print(f"request_access: log_request failed: {exc}")
        return 500, render_invite_form(
            name, record,
            "Something went wrong on our end — please try again in a few minutes, "
            "or email rhinusgaleo@gmail.com directly.",
        )
    try:
        send_notification_email(
            f"Review needed: {name} used a different email ({slug})",
            f"{name} (invite '{slug}') entered a DIFFERENT email than the one on file.\n\n"
            f"Expected: {known_email or '(none on file)'}\n"
            f"Submitted: {email}\n"
            f"Hypothesis username: {hyp_username or '(not given)'}\n"
            f"IP:   {ip}\n"
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n\n"
            "Add the submitted email to /etc/oauth2-proxy/authenticated-emails.txt "
            "yourself if this checks out.\n",
            reply_to=email,
        )
    except Exception as exc:
        print(f"request_access: notification email failed: {exc}")

    return 200, render_invite_result(
        name,
        "Thanks — that's a different email than we had on file for you, so "
        "we're double-checking before granting access. You'll hear back shortly.",
    )


# --- HTTP plumbing -----------------------------------------------------------


def _rate_limited(ip: str) -> bool:
    now = time.time()
    last = _last_submission_by_ip.get(ip, 0)
    if now - last < RATE_LIMIT_SECONDS:
        return True
    _last_submission_by_ip[ip] = now
    return False


class Handler(BaseHTTPRequestHandler):
    server_version = "RequestAccess/1.0"

    def log_message(self, fmt, *args):
        pass  # Caddy's own access log already records this upstream.

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", ""):
            status, body = handle_generic_get()
        else:
            status, body = handle_invite_get(path.strip("/"))
        self._send_html(status, body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8", errors="replace")
        fields = {k: v[0] for k, v in parse_qs(raw_body).items()}
        ip = self.client_address[0]

        path = self.path.split("?", 1)[0]
        if path in ("/", ""):
            status, body = handle_generic_post(fields, ip)
        else:
            status, body = handle_invite_post(path.strip("/"), fields, ip)
        self._send_html(status, body)

    def _send_html(self, status: int, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    server = ThreadingHTTPServer((BIND_HOST, BIND_PORT), Handler)
    print(f"request_access listening on {BIND_HOST}:{BIND_PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
