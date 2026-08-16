#!/usr/bin/env python3
"""build_dashboard.py -- render data/annotations.json as a single
self-contained, filterable/sortable HTML page: hypothesis/dashboard.html.

Pure standard library, same convention as the rest of this directory.
The output embeds all annotation content (readers' candid feedback) as
inline JSON, so dashboard.html carries the same privacy posture as
data/annotations.json itself -- gitignored, never committed.

Two publish paths:
  - No --install: writes hypothesis/dashboard.html only, for publishing
    by hand as a private Claude Artifact ("Reader Margins").
  - --install PATH: also writes the same content to PATH (parents
    created as needed) -- used on amrut by run_pipeline.sh to publish
    at https://secondshanti.org/as/private/dashboard/, self-refreshing
    on every cron run with no manual republish step. That route is
    gated by the same Google-OAuth login as the rest of /as/private/*,
    PLUS an extra owner-only check in the Caddyfile (X-Auth-Request-
    Email must be rhinusgaleo@gmail.com) -- /as/private/* alone would
    also admit every whitelisted reader, which would leak everyone's
    candid annotations to each other.

Usage:
    python3 build_dashboard.py
    python3 build_dashboard.py --install /var/www/as/private/dashboard/index.html
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HYPOTHESIS_DIR = Path(__file__).parent
DATA_PATH = HYPOTHESIS_DIR / "data" / "annotations.json"
TAXONOMY_PATH = HYPOTHESIS_DIR / "taxonomy.json"
OUTPUT_PATH = HYPOTHESIS_DIR / "dashboard.html"

# Six semantic clusters group the nine taxonomy tags by what kind of
# review action they call for, not by an arbitrary per-tag color --
# this is the same grouping a human editor would triage by.
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

CLUSTER_LABELS = {
    "mechanical": "Mechanical",
    "verify": "Needs verification",
    "clarify": "Needs clarity",
    "constructive": "Constructive",
    "precision": "Sanskrit precision",
    "positive": "Positive",
}


def chapter_slug(uri: str) -> str:
    parts = uri.rstrip("/").rsplit("/", 1)
    return parts[-1] if parts else uri


def annotation_link(annotation_id: str, uri: str) -> str:
    """Deep-link straight to the annotation on our own domain, via the
    Hypothesis CLIENT's own #annotations:<id> URL-fragment convention
    (documented, works with the embedded client the same as the
    extension -- not a hyp.is-specific feature). Every book/essay page
    already embeds https://hypothes.is/embed.js directly (see
    templates/html_chapter.html's js-hypothesis-config script), so this
    needs no browser extension and no third-party bounce service.
    Deliberately NOT hyp.is/<id>/<uri>: that's Hypothesis's own
    extension-detection relay -- with the extension it redirects
    straight to the page, but without one (most mobile browsers) it
    falls back to hypothes.is's "Via" proxy, which as of 2026-08-16
    returns "Access to Via is now restricted" instead of the page.
    Confirmed live: broken on mobile (no extension), fine on desktop
    (extension installed) -- exactly that split."""
    return f"{uri.rstrip('/')}/#annotations:{annotation_id}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", type=Path, default=None,
                         help="also write the rendered page to this path (e.g. a webroot)")
    args = parser.parse_args()

    if not DATA_PATH.exists():
        print(f"No {DATA_PATH} -- run pull_annotations.py first.")
        return 1

    annotations = json.loads(DATA_PATH.read_text())
    taxonomy = json.loads(TAXONOMY_PATH.read_text())["tags"]

    # An annotation's status comes from the LATEST message in its whole
    # reply thread, not just a single direct reply -- otherwise a
    # reader responding to an "awaiting-reader" note would leave the
    # card stuck showing "awaiting reader" forever even after the ball
    # is back in the owner's court. Threads are grouped by root (an
    # annotation with no references of its own); a reply belongs to
    # whichever known root appears anywhere in its own "references"
    # list, which works regardless of nesting depth or list ordering
    # (Hypothesis's own client can include the full ancestor chain, not
    # just the immediate parent, so this doesn't assume a fixed index).
    #
    #   - latest message is OUR reply carrying one of the three status
    #     tags -> that status (most recent action wins, so a reader
    #     pushing back after a "resolved" reply reopens it: their
    #     later message makes THEM the latest, triggering the next
    #     branch instead)
    #   - latest message is from anyone else, after we'd already
    #     replied at least once in the thread -> "reader-replied":
    #     they came back, needs a fresh look, regardless of whatever
    #     status our own last reply had
    #   - no replies yet, or nobody but the original author has ever
    #     posted in it -> no status (row reads as untouched)
    OWNER_USER = "rhinusgaleo"
    STATUS_TAGS = ("resolved", "acknowledged", "awaiting-reader")

    root_ids = {a["id"] for a in annotations if not a.get("references")}
    threads: dict[str, list[dict]] = {rid: [] for rid in root_ids}
    for a in annotations:
        for rid in (a.get("references") or []):
            if rid in threads:
                threads[rid].append(a)
                break  # a reply belongs to exactly one thread

    own_reply_status: dict[str, str] = {}
    parent_status: dict[str, str] = {}
    for root_id, msgs in threads.items():
        msgs.sort(key=lambda m: m["created"])
        for m in msgs:
            matched = next((t for t in STATUS_TAGS if t in m.get("tags", [])), None)
            if matched:
                own_reply_status[m["id"]] = matched
        if not msgs:
            continue
        last = msgs[-1]
        if last["user"] == OWNER_USER:
            matched = next((t for t in STATUS_TAGS if t in last.get("tags", [])), None)
            if matched:
                parent_status[root_id] = matched
        elif any(m["user"] == OWNER_USER for m in msgs):
            parent_status[root_id] = "reader-replied"

    def status_of(annotation_id: str) -> str | None:
        return own_reply_status.get(annotation_id) or parent_status.get(annotation_id)

    # Trim to what the page actually renders, and derive the chapter
    # slug once here rather than in client JS.
    rows = []
    for a in annotations:
        status = status_of(a["id"])
        rows.append({
            "id": a["id"],
            "created": a["created"],
            "user": a["user"],
            "group": a["group_name"],
            "chapter": chapter_slug(a["uri"]),
            "title": a["document_title"],
            "uri": a["uri"],
            "quote": a["quote"],
            "quote_prefix": a.get("quote_prefix", ""),
            "quote_suffix": a.get("quote_suffix", ""),
            "text": a["text"],
            "tags": a.get("tags", []),
            "suggested": a.get("suggested_tags", []),
            "reply": a.get("is_reply", False),
            "link": annotation_link(a["id"], a["uri"]),
            "status": status,
            "resolved": status in ("resolved", "acknowledged"),
        })

    data_json = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    taxonomy_json = json.dumps(taxonomy, ensure_ascii=False)
    clusters_json = json.dumps(TAG_CLUSTERS, ensure_ascii=False)
    cluster_labels_json = json.dumps(CLUSTER_LABELS, ensure_ascii=False)

    built_at = datetime.now(timezone.utc).isoformat()

    html = HTML_TEMPLATE.replace("__DATA__", data_json) \
                         .replace("__TAXONOMY__", taxonomy_json) \
                         .replace("__CLUSTERS__", clusters_json) \
                         .replace("__CLUSTER_LABELS__", cluster_labels_json) \
                         .replace("__BUILT_AT__", built_at)

    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Wrote {len(rows)} annotation(s) -> {OUTPUT_PATH}")

    if args.install:
        args.install.parent.mkdir(parents=True, exist_ok=True)
        args.install.write_text(html, encoding="utf-8")
        print(f"Installed -> {args.install}")

    return 0


HTML_TEMPLATE = r"""<!doctype html>
<title>Reader Margins</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {
  --bg: #eef0f2;
  --surface: #ffffff;
  --surface-2: #e4e8ec;
  --text: #1e2530;
  --text-muted: #5b6472;
  --border: #d7dce1;
  --accent: #3d4f7a;
  --accent-strong: #24304f;
  --accent-ink: #ffffff;

  --c-mechanical-bg: #e4e6ea; --c-mechanical-fg: #4b5563;
  --c-verify-bg: #f3e2d8; --c-verify-fg: #9a4a24;
  --c-clarify-bg: #f6ecc9; --c-clarify-fg: #8a6a10;
  --c-constructive-bg: #d9ece7; --c-constructive-fg: #1f6e5c;
  --c-precision-bg: #ebdff0; --c-precision-fg: #7a3a8a;
  --c-positive-bg: #dfeed2; --c-positive-fg: #3f6b1f;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #12151b;
    --surface: #1b2029;
    --surface-2: #232a35;
    --text: #e4e7ec;
    --text-muted: #97a0ad;
    --border: #2c333f;
    --accent: #8fa3d9;
    --accent-strong: #b7c6ea;
    --accent-ink: #12151b;

    --c-mechanical-bg: #2b3038; --c-mechanical-fg: #b8c0cc;
    --c-verify-bg: #3a2620; --c-verify-fg: #e7a67e;
    --c-clarify-bg: #3a3018; --c-clarify-fg: #e3c465;
    --c-constructive-bg: #17302b; --c-constructive-fg: #7fd6bf;
    --c-precision-bg: #2e2233; --c-precision-fg: #d2a6e0;
    --c-positive-bg: #202f18; --c-positive-fg: #a8d383;
  }
}
:root[data-theme="dark"] {
  --bg: #12151b;
  --surface: #1b2029;
  --surface-2: #232a35;
  --text: #e4e7ec;
  --text-muted: #97a0ad;
  --border: #2c333f;
  --accent: #8fa3d9;
  --accent-strong: #b7c6ea;
  --accent-ink: #12151b;

  --c-mechanical-bg: #2b3038; --c-mechanical-fg: #b8c0cc;
  --c-verify-bg: #3a2620; --c-verify-fg: #e7a67e;
  --c-clarify-bg: #3a3018; --c-clarify-fg: #e3c465;
  --c-constructive-bg: #17302b; --c-constructive-fg: #7fd6bf;
  --c-precision-bg: #2e2233; --c-precision-fg: #d2a6e0;
  --c-positive-bg: #202f18; --c-positive-fg: #a8d383;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  font-size: 15px;
  line-height: 1.5;
}
h1, h2, .serif {
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Noto Serif", serif;
}

