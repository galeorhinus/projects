# Chapters 11–12 — Vedic Grammatical Breadth: Verification Research

**Created:** 2026-08-20
**Status:** Research document. Not manuscript prose. No manuscript file was edited.
**Author of this document:** Claude (research pass)
**Companion planning document:** `working/10_active/as_ch11_ch12_vedic_engineering_rewrite_plan_codex.md`

---

## 0. Method, corpus, and the limits of this verification

### 0.1 What was searched

Every claim marked **verified** below was checked against a local, complete,
morphologically annotated Ṛgveda:

| Resource | Location | What it gives |
|---|---|---|
| DCS CoNLL-U dump of the Ṛgveda | `analysis/ganah/data/raw/dcs/dcs/data/conllu/files/Ṛgveda/` (1,028 chapter files) | Per-token lemma, part of speech, and morphological features (case, gender, number, person, tense, mood, VerbForm) |
| DCS `pada-and-analysis.dat` | `analysis/ganah/data/raw/dcs/dcs/data/rigveda/` (39,830 pāda lines) | Stanza- and pāda-precise citation (`book.hymn.stanza + pāda letter`) with pāda text and lemmata |

Both are from Oliver Hellwig's **Digital Corpus of Sanskrit** (DCS), CC BY 4.0,
already vendored in this repository for the Chapter 10 / Appendix Part 6
*gaṇa* analysis. Source: <http://www.sanskrit-linguistics.org/dcs/index.php>.
Morphosyntactic annotation of the Vedic portion derives from the Vedic
Treebank (Hellwig, Hettrich, Modi, Pinkal 2018–2020); see
<https://universaldependencies.org/treebanks/sa_vedic/index.html>.

A token index of **179,345 Ṛgvedic word-occurrences** was built for this pass
(script and index retained in the session scratchpad; see §11 for the
recommendation to commit them into `analysis/`).

### 0.2 Search limitations — read before citing anything below as "not found"

These bound every negative finding in this document:

1. **The Ṛgveda only.** The token index covers the Ṛgveda. It does **not**
   cover the Yajurveda, Sāmaveda, Atharvaveda, Brāhmaṇas, Āraṇyakas, or
   Upaniṣads. Every "not found" below means **not found in the Ṛgveda**, and
   must be written that way. The DCS dump does contain an Atharvaveda
   (Śaunaka) and several Brāhmaṇa/Upaniṣad texts that were **not** searched in
   this pass — see §10.1.
2. **Sandhi surface vs. unsandhied form.** The index records both the surface
   (sandhi-joined) form and DCS's `Unsandhied=` padapāṭha form. Searches
   matched either. A form present only inside an unresolved compound or under
   an unusual sandhi treatment could still be missed.
3. **Metrical lengthening is a real distinction.** Vedic final vowels are
   frequently lengthened for meter (`bhavatha` → `bhavathā`). A search for the
   exact form will not match the lengthened variant. Where this occurred it is
   flagged explicitly (see §2, `bhavatha`).
4. **DCS annotation is not infallible.** The DCS readme states the mapping in
   `pada-and-analysis.dat` "was performed automatically, so there may be errors."
   The CoNLL-U analyses are single-annotator verified. Where DCS's grammatical
   analysis conflicts with a standard grammar, this document records **both**
   and does not silently choose (see §7).
5. **Stanza numbers are missing from part of the CoNLL-U dump.** Some chapter
   files lack the `sent_counter` field, yielding chapter-level citations only
   (`RV 10.28` rather than `RV 10.28.3`). Every citation in this document was
   therefore re-checked against `pada-and-analysis.dat`, which is
   stanza-and-pāda precise. Citations below carry the pāda letter wherever
   established.
6. **Voice (parasmaipada / ātmanepada) is not tagged.** DCS tags `Voice=Pass`
   on 597 tokens and nothing else. Active/middle voice must be established from
   the ending itself against a grammar, not read off the corpus. Voice claims
   below are marked accordingly.

### 0.3 Terminology in this document

Per the standing rules: *dhātuḥ* (never *root*), no *stem*, no
*archaic / primitive / early / late / transitional*, no chronological framing of
*vaidika* and *laukika*, and no claim that Pāṇini created any form. Where a
cited external source uses *root*, its wording is preserved inside the
quotation only.

---

## 1. Executive summary — what can be demonstrated securely

**The Ṛgveda alone preserves grammatical breadth far exceeding what Chapters 11
and 12 currently deploy.** The corpus-wide counts below are from the 179,345-token
index and are the strongest single piece of evidence for the calibrant claim.

### 1.1 Person × number is completely filled

Every one of the nine person–number cells is populated by finite verbs in the
Ṛgveda:

| | *ekavacanam* (Sing) | *dvivacanam* (Dual) | *bahuvacanam* (Plur) |
|---|---:|---:|---:|
| **First person** | 1,048 | 29 | 1,561 |
| **Second person** | 5,532 | 1,376 | 1,229 |
| **Third person** | 8,153 | 355 | 4,399 |

No cell is empty. The dual — the category most often assumed to be sparse — carries
1,760 finite verb occurrences.

### 1.2 Mood and tense breadth

DCS mood tags across Ṛgvedic finite verbs:

| Mood tag | Count | Plain description |
|---|---:|---|
| `Ind` | 13,226 | indicative statement |
| `Imp` | 6,112 | imperative / command |
| `Jus` | 1,717 | jussive–injunctive |
| `Sub` | 1,622 | subjunctive |
| `Opt` | 970 | optative |
| `Prec` | 32 | precative / benedictive |
| `Cond` | 3 | conditional |

