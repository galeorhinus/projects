# Expanded Endnote Reduction: Lost and Found

**Started:** 2026-09-06
**Purpose:** Preserve substantive prose removed from expanded endnotes. This file is not assembled into either book.

## Batch 1

The complete pre-reduction entries remain recoverable from git commit `efe11a16`. The passages below retain research or interpretation removed from the reader-facing notes; purely repetitive transitions are not reproduced.

### `rigveda-10-71-2-sieve-vak`

> The *Ṛgvedic* speech-cluster treats *vāc* as a deeper category: meaningful, measured, hidden, revealed, transmitted, mantra-bearing, and formed by intelligence. Ṛgveda 10.71.1 links *vāc* with meaningful naming and with an excellent hidden portion disclosed through affection. Ṛgveda 10.71.2 describes Speech as sifted and refined like grain, then formed by the wise with the mind. Ṛgveda 10.71.3 says the path of Speech was found, that Speech entered the ṛṣis, and that she was distributed widely. Ṛgveda 10.71.4 distinguishes mere seeing and hearing from true access: one may look and not see Speech, listen and not hear her, while to another she reveals her body. Ṛgveda 10.71.7 grades speakers by depth of access despite shared eyes and ears. Ṛgveda 1.164.45 describes Speech as measured in four quarters, three hidden and one spoken. Ṛgveda 8.100.11 invokes divine Speech as generated, many-formed, spoken by animals, and nourishing like a cow. Ṛgveda 10.125 speaks in Vāc's own voice and presents her as the power that enables the ṛṣi and the one of clear intelligence.

> Sāyaṇa can stand in the note without changing the body. His ritual and recitational frame belongs to the lineage of use. The architectural account sits underneath that frame: ritual performance, recitation, and recognition presuppose Speech already sifted, formed, recognized, and preserved. The two accounts need not compete.

> The point does not depend on accepting the pyramid's clock for Maṇḍala 10. However that chronology is argued, the verse remains inside the Vedic speech-world. The Vedic corpus itself describes Speech through selection, refinement, mental formation, social recognition, and radiance.

### `rigveda-10-71-4-vach`

Additional sandhi notes removed from the expanded entry:

> - **पश्यन्न ददर्श** ← *paśyan* + *na dadarśa* — *paśyan* ends in *n*; *na* begins with *n*; the doubling is a Vedic sandhi geminate.
> - **उतो त्वस्मै** ← *uto* (= *uta* + *u* particle) + *tasmai*.
> - **जायेव** ← *jāyā* + *iva* — *guṇa* sandhi under *Aṣṭādhyāyī* 6.1.87: *ā* + *i* → *e*.

The removed word table parsed all eighteen words in the mantra: **उत, त्वः, पश्यन्, न, ददर्श, वाचम्, शृण्वन्, न, शृणोति, एनाम्, उतो, त्वस्मै, तन्वम्, वि सस्रे, जायेव, पत्ये, उशती, सुवासाः**. Their glosses established the same translation retained in the shortened note. The full table can be recovered from commit `efe11a16` if a later grammatical appendix needs it.

The longer application to Chapter 13 also listed trained ear, trained mouth, recitational discipline, correction, and lineage as the architecture that prepares a listener. That explanation remains in the chapter and was removed here to avoid repeating it.

### `rigveda-10-125-vak-ambhrini`

The full cosmic-scope verses removed from the note:

> **अहं सुवे पितरमस्य मूर्धन्मम योनिरप्स्वन्तः समुद्रे ।**
> **ततो वि तिष्ठे भुवनानु विश्वोतामूं द्यां वर्ष्मणोप स्पृशामि ॥**
>
> *ahaṃ suve pitaram asya mūrdhan mama yonir apsv antaḥ samudre |*
> *tato vi tiṣṭhe bhuvanānu viśvotāmūṃ dyāṃ varṣmaṇopa spṛśāmi ||*
>
> *I give birth to the Father on the summit of this; my womb is in the waters, within the ocean. From there I spread out over all worlds; I touch yonder sky with the crown of my head.*

> **अहमेव वात इव प्र वाम्यारभमाणा भुवनानि विश्वा ।**
> **परो दिवा पर एना पृथिव्यैतावती महिम्ना सं बभूव ॥**
>
> *aham eva vāta iva pra vāmy ārabhamāṇā bhuvanāni viśvā |*
> *paro divā para enā pṛthivyaitāvatī mahimnā saṃ babhūva ||*
>
> *Like the wind I blow forth, taking hold of all worlds. Beyond heaven, beyond this earth — such has my greatness become.*

