# Working Plan — RV 10.71.2 as the Book's Keystone

**Date:** 2026-06-09  
**Last updated:** 2026-06-10
**Author:** Parag Tope (find) + drafting collaboration  
**Status:** Preface pointer, Ch4 callback, Ch8/12/17/18 bridges, Ch9 epigraph, sieve figure, §9.1 reveal, Ch9 close, Ch10 callback, Ch14/15 radiance callback, Epilogue return, Vāk blessing, expanded endnote, and local DCS / Griffith / public Sanskrit-text source spot-check are implemented. Remaining work: selected printed-edition verification.

---

## 1. The Find

**Ṛgveda 10.71.2** — Bṛhaspati's hymn on Speech:

> सक्तुमिव तितउना पुनन्तो यत्र धीरा मनसा वाचमक्रत ।
> अत्रा सखायः सख्यानि जानते भद्रैषां लक्ष्मीर्निहिताधि वाचि ॥
>
> *saktum iva titaunā punanto yatra dhīrā manasā vācam akrata*  
> *atrā sakhāyaḥ sakhyāni jānate bhadraiṣāṃ lakṣmīr nihitādhi vāci*

**Text note:** The working saṃhitā form standardizes `तितउना`, not `तित्उना`, to match the current manuscript epigraph. Local DCS records the Roman form as *titaunā* and separates the final pāda as *bhadrā eṣām lakṣmīḥ nihitā adhi vāci*. A public unaccented Sanskrit text spot-check prints the difficult word as `तित-उना` / *tita-unā*, which supports keeping the working separation for now rather than silently changing it to `तितौना`. Final publication should still verify the saṃhitā text, accenting, and Devanagari orthography against the selected printed Ṛgveda edition.

## 2. What the Verse Can Carry

The verse names an operation. It does not need to be forced into modern terminology. Its own sequence is enough:

| Verse element | Sanskrit | Book-architectural correspondence |
|---|---|---|
| Larger field | ***saktum*** — grain / meal before refinement | The abundant sound-field Chapter 8 surveys. |
| Selection instrument | ***titaunā*** — by a sieve | The act of selection: field becomes inventory. |
| Refined result | ***punantaḥ*** — purifying, sifting, refining | The curated *varṇamālā*: chosen sonomers, not accumulated noise. |
| Intelligent agents | ***dhīrā manasā*** — the wise, with mind | Anonymous plural intelligence; architects visible through the work. |
| Making act | ***vācam akrata*** — they formed Speech | The Vedic verb for the book's central operation. |
| Radiant result | ***bhadrā eṣām lakṣmīḥ ... vāci*** — auspicious radiance placed in Speech | The *divyatā* claim: engineering made radiant and carried in Vāk. |

The body should avoid saying too early, "the verse proves Sanskrit was engineered." A more precise claim:

> Bṛhaspati describes Speech as sifted, refined, formed by the wise with the mind, socially recognized, and made radiant. This book shows Sanskrit as the most complete surviving architecture of that Vedic operation.

That distinction matters. The verse speaks of **Vāk**. The book applies the operation to **Sanskrit** by demonstrating the architecture from sonomer to sentence.

## 3. Why This Is the Keystone

### 3.1 The Sieve Gives the Chapter 8 → 9 Transition

Chapter 8 shows the field. Chapter 9 shows the selected inventory. RV 10.71.2 gives the exact image: grain sifted through a sieve.

The field supplies abundance. The sieve produces usable form. The *varṇamālā* is that sieve made audible.

### 3.2 The Verb Shares the Root of *Saṃskṛta*

***Vācam akrata*** means "they formed Speech." ***Akrata*** is a finite Vedic plural verb from **कृ (*kṛ*)**, to do, to make.

***Saṃskṛta*** is built from the same root: *sam-* + *kṛta* — well-made, brought together, made complete.

The verse names the making act at the root of the word *saṃskṛta* itself.

### 3.3 The Agents Are Plural and Anonymous

***Dhīrā manasā*** names the wise acting through mind. The verse does not require a single inventor. It fits the book's standing claim: Sanskrit's architects are plural, anonymous, and known by the architecture they left.

This also protects Pāṇini. Pāṇini decoded and compressed; he did not need to be made the inventor of Speech or grammar.

### 3.4 The Result Is Radiant