Tense tags: `Pres` 18,647 · `Past` 9,531 · `Impf` 1,496 · `Fut` 224 ·
`Plp` 91 · `Pqp` 28.

Non-finite forms: participles 8,372 · infinitives 796 · gerundives 258 ·
converbs (absolutives) 189.

**This is the core finding.** Present, past, imperfect, future, pluperfect,
six moods, participles, infinitives, gerundives, and absolutives all occur
inside one corpus. That is not a vocabulary list. It is a working grammatical
system, and it is what allows the Vedas to function as the calibrant rather
than as an archive of isolated words.

### 1.3 Nominal breadth

All eight *vibhaktis* occur, plus vocative and compound-member marking:

| *Vibhaktiḥ* | Tag | Count |
|---|---|---:|
| *prathamā* (nominative) | `Nom` | 32,877 |
| *dvitīyā* (accusative) | `Acc` | 29,533 |
| *ṣaṣṭhī* (genitive) | `Gen` | 11,201 |
| *tṛtīyā* (instrumental) | `Ins` | 8,023 |
| *sambodhana* (vocative) | `Voc` | 7,468 |
| *caturthī* (dative) | `Dat` | 6,250 |
| *saptamī* (locative) | `Loc` | 6,129 |
| — compound member | `Cpd` | 4,164 |
| *pañcamī* (ablative) | `Abl` | 1,366 |

### 1.4 The strongest single new finding

**⟪कृ⟫'s derived nominal family is already Ṛgvedic, including *saṃskṛta*.**

| Form | Citation | Analysis |
|---|---|---|
| **कर्मणः** (*karmaṇaḥ*) | RV 1.11.4 | *ṣaṣṭhī ekavacanam*, neuter — the deed |
| **कर्तृभिः** (*kartṛbhiḥ*) | RV 1.55.8 | *tṛtīyā bahuvacanam*, masculine — by the doers |
| **कर्त्वम्** (*kartvam*) | RV 1.10.2b | gerundive, *dvitīyā ekavacanam* neuter — what is to be done |
| **संस्कृतम्** (*saṃskṛtam*) | RV 5.76.2a | *dvitīyā ekavacanam* neuter |
| **संस्कृताः** (*saṃskṛtāḥ*) | RV 1.38.12 | participle, *prathamā bahuvacanam* masculine |
| **संस्कृतः** (*saṃskṛtaḥ*) | RV 8.33.9 | participle, *prathamā ekavacanam* masculine |
| **संस्कृते** (*saṃskṛte*) | RV 8.77.11 | participle, *prathamā dvivacanam* feminine |

Chapter 12 currently presents *karma*, *kartṛ*, *kārya*, and *saṃskāra* as a
*laukika* demonstration standing at a distance from the Vedic evidence. Three of
those four semantic slots — deed, agent, obligation — plus *saṃskṛta* itself are
**already in the Ṛgveda**, from the same atom, in several genders, numbers, and
cases. This converts the *kṛ* section from an assertion about generativity into
a demonstration of it inside the calibrant.

**Equally important, and a limit that must be stated:** ***prakṛti* and *vikṛti*
do not occur in the Ṛgveda.** Chapter 12's matrix presents *prakṛti* / *vikṛti* /
*saṃskṛti* as a set. Only the *saṃskṛ-* member is Ṛgvedic. The other two must be
presented as *laukika* formations built by the same procedure — which is the
honest and stronger version of the claim, because it shows the architecture
generating beyond the corpus rather than merely repeating it.

### 1.5 What cannot currently be demonstrated

- **A complete ten-*gaṇa* present-indicative paradigm from the Ṛgveda.** The
  90-slot ambition in `working/10_active.md` is not achievable from the Ṛgveda,
  and several of its "found" entries are wrong (§2). Two entire *gaṇa*
  representatives (⟪दिव्⟫ *dīvyati*, and the ⟪रुध्⟫ plural) fail outright.
- **Voice as a corpus-verifiable category.** Ātmanepada must be argued from the
  endings against a grammar; DCS does not tag it (§0.2.6).
- **A securely verbless Vedic sentence** was not established in this pass (§10).

---

## 2. Corrections required in `working/10_active.md`

Every one of the 62 substantive claims in that file was checked. The file's own
header states "Total Found: 25."

**Audit result: of the 25 claimed as found, 6 are wrong, and 9 forms the file
marks "Not found in Vedic corpus" do occur in the Ṛgveda.**

### 2.1 Claimed found, but the citation is wrong

