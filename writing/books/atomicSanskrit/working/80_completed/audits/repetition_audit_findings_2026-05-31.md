# Repetition Audit — Findings (2026-05-31)

*Manuscript-wide scan for repetition. Findings categorized by the seven decision labels defined in `working/80_completed/audits/repetition_audit_2026-05-31.md`. Fixes will run as a separate pass after user decision review.*

*Findings are globally numbered (no per-chapter resets). To redirect a finding, reference it by number alone.*

## Methodology

**Corpus scanned:** Front matter (`as_0_00` – `as_0_04`); body chapters (`as_1_00_seekers` – `as_1_19_life_after_pie`, 20 files); end matter (`as_2_01_epilogue`); appendix parts (`as_3_01_baking` – `as_3_08_glossary`, 8 files). Excluded per scope: `as_endnotes.md`, draft-notes blocks at the ends of chapter files, figure captions, epigraphs, TOC blocks, and reference / working / archive directories. Total manuscript wordcount as scanned: ~138,000 words.

**Procedure:** All in-scope files were read end-to-end. The prior audit (`working/80_completed/audits/repetition_audit_2026-05-31.md`, Passes 0–6 with mechanical scan IDs M001–M025, within-chapter IDs C001–C018, cross-book IDs X001–X014, and refrain IDs R001–R012) was loaded as the baseline. This pass extends the scaffold by (a) flagging substantial cross-chapter material repetition the earlier pass had set aside, (b) flagging within-chapter density problems the earlier batches did not cut, (c) identifying load-bearing claim repetitions whose cuts the user can now reconsider given the new wordcount target.

**What was flagged:** cross-chapter substantive repetition (whole arguments, defined examples, companion blocks reused across body and appendix); within-chapter redundancy of point or example; word- and metaphor-level over-deployment outside the canonical-refrain list.