header.top {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  padding: 20px clamp(16px, 4vw, 40px) 14px;
}
header.top h1 {
  margin: 0 0 2px;
  font-size: 1.5rem;
  font-weight: 600;
  text-wrap: balance;
}
header.top .subtitle {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.stats-hero {
  margin-top: 14px;
}
.hero-stat {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1px;
  background: var(--c-verify-bg);
  border: 1px solid var(--c-verify-fg);
  border-radius: 10px;
  padding: 12px 22px;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
}
.hero-stat:hover { filter: brightness(1.08); }
.hero-stat.active {
  background: var(--c-verify-fg);
  border-color: var(--c-verify-fg);
}
.hero-stat.active .hero-n, .hero-stat.active .hero-label, .hero-stat.active .hero-total {
  color: #fff;
}
.hero-n {
  font-variant-numeric: tabular-nums;
  font-size: 2.3rem;
  font-weight: 800;
  line-height: 1;
  color: var(--c-verify-fg);
}
.hero-label {
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--c-verify-fg);
}
.hero-total {
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 3px;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}
.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 10px;
  min-width: 70px;
}
.stat .n {
  font-variant-numeric: tabular-nums;
  font-size: 1rem;
  font-weight: 700;
  display: block;
}
.stat .label {
  color: var(--text-muted);
  font-size: 0.66rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
/* Status tiles (Resolved / Acknowledged / Awaiting reader / Reader
   replied) are real <button>s, clickable filters -- visually distinct
   from the plain informational tiles (Tagged / AI-suggested /
   Untagged / Readers), which stay muted and non-interactive.
   border/background/color must all be explicit here (matching .chip's
   approach elsewhere) -- a bare <button> carries its own UA-stylesheet
   text color (buttontext, effectively black) that beats inheritance
   from body's --text, so without this the numbers render black no
   matter what theme is active. Confirmed live 2026-08-16: only the
   button tiles were affected, the plain <div> tiles (.stat-muted)
   inherited correctly since a div has no such default. */
.stat-btn {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
  font-family: inherit;
  text-align: left;
}
.stat-btn:hover { border-color: var(--accent); }
.stat-btn.active {
  background: var(--accent);
  border-color: var(--accent);
}
.stat-btn.active .n, .stat-btn.active .label { color: var(--accent-ink); }
.stat-muted {
  opacity: 0.75;
}

.filters {
  position: sticky;
  top: 84px;
  z-index: 9;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  padding: 12px clamp(16px, 4vw, 40px);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.filter-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.filter-row .row-label {
  color: var(--text-muted);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  width: 74px;
  flex-shrink: 0;
}
input[type="search"] {
  flex: 1;
  min-width: 180px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 7px 12px;
  color: var(--text);
  font-size: 0.9rem;
}
input[type="search"]:focus, select:focus, .chip:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 1px;
}
select {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 10px;
  color: var(--text);
  font-size: 0.85rem;
}

.chip {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-muted);
  border-radius: 999px;
  padding: 4px 11px;
  font-size: 0.8rem;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.12s, color 0.12s, border-color 0.12s;
}
.chip .n { opacity: 0.7; margin-left: 4px; font-variant-numeric: tabular-nums; }
.chip.active {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--accent-ink);
}
.chip.active .n { opacity: 0.85; }
.chip.clear {
  color: var(--accent);
  border-style: dashed;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px 24px;
}
.header-main { min-width: 0; }
.header-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  flex-shrink: 0;
}
.refresh-btn-big {
  border: 2px solid var(--accent);
  background: var(--accent);
  color: var(--accent-ink);
  border-radius: 10px;
  padding: 14px 30px;
  font-size: 1.05rem;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  white-space: nowrap;
}
.refresh-btn-big:hover:not(:disabled) { filter: brightness(1.1); }
.refresh-btn-big:disabled {
  opacity: 0.6;
  cursor: default;
}
.built-note {
  margin: 0;
  font-size: 0.78rem;
  color: var(--text-muted);
  text-align: right;
  font-variant-numeric: tabular-nums;
}