| Form | File claims | Actual Ṛgvedic occurrence | Verdict |
|---|---|---|---|
| **भवति** (*bhavati*) | RV 10.85.34 | 37× in RV, e.g. **1.17.5c**, 1.28.1b, 1.55.4c | **Citation wrong.** RV 10.85.34 is *tṛṣṭam etat kaṭukam etat…* and contains no form of ⟪भू⟫. Use RV 1.17.5c — which is already the manuscript's own Chapter 11 citation. |
| **भवतः** (*bhavataḥ*) | RV 10.12.1 | 5× as 3rd dual: 1.162.19b, 2.27.15d, **10.12.1b**, 10.147.1c | **Citation correct but unverifiable as stated.** 10.12.1b does contain it. Retain, with pāda letter added. Note 1.96.7c is a *participle*, not a finite dual — do not count it. |
| **अत्सि** (*atsi*) | RV 10.28.3 | **10.28.3c** — *pacanti te vṛṣabhān atsi teṣām* | **Correct**; add pāda letter. |
| **कृणोषि** (*kṛṇoṣi*) | RV 7.81.4 | **7.81.4a** — *ucchantī yā kṛṇoṣi maṁhanā mahi* | **Correct**; add pāda letter. |
| **रुणद्धि** (*ruṇaddhi*) | RV 10.34.3 | **10.34.3a** — *dveṣṭi śvaśrūḥ apa jāyā ruṇaddhi* | **Correct**; add pāda letter. |
| **तनुते** (*tanute*) | RV 10.130.1 | 1.101.7b, 1.115.4d, **10.130.2a** | **Citation off by one stanza.** The form is at 10.130.**2**a, not 10.130.1. |
| **भवथ** (*bhavatha*) | RV 5.55.8 | RV 5.55.8c has **भवथा** (*bhavathā*, metrically lengthened); exact **भवथ** is at **3.54.17b** | **Form mismatch.** Under the "exact form must occur" rule, cite RV 3.54.17b. RV 5.55.8c may be cited separately as the metrically lengthened variant — which is itself a useful demonstration. |
| **रुन्धन्ति** (*rundhanti*) | RV 9.70.5 | **Not in the Ṛgveda.** RV 9.70.5 is *sa marmṛjānaḥ indriyāya dhāyase…* | **Claim fails.** Remove or replace. |
| **दीव्यति / दीव्यन्ति** | "Root attested RV 10.34" | **Neither form occurs anywhere in the Ṛgveda.** RV 10.34 contains *dīvyaḥ* (10.34.13a), *pratidīvne* (10.34.6d), *divyāḥ* (10.34.9c) — none is *dīvyati*. | **Claim fails, and it is the exact error the brief warns about:** the *dhātuḥ* occurring in the hymn is not evidence that the proposed completed form occurs there. |

### 2.2 Marked "not found," but present in the Ṛgveda

| Form | File claims | Actual Ṛgvedic occurrence |
|---|---|---|
| **ददामि** (*dadāmi*) | "missing in early Samhitas" | **RV 10.116.5c** — *ugrāya te sahaḥ balam dadāmi* |
| **कृणुतः** (*kṛṇutaḥ*) | not found | RV 8.31.9 |
| **कृणुथः** (*kṛṇuthaḥ*) | not found | RV 1.182.3, RV 10.39 |
| **कृणुथ** (*kṛṇutha*) | not found | RV 3.53.10, 6.28.6, 8.27.18, 8.67.17 (5×) |
| **विन्दन्ति** (*vindanti*) | not found | RV 1.105.1 |
| **विन्दसि** (*vindasi*) | not found | RV 1.176.1, 10.86.2 |
| **विन्दामि** (*vindāmi*) | not found | RV 8.24.12, 8.46.11, 10.34 (3×) |
| **तन्वते** (*tanvate*) | not found | 10× incl. 1.134.4, 1.159.4, 5.13.4 |
| **तन्वे** (*tanve*) | not found | 22× incl. 1.162.20, 1.165.11 |

The "not found" verdicts in that file are unreliable in both directions and
should not be carried into the manuscript or the appendix without re-checking
each one against a named corpus.

### 2.3 Structural corrections required

1. **The header mislabels the inventory.** "The 9 active (Parasmaipada /
   Ātmanepada) conjugations" conflates two different things. Nine
   person–number slots is not the same as voice. *Tanute* and *tanvate* are
   middle forms sitting inside a table headed "active." Retitle as a
   person-and-number inventory and treat voice as a separate axis.
2. **Remove the ⟪कृ⟫ chronological note.** The current note reads: "The Rigveda
   Samhita conjugates √kṛ as a 5th Class Svādi verb… However, the structural
   transition toward the 8th class is visible in the 10th Mandala." This
   imports a chronology (a "transition" located in a specific *maṇḍala*) and
   violates both the standing chronology rule and the Vedas-are-functional-not-
   chronological rule. **The observable fact, with no chronology attached:** the
   Ṛgveda uses *kṛṇoti*-type formations; the *laukika* domain uses
   *karoti*-type formations; the classification records two recurring behaviors
   of the same atom. State that and stop.
3. **Separate causative formation from tenth-*gaṇa* classification.**
   The file's own note concedes the problem ("we use the causative form of √dhṛ
   which utilizes the required 10th-class -aya- suffix"). **धारयति**
   (*dhārayati*, RV 7.85.3c) is verified as a form, but a form in *-aya-* is
   not by itself evidence of *curādi* lexical classification — the same
   *-aya-* appears in causatives of atoms classified elsewhere. Present
   *dhārayati* as a verified Vedic form exhibiting *-aya-* extension, and do not
   let it carry the tenth-*gaṇa* claim alone.
4. **Do not use `working/10_active.md` as a source of paradigms.** Its
   unverified rows are generated paradigm slots, not corpus evidence. The
   brief's rule — never present a generated paradigm as though every form
   occurs in the Vedas — applies directly to this file.

---

## 3. Recommended Chapter 11 body set

Ordered to follow the required argument sequence. Every form below is
**verified** in the Ṛgveda at the stated citation unless marked otherwise.

### 3.1 Keep the existing five-verb comparison unchanged

All five current Chapter 11 citations were checked pāda by pāda and **all five
are exactly correct**, including their pāda letters:

| Form | Citation | Pāda text (padapāṭha) | Status |
|---|---|---|---|
| **एति** (*eti*) | RV 1.23.11b | *marutām eti dhṛṣṇuyā* | verified |
| **अस्ति** (*asti*) | RV 1.22.4a | *nahi vām asti dūrake* | verified |
| **यजति** (*yajati*) | RV 1.26.3b | *āpiḥ yajati āpaye* | verified |
| **भवति** (*bhavati*) | RV 1.17.5c | *kratuḥ bhavati ukthyaḥ* | verified |
| **राजति** (*rājati*) | RV 5.25.4a | *agniḥ deveṣu rājati* | verified |

This section needs no evidentiary repair. It demonstrates atomic shape and
preparation under a controlled ending, and it does that job correctly.

### 3.2 Add: one atom across person and number

⟪भू⟫, all from the Ṛgveda, holding the atom constant while person and number vary:

| Form | Person / number | Citation | Pāda text |
|---|---|---|---|
| **भवति** | 3 sg | RV 1.17.5c | *kratuḥ bhavati ukthyaḥ* |
| **भवतः** | 3 dual | RV 10.12.1b | *abhiśrāve bhavataḥ satyavācā* |
| **भवन्ति** | 3 pl | RV 1.89.9c | verified (14× in RV) |
| **भवसि** | 2 sg | RV 1.31.5b | verified (13× in RV) |
| **भवथः** | 2 dual | RV 1.112.20a | verified (7× in RV) |
| **भवथ** | 2 pl | RV 3.54.17b | *yat ha devāḥ bhavatha viśve indre* |
| **भवाम** | 1 pl | RV 5.45.5a | verified (1× in RV) |

**Gap to state honestly:** first-person singular **भवामि** and first-person dual
**भवाव** do **not** occur in the Ṛgveda. The body should either (a) present a
seven-cell demonstration and say plainly that two cells are not filled by this
atom in this corpus, or (b) fill them from another *dhātuḥ* — §1.1 shows first
singular is populated 1,048× and first dual 29× overall, so the *category* is
demonstrably present even where ⟪भू⟫ does not supply it. **Option (b) is the
stronger argument and the honest one**: the breadth claim is about the corpus,
not about one atom.

### 3.3 Add: activation procedures, each with a verified Vedic form

| Procedure | Form | Citation | Note |
|---|---|---|---|
| direct attachment | **अस्ति** (*asti*) | RV 1.22.4a | already in chapter |
| inserted **अ** | **यजति** (*yajati*) | RV 1.26.3b | already in chapter |
| vowel strengthening | **एति** (*eti*) | RV 1.23.11b | already in chapter |
| strengthening + inserted **अ** | **भवति** (*bhavati*) | RV 1.17.5c | already in chapter |
| **reduplication** | **ददाति** (*dadāti*) | RV 1.40.4 (24× in RV) | ⟪दा⟫ |
| **reduplication** | **जुहोति** (*juhoti*) | RV 10.79.5 | ⟪हु⟫ — the atom that names the *juhotyādi* group |
| **reduplication** | **बिभर्ति** (*bibharti*) | RV 1.105.4 | ⟪भृ⟫ |
| **nasal infix** | **रुणद्धि** (*ruṇaddhi*) | RV 10.34.3a | ⟪रुध्⟫ |
| **nasal extension** | **कृणोति** (*kṛṇoti*) | RV 1.92.6 (31× in RV) | ⟪कृ⟫ |
| **nasal extension** | **क्रीणाति** (*krīṇāti*) | RV 4.24.10 | ⟪क्री⟫ |
| ***-aya-* extension** | **धारयति** (*dhārayati*) | RV 7.85.3c | see §2.3.3 — do not label *curādi* on this evidence alone |

### 3.4 Add: tense and mood beyond the present

| Category | Form | Citation | Notes |
|---|---|---|---|
| past (imperfect) | **आसीत्** (*āsīt*) | RV 10.129.1a | already in Appendix 7; *na asat āsīt na u sat āsīt tadānīm* |
| perfect | **वेद** (*veda*) | RV 1.164.39c | DCS: `Tense=Past`. Perfect form, present sense |
| perfect, plural | **विदुः** (*viduḥ*) | RV 1.164.39d | **Same atom ⟪विद्⟫, same stanza, singular vs plural** — an unusually clean minimal pair |
| future | **करिष्यति** (*kariṣyati*) | RV 1.164.39c | ⟪कृ⟫ + *-ṣya-*; the only occurrence in the RV |
| imperative | **भव** (*bhava*) | RV 1.1.9b | ⟪भू⟫, 2 sg — same hymn Appendix 7 already uses |
| subjunctive | **प्रचोदयात्** (*pracodayāt*) | RV 3.62.10 | **disputed analysis — see §7.2** |
| optative / jussive | **धीमहि** (*dhīmahi*) | RV 3.62.10 | **disputed analysis — see §7.1** |

### 3.5 Add: one clear *ātmanepada* set

Voice is not corpus-tagged (§0.2.6), so these are identified by ending against
a standard grammar:

| Form | Citation | Atom |
|---|---|---|
| **तनुते** (*tanute*) | RV 10.130.2a | ⟪तन्⟫ |
| **मन्यते** (*manyate*) | RV 6.52.2 | ⟪मन्⟫ |
| **यजते** (*yajate*) | RV 1.31.15 | ⟪यज्⟫ — **the same atom as *yajati* in §3.1**, in the other voice |
| **आसते** (*āsate*) | RV 1.164.39d | ⟪आस्⟫ |

***Yajati* / *yajate* is the recommended body contrast.** One atom, already
introduced to the reader in §11.2, appearing in both voices inside the same
corpus. It demonstrates voice without requiring a new atom or a new procedure.

