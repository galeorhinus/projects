# Vyañjana Timing — Concept Development

Captured from the initial response to *"in actual speech — how long, in milliseconds, does a consonant stop last?"* The full analytical sweep is preserved here: modern phonetics measurements alongside the Indic *Śikṣā* specification, with the convergence point named. Held for development into appendix material as more data lands.

**Companion endnote:** `vyanjana-duration-shiksha` (in `as_endnotes.md`) — the dossier-grade version with citations and the cross-reference network. This document carries the longer-form prose development for possible appendix deployment.

---

## The question

How long, in milliseconds, does a consonant stop (*vyañjana*) actually last in human speech?

Modern phonetics has measured this with spectrogram-based precision. The Indic *Śikṣā* tradition specified it with explicit *mātrā* fractions. The two answers converge remarkably well.

---

## Modern phonetics measurements

A stop consonant (Sanskrit *sparśa*: क ख ग घ ङ etc.) has three measurable components, each contributing duration:

| Component | What it is | Typical duration |
|---|---|---|
| **Closure** | The silent / quasi-silent hold while articulators are sealed | **60–100 ms** |
| **Release / burst** | Brief noise burst when closure opens | **5–20 ms** |
| **VOT** (Voice Onset Time) | The interval from release to onset of vocal-fold vibration for the next vowel | varies by category (see below) |

### VOT by stop category

The Sanskrit *aghoṣa* / *ghoṣa* × *alpaprāṇa* / *mahāprāṇa* cross-classification maps to four distinct VOT regimes:

- **Voiceless unaspirated** (Sanskrit क *ka*, त *ta*, प *pa* — ***aghoṣa-alpaprāṇa***): VOT ≈ **0–30 ms**
- **Voiceless aspirated** (ख *kha*, थ *tha*, फ *pha* — ***aghoṣa-mahāprāṇa***): VOT ≈ **50–90 ms** (the aspiration itself adds 40–70 ms)
- **Voiced unaspirated** (ग *ga*, द *da*, ब *ba* — ***ghoṣa-alpaprāṇa***): VOT ≈ **−100 to 0 ms** (prevoicing — voicing begins *during* closure)
- **Voiced aspirated** (घ *gha*, ध *dha*, भ *bha* — ***ghoṣa-mahāprāṇa***): closure voiced ≈ 60–80 ms; breathy release adds ≈ **50–100 ms**. This is the *vargānta-caturtha* category that is typologically rare outside Indic languages. Cross-linguistically, voiced-aspirated stops are absent or marginal in most language families. The substrate-borrowing claim Chapter 16 attacks has to contend with the fact that the proposed migrant populations would have had to acquire a phonetic category their own language lineages did not contain, then build an entire phonetic specification around it.

### Total stop duration

In conversational speech, stop durations (closure + release + aspiration if present) range from about **70 ms** (voiceless unaspirated *ka*) to about **180 ms** (voiced aspirated *gha*).

In careful speech / recitation, all durations stretch by roughly 50–100%.

**Anchor references:**

- Lisker, L., and Abramson, A. S., "A cross-language study of voicing in initial stops: Acoustical measurements," *Word* 20 (1964), pp. 384–422 — the foundational VOT study, ~600 stops measured across 11 languages including Hindi / Sanskrit-aspirate categories.
- Klatt, D. H., "Linguistic uses of segmental duration in English: Acoustic and perceptual evidence," *Journal of the Acoustical Society of America* 59 (1976), pp. 1208–1221 — the canonical durational study.

---

## The Indic *Śikṣā* answer — same number, thousands of years earlier

The *Pāṇinīya Śikṣā* specifies durations in *mātrās* (मात्राः):

| Sound class | Mātrā | Pāṇinīya gloss |
|---|---|---|
| **Hrasva** (short vowel) ह्रस्व | **1 mātrā** | *ह्रस्वो दीर्घः प्लुतो ज्ञेयः* |
| **Dīrgha** (long vowel) दीर्घ | **2 mātrās** | (same śloka) |
| **Pluta** (prolated vowel) प्लुत | **3 mātrās** | (same śloka) |
| **Vyañjana** (consonant) व्यञ्जन | **½ mātrā** | ***अर्धमात्रा तु व्यञ्जनम्*** |
| **Anusvāra / visarga** | **½ mātrā** | (*Śikṣā* continues) |