main {
  padding: 18px clamp(16px, 4vw, 40px) 60px;
  max-width: 900px;
  margin: 0 auto;
}
.empty {
  color: var(--text-muted);
  text-align: center;
  padding: 40px 0;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
}
.card .meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 10px;
  align-items: baseline;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 8px;
}
.card .meta .user { color: var(--text); font-weight: 600; }
.card .meta .sep { opacity: 0.5; }
.card .meta .ago { opacity: 0.7; font-variant-numeric: tabular-nums; }
.card .meta a { color: var(--accent); text-decoration: none; }
.card .meta a:hover { text-decoration: underline; }
.card blockquote {
  margin: 0 0 8px;
  padding: 6px 0 6px 12px;
  border-left: 3px solid var(--border);
  color: var(--text-muted);
  font-size: 0.88rem;
  font-style: italic;
}
.card blockquote mark {
  background: var(--c-clarify-bg);
  color: var(--text);
  font-style: normal;
  padding: 0 2px;
  border-radius: 2px;
}
.card .comment {
  margin: 0 0 10px;
  white-space: pre-wrap;
}
.card .tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.tag-chip {
  border-radius: 999px;
  padding: 2px 10px;
  font-size: 0.74rem;
  font-weight: 600;
}
.tag-chip.suggested {
  background: transparent;
  border: 1px dashed currentColor;
  opacity: 0.75;
}
.tag-chip.suggested::after {
  content: " · AI";
  font-weight: 400;
  opacity: 0.8;
}
.reply-badge {
  font-size: 0.72rem;
  color: var(--text-muted);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 1px 8px;
}
.resolved-badge {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-positive-fg);
  background: var(--c-positive-bg);
  border-radius: 999px;
  padding: 1px 8px;
}
.acknowledged-badge {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-precision-fg);
  background: var(--c-precision-bg);
  border-radius: 999px;
  padding: 1px 8px;
}
.awaiting-badge {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-clarify-fg);
  background: var(--c-clarify-bg);
  border-radius: 999px;
  padding: 1px 8px;
}
.reader-replied-badge {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--c-verify-fg);
  background: var(--c-verify-bg);
  border-radius: 999px;
  padding: 1px 8px;
}
.card.is-resolved {
  opacity: 0.6;
}
.resolve-row {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.reply-text {
  width: 100%;
  resize: vertical;
  font-family: inherit;
  font-size: 0.85rem;
  padding: 7px 10px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  box-sizing: border-box;
}
.reply-text:focus {
  outline: 2px solid var(--accent);
  outline-offset: -1px;
}
.resolve-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.reply-tag {
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  font-size: 0.8rem;
  padding: 5px 8px;
}
.resolve-btn {
  border: 1px solid var(--accent);
  background: transparent;
  color: var(--accent);
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}
.resolve-btn:hover:not(:disabled) {
  background: var(--accent);
  color: var(--accent-ink);
}
.resolve-btn:disabled {
  opacity: 0.6;
  cursor: default;
}
.resolve-btn-force {
  border-color: var(--c-verify-fg);
  color: var(--c-verify-fg);
}
.resolve-btn-force:hover:not(:disabled) {
  background: var(--c-verify-fg);
  color: #fff;
}
.resolve-warning {
  font-size: 0.78rem;
  color: var(--c-verify-fg);
}
.resolve-error {
  font-size: 0.78rem;
  color: var(--c-verify-fg);
}

footer {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.75rem;
  padding: 20px;
}
a { color: var(--accent); }

@media (max-width: 560px) {
  .filter-row .row-label { width: auto; }
}
</style>

<header class="top">
  <div class="header-row">
    <div class="header-main">
      <h1 class="serif">Reader Margins</h1>
      <p class="subtitle">Consolidated annotations across every Atomic Sanskrit reading group</p>
    </div>
    <div class="header-actions">
      <button class="refresh-btn-big" id="refresh-btn">⟳ Refresh now</button>
      <p class="built-note" id="built-note"></p>
    </div>
  </div>
  <div class="stats-hero" id="stats-hero"></div>
  <div class="stats" id="stats"></div>
</header>

<div class="filters">
  <div class="filter-row">
    <span class="row-label">Search</span>
    <input type="search" id="search" placeholder="Search quotes and comments…">
    <select id="sort">
      <option value="date-desc">Newest first</option>
      <option value="date-asc">Oldest first</option>
      <option value="chapter">By chapter</option>
      <option value="user">By reader</option>
    </select>
    <button class="chip active" id="resolved-toggle">Hide resolved<span class="n" id="resolved-count"></span></button>
  </div>
  <div class="filter-row" id="reader-filters"></div>
  <div class="filter-row" id="chapter-filter"></div>
  <div class="filter-row" id="tag-filters"></div>
</div>

<main id="main"></main>

<footer>Private working view · tags marked <span class="tag-chip suggested" style="border-color:var(--text-muted);color:var(--text-muted)">example</span> are AI-suggested only, not written to Hypothesis</footer>

<script>
const DATA = __DATA__;
const TAXONOMY = __TAXONOMY__;
const CLUSTERS = __CLUSTERS__;
const CLUSTER_LABELS = __CLUSTER_LABELS__;
const BUILT_AT = "__BUILT_AT__";  // ISO 8601 UTC, set by build_dashboard.py at render time

const state = {
  search: "",
  readers: new Set(),
  chapter: "",
  tags: new Set(),
  sort: "date-desc",
  hideResolved: true,
  statusFilter: null,  // null | "unresolved" | "resolved" | "acknowledged" | "awaiting-reader" | "reader-replied"
};

function clusterOf(tag) { return CLUSTERS[tag] || "mechanical"; }

function fmtDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

// Same idea as the header's "Built X ago" ticker (reader's own clock,
// no server round-trip) but coarser -- an annotation can be months
// old, so per-second precision would be noise. Cascades to the two
// most relevant units for the age: minutes alone under an hour, hours
// + minutes under a day, days alone under a month, months + days once
// a month or more (days dropped there -- "2mo 15d 4h" is more
// precision than anyone reads at a glance). Computed once per render()
// call, not on its own ticking interval -- render() already re-fires
// on every filter/sort/reply action, and a periodic full re-render
// would risk wiping an in-progress reply draft in an open textarea.
function fmtAgo(iso) {
  const diffMs = Math.max(0, Date.now() - new Date(iso).getTime());
  const minute = 60000, hour = 60 * minute, day = 24 * hour, month = 30 * day, year = 365 * day;
  if (diffMs < minute) return "just now";
  if (diffMs < hour) return `${Math.floor(diffMs / minute)}m ago`;
  if (diffMs < day) {
    const h = Math.floor(diffMs / hour), m = Math.floor((diffMs % hour) / minute);
    return m > 0 ? `${h}h ${m}m ago` : `${h}h ago`;
  }
  if (diffMs < month) return `${Math.floor(diffMs / day)}d ago`;
  if (diffMs < year) {
    const mo = Math.floor(diffMs / month), d = Math.floor((diffMs % month) / day);
    return d > 0 ? `${mo}mo ${d}d ago` : `${mo}mo ago`;
  }
  const y = Math.floor(diffMs / year), mo = Math.floor((diffMs % year) / month);
  return mo > 0 ? `${y}y ${mo}mo ago` : `${y}y ago`;
}

function uniqueSorted(arr) { return [...new Set(arr)].sort(); }

function buildReaderFilters() {
  const counts = {};
  DATA.forEach(a => counts[a.user] = (counts[a.user] || 0) + 1);
  const readers = uniqueSorted(DATA.map(a => a.user));
  const el = document.getElementById("reader-filters");
  el.innerHTML = '<span class="row-label">Reader</span>';
  readers.forEach(r => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.innerHTML = `${r}<span class="n">${counts[r]}</span>`;
    chip.onclick = () => {
      state.readers.has(r) ? state.readers.delete(r) : state.readers.add(r);
      chip.classList.toggle("active");
      render();
    };
    el.appendChild(chip);
  });
}

