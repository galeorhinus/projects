# Vaidika-Laukika Declensional Variations: Prevalence Ledger

**Status:** six-pass numerical prevalence audit  
**Inventory:** 83 rows  
**Primary grammatical sources:** Whitney, *Sanskrit Grammar* §§327-509;
Macdonell, *A Vedic Grammar for Students* §§97-112  
**Corpus checks:** GRETIL *Ṛgveda Padapāṭha*, all ten maṇḍalas; VedaWeb
morphologically annotated Ṛgveda TEI for homograph adjudication

This ledger preserves the numbers behind every prevalence label. A label such
as **COMMON** may help a reader scan a figure, but it must never replace the
numerator, denominator, percentage, textual range, or kind of unit that produced
it.

The Claude research file also reports counts from the Digital Corpus of
Sanskrit. Those counts provide a useful independent check, but they are not
merged into the figure values. The DCS counts cover a differently segmented and
morphologically tagged Saṃhitā corpus, whereas the independently reproduced
counts below use the ten-maṇḍala Ṛgveda *padapāṭha* and the stated VedaWeb
filters. Combining those totals would conceal differences in corpus boundary,
tokenization, and grammatical adjudication.

## Measurement Rules

### What the numbers count

- **Tokens** count occurrences.
- **Lexemes** count distinct words that use a form.
- **Ending classes** count grammatical classes, not occurrences.
- **Textual range** records where the source found the form.
- **Selection rate** compares a Vedic form with its defined alternative:

  `Vedic form / (Vedic form + comparison form)`

These units are not interchangeable. Six lexemes do not mean six occurrences,
and a form found in every maṇḍala can still account for a small percentage of
the available grammatical positions.

### Prevalence labels

| Label | Numerical rule |
|---|---|
| **DOMINANT** | At least 75% of the defined field |
| **COMMON** | 25% to 74.9% |
| **RECURRING** | 5% to 24.9%, or broad recurrence without a complete denominator |
| **RARE** | Below 5% with at least three secure occurrences, or a source-defined small class without a denominator |
| **ISOLATED** | One or two secure occurrences |
| **ABSENT** | Zero occurrences in a completely defined and checked field |
| **UNKNOWN** | The numerator, denominator, or morphological filtering remains incomplete |
| **N/A** | The row records an operation or contrast for which a selection rate would be misleading |

### Evidence grades

| Grade | Meaning |
|---|---|
| **A** | Independently counted and morphologically checked for the narrow claim shown |
| **B** | A grammar reports an exact count, ratio, or bounded numerical statement |
| **C** | Exact corpus spellings were counted, but one or both forms remain morphologically ambiguous |
| **D** | The grammar gives only a qualitative frequency description |
| **U** | No reliable prevalence measurement has yet been recovered |

`A/B` means that the corpus result agrees with an independently reported
grammatical count or ratio. A raw corpus percentage receives **C**, not **A**,
when the spelling can serve more than one grammatical function.

## *Ekavacanam*

