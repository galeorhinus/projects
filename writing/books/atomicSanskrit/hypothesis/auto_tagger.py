#!/usr/bin/env python3
"""auto_tagger.py -- classify annotations against taxonomy.json using
Claude, PATCH the resulting tags back to Hypothesis, and update the
local data/annotations.json snapshot to match.

Backstop philosophy: an annotation that already carries at least one
on-taxonomy tag is left alone (whether a reader typed it or a previous
run of this script added it) -- this script only fills gaps, it never
overrides a reader's own classification. That also makes re-running
this script safe and idempotent; it only ever spends API calls on
annotations that still need a verdict.

Ownership split (Hypothesis permission model, confirmed 2026-08-15
against https://web.hypothes.is/help/moderation-for-groups/): a
personal API token can only PATCH tags on annotations *its own account
authored*. Group membership grants read access to every member's
annotations but never write access to someone else's -- and there is
no moderation-API or paid-tier escape hatch; a group moderator can only
hide/unhide a flagged annotation. So:

  - annotations authored by this token's own account get tagged for
    real: PATCH to Hypothesis + write into "tags" in the local snapshot.
  - annotations authored by anyone else get a "suggested_tags" field in
    the local snapshot only -- never a PATCH attempt (it would always
    404). The dashboard can still show/filter on these; hypothes.is
    itself never will.

Usage:
    python3 auto_tagger.py              # tag everything that needs it
    python3 auto_tagger.py --dry-run    # show what would be tagged, write nothing
    python3 auto_tagger.py --limit 5    # only process the first 5 (testing)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from hypothesis_client import HypothesisClient, HypothesisError

HYPOTHESIS_DIR = Path(__file__).parent
DATA_PATH = HYPOTHESIS_DIR / "data" / "annotations.json"
TAXONOMY_PATH = HYPOTHESIS_DIR / "taxonomy.json"
ANTHROPIC_TOKEN_PATH = HYPOTHESIS_DIR / "anthropic_token.txt"

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
# Fast, cheap model -- this is a repetitive short-text classification
# task, not something that needs a frontier model's reasoning.
MODEL = "claude-haiku-4-5-20251001"


def load_anthropic_key() -> str:
    if not ANTHROPIC_TOKEN_PATH.exists() or not ANTHROPIC_TOKEN_PATH.read_text().strip():
        raise HypothesisError(
            f"No key at {ANTHROPIC_TOKEN_PATH}. Paste an Anthropic API key "
            f"(https://console.anthropic.com/settings/keys) into that file "
            f"as the only line -- see hypothesis/README.md."
        )
    return ANTHROPIC_TOKEN_PATH.read_text(encoding="utf-8").strip()


def build_prompt(taxonomy: dict[str, str], quote: str, text: str) -> str:
    tag_list = "\n".join(f"- {name}: {desc}" for name, desc in taxonomy.items())
    return f"""You are classifying a reader's annotation on a nonfiction book manuscript.
Choose 1 or 2 tags (rarely more than 2) from this exact list that best
describe the annotation. Respond with ONLY a JSON array of tag name
strings from the list below -- no other text, no explanation.

Tags:
{tag_list}

The passage the reader highlighted (may be empty for a note with no
selection):
\"\"\"{quote[:600]}\"\"\"

The reader's comment:
\"\"\"{text[:1000]}\"\"\"

