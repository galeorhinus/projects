#!/usr/bin/env python3
"""dashboard_api.py -- backend for Reader Margins' per-card reply
composer (build_dashboard.py). Loopback-only, reached only via Caddy's
reverse_proxy at /as/private/dashboard/api/*, which sits behind the
SAME owner-only gate as the dashboard itself (Google OAuth via
oauth2-proxy + the @dashboard_notowner check in the Caddyfile) -- this
service ALSO independently checks X-Forwarded-Email itself as
defense-in-depth: unlike the read-only dashboard, this one can WRITE to
Hypothesis, so it doesn't rely solely on the reverse-proxy chain.

One endpoint: POST / with
    {"id": <annotation id>, "text": <optional string>,
     "tag": "resolved" | "acknowledged" | "awaiting-reader",
     "force": bool}

Three tags, three different behaviors:

  resolved         -- verified against the LIVE deployed chapter page
                       first (not local files or git state -- the whole
                       point is to catch "I fixed it locally but
                       haven't pushed/deployed yet"). Still live and
                       force=false -> {"status": "still_live"}, nothing
                       posted, UI offers a "post anyway" override.
                       Empty text falls back to a canned "addressed in
                       a later revision" message.
  acknowledged      -- no live-check (there's nothing to verify -- a
                       "thanks!" or "noted" doesn't correspond to any
                       text change). Empty text falls back to a canned
                       thank-you.
  awaiting-reader   -- no live-check (not claiming resolution). Text is
                       REQUIRED -- a generic canned message would defeat
                       the point of a tag that exists specifically for
                       "I asked a follow-up, waiting on them."

All three post a reply (POST with references: [parent_id], same
mechanism regardless of who authored the parent -- replying only needs
create permission in the group, not write permission on the parent).

Pure standard library, same convention as the rest of this directory.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HYPOTHESIS_DIR = Path(__file__).parent
sys.path.insert(0, str(HYPOTHESIS_DIR))
from hypothesis_client import HypothesisClient, HypothesisError  # noqa: E402
from pull_annotations import normalize as normalize_annotation, ANNOTATIONS_PATH, GROUPS_PATH  # noqa: E402

BIND_HOST = "127.0.0.1"
BIND_PORT = 8092
OWNER_EMAIL = "rhinusgaleo@gmail.com"
DASHBOARD_INSTALL_PATH = "/var/www/as/private/dashboard/index.html"

VALID_TAGS = {"resolved", "acknowledged", "awaiting-reader"}
CANNED_TEXT = {
    "resolved": (
        "Looks like this has been addressed in a later revision -- confirmed "
        "against the live site, not just local edits. Reply if it's still an issue."
    ),
    "acknowledged": "Thank you for flagging this!",
    # awaiting-reader has NO canned fallback -- text is required for it,
    # enforced below, precisely so this tag can't be used as a content-
    # free "seen it" click the way acknowledged can.
}

_TAG_BLOCK_RE = re.compile(r"<(script|style)\b.*?</\1>", re.I | re.S)
_ANY_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_SMART_QUOTES = str.maketrans({
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...",
})


def strip_html(raw: str) -> str:
    text = _TAG_BLOCK_RE.sub(" ", raw)
    text = _ANY_TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = text.translate(_SMART_QUOTES)
    return _WS_RE.sub(" ", text).strip()


def normalize_anchor(text: str) -> str:
    return _WS_RE.sub(" ", text).translate(_SMART_QUOTES).strip()


def fetch_live_text(uri: str) -> str:
    """Fetch the deployed page's rendered text -- NOT via the public
    https://secondshanti.org URL. /as/book/* is gated by Google OAuth
    (302s to a login page for any unauthenticated request, this
    service included), so a plain fetch of the public URL would only
    ever see the login redirect and never the real content -- which
    would make the "still live?" check always report false and defeat
    the entire point of it silently. This service runs ON amrut, so it
    hits the same internal loopback origin (127.0.0.1:18080) that
    oauth2-proxy itself proxies AUTHENTICATED requests to -- no auth
    needed, since that listener only binds to localhost and trusts
    everything upstream of it (Caddy's public block) to have already
    gated access. Caught live 2026-08-16 before this ever shipped."""
    path = urllib.parse.urlsplit(uri).path
    internal_url = f"http://127.0.0.1:18080{path}"
    req = urllib.request.Request(
        internal_url,
        headers={"User-Agent": "dashboard_api/1.0", "Host": "secondshanti.org"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return strip_html(raw)


def refresh_dashboard_after_reply(reply: dict) -> None:
    """Append the just-posted reply to the local snapshot and rebuild
    dashboard.html in place, so the live page reflects this action on
    the very next load instead of waiting for the next scheduled
    pipeline run (twice daily via cron). Caught live 2026-08-16: the
    composer's optimistic client-side update made a resolve look
    instant, but the reply was never written back into the static
    snapshot -- a page refresh silently reverted to the pre-resolve
    count, even though the reply itself was already saved for real on
    Hypothesis (the write never failed; only the page's own view of it
    was stale). Local file operations only, no network re-pull, so
    this stays fast enough to run synchronously in the request."""
    groups = json.loads(GROUPS_PATH.read_text()) if GROUPS_PATH.exists() else {}
    group_name = groups.get(reply.get("group"), reply.get("group", ""))
    record = normalize_annotation(reply, group_name)

    data = json.loads(ANNOTATIONS_PATH.read_text()) if ANNOTATIONS_PATH.exists() else []
    data = [a for a in data if a.get("id") != record["id"]]  # idempotent on retry
    data.append(record)
    data.sort(key=lambda a: a["created"])
    ANNOTATIONS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    subprocess.run(
        [sys.executable, str(HYPOTHESIS_DIR / "build_dashboard.py"),
         "--install", DASHBOARD_INSTALL_PATH],
        cwd=str(HYPOTHESIS_DIR), check=True, capture_output=True, timeout=30, text=True,
    )


def is_anchor_still_live(annotation: dict) -> bool:
    prefix = quote = suffix = ""
    for target in annotation.get("target", []):
        for selector in target.get("selector", []):
            if selector.get("type") == "TextQuoteSelector":
                prefix = selector.get("prefix", "")
                quote = selector.get("exact", "")
                suffix = selector.get("suffix", "")

    anchor = normalize_anchor(prefix + quote + suffix)
    if not anchor:
        # Note-only annotation, nothing to check against -- don't block
        # on a check that can't mean anything for this annotation.
        return False

    live_text = fetch_live_text(annotation["uri"])
    return anchor in live_text


class Handler(BaseHTTPRequestHandler):
    server_version = "DashboardAPI/1.0"

    def log_message(self, fmt, *args):
        pass  # Caddy's own access log already records this upstream.

    def do_POST(self):
        owner_header = self.headers.get("X-Forwarded-Email", "")
        if owner_header.strip().lower() != OWNER_EMAIL:
            self._send_json(403, {"error": "forbidden"})
            return

        # handle_path in the Caddyfile strips the /as/private/dashboard/api
        # prefix before proxying here, so "/refresh" (from the Refresh
        # button) and "/" (the reply composer, the original single
        # route) are what's left to route on.
        if self.path.rstrip("/") == "/refresh":
            self._handle_refresh()
            return
        self._handle_reply_post()

    def _handle_refresh(self) -> None:
        """Full pull + tag + rebuild on demand, for the dashboard's own
        "Refresh now" button -- the background cadence
        (refresh_dashboard.sh, every 15 minutes via cron) already keeps
        the page reasonably current, but this exists for "check right
        now" instead of waiting up to 15 minutes."""
        try:
            subprocess.run(
                [str(HYPOTHESIS_DIR / "refresh_dashboard.sh")],
                cwd=str(HYPOTHESIS_DIR), check=True, capture_output=True, timeout=90, text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"manual refresh failed: {e}\nstdout: {e.stdout}\nstderr: {e.stderr}", file=sys.stderr)
            self._send_json(502, {"error": "refresh failed -- see server logs"})
            return
        except (subprocess.TimeoutExpired, OSError) as e:
            print(f"manual refresh failed: {e}", file=sys.stderr)
            self._send_json(502, {"error": str(e)})
            return
        self._send_json(200, {"status": "refreshed"})

    def _handle_reply_post(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "bad request body"})
            return

        annotation_id = (payload.get("id") or "").strip()
        tag = (payload.get("tag") or "resolved").strip()
        text = (payload.get("text") or "").strip()
        force = bool(payload.get("force"))

        if not annotation_id:
            self._send_json(400, {"error": "missing id"})
            return
        if tag not in VALID_TAGS:
            self._send_json(400, {"error": f"invalid tag: {tag}"})
            return
        if tag == "awaiting-reader" and not text:
            self._send_json(400, {"error": "text required for awaiting-reader"})
            return

        try:
            client = HypothesisClient()
            annotation = client.get_annotation(annotation_id)
        except (HypothesisError, urllib.error.URLError, urllib.error.HTTPError) as e:
            self._send_json(502, {"error": str(e)})
            return

        if tag == "resolved" and not force:
            try:
                still_live = is_anchor_still_live(annotation)
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                self._send_json(502, {"error": f"live-check failed: {e}"})
                return
            if still_live:
                self._send_json(200, {"status": "still_live"})
                return

        reply_text = text or CANNED_TEXT.get(tag, "")
        try:
            reply = client.create_reply(annotation, reply_text, tags=[tag])
        except HypothesisError as e:
            self._send_json(502, {"error": str(e)})
            return

        # The Hypothesis write already succeeded at this point -- that's
        # the guarantee that actually matters. A rebuild hiccup here
        # (e.g. build_dashboard.py throwing, or /var/www being briefly
        # unwritable) shouldn't be reported as the reply itself having
        # failed; it just means this page load stays stale until the
        # next successful rebuild (this one's retry, or the next cron
        # run) instead of updating immediately. Logged, not raised.
        try:
            refresh_dashboard_after_reply(reply)
        except subprocess.CalledProcessError as e:
            # stderr/stdout, not just the exception message -- the
            # message alone ("exit status 1") gave no way to diagnose
            # the actual cause without reproducing it by hand. Found
            # live: a ProtectSystem=strict sandbox gap silently blocked
            # every write this rebuild makes; this print would have
            # shown that directly instead of needing a manual run.
            print(f"dashboard rebuild after reply failed: {e}\n"
                  f"stdout: {e.stdout}\nstderr: {e.stderr}", file=sys.stderr)
        except (subprocess.TimeoutExpired, OSError) as e:
            print(f"dashboard rebuild after reply failed: {e}", file=sys.stderr)

        self._send_json(200, {"status": "posted", "tag": tag})

    def _send_json(self, status: int, body: dict) -> None:
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    server = ThreadingHTTPServer((BIND_HOST, BIND_PORT), Handler)
    print(f"dashboard_api listening on {BIND_HOST}:{BIND_PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