| ID | Preserved numerical evidence | Figure value | Scope | Label | Grade | Limitation or exclusion |
|---|---|---:|---|---|---|---|
| SG-01 | Whitney: **-ena** accounts for **8/9** of RV *akārānta* instrumentals; the remaining field includes **-ā**. RV exact example: *mahitvā* **3** times. | **1/9 = 11.1%** for the shorter **-ā** alternative | System-wide | RECURRING | B | **-enā** is a lengthened realization within the **-ena** family and lacks its own count. |
| SG-02 | Whitney: **-ayā → -ā** occurs in **nearly half** the Vedic occurrences. RV raw pair *manīṣā : manīṣayā* = **26:3**. | **≈50%** | System-wide | COMMON | B/C | *Manīṣā* can serve another grammatical relation, so the 89.7% lexical raw share is not the class rate. |
| SG-03 | Macdonell: *ikārānta* **-yā** appears with **5** lexemes against **25** with **-inā**; *ukārānta* **-vā** appears with **4** against **30** with **-unā**. RV raw *paśvā : paśunā* = **2:1**. | **5/30 = 16.7%** (*i* types); **4/34 = 11.8%** (*u* types) | Ending-class; lexical breadth | RECURRING | B/C | The type ratios measure lexemes, while the lexical RV pair measures tokens. |
| SG-04 | Whitney: feminine **-yā / -vā** contracts to **-ī** in **2/3** of occurrences; shorter **-i** occurs sometimes; feminine **-inā** is very rare. | **2/3 = 66.7%** for contraction | Ending-class | COMMON; rare subforms | B | The **-i** and feminine **-inā** subforms still lack exact counts. |
| SG-05 | Whitney: adverbial **-uyā** occurs from **about 6 lexemes**. | **≈6 lexemes** | Small lexical class | RARE | B | No denominator or complete token count is reported. |
| SG-06 | Macdonell: the prevailing *ukārānta* dative type occurs with **more than 60 lexemes**; the shorter **-ve** type with **3**. RV raw *śiśve : śiśave* = **1:2**. | **<3/63 = <4.8%** for the short *u*-class type | One ending-class subcategory | RARE in measured *u* subset | B/C | The *ikārānta* side of the combined row has no equivalent denominator. |
| SG-07 | VedaWeb supplies **18** reviewed neuter *ikārānta/ukārānta* dative-singular tokens; inserted **n** occurs once in *madhune*. The field contains five lexemes. | **1/18 = 5.6%** by token; **1/5 = 20.0%** by lexeme | Annotated RV ending-class subset | RECURRING | A | The token percentage should drive the figure; preserve the lexical breadth in its note. |
| SG-08 | Macdonell reports the prevailing *ukārānta* genitive-ablative type with **more than 70 lexemes** and the competing type with **6**. | **>70/(70+6) = >92.1%** for the prevailing *u*-class type | Related *u*-class field | DOMINANT in measured subset | B | The source denominator is not restricted to the neuter subfield represented by this row. |
| SG-09 | The same *u*-class comparison is **>70:6**; masculine **-unaḥ** occurs **2** times in RV. | **2 tokens** for masculine **-unaḥ** | Mixed common and exceptional subforms | ISOLATED for **-unaḥ** | B | Common **-yaḥ / -vaḥ** and rare **-unaḥ** must remain separate. |
| SG-10 | Whitney: *ikārānta* locative **-ā** occurs **about half as often** as **-au**. RV exact lexical pair *agnā : agnau* = **8:22**. | Source **1:2**, hence **33.3%**; *agni* pair **26.7%** | Ending-class; checked lexeme | COMMON | A/B | The class ratio should drive the figure; the lexical pair may appear as supporting detail. |
| SG-11 | Whitney reports **about 6** locatives in **-ī**. RV raw *vedī* = **3** tokens, including the checked *pragṛhya* passage. | **≈6 reported forms** | Small lexical group | RARE | B/C | Raw *vedī* includes forms whose grammatical function must be checked individually. |
| SG-12 | RV exact lexical pair *sānavi : sānau* = **9:19**. Whitney accepts **-avi** and calls the proposed **-ayi** parallel doubtful. | **9/28 = 32.1%** for *sānu* | Checked lexeme | COMMON for checked lexeme | A | This number cannot be generalized to every *ukārānta* word; **-ayi** remains outside the count. |
| SG-13 | Whitney reports **0** *ikārānta* neuter locatives in **-ini** in the oldest checked texts; **-uni** is “very rare.” | **0** for **-ini** | Defined absence field | ABSENT for **-ini** | B | The **-uni** numerator remains unknown and must not share the zero. |
| SG-14 | Whitney says the later expanded singular endings do not occur in the Veda except doubtful *bhiyāi* once. | **1 doubtful exception** | Broad long-vowel class | ABSENT with doubtful exception | B | Use a numbered dot or range note, not a percentage bar. |
| SG-15 | Same contraction as SG-02: Whitney gives **nearly half** the occurrences. | **≈50%** | System-wide derivative *ākārānta* | COMMON | B | Shares its numerical field and worked example with SG-02. |
| SG-16 | The annotated *śamī* instrumental-singular field has *śamī* **3**, *śami* **5**, and uncontracted *śamyā* **2**. | **8/10 = 80.0%** contracted | Checked lexical paradigm | DOMINANT | A | This is a complete checked lexeme, not a class-wide denominator. |
| SG-17 | VedaWeb confirms *gaurī* once as locative singular at RV 9.12.3c. | **1 token** | Checked lexeme | ISOLATED | A | A percentage from one lexical token would overstate the field. |
| SG-18 | Whitney prints *kartarī*; VedaWeb annotates the sole RV token as *kartari* at RV 1.139.7f. | — | Source-corpus disagreement | UNKNOWN | D | Leave the figure cell open until the accented editions and source scan are reconciled. |
| SG-19 | Whitney says the endingless locative is **considerably more frequent** than the regular form. RV exact pair *mūrdhan : mūrdhani* = **6:6**. | Lexeme pair **6/12 = 50.0%** | Broad class; checked lexeme | COMMON for checked lexeme | A/D | The class-wide source claim is stronger than the one-lexeme ratio but lacks a denominator. |
| SG-20 | Whitney lists **6** clear abbreviated instrumental formations, plus **2** doubtful one-off analyses. RV exact *mahinā : mahimnā* = **38:3**. | Checked lexeme **38/41 = 92.7%** | Rare lexical class; productive within one lexeme | RARE class; DOMINANT checked lexeme | A/B | A dominant lexical pair does not turn the six-lexeme class into a system-wide pattern. |
| SG-21 | Whitney says retained-**a** instances are about as numerous as metrically restored instances. RV *bhūmanā* = **2** raw tokens. | **≈1:1** between the two source groups | Class-level realization | COMMON | B/C | The two source groups are not simply two written endings; the raw token is illustrative only. |
| SG-22 | Whitney reports **more than 100** RV vocatives in **-as** and **0** unquestionable RV vocatives in later **-an**. | **>100/(>100+0) = 100%** | RV *mant/vant* vocatives | DOMINANT | B | This is one of the strongest prevalence measurements in the inventory. |
| SG-23 | RV exact exemplar *cikitvaḥ : cikitvan* = **11:0**; Whitney identifies **-vas** as the RV form. | Exemplar **11/11 = 100%** | Checked lexeme; RV class | DOMINANT for checked lexeme | A/D | A class-wide denominator has not been compiled. |
| SG-24 | RV exact exemplar *ojīyaḥ : ojīyan* = **2:0**; Whitney notes no examples outside RV. | **2 tokens** | RV-only lexical examples | ISOLATED in checked lexeme | A/B | Other comparative vocatives must be added before producing a class ratio. |
| SG-25 | Whitney lists roughly **6** *van*-ending vocative examples, **1** of them doubtful. | **≈5 secure lexemes + 1 doubtful** | Small lexical extension | RARE | B | Token counts remain open. |
| SG-26 | VedaWeb identifies instrumental *tvā* **5** times and instrumental *tvayā* **45** times. Another **590** visible *tvā* forms perform other grammatical jobs. | **5/50 = 10.0%** | Pronoun instrumental singular | RECURRING | A | The morphological filter turns the unusable raw count into a defined comparison. |
| SG-27 | VedaWeb confirms *asme* **212** times and *yuṣme* **6** times as plural pronoun forms. | **212** and **6** tokens | Pronoun case-range contrast | N/A | A | Their case range does not match *asmabhyam/yuṣmabhyam* one-to-one, so use dots rather than a percentage. |
| SG-28 | VedaWeb confirms instrumental *enā* **38** times and instrumental *ayā* **25** times; one verbal *ayā* homograph is excluded. | **38** and **25** tokens | Demonstrative family | RECURRING | A | These are two additional forms within a larger field and do not constitute a complete pair denominator. |
| SG-29 | Of **21** visible *tyā* tokens, VedaWeb identifies **1** as instrumental singular feminine. | **1 token** | Demonstrative family | ISOLATED | A | Twenty homographs are excluded; no *tyayā* token was found. |

