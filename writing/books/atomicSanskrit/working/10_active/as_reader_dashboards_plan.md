# Reader Dashboards — Plan

**Status:** Active
**Canonical:** Yes
**Owner:** Shared
**Next action:** Build phase 1 (generator + service + gate); nav and digest follow
**Last reviewed:** 2026-08-19

Design settled in conversation 2026-08-19. Extends the existing owner-only
"Reader Margins" dashboard (`hypothesis/build_dashboard.py`) so every invited
reader gets their own view of their group's annotations.

---

## 1. Purpose

A reader currently has no way to see what became of their annotations. Hypothesis
shows them in the sidebar of whichever page they are on, one page at a time, with
no consolidated view and no indication of whether the author has responded. The
one question a reader actually has — **did the author read this, and what did he
say?** — is the question Hypothesis answers worst.

The reader dashboard answers exactly that and nothing more. It is a **record**,
not a workspace: here is everything you flagged, here is what came back, click
through to continue the conversation where it lives.

This is deliberately *not* a smaller copy of the owner dashboard. That one is a
**work queue** — hero stat "55 Unresolved", urgency sorting, reply composer on
every card. The reader's question is different, so the instrument is different.

---

## 2. Decisions

| Question | Decision |
|---|---|
| URL | **One shared URL**, `/as/private/dashboard/`. No slug. |
| Who resolves the reader | A service reading `X-Forwarded-Email` |
| Filtering | By **group id** — partners in a shared group see each other's notes. A reader may hold several groups (`groups` array) and sees the union |
| Own notes | **Marked visually**; hero stat counts the reader's own |
| Reply composer | **Removed.** Deep-link to Hypothesis instead |
| Lookup key | `invite_status.json` `locked_email`, roster email as fallback |
| Rebuild | Piggyback the existing 15-minute cycle; show an "as of" stamp |
| Nav | Swap Essays → Dashboard on **gated templates only** |
| No-group readers | Graceful "not in a reading group yet" page, never a 404 |
| Digest | Only to readers with activity |
| Owner preview | `?as=<slug>`, honored only for the owner |

---

## 3. Access control

`/as/private/*` is open to **every whitelisted reader**, so the dashboard cannot
be plain static files behind one matcher — that is what the current owner-only
`@dashboard_notowner` check exists to handle, and it hardcodes a single email.

A shared URL resolved by a service is what makes this safe:

```
GET /as/private/dashboard/
  X-Forwarded-Email: <set by oauth2-proxy after login>

  owner            -> owner dashboard (existing behaviour, unchanged)
  known reader     -> that reader's dashboard
  whitelisted, but
  no roster entry  -> "not in a reading group yet" page
```

**There is no URL that returns another reader's data.** Nothing to guess, nothing
to type, no per-reader matcher, and adding a reader is a roster entry with no
Caddyfile change. That property is the main reason for the shared URL and should
not be traded away later without a replacement.

**Lookup order.** `locked_email` from `invite_status.json` first — that is the
address the reader actually authenticated with, and therefore what oauth2-proxy
puts in the header — then the roster email. They agree for all five current
signups, but they are different fields with different authority: the roster is
what *you expected*, `locked_email` is what *happened*. A reader approved under a
different address than the roster records must still reach their dashboard.

**Owner preview.** `?as=<slug>` renders that reader's dashboard. Resolve it
server-side against `X-Forwarded-Email`; ignore it entirely for anyone else. The
page must state **"previewing as <name>"** in the header, so a preview is never
mistaken for the owner's own view.

---

## 4. Build

One generator pass over the roster, extending `build_dashboard.py`:

```
for each roster entry:
    ids = {group id parsed from each url in entry["groups"]}
    annotations = [a for a in all_annotations if a["group_id"] in ids]
    render(annotations, viewer=entry)
```

**Match on the group id, never the group name.** Ids are immutable;
names are not — `QpG9pDKd` was renamed `as-pr` → `as-pr-sr` on
2026-08-19, which under name-matching would have silently emptied two
readers' dashboards with no error anywhere. An empty dashboard reads to
the reader as "you haven't annotated anything yet", so this failure is
invisible from both ends.

**A reader may hold several groups** (`groups` array, 2026-08-19) and
sees the union. This exists because a Hypothesis annotation's group is
fixed at creation — the API drops `group` on `PATCH` and returns `200` —
so notes cannot be migrated. *Moving* a reader therefore strands their
history in the old group; *adding* a group keeps it. `roster_groups()`
is duplicated in `build_dashboard.py` and `request_access.py` rather
than shared, because the latter is a stdlib-only single file deployed by
hand to `/opt/secondshanti/` and an import would add a second file that
must land in lockstep or the invite flow fails to start.

