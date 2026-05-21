# Appendix Part 5 — The Architecture by the Numbers

*Draft v2 (2026-05-20). Paraphrased four-tier merge of Codex compression (1,536 words) against the canonical draft (6,182 prose words). **Appendix register**: T1 + T2 + T4 substance preserved through paraphrase; T3 compressed to Codex-register tightness. Codex's flatter twelve-section structure adopted (§5.1 Source and Method → §5.12 Replication, eliminating canonical's §5.3.x sub-numbering); canonical's data tables restored in full (every percentage, every ρ value, every table — the empirical content IS the appendix); Aṣṭādhyāyī it-saṃjñā rules (1.3.2 / 1.3.3 / 1.3.5) restored with Devanagari; cell-level 65× allocation observation restored (labial m=131 vs velar ṅ=2 at identical engineering value); Mādhavīya Dhātuvṛtti / Siddhāntakaumudī / Kṣīrasvāmin commentary mentions restored; Monier-Williams 1899 + Apte 1890 productivity sources restored; full reproducibility-bundle file listing preserved at §5.12. The SYNC PENDING block from the canonical (flagging the Ch 10 §10.11 position-role / cluster-joiner / mūrdhanya 32.5% update that has not yet been folded back) is preserved verbatim as essential metadata.*

---

> **[SYNC PENDING — flagged 2026-05-18]** This appendix carries the original eleven empirical analyses (now flattened into §§5.2–5.10) and a six-principle synthesis (§5.11). Chapter 10 §10.11 was substantively reframed in the Part IV consistency pass with a new analytical layer that has not yet been folded back into this appendix:
>
> - **Position-role taxonomy** — onset-outer / onset-inner / coda-inner / coda-outer per consonant; the *role-valency* profile; the empirical foundation for *role-valency as the structural face of varṇa-śakti*.
> - **Cluster-joiner specialist class** — *ra* (र), *ya* (य), *ṣa* (ष), *na* (न), *la* (ल), *va* (व) as the cluster-bonders, carrying 73% of inner-cluster deployment.
> - **The five class-level signatures** — column / place / row / closure / bonding signatures named in Ch 10 §10.11.
> - **Extended-cluster dataset** — 1,852 single-*akṣara* atoms (cluster-extended), versus the appendix's current CVC-only 920-atom baseline.
> - **Place-level inner-position activity** — *mūrdhanya* (मूर्धन्य) class at 32.5%; load-bearing for the retroflex-as-architecturally-central argument in Ch 10 §10.13 and Ch 16 §16.3.
> - **New figures** — `building_dhatuh_position_roles.svg`, `building_dhatuh_subatomic_periodicity.svg`, `building_dhatuh_two_level_periodicity.svg` (deployed in Ch 10 §10.11; appendix does not yet reference them).
> - **The *ṛ* (ऋ) / *ra* (र) retroflex bridge** — cross-inventory coupling at the *mūrdhanya* site. The appendix has the raw *ṛ*-vowel-frequency data at §5.7 but not the bridge analysis Ch 10 §10.13 and Ch 16 §16.3 carry.
> - **Conceptual framings** — *svara* / *vyañjana* as atom / ion; two periodic tables stacked; position-preference as a hidden engineering axis (consolidated in `analysis/dhatupatha/FINDINGS.md`, updated 2026-05-17).
>
> **Sync deferred** to a coordinated Ch 10 / Ch 11 / Appendix 5 pass after the Path C empirical workstream completes (see `working/as_todo.md` CURRENT FOCUS — *Path C autonomous-night-session kickoff*). Path C's corpus-attested combinatorial-valency data feeds Ch 11's *Periodic Table of dhātavaḥ* analysis; updating the appendix now would mean updating it again after Path C lands.
>
> **Until the sync runs:** readers should consult Ch 10 §10.11 directly for the position-role analysis, `analysis/dhatupatha/FINDINGS.md` for the consolidated engineering-signal synthesis, and the chapter's figures for the visual analysis. The eleven analyses below remain valid as far as they go; the gap is in what they do not yet cover.

---

Chapter 10 states the claim. This appendix shows the arithmetic.

The claim is that the **धातुपाठ (*Dhātupāṭha*)** is not a loose list of "verbal roots." It is an engineered atomic inventory. If that claim is true, the inventory should carry statistical signatures: compression, cost-versus-distinguishability trade-offs, position-specific deployment, phonotactic constraints, class-specific behavior, and high productivity from minimal atoms.

The numbers show exactly that.

## 5.1 Source and Method

The source corpus is the digital Pāṇinian *Dhātupāṭha* from the open-source `sanskrit/vyakarana` project: 2,168 entries across the ten **गणाः (*gaṇāḥ*)**. This count sits within the conventional Pāṇinian range (~1,940 to ~2,200 depending on recension); the **माधवीय धातुवृत्ति (*Mādhavīya Dhātuvṛtti*)**, the **सिद्धान्तकौमुदी (*Siddhāntakaumudī*)**, and the **क्षीरस्वामिन् (*Kṣīrasvāmin*)** commentary yield comparable totals with minor recensional variation in marginal entries.

