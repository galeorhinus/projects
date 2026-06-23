# Draft 2 Structural Read Checklist

Purpose: move Draft 1 from writing mode into editorial production mode. This file tracks the structural read before manuscript edits. First collect issues, then revise deliberately.

Status key:

- `[ ]` Not started
- `[~]` In progress
- `[x]` Completed

## Pass Checklist

- `[x]` **Pass 1 — Reader Orientation**
  - Question: does the reader always know what the book is doing?
  - Scope: Preface, About Series, Prologue, Ch0, Ch1, Part openings, Epilogue.
  - Look for: terminology introduced too early, polemic before evidence, unclear book promise, missing reader handholds.

- `[x]` **Pass 2 — Argument Escalation**
  - Question: does the book move cleanly from claim -> evidence -> prosecution -> verdict -> invitation?
  - Scope: full chapter sequence.
  - Look for: premature verdicts, evidence arriving too late, prosecutions without prior grounding, remedy not connected to verdict.

- `[x]` **Pass 3 — Architecture Spine**
  - Question: do the architectural chapters form one continuous build?
  - Scope: Ch8-Ch14.
  - Track: sonomer -> akṣara/audiograph -> dhātuḥ -> kriyā -> vākya -> calibration matrix.
  - Look for: missing handoffs, repeated definitions, discontinuity between Ch10-12, Ch14 not answering Ch10 strongly enough.

- `[x]` **Pass 4 — Polemic Calibration**
  - Question: does the antagonist language land with force without drowning the evidence?
  - Scope: Prologue, Ch1-Ch3, Ch17-Ch18, Appendix Parts 1-3, Epilogue.
  - Track terms: orthodoxy, church of progress, asuric pyramid, codification, gaslighting, heroic erasure.
  - Look for: overuse, underdefined terms, register jumps, places where evidence should lead before accusation.

- `[x]` **Pass 5 — Chapter Opening / Close**
  - Question: does every chapter open with a clear task and close by handing off?
  - Scope: all chapters and appendices.
  - Look for: weak first paragraphs, draft-note residue, missing forward pointers, repeated closings.

- `[x]` **Pass 6 — Epilogue Loop Closure**
  - Question: does the Epilogue answer the Prologue and restore the Indic frame?
  - Scope: Prologue + Epilogue, with spot checks against Ch1, Ch3, Ch18, Ch19.
  - Track: prosecution -> dharmic close; sat / lokakṣema / āryatva; inward correction; final mantra.

## Findings

### Pass 1 — Reader Orientation

| Status | Location | Issue | Why It Matters | Suggested Fix |
|---|---|---|---|---|
| `[x]` | Global front/back matter and early chapters | Visible draft-version metadata and `## Draft notes` remain in source manuscript files, but the production build strips them. | The reader copy should not expose editorial scaffolding. | Validated 2026-05-31: `build_book.py assemble` and `assemble --endnotes short` produce reader-facing markdown with no `Draft v`, `Draft notes`, restoration logs, `[VERIFY]`, or `[TBD]` markers. |
| `[ ]` | Preface opening | The Preface states several high-friction conclusions before the reader has seen the evidence: PIE as imaginary, Sanskrit as source/calibrant for broad language families, and specific etymological claims. | Strong openings are fine, but a new reader may feel asked to accept verdicts before the case has been argued. | Add one brief reader handhold: these are not assumptions but claims the book will prove across the architectural and prosecution chapters, with Ch18/Ch19 pointers if needed. |
| `[x]` | Ch0 §0.4 | The sentence says the contrast “organizes the engineering the preceding chapters describe.” | In Ch0 there are no preceding chapters; the pointer runs backward from the reader’s position. | Changed to “the chapters that follow develop.” |
| `[x]` | Ch0 top draft note and §0.11 | The draft note says Ch0 does not argue the engineering thesis, but §0.11 now explicitly introduces engineered speech, procedure, statistical checks, and fractal recurrence. | The source note is stale, but it is not reader-facing in production output. | Production build strips the source note; §0.11 remains a reader-orientation summary, not a proof section. |
| `[x]` | Ch0 §0.8 | “Chapters 11 through 13 establish this generative engine as engineering” no longer matches the current structure. | Ch13 is now preservation/calibration, while Ch10-Ch12 carry the construction spine. | Changed to “Chapters 10 through 12.” |
| `[ ]` | About Series -> Prologue -> Ch0 | Fractal vocabulary, creation triad, courtroom prosecution, and category-theft now arrive early and in quick sequence. | The sequence is powerful, but the reader needs one clean promise: this volume proves the linguistic architecture first; later volumes extend the civilizational architecture. | Keep the material, but recheck after Pass 4 for density. If needed, add one orienting sentence before the Prologue or in Ch0 to separate “this volume proves mouth-to-language” from “later volumes extend language-to-civilization.” |
| `[x]` | Epilogue | The Epilogue source still includes a long restored draft note block after the final mantra. | The final close should end cleanly on the mantra/work-continuance, not on restoration metadata. | Production build strips the draft notes; assembled reader copy ends on the reader-facing close. |