## *Dvivacanam*

| ID | Preserved numerical evidence | Figure value | Scope | Label | Grade | Limitation or exclusion |
|---|---|---:|---|---|---|---|
| DU-01 | Whitney: Vedic masculine dual **-ā** accounts for **7/8** of RV occurrences. RV raw *aśvinā : aśvinau* = **351:31**. | **7/8 = 87.5%** | System-wide masculine dual | DOMINANT | B/C | The source ratio is preferable to the 91.9% lexical raw share. |
| DU-02 | Whitney reports only **10** RV **-āu** forms in the *ṛkārānta* dual and says **-ā** is regular there. | Comparator count **10** | Ending-class | DOMINANT | B | The total number of *ṛkārānta* dual tokens is not supplied. |
| DU-03 | For active participles, Whitney reports **-āu** only **1/6 as often** as **-ā**. | **6/7 = 85.7%** for participial **-ā** | One major subset of the combined row | DOMINANT in measured subset | B | Other consonant-ending classes in the row remain uncounted. |
| DU-04 | Whitney: later **-yau** is **unknown in RV**; Vedic **-ī** supplies the dual. RV raw *devī : devyau* = **57:0**. | **0** comparison forms; no token-selection rate | Derivative *īkārānta* dual | ABSENT comparison form | B/C | Raw *devī* also includes singular forms and cannot supply the token denominator. The zero applies to **-yau**, not to the whole dual field. |
| DU-05 | VedaWeb confirms short *śucī* once and a later-form candidate *hariṇī* once; Whitney also lists short *mahi* and treats the RV later-form analysis as uncertain. AV has **-inī 2** times. | RV dots **1 short + 1 later-form candidate**; AV dot **2** | Rare neuter dual field | UNKNOWN | A/B | Preserve source uncertainty and keep *mahi* open for passage review. |
| DU-06 | Whitney reports **1** RV *ukārānta* neuter dual in **-uī**; VS has **-unī 1** time. | RV **1 token** | One lexeme | ISOLATED | B | The comparison belongs to a different text and cannot form an RV percentage. |
| DU-07 | VedaWeb supplies **12** reviewed neuter dual tokens in fuller **-anī/-aṇī**. Whitney and Macdonell describe the fuller pattern as strongly preferred. | **12 tokens** | Ending-class | DOMINANT provisionally | A/D | The complete *an/man/van* denominator remains open; show a dot, not a bar. |
| DU-08 | Whitney reports **1 or 2 doubtful** Vedic **-os** instances. | **1-2 doubtful** | Doubtful field | UNKNOWN | B | Doubtful readings receive no prevalence bar. |
| DU-09 | RV exact raw counts for the second-person dual: *yuvam* **136**, *yuvām* **22**, *yuvabhyām* **1**, *yuvābhyām* **7**, *yuvat* **3**, *yuvoḥ* **31**. | Print six counts, no percentage | Five distinct relations | N/A | A/C | These forms divide grammatical work; they are not competing choices in one denominator. |
| DU-10 | RV exact pair *yuvabhyām : yuvābhyām* = **1:7**. | **1/8 = 12.5%** for the short-vowel form | One pronoun pair | RECURRING | A | The result measures this pronoun, not every instrumental-dative dual. |
| DU-11 | RV exact pair *enoḥ : enayoḥ* = **4:0**. | **4/4 = 100%** | One pronoun | DOMINANT | A | Small denominator; preserve the count with the percentage. |
| DU-12 | Whitney reports relative *yos* **1** time for *yayos*. Raw *yoḥ* has **25** matches, but most are the separate word in *śam yoḥ* and are rejected. | **1 accepted token** | Relative-pronoun exception | ISOLATED | B | Raw homographs must never enter the figure count. |