Each Pāṇinian *dhātu* citation form carries **अनुबन्ध (*anubandha*)** markers — phonemes present in the citation that are not part of the underlying root, used to signal grammatical properties the **अष्टाध्यायी (*Aṣṭādhyāyī*)** will use downstream. The **इत्संज्ञा (*it-saṃjñā*)** rules of *Aṣṭādhyāyī* 1.3.2–1.3.9 specify which phonemes are *anubandhas*. Three rules apply to *dhātus* and are implemented in every analysis script:

- **1.3.2 — *upadeśe 'janunāsika it*** (उपदेशेऽजनुनासिक इत्): a final *anunāsika*-marked short vowel is an *anubandha*. Trailing short *-a* / *-i* / *-u* after a consonant carries this status. Implementation strips such trailing short vowels *only when at least one other vowel remains* — preserving genuine CV-pattern roots like *ji* (जि, to conquer), *hu* (हु, to sacrifice), *sru* (स्रु, to flow).
- **1.3.3 — *halantyam*** (हलन्त्यम्): a trailing single-consonant *anubandha* is stripped when it sits immediately after a vowel. The canonical case is *kṛ* (कृ), cited as *ḍukṛñ* (डुकृञ्); after the initial *ḍu* is stripped by 1.3.5 and the trailing *ñ* by 1.3.3, the underlying root *kṛ* is recovered.
- **1.3.5 — *ādir ñiṭuḍavaḥ*** (आदिर्ञिटुडवः): the initial two-character sequences *ñi* / *ṭu* / *ḍu* in *dhātu* citation forms are *anubandhas* and are stripped from the front.

Accent markers (~, \\, ^) — the **उदात्त (*udātta*)** / **अनुदात्त (*anudātta*)** / **स्वरित (*svarita*)** recitational distinctions — are stripped before structural classification. The method is deliberately reproducible. Every table comes from scripts in `analysis/dhatupatha/`. The falsifications matter as much as the confirmations: they show where the engineering is deeper than the first model.

## 5.2 Compression — Particle and Akṣara Counts

**Prediction.** An engineered atomic inventory should favor compact forms: a peak near the minimum particle count compatible with semantic distinction; a sharp falloff beyond the single-**अक्षर (*akṣara*)** articulatory threshold; single-*akṣara* dominance.

**Data** (across all 2,168 *dhātus*):

| Particles | Count | % | Common patterns | Examples |
|---|---:|---:|---|---|
| 2 (minimum) | 236 | 10.9% | CV, VC | *kṛ* कृ, *bhū* भू, *dā* दा, *jñā* ज्ञा, *pā* पा, *ji* जि, *hu* हु, *ad* अद् |
| 3 (modal) | 1,051 | 48.5% | CVC, CCV, VCV | *gam* गम्, *pat* पत्, *vac* वच्, *yam* यम्, *labh* लभ्, *sthā* स्था |
| 4 | 676 | 31.2% | CCVC, CVCC, CVCV | *svap* स्वप्, *kalp* कल्प्, *jval* ज्वल्, *bandh* बन्ध्, *granth* ग्रन्थ् |
| 5 (threshold) | 156 | 7.2% | CCVCC, CVCVC, CCVCV | *spand* स्पन्द्, *skand* स्कन्द् |
| 6+ (cliff) | 42 | 1.9% | — | — |

*Akṣara* count: 1 *akṣara* 82.8%, 2 *akṣaras* 16.1%, 3+ *akṣaras* 1.2%.

**Verdict — all three predictions confirmed.** Peak at 3 particles (48.5%); cliff at 6+ (1.9%); single-*akṣara* dominance at 82.8%. The architecture compresses meaning into the smallest pronounceable unit that can still carry distinction.

**Cohort check.** A subsidiary test compares 1-*akṣara* and 2-*akṣara* cohort column distributions: every column differs by less than 2 percentage points between the cohorts. The engineering preferences are *not* artifacts of one cohort. Whether the engineer builds a 1-*akṣara* atom or a 2-*akṣara* atom, the same column-frequency distribution applies — the architecture's column preferences are structural properties of the system, not statistical artifacts of corpus composition.

## 5.3 Cost × Distinguishability — The Varga Columns

**Prediction.** The compression principle predicts an articulatory-cost gradient at the column level: C1 (unvoiced unaspirated — *k, c, ṭ, t, p*; क, च, ट, त, प) cheapest and dominant; C4 (voiced aspirated — *gh, jh, ḍh, dh, bh*; घ, झ, ढ, ध, भ) most expensive and rarest. Order predicted: C1 > C2 ≈ C3 > C4.

**Data** (*gaṇa* 1, the primary class — 1,485 *varga*-consonant occurrences):

| Column | Count | % |
|---|---:|---:|
| C1 (unv-unasp — *k, c, ṭ, t, p*) | 555 | **37.4%** |
| C2 (unv-asp — *kh, ch, ṭh, th, ph*) | 136 | **9.2%** |
| C3 (voi-unasp — *g, j, ḍ, d, b*) | 382 | 25.7% |
| C4 (voi-asp — *gh, jh, ḍh, dh, bh*) | 161 | **10.8%** |
| C5 (nasal — *ṅ, ñ, ṇ, n, m*) | 251 | 16.9% |

