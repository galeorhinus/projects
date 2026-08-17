# Atomic Sanskrit Repository Reorg Plan (Claude)

**Status:** Active
**Canonical:** Yes
**Owner:** Shared
**Next action:** Author review — approve/reject each phase; Phase 1 can execute immediately on approval
**Last reviewed:** 2026-08-17

---

## 1. Method

Full pass over the repository root and every documented directory, cross-checked against every actual path dependency in `build_book.py`, `build_html.py`, `deploy.sh`, the `Caddyfile`, `hypothesis/*.py`, `server/*.py`, and amrut's crontab/systemd units (as documented in `hypothesis/README.md` and `server/README.md`), plus a grep sweep for prose/doc references to each candidate directory across `as_*.md` and `working/**/*.md`. A directory is only proposed for archiving if **both** checks come back clean — no code path constructs it, and no doc points a reader at it. One correction along the way: a naive substring grep (`"filters/"`) said `filters/` was unused; it's actually referenced via `Path` joins (`BOOK_DIR / "filters" / "latex-strikeout.lua"`) in `build_book.py`. Every finding below was re-verified after that, not just first-pass grepped.

**Ground truth on what's actually load-bearing for the PDF and for amrut**, so the "do not touch" list is explicit up front:

| Consumer | Reads from |
|---|---|
| `build_book.py` (PDF) | `figures/`, `templates/devanagari-preamble.tex.in`, `filters/latex-strikeout.lua`, `as_book.yaml`, `as_endnotes.md`, `as_reference.yaml`, `as_reference_front.md`, `as_reference_*.md`, all root `as_*.md` chapter files, `working/` (one stale path, see §3) |
| `build_html.py` (website) | `figures/`, `templates/*.html`, `templates/*.css`, `working/50_projects/public_facing/outreach/`, `working/50_projects/public_facing/web/public/`, `working/50_projects/public_facing/web/private/` |
| `deploy.sh` | `build/html/`, `server/invite_roster.json`, `Caddyfile` |
| amrut cron/systemd (hypothesis pipeline) | `hypothesis/*` only, absolute paths under `/home/ubuntu/projects/writing/books/atomicSanskrit/hypothesis/` |
| amrut cron/systemd (server pipeline) | `server/*` only |
| `working/50_projects/dhatu_hexagons/{SPEC,TEMPLATES}.md` | `concepts/vyanjana_timing.md` via relative path `../../concepts/` |

None of the moves proposed below touch anything in this table. That's the scoping principle: everything the PDF build, the website build, or amrut's two pipelines actually read stays exactly where it is.

---

## 2. Phase 1 — Archive confirmed-dead top-level clutter (zero risk)

Six top-level items are undocumented in `CLAUDE.md`'s file map, unreferenced by any build script, and unreferenced by any other document except where a document already calls them stale. Each was individually verified, not assumed:

| Item | What it is | Verification |
|---|---|---|
| `scripts/` (7 files) | Pre-reorg draft of the dhātupāṭha analysis scripts, dated **18 May** | Superseded by `analysis/dhatupatha/scripts/` (same filenames, improved, dated **25 May**, matches CLAUDE.md's documented `analysis/` convention). `diff` confirms the two copies have actually diverged — the old ones are not just a redundant copy, they're stale content. Zero build-script references. |
| `svg/` (10 files) | Old mermaid-diagram experiments (`etymology_lord_decay.*`, `molecular-architecture-model.*`) plus a legacy `sh/pdfMake.sh` dependency (below) | Zero references anywhere. Superseded by the current `figures/` matplotlib pipeline. |
| `sh/pdfMake.sh` | Old monolithic single-file PDF build (`atomicSanskrit.md` → `atomicSanskrit.pdf`, driving `svg/`) | The `.md`/`.pdf` it builds already sit in `archive/` (`archive/atomicSanskrit.md`, `archive/atomicSanskrit.pdf`) — this script is the tool for a build that's already been retired. |
| `share/` (2 files) | `as_toc_share.md`/`.pdf`, a pocket-size shareable TOC card | `working/40_reference/decisions/eclipse_spine_conversion_plan.md` itself flags this as needing "a full rebuild" — it predates the AP0-promotion renumbering. Already known-stale by the project's own record. |
| `revision/codex/`, `revision/gemini/` | Two subdirectories | **Completely empty.** Nothing to archive; just remove. |
| `tmp.md` (root) | A 698-byte scratch file | Gitignored, untracked, not referenced anywhere. |

**Recommended action:** `git mv` the first four into `archive/`, deleting the two empty `revision/` subdirectories outright (nothing to preserve). Suggested destination layout, since `archive/` is currently one flat pile of ~30 files and this is a natural moment to give the newly-added material a home instead of adding four more loose top-level entries:

```
archive/
  pre_reorg_scripts/        <- scripts/*.py
  pre_buildbook_pipeline/   <- sh/pdfMake.sh, svg/*
  share_toc_card/           <- share/*
```

This is optional — dropping the four items straight into `archive/`'s existing flat structure is equally safe and lower-effort. Either way, **not one build script or doc reference needs updating** for this phase; that was the whole point of the verification.

**Not touched, and here's why `sh/tocPDF.sh` survives Phase 1:** unlike `pdfMake.sh`, `tocPDF.sh` is the actual tool that (re)builds `share/as_toc_share.pdf` from `share/as_toc_share.md` — it's live tooling for a stale *artifact*, not itself stale. See Phase 2.

**Not touched: `concepts/`.** Initially looked like a two-file orphan. It is not — `working/50_projects/dhatu_hexagons/SPEC.md` and `TEMPLATES.md` both reference `../../concepts/vyanjana_timing.md` by relative path for the ½/1/2-*mātrā* timing grounding behind that production project's hexagon widths. This stays exactly where it is. (It should, however, get a row in CLAUDE.md's file map — see Phase 4.)

---

## 3. Phase 2 — Relocate genuinely live but misplaced tooling

`sh/tocPDF.sh` is real, working tooling (confirmed by reading it: plain `pandoc`/`xelatex` invocation, no hidden dependencies) for regenerating `share/as_toc_share.pdf`, which `working/README.md`'s own documented `tools/` zone exists for: *"Scripts that support manuscript work... Move to a permanent project tool directory if it becomes production infrastructure."* `working/tools/` already holds exactly this class of thing (`deai_strip.py`, `endnotes_short_scaffold.py`).

**Recommended action:**
```
git mv share/as_toc_share.md share/as_toc_share.pdf working/tools/toc_share/
git mv sh/tocPDF.sh working/tools/toc_share/build.sh
```
Update `working/tools/toc_share/build.sh`'s bare `INPUT=`/`OUTPUT=` filenames only if the working-directory assumption changes (they're currently CWD-relative, so this move is transparent as long as the script is still run from inside its own directory). Delete the now-empty `share/` and `sh/` directories.

---

## 4. Phase 3 — Fix two stale references surfaced during this audit

Neither of these is a reorg-caused break; both are pre-existing bugs the audit surfaced while verifying what's safe to move.

1. **`build_book.py:589`** — `load_stub_descriptions()` reads `BOOK_DIR / "working" / "as_todo.md"`, but the file has lived at `working/10_active/as_todo.md` since the status-zone reorg. The function's own docstring already says the correct path; the code just never got updated. `path.exists()` silently returns `False` today, so this function has been quietly returning `{}` for every call. One-line fix: `BOOK_DIR / "working" / "10_active" / "as_todo.md"`.
2. **`as_endnotes.md` lines 5161, 5175, 5183** — three run-commands say bare `scripts/analyze_dhatupatha.py` / `scripts/analyze_varga_distribution.py`, left over from before the `analysis/dhatupatha/` migration. Every *other* script reference in the same file (lines 5221, 5225, 5231, 5243, 5313, 5868) correctly says `analysis/dhatupatha/scripts/...`. If Phase 1 retires the top-level `scripts/` directory, these three become actively misleading (a reader following the endnote would hit a 404 path) rather than just inconsistent. Fix: prefix all three with `analysis/dhatupatha/`.

---

## 5. Phase 4 — Documentation-only additions to `CLAUDE.md` (zero code risk)

`CLAUDE.md`'s "Project layout (directories)" table is missing several directories that are genuinely load-bearing, which is how this audit had to re-derive their status from scratch instead of reading it off. Recommend adding rows for:

- `hypothesis/` — the annotation/dashboard pipeline (has its own thorough `README.md`; just needs a pointer from the top-level map).
- `server/` — the invite/whitelist service (same — thorough own `README.md`, no pointer from the top).
- `concepts/` — small durable reference notes consumed by production sub-projects (currently just `vyanjana_timing.md`; document the pattern so a future author doesn't re-flag it as an orphan the way this audit initially did).
- A row (or a sentence in the existing Drafts paragraph) for `as_reference.yaml` / `as_reference_front.md` / `as_reference_*.md` — the *Source and Reference Companion*'s own source files. These are as load-bearing as `as_book.yaml` for the main book but currently don't appear anywhere in the file map.
- A row for `as_part_*.md` (the eclipse-spine Part openers, `as_part_00` through `as_part_07`) — mentioned in the "Book division structure" prose but not listed alongside the other manuscript file categories the way Front matter / body chapters / Appendix parts are.
- `Caddyfile` and `deploy.sh` — both root-level and both load-bearing for the live site; currently unmentioned in the file map (deploy.sh is referenced only in passing inside `hypothesis/README.md`).

None of this moves a single file. It's closing the gap between what the repository actually depends on and what a session's bootstrap read tells it to expect — which is exactly the gap this whole audit had to route around by grepping instead of reading.

---

## 6. Phase 5 — `working/` zone-discipline drift (needs its own triage pass, not attempted here)

`working/README.md` states `10_active/` should stay "small enough to scan in one editor pane." It currently holds **119 files** — including several multi-document sub-trees (`manuscript_readability_review_codex/`, `manuscript_readability_audit_codex/`) that read as completed audits sitting in the active zone rather than `80_completed/`. This is a real finding but a separate, larger task from the structural reorg: it requires reading each item to decide active / queued / paused / completed / superseded, not a mechanical move. Flagging it here so it's tracked; recommend a dedicated pass rather than folding it into this one.

One small, safe, immediate fix in the same spirit: `working/as_ten_designed_declensional_variations_gemini_research.md` sits loose directly in `working/`, outside any zone — a violation of the directory's own rule 1 ("Put new uncategorized notes in `00_inbox/`"). Its content (a sourced verification audit for Appendix Part 8) matches `40_reference/`'s stated purpose ("durable evidence... source material") better than `00_inbox`'s "awaiting classification." Recommend:
```
git mv working/as_ten_designed_declensional_variations_gemini_research.md working/40_reference/source_material/
```

Also noted, lower priority: `reference/as_thesis_summary_prepublication.md` looks like it may be a stale duplicate of `reference/as_thesis_summary.md` (still referenced from a few `working/10_active/` planning docs, so not touched here — needs a read-through to confirm before any move).

---

## 7. Phase 6 — Optional, cosmetic: subdivide `archive/`

`archive/` is ~30 loose files at one flat level (plus a `figures/` and `notes/` subdirectory already). Nothing references any of them by path — that's the point of the directory — so this is the lowest-risk, lowest-priority item in the whole plan: pure filing, purely optional, safe to defer indefinitely or skip. If ever done, natural groupings from what's there now: pre-split chapter drafts (`as_ch07*`, `as_ch08_draft-claude.md`, `as_ch16_rat_cutbin.md`), voice/style calibration (`ptStyleGuide.md`, `ptVoiceCalibration.md`, `voiceRevision.md`), old handoffs (`as_handoff.md`, `as_session9_handoff.md`, `session_handoff_instructions.md`), old TOC states (`as_toc_current.md`, `as_toc_proposed.md`), and source PDFs (`orlAppendix.pdf`).

---

## 8. Execution order

1. **Phase 1** (archive dead weight) — safe to run immediately, zero reference updates needed.
2. **Phase 3** (the two stale-reference fixes) — do alongside Phase 1, since Phase 1 is what makes the `as_endnotes.md` fix urgent rather than cosmetic.
3. **Phase 2** (relocate `tocPDF.sh` + share artifacts into `working/tools/`) — safe, independent, do whenever.
4. **Phase 4** (CLAUDE.md doc additions) — do last, once the moves above are final, so the new rows describe the settled state rather than needing a second edit.
5. **Phase 5 / 6** — separate, later passes; not blocking on anything above.

Nothing in Phases 1–4 touches `figures/`, `templates/`, `hypothesis/`, `server/`, `working/50_projects/`, `analysis/`, `reference/`'s existing files, `archive/`'s existing files, or any of the root `as_*.md` manuscript/companion source files. The PDF build and amrut's two pipelines read from none of the items in scope here.
