# Orphaned Endnotes — Triage

**Created:** 2026-08-22
**Status:** Complete 2026-08-22. Category A was repaired, reachable and intentionally
parked entries were identified, and all twelve entries that required a decision were
redeployed, merged, or retired. See *Second pass* through *Fourth pass* below.
**Scope:** the audit began with 39 stubs in `manuscript/as_endnotes.md` that had no direct `[NOTE:]` marker in the manuscript

---

## Headline

**356 stubs defined · 333 directly deployed · 23 without a direct body marker · 0 unresolved decisions · 0 live markers missing a stub.**

Nothing is broken. A marker without a stub would break the build; there are none.
Every entry without a direct body marker is now accounted for as reachable through
another endnote, intentionally parked, or retired source material. The explanatory
`[NOTE: stub-name]` example at the top of `as_endnotes.md` is not a live marker.

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

## Second pass (2026-08-22) — 33 open becomes 12

Three findings, in the order they landed.

### 1. An orphan is not necessarily unreachable

`jones-1786-anniversary-address` is deployed, and its body reads *"Forward-pointer to
the main `jones-1786-third-anniversary-discourse` endnote."* The orphan is the
**target of a pointer from a deployed endnote** — a reader following the citation
chain gets there. That is not a defect; it is a two-level citation, the same pattern
Category C already recognized for `modern-sanskrit-lineage-roles`.

Re-running the audit with a cross-reference test rather than a body-marker test:
**11 of the 33 are reachable from a deployed endnote.** Category C grows 6 → 11.

| Orphan | Reachable via |
|---|---|
| `aurobindo-kapali-sastry-mishra-vedic-lineage` | `modern-sanskrit-lineage-roles` |
| `dayananda-rgvedadi-bhashya` | `modern-sanskrit-lineage-roles` |
| `kak-vedic-structural-architecture` | `modern-sanskrit-lineage-roles` |
| `kapoor-text-and-interpretation` | `modern-sanskrit-lineage-roles` |
| `malhotra-battle-for-sanskrit-pollock-prosecution` | `modern-sanskrit-lineage-roles` |
| `ojha-vedic-architecture-corpus` | `modern-sanskrit-lineage-roles` |
| `jones-1786-third-anniversary-discourse` | `jones-1786-anniversary-address` |
| `rigveda-10-125-vak-ambhrini` | `rigveda-10-71-4-vach` |
| `staal-mendeleev-varga-comparison` | `vyanjana-duration-shiksha` |
| `western-linguistic-encounter-sanskrit-1786-1879` | Directly deployed in Chapter 20 §20.2 and reachable through `place-of-articulation-sanskrit-terms` |
| `yaska-deva-derivation` | `deva-sur-div-radiance-field` |

This also settles four of the entries listed "not tested" in Category D. The remaining pair has now been redeployed in Chapter 20 §20.2, with `ipa-1886-founding-1888-chart` corrected and renamed `ipa-1886-1900-chart`.

### 2. The Chapter 9 cluster — cause found, material recovered

The Ch 9 orphans were not a slow drift. They were created in a single commit:

> `1a7cb0f5` — **"Ch 8 & Ch 9: figure-caption sync + scare-quote convention + minor
> polish"**, 2026-06-08. 123 insertions, **181 deletions.**

Under "minor polish" that commit deleted **TABLE 9.1**, the regional-features survey
added three weeks earlier by "Ch09: Tier 3 addback". Four endnotes cite claims that
existed only in that table:

| Endnote | Table row it supported |
|---|---|
| `pahari-tonal-features` | Himalayan frontier — "Pahari tonal features" |
| `punjabi-tonal-development` | Indo-Gangetic — "Punjabi three-way lexical tone" |
| `bengali-va-ba-merger` | Eastern subcontinent — "Bengali व/ब labial merger" |
| `south-indian-mahaprana-loan-only` | Southern — *mahāprāṇa* "not native (Sanskrit loans only)" |

That date is the first of the two bursts in the trend table above: orphans **2 → 15**.

