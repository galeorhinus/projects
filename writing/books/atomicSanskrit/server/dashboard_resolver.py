#!/usr/bin/env python3
"""dashboard_resolver.py -- serves /as/private/dashboard/* by resolving the
authenticated visitor to the right page: the owner's full triage dashboard,
one reader's scoped page, or a graceful "not in a reading group yet" page for
a whitelisted visitor with no roster entry. Loopback-only, reached only
through Caddy's reverse_proxy inside the same oauth2-proxy gate that already
protects /as/private/*.

Design decision (2026-08-19): ALL requests to /as/private/dashboard/* --
including the owner's own, previously served directly by Caddy's static
file_server -- are routed through this resolver, not just non-owner ones.
The alternative (branch in Caddy: static serve for the owner, proxy for
everyone else) needs either a nested `handle` or a second matcher for the
`?as=<slug>` preview case, and this Caddyfile's own comments record more than
one hard-won bug from subtle matcher semantics (the `not`-matcher inline-vs-
block issue; X-Forwarded-Email vs X-Auth-Request-Email). Doing the owner/
preview/reader branch here in testable Python, with one proven bare
`reverse_proxy` directive on the Caddy side, trades a small amount of
resilience -- if this service is down, the OWNER also loses dashboard
viewing, not just readers -- for a much lower risk of a silent Caddy
misconfiguration. dashboard_api.py already carries a similar single-service
dependency for the reply composer; this keeps the same risk posture rather
than introducing a new category of one.

Two lookups this service depends on, and why it (not build_dashboard.py) is
the one that reads them directly: /etc/secondshanti/invite_roster.json and
invite_status.json are both 640 www-data:www-data. This service runs as
www-data (see dashboard-resolver.service), so it reads them natively -- no
permission workaround needed, unlike build_dashboard.py's cron job (runs as
`ubuntu`, not in the www-data group; see that script's ROSTER_PATH comment
for the live bug this exact asymmetry caused).

Read-only. This service never writes anything -- see the systemd unit.
"""

from __future__ import annotations

import html as html_lib
import json
import re
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BIND_HOST = "127.0.0.1"
BIND_PORT = 8091

OWNER_EMAIL = "rhinusgaleo@gmail.com"

ROSTER_PATH = Path("/etc/secondshanti/invite_roster.json")
STATUS_PATH = Path("/etc/secondshanti/invite_status.json")

# Written by build_dashboard.py's --readers flag (runs as `ubuntu` via cron,
# every 15 minutes -- see hypothesis/refresh_dashboard.sh). This directory is
# NOT under the ubuntu home tree (which is 750 ubuntu:ubuntu and blocks
# www-data's traversal entirely) -- it is a one-time-provisioned directory
# owned ubuntu:www-data, mode 2750, so ubuntu (owner) can write and www-data
# (group, setgid-inherited on new files) can read. See server/README.md for
# the provisioning command.
READERS_DIR = Path("/var/lib/secondshanti/dashboard_readers")

# The owner's full dashboard, same file Caddy used to serve directly via
# file_server. /var/www/as is 775 ubuntu:ubuntu (deploy.sh's own comment:
# "owned by the ubuntu user") -- world-readable, so www-data can read it
# with no extra grant, confirmed live 2026-08-19.
OWNER_DASHBOARD_PATH = Path("/var/www/as/private/dashboard/index.html")

_VIEWER_JSON_RE = re.compile(r"const VIEWER = (\{.*?\});")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8").strip()
    return json.loads(raw) if raw else {}


def resolve_slug(email: str, roster: dict, status: dict) -> str | None:
    """Map an authenticated email to a roster slug.

    Lookup order (plan decision 2026-08-19): for EACH slug, locked_email
    from invite_status.json if that slug has one -- it's the address the
    reader actually authenticated with, and therefore what oauth2-proxy
    puts in X-Forwarded-Email -- otherwise the roster's own `email` field,
    for a slug whose invite hasn't been used yet.

    This must be a per-slug choice, not two global passes (locked_email
    matched anywhere, then roster email matched anywhere): a first version
    of this function did exactly that and let a stale, no-longer-live
    roster `email` value still match once a slug had ALREADY locked to a
    different real address (caught by a test 2026-08-19, before deploy --
    ap's roster email pointed to an address nobody was using, ap's real
    Google account had already locked in as a different one, and the
    two-pass version happily resolved a request from the STALE address to
    ap's slug anyway). Once a slug is locked, its locked_email is the only
    valid key for it; the roster email stops being a live alternative.
    """
    email = email.strip().lower()
    for slug, rec in roster.items():
        locked = (status.get(slug, {}).get("locked_email") or "").strip().lower()
        key = locked or (rec.get("email") or "").strip().lower()
        if key and key == email:
            return slug
    return None


def reader_self(slug: str, roster: dict, status: dict) -> str | None:
    """Best Hypothesis username on file for `slug`, for own-note marking.

    Prefers the roster's hypothesis_username, which -- where present -- was
    recorded from OBSERVED annotation data (matches the real posted `user`
    field exactly). Falls back to invite_status.json's copy, which is
    self-reported at signup and may not match the account's actual posting
    username (typos, capitalization). Returns None if neither is on file,
    which leaves the page's __VIEWER_SELF__ token substituted with nothing
    changed -- own-note marking simply doesn't activate, a safe degrade
    already built into the page's own client-side check.
    """
    rec = roster.get(slug, {})
    if rec.get("hypothesis_username"):
        return rec["hypothesis_username"]
    return status.get(slug, {}).get("hypothesis_username") or None