## *Bahuvacanam*

| ID | Preserved numerical evidence | Figure value | Scope | Label | Grade | Limitation or exclusion |
|---|---|---:|---|---|---|---|
| PL-01 | Whitney: masculine **-āsas** accounts for **1/3** of RV occurrences. RV exact *devāsaḥ : devāḥ* = **123:322**. | Source **33.3%**; exemplar **27.6%** | System-wide; checked lexeme | COMMON | A/B | Use the class-wide source ratio as the principal value. |
| PL-02 | Whitney reports **about 20** feminine **-āsas** examples. RV *vaśāsaḥ* = **1** checked token. | **≈20 tokens** | Feminine extension | RARE | B/A | The total feminine nominative-plural field is not supplied. |
| PL-03 | Whitney says later **-yas** has only **1 or 2 doubtful** RV examples, while **-īs** is the Vedic form. RV raw *devīḥ : devyaḥ* = **53:0**. | Comparison **1-2 doubtful** | Derivative *īkārānta* nominative plural | DOUBTFUL comparison form | B/C | Raw *devīḥ* also includes accusative uses, so the evidence does not supply a token-selection rate. |
| PL-04 | For the checked lexeme *devīḥ*, VedaWeb identifies **37** nominative-plural and **5** accusative-plural tokens. | **37 NOM + 5 ACC** | Checked lexical case distribution | N/A | A | The same form performs both jobs. Use two dots; a class-wide denominator still requires a stem-class census. |
| PL-05 | Macdonell: the unstrengthened masculine type is represented by **1 lexeme occurring 4 times**; the feminine type has **2 examples**. | **4 tokens + 2 examples** | Two rare subcategories | RARE | B | The masculine and feminine subcategories must remain separate. |
| PL-06 | Whitney calls **-ias / -uas** accusatives “sparingly” used, but VedaWeb assigns the visible source-listed matches *paśvas, madhvas,* and doubtful *śucayas* to other relations. | — | Source-annotation disagreement | UNKNOWN | D | Do not convert the disagreement to zero; inspect the passages and source analysis. |
| PL-07 | Whitney: neuter **-ā : -āni = 3:2** in RV. Raw *viśvā : viśvāni* = **271:116**. | **3/5 = 60.0%** | System-wide neuter plural | COMMON | B/C | Raw *viśvā* has other grammatical uses; use the source ratio. |
| PL-08 | Macdonell: short **-ī/-i** forms occur **about 50** times; **-īni about 14** times. | **50/64 = 78.1%** | *Ikārānta* neuter plural | DOMINANT | B | Counts are approximate but share a defined field. |
| PL-09 | Whitney: short **-ū/-u** occurs **more than half as often** as **-ūni**. Macdonell reports the short type across **12 lexemes**. | Short share **>1/3 = >33.3%**; **12 lexemes** | *Ukārānta* neuter plural | COMMON | B | RV raw *madhū : madhūni* = 0:9 is not representative of the class. |
| PL-10 | Whitney: among the two short forms, **-a** occurs **twice as often** as **-ā**; both alternate with **-āni**. RV raw *brahma : brahmā : brahmāṇi* = **96:27:55**. | Preserve source **2:1** between short forms; no complete class share | *An/man/van* neuter plural | UNKNOWN overall | B/C | Raw *brahma* and *brahmā* have other grammatical functions. |
| PL-11 | Whitney reports exactly **2** RV neuter-plural **-ānti** forms. The *padapāṭha* separates the compounds and does not preserve the length contrast as a searchable token. | **2 accepted RV passages** | Two RV passages | ISOLATED in RV | B | Across the wider Vedic corpus the pattern remains rare; the RV figure should say **2**, not merely “rare.” |
| PL-12 | Whitney: **-ebhiḥ** is nearly as frequent as **-aiḥ**. RV broad suffix counts are **585:690**, or **45.9%** for **-ebhiḥ**. Exact pairs: *devebhiḥ : devaiḥ* **49:38**; *rudrebhiḥ : rudraiḥ* **12:4**. | Broad suffix share **585/1275 = 45.9%** | System-wide instrumental plural | COMMON | A/B | Broad suffix counts include pronouns as well as ordinary *akārānta* words; the source confirms the near-even result. |
| PL-13 | RV exact *yebhiḥ : yaiḥ* = **28:0**. | **28/28 = 100%** | Relative-pronoun instrumental plural | DOMINANT | A | This row shares its corpus evidence with PL-21. |
| PL-14 | Whitney calls resolved **-ebhiaḥ** “not infrequent.” | — | Recitational realization | N/A | D | The written *padapāṭha* cannot supply an audible denominator. Use an open cell and a worked recitation. |
| PL-15 | Whitney: simple **-ām** appears in **about 6** RV passages; resolved **-ānām** occurs in **less than half** the **-ānām** instances. | **≈6 tokens** for short form; resolution **<50%** | Two distinct phenomena | RARE short form; UNKNOWN resolution prevalence | B | Never combine the two numbers into one bar. The upper bound alone does not establish a prevalence label. |
| PL-16 | VedaWeb confirms *asme* **212** and *yuṣme* **6**. Whitney says **-bhya** occurs in a number of written or metrically required cases. | E-form dots **212** and **6**; nasal-loss cell open | Two pronoun subcategories | N/A / UNKNOWN | A/D | Split the e-forms from nasal loss because they perform different operations. |
| PL-17 | RV exact pairs: *asmāka : asmākam* **1:106** and *yuṣmāka : yuṣmākam* **2:11**. Combined = **3:117**. | **3/120 = 2.5%** | First- and second-person genitive plural | RARE | A | The combined percentage should retain both component counts. |
| PL-18 | Whitney reports feminine *yuṣmāḥ* **2** times in VS and **0** in the checked RV field. | **2 VS tokens** | VS-only exception | ISOLATED | B | Do not plot the RV zero as an absence claim for the Vaidika domain. |
| PL-19 | After the masculine-dual homograph is removed, VedaWeb gives neuter-plural *imā : imāni* = **63:8**. | **63/71 = 88.7%** | Demonstrative neuter plural | DOMINANT | A | Morphological filtering supplies the valid denominator. |
| PL-20 | After feminine-singular and masculine-dual homographs are removed, VedaWeb gives neuter-plural *yā : yāni* = **50:26**. | **50/76 = 65.8%** | Relative-pronoun neuter plural | COMMON | A | Morphological filtering supplies the valid denominator. |
| PL-21 | RV exact *yebhiḥ : yaiḥ* = **28:0**. | **28/28 = 100%** | Relative-pronoun instrumental plural | DOMINANT | A | Same tokens as PL-13; the figure must not add them twice in aggregate totals. |

