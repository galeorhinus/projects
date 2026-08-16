#!/usr/bin/env python3
"""resolve_check.py -- check whether reader annotations have already
been addressed by later manuscript edits, without needing an LLM for
the clear-cut cases.

The idea: an annotation carries the exact text the reader highlighted
(Hypothesis's own TextQuoteSelector). If that text no longer appears
anywhere in the chapter's *current* source -- not "was it edited in
commit X," just "does it exist right now" -- the flagged passage is
gone, which is strong evidence the concern was addressed. Checking
"the one commit that fixed it" turned out to be the wrong frame: a
manual audit (2026-08-16) found a single flagged word rewritten across
half a dozen separate commits over two months before it was finally
dropped -- there's no one commit to point to, but there IS a clean
current-state answer.

Two zero-API-cost tiers:

  Tier 0 (exact) -- after normalizing away Markdown decoration and
  pandoc's smart-typography substitutions, does the quote appear
  verbatim in the current chapter source? If yes: definitely still
  open, skip. If no: fall through to Tier 1.

  Tier 1 (fuzzy) -- find the chapter paragraph the quote best overlaps
  with (longest-common-substring ratio, not a whole-paragraph diff --
  a quote is much shorter than the paragraph it sits in) and classify
  by how much of the quote survives intact:
    >= FUZZY_STILL_OPEN   -> still open in substance, just reworded
    <  FUZZY_LIKELY_GONE  -> the passage is gone; likely resolved
    in between            -> ambiguous, needs a human (or later, an
                             LLM Tier 2 -- not built yet; Tier 0/1
                             alone resolves most of the clear cases
                             for free, so that tier is deferred until
                             there's a real backlog of ambiguous ones)

This script is draft-only: it classifies and writes a report, it does
not post replies or touch tags. See draft_replies() in this module for
the reply text it WOULD post -- reviewed by hand before any live-post
script gets built on top of this.

Usage:
    python3 resolve_check.py                 # full report to stdout + JSON
    python3 resolve_check.py --chapter preface   # one chapter only
    python3 resolve_check.py --show likely_resolved   # filter the printed detail
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HYPOTHESIS_DIR = Path(__file__).parent
BOOK_DIR = HYPOTHESIS_DIR.parent
DATA_PATH = HYPOTHESIS_DIR / "data" / "annotations.json"
REPORT_PATH = HYPOTHESIS_DIR / "data" / "resolve_report.json"
ANTHROPIC_TOKEN_PATH = HYPOTHESIS_DIR / "anthropic_token.txt"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
MODEL = "claude-haiku-4-5-20251001"  # same cheap model auto_tagger.py uses

sys.path.insert(0, str(BOOK_DIR))
from build_html import collect_content_entries  # noqa: E402

# Tier 1 thresholds -- longest-matching-run length / len(anchor span).
FUZZY_STILL_OPEN = 0.70
FUZZY_LIKELY_GONE = 0.30

# Below this length there's no usable context at all (empty prefix AND
# suffix, e.g. a quote that opens or closes its whole document) -- too
# little signal either way, so these get a distinct low-confidence
# status rather than a guess.
MIN_ANCHOR_LEN = 15

_MD_EMPHASIS_RE = re.compile(r"\*{1,3}")
_NOTE_MARKER_RE = re.compile(r"\[NOTE:\s*[\w-]+\]")
# Leading list markers -- "- item", "+ item", "1. item" -- at the start
# of a line. Must run BEFORE whitespace collapse (needs real newlines
# for ^ to anchor on) and independently of _MD_EMPHASIS_RE: an
# asterisk-bulleted "* item" already loses its marker to the emphasis
# strip, but a dash/plus/numbered marker never did. Found live
# 2026-08-16: a plain-line passage got reformatted as a Markdown bullet
# list with no wording change at all, and the unstripped "- " at every
# line start broke the exact match and capped the fuzzy ratio at
# roughly 1/(number of bullets) -- one line's worth of overlap out of
# five -- pushing a genuinely-unchanged passage into likely_resolved.
_LIST_MARKER_RE = re.compile(r"(?m)^[ \t]*(?:[-+]|\d+\.)\s+")
_WS_RE = re.compile(r"\s+")
_SMART_QUOTES = str.maketrans({
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...",
})


def normalize(text: str) -> str:
    """Approximate what a reader actually SAW in the rendered page from
    raw Markdown source: strip list markers, emphasis markers, and
    endnote stubs, collapse pandoc's smart-typography substitutions
    back to plain ASCII equivalents (both source and quote get the same
    treatment, so it doesn't matter which direction pandoc's
    substitution ran), collapse whitespace."""
    text = _NOTE_MARKER_RE.sub("", text)
    text = _LIST_MARKER_RE.sub("", text)
    text = _MD_EMPHASIS_RE.sub("", text)
    text = text.translate(_SMART_QUOTES)
    text = _WS_RE.sub(" ", text)
    return text.strip()


def slug_to_path() -> dict[str, Path]:
    entries = collect_content_entries()
    return {e["slug"]: BOOK_DIR / e["file"] for e in entries}


def chapter_slug(uri: str) -> str:
    return uri.rstrip("/").rsplit("/", 1)[-1]


def best_paragraph_match(quote: str, doc_text: str) -> tuple[float, str]:
    """Longest-common-substring ratio against each paragraph, returns
    (best_ratio, best_paragraph). A quote is short; comparing it to a
    whole chapter with SequenceMatcher.ratio() would always look like a
    bad match regardless of whether the quote survives intact somewhere
    inside it -- ratio() measures overall sequence similarity of the
    two FULL strings, not substring containment. Finding the longest
    matching run within each paragraph and dividing by the quote's own
    length answers the actual question: how much of what the reader
    highlighted still exists, contiguously, anywhere in the chapter."""
    if not quote:
        return 0.0, ""
    paragraphs = [p for p in re.split(r"\n\s*\n", doc_text) if p.strip()]
    best_ratio, best_para = 0.0, ""
    for para in paragraphs:
        para_norm = normalize(para)
        sm = difflib.SequenceMatcher(None, para_norm, quote, autojunk=False)
        match = sm.find_longest_match(0, len(para_norm), 0, len(quote))
        ratio = match.size / len(quote)
        if ratio > best_ratio:
            best_ratio, best_para = ratio, para
    return best_ratio, best_para


def classify_one(quote: str, prefix: str, suffix: str, doc_text: str) -> dict:
    """The anchor is prefix+quote+suffix, not the bare quote. A bare
    quote alone is unreliable in BOTH directions for short/common
    words: found live 2026-08-16 that "sonomer" (7 chars, genuinely
    gone) scored 0.571 against an unrelated paragraph under fuzzy
    matching -- pure chance character overlap -- while common short
    words like "why" or "gray" trivially exist SOMEWHERE in any
    chapter-length document regardless of whether the specific flagged
    sentence changed, so a bare-quote exact-match "still open" verdict
    for those is just as unreliable. Hypothesis's own prefix/suffix
    (already pulled for the digest email's quote-in-context display)
    anchor the check to the specific sentence the reader actually
    flagged, which fixes both directions at once and removes the need
    for a separate short-quote special case."""
    if not quote:
        return {"status": "no_quote", "ratio": None, "matched_paragraph": None}

    anchor_norm = normalize((prefix or "") + quote + (suffix or ""))
    doc_norm = normalize(doc_text)

    if len(anchor_norm) < MIN_ANCHOR_LEN:
        return {"status": "low_confidence", "ratio": None, "matched_paragraph": None}

    if anchor_norm in doc_norm:
        return {"status": "still_open", "ratio": 1.0, "matched_paragraph": None}

    ratio, para = best_paragraph_match(anchor_norm, doc_text)
    if ratio >= FUZZY_STILL_OPEN:
        status = "still_open"
    elif ratio < FUZZY_LIKELY_GONE:
        status = "likely_resolved"
    else:
        status = "ambiguous"
    return {"status": status, "ratio": round(ratio, 3), "matched_paragraph": para.strip() if para else None}


def draft_reply_text(annotation: dict, result: dict) -> str:
    """What a reply WOULD say -- reviewed by hand before any live post.
    Kept honest about the mechanism: text-match verdicts say the flagged
    passage is gone, not that the specific concern was addressed; the
    LLM-judged variant says a model made that call, not a person."""
    if result.get("resolved_by") == "llm":
        return (
            "This looks like it may already be addressed in the current draft -- "
            "an automated check compared your comment against the revised passage "
            "and judged it likely resolved, but a person hasn't confirmed that. "
            "Reply if it's still an issue."
        )
    return (
        "Looks like this has been addressed in a later revision -- the passage you "
        "flagged no longer appears in the current draft. Flagging here in case it "
        "was missed rather than intentionally reworded; reply if it's still an issue."
    )


def load_anthropic_key() -> str:
    if not ANTHROPIC_TOKEN_PATH.exists() or not ANTHROPIC_TOKEN_PATH.read_text().strip():
        raise RuntimeError(f"No Anthropic key at {ANTHROPIC_TOKEN_PATH} -- see hypothesis/README.md.")
    return ANTHROPIC_TOKEN_PATH.read_text(encoding="utf-8").strip()


def llm_judge(api_key: str, quote: str, comment: str, matched_paragraph: str) -> str:
    """One Haiku call for one ambiguous annotation. Returns 'resolved',
    'still_open', or 'unclear' -- called only on the Tier 0/1 leftovers,
    so this is a small, bounded number of calls, not one per annotation."""
    prompt = f"""You are checking whether a manuscript editor's later revision addressed a
reader's comment on a work-in-progress nonfiction book.

The reader originally highlighted this passage:
\"\"\"{quote[:500]}\"\"\"

The reader's comment on it:
\"\"\"{comment[:500]}\"\"\"

The closest-matching passage in the CURRENT (revised) manuscript is:
\"\"\"{matched_paragraph[:800]}\"\"\"

Has the reader's specific concern been addressed by the current passage? A typo/
rewording concern is addressed if the current text no longer has that problem, even
if the surrounding sentence changed for other reasons too. A substantive question or
factual concern is addressed only if the current text actually resolves it, not
merely if the sentence was reworded.

Answer with exactly one word: resolved, still_open, or unclear."""

    body = json.dumps({
        "model": MODEL,
        "max_tokens": 10,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = urllib.request.Request(ANTHROPIC_API_URL, data=body, method="POST")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", ANTHROPIC_VERSION)
    req.add_header("content-type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    reply = result["content"][0]["text"].strip().lower()
    for word in ("resolved", "still_open", "unclear"):
        if word in reply:
            return word
    return "unclear"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", default=None, help="restrict to one chapter slug")
    parser.add_argument("--show", default=None,
                         choices=["still_open", "likely_resolved", "ambiguous", "no_quote", "no_source", "low_confidence"],
                         help="print full detail for just this status")
    parser.add_argument("--llm", action="store_true",
                         help="run Tier 2 (one Haiku call per ambiguous annotation) to resolve the leftovers")
    args = parser.parse_args()

    if not DATA_PATH.exists():
        print(f"No {DATA_PATH} -- run pull_annotations.py first.", file=sys.stderr)
        return 1

    annotations = json.loads(DATA_PATH.read_text())
    slug_map = slug_to_path()

    results = []
    doc_cache: dict[str, str] = {}

    for a in annotations:
        slug = chapter_slug(a["uri"])
        if args.chapter and slug != args.chapter:
            continue

        path = slug_map.get(slug)
        if path is None:
            results.append({**a, "slug": slug, "status": "no_source", "ratio": None, "matched_paragraph": None})
            continue
        if not path.exists():
            results.append({**a, "slug": slug, "status": "no_source", "ratio": None, "matched_paragraph": None})
            continue

        if slug not in doc_cache:
            doc_cache[slug] = path.read_text(encoding="utf-8")
        doc_text = doc_cache[slug]

        classification = classify_one(
            a.get("quote", ""), a.get("quote_prefix", ""), a.get("quote_suffix", ""), doc_text
        )
        results.append({**a, "slug": slug, **classification})

    if args.llm:
        ambiguous = [r for r in results if r["status"] == "ambiguous"]
        if ambiguous:
            try:
                api_key = load_anthropic_key()
            except RuntimeError as e:
                print(f"ERROR: {e}", file=sys.stderr)
                return 1
            print(f"Tier 2: judging {len(ambiguous)} ambiguous annotation(s) via {MODEL}...")
            for r in ambiguous:
                try:
                    verdict = llm_judge(api_key, r["quote"], r["text"], r.get("matched_paragraph") or "")
                except (urllib.error.HTTPError, urllib.error.URLError, KeyError, IndexError) as e:
                    print(f"  ⚠ {r['id']}: LLM call failed ({e})", file=sys.stderr)
                    continue
                if verdict == "resolved":
                    r["status"] = "likely_resolved"
                    r["resolved_by"] = "llm"
                elif verdict == "still_open":
                    r["status"] = "still_open"
                    r["resolved_by"] = "llm"
                # "unclear" -- leave as ambiguous, no change
                time.sleep(0.3)

    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    tier_label = "Tier 0 (exact) + Tier 1 (fuzzy)" + (" + Tier 2 (LLM)" if args.llm else "")
    print(f"Resolution check -- {tier_label}, draft-only, nothing posted.\n")
    for status in ["still_open", "likely_resolved", "ambiguous", "low_confidence", "no_quote", "no_source"]:
        print(f"  {status:16s} {counts.get(status, 0)}")
    print()

    show = args.show or "likely_resolved"
    print(f"--- Detail: {show} ---\n")
    for r in results:
        if r["status"] != show:
            continue
        preview = f"{r['user']} / {r['slug']} / {r['created'][:10]}"
        print(f"[{r.get('ratio')}] {preview}")
        print(f"  quote:   {r['quote'][:140]!r}")
        print(f"  comment: {r['text'][:140]!r}")
        if r.get("matched_paragraph"):
            print(f"  closest match now: {r['matched_paragraph'][:160]!r}")
        if r["status"] == "likely_resolved":
            print(f"  draft reply: {draft_reply_text(r, r)}")
        print()

    REPORT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Full report -> {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
