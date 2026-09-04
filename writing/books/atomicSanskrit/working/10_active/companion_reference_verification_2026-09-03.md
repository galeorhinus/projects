# Source and Reference Companion Verification — 2026-09-03

## Scope

The manuscript endnote ledger does not audit the four companion-only files assembled before the expanded endnotes. This pass reviewed all four:

- `companion/as_reference_front.md`
- `companion/as_reference_00_where_this_argument_stands.md`
- `companion/as_reference_06_by_the_numbers_full.md`
- `companion/as_reference_08_let_coordinate_test.md`

The sources used for the positioning chapter have been registered and, where possible, archived with checksums. The numerical analyses behind Reference Appendix 6 were reproduced in endnote-verification Batch 037. The Vedic forms, grammatical rules, and figure data behind Reference Appendix 8 were verified in Batches 025 and 038.

The author approved these changes on 2026-09-04. They have now been applied to the companion sources and reference build.

## Companion Preface

### 1. Replace the stale account of the printed endnotes

**Current**

> The printed book contains one-sentence endnotes — citation anchors, named references, the one sentence the printed-book reader needs at the point of citation. The companion preserves the full long-form: technical appendices, complete bibliographic citations, primary-source quotes, verification trails, source-history discussions, structural-significance analysis. The two volumes share a single source. The printed book's endnote at *"See expanded endnote for X"* points here.

**Why it needs revision**

Many short endnotes contain more than one sentence, and the printed book does not use the quoted instruction “See expanded endnote for X.” The shared element is the keyed endnote source, not every page in both volumes.

**Proposed**

> The printed book contains condensed endnotes that identify the source and state the point needed at that citation. This companion carries the expanded entries: complete citations, primary-source passages, verification trails, source histories, and longer technical discussions. Both versions of an endnote come from the same source and use the same stub-name, so a reader can move from the printed note to its full companion entry.

### 2. Narrow the completeness claim

**Current**

> Every claim, every citation, every primary source.

**Proposed**

> It gathers the sources, calculations, and verification records behind the book's principal checkable claims.

This remains strong without promising that every sentence in the book has a separate source record.

## Where This Argument Stands

### 3. Attribute the root-family comparison only to the source that makes it

**Current**

> Both writers have also noticed an important asymmetry: Sanskrit retains active *dhātavaḥ* and generative families where European languages often preserve isolated related words.

**Finding**

The checked Talageri essay makes this comparison directly. The checked Elst essay supports his place in the Out-of-India discussion but does not make this *dhātuḥ* comparison.

**Proposed**

> Talageri also notices an important asymmetry: Sanskrit retains active *dhātavaḥ* and generative families where European languages often preserve isolated related words.

### 4. State Kazanas's position more precisely

**Current**

> He argues that the common source cannot be reconstructed as PIE and places Vedic Sanskrit much closer to that source than mainstream comparative philology permits.

**Finding**

Kazanas argues that prevailing PIE reconstructions should be scrapped and rebuilt. He treats Vedic Sanskrit as closer to the proposed source than other branches, but explicitly says that he does not regard Vedic Sanskrit as the Indo-European mother tongue.

**Proposed**

> He argues that prevailing PIE reconstructions should be discarded and rebuilt, and he places Vedic Sanskrit much closer to the proposed source than mainstream comparative philology permits. He explicitly stops short of calling Vedic Sanskrit the Indo-European mother tongue.

### 5. Complete the sources list

The chapter discusses Trubetzkoy and Brady but does not list their works. Add:

- N. S. Trubetzkoy, “Gedanken über das Indogermanenproblem,” *Acta Linguistica* 1 (1939): 81-89; English translation, “Thoughts on the Indo-European Problem,” in *N. S. Trubetzkoy: Studies in General Linguistics and Language Structure* (Duke University Press, 2001), pp. 87-98.
- Angela Marcantonio and R. M. Brady, “Evidence that Indo-European Reconstructions Are Artefacts of the Linguistic Method of Analysis” (2003), developed in Marcantonio's 2009 edited volume.

### 6. Scope the originality statement to the survey

**Current**

> The research did not locate another book that joins engineered sound, atomic *dhātavaḥ*, two-domain scope, the Vedas as calibrant, distributed aural preservation, expert-carried radiance, and architectural asymmetry into one account of how PIE reversed source and reflection.

**Proposed**

> Among the neighboring works surveyed here, none joins engineered sound, atomic *dhātavaḥ*, two-domain scope, the Vedas as calibrant, distributed aural preservation, expert-carried radiance, and architectural asymmetry into one account of how PIE reversed source and reflection.

This preserves the positioning claim while stating the field within which it was tested.

## Reference Appendix 6 — The Architecture by the Numbers

### 7. Remove editorial scaffolding from the published companion

The source begins with file-management instructions and a dated “Draft v3” record, then ends with approximately sixty lines of draft notes. The reference builder currently includes all of it because `cmd_reference()` does not apply the existing `DRAFT_NOTES_RE` filter to companion-only files.

**Proposed published opening**

> # Reference Appendix 6 — The Architecture by the Numbers
>
> Chapters 10 and 11 present the architectural argument. This appendix supplies the calculations, full tables, tests, and reproduction instructions behind it.

Keep the draft history in the Markdown source if it remains useful, but make the reference build strip the `## Draft notes` block. Correct the three opening section spans from `§§6.2–5.6`, `§§6.7–5.10`, and `§§6.11–5.12` to `§§6.2–6.6`, `§§6.7–6.10`, and `§§6.11–6.12`.

### 8. Correct the stale *juhotyādi* row

**Current**

> 22.7% | 0.0% | 22.7% | 33.3% | 22.7%

**Reproduced row**