JSON array of 1-2 tag names:"""


def classify(api_key: str, taxonomy: dict[str, str], quote: str, text: str) -> list[str]:
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 50,
        "messages": [{"role": "user", "content": build_prompt(taxonomy, quote, text)}],
    }).encode("utf-8")
    req = urllib.request.Request(ANTHROPIC_API_URL, data=body, method="POST")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", ANTHROPIC_VERSION)
    req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise HypothesisError(f"Anthropic API HTTP {e.code}: {detail[:300]}") from e

    reply = result["content"][0]["text"].strip()
    try:
        tags = json.loads(reply)
    except json.JSONDecodeError:
        # Occasionally the model wraps the array in a code fence despite
        # instructions; strip one layer of ``` and retry once before
        # giving up on this annotation.
        stripped = reply.strip("`").strip()
        if stripped.startswith("json"):
            stripped = stripped[4:].strip()
        tags = json.loads(stripped)

    return [t for t in tags if t in taxonomy]


def needs_tagging(annotation: dict, taxonomy: dict[str, str]) -> bool:
    # post_replies.py's own "resolved" tag marks a reply THIS pipeline
    # generated, not reader content -- it isn't in taxonomy.json (never
    # meant to be a reader-facing classification), so without this check
    # every such reply still looks untagged and gets a spurious reader
    # taxonomy tag piled on top (found live: a "resolved" reply got
    # tagged "question" too, since Haiku read "reply if it's still an
    # issue" as a question).
    if "resolved" in annotation.get("tags", []):
        return False
    if any(t in taxonomy for t in annotation.get("tags", [])):
        return False
    # A suggestion already on file (own-account or not) means a prior run
    # already spent the API call on this one -- skip it on re-runs too.
    if annotation.get("suggested_tags"):
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="classify and print, don't write")
    parser.add_argument("--limit", type=int, default=None, help="only process the first N candidates")
    args = parser.parse_args()

    if not DATA_PATH.exists():
        print(f"No {DATA_PATH} -- run pull_annotations.py first.", file=sys.stderr)
        return 1

    taxonomy = json.loads(TAXONOMY_PATH.read_text())["tags"]
    annotations = json.loads(DATA_PATH.read_text())

    try:
        api_key = load_anthropic_key()
    except HypothesisError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    hyp_client = None if args.dry_run else HypothesisClient()

    own_userid = None
    if not args.dry_run:
        try:
            own_userid = hyp_client.profile()["userid"]
        except (HypothesisError, KeyError) as e:
            print(f"ERROR fetching own profile: {e}", file=sys.stderr)
            return 1

    candidates = [a for a in annotations if needs_tagging(a, taxonomy) and (a["quote"] or a["text"])]
    if args.limit:
        candidates = candidates[: args.limit]

    print(f"{len(candidates)} annotation(s) need tagging"
          f"{' (dry run)' if args.dry_run else ''}.")

    tagged_count = 0
    suggested_count = 0
    for a in candidates:
        try:
            new_tags = classify(api_key, taxonomy, a["quote"], a["text"])
        except (HypothesisError, json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"  ⚠ {a['id']}: classification failed ({e})", file=sys.stderr)
            continue

        if not new_tags:
            print(f"  ? {a['id']} ({a['user']}): model returned no on-taxonomy tag")
            continue

        is_own = a.get("user_id") == own_userid
        preview = f"{a['user']} / {a['group_name']} / {a['uri'].rsplit('/', 2)[-2] or a['uri']}"

        if args.dry_run:
            print(f"  + {new_tags} -> {a['id']} ({preview})")
            continue

        if is_own:
            merged = sorted(set(a["tags"]) | set(new_tags))
            try:
                hyp_client.update_tags(a["id"], merged)
            except HypothesisError as e:
                print(f"  ⚠ {a['id']} ({preview}): failed to PATCH Hypothesis: {e}", file=sys.stderr)
                continue
            a["tags"] = merged
            tagged_count += 1
            print(f"  + {new_tags} -> {a['id']} ({preview}) [tagged on Hypothesis]")
            time.sleep(0.3)  # courtesy delay, not a documented rate limit
        else:
            # Not our annotation -- Hypothesis will never let this token
            # PATCH it (see module docstring), so don't attempt the call.
            # Record the suggestion locally instead.
            a["suggested_tags"] = sorted(set(a.get("suggested_tags", [])) | set(new_tags))
            suggested_count += 1
            print(f"  ~ {new_tags} -> {a['id']} ({preview}) [suggested only, not our annotation]")

    if not args.dry_run and (tagged_count or suggested_count):
        DATA_PATH.write_text(json.dumps(annotations, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nTagged {tagged_count} annotation(s) on Hypothesis; "
              f"recorded {suggested_count} local-only suggestion(s); snapshot updated.")
    elif args.dry_run:
        print("\nDry run -- nothing written to Hypothesis or the local snapshot.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
