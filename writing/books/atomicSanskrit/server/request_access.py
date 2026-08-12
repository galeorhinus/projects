#!/usr/bin/env python3
"""request_access.py — loopback-only access-request handler, two flows.

1. Generic form at "/" (Caddy: /as/request-access) — for strangers you
   don't know. Every submission needs manual review; see README.

2. Named invites at "/<slug>" (Caddy: /as/invite/<slug>) — for people you
   deliberately invited by name. The roster (invite_roster.json) is
   admin-authored and git-tracked, deployed read-only to the server; the
   status file (invite_status.json) is what this service writes live as
   people actually use their links. Submissions are handled by trust
   tier, checked against whichever of the two is relevant:

     - roster has a known email for the slug:
         submitted matches it   -> auto-whitelist
         submitted differs      -> manual review
     - roster has no known email for the slug (bare link, trust-on-
       first-use):
         first submission ever  -> auto-whitelist, and lock that email
                                    in as the slug's now-known email
         same email again       -> idempotent no-op ("you already have
                                    access"), no new grant, no email noise
         a DIFFERENT email shows
         up after the slug is
         already locked          -> NOT auto-whitelisted — flagged for
                                    manual review as a possible leaked
                                    invite link, without disturbing the
                                    original successful grant on record

Neither flow grants access on its own beyond the trust rules above — a
mismatched or post-lock email always needs a human. See server/README.md
for the full deployment and review workflow.

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
from string import Template
from urllib.parse import parse_qs

# --- Configuration — adjust for your deployment -----------------------------

BIND_HOST = "127.0.0.1"
BIND_PORT = 8090

# Append-only request log, outside the web root, never git-tracked.
LOG_PATH = Path("/var/lib/secondshanti/access-requests.log")

# Named-invite roster — one JSON object keyed by slug, admin-authored
# (see add_invite.py), git-tracked at server/invite_roster.json, and
# deployed here read-only by deploy.sh. The running service never writes
# this file — see server/README.md and the systemd unit's ReadWritePaths
# for the enforcement. Schema: server/invite_roster.example.json.
ROSTER_PATH = Path("/etc/secondshanti/invite_roster.json")

# Live status per slug — submitted_email, hypothesis_username,
# submitted_at, status, used, locked_email, and any flagged repeat
# attempts. Written only by this service as people use their links.
# Never git-tracked; lives only on the server.
STATUS_PATH = Path("/etc/secondshanti/invite_status.json")

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


# --- Named-invite page: dedicated template ----------------------------------
#
# Structurally distinct from PAGE_HTML (two-column layout, reader/group
# identity sidebar) and specific to the invite flow's content, so it gets
# its own template rather than being forced through the shared one used
# by the generic request-access form and the 404 page.
#
# Source: a Claude Design mockup (as_design_invite1.html), integrated
# 2026-08-11. The icon is a self-contained inline SVG <symbol>/<use> pair
# — no external file dependency at all, so the /opt/secondshanti deploy-
# path gotcha that bit the previous version of this page (see git history
# on this file) can't recur here.
#
# Uses string.Template ($name, not {name}) specifically because the CSS
# below is full of literal curly braces that str.format() would otherwise
# require doubling throughout — Template's $-syntax has no such conflict.
INVITE_PAGE_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<link rel="icon" href="/as/favicon.svg?v=2" type="image/svg+xml">
<link rel="icon" href="/as/favicon.ico" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400;1,700&family=Noto+Serif+Devanagari:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{
  --field:#f4f4f3;--panel:#fbf9f4;--sand:#ece4d3;--sand2:#f4efe4;
  --taupe:#aa9a7a;--brown:#766652;--deep:#4a3f30;
  --gold:#c19a4e;--gold-d:#9a7833;--sun:#cf8a2e;
  --ink:#2b2b2d;--ink2:#4a4136;--line:#d8cfbd;--line2:#c3b9a3;
  --lat:'Gentium Book Plus',Charter,'Charis SIL',Georgia,serif;
  --dev:'Noto Serif Devanagari','Adobe Devanagari',serif;
}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%;color:var(--ink);font-family:var(--lat);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--gold-d)}a:hover{color:var(--deep)}

/* ============ shared page bits ============ */
.btn{display:inline-block;font-family:var(--lat);font-size:16px;font-weight:700;text-decoration:none;border:0;border-radius:4px;padding:14px 26px;cursor:pointer;line-height:1.2}
.field{display:block;width:100%;font-family:var(--lat);font-size:16px;padding:11px 13px;border:1px solid var(--line2);border-radius:3px;background:#fff;color:var(--ink)}
.field:focus{outline:2px solid var(--gold);outline-offset:-1px}
label.lbl{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--brown);font-weight:700;margin:0 0 6px}
.hp{position:absolute;left:-9999px}

/* ============ shared lockup ============ */
.lockup{display:flex;align-items:center;gap:18px}
.lockup .mk{flex:none}
.lockup .tt{min-width:0}
.lockup .tt .bt{font-size:30px;font-weight:700;letter-spacing:-.012em;line-height:1.1;margin:0}
.lockup .tt .st{font-size:14.5px;color:var(--brown);line-height:1.45;margin:6px 0 0}
.lockup.sm .tt .bt{font-size:24px}
.lockup.sm .tt .st{font-size:13.5px;margin-top:4px}

/* ============ responsive: split wide, pass narrow ============ */
.R{min-height:100%;display:grid;grid-template-columns:44% 56%;background:var(--field)}
.R .left{background:var(--sand);padding:52px 40px;display:flex;flex-direction:column;justify-content:space-between;border-right:1px solid var(--line2)}
.R .series{font-size:11.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold-d);font-weight:700}
.R .left .big{margin-top:30px}
.R .left .who{margin-top:34px;padding-top:20px;border-top:1px solid var(--line2)}
.R .left .who .k{font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--brown);font-weight:700}
.R .left .who .v{font-size:19px;font-weight:700;margin-top:3px}
.R .left .who .v.grp{color:var(--gold-d);font-size:17px}
.R .left .rail{font-size:13.5px;color:var(--brown);font-style:italic;line-height:1.55;margin:26px 0 0}
.R .right{background:var(--panel);padding:52px 44px 70px;overflow:auto}
.R .lede{font-size:17px;line-height:1.62;color:var(--ink2);margin:0 0 6px;max-width:52ch}
.R .sec{margin-top:30px;padding-top:22px;border-top:1px solid var(--line)}
.R .sec .n{font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-d);font-weight:700}
.R .sec h3{font-size:21px;margin:8px 0 10px;font-weight:700}
.R .sec p{font-size:15px;line-height:1.62;color:var(--ink2);margin:0}
.R .sec p+p{margin-top:9px}
.R .sec p.fine{font-size:13.5px;color:var(--brown);font-style:italic;margin-top:10px}
.R .cta{background:var(--sun);color:#3a2a12;margin-top:16px}
.R .cta:hover{background:#b8781f}
.R .form{display:grid;gap:14px;margin-top:15px;max-width:390px}
.R .submit{background:var(--deep);color:#f6f2e8;justify-self:start;padding:12px 30px}
.R .submit:hover{background:#2f2820}
.R .code{background:#e9b96a;border:1px solid #c9973f;padding:2px 8px;border-radius:3px;font-weight:700;font-size:13.5px;color:#3a2a12}
.R .perf{display:none;height:0;border-top:2px dashed var(--line2);position:relative;margin:26px 0 0}
.R .perf::before,.R .perf::after{content:"";position:absolute;top:-11px;width:20px;height:20px;border-radius:50%;background:#ece7dc;border:1px solid var(--line2)}
.R .perf::before{left:-41px}.R .perf::after{right:-41px}
@media(max-width:760px){
  .R{display:block;background:repeating-linear-gradient(45deg,#efeae0 0 14px,#ece7dc 14px 28px);padding:38px 24px 60px}
  .R .left,.R .right{background:var(--panel);border:1px solid var(--line2);max-width:560px;margin:0 auto;display:block;padding:28px 30px;box-shadow:0 24px 54px -34px rgba(60,40,10,.8)}
  .R .left{border-radius:6px 6px 0 0;border-bottom:0}
  .R .right{border-radius:0 0 6px 6px;border-top:0;padding-top:6px;overflow:visible}
  .R .left .who{margin-top:22px;padding-top:16px}
  .R .left .rail{display:none}
  .R .left .who:last-of-type{display:none}
  .R .perf{display:block}
  .R .sec:first-of-type{border-top:0;padding-top:14px;margin-top:14px}
  .R .submit,.R .cta{width:100%;text-align:center;justify-self:stretch}
}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="mk-eng" viewBox="4 8 88 84"><path fill="#e6c98f" d="M53.5,50.8L42.5,31.9H20.7L9.8,50.8l10.9,18.9h21.9L53.5,50.8z"/><path fill="#cf8a2e" d="M86.3,31.9L75.3,13H53.5L42.5,31.9l10.9,18.9h21.9L86.3,31.9z"/><path fill="none" stroke="#766652" stroke-width="3.4" stroke-linejoin="round" d="M53.5,50.8L42.5,31.9H20.7L9.8,50.8l10.9,18.9h21.9L53.5,50.8z"/><path fill="none" stroke="#766652" stroke-width="3.4" stroke-linejoin="round" d="M86.3,31.9L75.3,13H53.5L42.5,31.9l10.9,18.9h21.9L86.3,31.9z"/><g fill="none" stroke="#aa9a7a" stroke-width="2.5" stroke-linecap="round"><line x1="14.1" y1="87.4" x2="82.1" y2="87.4"/><line x1="14.1" y1="87.4" x2="14.1" y2="79.5"/><line x1="82.1" y1="87.4" x2="82.1" y2="79.5"/><line x1="48" y1="87.4" x2="48.1" y2="79.5"/><line x1="30.8" y1="87.4" x2="30.8" y2="83.4"/><line x1="67.9" y1="87.4" x2="67.9" y2="83.4"/></g></symbol>
<symbol id="mk-eng-rev" viewBox="4 8 88 84"><path fill="#8a7350" d="M53.5,50.8L42.5,31.9H20.7L9.8,50.8l10.9,18.9h21.9L53.5,50.8z"/><path fill="#e2a951" d="M86.3,31.9L75.3,13H53.5L42.5,31.9l10.9,18.9h21.9L86.3,31.9z"/><path fill="none" stroke="#efe6d2" stroke-width="3.4" stroke-linejoin="round" d="M53.5,50.8L42.5,31.9H20.7L9.8,50.8l10.9,18.9h21.9L53.5,50.8z"/><path fill="none" stroke="#efe6d2" stroke-width="3.4" stroke-linejoin="round" d="M86.3,31.9L75.3,13H53.5L42.5,31.9l10.9,18.9h21.9L86.3,31.9z"/><g fill="none" stroke="#c6b99d" stroke-width="2.5" stroke-linecap="round"><line x1="14.1" y1="87.4" x2="82.1" y2="87.4"/><line x1="14.1" y1="87.4" x2="14.1" y2="79.5"/><line x1="82.1" y1="87.4" x2="82.1" y2="79.5"/><line x1="48" y1="87.4" x2="48.1" y2="79.5"/><line x1="30.8" y1="87.4" x2="30.8" y2="83.4"/><line x1="67.9" y1="87.4" x2="67.9" y2="83.4"/></g></symbol>
</defs></svg>
<div class="R">
  <aside class="left">
    <div>
      <div class="series">A Second Shanti book</div>
      <div class="lockup big"><svg class="mk" width="66" height="63" aria-hidden="true"><use href="#mk-eng"/></svg><div class="tt"><p class="bt">Atomic Sanskrit</p><p class="st">The Radiant, Calibrant, and Fractal Architecture of Sanātan</p></div></div>
      <div class="who"><div class="k">Reader</div><div class="v">$name</div></div>
      <div class="who"><div class="k">Reading group</div><div class="v grp">$group_code</div></div>
    </div>
    <p class="rail">Annotations stay inside your private group — visible only to the group and the author.</p>
    <div class="perf"></div>
  </aside>
  <main class="right">
    <p class="lede">Welcome, $name. $message</p>
    $content
  </main>
</div>
</body>
</html>
""")


