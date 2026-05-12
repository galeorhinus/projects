# Atomic Sanskrit — Ch7 Notes (Restructured for 7A/7B Split)

> **Status:** Ch7 splits into two chapters: **7A — *The World's First Instrument*** and **7B — *Mapping the Mouth***. During drafting, both live in a single file `as_ch07_draft.md` with distinct chapter-block separation. The final split (separate files, sequential chapter numbers) is mechanical and happens after both halves are reviewed and locked.
>
> Pre-split notes (architecturally superseded) archived at `as_ch07_notes_pre_split.md`. Some content-level details there (e.g., engineering payoff sequences, polemic phrasing) remain relevant to 7B; refer back when useful.

---

## Locked Architectural Decisions

### Chapter titles
- **7A**: *The World's First Instrument*
- **7B**: *Mapping the Mouth*

### Why the split
The pre-split single chapter was doing two distinct kinds of work — (a) introducing the vocal apparatus and its Sanskrit vocabulary, and (b) delivering the engineering argument that the *varṇamālā* is the engineered selection from that apparatus. Forcing both into one chapter inflated length to ~5,200 words and forced the reader into polemic before they understood the apparatus. Splitting separates teaching from arguing.

### Voice register
- **7A**: descriptive science. No polemic. No hammers. No scare quotes flagging establishment terms. No Western-vs-Indic verdict claims. Reads like an intelligent general-audience chapter on phonetics, anchored in Indian musical tradition. The Sanskrit vocabulary in Part 2 is introduced as another well-developed naming system — not declared superior; the reader is left to notice that Sanskrit's terms are anatomically grounded.
- **7B**: full polemic voice. Hammers. Scare quotes. Dichotomy → reframe. Pāṇini-was-second. *Phonics is a workaround. The varṇamālā is the engineering.*

### File strategy
**Option C** — Single file `as_ch07_draft.md` containing both chapters as distinct chapter blocks (`# Chapter 7A — The World's First Instrument` and `# Chapter 7B — Mapping the Mouth`), separated by clear delimiter. When ready to split: extract by chapter heading into two files. Mechanical operation.

### The category-vs-inventory boundary (load-bearing rule)
- **7A** names **categories** of sound — both in English and in Sanskrit — without naming any specific consonant or vowel.
- **7B** reveals the **inventory** — the specific 25 + 14 + 4 + 4 sounds and letters the *varṇamālā* committed to.

This rule is what makes the split pedagogically airtight. The reader finishes 7A knowing what kinds of sounds humans make and what Sanskrit calls each kind; they do not yet know which specific sounds Sanskrit selected. 7B's reveal lands fresh.

**Concretely, this means:**
- 7A uses *sparśa*, *swara*, *antaḥstha*, *ūṣman* as category-words (the kinds of sounds)
- 7A does NOT use *varṇa*, *varṇamālā*, *varga*, or any specific Devanagari letter (क, ख, ग, अ, इ, etc.)
- 7B introduces *varṇa* and *varṇamālā*, names the inventory counts, shows specific letters

### The 7B crystalline thesis
> **The names of the sound happen to be the sound itself.**

Placement: §7B.2 close (after the inventory is named and the *architects chose a selection* observation lands). The chapter's deepest engineering claim about the *varṇamālā* — that the script does not represent sound, it constitutes the sound's specification.

### Chronology rule (chapter-wide, inherited from style guide)
- No specific dating for Indic figures/texts. Use *across many generations of guru-shishya transmission*; *before Pāṇini*; *long before any European systematic phonology*.
- External dates fine: Jones 1786, Bopp 1816, IPA 1886/1888, etc.
- Internal-frame anchors: *Vedic mode*, *Prātiśākhya tradition*, *Post-Pāṇinian* — not *Old Indic*, not *family-tree taxonomy*.

---

## 7A — *The World's First Instrument*

### Architectural overview

**Target length:** ~2,500–3,000 words.

