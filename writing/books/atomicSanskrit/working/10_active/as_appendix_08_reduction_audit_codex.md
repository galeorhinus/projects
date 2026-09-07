# Appendix Part 8 Reduction Audit — Codex

**Manuscript:** `manuscript/as_3_08_one_architecture_two_domains.md`
**Status:** Executed 2026-09-06. The complete 83-category record remains in the printed appendix as 83 unnumbered data cards.
**Current length:** 3,425 words in the Markdown source, including the 83 image records; 3,041 words in Pandoc's rendered plain-text view. The earlier appendix source contained 4,880 words.

## Purpose

Appendix Part 8 supplies the technical evidence behind Chapter 16. It must:

1. demonstrate that वैदिक (*vaidika*) and लौकिक (*laukika*) are two domains within one Sanskrit architecture;
2. show how an additional Vedic resource can contribute to a passage while remaining bounded by fixed wording, pitch, meter, position, or lineage;
3. preserve exact examples of additional sounds, durations, endings, placements, and verbal forms;
4. document the लेट्–लोट् (*leṭ–loṭ*) collisions rather than merely asserting that collisions occur;
5. retain the complete 83-category research record, including open and uncertain findings;
6. show that Vedic preservation and laukika composition were responsibilities carried within one society rather than stages occupied by separate populations.

Chapter 9 already owns the complete explanation of sonances, sonomers, off-grid sonances, and PASS. Chapter 16 owns the conceptual and civilizational account of the two domains. Appendix Part 8 should preserve the evidence required to test those claims without teaching either chapter again.

## Data-Card Finding

The former eight Designed Variations figures did not lose words during PDF conversion. Their Python generator deliberately shortened fields and inserted an ellipsis before creating each SVG. Those figures contained **112 ellipses**, including `Case-agreement differ…`, `Recitation and senten…`, and `P + FN · OP…`.

The source record contains 83 categories and 107 physical rows because some categories carry more than one prevalence measurement. The first redesign stacked several complete records inside each figure. That removed truncation but repeated figure titles and captions, left an unnecessary identifier column, and made it harder to place explanation between groups.

### Implemented design

1. **Printed appendix:** The complete record remains in the main appendix. Each of the 83 categories now occupies one compact data card. The cards are unnumbered and do not appear in the Figure List.
2. **Complete labels:** Each record prints its class, relation, Vedic range, laukika form, qualification, contribution, evidence state, prevalence measure, and evidence grade without ellipses.
3. **Readable scale:** The record ID sits at the upper-right rather than occupying a column. The remaining content receives the full 4.75-inch width. Sanskrit forms appear in Devanagari without a repeated IAST rendering.
4. **Source data:** `working/10_active/as_vaidika_laukika_designed_variations_master.csv` remains the source of truth for all 83 categories and 107 prevalence rows.
5. **Validation:** The validator checks all 83 SVG cards, confirms that every record ID appears exactly once, and fails if an ellipsis or visible IAST returns.

## Proposed Revision

### Opening and §8.1

The opening correctly assigns conceptual ownership to Chapter 16 and technical ownership to this appendix. The second paragraph, however, explains figure machinery before the reader has seen the evidence.

**Current:**

> Chapter 16 explains why Sanskrit uses one architecture in two domains. The वैदिक (*vaidika*) domain preserves received passages exactly, while the लौकिक (*laukika*) domain allows speakers to create new expressions through the same language architecture. This appendix documents the differences between those domains.
>
> Each comparison begins with the form familiar to a student of लौकिक (*laukika*) Sanskrit. It then identifies the additional sound, ending, placement, pitch, or verbal form preserved in a Vedic passage. Chapter 16 defines ten ways in which those additional resources can contribute to the Vedic domain. The next section assigns each contribution a short code and explains how the figures record the passage, local function, frequency, and questions that remain open.
>
> As the book has repeatedly shown, the words वैदिक (*vaidika*) and लौकिक (*laukika*) identify domains of Sanskrit's use rather than periods in a botanical chronology. The Veda can preserve two alternate forms in adjacent verses, as **रुद्रैः (*rudraiḥ*)** and **रुद्रेभिः (*rudrebhiḥ*)** demonstrate below. Their coexistence requires an explanation based on function and setting rather than a story in which one form evolved into the other.

**Proposed:**