---

## 4. Recommended Chapter 12 body set

### 4.1 *Dhātuḥ* → derived word, all verified in the Ṛgveda

| Derived form | Citation | Atom | Category |
|---|---|---|---|
| **यज्ञस्य** (*yajñasya*) | RV 1.1.1b | ⟪यज्⟫ | action noun, *ṣaṣṭhī ekavacanam* |
| **होतारम्** (*hotāram*) | RV 1.1.1c | ⟪हु⟫ | **agent** noun in *-tṛ*, *dvitīyā ekavacanam* |
| **ऋत्विजम्** (*ṛtvijam*) | RV 1.1.1b | — | agent noun, *dvitīyā ekavacanam* |
| **पुरोहितम्** (*purohitam*) | RV 1.1.1a | ⟪धा⟫ | **compound with identifiable parts** + participial |
| **ईड्यः** (*īḍyaḥ*) | RV 1.1.2b | ⟪ईड्⟫ | **gerundive / obligation**, *prathamā ekavacanam* |
| **कर्त्वम्** (*kartvam*) | RV 1.10.2b | ⟪कृ⟫ | **gerundive / obligation from the flagship atom** |
| **कर्मणः** (*karmaṇaḥ*) | RV 1.11.4 | ⟪कृ⟫ | deed |
| **कर्तृभिः** (*kartṛbhiḥ*) | RV 1.55.8 | ⟪कृ⟫ | agent, *tṛtīyā bahuvacanam* |
| **संस्कृतम्** (*saṃskṛtam*) | RV 5.76.2a | *sam* + ⟪कृ⟫ | **head-bond + atom + tail-bond, in the corpus** |
| **सवितुः** (*savituḥ*) | RV 3.62.10 | ⟪सू⟫ | agent noun, *ṣaṣṭhī ekavacanam* |
| **वरेण्यम्** (*vareṇyam*) | RV 3.62.10 | ⟪वृ⟫ | gerundive-type, *dvitīyā ekavacanam* neuter |

**Recommendation:** rebuild §12.3–12.6 around ⟪कृ⟫ using RV 1.10.2b, 1.11.4,
1.55.8, and 5.76.2a. The chapter's flagship atom then demonstrates deed, agent,
obligation, and head-bonded refinement **inside the calibrant**, and *prakṛti* /
*vikṛti* follow as *laukika* formations built by the same procedure (§1.4).

### 4.2 One sentence carrying most of the required categories

**RV 1.164.39** — already the chapter's epigraph — is exceptionally dense.
Full verified analysis:

> ऋचो अक्षरे परमे व्योमन् । यस्मिन्देवा अधि विश्वे निषेदुः ।
> यस्तन्न वेद किमृचा करिष्यति । य इत्तद्विदुस्त इमे समासते ॥

| Form | Lemma | Analysis | Category demonstrated |
|---|---|---|---|
| **ऋचो** (*ṛcaḥ*) | *ṛc* | `Gen Fem Sing` | *ṣaṣṭhī* |
| **अक्षरे** (*akṣare*) | *akṣara* | `Loc Neut Sing` | *saptamī* |
| **परमे** (*parame*) | *parama* | `Loc Neut Sing` | agreement in case/number |
| **व्योमन्** (*vyoman*) | *vyoman* | `Loc Neut Sing` | *saptamī* |
| **यस्मिन्** (*yasmin*) | *yad* | `Loc Neut Sing` | **relative pronoun** |
| **देवा** (*devāḥ*) | *deva* | `Nom Masc Plur` | *prathamā bahuvacanam* |
| **अधि** (*adhi*) | *adhi* | `ADP` | ***upasargaḥ* separated from its verb** |
| **निषेदुः** (*niṣeduḥ*) | *niṣad* | `3 Plur Past Ind` | past, plural |
| **यस्** (*yaḥ*) | *yad* | `Nom Masc Sing` | relative |
| **तन्** (*tat*) | *tad* | `Acc Neut Sing` | **correlative** |
| **न** (*na*) | *na* | `PART` | **negation** |
| **वेद** (*veda*) | *vid* | `3 Sing Past Ind` | **perfect** |
| **किम्** (*kim*) | *ka* | `Acc Neut Sing` | interrogative pronoun |
| **ऋचा** (*ṛcā*) | *ṛc* | `Ins Fem Sing` | ***tṛtīyā*** — the chapter's existing example |
| **करिष्यति** (*kariṣyati*) | *kṛ* | `3 Sing Fut Ind` | **future** |
| **विदुस्** (*viduḥ*) | *vid* | `3 Plur Past Ind` | **same atom as *veda*, plural** |
| **त** (*te*) | *tad* | `Nom Masc Plur` | correlative plural |
| **इमे** (*ime*) | *idam* | `Nom Masc Plur` | demonstrative pronoun |
| **सम्** (*sam*) | *sam* | `ADP` | ***upasargaḥ* separated from its verb** |
| **आसते** (*āsate*) | *ās* | `3 Plur Pres Ind` | *ātmanepada* |

This one stanza supplies: four *vibhaktis*, singular/plural contrast on **one
atom** (*veda* / *viduḥ*), perfect, future, present, negation, relative–correlative
construction, three pronoun classes, *ātmanepada*, and **two floating
*upasargāḥ*** (*adhi*, *sam*).

**The floating *upasargaḥ* is worth special attention.** Chapter 12 §12.2
currently asserts that "in the vaidika domain the same *upasargaḥ* may float in
front of its atom" and points to Chapter 16 and Appendix Part 8. The chapter's
**own epigraph demonstrates it twice.** That claim can be shown rather than
deferred.

