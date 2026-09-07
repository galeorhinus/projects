# Appendices Post-Reduction Continuity Audit — Codex

**Scope:** Appendix Parts 1–10
**Status:** Completed 2026-09-06
**Purpose:** Check the reduced appendices for broken transitions, stale cross-references, inaccurate headings, and missing conclusions. This pass does not seek further cuts.

## Audit Rules

1. Preserve the argument, evidence, examples, and earned hammers retained by the reduction pass.
2. Change manuscript prose only when the reduced appendix contains a demonstrable factual or navigational defect.
3. Synchronize the canonical tables of contents with the headings that actually appear in the manuscript.
4. Record every manuscript correction below before applying it.
5. Defer any second reduction of B-ranked arguments until the post-reduction baseline has been reviewed.

## Continuity Results

| Appendix | Opening and internal sequence | Conclusion | Result |
|---|---|---|---|
| Part 1 | Moves from the colonial conversion mandate and institutional pipeline to seven atom families, operators, and the post-independence continuation. | Hands the institutional argument directly to Part 2. | Coherent. |
| Part 2 | Moves from the inherited institutional method to its five-category error, then proposes reclassification and curricular action. | Returns to the named institutions and the Sarasvatī invocation. | Coherent after two stale chapter references are repaired. |
| Part 3 | Establishes sonomer before audiograph, tests the Aramaic claim, and ends with a research program. | Keeps the history of visible marks open while asserting that the encoded architecture is Indic. | Coherent. |
| Part 4 | Explains the atlas method before presenting seven additional surveys and the complete coverage cascade. | Ends by inviting replication of the geographic test. | Coherent. |
| Part 5 | Defines the language factory, performs the Yenpro construction, and states what the experiment does and does not demonstrate. | Returns to Schleicher after the construction has supplied the comparison. | Coherent. |
| Part 6 | Separates the three datasets, presents eight engineering principles, and tests reach through two independent paths. | Points readers to the companion data and replication instructions. | Coherent. |
| Part 7 | Supplies the Vedic evidence behind Chapters 11 and 12 through concordances and four complete mantra analyses. | Establishes that the grammar preceded Pāṇini's manual and points to Parts 8 and 9. | Coherent after the inaccurate §7.5 heading is corrected. |
| Part 8 | Moves from the PASS method through representative cases, the complete 83-card record, and documented stewardship. | Ends with communities that carried both Vedic preservation and laukika composition. | Coherent. |
| Part 9 | Converts the codification story into predictions and a corpus-wide test. | Restates Pāṇini's achievement as decoding and documentation rather than imposed order. | Coherent. |
| Part 10 | Defines the book's vocabulary by conceptual function and gives book-coined terms their own index. | Closes with stable usage conventions rather than repeating the argument. | Coherent. |

## Corrections

### C1 — Appendix Part 2, §2.1

**Before:** `codification (Chapter 1 §1.1)`
**After:** `codification (Chapter 1 §1.3)`

**Reason:** Chapter 1 §1.1 now defines the apex-one. The discussion of Pāṇini as the supposed codifier appears in §1.3.

### C2 — Appendix Part 2, §2.10

**Before:** `Chapter 5 §5.6 introduced the word`
**After:** `Chapter 6 §6.7 introduced the word`

**Reason:** The जड (*jaḍa*) example moved from the earlier Chapter 5 structure to the current discussion of orbit, drift, and divergence in Chapter 6 §6.7.

### C3 — Appendix Part 7, §7.5

**Before:** `Six धातुः (*Dhātuḥ*) Groups Across Three Passages`
**After:** `Six धातुः (*Dhātuḥ*) Groups Across Two Mantras`

**Reason:** The six rows in the retained table come from Ṛgveda 1.1.1 and 3.62.10. The heading retained the count from an earlier version of the section.

### C4 — Canonical Tables of Contents

Synchronize the Appendix Part 2, 4, 7, and 8 entries in `reference/as_toc.md` and `reference/as_toc_annotated.md` with the current manuscript headings. Update the Part 4 annotation from the broad label `Munda 20/23` to the actual Santali-inclusive forest-belt survey.

### C5 — ORL Voice Reference

**Before:** `§1 A Choice, Not an Inheritance`
**After:** `§2.2 The Choice of 1948`

**Reason:** The reference points to Appendix Part 2 but retained both an old section number and an old heading.

### C6 — Appendix Part 2 Reduction Record

Correct the completed reduction record so it says that §2.7 remains in shorter form. The earlier proposal had suggested absorbing it into §2.8, but the executed appendix retained both sections.

## Reduction Decision

The low-risk C/D reduction is complete. This continuity pass found no missing argument or lost hammer that requires restoration. A second reduction round would have to enter B-ranked material and should wait until the present baseline has been read as a whole.

## Validation

- Appendix Parts 1–10 now contain 33,373 words by `wc -w`, down from 40,417 before reduction: a reduction of 7,044 words.
- The Appendix Part 8 validator confirmed 107 source subrows, 83 catalogue records, and 83 rendered data cards.
- `python3 build_book.py stubs` created no missing endnotes.
- The complete B5 short-endnotes build succeeded with 338 endnotes and 156,526 assembled words.
- The build retained the existing warning that Chapter 8 Figure 8.5 exceeds its page by 7.7 points. That figure is outside this appendix continuity pass.
