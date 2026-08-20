# Chapters 11-12 Vedic Grammatical Breadth Research - Codex

**Created:** 2026-08-20  
**Status:** Independent corpus audit complete; reconciliation with Claude and Gemini still pending  
**Purpose:** Identify a compact, verifiable Vedic evidence set for the Chapter 11 and Chapter 12 rewrite.

---

## 1. Sources and Method

This audit began with the locally preserved Digital Corpus of Sanskrit data for the Rigveda:

- `analysis/ganah/data/raw/dcs/dcs/data/rigveda/pada-and-analysis.dat`
- `analysis/ganah/data/raw/dcs/dcs/data/conllu/files/Ṛgveda/` CoNLL-U files
- generated search index: `analysis/ch11_ch12_vedic_engineering/codex/rv_index.tsv`

The generated index contains 1,028 source files and 179,345 tagged tokens. It makes it possible to search every Rigvedic form by passage, lemma, person, number, case, tense, mood, and verbal form.

The DCS annotations are useful for finding and comparing forms. They are not treated as an infallible grammatical authority. The corpus documentation states that some mappings were generated automatically and may contain errors. Every form proposed for the body must therefore pass three checks:

1. the form must occur in the cited Rigvedic passage;
2. the grammatical interpretation must fit the form and its sentence;
3. disputed analyses must remain identified as disputed.

The exact text of high-value passages was also compared with Vedic Heritage Portal pages and the University of Texas metrical Rigveda. The local corpus remains the main search instrument; those independent witnesses provide a second check on the displayed form.

This document does not use absence from a search result as proof that a form never occurs. It records absence only within the corpus and search method described above.

---

## 2. Main Finding

The Rigveda preserves the grammatical breadth needed for the proposed argument.

Its completed verbs occupy every person-and-number position:

| | *ekavacanam* | *dvivacanam* | *bahuvacanam* |
|---|---:|---:|---:|
| first person | 1,048 | 29 | 1,561 |
| second person | 5,532 | 1,376 | 1,229 |
| third person | 8,153 | 355 | 4,399 |

The corpus also preserves both *parasmaipada* and *atmanepada* endings, several ways of preparing a *dhatuḥ* before an ending is attached, past and future forms, imperatives, optatives, Vedic subjunctives, participles, infinitives, and converbs.

The nominal system has comparable breadth. The indexed corpus contains all seven *vibhaktis* and *sambodhanam* across singular, dual, and plural forms. A single sentence does not need to display the entire architecture. The corpus as a whole does.

These counts establish category coverage. They should not be printed as exact prevalence figures until the annotation method, duplicate treatment, and disputed tags have been documented. The chapter needs the breadth, not a false impression of precision.

---

## 3. Corrections to `working/10_active.md`

The source document is valuable, but it cannot move directly into the manuscript. It combines generated paradigm slots with attested Rigvedic forms, and several entries require correction.

### 3.1 Cited form or location needs correction

| Entry in the source document | Audit result | Required correction |
|---|---|---|
| **भवति (*bhavati*)**, RV 10.85.34 | **भवति** does not occur in that passage | Use RV 1.17.5c or another verified occurrence |
| **भवथ (*bhavatha*)**, RV 5.55.8 | The passage has **भवथा (*bhavatha*)** | Use the clearer **भवथ** at RV 3.54.17b if that exact ending is required |
| **तनुते (*tanute*)**, RV 10.130.1 | The form occurs in the next verse | Cite RV 10.130.2a |
| **रुन्धन्ति (*rundhanti*)**, RV 9.70.5 | The claimed form is absent from the cited passage | Remove this citation unless another exact occurrence is verified |
| **धारयथ (*dharayatha*)**, RV 6.36.1 | The received form is **धारयथाः (*dharayathaḥ*)** | Do not count the generated search form as an exact attestation |

### 3.2 Forms marked absent that are present

| Form | Verified Rigvedic location |
|---|---|
| **ददामि (*dadami*)** | RV 10.116.5c |
| **कृणुतः (*kṛṇutaḥ*)** | RV 8.31.9d |
| **कृणुथः (*kṛṇuthaḥ*)** | RV 1.182.3a; 10.39.11d; 10.143.1d |
| **कृणुथ (*kṛṇutha*)** | RV 3.53.10a; 6.28.6c; 8.67.17c |
| **विन्दन्ति (*vindanti*)** | RV 1.105.1d |
| **विन्दसि (*vindasi*)** | RV 1.176.1d; 10.86.2c |
| **विन्दामि (*vindami*)** | RV 8.24.12b; 8.46.11b; 10.34.3d |
| **रुणध्मि (*ruṇadhmi*)** | RV 10.34.12c |
| **तन्वते (*tanvate*)** | Ten indexed occurrences |
| **तन्वाथे (*tanvathe*)** | RV 10.106.1b |
| **धारयथः (*dharayathaḥ*)** | RV 5.69.1b |

