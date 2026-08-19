"""hypothesis_client.py -- minimal client for the Hypothes.is REST API.

Pure standard library, same convention as server/request_access.py --
no pip install needed to run any of the scripts in this directory.

API reference: https://h.readthedocs.io/en/latest/api-reference/
Auth: a personal API token from https://hypothes.is/account/developer,
sent as `Authorization: Bearer <token>`. Read from hypothesis/token.txt
(gitignored -- see README.md for how to create it), never from argv or
an env var that could end up in shell history.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://hypothes.is/api"
TOKEN_PATH = Path(__file__).parent / "token.txt"

# The API's own offset-based paging caps at 9,800 results (see
# https://web.hypothes.is/blog/new-search-api-parameter-search_after/);
# search_after is the documented way past that ceiling. 200 is the
# maximum page size the API accepts.
PAGE_SIZE = 200


class HypothesisError(RuntimeError):
    pass


def load_token() -> str:
    if not TOKEN_PATH.exists():
        raise HypothesisError(
            f"No token at {TOKEN_PATH}. Create it: paste your personal API "
            f"token (from https://hypothes.is/account/developer) into that "
            f"file as the only line, with no trailing newline issues -- "
            f"see hypothesis/README.md."
        )
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    if not token:
        raise HypothesisError(f"{TOKEN_PATH} is empty.")
    return token


class HypothesisClient:
    def __init__(self, token: str | None = None):
        self.token = token or load_token()

    def _request(self, method: str, path: str, *, params: dict | None = None,
                 body: dict | None = None) -> dict:
        url = f"{API_BASE}{path}"
        if params:
            # urlencode with doseq=True so a list value (e.g. multiple
            # `group` filters, if ever needed) becomes repeated query keys
            # rather than one comma-joined string the API won't parse.
            url += "?" + urllib.parse.urlencode(params, doseq=True)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise HypothesisError(
                f"{method} {path} -> HTTP {e.code}: {detail[:500]}"
            ) from e

    def profile_groups(self) -> list[dict]:
        """Every group the token's user belongs to -- the set to fan
        annotation search out across, since /search takes one group at a
        time and there's no 'all my groups' shortcut."""
        return self._request("GET", "/profile/groups")

    def profile(self) -> dict:
        """The token's own account info, notably 'userid' (e.g.
        'acct:rhinusgaleo@hypothes.is'). Used to tell which pulled
        annotations this token can actually PATCH: Hypothesis's write
        permission on an annotation belongs to its author only -- group
        membership grants read access to everyone's annotations but never
        write access to anyone else's. There is no moderation-API or
        paid-tier escape hatch; a group moderator can hide/unhide a
        flagged annotation and nothing else (confirmed against
        https://web.hypothes.is/help/moderation-for-groups/ 2026-08-15)."""
        return self._request("GET", "/profile")

    def search_all(self, group_id: str) -> list[dict]:
        """Every annotation in one group, paging past the 200-per-request
        limit via search_after (cursor = the sort key's value on the last
        row of the previous page, not an offset -- see module docstring)."""
        results: list[dict] = []
        search_after = None
        while True:
            params = {
                "group": group_id,
                "limit": PAGE_SIZE,
                "sort": "created",
                "order": "asc",
            }
            if search_after:
                params["search_after"] = search_after
            page = self._request("GET", "/search", params=params)
            rows = page.get("rows", [])
            if not rows:
                break
            results.extend(rows)
            if len(rows) < PAGE_SIZE:
                break
            search_after = rows[-1]["created"]
            time.sleep(0.2)  # a light courtesy delay between pages, not a rate-limit workaround
        return results

    def get_annotation(self, annotation_id: str) -> dict:
        """Fetch one annotation fresh from the API -- used where staleness
        matters (e.g. dashboard_api.py's live-resolve check), rather than
        trusting a locally cached pull that might be hours old."""
        return self._request("GET", f"/annotations/{annotation_id}")

    def update_tags(self, annotation_id: str, tags: list[str]) -> dict:
        """PATCH an annotation's tag list (replaces it wholesale -- callers
        that want to add rather than overwrite must merge first)."""
        return self._request(
            "PATCH", f"/annotations/{annotation_id}", body={"tags": tags}
        )

    def create_reply(self, parent: dict, text: str, tags: list[str] | None = None) -> dict:
        """POST a reply to `parent` (any annotation in a group this token
        belongs to -- replying only requires create permission in the
        group, not write permission on the parent, so this works
        regardless of who authored it). Minimal payload confirmed
        against h's CreateAnnotationSchema (2026-08-16): `target` isn't
        required for a reply, and `group` is actively IGNORED by the
        server when `references` is set -- the reply always inherits the
        parent's group, so there's no group field to get wrong here."""
        body = {
            "uri": parent["uri"],
            "references": [parent["id"]],
            "text": text,
            "tags": tags or [],
        }
        return self._request("POST", "/annotations", body=body)

    def create_annotation(self, *, uri: str, text: str, tags: list[str],
                           target: list[dict], group: str,
                           document: dict | None = None) -> dict:
        """POST a new TOP-LEVEL annotation (no `references` -- for a reply
        use create_reply, which also handles the group-is-ignored-for-
        replies rule that does NOT apply here: for a top-level annotation
        `group` is honored exactly as given). Used by move_annotation.py to
        recreate an annotation in a different group -- Hypothesis has no
        API to change an existing annotation's group (see
        UpdateAnnotationSchema in h's own source: group/groupid/userid/
        references are all silently dropped on PATCH), so "moving" one
        means creating a copy elsewhere and deleting the original."""
        body = {"uri": uri, "text": text, "tags": tags, "target": target, "group": group}
        if document:
            body["document"] = document
        return self._request("POST", "/annotations", body=body)

    def delete_annotation(self, annotation_id: str) -> dict:
        """DELETE -- only succeeds on annotations this token's account
        authored (same author-only write rule as update_tags)."""
        return self._request("DELETE", f"/annotations/{annotation_id}")