function buildChapterFilter() {
  const chapters = uniqueSorted(DATA.map(a => a.chapter));
  const el = document.getElementById("chapter-filter");
  el.innerHTML = '<span class="row-label">Chapter</span>';
  const select = document.createElement("select");
  select.innerHTML = '<option value="">All chapters</option>' +
    chapters.map(c => `<option value="${c}">${c}</option>`).join("");
  select.onchange = () => { state.chapter = select.value; render(); };
  el.appendChild(select);
}

function buildTagFilters() {
  const counts = {};
  DATA.forEach(a => {
    [...a.tags, ...a.suggested].forEach(t => counts[t] = (counts[t] || 0) + 1);
  });
  const el = document.getElementById("tag-filters");
  el.innerHTML = '<span class="row-label">Tag</span>';
  const clear = document.createElement("button");
  clear.className = "chip clear";
  clear.textContent = "Clear tags";
  clear.onclick = () => {
    state.tags.clear();
    document.querySelectorAll(".tag-filter-chip").forEach(c => c.classList.remove("active"));
    render();
  };
  el.appendChild(clear);
  Object.keys(TAXONOMY).forEach(tag => {
    const chip = document.createElement("button");
    chip.className = "chip tag-filter-chip";
    const cluster = clusterOf(tag);
    chip.style.setProperty("--tag-bg", `var(--c-${cluster}-bg)`);
    chip.style.setProperty("--tag-fg", `var(--c-${cluster}-fg)`);
    chip.innerHTML = `${tag}<span class="n">${counts[tag] || 0}</span>`;
    chip.onclick = () => {
      state.tags.has(tag) ? state.tags.delete(tag) : state.tags.add(tag);
      chip.classList.toggle("active");
      render();
    };
    el.appendChild(chip);
  });
}