### 3.3 Generated slots that should not be called attested forms

- **दीव्यति (*divyati*)** and **दीव्यन्ति (*divyanti*)** were not located as exact Rigvedic forms. The presence of the *dhatuḥ* elsewhere in a hymn does not attest these completed forms.
- Exact occurrences of **तन्वे (*tanve*)** in the search results are forms of **तनू (*tanu*)**, body or self. They must not fill a first-person verbal position for ⟪तन्⟫.
- **धारयति (*dharayati*)** occurs at RV 7.85.3, but the surface form alone does not prove that the *dhatuḥ* belongs to a later ten-*gaṇa* lexical classification. It securely demonstrates an **-aya-** formation.
- The source document's proposed ninety-form inventory mixes *parasmaipada* and *atmanepada* paradigms. It is better described as ninety generated person-and-number positions drawn from ten representative patterns, not as one uniform conjugation table.

### 3.4 What the corrected source can still demonstrate

The corrected inventory remains useful because it shows that the Rigveda preserves:

- every person and number;
- both sets of verbal endings;
- direct attachment;
- vowel change;
- reduplication;
- nasal insertion and nasal extension;
- **-aya-** extension;
- several present, past, future, imperative, optative, and Vedic-only forms.

The complete corrected inventory belongs in Appendix Part 7. The body needs representative examples, not ninety slots.

---

## 4. Recommended Chapter 11 Evidence

Chapter 11 should begin with completed Vedic forms and let the reader see the repeated procedures before introducing Pāṇini's analytical categories.

### 4.1 Five detailed examples

The strongest provisional set is:

| Form | Passage | What the reader can see |
|---|---|---|
| **अस्ति (*asti*)** from ⟪अस्⟫ | RV 1.22.4 | The atom accepts its ending without an inserted vowel |
| **भवति (*bhavati*)** from ⟪भू⟫ | RV 1.17.5 | The vowel changes and **अ** prepares the atom for the ending |
| **ददाति (*dadati*)** from ⟪दा⟫ | RV 10.117.3 | The opening part of the atom is repeated before the ending is added |
| **रुणद्धि (*ruṇaddhi*)** from ⟪रुध्⟫ | RV 10.34.3 | A nasal sound enters the atom during formation |
| **यजति / यजते (*yajati / yajate*)** from ⟪यज्⟫ | RV 1.26.3; 1.31.15 | The same prepared atom accepts two different sets of endings |

This set teaches five different facts. It avoids presenting five nearly identical **-ति** forms as though they demonstrated the whole verbal architecture. It also preserves several of the current chapter's strongest explanations.

The final five should be selected only after the Claude and Gemini evidence is reconciled. **एति (*eti*)**, **कृणोति (*kṛṇoti*)**, and **क्रीणाति (*krīṇati*)** remain strong alternatives if vowel strengthening or nasal extension deserves a full panel.

### 4.2 Compact breadth after the five examples

After the five detailed forms, one compact figure should show that the same corpus also includes:

- first, second, and third person;
- singular, dual, and plural;
- *parasmaipada* and *atmanepada*;
- present, past, future, imperative, optative, and Vedic subjunctive forms;
- participles, infinitives, and converbs.

Suggested forms for this compact figure include:

| Category | Form | Passage |
|---|---|---|
| first-person singular | **ईळे (*īḷe*)** | RV 1.1.1 |
| first-person plural | **धीमहि (*dhīmahi*)** | RV 3.62.10, with its analysis qualified |
| second-person dual | **कृणुथः (*kṛṇuthaḥ*)** | RV 1.182.3 |
| third-person plural | **विन्दन्ति (*vindanti*)** | RV 1.105.1 |
| past | **आसीत् (*āsīt*)** | RV 10.129.1 |
| future | **करिष्यति (*kariṣyati*)** | RV 1.164.39 |
| imperative | **भव (*bhava*)** | RV 1.1.9 |
| optative or Vedic mood | **प्रचोदयात् (*pracodayāt*)** | RV 3.62.10, with the disputed tag recorded |