> Chapter 16 explains why Sanskrit uses one architecture in two domains. The वैदिक (*vaidika*) domain preserves received passages exactly, while the लौकिक (*laukika*) domain allows speakers to create new expressions through the same architecture. This appendix presents the sounds, endings, placements, pitches, and verbal forms behind that distinction.
>
> Each comparison begins with a form familiar to a student of लौकिक (*laukika*) Sanskrit and then identifies an additional resource preserved in a Vedic passage. The evidence asks what that resource contributes, what additional load it creates, what contains that load, and why the resource belongs within its stated scope.
>
> वैदिक (*Vaidika*) and लौकिक (*laukika*) therefore identify domains of use, not periods in a botanical chronology. Adjacent Ṛgvedic verses can preserve **रुद्रैः (*rudraiḥ*)** and **रुद्रेभिः (*rudrebhiḥ*)**, two endings for the same grammatical relation. Their coexistence calls for an explanation based on their work within each line, not a story in which one form evolved into the other.

### §8.2 Evidence and PASS Method

The present section needs most of its method, but it can explain the records once instead of moving from the four PASS questions to contribution codes, evidence codes, prevalence symbols, grades, and units in six separate blocks.

**Keep:**

- the four PASS questions;
- the ten contribution codes and their table;
- the distinction among a documented form, an exact passage, a demonstrated function, and an open question;
- the distinction among percentages, raw counts, estimates, measured zero, and missing evidence;
- the A–D evidence grades.

**Replace the prose after the contribution-code table.**

**Current:**

> A single form can receive more than one code. An extended ending may complete a metrical line, strengthen its resonance, make a grammatical boundary easier to hear, and give reciters another way to detect a change.
>
> A passage may show exactly what an additional form contributes without explaining why Sanskrit confines that form to the Vedic domain. The appendix therefore records the passage and its immediate function separately from the cost of using the form, the features that keep it bounded, and its final scope. When the evidence does not establish one of those elements, the corresponding entry remains blank.
>
> The evidence column uses **P** when an exact passage has been checked and **FN** when the local function has been demonstrated. **OPEN** means that another part remains unresolved. A blank contribution cell means that the form has been documented but the reason for its selection in that passage has not yet been established.
>
> The prevalence column uses four kinds of markers because the available evidence cannot always be counted in the same way:
>
> 1. A filled bar shows a percentage calculated from a known numerator and denominator.
> 2. A numbered dot shows an absolute count when no complete denominator is available.
> 3. An outlined bar shows an approximate value or a stated upper or lower bound.
> 4. A dashed open cell shows that no reliable numerical measure has yet been established. A measured zero uses a crossed box, so zero cannot be confused with missing evidence.
>
> The letters **A–D** report the evidence grade, while the short unit labels distinguish tokens, lexemes, forms, passages, and examples. Where one grammatical category has several measurements, the figure shows the primary measure and marks the number of additional measurements retained in the underlying data.

**Proposed:**

> One form may contribute in several ways. An extended ending, for example, can complete a metrical line, strengthen its sound, make a grammatical boundary easier to hear, and give reciters another way to detect a change.
>
> The records separate four levels of evidence. **FORM** confirms the form itself. **P** marks an exact passage, and **FN** marks a function demonstrated within that passage. **OPEN** identifies something the present evidence has not explained. The record leaves an unknown field open rather than printing it as zero.
>
> Prevalence also requires different measures. A percentage comes from a known numerator and denominator. A raw number reports a count when no complete denominator exists, while **≈** marks an estimate or bound. A measured zero appears as **0**. The letters **A–D** report the evidence grade, and every measurement states whether it counts tokens, lexemes, forms, passages, or examples.

### §8.3 Sonances, Sonomers, and Domains

This subsection currently repeats Chapter 9's theory in seven paragraphs and then repeats it again in a five-row PASS table. Appendix Part 8 needs the three bounded sounds and their exact examples. It does not need the hypothetical **[ɰ]** and **[ɸ]** candidates that Chapter 9 uses to explain selection into the grid.

**Proposed replacement:**

