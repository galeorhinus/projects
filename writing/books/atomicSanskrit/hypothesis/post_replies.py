#!/usr/bin/env python3
"""post_replies.py -- reply to reader annotations resolve_check.py
classified as likely_resolved, and tag each reply "resolved".

Draft-first, same backstop philosophy as auto_tagger.py: default run
writes what WOULD be posted to data/draft_replies.md for you to skim,
touches nothing on Hypothesis. Only --post actually creates replies,
and only ever once per annotation -- posted parent IDs are tracked in
replied_state.json so a re-run (e.g. the next day's cron pass, once
this is wired into run_pipeline.sh) never double-replies.

A reply is a NEW annotation referencing the parent (POST with
"references": [parent_id]), not a PATCH to the parent -- so this works
on every annotation regardless of who authored it, unlike auto_tagger's
tag-PATCHing. See hypothesis_client.create_reply()'s docstring.

Usage:
    python3 post_replies.py                    # draft only, write .md + .json
    python3 post_replies.py --only text_match   # skip LLM-judged ones
    python3 post_replies.py --post              # actually post (after review!)
    python3 post_replies.py --post --limit 5    # post just a few, to spot-check live
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from hypothesis_client import HypothesisClient, HypothesisError

HYPOTHESIS_DIR = Path(__file__).parent
REPORT_PATH = HYPOTHESIS_DIR / "data" / "resolve_report.json"
DRAFT_MD_PATH = HYPOTHESIS_DIR / "data" / "draft_replies.md"
STATE_PATH = HYPOTHESIS_DIR / "replied_state.json"
REPLY_TAG = "resolved"


def load_state() -> set[str]:
    if not STATE_PATH.exists():
        return set()
    return set(json.loads(STATE_PATH.read_text()))


def save_state(replied_ids: set[str]) -> None:
    STATE_PATH.write_text(json.dumps(sorted(replied_ids), indent=2), encoding="utf-8")


def reply_text_for(r: dict) -> str:
    if r.get("resolved_by") == "llm":
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


def write_draft_markdown(candidates: list[dict]) -> None:
    lines = [f"# Draft replies -- {len(candidates)} candidate(s)\n",
             "Nothing here has been posted. Review, then `python3 post_replies.py --post`.\n"]
    for r in candidates:
        mechanism = "LLM-judged" if r.get("resolved_by") == "llm" else "text-match"
        lines.append(f"## {r['user']} / {r['slug']} / {r['created'][:10]}  ({mechanism})")
        lines.append(f"- annotation: {r['uri'].rstrip('/')}/#annotations:{r['id']}")
        lines.append(f"- quote: `{r['quote'][:200]}`")
        lines.append(f"- comment: {r['text'][:300]}")
        if r.get("matched_paragraph"):
            lines.append(f"- current passage: {r['matched_paragraph'][:300]}")
        lines.append(f"- **draft reply:** {reply_text_for(r)}")
        lines.append("")
    DRAFT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=["text_match", "llm"], default=None,
                         help="restrict to one resolution mechanism")
    parser.add_argument("--post", action="store_true", help="actually post replies (default: draft only)")
    parser.add_argument("--limit", type=int, default=None, help="cap how many to post, for spot-checking")
    args = parser.parse_args()

    if not REPORT_PATH.exists():
        print(f"No {REPORT_PATH} -- run resolve_check.py first.", file=sys.stderr)
        return 1

    report = json.loads(REPORT_PATH.read_text())
    already_replied = load_state()

    candidates = [r for r in report if r["status"] == "likely_resolved" and r["id"] not in already_replied]
    if args.only == "text_match":
        candidates = [r for r in candidates if r.get("resolved_by") != "llm"]
    elif args.only == "llm":
        candidates = [r for r in candidates if r.get("resolved_by") == "llm"]

    if args.post and args.limit:
        candidates = candidates[: args.limit]

    print(f"{len(candidates)} candidate(s) ({len(already_replied)} already replied to, skipped).")

    if not args.post:
        write_draft_markdown(candidates)
        print(f"Draft written -> {DRAFT_MD_PATH}")
        print("Nothing posted. Review the draft, then re-run with --post.")
        return 0

    try:
        client = HypothesisClient()
    except HypothesisError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    posted = 0
    for r in candidates:
        try:
            client.create_reply(r, reply_text_for(r), tags=[REPLY_TAG])
        except HypothesisError as e:
            print(f"  ⚠ {r['id']} ({r['user']}/{r['slug']}): failed to post ({e})", file=sys.stderr)
            continue
        already_replied.add(r["id"])
        posted += 1
        print(f"  + replied -> {r['id']} ({r['user']}/{r['slug']})")
        time.sleep(0.3)

    save_state(already_replied)
    print(f"\nPosted {posted} repl(y/ies); state updated -> {STATE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
