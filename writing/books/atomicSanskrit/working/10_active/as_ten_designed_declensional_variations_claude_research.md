# Ten Designed Declensional Variations — Corpus Verification

*Research deliverable for Appendix Part 8, **One Architecture, Two Domains**. Completed 2026-07-27 in the main loop (the parallel-agent workflow failed on a session limit; local-corpus attestation is the stronger method anyway — every form below is checked against a real corpus, nothing is recalled or reconstructed).*

---

## Method and evidence posture

**Primary corpus.** The Digital Corpus of Sanskrit (DCS), CoNLL-U morphological edition, restricted to the Vedic Saṃhitās: Ṛgveda, Atharvaveda (Śaunaka + Paippalāda), Kāṭhaka, Maitrāyaṇī, Taittirīya, Vājasaneyi (Mādhyandina). Path: `analysis/ganah/data/raw/dcs/dcs/data/conllu/files/`. Every count, form, morphological tag, maṇḍala/hymn header, and verse text below was pulled directly from this corpus on 2026-07-27 (2,565 Vedic Saṃhitā files, 472,190 tokens). Token matching filtered on the DCS `FEATS` morphology so that orthographic look-alikes (e.g. *devā* the nominative plural vs *devā* the dual) are separated by their tags, not by string.

**What the corpus does and does not give.** The DCS supplies the exact sandhied verse text and a reliable case/number/gender tag per token. It does **not** carry Vedic accent (*udātta / anudātta / svarita*) and does not reproduce the *padapāṭha*. Per the strict rules, no accent, *padaccheda*, or full metrical scansion is invented here. Where a point requires the accented text or the word-split, this document says so and points to the printed sources that carry them:

- **Accented text / meter:** van Nooten & Holland, *Rig Veda: A Metrically Restored Text* (HOS 50); Aufrecht, *Die Hymnen des Ṛgveda*.
- **Padapāṭha:** the Śākala *padapāṭha* (in Aufrecht and in the Poona/BORI apparatus).
- **Form catalogues (tier 4, for locating evidence only):** Macdonell, *Vedic Grammar for Students* §§ on declension; Whitney, *Sanskrit Grammar* §§329–425.

**Pāṇinian citations.** Three sūtras central to the Vedic case-endings were verified earlier this session against GRETIL's Aṣṭādhyāyī and the Kāśikā: **7.1.9 अतो भिस ऐस्**, **7.1.39 सुपां सुलुक्…**, **7.1.50 आज्जसेरसुक्**. These are presented with confidence. Every other sūtra number carries a **⚠ verify** flag and is my best identification of the documenting rule, to be checked against the Aṣṭādhyāyī/Kāśikā before it reaches print. Throughout, Pāṇini **documents** the form; he does not create, regularize, fix, standardize, or codify it.

---

## Headline finding — the corpus splits the ten into two classes

The verification does not return a flat "all ten confirmed." It returns a **structural split** that is itself the appendix's argument:

**Class A — both members live in the calibrant (7 of 10).** For SG-01, SG-02, SG-10, DU-01, PL-01, PL-07, PL-12 the *vaidika* form **and** its *laukika* counterpart both occur in the Vedic Saṃhitās, repeatedly, sometimes in the same hymn or the same verse. *rudrebhiḥ* and *rudraiḥ* both stand in the corpus; *agnā* (19×) and *agnau* (87×) both stand in the Ṛgveda; *viśvā* (373 neut.) and *viśvāni* (115) both stand in the Ṛgveda; *ṚV 10.63.2* carries *viśvā* and *devā* in one line while *devāso* sits in *10.63.4*. These are **parallel options selected in performance**, not two chronological layers. Difference here is not sequence.

**Class B — only the ending-class form lives in the calibrant; the *laukika* counterpart is NOT FOUND (2 of 10).** For DU-04 the *laukika* **देव्यौ (*devyau*)** and for PL-03 the *laukika* **देव्यः (*devyaḥ*)** do **not** occur anywhere in the searched Vedic Saṃhitās. The Vedic corpus attests only the *ī*-ending **देवी (*devī*, dual)** and **देवीः (*devīḥ*, nom. pl.)**. The *-y-* forms are the systematic *bhāṣā* outcome of a documented sandhi (*ī → y* before a vowel-initial ending, Pāṇini 6.1.77 इको यणचि / 6.4.77 …इयङुवङौ ⚠ verify) — **derived, not reconstructed.** No unattested ancestor is posited: the calibrant records one member and the grammar derives the other by a stated rule.

**DU-09 is a third, sharper case:** the pronoun dual shows the *vaidika* domain carrying **more distinct forms** than the *laukika* — a genuine *nominative* **युवम् (*yuvam*)** separate from the *accusative* **युवाम् (*yuvām*)**, plus a rare ablative **युवत् (*yuvat*)** — where Classical Sanskrit merges nominative and accusative into a single dual form. Here the calibrant is the higher-resolution instrument.

This split is the calibration-not-reconstruction thesis in miniature: for Class A the *vaiyākaraṇāḥ* **decode from the calibrant** (both forms are present to be recorded); for Class B they **derive by documented rule** where the calibrant records one member. In neither class is anything reconstructed from drift.

---

## The ten examples

### SG-01 — तृतीया एकवचनम्, अकारान्त — यज्ञेन / यज्ञा (*yajñena / yajñā*)

1. **Verification result:** **Confirmed** (the *-ā* instrumental *yajñā*). The third listed form *yajñenā* is **NOT FOUND** as a distinct instrumental token; the metrically-lengthened *yajñénā* is a realization of *yajñena*, not separately catalogued in the DCS. Treat the designed pair as **yajñena ~ yajñā**.
2. **Exact Vedic passage (unaccented, DCS):** यज्ञा यज्ञा वः अग्नये गिरा गिरा च दक्षसे… — *yajñā yajñā vaḥ agnaye girā girā ca dakṣase* (ṚV 6.48.1). Accent to be taken from van Nooten–Holland / Aufrecht.
3. **Citation:** Ṛgveda, maṇḍala 6, hymn 48 (DCS chapter_id 10165-series; header `ṚV, 6, 48`). Corpus: DCS. Printed: Aufrecht I, RV 6.48.1.
4. **Padaccheda:** editorial split — *yajñā | yajñā | vaḥ | agnaye | girā | girā | ca | dakṣase* (Śākala *padapāṭha* to be consulted for the authoritative split; marked editorial).
5. **IAST:** *yajñā yajñā vaḥ agnaye girā girā ca dakṣase*.
6. **Translation:** literal — "with sacrifice (and) sacrifice for you, for Agni, with song (and) song, for skill…"; readable — "Sacrifice upon sacrifice for you to Agni, song upon song, that he may prosper."
7. **Target form:** *yajñā* — *akārānta* masculine, **तृतीया विभक्ति एकवचनम्** (instrumental singular). The *-ā* ending directly on the *akārānta*.
8. **Laukika counterpart:** *yajñena*. Same *dhātu*-noun *yajña*, same case/number; the *-ena* ending (*-ina* affixed) replaces the bare *-ā*. Everything semantic is identical; the audible ending differs.
9. **Syllable analysis:** *ya-jñā* = 2σ; *ya-jñe-na* = 3σ. In this pāda the doubling *yajñā yajñā* runs the light-tail-free 2σ form twice against *girā girā*, another bare *-ā* instrumental.
10. **Laghu-guru:** *yajñā* = **G G** (ya heavy by the following *jñ* conjunct; * jñā* long). *yajñena* = **G G L**. The variation drops the final *laghu* — a real weight/count change.
11. **Svara:** the instrumental *-ā* and the thematic *-ena* differ in accent placement; **Open** — requires the accented edition. Not asserted here.
12. **Local function:** the verse is built on iterated bare instrumentals (*yajñā yajñā … girā girā*). The 2σ all-*guru* form gives a hammered, evenly-weighted iteration a 3σ *-ena* could not; the design serves the pāda's repetition-rhythm.
13. **DV codes:** **MAT Confirmed** (2σ vs 3σ, drops a *laghu*); **SON Confirmed** (*-ā* vs *-ena* audibly distinct endings); **REC Probable** (iteration-rhythm in a *gāyatrī*-type pāda); **ARR Probable** (the doubling *yajñā yajñā* is a compositional figure); **SVR Open**; **AUD Open**.
14. **Indic documentation:** the Vedic bare *-ā* instrumental of *akārānta* nouns is documented under **7.1.39 सुपां सुलुक्…** (*suluk*-class Vedic case-ending options; verified). Pāṇini records the option; he does not prefer it.
15. **Distribution:** *yajñena* 123× / *yajñā* (Ins) 4× across the Vedic Saṃhitās. Both Vedic; *-ena* dominant corpus-wide, the bare *-ā* selected in specific iterative/metrical pādas. Not śākhā-limited.
16. **Figure-ready:** *SG-01 · यज्ञा (Ins) ↔ यज्ञेन · MAT+SON · bare -ā instrumental drops a light syllable, fitting the doubled-instrumental pāda-rhythm.*
17. **Confidence:** **Strong** for the pair *yajñā ~ yajñena*; the third form *yajñenā* is dropped as unverified.

