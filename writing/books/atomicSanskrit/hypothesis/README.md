# Hypothesis annotation tooling

Consolidates reader annotations across all your Hypothesis reading groups
into one filterable view, auto-tags them against a published taxonomy, and
can send a digest email of what's new. Pure standard library -- no `pip
install` needed for anything in this directory (matches `server/`'s own
convention).

## One-time setup

1. **Get a personal API token**: <https://hypothes.is/account/developer>.
2. **Save it locally** -- paste it as the only line in `hypothesis/token.txt`
   (create the file yourself; it's gitignored and must never be committed
   or pasted into a chat/issue/commit message).
3. **For auto-tagging**, get an Anthropic API key from
   <https://console.anthropic.com/settings/keys> (a separate billing pool
   from any claude.ai/Claude Code subscription usage credit -- those can't
   fund direct API calls) and paste it as the only line in
   `hypothesis/anthropic_token.txt`.
4. **For the digest email**, a Gmail app password for the sending account
   (<https://myaccount.google.com/apppasswords>) pasted as the only line in
   `hypothesis/smtp_app_password.txt`. `server/request_access.py` already
   has one for the same account on amrut, at
   `/etc/secondshanti/smtp-app-password` -- reuse that value if you have it
   rather than minting a second app password.
5. You're done -- the scripts read each secret from its own gitignored file.

## The pipeline

```
pull_annotations.py   -- fetch every annotation from every group you're
                          in, normalize, write to data/annotations.json
auto_tagger.py         -- read taxonomy.json, tag anything untagged (or
                          off-taxonomy) via the LLM, PATCH tags back to
                          Hypothesis and to the local snapshot
build_dashboard.py     -- render data/annotations.json as a filterable,
                          sortable static HTML page. No args: writes
                          hypothesis/dashboard.html for publishing by
                          hand as a Claude Artifact. --install PATH:
                          also writes to PATH -- what run_pipeline.sh
                          uses to self-publish at
                          secondshanti.org/as/private/dashboard/
digest_send.py         -- email a summary of annotations new or updated
                          since the last digest, via the same Gmail SMTP
                          app-password setup server/request_access.py uses
```

Run `pull_annotations.py` first any time you want a fresh snapshot; the
other three scripts all read from `data/annotations.json` rather than
hitting the API themselves (except `auto_tagger.py`, which also writes
back). Full refresh, in order:

```
python3 pull_annotations.py && python3 auto_tagger.py && \
  python3 build_dashboard.py && python3 digest_send.py
```

**Ownership split in `auto_tagger.py`.** Hypothesis's write permission on
an annotation belongs to its author only -- group membership grants read
access to every member's annotations but never write access to someone
else's, and there's no moderation-API or paid-tier escape hatch (a group
moderator can only hide/unhide a flagged annotation). So the tagger PATCHes
real tags to Hypothesis only for annotations your own account authored;
everyone else's untagged annotations get a `suggested_tags` field in the
local snapshot instead -- visible in the dashboard, marked distinctly, but
never written to hypothes.is. Tag-autocomplete in the Hypothesis client is
also purely per-browser `localStorage`, never synced or shared -- so even
your own successfully-applied tags won't appear as suggestions for other
readers when they annotate.

**`digest_send.py`** tracks the newest `updated` timestamp it has already
reported in `digest_state.json`, so a reader editing an old annotation (or
`auto_tagger.py` adding tags to one) counts as "new" for the next digest,
not just brand-new annotations. Running it with nothing new since the last
send is a silent no-op by default (`--force` to send a "still quiet"
check-in anyway; `--dry-run` to preview without sending or advancing the
state file).

## Scheduled runs (amrut)

Two separate cadences, added 2026-08-17 so the dashboard can be a
near-real-time default view instead of only refreshing twice a day:

```
refresh_dashboard.sh      -- pull + tag + rebuild the dashboard.
                             Every 15 minutes via plain cron (no
                             gating needed -- "every 15 minutes" has
                             no timezone dependency, unlike a fixed
                             wall-clock time).
refresh_dashboard_fast.sh  -- pull + rebuild ONLY, no tagging. Not on
                             cron -- this is what the dashboard's own
                             "Refresh now" button calls (see below).
cron_gate.sh               -- digest_send.py only. Runs every minute
                             but only actually fires at 8am/6pm
                             Chicago (see "Why not a TZ= line" below)
                             -- an email notification every 15
                             minutes would be spam, not a digest.
run_pipeline.sh             -- the old all-in-one sequence (pull + tag
                             + dashboard + digest). Not cron's entry
                             point anymore; kept as a manual
                             convenience for testing or forcing
                             everything caught up by hand in one call.
