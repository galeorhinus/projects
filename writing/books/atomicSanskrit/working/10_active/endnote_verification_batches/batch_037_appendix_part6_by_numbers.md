# Endnote Verification Batch 037 — Appendix Part 6

**Audit date:** 2026-09-03  
**Scope:** All nine previously unreviewed endnotes in Appendix Part 6, *The Architecture by the Numbers*. The project calculations were rerun against the checked-in datasets. No appendix prose was changed.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `dcs-vs-dhatupatha-count` | P0 | Reproduced | Fresh runs confirmed 2,168 listed entries, 138 Path A atoms, and 3,839 normalized Path C verb lemmas. The note now points to the two project records that keep those denominators separate. |
| `cross-gana-column-distribution` | P0 | Narrowed | The 33.3% inventory and 42.9% corpus-visible C4 shares reproduce. The note now separates the observed enrichment from the book's proposed acoustic explanation. |
| `generative-reach-inversion-natural-language` | P1 | Strengthened | The two Sanskrit correlations reproduce at −0.485 and −0.4334. A direct empirical source now supports the English frequency-irregularity comparison, while the note explicitly declines to claim a completed cross-language paradigm audit. |
| `dictionary-audit-sources` | P0 | Qualified | The exact dictionary editions are Monier-Williams 1899 and Apte 1890. Path A is a hand-curated approximate sample, and the checked-in data does not preserve a headword-by-headword extraction ledger. The note now states that boundary. |
| `prayoga-audit-valency` | P0 | Reproduced | The DCS commit, file count, token count, lemma count, valency maximum, tier shares, and +0.6647 matched-sample correlation reproduce from the stored scripts and data. |
| `cross-corpus-invariance` | P0 | Narrowed | All nine reference atoms occur in all four checked corpora, but only six enter each Vedic top twenty. The note now claims recurrence across the corpora rather than invariant rank or use. |
| `racana-gana-matrix` | P1 | Reproduced | Fresh output confirmed 47 observed *racanāḥ*, 1,973 of 2,168 entries in the top ten, 91.01% coverage, and 140 populated cells. |
| `varga-column-as-engineering-axis` | P1 | Reproduced | The column-axis analysis and reported heterogeneity value reproduce. The note remains an explicitly architectural interpretation of project data. |
| `inherent-vowel-secondary-axis` | P1 | Corrected | The reported grouping and heterogeneity values reproduce. “Open-vowel core” was removed because ऋ (*ṛ*) is not phonetically an open vowel. |

## Companion Findings

The manuscript appendix already uses the narrower claims. The longer companion chapter predates that narrowing and contains several statements that require revision. These are recorded in the separate companion audit and were not changed in this batch.

## Digital Evidence Records

The DCS corpus snapshot, both project-analysis bundles, the dictionary interfaces, and the English irregular-verb study are registered in `working/40_reference/sources/as_source_registry.md`. Local project records include SHA-256 values for the principal inputs and outputs.

## Completion Tests

- All nine live Appendix Part 6 markers now have reviewed endnotes.
- All principal numerical results were reproduced from the checked-in scripts.
- The approximate Path A counts are identified as approximate.
- Observed numerical patterns and the book's architectural explanations remain distinct.
- No Appendix Part 6 prose change was applied.