**Two-part structure:**
- **Part 1** (~1,500 words): The mouth as instrument, anatomy in English, music-tradition framing throughout, cross-language examples.
- **Part 2** (~1,000–1,500 words): The same apparatus in Sanskrit vocabulary — anatomical terms (*sthāna*, *prāṇa*, *ghoṣa*, *anunāsika*), the *sthāna*/*prayatna* canonical pair, and category-vocabulary (*sparśa*, *swara*, *antaḥstha*, *ūṣman*) introduced as kinds-of-sounds.

**Pivot between parts:** §7A.6 turns the diagram over — same anatomy, Sanskrit naming system. No transitional fanfare. The chapter simply continues describing the apparatus, switching vocabulary.

### Music-tradition framing (the chapter's voice anchor)

**The core classical claim:** The human voice is the *original* instrument. All constructed instruments approximate one or another of its capabilities. This is a serious classical position, attested in *Nāṭyaśāstra* and the *Saṅgīta Ratnākara* tradition. Sanskrit term: *ādi-vādya* आदिवाद्य (original instrument); related: *gātra-vīṇā* गात्र-वीणा (body-instrument).

**The four-category instrument taxonomy** (from *Nāṭyaśāstra*, deferred to endnote):
- *Tata* तत — stringed (oscillator-based: sitar, sarangi, sarod, veena)
- *Suṣira* सुषिर — wind / hollow (resonant-tube-based: bansuri, shehnai, conch)
- *Avanaddha* अवनद्ध — covered / membrane (percussion-resonator-based: tabla, mridangam, dholak)
- *Ghana* घन — solid (self-resonating: manjira, ghaṭam)

**Implementation rule (Reading C from session):**
- Instrument names in prose: sitar, sarangi, bansuri, tabla — recognizable to readers, no glossing needed
- Sanskrit taxonomy terms (*tata, suṣira, avanaddha, ghana, ādi-vādya, gātra-vīṇā*) — in endnotes only
- Diagrams may include Sanskrit anatomy labels (FIGURE 7A.2)

**Instrument-to-sound-type mapping (locked):**

| Sound type | Indian instrument analog | Why it works |
|---|---|---|
| **Vowels** | **Sarangi + bansuri** | Sarangi: sustained pitch with continuous variation, sympathetic resonance — closest constructed instrument to the human voice. Bansuri: air column with finger-controlled effective length, exactly mirrors what the vocal tract does for vowels. |
| **Consonants** | **Tabla** | Discrete events of contact (hand-on-skin = tongue-on-palate). The *bol* pedagogy — drummers learn rhythm by speaking the syllables (*dha dhin dhin dha*) before striking the drum — is the single sharpest illustration that *the voice is the original instrument and the drum is constructed to approximate it*. Load-bearing for the chapter. |
| **Mixed case** | **Sitar** | Pluck-attack (consonant-like event) + sustained decay (vowel-like). Mentioned briefly as illustrating speech's alternation between consonant-events and vowel-sustains. |

**Sample voice lines that test the register (drafted):**

> The Indian classical tradition holds that the human voice is the original instrument. Every constructed instrument descends from it. The tabla extends what the voice does when it makes a plosive consonant; the bansuri extends what the voice does when it sustains a vowel; the sarangi extends what the vocal cords do continuously and the nasal cavity does as a sympathetic resonator. The instrument-builder approximates one aspect; the speaker has them all.

> A tabla player learns the rhythm by speaking the *bols* before striking the drum. *Dha dhin dhin dha.* The drum is taught from the mouth; the mouth is the source.

> The bansuri is a tube with finger-holes that change the effective length of a resonating air column. The human vocal tract is a tube with continuously movable surfaces — tongue, lips, soft palate — that change the effective length and shape of a resonating air column at every moment of speech. Same physics. Vastly more degrees of freedom.

> The sarangi is often called the closest constructed instrument to the human voice. A bowed string with continuous pitch variation, three drone strings beneath it for sympathetic resonance — exactly the apparatus the human voice provides: vocal cords as the bowed string, nasal cavity as the sympathetic resonator.

### Cm-axis framing: how to handle it

**The factual status:** No standard published chart maps consonants to specific cm distances from the lips. Standard phonetics instruction identifies places of articulation by anatomical region (bilabial, dental, alveolar, palatal, velar, etc.) on the IPA chart's qualitative front-to-back axis.

**However:** Acoustic phonetics research (Fant 1960, Story 2005, Stevens & Blumstein 1978) routinely models the vocal tract as a tube with cm-based constriction locations. Vocal tract length is well-attested at ~17 cm (adult male; 13–20 cm range across adults). The cm representation is rigorous in research literature but uncommon in pedagogical instruction.

**Our use of cm in this chapter is therefore legitimate but unfamiliar to most readers.** Implementation rule:

- **7A**: Anatomical-region names are primary. The vocal tract's ~17 cm length is established as a fact. cm scale appears in FIGURE 7A.1 (as a scale at the bottom of the diagram) but not as primary labels in prose. The reader notices that the vocal tract has measurable length without being asked to memorize specific cm values for specific consonants.
- **7B**: cm-axis framing is where the snap-to-grid argument lives (FIGURE 7B.1). Sanskrit's five *sthāna* plotted at approximate cm positions; English consonants at their approximate cm positions; Arabic pharyngeals at the back-of-range. cm values are approximate; the relative spacing is the argument.
- Endnote `vocal-tract-cm-modeling` credits Fant (1960), Story (2005), Stevens & Blumstein (1978) for the cm-based vocal-tract modeling tradition.

**Approximate cm positions for English consonants** (for FIGURE 7B.1 design reference):

| Place | English consonants | Approximate cm from lips |
|---|---|---|
| Bilabial | /p, b, m/ | ~0 |
| Labiodental | /f, v/ | ~1 |
| Dental (interdental) | /θ, ð/ ("th") | ~2 |
| Alveolar | /t, d, n, s, z, l, r/ | ~4–5 |
| Post-alveolar | /ʃ, ʒ, tʃ, dʒ/ | ~5–6 |
| Palatal | /j/ | ~9–10 |
| Velar | /k, g, ŋ/ | ~12–13 |
| Uvular | French /ʁ/ | ~13–14 |
| Pharyngeal | Arabic /ʕ, ħ/ | ~15–16 |
| Glottal | /h, ʔ/ | ~17 |

### To-Do During Drafting: Language-Hotzones Visualization

**Proposed FIGURE 7A.3** — a visualization showing where 3–4 language groups concentrate their consonant inventories along the vocal tract. Goal: make *every language is a selection* visible at §7A.5 rather than just asserted. Patterns emerge from the visual comparison.

**Design decisions (locked):**
- **Language groups exclude Indic.** Sanskrit/Hindi inventory is 7B's reveal — must not appear in 7A.
- **cm-axis** (not qualitative IPA front-to-back). Consistent with FIGURE 7B.1's cm framing and the acoustic-phonetics modeling tradition.
- **Vowels included** alongside consonants. Both kinds of sounds shown, ideally with visual distinction (different markers or colors).
- **3–4 language groups** to keep the visualization legible.

**Design decisions (open, to settle during drafting):**
- **Granularity**: every consonant as a dot, or aggregated as density (heatmap-style)? Lean: try dots first, see if it reads; switch to density if dots are too cluttered.
- **Which 3–4 language groups?** Candidates: English (Germanic — heavy alveolar cluster), Arabic (Semitic — extends back to pharyngeal), Mandarin (East Asian — retroflexes, palatals, light on labials), Hawaiian (Polynesian — sparse minimal inventory), Spanish (Romance — dense alveolar), click languages (Khoisan/Bantu — adds click-region). Pick 3–4 that maximize visible diversity without overloading the chart.
- **Y-axis encoding**: if dots are used, do consonants stack vertically by manner (stop / fricative / etc.) or just sit at their cm position?

**Where in the chapter:**
- Visualization lands at §7A.5 (*The Instrument's Range*) — the section where the *every language is a selection* observation is made
- May benefit §7A.3 (*How Consonants Are Made*) and §7A.4 (*How Vowels Are Made*) by foreshadowing the comparison

**To-Do marker for chapter prose:**
- §7A.5 should include `[TODO: FIGURE 7A.3 — language-hotzones visualization. Design pending. See notes file for decisions and open questions.]`

### The Pre-Pāṇinian Classification Framework

The pre-split notes mentioned *Prātiśākhya* and *Śikṣā* as the engineering tradition but did not document the **actual classification system** those texts use. This section corrects that gap. Some of this framework belongs in 7A Part 2 (descriptive); the full framework is what 7B's "Pāṇini was second" polemic refers to.

**Source texts:**
- Five *Prātiśākhya* texts, one per Veda:
  - *Ṛk-Prātiśākhya* (Rigveda)
  - *Taittirīya-Prātiśākhya* (Krishna Yajurveda)
  - *Vājasaneyī-Prātiśākhya* (Shukla Yajurveda)
  - *Atharva-Prātiśākhya*
  - *Sāmaveda-Prātiśākhya* — sometimes claimed earliest (Staal's attribution for the 5×5 *varga* organization)
- *Śikṣā* texts of the *Vedāṅga*: *Pāṇinīya-Śikṣā*, *Yājñavalkya-Śikṣā*, *Āpiśali-Śikṣā*, and others
- **Standard scholarly reference**: W.S. Allen, *Phonetics in Ancient India* (Oxford, 1953) — foundational English-language treatment

**The classification axes (canonical, pre-Pāṇinian):**

| Sanskrit term | What it classifies | Sub-categories |
|---|---|---|
| ***Sthāna*** स्थान | Place of articulation (passive articulator) | *kaṇṭhya*, *tālavya*, *mūrdhanya*, *dantya*, *oṣṭhya* — the five we've been using |
| ***Karaṇa*** करण | Active articulator | The active part that makes contact — typically the tongue (apex, blade, dorsum, root) or the lower lip |
| ***Prayatna*** प्रयत्न | Effort / manner of articulation | Splits into two sub-types ↓ |
| &nbsp;&nbsp;***Ābhyantara prayatna*** आभ्यन्तर प्रयत्न | Internal effort (type of constriction) | *Spṛṣṭa* (full contact = stop); *īṣat-spṛṣṭa* (light contact = approximant); *īṣat-saṃvṛta* (light closure = fricative); *vivṛta* (open = vowel) |
| &nbsp;&nbsp;***Bāhya prayatna*** बाह्य प्रयत्न | External effort (everything else) | Voicing, aspiration, glottal state, nasal coupling |
| ***Anupradāna*** अनुप्रदान | Phonation (glottal state) | *Śvāsa* श्वास (breath / voiceless) and *Nāda* नाद (resonance / voiced); *vivṛta* (open glottis) and *saṃvṛta* (closed glottis) |
| ***Aspṛṣṭa*** अस्पृष्ट | Non-contact category | The vowels — no closure between active and passive articulators |

**The 5×5 *varga* grid (per *Sāmaveda-Prātiśākhya*, earliest attribution):**

The *Prātiśākhya* tradition organizes the 25 *sparśa* consonants into a 5×5 matrix. Rows are *sthāna*; columns are *bāhya prayatna* combinations (voicing × aspiration × nasality). The matrix preserves systematic relationships horizontally AND vertically.

**Frits Staal's classical observation** — relevant for 7B's polemic:

> *Like Mendelejev's Periodic system of elements, the* varga *system was the result of centuries of analysis. In the course of that development, the basic concepts of phonology were discovered and defined.*

**How the chapter handles Staal's claim** — endorse-comparison / reject-history mode:

Staal's claim has two parts. **Part 1**: the structural comparison between the *varga* system and Mendeleev's periodic table — both place units at unique coordinates determined by their constituent components. **Part 2**: the historical claim that the *varga* system *was the result of centuries of analysis* and that *the basic concepts of phonology were discovered and defined* in the course of that development.

The chapter **endorses Part 1** and **rejects Part 2**.

- Part 1 (the structural comparison) justifies presenting the 5×5 grid through multiple complementary visualizations in §7B.7, including a periodic-table-styled rendering (FIGURE 7B.3). The structural parallel between the *varga* grid and the periodic table is genuine — both systems decompose their units into constituent parameters and place each unit at a unique coordinate.
- Part 2 (the constructed-over-time framing) is rejected outright. The framework was not built through centuries of analysis. It was already part of Sanskrit's architecture. The *Prātiśākhya* tradition preserves and transmits — it does not construct. *The Prātiśākhya tradition did not invent this framework. It carried forward what was already part of Sanskrit's architecture. The texts preserve and transmit; they do not construct.*

This is the chapter's signature move regarding Staal — agree on the structure-of-the-system, disagree on the history-of-the-system. The polemic lands at §7B.5 (Engineering Precedes Pāṇini); the visualization payoff lands at §7B.7 (Reading the Varṇamālā).

**The 5×5 grid visualization plan** (developed in §7B.7):

The grid is presented through multiple complementary views in 7B itself — control panel, periodic-table style, matrix table, and possibly vocal-tract overlay. Each view makes a different aspect of the engineering visible; the reader sees the same data through several visual idioms; the structure becomes inescapable. Full design in §7B.7 of these notes.

**No conflict with Ch9 *dhātus* reservation:** Ch9 uses the periodic-table-of-elements metaphor for *dhātus* (verbal roots — units of meaning). Ch7B uses the periodic-table-style visualization for the *varga* grid (units of sound, anatomically decomposed). Two distinct deployments at different linguistic scales — sound and meaning. The metaphors complement rather than conflict. Ch9 takes one row of the Ch7B grid (the retroflex *varga*) and develops it; Ch9 does not re-present the full grid.

**Categories beyond the *sparśa* 5×5:**

| Category | Sanskrit | What it is | Sounds |
|---|---|---|---|
| *Antaḥstha* (semivowels / approximants) | अन्तःस्थ | *Īṣat-spṛṣṭa* (light contact) at a *sthāna* | य, र, ल, व |
| *Ūṣman* (fricatives / sibilants — "hot-breath") | ऊष्मन् | *Īṣat-saṃvṛta* (light closure) at a *sthāna* | श, ष, स, ह |

**Vocabulary distribution between 7A and 7B:**

| Term | 7A introduces? | 7B uses? | Notes |
|---|---|---|---|
| *Sthāna* | Yes (§7A.7) | Yes — recap and deploy | Five anatomical contact-stations |
| *Karaṇa* | Yes (§7A.7, light) | Yes — recap | Active articulator (tongue, lips) |
| *Prayatna* | Yes (§7A.9) | Yes — deploy as engineering axis | Effort / manner |
| *Ābhyantara prayatna* | Yes (§7A.9, brief) | Yes — light recap | Type of constriction |
| *Bāhya prayatna* | Yes (§7A.9, brief) | Yes — connects to operating modes | Voicing / aspiration / glottal state |
| *Anupradāna* | Mention only (§7A.7) | Yes — deeper treatment | Phonation |
| *Śvāsa / Nāda* | Mention only | Yes — connects to *aghoṣa* / *ghoṣa* | Breath / resonance |
| *Vivṛta / Saṃvṛta* | Optional in 7A | Yes — glottal state framing | Open / closed glottis |
| *Spṛṣṭa* | Yes (§7A.8) | Yes — recap and use | Full contact (= *sparśa*) |
| *Aspṛṣṭa* | Yes (§7A.8) | Yes — recap | Non-contact (= *swara*) |
| *Īṣat-spṛṣṭa* | Mention in §7A.8 | Yes — *antaḥstha* explanation | Light contact (= *antaḥstha*) |
| *Īṣat-saṃvṛta* | Mention in §7A.8 | Yes — *ūṣman* explanation | Light closure (= *ūṣman*) |

This is what 7A Part 2 will document descriptively. 7B's Pāṇini-was-second polemic in §7B.5 deploys this full framework as the engineering Pāṇini inherited; §7B.7 presents the 5×5 grid through multiple complementary visualizations.

### Cross-language examples (Part 1)

**Languages to thread through 7A.3 and 7A.4** (4–6 total, not exhaustive):

| Language | Use it to illustrate |
|---|---|
| **English** | Default. Familiar starting examples. *th* as interdental fricative, alveolar stop region, etc. |
| **Arabic** | Pharyngeal consonants ع/ح as back-of-the-mouth extreme — sounds the human apparatus can produce far behind where English uses it |
| **Mandarin** | Retroflex affricates — a different selection at a similar tongue-position |
| **French** | Uvular *r*; nasal vowels — extends both the consonant-place range and the vowel-modification range |
| **Hawaiian** | Minimal consonant and vowel inventory — shows how few sounds a language can use and still function |
| **A click language** (Zulu / Xhosa / !Xóõ mention) | The extreme of consonantal possibility — sounds produced by ingressive airflow against the velar/palatal/dental regions |

**Languages NOT to use in 7A:**
- Sanskrit (the inventory is 7B's reveal)
- Hindi (same — would reveal *varṇamālā*-adjacent inventory)
- Tamil (will appear in 7B re: *alpaprāṇa*-only subset)

### Section structure

#### Part 1 — The Instrument

**§7A.1 — The Speaking Instrument**
- Opening: the human mouth as universal instrument of voice across all languages
- Quick illustrative tour: clicks, gutturals, trills, nasals, fricatives — the range
- Brief invocation of the Indian classical position: the voice is the *original instrument*; constructed instruments descend from it (cite *Nāṭyaśāstra* attribution in endnote)
- The chapter's plan (Part 1 anatomy + Part 2 Sanskrit description)
- Target: ~350 words

**§7A.2 — The Anatomy**
- Vocal tract as ~17 cm tube (adult male; smaller for adult female; smaller still for child)
- Active and passive articulators
- Lungs as breath-source (compare to bellows of a wind instrument; lungs as the *suṣira*-instruments' shared mechanism)
- Larynx and vocal cords as oscillator (compare to sarangi's bowed string, sitar's plucked string)
- Oral cavity as resonant tube (compare to bansuri bore)
- Nasal cavity as parallel resonator (compare to sarangi's drone strings as sympathetic resonators)
- Tongue with apex, blade, dorsum, root
- Lips, teeth, alveolar ridge, hard palate, soft palate/velum, uvula, pharynx
- **FIGURE 7A.1** placeholder — cross-section of human head, English anatomical labels, ~17 cm midline distance shown
- Target: ~450 words

**§7A.3 — How Consonants Are Made**
- The category of contact: where two anatomical structures meet to interrupt or shape airflow
- Place of articulation in English: bilabial, labiodental, dental, alveolar, post-alveolar, retroflex, palatal, velar, uvular, pharyngeal, glottal — **all eleven**, briefly
- Manner: stop, fricative, affricate, nasal, approximant, trill, tap
- Voicing (vocal cords vibrating during articulation)
- Aspiration (puff of breath on release)
- Cross-language examples threaded throughout: English *th* (interdental), Arabic ع/ح (pharyngeals), Mandarin retroflex affricates, French uvular *r*, click languages
- Brief note: most consonants involve some form of contact — the tabla-like aspect of the voice
- Target: ~500 words

**§7A.4 — How Vowels Are Made**
- Vowels as sustained tones (no closure, continuous airflow, mouth holds a shape, sound emerges and continues)
- Vowel space: tongue height (high / mid / low), advancement (front / central / back), rounding (rounded / unrounded)
- Nasalization: lowering the soft palate to couple the nasal cavity
- Length: short / long
- Cross-language examples: Spanish 5 vowels, Hawaiian 5 vowels, English ~15 vowels, French nasal vowels
- The bansuri-like and sarangi-like aspect of the voice: sustained tone, controlled pitch, sympathetic resonance
- Target: ~300 words

**§7A.5 — The Instrument's Range**
- The human vocal apparatus has many degrees of freedom and can produce a vast range of sounds
- No language uses them all; every language is a selection
- Selections vary widely (English vs Arabic vs Mandarin vs Hawaiian)
- The instrument is one; the languages many; the selections each language makes are characteristic of that language
- **FIGURE 7A.3** placeholder — language-hotzones visualization (3–4 language groups; cm-axis; vowels included; design pending — see Music-tradition framing → To-Do section above for decisions and open questions)
- In-prose to-do marker: `[TODO: FIGURE 7A.3 — language-hotzones visualization]`
- Transition to Part 2: just as English science has developed vocabulary to describe this instrument, so has the Indian tradition — over many generations of attention to the same physical apparatus
- Target: ~250 words

#### Part 2 — The Indian Description

**§7A.6 — The Indian Description**
- Brief pivot: the Indian classical tradition that catalogued instruments also catalogued the original instrument — the voice — and the anatomy that produces it
- Note: many of the same observations English science made about the apparatus, but in a different vocabulary, developed across many generations of attention to recitation, music, and articulation
- **FIGURE 7A.2** placeholder — same vocal-tract cross-section as FIGURE 7A.1, Sanskrit anatomical labels overlaid
- Target: ~200 words

**§7A.7 — The Anatomy in Sanskrit**
- The five *sthāna* — anatomical contact-stations Sanskrit identified:
  - *oṣṭha* ओष्ठ (lip) → *oṣṭhya* ओष्ठ्य (of-the-lips)
  - *danta* दन्त (tooth) → *dantya* दन्त्य (of-the-teeth)
  - *mūrdhan* मूर्धन् (crown of the head) → *mūrdhanya* मूर्धन्य (of-the-crown)
  - *tālu* तालु (palate) → *tālavya* तालव्य (of-the-palate)
  - *kaṇṭha* कण्ठ (throat) → *kaṇṭhya* कण्ठ्य (of-the-throat)
- Each term names the anatomical structure where contact happens; derivational pattern is consistent
- Note: these are the contact-stations Sanskrit chose to name — others exist (the interdental, the pharyngeal) but are not in this naming system
- ***Karaṇa*** करण (active articulator) — the part that *moves* to make contact: the tongue (with named regions — apex, blade, dorsum, root) or the lower lip. Sanskrit distinguishes *sthāna* (where contact happens, on the passive side) from *karaṇa* (what moves to make contact)
- The four anatomical systems (descriptive, not polemic):
  - Tongue/lips for *sthāna* + *karaṇa* (contact-making)
  - Lungs for *prāṇa* प्राण (breath pressure)
  - Vocal cords for *ghoṣa* घोष (vibration / voicing) — also called *anupradāna* अनुप्रदान in the classification framework when describing the glottal state
  - Soft palate for *anunāsika* अनुनासिक (nasal coupling)
- Each Sanskrit term names the anatomy it controls
- Brief mention: the *Prātiśākhya* tradition classifies sounds along multiple dimensions — *sthāna* (place), *karaṇa* (active articulator), *prayatna* (effort, treated in §7A.9), *anupradāna* (phonation: *śvāsa* breath / *nāda* resonance). Sanskrit's classification framework is multi-axis; this reflects centuries of attention to the apparatus
- Target: ~450 words (increased from 400 due to *karaṇa* and multi-axis mention)

**§7A.8 — Categories of Sound**
- Both English and Sanskrit have category-vocabulary for kinds of sounds. Both are introduced here.
- The underlying contact-distinction (the *ābhyantara prayatna* — internal effort — of the *Prātiśākhya* framework):
  - *Spṛṣṭa* स्पृष्ट (touched, full contact) — what makes a stop
  - *Īṣat-spṛṣṭa* (lightly touched) — what makes an approximant / semivowel
  - *Īṣat-saṃvṛta* (lightly closed) — what makes a fricative
  - *Aspṛṣṭa* अस्पृष्ट (untouched, non-contact) — what makes a vowel
- The four category-names that group sounds by this distinction:
  - **Sparśa** स्पर्श (contact, touch) — the category of consonants requiring *spṛṣṭa* (full contact) between two anatomical structures. English: stops, plosives.
  - **Swara** स्वर (sustained tone) — the *aspṛṣṭa* category. Air flows through an open cavity shaped to a specific resonance; sound emerges and sustains. English: vowels.
  - **Antaḥstha** अन्तःस्थ (in-between) — the *īṣat-spṛṣṭa* category. Sounds that share the open-airflow of swaras and the place-of-articulation specificity of *sparśa*. English: semivowels, approximants, glides.
  - **Ūṣman** ऊष्मन् (heat, hot-breath) — the *īṣat-saṃvṛta* category. Fricatives, where the two anatomies don't fully meet but the air is squeezed through a narrow channel, producing characteristic turbulence. English: fricatives, sibilants.
- **No specific consonants or vowels named.** Categories only. The chapter establishes that both English and Sanskrit have well-developed vocabulary for kinds of sounds — and that Sanskrit's category-naming sits on top of a deeper contact-distinction framework that organizes them systematically.
- Brief cross-language note: most languages have *sparśa*-like sounds and *swara*-like sounds; languages differ in how many *antaḥstha* and *ūṣman* sounds they use
- Target: ~450 words (increased from 400 due to *spṛṣṭa* framework)

**§7A.9 — Sthāna and Prayatna**
- The canonical two-axis decomposition: where the sound is shaped (*sthāna*) and how it's energized (*prayatna* प्रयत्न — effort, manner)
- *Sthāna* is the boundary condition — where contact or constriction happens, which determines the effective shape and length of the resonating cavity
- *Prayatna* is everything else — the coupled system of breath pressure (*prāṇa*), vocal cord vibration (*ghoṣa*), and nasal coupling (*anunāsika*) operating before air reaches the point of contact
- The *Prātiśākhya* tradition further subdivides *prayatna* into two:
  - ***Ābhyantara prayatna*** आभ्यन्तर प्रयत्न (internal effort) — the type of constriction at the place: *spṛṣṭa* (full contact, stops), *īṣat-spṛṣṭa* (light contact, approximants), *īṣat-saṃvṛta* (light closure, fricatives), *vivṛta* (open, vowels). This is what determines the manner of articulation.
  - ***Bāhya prayatna*** बाह्य प्रयत्न (external effort) — everything else applied on top of the constriction: voicing (*anupradāna*: *śvāsa* breath vs *nāda* resonance), aspiration (*alpaprāṇa* / *mahāprāṇa*), nasal coupling (*anunāsika*).
- Two axes describe the apparatus's operational space; the *prayatna* axis subdivides into internal (what kind of constriction) and external (what's layered on top)
- Brief observation (not polemic): this descriptive framework arrives at a decomposition that modern phonetics arrives at through different vocabulary — same instrument, multiple well-developed naming systems. The Sanskrit framework is multi-axis and granular; the English framework is also multi-axis (place, manner, voicing) and granular. Two well-developed traditions describing one apparatus.
- **7A close**: A soft transition. Something like: *The instrument has been mapped, in both English and in Sanskrit. The next chapter takes up the specific selection that one tradition committed to — and the script that encodes it.*
- Target: ~400 words (increased from 300 due to *prayatna* subdivision)

### Figures

- **FIGURE 7A.1**: Vocal tract cross-section, English labels. Lips, teeth, alveolar ridge, hard palate, soft palate, uvula, pharynx, larynx, vocal cords, tongue (with apex/blade/dorsum/root visible), lungs, nasal cavity, oral cavity. ~17 cm midline distance from lips to glottis indicated; cm scale at bottom as supplementary reference. The chapter's reference diagram for Part 1.

- **FIGURE 7A.2**: Same vocal-tract cross-section as FIGURE 7A.1 — same anatomical drawing — with Sanskrit labels overlaid. The five *sthāna* positions (*oṣṭhya*, *dantya*, *mūrdhanya*, *tālavya*, *kaṇṭhya*) marked at their cm-distances from lips. Other anatomical components labeled in Sanskrit (lungs as *prāṇa*-source, vocal cords as *ghoṣa*-source, soft palate as *anunāsika*-controller). The visual demonstration that two naming systems describe the same instrument.

- **FIGURE 7A.3** (design pending): Language-hotzones visualization. X-axis = cm distance along the vocal tract (lips at 0, glottis at ~17). 3–4 language groups represented (final selection TBD; Indic excluded — saved for 7B). Vowels and consonants both shown. Granularity decision (dots vs density) TBD during drafting. Patterns expected to emerge: English heavy in alveolar cluster; Arabic extends back through pharyngeal; Mandarin shifts toward retroflex/palatal; Hawaiian sparse minimal inventory. Anchors §7A.5's *every language is a selection* observation visually. **See "To-Do During Drafting" section above for full design state and open questions.**

### Endnote stubs (new for 7A)

- `nadyashastra-four-instrument-taxonomy` — *Nāṭyaśāstra*'s classification of constructed instruments into *tata / suṣira / avanaddha / ghana*; the position that all constructed instruments derive from the voice as primary
- `adi-vadya-voice-as-original-instrument` — the classical Indian position that the human voice is the *ādi-vādya* (original instrument); *gātra-vīṇā* as related term
- `sarangi-closest-to-human-voice` — the standard Indian classical attribution that the sarangi is the constructed instrument closest to the human voice
- `tabla-bols-mouth-to-drum` — the *bol* syllable system in tabla pedagogy; drummers learning rhythm by speaking the syllables before striking the drum; illustrates voice-as-source
- `vocal-tract-cm-modeling` — Fant (1960) *Acoustic Theory of Speech Production*; Story (2005); Stevens & Blumstein (1978); the cm-based vocal-tract modeling tradition in acoustic phonetics research. Justifies the cm-axis representations in FIGURE 7A.1, FIGURE 7A.3, and FIGURE 7B.1
- `allen-1953-phonetics-ancient-india` — W.S. Allen, *Phonetics in Ancient India* (Oxford, 1953) — foundational English-language scholarly treatment of the *Prātiśākhya* phonetic tradition. Cite for the *Prātiśākhya* classification framework
- `karana-active-articulator` — the *karaṇa* concept (active articulator) in *Prātiśākhya* / *Śikṣā* texts; distinguishes the moving articulator from the stationary *sthāna*
- `sprista-isatsprista-isatsamvrta-vivrta-constriction` — the *ābhyantara prayatna* categories for type of constriction (*spṛṣṭa*, *īṣat-spṛṣṭa*, *īṣat-saṃvṛta*, *vivṛta*) in *Prātiśākhya* texts
- `abhyantara-bahya-prayatna` — the *ābhyantara* / *bāhya prayatna* subdivision (internal vs external effort) in *Prātiśākhya* and *Śikṣā* texts
- `svasa-nada-vivrta-samvrta-phonation` — the *anupradāna* framework for phonation (*śvāsa* / *nāda* / *vivṛta* / *saṃvṛta*) in *Prātiśākhya* texts

### Endnote stubs (existing, partially stay in 7A)

- `place-of-articulation-sanskrit-terms` — Stays partially in 7A (the *sthāna* terms documented in *Prātiśākhya* / *Śikṣā* tradition); the Pāṇini-was-second elaboration moves to 7B
- `formants-source-filter-theory` — Possibly compresses or moves; depends on how deep 7A.4 goes into vowel acoustics. Lean: compress or move to 7B.

---

## 7B — *Mapping the Mouth*

### Architectural overview

**Target length:** ~3,000–3,500 words.

**Reused content** (largely from current `as_ch07_draft.md` with light editing for new section boundaries):
- §7B.1 phonics opener (current §7.1)
- §7B.3 snap-to-grid (current §7.4)
- §7B.5 Pāṇini-was-second (current §7.3 mid-section)
- §7B.6 acoustic engineering depth (current §7.5 engineering payoff)
- §7B.7 pipe-organ + *घ* neuro-motor (current §7.5 pipe-organ paragraph)
- §7B.8 *mahāprāṇa* and Hindi flap (current §7.5 late)
- §7B.9 two-instrument framing + swara temporal cuts (current §7.6)
- §7B close synthesis + hammer (current chapter close)

**New writing required** (light):
- §7B.2 *the selection* — connects 7A's *every language is a selection* observation to the specific *varṇamālā* inventory; introduces *varṇa*, *varṇamālā*, *varga*, the 25+14+4+4 counts; lands the crystalline thesis
- Section-boundary transitions throughout

**Vocabulary 7B may assume** (already established in 7A):
- Anatomical English vocabulary
- *Sthāna* (the five contact-stations)
- *Prayatna* and the four anatomies
- *Prāṇa*, *ghoṣa*, *anunāsika*
- *Sparśa*, *swara*, *antaḥstha*, *ūṣman* as category-words
- The instrument-as-music analogies (tabla, sarangi, bansuri)

**Vocabulary 7B introduces fresh:**
- *Varṇa* वर्ण (letter-sound; the load-bearing 7B unit)
- *Varṇamālā* वर्णमाला (garland of *varṇas*)
- *Varga* वर्ग (row, class — the 5×5 organizational structure)
- Specific Devanagari letters
- The inventory counts: 25 *sparśa* + 14 *swara* + 4 *antaḥstha* + 4 *ūṣman* + structural extras
- *Alpaprāṇa* / *mahāprāṇa*; *aghoṣa* / *ghoṣa* as specific contrast pairs
- *Hrasva*, *dīrgha*, *pluta* (temporal cuts on swaras)
- *Anusvara*, *visarga* (structural extras)
- *Sandhi* (rule-governed phonological adjustments at boundaries)

### Section structure

**§7B.1 — Mapping the Mouth** (~450 words)
- Phonics opener — current §7.1 essentially as-is
- *American schoolchildren are taught "phonics"...*
- Archaeological-site reframe
- *Children learning Indian languages don't need phonics*
- The chapter-defining dichotomy: Roman script as inherited archaeological deposit vs. Indic scripts as engineered phonetic specifications
- Transition: this chapter asks why Indic scripts work this way — what one tradition built on top of the apparatus 7A described

**§7B.2 — The Selection** (~600 words, MOSTLY NEW)
- Connect to 7A: the human vocal apparatus has many degrees of freedom; every language is a selection from that range
- The architects of Sanskrit — operating in the *Prātiśākhya* and *Śikṣā* traditions over many generations — chose specific target locations on the map of the mouth 7A laid out
- They could have chosen many; they chose a structured few
- Introduce *varṇa* वर्ण (sound-letter) — the canonical Sanskrit unit
- Introduce *varṇamālā* वर्णमाला (garland of *varṇas*) — the assembled inventory
- Introduce *varga* वर्ग (row, class) — the organizational structure
- The inventory (count): 25 *sparśa* organized in five *vargas* of five each (5 *sthāna* × 5 operating modes); 14 *swara*; 4 *antaḥstha* (य र ल व); 4 *ūṣman* (श ष स ह); plus structural extras (*anusvara*, *visarga*)
- Brief mention of the five *vargas* by their *sthāna* organization (without yet enumerating specific letters in each *varga* — that comes in §7B.3 with the *kavarga* example)
- **The crystalline thesis lands at section close:**
  > **The names of the sound happen to be the sound itself.**
- The Devanagari letter क is not a symbol that refers to a sound /k/. The letter *is* the sound. The script is not a notation system that maps to phonemes — it is the phonological specification rendered visually.

**§7B.3 — Snap to the Grid** (~700 words)
- Current §7.4 essentially as-is
- The apparatus could produce many more positions than the five *sthāna* the architects committed to
- English interdental (~2 cm) excluded — too close to dental (~3 cm)
- English alveolar/post-alveolar region (~4–6 cm) crossed in a single step
- Arabic pharyngeal (~15 cm) outside the grid's range
- The *kavarga* used as worked example here (since 7B.2 introduced *varga*): क ख ग घ ङ as the five operating modes at the *kaṇṭhya sthāna*
- The grid snaps; what the grid leaves out, the mouth can still do
- Sandhi as governed loosening at boundaries (*anusvara* assimilation, vowel sandhi)
- **FIGURE 7B.1** placeholder (currently FIGURE 7.2): linear vocal-tract diagram with English/Arabic exclusions plotted against the five *sthāna* positions

**§7B.4 — The Naming of the Sounds** (~350 words)
- The Sanskrit terminology that names the grid and its sounds
- The *sthāna* names already introduced in 7A (*oṣṭhya*, *dantya*, etc.) — brief recap
- The *varga* naming convention — each *varga* named by its leading consonant (*kavarga* by क, *cavarga* by च, etc.)
- These terms have been operating across many generations of *guru-shishya* transmission

**§7B.5 — The Engineering Precedes Pāṇini** (~800 words)
- Current §7.3 mid-section — the Pāṇini-was-second polemic, essentially as-is, plus the specific pre-Pāṇinian classification framework
- *Prātiśākhya* and *Śikṣā* texts as the engineering tradition that precedes Pāṇini
- **What the *Prātiśākhya* tradition actually classifies** (the engineering that precedes Pāṇini, named concretely — not just "the framework"):
  - *Sthāna* (place of articulation — the five anatomical contact-stations)
  - *Karaṇa* (active articulator — the moving part)
  - *Prayatna* split into *ābhyantara* (internal — type of constriction: *spṛṣṭa*, *īṣat-spṛṣṭa*, *īṣat-saṃvṛta*, *vivṛta*) and *bāhya* (external — voicing, aspiration, glottal state)
  - *Anupradāna* (phonation: *śvāsa* / *nāda*, *vivṛta* / *saṃvṛta*)
  - The 5×5 *varga* matrix (rows = *sthāna*; columns = *bāhya prayatna* combinations) for the 25 *sparśa* consonants
  - *Antaḥstha* and *ūṣman* categories for the liminal set
- **The architecture-not-analysis polemic** (load-bearing move in this section):
  - *The Prātiśākhya tradition did not invent this framework. It carried forward what was already part of Sanskrit's architecture. The texts preserve and transmit; they do not construct.*
  - The framework is part of Sanskrit's architecture, not the residue of a research program. Many generations of *guru-shishya* transmission carried it forward; the framework's depth is the depth of the language it describes — not the depth of an empirical inquiry that produced it.
  - This is the chapter's core stance toward how the *varṇamālā* came to be. The conventional framing of *centuries of analysis converging on the framework* is rejected outright.
- **Deployment of Staal's observation** — endorse-comparison / reject-history mode:
  - Staal's classical observation, drawn from secondary sources (primary source to verify):
    > *Like Mendelejev's Periodic system of elements, the* varga *system was the result of centuries of analysis. In the course of that development, the basic concepts of phonology were discovered and defined.*
  - **Endorse the structural comparison.** The *varga* grid and the periodic table share a logic — units placed at unique coordinates of their constituent components. The structural parallel is genuine and justifies the periodic-table-styled visualizations of the grid in §7B.7.
  - **Reject the constructed-over-time framing.** The framework was not built up through centuries of analysis. It was already part of Sanskrit's architecture. The *Prātiśākhya* texts preserve and transmit; they do not construct.
  - The chapter prose explicitly draws this distinction — agrees with Staal on Thing 1, disagrees with Staal on Thing 2.
- *The engineering precedes Pāṇini.*
- *Pāṇini was second.* (short-line pivot)
- The *Aṣṭādhyāyī* operates **all** of this terminology as already-established vocabulary; Pāṇini does not introduce these terms, he uses them. Pāṇini inherits *sthāna*, *karaṇa*, *prayatna*, *anupradāna*, *spṛṣṭa*, *vivṛta*, *saṃvṛta*, *aghoṣa*, *ghoṣa*, *alpaprāṇa*, *mahāprāṇa*, the 5×5 *varga* matrix, and the *antaḥstha* / *ūṣman* categories — all of it already there, all of it operating
- *Śiva Sūtras* reorder the *varṇamālā*'s sound-set for the analytical rule-system — reordering presupposes a prior ordering
- **Forward-pointer**: The 5×5 *varga* grid as visualization — through multiple complementary views including the periodic-table-styled rendering — is taken up in §7B.7 (Reading the Varṇamālā), where the grid's operational structure is shown
- Western philology's pedestal under Pāṇini; the older engineering tagged "pre-Pāṇinian" and stepped behind
- *Pāṇini was great. The engineering Pāṇini codified was greater.*
- The European-philology absorption chronology — Jones 1786, Bopp 1816, Böhtlingk 1839–40, Whitney 1879, IPA 1886/1888
- The English/Latin terms (*labial*, *dental*, etc.) translate the engineered framework Sanskrit grammar had been operating
- Section hammer: *The terminology was Sanskrit's. The systematization was Sanskrit's. Europeans did not invent, they translated.*

**§7B.6 — The Acoustic Engineering** (~650 words)
- *Stop thinking like a linguist. Start thinking like an acoustic engineer.*
- The Western model treats the mouth as a black box; the Indic model deconstructs it as a biological wind instrument
- The four anatomies framework — now deployed as engineering payoff (not just description, which is 7A's mode)
- Eight-anatomies fanout: five for *sthāna*, plus lungs, vocal cords, soft palate
- The Western abstract vocabulary vs Sanskrit anatomical: *voicing* does not point to the vocal cords; *aspiration* does not point to the lungs; *place* does not point to the tongue
- Physics: spatial well-separation produces acoustic well-separation; the five *sthāna* positions sample the formant space at well-separated acoustic points
- The grid is acoustically engineered, not just spatially organized

**§7B.7 — Reading the Varṇamālā** (~700 words, increased from 500)
- Current §7.5 pipe-organ + *घ* neuro-motor command paragraph
- *Imagine a grand pipe organ. The Roman alphabet expects the reader to memorize which pedal arbitrarily triggers which pipe. The varṇamālā is the engineering schematic of the organ itself.*
- The *घ* example: reading the coordinate on the matrix issues three commands — *mahāprāṇa* + *ghoṣa* + *kaṇṭhya*
- *The varṇamālā does not store sounds. It stores the parameter strings that the speaking body executes to produce sounds.*
- **The 5×5 grid through multiple complementary views:**
  - The grid is one structure, but its operational logic becomes inescapable when seen through different visual idioms. This section presents the grid through three or four complementary visualizations, each making a different aspect of the engineering visible
  - **View 1 (FIGURE 7B.2): Control panel.** *Sthāna* on Y-axis, *prayatna* on X-axis, each cell carries the Devanagari character. The operational reading — the grid as instrument board.
  - **View 2 (FIGURE 7B.3): Periodic-table style.** Each consonant in its own bordered cell, arranged in the 5×5 grid styled visually like Mendeleev's table. The anatomical parameters that produce each sound shown as encoded labels — possibly via color, position within the cell, or superscript/subscript notation indicating *sthāna* + *prayatna* combination. The systematic-decomposition reading — the grid as structured decomposition of every *sparśa* sound into its anatomical parameters. This visualization endorses Staal's structural comparison while saying nothing about how the grid came to be — it just shows what the grid *is*.
  - **View 3 (FIGURE 7B.4): Matrix table.** Plain rows × columns with cells, the most data-dense rendering. Suitable for reference, possibly placed in an appendix or as a sidebar callout. Provides a clean look-up for any reader who wants to verify what the chapter is describing.
  - **View 4 (possible — FIGURE 7B.5): Vocal-tract overlay.** The 25 *sparśa* consonants positioned on a stylized vocal-tract cross-section at their actual *sthāna* locations, with the five *prayatna* operating modes shown as variants at each location. Connects FIGURE 7B.1's snap-to-grid framing to the grid's full content.
- The reader sees the same grid through multiple idioms; the structure becomes inescapable. Each view reinforces what the others show; the *varṇamālā* as engineered architecture cannot be reduced to any single rendering
- Prose handling: the chapter walks through what each view makes visible. Not exhaustive description — short paragraphs (50–100 words) per view, each saying *here is what this rendering reveals that the others don't*
- **Forward-pointer for the retroflex *varga* specifically**: the third row of the grid (ट ठ ड ढ ण) is isolated and developed in Ch9 — the test of *āryatva* and the codification perimeter (what Pāṇini's *bhāṣāyām* bounded out, e.g., the ळ that *Ṛgveda* uses). This is one row of the grid Ch7B has presented; Ch9 takes that row and develops it.

**§7B.8 — The Subcontinental Substrate** (~400 words)
- *Mahāprāṇa* as Sanskrit-specific engineering elaboration on top of subcontinent-wide *alpaprāṇa* base
- Tamil contrast — *alpaprāṇa* only at the *varga* level; no *mahāprāṇa* doubling
- Hindi flap variants (ड़ ढ़) as positional realizations of ड ढ — same retroflex hardware, briefer contact, the script's *nuqta* as later notational accommodation

**§7B.9 — Two Instruments** (~500 words)
- Two-instrument framing as chapter-level synthesis: *sparśa* vs *swara* as two modes of the same apparatus
- The apparatus 7A mapped as instrument can be played with contact (struck mode) or without (continuous mode)
- *Sparśa* consonants are the struck mode; swaras are the continuous mode; *antaḥstha* is the engineered bridge; *ūṣman* is the squeezed-channel mode
- Swara temporal cuts: *hrasva* (1 *mātrā*), *dīrgha* (2 *mātrā*), *pluta* (3+ *mātrā*); the *mātrā* as engineered temporal unit
- The vowel matrix: five base swaras × temporal cuts + diphthongs
- Forward-pointer to Ch9 (formerly Ch8) — the retroflex *varga* ट ठ ड ढ ण as the third row, the structural midpoint; Ch9 isolates this row as the test of *āryatva*

**§7B close — Roman Inventory, Varṇamālā Anatomy** (~250 words)
- Final synthesis: *The Roman alphabet is an inherited visual inventory. The varṇamālā is an acoustic anatomy.*
- The four diagnostic questions: where is the sound struck, how forcefully is the breath released, are the vocal cords vibrating, is the nasal chamber opened?
- *The Roman alphabet behaves like an alphabet. The varṇamālā behaves like a scientific diagram of the speaking body.*
- Chapter hammer: *Phonics is a workaround. The varṇamālā is the engineering.*

### Figures

- **FIGURE 7B.1**: Linear stretched-out vocal-tract representation from 0 cm (lips) to ~17 cm (glottis). Sanskrit's five grid positions marked. English consonants plotted (interdental *th*, alveolar t/d/n/s/z/l/r, post-alveolar sh/ch/zh). Arabic ع/ح at ~15 cm. Arrows showing snap mechanism. Shows the superset vs the chosen subset.

- **FIGURE 7B.2** (View 1 — Control Panel): *Varṇamālā* as control panel. Y-axis = *sthāna* (top-to-bottom: *kaṇṭhya* → *tālavya* → *mūrdhanya* → *dantya* → *oṣṭhya*). X-axis = *prayatna* (left-to-right: *aghoṣa-alpaprāṇa* → *aghoṣa-mahāprāṇa* → *ghoṣa-alpaprāṇa* → *ghoṣa-mahāprāṇa* → *anunāsika*). Each cell with Devanagari + IAST. Plus middle (vowel matrix) and bottom (liminal set) panels. Reads as operational diagram. **Lands in §7B.7.**

- **FIGURE 7B.3** (View 2 — Periodic-Table Style): The 25 *sparśa* consonants in a 5×5 grid styled visually like Mendeleev's periodic table. Each consonant in its own bordered cell. Anatomical parameters encoded — possibly via cell-color (one color family per *sthāna* row), corner labels (small superscript/subscript indicating *prayatna* components — voicing, aspiration, nasal-coupling), and cell numbering for systematic reference. Visualization endorses Staal's structural comparison while remaining silent on the constructed-over-time framing. **Lands in §7B.7.**

- **FIGURE 7B.4** (View 3 — Matrix Table): Plain rows × columns table — most data-dense rendering. Each row a *sthāna*; each column a *prayatna* operating mode; each cell carries the Devanagari character, IAST transliteration, and the four-anatomy decomposition (*sthāna* + *karaṇa* + *ābhyantara prayatna* + *bāhya prayatna*). Suitable for reference. May land in main text body or as an appendix/sidebar — to be decided during drafting. **Lands in §7B.7 or appendix.**

- **FIGURE 7B.5** (View 4 — Vocal-Tract Overlay, possible): The 25 *sparśa* consonants positioned on a stylized vocal-tract cross-section at their actual *sthāna* locations. The five *prayatna* operating modes shown as variants stacked at each location (or shown in a small inset table at each location). Connects FIGURE 7B.1's snap-to-grid framing to the grid's full content. **Lands in §7B.7. Optional — include only if it adds genuine clarity, not for completeness.**

### Endnote stubs (carry over from current draft)

- `varnamala-grid-geometry` — moves to 7B §7B.2 or §7B.3
- `place-of-articulation-sanskrit-terms` — partially moves; the Pāṇini-was-second sub-content moves to 7B §7B.5
- `jones-1786-third-anniversary-discourse` — moves to 7B §7B.5
- `ipa-1886-founding-1888-chart` — moves to 7B §7B.5
- `history-of-linguistics-sanskrit-influence` — moves to 7B §7B.5
- `sandhi-anusvara-assimilation` — moves to 7B §7B.3
- `vedic-svara-system` — moves to 7B §7B.9
- `hrasva-dirgha-pluta-matra` — moves to 7B §7B.9

### Endnote stubs (new for 7B)

- `pre-panini-pratisakhya-classification` — the full multi-axis *sthāna* / *karaṇa* / *prayatna* / *anupradāna* classification framework as documented in the *Prātiśākhya* texts before Pāṇini. Primary citation: Allen 1953, *Phonetics in Ancient India*. Should also cite a primary-source *Prātiśākhya* reference. Anchors the polemic that Pāṇini inherited this framework rather than constructing it.
- `staal-mendeleev-varga-comparison` — Frits Staal's observation comparing the *varga* system to Mendeleev's periodic table. The chapter **endorses the structural comparison** (units placed at unique coordinates of their constituent components — both systems share this logic) but **rejects the constructed-over-time framing** (Staal's *result of centuries of analysis* claim — the chapter argues the framework was already part of Sanskrit's architecture, not constructed through inquiry over time). Find primary source — likely Staal's *Universals: Studies in Indian Logic and Linguistics* (Chicago, 1988), *Discovering the Vedas* (Penguin, 2008), *The Science of Language* (in *The Blackwell Companion to Hinduism*, 2003), or a journal article (possibly *The Sanskrit of Science*, *Journal of Indian Philosophy*, 1995). Verify the exact wording.
- `architecture-not-analysis-pratisakhya` — the chapter's stance that the *Prātiśākhya* tradition preserves and transmits rather than constructs. The framework's depth is the depth of Sanskrit's architecture, not the residue of centuries of empirical inquiry. Position taken in §7B.5 in opposition to the conventional constructed-over-time framing.

---

## Cross-Chapter Coordination

### Vocabulary handoff (what 7A establishes, what 7B can assume)

| Concept | 7A introduces as | 7B deploys as |
|---|---|---|
| The five anatomical contact-stations | *Sthāna* names (*oṣṭhya*, *dantya*, etc.) — derivational pattern shown | Already-known terminology; brief recap only |
| Two-axis description of apparatus | *Sthāna* / *prayatna* canonical pair | Already-known; used to label FIGURE 7B.2 axes |
| Four anatomical systems | *Sthāna*, *prāṇa*, *ghoṣa*, *anunāsika* — descriptive | Engineering payoff deployment |
| Categories of sound | *Sparśa*, *swara*, *antaḥstha*, *ūṣman* as category-words | Specific inventories revealed; counts named |
| Vowel temporal range | Vowels as sustained tones | *Hrasva*/*dīrgha*/*pluta* engineered cuts |
| The voice as instrument | Indian music-tradition framing (sarangi, bansuri, tabla) | Pipe-organ + control-panel + acoustic-engineer reframe |
| Cross-language diversity | English, Arabic, Mandarin, French, Hawaiian examples | English/Arabic exclusions in snap-to-grid; Tamil contrast for *mahāprāṇa* |

### Figure coordination

- **FIGURE 7A.1** and **FIGURE 7A.2** are the same anatomical cross-section with different label-overlays. Visual demonstration that two naming systems describe one apparatus.
- **FIGURE 7A.3** (design pending) — language-hotzones visualization at §7A.5
- **FIGURE 7B.1** is the linear-stretched version of the vocal tract — derived from but visually distinct from FIGURE 7A.1. Shows the superset/subset relationship that's load-bearing for snap-to-grid.
- **FIGURES 7B.2 through 7B.5** are the 5×5 *varga* grid presented through multiple complementary visualizations — control panel (7B.2), periodic-table style (7B.3), matrix table (7B.4), and optional vocal-tract overlay (7B.5). The reader sees the same grid through several visual idioms; the structure becomes inescapable.
- **Cross-chapter: the 5×5 grid lives in 7B.** The full grid (all 25 *sparśa* consonants, all 5 *sthāna* rows × 5 *prayatna* operating modes) is presented in 7B through the multiple-view treatment. Ch9 takes one row of that grid — the retroflex *varga* (ट ठ ड ढ ण) — and isolates it as the test of *āryatva*. Ch9 does not re-present the full grid; it takes the row Ch7B has shown and develops it.

### Transition mechanics

- **7A close**: Soft transition. *The instrument has been mapped, in both English and in Sanskrit. The next chapter takes up the specific selection that one tradition committed to — and the script that encodes it.*
- **7B open**: Phonics opener (current §7.1). The transition is not narratively bridged; 7B starts cold with a polemic move. The reader who absorbed 7A has the vocabulary; 7B turns the lens.

This is by design — 7A is descriptive, 7B is argumentative, and a soft narrative bridge between them would muddy the voice register shift.

---

## Style / Voice Reminders for Drafting

(Full treatments live in `ptStyleGuide.md` and `ptVoiceCalibration.md`. Brief reminders here for drafting convenience.)

### 7A specific (descriptive register)

- **No hammers.** Sections close with descriptive observations or transitions, not verdict statements.
- **No scare quotes for establishment terms.** *Linguistics*, *phonetics*, *phonology* are used neutrally.
- **No "engineered" / "engineering" language.** Save for 7B. In 7A, use *the apparatus*, *the instrument*, *the anatomy*, *the structure*.
- **No Pāṇini reference.** Pāṇini doesn't appear in 7A; his work belongs in 7B's polemic.
- **No *varṇamālā* reference.** Even the term doesn't appear.
- **No specific consonants or vowels named** from any tradition's inventory. Sanskrit category-terms only; English category-terms only.
- **The four-anatomies framework is descriptive in 7A, polemic in 7B.** Same content, different register.
- **Cross-language examples treated equally.** Sanskrit is one well-developed naming system among many; English science is another. The reader notices the depth of Sanskrit's grounding without being told.

### 7B specific (full polemic register)

- All current chapter polemic principles apply: hammers, scare quotes, dichotomy-reframe moves, named-actors establishment-naming, internal-frame anchors, the four diagnostic questions structure.
- The crystalline thesis (*The names of the sound happen to be the sound itself*) is load-bearing — placement at §7B.2 close.
- The chapter hammer (*Phonics is a workaround. The varṇamālā is the engineering.*) closes the chapter as §7.1-style callback.

### Sanskrit handling (both chapters)

- Devanagari + Roman + gloss on first introduction; italicized first use; plain thereafter
- For category-words in 7A (*sparśa*, *swara*, *antaḥstha*, *ūṣman*): introduce as kinds-of-sounds, with English gloss
- For specific letters in 7B (क, ख, etc.): introduce in §7B.3 worked example onward
- For *Nāṭyaśāstra* taxonomy terms (*tata*, *suṣira*, etc.): endnote only, not in prose

### Chronology rule (both chapters)

- No specific dating for Indic figures/texts
- External dates fine where they're the argument (Jones 1786, Bopp 1816, IPA 1886/1888)
- Internal-frame ordering acceptable (*before Pāṇini*, *across many generations of guru-shishya transmission*)

---

## Drafting Sequence (locked plan)

1. **Step 1 (done)**: Archive existing notes file as `as_ch07_notes_pre_split.md`
2. **Step 2 (done)**: Build new restructured `as_ch07_notes.md` (this file)
3. **Step 3**: User review and corrections to notes file
4. **Step 4**: Draft 7A end-to-end against the notes (~2,500–3,000 words)
5. **Step 5**: User review of 7A
6. **Step 6**: Revise 7A per feedback
7. **Step 7**: Assemble 7B from existing content into new structure (~3,000–3,500 words)
8. **Step 8**: User review of 7B
9. **Step 9**: Revise 7B per feedback
10. **Step 10**: Prepare handoff file in case session ends — durable record of decisions and progress
11. **Step 11**: Final integration — single `as_ch07_draft.md` with both chapter blocks
12. **Future**: When ready to split, mechanical extraction by chapter heading
