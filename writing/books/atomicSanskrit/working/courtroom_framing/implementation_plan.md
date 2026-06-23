# Courtroom Framing — Implementation Plan

> *Working document. Paraphrases and integrates Codex's input (`codex_input.md` in this folder) with the book's existing vocabulary and structural commitments. Outlines the four explicit deployments of the courtroom metaphor and the implementation phases. To be archived (this whole folder) when the work is complete.*

---

## What this is

A plan to make the book's already-prosecutorial arc **quietly explicit** through four targeted touchpoints — without renaming chapters, without theatrical labeling, and without sweeping new vocabulary across the manuscript.

The book's structure already reads as a prosecution; Codex mapped the existing arc cleanly:

| Courtroom role | Where in the book |
|---|---|
| Reader orientation | Front Matter (Preface, Ch 0) |
| **The prosecution announced** | **Prologue (*The Prosecution*)** |
| The charge | Part I (Chs 1–3) |
| Internal testimony | Part II (Chs 4–6) |
| Physical evidence | Part III (Chs 7–9) |
| Technical evidence | Part IV (Chs 10–12) |
| Chain of custody | Part V (Chs 13–15) |
| Cross-examination and verdict | Part VI (Chs 16–18) |
| The remedy | Part VII (Ch 19) |
| The closing statement | Epilogue (*Make the World Ārya*) |
| Exhibits | Appendices, figures, companion |

The ***Prologue — The Prosecution*** and ***Epilogue — Make the World Ārya*** bookend the book's prosecutorial arc as discrete dedicated divisions.

The touchpoints below give the reader the prosecutorial map at the surface level without making the book feel like a courtroom gimmick.

---

## The four-layer vocabulary hierarchy

The book has accumulated four levels of vocabulary for the orthodoxy's apparatus. The plan formalizes the hierarchy without disturbing the existing deployments:

| Level | Term | What it names |
|---|---|---|
| Surface (doctrine) | *the orthodoxy* | the claims, categories, approved explanations |
| Institutional | *the church of progress* | the institutional carrier |
| Functional | *priests / missionaries / jihadis of progress* | sub-classes by function |
| Structural | ***the asuric pyramid*** (Ch 3 §3.6) | what the formation IS |

Existing deployments of *orthodoxy* / *church of progress* / etc. stay where they are. The plan adds ***asuric pyramid*** as the explicit name of the accused at the four courtroom-framing touchpoints only — not a sweep.

Codex considered Greek/Latin coinages (*tenebrocracy*, *skotocracy*, *archontic pyramid*, *dominarchy*, *tenebral pyramid*) and rejected them as pulling away from the book's Sanskrit-native diagnostic vocabulary. ***Asuratva*** / ***asuric pyramid*** already gives the exact category; no new coinage is needed.

---

## The four touchpoints

### Touchpoint 1 — Prologue: *The Prosecution* (new file)

**Where:** A new dedicated file at `as_0_02_prologue.md` (zone 0 = front matter), placed in reading order between the Preface (`as_0_01_preface.md`) and Ch 0 (`as_1_00_seekers.md`).

**Why a Prologue rather than a Preface paragraph:** Codex's initial recommendation was a paragraph near the end of the Preface. The Preface already carries chronology refusal, terminology note, methodology, personal hook, the *Nāsadīya Sūkta* epistemic stance, and the *Two speculations* seed — embedding the prosecutorial frame as one more paragraph would get lost in that density. A dedicated Prologue isolates the courtroom-frame announcement so it lands as its own beat. The Prologue is intentionally short — a placard before the body, not a discussion.

**Full Prologue text** (verbatim — the entire content of the new file, with the H1 title):