---

### SG-02 — तृतीया एकवचनम्, आकारान्त — मनीषया / मनीषा (*manīṣayā / manīṣā*)

1. **Verification result:** **Confirmed** — both forms occur, and the contracted *-ā* is the more frequent in the Ṛgveda.
2. **Exact passage (unaccented, DCS):** इन्द्राय हृदा मनसा मनीषा प्रत्नाय पत्ये… — *indrāya hṛdā manasā manīṣā pratnāya patye dhiyo marjayanta* (ṚV 1.61.2). And the full form: तं नाकं चित्रशोचिषम् … परो मनीषया — *… paro manīṣayā* (ṚV 5.17.x).
3. **Citation:** Ṛgveda 1.61 (*manīṣā*) and 5.17 (*manīṣayā*). Corpus: DCS. Printed: Aufrecht I.
4. **Padaccheda:** editorial — *indrāya | hṛdā | manasā | manīṣā | pratnāya | patye | dhiyaḥ | marjayanta* (Śākala *padapāṭha* for the authoritative split).
5. **IAST:** *indrāya hṛdā manasā manīṣā pratnāya patye dhiyo marjayanta*.
6. **Translation:** literal — "for Indra, with heart, with mind, with thought, for the ancient lord, they burnish their prayers"; readable — "With heart, mind, and inspired thought they make their hymns bright for Indra, the ancient lord."
7. **Target form:** *manīṣā* — *ākārānta* feminine, **तृतीया विभक्ति एकवचनम्** (instrumental singular), the contracted *-ā* on the *ākārānta*.
8. **Laukika counterpart:** *manīṣayā* — same noun, same case; the full *-ayā* (*-y-* glide + *-ā*) instead of the contracted *-ā*.
9. **Syllable analysis:** *ma-nī-ṣā* = 3σ; *ma-nī-ṣa-yā* = 4σ. In ṚV 1.61.2 *manīṣā* completes a **triple bare-instrumental run** — *hṛdā, manasā, manīṣā* — three *-ā* instrumentals in sequence.
10. **Laghu-guru:** *manīṣā* = **L G G**; *manīṣayā* = **L G L G**. The contraction removes a medial *laghu* and shortens the word by one *mātrā*-bearing syllable.
11. **Svara:** feminine *ākārānta* instrumental accent; **Open** — accented edition required.
12. **Local function:** the design lets *manīṣā* rhyme by ending with *hṛdā* and *manasā* — three identical *-ā* tails close the instrumental triplet, a strong sound-figure (RES) the 4σ *-ayā* would break.
13. **DV codes:** **MAT Confirmed** (3σ vs 4σ); **RES Confirmed** (the *-ā / -ā / -ā* triplet in ṚV 1.61.2); **SON Confirmed**; **REL Probable** (the shared instrumental tail groups the three means audibly); **SVR Open**; **REC Open**.
14. **Indic documentation:** contracted *-ā* for *ākārānta* feminine instrumental is a Vedic *suluk*-class option under **7.1.39 सुपां सुलुक्…** (verified). Documented, not preferred.
15. **Distribution:** *manīṣā* (Ins) 10× / *manīṣayā* 6× in the Vedic Saṃhitās. Both Vedic; the contracted form actually dominant in the RV. Not śākhā-limited.
16. **Figure-ready:** *SG-02 · मनीषा (Ins) ↔ मनीषया · MAT+RES · contracted -ā closes a three-instrumental rhyme (hṛdā, manasā, manīṣā).*
17. **Confidence:** **Strong** — both forms attested with a clean local sound-function in ṚV 1.61.2.

---

### SG-10 — सप्तमी एकवचनम्, इकारान्त — अग्नौ / अग्ना (*agnau / agnā*)