def _invite_form_content(group_url: str, group_code: str, email_value: str) -> str:
    return f"""<section class="sec">
  <div class="n">First</div>
  <h3>Create your Hypothesis account</h3>
  <p>Before you start reading Atomic Sanskrit, create a free account on Hypothesis — or sign in if you already have one. It's how you'll annotate the book as you read.</p>
  <p>Highlight a passage, leave a note or a question, and see what others in your group have flagged.</p>
  <a class="btn cta" href="{group_url}" target="_blank" rel="noopener">Join your reading group: <span class="code">{group_code}</span></a>
  <p class="fine">New to Hypothesis? Clicking above lets you create a free account on the spot — no extension or software to install. Joining takes you straight into your private reading group, with no separate approval step on their end.</p>
</section>
<section class="sec">
  <div class="n">Then</div>
  <h3>Confirm your email and username</h3>
  <p>Once you've joined, remember the username you signed up with. Come back here and confirm your email below — paste in that username too, so we can set up your reading access on our side.</p>
  <form class="form" method="post">
    <div><label class="lbl" for="email">Email</label><input class="field" id="email" name="email" type="email" value="{email_value}" required></div>
    <div><label class="lbl" for="hypothesis_username">Your Hypothesis username</label><input class="field" id="hypothesis_username" name="hypothesis_username" type="text" placeholder="recommended"></div>
    <input class="hp" type="text" name="website" id="website" tabindex="-1" autocomplete="off" aria-hidden="true" placeholder="Website">
    <button class="btn submit" type="submit">Continue</button>
  </form>
</section>"""




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


