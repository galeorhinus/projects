# Orphaned Endnotes — Triage

**Created:** 2026-08-22
**Status:** Category A resolved 2026-08-22. Three App-6 entries in Category D also
resolved by the author in the same pass. 33 orphans remain, all Category B/C/D/E.
**Scope:** the 39 stubs in `manuscript/as_endnotes.md` with no `[NOTE:]` marker anywhere in the manuscript

---

## Headline

**356 stubs defined · 317 deployed · 39 orphaned · 0 markers missing a stub.**

Nothing is broken. A marker without a stub would break the build; there are none.
The reverse is inert — an undeployed stub simply sits in the file. The only live
consequence is the *Source and Reference Companion*, which draws from this file
and would print entries nothing points to.

**Not a creeping problem.** Traced through git history, the count accumulated in
two bursts in June and has been essentially flat since:

| Date | Stubs | Deployed | Orphans | |
|---|---:|---:|---:|---|
| 12 May | 1 | 71 | 0 | clean |
| 31 May | 187 | 190 | 2 | |
| **8 Jun** | 199 | 185 | **15** | "Endnote sweep: inventory-atlas methodology" |
| **15 Jun** | 217 | 189 | **29** | "Ch 5 + Ch 6 reframe-to-freeze" |
| 24 Jul | 278 | 246 | 33 | |
| 13 Aug | 341 | 308 | 34 | |
| 20 Aug | 354 | 315 | 39 | Ch11–12 rewrite (+5) |
| 22 Aug | 356 | 317 | 39 | flat |

Two months of heavy work between mid-June and mid-August moved it 29 → 34.

---

## Category A — Lost marker: the prose exists but is unlinked

> **RESOLVED 2026-08-22.** All three markers re-attached at the point each claim is
> made, and `ross-metatypy-takia`'s stale Deployments line corrected from Ch 19 §19.7
> to Ch 20 §20.2. Audit after the fix: 356 stubs, 323 deployed, 0 markers without a
> stub. Detail retained below as the record of what was lost and where.

**These are the actual defects.** In each case the material the endnote was written
for is still in the manuscript, carries no marker, and the reader therefore gets no
citation for a claim the endnote was written to support.

### A1. `english-sanskrit-loanwords` → Chapter 0 §0.3

Deployment record says Ch 0 §0.3. That section exists and the passage is there,
at `as_1_00_seekers.md:73`:

> "A Western reader already speaks Sanskrit casually through words that have
> entered the global vocabulary: **गुरु**, **कर्म**, **अवतार**, **मन्त्र**, and
> **योग**… Chapter 19 traces Sanskrit's radiance through thousands of familiar
> English words, including *king, station, genesis, native, constant,* and *state*"

**The sentence carries no `[NOTE:]` at all.** A claim about thousands of English
words is exactly the sort a reader checks.
**Action: re-attach.**

### A2. `ross-metatypy-takia` → moved chapter, marker not carried

Deployment record says Ch 19 §19.7. The term does not occur anywhere in Ch 19.
It now lives in **Chapter 20**, `as_1_20_life_after_pie.md:59`:

> "Contact linguistics calls this kind of transmission **methodological metatypy**."

**That sentence is unmarked.** The endnote is the citation anchor for Malcolm
Ross's 1996 paper and the Takia/Waskia case — i.e. the source for a technical
term the book borrows and leans on.
**Action: re-attach in Ch 20, and correct the Deployments line to Ch 20.**

### A3. `missionaries-of-progress-precedent` → Chapter 4 §4.4

The formal introduction of the term is present at `as_1_04_fourth_abrahamic.md:143`
and carries `[NOTE: rostow-modernization-theory]` — a *different* source (W. W.
Rostow, *Stages of Economic Growth*). The orphaned endnote is a different thing
entirely: **Parag Tope, "Missionaries of 'Progress'," *Quick Take*, 29 October 2011.**

That is the author's own prior use of a term the book presents as its standing
vocabulary. Losing it drops the priority claim.
**Action: re-attach alongside the Rostow note.**

---

## Category B — Parked by explicit decision (no action)

Each of these states in its own Deployments line that it is intentionally undeployed.
They are retained source material, not debt.

| Stub | Recorded reason |
|---|---|
| `as-bhu-being-paradigm` | "Retained as source material for future use" after the Ch 19 §19.9 / App 1 cut |
| `briggs-1985-ai-magazine` | Background for Position-2 / Pāṇinian formal-system context |
| `jakobson-1959-nursery-words` | "PARKED (not currently deployed)" — the 2026-07-06 rewrite retired the worked example |
| `kak-paninian-algorithmic` | Background, retained after the Preface lineage rewrite |
| `mendeleev-1869-table` | "Preserved as reference material after the Chapter 11 restructure" |
| `samarth-ramdas-mleccha-verse` | "No live body deployment after the Chapter 17 rewrite; retained" |
| `savarkar-ratnagiri-mleccha` | Same — retained for possible future public-facing use |
| `staal-formal-systems` | Background for Position-2 / formal-systems context |
| `where-this-argument-stands` | Positioning note; belongs to the *Companion*, not the body |

**9 stubs. Action: none.** Worth marking them so a future audit stops re-flagging them
— see the closing recommendation.

---

## Category C — Source anchors for a deployed parent (no action)

These six are second-level references: they support the endnote
`modern-sanskrit-lineage-roles` rather than the body directly. **Verified: the parent
IS deployed**, at `as_0_01_preface.md:98`. The pattern is legitimate — an endnote
citing its own sources.

`aurobindo-kapali-sastry-mishra-vedic-lineage` · `dayananda-rgvedadi-bhashya` ·
`kak-vedic-structural-architecture` · `kapoor-text-and-interpretation` ·
`malhotra-battle-for-sanskrit-pollock-prosecution` · `ojha-vedic-architecture-corpus`

