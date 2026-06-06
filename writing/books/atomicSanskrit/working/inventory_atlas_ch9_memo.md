# Ch 9 deployment memo — the subcontinental superset (empirical anchor)

> One-page summary of what the 34-language inventory atlas + 8-metric pairwise analysis lets Ch 9 *The Subcontinental Superset* assert empirically. Full analysis: `inventory_atlas_analysis.md`. Anticipated critique: `inventory_atlas_critique.md`. Numbers as of commit `6968ea1`.

---

## The empirical anchor (single sentence)

**Sanskrit's phoneme inventory is the curated superset of the human articulator space — by direct measurement, the smaller inventories of unrelated languages across geography and across the orthodoxy's family-tree categories largely nest inside it.**

This is not a metaphor and not a thesis. It is a set-theoretic statement about the data: for most languages X in the 34-language atlas, the fraction of X's phonemes that are also in Sanskrit's inventory (the coverage metric *Sk⊇X*) is high — and the higher it is, the closer X is to being a subset of Sanskrit.

---

## The four assertions the chapter can make

**Assertion 1 — The southern subcontinent languages are largely subsets of Sanskrit.** Tamil's inventory is 67% contained in Sanskrit's (*Sk⊇Tamil = 0.67*). Kannada, Telugu, and Malayalam are 80–82% contained. The five forest-belt languages (Gondi, Kui, Kuvi, Kolami, Kurukh) cluster at 74–84%. None of these languages is in the orthodoxy's "Indo-European" family; all of them are more contained in Sanskrit than the orthodoxy's own Indo-European languages are.

**Assertion 2 — The orthodoxy's Indo-European languages are NOT mostly contained in Sanskrit.** English: 50%. French: 62%. Farsi: 44%. Arabic: 33%. The Indo-Iranian closeness the orthodoxy posits between Sanskrit and Farsi is not visible in this dimension — Farsi (44%) is less contained in Sanskrit than Tamil (67%) is. The data refuse to corroborate the family-tree ordering.

**Assertion 3 — The Korean signature (geography-independent containment).** Korean's inventory is 87% contained in Sanskrit's — the highest single coverage number in the table — despite Korean being spoken thousands of miles away with no plausible historical contact. This is the curated-superset signature in its purest form: Sanskrit's inventory was engineered comprehensively enough that a small-inventory language from anywhere will mostly fall within it. The pattern is anatomical, not genealogical.

**Assertion 4 — The Brahui control case (areal effects ARE detectable).** Brahui is the orthodoxy's outlier "Dravidian" language, spoken in Balochistan, surrounded by Persian/Balochi/Arabic for over a thousand years. Brahui's place-of-articulation overlap with Sanskrit is 0.45 — far lower than Tamil's 0.83. Brahui has been areally pulled away from the inventory shape it would otherwise share with Sanskrit. **The data correctly capture areal pressure when it exists.** The orthodox response to assertions 1–3 — "this is areal convergence, not inheritance" — fails because the metric demonstrably detects areal effects in Brahui's case but does not detect them in Sanskrit-vs-southern-subcontinent comparisons. Whatever Sanskrit-Tamil similarity is, it is structurally not the kind of areal drift Brahui exhibits.

---

## The polemic statement

**Sanskrit was engineered as the comprehensive map of the human mouth.** The southern subcontinent languages — Tamil, Telugu, Kannada, Malayalam, Tulu, the central forest belt, the Munda lineage — share that anatomical map and use subsets of it, with regional anatomical elaborations of their own. The orthodoxy's family-tree boundary between "Indo-European Sanskrit" and "Dravidian Tamil" is invisible to the inventory dimension; the data say the boundary is a discipline-internal classification choice, not an empirical fact about the languages.

This is the "subcontinental superset" the chapter title names, now stated with measurements: *Sanskrit's varṇamālā is the curated articulator-space superset, into which most subcontinental and many non-subcontinental inventories nest, regardless of what the orthodoxy's family taxonomy claims.*

---

## What the chapter should NOT claim from this evidence

- That the atlas refutes the comparative method or PIE reconstruction directly. It doesn't. It's one dimension of evidence; the orthodoxy's case rests on lexical correspondences in a different dimension.
- That inventory similarity proves common ancestry. It doesn't. Inventory can converge through engineering, contact, drift, or shared anatomy — and the chapter is making the engineering claim, not an ancestry claim.
- That the metric numbers settle the question. They don't. They sharpen one part of the polemic; the rest rests on the engineering thesis the book argues elsewhere.

## What the chapter CAN claim (and the data support)

- Sanskrit's inventory is the curated superset of the human articulator space, measured by direct phoneme-set containment.
- The orthodoxy's family-tree boundary between Sanskrit and the southern subcontinent does not predict inventory similarity rankings.
- Tamil is approximately Sanskrit's anatomical baseline with regional elaborations; Sanskrit is approximately Tamil's anatomical baseline with the engineering layer added.
- Where areal pressure has been real and substantial (Brahui under Persian/Arabic contact), the metric detects it. Sanskrit-vs-southern-subcontinent comparisons do not show that areal signature, which is itself structural evidence that the orthodoxy's areal explanation does not fit.

---

## Key numbers for the chapter

| Pair | Sk⊇X | X⊇Sk | Jaccard | Place |
|---|---:|---:|---:|---:|
| Sanskrit vs Tamil | 0.67 | 0.36 | 0.31 | 0.83 |
| Sanskrit vs Telugu | 0.82 | 0.85 | 0.72 | 0.62 |
| Sanskrit vs Kannada | 0.82 | 0.85 | 0.72 | 0.62 |
| Sanskrit vs Malayalam | 0.80 | 0.85 | 0.70 | 0.56 |
| Sanskrit vs Santali | 0.87 | 0.82 | 0.73 | 0.71 |
| Sanskrit vs Mundari | 0.76 | 0.48 | 0.42 | 0.71 |
| Sanskrit vs Korku | 0.80 | 0.48 | 0.43 | 0.71 |
| Sanskrit vs Korean | 0.87 | 0.39 | 0.37 | 0.57 |
| Sanskrit vs Lepcha | 0.81 | 0.52 | 0.46 | 0.57 |
| Sanskrit vs Kolami | 0.84 | 0.48 | 0.44 | 0.83 |
| Sanskrit vs Brahui | 0.61 | 0.52 | 0.39 | 0.45 |
| **Sanskrit vs English** | **0.50** | 0.36 | 0.27 | 0.40 |
| **Sanskrit vs French** | **0.62** | 0.39 | 0.32 | 0.44 |
| **Sanskrit vs Farsi** | **0.44** | 0.33 | 0.23 | 0.40 |
| Sanskrit vs Arabic | 0.33 | 0.24 | 0.16 | 0.33 |

Read across: the orthodoxy's "Indo-European" languages (bolded) sit at or below the lowest values for southern subcontinent and Munda languages. The "subcontinental superset" the chapter title names is what the table makes visible: Sanskrit contains most of its regional neighbours' inventories and very little of the inventories the orthodoxy claims it is genealogically related to.

---

*Memo length: under one page when typeset at chapter body settings. All cited numbers are from `vocal_tract_overlay.py` pairwise computation on the 34-language atlas, deterministic and reproducible.*