```

The dashboard's own "Refresh now" button (`dashboard_api.py`'s
`/refresh` route) triggers `refresh_dashboard_fast.sh` on demand, for
checking right now instead of waiting up to 15 minutes. Deliberately
the FAST script, not the full `refresh_dashboard.sh` -- confirmed live
2026-08-17: when there's a tagging backlog, `auto_tagger.py`'s
per-annotation LLM calls could push a full refresh past a minute,
which made the button feel erratic, and a long-running `fetch()` is
fragile on top of that (a backgrounded tab or a locked phone can kill
it silently -- no error, no reload, which read exactly like "the
button has no callback"). Tagging still happens reliably on its own
15-minute cycle regardless of whether anyone clicks the button; a
manual refresh just shows new comments untagged until that next cycle
catches up.

**The live dashboard**: <https://secondshanti.org/as/private/dashboard/>
(owner-only). It sits inside `/as/private/*`'s Google-OAuth gate but adds
an *extra* check in the Caddyfile's loopback `:18080` block -- the request
must carry `X-Forwarded-Email: rhinusgaleo@gmail.com` (forwarded by
oauth2-proxy to the upstream after a successful login --
`--pass-user-headers`, on by default in reverse-proxy mode) or it 404s.
This matters because `/as/private/*` alone shares its whitelist with
every invited reader (`authenticated-emails.txt`) -- without the extra
check, everyone who can read the book could also see everyone else's
candid annotations. See the Caddyfile's own comments at the
`@dashboard_notowner` matcher. (`X-Auth-Request-Email` is a *different*
header oauth2-proxy sends back to the *client*, for nginx's
`auth_request` pattern -- not what reaches this upstream. First version
of this check used that header by mistake and 404'd for the owner too.)

Publishing `dashboard.html` as a Claude Artifact ("Reader Margins")
remains available too, run by hand from a Claude Code session whenever a
snapshot is worth sharing or viewing outside this flow -- the two publish
paths don't conflict, `build_dashboard.py --install` just adds a second
output alongside the usual `hypothesis/dashboard.html`.

Crontab on amrut (`crontab -e` as `ubuntu`):

```
*/15 * * * * /home/ubuntu/projects/writing/books/atomicSanskrit/hypothesis/refresh_dashboard.sh >> /home/ubuntu/projects/writing/books/atomicSanskrit/hypothesis/cron.log 2>&1
* * * * * /home/ubuntu/projects/writing/books/atomicSanskrit/hypothesis/cron_gate.sh >> /home/ubuntu/projects/writing/books/atomicSanskrit/hypothesis/cron.log 2>&1
```

**Why not a `TZ=` line + `0 8,18 * * *`, the obvious approach?**
Confirmed broken live 2026-08-16: amrut's `cron` package (Ubuntu's stock
Debian/Vixie-derived `cron`, not `cronie`) only exports a crontab's `TZ=`
line into the *job's own environment* -- it does **not** use it to
interpret the *schedule*. The daemon matches `0 8,18 * * *` against the
system's own timezone (`Etc/UTC` on amrut, per `timedatectl`), so that
config actually fired at 8am/6pm UTC = 3am/1pm Chicago, hours before
the "8am" the user expected and while they were asleep. `cron_gate.sh`
checks real Chicago wall time via `TZ=America/Chicago date +%H%M` (a
plain `date` invocation, unlike cron's scheduler, DOES honor an inline
`TZ=` and re-reads tzdata every call, so this stays correct across DST
without a hardcoded UTC offset) and only execs `digest_send.py` in the
exact target minute -- silent, no `cron.log` output, every other
minute.

The three secret files (`token.txt`, `anthropic_token.txt`,
`smtp_app_password.txt`) live only on amrut and this machine -- never
committed, copied by hand (`scp` / server-side `install`) whenever a new
machine needs them. `cron.log` is local runtime output, not source --
gitignored alongside the secrets and data.

## The TODO queue

Each card on the dashboard has a private "📌 Add to TODO" box, separate
from the reply composer -- a personal task note ("check this reference,
expand Ch3"), never posted to Hypothesis, never visible to readers.
Saved to `hypothesis/data/todo_queue.json` on amrut (gitignored, same
privacy posture as the rest of `data/`).

**That file never leaves amrut on its own** -- this project's convention
is amrut only ever `git pull`s, never pushes, so there's no automatic
path from that queue into `working/10_active/as_todo.md` on this
machine. Reconciling it is a standing task for the start of the next
session working on the manuscript: `ssh amrut cat
~/projects/writing/books/atomicSanskrit/hypothesis/data/todo_queue.json`,
fold each entry into `as_todo.md` with appropriate priority and a link
back to the annotation, then clear the queue (`echo '[]' | ssh amrut
'cat > ~/projects/writing/books/atomicSanskrit/hypothesis/data/todo_queue.json'`)
so entries aren't re-added next time.

Each card also has a "📋 Copy" button -- copies a single markdown TODO
line to the clipboard immediately, no queue involved, for pasting into
`as_todo.md` by hand right away instead of waiting for the next
session's reconciliation.

## The tag taxonomy

`taxonomy.json` is the published vocabulary. Hypothesis has no group-level
controlled tag list, so this is a convention, not a technical constraint --
tell readers what's in it (in the invite email / reading instructions) and
let `auto_tagger.py` backstop whoever doesn't tag or tags off-list. Edit
the file any time; the tagger picks up changes on its next run.

## Privacy

`data/*.json`, `token.txt`, `anthropic_token.txt`, `smtp_app_password.txt`,
`dashboard.html`, and `digest_state.json` are all gitignored. Annotation
content is readers' candid feedback -- treat it the same as
`server/invite_status.json`: never committed, machine-local only.
`dashboard.html` is published as a Claude Artifact for personal triage
(private by default, not indexed) rather than committed or hosted publicly.
