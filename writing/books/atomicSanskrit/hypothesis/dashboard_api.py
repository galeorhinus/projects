#!/usr/bin/env python3
"""dashboard_api.py -- tiny backend for the "Mark resolved" button in
Reader Margins (build_dashboard.py). Loopback-only, reached only via
Caddy's reverse_proxy at /as/private/dashboard/api/*, which sits behind
the SAME owner-only gate as the dashboard itself (Google OAuth via
oauth2-proxy + the @dashboard_notowner check in the Caddyfile) -- this
service ALSO independently checks X-Forwarded-Email itself as
defense-in-depth: unlike the read-only dashboard, this one can WRITE to
Hypothesis, so it doesn't rely solely on the reverse-proxy chain.

One endpoint: POST / with {"id": <annotation id>, "force": bool}.

Verifies against the LIVE deployed chapter page, not local files or
git state -- the whole point is to catch "I fixed it locally but
haven't pushed/deployed yet" before silently posting a reply that
nothing live actually backs up:

  - flagged passage gone from the live page  -> post the reply, tag
    "resolved", return {"status": "resolved"}
  - flagged passage still live, force=false  -> return
    {"status": "still_live"} without posting anything -- the UI shows
    a warning and offers to retry with force=true
  - flagged passage still live, force=true   -> post anyway (the user
    explicitly overrode the warning, e.g. they're confident and about
    to deploy)

Pure standard library, same convention as the rest of this directory.
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hypothesis_client import HypothesisClient, HypothesisError  # noqa: E402

BIND_HOST = "127.0.0.1"
BIND_PORT = 8092
OWNER_EMAIL = "rhinusgaleo@gmail.com"
REPLY_TAG = "resolved"
REPLY_TEXT = (
    "Looks like this has been addressed in a later revision -- confirmed "
    "against the live site, not just local edits. Reply if it's still an issue."
)

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


def anchor_still_live(client: HypothesisClient, annotation_id: str) -> tuple[bool, dict]:
    annotation = client.get_annotation(annotation_id)
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
        return False, annotation

    live_text = fetch_live_text(annotation["uri"])
    return anchor in live_text, annotation


class Handler(BaseHTTPRequestHandler):
    server_version = "DashboardAPI/1.0"

    def log_message(self, fmt, *args):
        pass  # Caddy's own access log already records this upstream.

    def do_POST(self):
        owner_header = self.headers.get("X-Forwarded-Email", "")
        if owner_header.strip().lower() != OWNER_EMAIL:
            self._send_json(403, {"error": "forbidden"})
            return

        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "bad request body"})
            return

        annotation_id = (payload.get("id") or "").strip()
        force = bool(payload.get("force"))
        if not annotation_id:
            self._send_json(400, {"error": "missing id"})
            return

        try:
            client = HypothesisClient()
            still_live, annotation = anchor_still_live(client, annotation_id)
        except (HypothesisError, urllib.error.URLError, urllib.error.HTTPError) as e:
            self._send_json(502, {"error": str(e)})
            return

        if still_live and not force:
            self._send_json(200, {"status": "still_live"})
            return

        try:
            client.create_reply(annotation, REPLY_TEXT, tags=[REPLY_TAG])
        except HypothesisError as e:
            self._send_json(502, {"error": str(e)})
            return

        self._send_json(200, {"status": "resolved"})

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