***Bhadrā eṣām lakṣmīḥ nihitā adhi vāci*** gives the *divyatā* layer. The result moves beyond function. Beauty rests in Speech. The engineering disappears into radiance.

This is the bridge from the Ch9 garland figure to the larger book: the poetry of the *mālā* carries engineering inside beauty.

### 3.5 The Maṇḍala-10 Move Is a Hypothetical Concession

The book should not accept the orthodoxy's chronology. It can use the orthodoxy's chronology against itself.

The clean body version:

> Even granting the orthodoxy's own stratification, this operation sits inside the Ṛgveda.

The longer argument belongs in the endnote. The body does not need to litigate Maṇḍala chronology. The point is simpler: the orthodoxy cannot dismiss the operation as a modern projection when the operation is stated inside the Vedic corpus it claims to analyze.

## 4. Deployment Decision

Use **Option C — restrained hybrid**.

1. **Preface:** implemented as one short forward pointer. No verse quotation. No six-step breakdown. No Maṇḍala-10 argument.
2. **Chapter 9 epigraph:** implemented. RV 10.71.2 gives the chapter its image before the prose begins.
3. **Chapter 9 §9.1:** implemented. The Vedic sieve now appears before the garland figure.
4. **Chapter 9 close:** implemented. The close now returns to the sieve insight and hands the selected sonomers to Chapter 10.
5. **Later chapters:** light callbacks only where the scale changes.
6. **Endnote:** first version implemented as `rigveda-10-71-2-sieve-vak`; local DCS / Griffith spot-check added. Optional Sāyaṇa / Maṇḍala-10 expansion remains pending.

This preserves both needs:

- The Preface signals that the book has a Vedic anchor, so the engineering thesis is not presented as a modern projection.
- Chapter 9 preserves the reveal-weight, because the reader has already seen the field before meeting the Vedic sieve. The epigraph makes the transition explicit without spending the full explanation before the chapter begins.

## 5. Preface Treatment

The Preface pointer must be restrained. It should protect the book without spending the keystone.

**Do not quote the verse in the Preface.**  
**Do not decompose it there.**  
**Do not use the phrase "verbatim engineering thesis" there.**

Preferred shape:

> The Vedic *paramparā* also preserves a direct anchor for this book's argument. Bṛhaspati describes Speech as sifted, formed by the wise with the mind, recognized among friends, and made radiant. Chapter 9 brings that *ṛc* forward at the moment where the sound-field becomes the *varṇamālā*. The book first shows the architecture; then the Vedic verse names the operation.

Possible shorter version:

> Chapter 9 will bring forward a Vedic anchor where Bṛhaspati describes Speech herself as sifted, formed by the wise with the mind, and made radiant. The book first shows the architecture; then the verse names the operation.

## 6. Chapter 9 Epigraph and Reveal

**Implemented in `atomicSanskrit/as_1_09_mapping_mouth.md`.** RV 10.71.2 is now the **Chapter 9 epigraph**. It gives the chapter the exact sequence it needs:

> sound-field → sieve → refined Speech → radiance in Vāk

The epigraph quotes the full verse. The prose of §9.1 now explains the image and moves into the figures.

Recommended epigraph:

> सक्तुमिव तितउना पुनन्तो यत्र धीरा मनसा वाचमक्रत ।  
> अत्रा सखायः सख्यानि जानते भद्रैषां लक्ष्मीर्निहिताधि वाचि ॥
>
> *saktum iva titaunā punanto yatra dhīrā manasā vācam akrata*  
> *atrā sakhāyaḥ sakhyāni jānate bhadraiṣāṃ lakṣmīr nihitādhi vāci*

The reveal now sits in **Chapter 9 §9.1**, immediately after the epigraph and before the existing *varṇamālā* garland figure.

The movement should be:

1. Chapter 8 is remembered as the sound-field.
2. The epigraph gives the Vedic sieve.
3. The new sieve figure shows loose sound-grains becoming a selected heap of Devanagari-marked sonomers.
4. The text names the selected result as *varṇamālā*.
5. The existing garland figure shows the poetic form of the selected inventory.
6. The section moves from garland to grid.

Suggested transition:

> The epigraph gives Chapter 9 its image: Speech sifted like grain. Chapter 8 showed the field. This chapter shows the sieve, the selected beads, and the grid.

Suggested body draft:

> Like grain sifted through a sieve, the wise refined Speech with the mind and formed her. There friends recognize friendship; auspicious radiance is placed in Speech.
>
> The image is exact. Grain is not created by the sieve, but usable measure is produced by selection. Chapter 8 showed the field. Chapter 9 shows the sieve. The field supplies abundance; the *varṇamālā* gives that abundance selected form.

Then the section can add the *kṛ* connection:

> The verb matters. ***Vācam akrata*** means "they formed Speech." The root is **कृ (*kṛ*)**, the same root inside ***saṃskṛta***. The verse names Speech as formed; the book shows the architecture of that formation.

Keep the Maṇḍala-10 line compressed:

> Even granting the orthodoxy's own stratification, this operation sits inside the Ṛgveda.

No longer than necessary. The reader should feel the verse's force, not get pulled into a chronology dispute.

## 6.1 Chapter 9 Sieve Figure

**Implemented.** The new figure now appears before the existing *varṇamālā* garland figure.

**Slug:** `vedic_sieve_sonomer_garland`
**Canonical path:** `figures/mapping_mouth/vedic_sieve_sonomer_garland.svg`
**Anchor:** `#fig:ch9-vedic-sieve-sonomer-garland`
**Current caption:** "The Vedic sieve: sound-grains pass through selection and fall as Devanagari-marked sonomers. The sieve selects; the *varṇamālā* will weave."

Claude Design concepts and variants live under:

- `figures/mapping_mouth/design_iterations/mapping_mouth_vedic_sieve_sonomer_garland_concept_a.svg`
- `figures/mapping_mouth/design_iterations/mapping_mouth_vedic_sieve_sonomer_garland_concept_b.svg`
- `figures/mapping_mouth/design_iterations/mapping_mouth_vedic_sieve_sonomer_garland_concept_c.svg`
- `figures/mapping_mouth/design_iterations/mapping_mouth_vedic_sieve_sonomer_garland_concept_d.svg`
- `figures/mapping_mouth/design_iterations/mapping_mouth_vedic_sieve_sonomer_garland_variant_*.svg`

Working title:

> **The Vedic Sieve and the Sonomer Garland**

Visual sequence:

> loose grains of sound → Vedic sieve → selected heap of Devanagari-marked sonomers → *varṇamālā* garland → ordered grid

Design principle:

- Use **grains** for the upper sound-field.
- Use **Devanagari-marked sonomers** for the selected heap below the sieve.
- Let the garland happen in the next figure, not inside the sieve figure.
- Let the sieve be geometric, architectural, or grid-like, not cartoon-farming imagery.
- Use the warm parchment / taupe visual family Claude Design has been producing; it should convert cleanly to grayscale while retaining warmth in color outputs.
- The 5x5 grid should read as the output of selection, not as the whole sieve.

Caption direction:

> RV 10.71.2 gives the sieve: Speech refined like grain. Sanskrit gives the garland: selected sonomers strung as *varṇamālā*. The field begins as abundance; the architecture emerges as chosen beads.

## 6.2 Chapter 9 Closing Return

**Implemented in `atomicSanskrit/as_1_09_mapping_mouth.md`.** The chapter now returns to the epigraph before handing off to Chapter 10 without re-quoting the whole mantra.

Suggested closing replacement:

> The epigraph named the operation before the chapter explained it. Speech is sifted like grain. The field is abundant, but abundance is not architecture. The sieve does not create the grain; it selects the usable measure.
>
> That is what the *varṇamālā* does. It takes the sound-field Chapter 8 surveyed and turns it into selected sonomers: compact, ordered, body-mapped, timed, teachable, and stable. In Sanskrit's own language, those sonomers are beads. In engineering language, they are coordinates. Both views describe the same object.
>
> The scale-chain now has its first visible Sanskritic grid:
>
> instrument → sound-field → sonomeric sieve → varṇamālā → atom
>
> Chapter 7 mapped the instrument. Chapter 8 surveyed the field. Chapter 9 has shown the sieve and the selected grid. Sanskrit now has measured sonomers. Chapter 10 asks what the system builds from them: the **धातुः (*dhātuḥ*)**, the semantic atom.

## 7. Recurring Anchor Phrase

Adopt ***vācam akrata*** as the recurring phrase.

First use in a chapter:

> ***vācam akrata*** — "they formed Speech"

Later uses in the same chapter:

> *vācam akrata*

Preferred claims:

- "Bṛhaspati describes the operation."
- "The verse names Speech as formed."
- "The book shows Sanskrit as the architecture of that operation."
- "The *Ṛṣi*'s verb runs through the scale-chain."

Avoid:

- "The verse proves Sanskrit was engineered."
- "The Veda states the modern engineering thesis verbatim."
- "The Veda anticipated systems theory."
- "This is just like manufacturing."

The verse is stronger when the text lets it speak in its own vocabulary: sifted, purified, made, radiant.

## 8. Sāyaṇa Guardrail

Sāyaṇa should be engaged, not dismissed.

Likely treatment:

> Sāyaṇa reads the verse through the ritual and recitational world. That reading stands. The engineering reading does not replace it; it names the architectural layer beneath it. A ritual world can operate only because Speech has already been refined, made, recognized, and held.

Endnote treatment:

- Summarize Sāyaṇa's ritual / allegorical reading.
- Give the relevant Sanskrit if available and verified.
- State that the book's reading is compatible with Sāyaṇa, not opposed to him.
- Keep the body free of a long commentary dispute.

## 9. Endnote Plan

Use one required dossier note and two optional supporting notes.

### 9.1 Implemented: `rigveda-10-71-2-sieve-vak`

Current note carries:

- Full verse in Devanagari and IAST.
- Sieve / selection reading.
- *kṛ* / *saṃskṛta* morphological note.
- Radiance / *varṇamālā* bridge.
- Source-basis note: local DCS records and Griffith support the current reading; final publication must still verify saṃhitā text, accenting, and Sāyaṇa against the selected printed edition.

Still to add if needed:

- Literal word-by-word table.
- Six-element decomposition.
- *dhīrāḥ* as plural intelligent agents.
- Maṇḍala-10 hypothetical-concession argument.
- Sāyaṇa compatibility note.

Short form:

> RV 10.71.2 describes Speech as sifted, refined, formed by the wise with the mind, socially recognized, and made radiant. The note gives the six-element decomposition and the *kṛ* / *saṃskṛta* connection.

### 9.2 Optional: `rigveda-10-71-2-bhadra-lakshmi-vaci`

Use only if Chapters 14/15 need a separate radiance note.

Carries:

- *bhadrā eṣām lakṣmīḥ nihitā adhi vāci*.
- Translation range: radiance, auspicious beauty, fortune, splendor.
- Connection to *divyatā* and preserved beauty.

### 9.3 Optional: `sayana-rv-10-71-2-ritual-and-engineering`

Use if the manuscript directly invokes Sāyaṇa.

Carries:

- Sāyaṇa's reading.
- The book's complementary architectural reading.
- Statement that both readings remain inside the *paramparā*.

## 10. Book-Wide Thread

Because RV 10.71.2 is a keystone, it should leave a light mark across the book. The mark should be controlled: a word, sentence, or short paragraph at the right scale. Do not repeat the full verse outside Chapter 9 unless a chapter explicitly needs it.

The thread has seven motifs:

1. **Field** — abundance before selection.
2. **Sieve** — selection from abundance.
3. **Refinement** — purification / ordering into usable form.
4. **Mind** — intelligence, not accident.
5. **Making** — ***vācam akrata***, Speech formed.
6. **Recognition** — friends recognize the formed result.
7. **Radiance** — beauty placed in Speech and held.

Each chapter should carry at most one motif unless the chapter is central to the keystone.

