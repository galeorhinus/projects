# Atomic Sanskrit Repository Restructure Proposal (Claude)

**Status:** Active — awaiting author decision
**Canonical:** Yes
**Owner:** Shared
**Next action:** Author picks Option A or Option B (or rejects); execution follows in phases
**Last reviewed:** 2026-08-17

Supersedes the directory-level portions of `as_repo_reorg_plan_claude.md` Phases 5–6. That document's Phases 1–4 are done or still valid; this document replaces its thinking about *where things live* with a whole-repository organizing principle.

---

## 1. The question this answers

`working/50_projects/public_facing/` is four levels deep for material that is neither "working" (in the manuscript-drafting sense) nor a "project" in the same sense as its sibling `dhatu_hexagons/`. The author's framing is the right one: **`working/` should focus on the manuscript.** Everything currently in the repository should be sortable by one question — *what job does this serve?* — and the top level should make those jobs visible.

---

## 2. The four jobs this repository actually does

Reading the whole tree, the repository serves four distinguishable jobs. The current layout expresses the first two clearly and buries the other two.

| Job | What it covers | Where it lives now |
|---|---|---|
| **1. Write the book** | Manuscript sources, endnotes, TOC, voice rules, drafting plans, audits, recovery ledgers, research bundles, figures | Root `as_*.md`, `reference/`, `figures/`, `analysis/`, `concepts/`, most of `working/` |
| **2. Build the artifacts** | PDF and website generation | `build_book.py`, `build_html.py`, `templates/`, `filters/`, `build/`, `as_book.yaml`, `as_reference.yaml` |
| **3. Get readers reading it** | The live site, access control, annotation collection, the reader dashboard | `Caddyfile`, `deploy.sh`, `server/`, `hypothesis/`, `working/50_projects/public_facing/web/` |
| **4. Get the book into the world** | Jacket copy, article drafts, publishing strategy, agent/publisher/press contacts, outreach messages | `working/50_projects/public_facing/{articles,strategy,outreach}/` |

Job 3 is already well-served at top level (`server/`, `hypothesis/`) — *except* for its web-content half, which is stranded down in `working/`. Job 4 has no top-level home at all, which is precisely the problem the author identified. And the reason it feels wrong is structural, not aesthetic: **jobs 3 and 4 are not manuscript work, and `working/`'s own README defines itself as manuscript development material** ("material that is still useful to the development of *Atomic Sanskrit*").

---

## 3. The organizing principle

> **Top-level directories name jobs. `working/` holds exactly one job: developing the manuscript.**

Two corollaries follow, and they resolve the awkward cases:

- **A directory earns top-level placement when it serves a job other than manuscript development,** regardless of size. `server/` is small and already top-level for exactly this reason; `outreach/` deserves the same treatment.
- **Build *inputs* live with the job they serve, not with the build.** Jacket copy is outreach material that the website happens to render; the essay drafts are publishing material that the website happens to host. The build script reaches out to them, not the reverse. This is already how `figures/` works — it is manuscript material that both builds consume, and it is not filed under `templates/`.

---

## 4. Option A — Two new top-level directories (recommended)

Split `public_facing/` along the seam that already exists inside it: **web-published content** versus **outreach and publishing campaign**.

```
atomicSanskrit/
  as_*.md,  as_book.yaml,  as_endnotes.md        manuscript + companion sources
  reference/                                       TOC, thesis summary, voice references
  figures/  analysis/  concepts/                   manuscript evidence + illustration
  working/                                         MANUSCRIPT DEVELOPMENT ONLY
  build_book.py  build_html.py  templates/  filters/  build/
  Caddyfile  deploy.sh  server/  hypothesis/
  web/                                             NEW — content published to the site
    public/                                        ungated essays + landing copy
    private/                                       gated essays for invited readers
  outreach/                                        NEW — getting the book into the world
    jacket_copy/                                   the 4 variants build_html.py renders
    articles/                                      article + essay drafts
    strategy/                                      publishing strategy (3 agent drafts)
    contacts/                                      was outreach/{people,outlets,publishers}
    messages/                                      WhatsApp / advance-reader drafts
    parag_bio.md
    atomic_sanskrit_proposal_overview.md
    atomic_sanskrit_spoken_descriptions.md
```

**Why `web/` and `outreach/` separately, rather than one folder?** They have different lifecycles and different audiences. `web/` content is *published* — it is live, it is built on every deploy, and changing it changes what readers see immediately. `outreach/` is *preparatory* — drafts, contact notes, strategy, most of which never ships anywhere. Merging them would recreate the current problem in a new location: one folder where the build-critical and the purely-planning sit side by side with nothing marking which is which.