**The cut was never logged.** CLAUDE.md requires material to be copied into a recovery
ledger before removal; no ledger holds this table, and no working file contains the
phrases "labial merger", "three-way lexical tone", or "Pahari tonal". Git had it, but
the ledger — the thing the rule exists to guarantee — did not.

**Recovered 2026-08-22** in full to
`working/40_reference/source_material/ch9_regional_features_lost_and_found_2026-06-08.md`.
This follows the precedent already set by `hlad-contrast-atom`, which parks cleanly
against `ch12_pre_vedic_breadth_rewrite_*`.

One row in the recovered table bears on open work: **"Tamil ற alveolar trill"** — the
same ற் raised on 2026-08-21 when checking Tamil's liquids against the *varṇamālā*.
The book had that observation and lost it.

### 3. Nine parked entries now declare themselves

The nine Category B stubs stated their parked status only in prose inside their
Deployments line, so every audit re-flagged them and a human had to re-read nine
reasons. Each now carries a machine-readable field, matching the format
`hlad-contrast-atom` already used:

```
**Status:** Parked — intentionally undeployed; retained source material.
```

`hlad-contrast-atom` was itself already parked (`**Status:** Parked after the Chapter
12 Vedic-breadth rewrite.`), so it leaves the decision list too — Category D loses one.

**Net: 33 open → 12 needing a decision.**

---

## The 12 that need a decision

| Stub | Target | Situation |
|---|---|---|
| ~~`south-indian-mahaprana-loan-only`~~ | Ch 8 §8.5 | **RESOLVED — relinked.** See *Third pass* |
| ~~`pahari-tonal-features`~~ | — | **RETIRED** against the ledger |
| ~~`punjabi-tonal-development`~~ | — | **RETIRED** against the ledger |
| ~~`bengali-va-ba-merger`~~ | — | **RETIRED** against the ledger |
| ~~`architecture-not-analysis-pratisakhya`~~ | Chapter 9 §9.4 | **RESOLVED — relinked to the passage distinguishing acoustic confirmation from architectural creation.** |
| ~~`varnamala-grid-geometry`~~ | Chapter 9 §9.4 | **RESOLVED — relinked to the five anatomical distances.** |
| ~~`formants-source-filter-theory`~~ | Chapter 9 §9.4 | **RESOLVED — relinked to the vocal-tract filtering explanation.** |
| ~~`history-of-linguistics-sanskrit-influence`~~ | Chapter 20 §20.2 | **RESOLVED — redeployed in “The Pyramid Steals the Sonomer.”** |
| ~~`ipa-1886-1900-chart`~~ | Chapter 20 §20.2 | **RESOLVED — corrected and redeployed.** |
| ~~`sanskrit-field-52b-reach`~~ | Chapter 0 §0.3 | **RESOLVED — retired; source material archived in `working/40_reference/source_material/sanskrit_52b_reach_retired_endnote.md`.** |
| ~~`pratisakhya-bhashyam-chandasi`~~ | Chapter 9 §9.10 | **RESOLVED — retired and merged into `agnimile-rigveda-opening`, which cites the exact *Ṛgveda-Prātiśākhya* 1.11–12 rule.** |
| ~~`kailasa-temple-ellora-engineering`~~ | Chapter 18 opening | **RESOLVED — relinked to the Kailasa architectural-test passage.** |

All twelve entries now have a recorded disposition.

---

## Third pass (2026-08-22) — the TABLE 9.1 group settled

### The chapter split is why the trail went cold

The commit that deleted TABLE 9.1 was a figure-conversion pass, and it converted one
table correctly: the sonomer-duration table became **Figure 9.7, *Mātrā Duration***.
TABLE 9.1 got no such treatment. The same commit also deleted the placeholder that
would have carried it visually — *"FIGURE 9.1: The subcontinental sound-field — map of
the subcontinent by region, marking retroflex distribution…"*. Table and figure went
together, and the new Figures 9.1–9.6 took the numbering with unrelated content. None
of Chapter 9's thirteen current figures is regional.

