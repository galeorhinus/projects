# Command reference

Quick-reference for every script in this directory. All run from
`hypothesis/`:

```
cd /Users/paragtope/projects/writing/books/atomicSanskrit/hypothesis
```

One-time setup (tokens, etc.) is in `README.md`, not here — this file
is just the commands.

## Full refresh, in order

```
python3 pull_annotations.py && python3 auto_tagger.py && \
  python3 build_dashboard.py && python3 digest_send.py
```

On amrut this is split across two cron cadences instead of running all
together: `refresh_dashboard.sh` (pull + tag + dashboard) every 15
minutes, `cron_gate.sh` (digest only) at 8am/6pm Chicago. You don't
need to run the full sequence by hand unless you're testing a change
or want everything forced to catch up immediately -- the dashboard's
own "Refresh now" button does the pull+tag+rebuild part on demand too.

---

## pull_annotations.py -- fetch everything from Hypothesis

```
python3 pull_annotations.py
```

No flags. Always does a full pull across every group you're in, writes
`data/annotations.json` + `data/groups.json`. Re-run any time you want
current data before running one of the other scripts.

---

## auto_tagger.py -- tag whatever's untagged

```
python3 auto_tagger.py                 # tag everything that needs it
python3 auto_tagger.py --dry-run       # classify and print, write nothing
python3 auto_tagger.py --limit 5       # only process the first 5 (testing)
```

Idempotent -- only processes annotations without an on-taxonomy tag
(real tag or `suggested_tags`), so re-running costs nothing extra for
ones already handled. Your own annotations get a real tag PATCHed to
Hypothesis; everyone else's get `suggested_tags` locally only (can't
write to an annotation you didn't author).

---

## build_dashboard.py -- render "Reader Margins"

```
python3 build_dashboard.py                                          # hypothesis/dashboard.html only
python3 build_dashboard.py --install /var/www/as/private/dashboard/index.html  # amrut only -- also installs to the live site
```

After running with no `--install`, publish `dashboard.html` as a Claude
Artifact by asking Claude to republish it (same URL each time). The
`--install` form (used by `run_pipeline.sh` on amrut) needs no manual
step -- it's already live at
<https://secondshanti.org/as/private/dashboard/> (owner-only login).

---

## digest_send.py -- email what's new

```
python3 digest_send.py                 # send if anything's new since last digest
python3 digest_send.py --dry-run       # write digest_preview.html, send nothing
python3 digest_send.py --force         # send even if nothing is new
python3 digest_send.py --to other@example.com  # override recipient
```

Silent no-op when nothing's new -- safe to run as often as you like.
`--dry-run` writes `digest_preview.html` locally so you can open it in
a browser without sending anything or advancing the "already reported"
state.

---

## resolve_check.py -- has this annotation already been fixed?

```
python3 resolve_check.py                        # Tier 0/1 only (free), full report
python3 resolve_check.py --llm                   # + Tier 2 (Haiku, ambiguous cases only)
python3 resolve_check.py --chapter preface       # restrict to one chapter
python3 resolve_check.py --show still_open       # print detail for one status instead of the default (likely_resolved)
```

`--show` choices: `still_open`, `likely_resolved`, `ambiguous`,
`no_quote`, `no_source`, `low_confidence`. Reads the *current* local
`.md` files on disk (including uncommitted edits) -- not a git commit,
not the deployed site. Draft-only: writes `data/resolve_report.json`,
never touches Hypothesis. Run `--llm` any time you want the `ambiguous`
bucket re-judged; it's cheap (Haiku, only the leftovers).

---

## post_replies.py -- reply to the resolved ones

```
python3 post_replies.py                       # draft only -> data/draft_replies.md, posts nothing
python3 post_replies.py --only text_match      # draft, restricted to non-LLM-judged cases
python3 post_replies.py --only llm             # draft, restricted to LLM-judged cases
python3 post_replies.py --post --limit 5       # POST 5 replies for real -- spot-check before going wide
python3 post_replies.py --post                 # POST all remaining candidates for real
```

Always run `resolve_check.py` first (this reads its report, doesn't
re-classify). Every `--post` run skips annotations already replied to
(tracked in `replied_state.json`), so it's safe to re-run after
resolve_check.py finds new candidates -- never double-replies. Review
`data/draft_replies.md` before any `--post` run without `--limit`.

---

## Typical workflow when you've made manuscript edits and want to catch up

```
python3 pull_annotations.py
python3 auto_tagger.py
python3 resolve_check.py --llm
python3 post_replies.py            # review data/draft_replies.md
python3 post_replies.py --post --limit 5   # spot-check live
python3 post_replies.py --post             # the rest, once you're happy
```