### Pass 2 — Argument Escalation

| Status | Location | Issue | Why It Matters | Suggested Fix |
|---|---|---|---|---|
| `[x]` | Ch13 §13.1 | The roadmap says “The four sections that follow,” but the chapter now has five substantive sections and the sentence only names §13.2-§13.4. | The preservation-to-calibration escalation now includes §13.5 as a major category move; the roadmap undersells the chapter and miscounts the structure. | Added §13.5 as the codification/calibration handoff to Ch14. |
| `[x]` | Ch14 §14.5 | The sentence says the generative architecture was documented by “Chapters 11-13.” | Ch13 is preservation, not the generative-engine chapter; this blurs the escalation from construction to preservation. | Changed to “Chapters 10-12.” |
| `[x]` | Reference TOC, Appendix Part 4 | The Appendix Part 4 section list appears to contain Appendix Part 2 section titles rather than the Language Factory section titles. | The TOC misdirects the reader in the exhibits section after the prosecution/verdict arc. | Replaced with the actual Language Factory headings from `as_3_04_language_factory.md`. |
| `[x]` | Ch18 -> Ch19 -> Epilogue | The escalation works: Ch18 convicts, Ch19 supplies the replacement model, Epilogue restores the dharmic frame. | The remedy chapter should not feel skipped in the Epilogue’s opening summary. | Added the bridge: Ch18 closed the prosecution, Ch19 began the remedy, the Epilogue returns the whole movement to dharmic ground. |
| `[ ]` | Global draft-note residue | Draft notes frequently contain obsolete structural summaries from earlier chapter states. | These stale summaries can conceal real escalation changes and will confuse future audits if left in reader files. | Treat production-note cleanup as prerequisite before final escalation read. |

### Pass 3 — Architecture Spine