## Word-Class and Paradigm Redistribution

| ID | Preserved numerical evidence | Figure value | Scope | Label | Grade | Limitation or exclusion |
|---|---|---:|---|---|---|---|
| CL-01 | Macdonell reports **more than 80** polysyllabic long-vowel lexemes in the secondary group. | **>80 lexemes** | Major word class | RECURRING | B | This is lexical breadth, not a selection rate. |
| CL-02 | Whitney lists three secure RV transfer forms: *dūtiām, śvaśruām,* and *dravitnuā*, with two or three further cases doubtful. | **3 secure + 2-3 doubtful** | Class redistribution examples | RARE | B | The list supplies a dot and a range, not a class percentage. |
| CL-03 | Whitney illustrates four contractions: *āśām, vedhām, surādhās,* and *anāgās*. | **4 source examples** | Cross-class contraction | RECURRING | B | These are source examples, not a complete occurrence denominator. |
| CL-04 | Whitney reports *janūs* once as a transition from an *us*-ending word. | **1 token** | One lexical transition | ISOLATED | B | Broader *is/us* redistribution remains qualitative. |
| CL-05 | One lexical paradigm: *ahan / ahar / ahas*. | **1 paradigm** | One lexeme | N/A | A | A prevalence percentage would add no information. |
| CL-06 | One lexical paradigm: *ūdhan / ūdhar / ūdhas*. | **1 paradigm** | One lexeme | N/A | A | A prevalence percentage would add no information. |
| CL-07 | Inventory covers **4 named lexemes**. | **4 lexemes** | Small lexical class | RARE | B | Token frequencies remain open. |
| CL-08 | One lexical paradigm: *panthā / pathi / path*. | **1 paradigm** | One lexeme | N/A | A | Show the paradigm rather than a percentage. |
| CL-09 | Whitney reports only **3** RV forms built from the later middle **-vat** form and **0** in AV. | **3 RV tokens; 0 AV** | Perfect-participle redistribution | RARE | B | The competing weak-form denominator remains open. |
| CL-10 | Participial dual **-āu** occurs **1/6 as often** as **-ā**, so **-ā** has a **6/7** share. The separate neuter plural **-ānti** occurs in **2** RV passages. | Dual **85.7%**; plural **2 tokens** | Two distinct subclaims | DOMINANT dual; ISOLATED plural | B | Split this row visually. |