> Chapter 9 §9.10 distinguishes reusable sonomers from off-grid sonances. This appendix records three such sounds and the boundaries that contain them.
>
> In Ṛgveda 1.1.2, the विसर्ग (*visarga*) before **प** in **अग्निः पूर्वेभिर् (*agniḥ pūrvebhir*)** becomes the [ɸ]-like उपध्मानीय (*upadhmānīya*). Before **क** or **ख**, the corresponding junction produces जिह्वामूलीय (*jihvāmūlīya*) near the back of the mouth. The Taittirīya Saṃhitā preserves that junction in **नमः कपर्दिने च (*namaḥ kapardine ca*)**. The neighboring sounds generate both sonances under stated Sanskrit-wide conditions, so neither requires an independent grid address.[NOTE: vedic-jihvamuliya-upadhmaniya-pair]
>
> The Ṛgvedic **ळ [ɭ]** belongs to a narrower scope. The received words fix its position, and the Ṛgveda-Prātiśākhya specifies its recitational operation. A trained reciter preserves the sound wherever that corpus requires it, while the reusable laukika grid leaves the neighboring retroflex address unassigned.
>
> | Off-grid sonance | Contribution | Bounding support | Scope |
> |---|---|---|---|
> | जिह्वामूलीय (*jihvāmūlīya*) | velar realization of विसर्ग (*visarga*) before **क/ख** | the stated junction generates it | **Restricted** |
> | उपध्मानीय (*upadhmānīya*) | labial realization of विसर्ग (*visarga*) before **प/फ** | the stated junction generates it | **Restricted** |
> | Ṛgvedic **ळ [ɭ]** | exact sound of received Ṛgvedic words | fixed passage, position, and recitational specification | **Lineage-Bounded** |

**Cut:**

- the two hypothetical candidate rows for independent **[ɰ]** and **[ɸ]**;
- the repeated definition of sonance, sonomer, and off-grid sonance;
- the repeated argument about crowding the retroflex grid beside **ड**;
- the third summary of **ळ** as both selection and error detection.

All of that reasoning remains in Chapter 9 §9.10. The exact Vedic examples remain here.

### §8.3 Svara, Chandas, and Exact Recitation

**Keep:** the complete Ṛgveda 10.129.5 example, its translation, the two three-मात्रा (*mātrā*) vowels, and the contrast between a permanent Vedic position and condition-based laukika use.

**Delete after that example:**

> These features change what a student must learn for exact recitation; they do not replace the shared grammar through which the sentence is understood. The opening mantra has no additional ***सुबन्तरूप (*subanta-rūpa*, nominal form)*** or ***तिङन्तरूप (*tiṅanta-rūpa*, finite verbal form)*** that a लौकिक (*laukika*) student must learn.
>
> Students learn these features through a ***शाखा (*śākhā*)***. Its teachers, reciters, छन्दस् (*chandas*), स्वर (*svara*), fixed sequence, and ***पाठ (*pāṭha*)*** methods create several independent checks on the received form.
>
> The assigned स्वर (*svara*) and छन्दस् (*chandas*) satisfy four criteria directly: syllable count and weight, pitch architecture, recitational function, and error detection. स्वर (*Svara*) also contributes to interpretation. Together, pitch and meter make the received form easier to remember, preserve more of its meaning in sound, and give the recitational community more than one way to detect a change.

**Reason:** Chapter 16 owns this conceptual explanation. The phrase “the opening mantra” is also unclear after the RV 10.129.5 quotation. The exact passage and its measured duration carry the appendix's evidentiary work.

### §8.3 Sentence Position, Svara, and a Personal Ending

**Keep substantially unchanged.** The paired **अग्ने / अग्ने॑ (*agne / ágne*)** comparison and the metrical work performed by **एमसि (*emasi*)** are exact examples not supplied together elsewhere in the appendix.

Change the subsection title to plain English after the Sanskrit terms have already been introduced:

> ### Sentence Position, Pitch, and a Personal Ending

### §8.4 Floating Upasargas

The Aitareya Brāhmaṇa example is valuable because prose removes meter as the explanation for the separated operators.

**Current conclusion:**

> The prose passage establishes **REL**, recoverable grammatical relations under invariant sequence. It also establishes that meter cannot be the only reason the वैदिक (*vaidika*) domain permits a separated उपसर्ग (*upasarga*).[NOTE: aitareya-brahmana-separated-upasargas]
>
> The reason for the Vedic scope is specific. Separating an उपसर्गः (*upasargaḥ*) from its atom gives the composer greater freedom over position and arrangement, but it can make the bond between them harder to recover. A Vedic passage prevents that confusion because its words, sequence, and interpretation remain fixed.
>
> Newly composed laukika prose has no fixed passage to preserve the bond. It therefore keeps the उपसर्गः (*upasargaḥ*) closer to its atom.