function matches(a) {
  if (state.statusFilter === "unresolved") {
    if (a.status === "resolved" || a.status === "acknowledged") return false;
  } else if (state.statusFilter) {
    if (a.status !== state.statusFilter) return false;
  }
  if (state.hideResolved && a.resolved) return false;
  if (state.readers.size && !state.readers.has(a.user)) return false;
  if (state.chapter && a.chapter !== state.chapter) return false;
  if (state.tags.size) {
    const all = new Set([...a.tags, ...a.suggested]);
    let ok = false;
    state.tags.forEach(t => { if (all.has(t)) ok = true; });
    if (!ok) return false;
  }
  if (state.search) {
    const hay = (a.quote + " " + a.text + " " + a.user).toLowerCase();
    if (!hay.includes(state.search)) return false;
  }
  return true;
}

// Only applied within the two date-based sorts, not chapter/user --
// those modes mean "group strictly by chapter/reader" and interleaving
// by status would break that. reader-replied floats to the very top
// (a live conversation needs a response more urgently than something
// nobody's looked at yet); awaiting-reader sinks toward the bottom
// (the ball's in the reader's court, not yours -- see "should it go
// down?", answered 2026-08-16); untouched (no status) sits in between.
const STATUS_SORT_WEIGHT = { "reader-replied": 0, "awaiting-reader": 2 };
function statusWeight(a) { return STATUS_SORT_WEIGHT[a.status] ?? 1; }