The removed three-layer formulation argued that the received object is grammatically feminine, the reception mechanism is based on the faculty of seeing, and the *Sarvānukramaṇī* records female and male seers through the same categories. The shortened note retains the received classification and the list of female seers without repeating the argument three times.

### `rigveda-1-164-39-akshara-assembly`

> The four-term stack (*engineered / encoded / decoded*) ordinarily casts the Veda as *encoding*: the architecture is encoded *in the form* of the language — the *varṇamālā* in how sounds are ordered, the bonding procedure in how words assemble — and a *vaiyākaraṇaḥ* must *decode* it to state the specification explicitly. Verse 39 is the unusual case. It does not merely encode the architecture in its form; its *content* states the principle outright — the *ṛc* resides in the *akṣara*, the assembled utterance grounded in the imperishable unit beneath it. This is a self-definitional moment: the Veda stating, in propositional form, the very scale-relation the rest of the corpus only encodes.

> The verse does not lift the *ṛc* into a heaven *above* it. It locates the *ṛc* in the *akṣara* — the syllable, a scale *below* the assembled utterance — and the locatives *akṣare* and *parame vyoman* can be read in apposition: the imperishable syllable *is* **परमे व्योमन् (*parame vyoman*)**, the highest heaven. The supreme ground is then not the loftiest point but the smallest recoverable unit; the architecture's highest place is reached by descending the scale to the unit beneath the form, not by ascending above it.

### `dhatupatha-empirical-distribution`

The shortened note points to Reference Appendix 6 for these implementation details:

> - Read `data/dhatupatha.csv`.
> - Apply *it-saṃjñā* rules to the marked citation form before deleting the remaining notation.
> - Map every remaining SLP1 character to V or C.
> - Classify each धातुः (*dhātuḥ*) by structural pattern, sonomer count, and अक्षर (*akṣara*) count.
> - Produce summaries by गणः (*gaṇaḥ*), scaffold, sonomer count, and अक्षर (*akṣara*) count.

The original entry also recorded the parser's legacy fallback for unmarked final short vowels and the complete SLP1 vowel and consonant inventories. Those belong with the script documentation rather than in a second copy inside the endnotes.

## Batch 2

### `paspashahnika-apabhramsa-passage`

The longer entry presented three observations after quoting Patañjali's complete passage. It separately explained that the maxim and example form one argument, that **तद्यथा (*tadyathā*)** connects the example to the principle, and that the passage is commentarial prose rather than verse. The shortened note retains all three points without restating the textual unity after each one.

### `sura-dhatu-dipti`

The removed later comparison came from Śatapatha Brāhmaṇa 11.1.6.7–8 in Julius Eggeling's translation, *Sacred Books of the East*, volume 44 (1900), pages 13–14. The passage associates creation through the mouth with daylight and creation through downward breath with darkness. Taittirīya Brāhmaṇa 2.2.9.5–8 offers a parallel creation sequence, while 2.3.8.2 and 4 use a *su-/asu-* wordplay. These later passages can support a separate study of light and darkness, but they do not determine how a particular Rigvedic ***asura*** should be divided.

The removed modern-reception paragraph noted that a WisdomLib rendering of RV 2.1.6 distinguishes a praised title from an “A-Sura” or “Anti-Shining” interpretation. It established only that a modern interpreter had used the privative reading, not that the mantra required it.

### `brugmann-grundriss-1886`

The longer production history named the first-edition volume sequence: *Lautlehre* (1886–1892), *Wortbildungslehre* (1889–1892), *Stammbildungs- und Flexionslehre* (1888–1892), and Delbrück's *Syntax* (1893), followed by revised editions through 1916. It also named August Leskien's *Die Declination im Slavisch-Litauischen und Germanischen* (1876), Konrad Koerner's *Historiographia Linguistica*, and H. A. Strong's English translation of Hermann Paul's *Principles of the History of Language* (1890). These details remain recoverable from commit `efe11a16` if the historiographic appendix later needs expansion.

### `petrified-bounded-forms`

The longer Arabic discussion distinguished Quranic Arabic, Modern Standard Arabic, and spoken Arabics, then described ALECSO and the Arabization Coordination Bureau as institutions that influence formal terminology and circulation. The source links remain in `arabic-religio-political-authority`, `quranic-engineered-preservation`, and the source registry.