## Numerals

| ID | Preserved numerical evidence | Figure value | Scope | Label | Grade | Limitation or exclusion |
|---|---|---:|---|---|---|---|
| NU-01 | RV exact *dvā : dvau* = **17:4**. | **17/21 = 81.0%** | Masculine form of “two” | DOMINANT | A | Small but fully searchable contrast. |
| NU-02 | VedaWeb identifies all *trī/trīṇi* matches as nominative-accusative neuter plural: **22:32**. | **22/54 = 40.7%** | Neuter “three” | COMMON | A | Morphological filtering supplies the complete pair field. |
| NU-03 | Whitney reports *trīṇām* **1** time in RV; corpus pair *trīṇām : trayāṇām* = **1:0**. | **1 token** | One numeral relation | ISOLATED | A/B | The 100% pair share is less informative than the single occurrence. |
| NU-04 | After four verbal *aṣṭa* homographs are removed, VedaWeb gives numeral *aṣṭa : aṣṭā : aṣṭau* = **1:2:3**. | **16.7% : 33.3% : 50.0%** in a six-token field | Numeral-specific range | RECURRING / COMMON | A | Preserve each count beside its small-denominator percentage. |
| NU-05 | *Pañca* has **40** visible tokens, but token morphology alone cannot identify every uninflected numeral beside an oblique noun. RV 2.2.10c verifies *pañca kṛṣṭiṣu*. | **1 checked construction** | Syntactic construction | N/A | A/C | Use a checked-example dot; do not graph the forty visible tokens. |
| NU-06 | *Sahasram* has **54** visible annotated tokens and *śatam* **83**, but token morphology alone cannot identify every construction. Two passages verify the pattern. | **2 checked constructions** | Syntactic construction | N/A | A/C | Use checked-example dots; do not graph the visible token totals. |
| NU-07 | Accent placement is an operation, not a choice between two written forms. | — | Accent rule | N/A | U | Measure textual spread later, not selection rate. |