Compounding it, the old `as_1_09_superset.md` later **split into Chapter 8**
(`as_1_08_superset.md`) **and Chapter 9** (`as_1_09_mapping_mouth.md`). The four
endnotes point at "Ch 9 §9.3 / §9.5" — an address that no longer means what it meant
when they were written. Any audit keyed to the recorded target was looking in the
wrong chapter.

### One relinked — a real gap in Chapter 8

`south-indian-mahaprana-loan-only` **was a live defect, not a stranded citation.**
Chapter 8's four coverage surveys count against a 23-cell base with the ten
*mahāprāṇa* cells set aside. The chapter states the set-aside at §8.5 and again at
§8.7 but never justifies it, so a reader asking "why 23 and not 33?" gets no answer
and the trimmed base looks chosen to flatter the result. The justification is exactly
what the orphaned endnote supplies: the southern languages use *mahāprāṇa* only in
*tatsama* loans.

Marker attached at `manuscript/as_1_08_superset.md:73`; Deployments retargeted
Ch 9 §9.3 → Ch 8 §8.5 with the move recorded in the entry. Same defect class as A2
(`ross-metatypy-takia`): chapter moved, marker not carried.

### Three retired — no host text, and the replacement is better

`pahari-tonal-features`, `punjabi-tonal-development`, and `bengali-va-ba-merger` have
nothing to relink to. Punjabi and Bengali survive in Chapter 8 in a single sentence,
and it says those languages are *excluded* from the surveys. Restoring the citations
would mean writing new prose, not re-attaching markers.

Restoring the table is also the weaker move. Chapter 8 now counts cell coverage
against real language data — 22, 20, 16, and 15 of 23 — which is evidence; a survey
row asserting "Punjabi three-way lexical tone" is a list. The two tone rows fit worst:
tone is not a *varṇamālā* coordinate, so those rows raised a feature Sanskrit's grid
does not encode and then did nothing with it.

All three now carry `**Status:** Retired 2026-08-22` with a pointer to the ledger. The
material is not lost — the ledger holds the table in full.

**Open: 12 → 8.**

---

## Fourth pass (2026-08-22) — the decision queue closed

The remaining Chapter 9 notes were reattached to §9.4: `varnamala-grid-geometry`
supports the anatomical spacing, `formants-source-filter-theory` supports the
vocal-tract filtering explanation, and `architecture-not-analysis-pratisakhya`
supports the distinction between modern confirmation and architectural creation.

The two history-of-linguistics notes now support Chapter 20 §20.2. The older
`pratisakhya-bhashyam-chandasi` note was superseded by
`agnimile-rigveda-opening`, which quotes the exact *Ṛgveda-Prātiśākhya* 1.11–12
rule. `kailasa-temple-ellora-engineering` now supports the opening architectural
test in Chapter 18.

The final undecided entry, `sanskrit-field-52b-reach`, was retired. Chapter 0 now
demonstrates Sanskrit's reach through evidence already available to the reader.
The aggregate depended on the Radiance Thesis before the book had established it,
combined overlapping populations, and treated residence within a transmission
zone as evidence of Sanskrit's reach. Its source material is preserved in
`working/40_reference/source_material/sanskrit_52b_reach_retired_endnote.md`.