```markdown
# Prologue — The Prosecution

This book proceeds as a prosecution.

The accused is not every scholar, every institution, or every Western reader. The accused is the *asuric pyramid* — the apex-and-layer formation Chapter 3 names — that converted Sanskrit into data, data into doctrine, and doctrine into containment.

The evidence is the architecture: the mouth-map, the *varṇamālā*, the *dhātuḥ*, the *Dhātupāṭha*, the calibration matrix, the recitation lineages, the retroflex row, and the false ancestor built to contain them.

The injured party is the civilization forced to answer to a false description of its own language.

The verdict comes late because verdicts must be earned.

This book borrows the courtroom framing because the *asuric pyramid* understands the courtroom. The modern judicial imagination across much of the world was shaped inside Abrahamic and post-Abrahamic frames: law as command, guilt as violation, justice as punishment, argument as adversarial contest, verdict as victory over the opposing side. The book uses that form deliberately. The *asuric pyramid* built an accusatory apparatus around Sanskrit; the book answers inside a form that apparatus recognizes.

The Epilogue leaves the borrowed courtroom and returns to the Indic frame: not punishment, but karma; not payback, but recalibration; and finally, the recovery of an aspiration the nineteenth and twentieth centuries taught the world to misread.
```

**Rhetorical notes:**