### 4.3 Second and third sentence architectures

- **RV 1.1.1** — verb + accusatives in apposition + genitive + compound.
  Verified: *agnim* `Acc`, *purohitam* `Acc`, *devam* `Acc`, *ṛtvijam* `Acc`,
  *hotāram* `Acc` (pāda c), *yajñasya* `Gen`, *īḷe* 1 sg present.
  **Correction to Appendix 7:** it calls *ṛtvijam* the "Fourth apposition,"
  but within the quoted two pādas *ṛtvijam* is the third appositive
  (*purohitam*, *devam*, *ṛtvijam*). *Hotāram* is the fourth and sits in pāda c,
  which the excerpt does not quote. Either quote pāda c or renumber.
- **RV 10.129.1** — negation, existence, past. Verified stanza-precise:
  10.129.1a *na asat āsīt na u sat āsīt tadānīm*. Supplies **doubled negation**,
  *āsīt* imperfect ×3, and the *sat* / *asat* participial contrast from ⟪अस्⟫.
- **RV 3.62.10** — derivation, *upasargaḥ*, causative, mood. See §7 for the two
  disputed analyses before drafting.

---

## 5. Appendix Part 7 — evidence inventory

Recommended structure, with everything verified in this pass:

1. **Complete parsing of the four body passages** — RV 1.1.1, 1.164.39,
   3.62.10, 10.129.1. Full token tables as in §4.2 above.
2. **Person × number inventory** for ⟪भू⟫ (§3.2), with the two Ṛgvedic gaps
   stated plainly and filled from other atoms.
3. **Activation-procedure inventory** (§3.3), eleven verified forms.
4. **Tense and mood inventory** (§3.4), seven categories.
5. **Ātmanepada inventory** (§3.5), with the voice-tagging caveat (§0.2.6).
6. **⟪कृ⟫ derived-nominal inventory** (§4.1), including the *prakṛti* / *vikṛti*
   absence finding (§1.4).
7. **Corpus-wide breadth tables** (§1.1–1.3) — these are the calibrant argument
   in its most compact form.
8. **The corrected `10_active.md` audit** (§2), retained as a record of what
   was checked, what failed, and what the search boundary was.

---

## 6. Tables requested in the brief

### 6.1 Person × number × voice

Corpus-wide counts are in §1.1. Worked forms:

| Person | Number | Parasmaipada example | Citation | Ātmanepada example | Citation |
|---|---|---|---|---|---|
| 1 | sg | **कृणोमि** (*kṛṇomi*) | RV 10.125.5 | **ईळे** (*īḷe*) | RV 1.1.1a |
| 1 | dual | *(not from ⟪भू⟫ in RV; category populated 29× overall)* | §1.1 | — | — |
| 1 | pl | **भवाम** (*bhavāma*) | RV 5.45.5a | **धीमहि** (*dhīmahi*) | RV 3.62.10 (§7.1) |
| 2 | sg | **भवसि** (*bhavasi*) | RV 1.31.5b | — | — |
| 2 | dual | **भवथः** (*bhavathaḥ*) | RV 1.112.20a | — | — |
| 2 | pl | **भवथ** (*bhavatha*) | RV 3.54.17b | — | — |
| 3 | sg | **भवति** (*bhavati*) | RV 1.17.5c | **तनुते** (*tanute*) | RV 10.130.2a |
| 3 | dual | **भवतः** (*bhavataḥ*) | RV 10.12.1b | — | — |
| 3 | pl | **भवन्ति** (*bhavanti*) | RV 1.89.9c | **आसते** (*āsate*) | RV 1.164.39d |

Empty ātmanepada cells are **not** claims of absence — they were not searched
form-by-form in this pass, and voice is not corpus-tagged. See §10.

### 6.2 Tense and mood

| Category | Form | Citation | DCS tag |
|---|---|---|---|
| present | **भवति** | RV 1.17.5c | `Pres Ind` |
| imperfect / past | **आसीत्** | RV 10.129.1a | `Impf`/`Past Ind` |
| perfect | **वेद** | RV 1.164.39c | `Past Ind` |
| perfect plural | **विदुः** | RV 1.164.39d | `Past Ind` |
| future | **करिष्यति** | RV 1.164.39c | `Fut Ind` |
| imperative | **भव** | RV 1.1.9b | `Pres Imp` |
| subjunctive | **प्रचोदयात्** | RV 3.62.10 | `Pres Sub` — disputed, §7.2 |
| jussive / optative | **धीमहि** | RV 3.62.10 | `Past Jus` — disputed, §7.1 |
| participle | **सन्** / **सत्** | RV 10.129.1a | from ⟪अस्⟫ |
| gerundive | **कर्त्वम्** | RV 1.10.2b | `Gdv` |

### 6.3 Activation procedures

See §3.3 — eleven procedures, each with a verified Ṛgvedic form.

### 6.4 Nominal and sentence architecture

See §1.3 (all eight *vibhaktis* with counts) and §4.2–4.3 (three sentence
architectures with full parsing).

---

## 7. Disputed analyses — recorded, not resolved

The brief requires recording disagreements instead of silently choosing. Two
matter enough to change what the manuscript currently says.

### 7.1 धीमहि (*dhīmahi*) — atom and mood both disputed

**The manuscript currently states** (Appendix Part 7 §7.2 and §7.3): "**1pl
optative middle** (*liṅ-lakāra* लिङ्, *bahuvacana*, *ātmanepada*) of *dhī*
(धी, *to contemplate*)," with the *Dhātupāṭha* row giving
"⟪धी⟫ *dhī* / ⟪ध्यै⟫ *dhyai* (*to contemplate*)."

