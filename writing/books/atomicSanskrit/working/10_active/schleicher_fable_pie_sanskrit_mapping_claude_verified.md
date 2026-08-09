# Schleicher's Fable: Verified Sanskrit Mapping

**Status:** Corrected verification pass on `schleicher_fable_pie_sanskrit_mapping.md`.
The earlier document is a draft. Claude's first verification improved several
rows but also treated reconstructed morphology as if it were recorded Sanskrit.
This pass corrects those remaining errors before the results enter the appendix
and endnotes.

---

## 1. Method and Counting Rules

August Schleicher's 1868 text — *Eine Fabel in indogermanischer Ursprache*,
published in *Beiträge zur vergleichenden Sprachforschung* 5 (1868): 206–208
— is the object under study. The full text:

> Avis, jasmin varnā na ā ast, dadarka akvams, tam, vāgham garum vaghantam,
> tam, bhāram magham, tam, manum āku bharantam. Avis akvabhjams ā vavakat:
> kard aghnutai mai vidanti manum akvams agantam. Akvāsas ā vavakant: krudhi
> avai, kard aghnutai vividvant-svas: manus patis varnām avisāms karnauti
> svabhjam gharmam vastram avibhjams ka varnā na asti. Tat kukruvants avis
> agram ā bhugat.

**Counting the words.** Reading the text as a plain sequence of
space-separated units, and counting a comma as a word-boundary rather than a
word, the text contains **57 word-occurrences**. Folding case (treating
sentence-initial "Avis" and mid-sentence "avis" as the same written word) and
merging exact repeats gives **44 distinct written forms**. Schleicher's own
hyphen in *vividvant-svas* is preserved as part of one written form for
counting purposes, without claiming that it reveals a Sanskrit grammatical
division.

**Why written forms are not roots.** A written form in the fable is an
inflected word: a root or stem plus whatever case-ending, person-ending, or
participial suffix the sentence requires. *Akvams*, *akvāsas*, and
*akvabhjams* are three different written forms built from one shared base
(the word for "horse"); *bharantam* and *bhāram* are two different written
forms built from one shared verbal base (the word for "carry"). Counting 44
written forms therefore does not mean 44 separate underlying words, and
still less does it mean 44 roots. The table below tracks both the written
form and, separately, the Sanskrit **dhātuḥ** or grammatical base it can be
compared with.

---

## 2. Corrected 44-Form Table

**Relationship classes**, per the assignment given for this task:

- **A** — Exact or nearly exact recorded Sanskrit form
- **B** — The same Sanskrit form or grammatical base after one explainable sonomer change
- **C** — A Sanskrit grammatical base carrying reconstructed or altered morphology
- **D** — Semantically suggestive but uncertain
- **E** — No secure Sanskrit comparison

