#!/usr/bin/env python3
"""dashboard_api.py -- backend for Reader Margins' per-card reply
composer (build_dashboard.py). Loopback-only, reached only via Caddy's
reverse_proxy at /as/private/dashboard/api/*, which sits behind the
SAME owner-only gate as the dashboard itself (Google OAuth via
oauth2-proxy + the @dashboard_notowner check in the Caddyfile) -- this
service ALSO independently checks X-Forwarded-Email itself as
defense-in-depth: unlike the read-only dashboard, this one can WRITE to
Hypothesis, so it doesn't rely solely on the reverse-proxy chain.

Two POST routes (Caddy's handle_path strips /as/private/dashboard/api,
so these are the paths left to route on):

  POST /            {"id", "text", "tag": "resolved"|"acknowledged"
                     |"awaiting-reader", "force"} -- reply composer.
  POST /refresh      pull + rebuild (see refresh_dashboard_fast.sh).
  POST /todo         {"id", "note", "remove": bool} -- private TODO
                     queue, see below.

Reply composer: three tags, three different behaviors:

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

TODO queue: deliberately NOT a Hypothesis reply -- a personal task note
("check this reference, expand Ch3") has no business being visible to
readers in a shared annotation thread the way the composer's replies
are. Appended instead to data/todo_queue.json, a plain local file that
never leaves amrut on its own (amrut only ever `git pull`s in this
project, never pushes) -- reconciled into working/10_active/as_todo.md
by Claude at the start of the next session working on the manuscript,
who then clears the queue. Independent of the reply composer: queueing
a TODO note doesn't touch resolved/acknowledged/awaiting-reader status,
and both can be used on the same annotation.

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
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HYPOTHESIS_DIR = Path(__file__).parent
sys.path.insert(0, str(HYPOTHESIS_DIR))
from hypothesis_client import HypothesisClient, HypothesisError  # noqa: E402
from pull_annotations import (  # noqa: E402
    normalize as normalize_annotation,
    clean_user,
    ANNOTATIONS_PATH,
    GROUPS_PATH,
)

BIND_HOST = "127.0.0.1"
BIND_PORT = 8092
OWNER_EMAIL = "rhinusgaleo@gmail.com"
DASHBOARD_INSTALL_PATH = "/var/www/as/private/dashboard/index.html"
READERS_INSTALL_DIR = "/var/lib/secondshanti/dashboard_readers"
TODO_QUEUE_PATH = HYPOTHESIS_DIR / "data" / "todo_queue.json"

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


def rebuild_dashboard_file() -> None:
    """Just the rebuild half -- shared by refresh_dashboard_after_reply
    (which also appends the new reply first) and the TODO queue handler
    (which needs the freshly-rebuilt page to show the queued badge, but
    has no annotation record of its own to append -- the queued item is
    still a normal reader annotation already in the local snapshot,
    only its queued-for-TODO status changed)."""
    subprocess.run(
        [sys.executable, str(HYPOTHESIS_DIR / "build_dashboard.py"),
         "--install", DASHBOARD_INSTALL_PATH,
         "--readers", READERS_INSTALL_DIR],
        cwd=str(HYPOTHESIS_DIR), check=True, capture_output=True, timeout=30, text=True,
    )


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

    rebuild_dashboard_file()


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


def chapter_slug(uri: str) -> str:
    return uri.rstrip("/").rsplit("/", 1)[-1]


def annotation_quote(annotation: dict) -> str:
    for target in annotation.get("target", []):
        for selector in target.get("selector", []):
            if selector.get("type") == "TextQuoteSelector":
                return selector.get("exact", "")
    return ""


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
        if self.path.rstrip("/") == "/todo":
            self._handle_todo()
            return
        self._handle_reply_post()

    def _handle_refresh(self) -> None:
        """Pull + rebuild on demand, for the dashboard's own "Refresh
        now" button -- the background cadence (refresh_dashboard.sh,
        every 15 minutes via cron) already keeps the page reasonably
        current, but this exists for "check right now" instead of
        waiting up to 15 minutes.

        Deliberately the FAST script (pull + rebuild only, no tagging)
        -- confirmed live 2026-08-16: auto_tagger.py's per-annotation
        LLM calls could push a full refresh past a minute when there
        was a tagging backlog, which made the button feel erratic, and
        a long fetch() is fragile on top of that (a backgrounded tab
        can kill it silently, no error shown, no reload -- "no
        callback"). Tagging still happens on its own 15-minute cycle
        regardless of this button; new comments just show up here
        untagged until that next cycle catches up."""
        try:
            subprocess.run(
                [str(HYPOTHESIS_DIR / "refresh_dashboard_fast.sh")],
                cwd=str(HYPOTHESIS_DIR), check=True, capture_output=True, timeout=45, text=True,
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

    def _handle_todo(self) -> None:
        """Queue (or un-queue) a private TODO note for one annotation.
        See the module docstring for why this is a local file, not a
        Hypothesis reply. {"id", "note", "remove": bool}."""
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "bad request body"})
            return

        annotation_id = (payload.get("id") or "").strip()
        note = (payload.get("note") or "").strip()
        remove = bool(payload.get("remove"))

        if not annotation_id:
            self._send_json(400, {"error": "missing id"})
            return
        if not remove and not note:
            self._send_json(400, {"error": "note required to queue (or pass remove: true)"})
            return

        queue = json.loads(TODO_QUEUE_PATH.read_text()) if TODO_QUEUE_PATH.exists() else []
        queue = [e for e in queue if e["id"] != annotation_id]  # idempotent either way

        if not remove:
            try:
                client = HypothesisClient()
                annotation = client.get_annotation(annotation_id)
            except (HypothesisError, urllib.error.URLError, urllib.error.HTTPError) as e:
                self._send_json(502, {"error": str(e)})
                return
            queue.append({
                "id": annotation_id,
                "queued_at": datetime.now(timezone.utc).isoformat(),
                "user": clean_user(annotation.get("user", "")),
                "chapter": chapter_slug(annotation.get("uri", "")),
                "document_title": (annotation.get("document", {}).get("title") or [""])[0],
                "uri": annotation.get("uri", ""),
                "quote": annotation_quote(annotation),
                "reader_comment": annotation.get("text", ""),
                "note": note,
            })

        TODO_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
        TODO_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

        # Same reasoning as refresh_dashboard_after_reply(): rebuild now
        # so the queued/un-queued badge survives a page refresh instead
        # of only updating this tab's in-memory view.
        try:
            rebuild_dashboard_file()
        except subprocess.CalledProcessError as e:
            print(f"dashboard rebuild after todo change failed: {e}\n"
                  f"stdout: {e.stdout}\nstderr: {e.stderr}", file=sys.stderr)
        except (subprocess.TimeoutExpired, OSError) as e:
            print(f"dashboard rebuild after todo change failed: {e}", file=sys.stderr)

        self._send_json(200, {"status": "removed" if remove else "queued"})

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
        # A forced post with empty text is almost certainly the client
        # having lost the author's words rather than a deliberate canned
        # send: force=true is only reachable from the "still live" retry,
        # which the author only sees after composing something. Refusing
        # it here is the backstop for the 2026-08-20 data-loss bug, where
        # the client destroyed its own textarea on that warning and the
        # canned message was silently posted in place of what the author
        # had written. An intentional canned "resolved" needs no force,
        # so this costs nothing real. Checked with the other input
        # validation, before any network call, so it fails fast.
        if force and not text:
            self._send_json(400, {
                "error": "Refusing to force-post an empty reply -- the canned "
                         "message would replace your own words. Retype the "
                         "note and post again."
            })
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