**Three independent findings contradict the atom assignment:**

| Source | Atom | Mood/tense |
|---|---|---|
| DCS (all 23 Ṛgvedic occurrences) | **धा** *dhā* | `Tense=Past`, `Mood=Jus` |
| K. Hoffmann, *Aufsätze zur Indoiranistik*, cited in INDOLOGY discussion | **धा** *dhā* | aorist optative — "we wish to place" |
| Werba, *Verba Indoarica* p. 298, cited in the same discussion | **धा** *dhā* | aorist optative |
| Witzel–Gotō; Jamison–Brereton translations | **धा** *dhā* | rendered "we wish to place" |

The INDOLOGY thread states the point directly: "It is indeed *optative*, not of
*dhī* but of *dhā*," and separately, "*dhīmahi* cannot actually be a present
form: it would have to be *dhīmahe*."

**On the mood, Whitney supports the manuscript's *optative* label** while
contradicting its atom: Whitney §564–568 gives **īmáhi** as the **optative**
ātmanepada first-plural ending (contrast §569–571, imperative `āmahāi`, and
§557–563, subjunctive `āmahāi`). So *-mahi* is an optative ending, and DCS's
`Jus` reflects the injunctive-adjacent reading the INDOLOGY thread calls "less
probable."

**Recommended handling.** Keep *optative* (defensible, and Whitney supports the
ending). **Change the atom from ⟪धी⟫ to ⟪धा⟫**, and record the *dhī*
reinterpretation as exactly that — a later reading, popularized by Sāyaṇa, of a
form whose grammatical shape points to ⟪धा⟫. **This is a correction the book
should welcome:** *dhīmahi* being from ⟪धा⟫ *place/establish* rather than ⟪धी⟫
*contemplate* is precisely the kind of recoverable-atom evidence Chapter 11
argues for, and it lands better as a demonstration than the received gloss does.

**Caution:** do not describe the *dhī* reading using chronological vocabulary
("late," "post-Vedic reinterpretation"). State it as a competing analysis and
identify who holds it.

### 7.2 प्रचोदयात् (*pracodayāt*) — mood disputed

**The manuscript states:** "**3sg optative active** (*liṅ-lakāra*,
*parasmaipada*) of *pracud*."

**DCS tags it `Tense=Pres | Mood=Sub | Person=3 | Number=Sing`** — subjunctive,
not optative. DCS treats the causative as lemmatized (`lemma=pracoday`), and
tags the parallel form *prācodayat* (RV 5.31.3) as `Impf Ind`.

Both analyses appear in the literature. The form is widely translated "may he
impel," which is compatible with either. **Recommended handling:** present the
form for what is not disputed — ⟪चुद्⟫ + *pra-* + *-aya-* + a modal ending, one
word carrying head-bond, causative extension, and mood — and record the
optative/subjunctive disagreement in an endnote rather than asserting *liṅ*
without qualification.

### 7.3 Minor: ऋचः in the Chapter 12 epigraph

Chapter 12 §12.1 refers to "the sacred hymns, the ऋचः (*ṛcaḥ*)," implying
plural. **DCS analyzes *ṛco* at RV 1.164.39a as `Case=Gen | Number=Sing`** —
genitive singular. Worth re-checking before the sentence is redrafted, since
the chapter builds a point on this word.

---

## 8. Proposed figure — the breadth table

**Recommendation: one figure, replacing several.** A single grid showing, for the
Ṛgveda:

- **rows** = person (1/2/3) × number (sg/dual/pl), nine cells;
- **each cell** = one verified Vedic form + citation;
- **a second band** = the mood/tense inventory (§6.2), eight categories, each
  with one verified form;
- **a third band** = the activation procedures (§6.3), each with one verified form.

This is compact, it is entirely verified, and it makes the calibrant argument
visually in one plate: **the Vedas fill the grid.** It replaces the current
reactivity-tier and rank-trajectory charts in the body (which §11.5–11.6 of the
existing chapter use, and which the rewrite plan already moves to Appendix Part 6).

A useful second figure: **one atom, two voices** — *yajati* (RV 1.26.3b) beside
*yajate* (RV 1.31.15), reusing the existing five-verb figure convention.

---

## 9. How this evidence supports the calibrant claim

The argument, in the order the brief requires:

1. **The Vedas preserve completed Sanskrit forms.** 179,345 word-occurrences in
   the Ṛgveda alone, each a finished form in a fixed transmitted context.
2. **Those forms show restricted, repeatable procedures.** Eleven distinct
   activation procedures are verified (§3.3), each recurring across many atoms:
   direct attachment, inserted **अ**, vowel strengthening, reduplication, nasal
   infix, nasal extension, *-aya-* extension. The same atom under different
   procedures (*kṛṇoti* / *karoti*-type) and different atoms under the same
   procedure (*dadāti*, *juhoti*, *bibharti*) are both observable.
3. **The procedures cover enough range to preserve grammar, not vocabulary.**
   Every person–number cell filled (§1.1). Six moods, six tense categories,
   participles, infinitives, gerundives, absolutives (§1.2). All eight
   *vibhaktis* (§1.3). A single stanza — RV 1.164.39 — carrying four cases,
   three pronoun classes, negation, relative–correlative structure, perfect,
   future, present, *ātmanepada*, and two floating *upasargāḥ* (§4.2). **A
   corpus that fills the entire grid is a calibrant. A corpus that preserved
   isolated words would leave cells empty.**