**What was NOT flagged:** the canonical standing-polemic phrase (*Sanskrit was engineered. Encoded in the Vedas. Decoded by many. Pāṇini's decoding is the finest.*), the four-term *engineered / encoded / decoded / codified* stack, the locked hammer-pairs (*Pyramid: correction by authority. Sanātan: correction by architecture.* / *Domain is not chronology. Mode is not drift.* / *The orthodoxy makes Pāṇini a rupture. The architecture makes him a witness.*), the scale-chain enumeration (*sonomer → akṣara → dhātuḥ → kriyāpada → śabda → vākya → sūtra → calibrated language*), or *prakṛti / saṃskṛti / vikṛti* triad deployments at hinge points. These are flagged KEEP when surfaced; otherwise omitted. Per-chapter establishment-of-cluster-vocabulary (*progressive orthodoxy*, *foundational orthodoxy*, *church of progress*, *asuric pyramid*, *heroic erasure*) is also expected refrain — flagged KEEP only where density seems excessive.

**Wordcount estimates** are conservative; they assume the recommended action is applied cleanly (compress to one line, replace with pointer of equal precision, etc.). True total cut may be ~10-20% higher in practice once seams are tightened after each fix.

## Summary

| Label | Count | Approx. word-count impact if applied |
|---|---:|---:|
| KEEP | 8 | (no cut) |
| COMPRESS | 65 | ~5,200 |
| MERGE | 1 | ~50 (applied 2026-05-31) |
| CUT | 14 | ~3,800 |
| POINTER | 29 | ~6,300 |
| ENDNOTE | 5 | ~2,100 (moved, not cut from book — but cut from body) |
| PROMOTE | 3 | ~400 (small body savings via glossary/sidebar consolidation) |
| **Total findings** | **125** | **~17,850 words trimmed from body if all non-KEEP applied** |

*Counts corrected 2026-05-31 from initial summary (which had transposed several label totals); body labels are authoritative.*

Of this, **~16,400 words are pure cut** (COMPRESS + MERGE + CUT + POINTER + PROMOTE); the **~2,100 ENDNOTE words move out of body but stay in the book as endnotes**. The 49,000-word trim target the user is chasing cannot be hit by repetition cuts alone — the audit suggests repetition can plausibly deliver 15-20k words. The remaining 30k will need scope cuts (whole sections, whole examples, whole worked-walkthroughs) elsewhere.

**Pattern flagged at methodology level:** the largest single class of cuts is **body-appendix duplication**. Appendix Parts 1, 2, 3, 6, 7 re-prosecute claims the body chapters already prosecuted, with substantial verbatim or near-verbatim overlap. The appendix register justifies *some* of this — appendix material is reference-grade, the body is polemic-grade — but the current structure has Appendix 7 (Codification Story Refuted) re-running the bulk of the codification polemic the body already developed across Ch 1, 4, 5, 14, 17. Appendix 7 alone is ~7,500 words; a tight reduction targeted at body-overlap could trim it by 3,000-4,000. Appendix 6 (Vedic Carrier) and Ch 5 §5.6 share the eight-drift-claims discussion in two places. Appendix 1 re-runs Schleicher / PIE / bake material already in Ch 1, Ch 17, Ch 18.

---

## Findings

### Finding 1 — POINTER

**Repeated content:** Four-term polemic stack table (engineered / encoded / decoded / codified) deployed in full table form.

**Instances:**
- `as_1_01_botanical.md` §1.6 lines 141-148 — full four-row table
- `as_3_08_glossary.md` lines 263-271 — same four-row content in compressed form

**Pattern:** The Ch 1 §1.6 table is the canonical exposition. The glossary entry runs the same content. Glossary is the right home for term-by-term reference; Ch 1's table is the right home for the polemic move. Both work; one full table can become a pointer.

**Recommendation:** POINTER — keep Ch 1 §1.6 full table as the polemic deployment; reduce the glossary entry to a one-paragraph pointer to §1.6.

**Word-count impact:** ~120 words

---

### Finding 2 — KEEP

**Repeated content:** Standing polemic phrase *Sanskrit was engineered. Encoded in the Vedas. Decoded by many. Pāṇini's decoding is the finest.*

**Instances:** Preface (twice — opening and chronology section bridge); Ch 1 §1.6; Ch 4 §4.1; Ch 11 §11.10; Ch 14 §14.6 (varied); glossary entry; Appendix 6 §6.7 (varied form: "The Vedas encode the architecture. The vaiyākaraṇāḥ decode...").

**Pattern:** This is the book's signature refrain. The mechanical scan ID M002 already flagged 9 hits; Batch A (per the prior audit) varied the second Preface use and other body uses. The current deployment count is acceptable given the role.

**Recommendation:** KEEP. Already controlled in prior batches.

**Word-count impact:** no cut.

---

### Finding 3 — CUT

**Repeated content:** Banner explanation that *engineered* is an empirical-descriptive judgment, not a historical-active claim about engineers, with *apauruṣeyatva* anchor.

**Instances:**
- `as_0_01_preface.md` line 47 — full explanation
- `as_1_00_seekers.md` §0.11 — partial restatement
- `as_1_01_botanical.md` §1.6 table cell — full explanation again
- `as_1_04_siddha.md` §4.1 ¶ — partial
- `as_1_17_wrong_question.md` §17.6 ¶3 — partial
- `as_3_08_glossary.md` *Engineered* entry — full
- `as_endnotes.md` `apauruseya-mimamsa-sutra-1-1-5` — full

**Pattern:** The same definitional clarification recurs across at least seven places. Two homes are sufficient: Preface (first encounter) + the glossary entry. Other instances can compress to "*engineered* in the empirical-descriptive sense the Preface and glossary anchor."

**Recommendation:** CUT or COMPRESS. Keep Preface line 47 as primary home. Compress Ch 1 §1.6 cell to one sentence. Replace Ch 4 §4.1, Ch 17 §17.6 standalone restatements with one-clause pointers ("the empirical-descriptive sense").

**Word-count impact:** ~250 words

---

### Finding 4 — COMPRESS

**Repeated content:** The "Pāṇini wrote no preface to the *Aṣṭādhyāyī*" observation as evidence that he was a documenter, not an inventor.

**Instances:**
- `as_1_04_siddha.md` §4.2 ¶3 — full development
- `as_3_07_codification_story.md` §7.7 — re-deployed

**Pattern:** Strong specific evidence; loses force when repeated. Ch 4 is the primary home (the chapter is about *siddha*/*kārya*); Appendix 7 should point to Ch 4 rather than re-running the observation.

**Recommendation:** COMPRESS. Keep Ch 4 deployment. In Appendix 7 §7.7, replace with "Pāṇini opens with no statement of authorial intent (Ch 4 §4.2 develops)."

**Word-count impact:** ~120 words

---

### Finding 5 — CUT

**Repeated content:** Full list of pre-Pāṇinian grammarians with Devanagari (Śākalya, Āpiśali, Kāśyapa, Gārgya, Gālava, Cākravarmaṇa, Bhāradvāja, Saunaga, Senaka, Sphoṭāyana).

**Instances:**
- `as_1_01_botanical.md` §1.6 — full list with Devanagari
- `as_1_04_siddha.md` §4.1 — full list with Devanagari
- `as_3_07_codification_story.md` §7.7 — full list with Devanagari
- `as_3_01_baking.md` §1.3 — partial
- `as_1_17_wrong_question.md` §17.5 — partial roster
- `as_1_19_life_after_pie.md` §19.1 — Saptaṛṣi roster (different but adjacent)
- glossary references

**Pattern:** The full ten-name roster with Devanagari pairings appears three times verbatim (Ch 1, Ch 4, Appendix 7). Ch 4 is the canonical home (the chapter dedicated to pre-Pāṇinian grammar). The prior audit's M010 already flagged this; the recommendation was Ch 4 / App 7 as full home, Ch 1 to compress. That recommendation was apparently not applied.

**Recommendation:** CUT to single canonical home. Ch 4 §4.1 keeps the full roster. Ch 1 §1.6 compresses to "Śākalya, Āpiśali, and the rest of the roster Ch 4 names." Appendix 7 §7.7 compresses to a pointer "the pre-Pāṇinian roster Ch 4 §4.1 names."

**Word-count impact:** ~280 words

---

### Finding 6 — COMPRESS

**Repeated content:** *Saṃskṛtam* canonical gloss — "perfectly synthesized or wholly created" — with *sam-* + *kṛta* etymology.

**Instances:**
- `as_0_01_preface.md` §The Engineering Claim
- `as_1_00_seekers.md` §0.4
- `as_1_01_botanical.md` §1.4
- `as_3_08_glossary.md`
- `as_endnotes.md` `samskrtam-morphology`

**Pattern:** The canonical gloss appears unbroken in Preface, Ch 0 §0.4, and Ch 1 §1.4 in succession — three back-to-back books-opening sections. CLAUDE.md says "may be compressed but not broken in later chapters" — currently it is delivered in full three times before the reader has finished Part I.

**Recommendation:** COMPRESS. Keep Preface as full deployment. Ch 0 §0.4 compresses to "*saṃskṛtam* — perfectly synthesized (Preface)." Ch 1 §1.4 keeps the structural-declaration framing but drops the *sam-* + *kṛta* breakdown, pointing back to Preface and the `samskrtam-morphology` endnote.

**Word-count impact:** ~200 words

---

### Finding 7 — MERGE ✓ APPLIED 2026-05-31

**Status:** Applied 2026-05-31. Preface line 31 received per-chapter first-use Devanagari (प्रतिबिम्ब); Ch 19 opening exposition paragraph cut; Ch 19 §19.3 Romani paragraph promoted to first-use Devanagari; Epilogue §1 *reflections-or-a* re-gloss dropped and promoted to first-use Devanagari. Ch 0 §0.3, Ch 5 §5.6 cross-reference, Ch 18 §§18.5–18.6, and Glossary entry retained per the keep-recommendation. ~50 body words trimmed.

**Repeated content:** *Pratibimba* (प्रतिबिम्ब) introduction — what the cognates carry as reflections of the Sanskrit calibrant.

**Instances:**
- `as_0_01_preface.md` line 31 — short deployment
- `as_1_00_seekers.md` §0.3 — *Pratibimba* of the calibrant
- `as_1_05_apabhramsa.md` §5.6 close — calibrant-anchored language argument adjacent
- `as_1_18_pie_in_sky.md` §18.5, §18.6 — main development
- `as_1_19_life_after_pie.md` opening — restated
- `as_2_01_epilogue.md` §1 — restated
- `as_3_08_glossary.md` — full definition

**Pattern:** The concept is established in Preface (line 31), redeployed in Ch 0 §0.3, then carried as a load-bearing claim across Ch 18 (the prosecution). Ch 19 opens by restating "PIE was an average of *Pratibimba*s," and the Epilogue restates the calibrant-and-reflection frame. Three of these (Ch 19 opening, Epilogue §1, glossary) are pure restatements of what Ch 18 just developed.

**Recommendation:** MERGE. Preface line 31 is the seeding hint. Ch 18 §18.6 is the load-bearing development. Ch 19 opening can drop the *Pratibimba* exposition (the reader has just read it) and open with the wave framework directly. Epilogue §1 can use *Pratibimba* without re-defining. Glossary entry is reference-correct as-is.

**Word-count impact:** ~250 words

---

### Finding 8 — COMPRESS

**Repeated content:** Schleicher 1868 fable + *Avis akvāsas ka* + asterisk-invention details.

**Instances:**
- `as_1_01_botanical.md` §1.2 — Schleicher 1860s, family tree
- `as_1_03_fourth_abrahamic.md` §3.6 close — Schleicher as asuric operator with the bake; references Appendix Part 4 §4.8
- `as_1_18_pie_in_sky.md` §18.1 — full development of fable + reconstructed words
- `as_3_01_baking.md` §1.4 — Schleicher full biographical block with *Compendium* (1861), *Stammbaumtheorie*, *Avis akvāsas ka* (1868), full reconstructed words
- `as_3_04_language_factory.md` §4.1 + §4.8 — Schleicher polemic re-developed with full context (had the recipe / chose not to use it / Compendium 1861 / Avis akvāsas ka 1868)

**Pattern:** The Schleicher polemic — including the 1868 fable, the asterisk invention, the specific reconstructed-word inventory, and the "had the recipe but chose not to use it" thesis — appears in increasingly detailed form across Ch 1, Ch 3, Ch 18, Appendix 1, Appendix 4. App 4 §4.8 substantially duplicates App 1 §1.4 and Ch 18 §18.1.

**Recommendation:** COMPRESS. Ch 18 §18.1 is the prosecution-spine home of the Schleicher case. Appendix 1 §1.4 keeps the reference-grade biographical apparatus (Bopp, Pott, Schleicher, Brugmann timeline — appendix register). Appendix 4 §4.1 + §4.8 compresses the Schleicher repeat to a pointer to Ch 18 + App 1; the "had the recipe but chose not to use it" thesis appears once in App 4 §4.8 (where it serves the language-factory contrast); the Schleicher biographical specifics are dropped from App 4. Ch 3 §3.6 close keeps its compressed naming of Schleicher as a contemporary asuric operator (one paragraph; current treatment fine).

**Word-count impact:** ~500 words

---

### Finding 9 — CUT

**Repeated content:** Detailed Bhāṇḍārkar biographical record (CIE 1889, KCIE 1911, Göttingen Honorary Ph.D. 1885, etc.).

**Instances:**
- `as_3_01_baking.md` §1.3 — full record (~200 words)
- prior session work referenced him in `working/` files

**Pattern:** Single deployment in App 1. No body chapter repeats it. Internal to App 1: the level of biographical detail (six honors, three council memberships, four honorary doctorates, three scholarly correspondents, BORI founding date and birthday) carries the companion register. But the appendix's structural point — that the colonial honors system was the elevation rite — does not require all six honors named individually.

**Recommendation:** CUT detail; keep structural exemplar. Compress the Bhāṇḍārkar paragraph from ~200 words to ~90 words: name Bhāṇḍārkar, CIE 1889 / KCIE 1911, Deccan College professor, Göttingen Honorary Ph.D. 1885, BORI named for him 1917. Drop the four-doctorate list, the multi-council list, and the scholarly-correspondents list.

**Word-count impact:** ~110 words

---

### Finding 10 — COMPRESS

**Repeated content:** *Heroic erasure* definition and the four-case pattern (Pāṇini / Prātiśākhya / Śikṣā / script adapter).

**Instances:**
- `CLAUDE.md` reference block (out of scope)
- `as_1_08_mapping_mouth.md` §8.6 — establishes
- `as_1_13_preservation.md` §13.3 — re-develops with full four-case pattern
- `as_1_14_calibration.md` §14.5 — explicit naming at preservation-system level
- `as_1_17_wrong_question.md` §17.7 — re-deployed
- `as_3_03_audiography.md` §3.3 — re-deployed for script case
- `as_3_07_codification_story.md` opening — re-deployed
- `as_3_08_glossary.md` — full definition

**Pattern:** The term recurs ~7 times. CLAUDE.md says establish in Ch 8 §8.6, deploy where the polemic move surfaces. Current deployment is functional but the four-case pattern enumeration runs twice in full (Ch 13 §13.3 + Ch 14 §14.5), and Ch 17 §17.7 redevelops the move at the matrix scale.

**Recommendation:** COMPRESS. Ch 8 §8.6 establishes. Ch 13 §13.3 keeps the full four-case pattern (it's about preservation-level heroic erasure). Ch 14 §14.5 deploys the term without re-listing the four cases. Ch 17 §17.7 keeps its specific deployment (Pāṇini-as-rupture is one case). App 3 §3.3 is fine. App 7 opening loses the standalone heroic-erasure naming and folds it into existing prose ("the praise is the mechanism the book has named heroic erasure").

**Word-count impact:** ~300 words

---

### Finding 11 — POINTER

**Repeated content:** *Sindhuḥ* → *Hinduš* → *Indós* / *Indus* worked example of visarga/contact-language loss.

**Instances:**
- `as_1_08_mapping_mouth.md` §8.3 — full development
- `as_1_18_pie_in_sky.md` §18.6 — referenced as parallel to *deva* / *asura*
- `as_1_18_pie_in_sky.md` §18.7 — Ch 8 §8.3 cross-referenced for *s* → *h* shift

**Pattern:** Ch 8 §8.3 is the canonical home. Ch 18 references are mostly pointers already; no cut needed.

**Recommendation:** KEEP as-is (already operating as pointer). No new finding.

**Word-count impact:** no cut.

(Tag: bookkeeping — flagged here so the user does not re-prosecute it.)

---

### Finding 12 — CUT

**Repeated content:** *Mahābhāṣya* Vārttika opening — *siddhe śabdārthasambandhe lokato 'rthaprayukte śabdaprayoge śāstreṇa dharmaniyamaḥ* — full Sanskrit + translation block.

**Instances:**
- `as_1_04_siddha.md` §4.2 — full Sanskrit block + translation + breakdown
- `as_3_02_encyclopaedic.md` §2.3 — partial (the chapter epigraph short form)
- `as_3_02_encyclopaedic.md` §2.9 — both Sanskrit lines (Patañjali siddha + apabhraṃśa) in two-slogan blockquote
- `as_3_07_codification_story.md` §7.8 — full Sanskrit block + translation
- glossary entry — references

**Pattern:** The full Vārttika appears twice (Ch 4 §4.2, App 7 §7.8). The order-walking analysis (bond first / usage second / *śāstra* third) appears in both Ch 4 §4.2 and App 7 §7.8. The two-slogan Patañjali blockquote in App 2 §2.9 (which restages siddhe-śabdārthasambandhe + bhūyāṃsaḥ apabhraṃśāḥ) is a separate device but compounds the density.

**Recommendation:** CUT one deployment. Ch 4 is the canonical home. App 7 §7.8 keeps the principle ("Patañjali begins with siddhe śabdārthasambandhe") and the bond-first-usage-second-śāstra-third order, but drops the full Sanskrit block, pointing to Ch 4 §4.2. App 2 §2.9's two-slogan blockquote can stay (it's a rhetorical device for the dictionary recommendation, not a re-argument).

**Word-count impact:** ~180 words

---

### Finding 13 — CUT

**Repeated content:** Patañjali's four documented *apabhraṃśas* of *gauḥ* (*gāvī, goṇī, gotā, gopotalikā*) with the *bhūyāṃso 'pabhraṃśāḥ* quantitative observation.

**Instances:**
- `as_1_05_apabhramsa.md` §5.3 + FIGURE 5.1 — full development
- `as_1_13_preservation.md` §13.1 — restated
- `as_3_02_encyclopaedic.md` §2.5 — restated with Sanskrit blockquote
- `as_3_07_codification_story.md` §7.8 — full list with Devanagari restated

**Pattern:** The four corruption forms with Devanagari (*gāvī, goṇī, gotā, gopotalikā*) appear in four chapters. Ch 5 is the canonical home with the figure. Ch 13 §13.1 and App 2 §2.5 and App 7 §7.8 re-deploy.

**Recommendation:** CUT to canonical home + minimal pointer. Ch 5 keeps. Ch 13 §13.1 reduces to one sentence ("Chapter 5 §5.3 examined Patañjali's canonical *gauḥ* / *gāvī / goṇī / gotā / gopotalikā* case"). App 2 §2.5 keeps the Sanskrit blockquote (it's argumentatively necessary at that point) but drops the four-form list. App 7 §7.8 reduces to "*gauḥ* becomes *gāvī, goṇī, gotā, gopotalikā* (Chapter 5)."

**Word-count impact:** ~220 words

---

### Finding 14 — COMPRESS

**Repeated content:** Eight orthodox drift-claims with engineering-mode responses — the *chandasi*/*bhāṣāyām* mode-difference defense at length.

**Instances:**
- `as_1_05_apabhramsa.md` §5.6 — summary paragraph + Appendix Part 6 forward-pointer
- `as_3_06_vedic_carrier.md` §6.5 — full 8-row table with all eight examples
- `as_1_14_calibration.md` §14.4 — *vaicitrya* deployment with multiple-infinitive, plutaḥ, leṭ-lakāra, ळ, pronoun alternates list
- `as_1_16_retroflex.md` §16.4 — full ळ argument as worked case
- `as_3_07_codification_story.md` §7.5, §7.13 — re-deployed without the table

**Pattern:** Appendix 6 §6.5 is the canonical home (it has the table). The same examples (multiple infinitives, *plutaḥ*, *leṭ-lakāra*, ळ, pronoun alternates) recur in Ch 5, Ch 14, Ch 16, App 7. Three of these (Ch 14, Ch 16, App 7) carry the load of the polemic; Ch 5 already points forward; App 7 re-runs without adding new evidence.

**Recommendation:** COMPRESS App 7 §7.5. The section restates the mode-not-drift argument; the table is in App 6 §6.5. App 7 §7.5 can be compressed from ~350 words to ~150 words by pointing to App 6's table after one or two illustrative cases.

**Word-count impact:** ~200 words

---

### Finding 15 — COMPRESS

**Repeated content:** *Sūtra-lakṣaṇam* six characteristics list with Devanagari pairings.

**Instances:**
- `as_1_10_building_dhatuh.md` §10.1, §10.6, §10.16 — full enumeration three times in one chapter
- `as_1_14_calibration.md` §14.4 — same six characteristics applied to the whole language

**Pattern:** Within Ch 10, the six characteristics appear in §10.1 (full Devanagari list as the chapter's specification), restated as engineering criteria in §10.6 (renamed and reordered), and recounted in §10.16 ("alpākṣaram appears in compact sonomer..."). The §10.6 restatement is the prior audit's C008 flagged-for-compression item, which the audit batches reportedly compressed. The §10.16 verdict pass is also a full enumeration. Ch 14 §14.4 then re-deploys at language scale.

**Recommendation:** COMPRESS §10.16 verdict. Keep §10.1 (specification) and §10.6 (criteria). §10.16 can drop the per-criterion re-enumeration and run "The dhātuḥ passes all six tests. The principle stated at the level of the sūtra reaches the atom." Saves ~120 words while preserving the verdict. Ch 14 §14.4 is fine (load-bearing — it's the scale-up claim).

**Word-count impact:** ~120 words

---

### Finding 16 — KEEP

**Repeated content:** *Pyramid: correction by authority. Sanātan: correction by architecture.* hammer pair.

**Instances:** Ch 5 §5.4 (canonical home); Ch 9 §9.11 (variant: *standardization by architecture, not by authority*); Ch 13 §13.5; App 7 §7.4.

**Pattern:** Canonical hammer per CLAUDE.md. Prior audit R012 flagged for KEEP at Ch 5; pointer elsewhere. Currently Ch 9, Ch 13, App 7 all carry the same hammer or close variants. Density is acceptable for a signature hammer that's the spine of the calibration polemic.

**Recommendation:** KEEP. Density is within bounds. Do not cut.

**Word-count impact:** no cut.

---

### Finding 17 — COMPRESS

**Repeated content:** *Calibration is standardization by architecture. Codification is standardization by authority.* expansion — the three-frame distinction (natural drift / codification / calibration).

**Instances:**
- `as_1_05_apabhramsa.md` §5.4 — full three-frame development
- `as_1_13_preservation.md` §13.5 — Greek / Latin / Arabic / Hebrew / Tibetan five-language drumbeat with codification-doesn't-stop-drift opening
- `as_1_14_calibration.md` §14.5 — Masoretic / Quranic / Vulgate as control cases
- `as_3_07_codification_story.md` §7.4 — full three-frame restatement
- `as_2_01_epilogue.md` §1 — swastika-systems paragraph with same five-language drumbeat
- `as_3_07_codification_story.md` §7.4 — explicit three-frame list

**Pattern:** Three-frame distinction is the spine claim. Ch 5 §5.4 is the canonical home. Ch 13 §13.5 develops the codified-languages-keep-drifting argument with a different drumbeat (Greek / Latin / Arabic / Hebrew / Tibetan as five examples of codification failing to stop drift). Ch 14 §14.5 covers Masoretic / Quranic / Vulgate as positive engineered-preservation control cases that the orthodoxy already recognizes. App 7 §7.4 restates the three-frame distinction from Ch 5 in full. Epilogue §1's swastika-systems paragraph re-runs the Hebrew / Quranic Arabic / ecclesiastical Latin / Greek / Tibetan drumbeat from Ch 13 §13.5 with the same structural verdict.

**Recommendation:** COMPRESS the App 7 §7.4 restatement of Ch 5's three frames to a pointer. The Epilogue §1 swastika-systems paragraph keeps the verdict-register hammer but compresses the five-language drumbeat from full prose to a single sentence ("Greek, Latin, Arabic, Hebrew, and Tibetan all show the limit: codification holds a standard by authority around a bounded object while ordinary speech keeps moving — Ch 13 §13.5 develops"). Ch 14 §14.5 keeps its full Masoretic/Quranic/Vulgate development (that's about preservation control cases, structurally different).

**Word-count impact:** ~400 words

---

### Finding 18 — POINTER

**Repeated content:** Yāska's *agni* decoding (four-fold derivation: *agra-nī, aṅga-nī, aknopana, i+añj+dah*) with Devanagari + Sthaulāṣṭhīvi + Śakapūṇi attributions.

**Instances:**
- `as_1_10_building_dhatuh.md` §10.13 — full development as worked example
- `as_1_01_botanical.md` §1.6 reference (one-liner with Ch 10 §10.13 cross-reference)
- `as_1_04_siddha.md` §4.1 — Yāska + Sthaulāṣṭhīvi + Śakapūṇi naming

**Pattern:** Ch 10 §10.13 carries the full *agni* analysis. Ch 1 and Ch 4 reference the lineage; they don't repeat the agni decoding. Current treatment is correct.

**Recommendation:** KEEP. Already a pointer pattern. (Flagged for bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 19 — POINTER

**Repeated content:** Western philological apparatus' demotion of Sanskrit from source to cognate — the *mother* / *mātṛ* dictionary-shift example.

**Instances:**
- `as_1_18_pie_in_sky.md` opening + §18.5 — full development with AHD 1992 / MW 1993 side-by-side entries + three-stage demotion + nursery-word deflection death-at-*yoke*
- `as_3_01_baking.md` §1.5 Case 3 — same *mātṛ* / *mother* case with Watkins-baby-talk-routing apology

**Pattern:** Ch 18 §18.5 is the polemic-spine deployment. App 1 §1.5 Case 3 re-deploys for the dhātu-cluster-evidence prosecution. The overlap is partial — App 1's framing is *Sanskrit dhātu splintered across multiple PIE roots* while Ch 18's framing is *Sanskrit demoted from terminus to cognate*. But the central evidence (Sanskrit *mātṛ* paired with reconstructed PIE *\*méh₂tēr-*) is the same.

**Recommendation:** POINTER. App 1 §1.5 Case 3 keeps the dhātu-splinter point but drops the *mother* / *mātṛ* dictionary-entry detail (it's in Ch 18 §18.5). The Case 3 can run as "√मा (*mā*, to measure) → *mātṛ*, *mātrā*, *māna*, *māsa*, *māyā* — one *dhātu*, one semantic axis. Orthodox account splits into \*méh₂tēr- ('mother') and \*meh₁- / \*me- (2) ('measure'), held separately in the lookup pages despite Sanskrit's structural connection (Ch 18 §18.5 develops the mother chain in detail)."

**Word-count impact:** ~250 words

---

### Finding 20 — POINTER

**Repeated content:** *dṛś* / *paśyati* one-dhātu-many-PIEs case with the *suppletion* Wiktionary quote.

**Instances:**
- `as_1_18_pie_in_sky.md` §18.8 — full development with table
- `as_3_01_baking.md` §1.5 Case 1 — same case with same table

**Pattern:** Verbatim or near-verbatim restatement. Ch 18 §18.8 is the climactic prosecution; App 1 §1.5 leads off with the same case.

**Recommendation:** POINTER. App 1 §1.5 keeps the case header and the dhātu introduction. The table and Wiktionary suppletion quote stay in Ch 18 §18.8 (the polemic-spine home). App 1 Case 1 compresses to ~80 words: "√दृश् (*dṛś*, to see) generates the unified family *darśanam* / *dṛṣṭi* / *dṛśyam* / *paśyati*. Orthodox account splits across \*derḱ-, \*spek-, and (for *theory*) \*wer-(3) — one dhātu, three PIE roots, with the regime's *suppletive* admission on the Wiktionary entry for paśyati. Ch 18 §18.8 prosecutes in detail."

**Word-count impact:** ~280 words

---

### Finding 21 — COMPRESS

**Repeated content:** *Apabhraṃśa* / vivimorphosis arrow chain — *dhātu → śabda → bīja → apaśabda* with the "atom → molecule → seed → root — life begins" punch line.

**Instances:**
- `as_1_12_building_vakya.md` §12.9 — full development as the chapter's coda
- `as_1_18_pie_in_sky.md` §18.5 (yoke), §18.6 (devaḥ), §18.7 (asura) — three worked examples deploying the chain
- `as_3_01_baking.md` §1.4 — references *apaśabda → śabda* inversion polemic

**Pattern:** Ch 12 §12.9 is the canonical mechanism home. Ch 18 deploys the mechanism three times in three sections. The third deployment (asura, §18.7) ends with the same "atom → molecule → seed → root — life begins" hammer that's been delivered twice already in the same chapter (yoke §18.5, devaḥ §18.6).

**Recommendation:** COMPRESS. Ch 18 §18.5 (yoke) keeps the full chain. Ch 18 §18.6 (devaḥ) compresses the chain to two lines, drops the "life begins" close (the reader saw it five paragraphs ago). Ch 18 §18.7 (asura) keeps the chain (it's the *asura* polemic, structurally distinct), but drops the "life begins" tagline.

**Word-count impact:** ~180 words

---

### Finding 22 — KEEP

**Repeated content:** *Make it small. Remove waste. Prevent ambiguity. Give it meaning. Let it face many directions. Preserve identity through use.* — the six-step engineering sequence.

**Instances:**
- Ch 10 §10.2 (chapter method) and §10.6 (six atomic criteria) — flagged in prior audit C008.

**Pattern:** Per the prior audit's Batch D, §10.6 was converted to a pointer to §10.2. Re-reading the current text suggests both still carry the sequence in tabular form. Current treatment with the §10.2 → §10.6 progression is correct (one as method, one as criteria), but the prior audit's pointer-compression may not have fully applied.

**Recommendation:** KEEP if the prior C008 fix has been applied as intended. If still showing redundant six-line lists, COMPRESS §10.6 to one sentence saying "The six-step method becomes six atomic criteria below" without re-listing.

**Word-count impact:** ~80 words (conditional).

---

### Finding 23 — COMPRESS

**Repeated content:** "Sanātan did not require every person to speak the calibrant language" + the *prākṛtika* speech allowed to flow / Sanskrit-as-calibrant distinction.

**Instances:**
- `as_1_13_preservation.md` §13.5 — full development
- `as_3_07_codification_story.md` §7.9 — restated
- `as_2_01_epilogue.md` §6 The Inward Correction — restated with Marathi-Pune / Konkani-separation specifics

**Pattern:** Ch 13 §13.5 is the canonical home for the calibrant-vs-imperial-tongue distinction. App 7 §7.9 restates. Epilogue §6 deploys (correctly, as the inward-correction call). The two repeats add nothing the §13.5 deployment didn't already say.

**Recommendation:** COMPRESS App 7 §7.9 restatement; keep Epilogue (its inward-correction context is distinct). App 7 §7.9 can run as "Ordinary speech always changes; Sanskrit's calibrated architecture did not collapse into that change. Prākṛtika speech flowed; the calibrant remained. Ch 13 §13.5 develops."

**Word-count impact:** ~140 words

---

### Finding 24 — COMPRESS

**Repeated content:** Mitanni evidence — Mitra/Varuṇa/Indra/Nāsatya treaty, Kikkuli numerical correspondences, throne names, *marya* warrior term.

**Instances:**
- `as_1_19_life_after_pie.md` §19.1 — full development with Suppiluliuma/Shattiwaza treaty, Bogazköy archive, Kikkuli 184-day/1080-line/4-tablet detail, *aika*/*tera*/*panza*/*satta*/*na*/*vartana* numerical correspondences, throne names list, *marya*
- `as_3_07_codification_story.md` §7.14 — referenced briefly + Ch 13 and Ch 18 cross-references
- `as_1_18_pie_in_sky.md` §18.6 — referenced briefly

**Pattern:** Ch 19 §19.1 is the canonical-home companion (the Wave 1 transmission chapter). Ch 18 §18.6 and App 7 §7.14 reference it. Current treatment is mostly correct — App 7 §7.14 compresses correctly. The Ch 19 §19.1 detail block is appropriate for its load-bearing role.

**Recommendation:** KEEP Ch 19 + App 7 pattern as-is. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 25 — COMPRESS

**Repeated content:** Ch 19 §19.2 Wave-2-of-methodological-metatypy six cases (Greek / Latin / Tibetan / Arabic / Hebrew / Chinese-as-contrast) — full development.

**Instances:**
- `as_1_19_life_after_pie.md` §19.2 — full development
- `as_2_01_epilogue.md` §1 The Path to Redemption + swastika-systems — partial restatement
- `as_1_14_calibration.md` §14.5 forward-points

**Pattern:** Ch 19 §19.2 is the canonical home (~1,200 words of detail). The Epilogue swastika-systems paragraph then restates the Greek/Latin/Arabic/Hebrew/Tibetan five examples in compressed form. This isn't strict repetition but it carries enough content that the Epilogue paragraph can be reduced further by pointing to Ch 19 §19.2.

**Recommendation:** COMPRESS. Epilogue swastika-systems paragraph keeps its verdict-register hammer (codification holds-by-authority around bounded object; calibration holds-by-architecture across living architecture) but drops the language-by-language enumeration, pointing to Ch 19 §19.2 and Ch 14 §14.5 for the cases.

**Word-count impact:** ~180 words

---

### Finding 26 — COMPRESS

**Repeated content:** *Yaska / Sthaulāṣṭhīvi / Śakapūṇi* attribution pattern for pre-Pāṇinian decoders.

**Instances:**
- `as_1_01_botanical.md` §1.6 — naming
- `as_1_04_siddha.md` §4.1 — naming with full Nirukta extension
- `as_1_10_building_dhatuh.md` §10.13 — naming via agni-decoding development
- `as_1_17_wrong_question.md` §17.5 (honest speculation) — naming
- `as_3_07_codification_story.md` §7.7 — naming

**Pattern:** The Yāska + Sthaulāṣṭhīvi + Śakapūṇi trio appears in five chapters. Ch 4 is the canonical home (the chapter dedicated to pre-Pāṇinian grammar). Ch 10 §10.13 uses them functionally (in the agni worked example). The other deployments (Ch 1, Ch 17, App 7) are restatements without new evidence.

**Recommendation:** COMPRESS Ch 1, Ch 17, App 7 to pointers ("Yāska, Sthaulāṣṭhīvi, Śakapūṇi, and the rest of the pre-Pāṇinian roster — see Ch 4 §4.1"). Ch 4 keeps. Ch 10 §10.13 keeps (functional use).

**Word-count impact:** ~120 words

---

### Finding 27 — COMPRESS

**Repeated content:** "*śabdāḥ* become *apaśabdāḥ*" inversion-direction polemic against PIE.

**Instances:**
- `as_3_01_baking.md` §1.4 — "*śabdāḥ* become *apaśabdāḥ*" with cross-reference to Ch 5 §5.3 + Ch 12 §12.5
- `as_1_17_wrong_question.md` §17.6 (honest speculation #3) — "*śabdāḥ* become *apaśabdāḥ*. *gauḥ* becomes *gāvī, goṇī, gotā, gopotālikā*"
- `as_3_07_codification_story.md` §7.8 — "*śabdāḥ* become *apaśabdāḥ*. *gauḥ* becomes *gāvī, goṇī, gotā, gopotālikā*"
- `as_1_12_building_vakya.md` §12.9 — *apaśabda* mechanism

**Pattern:** The inversion claim appears multiple times. Ch 12 §12.9 is the mechanism home (vivimorphosis); Ch 5 §5.3 is the *apabhraṃśa* / *apaśabda* example home. Ch 17 §17.6 and App 7 §7.8 each carry both — the *gauḥ* list (which is Ch 5's job) and the inversion direction polemic (which is App 1's job).

**Recommendation:** COMPRESS. Ch 17 §17.6 and App 7 §7.8 each drop the *gauḥ → gāvī* etc. list (pointer to Ch 5 §5.3 suffices). The inversion polemic stays in one of the two; the other compresses to a pointer.

**Word-count impact:** ~150 words

---

### Finding 28 — POINTER

**Repeated content:** *Asuratva* full morphological derivation — *svar* → *suraḥ* → *asuraḥ* via privative *a-*.

**Instances:**
- `as_1_03_fourth_abrahamic.md` §3.6 — establishes
- `as_1_18_pie_in_sky.md` §18.7 — re-developed for vivimorphosis worked example
- `as_3_08_glossary.md` — full definition

**Pattern:** Ch 3 §3.6 establishes; Ch 18 §18.7 uses it functionally (the morphology drives the vivimorphosis chain at the contact-language boundary). Ch 18's use is structurally distinct (it's about Avestan *ahura* as *apaśabda*); no cut.

**Recommendation:** KEEP both. Ch 18 §18.7 is a different argument that needs the morphology. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 29 — CUT

**Repeated content:** Five-discipline list of "decoding disciplines" (*vyākaraṇam, nirukta, śikṣā, chandas, mīmāṃsā* or *vyākaraṇam, nirukta, prātiśākhya, śikṣā, chandas*).

**Instances:**
- `as_1_00_seekers.md` §0.5 — corpus inventory
- `as_1_01_botanical.md` §1.6 — naming
- `as_1_10_building_dhatuh.md` §10.13 — naming
- `as_1_13_preservation.md` §13.5 — preservation architecture list
- `as_1_14_calibration.md` §14.3, §14.6 — six-layer calibration matrix with all six
- `as_1_17_wrong_question.md` §17.1 (the architectural test sixth requirement) — naming
- `as_2_01_epilogue.md` §1 swastika-systems — naming
- `as_3_07_codification_story.md` §7.4 — naming

**Pattern:** The Vedāṅga list and "decoding disciplines" enumeration is functionally necessary in many places but the full Devanagari + IAST + gloss pairing appears more often than needed. Ch 14 §14.3 is the canonical six-layer-calibration-matrix home with full per-layer development. Other deployments can use plain English / italic Roman without re-glossing.

**Recommendation:** CUT redundant glossing. Ch 14 §14.3 is the full development. Other appearances run as "the Vedāṅga disciplines" or "Prātiśākhya, Śikṣā, Chandas, Vyākaraṇam, the *pāṭha*s" without Devanagari first-use re-glossing (each was anchored in Ch 14 §14.3 or earlier).

**Word-count impact:** ~180 words

---

### Finding 30 — COMPRESS

**Repeated content:** Eleven *pāṭha* recitation forms enumeration (saṃhitā, pada, krama, jaṭā, ghana + six vikṛti: mālā, śikhā, rekhā, dhvaja, daṇḍa, ratha) with all Devanagari + glosses.

**Instances:**
- `as_0_01_preface.md` line 112 — reference (no enumeration)
- `as_1_15_aural.md` §15.2 — full eleven-pāṭha enumeration with Devanagari + glosses
- `as_1_14_calibration.md` §14.5 — references "jaṭā and ghana pāṭhas"
- `as_2_01_epilogue.md` §1 — references "eleven *pāṭhas* — *saṃhitā*, *pada*, *krama*, *jaṭā*, *ghana*, plus the six *vikṛti* recitations" without Devanagari

**Pattern:** Ch 15 §15.2 is the canonical home. Epilogue §1's listing is fine (no Devanagari re-glossing). Current pattern works.

**Recommendation:** KEEP as-is. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 31 — POINTER

**Repeated content:** Frits Staal's *varga*-as-Mendeleev-periodic-table comparison.

**Instances:**
- `as_1_08_mapping_mouth.md` §8.6 — full development
- `as_1_11_building_kriya.md` §11.10 — Mendeleev 1869 referenced
- `as_3_08_glossary.md` — references

**Pattern:** Ch 8 §8.6 is the polemic home (with the structural refutation of Staal's "centuries of analysis" hypothesis). Ch 11 §11.10 deploys the Mendeleev figure functionally (the Dhātupāṭha as the table of reactive atoms). No real overlap; different scales.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 32 — COMPRESS

**Repeated content:** "The architecture is on the ground." hammer.

**Instances:** Per prior audit M001 (9 exact hits across Ch 9, Ch 13, Ch 14, Ch 15, Ch 18 multiple, App 1).

**Pattern:** Already addressed in Batch H (Closeout) of prior audit per the edit log. Re-reading confirms most instances were varied. Ch 18 carries the title-payoff variant. No further action needed beyond bookkeeping.

**Recommendation:** KEEP as currently deployed. Prior batches already adjusted.

**Word-count impact:** no cut.

---

### Finding 33 — COMPRESS

**Repeated content:** Three-tier "depth band" chronology vocabulary (recent/middle/deep) explanation — when to use *thousands of years* vs *generations* vs internal-frame ordering.

**Instances:**
- `as_0_01_preface.md` §Chronology Refused — full explanation
- `as_3_02_encyclopaedic.md` §2.3 — partial restatement ("This book uses different language for Indic texts: thousands of years as the primary phrase...")
- `as_2_01_epilogue.md` §4 The Chronology Refusal — restatement

**Pattern:** Preface is the canonical home with the full three-tier table. App 2 §2.3 and Epilogue §4 carry the strategic-refusal claim functionally — they don't restate the table, but they do paraphrase the same position twice more.

**Recommendation:** COMPRESS the Epilogue §4 chronology-refusal section. The current draft runs ~600 words explaining the refusal again. It can compress to ~350 words by removing the "Eighty years after India's political independence..." passage (which repeats Preface verbatim) and pointing to Preface for the strategic-refusal frame. The Deccan-College institutional-continuation point is structurally distinct and stays.

**Word-count impact:** ~250 words

---

### Finding 34 — COMPRESS

**Repeated content:** Ambedkar block-quote from *Pakistan, or the Partition of India* (1940/1945) about Islam as a closed corporation.

**Instances:**
- `as_1_03_fourth_abrahamic.md` §3.1 — full block-quote with framing

**Pattern:** Single deployment. No repetition. (Flagged here only because the prior audit may have considered it as a potential cut for fitting other examples — the block-quote is ~80 words and the framing around it is another ~150.)

**Recommendation:** KEEP. Single deployment.

**Word-count impact:** no cut. (Bookkeeping.)

---

### Finding 35 — CUT

**Repeated content:** The "asuric pyramid converts X" formula trio (chronology / codification / etc.).

**Instances:**
- `as_0_03_prologue.md` — "The apparatus converts evidence into containment. It converts domain and mode into chronology. It converts decoding into codification."
- `as_1_01_botanical.md` §1.1 Move 7 — "The asuric apparatus converts domain and mode into chronology."

**Pattern:** Both formulations carry the same conversion claim. Prologue establishes; Ch 1 redeploys.

**Recommendation:** KEEP. Each lands the structural claim in a different polemic context (Prologue as accusation; Ch 1 as the Move-7 prosecution). Acceptable density.

**Word-count impact:** no cut. (Bookkeeping.)

---

### Finding 36 — POINTER

**Repeated content:** Devakcollege founding history (1821 as Pāṭhaśālā under Elphinstone with Dakṣiṇā endowment + Bajirao II + renamings).

**Instances:**
- `as_3_01_baking.md` §1.2 — full
- `as_3_02_encyclopaedic.md` §2.2 — restated

**Pattern:** App 1 and App 2 both rehearse the founding arc. App 1's deployment is structurally appropriate (the bake chapter). App 2's deployment is also functional (the postcolonial continuation chapter) but it does not need to restate the founding arc — only the post-independence period matters for App 2.

**Recommendation:** POINTER. App 2 §2.2 compresses the founding-arc paragraph to one sentence pointing to App 1 §1.2 ("Deccan College carried the institutional lineage Appendix Part 1 §1.2 traces — Pāṭhaśālā 1821, Poona College 1851, Deccan College 1864, Post-Graduate Research Institute after independence"). Drop the Elphinstone / Bajirao II / Dakṣiṇā / endowment-redirection detail.

**Word-count impact:** ~140 words

---

### Finding 37 — COMPRESS

**Repeated content:** Masoretic / Quranic / Vulgate "control cases" three-tradition development.

**Instances:**
- `as_1_14_calibration.md` §14.5 — full development with Tiberias/Babylonia codices, Uthmanic mushaf, Jerome Vulgate
- `as_1_15_aural.md` §15.5 — re-deployed in compressed form
- `as_3_02_encyclopaedic.md` §2.4 — re-deployed with extended Hebrew-Bible reductio scenario
- `as_2_01_epilogue.md` §1 — references "Hebrew, Quranic Arabic, ecclesiastical Latin"

**Pattern:** Ch 14 §14.5 is the canonical home. Ch 15 §15.5 references appropriately. App 2 §2.4 re-deploys with the structural reductio (imagine the OED applied to the Hebrew Bible) — load-bearing for App 2's argument about double standards.

**Recommendation:** COMPRESS. App 2 §2.4 keeps its reductio (it's the local argument-spine) but compresses the three-tradition restatement to one sentence pointing to Ch 14 §14.5 for the institutional histories.

**Word-count impact:** ~150 words

---

### Finding 38 — COMPRESS

**Repeated content:** Six-layer calibration matrix per-layer prose (Vedas / Prātiśākhya / Vyākaraṇam / Dhātupāṭha / Varṇamālā / Chandas).

**Instances:**
- `as_1_14_calibration.md` §14.3 — full per-layer development
- `as_1_17_wrong_question.md` §17.1 — the architectural-test six-requirement enumeration recapitulates substantial parts
- `as_3_07_codification_story.md` §7.11 — names the six in a compressed form

**Pattern:** Ch 14 §14.3 is canonical. Ch 17 §17.1's architectural-test enumeration is functionally different (it's the test framework, not a re-development of the matrix). App 7 §7.11 references appropriately.

**Recommendation:** KEEP. Functional distinctions hold. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 39 — POINTER

**Repeated content:** Brāhmī-as-*varṇamālā*-made-visible argument with the "encoding system could not be borrowed from a source that does not have it" hammer.

**Instances:**
- `as_1_13_preservation.md` §13.3 — full development
- `as_3_03_audiography.md` §3.4 — full development (verbatim or near-verbatim)
- `as_2_01_epilogue.md` §1 The Brāhmī thesis — restated

**Pattern:** Ch 13 §13.3 introduces the argument; App 3 §3.4 develops it in the appendix that's dedicated to the script case. The two carry substantial overlap. Per the audit convention that appendix is the reference-grade home, App 3 §3.4 should be the full development and Ch 13 §13.3 should be the body-grade summary. Currently Ch 13 §13.3 is also full-grade.

**Recommendation:** COMPRESS Ch 13 §13.3 — keep the heroic-erasure structural argument (the four-case pattern), compress the Brāhmī-architecture-vs-Aramaic technical demonstration to a pointer to App 3. The "encoding system could not be borrowed" hammer stays in App 3 §3.4 (where it's the section's spine).

**Word-count impact:** ~280 words

---

### Finding 40 — COMPRESS

**Repeated content:** Photography / audiography parallel — Herschel 1839 / Niépce / Daguerre / Talbot vs sonomer engineering.

**Instances:**
- `as_3_03_audiography.md` §3.6 — full development

**Pattern:** Single deployment. No repetition. Strong original argument.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 41 — POINTER

**Repeated content:** Hangul (Sejong 1443) as the foundational-orthodoxy control case — Sampson 1985 *featural* coinage, UNESCO Sejong Prize, ~80M users.

**Instances:**
- `as_3_03_audiography.md` §3.7 — full development
- `as_2_01_epilogue.md` §3 The Exhibits — restated with 80M Hangul / 1.5B audiographic-family numbers

**Pattern:** App 3 §3.7 is the canonical home with the full prosecution. Epilogue §3 re-deploys the user-count statistics and the Sejong 1443 anchor.

**Recommendation:** POINTER. Epilogue §3 compresses the Hangul restatement: name Sejong 1443 + featural-category coinage + ~1.5B audiographic-family + 80M Hangul, point to App 3 §3.7 for the prosecution. Saves the restatement of the asymmetry-with-Brāhmī argument.

**Word-count impact:** ~150 words

---

### Finding 42 — COMPRESS

**Repeated content:** *Atomic Corollary* full enumeration — *dhātuḥ* is the unit of stable identity holding structure through bonding...

**Instances:**
- `as_1_10_building_dhatuh.md` §10.15 — full statement + four-clause exposition

**Pattern:** Single deployment in the chapter that introduces it. No repetition.

**Recommendation:** KEEP. (Bookkeeping. Note: this is one of the named principles the book introduces; the §10.15 deployment is the canonical home.)

**Word-count impact:** no cut.

---

### Finding 43 — CUT

**Repeated content:** Reactivity-tier table (polyvalent / bivalent / monovalent — kṛ/bhū/sthā/gam/jñā/dā/dhā/nī/hṛ canonical nine).

**Instances:**
- `as_1_11_building_kriya.md` §11.6 — full development with the tier table
- `as_1_11_building_kriya.md` §11.7 — Hyper-Reactive Atoms section restates the carbon-class metaphor and the canonical nine
- `as_1_11_building_kriya.md` §11.9 — restated as "9/9 present in every sub-corpus"
- `as_3_05_by_the_numbers.md` §5.13 — same canonical nine restated in Path A productivity table

**Pattern:** Within Ch 11, the canonical nine recur three times in three adjacent sections. The §11.7 hyper-reactive section is essentially a restatement of §11.6's polyvalent-tier finding. App 5 §5.13 develops the same productivity argument with the same nine.

**Recommendation:** COMPRESS within Ch 11. §11.6 keeps the full tier-table development. §11.7 compresses to one paragraph naming *kṛ* as the cleanest case and pointing back to §11.6 (drop the restatement of the carbon-class metaphor and the nine-name re-enumeration). §11.9 keeps (it's the cross-corpus invariance argument — distinct claim).

**Word-count impact:** ~180 words

---

### Finding 44 — POINTER

**Repeated content:** *Kṛ* as flagship atom — combination derivatives table (*karma, kartṛ, kārya, saṃskāra, prakṛti, saṃskṛti, vikṛti*).

**Instances:**
- `as_1_10_building_dhatuh.md` §10.10 *sāravat* test — table of *kṛ* and four other dhātus
- `as_1_10_building_dhatuh.md` §10.11 *viśvatomukham* test — *kṛ* derivative list
- `as_1_10_building_dhatuh.md` §10.12 *anavadyam* test — *kṛ* example again
- `as_1_10_building_dhatuh.md` §10.15 — *kṛ* derivative list in the Atomic Corollary
- `as_1_12_building_vakya.md` §12.3 — *kṛ* chapter-flagship table
- `as_1_12_building_vakya.md` §12.4 — head-bonds redirecting *kṛ*
- `as_1_12_building_vakya.md` §12.5 — tail-bonds stabilizing molecule
- `as_1_12_building_vakya.md` §12.6 — *kṛ* bonding matrix

**Pattern:** Within Ch 10, the *kṛ* derivative list appears in four consecutive sections (§10.10, §10.11, §10.12, §10.15). Within Ch 12, *kṛ* is the chapter's flagship and rightly carries multiple deployments — but the four Ch 10 deployments in immediate sequence are dense.

**Recommendation:** COMPRESS Ch 10. §10.10 keeps the full *kṛ* row in its table (canonical *sāravat* test). §10.11 *viśvatomukham* test can use *kṛ* as one example without re-listing the eight derivatives (compress to "*kṛ* appears as action in *karoti*, deed in *karma*, agent in *kartṛ*, and through six more *upasarga*-bonded forms"). §10.12 *anavadyam* test compresses similarly. §10.15 Atomic Corollary keeps full deployment (corollary statement). Ch 12 is fine — it's the chapter's flagship.

**Word-count impact:** ~200 words

---

### Finding 45 — POINTER

**Repeated content:** *vaicitrya* (engineered range) explanation as the principle behind the long-tail of scaffolds.

**Instances:**
- `as_1_10_building_dhatuh.md` §10.8 — establishes
- `as_1_14_calibration.md` §14.4 — re-deploys at morphological level
- `as_3_05_by_the_numbers.md` §5.10 — develops empirically
- `as_3_06_vedic_carrier.md` references

**Pattern:** Ch 10 §10.8 establishes. Ch 14 §14.4 applies at morphological scale (the chandas/bhāṣā mode-difference). App 5 §5.10 develops as the empirical Path A finding. All three deployments are functionally distinct. Density is acceptable.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 46 — COMPRESS

**Repeated content:** "*Chandas* makes phonetic drift register as metrical mismatch. *Śruti* makes perceptual drift audible..." — the anti-entropy mechanism description.

**Instances:**
- `as_1_05_apabhramsa.md` §5.5 — establishes
- `as_1_14_calibration.md` §14.3 — develops Chandas-as-cryptographic-hash
- `as_1_15_aural.md` §15.3 — Combinatorial re-encoding develops the pāṭha mechanism
- `as_3_06_vedic_carrier.md` §6.7 — restates the principle

**Pattern:** Ch 5 §5.5 introduces. Ch 14 §14.3 develops at full layer-by-layer. Ch 15 §15.3 develops at pāṭha mechanism. App 6 §6.7 restates as the appendix close.

**Recommendation:** COMPRESS App 6 §6.7 restatement. The principle is established in Ch 5, developed in Ch 14 §14.3, operationalized in Ch 15 §15.3. App 6 §6.7's restatement runs ~120 words; can compress to ~50 by pointing to Ch 5 / Ch 14 / Ch 15.

**Word-count impact:** ~70 words

---

### Finding 47 — KEEP

**Repeated content:** Standing two-axes phrase set — *vaidika / laukika are domains; chandas / bhāṣā are modes*.

**Instances:** Preface §Domains and Modes; Ch 1 §1.1 Move 7; Ch 5 §5.6; Ch 14 §14.4; Ch 16 §16.4; App 6 throughout; App 7 §7.2, §7.6.

**Pattern:** Locked phrase per CLAUDE.md. Each deployment lands the two-axes correction in a different argumentative context.

**Recommendation:** KEEP. Canonical refrain.

**Word-count impact:** no cut.

---

### Finding 48 — POINTER

**Repeated content:** Wilson/Griffith mistranslation of Rigveda 9.63.5 (*viśvam āryam* omitted, *arāvṇaḥ* mistranslated) + Jamison-Brereton 2014 vindication.

**Instances:**
- `as_1_03_fourth_abrahamic.md` §3.4 — full development
- `as_2_01_epilogue.md` §5 — referenced with Ch 3 §3.4 cross-reference

**Pattern:** Single primary deployment with Epilogue pointer. Works as-is.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 49 — COMPRESS

**Repeated content:** *Kālacakra* vs linear progress — the wheel-of-time-vs-linear-time contrast.

**Instances:**
- `as_0_01_preface.md` line 55 — establishes
- `as_1_02_strategic.md` §2.4 — full development with FIGURE 2.1
- `as_3_02_encyclopaedic.md` §2.1, §2.3 — references
- `as_2_01_epilogue.md` §4 — references (kālacakra not linear ladder)

**Pattern:** Preface and Ch 2 §2.4 establish in full. App 2 and Epilogue reference appropriately. Current treatment fine.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 50 — CUT

**Repeated content:** Three-apex nexus opener — church + businessmen + politicians + the conversion-extraction frame.

**Instances:**
- `as_3_01_baking.md` §1.1 — full development with Catholic/Islamic precedent, juggernaut etymology, 1857
- `as_3_02_encyclopaedic.md` opening + §2.1 — restated as three-apex shifting form (Anglican church → church of progress; Company → publishing economy; Westminster → postcolonial Indian state)

**Pattern:** App 1 §1.1 establishes the three-apex nexus opener (~280 words). App 2 opener restates the same three-apex structure shifting form post-independence (~200 words). The structural-continuation point is App 2's load-bearing argument; the three-apex framing is App 1's. App 2 doesn't need to restate the framework — it can deploy it directly without the ground-up restatement.

**Recommendation:** COMPRESS App 2 opener. Drop the three-apex restatement enumeration. Use the existing structural cues: "Appendix Part 1 prosecuted the pre-independence operation. The political empire withdrew. The institutional machinery stayed." That's the load-bearing claim. Save the church/Company/politicians → church-of-progress/publishing/state mapping as one sentence pointing to App 1 §1.1.

**Word-count impact:** ~180 words

---

### Finding 51 — POINTER

**Repeated content:** The *Assalāyana Sutta* — Buddha observing that *ārya/dāsa* binary belongs to Yona/Kamboja borderlands.

**Instances:**
- `as_1_02_strategic.md` §2.2 — full deployment
- `as_1_03_fourth_abrahamic.md` §3.6 — re-deployed
- `as_1_16_retroflex.md` §16.5 — restated
- `as_2_01_epilogue.md` — references

**Pattern:** Three full deployments. Ch 2 §2.2 introduces; Ch 3 §3.6 redevelops; Ch 16 §16.5 re-uses for the English-failed-the-test argument.

**Recommendation:** COMPRESS. Ch 2 §2.2 is the canonical home. Ch 3 §3.6 points back ("the Assalāyana Sutta's foreign-bordering-nations diagnosis Ch 2 §2.2 develops"). Ch 16 §16.5 deploys functionally (English as *mleccha*); can also point back.

**Word-count impact:** ~180 words

---

### Finding 52 — COMPRESS

**Repeated content:** "The orthodoxy makes Pāṇini a rupture. The architecture makes him a witness." hammer.

**Instances:**
- `as_0_01_preface.md` §Domains and Modes — full deployment
- `as_1_01_botanical.md` §1.1 Move 7 — variant "The asuric apparatus makes Pāṇini a rupture..."
- `as_1_14_calibration.md` §14.6 — re-deployed at full
- `as_3_06_vedic_carrier.md` §6.7 — re-deployed at full
- `as_3_07_codification_story.md` §7.6, §7.18 — re-deployed

**Pattern:** Canonical two-beat hammer. Per CLAUDE.md, it's a locked phrase. Five deployments is within the canonical-refrain envelope, but density spikes in the late chapters (Ch 14 / App 6 / App 7 all use the full hammer within 30 pages).

**Recommendation:** KEEP. Within canonical-refrain bounds.

**Word-count impact:** no cut.

---

### Finding 53 — CUT

**Repeated content:** "Sanātan: correction by architecture. Pyramid: correction by authority." three-frame distinction (related to Finding 16/17 but in compressed sloganized form).

**Instances:** Variants appear in Ch 5 §5.4 (canonical); Ch 9 §9.11; Ch 13 §13.5; App 7 §7.4.

**Pattern:** Each instance is the compressed slogan-form of the three-frame distinction (Finding 17). KEEP for the canonical refrain pair as locked.

**Recommendation:** Combined with Finding 17 — no additional cut beyond what Finding 17 captures.

**Word-count impact:** rolled into Finding 17.

---

### Finding 54 — COMPRESS

**Repeated content:** Botanical-metaphor critique — *root* as the imported botanical organ for *dhātuḥ*.

**Instances:**
- `as_1_01_botanical.md` §1.5 — full development
- `as_1_06_dhatuh.md` §6.1, §6.5 — full re-development
- `as_1_18_pie_in_sky.md` §18.3 — restated ("the *dhātuḥ*-as-root mistranslation Chapter 1 named was not an accident...")
- `as_3_08_glossary.md` — references

**Pattern:** Ch 1 §1.5 establishes the polemic ("dhātuḥ is not a root"). Ch 6 is the chapter dedicated to recovering the term (justifies its own development). Ch 18 §18.3 re-runs the polemic in compressed form. The current treatment is mostly correct but Ch 18 §18.3's restatement runs ~120 words developing the same point Ch 6 already made.

**Recommendation:** COMPRESS Ch 18 §18.3. The chapter is about PIE prosecution; the *dhātuḥ*-as-root point can compress to one or two sentences pointing to Ch 6.

**Word-count impact:** ~100 words

---

### Finding 55 — POINTER

**Repeated content:** *Hlāfweard* → *laverd* → *lorde* → *Lord* worked example of natural English drift.

**Instances:**
- `as_1_01_botanical.md` §1.3 — full development
- `as_1_05_apabhramsa.md` §5.5 — restated for *apabhraṃśa* contrast
- `as_3_06_vedic_carrier.md` §6.6 — restated as natural-drift signature
- `as_3_07_codification_story.md` §7.9 — restated

**Pattern:** Ch 1 §1.3 introduces. Three subsequent re-deployments. The example is functionally useful but the *hlāfweard* etymology chain doesn't need to be re-walked each time.

**Recommendation:** COMPRESS. Ch 5 §5.5, App 6 §6.6, App 7 §7.9 each compress the worked-example detail to a phrase: "the *hlāfweard* → *Lord* drift Ch 1 §1.3 traces."

**Word-count impact:** ~180 words

---

### Finding 56 — COMPRESS

**Repeated content:** *Moron* / euphemism-treadmill worked example with Goddard 1910 + Rosa's Law 2010 + DSM-5 2013 timeline.

**Instances:**
- `as_1_05_apabhramsa.md` §5.7 — full development
- `as_3_06_vedic_carrier.md` §6.6 — restated as meaning-drift signature

**Pattern:** Ch 5 §5.7 is canonical. App 6 §6.6 re-uses to make the meaning-drift point.

**Recommendation:** COMPRESS App 6 §6.6 deployment. The Goddard 1910 / Rosa's Law / DSM-5 timeline can compress to "Goddard's *moron* (1910) traversed the euphemism treadmill into formal retirement by Rosa's Law (2010) and DSM-5 (2013) — Ch 5 §5.7 develops."

**Word-count impact:** ~100 words

---

### Finding 57 — KEEP

**Repeated content:** *Vyākaraṇam* etymology — *vi-* + *ā-* + *kṛ* — "unfolding apart" / decomposition not composition.

**Instances:** Ch 1 §1.6; Ch 4 §4.1; Ch 8 §8.6; App 7 throughout.

**Pattern:** Each deployment lands the etymology in a different argumentative context (botanical/codification critique in Ch 1; pre-Pāṇinian decoder lineage in Ch 4; sound-engineering decoding in Ch 8; codification story refutation in App 7). The decomposition-not-composition hammer is functionally load-bearing each time.

**Recommendation:** KEEP. Canonical engineering vocabulary establishment.

**Word-count impact:** no cut.

---

### Finding 58 — COMPRESS

**Repeated content:** *Pāṇini was second* / *Pāṇini decoded; he did not codify* hammer pair.

**Instances:**
- `as_1_01_botanical.md` §1.6 — establishes
- `as_1_04_siddha.md` §4.5 — develops with "Pāṇini documented a siddha system"
- `as_1_08_mapping_mouth.md` §8.6 *Pāṇini Was Second* section
- `as_1_11_building_kriya.md` §11.10 — re-deployed
- `as_1_14_calibration.md` §14.6 — re-deployed
- `as_1_17_wrong_question.md` §17.7 — re-deployed
- `as_3_07_codification_story.md` §7.18 — re-deployed
- Per prior audit R001 already flagged

**Pattern:** The locked refrain. Prior audit R001 marked KEEP at Preface/Ch1/Ch4/Ch11/App7 with POINTER elsewhere. Current deployment respects this — Ch 8 §8.6 carries the variant "Pāṇini was second"; the other deployments mostly land it as a closing hammer.

**Recommendation:** KEEP per prior R001. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 59 — COMPRESS

**Repeated content:** Auditure / Mnemoniture / Flexture / Scripture four-mode preservation taxonomy.

**Instances:**
- `as_1_13_preservation.md` §13.4 — names Auditure
- `as_1_14_calibration.md` §14.1 — full table with all four modes and their Indic counterparts
- `as_1_15_aural.md` opening — restated
- `as_3_03_audiography.md` §3.6 — Auditure paired with audiography

**Pattern:** Ch 14 §14.1 is the full home with the table. Ch 13 §13.4 names Auditure (correct setup). Ch 15 opening restates the four modes in a paragraph — adequate as it establishes the chapter's stake. App 3 §3.6 deploys Auditure functionally.

**Recommendation:** KEEP. Current pattern works. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 60 — COMPRESS

**Repeated content:** "Stone preserves the pyramid. It does not preserve the notebook." hammer.

**Instances:**
- `as_3_03_audiography.md` §3.5 — full development (~600 words on the archaeological-record argument)
- `as_2_01_epilogue.md` §1 — restated as a standalone hammer-line

**Pattern:** App 3 §3.5 is canonical (the chapter is about the script case). Epilogue §1 uses the hammer as a one-line pivot, which is the right deployment per the prior audit's note that this line is "lifted from Appendix Part 3 §3.3."

**Recommendation:** KEEP. Hammer is correctly attributed to its home. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 61 — CUT

**Repeated content:** The "engineered against entropy" anti-entropy claim — Sanskrit was built so neither growth nor decay would define it.

**Instances:**
- `as_1_01_botanical.md` §1.4, §1.7 — multiple deployments
- `as_1_05_apabhramsa.md` §5.5, §5.6, §5.7 — multiple deployments
- `as_1_13_preservation.md` §13.1 — restated
- `as_1_14_calibration.md` §14.6 — restated
- `as_3_06_vedic_carrier.md` §6.7 — restated
- `as_3_07_codification_story.md` §7.4, §7.8 — restated

**Pattern:** The anti-entropy claim is the engineering-thesis spine. It necessarily recurs. But the same formulation ("engineered against entropy" / "engineered against drift" / "anti-entropy architecture") appears with mild variation in 8-10 chapters.

**Recommendation:** KEEP the spine claim. COMPRESS deployments in App 6 §6.7 and App 7 §7.4, §7.8 (the appendix re-deployments) to pointers. The body chapters (Ch 1, 5, 13, 14) carry the load.

**Word-count impact:** ~150 words

---

### Finding 62 — COMPRESS

**Repeated content:** "Pratītsākhya texts document no analytical process" / "They made it up" — the Staal-rebuttal hammer.

**Instances:**
- `as_1_08_mapping_mouth.md` §8.6 — full development
- `as_1_14_calibration.md` §14.6 — restated as "centuries of analysis" fabrication

**Pattern:** Ch 8 §8.6 is canonical. Ch 14 §14.6 redeploys at matrix scale (a different scope — the *Prātiśākhya* and *Śikṣā* texts at the calibration matrix level). Acceptable.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 63 — COMPRESS

**Repeated content:** The "engineering implies engineers" diagnostic — including the explicit denial that the book hypothesizes a designing-agent class.

**Instances:**
- `as_0_01_preface.md` §The Engineering Claim — establishes
- `as_1_01_botanical.md` §1.6 — restated in the four-term-stack table
- `as_1_07_adivadya.md` (?) — implicit
- `as_1_17_wrong_question.md` §17.2 — "Engineering presupposes engineers. Specifications presuppose specifiers. Preservation architecture presupposes designers of the infrastructure."
- `as_endnotes.md` `apauruseya-mimamsa-sutra-1-1-5` — full

**Pattern:** The empirical-descriptive frame requires occasional restatement. Ch 17 §17.2's triplet ("Engineering presupposes engineers...") is the polemic-spine deployment that motivates the category-error argument. The CLAUDE.md banned-phrase rule (do not use "architects of Sanskrit" as a designing-agent framing) is anchored separately.

**Recommendation:** KEEP. Functional density. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 64 — POINTER

**Repeated content:** Ch 16 the English failed the test argument — Savarkar Ratnagiri internment + Samarth Ramdas *ovi* + mleccha + retroflex test.

**Instances:**
- `as_1_16_retroflex.md` §16.5 — full development (~750 words)

**Pattern:** Single deployment. Strong worked example. No repetition.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 65 — COMPRESS

**Repeated content:** Definition of *audiography* — engineered visual capture of articulated sound.

**Instances:**
- `as_1_08_mapping_mouth.md` §8.5 — establishes
- `as_1_13_preservation.md` §13.3 — restated (coined here for the appendix)
- `as_3_03_audiography.md` §3.1, §3.6 — full development
- `as_3_08_glossary.md` — full definition

**Pattern:** Multiple deployments establish the term progressively. App 3 §3.6 is the canonical home with the full Herschel/photography parallel. Earlier deployments (Ch 8 §8.5, Ch 13 §13.3) are establishment points and don't repeat the full apparatus.

**Recommendation:** KEEP. Progressive establishment is correct. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 66 — COMPRESS

**Repeated content:** The "*akṣara* means imperishable" + *a-* (privative) + √*kṣar* etymology.

**Instances:**
- `as_1_08_mapping_mouth.md` §8.5 — establishes with Gītā 8.3 reference
- `as_1_09_superset.md` §9.6 — restated
- `as_1_10_building_dhatuh.md` §10.4 — re-stated for the atomic context
- `as_1_10_building_dhatuh.md` §10.15 — re-stated in the Atomic Corollary
- `as_3_03_audiography.md` §3.6 — re-stated
- `as_3_08_glossary.md` — full

**Pattern:** Ch 8 §8.5 is canonical. The repeated re-glossing of the etymology in Ch 9, Ch 10 (twice), and App 3 is structural — each section needs to invoke *akṣara* as imperishable. But the *a-* + √*kṣar* breakdown is being delivered three or four times in body chapters.

**Recommendation:** COMPRESS. Ch 8 §8.5 keeps full etymology. Ch 9 §9.6 and Ch 10 §10.4 / §10.15 use *akṣara* without re-glossing (the term is established). App 3 §3.6 keeps (it's the section about audiography). Saves the imperishable-etymology re-development.

**Word-count impact:** ~120 words

---

### Finding 67 — KEEP

**Repeated content:** "The architecture is fractal." — scale-recurring architecture claim.

**Instances:** Across Preface, Ch 0, Ch 10 §10.16 (canonical), Ch 14, Ch 19, Epilogue, glossary.

**Pattern:** Per prior audit R007 — KEEP exact hammer at Ch 10 close, vary other deployments. Current treatment is acceptable.

**Recommendation:** KEEP per prior R007.

**Word-count impact:** no cut.

---

### Finding 68 — COMPRESS

**Repeated content:** The "engineered visual capture of articulated sound" exact phrase for *audiograph*.

**Instances:** Prior audit M012 flagged: Ch 8; Ch 13; Epilogue; glossary.

**Pattern:** Already addressed.

**Recommendation:** KEEP per prior M012.

**Word-count impact:** no cut.

---

### Finding 69 — COMPRESS

**Repeated content:** Sanskrit's reach via 5.2 billion / subcontinental + Indo-Iranian + Buddhist-Asian populations.

**Instances:**
- `as_1_00_seekers.md` §0.3 — full development with the three populations + Pratibimba framing
- `as_2_01_epilogue.md` §5 — restated as "to India, Pakistan, Bangladesh, Nepal, Sri Lanka..." with full country list

**Pattern:** Ch 0 §0.3 is the canonical home with the *Pratibimba* framing. Epilogue §5 re-deploys the country lists (subcontinent + Indo-European + Buddhist Asian — virtually the same enumeration).

**Recommendation:** COMPRESS Epilogue §5 country list. Drop the explicit subcontinent / Indo-Iranian / Buddhist Asian breakdown; replace with "the field Sanskrit touched — the subcontinent, the Indo-Iranian and Indo-European world, the Buddhist Asian world Ch 0 §0.3 maps."

**Word-count impact:** ~100 words

---

### Finding 70 — POINTER

**Repeated content:** Sanskrit's *Aṣṭādhyāyī* sūtra-count (~4000) + Sanskrit's *Dhātupāṭha* count (~2,000 / 2,168).

**Instances:** Distributed across Preface; Ch 0 §0.8; Ch 4 §4.2; Ch 6 §6.3; Ch 10 §10.3; Ch 11 §11.1; App 5 §5.1; App 6; App 7; Epilogue §1.

**Pattern:** The counts are functionally necessary in many places. The phrasing varies enough that no specific cut helps.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 71 — COMPRESS

**Repeated content:** The *dhātuḥ* atom-vs-root distinction.

**Instances:** Per prior audit R004 already flagged: Ch 1 §1.5; Ch 6; Ch 10; Ch 11; Ch 12; Ch 18; App 1/App 5; glossary.

**Pattern:** Per prior R004, KEEP refrain, COMPRESS botanical-explanation after Ch 6.

**Recommendation:** KEEP per prior R004. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 72 — COMPRESS

**Repeated content:** Ch 11 §11.6 + §11.8 + §11.9 internal repetition — the carbon-class metaphor + canonical nine + cross-corpus invariance.

**Instances:** Ch 11 §11.6 (full reactivity tier development), §11.7 (Hyper-Reactive Atoms restating polyvalent core), §11.9 (Stability Across Use restating canonical nine cross-corpus).

**Pattern:** Three adjacent sections all develop the polyvalent / carbon-class / canonical-nine claim from different angles. §11.7 in particular re-treads §11.6 material.

**Recommendation:** Combined with Finding 43. COMPRESS §11.7 to one short paragraph + pointer to §11.6.

**Word-count impact:** rolled into Finding 43.

---

### Finding 73 — POINTER

**Repeated content:** Tabla-as-extension-of-tongue / mouth-as-original-instrument.

**Instances:**
- `as_1_07_adivadya.md` §7.1, §7.3 — full development
- referenced elsewhere

**Pattern:** Single chapter home. Strong development. No repetition.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 74 — COMPRESS

**Repeated content:** Sanskrit *as* / Latin *esse* / Greek *eimi* — "natural languages concentrate use" + suppletive / irregular cores comparison.

**Instances:**
- `as_1_11_building_kriya.md` §11.6 — full development
- `as_3_05_by_the_numbers.md` §5.13 — restated as the "natural-language inversion"

**Pattern:** Ch 11 §11.6 is the polemic deployment (Sanskrit-vs-natural-language comparison table). App 5 §5.13 re-deploys empirically with Path A productivity data.

**Recommendation:** COMPRESS Ch 11 §11.6 comparison table to compressed text + pointer to App 5 §5.13 for empirical detail. Ch 11 keeps the polemic-grade hammer ("Similarity shows Sanskrit is usable speech. The persistent sonomeric procedure shows engineered speech.").

**Word-count impact:** ~120 words

---

### Finding 75 — COMPRESS

**Repeated content:** Word factory / language factory / generative engine — Sanskrit can generate words on demand.

**Instances:**
- `as_0_01_preface.md` §The Engineering Claim
- `as_1_00_seekers.md` §0.3, §0.8 — full Chandrayāna/Mangalyāna/Gaganyāna example
- `as_3_04_language_factory.md` §4.2 — references back as the chapter's starting point

**Pattern:** Ch 0 §0.8 is the canonical seed (the *Words Without Limit* section). App 4 §4.2 references appropriately.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 76 — COMPRESS

**Repeated content:** *Apauruṣeya* / *apauruṣeyatva* — Mīmāṃsā doctrine of Vedas as without-human-authorship.

**Instances:**
- `as_0_01_preface.md` §What This Book Claims
- `as_1_01_botanical.md` §1.4
- `as_1_03_fourth_abrahamic.md` §3.6
- `as_1_16_retroflex.md` §16.1
- `as_1_17_wrong_question.md` §17.5
- `as_3_06_vedic_carrier.md` §6.1 (load-bearing blockquote opener)
- `as_3_08_glossary.md`
- `as_endnotes.md`

**Pattern:** The term is structurally important and recurs naturally. The full Jaimini *Mīmāṃsā Sūtra* 1.1.5 citation appears in the endnote and glossary. Body chapters use the term without re-citing.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 77 — CUT

**Repeated content:** "The architecture is on the page and in the mouth" + variants.

**Instances:** Preface line 47, line 120; Ch 0 §0.5, §0.10, §0.12; Ch 7; Ch 13; Ch 15.

**Pattern:** A favored hammer-phrase. Density is acceptable individually but the variants accumulate. Prior audit didn't flag this as a separate item; treating it as a Tier-3 polish find.

**Recommendation:** KEEP. (Bookkeeping. Mild density flag.)

**Word-count impact:** no cut.

---

### Finding 78 — COMPRESS

**Repeated content:** "Pāṇini's act" two-column comparison table (codified vs decoded).

**Instances:**
- `as_1_17_wrong_question.md` §17.7 — full table (~7 rows)
- `as_3_07_codification_story.md` §7.16 — full table (~10 rows)

**Pattern:** Two full tables across two appendix-adjacent prosecutions. Ch 17 §17.7 carries the seven-row "Two Speculations" comparison; App 7 §7.16 carries the ten-row "Point-by-Point Response" comparison. Substantial overlap in claims but framed for different purposes (Ch 17 is the structural-axis comparison; App 7 is the catechismic response).

**Recommendation:** COMPRESS App 7 §7.16. The ten-row table can drop rows that duplicate Ch 17 §17.7 directly (4-5 rows), reducing to a focused 5-row catechism of points not already prosecuted at Ch 17.

**Word-count impact:** ~250 words

---

### Finding 79 — POINTER

**Repeated content:** The Greco-Indic-contact transmission for Wave 2 — Alexander / Mauryan-Seleucid / Greco-Bactrian / Indo-Greek / Aśoka edicts.

**Instances:**
- `as_1_19_life_after_pie.md` §19.2 — full development
- `as_endnotes.md` `dionysius-thrax-techne` — referenced

**Pattern:** Single primary deployment in Ch 19. Endnote carries the verification material. Correct treatment.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 80 — COMPRESS

**Repeated content:** Schleicher had-the-recipe / chose-to-bake-against-it polemic.

**Instances:**
- `as_1_03_fourth_abrahamic.md` §3.6 — full development
- `as_1_18_pie_in_sky.md` §18.1 — partial
- `as_3_04_language_factory.md` §4.8 — full re-development (~500 words)

**Pattern:** Ch 3 §3.6 establishes Schleicher as the named individual asuric operator. App 4 §4.8 re-develops the entire polemic to make App 4's polemic close. The two deployments substantially overlap.

**Recommendation:** COMPRESS App 4 §4.8. Keep the "language-factory contrast" framing (App 4's specific contribution: working recipe vs hollow bake). Cut the re-development of the Schleicher motive analysis, pointing to Ch 3 §3.6 + Ch 18 §18.1.

**Word-count impact:** ~280 words

---

### Finding 81 — POINTER

**Repeated content:** *Apaurusheya* + *śruti* / *dṛṣṭāḥ* honest-speculation triple (rationalist mind framing for Sanskrit's origin).

**Instances:**
- `as_0_01_preface.md` §What This Book Claims
- `as_1_17_wrong_question.md` §17.6 — full honest-speculation development
- `as_3_07_codification_story.md` §7.17 — re-deployed as "the replacement model"

**Pattern:** Ch 17 §17.6 is the canonical honest-speculation home. App 7 §7.17 re-deploys with the same content ("The seers saw. The lineage heard. The grammarians decoded. Pāṇini compressed. The Vedas remained the measure.").

**Recommendation:** POINTER. App 7 §7.17 compresses to a pointer + the four-line summary verse: "The Vedas are the primary calibration matrix. The pre-Pāṇinian disciplines decode. Pāṇini compresses. Living speech flows; Sanskrit stands as calibrant. Ch 17 §17.6 develops the full honest speculation."

**Word-count impact:** ~250 words

---

### Finding 82 — COMPRESS

**Repeated content:** The "Bandin / Aṣṭāvakra" + peer-review-as-pyramidal-gatekeeping polemic.

**Instances:**
- `as_1_03_fourth_abrahamic.md` §3.5 — full development

**Pattern:** Single deployment. Strong worked example. No repetition.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 83 — COMPRESS

**Repeated content:** *Ṛ* / *ra* bridge — the cross-inventory coupling at *mūrdhanya* site.

**Instances:**
- `as_1_10_building_dhatuh.md` §10.14 — full development
- `as_1_16_retroflex.md` §16.2 — full re-development
- `as_3_05_by_the_numbers.md` §5.6 — full empirical development

**Pattern:** Ch 10 §10.14 introduces (as the chapter close). Ch 16 §16.2 redeploys with the *kṛ*/*vṛ*/*dṛś* dhātu family list + position-role data. App 5 §5.6 develops the empirical case.

**Recommendation:** COMPRESS Ch 16 §16.2. The chapter's argument is the retroflex-is-architectural case; the *ṛ*/*ra* bridge is one of four pieces of evidence Ch 16 §16.2 deploys. Ch 16 can compress the *ṛ* development to ~200 words from current ~350, pointing to Ch 10 §10.14 + App 5 §5.6 for the technical detail.

**Word-count impact:** ~150 words

---

### Finding 84 — COMPRESS

**Repeated content:** The "47 scaffolds carrying 91% / top-10 carry the work" empirical signature.

**Instances:**
- `as_1_10_building_dhatuh.md` §10.8 — full development
- `as_1_11_building_kriya.md` §11.5 — restated
- `as_3_05_by_the_numbers.md` §§5.7-5.10 — full empirical development

**Pattern:** Ch 10 §10.8 establishes. Ch 11 §11.5 deploys functionally (in the racana-gana matrix). App 5 develops empirically. Current pattern works.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 85 — COMPRESS

**Repeated content:** The "*dṛṣṭāḥ* saw" / "*mantra-dṛṣṭāḥ* not *mantra-kartṛs*" formulation.

**Instances:**
- `as_0_01_preface.md` (twice — opening + What This Book Claims)
- `as_1_01_botanical.md` §1.6
- `as_1_17_wrong_question.md` §17.6
- `as_endnotes.md`
- `as_3_08_glossary.md`

**Pattern:** Per CLAUDE.md, this formulation is canonical — it's the *apauruṣeyatva* engineering-thesis pair. The Preface uses it twice (opening epigraph + §What This Book Claims). Subsequent body deployments are functional.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 86 — POINTER

**Repeated content:** Two-mode architecture for chandas / bhāṣā — Pāṇini marks *chandasi* / *bhāṣāyām* as rule-context locatives, not chronology markers.

**Instances:**
- Preface §Domains and Modes
- `as_1_01_botanical.md` §1.1 Move 7
- `as_1_05_apabhramsa.md` §5.6
- `as_1_14_calibration.md` §14.4
- `as_1_16_retroflex.md` §16.4
- `as_3_06_vedic_carrier.md` throughout
- `as_3_07_codification_story.md` §7.2, §7.6

**Pattern:** The two-modes argument is the spine of the chronology refusal. Per CLAUDE.md it's a locked refrain. Density across nine deployments is high but each carries functional weight.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 87 — COMPRESS

**Repeated content:** App 7 §7.10 same-timeline test — Sanskrit vs English across the orthodoxy's own calendar.

**Instances:**
- `as_3_07_codification_story.md` §7.10 — full ~1,200 word development

**Pattern:** Single deployment. The section walks 3 Vedic verses + 3 post-Pāṇinian Sanskrit examples + 3 English examples. Strong empirical demonstration but very long for the polemic point (which is already made in compressed form).

**Recommendation:** COMPRESS within section. The section can lose two of the three Sanskrit-side examples (keep one Vedic + one post-Pāṇinian) and two of the three English examples (keep *Beowulf* + Lord's Prayer; cut Chaucer middle-example). The trim preserves the empirical demonstration while saving ~400 words.

**Word-count impact:** ~400 words

---

### Finding 88 — CUT

**Repeated content:** "Word factory" → "Language factory" framing in App 4.

**Instances:**
- `as_3_04_language_factory.md` §4.2 — establishes (referencing Ch 10-12)
- `as_3_04_language_factory.md` §4.7 — restates as conclusion

**Pattern:** Internal-to-App-4 repetition. The §4.7 restatement of the language-factory claim is a verdict-close — functional but adds little.

**Recommendation:** COMPRESS §4.7 "What This Demonstrates" closing. The three numbered conclusions are mostly recapitulation; tightening saves ~150 words.

**Word-count impact:** ~150 words

---

### Finding 89 — KEEP

**Repeated content:** Saptaṛṣi roster with Devanagari pairings (Agastya / Kaśyapa / Bharadvāja / Bhṛgu / Aṅgiras).

**Instances:** Ch 19 §19.1 — single full deployment.

**Pattern:** Single deployment. Functional.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 90 — COMPRESS

**Repeated content:** *Mantra-dṛṣṭāḥ* etymology and *uto tvasmai tanvaṃ vi sasre* second-half-of-Vāk-epigraph explanation.

**Instances:**
- `as_0_01_preface.md` line 29 — full development with female ṛṣikāḥ list

**Pattern:** Single deployment.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 91 — POINTER

**Repeated content:** The four-Abrahamic-religions full enumeration (Judaism / Christianity / Islam / Progressivism) + the structural-template table.

**Instances:**
- `as_1_03_fourth_abrahamic.md` §3.1 — establishes with the FIGURE 3.1 placeholder
- `as_1_03_fourth_abrahamic.md` §3.3 — develops with the pyramid table
- `as_1_19_life_after_pie.md` §19.3 — cluster-term deployment
- `as_2_01_epilogue.md` — references
- `as_3_02_encyclopaedic.md` §2.1 — cluster-term deployment

**Pattern:** Ch 3 is the canonical home for the full Four Abrahamic Religions argument. Later chapters deploy the cluster term *fourth Abrahamic religion* without re-developing the four-religion analysis. Current pattern works.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 92 — COMPRESS

**Repeated content:** Three pillars argument — Aryan / Theological / Progress.

**Instances:**
- `as_1_02_strategic.md` §§2.2-2.5 — full development with FIGURE 2.2
- `as_1_03_fourth_abrahamic.md` §3.6 — restated pyramid-by-pillar mapping
- `as_1_18_pie_in_sky.md` §18.4 — restated

**Pattern:** Ch 2 is the canonical home. Ch 3 §3.6 re-deploys (mapping each pillar to a pyramid). Ch 18 §18.4 re-deploys (the progress pillar specifically). The three deployments are each load-bearing.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 93 — COMPRESS

**Repeated content:** Chapter-opening "Chapter X ended with Y. This chapter Z." formulation.

**Instances:** Ch 10 opening; Ch 11 opening; Ch 12 opening; Ch 13 §13.1; Ch 14 opening; Ch 15 opening; Ch 16 opening; Ch 17 opening; Ch 18 opening; Ch 19 opening.

**Pattern:** The setup-by-handoff opening is a structural convention. Each chapter opens by establishing the prior chapter's close. The convention is helpful but every opener carries 100-200 words of "Chapter N closed with..." material. Across 10 chapters, that's ~1,500 words of bridge prose.

**Recommendation:** COMPRESS by ~30% across all openers. Each chapter's "previously" paragraph can run as 1-2 sentences instead of a paragraph. Drop the explicit summary of the prior chapter's closing claim; trust the reader to recall.

**Word-count impact:** ~500 words

---

### Finding 94 — COMPRESS

**Repeated content:** "The architecture is fractal" enumerations — listing sonomer → akṣara → dhātuḥ → kriyāpada → śabda → vākya → sūtra → calibration matrix.

**Instances:** About Series; Preface; Ch 0; Ch 10 §10.16; Ch 14; Ch 18 §18.3; Ch 19 §19.4; glossary; multiple chapter closes.

**Pattern:** Per the user spec, scale-chain enumeration is intentional and KEEP. The enumeration appears 8-10 times. Density is within the canonical-architecture bounds.

**Recommendation:** KEEP per user spec. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 95 — POINTER

**Repeated content:** Patañjali *Mahābhāṣya* opening as anchor for *siddha* axiom.

**Instances:** Preface; Ch 4 §4.2 (canonical); Ch 18 §18.3; App 2 §2.3; App 7 §7.8.

**Pattern:** Ch 4 §4.2 is canonical. Other deployments reference appropriately.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 96 — COMPRESS

**Repeated content:** *Sat-asat-viveka* — discernment standard explanation.

**Instances:**
- `as_0_03_prologue.md` — establishes
- `as_2_01_epilogue.md` §2 The Contest of Architectures — restated with *yat bhūta-hitam atyantaṃ tat satyam* anchor
- `as_3_08_glossary.md`

**Pattern:** Prologue establishes. Epilogue §2 redeploys. The *bhūta-hitam* standard is the spine of both deployments. Each lands in a different framing context.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 97 — CUT

**Repeated content:** Brāhmī = the *varṇamālā* made visible — same-glyph encoding as Devanagari.

**Instances:**
- `as_1_08_mapping_mouth.md` §8.5 — references (forward-pointer to App 3)
- `as_1_13_preservation.md` §13.3 — full development with structural-identity argument
- `as_3_03_audiography.md` §3.4 — full development with same structural-identity argument

**Pattern:** The "Brāhmī encodes the same architecture as Devanāgarī, with different glyph shapes" claim appears in both Ch 13 §13.3 and App 3 §3.4. Both develop the *varga* matrix / *sthāna* / *prayatna* / vowel-diacritic / *ayogavāha* breakdown.

**Recommendation:** CUT one. App 3 §3.4 is the canonical home (the chapter is dedicated to script case). Ch 13 §13.3 compresses to two sentences naming the structural identity + pointer to App 3 §3.4 for the architecture breakdown.

**Word-count impact:** ~300 words

---

### Finding 98 — COMPRESS

**Repeated content:** Frequency / suppletion / English be-have-do irregular core comparison.

**Instances:**
- `as_1_11_building_kriya.md` §11.6 — comparison table
- `as_3_05_by_the_numbers.md` §5.13 — restated as "natural-language inversion"

**Pattern:** Combined with Finding 74.

**Recommendation:** Combined with Finding 74.

**Word-count impact:** rolled into Finding 74.

---

### Finding 99 — POINTER

**Repeated content:** Briggs 1985 *AI Magazine* / Subhash Kak / Frits Staal — prior approaches mentioned.

**Instances:**
- `as_0_01_preface.md` §Earlier Glimpses — full development
- `as_endnotes.md`

**Pattern:** Single body deployment with endnote backing. Correct.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 100 — COMPRESS

**Repeated content:** "*Apabhraṃśa* is the default trajectory of any linguistic form left in unprotected human use."

**Instances:**
- `as_1_05_apabhramsa.md` §5.3 — establishes
- `as_1_13_preservation.md` §13.1 — restated

**Pattern:** Two deployments. Ch 5 §5.3 introduces. Ch 13 §13.1 restates as the preservation chapter's setup.

**Recommendation:** COMPRESS Ch 13 §13.1 restatement to one sentence pointing back to Ch 5 §5.3.

**Word-count impact:** ~50 words

---

### Finding 101 — COMPRESS

**Repeated content:** "Stone preserves what authority wanted preserved" — the archaeological-record-is-pyramid-media argument.

**Instances:**
- `as_1_13_preservation.md` §13.3 — full development
- `as_3_03_audiography.md` §3.5 — full re-development

**Pattern:** The argument appears in both Ch 13 §13.3 (the writing-disqualified-for-Vedas argument) and App 3 §3.5 (the script-chronology argument). Both deployments develop the survival-archive-vs-invention-archive distinction.

**Recommendation:** COMPRESS Ch 13 §13.3. The chapter's argument is *lipi*-as-disqualified-medium for *sāṃskṛtika* content. The pyramid-media archaeology argument can compress to one paragraph pointing forward to App 3 §3.5 for the full Brāhmī-chronology development.

**Word-count impact:** ~250 words

---

### Finding 102 — COMPRESS

**Repeated content:** The "*Vedas* are not scripture / Vedas are calibration matrix" hammer.

**Instances:** Distributed across Ch 0 §0.5; Ch 13 §13.1, §13.3; Ch 14 throughout; Ch 17; App 7.

**Pattern:** Per prior audit X008, canonical refrain. Density is acceptable. Current pattern works.

**Recommendation:** KEEP per prior X008. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 103 — POINTER

**Repeated content:** *Yantra* / *dharma* / *brahman* semantic-extension examples — the "phonetic form preserved while meaning extends" argument.

**Instances:**
- `as_3_02_encyclopaedic.md` §2.5 — full development with all three terms + Devanagari pairings
- `as_3_06_vedic_carrier.md` §6.6 — restated as the "Sanskrit shows nothing of either pattern" hammer

**Pattern:** App 2 §2.5 is the canonical home (the chapter is about the dictionary project documenting variation). App 6 §6.6 restates as part of the natural-drift contrast.

**Recommendation:** POINTER. App 6 §6.6 keeps the *jaḍa / mūrkha / gauḥ* preserved-meaning examples (Ch 5 §5.6 source) but compresses the *yantra / dharma / brahman* restatement to a pointer to App 2 §2.5.

**Word-count impact:** ~120 words

---

### Finding 104 — ENDNOTE

**Repeated content:** Goddard 1910 *moron* timeline + Rosa's Law 2010 + DSM-5 2013 — the euphemism treadmill historical detail.

**Instances:** Per Finding 56 (Ch 5 §5.7 + App 6 §6.6).

**Pattern:** Combined with Finding 56.

**Recommendation:** Per Finding 56 — also worth considering ENDNOTE move. The Goddard / Rosa's Law / DSM-5 dating detail could move to an endnote, with the body running "the euphemism treadmill — *moron* across a century from neutral clinical term to retired slur."

**Word-count impact:** combined with Finding 56.

---

### Finding 105 — ENDNOTE

**Repeated content:** Boden Chair endowment details — Lieutenant Colonel Joseph Boden, Bombay Native Infantry, evangelical-purpose specifications.

**Instances:** `as_3_01_baking.md` §1.2 — single deployment.

**Pattern:** Single deployment. Reference-grade detail.

**Recommendation:** Consider ENDNOTE move for the more granular biographical detail (Lt Col / Bombay Native Infantry / will-specifying-evangelical-purpose). Keep one sentence in body: "the Boden Chair of Sanskrit at Oxford, endowed in 1832 to enable the conversion of Indians to Christianity (Lieutenant Colonel Joseph Boden's will; see endnote)." Saves ~80 words.

**Word-count impact:** ~80 words

---

### Finding 106 — ENDNOTE

**Repeated content:** Wheeler/Mohenjo-daro full historical detail — 1947 / Director General of ASI / 37 skeletons / 6 in HR area / "Indra stands accused" / Dales 1964 / Kenoyer / Possehl / Kennedy refutation.

**Instances:**
- `as_3_06_vedic_carrier.md` §6.4 — full ~400-word development

**Pattern:** Single deployment in the appendix.

**Recommendation:** ENDNOTE the full Wheeler-Mohenjo-daro companion (1947 article title; Director General role; skeleton counts; refutation authors). Keep one paragraph in body naming Wheeler's overreach as a structural parallel and pointing to the endnote.

**Word-count impact:** ~200 words

---

### Finding 107 — ENDNOTE

**Repeated content:** Full Mitanni companion — Suppiluliuma I / Shattiwaza treaty / Bogazköy archive / Kikkuli 184-day/1080-line/4-cuneiform-tablet treatise / numerical correspondences / throne names / *marya*.

**Instances:** `as_1_19_life_after_pie.md` §19.1 — full deployment.

**Pattern:** Single deployment in the chapter.

**Recommendation:** Consider ENDNOTE move of the deepest reference-grade detail. Body keeps: treaty deities (Mitra/Varuṇa/Indra/Nāsatya), Kikkuli reference, the key numerical correspondences (*aika* as pre-Vedic-Sanskritic), one throne name (Tushratta), *marya*. Endnote carries: Suppiluliuma/Shattiwaza names, Bogazköy archive, 184-day/1080-line/4-tablet specifics, full numerical list, full throne-name list. Saves ~300 words from body.

**Word-count impact:** ~300 words

---

### Finding 108 — ENDNOTE

**Repeated content:** Detailed Bopp/Pott/Schleicher/Brugmann biographical timeline in App 1 §1.4.

**Instances:** `as_3_01_baking.md` §1.4 — full development.

**Pattern:** Single deployment but with extensive dates and publication-title detail.

**Recommendation:** Consider ENDNOTE move of publication titles in full (e.g., *Vergleichende Grammatik der Sanskrit-, Send-, Armenischen-, Griechischen-, Lateinischen-, Litauischen-, Altslavischen-, Gothischen- und Deutschen*) and birth-death dates. Body keeps the structural timeline (Bopp 1816 / Pott 1830s / Schleicher 1860s / Brugmann 1880s) and the institutional placements. Saves ~200 words.

**Word-count impact:** ~200 words

---

### Finding 109 — POINTER

**Repeated content:** *Atomic Sanskrit* as a Wave 3 instrument framing.

**Instances:**
- `as_1_19_life_after_pie.md` §19.4 — establishes
- `as_2_01_epilogue.md` §8 The Mantra — restated

**Pattern:** Ch 19 §19.4 establishes. Epilogue restates as part of the inward-correction call.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 110 — PROMOTE

**Repeated content:** "Codification is standardization by authority. Calibration is standardization by architecture." — needs a named-principle anchor.

**Instances:** Per Findings 16, 17, 53.

**Pattern:** Recurring spine claim. Currently distributed across Ch 5, Ch 13, App 7 with mild variation.

**Recommendation:** PROMOTE to a named principle (e.g., the *Calibration Principle*) with a single canonical statement in Ch 5 §5.4 + glossary entry. Subsequent deployments reference the principle by name rather than re-developing the contrast. Saves repetition + sharpens polemic.

**Word-count impact:** ~100 words (modest body savings; main value is conceptual sharpening).

---

### Finding 111 — POINTER

**Repeated content:** "Calibrant" definition + role.

**Instances:**
- `as_1_05_apabhramsa.md` §5.7 — establishes The Calibrant Envelope
- `as_1_14_calibration.md` — implicit in matrix development
- `as_1_18_pie_in_sky.md` §18.6 — "calibrant contact"
- `as_3_08_glossary.md`

**Pattern:** Ch 5 §5.7 establishes. Ch 18 §18.6 extends to "calibrant contact" (new specific use). Glossary anchors.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 112 — COMPRESS

**Repeated content:** The *gauḥ* worked example walked through *gāvī / goṇī / gotā / gopotalikā* with FIGURE 5.1.

**Instances:** Ch 5 §5.3 (canonical home); Ch 13 §13.1 + App 2 §2.5 + App 7 §7.8 restatements per Finding 13.

**Pattern:** Combined with Finding 13.

**Recommendation:** Per Finding 13.

**Word-count impact:** rolled into Finding 13.

---

### Finding 113 — COMPRESS

**Repeated content:** Description of corpus inventory (Vedas / Vedāṅgas / Itihāsa / Purāṇa / Kāvya / Āyurveda / Nyāya / Sāṃkhya / etc.) per the Ch 0 §0.5 enumeration.

**Instances:**
- `as_1_00_seekers.md` §0.5 — full enumeration with Devanagari pairings (~400 words)

**Pattern:** Single deployment. Functions as a reader-orientation reference.

**Recommendation:** COMPRESS. The Ch 0 §0.5 corpus inventory is useful but exhaustive. Consider trimming the per-discipline gloss to bare names with Devanagari, dropping the per-discipline explanation paragraph for *Dharmaśāstra/Kāvya* and *Cross-domain scientific disciplines*. Saves ~150 words while preserving the orientation function.

**Word-count impact:** ~150 words

---

### Finding 114 — COMPRESS

**Repeated content:** The "place-value system, śūnya, ten digits span all of arithmetic" deployment as the math-parallel-to-language-engine analogy.

**Instances:**
- `as_1_00_seekers.md` §0.1, §0.9 — full development (~600 words across the two sections)
- `as_3_03_audiography.md` §3.6 — restated as the place-value-system precedent for the sonomer
- `as_2_01_epilogue.md` §3 — references

**Pattern:** Ch 0 §0.9 is canonical. App 3 §3.6 re-deploys as the *kaplan-zero-erasure* parallel. The two deployments are both functional but the App 3 use can compress.

**Recommendation:** COMPRESS App 3 §3.6 deployment. The Kaplan-zero parallel can run in 2-3 sentences pointing to Ch 0 §0.9 instead of redeveloping the Indic-origin / Arabic-transmission / Mesopotamian-displacement narrative.

**Word-count impact:** ~120 words

---

### Finding 115 — POINTER

**Repeated content:** Ten *gaṇāḥ* full table with vikaraṇa signatures.

**Instances:**
- `as_1_11_building_kriya.md` §11.4 — full development with the 10-row table

**Pattern:** Single deployment.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 116 — COMPRESS

**Repeated content:** The "Sanskrit is the calibrant for the science of grammar globally" verdict for Wave 2.

**Instances:**
- `as_1_19_life_after_pie.md` §19.2 close
- `as_2_01_epilogue.md` §1 — references

**Pattern:** Ch 19 §19.2 close lands as the verdict. Epilogue references in compressed form. Current pattern works.

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 117 — KEEP

**Repeated content:** *Ārya* / *āryatva* — discipline-not-race definition.

**Instances:** Per prior audit X011 — Ch 0 §0.3; Ch 3 §3.4; Ch 16 §16.5-16.6; Ch 19 §19.4; Epilogue.

**Pattern:** Per prior X011, clean arc from word to conduct to invitation. KEEP.

**Recommendation:** KEEP per prior X011.

**Word-count impact:** no cut.

---

### Finding 118 — COMPRESS

**Repeated content:** "Make the world ārya" / *kṛṇvanto viśvam āryam* mantra deployment.

**Instances:**
- `as_1_03_fourth_abrahamic.md` §3.4 — Wilson/Griffith mistranslation context
- `as_1_16_retroflex.md` §16.6 — first deployment of the Rigvedic call
- `as_1_19_life_after_pie.md` §19.3 — second deployment
- `as_2_01_epilogue.md` §§5, 8 — full mantra deployment (twice)

**Pattern:** Each deployment lands in a different argumentative context. Per CLAUDE.md, this is the book's closing call. Epilogue carries two full deployments by design (§5 The Invitation + §8 The Mantra close).

**Recommendation:** KEEP. (Bookkeeping. The Epilogue double-deployment is the canonical convention for the mantra-landing structure.)

**Word-count impact:** no cut.

---

### Finding 119 — COMPRESS

**Repeated content:** *Asuratva* establishment + the asuric pyramid as the formation diagnostic.

**Instances:** Per CLAUDE.md cluster-vocabulary convention — Ch 3 §3.6 establishes; subsequent deployments reference the established cluster.

**Pattern:** Current deployments work per the convention. (Bookkeeping.)

**Recommendation:** KEEP. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 120 — COMPRESS

**Repeated content:** "*Apaurusheya* is the paramparā's own anchor" — the Mīmāṃsā doctrine of apaurusheyatva as the engineering thesis's empirical face.

**Instances:**
- `as_0_01_preface.md` line 47 — establishes
- `as_1_01_botanical.md` §1.6 — restated in the four-term-stack
- `as_1_17_wrong_question.md` §17.6 — restated in honest speculation
- `as_3_08_glossary.md`
- `as_endnotes.md`

**Pattern:** Distributed deployment. Functional.

**Recommendation:** KEEP per Finding 76. (Bookkeeping.)

**Word-count impact:** no cut.

---

### Finding 121 — COMPRESS

**Repeated content:** Tabular comparison tables of orthodox-account vs engineering-thesis claims.

**Instances:**
- `as_1_17_wrong_question.md` §17.7 — 7-row two-speculation comparison
- `as_3_07_codification_story.md` §7.16 — 10-row point-by-point response

**Pattern:** Combined with Finding 78.

**Recommendation:** Per Finding 78.

**Word-count impact:** rolled into Finding 78.

---

### Finding 122 — POINTER

**Repeated content:** App 5 §5.13 "natural-language inversion" extended argument.

**Instances:**
- `as_3_05_by_the_numbers.md` §5.13 — full development
- `as_1_11_building_kriya.md` §11.6 — initial polemic deployment

**Pattern:** Combined with Findings 74, 98.

**Recommendation:** Per Finding 74.

**Word-count impact:** rolled into Finding 74.

---

### Finding 123 — PROMOTE

**Repeated content:** The "*Pratibimba*" frame — its place in the broader engineering thesis.

**Instances:** Per Finding 7.

**Pattern:** Already a named principle (capitalized). Could be promoted into a named-principle status visible in TOC / running heads (currently it appears as a key term but isn't surfaced as a named architectural principle equivalent to *Atomic Corollary* or *Fractal Corollary*).

**Recommendation:** PROMOTE to *Pratibimba Principle* or similar named principle with a single one-sentence canonical statement. Subsequent deployments can use the principle name. Conceptual savings + reduces some restatement of what *Pratibimba* names.

**Word-count impact:** ~50 words (small body savings; main value is conceptual).

---

### Finding 124 — PROMOTE

**Repeated content:** The "engineering presupposes engineers" diagnostic triplet from Ch 17 §17.2.

**Instances:**
- `as_1_17_wrong_question.md` §17.2 — full deployment
- `as_0_01_preface.md` — implicit
- Other chapters carry the implicit logic

**Pattern:** The triplet is a strong specific deployment. Could be promoted to a named-principle (e.g., the *Implication Triplet* or similar) and referenced rather than re-stated.

**Recommendation:** PROMOTE — relatively low impact. Single named deployment with subsequent references. Mainly a sharpening move rather than a cut.

**Word-count impact:** ~50 words.

---

### Finding 125 — COMPRESS

**Repeated content:** Cross-chapter "see Appendix Part X" pointers — overall the appendix system is sometimes referenced multiple times for the same forward direction.

**Instances:** Distributed.

**Pattern:** Many sections close with cross-references to Appendix Parts 1-7. Some chapters cross-reference the same appendix multiple times (e.g., App 1 is referenced in Ch 1, Ch 3, Ch 17, Ch 18, and the Epilogue).

**Recommendation:** COMPRESS. Audit pass to consolidate cross-reference apparatus — one canonical "for the full prosecution see App X" deployment per chapter rather than per section. Small savings (~100 words across the manuscript) but improves reader experience.

**Word-count impact:** ~100 words.

---

## Closing observations for the user

**Pattern 1 — Body / appendix re-prosecution is the largest cut lever.** Appendix Parts 1, 2, 3, 6, 7 each re-run material the body chapters already developed. The reference-grade frame justifies *some* re-development (the appendix carries verification material the body footnotes-out), but the current structure has multiple appendix sections doing full polemic re-runs rather than evidence accounts. Appendix 7 (Codification Story Refuted) is the most extreme — ~7,500 words of which 2,500-3,000 could compress to body pointers without losing the appendix's load-bearing case.

**Pattern 2 — Ch 11 has unusually dense internal repetition.** Three adjacent sections (§11.6, §11.7, §11.9) re-tread the polyvalent / carbon-class / canonical-nine ground. The chapter would benefit from internal consolidation.

**Pattern 3 — Devanagari first-use re-glossing is happening across many chapters even after the term is established.** The CLAUDE.md convention is first-use Devanagari pairing per chapter; many terms (*vyākaraṇam*, *Aṣṭādhyāyī*, *Dhātupāṭha*, *Prātiśākhya*, *Śikṣā*, *Chandas*) are re-paired in nearly every chapter. Audit pass could trim ~300-500 words by enforcing strict first-use-per-volume rather than first-use-per-chapter for the most established terms.

**Pattern 4 — Locked refrains are well-managed.** The standing polemic phrase, the two-axes hammer, and the *Pyramid: correction by authority / Sanātan: correction by architecture* hammer are deployed with appropriate density. The prior audit's Pass 4 + 5 batches did the work.

**Pattern 5 — Cross-chapter pointers ARE doing the forwarding work CLAUDE.md asks for** in most cases. The "Chapter X §X.Y develops in detail" convention is in active use. Some pointers are bidirectional (Ch 10 references Ch 11 + 12 + 13 + App 5; App 5 references back) and these chains help readers navigate but they also add cumulative word count.

**Pattern 6 — Repetition cuts alone cannot reach the 49k-word target.** Best-case cuts from this audit ≈ 16k-20k words. The remaining 30k will need scope decisions (cutting whole sections, dropping examples, condensing whole arguments, moving substantial companion material to endnotes or appendix-only treatment). The user should expect to make scope cuts separately.

**Pattern 7 — Some "compress" recommendations should be deferred** until the user has made scope decisions. If Appendix 7 is going to remain as a full re-prosecution chapter, the App 7 → Ch 4/Ch 5/Ch 14 pointer compression doesn't make sense (it weakens App 7's structural integrity). If App 7 is going to compress dramatically or merge with Ch 17, the pointer compression should follow that decision.