**Why does `jacket_copy/` go under `outreach/` and not `web/`,** when `build_html.py` renders it? Because it is outreach copy first — the text that sells the book to a reader, an agent, or a publisher — and its rendering as a gated reviewer page is one downstream use. Keeping the four variants next to the proposal overview and the spoken descriptions groups them by what they *are*. This is a genuine judgment call: filing them under `web/` alongside the other rendered content would also be defensible. Flagging it rather than pretending it is obvious.

### Cost

Five path constants in `build_html.py` (`JACKET_COPY_SRC`, `_JACKET_OUTREACH_DIR`, `FAVICON_SRC_DIR`, `ESSAYS_PUBLIC_SRC`, `ESSAYS_PRIVATE_SRC`) plus a redeploy on amrut. `build_book.py`, `deploy.sh`, the `Caddyfile`, `server/`, and `hypothesis/` are untouched — verified by direct grep, this is the complete dependency list.

---

## 5. Option B — One new top-level directory

If two new top-level entries feels like too much, everything moves under a single `publishing/`:

```
  publishing/
    web/{public,private}/
    jacket_copy/  articles/  strategy/  contacts/  messages/
```

Same five `build_html.py` constants change. Simpler top level; the cost is that live-published content and never-shipped planning notes sit as siblings again, which is the ambiguity Option A exists to remove. Recommended only if the top level is felt to be crowded.

---

## 6. What does NOT move, and why

Recorded explicitly so a future pass does not re-litigate settled ground:

- **`working/50_projects/dhatu_hexagons/`** stays. Confirmed by reading its `SPEC.md`: it is a figure-generation project for manuscript illustrations, grounded in `concepts/vyanjana_timing.md` and an endnote. That is manuscript development, correctly placed.
- **`hypothesis/` and `server/`** stay at top level. Already correct under the organizing principle — they serve job 3, and they already have thorough READMEs.
- **`reference/`, `figures/`, `analysis/`, `concepts/`** stay. All manuscript material; all correctly placed.
- **`templates/`, `filters/`, `build/`** stay. Build machinery, correctly placed.

After the move, `working/50_projects/` contains only `dhatu_hexagons/`. That is fine — the zone's definition ("multi-file production workstreams" supporting the manuscript) still describes it accurately, and a second such project may well appear.

---

## 7. Execution plan (on approval)

Each phase is independently committable and independently verifiable.

1. **Move `web/`.** `git mv working/50_projects/public_facing/web web`. Update `FAVICON_SRC_DIR`, `ESSAYS_PUBLIC_SRC`, `ESSAYS_PRIVATE_SRC` in `build_html.py`.
2. **Move `outreach/`.** `git mv` the remaining `public_facing/` subdirectories into a new top-level `outreach/`, regrouping `{people,outlets,publishers}` → `contacts/`, the WhatsApp drafts → `messages/`, and the four jacket variants → `jacket_copy/`. Update `JACKET_COPY_SRC` and `_JACKET_OUTREACH_DIR`.
3. **Verify before deploying.** Run `python3 build_html.py` locally and confirm the rendered `build/html/` tree is byte-identical to the pre-move build except for expected differences. This is the real safety gate — a path constant pointing at nothing would otherwise fail silently or drop a page, and `deploy.sh`'s `rsync --delete` would then propagate that deletion to the live site.
4. **Deploy.** `ssh amrut`, `git pull`, `python3 build_html.py`, `./deploy.sh --skip-build`. Confirm the landing page, an ungated essay, a gated essay, and a jacket-copy variant all load.
5. **Update `CLAUDE.md`.** Add the new top-level directories to the file map, along with the entries `as_repo_reorg_plan_claude.md` Phase 4 already identified as missing (`hypothesis/`, `server/`, `concepts/`, `Caddyfile`, `deploy.sh`, the `as_reference_*` companion sources, `as_part_*.md`).
6. **Grep sweep.** Repair any documentation references to the old `working/50_projects/public_facing/` paths, per `working/README.md`'s maintenance rule 5.

Steps 1–2 are mechanical. Step 3 is the one that must not be skipped.

---

## 8. Still open, separately

Independent of this restructure, from the earlier audit: the ~78 remaining files in `working/10_active/` include roughly 30 multi-agent comparison drafts and 14 lost-and-found ledgers whose exit rules in `working/README.md` suggest they belong in `90_superseded/` and `80_completed/`. That triage needs per-file judgment about which comparisons were reconciled and which recovery passes closed — the author can resolve most of it faster than a file-by-file reading can. Tracked here so it is not lost; not blocked by this restructure.