function sortRows(rows) {
  const s = [...rows];
  if (state.sort === "date-desc") s.sort((a, b) => statusWeight(a) - statusWeight(b) || b.created.localeCompare(a.created));
  else if (state.sort === "date-asc") s.sort((a, b) => statusWeight(a) - statusWeight(b) || a.created.localeCompare(b.created));
  else if (state.sort === "chapter") s.sort((a, b) => a.chapter.localeCompare(b.chapter) || b.created.localeCompare(a.created));
  else if (state.sort === "user") s.sort((a, b) => a.user.localeCompare(b.user) || b.created.localeCompare(a.created));
  return s;
}

function tagChipHTML(tag, suggested) {
  const cluster = clusterOf(tag);
  const cls = suggested ? "tag-chip suggested" : "tag-chip";
  const style = suggested
    ? `color:var(--c-${cluster}-fg)`
    : `background:var(--c-${cluster}-bg);color:var(--c-${cluster}-fg)`;
  return `<span class="${cls}" style="${style}">${tag}</span>`;
}

const STATUS_BADGE = {
  "resolved": ["resolved-badge", "resolved"],
  "acknowledged": ["acknowledged-badge", "acknowledged"],
  "awaiting-reader": ["awaiting-badge", "awaiting reader"],
  "reader-replied": ["reader-replied-badge", "reader replied ↩"],
};

function cardHTML(a) {
  const tagHTML = a.tags.map(t => tagChipHTML(t, false)).join("") +
                   a.suggested.map(t => tagChipHTML(t, true)).join("");
  const quote = a.quote
    ? `<blockquote>&hellip;${escapeHTML(a.quote_prefix || "")}<mark>${escapeHTML(a.quote)}</mark>${escapeHTML(a.quote_suffix || "")}&hellip;</blockquote>`
    : "";
  const reply = a.reply ? '<span class="reply-badge">reply</span>' : "";
  const badge = STATUS_BADGE[a.status];
  const statusBadge = badge ? `<span class="${badge[0]}">${badge[1]}</span>` : "";
  // Composer stays available for anything not fully closed -- including
  // "awaiting-reader", so a conversation can continue -- and never on a
  // reply annotation itself (this composer replies to READER comments,
  // not to our own replies).
  const showComposer = !a.reply && a.status !== "resolved" && a.status !== "acknowledged";
  const resolveControl = showComposer
    ? `<div class="resolve-row" id="resolve-row-${a.id}">
         <textarea class="reply-text" id="reply-text-${a.id}" rows="2" placeholder="Optional note to the reader…"></textarea>
         <div class="resolve-controls">
           <select class="reply-tag" id="reply-tag-${a.id}">
             <option value="resolved">Resolved</option>
             <option value="acknowledged">Acknowledged</option>
             <option value="awaiting-reader">Awaiting reader reply</option>
           </select>
           <button class="resolve-btn" onclick="postReply('${a.id}', false, this)">Post</button>
         </div>
       </div>`
    : "";
  return `<article class="card${a.resolved ? " is-resolved" : ""}" id="card-${a.id}">
    <div class="meta">
      <span class="user">${escapeHTML(a.user)}</span>
      <span class="sep">·</span>
      <a href="${a.uri}" target="_blank" rel="noopener">${escapeHTML(a.chapter)}</a>
      <span class="sep">·</span>
      <span>${escapeHTML(a.group)}</span>
      <span class="sep">·</span>
      <span>${fmtDate(a.created)} <span class="ago">(${fmtAgo(a.created)})</span></span>
      ${reply}
      ${statusBadge}
      <span class="sep">·</span>
      <a href="${a.link}" target="_blank" rel="noopener">View on Hypothesis &rarr;</a>
    </div>
    ${quote}
    <p class="comment">${escapeHTML(a.text)}</p>
    <div class="tags">${tagHTML}</div>
    ${resolveControl}
  </article>`;
}