So the *Śikṣā* answer to *"how long does a consonant last?"* is: **a consonant is half a mātrā.**

### What is one *mātrā* in milliseconds?

The *Pāṇinīya Śikṣā* defines one *mātrā* as ***kālo varṇasya prayoge*** — *the time taken to pronounce one short varṇa*.

In modern measurement of disciplined Vedic recitation (Sāmavedic / Ṛgvedic chanting, multiple studies on lineage-trained reciters):

- **1 mātrā ≈ 150–200 ms** (short-vowel duration in recitation)
- **½ mātrā ≈ 75–100 ms** (vyañjana duration per *Śikṣā*)

This is exactly the **60–100 ms range modern phonetics measures for stop closure**.

Conversational speech compresses these durations; recitation pace stretches them. The ratios — 1 (short vowel) : 2 (long vowel) : ½ (consonant) — remain stable across pace variation. This is the *Śikṣā*'s engineering signature: the absolute durations vary with pace, but the *ratios* are fixed.

---

## The convergence

The *Śikṣā* specification and the millisecond measurement land on the same number through completely different methods:

- The *Śikṣā* specified by ear, by lineage-internal training, by an explicit fractional notation embedded in metrical practice — thousands of years ago.
- Modern phonetics measured the same number by acoustic instrument in the twentieth century.

The correspondence is not approximate. It is exact within the natural variance of careful speech.

---

## What this tells us about the engineering

The *Śikṣā* tradition did not estimate or guess at consonant durations. It *specified* them. Half a *mātrā* is a precise fraction, not a folk-impression. The architecture encoded the timing of every sound class:

- Short vowel: 1 unit
- Long vowel: 2 units
- Prolated vowel: 3 units
- Consonant: ½ unit
- Anusvāra / visarga: ½ unit

This timing specification is what makes the metrical system work. *Gāyatrī* (24 syllables), *Anuṣṭubh* (32), *Triṣṭubh* (44), *Jagatī* (48) — these are not just syllable counts. They are *temporal patterns* governed by *mātrā*-counting, where each consonant contributes ½ *mātrā* and each vowel its time-class to the line's total temporal pattern. The recitation's timing has to hit specifications precisely or the metrical fingerprint breaks.

The timing-precision is the architecture's anti-drift mechanism at the temporal axis — parallel to the *sandhi* / *Prātiśākhya* / *padapāṭha* mechanisms at other axes. The *guru-shishya paramparā* transmits this timing-precision across generations; multiple modern measurements of Vedic recitation across distinct *śākhā* lineages confirm reproducible 1:2:3 vowel-duration ratios and ½-*mātrā* consonants.

---

## Reading the category correctly

The orthodoxy reads the *Śikṣā* tradition as *"phonetic prescriptions"* or *"pre-scientific approximations to modern phonetic measurement."* That is the wrong category.

The *Śikṣā* texts are the **timing-engineering specification** for the calibration matrix — the audio-engineering manual for a system designed to be reproduced without drift across generations.

A modern audio engineer specifying *"70 ms for a stop closure, 150 ms for a short vowel, half that for a consonant"* is doing what the *Śikṣā* tradition already did, with the same numbers, with the same precision, through ear-trained calibration rather than instrument-mediated measurement.

That is engineering. The *Śikṣā* writers knew it. The orthodoxy that calls their work *"phonetic theory"* or *"pre-scientific approximation"* is reading the wrong category.

---

## Consonant clusters — the two-layer rule

A natural extension question: when a *dhātu* has a consonant cluster like CC in क्षि (*kṣi*), श्रु (*śru*), or ज्वल् (*jval*), how is the cluster's duration handled? Together half a *mātrā*, or do they sum to a full *mātrā*?

**Direct answer:** At the *varṇa* level, CC = 1 *mātrā* (½ + ½). Each consonant in the cluster keeps its own ½-*mātrā* specification. The *Śikṣā* tradition does not compress clusters.

But Sanskrit's timing system operates at two levels, and the second level introduces a wrinkle worth naming.