**Proposed:**

> The prose passage removes meter as the explanation for the separated उपसर्गाः (*upasargāḥ*).[NOTE: aitareya-brahmana-separated-upasargas] The Vedic passage can place other words between each उपसर्गः (*upasargaḥ*) and its atom because the wording, sequence, and interpretation never change. A newly composed laukika sentence must make the same bond clear on its first use, so it keeps the उपसर्गः (*upasargaḥ*) with its atom.

### §8.4 Extended Vibhakti Forms

**Keep:** the complete **रुद्रैः / रुद्रेभिः (*rudraiḥ / rudrebhiḥ*)** comparison, the adjacent Ṛgvedic lines, their translations, and the eleven-syllable calculation.

**Current conclusion:**

> The pair therefore receives **MAT** for syllable count and **ARR** for poetic arrangement. **REL** remains open: the fuller ending may make the grammatical boundary easier to hear, but the present evidence has not demonstrated that contribution.
>
> The selection-and-scope profile explains why the Vedic domain can retain both endings without giving the read-write domain two interchangeable forms for every akārānta word. Their demonstrated contribution is metrical and compositional choice. Their load is duplication: two endings express the same विभक्ति (*vibhakti*), number, and grammatical relation. Fixed passages and meter contain that load in the Veda. Laukika Sanskrit uses **-aiḥ** as the reusable form for new composition.

**Proposed:**

> The two endings perform the same grammatical work but supply different syllable counts. The received lines and their meter keep the choice exact. Laukika Sanskrit uses **-aiḥ** as the reusable ending for new composition, where offering two interchangeable endings for every अकारान्त (*akārānta*) word would add duplication without the Vedic passage to govern the choice.

The proposed paragraph retains contribution, load, boundary, and scope without restating the four labels.

### §8.4 Complete Declensional Record

The eight unreadable figures were replaced first by twenty-one figures and then by 83 unnumbered data cards. The revised introduction states:

> Vedic ***विभक्तिरूपाणि (*vibhakti-rūpāṇi*, declensional forms)*** extend far beyond the **-ebhiḥ / -aiḥ** comparison. The 83 records below include 29 singular, 12 dual, 21 plural, 10 word-class, 7 numeral, and 4 accent-and-recitation records. They retain rare, doubtful, isolated, and unexplained forms alongside the better-understood patterns. Every record gives the Vedic range, the laukika form used for new composition, the contribution established so far, the evidence state, and the available prevalence measure. Its upper-right label provides a stable address into the source record. The codes and evidence grades follow the key in §8.2.

**Delete after the data-card series:**

> The figures produce two kinds of result. In some passages, the evidence explains what the additional form does: it may add or remove a syllable, preserve another grammatical relation, govern a junction, or support a particular arrangement. In others, the evidence confirms the Vedic form but does not yet explain why that passage uses it.

This distinction already appears in the shortened §8.2 method and in the complete data-card record.

### §8.5 The Leṭ–Loṭ Collision Record

**Keep:**

- the exact first-person collisions in both परस्मैपदम् (*parasmaipadam*) and आत्मनेपदम् (*ātmanepadam*);
- the limit of pitch as a disambiguator;
- the difference between exact formal collision and wider functional overlap;
- the pointer to the eighteen-coordinate companion analysis;
- the sequence in which the Vedas use लेट् (*leṭ*) before Pāṇini documents it.

**Delete the concluding PASS table:**

> | Contribution | Load | Bounding support | Scope |
> |---|---|---|---|
> | लेट् (*Leṭ*) gathers desire, intention, urging, and action approaching realization into one verbal resource. | Some forms collide visibly with लोट् (*loṭ*), and much of the semantic range overlaps with लोट् (*loṭ*), लिङ् (*liṅ*), आशीर्लिङ् (*āśīrliṅ*), and लृट् (*lṛṭ*). | Vedic pitch adds grammatical information; fixed wording, syntax, sequence, position, and inherited interpretation complete the boundary. | **वैदिक (*Vaidika*)** |