| Location | Motif | Deployment |
|---|---|---|
| Preface | Anchor | One restrained forward-pointer: Bṛhaspati describes Speech as sifted, formed by the wise, and made radiant. No quotation. |
| Ch0 | Whole / Pūrṇam | Optional one sentence: the book will follow how a complete architecture makes speech without exhausting its generative fullness. |
| Ch1 | Category theft | Optional one sentence: the pyramid hides formed Speech by forcing her into nature before Pāṇini and codification after Pāṇini. |
| Ch2 | Strategic necessity | Optional one sentence: a civilization that loses the category of formed Speech loses the ability to describe its own architecture. |
| Ch3 | Asuric pyramid | Optional one sentence: the pyramid cannot permit *vācam akrata* to stand, because formed Speech implies distributed calibration rather than apex command. |
| Ch4 | *Siddha* | Implemented: Bṛhaspati's *vācam akrata* names Speech as formed; Patañjali's *siddha* states the grammatical consequence. |
| Ch5 | Entropy / *apabhraṃśa* | Optional one sentence: refinement must be protected because unsieved speech falls away into many corruptions. |
| Ch6 | Architectural *dhātuḥ* | Optional one sentence: if Speech is made, the *dhātuḥ* is the first semantic unit whose making must be examined. |
| Ch7 | Instrument | Optional one sentence: before Speech can be sifted, the instrument that produces sound must be understood. |
| Ch8 | Sound-field | Implemented: the field supplies abundance; Ch9 gives the Vedic sieve image. |
| Ch9 | Keystone | Full epigraph, sieve figure, §9.1 explanation, and chapter-close return. |
| Ch10 | Atom | Implemented: *vācam akrata* at atomic scale — selected sonomers enter scaffolds and become *dhātavaḥ*. |
| Ch11 | Molecule | Optional one sentence: the made atom remains visible as it becomes action. |
| Ch12 | Assembly | Implemented: formed Speech keeps sonomers, atoms, molecules, bonds, and roles traceable inside the assembly. |
| Ch13 | Preservation | Optional one sentence: what is made by refinement must be preserved against drift. |
| Ch14 | Calibration | Strong callback: *bhadrā eṣām lakṣmīḥ* — radiance placed in Speech is held by the calibration matrix. |
| Ch15 | Aural architecture | Optional one sentence: the formed result is carried by trained hearing as well as writing. |
| Ch16 | Vedic boundary | Optional one sentence: the perimeter protects the made architecture without mistaking the boundary for the source. |
| Ch17 | Wrong question | Implemented: genealogy asks for ancestry; *vācam akrata* points to construction. |
| Ch18 | PIE | Implemented: PIE turns reflections into source; the Vedic witness points to formed Speech first, reflections afterward. |
| Epilogue | Verdict + blessing | Required return: Bṛhaspati had named the operation; the book has followed it from mouth to calibrated language. Then a separate Vāk blessing invites the reader to carry the architecture forward. |

### 10.1 Book-Wide Restraint Rules

- Full verse only in Chapter 9, unless a later chapter explicitly needs a fragment.
- Use ***vācam akrata*** sparingly; it should feel like an anchor, not a slogan.
- Use "formed Speech" where the reader needs clarity; use *vācam akrata* where the Sanskrit itself carries force.
- Keep the claim precise: the verse speaks of **Vāk**; the book shows **Sanskrit** as the surviving architecture of that operation.
- Do not add the motif mechanically to every chapter. The table is a menu, not a quota.

## 11. Chapter Callback Drafts

### Chapter 4 — *Siddha* and *Kārya*

**Implemented in `atomicSanskrit/as_1_04_siddha.md`.**

Small callback after *siddha* is established:

> The Vedic anchor sits one layer deeper. Bṛhaspati's ***vācam akrata*** names Speech as formed by the wise with the mind. Patañjali's *siddha* gives the grammatical consequence: the formed architecture is already established before an individual speaker uses it.

### Chapter 10 — Atomic Scale

**Implemented in `atomicSanskrit/as_1_10_building_dhatuh.md`.**

Use when the *dhātuḥ* is shown as an atomic construction:

> At the *varṇamālā* scale, *vācam akrata* appears as selected sonomers. At the *dhātuḥ* scale, the same formation becomes atomic: sonomers enter measured scaffolds and become semantic atoms.

### Chapters 14–15 — Radiance Held

**Implemented in `atomicSanskrit/as_1_14_calibration.md` and `atomicSanskrit/as_1_15_aural.md`.**

Use the *bhadrā eṣām lakṣmīḥ* clause lightly:

> RV 10.71.2 does not end with making alone. It ends with radiance placed in Speech. The calibration matrix is how that radiance is held against time.

Current deployment:

- **Chapter 14 opening:** after "The calibration matrix is the radiant matrix," the text recalls ***bhadrā eṣām lakṣmīḥ nihitā adhi vāci*** and asks how that radiance is held.
- **Chapter 15 opening:** one sentence carries the claim into Auditure: formed and radiant Speech becomes audible preservation.

### Epilogue

Return to RV 10.71.2 as verdict, not as new explanation:

> Bṛhaspati had already named the operation: Speech sifted, formed by the wise with the mind, recognized among friends, and made radiant. The book has followed that operation from mouth to sonomer, from sonomer to atom, from atom to molecule, and from molecule to calibrated language.

Then add a **separate Vāk blessing** before the final invitation. Do not let it compete with RV 10.71.2. RV 10.71.2 is the keystone for formed Speech; RV 8.100.11 is the blessing for readers who will carry Speech forward.

Recommended mantra:

> देवीं वाचमजनयन्त देवास्तां विश्वरूपाः पशवो वदन्ति ।
> सा नो मन्द्रेषमूर्जं दुहाना धेनुर्वागस्मानुप सुष्टुतैतु ॥
>
> *devīṃ vācam ajanayanta devās tāṃ viśvarūpāḥ paśavo vadanti*
> *sā no mandreṣam ūrjaṃ duhānā dhenur vāg asmān upa suṣṭutaitu*

Working translation:

> The devas generated divine Speech; all beings, in many forms, speak her. May Vāk come to us, well-praised, like a milk-cow yielding sweetness and strength.

Suggested epilogue bridge:

> The invitation is not to compose new *śruti*. It is to become capable of seeing what Vāk has already revealed, to carry the architecture forward, and to let Speech nourish the next civilizational act.

Use this where the Epilogue turns from prosecution to invitation: after the verdict has landed, before asking readers to become the next wave of carriers / seers.

## 12. Implementation Sequence

- [x] **Make RV 10.71.2 the Chapter 9 epigraph.**
- [x] **Add the final SVG** using `vedic_sieve_sonomer_garland`.
- [x] **Revise Chapter 9 §9.1** around the epigraph, sieve image, selected heap, garland, and grid.
- [x] **Add the first required endnote** as `rigveda-10-71-2-sieve-vak`.
- [x] **Revise the Chapter 9 close** to return to the sieve insight before the Ch10 handoff.
- [x] **Add the restrained Preface pointer.**
- [x] **Add the Chapter 4 callback.**
- [x] **Add the Chapter 10 callback.**
- [x] **Add the Chapters 14/15 radiance callback only if it improves flow.**
- [x] **Add the Epilogue return to RV 10.71.2 only after the chapter callbacks are stable.**
- [x] **Add the RV 8.100.11 Vāk blessing** near the Epilogue's final invitation.
- [x] **Expand the endnote** only where the manuscript needs more support: word-by-word, Sāyaṇa, Maṇḍala-10, or source edition.
- [x] **Run a verse-text consistency search** for `तित्उना`, `तितउना`, `तितौना`, `titaunā`, `tita-unā`, `vācam akrata`, and `वाचमक्रत`.
- [x] **Run the Vāk-blessing consistency search** for `देवीं वाचम्`, `devīṃ vācam`, `8.100.11`, and `Vāk blessing`.
- [x] **Run the book-wide thread pass** using §10 as the guide; deploy only where the motif improves chapter flow.

## 13. Open Checks Before Manuscript Deployment

1. Verify the Devanagari verse text against the selected printed Ṛgveda edition, especially `तितउना` / `तित-उना` / possible editorial `तितौना` and the accenting.
2. Translation decision recorded in the endnote: use "grain" in the body for reader clarity; acknowledge meal / flour as possible.
3. Translation decision recorded in the endnote: use "refined" in the body because *titaunā* supplies the sieve image.
4. Body decision recorded in the endnote: keep "auspicious radiance" for *bhadrā eṣām lakṣmīḥ* because Chapter 9 links it to *divyatā*.
5. Sāyaṇa placement decided: endnote only, as a compatibility guardrail rather than a body argument.
6. RV 8.100.11 local spot-check complete against DCS pada / conllu, Jamison-Brereton, and Griffith; final printed-edition verification can still be done before publication.
7. Decide the final term for the reader invitation: "Wave 3 ṛṣis," "next wave of carriers," "new seers," or another phrase.

## 14. Final Principle

This verse should not replace the book's proof. It should compress it.

The book first demonstrates architecture through procedure, figures, and analysis. RV 10.71.2 then shows that the Vedic corpus already describes Speech through the same operational sequence: field, sieve, refinement, mind, making, recognition, radiance.

That is why the verse is the keystone.