The figure should not require every form to come from the same *dhatuḥ*. The point is that the Vedic corpus preserves every grammatical position, not that one atom fills every position in the surviving text.

### 4.3 What should remain outside the body

Appendix Part 7 should retain:

- the corrected ninety-position search;
- every exact passage location;
- forms not found;
- forms whose analysis remains disputed;
- the larger person-number table;
- the full list of activation procedures.

The current **एति, अस्ति, यजति, भवति, राजति** comparison should not disappear. Any example removed from the detailed body set should move to the appendix or Lost and Found until its destination is approved.

---

## 5. Recommended Chapter 12 Evidence

Chapter 12 needs to show the next transition: a *dhatuḥ* becomes several kinds of completed words, those words receive sentence roles, and the roles bind them into a *vakyam*.

### 5.1 Use Vedic ⟪कृ⟫ forms before later derivatives

The current chapter moves quickly from ⟪कृ⟫ to mostly *laukika* words. The Vedic corpus can establish the family first:

| Form | Passage | Contribution |
|---|---|---|
| **कर्त्वम् (*kartvam*)** | RV 1.10.2 | action or task derived from ⟪कृ⟫ |
| **कर्मणः (*karmaṇaḥ*)** | RV 1.11.4 | completed action in a sentence role |
| **कर्तृभिः (*kartṛbhiḥ*)** | RV 1.55.8 | agents marked by instrumental plural |
| **करिष्यति (*kariṣyati*)** | RV 1.164.39 | future completed verb from the same atom |
| **संस्कृतम् (*saṃskṛtam*)** | RV 5.76.2 | something carefully prepared or completed |

The passage at RV 5.76.2 does not use **संस्कृतम्** as the proper name of the language. It demonstrates that the formed word already exists in Vedic use and carries the sense of something prepared or brought to completion.

Other Rigvedic forms include **सुसंस्कृताः (*susaṃskṛtaḥ*)** at RV 1.38.12, **संस्कृतः (*saṃskṛtaḥ*)** at RV 8.33.9, and a dual form in RV 8.77.11. The last form requires an additional textual and grammatical check because the corpus transcription and its automatic annotation disagree about the displayed ending.

After this Vedic family has been established, the chapter can turn to *prakṛti, vikṛti, saṃskṛti, saṃskāra, kārya,* and modern formations. That order makes the calibrant relationship concrete: the Veda supplies the preserved forms; the *laukika* domain continues using the architecture.

### 5.2 Use more than one sentence architecture

Four passages together provide the required breadth:

#### RV 1.1.1

**अग्निमीळे पुरोहितं यज्ञस्य देवमृत्विजम् होतारं रत्नधातमम्**

This sentence provides:

- first-person singular *atmanepada* **ईळे**;
- accusative relations around **अग्निम्**;
- genitive **यज्ञस्य**;
- derived words and compounds such as **पुरोहितम्, ऋत्विजम्, होतारम्,** and **रत्नधातमम्**;
- a sentence whose relations remain clear because the endings identify each role.

#### RV 1.164.39

**ऋचो अक्षरे परमे व्योमन्यस्मिन्देवा अधि विश्वे निषेदुः। यस्तन्न वेद किमृचा करिष्यति। य इत्तद्विदुस्त इमे समासते॥**

This passage provides:

- locative relations;
- instrumental **ऋचा**;
- relative pronouns;
- past, future, and present verbal forms;
- more than one clause joined through explicit relations.

#### RV 10.129.1

**नासदासीन्नो सदासीत्तदानीं** and the remainder of the verse provide:

- negation;
- repeated imperfect past **आसीत्**;
- nominal contrasts;
- questions carried by pronouns and case relations.

#### RV 3.62.10

The Gāyatrī mantra provides:

- genitive **सवितुः** and **देवस्य**;
- accusative **भर्गः / भर्गम्** as received in the sentence tradition;
- first-person plural **धीमहि**;
- a relative construction with **यः**;
- **प्रचोदयात्**, whose precise mood label should remain qualified until the competing analyses are resolved.

The body does not need to parse every word in all four passages. RV 1.1.1 and RV 1.164.39 can carry the detailed explanation. RV 10.129.1 and RV 3.62.10 can add compact evidence of past time, negation, plural agency, and a different clause structure.