| Status | Location | Issue | Why It Matters | Suggested Fix |
|---|---|---|---|---|
| `[x]` | Ch8 close -> Ch9 | Ch8 previously closed by saying the next chapter isolates the retroflex row, but Ch9 first surveys the whole subcontinental sound-field and only later lands the retroflex fingerprint. | The handoff was too narrow for what Ch9 actually does. | Revised the Ch8 close to frame Ch9 as a subcontinental sound-field survey that lands on the retroflex row. |
| `[ ]` | Ch9 §9.7 and §9.11 | Ch9 uses `C`, `V1`, `V2`, and `CVC` notation before Ch10 has fully taught the scaffold vocabulary and icons. | The notation is accurate, but the reader has just been introduced to sonomer/*akṣara*/*mātrā*; the shorthand may feel abrupt. | Add one plain-language sentence before the notation, or move the shorthand explanation into Ch10 while Ch9 keeps the timing table at concept level. |
| `[x]` | Ch12 opening | Ch12 previously promised “names, role-marked words, compounds, and sentences,” but the chapter develops names, bonds, *padāni*, and *vākyāni*. | The chapter promise was broader than the current demonstration. | Removed “compounds” from the opening promise and reserved *samāsa* for a later pass/appendix. |
| `[ ]` | Ch12 §12.9 | Vivimorphosis is strong, but it expands beyond assembly into contact-language theory and Ch18 territory. | The concept is important, but it may pull the chapter from construction spine into PIE prosecution before the reader reaches Part VI. | Keep the section, but consider trimming the contact-language exposition in Ch12 and leaving the fuller prosecutorial use to Ch18. |
| `[x]` | Ch14 §14.1 and §14.3 figures | Ch14 still contains figure placeholders for the four preservation modes and six-layer calibration matrix, while Ch10-Ch12 now use rendered figures. | The architecture spine becomes visually uneven exactly where the book names the matrix. | Promoted to `working/as_figure_production_queue.md` as P0 figure tasks. |
| `[x]` | Ch8-Ch14 Devanagari first-use convention | Some high-value terms were recalled without checking whether their first use in each chapter carries Devanagari, especially in Ch9 and Ch12. | The book convention is now explicit, and architecture chapters carry many key technical terms. | Conservative pass completed 2026-05-31 for load-bearing terms across Ch8-Ch14. |

### Pass 4 — Polemic Calibration

| Status | Location | Issue | Why It Matters | Suggested Fix |
|---|---|---|---|---|
| `[ ]` | Main accusation arc: Prologue, Ch1, Ch17, Ch18, Epilogue | The antagonist vocabulary is mostly calibrated. The Prologue names the accused as the asuric pyramid, Ch1 names the two-category split, Ch17 names gaslighting/heroic erasure, Ch18 convicts PIE, and the Epilogue restores Sanskrit's category. | The main polemic now has an accusation-to-verdict structure instead of scattered anger. This should be protected during edits. | Keep this arc intact. Fix local overheat without weakening the frame: category theft, misclassification, codification, heroic erasure, gaslighting, verdict, restoration. |
| `[x]` | Appendix Part 1 §1.1-§1.3 | Appendix Part 1 opened in a hotter register than the main book: “asuric English pyramid,” church/businessmen/politicians, colonial extraction, honors-system elevation, and named Indian collaborators all arrived quickly. | The appendix is prosecutorial by design, but it needed the evidence sequence to remain structural. | Reframed the opening around Church, Company, Crown and preserved structural-not-personal framing. |
| `[x]` | Appendix Part 1 §1.3 | The Bhāṇḍārkar paragraph is careful in one way (“His Sanskrit scholarship was serious...”), but the named-person section still carried a high-charge frame. | This is where readers may confuse institutional mechanism with personal accusation. | Preserved the scholarship concession and kept function/intention distinct. |
| `[x]` | Appendix Part 1 §1.6 and draft notes | The word “cartel” appeared in reader-facing Appendix Part 1 register. | Earlier semantic rules held that “cartel” should remain rare and evidence-heavy. | Removed “cartel” from reader-facing prose and used institutional/apparatus language instead. |
| `[x]` | Appendix Part 1 §1.3 and notes | `[VERIFY: bhandarkar-cie-date]` remained in the reader-facing body and draft notes. | Verification markers are useful internally but cannot remain in a production manuscript. | Cleared reader-facing verification marker; remaining uncertainty is outside the production prose. |
| `[x]` | Ch18 Appendix forward-pointer | Ch18 forwarded to Appendix Part 1 as “institutional cartel” while Appendix Part 1 itself carried unresolved register issues. | The main verdict leans on that appendix as a companion. | Calibrated Appendix Part 1 register and removed the reader-facing cartel framing. |
| `[ ]` | Prologue | The Prologue’s “not every scholar, every institution...” guard is working. | It prevents the book from accusing whole populations while still indicting a formation. | Preserve this guard. Use it as the template for any appendix-level guard. |

