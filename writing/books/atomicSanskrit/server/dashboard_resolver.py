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
import time
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

# Reader-triggered "Update now". This service runs as www-data and cannot
# run the refresh itself: hypothesis/token.txt is 600 ubuntu, and the
# scripts write files owned by ubuntu. Rather than widening access to the
# owner's API token, www-data only TOUCHES a trigger file it already has
# write access to, and a root-owned systemd .path unit runs the actual
# refresh as ubuntu -- exactly the pattern already used for the
# oauth2-proxy whitelist reload (see server/README.md and
# oauth2-proxy-whitelist-reload.path). No privilege escalation anywhere,
# and the token stays readable only by ubuntu.
REFRESH_TRIGGER = Path("/var/lib/secondshanti/refresh-dashboard-request")

# Per-slug cooldown. The refresh is the FAST script (pull + rebuild, no
# LLM tagging) and takes up to ~45s, so anything shorter than this just
# queues work behind work. Held in memory: this is a long-lived service,
# and a cooldown that resets on restart is a non-problem.
REFRESH_COOLDOWN_S = 90
_last_refresh: dict[str, float] = {}

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

    def _page_built_ms(self, email: str, roster: dict, status: dict) -> int:
        """Mtime of the file this viewer is actually served, in ms. The
        client polls this after triggering a refresh and reloads once it
        advances past the BUILT_AT it loaded with."""
        if email == OWNER_EMAIL:
            path = OWNER_DASHBOARD_PATH
        else:
            slug = resolve_slug(email, roster, status)
            path = READERS_DIR / f"{slug}.html" if slug else None
        try:
            return int(path.stat().st_mtime * 1000) if path else 0
        except OSError:
            return 0

    def do_POST(self):
        """Reader-triggered refresh. The only POST this service accepts."""
        email = (self.headers.get("X-Forwarded-Email") or "").strip().lower()
        parsed = urllib.parse.urlsplit(self.path)
        if parsed.path.rstrip("/") != "/as/private/dashboard/refresh":
            self._send_json(404, {"error": "not found"})
            return
        if not email:
            self._send_json(400, {"error": "missing authentication"})
            return

        roster = load_json(ROSTER_PATH)
        status = load_json(STATUS_PATH)
        # Identity comes from the OAuth header, never from the request
        # body -- a reader cannot ask to refresh on anyone else's behalf,
        # and the refresh itself is global anyway (one shared pipeline),
        # so the slug here is only used for rate-limiting fairness.
        key = email if email == OWNER_EMAIL else (resolve_slug(email, roster, status) or email)

        now = time.time()
        last = _last_refresh.get(key, 0.0)
        remaining = REFRESH_COOLDOWN_S - (now - last)
        if remaining > 0:
            self._send_json(429, {"error": "too soon", "retry_in": int(remaining) + 1})
            return
        try:
            REFRESH_TRIGGER.parent.mkdir(parents=True, exist_ok=True)
            REFRESH_TRIGGER.touch()
        except OSError as e:
            # Cooldown is recorded only AFTER a successful trigger. Setting
            # it first meant a failed request still burned the reader's
            # 90 seconds, so a transient error locked them out of retrying.
            self._send_json(500, {"error": f"could not request refresh: {e}"})
            return
        _last_refresh[key] = now
        self._send_json(202, {"status": "requested",
                              "built": self._page_built_ms(email, roster, status)})

    def do_GET(self):
        email = (self.headers.get("X-Forwarded-Email") or "").strip().lower()
        if not email:
            # Shouldn't happen behind oauth2-proxy -- defensive only.
            self._send_html(400, render_error_page("Missing authentication."))
            return

        roster = load_json(ROSTER_PATH)
        status = load_json(STATUS_PATH)

        parsed = urllib.parse.urlsplit(self.path)

        # Polled by the client after a refresh request, to learn when the
        # rebuild has actually landed. Cheap: one stat() per call.
        if parsed.path.rstrip("/") == "/as/private/dashboard/refresh-status":
            self._send_json(200, {"built": self._page_built_ms(email, roster, status)})
            return

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



    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
def main() -> None:
    server = ThreadingHTTPServer((BIND_HOST, BIND_PORT), Handler)
    print(f"dashboard_resolver listening on {BIND_HOST}:{BIND_PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