### 5.3 What the sentence demonstration should say

The examples support a plain sequence:

1. the *dhātuḥ* receives a restricted transformation and an ending;
2. a derived word retains the atom while adding a new function;
3. a *vibhakti* marks number and relation;
4. the completed *padāni* form a sentence;
5. the listener reconstructs the relations from the completed forms, not from a compulsory English-like word order.

Pāṇini should enter after this sequence. His documentation gives compact rules and analytical names to the architecture already demonstrated by the Vedic sentences.

---

## 6. Disputed or Unsafe Claims

The rewrite should not depend on the following claims until they are resolved:

1. **धीमहि (*dhīmahi*)** has competing derivations and mood labels. It is safe as a first-person plural Vedic form; its exact derivational walk-through needs a source note.
2. **प्रचोदयात् (*pracodayāt*)** is variously tagged. It is safe as a Vedic verbal form carrying desired or invoked action; its precise mood label must be sourced.
3. RV 8.77.11 displays **सुसंस्कृता** in the pada text while one automatic annotation parses **संस्कृते**. Do not use it to establish a feminine dual ending without checking a reliable accented edition and commentary.
4. **धारयति** securely demonstrates an **-aya-** extension. It does not by itself settle a later *gaṇa* classification.
5. A missing positive form does not prevent Sanskrit from generating a privative. The chapter already makes that larger point elsewhere; Chapters 11 and 12 do not need to repeat the full *a-dabdha* argument.
6. The occurrence of **संस्कृतम्** in RV 5.76.2 does not make it the proper name of the language in that mantra.
7. Corpus annotation counts establish breadth but should not be presented as exact linguistic prevalence without a reproducible counting protocol.

---

## 7. Proposed Figure

One compact figure can summarize the breadth after the detailed examples.

### Figure structure

Use a central band labeled **The Rigveda preserves the completed forms**. Arrange four surrounding groups:

1. **Who acts?** first, second, third person
2. **How many act?** singular, dual, plural
3. **How is the atom prepared?** direct, vowel change, insertion, reduplication, nasal insertion, nasal extension, **-aya-** extension
4. **How is the action placed?** present, past, future, command, possibility or desire, Vedic subjunctive

Each category should carry one verified Devanagari form and its passage number. The body should explain five forms. The figure should show that those five belong to a much larger preserved architecture.

Appendix Part 7 can then expand the figure into full tables with exact forms, passages, grammatical labels, and uncertainty notes.

---

## 8. How the Evidence Supports the Calibrant Claim

The calibrant claim does not depend on finding one complete paradigm in one hymn.

The Vedas preserve thousands of completed forms across every person and number, both sets of verbal endings, several tenses and moods, all *vibhaktis*, three grammatical numbers, derived words, compounds, and several sentence structures. Exact transmission holds those forms and their contexts in place. A later student can compare one formation with another because the evidence does not change between comparisons.

The *laukika* domain uses the same architecture to create new expressions. It does not need every later word to occur in the Vedas. It needs the sounds, bonds, transformations, endings, and sentence relations to remain available. The Vedic corpus preserves that range.

Pāṇini's contribution becomes clearer in this order. He did not need to invent the grammatical behavior demonstrated by **अस्ति, भवति, ददाति, रुणद्धि, यजते, ईळे, आसीत्,** or **करिष्यति**. Those forms already existed in invariant passages. His documentation made their recurring architecture explicit, compact, derivable, and teachable.

---

## 9. Provisional Rewrite Recommendation

Before the three-way comparison, this audit recommends:

1. Replace the five equal-length **-ति** demonstrations in Chapter 11 with five examples chosen for different transformations.
2. Preserve unused current examples in Appendix Part 7 or Lost and Found.
3. Add one compact breadth figure rather than a long conjugation lesson.
4. Establish the Vedic ⟪कृ⟫ family near the beginning of Chapter 12.
5. Use RV 1.1.1 and RV 1.164.39 as the two main sentence demonstrations.
6. Use RV 10.129.1 and RV 3.62.10 only for additional breadth, with disputed verbal analyses qualified.
7. Introduce Pāṇini after the Vedic demonstrations.
8. Move dictionary statistics, cross-corpus ranks, and large reactivity calculations out of the teaching sequence unless they directly support a claim the examples cannot establish.

The final recommendation must now be compared with the complete Claude and Gemini reports.