**Open: 8 → 0.**

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
| ~~`architecture-not-analysis-pratisakhya`~~ | Chapter 9 §9.4 | **RESOLVED — relinked.** |
| `staal-mendeleev-varga-comparison` | Ch 9 §9.4 | no — Staal/Mendeleev absent |
| ~~`varnamala-grid-geometry`~~ | Chapter 9 §9.4 | **RESOLVED — relinked.** |
| `bengali-va-ba-merger` | Ch 9 §9.3 | no — Bengali absent |
| `south-indian-mahaprana-loan-only` | Ch 9 §9.3 | no |
| `pahari-tonal-features` | Ch 9 §9.5 | no — tone absent |
| `punjabi-tonal-development` | Ch 9 §9.5 | no — tone absent |
| ~~`formants-source-filter-theory`~~ | Chapter 9 §9.4 | **RESOLVED — relinked.** |
| ~~`sanskrit-field-52b-reach`~~ | Chapter 0 §0.3 | **RESOLVED — retired and archived.** |
| `yaska-deva-derivation` | Ch 0 §0.3 | no |
| `rigveda-10-125-vak-ambhrini` | Preface | no — the "only men see" passage moved |
| ~~`pratisakhya-bhashyam-chandasi`~~ | Chapter 9 §9.10 | **RESOLVED — merged into `agnimile-rigveda-opening`.** |
| `hlad-contrast-atom` | Ch 12 §12.3 | no — §12.3 is now "From *Śabda* to *Padam*"; the *hlād* contrast was cut in the Ch 12 rewrite |
| ~~`dcs-vs-dhatupatha-count`~~ | Ch 11 §11.5 | **RESOLVED** — redeployed in App 6, as predicted; the reactivity tiers moved there from Ch 11 §11.5 |
| ~~`cross-gana-column-distribution`~~ | App 6 §§6.2, 6.4 | **RESOLVED** — redeployed in App 6 |
| ~~`generative-reach-inversion-natural-language`~~ | App 6 §6.3 | **RESOLVED** — redeployed in App 6 |
| ~~`history-of-linguistics-sanskrit-influence`~~ | Chapter 20 §20.2 | **RESOLVED** |
| ~~`ipa-1886-1900-chart`~~ | Chapter 20 §20.2 | **RESOLVED** |
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
| B. Parked by decision | 9 → **10** | none — declared via `**Status:** Parked` |
| C. Reachable from a deployed endnote | 6 → **11** | none — two-level citation, working as intended |
| D. Stranded by restructure | 20 → **7** | read target, then redeploy or retire |
| E. No record | 1 | consider Ch 6 §6.1 |
| F. Retired against a ledger | **3** | none — declared via `**Status:** Retired` |
| | **39 → 8 open** | |

**Four defects fixed** — the three in Category A, plus `south-indian-mahaprana-loan-only`,
which turned out to be a missing justification in Chapter 8 rather than a stranded
citation. 24 entries are working as intended: 10 parked, 11 reachable through a citation
chain, 3 retired against the ledger.

**8 remain**, and they collapse into **six** decisions, since the two App 3 §3.8 stubs
settle together.

The headline number was never 39 real problems. It was 4 defects, 24 entries in order,
and a handful of open questions — and the audit could not tell them apart because it
tested the wrong condition. Each defect it did contain was found by reading the
manuscript, not by counting stubs.

---

## Recommendation: make this self-checking

The audit above is a fifteen-line script. Adding it to the build — or to
`working/tools/` — would surface a lost marker in the commit that causes it, rather
than three months later. The check that matters is not "is a stub unused" but **"is a
stub's recorded Deployments target still present, and does it still carry the
marker?"** — that is precisely the condition that caught A1, A2, and A3.

**Done 2026-08-22.** Thirteen entries now declare their state in a machine-readable
field, so the check skips them by declaration rather than by a human re-reading a
reason each time. Two tokens are in use and the check should skip both:

- `**Status:** Parked` — intentionally undeployed, retained for possible future use (10).
- `**Status:** Retired` — the claim is not returning; material preserved in a ledger (3).

The audit's condition should be **"orphaned, undeclared, and not reachable from a
deployed endnote"** — that is what reduces 39 to 8. Testing bare `[NOTE:]` presence
produced 21 false positives.

One further lesson from the third pass: a stub's recorded Deployments target can be
stale in a way that hides a real defect. `south-indian-mahaprana-loan-only` pointed at
a chapter that had since split in two, so the audit looked in the wrong file and the
missing justification in Chapter 8 went unseen. Chapter renames and splits should
trigger a Deployments sweep.

### Method note

The keyword test used for Category D matched substrings, so `Ross` matched inside
*across* and *cross* and produced a false positive on `ross-metatypy-takia`. That
one was caught and corrected by hand — which is how A2 was found. Entries marked
"not tested" above were not keyword-checked at all and should be read directly. Any
re-run of this analysis should use word-boundary matching.