| # | Schleicher's form | Meaning and grammar in fable | Sanskrit comparison | Sanskrit atom/base | Class | Domain | Source | Location | Note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | avis | sheep (subject) | **अवि (avi)**, "sheep, ewe" | Nominal base अवि | A | Both | Monier-Williams Skt.-Eng. Dict., s.v. *avi* | Endnote | Well-recorded noun across the corpus. A deeper connection to a verbal root is disputed; do not assert one. |
| 2 | jasmin | relative form, used for the sheep that lacks wool | **यस्मिन् (yasmin)**, locative singular of यद् (yad) | Pronominal base यद् | A | Both | Whitney, *Sanskrit Grammar*, pronoun declension tables | Endnote | The written form is nearly exact. Later grammatical analyses assign a dative function to the reconstructed relative, while Sanskrit **यस्मिन्** is locative; the surface correspondence should not be turned into grammatical identity. |
| 3 | varnā | wool (subject of "has no") | **ऊर्णा (ūrṇā)**, "wool" | Nominal base ऊर्णा | B | Both | Monier-Williams, s.v. *ūrṇā* | Endnote | Same word-family as reconstructed by comparativists for the fable's "wool," but the Sanskrit initial is ū-, not v-. Schleicher's *varnā* is a reconstruction, not a spelling variant actually recorded in Sanskrit. |
| 4 | na | not | **न (na)**, "not" | Particle न | A | Both | Monier-Williams, s.v. *na* | Endnote | Exact. |
| 5 | ā | verbal particle placed before several past or reported actions | **आ (ā)**, a Sanskrit upasarga; compare also the Sanskrit past augment **अ (a)** | Particle or verbal marker | D | Both | Schleicher 1868, pages 206–208; Whitney §§585, 1077ff. | Endnote | The sound-form is Sanskrit, but its function in the reconstructed sentence is not securely the Sanskrit **आ** upasarga. It may instead be serving as a reconstructed past marker. Do not count a one-letter resemblance as an exact grammatical match. |
| 6 | ast | was (3sg past) | **आसीत् (āsīt)**, imperfect 3sg of ⟪अस्⟫ (as) | Dhātuḥ ⟪अस्⟫ | C | Both | Whitney §800 (irregular imperfect of *as*) | Endnote | Same base, different architecture: Schleicher's *ast* looks like a bare root plus the secondary ending *-t*, with no augment. The recorded Sanskrit form carries the augment ā- and an extra sibilant, आ-सी-त् (ā-s-īt). Compare it to the base, not treat it as identical to āsīt. |
| 7 | dadarka | saw (3sg perfect) | **ददर्श (dadarśa)**, perfect 3sg of ⟪दृश्⟫ (dṛś) | Dhātuḥ ⟪दृश्⟫ | B | Both | Monier-Williams, s.v. *dṛś*; Whitney §794 (perfect of *dṛś*) | Appendix | Both forms use the same reduplicated-perfect architecture. Schleicher substitutes **k** where Sanskrit has **ś**, so the forms are close but not identical. |
| 8 | akvams | horses (accusative plural) | **अश्वान् (aśvān)**, accusative plural of अश्व (aśva) | Nominal base अश्व | B | Both | Monier-Williams, s.v. *aśva* | Endnote | Regular sound correspondence (Schleicher's k for Sanskrit's ś). |
| 9 | tam | that/him (accusative) | **तम् (tam)**, accusative singular of तद् (tad) | Pronominal base तद् | A | Both | Whitney, pronoun tables | Endnote | Exact. |
| 10 | vāgham | wagon (accusative) | **वाहम् (vāham)**, accusative singular of वाह (vāha), "vehicle, carrier" | Dhātuḥ ⟪वह्⟫ (vah) | B | Both | Monier-Williams, s.v. *vāha* | Appendix | वाह is a real, dictionary-recorded Sanskrit noun built regularly from वह् ("to carry"). Schleicher's g in place of Sanskrit's h reflects one specific, regular sound correspondence — this is a real derived Sanskrit word, not just a shared root, once the sound law is applied. |
| 11 | garum | heavy (accusative) | **गुरुम् (gurum)**, accusative singular of गुरु (guru) | Nominal base गुरु | B | Both | Monier-Williams, s.v. *guru* | Appendix | The case-form and consonants remain visible, while Schleicher changes Sanskrit **u** to **a**. |
| 12 | vaghantam | pulling (present participle, accusative) | **वहन्तम् (vahantam)**, present participle accusative of ⟪वह्⟫ (vah) | Dhātuḥ ⟪वह्⟫ | B | Both | Whitney §299 (present participles) | Appendix | The same participial architecture remains visible; Schleicher inserts **g** before Sanskrit **h**. |
| 13 | bhāram | load (accusative) | **भारम् (bhāram)**, accusative singular of भार (bhāra) | Dhātuḥ ⟪भृ⟫ (bhṛ) | A | Both | Monier-Williams, s.v. *bhāra* | Appendix | Exact. |
| 14 | magham | big (accusative) | **महान्तम् (mahāntam)**, accusative singular of महत् (mahat), from ⟪मह्⟫ (mah) | Dhātuḥ ⟪मह्⟫ | C | Both | Whitney, adjective declension of *mahat* | Endnote | Same base; Schleicher's written form is not the actual Sanskrit accusative, which carries an extra -ant- stem element. |
| 15 | manum | man (accusative) | **मनुम् (manum)**, accusative singular of मनु (Manu/manu) | Nominal base मनु | A | Both | Monier-Williams, s.v. *manu* | Appendix | Exact. Sanskrit मनु carries two distinct senses that should not be blurred: a common noun for a thinking human being, and the proper name of the lawgiver-progenitor figure of the Manusmṛti tradition. The fable uses the common-noun sense only. |
| 16 | āku | quickly | **आशु (āśu)**, "swift, quick" | Nominal base आशु | B | Both | Monier-Williams, s.v. *āśu* | Endnote | Regular correspondence (Schleicher's k for Sanskrit's palatal ś). |
| 17 | bharantam | carrying (present participle, accusative) | **भरन्तम् (bharantam)**, present participle accusative of ⟪भृ⟫ (bhṛ) | Dhātuḥ ⟪भृ⟫ | A | Both | Whitney §299 | Appendix | Exact — identical written form to the recorded Sanskrit participle. |
| 18 | akvabhjams | to/with the horses | **अश्वेभ्यः (aśvebhyaḥ)** dative plural, or **अश्वैः (aśvaiḥ)** instrumental plural | Nominal base अश्व | C | Both | Whitney, a-stem declension | Endnote | The root अश्व is confirmed; the case-ending itself is a reconstructed non-Sanskrit form, not the Sanskrit dative or instrumental plural ending. |
| 19 | vavakat | said (3sg, singular subject) | **⟪वच्⟫ (vac)**, "to speak"; recorded perfect उवाच (uvāca) | Dhātuḥ ⟪वच्⟫ | C | Both | Monier-Williams, s.v. *vac*; Whitney §793 (perfect of roots in initial *va-*) | Endnote | Same base, but the recorded Sanskrit perfect is irregular: initial va- weakens to u- (उवाच, ūcuḥ), not a regular reduplication. Schleicher built a regular-looking reduplicated form the corpus does not actually use for this meaning. A closer written match, though a different mood, is the Vedic subjunctive vócati/vócāti, which keeps the voc- shape Schleicher used. |
| 20 | kard | heart (grammatical subject of "pains") | **हृद् / हृदय (hṛd / hṛdaya)**, "heart" | Nominal base हृद् | C | Both | Standard Indo-Iranian comparative treatments (e.g. Burrow, *The Sanskrit Language*) | Appendix | This is not the regular sound correspondence. The ordinary outcome of the sound Schleicher wrote as k is Sanskrit's palatal ś; "heart" instead shows h, a specific, lexically irregular development also visible in the mismatch with Avestan's zərəd- (which does show the expected outcome). Present it as an irregular but real correspondence, not a systematic rule applied cleanly. |
| 21 | aghnutai | pains, grieves (3sg) | **अघ (agha)**, "distress, evil, sin" | Nominal base अघ | D | Both | Monier-Williams, s.v. *agha* | Endnote | The noun is well recorded; a matching finite verb root is not commonly cited. Root-level suggestion only. |
| 22 | mai | to me (dative) | **मे (me)**, enclitic dative/genitive of first person | Pronominal base अहम् | A | Both | Whitney, personal pronoun tables | Endnote | Near-exact. |
| 23 | vidanti | seeing (reconstructed present participle, dative singular) | Compare Sanskrit ⟪विद्⟫ (*vid*), "know, perceive" | Dhātuḥ ⟪विद्⟫ | C | Both | Schleicher's literal translation; Beekes's grammatical gloss of the later fable; Monier-Williams, s.v. *vid* | Endnote | This is not Sanskrit **विदन्ति**, the finite third-person plural. In the sentence it modifies the singular experiencer: "the heart pains me while seeing a man driving horses." The reconstructed form uses the Sanskrit base **विद्** under non-Sanskrit participial morphology. |
| 24 | agantam | driving (present participle, accusative) | **अजन्तम् (ajantam)**, present participle accusative of ⟪अज्⟫ (aj) | Dhātuḥ ⟪अज्⟫ | B | Both | Whitney §299; Monier-Williams s.v. *aj* | Endnote | Regular correspondence (Schleicher's g for Sanskrit's j). |
| 25 | akvāsas | horses (nominative plural) | **अश्वासः (aśvāsaḥ)**, a Vedic-domain nominative plural of अश्व | Nominal base अश्व | B | Vaidika-specific ending | Whitney §335 (Vedic -āsaḥ nom. pl.) | Endnote | This ending belongs to the *chandasi* domain specifically; the *laukika* nominative plural is अश्वाः (aśvāḥ). A domain variant, not an earlier stage of the *laukika* form. |
| 26 | vavakant | said (3pl) | **⟪वच्⟫ (vac)**; recorded perfect ऊचुः (ūcuḥ) | Dhātuḥ ⟪वच्⟫ | C | Both | Same as row 19 | Endnote | Same caveat as row 19. |
| 27 | krudhi | listen! (imperative) | **श्रुधि (śrudhi)**, a recorded Rigvedic imperative of ⟪श्रु⟫ (śru), "to hear" | Dhātuḥ ⟪श्रु⟫ | B | Vaidika | Recorded at Ṛgveda 8.82.6 ("indra śrudhi") and 10.61.21; the laukika imperative is **शृणु (śṛṇu)** | Appendix | The earlier draft left this comparison unverified. The Vedic form establishes it directly. |
| 28 | avai | O sheep (vocative) | **अवे (ave)**, vocative singular of अवि | Nominal base अवि | B | Both | Whitney, vocative formation | Endnote | The grammatical function matches; Schleicher's final vowel differs from the recorded Sanskrit vocative. |
| 29 | vividvant-svas | seeing/knowing, with reconstructed morphology | Compare the Sanskrit perfect-participial base **विद्वस् (vidvas)** from ⟪विद्⟫ (vid) | Dhātuḥ ⟪विद्⟫ | C | Both | Whitney §794; Schleicher 1868, pages 206–208 | Endnote | The earlier verification split this as **विद्वांसः + स्मः**, but Schleicher's hyphen does not establish that Sanskrit analysis. The **vid/vivid** base and reduplication remain visible; the exact morphology and the function of **-svas** should remain unresolved. |
| 30 | manus | man (nominative) | **मनुः (manuḥ)**, nominative singular of मनु | Nominal base मनु | A | Both | Monier-Williams, s.v. *manu* | Endnote | Exact; common-noun sense, as in row 15. |
| 31 | patis | master (nominative) | **पतिः (patiḥ)**, "lord, master, husband" | Nominal base पति | A | Both | Monier-Williams, s.v. *pati* | Appendix | Exact — one of the most familiar Sanskrit nouns. |
| 32 | varnām | wool (accusative) | **ऊर्णाम् (ūrṇām)**, accusative of ऊर्णा | Nominal base ऊर्णा | B | Both | Monier-Williams, s.v. *ūrṇā* | Endnote | Same caveat as row 3. |
| 33 | avisāms | of the sheep (genitive plural) | **अवीनाम् (avīnām)**, genitive plural of अवि | Nominal base अवि | C | Both | Whitney, i-stem declension | Endnote | Root confirmed; ending is a reconstructed non-Sanskrit form. |
| 34 | karnauti | makes (3sg present) | **कृणोति (kṛṇoti)**, "does, makes," from ⟪कृ⟫ (kṛ) | Dhātuḥ ⟪कृ⟫ | B | Vaidika | Ṛgveda 1.48.8 and 6.64.1; UT Austin, *Rigveda VII, 81*, grammatical analysis of **kṛṇoti** | Appendix | The Ṛgveda itself uses **कृणोति** with the meaning "does/makes." Schleicher changes the vowel and retains the same consonantal frame, present formation, person, number, and meaning. No appeal to a later Dhātupāṭha classification is needed. |
| 35 | svabhjam | for himself (dative) | **स्व (sva)**, "own, self" | Reflexive base स्व | C | Both | Monier-Williams, s.v. *sva* | Endnote | Root confirmed; exact case-form is a reconstruction. |
| 36 | gharmam | warm (accusative) | **घर्मम् (gharmam)**, accusative of घर्म (gharma), "heat" | Nominal base घर्म | A | Vaidika (ritual heat-offering) and laukika (general "warm/heat") | Monier-Williams, s.v. *gharma* | Appendix | Exact; a well-known Vedic ritual term (the heated milk-offering) that also carries the general sense "heat, warmth." |
| 37 | vastram | garment (accusative) | **वस्त्रम् (vastram)**, from ⟪वस्⟫ (vas), "to wear, clothe" | Dhātuḥ ⟪वस्⟫ | A | Both | Monier-Williams, s.v. *vastra* | Appendix | Exact. |
| 38 | avibhjams | to the sheep (dative plural) | **अविभ्यः (avibhyaḥ)** | Nominal base अवि | C | Both | Whitney, i-stem declension | Endnote | Same ending caveat as row 18. |
| 39 | ka | and | **च (ca)**, "and" | Particle च | B | Both | Monier-Williams, s.v. *ca* | Endnote | Regular sound correspondence. |
| 40 | asti | is (3sg present) | **अस्ति (asti)**, 3sg present of ⟪अस्⟫ (as) | Dhātuḥ ⟪अस्⟫ | A | Both | Whitney §636 | Appendix | Exact — the same word-family as Latin *est*, Greek *esti*, English *is*, and Sanskrit *asti*. |
| 41 | tat | that (neuter) | **तत् (tat)**, neuter of तद् (tad) | Pronominal base तद् | A | Both | Whitney, pronoun tables | Endnote | Exact. |
| 42 | kukruvants | having heard (perfect participle) | **शुश्रुवस् / शुश्रुवान् (śuśruvas / śuśruvān)**, reduplicated perfect active participle of ⟪श्रु⟫ (śru) | Dhātuḥ ⟪श्रु⟫ | B | Both | Whitney §794, perfect participles | Appendix | The Sanskrit perfect-participle architecture reproduces the same reduplication and the same **श्रु** base. The appendix should compare the formation without claiming that Schleicher copied one exact recorded inflected form. |
| 43 | agram | field, plain (accusative) | **अज्रम् (ajram)**, accusative singular of Vedic **अज्र (ajra)**, "field, plain" — not **अग्रम् (agram)**, "tip, point, foremost part" | Nominal base अज्र | B | Vaidika | Monier-Williams, s.v. *ajra*; s.v. *agra* for the contrast | Appendix | This corrects the earlier comparison to the wrong Sanskrit word. Schleicher's meaning matches Vedic **अज्र**, while his **g** replaces Sanskrit **j**. |
| 44 | bhugat | bent away, hence fled (3sg past) | Compare Sanskrit ⟪भुज्⟫ (bhuj), "bend"; the exact relationship remains disputed | Dhātuḥ ⟪भुज्⟫ | D | Both | Schleicher's own German gloss, *bog (entwich)*; Kortlandt's later comparison with Greek *ephyge* and Latin *fūgit* | Endnote only | Schleicher himself explains the action through bending away and fleeing. Sanskrit **भुज्** therefore supplies a semantic as well as phonetic comparison, but the competing reconstructed roots prevent a confident equation. Retain the comparison as unresolved instead of declaring it either exact or coincidental. |

