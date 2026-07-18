# Varṇa-Grid Distinguishability Findings — Ch 11 Source Material

> **Status:** dropped from Ch 10 §10.9 (2026-05-23). These findings operate at the *varṇa*-grid level (consonant-column × consonant-row × cell allocation) rather than at the *racanā*/*mātrā* level that Ch 10 now uses for its distinguishability case. They belong with Ch 11's periodic-table-of-*dhātavaḥ* work (`working/80_completed/plans/as_1_11_building_kriya_workplan.md`).
>
> The text below is the verbatim paragraphs as they stood in Ch 10. Empirical numbers (9.2%, 10.8%, 13.3%, etc.) come from the older varṇa-only analysis pipeline (not the V1/V2-aware template pipeline). Verify the underlying CSVs before redeploying.

---

## 1. C2 / C4 inversion — voiced-aspirate over voiceless-aspirate

> The C2 / C4 inversion is the clean test. C2 (unvoiced aspirated stops) deploys at 9.2% of *varga* consonants in primary-class *dhātavaḥ*. C4 (voiced aspirated stops) deploys at 10.8%. The *most expensive* column is *more deployed* than a column one step cheaper. The engineering does not minimize cost. It optimizes cost against acoustic return. Voiceless aspirates cost breath but yield only a modest acoustic gain. Voiced aspirates cost more but produce a much more distinctive *mahāprāṇa-ghoṣavat* signature. C4 buys difference; C2 does not.

**Why useful for Ch 11:** the column-axis polemic ("structure determines behavior, not meaning") wants empirical proofs that the orthodoxy's articulatory-cost framework fails to predict deployment. C2 < C4 is the cleanest such proof.

---

## 2. Cell-level allocation — row × column variance at "identical column cost"

> Cell-level allocation confirms distinguishability at the row × column level. *K* (velar C1) at 13.3% of all *varga* consonants; *m* (labial C5) at 8.8%; *d* (dental C3) at 7.4%; *p* (labial C1) at 6.8%. Some cells are essentially empty: ***ch* (palatal C2) at 0.0%** — completely absent from the primary class; *ḍh* (retroflex C4) at 0.1%; *ṅ* (velar C5) at 0.1%; *jh* (palatal C4) at 0.3%. Within the C5 nasal row alone, *m* at 131 occurrences and *ṅ* at 2 — a **65× variation at "identical column cost."** Each cell carries a specific allocation the engineering calibrates.

**Why useful for Ch 11:** the Mendeleev analogy needs concrete empty-cell + heavily-deployed-cell pairs to make the case that the *gaṇa* grid is engineered, not random. *ch* at 0% and *m* at 131 are the headline cells.

---

## 3. Same-*sthāna* CVC suppression — 62% below chance

> The same principle appears in the CVC frame. For 271 single-syllable primary *dhātavaḥ* with both initial and final *varga* consonants, only 28 (10.3%) share the same place of articulation at both ends. Independence would predict 75 (27.7%). The observed share is **~62% below chance**. The system suppresses *kak*, *pap*, *tat* style repetition because those atoms blur the grid.

**Why useful for Ch 11:** demonstrates that the engineering operates not just at the column level but at the *position-within-atom* level — the grid is calibrated across slots, not just within cells. Pairs with the cell-level allocation finding.

**Reframing note:** if Ch 11 wants to ground this in the *racanā* framework, restrict the analysis to the 819 CV1C (*gamādi*) entries specifically — that's a cleaner "inside-one-scaffold" version of the same suppression test.

---

## 4. Vowel deployment — /a/ as default carrier, /ṛ/ as engineered choice

> The vowel system makes the point sharper. The inherent /a/ dominates at 36.6% of vowel occurrences in primary *dhātavaḥ* — the lowest-cost default carrier. The second most common vowel is the syllabic /ṛ/ (ऋ) at **15.3%**, with 214 distinct primary-class *dhātavaḥ* deploying it (*kṛ*, *vṛ*, *dṛś*, *mṛ*, *hṛ*, *tṛp* and the hundreds of derivatives — *karma*, *mṛtyu*, *prakṛti*, *sṛṣṭi*). Cross-linguistically rare, articulatorily difficult, marginal elsewhere; in Sanskrit it is central.

**Why useful for Ch 11:** the vowel-row of the periodic-table figure needs this. /a/ as the default carrier is the row's anchor; /ṛ/ at 15.3% is the engineered-cost-buys-distinguishability headline. The cross-linguistic rarity of /ṛ/ is exactly the kind of "Sanskrit pays the cost where it buys difference" claim Ch 11 wants to make about the periodic-table structure.

---

## Underlying sources

- C2 / C4 deployment percentages: pre-V1/V2 *varṇa*-only analysis, exact script path TBD (older `analyze_varna_distribution.py` style — re-verify before publication).
- 271-set CVC same-place finding: lives in Ch 10 §10.9 now, but reframe to within-CVC-scaffold there.
- Cell-level percentages (*k* 13.3%, *m* 8.8%, *ch* 0.0%, etc.): same older pipeline.

The current V1/V2-aware template analysis (`analyze_shells.py`, `analyze_matra_distribution.py`, `analyze_matra_by_particle_count.py`) does not produce these numbers directly. Re-running the varṇa-only analysis under the *Yi* correction (parser fix, commit 9455d07) may shift these slightly.