4. **The *laukika* domain applies the same architecture to new composition.**
   ⟪कृ⟫ yields *karman*, *kartṛ*, *kartvam*, and *saṃskṛta* **inside** the
   Ṛgveda (§1.4), and *prakṛti*, *vikṛti*, *saṃskṛti*, *saṃskāra*, *kārya*
   outside it — same atom, same head-bonds and tail-bonds, applied to what the
   corpus never needed to say. The absence of *prakṛti* and *vikṛti* from the
   Ṛgveda is not a weakness in the argument; it is the demonstration that the
   architecture generates beyond its calibrant while remaining checkable
   against it.
5. **Pāṇini made the evident analysis explicit.** Every form in §§3–4 was
   preserved, recited, and transmitted before any analytical apparatus is
   applied to it here. The grammatical categories in this document — person,
   number, mood, *vibhaktiḥ*, gerundive — are **read off the forms**, which is
   the same operation the *vaiyākaraṇāḥ* performed and the same one this
   research pass performed with a corpus index. That the operation succeeds is
   the evidence.

---

## 10. Uncertain claims requiring further research

| # | Item | What is needed |
|---|---|---|
| 1 | **Non-Ṛgvedic corpora unsearched.** | The DCS dump vendored here also contains Atharvaveda (Śaunaka), Atharvaveda (Paippalāda), Aitareya-Āraṇyaka, Aitareyabrāhmaṇa, Gopathabrāhmaṇa, Bṛhadāraṇyakopaniṣad, and Ṛgvedakhilāni. The brief permits these where they supply a category the Ṛgveda does not. **Search them before writing any "not found in the Vedic corpus" claim.** The two ⟪भू⟫ gaps (§3.2) and *bhavāmi* / *bhavāva* / *dadmaḥ* specifically. |
| 2 | **Verbless (nominal) sentence.** | Not securely established in this pass. Requires clause-level analysis, not token search. |
| 3 | **Ātmanepada beyond four forms.** | Voice is not corpus-tagged (§0.2.6). A form-by-form pass against a grammar's ending tables is needed to populate §6.1's empty cells. |
| 4 | **Word-order demonstration.** | The plan calls for a clearly-labeled hypothetical reordering. Not attempted here; requires author judgment about presenting a rearranged mantra. |
| 5 | ***dhīmahi* atom.** | §7.1. Recommend consulting Hoffmann and Werba directly rather than relying on the INDOLOGY summary. |
| 6 | ***pracodayāt* mood.** | §7.2. Needs a second grammatical authority. |
| 7 | **ऋचः number in RV 1.164.39a.** | §7.3. |
| 8 | **Vedic-to-*laukika* calibration pairs.** | §9.4 gives the ⟪कृ⟫ pair. A second pair should be verified on the same basis. |
| 9 | **Accented text.** | Every citation here is from unaccented DCS text. Appendix Part 7 discusses Vedic accent; accented forms need a separate source (e.g. van Nooten–Holland, or the accented Śākala text). |
| 10 | **Gaṇa classification.** | Treat the ten *gaṇāḥ* as an analytical classification of recurring behavior (per the brief). Nothing in this pass verifies *gaṇa* membership; the DCS lemma is not a *gaṇa* assignment. |

---

## 11. Reproducibility recommendation

The verification substrate built for this pass should not be discarded. Suggest
committing to `analysis/ch11_ch12_vedic_engineering/`:

- `build_index.py` — builds the 179,345-token TSV index from the vendored DCS
  CoNLL-U dump;
- `q.py`, `find.py`, `sent.py` — form lookup, feature filter, sentence parse;
- `audit.py` — the `working/10_active.md` claim audit that produced §2;
- `rv_index.tsv` — the index itself (or regenerate on demand; ~25 MB).

This matches the existing `analysis/dhatupatha/` and `analysis/ganah/` bundle
convention (each with `README.md`, `data/`, `derived/`, `scripts/`), and makes
every citation in Chapters 11–12 and Appendix Part 7 re-checkable by a reader or
a hostile reviewer with one command.

---

## 12. Sources

- **Digital Corpus of Sanskrit** (Oliver Hellwig, 2010–2024), CC BY 4.0 —
  <http://www.sanskrit-linguistics.org/dcs/index.php>. Vendored locally at
  `analysis/ganah/data/raw/dcs/`.
- **Vedic Treebank / UD_Sanskrit-Vedic** (Hellwig, Hettrich, Modi, Pinkal) —
  <https://universaldependencies.org/treebanks/sa_vedic/index.html>
- **Whitney, *Sanskrit Grammar*, Chapter VIII (Conjugation)**, §§557–571 for
  subjunctive, optative, and imperative ātmanepada endings —
  <https://en.wikisource.org/wiki/Sanskrit_Grammar_(Whitney)/Chapter_VIII>
- **INDOLOGY list discussion of *dhīmahi*** (July 2021), citing Hoffmann,
  Werba, Witzel–Gotō, Jamison–Brereton —
  <https://list.indology.info/pipermail/indology/2021-July/055002.html>
- **Macdonell, *A Vedic Grammar for Students*** —
  <https://archive.org/details/vedicgrammarfor00macduoft>
- **"Translating the Gāyatrī-Mantra," *Asian Literature and Translation*** —
  <https://orca.cardiff.ac.uk/id/eprint/157746/1/63fe0d551bfab.pdf>
  (metadata retrieved; full text returned HTTP 403 in this pass)