The four preceding paragraphs already establish every cell in complete sentences. The table adds no new evidence.

### §8.6 Other Vedic Verbal Forms

**Keep all four examples:**

- **वोचम् (*vocam*)**, including the unaugmented form, immediate force, accent, and syllable count;
- **पीत्वी (*pītvī*)**, because its form is secure even though its local selection remains open;
- **अन्वेतवै (*anvetavai*)** and **प्रतिधातवे (*pratidhātave*)**, including their work in Triṣṭubh;
- **चिकित्वः (*cikitvaḥ*)**, because it records a secure Vedic distribution whose local purpose remains open.

Two endings currently repeat that the figure leaves a field blank.

**Current after पीत्वी (*pītvī*):**

> Both forms occupy two syllables, so the change from **-त्वा** to **-त्वी** does not help the meter by adding or removing a syllable. The mantra confirms that the Vedic domain uses **पीत्वी**, but this passage does not tell us why **-त्वी** was selected instead of **-त्वा**. The figure therefore leaves the reason blank.

**Proposed:**

> Both forms occupy two syllables, so **-त्वी** does not alter the meter. The mantra establishes the Vedic form but does not explain why this passage selects it instead of **-त्वा**.

**Current after चिकित्वः (*cikitvaḥ*):**

> Ṛgveda 3.25.1 addresses Agni as **चिकित्वः (*cikitvaḥ*)**, *O knowing one*. It is a ***क्वसु-कृदन्त (*kvasu-kṛdanta*, perfect participle)***. The corresponding लौकिक (*laukika*) vocative, or सम्बोधन (*sambodhana*), is **चिकित्वन् (*cikitvan*)**. The Vedic form is well established in the passage, and its direct-address function is clear, but the local reason for selecting **-वः (*-vaḥ*)** instead of **-वन् (*-van*)** has not yet been demonstrated.[NOTE: vedic-participle-cikitvah]
>
> The passage confirms the Vedic form and its function as a direct address. It does not tell us why the address ends in **-वः** rather than **-वन्**, so the figure leaves the reason blank.

**Proposed:**

> Ṛgveda 3.25.1 addresses Agni as **चिकित्वः (*cikitvaḥ*)**, *O knowing one*. It is a क्वसु-कृदन्त (*kvasu-kṛdanta*), or perfect participle. The corresponding लौकिक (*laukika*) vocative is **चिकित्वन् (*cikitvan*)**. The passage establishes the Vedic form and its direct-address function, but it does not explain why this address ends in **-वः (*-vaḥ*)** rather than **-वन् (*-van*)**.[NOTE: vedic-participle-cikitvah]

### §8.7 The Differences at a Glance

**Keep the small laukika-only table.** Its four rows prevent the two-domain account from falsely implying that every scoped addition belongs to the Vedic side.

The seventeen-row “Complete Comparison” repeats the subjects already demonstrated in §§8.3–8.6 and summarized conceptually in Chapter 16. Replace it with a short conclusion after the laukika-only table.

**Proposed replacement for “The Complete Comparison”:**

> ### The Complete Record
>
> The evidence extends across pitch, duration, off-grid sonances, sound junctions, hiatus, declensional and pronoun forms, verbal endings, participles, infinitives, movable उपसर्गाः (*upasargāḥ*), compounds, derivation, and styles of composition. The sections above demonstrate representative cases in full. The data cards preserve the complete 83-category record, while the Source and Reference Companion supplies the eighteen-coordinate लेट्–लोट् (*leṭ–loṭ*) comparison.[NOTE: designed-variations-figure-sources]

**Cut:** the seventeen-row summary table. It adds no example or measurement that does not already occur in this appendix, Chapter 16, or the companion record.

### §8.8 Documented Stewardship Across Both Domains

The two historical cases are specifically promised by Chapter 16 and should remain.

**Current:**