> 23.8% | 0.0% | 23.8% | 33.3% | 19.0%

The 33.3% C4 headline remains correct; the other percentages came from an older denominator.

### 9. Replace target-implying verbs with the observed comparison

**Current**

> The *Dhātupāṭha* over-allocates voiced aspirates to *juhotyādi*; the corpus over-deploys them further.

**Proposed**

> The *Dhātupāṭha* shows a higher C4 share in *juhotyādi* than in the other classes. The corpus-visible subset raises that share from 33.3% to 42.9%.

“Over-allocates” and “over-deploys” assume a correct target that the calculation does not establish.

### 10. Mark the acoustic explanation as the book's inference

**Current heading**

> Why the *juhotyādi* C4 enrichment makes engineering sense

**Proposed heading and opening**

> A Possible Architectural Explanation
>
> This book proposes that reduplication benefits from an acoustically distinctive initial consonant.

The data establishes enrichment. It does not by itself establish why the enrichment occurs.

### 11. Correct the description of the 3,839 Path C records

**Current**

> 3,839 unique bare dhātavaḥ.

**Proposed**

> 3,839 normalized verb lemmas, including corpus-derived forms as well as listed *Dhātupāṭha* atoms.

The appendix itself identifies *vartay* as a derived causative lemma, so “bare dhātavaḥ” is not accurate.

### 12. Describe the Path A / Path C relation at its demonstrated strength

**Current**

> ρ = +0.6647 between Path A and Path C means the two instruments agree strongly.

**Proposed**

> ρ = +0.6647 shows substantial positive agreement between the hand-curated Path A estimates and corpus-derived Path C valency.

Path A is an approximate 138-entry sample, so “substantial positive agreement” states what the calculation demonstrates.

### 13. Replace “generates” in the token-share sentence

**Current**

> The polyvalent tier — 3.8% of the inventory — generates 67.6% of all corpus-attested verb tokens.

**Proposed**

> The polyvalent tier — 3.8% of the inventory — accounts for 67.6% of the recorded verb-token uses.

The calculation counts recorded uses; it does not count every word each atom can generate.

### 14. Replace “invariant core” with the measured recurrence

**Current**

> The carbon-class core is invariant across the design-purpose split. The Ṛgveda's top-20 includes ritual-specific atoms ...; the reference core remains visible at high valency in every sub-corpus regardless.

**Proposed**

> All nine reference atoms recur in each of the four checked corpora, although their ranks change with the work each corpus performs. Six of the nine enter the Ṛgveda's top twenty; the others remain present below that threshold.

This states the reproduced result without treating four corpora or changing ranks as proof of invariance.

### 15. Name the two scales actually tested

**Current**

> The compression principle recurs at every measurement scale tested — curated 138-dhātu MW sample, full 3,839-dhātu corpus, both directions.

**Proposed**

> The inverse relation recurs in both calculations: the curated 138-*dhātuḥ* Path A sample and the 3,839-lemma Path C corpus audit.

### 16. Remove the unsupported paradigm-regularity conclusion

**Current**

> In Sanskrit's engineered case, the correlation runs the opposite way: the *dhātavaḥ* with the greatest generative reach are *also* the most structurally minimal *and* paradigmatically regular. There is no idiosyncrasy at the top.

**Proposed**

> The Sanskrit audit tests a different relation. In both Path A and Path C, smaller atoms tend to have wider recorded reach. These calculations do not test paradigm regularity.

Remove “paradigmatically regular” from synthesis item 8 for the same reason.

### 17. Mark the *juhotyādi* functional explanation as an interpretation

**Current**

> The *juhotyādi* reduplicating class enriches C4 ... because reduplication needs acoustic robustness.

**Proposed**

> The *juhotyādi* reduplicating class enriches C4 ... . This book proposes that the pattern may reflect the value of an acoustically distinctive consonant during reduplication.

### 18. Do not call Paths A and C independent

**Current**

> The three paths cross-check the engineering thesis at three independent layers.

**Proposed**

> The three paths would test the engineering thesis against three different records.

Path A and Path C examine the same language and partially overlapping lexical material; they are different measurements, not fully independent evidence.

## Reference Appendix 8 — The *Leṭ* Coordinate Test

### 19. Add the omitted mantra to the sources

The chapter's principal collision example is Ṛgveda 6.16.16, but the source list names only Ṛgveda 10.186.1.

**Proposed source line**

> - Ṛgveda 6.16.16 and 10.186.1.

### 20. Add the imperative-table locator

Whitney §562 supports the subjunctive endings. The *loṭ* comparison also uses his imperative table.

**Proposed replacement**

> - William Dwight Whitney, *Sanskrit Grammar*, §553d for the imperative endings and §562 for the active and middle subjunctive endings. The tables were checked against the Pāṇinian operations above rather than used as the governing analysis.

## Verification Result

- Appendix Part 9's three live manuscript endnotes are verified and recorded in Batch 039.
- Every live manuscript endnote now has a reviewed result in the batch ledger.
- The companion-only audit found no reason to alter the core purpose or argument of either technical chapter.
- Reference Appendix 6 has been synchronized with its reproduced data.
- Reference Appendix 8 now includes both missing source locators.
- “Where This Argument Stands” now carries the corrected attributions and completed source list.
- The companion preface now describes the current endnote build.
- Appendix 6's draft history remains in its source file but is excluded from the published reference build.
- The source registry passes with 645 endnote source links and 392 registered sources.
- The endnote ledger passes with 341 live entries, no missing entries, no duplicates, and no structural failures.
- The A4 reference companion builds successfully at 224 pages. A publication scan found no draft-history text, stale Appendix 6 claims, or raw note markers in the assembled output.