---

## 3. Corrected Counts

Each of the 44 rows belongs to one class:

- **Class A (exact or near-exact recorded Sanskrit form): 14** — rows 1, 2, 4, 9, 13, 15, 17, 22, 30, 31, 36, 37, 40, 41
- **Class B (same Sanskrit form or grammatical base after one explainable sonomer change): 16** — rows 3, 7, 8, 10, 11, 12, 16, 24, 25, 27, 28, 32, 34, 39, 42, 43
- **Class C (Sanskrit base under reconstructed or altered morphology): 11** — rows 6, 14, 18, 19, 20, 23, 26, 29, 33, 35, 38
- **Class D (suggestive but unresolved): 3** — rows 5, 21, 44
- **Class E (no secure Sanskrit comparison): 0**

The table therefore finds a direct recorded Sanskrit form, or a Sanskrit form
separated by one explainable sonomer change, behind **30 of Schleicher's 44
distinct written forms**. Eleven more preserve a Sanskrit grammatical base
under reconstructed morphology. The remaining three comparisons stay
unresolved. These are written forms, not forty-four separate *dhātavaḥ*.

---

## 4. Strongest Examples for the Appendix

Selected for a mix of exact forms, atoms, case relationships, participles,
reduplication, Vedic-domain forms, and one deliberately corrected example,
in the order they appear in the fable:

1. **`dadarka` ↔ ददर्श (dadarśa)** — reduplicated perfect of ⟪दृश्⟫ (dṛś), "saw." Near-verbatim reproduction of the real Sanskrit perfect.
2. **`vaghantam` ↔ वहन्तम् (vahantam)** — present participle of ⟪वह्⟫ (vah), "pulling." Exact participial architecture.
3. **`vāgham` ↔ वाहम् (vāham)** — accusative of वाह (vāha), "vehicle," from ⟪वह्⟫. A real derived Sanskrit noun, one regular sound-change away from Schleicher's spelling.
4. **`bharantam` ↔ भरन्तम् (bharantam)** — present participle of ⟪भृ⟫ (bhṛ), "carrying." Identical written form.
5. **`manum` / `manus` ↔ मनुम् / मनुः (manum / manuḥ)** — accusative and nominative of मनु. Exact, and an occasion to distinguish the common noun from the civilizational name Manu.
6. **`karnauti` ↔ कृणोति (kṛṇoti)**, ⟪कृ⟫ — the Ṛgveda uses **कृणोति** for "does/makes." Schleicher changes the vowel while retaining the consonantal frame, present formation, person, number, and meaning.
7. **`patis` ↔ पतिः (patiḥ)** — "master." Exact, and one of the most recognizable Sanskrit nouns to a general reader.
8. **`krudhi` ↔ श्रुधि (śrudhi)** — a recorded Rigvedic imperative (RV 8.82.6, 10.61.21) of ⟪श्रु⟫ (śru), "hear."
9. **`gharmam` ↔ घर्मम् (gharmam)** — "warm," from घर्म, a real Vedic term for heat. Exact.
10. **`vastram` ↔ वस्त्रम् (vastram)** — "garment," from ⟪वस्⟫ (vas). Exact.
11. **`agram` ↔ अज्रम् (ajram)**, not **अग्रम् (agram)** — Schleicher's meaning is "field/plain." The matching Vedic word is **अज्र**, while **अग्र** means the foremost part, point, or tip.

Held back from the appendix shortlist and retained in the endnote: `vidanti`
and `vividvant-svas`, whose Sanskrit bases are visible but whose reconstructed
grammar is not Sanskrit; `bhugat`, whose relationship to ⟪भुज्⟫ remains
unresolved; and the case-ending rows where the grammatical base is real but
the ending is reconstructed.

---

## 5. Limits Retained in the Endnote

1. Row 6 (`ast` ↔ आसीत्) and row 29 (`vividvant-svas`) remain comparisons to
   a Sanskrit base, not claims of identical Sanskrit grammar.
2. Row 5 (`ā`), row 21 (`aghnutai`), and row 44 (`bhugat`) remain unresolved
   and do not support the appendix argument.
3. The appendix uses only the clearest examples. The endnote preserves all
   forty-four so that a reader can inspect the strong, qualified, and rejected
   comparisons together.
