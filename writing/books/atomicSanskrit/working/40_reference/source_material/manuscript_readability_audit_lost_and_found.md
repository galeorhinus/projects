# Manuscript Readability Audit — Lost and Found

*Active recovery ledger for material removed through the Codex readability review. Nothing substantive leaves the manuscript silently.*

## Purpose

The chapter review files preserve each original passage beside a proposed revision, but the number and distribution of those files make it difficult to review everything that disappears. This ledger gathers removed material in one place so the author can decide whether it should:

- return to its original location;
- move to another chapter;
- become an endnote, figure caption, appendix passage, or later-volume seed;
- remain cut;
- receive another revision.

The ledger records removal; it does not presume that removal was correct.

## What Must Be Logged

Create an entry before applying an audit revision whenever the revision removes or materially narrows any:

- complete sentence or clause;
- claim, inference, qualification, or limitation;
- example, analogy, comparison, or counterexample;
- quotation, mantra, citation, note anchor, or source reference;
- definition, term installation, refrain, or rhetorical beat;
- heading, figure, caption, table row, list item, or cross-reference;
- historical detail, personal memory, or civilizational argument.

Ordinary copyediting does not require an entry when the new sentence preserves the complete meaning and changes only grammar, spelling, rhythm, or word choice. The audit block must mark that case **REPHRASE — NO SUBSTANTIVE CUT**. When reasonable readers could disagree about whether meaning survived, log the material.

Material moved intact is not a cut, but the ledger must still record the move and its destination so it cannot become lost during structural editing.

## Application Gate

The sequence is mandatory:

1. identify what will disappear;
2. copy the exact material into this ledger;
3. assign a Lost and Found ID;
4. link that ID from the audit block and application manifest;
5. apply the manuscript revision;
6. record the new manuscript location and disposition.

An accepted audit block with **CUT**, **CONDENSE**, or **MOVE** impact cannot be applied without a Lost and Found ID. Nothing gets cut first and reconstructed later from Git history.

## Author Decisions

Use one disposition for each entry:

- `[ ] RESTORE IN PLACE`
- `[ ] RELOCATE`
- `[ ] INCORPORATE PART`
- `[ ] DEVELOP LATER`
- `[ ] KEEP CUT`
- `[ ] REVISE AGAIN`
- `[ ] UNDECIDED`

Author comments control the next action. Codex does not infer a disposition from edits made elsewhere.

## Backfill Queue

### Application batch of 2026-07-23

**Status:** COMPLETE — all 74 applied revisions classified; 32 recovery entries created

The application manifest records 74 applied revisions from review files 01–22, including structural consolidations and contradiction repairs. Every applied original has now been compared with the resulting manuscript text. Forty-two blocks preserve their substance through rephrasing, expansion, or structural treatment; thirty-two blocks have recovery entries below for material that moved, narrowed, disappeared, or was superseded.

Source: [`31_application_manifest.md`](../../80_completed/manuscript_readability_review_codex/31_application_manifest.md)

### Open review files 23–28

**Status:** GATED

No accepted revision from Chapters 18–19, the Epilogue, remaining front/back matter, appendices, endnotes, captions, or global decisions may be applied until every proposed cut has an entry here.

## Backfill Record

### Pass 1 — Audits 01–06