### Pass 5 — Chapter Opening / Close

| Status | Location | Issue | Why It Matters | Suggested Fix |
|---|---|---|---|---|
| `[x]` | Global manuscript files | Many source chapters still open or close with draft metadata: `Draft v...`, `## Draft notes`, restoration logs, voice notes, cross-reference notes, open items. | These notes are useful internally, but they cannot appear in reader copy. | Production build already strips them; validated both full and short assembled manuscripts on 2026-05-31. |
| `[x]` | Global figures | Several chapters still contain bracketed figure placeholders, especially Ch2, Ch3, Ch9, and Ch14. Ch10-12 already have production-style rendered figures. | The visual standard is now uneven. The spine chapters look more finished than earlier and later architectural chapters. | Created `working/as_figure_production_queue.md`; prioritized Ch14 first, then Ch2/Ch3/Ch9. |
| `[x]` | Ch0 close | Ch0 source still contains extensive draft notes after the reader-facing close. | Ch0 is the reader's first chapter; production output must hand off cleanly into Ch1. | Build strips the source notes; assembled manuscript preserves the reader-facing close. |
| `[ ]` | Ch10 close | Ch10 now closes strongly: varṇamālā as sonomeric sūtra, dhātuḥ as atomic sūtra, Chapter 14 as whole-language answer, then Ch11 handoff. | This is the clearest scale-chain close in the book and should be used as a standard for the architecture spine. | Preserve the close. Only adjust if later Ch14 edits change the promised answer. |
| `[ ]` | Ch11 close | Ch11 closes cleanly into Ch12: molecule formation, operational class, then bonding chemistry. | This handoff now matches the Ch10 close and supports the atom -> molecule -> assembly spine. | Preserve. During style edits, avoid reintroducing “packet” or scratch-note language. |
| `[x]` | Ch12 opening and close | Ch12 previously opened with names, role-marked words, compounds, and sentences, but the actual procedural development focuses on names, bonds, *padāni*, *vākyāni*, and vivimorphosis. | The close is strong, but the opening promise over-included compounds. | Removed “compounds” from the promise. |
| `[ ]` | Ch13 close | Ch13 closes strongly with saturation/grammar, two redundancy layers, and drift/codification/calibration. | This is a good bridge into Ch14; it also reinforces Pāṇini as redundancy layer rather than origin. | Preserve the close. Fix the §13.1 roadmap so the chapter opening matches the current five-section structure. |
| `[x]` | Ch14 close | Ch14 source still ends in draft notes after a strong calibration-matrix close. | The reader should leave Ch14 on the matrix, not on restoration logs. | Production build strips the draft notes; figure placeholders remain tracked separately in the figure queue. |
| `[x]` | Endnotes | Endnotes previously carried `[VERIFY]` and `[TBD]` markers. | The main manuscript may look clean while the notes still reveal unfinished citation work. | Cleared 2026-05-31: reader-facing endnotes no longer carry inline `[VERIFY]` or `Short: [TBD]` placeholders. Remaining `TBD` hits are in workflow/reference planning material, not `as_endnotes.md`. |

### Pass 6 — Epilogue Loop Closure