- The Prologue's title (*The Prosecution*) IS the courtroom-frame name; no separate italicized subtitle is added. Symmetric with the Epilogue, whose title (*Make the World Ārya*) is dharmic and whose courtroom subtitle (*The closing statement.*) does the arc-frame work.
- The Prologue runs in **two movements**:
  - **First five paragraphs (the indictment)** — name the accused, the evidence, the injured party, the verdict's earned-status.
  - **Last two paragraphs (the form-and-frame)** — explain *why* the book borrows the courtroom (the *asuric pyramid* understands that form) and preview *what comes after the courtroom* (the Epilogue's return to the Indic frame). The two-movement structure makes the Prologue self-contained: it announces, justifies its form, and previews its eventual exit.
- *Asuric pyramid* appears three times in the Prologue. This is intentional drumbeat — the term gets installed at the entry door. (Outside the Prologue, the term is rationed: once in the Ch 18 three-beat close; twice or so in the Epilogue moral-asymmetry block.)
- "The injured party is the civilization forced to answer to a false description of its own language" — preserves Sanskrit's power. Codex flagged that "victim: Sanskrit" reads as too passive; the injured-party formulation keeps the polemic frame without weakening Sanskrit.
- The list of evidence (mouth-map / *varṇamālā* / *dhātuḥ* / *Dhātupāṭha* / calibration matrix / recitation lineages / retroflex row / false ancestor) compresses the book's content. Reading the Prologue gives the new reader the architecture-at-a-glance plus the prosecutorial frame.
- The Epilogue-bridge paragraph ("not punishment, but karma; not payback, but recalibration; and finally, the recovery of an aspiration...") explicitly promises the moral arc the Epilogue delivers. The Prologue makes the promise; the Epilogue carries it out.

**Build pipeline note:** `build_book.py` needs to be told the Prologue belongs in the front matter between the Preface and Ch 0. The existing zone-0 ordering sorts numerically, so the `02` slot puts the Prologue right after the Preface (`as_0_01_*`). Verify the `assemble` phase picks it up correctly before the body assemblies.

### Touchpoint 2 — Part subtitles + Part VII split

**Where:** The three TOC files (`reference/as_toc.md`, `reference/as_toc_annotated.md`, `reference/as_toc_notes.md`); optionally also the part-divider line at the top of the first chapter of each part if those exist in the chapter files.

**Why:** Gives the reader the prosecutorial map at the TOC level. Current Part titles stay; subtitles do the courtroom work. Codex's strongest catch: *Chain of custody* for Part V (preservation chapters literally prove the architecture was not corrupted across thousands of years — courtroom-native AND book-native simultaneously).

**Two changes are bundled in this touchpoint:**

1. **Subtitles added** to every division of the book (italicized one-line callouts beneath the existing division title).
2. **Part VII split out from Part VI.** Ch 19 (*Life After PIE*) moves from the current Part VI (which presently groups Chs 17–19) into its own new **Part VII — Life After PIE**. The structural change tightens Part VI to Chs 16–18 — exclusively cross-examination + verdict — and gives the affirmative answer its own dedicated Part. The Epilogue (***Make the World Ārya***) stays as its own division between Part VII and the Appendices, carrying the *closing statement* that bookends the Front Matter's *opening statement*.

**Proposed structure (the full division-by-division map):**

| Division | Title | Courtroom subtitle | Contents |
|---|---|---|---|
| **Front Matter** | *(existing front matter)* | *(no courtroom subtitle — Preface / Ch 0 do orientation work, not prosecutorial)* | Preface, Ch 0 |
| **Prologue (new)** | **The Prosecution** | *(no separate subtitle — the title IS the prosecutorial frame)* | five-paragraph prosecutorial statement (see Touchpoint 1) |
| **Part I** | The Wrong Metaphor | *The charge.* | Chs 1–3 |
| **Part II** | The Sanskrit Self-Conception | *Internal testimony.* | Chs 4–6 |
| **Part III** | The Sound-Field | *Physical evidence.* | Chs 7–9 |
| **Part IV** | The Atomic Architecture | *Technical evidence.* | Chs 10–12 |
| **Part V** | Anti-Entropy in Practice | *Chain of custody.* | Chs 13–15 |
| **Part VI** | Killing PIE | *Cross-examination and verdict.* | Chs 16–18 |
| **Part VII (new)** | **Life After PIE** | *The remedy.* | **Ch 19** |
| **Epilogue** | **Make the World Ārya** | *The closing statement.* | reader-facing close: Wave 3 as personal obligation; Rigvedic mantra landing; moral-asymmetry block (Touchpoint 4) |
| **Appendices** | *(existing appendix titles)* | *Exhibits.* | Appendix Parts 1–6 |

The ***Prologue — The Prosecution*** and ***Epilogue — Make the World Ārya*** are discrete dedicated divisions at the two extremes of the book, bookending the courtroom arc. Front Matter (Preface + Ch 0) does orientation work and does not need a courtroom subtitle.

**Format example** (in markdown — Part name on first line, italicized subtitle on second line):

```markdown
## Part V — Anti-Entropy in Practice
*Chain of custody.*
```

**File-naming note:** the chapter file `as_1_19_life_after_pie.md` (zone 1 = body) stays in zone 1; the Epilogue file `as_2_01_epilogue.md` (zone 2 = end matter) stays in zone 2. No file renames are needed. The Part-VII grouping is a TOC-level division, not a file-zone change.

### Touchpoint 3 — Ch 18 three-beat close

**Where:** End of Chapter 18, immediately after the PIE verdict is formally rendered.

**Why:** Ch 18 closes the prosecution on PIE specifically; the three-beat close is the prosecutorial-arc cadence-marker. Codex initially suggested Ch 17 for a single closing line, but Ch 18 carries the actual verdict — the close lands harder there (see decision point). The three beats do three distinct jobs: (a) formal conviction; (b) explicit naming of the perpetrator (pulls *asuric pyramid* into the close, where the four-layer hierarchy promises it); (c) cadence-marker that rests the prosecutorial arc.

**Proposed close** (three discrete short lines, deployed exactly once across the manuscript):

> ***The accused is now convicted.***
>
> ***The asuric pyramid is the perpetrator.***
>
> ***The prosecution rests.***

Each line is its own beat — typeset as three separate emphasized lines, not one paragraph. The progression: *verdict → perpetrator named → prosecution rests.*

**Discipline:** the three lines appear exactly once across the manuscript. No earlier mention. No Epilogue echo. The block is the cadence-marker for the prosecutorial arc and only that.

### Touchpoint 4 — Epilogue moral-asymmetry block

**Where:** As a closing movement in the Epilogue (***Make the World Ārya***), before (or absorbing) the existing *kṛṇvanto viśvam āryam* close. The Epilogue is its own division under the new structure (between Part VII and the Appendices); the moral-asymmetry block becomes the substantive content of *The closing statement.*

**Why:** The courtroom frame, left unqualified, risks turning the dharmic conclusion into vengeance — which would betray Sanātan's own moral universe. The block names the asymmetry explicitly: borrowed adversarial instrument vs. dharmic restoration.

**Proposed prose** (Codex's draft, lightly tightened; the why-the-courtroom paragraph has moved to the Prologue's two-movement structure, so the Epilogue now opens directly on the verdict's aftermath):

> The book does not end where the adversarial form ends. A verdict is necessary because false description has consequences. The *asuric pyramid* has committed a civilizational wrong: it misnamed Sanskrit, buried the architecture, manufactured an ancestor, and taught the falsehood back to Hindus as knowledge. That wrong must be named. PIE must die.
>
> What follows is not revenge. *Sanātan* does not keep the same moral ledger. The dharmic frame is karmic: action bears consequence, but restoration remains possible when action changes. The close of the book therefore turns from conviction to recalibration. Nineteenth-century Europe wanted to be *ārya*, but it reserved *āryatva* for the apex of its own racial pyramid. The book rejects the pyramid and keeps the aspiration. Let them become *ārya* also. Let everyone become *ārya*.
>
> The verdict is death for PIE, not death for the people who inherited it. The remedy is not payback. The remedy is re-learning.
>
> ***Convict the pyramid. Kill the false ancestor. Invite the world.***
>
> *kṛṇvanto viśvam āryam* — make the whole world *ārya*.

The closing three-beat formula (***Convict the pyramid. Kill the false ancestor. Invite the world.***) is the book's named moral sequence.

**Note on the Prologue→Epilogue handoff:** the Prologue's last paragraph explicitly promised: *"The Epilogue leaves the borrowed courtroom and returns to the Indic frame: not punishment, but karma; not payback, but recalibration; and finally, the recovery of an aspiration the nineteenth and twentieth centuries taught the world to misread."* The Epilogue paragraphs above deliver each promised beat: *"Sanātan does not keep the same moral ledger. The dharmic frame is karmic"* (karma); *"The close of the book therefore turns from conviction to recalibration"* (recalibration); *"Nineteenth-century Europe wanted to be ārya, but it reserved āryatva for the apex of its own racial pyramid. The book rejects the pyramid and keeps the aspiration"* (the misread aspiration restored). The Prologue makes the promise; the Epilogue delivers each beat in sequence.

---

## Discipline rules (locked)

1. ***Asuric pyramid*** is deployed only at the four courtroom-framing touchpoints (Preface paragraph, Ch 18 three-beat close, Epilogue moral-asymmetry block — three deployment sites across the manuscript). **Do not sweep** *orthodoxy* → *asuric pyramid* across the book. The hierarchy depends on the distinction; the existing surface / institutional / functional terms keep doing their work elsewhere.
2. The **Ch 18 three-beat close** is deployed exactly once. End of Ch 18 (proposed). No earlier mention of any of the three lines. No Epilogue echo of the *prosecution rests* line. The block is the cadence-marker for the prosecutorial arc and only that.
3. No *courtroom* / *trial* / *defendant* / *jury* vocabulary sprinkled through the manuscript. Four touchpoints, full stop.
4. Part subtitles are italicized one-line callouts in the TOC files, not chapter-spanning headers.
5. Codex initially proposed renaming Parts (e.g., *Part I — The Charge*). **Rejected** — the current Part titles carry the book's substantive register. Subtitles are an overlay, not a replacement.

---

## Items deferred / out of scope

- **Greek/Latin coinage search** for the asuric-pyramid referent (*tenebrocracy*, *skotocracy*, etc.). Codex considered and rejected; agree.
- **Minor TOC cleanup** items Codex flagged: Part V's old section labels (`14.1`, `15.1`, `16.1`) under Chapters 13–15 in `as_toc_annotated.md`; Ch 3 status marked "in planning" though the file is drafted. Separate housekeeping pass, lower priority.
- **A standalone "Charge sheet" page** at the front of the book. Codex's draft (asuric pyramid / civilizational containment through false description / Sanskrit continuum / architecture / PIE must die / make the world *ārya*) could become a standalone framing page. Deferred until the four touchpoints are in place and we can see how visible the courtroom map is.

---

## Implementation phases

### Phase 1 — Lightweight framing
- Touchpoint 1 (new `as_0_02_prologue.md` file with the five-paragraph prosecutorial statement)
- Touchpoint 2 (Part subtitles + Part VII split + Epilogue title in the three TOC files; build-pipeline check)
- One commit.

### Phase 2 — Verdict close
- Touchpoint 3 (*The prosecution rests* at end of Ch 18).
- Smallest commit.

### Phase 3 — Epilogue moral-asymmetry block
- Read current Epilogue close.
- Slot in the Codex-drafted block (lightly tightened).
- Largest commit; biggest narrative move.

---

## Open decisions (discussion before Phase 1 starts)

### Decision 1 — Part VI subtitle wording [RESOLVED — *Cross-examination and verdict*]

The user resolved this in conjunction with the Part VII split (2026-05-19). With Ch 19 moved out of Part VI into its own Part VII, Part VI now contains only Chs 16–18 — cross-examination (Ch 16 *āryatva* + Ch 17 architectural test) plus verdict (Ch 18). The earlier concern about *cross-examination* being too narrow no longer applies; the split tightens Part VI to exactly the cross-examination-and-verdict scope.

Locked subtitle: ***Cross-examination and verdict.***

### Decision 2 — Where the Ch 18 three-beat close lands

| Option | Location | Rationale |
|---|---|---|
| **A** (recommended) | End of Ch 18 | Ch 18 renders the verdict; the three-beat close lands as the formal close of the prosecutorial arc. *Asuric pyramid* gets explicitly named as the perpetrator at the close — pulls the four-layer hierarchy into the cadence. |
| B | End of Ch 17 | Codex's initial suggestion. Ch 17 establishes the architectural test; the verdict is Ch 18's job. |
| C | Both Ch 18 and Epilogue | Echoed twice. Risks dilution of the "use it once" discipline. |

### Decision 3 — Phase order and review checkpoints

| Option | Approach |
|---|---|
| **A** (recommended) | Phase 1 first, review the TOC-level map, then Phases 2 and 3. |
| B | All three phases in one pass; commit per phase. |
| C | Phase 1 only; defer Phases 2 and 3 to a future session. |

---

## Files that will be touched

**Phase 1:**
- `as_0_02_prologue.md` — **new file**, full Prologue text per Touchpoint 1.
- `reference/as_toc.md` — Part subtitles + Prologue entry + Part VII split (Ch 19 out of Part VI into new Part VII) + Epilogue title (*Make the World Ārya*).
- `reference/as_toc_annotated.md` — Part subtitles + Prologue entry + Part VII split (the structural reorganization is most visible in this file since it carries chapter summaries).
- `reference/as_toc_notes.md` — Part subtitles + Prologue entry + Part VII split (working document; align with the canonical TOCs).
- `working/as_todo.md` — note the structural change (new Prologue, Part VII split, Epilogue title) so the next session has the new architecture visible at a glance.
- `CLAUDE.md` — update the file-map / structure references if any cross-references invoke "Part VI Chs 16–19" or the front-matter file list; add the Prologue to the front-matter listing.
- `build_book.py` — verify the `assemble` phase picks up `as_0_02_prologue.md` in the right position (between Preface and Ch 0). The existing zone-0 numerical sort should handle it automatically; verify and patch if not.

**Phase 2:**
- `as_1_18_pie_in_sky.md` — Touchpoint 3 closing line.

**Phase 3:**
- `as_2_01_epilogue.md` — Touchpoint 4 moral-asymmetry block.

---

## Folder lifecycle

This folder (`working/courtroom_framing/`) holds two files:
- `codex_input.md` — Codex's original input (paraphrased and integrated into this plan).
- `implementation_plan.md` — this file.

When the four touchpoints are deployed and the implementation passes a final review, the folder moves to `archive/` per the project's archive convention. No content from this folder belongs in the published manuscript.