The longer Hebrew source list included Benjamin Harshav's *Language in Time of Revolution* (1993), Lewis Glinert's *The Story of Hebrew* (2017), Ghil'ad Zuckermann's *Language Contact and Lexical Enrichment in Israeli Hebrew* (2003), Bernard Spolsky on revernacularization, and the Academy of the Hebrew Language's “Hebrew through the Ages.” These records remain in the dedicated Hebrew notes and source registry.

## Batch 3

### `bhagavad-gita-16-6-daiva-asura`

The removed word table parsed all fourteen words in Bhagavad Gītā 16.6. The four removed sandhi notes explained **लोकेऽस्मिन्**, **दैव आसुर**, **दैवो विस्तरशः**, and **प्रोक्त आसुरम्**. Neither the table nor those junction operations were used by Chapter 1, which cites the verse only for **द्वौ भूतसर्गौ (*dvau bhūtasargau*)**, the two created formations. The complete pre-reduction parsing remains recoverable from commit `efe11a16`.

### `deccan-college-founding-arc`

The longer interpretation described Deccan College as the principal western-Indian institutional home of Sanskrit scholarship and argued that deep Indian work in editing, manuscript collation, grammar, and *darśana* was placed inside an academic structure serving European comparative philology. It then characterized the post-1948 *Encyclopaedic Dictionary of Sanskrit on Historical Principles* as a continuation of that framework. The shortened note retains the institutional transition and the Appendix deployments without repeating their full indictment.

## Batch 4

### `skeat-aryan-roots-and-edition-drift`

The longer entry reproduced Skeat's 1882 key, Root 87, and GENUS entry at greater length, then repeated the same GAN/GEN and SKAR/SKER comparison under a second heading. It also explained twice that Skeat treated the capitalized forms as reconstructions and that the chapter follows their changing presentation rather than accusing him of presenting them as recorded words. The shortened note retains the two editions, page locators, scan identifiers, Sanskrit-alphabet ordering, and all changes used by Chapter 19.

### `place-of-articulation-sanskrit-terms`

The removed conclusion compared Sanskrit's place-and-manner organization with the International Phonetic Alphabet and argued that modern speech science retains nearly the same organizing structure without crediting Sanskrit. That is a separate historical claim documented by `western-linguistic-encounter-sanskrit-1786-1879`. The shortened note keeps the five Sanskrit terms, their anatomy, the five *vargas*, and Allen's page locator.

### `bopp-1816-conjugationssystem`

The longer entry named Bopp's 1816 study as the beginning of the operation, then restated the same Sanskrit-to-PIE anchor change through a four-stage chronology and the baking metaphor. The shortened note keeps Bopp's training, full 1816 title and method, the 1833–1852 extension, and the transition through Schleicher and Brugmann.

### `schleicher-1861-compendium`

The removed close repeated that the *Compendium* placed a reconstruction above the recorded evidence and described the 1868 fable as the bake's first finished good. The shortened note keeps the systematization claim and points directly to the separate fable note.

## Batch 5

### `compatibility-is-not-immunity`

The longer entry separately catalogued the strengths of *nāstika* and *prākṛtika* formations, followed by a list of the pyramid's methods: centralization, institutional capture, scriptural finality, imperial patronage, conversion, shame, administrative classification, and ideological re-authoring. The shortened note retains the compatibility/immunity distinction, the role of civilizational memory, the linguistic parallel, and the two institutional research records.

### `ramayana-homer-chronology-capture`

The removed close restated that the sources establish the imposed chronology, Weber's direct-borrowing claim, and West's common-inheritance framework. The shortened note retains each of those facts where its source is discussed. It also removes a duplicated deployment line and corrects an accidentally repeated phrase.

### `three-deployments-framework`

The longer entry repeated the complete corpus/document/restatement explanation from the Short, then explained the same distinction again in a separate paragraph. The shortened entry keeps the three definitions, explains why they are not codifications, and identifies the internal chapter and thesis sources.

### `ipa-1886-1900-chart`

The removed material listed later IPA chart revisions in 1932, 1989, 1993, 1996, and 2005. It also repeated the Schlegel, Bopp, Böhtlingk, and Whitney chronology already held by `western-linguistic-encounter-sanskrit-1786-1879`. The deployed claim ends with the first full chart in 1900, so the shortened note retains that sequence and points to the dedicated chronology.

## Batch 6

### `jones-1786-third-anniversary-discourse`