| Audit block | Source unit | Cut impact | Lost and Found entry | Status |
|---|---|---|---|---|
| AS-001 | About the Series | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| AS-002 | About the Series | Condense | [LAF-R-001](#laf-r-001--alignment-and-welfare-across-generations) | REVIEW REQUIRED |
| AS-003 | About the Series | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| PF-002 | Preface | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| PF-003 | Preface | Narrow claim | [LAF-R-002](#laf-r-002--the-lineage-does-not-claim-invention) | REVIEW REQUIRED |
| PF-005 | Preface | Narrow contrast | [LAF-R-003](#laf-r-003--preservation-machinery-rather-than-cultural-ornament) | REVIEW REQUIRED |
| PF-006 | Preface | Move heading | [LAF-R-004](#laf-r-004--what-follows-heading) | MOVE CONFIRMED |
| OV-001 | Overture | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| OV-002 | Overture | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C00-001 | Chapter 0 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C00-002 | Chapter 0 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C00-004 | Chapter 0 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C00-005 | Chapter 0 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C00-006 | Chapter 0 | Condense | [LAF-R-005](#laf-r-005--the-transmission-exists-now) | REVIEW REQUIRED |
| C01-001 | Chapter 1 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C01-002 | Chapter 1 | Reframe and expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C01-003 | Chapter 1 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C01-004 | Chapter 1 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C01-005 | Chapter 1 | Condense | [LAF-R-006](#laf-r-006--stories-as-diagnostic-recipes) | REVIEW REQUIRED |
| C01-006 | Chapter 1 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |

### Pass 2 — Audits 07–12

| Audit block | Source unit | Cut impact | Lost and Found entry | Status |
|---|---|---|---|---|
| C02-001 | Chapter 2 | Rephrase and expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C02-002 | Chapter 2 | Move detail | [LAF-R-007](#laf-r-007--esperanto-inventory-counts) | MOVE CONFIRMED |
| C02-003 | Chapter 2 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C02-004 | Chapter 2 | Rephrase and correct perspective | — | REPHRASE — NO SUBSTANTIVE CUT |
| C02-005 | Chapter 2 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C03-001 | Chapter 3 | Rephrase, then contradiction repair | — | REPHRASE — NO SUBSTANTIVE CUT AFTER REPAIR |
| C03-002 | Chapter 3 | Condense | [LAF-R-008](#laf-r-008--the-pre-emptive-enclosure) | REVIEW REQUIRED |
| C03-003 | Chapter 3 | Condense examples | [LAF-R-009](#laf-r-009--lexical-memory-and-the-reciter) | REVIEW REQUIRED |
| C03-004 | Chapter 3 | Clarify attribution | — | REPHRASE — NO SUBSTANTIVE CUT |
| C04-002 | Chapter 4 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C04-003 | Chapter 4 | Rephrase and expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C04-004 | Chapter 4 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C04-005 | Chapter 4 | Narrow accusation and close | [LAF-R-010](#laf-r-010--refusal-and-the-false-premise) | REVIEW REQUIRED |
| C05-001 | Chapter 5 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C05-002 | Chapter 5 | Move names | [LAF-R-011](#laf-r-011--pre-paninian-analysts) | MOVE CONFIRMED |
| C06-002 | Chapter 6 | Rephrase, then contradiction repair | — | REPHRASE — NO SUBSTANTIVE CUT AFTER REPAIR |
| C06-003 | Chapter 6 | Expand and reorganize | — | REPHRASE — NO SUBSTANTIVE CUT |
| C07-001 | Chapter 7 | Withdraw literal descent claim | [LAF-R-012](#laf-r-012--instruments-as-partial-descendants-of-the-voice) | REVIEW REQUIRED |
| C07-002 | Chapter 7 | Move measurements | [LAF-R-013](#laf-r-013--vocal-tract-measurements) | MOVE CONFIRMED |
| C07-003 | Chapter 7 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |

### Pass 3 — Audits 13–17

| Audit block | Source unit | Cut impact | Lost and Found entry | Status |
|---|---|---|---|---|
| C08-001 | Chapter 8 | Rephrase and expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C08-003 | Chapter 8 | Narrow inference | [LAF-R-014](#laf-r-014--anchored-geography) | REVIEW REQUIRED |
| C09-002 | Chapter 9 | Reframe without chronology | — | REPHRASE — NO SUBSTANTIVE CUT |
| C09-003 | Chapter 9 | Add subheadings | — | STRUCTURE — NO CUT |
| C09-004 | Chapter 9 | Condense and narrow | [LAF-R-015](#laf-r-015--script-as-procedural-implementation) | REVIEW REQUIRED |
| C10-001 | Chapter 10 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C10-002 | Chapter 10 | Merge and condense | [LAF-R-016](#laf-r-016--sūtra-lāghavam-and-the-fractal-definition) | REVIEW REQUIRED |
| C10-003 | Chapter 10 | Bound analogy | [LAF-R-017](#laf-r-017--furnace-laboratory-body-sentence) | REVIEW REQUIRED |
| C11-001 | Chapter 11 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C11-002 | Chapter 11 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C11-003 | Chapter 11 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C11-004 | Chapter 11 | Explain statistic | — | REPHRASE — NO SUBSTANTIVE CUT |
| C11-005 | Chapter 11 | Narrow inference | [LAF-R-018](#laf-r-018--c4-as-a-strict-functional-placement) | REVIEW REQUIRED |
| C12-001 | Chapter 12 | Install replacement term | — | REPHRASE — NO SUBSTANTIVE CUT |
| C12-002 | Chapter 12 | Narrow interpretation, then contradiction repair | [LAF-R-019](#laf-r-019--the-lower-fractal-scale) | REVIEW REQUIRED |
| C12-003 | Chapter 12 | Correct and narrow ending description | [LAF-R-020](#laf-r-020--relation-in-the-verbal-ending) | REVIEW REQUIRED |
| C12-004 | Chapter 12 | Explain model boundary | — | REPHRASE — NO SUBSTANTIVE CUT |
| C12-005 | Chapter 12 | Rename heading | — | STRUCTURE — NO SUBSTANTIVE CUT |

### Pass 4 — Audits 18–22 and contradiction repairs

| Audit block | Source unit | Cut impact | Lost and Found entry | Status |
|---|---|---|---|---|
| C13-001 | Chapter 13 | Replace aphorism | [LAF-R-021](#laf-r-021--a-calibrant-calibrated-by-what-it-calibrates) | REVIEW REQUIRED |
| C13-003 | Chapter 13 | Correct broad contrast | [LAF-R-022](#laf-r-022--what-the-ear-catches) | REVIEW REQUIRED |
| C14-001 | Chapter 14 | Expand and label coinages | — | REPHRASE — NO SUBSTANTIVE CUT |
| C14-003 | Chapter 14 | Move dates and catalogues | [LAF-R-023](#laf-r-023--benchmark-preservation-details) | MOVE CONFIRMED |
| C15-002 | Chapter 15 | Expand | — | REPHRASE — NO SUBSTANTIVE CUT |
| C15-003 | Chapter 15 | Remove industrial image | [LAF-R-024](#laf-r-024--immediate-correction-and-the-welded-chain) | REVIEW REQUIRED |
| C15-004 | Chapter 15 | Narrow inference | [LAF-R-025](#laf-r-025--the-priority-of-śikṣā) | REVIEW REQUIRED |
| C15-006 | Chapter 15 | Condense mechanism | [LAF-R-026](#laf-r-026--what-reversal-tests) | REVIEW REQUIRED |
| C15-007 | Chapter 15 | Condense evidence, then contradiction repair | [LAF-R-027](#laf-r-027--the-full-empirical-verification-claim) | REVIEW REQUIRED |
| C16-002 | Chapter 16 | Move and condense anatomy | [LAF-R-028](#laf-r-028--the-mouth-field-is-older-than-the-taxonomy) | REVIEW REQUIRED |
| C16-003 | Chapter 16 | Narrow synthesis | [LAF-R-029](#laf-r-029--one-sonomer-across-four-levels) | REVIEW REQUIRED |
| C16-006 | Chapter 16 | Rephrase | — | REPHRASE — NO SUBSTANTIVE CUT |
| C16-007 | Chapter 16 | Remove workshop image, then contradiction repair | [LAF-R-030](#laf-r-030--the-continuous-return-to-the-workshop) | REVIEW REQUIRED |
| C16-008 | Chapter 16 | Merge and remove repeated recap | [LAF-R-031](#laf-r-031--the-second-five-feature-recap) | REVIEW REQUIRED |
| C17-006 | Chapter 17 | Rephrase, then contradiction repair | — | REPHRASE — NO SUBSTANTIVE CUT AFTER REPAIR |
| C19-003 | Chapter 19 | Correct chronology contradiction | [LAF-R-032](#laf-r-032--the-pre-vedic-mitanni-claim) | SUPERSEDED CLAIM RECORDED |

#### Contradiction repairs

| Repair | Result | Cut impact |
|---|---|---|
| A1 — Chapter 16 portability routes | Restored an affirmative conclusion for both timing routes | NO SUBSTANTIVE CUT |
| A2 — Chapter 3 Biblical chronology | Restored the surviving clock after its Biblical label disappeared | NO SUBSTANTIVE CUT |
| A3 — Chapter 15 exact recurrence | Restored exactness within a specified *śākhā* and governed differences across branches | NO SUBSTANTIVE CUT |
| A4 — Chapter 12 Vedic operation | Restored the mantra as evidence rather than decoration | Remaining omissions logged in LAF-R-019 |
| A5 — Chapter 17 completed test | Restored the test as completed rather than pending | NO SUBSTANTIVE CUT |
| A6 — Chapter 6 Patañjali | Restored Patañjali's prior architectural analysis | NO SUBSTANTIVE CUT |

### Remaining Backfill

| Audit range | Status |
|---|---|
| Review files 01–22 and C19-003 | COMPLETE |
| Review files 23–27 | APPLICATION BLOCKED — ENTRIES REQUIRED AFTER AUTHOR ACCEPTANCE |
| Review file 28 | THREE EXACT PROPOSALS LOGGED; ALL OTHER GLOBAL WORK BLOCKED |

## Entries

Add entries in source order using the next available ID.

---

## LAF-R-001 — Alignment and welfare across generations

**Source:** [About the Series](/Users/paragtope/projects/writing/books/atomicSanskrit/as_0_00_about_series.md:25)  
**Audit block:** [AS-002](../../80_completed/manuscript_readability_review_codex/01_about_series.md#as-002---replace-the-repeated-architecture-summary-after-the-subtitle)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Its radiant, calibrant, and fractal architecture forms the linguistic foundation of *Sanātan* by preserving a measure, distributing correction, inspiring alignment, and remaining directed toward welfare across generations.

### Replacement or Result

The replacement explains *radiant*, *calibrant*, and *fractal* separately, but it no longer states that the architecture inspires alignment or remains directed toward welfare across generations.

### Reason Proposed

The audit replaced a repeated architecture summary with a concrete explanation of the subtitle.

### What May Have Been Lost

The connection between calibration and welfare across generations may be important to the later civilizational volumes. The replacement explains mechanism more clearly but narrows purpose.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-002 — The lineage does not claim invention

**Source:** [Preface](/Users/paragtope/projects/writing/books/atomicSanskrit/as_0_01_preface.md:88)  
**Audit block:** [PF-003](../../80_completed/manuscript_readability_review_codex/02_preface.md#pf-003---describe-the-lineage-through-its-work)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Every *vaiyākaraṇaḥ* in the chain decodes; none claims to invent.

### Replacement or Result

> Each *vaiyākaraṇaḥ* in the chain decodes and explains that established architecture.

### Reason Proposed

The audit described the lineage through audible and analytical actions.

### What May Have Been Lost

The replacement preserves decoding and explanation but removes the explicit contrast with invention. That contrast supports the book's repeated distinction between documentation and codification.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-003 — Preservation machinery rather than cultural ornament

**Source:** [Preface](/Users/paragtope/projects/writing/books/atomicSanskrit/as_0_01_preface.md:92)  
**Audit block:** [PF-005](../../80_completed/manuscript_readability_review_codex/02_preface.md#pf-005---unpack-the-architecture-across-scale)  
**Change type:** NARROW CONTRAST  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> the Vedic recitation systems are preservation machinery rather than cultural ornament.

### Replacement or Result

> the Vedic recitation systems keep it audible through a set of mutually checking procedures.

### Reason Proposed

The audit replaced the categorical contrast with an explanation of what the procedures do.

### What May Have Been Lost

The new wording explains preservation more clearly, but the direct rejection of the “cultural ornament” category disappeared.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-004 — “What Follows” heading

**Source:** [Preface](/Users/paragtope/projects/writing/books/atomicSanskrit/as_0_01_preface.md:98)  
**Audit block:** [PF-006](../../80_completed/manuscript_readability_review_codex/02_preface.md#pf-006---merge-the-final-heading-into-lineage-and-method)  
**Change type:** MOVE  
**Status:** MOVE CONFIRMED  
**Applied:** YES  
**Destination if moved:** The two closing paragraphs remain under `## Lineage and Method`.

### Material Removed

> ## What Follows

### Replacement or Result

Only the heading was removed. Its two paragraphs remain intact as the close of the preceding section.

### Reason Proposed

The short final section interrupted the Preface close without adding a distinct argumentative unit.

### What May Have Been Lost

No prose was lost. The explicit navigation label disappeared.

### Author Decision

- [ ] RESTORE IN PLACE
- [x] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [ ] UNDECIDED

### Author Comments

```text
The material remains in place under the preceding heading.
```

---

## LAF-R-005 — The transmission exists now

**Source:** [Chapter 0](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_00_seekers.md:153)  
**Audit block:** [C00-006](../../80_completed/manuscript_readability_review_codex/04_ch00.md#c00-006---consolidate-the-present-day-transmission-statement)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The transmission is operating now, audibly. The recordings exist. The lineages exist. The transmission exists.

### Replacement or Result

> Recordings now let people outside the lineages hear the living transmission for themselves.

### Reason Proposed

The audit consolidated four short declarations into one explanatory sentence.

### What May Have Been Lost

The replacement preserves the present-day and audible claims, but it removes the repeated hammer that insists on the continued existence of both lineages and transmission.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-006 — Stories as diagnostic recipes

**Source:** [Chapter 1](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_01_one_oppressors_finite.md:93)  
**Audit block:** [C01-005](../../80_completed/manuscript_readability_review_codex/05_ch01.md#c01-005---explain-what-the-operations-list-demonstrates)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Each story works as both memory and diagnostic recipe, while the varied casts teach successive generations to recognize the same asuric operation beneath a new costume.

### Replacement or Result

> Each story preserves a way to recognize an asuric action when it appears under a new costume.

### Reason Proposed

The audit prepared the reader for the operations list in more direct language.

### What May Have Been Lost

The replacement keeps recognition across changing costumes, but it removes the “diagnostic recipe” formulation and the role played by varied casts across successive generations.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-007 — Esperanto inventory counts

**Source:** [Chapter 2](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_02_botanical.md:59)  
**Audit block:** [C02-002](../../80_completed/manuscript_readability_review_codex/07_ch02.md#c02-002---shorten-the-numerical-esperanto-comparison-in-the-body)  
**Change type:** MOVE  
**Status:** MOVE CONFIRMED  
**Applied:** YES  
**Destination if moved:** Endnote `esperanto-engineered-botanical-transition`

### Material Removed

> Esperanto began with about forty productive affixes and 2,768 foundational lexical elements, both larger inventories than Sanskrit's twenty-two *upasargāḥ* and 2,168 listed *dhātavaḥ*, although the two systems do not classify these resources identically.

### Replacement or Result

The body keeps the comparison between Esperanto's plan and its botanical transition. The counts and the warning that the two inventories classify resources differently now appear in the endnote.

### Reason Proposed

The numerical comparison interrupted the Chapter 2 explanation and required qualifications better suited to the Source and Reference Companion.

### What May Have Been Lost

Nothing is untracked. The visual numerical resemblance no longer appears in the body.

### Author Decision

- [ ] RESTORE IN PLACE
- [x] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [ ] UNDECIDED

### Author Comments

```text
Moved to endnote `esperanto-engineered-botanical-transition`.
```

---

## LAF-R-008 — The pre-emptive enclosure

**Source:** [Chapter 3](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_03_strategic.md:37)  
**Audit block:** [C03-002](../../80_completed/manuscript_readability_review_codex/08_ch03.md#c03-002---show-how-accepted-categories-prevent-the-thesis-from-forming)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The discipline has not opposed the engineered Sanskrit thesis; until now, there has been no engineered Sanskrit thesis to oppose. Its defense is pre-emptive.

### Replacement or Result

The current two-paragraph explanation shows how inherited categories reach the student before the evidence and prevent the alternative account from being assembled. It no longer calls that defense “pre-emptive.”

### Reason Proposed

The audit replaced an abstract account of enclosure with the sequence a student actually encounters.

### What May Have Been Lost

The causal mechanism remains, but the explicit indictment that the defense precedes the thesis has disappeared.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-009 — Lexical memory and the reciter

**Source:** [Chapter 3](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_03_strategic.md:129)  
**Audit block:** [C03-003](../../80_completed/manuscript_readability_review_codex/08_ch03.md#c03-003---split-the-two-kinds-of-shared-sound-form)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> the **अमरकोश (*Amarakośa*)**, the most-memorized thesaurus in the lineage-chain
>
> **गो (*go*)** is cow, and earth, and speech, and the ray of light — one form, four referents, and the reciter holds all four without strain. **हरि (*hari*)** is Viṣṇu, and Indra, and lion, and horse, and the color green — one form, and the verse settles which.
>
> That is precisely the distinction the pyramid's reversal-story needs and will not draw.

### Replacement or Result

The revised passage retains the *Amarakośa*, the examples of *go* and *hari*, contextual selection of meaning, and the distinction between one word with several senses and several words sharing one sound-form. It removes the memorization detail, the reciter's ease, and the direct accusation attached to the distinction.

### Reason Proposed

The audit separated the two lexical relations and explained them in ordinary prose.

### What May Have Been Lost

The present wording is clearer analytically but less connected to lived recitation, civilizational memory, and the pyramid's motive for refusing the distinction.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-010 — Refusal and the false premise

**Source:** [Chapter 4](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_04_fourth_abrahamic.md:168)  
**Audit block:** [C04-005](../../80_completed/manuscript_readability_review_codex/09_ch04.md#c04-005---unpack-authorship-preservation-and-apex-authority)  
**Change type:** NARROW CLAIM AND CLOSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The *Vedas* break this chain of command; thus, because the pyramid cannot control them, it refuses to accept them.
>
> Order at architectural scale can be maintained without pyramidal authority. The premise is false.

### Replacement or Result

The revised passage explains why *apauruṣeya* gives the pyramid no author or original office to capture and presents distributed Vedic preservation as evidence that architectural order can persist without an apex. It no longer states that the pyramid refuses the Vedas because it cannot control them, and it removes the final verdict.

### Reason Proposed

The audit unpacked the relationship among authorship, custody, preservation, and apex authority.

### What May Have Been Lost

The mechanism is clearer, but the pyramid's refusal and the categorical rejection of its premise are less forceful.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-011 — Pre-Pāṇinian analysts

**Source:** [Chapter 5](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_05_siddha.md:29)  
**Audit block:** [C05-002](../../80_completed/manuscript_readability_review_codex/10_ch05.md#c05-002---keep-śākalya-in-the-body-and-move-the-catalogue-into-the-note)  
**Change type:** MOVE  
**Status:** MOVE CONFIRMED  
**Applied:** YES  
**Destination if moved:** Endnote `panini-cites-pre-paninian-vaiyakaranas`

### Material Removed

> **Āpiśali** (आपिशलि), **Kāśyapa** (काश्यप), **Gārgya** (गार्ग्य), **Gālava** (गालव), **Cākravarmaṇa** (चाक्रवर्मण), **Bhāradvāja** (भारद्वाज), **Saunaga** (सौनाग), **Senaka** (सेनक), and **Sphoṭāyana** (स्फोटायन) are not decorative names. They are the documentary trace of a discipline already operating.

### Replacement or Result

Śākalya remains as the body example. The other analysts and their cited locations now appear in the endnote.

### Reason Proposed

The book's naming rule requires each person named in the body to be praised or shamed through a specific action. The endnote can connect every analyst to evidence without interrupting the main explanation.

### What May Have Been Lost

The body no longer delivers the roster as a collective rhetorical demonstration of prior analytical depth.

### Author Decision

- [ ] RESTORE IN PLACE
- [x] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [ ] UNDECIDED

### Author Comments

```text
Moved to endnote `panini-cites-pre-paninian-vaiyakaranas`.
```

---

## LAF-R-012 — Instruments as partial descendants of the voice

**Source:** [Chapter 7](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_07_adivadya.md:37)  
**Audit block:** [C07-001](../../80_completed/manuscript_readability_review_codex/12_ch07.md#c07-001---mark-the-instrument-comparisons-as-analogies)  
**Change type:** WITHDRAW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The voice is the original instrument; constructed instruments are partial descendants.

### Replacement or Result

The passage retains the voice as the original instrument and presents tabla, bansuri, and sarangi as explanatory analogies. It no longer claims that constructed instruments descend from separate capacities of the voice.

### Reason Proposed

The cited material supports the voice as the original instrument more securely than a literal historical descent for each constructed instrument.

### What May Have Been Lost

The revision narrows the historical claim while preserving the anatomical analogy. The author may prefer to restore “partial descendants” if the endnote can support it.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-013 — Vocal-tract measurements

**Source:** [Chapter 7](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_07_adivadya.md:45)  
**Audit block:** [C07-002](../../80_completed/manuscript_readability_review_codex/12_ch07.md#c07-002---remove-centimeter-ranges-from-the-anatomy-lesson)  
**Change type:** MOVE  
**Status:** MOVE CONFIRMED  
**Applied:** YES  
**Destination if moved:** Endnote `vocal-tract-cm-modeling`

### Material Removed

> The distance from lips to glottis averages roughly seventeen centimeters in adult males, ~14–15 cm in adult females, and shorter still in children, with the adult range running from about 13 cm to about 20 cm.

### Replacement or Result

The body states that vocal tracts vary with age and body while using the same anatomical parts and operations. The numerical ranges and sources remain in the endnote.

### Reason Proposed

The measurements interrupted the first anatomy lesson and needed source qualifications.

### What May Have Been Lost

Nothing is untracked. The measurable physical scale no longer appears in the body.

### Author Decision

- [ ] RESTORE IN PLACE
- [x] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [ ] UNDECIDED

### Author Comments

```text
Moved to endnote `vocal-tract-cm-modeling`.
```

---

## LAF-R-014 — Anchored geography

**Source:** [Chapter 8](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_08_superset.md:207)  
**Audit block:** [C08-003](../../80_completed/manuscript_readability_review_codex/13_ch08.md#c08-003---replace-the-overwritten-score-summary)  
**Change type:** NARROW INFERENCE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> the sound-field behaves precisely like anchored geography rather than transported cargo.
>
> the closer the set is to the subcontinental field, the more of the Sanskrit base it naturally covers—and conversely, the farther the set moves from that field, the more the coverage precipitously falls

### Replacement or Result

The replacement gives the four scores and says that the proposed corridor resembles Sanskrit's selected base less than the southern and forest-belt fields do. It frames this as a physical problem for the transported-cargo thesis rather than as conclusive proof of anchored geography.

### Reason Proposed

The audit separated the measured comparison from the historical inference it supports.

### What May Have Been Lost

The result is more precisely bounded, but the chapter's affirmative interpretation of the geographical gradient has weakened.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-015 — Script as procedural implementation

**Source:** [Chapter 9](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_09_mapping_mouth.md:281)  
**Audit block:** [C09-004](../../80_completed/manuscript_readability_review_codex/14_ch09.md#c09-004---rewrite-varṇa-and-script-in-active-ordinary-prose)  
**Change type:** CONDENSE AND NARROW  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> once the *varṇamālā* fully exists, the script merely becomes implementation.
>
> representing those precise sounds with written symbols is just a trivial, procedural implementation of a scalable, fractal idea.
>
> By restoring the precise Sanskrit terms, the engineering immediately returns to focus, revealing that the glyphs are secondary while the sound-architecture is the true language.

### Replacement or Result

The revised section explains that sound precedes the glyph, script supplies a visible interface, and the interface can eclipse the physical architecture. It no longer calls the act of representation trivial or procedural, and it removes the explicit claim that restoring Sanskrit's terms restores the engineering to view.

### Reason Proposed

The audit replaced compressed contrast chains with an active, classroom-style explanation.

### What May Have Been Lost

The causal order remains clear, but the book's stronger evaluation of conceptual invention versus interface implementation has softened.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-016 — *Sūtra-lāghavam* and the fractal definition

**Source:** [Chapter 10](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_10_building_dhatuh.md:23)  
**Audit block:** [C10-002](../../80_completed/manuscript_readability_review_codex/15_ch10.md#c10-002---merge-the-repeated-design-test-introductions)  
**Change type:** MERGE AND CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Together, these six characteristics produce **सूत्रलाघवम् (*sūtra-lāghavam*)**: engineered brevity. The form is short, but the structure it holds is large. The *sūtra* is compact, clear, meaningful, wide-facing, economical, and stable.
>
> That recurrence defines **fractal** in the architectural sense: the same organizing principle appearing at different scales. What governs the *sūtra* should also be visible inside the *dhātuḥ*.

### Replacement or Result

The merged section keeps the six characteristics and explains that their recurrence in the *dhātuḥ* would show an organizing principle repeated across scale. It no longer introduces *sūtra-lāghavam* or defines *fractal* explicitly at this location.

### Reason Proposed

The two opening sections repeated the same design test and were merged.

### What May Have Been Lost

Two useful terms disappeared during consolidation: the Sanskrit name for engineered brevity and the concise definition of the book's architectural use of *fractal*.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-017 — Furnace, laboratory, body, sentence

**Source:** [Chapter 10](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_10_building_dhatuh.md:50)  
**Audit block:** [C10-003](../../80_completed/manuscript_readability_review_codex/15_ch10.md#c10-003---bound-the-chemistry-analogy)  
**Change type:** NARROW ANALOGY  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Furnace, laboratory, body, sentence: the same architectural word. The grammatical *dhātuḥ* belongs in that family. *Dhātuḥ* survives the botanical demotion; the discipline that accepts the demotion loses access to what the term denotes.

### Replacement or Result

The revised section explains the constituent sense of *dhātuḥ* in metallurgy, combination, medicine, and grammar, then states the limits of the chemistry analogy.

### Reason Proposed

The audit bounded the analogy so that particles, atoms, bonds, and molecules describe assembly without claiming that sound is matter.

### What May Have Been Lost

The explanation remains, but the memorable four-domain line and the consequence of accepting botanical demotion have disappeared.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-018 — C4 as a strict functional placement

**Source:** [Chapter 11](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_11_building_kriya.md:294)  
**Audit block:** [C11-005](../../80_completed/manuscript_readability_review_codex/16_ch11.md#c11-005---mark-the-c4-explanation-as-an-interpretation)  
**Change type:** NARROW INFERENCE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> That number is a procedural fit, not just a distribution fact.
>
> the architecture parks its most distinctive consonants exactly where the operation needs the most distinction. The sounds are distributed strictly by function.

### Replacement or Result

The revised passage says the concentration suggests a possible procedural fit and may help the consonants remain perceptually distinct. It states that the measured distribution alone cannot establish deliberate placement.

### Reason Proposed

The count demonstrates a distribution; intention requires additional evidence.

### What May Have Been Lost

The categorical design conclusion has been replaced by a bounded functional interpretation. This may be the correct evidentiary limit, but the stronger claim is now recoverable here for explicit author review.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-019 — The lower fractal scale

**Source:** [Chapter 12](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_12_building_vakya.md:29)  
**Audit block:** [C12-002](../../80_completed/manuscript_readability_review_codex/17_ch12.md#c12-002---explain-the-epigraph-as-an-application-not-a-literal-grammar-lesson)  
**Change type:** NARROW INTERPRETATION  
**Status:** UNDECIDED  
**Applied:** YES; later repaired by contradiction audit A4  
**Destination if moved:** —

### Material Removed

> The one who does not know what holds it cannot use it properly.
>
> the supreme ground is the **lower fractal** scale, found by going down, not up.

### Replacement or Result

The contradiction repair now states that the hierarchy itself operates in the mantra while the modern molecular terminology belongs to the book. It also explains that the supporting layer lies below the completed sentence even though the verse calls the ground the highest heaven. The two quoted conclusions do not return verbatim.

### Reason Proposed

The original audit tried to distinguish the mantra's wording from the book's explanatory model. The contradiction audit later restored the mantra's evidentiary role.

### What May Have Been Lost

The repaired passage preserves the architecture but not the direct claim about proper use or the “found by going down” formulation.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-020 — Relation in the verbal ending

**Source:** [Chapter 12](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_12_building_vakya.md:47)  
**Audit block:** [C12-003](../../80_completed/manuscript_readability_review_codex/17_ch12.md#c12-003---explain-what-tail-bonds-do)  
**Change type:** NARROW DESCRIPTION  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> a **तिङ्-प्रत्ययः (*tiṅ-pratyayaḥ*)** sets a verb's person, number, and relation.

### Replacement or Result

> a **तिङ्-प्रत्ययः (*tiṅ-pratyayaḥ*)** marks a verb's person and number.

### Reason Proposed

The revision removed the undefined and potentially misleading word “relation” while expanding the function of tail-bonds.

### What May Have Been Lost

If “relation” referred to voice, pada, or another recoverable grammatical value, it should be restored with the exact Sanskrit category rather than as an unexplained English term.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-021 — A calibrant calibrated by what it calibrates

**Source:** [Chapter 13](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_13_preservation.md:23)  
**Audit block:** [C13-001](../../80_completed/manuscript_readability_review_codex/18_ch13.md#c13-001---replace-the-compressed-calibrant-opener)  
**Change type:** REPLACE APHORISM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Because a specification that drifts is no longer a specification, it follows logically that a calibrant calibrated by what it calibrates is no longer a calibrant.

### Replacement or Result

The new opening explains that Sanskrit can remain a measure only while its sounds, relations, and forms stay stable enough to reveal change in ordinary speech.

### Reason Proposed

The audit replaced a compressed abstraction with a causal explanation.

### What May Have Been Lost

The explanatory content survives, but the concise paradox may be useful as a concluding hammer after the explanation.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-022 — What the ear catches

**Source:** [Chapter 13](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_13_preservation.md:107)  
**Audit block:** [C13-003](../../80_completed/manuscript_readability_review_codex/18_ch13.md#c13-003---distinguish-broad-oral-transmission-from-vedic-aural-precision)  
**Change type:** CORRECT BROAD CLAIM AND CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Oral tradition preserves content approximately: the story remains, the wording shifts; the song remains, the regional form varies; the meaning survives, the surface changes.
>
> The mouth produces. The ear preserves. The engineering is in what the ear catches that the mouth cannot be trusted to remember alone.

### Replacement or Result

The revised passage acknowledges that some oral systems preserve wording with high precision, then defines Vedic aural engineering through trained production and an independent auditory check.

### Reason Proposed

The original universal claim about oral transmission was too broad.

### What May Have Been Lost

The correction is necessary, but the final sentence's account of the ear as an independent safeguard may deserve a new version that does not depend on the inaccurate generalization.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-023 — Benchmark preservation details

**Source:** [Chapter 14](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_14_calibration.md:135)  
**Audit block:** [C14-003](../../80_completed/manuscript_readability_review_codex/19_ch14.md#c14-003---give-each-benchmark-tradition-its-own-paragraph)  
**Change type:** MOVE  
**Status:** MOVE CONFIRMED  
**Applied:** YES  
**Destination if moved:** Endnotes `masoretic-engineered-preservation`, `quranic-engineered-preservation`, and `latin-vulgate-engineered-preservation`

### Material Removed

The body removed the detailed dates, named codices, named institutional interventions, and full technical catalogues for Masoretic Hebrew, Quranic Arabic, and ecclesiastical Latin.

### Replacement or Result

Each comparison now has its own short paragraph. The named dates, manuscripts, councils, authorized editions, and technical inventories remain in the three endnotes.

### Reason Proposed

The body needed the structural comparison; the Source and Reference Companion can preserve the detailed chronology and sources.

### What May Have Been Lost

Nothing is untracked. The body no longer displays the density of datable institutional interventions.

### Author Decision

- [ ] RESTORE IN PLACE
- [x] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [ ] UNDECIDED

### Author Comments

```text
Moved to the three existing preservation endnotes.
```

---

## LAF-R-024 — Immediate correction and the welded chain

**Source:** [Chapter 15](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_15_aural.md:21)  
**Audit block:** [C15-003](../../80_completed/manuscript_readability_review_codex/20_ch15.md#c15-003---keep-the-public-audit-and-remove-the-industrial-image)  
**Change type:** NARROW AND REMOVE IMAGE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Any deviation from the established form is immediately heard, and therefore immediately corrected.
>
> Through this constant calibration, the student is welded to the transmission chain by being corrected into it.

### Replacement or Result

The revision says that a departure can be heard and corrected as it occurs, and that the student joins the lineage by learning to produce and recognize the same measure.

### Reason Proposed

The audit retained public audit while removing the industrial image and the absolute “any deviation” claim.

### What May Have Been Lost

The process remains clear, but the immediacy and force of being corrected into the chain are less visible.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-025 — The priority of *Śikṣā*

**Source:** [Chapter 15](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_15_aural.md:23)  
**Audit block:** [C15-004](../../80_completed/manuscript_readability_review_codex/20_ch15.md#c15-004---qualify-what-the-order-of-the-vedāṅgas-demonstrates)  
**Change type:** NARROW INFERENCE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The standard enumeration of the *Vedāṅgas* correctly preserves this priority by placing *Śikṣā* first, demonstrating that sound-production precedes the grammar that analyzes the form, the etymology that explains it, the ritual that employs it, and the calendrical discipline that times its use.

### Replacement or Result

The revision says that placing *Śikṣā* first is consistent with the practical order of preservation.

### Reason Proposed

Enumeration order alone may not demonstrate historical or conceptual priority.

### What May Have Been Lost

The practical sequence remains, but “consistent with” is a weaker conclusion than “correctly preserves this priority.” The source note should determine which formulation the evidence supports.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-026 — What reversal tests

**Source:** [Chapter 15](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_15_aural.md:51)  
**Audit block:** [C15-006](../../80_completed/manuscript_readability_review_codex/20_ch15.md#c15-006---bound-the-information-theory-analogy)  
**Change type:** CONDENSE MECHANISM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> *Sandhi* rules are not symmetric — what happens when *aḥ* meets *a* is not the inverse of what happens when *a* meets *aḥ*. A join that passes unnoticed in ordinary forward flow can fail when the pair reverses. The braid exposes the weak point.
>
> Consequently, a *Ghanapāṭhī* who reaches the end of a verse has executed adjacent joins repeatedly across multiple orderings under auditory supervision, proving that the density itself is the point.

### Replacement or Result

The revised section retains pair overlap, reversal, moving three-word windows, repeated joins, specified orders, and auditory supervision. It removes the concrete asymmetric-*sandhi* example and the concluding explanation of density.

### Reason Proposed

The audit bounded the information-theory analogy and shortened a repeated explanation of the *pāṭhas*.

### What May Have Been Lost

The current version says what each recitation does, but the removed example shows why reversal catches a failure that forward recitation can miss.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-027 — The full empirical-verification claim

**Source:** [Chapter 15](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_15_aural.md:65)  
**Audit block:** [C15-007](../../80_completed/manuscript_readability_review_codex/20_ch15.md#c15-007---state-what-the-recordings-establish)  
**Change type:** CONDENSE AND NARROW; PARTIALLY RESTORED  
**Status:** UNDECIDED  
**Applied:** YES; later repaired by contradiction audit A3  
**Destination if moved:** —

### Material Removed

> the Nambūdiri Brahmins of Kerala; Maharashtra Brahmin lineages; Tamil Nadu and Karnataka lineages; the Banaras and Allahabad lineages of the northern plains; Gujarat and Rajasthan lineages of the western coast; the Kashmir Pandit lineages preserved through displacement.
>
> the phonetic constants match exactly at the level the architecture predicts (*varṇa* inventory, accent where preserved, *sandhi* execution, metrical structure, and recitational discipline)
>
> The reader can test the claim directly

### Replacement or Result

The final repaired passage lists the regions, states exact preservation within a specified *śākhā*, describes recurring shared constants and governed branch differences, and explains how recordings make the continuity claim audible. It does not retain every named community or the full parenthetical list of constants.

### Reason Proposed

The initial audit separated what present recordings directly demonstrate from the full historical-continuity claim. The contradiction repair restored exact recurrence without presenting different *śākhās* as identical.

### What May Have Been Lost

The evidentiary structure is now sound, but the specific communities, the explicit list of compared properties, and the invitation to test the claim directly may still be useful.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-028 — The mouth-field is older than the taxonomy

**Source:** [Chapter 16](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_16_retroflex.md:29)  
**Audit block:** [C16-002](../../80_completed/manuscript_readability_review_codex/21_ch16.md#c16-002---put-the-visible-tongue-movement-before-anatomical-precision)  
**Change type:** CONDENSE AND CLAIMED MOVE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** Figure 16.1; the promised endnote is not linked from the current paragraph.

### Material Removed

> isolate and contract the superior longitudinal muscle, curl the apex of the tongue backward, and strike it cleanly against the hard palate at roughly the midpoint of the vocal tract.
>
> the mouth-field is older and wider than the taxonomy.

### Replacement or Result

The visible tongue movement now precedes the muscle name, and Figure 16.1 shows the anatomy. The paragraph says that anatomical detail appears in “the note,” but it currently has no note anchor. The family-crossing observation remains, while the age and breadth conclusion has disappeared.

### Reason Proposed

The audit put an action the reader can perform before anatomical precision.

### What May Have Been Lost

The anatomical detail is only partly relocated, and the sentence connecting the shared articulatory field to the later taxonomy no longer appears.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-029 — One sonomer across four levels

**Source:** [Chapter 16](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_16_retroflex.md:39)  
**Audit block:** [C16-003](../../80_completed/manuscript_readability_review_codex/21_ch16.md#c16-003---distinguish-the-measured-finding-from-the-chapters-inference)  
**Change type:** NARROW SYNTHESIS  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> One sonomer appears as mouth-position, semantic atom, textual name, and civilizational category.
>
> The retroflex is structural.

### Replacement or Result

The revision preserves all four appearances, warns that they do not form one etymological chain, and states that *ṛ* and *ra* recur in structural positions. It no longer closes the first sequence with the four-level synthesis or the section with the shorter hammer.

### Reason Proposed

The audit distinguished measured recurrence from an implied derivational chain.

### What May Have Been Lost

The factual qualification is useful, but the synthesis can coexist with it because “appears as” does not require a single etymology.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-030 — The continuous return to the workshop

**Source:** [Chapter 16](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_16_retroflex.md:153)  
**Audit block:** [C16-007](../../80_completed/manuscript_readability_review_codex/21_ch16.md#c16-007---state-the-corpus-burden-without-the-workshop-caricature)  
**Change type:** REMOVE ANALOGY; LATER REPAIR CONCLUSION  
**Status:** UNDECIDED  
**Applied:** YES; later repaired by contradiction audit A1  
**Destination if moved:** —

### Material Removed

> Acquiring these features would demand a continuous return to the workshop, requiring the hymns to receive the curled tongue, the mantras to receive the doubled syllable, the receiver to enter the case-system, and the folded action to enter the sentence. The pyramid's hypothesis therefore asks an engineered preservation culture to behave like an absent-minded editing office.

### Replacement or Result

The contradiction repair now closes both timing routes in direct prose: early contact locates Sanskrit's defining engineering inside the subcontinent, while later contact requires rewriting a corpus organized for exact recurrence.

### Reason Proposed

The audit removed a workshop caricature and stated the historical burden directly.

### What May Have Been Lost

The final argument is stronger after repair, but the removed sentence makes the scale of the required retrofitting easy to visualize.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-031 — The second five-feature recap

**Source:** [Chapter 16](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_16_retroflex.md:165)  
**Audit block:** [C16-008](../../80_completed/manuscript_readability_review_codex/21_ch16.md#c16-008---remove-the-repeated-five-feature-catalogue-from-the-close)  
**Change type:** MERGE AND CUT REPETITION  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Through *īḷe* curling the tongue to the dome and *dadarśa* turning repetition into a disciplined syllabic switch, the subcontinental field is explicitly made audible. As *mahyam* and *tvasmai* let grace and revelation arrive at a receiver, *paṭhyate* lets the deed stand while the doer steps back, and *pītvā* lets one action pass into the next, the entire architecture structurally aligns: the tongue curls, the sound doubles, the self receives, the doer recedes, and the act folds.

### Replacement or Result

The merged §16.10 retains one detailed recap of all five features and follows it with the Vedic, Upaniṣadic, Gītā, and *saṃskṛti* discussion.

### Reason Proposed

Two consecutive sections repeated the same five examples.

### What May Have Been Lost

The facts remain, but this version supplied the chapter's most rhythmic synthesis of mouth, sound, receiver, doer, and action.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-032 — The “pre-Vedic” Mitanni claim

**Source:** [Chapter 19](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:25)  
**Audit block:** [C19-003](../../80_completed/manuscript_readability_review_codex/24_ch19.md#c19-003---remove-the-pre-vedic-chronology-claim-from-mitanni)  
**Change type:** CORRECT CONTRADICTION  
**Status:** SUPERSEDED CLAIM RECORDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The form *aika* is structurally pre-Vedic-Sanskritic — Vedic Sanskrit has *eka*, with the contraction *ai* > *e* — placing the Mitanni Sanskritic layer in a phonologically pre-Vedic-Sanskritic position.

### Replacement or Result

The current passage derives **एक (*eka*)** internally from ⟪इ⟫ with *kan* and *guṇa*, then treats Mitanni *aika* as a receiving-language rendering. The tablet dates the receiving record, not Sanskrit's formation.

### Reason Proposed

The removed sentence contradicted the book's internal derivation of *eka* and imported chronology into a receiving-language form.

### What May Have Been Lost

No valid claim was lost. This entry preserves the discarded chronology so it cannot re-enter through a later edit.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [x] KEEP CUT
- [ ] REVISE AGAIN
- [ ] UNDECIDED

### Author Comments

```text
Superseded because it contradicts the manuscript's internal derivation of *eka*.
```

---

## LAF-R-033 — Expanded-endnotes production metadata

**Source:** [Source and Reference Companion](/Users/paragtope/projects/writing/books/atomicSanskrit/as_endnotes.md:1)  
**Audit block:** [GLOBAL-001](../../80_completed/manuscript_readability_review_codex/28_endnotes_figures_global.md#global-001---replace-the-production-introduction-to-the-expanded-endnotes)  
**Change type:** CUT PRODUCTION METADATA  
**Status:** APPROVED IN AUDIT; AWAITING LOST AND FOUND REVIEW  
**Applied:** NO  
**Destination if moved:** Project working documentation

### Material Removed

> **Status:** Reference file for expanded endnote prose. Endnote stubs throughout the chapter drafts are marked inline as `[NOTE: stub-name]`. As stubs are expanded into full endnote prose, the expanded version lives here, keyed by stub name. Each entry includes the deployment locations (which chapters/sections cite the endnote) so the prose can be revised once and the revision propagates to all citations.
>
> Convention: each endnote begins with its stub name as a level-3 heading. The prose follows. Length varies — most endnotes are 50–200 words (standard citation-plus-context); a few central endnotes are longer (400–800 words) where the supporting analysis is substantive.
>
> Endnote production sessions accumulate expansions in this file. Stubs not yet expanded remain as bare references in the chapter drafts.

### Replacement or Result

GLOBAL-001 proposes a public-facing introduction to the Source and Reference Companion. The production workflow would remain in project documentation rather than in the published companion.

### Reason Proposed

The current opening addresses editors rather than readers.

### What May Have Been Lost

The publication file would no longer document stub syntax, deployment fields, expected note length, or unfinished-note workflow. Those instructions must remain discoverable in working documentation.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-034 — Two Chapter 17 gaslighting paragraphs

**Source:** [Chapter 17](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_17_wrong_question.md:90)  
**Audit block:** [GLOBAL-006-A](../../80_completed/manuscript_readability_review_codex/28_endnotes_figures_global.md#global-006-a--combine-the-two-chapter-17-gaslighting-paragraphs)  
**Change type:** PROPOSED CONDENSATION  
**Status:** AWAITING AUTHOR DECISION  
**Applied:** NO  
**Destination if moved:** —

### Material Removed

> Gaslighting can redirect memory without erasing it. The machinery asks India to remember Pāṇini incorrectly, turning the decoder into codifier and the documenter into origin. A civilization's reverence for one of its finest decoders is thereby redirected toward codification itself.
>
> Praise becomes a weapon here. The machinery does not need to insult Pāṇini. It can praise him for the wrong act. Miscast him as codifier, and the civilization is trained to honor authority where it should be recognizing calibration. The memory remains reverent, but the machinery has altered the object of reverence. That is gaslighting at civilizational scale.

### Replacement or Result

GLOBAL-006-A proposes one paragraph that retains praise as weapon, decoder-to-codifier reversal, redirected reverence, and gaslighting.

### Reason Proposed

The two paragraphs perform the same explanatory movement consecutively.

### What May Have Been Lost

The proposed single paragraph removes the separate emphasis provided by “Praise becomes a weapon here” and “That is gaslighting at civilizational scale.”

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-035 — Repeated Chapter 14 matrix explanation

**Source:** [Chapter 14](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_14_calibration.md:193)  
**Audit block:** [GLOBAL-006-B](../../80_completed/manuscript_readability_review_codex/28_endnotes_figures_global.md#global-006-b--remove-the-duplicate-matrix-explanation-in-chapter-14)  
**Change type:** PROPOSED CONDENSATION  
**Status:** AWAITING AUTHOR DECISION  
**Applied:** NO  
**Destination if moved:** —

### Material Removed

> The standing sequence holds at matrix scale: engineered architecture, Vedic encoding, many decoding disciplines, and Pāṇini's compressed rule-system as the finest surviving documentation of that architecture.
>
> Within this framework, the calibration matrix serves as the engineered architecture, the Vedas operate as the encoding, and the *Prātiśākhya*, *Śikṣā*, *Chandas*, and *Vyākaraṇam* function as the decoding disciplines. Because Pāṇini's decoding is the most compressed and generative, it remains the finest expression of the system, though it is not the origin of the architecture itself.
>
> The teaching-level form of the same claim (Chapter 13 §13.5): the Veda preserves the form as performed; the *Aṣṭādhyāyī* preserves the form as derivable. Pāṇini added redundancy, not origin.

### Replacement or Result

GLOBAL-006-B proposes one paragraph that keeps the four-part sequence and the distinction between form as performed and form as derivable.

### Reason Proposed

The first two paragraphs restate the same mapping before the third provides the sharper teaching form.

### What May Have Been Lost

The proposed condensation no longer names the four decoding disciplines individually at this location.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-037 — Reconstruction as etymon

**Source:** [Chapter 18](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:50)  
**Audit block:** [C18-001](../../80_completed/manuscript_readability_review_codex/23_ch18.md#c18-001---state-the-bookkeeping-dispute-in-ordinary-language)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> PIE cannot be the etymon of any word, and the logic breaks again on that fact. A reconstructed form is not an etymon. The endpoint of going backward in time is the *earliest* real form, not a reconstruction the procedure has projected behind that form. A reconstruction may summarize features shared by real forms; it cannot be the source from which those forms descend unless the reconstruction corresponds to a real spoken form. *Janaka* exists. *Genus* exists. *Génos* exists. **\*ǵenh₁** does not.

### Replacement or Result

The replacement distinguishes a modern reconstruction from a demonstrated historical source and retains the burden of proving ancestry.

### Reason Proposed

The absolute wording treated the model and the proposed spoken form as the same object.

### What May Have Been Lost

The categorical refusal to let a reconstructed form function as an etymon.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-038 — The sound-field and varṇamālā recapitulation

**Source:** [Chapter 18](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:62)  
**Audit block:** [C18-002](../../80_completed/manuscript_readability_review_codex/23_ch18.md#c18-002---replace-the-repeated-chapter-17-catalogue-with-a-focused-application)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** Chapter 17 retains the full demonstration.

### Material Removed

> PIE cannot account for the Indian sound-field. Sanskrit's retroflex core is subcontinental, muscular, and architectural. PIE has no *mūrdhanya* row and no explanation for why Sanskrit places that row at the center of its phonetic system.
>
> PIE cannot account for the *varṇamālā*. A reconstructed precursor can offer an inventory. It cannot explain an engineered articulatory grid.

### Replacement or Result

A transition points back to Chapter 17 and carries the comparison forward to the *dhātavaḥ*, scaffold architecture, and *siddha*.

### Reason Proposed

Chapter 17 has just completed the sound-field and *varṇamālā* demonstration.

### What May Have Been Lost

The direct two-beat statement that PIE cannot account for either feature.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-039 — Three confessions in the cutting tree

**Source:** [Chapter 18](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:120)  
**Audit block:** [C18-004](../../80_completed/manuscript_readability_review_codex/23_ch18.md#c18-004---separate-what-the-cutting-tree-shows-from-what-the-book-infers)  
**Change type:** CONDENSE AND NARROW  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The asterisk is the first: the form was never spoken, never heard, never written by anyone — it is a procedural average, the bake this chapter opened with.
>
> The discipline's term for this is the *s-mobile* — a consonant with no source, no rule, no conditioning environment, and no meaning, "mobile" because it comes and goes as the data demands.
>
> A phantom base, a floating consonant, a meaningless appendix. That is what the whole tree stands on.

### Replacement or Result

The replacement states what the notation directly establishes and retains the final indictment with slightly narrower supporting language.

### Reason Proposed

The notation establishes reconstruction and alternation; it does not independently establish that no corresponding form was ever spoken.

### What May Have Been Lost

The sharper confession cadence and the phrase “procedural average.”

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-040 — Contact-linguistics specialist catalogue

**Source:** [Chapter 18 §18.7](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:183)  
**Audit block:** [C18-005](../../80_completed/manuscript_readability_review_codex/23_ch18.md#c18-005---move-the-contact-linguistics-catalogue-out-of-the-main-argument)  
**Change type:** MOVE  
**Status:** MOVE CONFIRMED  
**Applied:** YES  
**Destination if moved:** Endnotes `thomason-kaufman-1988` and `ross-metatypy-takia`.

### Material Removed

> Contact linguistics already knows that structural and lexical features can move across languages under intense contact. Thomason and Kaufman's account (1988, *Language Contact, Creolization, and Genetic Linguistics*) holds two central claims here.[NOTE: thomason-kaufman-1988] First, any feature — structural or lexical — can in principle transfer between languages in contact; the older assumption that grammar is borrowing-proof has been definitively rejected. Second, the intensity and duration of contact predicts the depth of structural transfer. The Sanskrit case presents exactly the conditions Thomason and Kaufman identified as producing extreme contact effects: prolonged, multi-generational engagement of Sanskrit-bearing specialists with the natural languages of Central and West Asia. The Mitanni evidence is direct documentation of exactly this kind of multi-generational specialist contact.
>
> The closest specific account is *metatypy* — coined in 1996 — describing the most extreme outcome of contact-induced structural change: a language's morphosyntax is wholesale restructured to match a model language while the recipient retains its inherited vocabulary. The central observation is that metatypy is typically asymmetric. One language is the **model**; the other is the **replica**. The replica restructures itself toward the model; the model is structurally untouched. A classic case is Takia, an Oceanic language in Papua New Guinea, restructured by contact with Waskia.[NOTE: ross-metatypy-takia]
>
> The Sanskrit case falls outside ordinary metatypy. The major contact-linguistics categories—substrate, superstrate, adstrate, the Thomason-Kaufman scale, even metatypy—rely on the assumption that contact happens between natural languages of comparable type. Consequently, Sanskrit fits none of the standard slots: it operates neither as a lower-prestige substrate (Sanskrit's prestige was high), nor as a militarily imposed superstrate, nor as a geographically adjacent adstrate (its bearers traveled). It functions instead as an engineered calibrant rather than a typical Ross-style model language.
>
> What the existing categories have no vocabulary for is a deliberately engineered, anti-entropic linguistic system in a model role. Contact linguistics has never had to deal with an engineered language because, with the singular exception of Sanskrit, no other known civilization has built one. The silence on the Sanskrit case is evidence that Sanskrit is a category of one — not an oversight.

### Replacement or Result

The body introduces **calibrant contact** and *pratibimba* in ordinary language. The existing endnotes preserve Thomason–Kaufman, metatypy, and the Takia–Waskia comparison in detail.

### Reason Proposed

The catalogue interrupts the chapter's own category before that category is stated.

### What May Have Been Lost

The explicit elimination of substrate, superstrate, and adstrate as adequate categories, and the claim that contact linguistics lacks vocabulary for an engineered calibrant in the model role.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-041 — “Contested is the confession”

**Source:** [Chapter 18](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:246)  
**Audit block:** [C18-006](../../80_completed/manuscript_readability_review_codex/23_ch18.md#c18-006---make-the-asura-dispute-precise-before-the-hammer)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> *Contested* is the confession.

### Replacement or Result

The replacement locates the fraud in installing a disputed reconstruction above Sanskrit's recorded analyses, rather than in the existence of scholarly disagreement.

### Reason Proposed

Uncertainty by itself is not fraud.

### What May Have Been Lost

The abrupt two-line approach to the `PIE is a lie` hammer.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-042 — Chapter 18 closing judgments

**Source:** [Chapter 18 close](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:322)  
**Audit block:** [C18-008](../../80_completed/manuscript_readability_review_codex/23_ch18.md#c18-008---keep-four-closing-beats)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Once this continuity is recognized, PIE loses its assigned work: it can no longer explain Sanskrit, because Sanskrit itself is the calibrant that the entire explanation was built to hide.
>
> That judgment must now reverse. Sanskrit lives. PIE must die as doctrine because PIE never lived as language.
>
> The engineered-model category contact linguistics lacks is the category Sanskrit provides.
>
> ***The imaginary ancestor loses its assigned life.***
>
> ***The asuric pyramid is the machinery that installed it.***
>
> The arithmetic of this section is the recipe of §18.5 running unchanged: one attested atom, three phantom ancestors — the device-count rising to cover what the averaging cannot.

### Replacement or Result

The close is consolidated around the inversion, Rāhu, continuity through Pāṇini, and the retained hammers `PIE is a lie`, `PIE must die`, and `The handoff begins`.

### Reason Proposed

Several adjacent lines repeat the same verdict and obscure the transition to Chapter 19.

### What May Have Been Lost

The explicit statement that PIE's assigned work was to hide Sanskrit as calibrant, the named asuric actor, and the one-to-three arithmetic.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-043 — Chapter 19 lineage claims

**Source:** [Chapter 19 §19.1](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:19)  
**Audit block:** [C19-002](../../80_completed/manuscript_readability_review_codex/24_ch19.md#c19-002---separate-remembered-lineages-from-documentary-evidence)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The **सप्तर्षि (*Saptaṛṣi*)** lineage supplies the structural roster of pre-Pāṇinian Vedic experts whose lines extend geographically.
>
> **अगस्त्य (*Agastya*)** — co-author with Lopāmudrā of Rigvedic hymns 1.165–1.191 — travels south, crosses the Vindhyas, and establishes a Vedic foothold in the Tamil country.
>
> Both northern and southern lineages agree on his north-to-south travel and on his teaching role.
>
> Bharadvāja is the most direct Wave-1 analytical-traveler candidate the continuum records.

### Replacement or Result

The revised section distinguishes inherited civilizational memory from contemporary documentary evidence and corrects the Lopāmudrā attribution.

### Reason Proposed

The sources preserve lineage memory rather than one contemporary travel record; Lopāmudrā is associated specifically with Ṛgveda 1.179.

### What May Have Been Lost

The stronger geographic-carrier framing and the specific analytical-traveler characterization of Bharadvāja.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-044 — Direct and inferred Wave 2 routes

**Source:** [Chapter 19 §19.2](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:69)  
**Audit block:** [C19-004](../../80_completed/manuscript_readability_review_codex/24_ch19.md#c19-004---label-the-six-transmission-cases-by-confidence)  
**Change type:** NARROW AND REORGANIZE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The *Téchnē* brought these pieces together as a complete grammatical system after sustained contact with India. It places the Greek achievement inside a world where Pāṇinian methods were already circulating.
>
> **Arabic** — *direct*, 8th c. CE.
>
> Why would grammar be the one Indic export Basra somehow developed independently?
>
> If Arabic grammar derives from Pāṇinian methodology, Hebrew is triply so.
>
> When Greek, Latin, Tibetan, Arabic, and Hebrew are taken together, the evidence reveals a clear pattern: one direct transmission, one widely admitted transitive descent, one direct transmission documented in the receiving lineage's own records, and two additional cases holding the identical shape.

### Replacement or Result

The detailed cases remain, reorganized by the kind of evidence each route preserves. Greek and Arabic become argued proposals rather than documented direct routes.

### Reason Proposed

The six routes do not preserve the same kind or strength of evidence.

### What May Have Been Lost

The stronger declaration of direct Arabic transmission and the cumulative “identical shape” conclusion.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-045 — Romani continuity and influence

**Source:** [Chapter 19 §19.3](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:105)  
**Audit block:** [C19-005](../../80_completed/manuscript_readability_review_codex/24_ch19.md#c19-005---narrow-the-romani-claims-to-what-the-evidence-supports)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Their language is Indic — close enough to Hindi and Punjabi that mutual understanding is possible at the basic-vocabulary level today.
>
> Romani music, dance, and improvisational practices have demonstrably reshaped flamenco in Andalusia, the folk-classical traditions of Hungary and Romania, manouche jazz in France, and the gypsy-song repertoire of Russia.
>
> They preserved the Indic source itself, intact, within European linguistic environments.

### Replacement or Result

The revision describes audible familiarity without claiming mutual intelligibility, varies the strength of musical influence by region, and describes continuity alongside contact-driven change.

### Reason Proposed

The original stated three claims more broadly than the evidence supports.

### What May Have Been Lost

The word `intact` and the broad civilizational reach of the performance claim.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-046 — Diaspora as direct source

**Source:** [Chapter 19 §19.3](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:118)  
**Audit block:** [C19-006](../../80_completed/manuscript_readability_review_codex/24_ch19.md#c19-006---explain-what-calibrant-capacity-means)  
**Change type:** NARROW AND EXPAND  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The Diasporic Wave remains structurally distinct from Waves 1 and 2 in one critical sense: it preserves the source directly.
>
> Entering host languages as direct loans rather than as *Pratibimba*, modern diasporic vocabulary—*yoga*, *mantra*, *guru*, *dharma*, *karma*, *avatar*, *namaste*, *pundit*—is explicitly recognized as Indic. In every case, the diaspora has held the source rather than the reflection.
>
> The Diasporic Wave is the demographic substrate through which the third calibrant wave must propagate, if it is to propagate as a calibrant wave at all.

### Replacement or Result

The revision keeps whole-community transmission distinct, acknowledges several routes for the listed loans, and defines calibrant capacity through concrete disciplines.

### Reason Proposed

Not every listed word entered host languages through a modern diaspora.

### What May Have Been Lost

The categorical claim that Wave 3 must propagate through the diasporic substrate.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-047 — Repeated Wave 3 preconditions

**Source:** [Chapter 19 §19.4](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:141)  
**Audit block:** [C19-007](../../80_completed/manuscript_readability_review_codex/24_ch19.md#c19-007---remove-repetition-from-the-wave-3-close)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> That precondition now becomes Wave 3's first discipline: Indians in the subcontinent, the modern global Indian diaspora, and the Romani branch that held Indic substrate longest outside the subcontinent must reconstitute *āryatva* before attempting to extend it.
>
> Wave 3 therefore requires its carriers to reenter Sanskrit's discipline before they attempt to transmit its radiance.

### Replacement or Result

The preceding section retains and explains the relearning requirement; §19.4 closes with the four recognitions and points to the epilogue.

### Reason Proposed

The two paragraphs repeat the precondition established immediately before §19.4.

### What May Have Been Lost

The explicit imperative to reconstitute *āryatva* before transmission.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-048 — Population transfer wording

**Source:** [Chapter 19 §19.4](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:137)  
**Audit block:** [C19-007](../../80_completed/manuscript_readability_review_codex/24_ch19.md#c19-007---remove-repetition-from-the-wave-3-close)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Sanskrit's reach moved through calibrant transmission, not population transfer.

### Replacement or Result

The replacement states that population movement may accompany transmission but does not author Sanskrit's architecture.

### Reason Proposed

The book disputes population movement as authorship, not every movement of people.

### What May Have Been Lost

The concise opposition between calibrant transmission and the migration thesis.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-049 — Total-conquest and chapter-remedy framing

**Source:** [Epilogue, The Eclipse Is Over](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:19)  
**Audit block:** [EPI-001](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-001---reconcile-recovery-with-the-residual-plates)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The eclipse passed because the Sun remained — and keeping that light visible is the work this ending asks the reader to enter.
>
> The recovery image is not total conquest. The Sun is visible, the seven core plates have fallen, and points of caretaking light appear across the world-field. The residual plates remain as work that no single book can finish.
>
> The core shadow is cleared. Plate by plate the obscuration falls away — Descended, Botanical, Codified, Alphabetic, Abugida, Sibling Language, Early Literature — and Rāhu, the invented ancestor, is dispelled. The asuric pyramid casts the shadow. Chapter 19 begins the remedy with the waves of transmission and the work of relearning.

### Replacement or Result

The revision states which seven plates have fallen, identifies the three residual shadows, and places responsibility with teachers, families, institutions, and communities.

### Reason Proposed

The original says both that the recovery is incomplete and that the core shadow is cleared, then points backward to Chapter 19 after the reader has already completed it.

### What May Have Been Lost

The phrase `not total conquest`, the explicit identification of Rāhu as the invented ancestor, and the direct reminder that the pyramid cast the shadow.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-050 — Āryatva discussion moved to the invitation

**Source:** [Epilogue, The Eclipse Is Over](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:33)  
**Audit block:** [EPI-002](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-002---move-the-full-āryatva-discussion-to-the-invitation)  
**Change type:** MOVE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** Epilogue, The Invitation

### Material Removed

> Hindu stories are full of **असुर (*asuras*)** jealous of **देव (*devas*, the radiant ones)** — jealous of what the *devas* possessed and the *asuras* could not earn, and full of the *asuras*' constant desire to appropriate, to control, to take what they did not possess. The nineteenth-century European pyramid wanted **आर्यत्व (*āryatva*)** with that same hunger. It wanted the respect attached to *ārya* — discipline, learning, restraint, skill, and conduct in *Sanātan*'s own terms — without the work the word required.
>
> The pyramid realized that *āryatva* cannot be demanded, only earned — so it redefined the word, making *ārya* about race, power, authority, ego, and the desire to lord over others.
>
> The pyramid has been exposed, and the aspiration for **आर्यत्व (*āryatva*)** emerges unobscured. PIE has fallen, not the people who have inherited its darkness. The remedy is not retribution. Anyone within the pyramid—whether low or high in its hierarchy, whether an active or passive participant in its agenda—who finds the courage can make a new choice. The remedy is re-learning.

### Replacement or Result

These paragraphs move intact to `The Invitation`, immediately before the chapter explains what earning *āryatva* requires.

### Reason Proposed

The discussion belongs beside the closing mantra and its account of *ārya* as discipline rather than race.

### What May Have Been Lost

Nothing if the move is completed intact.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-051 — Samudra-manthana interpretive preface

**Source:** [Epilogue, Where the Nectar Rises](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:41)  
**Audit block:** [EPI-003](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-003---tell-the-samudra-manthana-story-before-interpreting-it)  
**Change type:** EXPAND AND NARROW  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The asuras pulled expecting to drink first.
>
> The story has many learnings, among them what the churning costs, who bears the poison, and why Mohinī discriminated.

### Replacement or Result

The revision first supplies Vāsuki, Mandara, Śiva, and *nīlakaṇṭha*, then develops the academic analogy in a separate paragraph.

### Reason Proposed

Readers need the main story before the epilogue interprets it.

### What May Have Been Lost

The asuras' expectation that they would drink first and the compact three-part statement of the story's lessons.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-052 — Exact replay of Svarbhānu's theft

**Source:** [Epilogue, Where the Nectar Rises](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:45)  
**Audit block:** [EPI-004](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-004---present-svarbhānu-as-a-structural-analogy)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The pyramid repeated the theft exactly.

### Replacement or Result

The revision says that the pyramid repeated the pattern and adds a paragraph explaining how the accumulated scholarship can now be reused.

### Reason Proposed

The analogy is structural rather than a literal replay.

### What May Have Been Lost

The force of `exactly`.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-053 — Full Mohinī engineering interpretation

**Source:** [Epilogue, Where the Nectar Rises](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:47)  
**Audit block:** [EPI-005](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-005---slow-the-mohinī-interpretation)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Mohinī's discrimination is founded in engineering, not favoritism.
>
> The *devāḥ* are not persons collecting a reward.
>
> And amṛta is the anti-entropy agent itself: *a-mṛta*, the un-dying — the same privative *a-* that un-shines the *a-sura*.
>
> Pour the un-dying into the principles of flow, and the system becomes self-renewing: the light circulates without loss, and what the shining ones govern stays **सनातन (*sanātana*)** — eternal because its order cannot decay.
>
> Pour the un-dying into a container, and the container becomes a prison no age can unlock — which is why the severing of Svarbhānu is instant: one immortal container would have ended the living cosmos.

### Replacement or Result

The revision identifies this as the epilogue's interpretation, preserves the opposition between undying flow and an undying container, and applies it explicitly to calibration and codification.

### Reason Proposed

The original moves from story to a detailed metaphysical reading too quickly and states that reading as though it were the story's only possible meaning.

### What May Have Been Lost

The direct defense of Mohinī's discrimination, the anti-entropy definition, the *sanātana* connection, and the explanation for Svarbhānu's immediate severing.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-054 — Foreign chronology machinery

**Source:** [Epilogue, The Chronology Refusal](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:99)  
**Audit block:** [EPI-007](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-007---merge-the-chronology-refusal-into-the-architectural-contest)  
**Change type:** CONDENSE AND CLARIFY  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The opening antagonist account exposes the danger: chronology capture. Once the pyramid owns the clock, it can call the *Veda* early, late, primitive, developed, borrowed, interpolated, priestly, or political. A chronology produced inside the same machinery that misclassified Sanskrit cannot sit above Sanskrit’s architecture and dictate its sequence.
>
> Once that light is visible, the hunger for the pyramid's calendar may weaken on its own.

### Replacement or Result

The revision distinguishes the Hindu continuum's internal chronology from a foreign clock that uses an imposed sequence to dictate Sanskrit's category.

### Reason Proposed

The original could be read as refusing chronology itself rather than refusing chronology capture.

### What May Have Been Lost

The full list of labels imposed through chronology and the observation that the desire for the pyramid's calendar may weaken.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-055 — Reader designated as an Atri in potential

**Source:** [Epilogue, The Mantra](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:149)  
**Audit block:** [EPI-008](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-008---make-the-atri-invitation-gentler-and-more-precise)  
**Change type:** NARROW AND EXPAND  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The reader is addressed as a Wave 3 *ṛṣi* or *ṛṣikā* in potential, after the re-learning — an Atri in potential, for an Atri is exactly that: the Wave 3 carrier whose particular work is clearing what remains of the eclipse.
>
> Indians in the subcontinent, the global Indian diaspora, and the Romani branch that held Indic substrate longest outside the subcontinent are the first human substrate through which Wave 3 must propagate.

### Replacement or Result

The revision identifies the immediate carriers, describes the book as one Wave 3 instrument, and connects it gently to the Atris' work without designating the reader directly.

### Reason Proposed

The plan calls for a restrained Atri identification: one attempt to make the Sun visible, not a declaration that the author or reader is already an Atri.

### What May Have Been Lost

The explicit definition of an Atri as a Wave 3 carrier and the claim that the Romani branch held Indic substrate longest outside the subcontinent.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-056 — Overture's narrowing to the shadow

**Source:** [Overture close](/Users/paragtope/projects/writing/books/atomicSanskrit/as_part_00_overture_shankha.md:29)  
**Audit block:** [PARTS-001](../../80_completed/manuscript_readability_review_codex/26_parts_front_back.md#parts-001---simplify-the-overtures-final-orientation)  
**Change type:** CLARIFY  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> On one side stand the seekers and caretakers, people trained to listen, correct, remember, and keep looking.
>
> With the caretakers and the finite order now visible, the work narrows to the shadow itself — how it was cast, and how it lifts.

### Replacement or Result

The revision defines caretakers through their actions and gives the reader the exact sequence: Chapters 0 and 1 introduce the parties; Part I begins removing the plates.

### Reason Proposed

The Overture should orient the reader toward the book's visible structure rather than end with an abstract description of narrowing.

### What May Have Been Lost

The phrase `keep looking` and the concise movement from parties to shadow.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-057 — Part I catalogues and actor taxonomy

**Source:** [Part I opener](/Users/paragtope/projects/writing/books/atomicSanskrit/as_part_01_wrong_metaphor.md:27)  
**Audit block:** [PARTS-002](../../80_completed/manuscript_readability_review_codex/26_parts_front_back.md#parts-002---reduce-part-i-to-the-work-of-an-opener)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** Chapters 2–4 already develop the material

### Material Removed

> Category theft casts the shadow: theft by misclassification, inversion by metaphor, subordination by genealogy, concealment by doctrine.
>
> What it darkens is the Sanskrit continuum — the civilization subjected to a false description of its own language. The injury is deeper than misdescription. The pyramid sustained, and sustains, a systematic effort to convince a civilization that its own understanding of reality is a mass delusion. Chapter 17 calls out one instrument of that tactic under its proper name: *gaslighting with footnotes*.
>
> That concealment is the shadow. The pyramid first forces a swastika architecture—built for well-being, distributed order, and civilizational continuity—into a botanical tree, then into a codified standard.
>
> That motive is civilizational envy sharpened into institutional strategy. Sanskrit displays an order the pyramid cannot generate: distributed, calibrated, self-correcting, free of apex command. That exposes the pyramid's inferiority. The envy is personal before it is institutional: the one at the apex faces an order above his own that he did not build and cannot abide.
>
> The shadow-caster wears several names, each for a different layer. The *dogma* denotes the protected belief-content: the authorized account of Sanskrit, PIE, chronology, progress, and civilizational origin. The *church of progress*, developed in Chapter 3, labels the institutional carrier: the academy, reference works, journals, museums, universities, foundations, and credentialing systems that make the doctrine durable. The *priests*, *missionaries*, and *jihadis of progress* designate the function-classes that sanctify, export, and defend it.
>
> Over this machinery stands the asuric pyramid: the geometry of apex authority, controlled doctrine, extracted labor, and withheld light. Its working system is the *asuric machinery*: it converts evidence into concealment, domain and mode into chronology, and decoding into codification.
>
> What the shadow hides is the architecture: the mouth-map, the *varṇamālā*, the *dhātuḥ*, the *Dhātupāṭha*, the demonstrated fractality of the *dhātuḥ* as atomic *sūtra*, the calibration matrix, the recitation lineages, the retroflex row — and राहु (*Rāhu*), the imaginary ancestor built to contain them.
>
> The architecture shows redundancy even at the human scale: the Veda preserves form as performed; Pāṇini's grammar keeps the same form derivable by rule.
>
> The Sun remains behind the shadow. The eclipse is caused by स्वर्भानु; the imaginary ancestor is राहु. The Atris found the hidden Sun by the fourth formulation, not by force — and the same formulation clears the shadow here, plate by plate, until the light stands whole.
>
> Only when the shadow's mechanism stands visible can the Sun's own light be restored.

### Replacement or Result

The shorter opener retains the three plates, Sanskrit as *saṃskṛti*, Svarbhānu, the masculine apex beat, *sat-asat-viveka*, and the Chapter 2–4 map. Chapters 2–4 retain the fuller catalogues and definitions.

### Reason Proposed

The original Part opener repeats definitions and catalogues that the next three chapters develop in full.

### What May Have Been Lost

The direct phrase `gaslighting with footnotes`, the actor taxonomy, the architectural catalogue, the Veda/Pāṇini redundancy example, the Svarbhānu/Rāhu distinction, the reference to the Atris' fourth formulation, and two closing hammers.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-058 — Heroic erasure in the Part VI chapter map

**Source:** [Part VI opener](/Users/paragtope/projects/writing/books/atomicSanskrit/as_part_06_killing_pie.md:13)  
**Audit block:** [PARTS-004](../../80_completed/manuscript_readability_review_codex/26_parts_front_back.md#parts-004---state-the-actual-question-in-part-vi)  
**Change type:** REFRAME  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** Chapter 17 retains the full treatment

### Material Removed

> Chapter 17 exposes why the standard question is wrong, and how heroic erasure redirected civilizational memory toward codification.

### Replacement or Result

The revision states the inquiry directly: who selected Sanskrit's sounds, arranged its atoms, and built its preservation disciplines.

### Reason Proposed

The Part opener should tell readers what Chapter 17 investigates rather than summarize the mechanism in specialist vocabulary.

### What May Have Been Lost

The term `heroic erasure` and its link to redirected civilizational memory.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-059 — Part VII's recognition inquiry

**Source:** [Part VII opener](/Users/paragtope/projects/writing/books/atomicSanskrit/as_part_07_life_after_pie.md:7)  
**Audit block:** [PARTS-005](../../80_completed/manuscript_readability_review_codex/26_parts_front_back.md#parts-005---give-part-vii-a-positive-task)  
**Change type:** REFRAME  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> With Rāhu dispelled, the Sun stands clear, and explanation begins.
>
> The next question is what becomes visible when the pyramid no longer categorizes Sanskrit as a daughter of PIE.

### Replacement or Result

The revision gives Part VII a positive task: tracing how Sanskritic words, structures, and methods reached other languages through radiance and contact.

### Reason Proposed

The old opening says that explanation begins after the entire book has already explained the architecture.

### What May Have Been Lost

The open-ended invitation to consider everything that becomes visible after PIE.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-060 — Acknowledgments production placeholder

**Source:** [Acknowledgments](/Users/paragtope/projects/writing/books/atomicSanskrit/as_0_02_acknowledgements.md:3)  
**Audit block:** [PARTS-006](../../80_completed/manuscript_readability_review_codex/26_parts_front_back.md#parts-006---remove-production-notes-from-acknowledgments)  
**Change type:** MOVE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** `working/10_active/as_todo.md`

### Material Removed

> *Draft v1 — for iteration. More entries to be added by the author.*
>
> > **[ACKNOWLEDGMENTS — TO BE EXPANDED BY AUTHOR]**
> >
> > Family, contributors, scholarly debts, archives, translators, readers of early drafts. The *Operation Red Lotus* preface's structure of recognizing each contributor by name and role works well here too.

### Replacement or Result

The production reminder moves to the active task list. The compiled manuscript retains the completed Samskrita Bharati acknowledgment.

### Reason Proposed

Draft metadata and private reminders should not appear in the printed book.

### What May Have Been Lost

Nothing if the task-list move is completed.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-061 — Courtroom account of the notes

**Source:** [A Note on the Notes](/Users/paragtope/projects/writing/books/atomicSanskrit/as_0_04_note_on_notes.md:3)  
**Audit block:** [PARTS-007](../../80_completed/manuscript_readability_review_codex/26_parts_front_back.md#parts-007---replace-the-stale-courtroom-language-in-note-on-the-notes)  
**Change type:** REPLACE FRAME  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The main book contains the prosecution. The notes preserve verification. They do not retry the case; they preserve the sources, distinctions, and trails by which the case can be checked.

### Replacement or Result

The revision says that the main book develops the argument and the Source and Reference Companion preserves the material by which readers can check it.

### Reason Proposed

The book no longer uses the courtroom as its structural frame.

### What May Have Been Lost

The force of separating the main case from its verification apparatus.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-062 — Appendix 1 production and courtroom framing

**Source:** [Appendix Part 1](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_01_baking.md:3)  
**Audit block:** [APP-001](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-001---rebuild-appendix-1-around-evidence-institution-inference-and-survival)  
**Change type:** CUT AND REFRAME  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> *Draft v2 (2026-05-20). Four-tier merge of Codex compression (2,084 words) against the reference session-2026-05-14 draft (5,800 prose words). **Appendix voice**: T1 + T2 + T4 restored verbatim; T3 compressed to Codex-style tightness. T4 = reference preservation (dated-figure chains, primary-source quotation specifics, institutional/pipeline named specifics, verification-trail material the body footnotes-out but the appendix keeps inline). Prosecutorial-appendix posture: the receipts stay on the page.*
>
> The prosecution begins with the pre-independence operation.
>
> Deccan College, Pune, the institution that anchors the prosecution.
>
> The structural irony is the charge.
>
> The polemic does not deny that.
>
> Appendix Part 2 prosecutes that continuation in detail.
>
> The institutional defendant remains; only the flags have changed.
>
> The four-beat verdict closes the prosecution in parallel with Chapter 18.

### Replacement or Result

The production history disappears from the published appendix. `The receipts stay on the page` becomes an explicit statement of method, and the remaining courtroom terms are replaced with direct descriptions of the evidence and argument.

### Reason Proposed

The eclipse replaced the courtroom as the book's structural frame, while private merge history does not belong in the published appendix.

### What May Have Been Lost

The concentrated prosecutorial tone and the record of how the draft was assembled.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-063 — Appendix 2 production and prosecution framing

**Source:** [Appendix Part 2](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_02_encyclopaedic.md:3)  
**Audit block:** [APP-002](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-002---lead-appendix-2-toward-its-strongest-comparison)  
**Change type:** CUT AND REFRAME  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> *Draft v2 (2026-05-20). Four-tier merge of Codex compression (2,084 words) against the reference draft (5,700 prose words). **Appendix voice**: T1 + T2 + T4 restored verbatim; T3 compressed to Codex-style tightness. T4 = reference preservation. Sibling appendix to Part 1: Part 1 prosecutes the pre-independence operation (the colonial Sanskrit-knowledge pipeline that fed the German bake); Part 2 prosecutes the post-independence continuation (the Encyclopaedic Dictionary of Sanskrit on Historical Principles, Deccan College Pune, 1948–present).*
>
> The Deccan College dictionary is the detailed case for prosecution.
>
> The prosecution targets that contemporary form.
>
> The structural fact is the prosecutorial target.

### Replacement or Result

The appendix begins with the preservation-architecture distinction and presents Deccan College as the detailed institutional case rather than as a courtroom exhibit.

### Reason Proposed

Private draft history and stale courtroom vocabulary obscure the comparison the appendix is making.

### What May Have Been Lost

The explicit sibling relationship between Appendices 1 and 2 and their former prosecutorial division.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-064 — Claim about Katre's personal reading

**Source:** [Appendix Part 2 §2.5](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_02_encyclopaedic.md:121)  
**Audit block:** [APP-002](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-002---lead-appendix-2-toward-its-strongest-comparison)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Katre could have read the *Paspaśāhnika*. He did not.

### Replacement or Result

The revision limits itself to the institutional record: the project's published method does not use Patañjali's categories to classify the variation it collects.

### Reason Proposed

The manuscript does not establish what Katre personally read or chose not to read.

### What May Have Been Lost

The direct personal accountability and punch of the original.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-065 — Universal geographic prediction in the sound atlas

**Source:** [Appendix Part 4](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_04_inventory_atlas.md:5)  
**Audit block:** [APP-004](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-004---present-appendix-4-as-an-exploratory-atlas)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The polemic ladder descends cleanly through four step-points.
>
> Geography alone predicts the count, leaving the classifications powerless to explain it.
>
> The IE-classified sets span 11/23 to 20/23 depending only on which IE languages sat geographically close to the subcontinental contact zone.
>
> The eleven surveys — four in the body, seven in this appendix — stack into a monotone cascade. Geography produces the signal. Family-tree classification produces noise on top of it.
>
> Geographic distance from the subcontinent predicts coverage.
>
> The seven appendix controls confirm that each step is real, is not driven by which three languages a survey set happens to use, and persists across alternate language choices the pyramid might insist on.

### Replacement or Result

The revision reports the ordering found in the selected samples, identifies the inventory and selection choices on which it depends, and presents the atlas as a reproducible exploratory method rather than a universal geographic law.

### Reason Proposed

Eleven editorially selected three-language sets do not by themselves establish a universal predictor or a statistically tested monotone relationship.

### What May Have Been Lost

The force and simplicity of geography as the sole explanation.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-066 — Appendix 5 draft metadata and unrestricted opening claim

**Source:** [Appendix Part 5 opening](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_05_language_factory.md:1)  
**Audit block:** [APP-005](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-005---define-what-the-language-factory-actually-demonstrates)  
**Change type:** CUT + NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> *Draft v2 (2026-05-20). Paraphrased four-tier merge of Codex compression (1,375 words) against the reference draft (4,300 prose words). **Appendix voice**: T1 + T2 + T4 substance preserved through paraphrase; T3 compressed to Codex-style tightness. Codex's nine-section structure preserved; the reference draft's specifics (Bopp's *Vergleichende Grammatik* 1833–1852 + Schleicher's *Compendium* 1861 + *Avis akvāsas ka* 1868; Pune-Calcutta-Oxford-Göttingen pipeline; full §5.6 paradigm table with apacat / pacatu / paktaḥ / paktiḥ / pācakāḥ / hāsakaḥ; three-reasons-for-Japanese rationale; *asuratva* Ch 3 §3.7 + *lokakṣema* polemic) restored in paraphrased form. Devanagari first-use audit run on Indic terms.*
>
> A construction settles the question. Build a working language out of someone else's phonemes, on Sanskrit's grammatical engine — and watch whether the engine still runs.
>
> Sanskrit is more than a word factory; it is a language factory. The architecture is robust enough to be detached from Sanskrit's own sonomeric inventory and applied to a foreign set of phonemes, generating a language that sounds completely different but remains fully operational.

### Replacement or Result

The revision describes the experiment, the result it demonstrates, and its limits. It continues to call Yenpro a deliberately constructed language, while distinguishing that construction from a historical speech community or a proof of long-term stability.

### Reason Proposed

The metadata belongs to drafting history rather than the published appendix. The opening also claimed more than the substitution experiment demonstrates.

### What May Have Been Lost

The original opening reaches its verdict more quickly and calls the result fully operational without qualification.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-067 — Appendix 5 count and Japanese-phonology claims

**Source:** [Appendix Part 5 §§5.4–5.6](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_05_language_factory.md:60)  
**Audit block:** [APP-005](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-005---define-what-the-language-factory-actually-demonstrates)  
**Change type:** CORRECT  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Japanese has five vowels (/a, i, u, e, o/) and roughly fifteen consonant phonemes (/k, g, s, z, sh, j, t, d, ch, ts, n, m, h, b, p, r, w, y/).
>
> Six lexical primitives — ⟪पच्⟫ (*pac*, to cook / bake), ⟪पिष्⟫ (*piṣ*, to grind / knead), ⟪हस्⟫ (*has*, to laugh), *śūnya* (hollow), *eka* (one) — and five grammatical morphemes: *-aka* (agent-noun suffix), *-ta* (past-participle), *-ākī* (adverbial-modifier), *-ti* (present 3sg verb ending), *-ḥ* (masc. nom. sg.), *-aṁ* (neuter acc. sg.).
>
> Vowel-length distinctions collapse (Japanese has no phonemic vowel length in this cipher). The cipher is chosen for *distinctness*: every Sanskrit phoneme used in the example maps to a different phoneme in the output.
>
> Five *dhātus* and the associated suffix-and-ending inventory will produce, by simple combinatorics, several hundred surface forms.
>
> ...the kind of homophony every language has in some form, and exactly what one expects when the substrate (Japanese) lacks a phonemic contrast the source language (Sanskrit) deploys.

### Replacement or Result

The revision identifies the Japanese inventory as a simplified working set, corrects the example to five lexical elements and six grammatical elements, states that the cipher deliberately collapses vowel length and several consonantal distinctions, and identifies the three *dhātus* actually used.

### Reason Proposed

The visible lists contradicted their stated totals. Japanese has contrastive vowel length, and the cipher does not map every Sanskrit sound to a distinct output.

### What May Have Been Lost

The cleaner claim that every sound remains distinct and that the substrate itself forced every collapse.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-068 — Schleicher's inferred institutional motive

**Source:** [Appendix Part 5 §5.8](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_05_language_factory.md:159)  
**Audit block:** [APP-005](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-005---define-what-the-language-factory-actually-demonstrates)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> He could read the recipe.
>
> He had read the recipe. He chose to bake against it.
>
> Schleicher's refusal was an instance of ***asuratva*** operating at the institutional level...
>
> The baker was *jealous* of the recipe in the institutional-possessive sense...
>
> Schleicher's job was to manufacture an alternative source...
>
> The baker is not a hapless cook who didn't know any better. He had read the recipe, kept it on his shelf...

### Replacement or Result

The revision preserves Schleicher's accountability for the model he published and the intellectual environment in which he worked. It distinguishes those documented facts from the book's interpretation of the model's institutional function.

### Reason Proposed

Published access to Sanskrit scholarship does not by itself establish what Schleicher personally read, felt, or understood as his assigned “job.”

### What May Have Been Lost

The personal accusation, jealousy image, and repeated baker refrain become less direct.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-069 — Appendix 6 conflation of three counted datasets

**Source:** [Appendix Part 6 opening and §6.3](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_06_by_the_numbers.md:3)  
**Audit block:** [APP-006](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-006---reconcile-appendix-6s-datasets-before-polishing-prose)  
**Change type:** CORRECT + EXPAND  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> Two paths hold the audit. **Path A** measures the digital Pāṇinian **धातुपाठ (*Dhātupāṭha*)**: 2,168 entries across the ten **गणाः (*gaṇāḥ*)**, after **अनुबन्ध (*anubandha*)** markers are removed by the relevant *Aṣṭādhyāyī* rules. **Path C** measures actual use through the Digital Corpus of Sanskrit: corpus-attested combinatorial valency across parsed Sanskrit texts. Path A tests the inventory. Path C tests deployment.
>
> Path A gives Spearman ρ = **−0.485** between productivity and particle count. Path C, using actual corpus-attested valency across 3,839 dhātavaḥ, gives ρ = **−0.4334**.

### Replacement or Result

The revision distinguishes the full 2,168-entry structural inventory, the 138-atom Path A dictionary sample, and the 3,839 normalized verb lemmas produced by the DCS parser for Path C. It defines Path C valency as the number of distinct preverb-and-form-class combinations recorded for each lemma.

### Reason Proposed

The three totals count different units. Presenting 2,168 and 3,839 as two totals for the same *dhātavaḥ* made the method internally contradictory.

### What May Have Been Lost

The old two-path explanation was shorter and easier to repeat.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-070 — Universal irregularity and design claims in Appendix 6

**Source:** [Appendix Part 6 §§6.2–6.4](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_06_by_the_numbers.md:33)  
**Audit block:** [APP-006](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-006---reconcile-appendix-6s-datasets-before-polishing-prose)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> The ten *gaṇāḥ* are more than bins. Their sound profiles match the work they do.
>
> The most productive *dhātavaḥ* are the smallest, not the largest and not the most irregular.
>
> Sanskrit aggressively reverses that tendency. Its high-productivity atoms never collapse into idiosyncrasy, ensuring that the smallest atoms remain structurally regular and maximally reusable.
>
> The numerical pattern shows compact atoms designed for controlled expansion.
>
> If the *dhātuḥ* were a botanical organ, the measurements would have no reason to converge.
>
> The atom built in Chapter 10 and activated in Chapter 11 behaves, under measurement, like a designed unit.
>
> Ultimately, the *Dhātupāṭha* operates as a strictly atomic inventory whose underlying numbers vividly expose its engineering.

### Replacement or Result

The revision states the measured distributions first, then identifies intentional architecture as the book's explanation. It retains the engineering conclusion while avoiding claims that the current datasets establish universal regularity, causation, or design by themselves.

### Reason Proposed

The measurements cover sound distribution, a selected dictionary sample, and corpus-visible combinations. They do not include a complete paradigm-irregularity audit or independently prove the cause of every distribution.

### What May Have Been Lost

The old prose moves directly from pattern to design and gives the engineering conclusion greater certainty.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-071 — Appendix 7 draft metadata and compressed opening

**Source:** [Appendix Part 7 opening](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_07_vedic_carrier.md:1)  
**Audit block:** [APP-007](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-007---keep-appendix-7-on-the-vedic-evidence)  
**Change type:** CUT + REWRITE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> *Draft v2 (2026-05-20). Paraphrased four-tier merge of Codex compression (1,384 words) against the reference draft (5,471 prose words). **Appendix voice**: T1 + T2 + T4 substance preserved through paraphrase; T3 compressed to Codex-style tightness. Codex's seven-section structure adopted (cleaner than the reference draft's six-section structure with sub-numbered §7.2.1–§7.2.4 and §7.3.1–§7.3.2). The two empirical tables (12-row dhātu table at §7.3; 8-row drift-claims table at §7.5) preserved verbatim. Per-verse phrase-by-phrase analysis with full Devanagari + IAST + translation + Pāṇinian grammar-term pairings restored in §7.2. Wheeler-overreach full companion (1947 Mohenjo-daro / "Indra stands accused" / Dales 1964 / Kenoyer / Possehl / Kennedy) restored in §7.4. Form-drift / meaning-drift two-mode analysis with hlāfweard → Lord (Goddard 1910 *moron* → Rosa's Law 2010 → DSM-5 2013) restored in §7.6.*
>
> The claim established in Chapter 1 is demonstrated here.
>
> The *Vedas* firmly hold Sanskrit's engineering as corpus form...

### Replacement or Result

The published opening begins with the appendix's evidence: three Vedic passages contain the sound junctions, inflections, derivations, verbal forms, accents, and metrical structures that Pāṇini later documented.

### Reason Proposed

Draft history does not belong in the published appendix, and the old opening announced a conclusion before showing the evidence.

### What May Have Been Lost

The direct bridge to Chapter 1 becomes less immediate.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-072 — Full Wheeler and Mohenjo-daro digression

**Source:** [Appendix Part 7 §7.4](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_07_vedic_carrier.md:124)  
**Audit block:** [APP-007](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-007---keep-appendix-7-on-the-vedic-evidence)  
**Change type:** MOVE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** `as_endnotes.md`, note `wheeler-mohenjo-daro-overreach`

### Material Removed

> **Wheeler's overreach — the parallel case.** In 1947, the British archaeologist **Sir Mortimer Wheeler** (1890–1976), then Director General of the Archaeological Survey of India, excavated portions of *Mohenjo-daro* and identified approximately thirty-seven skeletons across multiple excavation areas; the famously cited *"massacre group"* in the HR area comprised approximately six skeletons in unusual burial positions. From this handful of bodies, Wheeler concluded a mass invasion. In his 1947 article *"Harappa 1946: The Defences and Cemetery R-37"* in *Ancient India*, Wheeler wrote: *"On circumstantial evidence, Indra stands accused."* The scenario, restated in *The Indus Civilization* (Cambridge, 1953): invading *"Aryans"* had *mowed down the native populations like grass*, with the unburied skeletons serving as physical proof.
>
> The interpretation has been substantially abandoned. **George F. Dales** published the field-defining refutation as *"The Mythical Massacre at Mohenjo-daro"* in *Expedition* magazine in 1964, demonstrating that the skeletons belonged to different stratigraphic levels and were not recovered from a single massacre horizon. Subsequent work by **Jonathan Mark Kenoyer**, **Gregory Possehl**, and **Kenneth Kennedy** confirmed: skeletons not coeval; not located in elite citadel areas where invasion victims would have fallen; many showed signs of disease (anemia, leprosy, malnutrition) inconsistent with battle-death. The archaeological-invasion case has been retired from serious scholarship. What survives in the textbook record is Wheeler's overreach as the clearest example of evidence-poor inference inflated into a civilizational-scale claim. *Six skeletons. One massacre. One race-replacement narrative anchored on six unburied bodies.*
>
> The *progressive dogma*'s *"Sanskrit was constantly evolving"* claim is the same structural overreach in a different domain. The pyramid extrapolates a handful of Vedic-internal variations — variant case-endings here, variant verb-stems there, variant *sandhi* outcomes in another verse — to civilizational-scale linguistic evolution. The evidence base is far smaller than the claim. The machinery makes *two-form alternations* and *recensional-marginal variants* support *the entire evolution from Vedic to Classical Sanskrit*. Wheeler's six bodies and the pyramid's handful of Vedic alternations are doing the same kind of work.

### Replacement or Result

The body keeps a short structural analogy and points to a new endnote containing the names, dates, skeleton counts, quotation, and later reassessment.

### Reason Proposed

The full archaeological history interrupts an appendix centered on Vedic linguistic evidence and repeats the racial-Arya case developed elsewhere.

### What May Have Been Lost

The body loses the memorable sequence of six bodies becoming a race-replacement narrative.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-073 — Extended English, Romance, Chinese, and clinical-term drift comparison

**Source:** [Appendix Part 7 §7.6](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_07_vedic_carrier.md:170)  
**Audit block:** [APP-007](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-007---keep-appendix-7-on-the-vedic-evidence)  
**Change type:** CONDENSE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** Existing chapter references remain available for the full examples.

### Material Removed

> Other natural-drift cases show the same pattern:
>
> - **English from Old English to Modern.** The Great Vowel Shift (15th–18th centuries) cascaded through the long-vowel system; the inflectional system collapsed across centuries; phoneme inventories shifted at every position.
> - **Latin to Romance.** The Latin phoneme inventory fragmented across a dozen distinct daughter languages within roughly a thousand years. French lost most word-final consonants; Spanish merged labial/dental distinctions in specific positions; Italian preserved geminates the others lost; Romanian retained a vocative the others lost. Every Romance language differs from the parent at the level of the core phoneme inventory.
> - **Mandarin Chinese from classical to modern.** Historical voiced-obstruent series collapsed; tonal system reshaped; syllabic inventory simplified dramatically.
>
> **Mode two: meaning drift.** The word's phonological form is preserved — often deliberately, through borrowing from a prestige source — but the *meaning* the form was minted to hold slides until it bears no relation to the original. Henry Goddard's coinage of ***moron*** in 1910 (Chapter 5 §5.6's *moron treadmill*) is meaning-drift's clearest signature: from Greek *mōros* (*dull*) imported as a neutral clinical term for mild intellectual disability, the word slid to playground insult within a generation, hardened into slur within two, and was retired from formal usage by ***Rosa's Law*** (2010) and DSM-5 (2013) within a century. The phonological form *moron* survived intact; the *meaning* the form was minted to hold has cascaded out of recognizability.

### Replacement or Result

The body keeps *hlāfweard* → *Lord* as the form-drift example and retains the clinical term as a shorter meaning-drift example, with pointers to Chapters 1 and 5 for the fuller discussions.

### Reason Proposed

The appendix has already established its point through Vedic evidence. The long cross-language catalogue repeats material developed elsewhere and delays the conclusion.

### What May Have Been Lost

The breadth of the natural-drift comparison across several language families becomes less visible.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-074 — Causal and chronological absolutes in Appendix 7

**Source:** [Appendix Part 7 §§7.1, 7.2, 7.5, 7.7](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_07_vedic_carrier.md:17)  
**Audit block:** [APP-007](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-007---keep-appendix-7-on-the-vedic-evidence)  
**Change type:** NARROW CLAIM  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** —

### Material Removed

> ...but no **व्याकरण (*vyākaraṇa*)** text yet exists to describe it.
>
> ...across thousands of years before Pāṇini sits down to describe it.
>
> **No *vyākaraṇa* text yet exists to describe what is operating.**
>
> While *devaiḥ* remains shorter and *devebhiḥ* longer, meter alone decides the deployment.
>
> ...all functioning before any *vyākaraṇa* text exists to describe them.

### Replacement or Result

The revision compares the Vedic evidence with the surviving Pāṇinian documentation and describes what the cited metrical examples show without claiming that meter alone caused every alternate.

### Reason Proposed

The survival of Pāṇini's work does not establish the absence of every earlier analytical text. Occurrence in metrical positions supports a metrical function but does not by itself prove exclusive causation.

### What May Have Been Lost

The older prose states Vedic priority and metrical purpose more categorically.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-075 — Appendix 8 pre-restructure text

**Source:** [Appendix Part 9](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_09_codification_story.md:1)  
**Audit block:** [APP-008](../../80_completed/manuscript_readability_review_codex/27_appendices.md#app-008---reduce-and-reorganize-appendix-8)  
**Change type:** CONDENSE + REORGANIZE  
**Status:** UNDECIDED  
**Applied:** YES  
**Destination if moved:** [Exact pre-restructure snapshot](appendix_08_codification_story_pre_readability_restructure.md)

### Material Removed

The complete 7,530-word pre-restructure appendix is preserved verbatim in [Appendix 8 before the readability restructure](appendix_08_codification_story_pre_readability_restructure.md). The principal consolidations are:

- the draft metadata and repeated introductory verdicts;
- §§8.1–8.2, combined into one account of the inherited story and its two drift claims;
- §§8.5–8.8, combined around domain, mode, the pre-Pāṇinian decoding disciplines, and Patañjali's established bond;
- §§8.9–8.10, reduced to a shorter comparison of actual language change;
- §§8.11–8.12, combined into one calibration-audit section;
- §§8.15–8.18, combined into the institutional explanation, comparison table, replacement model, and final verdict;
- repeated hammers and repeated inventories already developed in the body chapters and Appendix Part 7.

### Replacement or Result

The revised appendix uses nine sections in the accepted order:

1. inherited story and two drift claims;
2. circular chronology;
3. three possible models;
4. domains, modes, and evidence before Pāṇini;
5. actual language change;
6. calibration audit;
7. optionality and Mitanni;
8. why the story persists;
9. comparison table and conclusion.

### Reason Proposed

The original eighteen-section appendix repeated several body chapters and delayed its calibration test until after a long control-case comparison. The accepted audit called for a 30–45 percent reduction while preserving the evidence, comparison table, and strongest verdict.

### What May Have Been Lost

The revised appendix restores the main Same-Timeline Test, representative Vedic and English passages, and the named pre-Pāṇinian analytical field. The snapshot still contains the fuller versions of those demonstrations, the extended institutional analysis, and every repeated closing hammer. Readers reviewing the reduction should consult that file before deciding whether any additional example or beat should return.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-076 — The earlier dṛś, paśyati, and theory indictment

**Source:** [Chapter 18 §18.9](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:296)
**Audit block:** [C18-007](../../80_completed/manuscript_readability_review_codex/23_ch18.md#c18-007---bound-the-dṛś-paśyati-and-theory-case)
**Change type:** REPHRASE + EXPANSION
**Status:** UNDECIDED  
**Applied:** YES
**Destination if moved:** —

### Material Removed

> **One Sanskrit *dhātu*. The Western philological machinery splits the family.** And the splinter is in plain print on the same reference page. The Wiktionary entry for पश्यति, retrieved verbatim:
>
> > The entry claims that पश्यति (*paśyati*) derives from Proto-Indo-European \*speḱ-, while the rest of the paradigm derives from Proto-Indo-European \*derḱ-.[NOTE: wiktionary-pasyati-suppletion]
>
> In one sentence, the pyramid admits the splinter: what Sanskrit treats as one *dhātu* with one paradigm, the pyramid's account attributes to *two* reconstructed PIE ancestor-forms. The connector word is *suppletive* — the technical name for the account's confession. When the inflected forms of what looks like one verb refuse to be traced back to one ancestor, the reconstruction regime invokes *suppletion*: the doctrine that different verb-forms come from different ancestral forms and have, by historical accident, fused into one paradigm. The Pāṇinian architecture does not need *suppletion* anywhere; it generates पश्यति from दृश् through standard present-tense derivation, and a Sanskrit schoolchild can show the steps. The PIE machinery invokes *suppletion* here because it cannot explain how the दृश्-class forms and the पश्यति-class forms can both belong to one verb.
>
> *Suppletion is not a feature of the language. It is the regime's signature on its own failure.*
>
> The third row of the table — *theory* — sharpens the same point in a different idiom. The English word inherits the visual semantics of ⟪दृश्⟫ through the Greek chain *theōros* (spectator, seer); the machinery, however, lists no Sanskrit cognation for *theory* in its standard reference account, routing the cognate cluster instead to a tentative **\*wer-(3)** "to perceive" (Watkins's "perhaps") with no Sanskrit derivative attached. Where row 1 and row 2 split the *dhātu*, row 3 drops the *dhātu* altogether — the Sanskrit semantic origin of *seeing as theory* simply does not appear in the ecosystem's account of where *theory* comes from.

### Replacement or Result

Chapter 18 retains the split-family indictment, corrects the account of **पश्यति (*paśyati*)** by identifying Pāṇini's stated replacement operation, and expands the *theory* row into a worked fivefold *vyutpatti*. The new analysis states the proposed **द → त → थ (*d → t → th*)** change, vowel and ending additions, loss of *ś*, and continuity of the semantic field.

### Reason Proposed

The earlier passage treated the *theory* connection as a semantic assertion without showing the derivational method. It also claimed too broadly that the Pāṇinian architecture required no operation resembling suppletion, even though Pāṇini explicitly prescribes the replacement of *dṛś* by *paśya* in the relevant environment.

### What May Have Been Lost

The replacement softens two original hammers: "the splinter is in plain print" and "the regime's signature on its own failure." Both remain available here if the author later decides that the corrected explanation can support either line.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-077 — The earlier five-step nectar protocol

**Source:** [Epilogue, "Where the Nectar Rises"](/Users/paragtope/projects/writing/books/atomicSanskrit/as_2_01_epilogue.md:67)
**Audit block:** [EPI-009](../../80_completed/manuscript_readability_review_codex/25_epilogue.md#epi-009---make-vyutpatti-the-university-research-protocol)
**Change type:** REPHRASE + EXPANSION
**Status:** UNDECIDED
**Applied:** YES
**Destination if moved:** —

### Material Removed

> The method can be repeated:
>
> 1. Place one starred reconstruction beside the recorded word-family it was designed to explain.
> 2. Search the *Dhātupāṭha* for Sanskrit atoms that fit both sound and meaning.
> 3. Derive the Sanskrit molecules under stated Sanskrit rules.
> 4. Compare them with the recorded forms and identify plausible routes of contact.
> 5. Publish weak cases, counterexamples, and uncertainty along with the strong results.
>
> The sound correspondences, cognate tables, etymological dictionaries, inscriptional corpora, and university departments need not be discarded; they need to be turned around. The work ahead maps two fields: the orbital field bound by Sanskritic gravity, and the radiance-field where Sanskritic reflections traveled outward and then drifted.

### Replacement or Result

The Epilogue now assigns the method explicitly to Indian universities, joins Sanskrit, Greek, Latin, Persian, and computational analysis in one program, adds the fivefold *vyutpatti* operations to the protocol, and points back to the worked **⟪अस्⟫ / ⟪भू⟫** example in Chapter 18.

### Reason Proposed

The earlier checklist did not explain how scholars should compare the forms, and it did not identify the departments capable of carrying out the program. The expanded protocol turns the invitation into a method that can be repeated and evaluated.

### What May Have Been Lost

The replacement preserves the original reversal by making Indian scholars the actors who turn the machinery around.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```

---

## LAF-R-078 — The retired ⟪दृश्⟫–*theory* case

**Source:** Chapter 18 §18.9; Appendix Part 1 §1.5; Epilogue, "Where the Nectar Rises"; supporting endnotes
**Checkpoint:** `a922e903`
**Change type:** REPLACE + RELOCATE
**Status:** DEVELOP LATER
**Applied:** YES
**Destination:** [Dedicated Lost and Found record](drsh_theory_case_lost_and_found.md)

### Material Removed

The worked **⟪दृश्⟫ / पश्यति / theory** case, its appendix summary, its epilogue pointer, and its two supporting endnotes were removed from active deployment. The dedicated record preserves the complete Chapter 18 section and appendix case; checkpoint `a922e903` preserves the exact final state of the former endnotes.

### Replacement or Result

Chapter 18 §18.9 now uses **⟪अस्⟫ / ⟪भू⟫** and Latin ***sum, esse, fuī, futūrus***. The replacement begins with the two Sanskrit atoms, shows both already operating in Ṛgveda 10.129, presents Pāṇini's later documentation in **अस्तेर्भूः (2.4.52)**, and then applies the fivefold *vyutpatti* method to the recorded Greek and Latin forms.

### Reason Proposed

The *dṛś–theory* derivation depended on a sound path that had not yet been tested across a larger set of families, while the Sanskrit-side reason for the **दृश् / पश्य** relationship remains open. The **⟪अस्⟫ / ⟪भू⟫** case supplies a visible Sanskrit rule and a familiar Latin paradigm.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [x] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN

### Author Comments

```text
The dṛś case may return after the Sanskrit-side architecture and the proposed Greek sound path have been investigated separately.
```

---

## LAF-R-079 — Modern linguistics vs. Patañjali's refusal (Ch5 §5.2 area)

**Source:** [Chapter 5](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_05_siddha.md)
**Audit block:** none — found during commit review 2026-08-12, not tracked by any C05 item
**Change type:** CUT
**Status:** Found already cut in the working tree
**Applied:** YES (already on disk before this ledger entry was written)
**Destination if moved:** Not relocated

### Material Removed

> Modern linguistics begins entirely elsewhere, treating the relationship between word and meaning as conventional, contingent, and historically mutable. Because speech communities make the bond and later speech communities remake it, historical linguistics merely studies that remaking. In contrast, Patañjali begins from a total refusal of that premise: the bond does not drift, has not drifted, and will not drift, simply because the bond is already *siddha*.

### Replacement or Result

No direct replacement at this location. A related but differently-worded contrast between modern linguistics and Patañjali's *kārya*/*siddha* distinction appears later in the chapter (see LAF-R-081, the C05-004 area).

### Reason Proposed

Not recorded — the cut predates this ledger entry.

### What May Have Been Lost

The specific claim that historical linguistics "merely studies" the remaking of the bond, and the three-part refusal formula ("does not drift, has not drifted, and will not drift").

---

## LAF-R-080 — "The dogma's codification vocabulary fundamentally fails" (Ch5, old §5.4)

**Source:** [Chapter 5](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_05_siddha.md)
**Audit block:** none — found during commit review 2026-08-12, not tracked by any C05 item
**Change type:** CUT
**Status:** Found already cut in the working tree
**Applied:** YES (already on disk before this ledger entry was written)
**Destination if moved:** Not relocated

### Material Removed

> The dogma's *codification* vocabulary fundamentally fails at this point because codification imagines drift first and order later. By contrast, Patañjali provides the exact opposite: an established bond first, followed by grammatical defense afterward. Therefore, there is no transition from disorder to order; there is only order, and subsequent slips from that order.
>
> Patañjali's *Mahābhāṣya*, standing over Pāṇini's *Aṣṭādhyāyī*, called the bond *siddha*. The engineering conclusion follows: grammar calibrates usage against an established architecture.

### Replacement or Result

No direct replacement — old §5.4 ("Sanskrit Begins from Permanence") was replaced wholesale by a new §5.5 ("The Evidence Before and After Pāṇini") covering related but differently structured ground (see LAF-R-081).

### Reason Proposed

Not recorded — the cut predates this ledger entry.

### What May Have Been Lost

The explicit "codification imagines drift first, order later" contrast, and the closing hammer naming the *Mahābhāṣya* as standing over the *Aṣṭādhyāyī* and calling the bond *siddha*.

---

## LAF-R-081 — "Sanskrit Begins from Permanence" (old §5.5, full section)

**Source:** [Chapter 5](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_05_siddha.md)
**Audit block:** none — found during commit review 2026-08-12, not tracked by any C05 item
**Change type:** REPLACE (whole section)
**Status:** Found already replaced in the working tree
**Applied:** YES (already on disk before this ledger entry was written)
**Destination if moved:** Not relocated; superseded by new content covering related ground

### Material Removed

> Patañjali's argument rests on two claims.
>
> First: by treating the bond between a word and its meaning as fixed, Patañjali automatically rejects the premise of change and drift. Modern historical linguistics assumes languages mutate, drift, and renew, and the linguist tracks the trajectory. Patañjali's framework refuses that assumption at the metaphysical level: grammar exists to defend the bond.
>
> The second: Sanskrit begins from permanence, a premise that accommodates error without treating variation as the bond's behavior. Patañjali fully recognized variation, misuse, and corruption, but maintained that the bond remains established while speakers slip from it. The *vaiyākaraṇaḥ* keeps that bond visible against the linguistic slips.
>
> The engineered Sanskrit thesis is therefore not alien to the Sanskrit lineage. Engineering language restates Sanskrit's own grammatical self-description. *Engineered first* states the architecture's priority. *Siddha* captures the architecture's metaphysical property. There is no codification event because there is no transition from drift to fixity. The bond was *siddha* before Pāṇini sat down to document it; it remained *siddha* after he finished. Pāṇini documented a *siddha* system. Patañjali says so at the opening of the *Mahābhāṣya*.
>
> Without *siddha*, there is nothing to defend. Chapter 6 identifies the exact threat this defense was built against.

### Replacement or Result

Replaced by a new section, "## 5.5 The Evidence Before and After Pāṇini," which reorganizes the chapter around a before/after-Pāṇini evidentiary structure (Vedic and pre-Pāṇinian evidence establishing prior existence; Patañjali explaining grammar's regulatory role afterward) rather than the two-claims "Sanskrit begins from permanence" structure.

### Reason Proposed

Not recorded — the replacement predates this ledger entry.

### What May Have Been Lost

The "two claims" framing itself, the explicit line "Sanskrit begins from permanence," and the closing hammer "Without *siddha*, there is nothing to defend."

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN

### Author Comments

```text
Flagged during commit review 2026-08-12 — recommend author confirm the new §5.5 is the intended final replacement.
```

---

## LAF-R-082 — Patañjali's priority over the modern change-categories (§6.3 close)

**Source:** [Chapter 6](/Users/paragtope/projects/writing/books/atomicSanskrit/manuscript/as_1_06_apabhramsa.md)
**Audit block:** none — found during a drift/deviation/divergence review, 2026-08-17
**Change type:** CUT (paragraph), during the revision that installed the three-term drift / deviation / divergence distinction
**Status:** Cut in the working tree; partially restored as one sentence (see Replacement or Result)
**Applied:** YES (cut was already on disk before this entry was written)
**Destination if moved:** Not relocated

### Material Removed

> Modern linguists describe comparable changes through categories such as phonetic erosion, morphological reanalysis, and lexical replacement. Long before those categories appeared, Patañjali had already documented the central asymmetry: many circulating departures gather around one calibrated form. His *gauḥ* example does more than list variants. It compares them with Sanskrit's architecture, places *gauḥ* at the calibrated center, and records how quickly the possible departures multiply around it.

### Replacement or Result

Three of the paragraph's five clauses survive in the revised chapter and need no restoration:

- *gauḥ* at the calibrated center, and the list as comparison rather than enumeration → §6.3 retains, in sharper form: "His list therefore establishes a center and compares several departures with it, rather than treating five circulating forms as equally constitutive of the language."
- departures multiplying quickly → §6.2 retains: "the corruptions multiply much faster than the calibrated words they distort."

What did not survive was the naming of the modern categories and the priority claim over them. One sentence was added at the §6.3 close on 2026-08-17 to carry that move in compressed form:

> Modern linguistics later labeled these movements phonetic erosion, morphological reanalysis, and lexical replacement. Patañjali had already analyzed all three in *gauḥ*.

### Reason Proposed

Not recorded. The cut appears incidental to the three-term revision rather than deliberate: the revision's work was in §6.4 and §6.7, and this paragraph sat at the close of §6.3.

### What May Have Been Lost

The heroic-erasure counter-punch at the point where the *gauḥ* evidence is freshest — naming *phonetic erosion*, *morphological reanalysis*, and *lexical replacement* specifically, and asserting Patañjali's priority over all three. The added sentence restores the move but not the paragraph's full development.

**Note on prior history:** the ledger's contradiction-repair table, entry **A6 — Chapter 6 Patañjali**, records this material as previously cut and deliberately *restored* ("Restored Patañjali's prior architectural analysis"). This is therefore its second removal, which is why it is logged here rather than left as an ordinary compression.

**Related:** LAF-R-081's Replacement note records a differently-worded contrast between modern linguistics and Patañjali's *kārya* / *siddha* distinction elsewhere in Chapter 5; the two make adjacent but distinct claims.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [x] INCORPORATE PART — one-sentence version added at §6.3 close, 2026-08-17
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN

### Author Comments

```text
The one-sentence restoration is provisional. If the fuller paragraph is wanted back, the
clauses it duplicated (center/comparison, multiplication rate) should be trimmed so the
restored text does not repeat §6.2 and the surviving §6.3 sentence.
```