def inject_preview_flag(content: str) -> str:
    """Set VIEWER.preview = true in the baked page without touching
    anything else. The page's own client JS already renders a "Previewing
    as <name>" banner keyed on this flag while IS_OWNER stays false (VIEWER.
    mode is still "reader") -- so a preview shows exactly the reader's own
    UI, not the owner's composer/TODO chrome, with only the banner added."""
    m = _VIEWER_JSON_RE.search(content)
    if not m:
        return content  # unexpected page shape; serve as-is rather than 500
    viewer = json.loads(m.group(1))
    viewer["preview"] = True
    replacement = "const VIEWER = " + json.dumps(viewer, ensure_ascii=False) + ";"
    return content[:m.start()] + replacement + content[m.end():]


def render_reader_page(slug: str, roster: dict, status: dict, *, preview: bool) -> str | None:
    path = READERS_DIR / f"{slug}.html"
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8")
    self_name = reader_self(slug, roster, status)
    if self_name:
        # Safe as an unscoped substring replace: the literal unsplit string
        # "__VIEWER_SELF__" appears in the baked page ONLY inside the
        # VIEWER JSON's "self" value. The client-side comparison against
        # this same token is deliberately written as "__VIEWER_" + "SELF__"
        # in build_dashboard.py's template specifically so a server-side
        # replace here can never also corrupt that JS.
        content = content.replace("__VIEWER_SELF__", self_name)
    if preview:
        content = inject_preview_flag(content)
    return content


PAGE_STYLE = """
<style>
  :root { --bg:#eef0f2; --surface:#fff; --text:#1e2530; --muted:#5b6472; --border:#d7dce1; --accent:#3d4f7a; }
  * { box-sizing: border-box; }
  body { margin:0; padding:3rem 1.5rem; background:var(--bg); color:var(--text);
         font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
  .card { max-width: 34rem; margin: 4rem auto 0; background: var(--surface); border: 1px solid var(--border);
          border-radius: 12px; padding: 2rem 2.25rem; }
  h1 { font-size: 1.35rem; margin: 0 0 0.75rem; }
  p { color: var(--muted); margin: 0.5rem 0; }
  a { color: var(--accent); }
</style>
"""


def render_no_group_page(name: str | None, *, preview: bool = False) -> str:
    who = html_lib.escape(name) if name else "You"
    banner = (
        f'<p style="color:#8a6a10">Previewing as {who} — this reader has no built page yet '
        "(no reading group on file, or no annotations collected so far).</p>"
        if preview else ""
    )
    greeting = f"Hi {who}," if name else "Hi,"
    return f"""<!doctype html>
<title>Reader Margins</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
{PAGE_STYLE}
<div class="card">
  <h1>Not in a reading group yet</h1>
  {banner}
  <p>{greeting} you're on the access list, but you haven't been placed in a
  reading group's dashboard yet.</p>
  <p>Once you're added, this page will show your annotations and the
  replies to them. Reach out if you think this is a mistake.</p>
</div>"""


def render_error_page(message: str) -> str:
    return f"""<!doctype html>
<title>Reader Margins</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
{PAGE_STYLE}
<div class="card">
  <h1>Something went wrong</h1>
  <p>{html_lib.escape(message)}</p>
</div>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "DashboardResolver/1.0"

    def log_message(self, fmt, *args):
        pass  # Caddy's own access log already records this upstream.

    def do_GET(self):
        email = (self.headers.get("X-Forwarded-Email") or "").strip().lower()
        if not email:
            # Shouldn't happen behind oauth2-proxy -- defensive only.
            self._send_html(400, render_error_page("Missing authentication."))
            return

        roster = load_json(ROSTER_PATH)
        status = load_json(STATUS_PATH)

        parsed = urllib.parse.urlsplit(self.path)
        preview_slug = (urllib.parse.parse_qs(parsed.query).get("as", [""])[0] or "").strip()

        if email == OWNER_EMAIL:
            self._serve_owner(preview_slug, roster, status)
            return

        # Non-owner: `?as=` is ignored entirely, per the plan -- only the
        # owner may preview another reader's page.
        slug = resolve_slug(email, roster, status)
        if not slug:
            self._send_html(200, render_no_group_page(None))
            return
        content = render_reader_page(slug, roster, status, preview=False)
        if content is None:
            name = roster.get(slug, {}).get("name", slug)
            self._send_html(200, render_no_group_page(name))
            return
        self._send_html(200, content)

    def _serve_owner(self, preview_slug: str, roster: dict, status: dict) -> None:
        if preview_slug:
            if preview_slug not in roster:
                self._send_html(404, render_error_page(f"No reader '{preview_slug}' on the roster."))
                return
            content = render_reader_page(preview_slug, roster, status, preview=True)
            if content is None:
                name = roster.get(preview_slug, {}).get("name", preview_slug)
                self._send_html(200, render_no_group_page(name, preview=True))
                return
            self._send_html(200, content)
            return
        # No preview requested -- the owner's own full dashboard, byte-for-
        # byte the same file Caddy used to serve directly.
        if not OWNER_DASHBOARD_PATH.exists():
            self._send_html(503, render_error_page("Dashboard not built yet."))
            return
        self._send_html(200, OWNER_DASHBOARD_PATH.read_text(encoding="utf-8"))

    def _send_html(self, status_code: int, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        # Rebuilt on a 15-minute cycle; never let a browser or intermediary
        # cache a stale reader's page against a shared URL.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    server = ThreadingHTTPServer((BIND_HOST, BIND_PORT), Handler)
    print(f"dashboard_resolver listening on {BIND_HOST}:{BIND_PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