| Status | Location | Issue | Why It Matters | Suggested Fix |
|---|---|---|---|---|
| `[x]` | Epilogue opening | The Epilogue previously opened by pointing from the Prologue to Chapter 18 without naming Ch19's remedy work. | The courtroom loop is correct, but the remedy chapter should not feel skipped in the opening recap. | Added the Ch18 / Ch19 / Epilogue bridge. |
| `[ ]` | Prologue + Epilogue | The loop now works: Prologue names category theft and the asuric pyramid; Epilogue restores Sanskrit as *saṃskṛti* and returns to pyramid vs swastika. | This is the book's strongest global closure. | Preserve the terms and sequence. Do not add new categories in the Epilogue unless they were already prepared earlier. |
| `[ ]` | Epilogue §The Contest of Architectures | Moving `यत् भूतहितम् अत्यन्तं तत् सत्यम्` into the sat/lokakṣema section works. | The standard now lands where the book names truth, welfare of beings, and the contest between architectures. | Preserve this placement. Make sure the endnote is complete and that *bhūta* as all living beings remains explicit. |
| `[ ]` | Epilogue invitation | The invitation to global relearning and *āryatva* now follows the sat/lokakṣema frame. | This prevents the invitation from sounding ethnic or triumphalist; it becomes discipline aligned with welfare. | Preserve the “Do not claim *āryatva*. Become capable of it.” close. |
| `[ ]` | Epilogue inward correction | The inward-correction section works as the India-facing counterpart to the global invitation. | It prevents the book from only prosecuting external formations and returns responsibility inward. | Keep the distinction: restore Sanskrit as calibrant inside Indian life, not as slogan, credential, or museum object. |
| `[x]` | Epilogue ending | The final reader-facing ending is strong, but source prose is followed by a long `## Draft notes` block. | The final mantra and work-close should be the last reader experience. | Production build strips the draft notes; assembled manuscript preserves the reader-facing ending. |

## Revision Queue

Items promoted here only after the relevant audit pass is complete.

| Priority | Location | Revision | Source Pass | Status |
|---|---|---|---|---|
| P0 | Global manuscript | Move/archive/strip all visible draft metadata, restoration logs, `## Draft notes`, and editorial notes from reader-facing files. | Pass 1, Pass 5, Pass 6 | `[x]` |
| P0 | Endnotes + Appendix Part 1 | Resolve or remove all `[VERIFY]` and `[TBD]` markers that appear in reader-facing material. Audit logged in `working/as_verification_todo.md` under “Production blocker audit — 2026-05-31.” | Pass 4, Pass 5 | `[x]` |
| P0 | Ch0, Ch13, Ch14, reference TOC | Fix stale cross-references and roadmaps: Ch0 “preceding chapters” and “Chapters 11-13”; Ch13 “four sections”; Ch14 “Chapters 11-13”; Reference TOC Appendix Part 4 section mismatch. | Pass 1, Pass 2 | `[x]` |
| P1 | Ch8 -> Ch9 | Revise the Ch8 close so Ch9 is framed as a subcontinental sound-field survey that lands the retroflex row, not as only the retroflex isolation chapter. | Pass 3 | `[x]` |
| P1 | Ch9 | Add one reader handhold before `C`, `V1`, `V2`, `CVC` notation, or defer shorthand until Ch10. | Pass 3 | `[x]` |
| P1 | Ch12 | Either add a compact *samāsa* treatment or remove “compounds” from the opening promise. Consider trimming §12.9 if vivimorphosis pulls too far into Ch18 territory. | Pass 3, Pass 5 | `[x]` |
| P1 | Appendix Part 1 | Calibrate the opening and named-person register; decide whether “cartel” remains; preserve structural-not-personal framing. | Pass 4 | `[x]` |
| P1 | Epilogue opening | Add one bridge that includes Ch19: Ch18 closed prosecution, Ch19 began remedy, Epilogue returns the movement to dharmic ground. | Pass 2, Pass 6 | `[x]` |
| P1 | Figures | Promote remaining bracketed figure placeholders into a figure-production queue. Prioritize Ch14 figures, then Ch2/Ch3 and Ch9. | Pass 3, Pass 5 | `[x]` |
| P2 | Ch8-Ch14 | Run Devanagari first-use convention pass after structural edits settle. | Pass 3 | `[x]` |
| P2 | Full manuscript | Run a notes-specific pass after prose lock: endnote completeness, source quality, repeated note IDs, unresolved citations. Integrity checks found no missing note stubs, duplicate endnote headings, missing short notes, `[VERIFY]`, or `[TBD]`; the ORL companion-work note still needs final publication chapter/page citation at production lock. | Pass 5 | `[~]` |