### Level 1 — Per-*varṇa* duration (*Śikṣā* specification)

Each *varṇa* has its fixed *mātrā* cost regardless of position:

- Short vowel: 1 *mātrā*
- Long vowel: 2 *mātrās*
- *Vyañjana*: ½ *mātrā* (uniformly, regardless of cluster position)
- Anusvāra / visarga: ½ *mātrā*

In **CCV** like श्रु (*śru*): each C = ½, V = 1, total cluster CC = 1 *mātrā*, total *dhātu* = 2 *mātrās* of articulation time.

The Sanskrit term for a cluster is ***saṃyoga*** (संयोग, *joining*) or ***saṃyukta*** (संयुक्त, *joined*). The grammar treats the cluster as bonded but composed of distinct *varṇas*, each retaining its own *mātrā* cost. There is no cluster-compression rule.

### Level 2 — Syllable weight (*Chandas* / scansion rule)

For metrical scansion, each syllable is classified as ***laghu*** (लघु, light, 1-*mātrā* weight) or ***guru*** (गुरु, heavy, 2-*mātrā* weight). The rule:

A syllable is ***guru*** if it contains —

- A long vowel (*dīrgha*), or
- A short vowel followed by ***anusvāra*** / ***visarga***, or
- A short vowel followed by ***two or more consonants*** (the *saṃyoga* case), or
- The final syllable of a *pāda* (in some traditions).

Otherwise ***laghu***.

The CC-after-short-vowel rule is where the cluster interacts with metrical weight. A short vowel followed by CC makes the preceding syllable *guru*, even though the vowel itself is still phonetically short. The cluster does not lengthen the vowel; it lengthens the syllable's *metrical count*.

### How the two levels cohere

The metrical *guru*-weighting is not arbitrary. It tracks the actual temporal occupation: a short vowel (1 *mātrā*) followed by a cluster CC (1 *mātrā*) takes about 2 *mātrās* of total time, which is exactly what the *guru* weight assigns. The cluster's articulation time fills the rhythmic space that an unfollowed short vowel would leave empty.

*Śikṣā* (per-*varṇa* time) and *Chandas* (per-syllable metrical weight) are not two independent traditions that happen to be compatible. They are two faces of one engineering specification, audited against each other through the *mātrā* unit. The per-*varṇa* time is the input; the per-syllable metrical weight is the integrated output.

### Worked examples

| Configuration | Per-*varṇa* time | Syllable metrical weight |
|---|---|---|
| **CV_short** (CV, *laghu*) | ½ + 1 = 1.5 *mātrās* | 1 (*laghu*) |
| **CV_long** (CV, *guru* by long vowel) | ½ + 2 = 2.5 *mātrās* | 2 (*guru*) |
| **CV_short + CV_short** (CVCV, two *laghu*) | ½ + 1 + ½ + 1 = 3 *mātrās* | 1 + 1 |
| **CV_short + CCV_short** (CVCCV, *guru* + *laghu*) | ½ + 1 + ½ + ½ + 1 = 3.5 *mātrās* | **2** + 1 |
| **CCV_short** (CCV, opening cluster) | ½ + ½ + 1 = 2 *mātrās* | 1 (*laghu*) — cluster precedes vowel, no prior syllable to lengthen |