async function postReply(id, force, btnEl) {
  const row = document.getElementById(`resolve-row-${id}`);
  const textEl = document.getElementById(`reply-text-${id}`);
  const tagEl = document.getElementById(`reply-tag-${id}`);
  const text = textEl ? textEl.value.trim() : "";
  const tag = tagEl ? tagEl.value : "resolved";

  if (tag === "awaiting-reader" && !text) {
    const controls = row.querySelector(".resolve-controls");
    if (!controls.querySelector(".resolve-error")) {
      controls.insertAdjacentHTML("beforeend",
        '<span class="resolve-error">Add a note for the reader first.</span>');
    }
    return;
  }

  btnEl.disabled = true;
  btnEl.textContent = force ? "Posting anyway…" : "Posting…";
  let res;
  try {
    res = await fetch("/as/private/dashboard/api/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, text, tag, force }),
    });
  } catch (e) {
    row.innerHTML = `<span class="resolve-error">Network error -- try again.</span>`;
    return;
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    row.innerHTML = `<span class="resolve-error">${escapeHTML(body.error || `HTTP ${res.status}`)}</span>`;
    return;
  }
  const body = await res.json();
  if (body.status === "still_live") {
    row.innerHTML = `<span class="resolve-warning">Still live on the deployed site -- push/deploy first, or</span>
      <button class="resolve-btn resolve-btn-force" onclick="postReply('${id}', true, this)">post anyway</button>`;
    return;
  }
  if (body.status === "posted") {
    const item = DATA.find(d => d.id === id);
    if (item) {
      item.status = body.tag;
      item.resolved = body.tag === "resolved" || body.tag === "acknowledged";
    }
    renderStats();
    render();
    return;
  }
  row.innerHTML = `<span class="resolve-error">Unexpected response.</span>`;
}

