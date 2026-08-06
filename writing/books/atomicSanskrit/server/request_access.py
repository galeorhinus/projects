#!/usr/bin/env python3
"""request_access.py — loopback-only "request access" form handler.

Serves the public /as/request-access form (Caddy proxies it here, no
oauth2-proxy gate — this endpoint is how someone WITHOUT access yet gets
in touch). On submission: validates input, appends a JSON-line record to
LOG_PATH, and emails OWNER_EMAIL so a human decides whether to add the
requester to the oauth2-proxy whitelist and a Hypothesis group.

This never grants access itself — it only ever creates a request. See
server/README.md for the full deployment and review workflow.

Pure standard library, deliberately — no pip install on the server.
"""

from __future__ import annotations

import html
import json
import re
import smtplib
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

PAGE_HTML = """<!doctype html>
<html><head><meta charset="utf-8">
<title>Request access &mdash; Atomic Sanskrit</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: Georgia, 'Charter', serif; max-width: 32em; margin: 4em auto;
         padding: 0 1.5em; color: #2b2b2d; line-height: 1.5; }}
  h1 {{ font-size: 1.4em; }}
  label {{ display: block; margin-top: 1.2em; font-weight: bold; }}
  input[type=text], input[type=email], textarea {{
    width: 100%; padding: 0.5em; font-size: 1em; margin-top: 0.3em;
    box-sizing: border-box; font-family: inherit; border: 1px solid #999;
  }}
  button {{
    margin-top: 1.5em; padding: 0.6em 1.4em; font-size: 1em; cursor: pointer;
    background: #2b2b2d; color: #f4f4f3; border: none;
  }}
  .hp {{ position: absolute; left: -9999px; }}
  p.note {{ color: #666; font-size: 0.9em; }}
</style>
</head><body>
<h1>Request access to <em>Atomic Sanskrit</em></h1>
<p>{message}</p>
{form}
</body></html>
"""

FORM_BLOCK = """<form method="post">
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


def render(message: str, show_form: bool = True) -> str:
    return PAGE_HTML.format(message=message, form=FORM_BLOCK if show_form else "")


def send_owner_email(name: str, email: str, note: str, ip: str) -> None:
    password = SMTP_APP_PASSWORD_FILE.read_text().strip()
    body = (
        "New access request for Atomic Sanskrit\n\n"
        f"Name:  {name}\n"
        f"Email: {email}\n"
        f"Note:  {note or '(none)'}\n"
        f"IP:    {ip}\n"
        f"Time:  {time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
    )
    msg = MIMEText(body)
    msg["Subject"] = f"Access request: {name} <{email}>"
    msg["From"] = SMTP_USER
    msg["To"] = OWNER_EMAIL
    msg["Reply-To"] = email

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


class Handler(BaseHTTPRequestHandler):
    server_version = "RequestAccess/1.0"

    def log_message(self, fmt, *args):
        pass  # Caddy's own access log already records this upstream.

    def do_GET(self):
        if self.path.split("?", 1)[0] not in ("/", ""):
            self.send_response(404)
            self.end_headers()
            return
        self._send_html(200, render("Fill in your details below."))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        fields = {k: v[0] for k, v in parse_qs(body).items()}

        # Honeypot: real visitors never see or fill this field.
        if fields.get("website"):
            self._send_html(200, render("Thanks — your request has been received.", show_form=False))
            return

        name = fields.get("name", "").strip()
        email = fields.get("email", "").strip()
        note = fields.get("note", "").strip()

        if not name or not EMAIL_RE.match(email):
            self._send_html(400, render("Please provide your name and a valid email address."))
            return

        ip = self.client_address[0]
        now = time.time()
        last = _last_submission_by_ip.get(ip, 0)
        if now - last < RATE_LIMIT_SECONDS:
            self._send_html(429, render("Please wait a moment before submitting again."))
            return
        _last_submission_by_ip[ip] = now

        try:
            log_request(name, email, note, ip)
        except Exception as exc:
            # Can't durably record the request — tell the visitor plainly
            # rather than dropping the connection, and surface it in the
            # service's own logs (journalctl) so it gets noticed and fixed.
            print(f"request_access: log_request failed: {exc}")
            self._send_html(
                500,
                render("Something went wrong on our end — please try again in a few minutes, "
                       "or email rhinusgaleo@gmail.com directly."),
            )
            return

        try:
            send_owner_email(name, email, note, ip)
        except Exception as exc:
            # Request is already durably logged even if the email bounces.
            print(f"request_access: email send failed: {exc}")

        self._send_html(
            200,
            render(
                f"Thanks, {html.escape(name)} — your request has been received. "
                "You'll hear back by email once it's reviewed.",
                show_form=False,
            ),
        )

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