1. **Verification result:** **Confirmed** — both *agnā* (loc.) and *agnau* (loc.) occur in the Ṛgveda; *agnau* is the more frequent even in the RV.
2. **Exact passage (unaccented, DCS):** उषा उच्छन्ती समिधाने अग्ना उद्यन् सूर्य उर्विया ज्योतिर् अश्रेत् — *uṣā ucchantī samidhāne agnā udyan sūrya urviyā jyotir aśret* (ṚV 1.124.1).
3. **Citation:** Ṛgveda 1.124.1 (*agnā*, loc.); *agnau* passim (e.g. ṚV 1.189, 5.1). Corpus: DCS. Printed: Aufrecht I.
4. **Padaccheda:** editorial — *uṣāḥ | ucchantī | samidhāne | agnā | udyan | sūryaḥ | urviyā | jyotiḥ | aśret* (Śākala *padapāṭha* for the authoritative split).
5. **IAST:** *uṣā ucchantī samidhāne agnā udyan sūrya urviyā jyotir aśret*.
6. **Translation:** literal — "Dawn shining forth, the fire being kindled (loc.), the sun rising, has spread its light widely"; readable — "As Dawn breaks and the fire is kindled and the sun climbs, its light spreads wide."
7. **Target form:** *agnā* — *ikārānta* masculine *agni*, **सप्तमी विभक्ति एकवचनम्** (locative singular), the *-ā* locative.
8. **Laukika counterpart:** *agnau* — same noun, same case; the *-au* locative (*guṇa* + *-i* → *-au*) instead of *-ā*.
9. **Syllable analysis:** *ag-nā* = 2σ; *ag-nau* = 2σ. Equal count.
10. **Laghu-guru:** *agnā* = **G G**; *agnau* = **G G** (diphthong *au* heavy). **No weight or count change** — this is the diagnostic case where the variation is **not** metrical.
11. **Svara:** locative accent; **Open** — accented edition required.
12. **Local function:** because weight is identical, the design here is **sonomeric**, not prosodic: the final long *-ā* vs the diphthong *-au* is a pure quality contrast on the same weight. In a *loc.-absolute* string (*samidhāne agnā … udyan sūrya*) the *-ā* tail harmonizes with the surrounding *-e / -ā* vowels.
13. **DV codes:** **SON Confirmed** (*-ā* vs *-au* on identical weight); **MAT Rejected** (no weight/count change — the plan's implicit metrical reading fails here); **RES Probable** (vowel-harmony with the *-e/-ā* neighbours); **REL Open**; **SVR Open**.
14. **Indic documentation:** the Vedic *-ā* locative of *ikārānta* nouns is a *suluk*-class option under **7.1.39 सुपां सुलुक्…** (verified); the Classical *-au* is the *ghi* locative substitution (7.3.119 अच्च घेः ⚠ verify). Both documented.
15. **Distribution:** *agnau* (Loc) 87× / *agnā* (Loc) 19× in the Vedic Saṃhitās — **both in the Ṛgveda**, the *-au* form already dominant there. This directly refutes any "*-au* is the later Classical form" reading: the calibrant carries both.
16. **Figure-ready:** *SG-10 · अग्ना (Loc) ↔ अग्नौ · SON (not MAT) · same weight, pure vowel-quality contrast — the clean case that variation is not always metrical.*
17. **Confidence:** **Strong**, and diagnostically important: it is the example that proves the design axis is sonomeric/quality, not only *mātrā*.

---

### DU-01 — प्रथमा–द्वितीया–संबोधन द्विवचनम्, अकारान्त — देवौ / देवा (*devau / devā*)

1. **Verification result:** **Confirmed** — the *-ā* dual and the *-au* dual both occur in the Ṛgveda (morphology-tag `Number=Dual` isolates them from the many other *devā* strings).
2. **Exact passage (unaccented, DCS):** विश्वा हि वो नमस्यानि वन्द्या नामानि देवा उत यज्ञिया वः — *viśvā hi vo namasyāni vandyā nāmāni devā uta yajñiyāni vaḥ* (ṚV 10.63.2; DCS tags *devā* here `Voc … Dual`).
3. **Citation:** Ṛgveda 10.63.2 (a Viśvedevāḥ hymn); nominative-dual *devā* at 1.184, 1.22; *devau* passim. Corpus: DCS. Printed: Aufrecht II.
4. **Padaccheda:** editorial — *viśvā | hi | vaḥ | namasyāni | vandyā | nāmāni | devā | uta | yajñiyāni | vaḥ* (Śākala *padapāṭha* for the authoritative split).
5. **IAST:** *viśvā hi vo namasyāni vandyā nāmāni devā uta yajñiyāni vaḥ*.
6. **Translation:** literal — "for all your names are to-be-revered and to-be-praised, O two devas, and worshipful are yours"; readable — "All your names deserve reverence and praise, O paired devas, and worship is yours."
7. **Target form:** *devā* — *akārānta* masculine, dual, **प्रथमा/संबोधन द्विवचनम्** (nominative/vocative dual), the *-ā* dual ending.
8. **Laukika counterpart:** *devau* — same noun, same case/number; the *-au* dual instead of *-ā*.
9. **Syllable analysis:** *de-vā* = 2σ; *de-vau* = 2σ. Equal.
10. **Laghu-guru:** *devā* = **G G**; *devau* = **G G**. **No weight/count change** — like SG-10, a sonomeric, not metrical, variation.
11. **Svara:** dual accent; **Open** — accented edition required.
12. **Local function:** the *-ā* dual *devā* removes one distinct signal — it collides in surface shape with *devā* the nominative plural and vocative singular. The *laukika* *-au* is the **more distinguishable** dual. This example runs the design **in the *laukika* direction**: the worldly domain buys disambiguation at no metrical cost, exactly the read-write trade the appendix argues.
13. **DV codes:** **SON Confirmed**; **REL Confirmed** (*-au* disambiguates the dual from the collision-prone *-ā*); **MAT Rejected** (no weight change); **SVR Open**; **AUD Probable** (the *-au* adds a self-checking distinct dual marker).
14. **Indic documentation:** the Vedic *-ā* for the dual *auṄ* ending is listed explicitly in **7.1.39 सुपां सुलुक्…** (the *āṄ*/*āḍ* substitution for the dual in *chandas*; verified). Pāṇini documents the *-ā* dual as a Vedic option beside the standard *-au*.
15. **Distribution:** *devā* (Dual) 28× / *devau* (Dual) 16× in the Vedic Saṃhitās — both in the RV. The *-ā* dual slightly dominant in the calibrant.
16. **Figure-ready:** *DU-01 · देवा (dual) ↔ देवौ · SON+REL · same weight; the laukika -au is the more distinguishable dual — designed variation running toward disambiguation.*
17. **Confidence:** **Strong** — clean dual tagging, both forms in the RV, and a clear disambiguation function.

---

### PL-01 — प्रथमा बहुवचनम्, अकारान्त पुल्लिङ्ग — देवाः / देवासः (*devāḥ / devāsaḥ*)

1. **Verification result:** **Confirmed** — the extended *-āsaḥ* nominative plural is robustly Vedic.
2. **Exact passage (unaccented, DCS):** नृचक्षसो अनिमिषन्तो अर्हणा बृहद् देवासो अमृतत्वम् आनशुः — *nṛcakṣaso animiṣanto arhaṇā bṛhad devāso amṛtatvam ānaśuḥ* (ṚV 10.63.4).
3. **Citation:** Ṛgveda 10.63.4 (the same Viśvedevāḥ hymn as DU-01 and PL-07). Corpus: DCS. Printed: Aufrecht II.
4. **Padaccheda:** editorial — *nṛcakṣasaḥ | animiṣantaḥ | arhaṇā | bṛhat | devāsaḥ | amṛtatvam | ānaśuḥ* (Śākala *padapāṭha* for the authoritative split).
5. **IAST:** *nṛcakṣaso animiṣanto arhaṇā bṛhad devāso amṛtatvam ānaśuḥ*.
6. **Translation:** literal — "beholding men, unwinking, by their worth, the devas have attained great immortality"; readable — "Watching over mortals, never closing their eyes, by their own worth the devas have won high immortality."
7. **Target form:** *devāsaḥ* (sandhi *devāso*) — *akārānta* masculine, **प्रथमा विभक्ति बहुवचनम्** (nominative plural), the extended *-āsaḥ* ending.
8. **Laukika counterpart:** *devāḥ* — same noun, same case/number; the plain *-āḥ* instead of the extended *-āsaḥ*.
9. **Syllable analysis:** *de-vā-saḥ* = 3σ; *de-vāḥ* = 2σ. The extension adds one syllable.
10. **Laghu-guru:** *devāsaḥ* = **G G G**; *devāḥ* = **G G**. Adds a *guru* — a real *mātrā* increase.
11. **Svara:** plural accent; **Open** — accented edition required.
12. **Local function:** in a *triṣṭubh/jagatī*-length pāda the 3σ *devāso* fills the metre and, with the internal *-s-*, plants an audible morpheme boundary before *amṛtatvam*, keeping the nominative-plural subject sharply marked across the long line.
13. **DV codes:** **MAT Confirmed** (2σ vs 3σ); **REL Confirmed** (the *-s-* is an audible plural-boundary marker); **AUD Confirmed** (the extra syllable + *s* is exactly redundancy — a self-checking plural signal); **SON Confirmed**; **SVR Open**; **REC Probable**.
14. **Indic documentation:** **7.1.50 आज्जसेरसुक्** (*āj jaser asuk*, verified) — after an *ā*-final, the augment *asUK* is added to the *jas* (nominative-plural) ending *in chandas*, producing *devās-as → devāsaḥ*. This is the exact documenting sūtra; Pāṇini records the Vedic option explicitly with the locative *chandasi*.
15. **Distribution:** *devāso* 81× + *devāsaḥ* 34× + *devāsas* 3× = 118 in the Vedic Saṃhitās. System-wide Vedic option for *akārānta* masculines, not a lexical one-off; the plain *-āḥ* also present throughout.
16. **Figure-ready:** *PL-01 · देवासः (nom.pl) ↔ देवाः · MAT+REL+AUD · the -āsaḥ augment adds a syllable and an audible plural-boundary check (Pāṇini 7.1.50).*
17. **Confidence:** **Strong** — exact Pāṇinian sūtra verified, 118 attestations, clear redundancy function.

---

### PL-07 — प्रथमा–द्वितीया–संबोधन बहुवचनम्, अकारान्त नपुंसकलिङ्ग — विश्वानि / विश्वा (*viśvāni / viśvā*)

1. **Verification result:** **Confirmed** — the bare *-ā* neuter plural and the *-āni* neuter plural both stand in the Ṛgveda, both abundantly.
2. **Exact passage (unaccented, DCS):** विश्वा हि वो नमस्यानि वन्द्या नामानि देवा उत यज्ञिया वः — *viśvā hi vo namasyāni …* (ṚV 10.63.2; DCS tags *viśvā* here `Nom Neut Plur`).
3. **Citation:** Ṛgveda 10.63.2 (*viśvā*, neut. nom. pl.); *viśvāni* passim (e.g. ṚV 10.63.x, 7.4). Corpus: DCS. Printed: Aufrecht II.
4. **Padaccheda:** editorial — *viśvā | hi | vaḥ | namasyāni | vandyā | nāmāni | devā | uta | yajñiyāni | vaḥ* (as DU-01).
5. **IAST:** *viśvā hi vo namasyāni vandyā nāmāni devā uta yajñiyāni vaḥ*.
6. **Translation:** as DU-01 above — "All your names…". *viśvā* here modifies *nāmāni* ("all names").
7. **Target form:** *viśvā* — *akārānta* neuter, **प्रथमा/द्वितीया बहुवचनम्** (nominative/accusative plural), the bare *-ā* (uninflected-looking) neuter plural.
8. **Laukika counterpart:** *viśvāni* — same word, same case/number; the *-āni* (num-augmented) neuter plural.
9. **Syllable analysis:** *viś-vā* = 2σ; *viś-vā-ni* = 3σ. The *-āni* adds one syllable.
10. **Laghu-guru:** *viśvā* = **G G**; *viśvāni* = **G G L**. Adds a final *laghu*.
11. **Svara:** neuter-plural accent; **Open** — accented edition required.
12. **Local function:** note the design running **both ways in one verse**: *viśvā* (bare, 2σ) opens the pāda while *namasyāni, nāmāni, yajñiyāni* (all *-āni*, 3σ) close their words. The composer picks the 2σ neuter for the pāda-head and the 3σ neuters for the fuller cadences — a deliberate weight distribution, not free variation.
13. **DV codes:** **MAT Confirmed** (2σ vs 3σ); **REL Confirmed** (*-āni* is the more audibly-marked neuter plural; bare *-ā* is lighter but collides with feminine *-ā* singular/plural); **ARR Confirmed** (the *viśvā … -āni … -āni … -āni* weight patterning within the verse); **SON Confirmed**; **SVR Open**.
14. **Indic documentation:** the *-āni* neuter plural = *śi* substitution (7.1.20 जश्शसोः शिः ⚠ verify) + *num* augment (7.1.72 नपुंसकस्य झलचः ⚠ verify); the Vedic bare *-ā* = *suluk* of the ending in *chandas* under **7.1.39 सुपां सुलुक्…** (verified). Both documented as options.
15. **Distribution:** *viśvā* neuter (Nom 84 + Acc 289) = 373 neuter-plural tokens; *viśvāni* 115 — **both in the Ṛgveda**, the bare *-ā* far more frequent for this high-frequency word. (The 470 total *viśvā* plural tokens split Neut 373 / Fem 97; the neuter subset is isolated here.)
16. **Figure-ready:** *PL-07 · विश्वा (neut.pl) ↔ विश्वानि · MAT+REL+ARR · bare -ā at the pāda-head, -āni at the cadence — weight placed by design within one verse.*
17. **Confidence:** **Strong** — both forms in the RV in large numbers, with a visible within-verse weight distribution.

---

### PL-12 — तृतीया बहुवचनम्, अकारान्त — रुद्रैः / रुद्रेभिः (*rudraiḥ / rudrebhiḥ*)

1. **Verification result:** **Confirmed** — *rudrebhiḥ* (*-ebhiḥ*) and *rudraiḥ* (*-aiḥ*) both occur; they even share the same Ṛgvedic hymn (3.32).
2. **Exact passage (unaccented, DCS):** माध्यन्दिने सवने वज्रहस्त पिबा रुद्रेभिः सगणः सुशिप्र — *mādhyandine savane vajrahasta pibā rudrebhiḥ sagaṇaḥ suśipra* (ṚV 3.32.2).
3. **Citation:** Ṛgveda 3.32.2 (*rudrebhiḥ*, to Indra); *rudraiḥ* at ṚV 3.32 and Maitrāyaṇī 2.8.1 (*sajū rudraiḥ*). Corpus: DCS. Printed: Aufrecht I; MS in the von Schroeder edition.
4. **Padaccheda:** editorial — *mādhyandine | savane | vajrahasta | piba | rudrebhiḥ | sagaṇaḥ | suśipra* (Śākala *padapāṭha* for the authoritative split).
5. **IAST:** *mādhyandine savane vajrahasta pibā rudrebhiḥ sagaṇaḥ suśipra*.
6. **Translation:** literal — "at the midday pressing, O mace-in-hand, drink with the Rudras, with your troop, O fair-jawed one"; readable — "At the noon pressing, thunderbolt in hand, drink alongside the Rudras with your host, fair-lipped Indra."
7. **Target form:** *rudrebhiḥ* — *akārānta* masculine, **तृतीया विभक्ति बहुवचनम्** (instrumental plural), the *-ebhiḥ* ending.
8. **Laukika counterpart:** *rudraiḥ* — same noun, same case/number; the contracted *-aiḥ* (*a + bhis → ais*) instead of *-ebhiḥ*.
9. **Syllable analysis:** *rud-re-bhiḥ* = 3σ; *rud-raiḥ* = 2σ. The *-ebhiḥ* is one syllable heavier.
10. **Laghu-guru:** *rudrebhiḥ* = **G G G**; *rudraiḥ* = **G G**. A full *guru* difference.
11. **Svara:** instrumental-plural accent; **Open** — accented edition required.
12. **Local function:** in the *triṣṭubh* pāda the 3σ *rudrebhiḥ* fills the metre where the 2σ *rudraiḥ* would leave it short; the retained *-bhiḥ* also keeps the instrumental morpheme audible and shared with the other *-bhiḥ* instrumentals of the domain (REL).
13. **DV codes:** **MAT Confirmed** (2σ vs 3σ); **SON Confirmed** (*-ebhiḥ* vs *-aiḥ*); **REL Confirmed** (the *-bhiḥ* instrumental morpheme is transparent and cross-paradigm); **AUD Probable** (extra syllable = redundancy); **SVR Open**.
14. **Indic documentation:** **7.1.9 अतो भिस ऐस्** (*ato bhisa ais*, verified) documents *a + bhis → ais* → *rudraiḥ*; the retention of *-bhis* (→ *rudrebhiḥ*) is the Vedic option under **7.1.39 सुपां सुलुक्…** (verified). Both endings are Pāṇini's documented alternatives, one marked *chandasi*.
15. **Distribution:** *rudrebhiḥ* 5× / *rudraiḥ* 6× (+ *rudrais* 1×) in the Vedic Saṃhitās — **near-parity, and both in the RV** (with *rudraiḥ* also in the Maitrāyaṇī). The cleanest coexistence case: two instrumental-plural endings side by side in the calibrant, one even within the same hymn family.
16. **Figure-ready:** *PL-12 · रुद्रेभिः (instr.pl) ↔ रुद्रैः · MAT+SON+REL · the -ebhiḥ fills the triṣṭubh and keeps the -bhiḥ morpheme audible; the -aiḥ contracts (Pāṇini 7.1.9). Both in the calibrant.*
17. **Confidence:** **Strong** — verified sūtra (7.1.9), near-equal counts, coexistence within the RV.

---

### DU-04 — ईकारान्त स्त्रीलिङ्ग द्विवचनम् — देव्यौ / देवी (*devyau / devī*)

1. **Verification result:** **Partial / Class B.** The *ī*-ending dual **देवी (*devī*)** is **Confirmed** in the Ṛgveda (tagged `Nom Fem Dual`). The *laukika* **देव्यौ (*devyau*)** is **NOT FOUND** in the searched Vedic Saṃhitās.
2. **Exact passage (unaccented, DCS):** अवन्तु नः पितरः सुप्रवाचनाः उत देवी देवपुत्रे ऋतावृधा — *avantu naḥ pitaraḥ su-pravācanāḥ uta devī deva-putre ṛtāvṛdhā* (ṚV 1.106.3; the two divine daughters / Heaven-and-Earth pair).
3. **Citation:** Ṛgveda 1.106.3; dual *devī* also at 2.31, 10.64. *devyau*: NOT FOUND (checked all seven Vedic Saṃhitā folders, `Number=Dual`, string *devyau* — zero). Corpus: DCS. Printed: Aufrecht I.
4. **Padaccheda:** editorial — *avantu | naḥ | pitaraḥ | su-pravācanāḥ | uta | devī | deva-putre | ṛtāvṛdhā* (Śākala *padapāṭha* for the authoritative split; note *devaputre* is a dual vocative dvandva).
5. **IAST:** *avantu naḥ pitaraḥ su-pravācanāḥ uta devī deva-putre ṛtāvṛdhā*.
6. **Translation:** literal — "may the fathers, well-proclaiming, help us, and the two devīs, having devas for sons, strengthened by *ṛta*"; readable — "May our well-spoken forefathers aid us, and the two goddesses whose children are devas, nourished by cosmic order."
7. **Target form:** *devī* — *īkārānta* feminine, **प्रथमा/संबोधन द्विवचनम्** (nominative/vocative dual), the *ī*-ending dual (surface *-ī*).
8. **Laukika counterpart:** *devyau* — same noun, same case/number; the Classical *-yau* dual, formed by *ī → y* before the *-au* ending. What stays: the *dev-* base and the dual meaning. What changes: the *ī* resolves to the semivowel *y* and takes overt *-au*.
9. **Syllable analysis:** *de-vī* = 2σ; *dev-yau* = 2σ. Equal count.
10. **Laghu-guru:** *devī* = **G G**; *devyau* = **G G**. No weight change; the difference is sonomeric (*-ī* vs *-yau*).
11. **Svara:** *nadī*-class feminine dual accent; **Open** — accented edition required.
12. **Local function:** the *ī*-dual *devī* is what the verse uses; the *laukika* *-yau* would give a more distinct dual (it cannot be confused with the *ī*-stem nominative singular *devī*). The *bhāṣā* domain later takes that disambiguation systematically — but the calibrant does not need it, because context and accent carry the dual.
13. **DV codes:** **SON Confirmed** (once *devyau* is compared); **REL Probable** (the *laukika* *-yau* is the more distinguishable dual, but this is a property of the *derived* form, not of the Vedic passage); **MAT Rejected** (no weight change); **SVR Open**. The Vedic passage itself supports only that *devī* is the calibrant dual.
14. **Indic documentation:** the *-yau* form is the *iyaṅ/yaṇ* outcome — **6.1.77 इको यणचि** (*i → y* before a vowel) / **6.4.77 …इयङुवङौ** (⚠ verify) — a documented sandhi, so *devyau* is **derived, not reconstructed**. The Vedic *ī*-dual is the *nadī*-class dual (Pāṇini's *ṅī* feminine paradigm; exact sūtra ⚠ verify).
15. **Distribution:** *devī* (Dual) 23× in the Vedic Saṃhitās (all RV in the sample); *devyau* 0× in the Vedic Saṃhitās. This is a genuine **Class B** case: the calibrant records one member; the grammar derives the other.
16. **Figure-ready:** *DU-04 · देवी (dual) ↔ देव्यौ (NOT FOUND in the Veda) · SON · the laukika -yau is derived by documented ī→y sandhi (Pāṇini 6.1.77), not reconstructed.*
17. **Confidence:** **Moderate–Strong** for the finding as stated (Vedic *devī* strongly attested; *devyau* honestly absent). The DV design-function is weaker because only one member is in the calibrant — the contrast is derivational, not performance-selected.

---

### PL-03 — ईकारान्त स्त्रीलिङ्ग प्रथमा बहुवचनम् — देव्यः / देवीः (*devyaḥ / devīḥ*)

1. **Verification result:** **Partial / Class B.** The *ī*-ending nominative plural **देवीः (*devīḥ*)** is **Confirmed** in the Ṛgveda. The *laukika* **देव्यः (*devyaḥ*)** is **NOT FOUND** in the searched Vedic Saṃhitās.
2. **Exact passage (unaccented, DCS):** इन्द्रः याः वज्री वृषभः रराद ताः आपः देवीः इह माम् अवन्तु — *indraḥ yāḥ vajrī vṛṣabhaḥ rarāda tāḥ āpaḥ devīḥ iha mām avantu* (ṚV 7.49.1; the Waters as *devīḥ*).
3. **Citation:** Ṛgveda 7.49.1 (the *āpaḥ devīḥ*, divine Waters). *devyaḥ*: NOT FOUND (all seven Saṃhitā folders, `Nom Fem Plur`, string *devyaḥ / devyas* — zero). Corpus: DCS. Printed: Aufrecht II.
4. **Padaccheda:** editorial — *indraḥ | yāḥ | vajrī | vṛṣabhaḥ | rarāda | tāḥ | āpaḥ | devīḥ | iha | mām | avantu* (Śākala *padapāṭha* for the authoritative split).
5. **IAST:** *indraḥ yāḥ vajrī vṛṣabhaḥ rarāda tāḥ āpaḥ devīḥ iha mām avantu*.
6. **Translation:** literal — "which (waters) Indra the mace-bearing bull released, those divine waters, may they help me here"; readable — "The waters that Indra, the thunderbolt-bull, set free — those divine waters, may they favour me here."
7. **Target form:** *devīḥ* — *īkārānta* feminine, **प्रथमा विभक्ति बहुवचनम्** (nominative plural), the *ī*-ending plural (*-īḥ*).
8. **Laukika counterpart:** *devyaḥ* — same noun, same case/number; the Classical *-yaḥ*, formed by *ī → y* before *-aḥ*. Base and meaning identical; the *ī* resolves to *y* and the ending surfaces as *-aḥ*.
9. **Syllable analysis:** *de-vīḥ* = 2σ; *dev-yaḥ* = 2σ. Equal count.
10. **Laghu-guru:** *devīḥ* = **G G**; *devyaḥ* = **G G**. No weight change; the difference is sonomeric (*-īḥ* vs *-yaḥ*).
11. **Svara:** *nadī*-class feminine plural accent; **Open** — accented edition required.
12. **Local function:** the calibrant uses the transparent *ī*-plural *devīḥ*, whose long *-ī-* keeps the feminine *ī*-class audible right up to the *-ḥ*. The *laukika* *-yaḥ* compresses the *ī* to a glide; the *bhāṣā* domain accepts that compression, the calibrant does not.
13. **DV codes:** **SON Confirmed** (once *devyaḥ* is compared); **REL Probable** (the full *-īḥ* keeps the *ī*-class marker audible); **MAT Rejected** (no weight change); **SVR Open**. As with DU-04, the Vedic passage supports only that *devīḥ* is the calibrant plural.
14. **Indic documentation:** *devyaḥ* is the *yaṇ*-sandhi outcome under **6.1.77 इको यणचि** (⚠ verify) — **derived, not reconstructed**. The Vedic *-īḥ* plural is the *nadī*-class nominative plural (Pāṇini's *ṅī* paradigm + *jas → -ḥ* with long *ī*; exact chain ⚠ verify).
15. **Distribution:** *devīḥ* 79× + *devīs* 6× = 85 in the Vedic Saṃhitās; *devyaḥ* 0×. A second clean **Class B** case, parallel to DU-04.
16. **Figure-ready:** *PL-03 · देवीः (nom.pl) ↔ देव्यः (NOT FOUND in the Veda) · SON · the laukika -yaḥ is derived by documented ī→y sandhi (Pāṇini 6.1.77), not reconstructed.*
17. **Confidence:** **Moderate–Strong** — Vedic *devīḥ* strongly attested; *devyaḥ* honestly absent; contrast is derivational.

---

### DU-09 — first/second-person pronoun dual — the five-way distinction

1. **Verification result:** **Confirmed with correction.** The Vedic dual pronoun carries a distinct **nominative** *yuvam / āvam* separate from the **accusative** *yuvām / āvām*, plus a rare **ablative** *yuvat* — distinctions the *laukika* dual collapses. The bare 1st-person *āva-* case-forms are largely in the Yajus prose Saṃhitās, not the RV; the RV leans on the enclitics *vām / nau*.
2. **Exact passages (unaccented, DCS):**
   - Nom. 2du: युवम् अत्रये ऽवनीताय तप्तम्… अश्विनाव् अधत्तम् — *yuvam atraye 'vanītāya taptam … aśvināv adhattam* (ṚV 1.118.7).
   - Acc. 2du: आ वां पतित्वं सख्याय जग्मुषी यो षावृणीत जेन्या युवां पती — *… yoṣāvṛṇīta jenyā yuvām patī* (ṚV 1.119.5).
   - Abl. 2du: नान्या युवत् प्रमतिर् अस्ति मह्यम् — *nānyā yuvat pramatir asti mahyam* (ṚV 1.109.1).
   - Nom. 1du: आवम् इदं भविष्यावो यद् आदित्या इति — *āvam idaṃ bhaviṣyāvo yad ādityā iti* (Maitrāyaṇī 1.6.12).
3. **Citation:** Ṛgveda 1.118.7 (*yuvam*), 1.119.5 (*yuvām*), 1.109.1 (*yuvat*) — all Aśvin/dual-deity hymns; Maitrāyaṇī 1.6.12 (*āvam*). Corpus: DCS. Printed: Aufrecht I; MS von Schroeder.
4. **Padaccheda:** editorial where shown; the Śākala/MS *padapāṭha* to be consulted for authoritative splits (the pronoun clitics *vām/nau* are separately padded in the tradition).
5. **IAST:** as in point 2.
6. **Translation:** e.g. ṚV 1.118.7 literal — "you two (nom.) set warm strength for the cast-down Atri, O Aśvins"; readable — "You two Aśvins granted warm vigour to Atri when he was cast down." ṚV 1.119.5 — "the noble maiden chose you two (acc.) as husbands." MS 1.6.12 — "'We two (nom.) shall become this,' said the Ādityas."
7. **Target forms:** first/second-person pronoun **द्विवचनम्** (dual). The *vaidika* inventory the corpus confirms:
   - Nom.: *yuvam* (2du), *āvam* (1du).
   - Acc.: *yuvām* (2du), *āvām* (1du).
   - Inst./Dat./Abl.: *yuvābhyām / āvābhyām* (the *-bhyām* forms).
   - Abl. (distinct): *yuvat* (2du).
   - Gen./Loc.: *yuvoḥ / āvayoḥ* (the *-oḥ* forms).
   - Enclitics: *vām* (2du), *nau* (1du).
8. **Laukika counterpart:** Classical Sanskrit reduces the dual to **three combined form-groups** — *yuvām/āvām* (nom.+acc.), *yuvābhyām/āvābhyām* (inst.+dat.+abl.), *yuvayoḥ/āvayoḥ* (gen.+loc.) — plus the enclitics *vām/nau*. The Vedic **nominative** *yuvam/āvam* and the ablative *yuvat* have no separate slot in the *laukika* paradigm.
9. **Syllable analysis:** *yu-vam* = 2σ; *yu-vām* = 2σ; *yu-vat* = 2σ. The nom./acc. contrast is carried on syllable 2 (*-vam* vs *-vām*).
10. **Laghu-guru:** *yuvam* = **L G** (*-vam* heavy by the *m*); *yuvām* = **L G** (*-vām* heavy by length). Same weight profile — so nom. vs acc. is distinguished by **vowel quality/length identity of the coda**, an audible *-vam / -vām* contrast, not by weight.
11. **Svara:** the enclitics *vām/nau* are inherently unaccented (*anudātta*); the full forms *yuvam/yuvām* bear accent. This accent contrast is real and load-bearing but **Open** here — requires the accented edition to show per-passage.
12. **Local function:** the calibrant keeps subject (*yuvam*, "you two act") and object (*yuvām*, "someone acts on you two") **audibly separate** — critical in the Aśvin hymns, which are dense with "you two did X for me / I invoke you two." The *laukika* domain, less dependent on unaccompanied audition, merges them.
13. **DV codes:** **SEM Confirmed** (a finer meaning distinction — nom. vs acc. — preserved in the *vaidika* system and lost in the *laukika*); **REL Confirmed** (subject/object audibly separated); **AUD Probable** (more distinct forms = more error-detection surface); **SVR Probable** (accented full forms vs *anudātta* enclitics); **MAT Open**.
14. **Indic documentation:** Pāṇini documents the dual pronoun stems by **7.2.92 युवावौ द्विवचने** (⚠ verify — *yuṣmad → yuva*, *asmad → āva* before dual endings) and the enclitics *vām/nau* by **8.1.21/8.1.22** (⚠ verify). The Vedic distinct nominative and ablative are documented as *chandasi* options in the pronominal section (exact sūtras ⚠ verify). Pāṇini **records** the richer Vedic set; he does not invent it.
15. **Distribution (Vedic Saṃhitās):** *yuvam* 91×, *yuvām* 14×, *yuvoḥ* 14×, *yuvābhyām* 3×, *yuvat* 1× (all with RV loci); *vām* 351× (enclitic, dominant). 1st-person: *nau* 31× (enclitic, dominant); *āvām* 1× (KS), *āvam* 1× (MS), *āvābhyām* 1× (KS), *āvayoḥ* 1× (TS). **Correction to the plan:** the full 1st-person *āva-* forms are vanishingly rare and sit in the Yajus prose Saṃhitās, not the RV; the RV realizes the 1st dual almost entirely through the enclitic *nau*. The 2nd-person full forms (*yuvam/yuvām*) are, by contrast, common in the RV. State the five-way as a **system-level Vedic distinction unevenly filled by word and Veda**, not as a full paradigm attested for both persons in the RV.
16. **Figure-ready:** *DU-09 · युवम् (nom) vs युवाम् (acc) vs युवत् (abl) ↔ laukika युवाम् (nom+acc) · SEM+REL · the calibrant keeps subject/object/source audibly separate where the worldly dual merges them.*
17. **Confidence:** **Strong** for the 2nd-person nom./acc. distinction and the ablative *yuvat*; **Moderate** for the 1st-person full forms (rare, Yajus-prose, not RV). The corrected framing is well-supported.

---

## Table 1 — Evidence

| ID | Exact Vedic form | Passage (DCS) | Padaccheda | Laukika form | Indic source | Strength |
|---|---|---|---|---|---|---|
| SG-01 | यज्ञा *yajñā* (Ins sg) | ṚV 6.48.1 *yajñā yajñā vaḥ agnaye* | ed.; Śākala PP | यज्ञेन *yajñena* | 7.1.39 सुपां सुलुक् ✓ | Strong |
| SG-02 | मनीषा *manīṣā* (Ins sg) | ṚV 1.61.2 *hṛdā manasā manīṣā* | ed.; Śākala PP | मनीषया *manīṣayā* | 7.1.39 सुपां सुलुक् ✓ | Strong |
| SG-10 | अग्ना *agnā* (Loc sg) | ṚV 1.124.1 *samidhāne agnā* | ed.; Śākala PP | अग्नौ *agnau* | 7.1.39 ✓ / 7.3.119 ⚠ | Strong |
| DU-01 | देवा *devā* (dual) | ṚV 10.63.2 *nāmāni devā uta* | ed.; Śākala PP | देवौ *devau* | 7.1.39 (āṄ dual) ✓ | Strong |
| PL-01 | देवासः *devāsaḥ* (Nom pl) | ṚV 10.63.4 *bṛhad devāso amṛtatvam* | ed.; Śākala PP | देवाः *devāḥ* | 7.1.50 आज्जसेरसुक् ✓ | Strong |
| PL-07 | विश्वा *viśvā* (Neut pl) | ṚV 10.63.2 *viśvā hi vo* | ed.; Śākala PP | विश्वानि *viśvāni* | 7.1.39 ✓ / 7.1.72 ⚠ | Strong |
| PL-12 | रुद्रेभिः *rudrebhiḥ* (Ins pl) | ṚV 3.32.2 *pibā rudrebhiḥ sagaṇaḥ* | ed.; Śākala PP | रुद्रैः *rudraiḥ* | 7.1.9 अतो भिस ऐस् ✓ | Strong |
| DU-04 | देवी *devī* (dual) | ṚV 1.106.3 *devī devaputre* | ed.; Śākala PP | देव्यौ *devyau* **NOT FOUND** | 6.1.77 इको यणचि ⚠ | Mod–Strong |
| PL-03 | देवीः *devīḥ* (Nom pl) | ṚV 7.49.1 *āpaḥ devīḥ iha* | ed.; Śākala PP | देव्यः *devyaḥ* **NOT FOUND** | 6.1.77 इको यणचि ⚠ | Mod–Strong |
| DU-09 | युवम्/युवाम्/युवत् *yuvam/yuvām/yuvat* | ṚV 1.118.7 / 1.119.5 / 1.109.1 | ed.; Śākala PP | युवाम् (nom+acc merged) | 7.2.92 युवावौ द्विवचने ⚠ | Strong (2nd p.) |

✓ = sūtra verified this session; ⚠ = best-identified documenting sūtra, verify against Aṣṭādhyāyī/Kāśikā before print. PP = *padapāṭha*.

## Table 2 — Designed function

| ID | Syllable change | Weight change | Svara effect | Confirmed DV | Open/Rejected DV | Local explanation |
|---|---|---|---|---|---|---|
| SG-01 | 2σ ↔ 3σ | drops final *laghu* | Open | MAT, SON | SVR-open; AUD-open | bare *-ā* powers the doubled *yajñā yajñā / girā girā* iteration |
| SG-02 | 3σ ↔ 4σ | drops medial *laghu* | Open | MAT, RES, SON | SVR-open; REC-open | contracted *-ā* completes the *hṛdā/manasā/manīṣā* rhyme |
| SG-10 | 2σ = 2σ | **none** | Open | SON | **MAT-Rejected**; REL-open | pure vowel-quality contrast (*-ā*/*-au*), not metrical |
| DU-01 | 2σ = 2σ | **none** | Open | SON, REL | **MAT-Rejected**; AUD-prob | *laukika -au* is the more distinguishable dual |
| PL-01 | 2σ ↔ 3σ | adds *guru* | Open | MAT, REL, AUD, SON | SVR-open; REC-prob | *-āsaḥ* augment = extra syllable + audible plural check |
| PL-07 | 2σ ↔ 3σ | adds final *laghu* | Open | MAT, REL, ARR, SON | SVR-open | bare *-ā* at pāda-head, *-āni* at cadence — weight by design |
| PL-12 | 2σ ↔ 3σ | adds *guru* | Open | MAT, SON, REL | AUD-prob; SVR-open | *-ebhiḥ* fills *triṣṭubh*, keeps *-bhiḥ* morpheme audible |
| DU-04 | 2σ = 2σ | none | Open | SON | REL-prob; **MAT-Rejected** | *laukika -yau* derived by *ī→y* sandhi; Vedic keeps *-ī* |
| PL-03 | 2σ = 2σ | none | Open | SON | REL-prob; **MAT-Rejected** | *laukika -yaḥ* derived by *ī→y* sandhi; Vedic keeps *-īḥ* |
| DU-09 | 2σ = 2σ | none | accented full vs *anudātta* enclitic | SEM, REL | AUD-prob; SVR-prob; MAT-open | calibrant keeps nom/acc/abl audibly separate |

## Table 3 — Figure copy

| ID | Vaidika | Laukika | DV | Compact explanation |
|---|---|---|---|---|
| SG-01 | यज्ञा | यज्ञेन | MAT·SON | bare *-ā* instrumental drops a light syllable for iterative pādas |
| SG-02 | मनीषा | मनीषया | MAT·RES | contracted *-ā* closes a three-instrumental rhyme |
| SG-10 | अग्ना | अग्नौ | SON | same weight, pure vowel-quality contrast — variation need not be metrical |
| DU-01 | देवा | देवौ | SON·REL | *-au* is the more distinguishable dual, at equal weight |
| PL-01 | देवासः | देवाः | MAT·REL·AUD | *-āsaḥ* adds a syllable and an audible plural-boundary check |
| PL-07 | विश्वा | विश्वानि | MAT·REL·ARR | light *-ā* at the head, *-āni* at the cadence — weight placed by design |
| PL-12 | रुद्रेभिः | रुद्रैः | MAT·SON·REL | *-ebhiḥ* fills the metre and keeps the instrumental morpheme audible |
| DU-04 | देवी | देव्यौ* | SON | *laukika* dual derived by *ī→y* sandhi (*devyau* not in the Veda) |
| PL-03 | देवीः | देव्यः* | SON | *laukika* plural derived by *ī→y* sandhi (*devyaḥ* not in the Veda) |
| DU-09 | युवम्/युवाम्/युवत् | युवाम् (merged) | SEM·REL | calibrant separates subject/object/source; worldly dual merges them |

\* *laukika* form NOT FOUND in the searched Vedic Saṃhitās — derived by documented rule, shown for contrast.

---

## Final synthesis

**1. Examples that strongly support designed variation.** Seven of the ten, with function verified in the actual passage:
- **PL-01 (देवासः)** and **PL-12 (रुद्रेभिः)** are the strongest — each has an **exact, verified Pāṇinian sūtra** (7.1.50, 7.1.9), a clear metrical + redundancy function, and coexistence with the counterpart in the calibrant (*rudrebhiḥ / rudraiḥ* even share the RV 3.32 hymn family).
- **SG-02 (मनीषा)** and **PL-07 (विश्वा)** show the design *inside a single verse* (the *hṛdā/manasā/manīṣā* rhyme; the *viśvā*-head vs *-āni*-cadence weighting) — the cleanest demonstrations that the choice is compositional, not free.
- **SG-01 (यज्ञा)** supports it once the phantom third form *yajñenā* is dropped.
- **DU-09 (युवम्/युवाम्)** supports it on a different axis — the *vaidika* system carrying **more distinctions** (nom≠acc, plus abl *yuvat*) than the *laukika*.

**2. Examples showing a real difference whose purpose remains open.** 
- **SG-10 (अग्ना)** and **DU-01 (देवा)** are real and confirmed, but they carry **no weight change** — the design is sonomeric (quality/disambiguation), not metrical. They are valuable precisely as the counter-cases to a "meter explains everything" reading, but their positive *function* (why *-ā* here, *-au* there) is **Open** without accent and fuller distributional study. Keep them, and frame them honestly as the sonomeric axis.
- **DU-04 (देवी)** and **PL-03 (देवीः)** are **Class B**: the design contrast is *derivational* (the *laukika -y-* form is produced by sandhi), not a performance-selected calibrant alternation. Their "purpose" is real but different in kind — they show *bhāṣā* regularizing what the calibrant keeps transparent.

**3. Examples that should be removed or reframed.** None removed. Two **reframings** are mandatory:
- Drop **यज्ञेना (*yajñenā*)** from SG-01 — NOT FOUND as a distinct instrumental; present the pair as *yajñā ~ yajñena*.
- Correct **DU-09**: the full **1st-person *āva-* forms are Yajus-prose and vanishingly rare, not RV**; the RV realizes the 1st dual through the enclitic *nau*. State the five-way as a *system-level distinction unevenly filled by word and Veda*, carried in the RV chiefly by the 2nd person.
- Mark **DU-04 / PL-03** explicitly as **Class B (laukika counterpart NOT FOUND; derived by rule)** so the appendix does not imply *devyau/devyaḥ* stand in the Veda.

**4. Stronger replacement examples found.** The corpus surfaced a **cluster worth its own figure: Ṛgveda 10.63.2–4** (a Viśvedevāḥ hymn) carries *viśvā* (neut. pl.), *devā* (dual), and *devāso* (extended nom. pl.) within three verses — three designed variations in one short passage. This is a better single-verse showcase than any isolated pair and should anchor the appendix's opening figure. Also note **ṚV 1.61.2** (*hṛdā / manasā / manīṣā*, triple bare-*-ā* instrumental) and **ṚV 6.48.1** (*yajñā yajñā / girā girā*) as ready-made iteration exhibits.

**5. DV codes that recur most.** **SON** (9/10 — sonomeric distinguishability is the through-line) and **MAT** (6/10, and diagnostically *Rejected* in 3, which is itself informative). **REL** (7/10) is the next most frequent — audible grammatical boundaries. **SVR is Open across all ten** because the DCS is unaccented; closing the SVR column is the single biggest remaining evidence gap. **RES, ARR, AUD, SEM, REC** each carry 1–3 confirmed cases and give the appendix its variety.

**6. Do the ten collectively support separate read-only / read-write deployment?** **Yes, and with a sharper structure than the plan assumed.** The read-only (*calibrant*) vs read-write (*worldly*) distinction is supported on **three different mechanisms**, not one:
- *Class A coexistence* (7 cases): both forms in the calibrant, selected in performance by metre/emphasis/disambiguation — the calibrant is a **richer option-set**.
- *Class B derivation* (DU-04, PL-03): the calibrant keeps the transparent *ī*-form; *bhāṣā* derives the compressed *-y-* form by documented sandhi — the worldly domain **regularizes**.
- *Resolution asymmetry* (DU-09): the calibrant keeps **more distinct forms** (nom≠acc) than the worldly dual — the calibrant is the **higher-resolution instrument**.
All three are the same thesis (one architecture, two deployments) and **none requires reconstruction** — every worldly form is either co-present in the calibrant or derived from it by a stated rule. That is the appendix's payload.

**7. Remaining research gaps (precise).**
- **Accent (SVR) for all ten** — pull *udātta/anudātta/svarita* from van Nooten–Holland (RV) and the Śākala *padapāṭha*; this is the one column the DCS cannot fill and it currently caps every SVR code at Open.
- **Padapāṭha splits** — replace the editorial *padaccheda* in Table 1 with the authoritative Śākala (and MS/TS for the non-RV loci) word-splits.
- **⚠-flagged sūtras** — verify **7.3.119** (SG-10 *-au* locative), **7.1.20 / 7.1.72** (PL-07 *-āni*), **6.1.77 / 6.4.77** (DU-04, PL-03 *-y-* sandhi), **7.2.92 युवावौ द्विवचने** and **8.1.21–22** (DU-09) against the Aṣṭādhyāyī/Kāśikā. The three core sūtras (7.1.9, 7.1.39, 7.1.50) are verified.
- **Metrical scansion of the full pāda** — points 9–10 give the isolated-word weight reliably; the *complete*-pāda scansion (and thus the metrical claim in point 12) needs the metrically-restored text for SG-01, PL-01, PL-12, PL-07.
- **DU-09 1st-person forms** — confirm the *āva-* count and Yajus-prose distribution against the KS/MS/TS critical editions; the DCS gives 1 token each and that should be double-checked, not generalized.
- **Class B check in other *ī*-stems** — test whether *any* *-y-* feminine dual/plural (*devyau/devyaḥ*-type) occurs anywhere in the wider Vedic corpus (Brāhmaṇa prose included) before stating the NOT FOUND as corpus-wide rather than Saṃhitā-wide.
