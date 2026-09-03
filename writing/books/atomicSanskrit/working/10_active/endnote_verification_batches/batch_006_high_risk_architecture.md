# Endnote Verification Batch 006 — High-Risk Architectural Claims

**Audit date:** 2026-09-02  
**Scope:** Ten unreviewed notes carrying claims about Sanskrit morphology, PIE reference practice and curricula, māyā, generativity, the grammatical tradition, and *apauruṣeyatva*.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `samskrtam-morphology` | P1 | Corrected | Reclassified संस्कृत as a prefixed verbal derivative rather than a *karmadhāraya* compound; restored the **स्** operation represented by Aṣṭādhyāyī 6.1.137; removed the unsupported claim that ⟪कृ⟫ excludes assembly; identified the book's English renderings as interpretations. |
| `pre-pie-dictionary-shift` | P1 | Narrowed | Replaced the universal six-stage dictionary history with the primary sequence actually demonstrated by Chambers, Müller, and two Skeat editions. Removed the unsupported claim that 1990s desk dictionaries generally stopped at Sanskrit. |
| `pie-cementing-recent-decades` | P0 | Narrowed | Verified the reference-work publication sequence and Etymonline's 2001 origin. Separated those dates from the book's inference about timing, coordination, and dharmic re-emergence. |
| `pie-indian-university-curricula` | P1 | Strengthened | Verified the national module and official materials from seven universities. Archived six official PDFs and one university page; recorded the two official pages that could be inspected but not retained. |
| `rigveda-1-11-7-maya-mayin` | P1 | Strengthened | Confirmed that Indra defeats the मायिन् Śuṣṇa through his own मायाः. Distinguished the mantra from the later expressions दैवी माया and आसुरी माया and marked moral neutrality as the book's inference. |
| `maya-concealment-projection` | P1 | Strengthened | Located the two powers and both analogies precisely at *Vedāntasāra* §§51–54. Marked their application to Svarbhānu, PIE, and gaslighting as the book's later analogy. |
| `sanskrit-generative-wordspace` | P0 | Corrected | Reproduced the arithmetic but found that 20,942,880 counts formal grid slots, not valid or distinct words. Added a reproducible calculation and stated the combinatorial restrictions the old note ignored. |
| `dhatu-pre-panini-vedic` | P1 | Corrected | Confirmed technical grammatical use in the *Nirukta*, *Ṛgveda-Prātiśākhya*, and Aṣṭādhyāyī 1.3.1. Removed uncertain chronology, anachronistic metallurgical material, and the claim that the word itself proves an engineering category. |
| `panini-cites-pre-paninian-vaiyakaranas` | P1 | Corrected | Checked the named sūtras and removed incorrect descriptions of several rules. The evidence establishes earlier attributed positions, not one teacher-student chain or a separate institution for every name. |
| `apauruseya-mimamsa-sutra-1-1-5` | P0 | Corrected | Restricted the sūtra to the originary word-meaning relation and independent Vedic testimony. Removed the unsupported cosmic-Puruṣa argument, corrected the chronology of the Nyāya counter-position, and separated doctrine from the book's engineering thesis. |

## Manuscript Corrections Requiring Author Approval

No body prose was changed during this batch. Four corrections should be reviewed before the note and body are considered fully aligned.

### 1. Chapter 0 §0.5

**Current:** “A conservative count of the forms available before compounding already exceeds **twenty million words**.”

**Proposed:** “An intentionally overcomplete grid of verbal and nominal combinations contains more than **twenty million formal slots** before compounding. Not every slot produces a valid or distinct word; the calculation demonstrates the scale of the architecture rather than the size of a dictionary.”

### 2. Chapter 12 §12.7

**Current:** “Even before compounding begins, that first pass produces more than **twenty million possible formations**.”

**Proposed:** “Before compounding begins, that deliberately overcomplete grid contains more than **twenty million formal slots**. Sanskrit does not fill every slot, but the grid shows how quickly finite reusable operations create generative reach.”

### 3. Chapter 5 §5.1

**Current:** “Their names preserve evidence of established schools, competing positions, and sustained grammatical analysis.”

**Proposed:** “Their names preserve evidence of earlier authorities, alternative positions, and sustained grammatical analysis.”

### 4. Chapter 19 §19.4

**Current:** “Dictionaries that gave proximate etymologies — Latin, Greek, Sanskrit — to ordinary readers in the 1990s give PIE-anchored etymologies routinely now.”

**Proposed:** “Older public-facing references often ended the visible chain with recorded Latin, Greek, or Sanskrit forms. Contemporary online references routinely extend those chains into reconstructed PIE.”

Chapter 1's “As if by coordination” and Chapters 4 and 19's interpretation of the timing remain identifiable rhetorical or structural inferences. The sources verify the publication sequence, not coordination or motive.

## Digital Evidence Records

New records and retained source files are catalogued in [the digital source registry](../../40_reference/sources/as_source_registry.md) under:

- `american-heritage-ie-roots-guide`
- `etymonline-about`
- `pie-reference-ecosystem-metadata`
- `indian-university-pie-curricula`
- `ashtadhyayi-named-authorities`
- `gita-supersite-7-14`
- `vedantasara-two-powers`
- `project-generative-wordspace-calculation`
- `mimamsa-sutra-sandal-1923`
- `sep-kumarila`

The audit also reuses the registered Rigvedic, Monier-Williams, *Nirukta*, *Ṛgveda-Prātiśākhya*, historical-linguistics, and dictionary records from earlier batches.

## Apparatus Cleanup

The separate structural pass supplied a `Deployments` field to all 39 entries that lacked one. Live entries now identify their manuscript locations. Unused entries explicitly say that they are parked. No body prose changed during that cleanup.

## Required Completion Tests

1. Regenerate and check the master ledger.
2. Confirm zero missing `Deployments` fields.
3. Run the source-registry validator.
4. Run full and short manuscript assembly.
5. Run `git diff --check`.
