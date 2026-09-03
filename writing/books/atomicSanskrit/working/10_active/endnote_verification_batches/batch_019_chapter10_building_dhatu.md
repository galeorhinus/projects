# Endnote Verification Batch 019 — Chapter 10

**Audit date:** 2026-09-02  
**Scope:** All seventeen live Chapter 10 endnotes. Endnotes and source records were corrected where necessary. The Chapter 10 manuscript was not edited.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `sutra-laksana-six-criteria` | P0 | Verified | The six-part verse and the Vāyu Purāṇa 59.117 / Tagare p. 429 locator agree with the cited printed anchor. |
| `rasashastra-chemistry-anticipation` | P0 | Corrected | Removed the unsupported claim that the classifications anticipate the periodic table. The note now supports only the constituent sense of *dhātu* used in the chapter. |
| `saptadhatu-standard` | P1 | Narrowed | Retains the standard seven bodily constituents. Removed the unused one-month cascade and modern biochemical analogy. |
| `dhatupatha-count-and-ganas` | P0 | Corrected | Separates edition-dependent *Dhātupāṭha* counts from this book's dataset: 2,235 instructional rows and 2,168 analyzed pronounced forms after the stated processing. |
| `dhatu-cross-linguistic-analogues` | P1 | Qualified | Semitic consonantal bases and Tamil verbal bases are valid comparisons. Their contrast with the Sanskrit atom is identified as the chapter's architectural analysis. |
| `panini-adi-naming-convention` | P2 | Verified | The book explicitly adapts the ordinary Sanskrit *-ādi* class-naming convention rather than attributing its scaffold names to Pāṇini. |
| `dhatupatha-empirical-distribution` | P0 | Reproduced | The local scripts regenerate 2,168 analyzed forms, forty-seven scaffolds, and the 91.0% top-ten result. |
| `zipf-rank-frequency` | P1 | Verified | Zipf is used only as a contrast between usage frequency and inventory structure. |
| `vaicitrya-racana-tail` | P1 | Reproduced | The derived table confirms 195 entries across the thirty-seven scaffolds outside the top ten. |
| `scaffold-distinguishability-by-matra` | P0 | Reproduced | The result and cited output files agree with the current 2,168-form dataset. |
| `varnavada-presupposes-engineering` | P0 | Verified | Kielhorn I.30–32 records the arguments over whether individual *varṇāḥ* carry meaning. The architectural conclusion remains identified as this book's inference. |
| `paspashahnika-brihaspati-indra-word-list` | P0 | Reconfirmed | The Patañjali passage and Bṛhaspati-Indra teaching story were verified in the pilot batch. |
| `scaffold-deployment-join` | P0 | Reproduced | The join script regenerates 91.0%, 89.0%, 92.5%, and 93.6% for the four reported top-ten scaffold measures. |
| `yaska-agni-nirukta-7-14` | P0 | Strengthened | Removed the unfinished verification instruction. GRETIL and Sarup support the analyses involving leading, the body, non-moistening, motion, shining or burning, and leading. |
| `yoga-sutra-1-2` | P1 | Verified | The Sanskrit text, separation, and limited use as an example of compact *sūtra* form are sound. |
| `nyaya-sutra-pramana-1-1-3` | P1 | Verified | The four *pramāṇāni* and the quoted Sanskrit agree with Nyāya Sūtra 1.1.3. |
| `om-vocal-tract-macro-gesture` | P0 | Reconfirmed | The Upaniṣadic and Yoga Sūtra passages were verified in Batch 016. The vocal-tract interpretation remains the book's stated synthesis. |

## Manuscript Review

No Chapter 10 prose was changed. The pre-audit and post-audit SHA-1 is:

`2f19ae44e77ab7f24de654767d5350aa9955a7ea`

No body correction is proposed from this batch.

## Reproducibility Checks

- `analysis/dhatupatha/scripts/analyze_shells.py` regenerated 2,168 forms, forty-seven scaffolds, and the top-ten 91.0% result.
- `analysis/ganah/scripts/summarize_scaffold_reactivity.py` regenerated the four scaffold-deployment shares.
- The existing GRETIL Yāska source record now includes *Nirukta* 7.14.

## Completion Tests

- No Chapter 10 manuscript prose was changed during this audit.
- Endnote-source registry and master-ledger checks remain to be run after the Chapter 8–12 sequence is complete.