def load_roster() -> dict:
    """Read-only. The service never writes ROSTER_PATH — deploy.sh installs
    it fresh from the git-tracked server/invite_roster.json on every push."""
    if not ROSTER_PATH.exists():
        return {}
    with ROSTER_PATH.open(encoding="utf-8") as f:
        raw = f.read().strip()
    return json.loads(raw) if raw else {}


def _with_status_lock(fn):
    """Run fn(status_dict) -> status_dict under an flock, then persist the
    returned dict. Simple advisory locking — traffic here is low enough
    that this is about correctness under rare concurrent hits, not
    throughput."""
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.touch(exist_ok=True)
    with STATUS_PATH.open("r+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            raw = f.read().strip()
            status = json.loads(raw) if raw else {}
            status = fn(status)
            f.seek(0)
            f.truncate()
            json.dump(status, f, indent=2, ensure_ascii=False)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    return status


def get_status(slug: str) -> dict:
    if not STATUS_PATH.exists():
        return {}
    with STATUS_PATH.open(encoding="utf-8") as f:
        raw = f.read().strip()
    all_status = json.loads(raw) if raw else {}
    return all_status.get(slug, {})


def update_status(slug: str, **fields) -> dict:
    def apply(status: dict) -> dict:
        record = status.get(slug, {})
        record.update(fields)
        status[slug] = record
        return status

    return _with_status_lock(apply)[slug]


def append_review_attempt(slug: str, **attempt_fields) -> None:
    """Record a flagged repeat/mismatched attempt without disturbing the
    slug's existing top-level status fields — used when a case-B slug
    (no known email, trust-on-first-use) is already locked to a
    successful grant and a DIFFERENT email shows up afterward. That's
    the possible-leaked-link scenario: the original grant stays on the
    record exactly as it was, and this attempt is appended for review."""
    def apply(status: dict) -> dict:
        record = status.get(slug, {})
        attempts = record.setdefault("review_attempts", [])
        attempts.append(attempt_fields)
        status[slug] = record
        return status

    _with_status_lock(apply)


def decide_invite_action(roster_record: dict, status_record: dict, submitted_email: str) -> str:
    """Returns "auto_whitelist", "idempotent_ok", or "manual_review"."""
    known_email = (roster_record.get("email") or "").strip().lower()
    submitted = submitted_email.strip().lower()
    used = bool(status_record.get("used"))
    locked_email = (status_record.get("locked_email") or "").strip().lower()

    if used and submitted == locked_email:
        # Already handled this exact email for this slug before, whether
        # matched-known (case A) or trust-on-first-use (case B) — a
        # friendly no-op instead of re-running grant/notification.
        return "idempotent_ok"

    if known_email:
        return "auto_whitelist" if submitted == known_email else "manual_review"

    # No known email on file (case B): first touch grants and locks;
    # anything after that which doesn't match the lock needs a human.
    return "auto_whitelist" if not used else "manual_review"


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

def render_invite_form(name: str, record: dict, message: str) -> str:
    name_esc = html.escape(name)
    content = _invite_form_content(
        group_url=html.escape(record.get("hypothesis_group_url", "")),
        group_code=html.escape(record.get("hypothesis_group_name", "your group")),
        email_value=html.escape(record.get("email") or ""),
    )
    return INVITE_PAGE_TEMPLATE.substitute(
        title=f"Welcome, {name} &mdash; Atomic Sanskrit",
        name=name_esc,
        group_code=html.escape(record.get("hypothesis_group_name", "your group")),
        message=message,
        content=content,
    )


def render_invite_result(name: str, record: dict, message: str) -> str:
    return INVITE_PAGE_TEMPLATE.substitute(
        title=f"Welcome, {name} &mdash; Atomic Sanskrit",
        name=html.escape(name),
        group_code=html.escape(record.get("hypothesis_group_name", "your group")),
        message=message,
        content="",
    )


def render_not_found() -> str:
    return page(
        "Not found",
        "Invite link not recognized",
        "<p>This invite link isn't recognized. Please double-check the URL, "
        "or use the <a href=\"/as/request-access\">general request-access form</a> instead.</p>",
    )


def handle_invite_get(slug: str) -> tuple[int, str]:
    roster = load_roster()
    record = roster.get(slug)
    if not record:
        return 404, render_not_found()
    name = record.get("name", slug)
    return 200, render_invite_form(
        name, record, "Thank you for taking the time — glad to have you reading along."
    )


def handle_invite_post(slug: str, fields: dict, ip: str) -> tuple[int, str]:
    roster = load_roster()
    record = roster.get(slug)
    if not record:
        return 404, render_not_found()
    name = record.get("name", slug)

    if fields.get("website"):  # honeypot
        return 200, render_invite_result(name, record, "Thanks — you're all set.")

    email = fields.get("email", "").strip()
    hyp_username = fields.get("hypothesis_username", "").strip()

    if not EMAIL_RE.match(email):
        return 400, render_invite_form(name, record, "Please enter a valid email address.")

    if _rate_limited(ip):
        return 429, render_invite_form(name, record, "Please wait a moment before submitting again.")

    status_record = get_status(slug)
    action = decide_invite_action(record, status_record, email)
    known_email = (record.get("email") or "").strip().lower()

    if action == "idempotent_ok":
        return 200, render_invite_result(
            name, record,
            "You already have access — no need to do anything else. "
            '<a href="/as/book/">Head to the book here</a>.',
        )

    if action == "auto_whitelist":
        update_status(
            slug,
            submitted_email=email,
            hypothesis_username=hyp_username,
            submitted_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            status="whitelisted",
            used=True,
            locked_email=email,
        )
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
            name, record,
            "Thank you for joining us — you're all set. "
            '<a href="/as/book/">Head to the book here</a>.',
        )

    # action == "manual_review" — two distinct scenarios needing different
    # handling: an unexpected email against a known-email slug (case A,
    # safe to overwrite the status fields since nothing was granted yet
    # for this slug), versus a different email showing up after a case-B
    # slug is already locked to a successful grant (must NOT clobber that
    # grant's record — append a flagged attempt instead).
    already_locked = (not known_email) and bool(status_record.get("used"))

    if already_locked:
        locked_email = status_record.get("locked_email") or "(none on file)"
        reason = (
            f"this invite link was already used to grant access to {locked_email}, "
            f"and a DIFFERENT email just used the same link — possible leaked invite"
        )
        expected_line = locked_email
        subject = f"Review needed: possible leaked invite link ({slug})"
        append_review_attempt(
            slug,
            submitted_email=email,
            hypothesis_username=hyp_username,
            submitted_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            ip=ip,
            reason=reason,
        )
    else:
        reason = f"different email than on file (expected {known_email or '(none on file)'})"
        expected_line = known_email or "(none on file)"
        subject = f"Review needed: {name} used a different email ({slug})"
        update_status(
            slug,
            submitted_email=email,
            hypothesis_username=hyp_username,
            submitted_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            status="pending_review",
        )

    try:
        log_request(name, email, f"INVITE '{slug}' — {reason}", ip)
    except Exception as exc:
        print(f"request_access: log_request failed: {exc}")
        return 500, render_invite_form(
            name, record,
            "Something went wrong on our end — please try again in a few minutes, "
            "or email rhinusgaleo@gmail.com directly.",
        )
    try:
        send_notification_email(
            subject,
            f"{name} (invite '{slug}') triggered manual review.\n\n"
            f"Reason: {reason}\n"
            f"Expected: {expected_line}\n"
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
        name, record,
        "Thanks — that's not the email we were expecting for this link, so "
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