**Verdict — partially confirmed, one substantive refinement.** C1 dominance ✓. But the rarest column is **C2 (9.2%), not C4 (10.8%)**. The cost-only model predicted that voiced aspirates should be suppressed most. The data says otherwise. Aspiration on a voiceless stop is a *small* perceptual change (a longer breath puff after release). Aspiration on a voiced stop is a *large* perceptual change — the breathy-voice / **महाप्राण-घोषवत् (*mahāprāṇa-ghoṣavat*)** signature is highly salient. C4 pays its cost; C2 pays cost for negligible distinguishability gain.

The engineering principle is therefore **cost × distinguishability**, not cost alone.

**Quantitative test.** Each of the 25 *varga* consonants is assigned (place, voicing, aspiration, nasality) features. Weighted feature-distance uses asymmetric-aspiration weighting per above. Engineering value = mean_weighted_distance / (1 + cost). Spearman rank correlations against *gaṇa* 1 frequency:

| Metric | ρ |
|---|---:|
| **Engineering value** (distinguishability / (1+cost)) | **+0.304** |
| Mean weighted distance (distinguishability alone) | −0.465 |
| Mean binary Hamming distance | −0.339 |
| Cost (raw) | −0.401 |

Engineering value is the strongest positive predictor (ρ = +0.304). Pure distinguishability is *negatively* correlated with frequency because cost dominates — high-distinguishability consonants are also high-cost. The combined metric captures the trade-off.

**The limitation, and the deeper architecture.** ρ = +0.304 means roughly 9% of frequency variance is explained by engineering value. The remaining 91% is unexplained by this two-factor model. Looking at the per-cell data shows why. Within the C1 row (engineering value 2.40, all five cells tied):

- ***k*** (क, velar): 197 occurrences
- ***p*** (प, labial): 101
- ***c*** (च, palatal): 98
- ***t*** (त, dental): 83
- ***ṭ*** (ट, retroflex): 76

Within the C5 row (nasals, engineering value 1.29):

- ***m*** (म, labial): 131
- ***ṇ*** (ण, retroflex): 58
- ***n*** (न, dental): 38
- ***ñ*** (ञ, palatal): 22
- ***ṅ*** (ङ, velar): **2**

*m* vs *ṅ* — a **65× difference at identical engineering value**. The architecture's cell-level preferences are real and substantial — not statistical noise. Specific (place × column) cells are deployed at wildly different rates that the two-factor model cannot capture.

The framework is column-aware *and* cell-aware. Column-level engineering is real; the deeper architecture works cell by cell.

## 5.4 Position Changes the Function

**Prediction.** Distinguishability varies by position because acoustic cues vary. Aspiration is strong in initial / medial, weak in final. Voicing is strong in initial / medial, moderate in final. Place cue is strong in initial, moderate in final.

**Data** (*gaṇa* 1, column distribution within each position):

| Position | C1 | C2 | C3 | C4 | C5 | N |
|---|---:|---:|---:|---:|---:|---:|
| Initial | 41.5% | 4.3% | 22.2% | 14.4% | 17.6% | 653 |
| Medial | 42.4% | 10.2% | 18.5% | 6.4% | 22.6% | 314 |
| Final | 29.2% | 14.7% | 34.6% | 9.1% | 12.5% | 518 |

**Verdict — initial confirmed; final breaks the framework.**

- **Initial.** C1 (41.5%) > C3 (22.2%) > C5 (17.6%) > C4 (14.4%) > C2 (4.3%). The cleanest single confirmation: C2 at initial is the rarest column at 4.3%.
- **Final.** Two major divergences. (i) **C3 outranks C1** in final position (34.6% vs 29.2%) — voiced consonants are *preferred* as finals over voiceless. (ii) C2 is *more* common in final (14.7%) than in initial (4.3%) — contrary to the weakened-aspiration-cue prediction.

**Why finals break the model.** Final consonants in Sanskrit *dhātus* have a third role beyond standing distinguishably: they are the **bonding sites** where *dhātus* combine with **प्रत्यय (*pratyaya*)** affixes (Chapter 12) and where words combine with following words via **सन्धि (*sandhi*)**. The architecture of *sandhi* requires a rich, diverse final-consonant inventory — voiced and aspirated finals participate in specific *sandhi* transformations essential to the combinatorial chemistry.

The framework therefore is **cost × distinguishability × combinatorial load**. The two-factor model holds at initial; the three-factor model is needed at final.

The engineering is not assigning sounds to empty slots. It is assigning sounds to roles.

## 5.5 Place and the Retroflex Signature