The longer supporting entry repeated the nineteenth-century engagement with Sanskrit and the eventual IPA place-and-manner grid. The shortened note retains Jones's date, publication, argument, place in comparative philology, and modern source list, then points to the dedicated chronology.

### `staal-mendeleev-varga-comparison`

The longer entry explained three times that the periodic table and *varga* matrix assign units to property-bearing coordinates and permit an open cell to be characterized. The shortened note keeps that comparison and the boundary between Staal's structural insight and his unsupported historical extension.

## Batch 7

### `indo-european-narrative-inheritance`

The longer close restated the recorded status of the Vedic and Greek figures before repeating that the proposed common ancestral corpus is inferred. The shortened note retains all three comparisons, West's page ranges, Watkins's formula, and the distinction between recorded stories and their reconstructed ancestor.

### `architecture-not-analysis-pratisakhya`

The removed chemistry survey named Lavoisier's 1789 treatise, Dalton's atomic theory, Mendeleev's 1869–1871 *Principles of Chemistry*, the later discoveries of gallium, scandium, and germanium, and Moseley's 1913 atomic-number analysis. The shortened note preserves that development sequence without reproducing every date and example inside a Sanskrit phonetics note.

### `dionysius-thrax-techne`

The longer entry listed the same Greco-Indic routes twice: Alexander's campaigns, Mauryan-Seleucid exchange, Greco-Bactrian and Indo-Greek rule, Aśoka's Greek inscriptions, and Buddhist movement. The shortened note retains the complete sequence once and preserves the distinction between possible transmission and a directly recorded teacher or work.

## Batch 8

### `sandhi-anusvara-assimilation`

The longer entry first identified *anusvāra* assimilation as snap-to-grid and then described separate articulator movements, acoustic clarity, and mechanical simplicity in a second paragraph. The shortened note retains the complete five-place table, both Pāṇinian rules, and one direct explanation of the shared contact point.

### `vyanjana-duration-shiksha`

The longer entry stated three times that a *mātrā* is proportional rather than a fixed millisecond value. The shortened note keeps the complete *Śikṣā* verse, the four ratios, the scaffold application, the distinction from metrical syllable weight, and the modern-phonetics boundary.

## Shorter-Entry Structural Cleanup

The published notes no longer narrate superseded drafts. The removed editorial history covered these corrections:

- The *mūrdhanya* articulation line is sourced to the *Siddhāntakaumudī* and *Laghusiddhāntakaumudī*, not the *Pāṇinīya Śikṣā*.
- The *suṭ* note now separates rules 6.1.135 and 6.1.137–139 from the unrelated visarga context of 8.3.46.
- Yāska's *Nirukta* does not contain the phrase ***asurāḥ suravirodhinaḥ***; the Kauthuma Padapāṭha supplies the explicit privative division.
- The Nārāyaṇīya Madhu-Kaiṭabha theft and the *Bhāgavata Purāṇa* Hayagrīva theft remain separate from the different *Devī Māhātmya* and *Devī Bhāgavata* narratives.
- Schleicher's organic account of language does not make him a professional botanist.
- The pre-Pāṇinian grammarian entry now gives rule locators without attaching inaccurate one-line summaries.
- The *ayogavāha*, *anusvāra*, *visarga*, and Mishra notes no longer use unsupported *kumbhaka/recaka* equations.
- The *Sindhu/Hinduš/Indos/Indus* note treats each ending through the grammar of its receiving language rather than as a rendering of Sanskrit visarga.
- The received *Prātiśākhya* and *Śikṣā* works document a logically prior sound discipline without assigning every work a pre-Pāṇinian date.
- The Tamil aspiration, Ho/Mundari glottal, and global retroflex notes now stay within their directly sourced inventories and regional claims.
- The *Vāsiṣṭhī-Śikṣā* is described through its corpus-counting function rather than as a Sāmavedic recitation manual.
- The *asura* note separates Mayrhofer's lord/king proposal, Yāska's life-breath analysis, the Kauthuma division, and the Uṇādi record.
- The Kailāsa note no longer relies on unsupported stone-volume, excavation-sequence, or load-calculation claims.
- The Nambūdiri fieldwork notes distinguish documentation of one community or several named branches from a universal sound-by-sound comparison.
- Appendix Part 1's source note keeps ⟪भा⟫ and ⟪भाष्⟫ distinct and removes incorrect assignments of **जगति** and **प्राप्ति**.
- The inherent-vowel axis uses that anatomical name rather than the inaccurate label “open-vowel core.”