function escapeHTML(s) {
  return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function setStatusFilter(key) {
  state.statusFilter = state.statusFilter === key ? null : key;
  // A status filter and "hide resolved/acknowledged" can conflict the
  // same way the toggle-side check above does (e.g. filtering to
  // "Resolved" while hiding resolved would just be empty) -- clearing
  // hideResolved here keeps a filter click always showing SOMETHING.
  if (state.statusFilter) {
    state.hideResolved = false;
    const toggle = document.getElementById("resolved-toggle");
    toggle.classList.remove("active");
    toggle.firstChild.textContent = "Hide resolved";
  }
  renderStats();
  render();
}

function renderStats() {
  // Reply annotations (our own composer posts) aren't reader content --
  // counting them alongside root annotations would inflate every tile
  // (a resolved thread is 2 DATA rows: the flagged comment + our
  // reply, both carrying the same status). Every count here is rooted
  // annotations only, matching what a reader actually wrote.
  const roots = DATA.filter(a => !a.reply);
  const total = roots.length;
  const tagged = roots.filter(a => a.tags.length).length;
  const aiOnly = roots.filter(a => !a.tags.length && a.suggested.length).length;
  const untagged = roots.filter(a => !a.tags.length && !a.suggested.length).length;
  const readers = uniqueSorted(DATA.map(a => a.user)).length;

  const countOf = status => roots.filter(a => a.status === status).length;
  const resolved = countOf("resolved");
  const acknowledged = countOf("acknowledged");
  const awaitingReader = countOf("awaiting-reader");
  const readerReplied = countOf("reader-replied");
  const unresolved = total - resolved - acknowledged;

  const heroActive = state.statusFilter === "unresolved" ? " active" : "";
  document.getElementById("stats-hero").innerHTML = `
    <button class="hero-stat${heroActive}" onclick="setStatusFilter('unresolved')">
      <span class="hero-n">${unresolved}</span>
      <span class="hero-label">Unresolved</span>
      <span class="hero-total">of ${total} total</span>
    </button>`;

  const statusStats = [
    ["resolved", "Resolved", resolved],
    ["acknowledged", "Acknowledged", acknowledged],
    ["awaiting-reader", "Awaiting reader", awaitingReader],
    ["reader-replied", "Reader replied", readerReplied],
  ];
  const metaStats = [
    ["Tagged", tagged],
    ["AI-suggested", aiOnly],
    ["Untagged", untagged],
    ["Readers", readers],
  ];

  const statusHTML = statusStats.map(([key, label, n]) =>
    `<button class="stat stat-btn${state.statusFilter === key ? " active" : ""}" onclick="setStatusFilter('${key}')">
       <span class="n">${n}</span><span class="label">${label}</span>
     </button>`
  ).join("");
  const metaHTML = metaStats.map(([label, n]) =>
    `<div class="stat stat-muted"><span class="n">${n}</span><span class="label">${label}</span></div>`
  ).join("");
  document.getElementById("stats").innerHTML = statusHTML + metaHTML;

  // The toggle hides anything a.resolved (resolved OR acknowledged --
  // both closed states), so its count reflects that, not the
  // "Resolved" stat tile above (which is resolved-only for clarity).
  document.getElementById("resolved-count").textContent = DATA.filter(a => !a.reply && a.resolved).length;
}

function render() {
  const rows = sortRows(DATA.filter(matches));
  const main = document.getElementById("main");
  main.innerHTML = rows.length
    ? rows.map(cardHTML).join("")
    : '<p class="empty">No annotations match the current filters.</p>';
}

document.getElementById("search").addEventListener("input", e => {
  state.search = e.target.value.trim().toLowerCase();
  render();
});
document.getElementById("sort").addEventListener("change", e => {
  state.sort = e.target.value;
  render();
});
const resolvedToggle = document.getElementById("resolved-toggle");
resolvedToggle.addEventListener("click", () => {
  state.hideResolved = !state.hideResolved;
  // Hiding resolved/acknowledged while a status filter demands showing
  // ONLY resolved/acknowledged would just produce an empty list -- the
  // two are conflicting intents, so turning the toggle on clears any
  // such filter rather than leaving a confusing blank page.
  if (state.hideResolved && (state.statusFilter === "resolved" || state.statusFilter === "acknowledged")) {
    state.statusFilter = null;
    renderStats();
  }
  resolvedToggle.classList.toggle("active", state.hideResolved);
  resolvedToggle.firstChild.textContent = state.hideResolved ? "Hide resolved" : "Show resolved";
  render();
});

const refreshBtn = document.getElementById("refresh-btn");
refreshBtn.addEventListener("click", async () => {
  refreshBtn.disabled = true;
  refreshBtn.textContent = "⟳ Refreshing…";
  // Bounded client-side timeout, on top of the backend now also being
  // fast by design (pull + rebuild only, no tagging -- see
  // refresh_dashboard_fast.sh) -- a plain unbounded fetch() can die
  // silently with no error and no reload if the tab gets backgrounded
  // or the phone locks mid-wait, which read exactly like "no callback,
  // had to refresh manually" before this existed.
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 45000);
  let res;
  try {
    res = await fetch("/as/private/dashboard/api/refresh", { method: "POST", signal: controller.signal });
  } catch (e) {
    refreshBtn.textContent = e.name === "AbortError" ? "⟳ Timed out — retry" : "⟳ Network error — retry";
    refreshBtn.disabled = false;
    return;
  } finally {
    clearTimeout(timeoutId);
  }
  if (!res.ok) {
    refreshBtn.textContent = "⟳ Refresh failed — retry";
    refreshBtn.disabled = false;
    return;
  }
  // Full page reload (not a DATA patch) -- the whole point is to pick
  // up everything new since page load, not just the one thing this
  // button call knows about, including brand-new reader annotations
  // this session's DATA array was never given.
  window.location.reload();
});

// "Built X ago" ticks every second, purely local text formatting --
// per explicit instruction, this must NEVER re-fetch or touch DATA,
// only reformat the elapsed time since BUILT_AT (embedded at build
// time, see build_dashboard.py) against the reader's own clock.
function formatAgo(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  const parts = [];
  if (h > 0) parts.push(`${h}h`);
  if (h > 0 || m > 0) parts.push(`${m}m`);
  parts.push(`${s}s`);
  return parts.join(" ");
}
function tickBuiltNote() {
  const builtMs = new Date(BUILT_AT).getTime();
  document.getElementById("built-note").textContent = `Built ${formatAgo(Date.now() - builtMs)} ago`;
}
tickBuiltNote();
setInterval(tickBuiltNote, 1000);

renderStats();
buildReaderFilters();
buildChapterFilter();
buildTagFilters();
render();
</script>
"""


if __name__ == "__main__":
    raise SystemExit(main())