**Prediction.** All five places (velar, palatal, retroflex, dental, labial) roughly comparable; retroflex slightly under (tongue-tip-curl is the most demanding gesture); retroflex depleted in initial (Sanskrit's phonotactic discipline treats retroflex as *triggered* phonemes); dentals + labials over-represented in final (clean syllable-closers); palatals depleted in final (typologically unusual coda).

**Data** (*gaṇa* 1):

| Place | Count | % | Initial | Medial | Final |
|---|---:|---:|---:|---:|---:|
| Velar | 364 | 24.5% | 54.1% | 23.9% | 22.0% |
| Palatal | 220 | 14.8% | 39.1% | 15.9% | 45.0% |
| Retroflex | 226 | 15.2% | **13.7%** | 23.5% | **62.8%** |
| Dental | 311 | 20.9% | 46.0% | 21.2% | 32.8% |
| Labial | 364 | 24.5% | 53.8% | 20.1% | 26.1% |

**Verdict — predictions split.**

- **Three-tier place structure** (not uniform): top (velar 24.5%, labial 24.5%), middle (dental 20.9%), bottom (palatal 14.8%, retroflex 15.2%).
- **Retroflex initial-depletion strongly confirmed.** 13.7% initial vs ~50% for velar / labial. Mirror image: retroflex final share is **62.8%** — nearly three times uniform.
- **Dentals + labials *not* over-represented in final** — they sit at 32.8% and 26.1%, both below uniform.
- **Palatals *not* depleted in final** — they sit at 45.0%, *more* than initial 39.1%.

**What this reveals.** Retroflex finals participate in the **रुकि (*ruki*)** rule, **विसर्ग (*visarga*)** conditioning, the cerebralization of *s* → *ṣ* (स → ष), and other *sandhi* mechanisms. The architecture places retroflex force where it can bond, trigger, and transform. Palatals likewise: their final-position prominence reflects the *sandhi* mechanisms operating on *-j*, *-c*, *-bhuj*-style endings.

The architecture is not optimizing ease of closure. It is optimizing downstream combinatorics.

## 5.6 Clusters and Bonding

**Prediction.** Initial 2-consonant clusters dominated by stop + sonorant (sonority-rising onsets — *kr-*, *tr-*, *pr-*, *dr-*, *gr-*, *bhr-*, *dhr-*, *śr-*). S + stop clusters (*sp-*, *st-*, *sk-*, *sm-*, *sn-*) — Sanskrit's famous exception to sonority sequencing — present. Three-consonant initial clusters rare. Final 2-consonant clusters dominated by nasal + stop (*-nd*, *-nt*, *-mb*, *-mp*).

**Data** (*gaṇa* 1):

- 22.8% of *dhātus* have 2-consonant initial clusters; 0.6% have 3-consonant initial clusters.
- 14.1% of *dhātus* have 2-consonant final clusters; 0.6% have 3-consonant final clusters.

Top initial 2-consonant clusters: **tr-** (त्र-, 5.4%), **śr-** (श्र-, 4.7%), **kṣ-** (क्ष-, 4.3%), *dhr-* / *ṣṭ-* / *bhr-* / *gl-* (3.9% each).

Top final 2-consonant clusters: **-kṣ** (-क्ष्, 20.0% — single-cluster dominance), *-rd* (7.5%), *-ñc* (7.5%), *-rb* (6.9%), *-rv* (6.9%), *-ll* (6.2%).

**Verdict — partially confirmed; one striking surprise.**

- Stop + sonorant ✓; S + stop ✓; three-consonant rarity ✓.
- **Final cluster prediction wrong**: nasal + stop is *not* dominant. The dominant final cluster is **-kṣ** (-क्ष्), accounting for 20% of all final 2-consonant clusters (*dakṣ*, *lakṣ*, *sakṣ*, *rakṣ*, *bhakṣ*). Nasal-plus-stop clusters appear (*-ñc*, *-mbh*, *-ñj*, *-lbh*) but each is a small fraction.

The *-kṣ* over-representation is a Sanskrit signature. Geminate finals (*-ll*, *-ḍḍ*, *-kk*, *-ṭṭ*) also appear — doubling as a structural device.

The cluster data points toward the position-role analysis in Chapter 10 §10.11: consonants do not merely appear; they specialize.

## 5.7 The Ṛ Signal

**Prediction.** अ (*a*, the inherent vowel) should dominate — lowest cost, default carrier. ऋ (*ṛ*) should cluster with specific consonants (the classic *vṛ-* वृ-, *kṛ-* कृ- root pattern). Long vowels should be over-represented in compact CV / CCV *dhātus*.

**Data** (*gaṇa* 1, 1,397 vowel occurrences):

| Rank | IAST | Count | % |
|---:|---|---:|---:|
| 1 | *a* (अ) | 512 | **36.6%** |
| 2 | ***ṛ*** (ऋ) | 214 | **15.3%** |
| 3 | *u* (उ) | 182 | 13.0% |
| 4 | *i* (इ) | 119 | 8.5% |
| 5 | *e* (ए) | 108 | 7.7% |
| 6 | *ā* (आ) | 87 | 6.2% |
| 7 | *ī* (ई) | 61 | 4.4% |
| 8 | *ū* (ऊ) | 45 | 3.2% |
| 9–13 | *ai, o, ḷ, au, ṝ* | (small) | <2% each |

Top consonants preceding *ṛ*: *v* (11.2%), *k* (8.9%), *ṣ* (7.9%), *ḍ* (7.5%), *p* (7.0%).

**Verdict — predictions confirmed; one striking new finding.**

- *a*-dominance ✓ at 36.6%.
- *ṛ* pairs with specific consonants ✓ (*vṛ*, *kṛ*, *ṣṛ*, *ḍṛ*, *pṛ*).
- Long vowels collectively ~14%; short vowels ~75%.

**The headline finding.** ***ṛ* is the second-most-common vowel in the *Dhātupāṭha* at 15.3%.** Cross-linguistically extraordinary. Syllabic *ṛ* is a typologically rare phoneme — most languages do not have one at all; where it exists it is typically marginal. In Sanskrit, *ṛ* is placed as a load-bearing vowel of the foundational atomic inventory, used in 214 distinct primary-class *dhātus*: *kṛ*, *vṛ*, *dṛś*, *mṛ*, *hṛ*, *tṛp*, *vṛt*, *kṛp*, *mṛj*, *sṛj*, *dṛp*. These atoms generate massive vocabulary: *karma* (कर्म), *manas* (मनस्), *mṛtyu* (मृत्यु), *mokṣa* (मोक्ष), *sṛṣṭi* (सृष्टि), *vṛddhi* (वृद्धि), *kṛti* (कृति), *prakṛti* (प्रकृति), *vikṛti* (विकृति), and hundreds more.

The *ṛ* signal later becomes the bridge to र (*ra*): vowel and consonant coupled at the retroflex-adjacent site (Ch 10 §10.13; Ch 16 §16.3 develop the bridge). The raw appendix data already shows the load-bearing fact. Sanskrit did not treat *ṛ* as marginal. It made *ṛ* architecturally central.

## 5.8 The OCP Signature

**Prediction.** For single-syllable (1-*akṣara*) *dhātus* with both initial and final *varga* consonants, two patterns may emerge: place harmony (initial and final share place — *kak*-style), voicing harmony (initial and final share voicing — *gam*-style), or avoidance. No strong directional prediction.

**Data** (*gaṇa* 1, 271 single-syllable *dhātus* with both initial and final *varga* consonants):

- **Place harmony — observed 10.3%, expected 27.7%** (under independence) → **STRONG AVOIDANCE**. Only 28 of 271 *dhātus* have same-place initial and final, when independence would predict ~75. ~62% below chance.
- **Voicing harmony — observed 55.7%, expected 49.4%** → modest harmony (~13% above chance).

**The OCP signature.** Sanskrit *dhātus* *avoid* same place of articulation flanking the vowel. The Obligatory Contour Principle operates as design: *kak* and *pap* are suppressed; *kap*, *gat*, *pun* preferred. Place-variation is engineered into the CVC structure for maximum acoustic distinctiveness across the syllable.

**This is the strongest single empirical signal in the entire appendix.** The *dhātu* is not merely compressed. It is internally distributed for acoustic distinction.

Voicing harmony is the milder secondary effect — easier to maintain a voicing state across the syllable than to switch.

## 5.9 Gaṇa-Specific Functional Matching

**Prediction.** The column distribution in *gaṇa* 1 should hold across all 10 *gaṇāḥ* with minor variation. The C1-first pattern should be robust.

**Data** (all 10 *gaṇāḥ*):

| Gaṇa | Class | Dhātus | C1 | C2 | C3 | C4 | C5 |
|---:|:---:|---:|---:|---:|---:|---:|---:|
| 1 | *bhvādi* | 1,134 | 37.4% | 9.2% | 25.7% | 10.8% | 16.9% |
| 2 | *adādi* | 76 | 37.3% | 1.5% | 35.8% | 3.0% | 22.4% |
| **3** | ***juhotyādi*** | **25** | **22.7%** | **0.0%** | **22.7%** | **31.8%** | **22.7%** |
| 4 | *divādi* | 151 | 36.5% | 2.4% | 22.2% | 15.6% | 23.4% |
| 5 | *svādi* | 39 | 43.6% | 0.0% | 17.9% | 25.6% | 12.8% |
| 6 | *tudādi* | 171 | 38.4% | 10.3% | 26.4% | 8.7% | 16.1% |
| 7 | *rudhādi* | 25 | 35.0% | 2.5% | 35.0% | 12.5% | 15.0% |
| 8 | *tanādi* | 10 | 31.2% | 0.0% | 0.0% | 6.2% | 62.5% |
| 9 | *kryādi* | 69 | 30.0% | 10.0% | 15.0% | 18.8% | 26.2% |
| 10 | *curādi* | 468 | 47.3% | 6.0% | 24.6% | 6.9% | 15.0% |

**Verdict — robust with one substantive outlier.**

- C1-first holds in 8 of 10 *gaṇas* (1, 2, 4, 5, 6, 7, 9, 10).
- *Gaṇa* 8 (*tanādi*, n=10) too small to read confidently; the C5 spike (62.5%) reflects small-class composition.
- ***Gaṇa* 3 (*juhotyādi*) — the substantive outlier**: **C4 leads at 31.8%**. This is the reduplicating class — *dhātus* like *hu*, *dā*, *dhā*, *mā* that reduplicate in present-tense formation (*juhoti*, *dadāti*, *dadhāti*, *mimīte*).

**Why the *juhotyādi* C4 enrichment makes engineering sense.** Reduplication is a redundancy mechanism — the *dhātu*'s initial consonant doubles to form the present-tense stem. For the doubled consonant to remain identifiable across the syllable boundary, the consonant must be acoustically robust. C4 — voiced, aspirated, breathy — is the column with the most distinctive acoustic signature; the same property that made C4 less-suppressed than C2 in §5.3.

The architecture deploys the most-distinguishable column where distinguishability matters most. **Functional matching.**

## 5.10 Productivity from Minimum

**Prediction.** If the compression principle governs the architecture, the simplest *dhātus* (CV pattern, 2 particles) should also be the *most productive* — generating the largest derivative vocabularies. Engineering produces minimum atoms because minimum atoms support maximum combinatorial reach. Predicted Spearman ρ between productivity and particle-count: strongly negative.

**Data** (curated sample of 138 *dhātus* spanning the *Dhātupāṭha*'s structural pattern space; productivity = estimated count of primary derivatives per *dhātu*, drawn from the Monier-Williams *Sanskrit-English Dictionary* (1899) and V. S. Apte's *Practical Sanskrit-English Dictionary* (1890); approximate ±20%, ranking is load-bearing).

Top 15 *dhātus* by productivity:

| Rank | Dhātu | Pattern | Particles | Productivity | Gloss |
|---:|:--|:---|---:|---:|---|
| 1 | *kṛ* कृ | CV | 2 | 75 | do/make |
| 2 | *bhū* भू | CV | 2 | 55 | be/become |
| 3 | *sthā* स्था | CCV | 3 | 55 | stand |
| 4 | *gam* गम् | CVC | 3 | 55 | go |
| 5 | *dā* दा | CV | 2 | 45 | give |
| 6 | *dhā* धा | CV | 2 | 40 | place/set |
| 7 | *jñā* ज्ञा | CV | 2 | 40 | know |
| 8 | *hṛ* हृ | CV | 2 | 40 | carry/take |
| 9 | *nī* नी | CV | 2 | 40 | lead |
| 10 | *as* अस् | VC | 2 | 40 | be/exist |
| 11 | *vac* वच् | CVC | 3 | 40 | speak |
| 12 | *jan* जन् | CVC | 3 | 40 | be born |
| 13 | *vid* विद् | CVC | 3 | 40 | know |
| 14 | *vṛt* वृत् | CVC | 3 | 40 | turn/exist |
| 15 | *śrū* श्रू | CV | 2 | 35 | hear |

Productivity stratified by particle count:

| Particles | n | Mean | Median | Max |
|---:|---:|---:|---:|---:|
| 2 | 26 | **30.1** | 30.0 | 75 |
| 3 | 72 | 20.5 | 18.0 | 55 |
| 4 | 31 | 13.5 | 12.0 | 30 |
| 5 | 8 | **11.4** | 12.0 | 18 |

Productivity by structural pattern:

| Pattern | n | Mean productivity |
|---|---:|---:|
| **CV** | 21 | **32.6** |
| CVC | 57 | 22.3 |
| VC | 5 | 19.6 |
| CVCC | 8 | 16.1 |
| CCV | 10 | 15.3 |
| CCVC | 23 | 12.5 |
| **CCVCC** | 8 | **11.4** |

Spearman ρ (productivity vs. particle count): **−0.485**.

Mean particle count, top 20 by productivity: **2.40**. Mean particle count, bottom 20: **3.50**. Bottom-to-top ratio: 1.46×.

**Verdict — strongly confirmed.** The CV pattern's mean productivity (32.6) is **2.9×** higher than CCVCC (11.4). The top 20 productivity ranks are dominated by 2-particle CV *dhātus* (11 of 20). *Kṛ* alone — two particles — anchors 75+ primary derivatives, more than the entire CCVCC sample combined.

**The natural-language inversion.**[NOTE: productivity-inversion-natural-language] In natural languages, the most-frequent forms tend toward idiosyncratic irregularity: English *be / have / do* are paradigmatically broken; Latin *esse / ire / ferre* are suppletive; Greek *eimi / oida / phēmi* same pattern. The frequency-irregularity correlation is one of the most-replicated typological findings in natural-language morphology. In Sanskrit's engineered case, the correlation runs the opposite way: the highest-productivity *dhātus* are *also* the most structurally minimal *and* paradigmatically regular. There is no idiosyncrasy at the top.

That is not drift. That is engineering.

## 5.11 Synthesis — Six Engineering Principles

The numbers reveal the architecture operating at six levels:

1. **Cost × distinguishability** (per-consonant). C1 dominates because it is cheap and clear; C4 survives because it earns its cost through perceptual value; C2 is under-deployed because it pays cost for negligible distinctiveness gain. Spearman ρ = +0.304.
2. **Cell-level allocation** (per place × column). Specific cells are deployed at wildly different rates the two-factor model cannot capture. Labial *m* (131) vs velar *ṅ* (2) — 65× at identical engineering value. The architecture allocates at the cell.
3. **Position-conditional preferences** (per position × column / place). Each column and each place has a position-specific signature. Retroflex strongly prefers final (62.8%); palatals favor final (45%); velars and labials favor initial.
4. **Cross-position OCP** (per *dhātu*). Place-of-articulation avoidance across the syllable operates at 62% below chance. The strongest single empirical signal in the appendix.
5. **Gaṇa-specific functional matching** (per derivational class). The *juhotyādi* reduplicating class enriches C4 (the most acoustically robust column) because reduplication needs robustness.
6. **Productivity-from-minimum** (per *dhātu* productivity-axis). The simplest *dhātus* (2-particle CV) are the most-productive atoms; ρ = −0.485 between productivity and particle count. Unlike natural languages, high-productivity *dhātus* are also paradigmatically regular.

These principles operate simultaneously and reinforce each other. The architecture is compact, but not merely compact — it is cost-aware, contrast-aware, position-aware, boundary-aware, class-aware, and productivity-aware.

The *Dhātupāṭha* is an atomic inventory. The numbers show the engineering.

## 5.12 Replication

The reproducibility bundle lives at `analysis/dhatupatha/`.

- **`data/dhatupatha.csv`** — source data (2,168 entries) from the open-source `sanskrit/vyakarana` GitHub project. Three columns: *gaṇa*-number, position-within-*gaṇa*, *dhātu* in SLP1.
- **`data/derived/dhatupatha_decomposed.md`** — every *dhātu* rendered in Devanāgarī with **वर्ण (*varṇa*)**-level decomposition. Generated by `decompose_dhatupatha.py`.
- **`scripts/analyze_dhatupatha.py`** — structural classification, particle count, *akṣara* count, pattern, *gaṇa* distribution. Generates §5.2 figures.
- **`scripts/decompose_dhatupatha.py`** — SLP1 → Devanāgarī conversion + *varṇa*-level decomposition.
- **`scripts/analyze_varga_distribution.py [gaṇa]`** — column × position analysis. §5.3 and §5.4 figures.
- **`scripts/analyze_place_distribution.py [gaṇa]`** — place × position analysis. §5.5 figures.
- **`scripts/analyze_extensions.py [gaṇa]`** — cluster, *akṣara*-count breakdown, vowel × consonant. §5.6 and §5.7 figures.
- **`scripts/analyze_distinguishability.py`** — feature-distance scoring, onset-coda OCP, cross-*gaṇa*. §5.8 and §5.9 figures.
- **`scripts/analyze_productivity.py`** — productivity correlated against structural complexity. §5.10 figures.
- **`data/dhatu_productivity.csv`** — curated productivity sample (138 *dhātus*) with derivative-count estimates and source attribution (MW 1899; Apte 1890).

Requirements: Python 3.10+. Standard library only. From the bundle root: `python3 scripts/<script-name>.py [gaṇa]` (`[gaṇa]` is an optional numerical filter 1–10).

The bundle is self-contained and includes a README with full attribution, methodology notes, and a license file. Every empirical claim in Chapter 10 and in this appendix can be verified by re-running the scripts against the source CSV.

The appendix is not asking the reader to trust the conclusion. It gives the reader the machinery to rerun the test.

The architecture is visible. The numbers are reproducible.

---

## Draft notes (Appendix Part 5 v2)

**Word count:** ~4,700 prose words across twelve sections after the **2026-05-20 paraphrased four-tier merge** (Codex base 1,536; canonical 6,182). The tables themselves account for ~30% of the word count. Paraphrase compression of canonical prose ≈ 30% net; data tables preserved verbatim.

**Four-tier merge (appendix-register posture: T1 + T2 + T4 substance preserved through paraphrase; T3 compressed to Codex-register tightness; data tables T4-verbatim because they ARE the empirical content):**

- **T1 substance preserved (paraphrased — load-bearing):**
  - **[SYNC PENDING] block** preserved verbatim at the top. It is essential metadata: the appendix is partially out of date relative to Ch 10 §10.11's position-role / cluster-joiner / mūrdhanya 32.5% / extended-cluster 1,852-atom analysis; sync deferred to a coordinated Ch 10 / Ch 11 / Appendix 5 pass after Path C completes. Readers are directed to Ch 10 §10.11 and `analysis/dhatupatha/FINDINGS.md` for the consolidated current state.
  - §5.8 OCP signature ("strongest single empirical signal in the entire appendix") — 62% below chance suppression of same-place flanking.
  - §5.7 *ṛ* finding (typologically rare; second-most-common vowel at 15.3%; load-bearing for the *ṛ* / *ra* retroflex bridge to be developed in Ch 10 §10.13 + Ch 16 §16.3).
  - §5.10 productivity-from-minimum + natural-language inversion (English be/have/do; Latin esse/ire/ferre; Greek eimi/oida/phēmi) — comparative-architecture polemic that distinguishes Sanskrit from natural-language drift.
  - §5.11 six-principle synthesis preserved as numbered list.

- **T2 substance preserved (paraphrased — substantive):**
  - §5.1: Aṣṭādhyāyī 1.3.2 / 1.3.3 / 1.3.5 *it-saṃjñā* rules restored with full Sanskrit + Devanagari + IAST + gloss + implementation detail.
  - §5.1: Accent markers (*udātta* / *anudātta* / *svarita*) named.
  - §5.1: Mādhavīya Dhātuvṛtti / Siddhāntakaumudī / Kṣīrasvāmin commentary mentions restored (cross-validation of corpus count against recensional variation).
  - §5.2 cohort check restored — 1-*akṣara* and 2-*akṣara* cohorts show identical column distributions (architecture's preferences are structural not corpus artifacts).
  - §5.3 cost × distinguishability framework restored with C2 vs C4 refinement; perceptual phonetics rationale (*mahāprāṇa-ghoṣavat* signature on voiced aspirates).
  - §5.3 cell-level allocation restored: labial *m* (131) vs velar *ṅ* (2) — 65× at identical engineering value. The cell-level data point is one of the appendix's most striking empirical signals; Codex omitted it.
  - §5.4 combinatorial-load three-factor model for finals (cost × distinguishability × combinatorial load); *pratyaya* + *sandhi* bonding-site mechanism.
  - §5.5 *ruki* + *visarga* + cerebralization-of-s mechanisms named.
  - §5.9 *juhotyādi* C4 enrichment + functional-matching argument.
  - §5.10 Monier-Williams 1899 + Apte 1890 productivity-sample sources cited.
  - §5.12 full reproducibility-bundle file listing preserved.

- **T3 (defensible compressions retained from Codex):**
  - Codex's flatter twelve-section structure adopted (eliminates canonical's three-level §5.3.x sub-numbering).
  - Per-section verdict language preserved in Codex's tighter form.
  - §5.6 cluster verdict prose compressed.
  - §5.11 synthesis preserved in Codex's tight enumerated form.

- **T4 substance preserved (verbatim because data tables ARE the empirical content):**
  - §5.2: Full particle-count distribution table (5 rows × 5 columns; 2,168 *dhātus*); *akṣara*-count percentages (82.8% / 16.1% / 1.2%).
  - §5.3: Full *varga* column distribution table (5 columns; 1,485 occurrences); full feature-distance correlation table (4 metrics with ρ); cell-level allocation lists for C1 row (5 cells, 76–197 range) and C5 row (5 cells, 2–131 range).
  - §5.4: Full position × column table (3 positions × 5 columns; N column).
  - §5.5: Full place × position table (5 places × 4 columns).
  - §5.6: Cluster percentages (top initial clusters; top final clusters; -kṣ 20% dominance).
  - §5.7: Full vowel × frequency table (13 vowels with rank); top consonants preceding *ṛ*.
  - §5.8: OCP numbers (10.3% observed vs 27.7% expected; 28 of 271; 55.7% voicing).
  - §5.9: Full cross-*gaṇa* table (10 *gaṇāḥ* × 7 columns); *juhotyādi* highlighted.
  - §5.10: Top-15 *dhātus* by productivity table; particle-count-stratified productivity table; pattern-stratified productivity table; ρ = −0.485; bottom-to-top ratio 1.46×.
  - §5.12: Full reproducibility-bundle file listing.

**Devanagari first-use audit:**

- धातुपाठ (*Dhātupāṭha*) — chapter opening
- गणाः (*gaṇāḥ*) — §5.1
- माधवीय धातुवृत्ति (*Mādhavīya Dhātuvṛtti*) / सिद्धान्तकौमुदी (*Siddhāntakaumudī*) / क्षीरस्वामिन् (*Kṣīrasvāmin*) — §5.1
- अनुबन्ध (*anubandha*) / अष्टाध्यायी (*Aṣṭādhyāyī*) / इत्संज्ञा (*it-saṃjñā*) — §5.1
- उदात्त (*udātta*) / अनुदात्त (*anudātta*) / स्वरित (*svarita*) — §5.1
- Aṣṭādhyāyī rules 1.3.2 / 1.3.3 / 1.3.5 — Sanskrit + Devanagari first-use in §5.1
- अक्षर (*akṣara*) — §5.2
- महाप्राण-घोषवत् (*mahāprāṇa-ghoṣavat*) — §5.3
- प्रत्यय (*pratyaya*) / सन्धि (*sandhi*) — §5.4
- रुकि (*ruki*) / विसर्ग (*visarga*) — §5.5
- वर्ण (*varṇa*) — §5.12
- मूर्धन्य (*mūrdhanya*) — preserved in SYNC PENDING block
- All *dhātu* examples in tables paired with Devanagari (kṛ कृ, bhū भू, etc.)

**Cross-references:**

Backward — Chapter 10 (the structural claim; §10.11 reframed with position-role analysis); Chapter 10 §10.13 (*ṛ* / *ra* retroflex bridge); Chapter 11 (the Periodic Table of *dhātavaḥ*); Chapter 12 (the chemistry of affixation; *pratyaya* combinatorics); Chapter 16 §16.3 (retroflex-as-architecturally-central argument).

Forward — Coordinated Ch 10 / Ch 11 / Appendix 5 sync pass after Path C empirical workstream completes; will fold in the position-role taxonomy, cluster-joiner specialist class (*ra* / *ya* / *ṣa* / *na* / *la* / *va*), five class-level signatures, extended-cluster 1,852-atom dataset, *mūrdhanya* 32.5% inner-position activity, and the new figures.

**Voice notes:**

- Voice register: empirical-engineering report with prediction-data-verdict cycles. Closer to a technical appendix than to the prosecutorial register of Parts 1–3 or the constructive-demonstrative register of Part 4.
- Polemic carried at §5.10 close (natural-language inversion: "That is not drift. That is engineering.") and §5.11 synthesis close ("The numbers show the engineering.").
- Falsifications named in the open at each verdict block — empirical-rigor signal that distinguishes engineering thesis from confirmation-only register.

**Endnote stubs (preserved from canonical):**

- `productivity-inversion-natural-language` — the frequency-irregularity correlation in natural-language typology (English / Latin / Greek suppletives) versus Sanskrit's frequency-regularity correlation; document the canonical typological-morphology literature on suppletion and idiosyncrasy at high frequency.