Note the last row: a CCV *dhātu* like श्रु opens with a cluster. The cluster takes 1 *mātrā* of articulation time, but it does not lengthen any preceding syllable (there isn't one). The opening syllable is *laghu*.

### Implication for the *dhātu* hexagon visualization

The cluster needs no special handling. क्षि (*kṣi*) renders as C-hex + C-hex + V1-hex — two ½-*mātrā* hexagons followed by a 1-*mātrā* hexagon. The two consonants sit adjacent in the zigzag, with edge-matching as usual.

If the visualization later needs to layer *guru* / *laghu* metrical weight on top of the per-*varṇa* hexagons, that becomes a Level-2 overlay — a frame around each syllable's hexagon cluster encoding its weight (1-*mātrā* frame = *laghu*, 2-*mātrā* frame = *guru*). The Level-1 hexagons stay unchanged. The two levels stack cleanly because the underlying architecture stacks cleanly.

---

## Snap to grid — in time as well as space

The *varṇamālā* chapter (Ch 8 §8.4) develops a canonical analogy for the spatial axis of the engineered phonetic grid: ***snap-to-grid***. Like Illustrator, Figma, or Blender — when a designer's cursor nears a grid intersection, it jumps to the grid point. The grid is the destination; the cursor is what approximates. The function exists because precision matters and the human hand cannot place a point exactly without help.

The *varṇamālā* defines five articulator places (*kaṇṭhya* / *tālavya* / *mūrdhanya* / *dantya* / *oṣṭhya*) — discrete grid points across the mouth. Continuous articulatory space (the alveolar region between dental and retroflex; the labio-dental region between labial and dental; the glottal region) is *not* sampled. The engineering snaps to five places, spaced deliberately ~2 cm apart for acoustic distinguishability (see endnotes `varnamala-grid-geometry` and `tamil-alveolar-place-station`, and the Ch 9 superset development).

**The same principle operates on the temporal axis.**

The *Śikṣā* defines four duration values: ½, 1, 2, 3 *mātrā*. Continuous time is *not* sampled. Speech is snapped to these four grid points. A consonant snaps to ½ *mātrā*. A short vowel snaps to 1. A long vowel snaps to 2. A *pluta* vowel snaps to 3. Nothing in between is specified.

Articulation approximates the grid. Modern measurement of disciplined recitation finds slight shortening due to coarticulation — observed CC duration runs about 0.8–0.9 *mātrā* rather than the specified 1.0. This is exactly what an engineered grid would produce: speakers *target* the grid points and *approximate* them within measurement tolerance. **The grid is the specification; the production is the approximation.** The same articulator hand-tremor logic that makes Illustrator's snap-to-grid feature useful makes the *Śikṣā*'s temporal grid useful.

### The spatial / temporal grid principles, paired

| | Spatial axis (where sound is made) | Temporal axis (how long sound takes) |
|---|---|---|
| **Grid points** | Five *sthāna*: *kaṇṭhya*, *tālavya*, *mūrdhanya*, *dantya*, *oṣṭhya* | Four *mātrā* values: ½, 1, 2, 3 |
| **Continuous interpolation excluded** | Alveolar (between dental and retroflex), labio-dental (between labial and dental), glottal — all available to the mouth, none included | Intermediate durations (0.75, 1.5, etc.) — all available to speech, none specified |
| **Spacing rationale** | ~2 cm minimum between adjacent places, for acoustic distinguishability | 1 : 2 ratio between grid points, for unambiguous rhythmic distinction |
| **Production approximates grid** | Articulator contact varies within a tolerance band around the ideal place | Duration varies within a tolerance band around the ideal *mātrā* count |
| **Canonical introduction in manuscript** | Ch 8 §8.4 (Illustrator / Figma / Blender analogy) | This concept document; eventual Ch 15 / App 3 / App 5 deployment |
| **Engineering signature** | Discrete spatial sampling of a continuous articulatory range | Discrete temporal sampling of a continuous duration range |

### Why this unification matters for the engineering thesis

A natural language does not snap to either grid. Natural-language phonologies have continuous-distribution articulation: speakers cluster around a place of articulation, but the distribution is smooth, with substantial overlap between adjacent places. Natural-language durations are even more continuous — vowel and consonant timing varies smoothly with stress, position, speech rate, emotional state, and dialect.

Sanskrit's architecture does the opposite at *both* axes. The mouth is divided into five discrete *sthāna*. Time is divided into four discrete *mātrā* values. Production approximates the grid; the grid does not adjust to production.

This is the signature of digital sampling — a discrete grid imposed on a continuous space. Modern audio engineering does this at 44.1 kHz (continuous analog signal sampled at discrete intervals). The *varṇamālā* does it spatially. The *Śikṣā* does it temporally. **The two together form a complete digital-sampling specification for human speech: where each sound is made, how it is made, and for how long.**

A natural language does not produce this signature on either axis. The *varṇamālā* + *Śikṣā* pair is engineered, and the engineering is visible at the same structural register — snap-to-grid — on both axes simultaneously.

This is a unification worth carrying forward. The orthodoxy treats the spatial *varṇamālā* and the temporal *Śikṣā* timing as two unrelated areas of Indic "phonetic theory." The architecture treats them as two axes of one engineered specification, with the snap-to-grid principle operative on each. Recognizing both as snap-to-grid sharpens the engineering claim by a measurable amount: it is not just that each axis is engineered; the two axes are engineered with the *same engineering principle*.

---

## Open questions / expansion paths

(Add as we learn more — this is the section that will grow as analysis matures.)

- **Per-*varga* timing differentiation.** Do the five *vargas* (*kaṇṭhya* / *tālavya* / *mūrdhanya* / *dantya* / *oṣṭhya*) show measurably different total durations? Modern phonetics says yes — place of articulation influences both VOT and closure duration. The *Śikṣā* specifies ½ *mātrā* uniformly across all *vyañjanas*. Where does the per-*varga* variation hide? Possibilities: in the *bala* (force) parameter of the Taittirīya *Śikṣā*'s six-parameter framework; in the release-burst component (which differs by place); in the VOT-by-column structure already mapped above.
- **Recitation-pace measurement of trained reciters.** W. S. Allen, *Phonetics in Ancient India* (1953), Ch. 6 is the classical reference. Post-1953 instrumented studies of lineage-trained Vedic reciters need cataloguing — confirming the 1:2:3 vowel-duration ratio and the ½-*mātrā* consonant duration with modern equipment.
- **Cross-*śākhā* comparison.** Do different *śākhā* lineages (Ṛgveda Śākala-pāṭha, Sāmaveda Kauthuma, Yajurveda Mādhyandina, Atharvaveda Śaunaka, etc.) show the same timing-ratios? If yes, the architecture's timing-precision has held across distinct preservation paths — a strong empirical confirmation of the engineered-architecture thesis.
- **The *mātrā* as percussive unit.** Does the *mātrā* in Vedic recitation correspond to a percussive beat (finger-count, *tāla*-like) that the reciter feels physically? Field reports from Nambūdiri / Maharashtra / Tamil Nadu reciters could establish this. If the *mātrā* is felt as a *beat*, then the timing-precision has both a specification side (*Śikṣā*) and an enforcement side (embodied rhythm).
- **The *dhātu*-shape distribution.** How does the timing-cost of each *dhātu* shape (CV, VC, CVC, CCV, CCVC, etc.) compose to give the *dhātu* its temporal signature? This is the analysis the *dhātu* hexagon visualization is built to support — each shape has a quantifiable total *mātrā* count. The follow-on question: do certain shapes dominate empirically because they hit favored temporal patterns?
- **Aspirated-consonant exception.** The mahāprāṇa categories have measurable aspiration-time added beyond the ½-*mātrā* closure. Does the *Śikṣā* tradition account for this separately? Or is the aspiration treated as part of the consonant's ½-*mātrā* envelope? Worth checking the *Pāṇinīya Śikṣā* and *Taittirīya Prātiśākhya* texts directly.
- **The voiced-aspirate typological argument.** The *ghoṣa-mahāprāṇa* category (घ ध भ) is typologically rare. Modern measurement confirms it requires articulator coordination (simultaneous closure-voicing + breathy release) that most languages cannot produce. Chapter 16 prosecutes the substrate-borrowing claim; this temporal-fingerprint data is direct evidence for the prosecution.
- **Snap-to-grid precision per lineage.** How tight is the variance around each *mātrā* grid point in trained Vedic reciters? A single lineage might produce CC durations in a band of, say, 0.85–0.95 *mātrā* (tight) or 0.7–1.1 *mātrā* (loose). The variance is a measurable signature of the architecture's temporal grid-precision — comparable to the measurable acoustic-distinguishability bandwidth around each spatial *sthāna*. Cross-*śākhā* comparison of this variance would test whether the snap-to-grid temporal precision has held identically across distinct preservation paths.
- **Spatial-temporal grid-precision correlation.** If a single reciter or lineage has tighter spatial-grid precision (articulator placement variance is smaller), do they also have tighter temporal-grid precision (duration variance is smaller)? A correlation would be evidence that the snap-to-grid discipline is one discipline operating on two axes, not two separate disciplines.
- **The *Chandas* meter as the audit instrument.** *Chandas* enforces metrical patterns at the syllable level (*guru*/*laghu* sequences). The patterns work only if the underlying per-*varṇa* timing approximates the *Śikṣā* grid closely. *Chandas* therefore acts as a **systemic audit** of the *Śikṣā* timing-precision: a recitation that fails to hit the metrical pattern reveals a *Śikṣā*-level timing failure. This is the same auditing logic the *padapāṭha* / *krama* / *jaṭā* / *ghana* recitation forms apply to other axes — the architecture builds in cross-axis checks. Worth developing as its own section if the snap-to-grid framing matures.

---

## Possible appendix placements

When the analytical work matures enough to commit, this material could land as:

1. **Standalone appendix part** — *The Timing Specification: Mātrā as Engineering Unit*. Companion to Appendix Part 3 (*The Imperishable Audiograph*) and Appendix Part 5 (*The Architecture by the Numbers*). This is the strongest option if the per-*varga*, cross-*śākhā*, and snap-to-grid analyses produce substantial new data. The snap-to-grid unification alone may justify a standalone appendix by sharpening the engineering claim at two axes simultaneously.
2. **Section within Appendix Part 5** — extending the *Dhātupāṭha* numerical analysis with the temporal axis. Fits if the *dhātu* hexagon visualization yields empirical timing distributions tied to the corpus.
3. **Section within Appendix Part 3** — extending the audiograph framework with the timing layer. Fits if the focus stays on the recording-engineering character of the *Śikṣā* specification.
4. **Section within Chapter 15** — extending the aural-architecture discussion (the existing endnote `vyanjana-duration-shiksha` already deploys here at §15.1). Fits if the material remains compact.
5. **Section within Chapter 8 §8.4** — extending the existing spatial snap-to-grid discussion to add the temporal axis. Most natural home for the snap-to-grid unification specifically. Fits if the cluster / *Chandas* material is held elsewhere and only the snap-to-grid two-axis claim lands at Ch 8.

The decision rests on how much new data the open-questions list above yields. A standalone appendix needs enough material to stand alone; a chapter section needs to integrate without disrupting the chapter's existing arc. The snap-to-grid two-axis unification specifically is strong enough to land *somewhere* — whether at Ch 8 §8.4 (extending the existing canonical introduction) or as the spine of a standalone temporal-axis appendix is the open question.

---

## Cross-references

- **Endnote** `vyanjana-duration-shiksha` — dossier-grade version (in `as_endnotes.md`), deployed at Ch 15 §15.1.
- **Endnote** `hrasva-dirgha-pluta-matra` — vowel-duration framework (companion specification, in `as_endnotes.md`).
- **Design notes** `working/as_dhatu_hexagon_design_notes.md` — the visualization scheme that builds on this timing specification (½:1:2 ratios encoded as hexagon widths).
- **Visualization tool** `working/dhatu_hexagons/dhatu_hexagon.py` — generates SVGs encoding the ½-mātrā vyañjana / 1-mātrā hrasva / 2-mātrā dīrgha distinction as constant-height variable-width hexagons.
- **Chapter 15 §15.1** — the body-prose deployment of the ½-*mātrā* claim ("Vowel durations are quantified in **मात्रा (*mātrā*)** counts; consonants are fixed at half a *mātrā* — ***अर्धमात्रा तु व्यञ्जनम्***.").
- **Chapter 16** — the retroflex / substrate-borrowing chapter that the voiced-aspirate temporal-fingerprint data feeds.
- **Chapter 8 §8.4** — canonical introduction of the *spatial* snap-to-grid principle (Illustrator / Figma / Blender analogy). The temporal snap-to-grid argument extends this discussion to the second axis.
- **Chapter 9** — superset development; snap-to-grid as selective-inclusion principle at the spatial axis (the alveolar exclusion case).
- **Endnotes** `varnamala-grid-geometry`, `tamil-alveolar-place-station`, `paninian-anusvara-yayi-parasavarnah` — develop the spatial snap-to-grid principle from different angles.

---

*Last updated: 2026-05-23. Open for expansion as per-*varga*, cross-*śākhā*, *dhātu*-shape, and snap-to-grid-precision analyses develop.*
