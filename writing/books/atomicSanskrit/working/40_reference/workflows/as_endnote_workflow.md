# Endnote Workflow — Two-Form Architecture

*Companion to the CLAUDE.md *Endnote convention* section. Practical workflow doc for the day-to-day handling of endnotes under the two-form (short + long) architecture established in commits `101c3e6` (scaffold + convention) and `b0fd7fc` (140/140 short forms filled).*

---

## The architecture in one paragraph

Every endnote entry in `as_endnotes.md` carries **two forms** in the same file: a one-sentence **Short** form for the printed book, and the **long-form body** for the companion (planned separate free PDF / web artifact). The Short form is tagged with a parseable `**Short:**` field on the line directly after the `### \`stub-name\`` heading; the long form follows below it. Single source of truth, no parallel versions to drift, build pipeline projects either form when needed.

```markdown
### `stub-name`

**Short:** One sentence ending in a period. (Optional: "See Expanded Endnotes for X.")

**Deployments:** Chapter N §N.M ¶ — what the note anchors.

[full long-form body — paragraphs, primary-source quotes, source references]

---
```

---

## Adding a new endnote

When chapter prose adds a `[NOTE: stub-name]` marker, the corresponding entry in `as_endnotes.md` gets **both fields authored together**.

1. **Pick a stub name.** Lowercase-hyphenated, stable, public-facing-friendly (the stub-name becomes a durable identifier in the companion). Examples: `bopp-1816-conjugationssystem`, `eleven-pathas`, `samskrtam-morphology`.
2. **Insert the entry alphabetically-by-topic or at the natural deployment-grouped position** in `as_endnotes.md` (the file is organized by topic-cluster, not strict alphabetical — match the surrounding context).
3. **Author the Short field at draft time.** One sentence ending in a period. Ask: *what does the printed-book reader need from this note?* Pair Sanskrit terms with Devanāgarī on first use per CLAUDE.md voice convention.
4. **Author the Deployments line.** `Chapter N §N.M ¶ — short description of what the note anchors at this deployment.` Multiple deployments listed semicolon-separated.
5. **Author the long-form body.** Whatever the companion reader needs — primary-source citation, verification trail, source-history context, structural significance.
6. **End with the `---` separator.**

**If editorial decision isn't crystal at draft time** — write `**Short:** [TBD: <category>]` (Citation / Citation+Context / Mini-essay / Verification) as placeholder. The discipline is *have the slot, fill it in the moment*. TBD is permitted as a temporary state, not a long-term resting state.

---

## Editing an existing endnote

When the long-form body changes in a way that shifts the load-bearing claim, **review the Short field too**. The short form is the editorial compression of the long form; if the long form's center of gravity moves, the short can drift out of sync.

**Quick check after any long-form edit:**
1. Read the new long-form body.
2. Re-read the existing Short.
3. Does the Short still capture the *one sentence the printed-book reader needs*? If yes, leave alone. If no, refresh.

Voice / cadence touch-ups to the long form don't usually require Short edits. Substantive content changes (new citation added, structural argument shifted, primary-source updated) usually do.

---

## Deleting an endnote

When removing a `[NOTE: stub]` reference from chapter prose:

1. **Check the `**Deployments:**` line** for other places that still reference the stub. If yes, leave the entry alone — only the specific deployment is being removed, not the endnote.
2. **If no other deployments remain**, delete the entire entry from `as_endnotes.md` (heading + Short + Deployments + body + trailing `---`).
3. **If the entry is referenced from another endnote's body** ("See endnote `stub-name`"), update the cross-reference before deleting.

---

## Periodic guardrail — the auto-pass script

`working/tools/endnotes_short_scaffold.py` is idempotent. Re-running it:
- Skips entries that already have a `**Short:**` field.
- Inserts `**Short:** [TBD: <category>]` placeholder into any entry that slipped through without one.

**Useful pre-commit / pre-build check** to catch entries added without a Short field (mistake or hurry):

```bash
python3 working/tools/endnotes_short_scaffold.py
```

The script prints a summary of how many entries got placeholders inserted; if it reports anything other than `Inserted: 0`, an entry was missing its Short field and now has a TBD placeholder for editorial follow-up.

---

## Build pipeline integration

Currently `build_book.py` emits the full body of each endnote (long-form mode is the default and only mode). When print-prep starts, add a `--endnotes=short` flag.

**Implementation sketch** (~30 lines in `build_book.py`):

1. Add a CLI flag: `--endnotes={full,short}`, default `full`.
2. In the existing `load_drafted_endnotes()` function (around line 255), detect the mode.
3. **Short mode:** for each entry, emit only the `### \`stub\`` heading + the content of the `**Short:**` line (with the `**Short:** ` marker stripped). Drop the `**Deployments:**` line and the body. The numbered references in the body of the book still emit as `**[N] \`stub\`.** <short-content>`.
4. **Full mode** (current behavior): emit everything below the heading.
5. **Fallback:** if a Short field is missing or contains `[TBD: ...]`, fall back to the full body and warn in build output. Graceful degradation.

**Don't implement until ready to produce a print proof.** Premature build-pipeline work is wasted cycles; today's value is in keeping authoring discipline intact, not in the projection layer.

---

## Companion productionization (future)

The long-form endnotes become a separately-shipped *Atomic Sanskrit: Source and Reference Companion* artifact — free PDF or web-hosted. When productionizing:

- The companion needs a stable name and canonical URL or print/PDF reference.
- Stub-names become durable public identifiers — anchor links / section IDs in the companion match the stub-names in `as_endnotes.md` so the printed book's "See Expanded Endnotes for X" pointers land.
- Therefore: **don't rename stub-names casually**. Once an entry has been deployed in chapter prose and is being referenced via `[NOTE: stub]` markers, the stub-name is effectively public-facing. Renames break the companion-pointer chain.

Today's action: just don't break the stub-name identifiers.

---

## The mental model

- **Short** = the one sentence the printed-book reader needs. Editorial decision.
- **Long** = the reference-grade citation, verification trail, source-history mini-essay. Reference material.
- **Source of truth** = one file, both fields, no parallel versions to drift.
- **Build pipeline** = projection. Short mode pulls Short; full mode pulls everything. Authoring discipline stays unchanged.
- **Stub-names** = durable identifiers, public-facing in the companion. Treat carefully.

---

## Open follow-ups

1. ~~**Voice review on batches 4-6** (entries 61–140 of the original sweep).~~ **Resolved 2026-05-18** — author reviewed via the rendered short-form PDF (`build/atomic_sanskrit.trade.short.pdf`, commit `49438c5`) and confirmed the back-half reads cleanly. No re-voicing pass needed.
2. **Companion artifact name, URL, and anchor scheme** — open productionization decision; not blocking until print. Today's discipline: don't rename stub-names casually; they become public-facing identifiers in the companion.

---

*Reference commits, in order: `101c3e6` (two-form scaffold + CLAUDE.md convention) → `b0fd7fc` (140/140 short forms filled) → `49438c5` (`build_book.py --endnotes={full,short}` flag). Auto-pass script preserved at `working/tools/endnotes_short_scaffold.py`.*