## Accent and Recitation

| ID | Preserved numerical evidence | Figure value | Scope | Label | Grade | Limitation or exclusion |
|---|---|---:|---|---|---|---|
| AC-01 | No complete count of vocative-accent expressions has been assembled. | — | Sentence accent | N/A | U | A passage count may later show textual spread. |
| AC-02 | No complete count of accent-moving declensional classes has been assembled. | — | Declensional accent | N/A | U | Count classes and passages separately. |
| AC-03 | Whitney: resolved **-ānām** occurs in **less than half** its instances; resolved **-ebhiaḥ** is “not infrequent”; other resolutions remain uncounted. | **<50%** for the **-ānām** suboperation | Recitational realization | UNKNOWN prevalence | B/D | The upper bound does not establish a prevalence band, and the written corpus cannot alone recover audible resolution. |
| AC-04 | Three checked examples currently support *pragṛhya*: *vedī asyām, yuṣme id,* and *tve id*. | **3 worked examples** | Junction behavior | RECURRING evidence, prevalence unknown | A | These examples demonstrate the operation but do not measure its entire field. |

## Evidence Progress

These counts measure the state of the research, not the prevalence of Vedic
forms.

| Measure | Count |
|---|---:|
| Inventory rows | 83 |
| Rows carrying at least one retained number, including a defined zero | 76 |
| Rows with a graphable percentage or bounded percentage | 39 |
| Rows with exact or approximate absolute counts but no complete denominator | 37 |
| Rows still lacking a reliable numerical measurement | 7 |
| Rows represented by more than one numerical or evidentiary subrow | 18 |

## Prevalence Coverage

| Best available numerical treatment | Rows |
|---|---:|
| Percentage, ratio converted to a percentage, bounded percentage, or defined zero | 39 |
| Absolute token count, lexical breadth, or raw count with no complete denominator | 37 |
| No reliable number yet | 7 |
| **Total** | **83** |

Eight of the 83 rows are marked **N/A** because they describe distinct
grammatical relations, a lexical paradigm, or an audible operation rather than
two competing forms. Some of those seven still retain useful absolute counts.

## Figure Rules

1. Preserve the numerator and denominator beside every plotted percentage.
2. Mark **tokens**, **lexemes**, and **ending classes** with different symbols.
3. Use open bars for approximate or bounded values such as **≈50%**, **>33.3%**,
   and **<4.8%**.
4. Use dots rather than bars for isolated absolute counts.
5. Give raw spelling counts a visibly different treatment from grammatical
   counts.
6. Split mixed rows before graphing them. SG-09, SG-13, SG-20, PL-05, PL-15,
   PL-16, CL-10, and AC-03 especially require separate subrows.
7. Preserve an explicit **UNKNOWN** state. An empty field must never be rendered
   as zero.
8. Record the corpus boundary in the figure note: the independent token counts
   currently cover the ten-maṇḍala RV *padapāṭha*, while some grammar-reported
   counts extend to AV, VS, Brāhmaṇa prose, or the wider Vaidika domain.

## Reproduction

Run:

```bash
python3 analysis/vaidika_laukika/count_rv_padapatha_prevalence.py \
  --format csv > /tmp/rv_padapatha_prevalence.csv
```

The script downloads the ten GRETIL RV *padapāṭha* files into a temporary cache
and reports exact token spellings with passage references. Its output is a raw
measurement. The acceptance and exclusion decisions in this ledger supply the
grammatical review that a spelling search cannot perform.

Rows that required morphological filtering were reproduced with:

```bash
python3 analysis/vaidika_laukika/adjudicate_rv_prevalence.py \
  --tei-dir /path/to/c-salt_vedaweb_tei \
  --output working/10_active/as_vaidika_laukika_morphological_adjudication.csv
```

The checked extraction used VedaWeb TEI commit
`6d94702e078b2d8fc04af1241aba63132c4601a3`. Add
`--include-rejected` to retain every rejected homograph and suffix match.