**Filtering happens before serialisation — this is the load-bearing
requirement.** `build_dashboard.py` embeds its whole dataset inline as
`const DATA = __DATA__`. Build a reader page from the full `annotations.json`
and filter in JavaScript, and every reader's HTML contains every other reader's
private annotations, one View Source away. That would defeat the exact thing the
access gate protects.

The same applies to the **filter chips**: the chapter dropdown and reader chips
must be generated from the filtered subset. Build them before filtering and a
reader's page carries the names of every other reader and group in a `<select>`,
even though the cards themselves are correctly scoped.

**Cost.** Thirteen small pages instead of one large one, on the 15-minute cycle.
Each reader's dataset is a fraction of the full set, so the added time should be
under a second per reader; confirm on the first run rather than assuming.

---

## 5. What the reader version removes

| Removed | Why |
|---|---|
| **Reply composer** | `dashboard_api.py` posts via `HypothesisClient()`, which reads the owner's `token.txt`. A reader pressing Post would publish **as the owner**, with the owner's status tag, visible to their group. Not a permission error — the API would accept it. |
| **TODO queue** | The owner's private manuscript task list. |
| **Refresh button** | Triggers a pull across *all* groups. |
| **"Readers" tile** | Counts across groups. |

`/as/private/dashboard/api/*` keeps its owner-only check as defence in depth,
independent of the composer being absent from the reader page.

**Replying is not lost — it moves to where it belongs.** Every card already
carries "View on Hypothesis →" using the `#annotations:<id>` fragment, which
opens the chapter with that annotation focused and the sidebar open. The reader
replies there, as themselves, beside the passage. That is better than a dashboard
composer would be: a reply written next to the highlighted text beats one written
against a quote fragment.

**Reader API tokens were considered and rejected.** A Hypothesis personal token
is unscoped — full read, edit, and delete across every group the person belongs
to, including private groups unrelated to this book. Collecting thirteen of them
would turn a single-credential system into a custodian of other people's
accounts, add real signup friction for people doing a favour, and duplicate
something Hypothesis already does better in context.

---

## 6. Reader-facing framing

- **Hero stat**: replies to *their own* notes, with the group total secondary.
  With group filtering a reader sees a mixed set, so an undifferentiated count
  blurs the one number they care about.
- **Own notes visually marked** so a reader can tell theirs from a partner's.
- **Status badges kept** — they tell a reader whether they have been answered.
  Note *awaiting-reader* reads as a call to action from their side, not a parking
  state; consider labelling it accordingly.
- **Threads kept** — the conversation is the point.
- **Default sort** newest-first or by chapter, not the owner's urgency weighting.
- **"As of" timestamp** visible, since the page is rebuilt on a cycle rather than
  on demand.

---

## 7. Open items

- **Digest unsubscribe.** `digest_send.py` already tracks the newest reported
  `updated` timestamp and no-ops when nothing is new, so "only active readers" is
  that logic keyed per reader. It has no unsubscribe path, and readers did not
  ask for mail. Settle cadence and opt-out **before** the first send.
- **`html_essay.html`.** It renders both public essays and gated advance-reader
  essays from one template, so the nav swap there needs a conditional or a
  decision. `html_chapter.html` and `html_index.html` are unambiguous; leave
  `landing.html` and `error_404.html` alone — they are public, and a reader-only
  link there would send anonymous visitors through Google login into a 404.
- **Shared-group consent.** Group filtering is confirmed and intended. Worth a
  line in the invite email so a paired reader learns it from you rather than by
  discovering a stranger's notes in their dashboard.

---

## 8. Execution order

1. ~~**Generator**~~ — *done 2026-08-19.* Per-reader filtered build in
   `build_dashboard.py`, own-note marking, reader hero stat, composer/TODO/
   refresh removed; group-id matching and the `groups` array landed with it.
   A roster-recorded `hypothesis_username` now supplies `VIEWER.self`
   directly, so own-note marking works without the resolver for the four
   readers whose accounts are known.
2. **Service + gate** — email → reader resolution, no-group page, `?as=` preview,
   Caddy route replacing the static handler.
3. **Verify** — confirm a reader page contains *only* that group's data (cards
   *and* chips), that the owner page is unchanged, and that a whitelisted
   non-reader gets the no-group page rather than a 404 or someone else's data.
4. **Nav** — swap on the gated templates.
5. **Digest** — last, once unsubscribe and cadence are settled.