**6 stubs. Action: none.**

---

## Category D — Stranded by restructuring: target section exists, topic does not

The named section still exists, but the material the endnote cites is no longer in
it. The prose was rewritten or cut. Each needs a decision: **redeploy** (the claim
should return) or **retire to the Companion** (the claim is gone for good).

**The Chapter 9 cluster is the largest and most suspicious — eight stubs across four
sections.** That concentration suggests §§9.1–9.5 were rewritten as a block and the
citations were not carried forward. Worth reading those sections against these eight
before deciding, since some claims may have survived in reworded form.

| Stub | Claimed target | Topic now in that section? |
|---|---|---|
| `architecture-not-analysis-pratisakhya` | Ch 9 §9.4 | no — Staal critique absent |
| `staal-mendeleev-varga-comparison` | Ch 9 §9.4 | no — Staal/Mendeleev absent |
| `varnamala-grid-geometry` | Ch 9 §9.4 | unclear — "grid" is ubiquitous; needs a read |
| `bengali-va-ba-merger` | Ch 9 §9.3 | no — Bengali absent |
| `south-indian-mahaprana-loan-only` | Ch 9 §9.3 | no |
| `pahari-tonal-features` | Ch 9 §9.5 | no — tone absent |
| `punjabi-tonal-development` | Ch 9 §9.5 | no — tone absent |
| `formants-source-filter-theory` | Ch 7 §7.5, Ch 9 §9.1 | no |
| `sanskrit-field-52b-reach` | Ch 0 §0.3 | no — the 5.2-billion figure is gone |
| `yaska-deva-derivation` | Ch 0 §0.3 | no |
| `rigveda-10-125-vak-ambhrini` | Preface | no — the "only men see" passage moved |
| `pratisakhya-bhashyam-chandasi` | Ch 17 §17.4 | no |
| `hlad-contrast-atom` | Ch 12 §12.3 | no — §12.3 is now "From *Śabda* to *Padam*"; the *hlād* contrast was cut in the Ch 12 rewrite |
| ~~`dcs-vs-dhatupatha-count`~~ | Ch 11 §11.5 | **RESOLVED** — redeployed in App 6, as predicted; the reactivity tiers moved there from Ch 11 §11.5 |
| ~~`cross-gana-column-distribution`~~ | App 6 §§6.2, 6.4 | **RESOLVED** — redeployed in App 6 |
| ~~`generative-reach-inversion-natural-language`~~ | App 6 §6.3 | **RESOLVED** — redeployed in App 6 |
| `history-of-linguistics-sanskrit-influence` | App 3 §3.8, App 5 §5.8 | not tested |
| `ipa-1886-founding-1888-chart` | App 3 §3.8 | not tested |
| `jones-1786-third-anniversary-discourse` | App 3 §3.8, App 5 §5.8 | not tested |
| `western-linguistic-encounter-sanskrit-1786-1879` | App 3 §3.8, App 5 §5.8 | not tested |

**Note on the two Ch 11–12 entries.** `hlad-contrast-atom` and `dcs-vs-dhatupatha-count`
are the +5 from the 20 Aug rewrite. Both cite material that *moved to Appendix Part 6*
rather than being deleted — so these are probably **redeploy in App 6**, not retire.

**The four App 3 §3.8 / App 5 §5.8 stubs** (Jones 1786, IPA 1886, history-of-linguistics,
western-linguistic-encounter) are one coherent group: the standard Western
history-of-linguistics citation apparatus. They should be checked together, since if
that passage still exists all four re-attach at once.

**20 stubs. Action: read the targets, then redeploy or retire.**

---

## Category E — No deployment record at all

| Stub | Note |
|---|---|
| `kailasa-temple-ellora-engineering` | No `**Deployments:**` line. Topically adjacent to the new Ch 6 §6.1 temple argument (Ta Prohm) — plausibly wants a home there as the *engineered* counterpart to the *overgrown* temple. |

**1 stub. Action: consider for Ch 6 §6.1.**

---

## Summary

| Category | Count | Action |
|---|---:|---|
| ~~A. Lost marker, prose present~~ | ~~3~~ | **done 2026-08-22** |
| B. Parked by decision | 9 | none |
| C. Source anchor, parent deployed | 6 | none |
| D. Stranded by restructure | 20 → **17** | read target, then redeploy or retire (3 App-6 entries resolved) |
| E. No record | 1 | consider Ch 6 §6.1 |
| | **39 → 33 open** | |

**The 3 defects are fixed.** 15 are working as intended. 17 still need a read-and-decide,
and of those the Ch 9 cluster (8) and the App 3/5 group (4) can each be settled in one pass —
those two groups are now most of what is left.

---

## Recommendation: make this self-checking

The audit above is a fifteen-line script. Adding it to the build — or to
`working/tools/` — would surface a lost marker in the commit that causes it, rather
than three months later. The check that matters is not "is a stub unused" but **"is a
stub's recorded Deployments target still present, and does it still carry the
marker?"** — that is precisely the condition that caught A1, A2, and A3.

To stop Category B being re-flagged every run, those nine could carry an explicit
field, e.g. `**Status:** parked`, letting the check skip them by declaration instead
of by a human re-reading the reason each time.

### Method note

The keyword test used for Category D matched substrings, so `Ross` matched inside
*across* and *cross* and produced a false positive on `ross-metatypy-takia`. That
one was caught and corrected by hand — which is how A2 was found. Entries marked
"not tested" above were not keyword-checked at all and should be read directly. Any
re-run of this analysis should use word-boundary matching.