> Chapter 16 explains that वैदिक (*vaidika*) and लौकिक (*laukika*) identify two responsibilities, not two populations. Historical examples show the same scholars, households, and regional communities preserving Vedic passages while also composing and teaching in laukika Sanskrit.
>
> The fourteenth-century Vijayanagara household associated with Sāyaṇa and Mādhava combined both responsibilities. Its scholars produced extensive explanations of the Vedas while also contributing to व्याकरणम् (*vyākaraṇam*), philosophy, medicine, poetics, music, governance, and other laukika disciplines. Sāyaṇa and Mādhava deserve praise for this range: they preserved and explained the Vedic reference while applying Sanskrit throughout the laukika world.
>
> Kerala's records show the same arrangement at the level of lineages. Named Nambudiri families preserved Ṛgvedic and Jaiminīya Sāmavedic recitation through demanding oral methods. The same regional Sanskrit society produced commentaries on Brāhmaṇas and शिक्षा (*śikṣā*) texts, a निरुक्त (*Nirukta*) analysis, Malayalam explanations of the Ṛgveda, and independent works on Vedic subjects. These records do not establish that every household performed every task. They show that exact Vedic preservation and wide-ranging Sanskrit explanation belonged to one living society rather than to two populations separated by language or chronology.[NOTE: vaidika-laukika-household-responsibility-cases]

**Proposed:**

> वैदिक (*Vaidika*) preservation and लौकिक (*laukika*) composition were two responsibilities within one Sanskrit society. The same households, teachers, and regional communities could preserve received passages while also composing and teaching beyond them.
>
> The fourteenth-century Vijayanagara household associated with Sāyaṇa and Mādhava combined both responsibilities. Its scholars explained the Vedas and contributed to व्याकरणम् (*vyākaraṇam*), philosophy, medicine, poetics, music, governance, and other laukika disciplines. Sāyaṇa and Mādhava deserve praise for that range.
>
> Kerala supplies another documented case. Nambudiri families preserved Ṛgvedic and Jaiminīya Sāmavedic recitation through demanding oral methods. The surrounding Sanskrit society also produced Vedic commentaries, works on शिक्षा (*śikṣā*) and निरुक्त (*Nirukta*), Malayalam explanations of the Ṛgveda, and independent studies of Vedic subjects. Exact Vedic preservation and wide-ranging Sanskrit explanation belonged to one living society.[NOTE: vaidika-laukika-household-responsibility-cases]

**Cut:** the defensive qualification that the records do not establish that every household performed every task. The endnote already handles attribution and scope.

## Cross-Reference Corrections

1. Chapter 16 continues to point to Appendix Part 8 for the full declensional inventory and data-card record.
2. Appendix Part 9 continues to cite Appendix Part 8 as the beginning of the corpus-wide audit.
3. The annotated contents now records the 83-card design.
4. Endnote `designed-variations-figure-sources` now lists §§8.2, 8.4, and 8.7 as its deployments.
5. The source records now identify 83 data cards rather than a numbered figure series.

## Hammer Policy

Appendix Part 8 does not need a new hammer. Its force comes from exact contrasts:

- two endings in adjacent Ṛgvedic verses;
- a prose passage that preserves separated उपसर्गाः (*upasargāḥ*) without metrical pressure;
- exact लेट्–लोट् (*leṭ–loṭ*) collisions;
- Vedic forms whose presence is certain even where their local purpose remains open;
- the same society carrying both responsibilities.

The appendix should end on the last documented stewardship case rather than add a slogan after it.

## Expected Result

The appendix fell from 4,880 words while retaining every substantial Vedic passage, every distinct technical argument, and all 83 catalogue records. Each record is now a self-contained data card that can flow with the surrounding prose.

No evidence would be discarded:

- the printed appendix retains the worked examples and findings;
- the printed appendix retains all 83 categories without ellipses;
- the CSV, prevalence ledger, scripts, and validators remain the source record;
- every removed manuscript passage was copied verbatim into the existing Appendix Part 8 lost-and-found before deletion.

## Build Validation

The validator confirms 107 master subrows, 83 catalogue records, and 83 SVG data cards. Every record appears exactly once. None of the generated SVGs contains an ellipsis or visible IAST.

Pandoc classifies the cards as 83 ordinary images and zero figures. The old twenty-one figures therefore no longer enter the Figure List; the complete B5 build contains 106 numbered figures instead of 127.

The standalone B5 appendix occupies 24 pages. In the complete 498-page B5 short-notes build, the card sequence runs from pages 395 through 409. Representative pages from the singular, dual, plural, word-class, numeral, and accent groups were rendered and inspected. The headings stay with their first cards, the upper-right record labels remain clear, and no card shows clipping, text collision, or an overflow warning.
