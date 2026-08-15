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


def hyp_is_link(annotation_id: str, uri: str) -> str:
    stripped = uri.split("://", 1)[-1]
    return f"https://hyp.is/{annotation_id}/{stripped}"


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

    # Trim to what the page actually renders, and derive the chapter
    # slug once here rather than in client JS.
    rows = []
    for a in annotations:
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
            "link": hyp_is_link(a["id"], a["uri"]),
        })

    data_json = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    taxonomy_json = json.dumps(taxonomy, ensure_ascii=False)
    clusters_json = json.dumps(TAG_CLUSTERS, ensure_ascii=False)
    cluster_labels_json = json.dumps(CLUSTER_LABELS, ensure_ascii=False)

    html = HTML_TEMPLATE.replace("__DATA__", data_json) \
                         .replace("__TAXONOMY__", taxonomy_json) \
                         .replace("__CLUSTERS__", clusters_json) \
                         .replace("__CLUSTER_LABELS__", cluster_labels_json)

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

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}
.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  min-width: 84px;
}
.stat .n {
  font-variant-numeric: tabular-nums;
  font-size: 1.15rem;
  font-weight: 700;
  display: block;
}
.stat .label {
  color: var(--text-muted);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
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
  <h1 class="serif">Reader Margins</h1>
  <p class="subtitle">Consolidated annotations across every Atomic Sanskrit reading group</p>
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

const state = {
  search: "",
  readers: new Set(),
  chapter: "",
  tags: new Set(),
  sort: "date-desc",
};

function clusterOf(tag) { return CLUSTERS[tag] || "mechanical"; }

function fmtDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
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

function sortRows(rows) {
  const s = [...rows];
  if (state.sort === "date-desc") s.sort((a, b) => b.created.localeCompare(a.created));
  else if (state.sort === "date-asc") s.sort((a, b) => a.created.localeCompare(b.created));
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

function cardHTML(a) {
  const tagHTML = a.tags.map(t => tagChipHTML(t, false)).join("") +
                   a.suggested.map(t => tagChipHTML(t, true)).join("");
  const quote = a.quote
    ? `<blockquote>&hellip;${escapeHTML(a.quote_prefix || "")}<mark>${escapeHTML(a.quote)}</mark>${escapeHTML(a.quote_suffix || "")}&hellip;</blockquote>`
    : "";
  const reply = a.reply ? '<span class="reply-badge">reply</span>' : "";
  return `<article class="card">
    <div class="meta">
      <span class="user">${escapeHTML(a.user)}</span>
      <span class="sep">·</span>
      <a href="${a.uri}" target="_blank" rel="noopener">${escapeHTML(a.chapter)}</a>
      <span class="sep">·</span>
      <span>${escapeHTML(a.group)}</span>
      <span class="sep">·</span>
      <span>${fmtDate(a.created)}</span>
      ${reply}
      <span class="sep">·</span>
      <a href="${a.link}" target="_blank" rel="noopener">View on Hypothesis &rarr;</a>
    </div>
    ${quote}
    <p class="comment">${escapeHTML(a.text)}</p>
    <div class="tags">${tagHTML}</div>
  </article>`;
}

function escapeHTML(s) {
  return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderStats() {
  const total = DATA.length;
  const tagged = DATA.filter(a => a.tags.length).length;
  const aiOnly = DATA.filter(a => !a.tags.length && a.suggested.length).length;
  const untagged = DATA.filter(a => !a.tags.length && !a.suggested.length).length;
  const readers = uniqueSorted(DATA.map(a => a.user)).length;
  const stats = [
    ["Annotations", total],
    ["Tagged", tagged],
    ["AI-suggested", aiOnly],
    ["Untagged", untagged],
    ["Readers", readers],
  ];
  document.getElementById("stats").innerHTML = stats.map(([label, n]) =>
    `<div class="stat"><span class="n">${n}</span><span class="label">${label}</span></div>`
  ).join("");
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

renderStats();
buildReaderFilters();
buildChapterFilter();
buildTagFilters();
render();
</script>
"""


if __name__ == "__main__":
    raise SystemExit(main())
