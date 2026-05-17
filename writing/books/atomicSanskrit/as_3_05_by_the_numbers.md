# Appendix Part 5 — The Architecture by the Numbers

*The full empirical work behind Chapter 11. Predictions stated in engineering-method order, tested against the 2,168-entry Pāṇinian* Dhātupāṭha *(धातुपाठ) with* anubandhas *(अनुबन्धाः) stripped per* Aṣṭādhyāyī *(अष्टाध्यायी) 1.3.2, 1.3.3, 1.3.5; verdicts on each prediction including the falsifications. The chapter prose carries the load-bearing findings; this appendix carries the full work so any reader can verify every claim. A reproducibility bundle accompanies the book at* `analysis/dhatupatha/` *with the source CSV, the derived Devanāgarī decomposition, and the Python scripts that produce every figure cited here.*

---

## 5.1 Introduction

Chapter 11 makes a structural claim: Sanskrit's *Dhātupāṭha* (धातुपाठ) is an engineered atomic inventory whose composition follows engineering principles that can be predicted in advance and tested against the corpus. The chapter states the principles (compression, cost-versus-distinguishability, the Atomic Corollary) and cites the empirical headlines that confirm them. This appendix supplies the full demonstration.

The work proceeds in engineering-method order. For each empirical question, a prediction is stated *before* the data is consulted — what the engineering framework expects to see in the *Dhātupāṭha*. The data is then computed. The verdict on each prediction — confirmed, refined, falsified — is named in the open. Where predictions fail, the appendix names the deeper principle the failure reveals. The architecture's signature is the *pattern of confirmations and falsifications*, not any single result.

Eleven specific analyses follow, each producing its own prediction → data → verdict cycle. They cumulate into a five-principle synthesis: cost × distinguishability, place-specific deployment, position-conditional preferences, cross-position phonotactic constraints (the OCP / place-avoidance principle), and gaṇa (गण)-specific functional matching. None of these principles is visible to a feature-counting model alone; the architecture's depth requires all five.

---

## 5.2 Source data and methodology

**The source data.** The digital *Dhātupāṭha* (धातुपाठ) is the `data/dhatupatha.csv` file from the open-source `sanskrit/vyakarana` project on GitHub. The CSV has three columns — *gaṇa* (गण)-number, *position-within-gaṇa*, and the *dhātu* (धातु) in SLP1 transliteration with Pāṇinian accent markers (~, \\, ^). The corpus is 2,168 entries across the ten *gaṇāḥ* (गणाः). This count sits within the conventional Pāṇinian range (~1,940 to ~2,200 depending on recension); the *Mādhavīya Dhātuvṛtti* (माधवीय धातुवृत्ति), the *Siddhāntakaumudī* (सिद्धान्तकौमुदी), and the *Kṣīrasvāmin* (क्षीरस्वामिन्) commentary yield comparable totals with minor recensional variation in marginal entries. The full reproducibility bundle is at the repo subdirectory `analysis/dhatupatha/`.

**The anubandha-stripping methodology.** Each Pāṇinian dhātu (धातु) citation form contains *anubandha* (अनुबन्ध) markers — phonemes present in the citation that are not part of the underlying root, used to signal grammatical properties the *Aṣṭādhyāyī* (अष्टाध्यायी)'s rules will use downstream. The *it-saṃjñā* (इत्संज्ञा) rules (*Aṣṭādhyāyī* 1.3.2–1.3.9) specify which phonemes in citation forms are *anubandhas* (अनुबन्धाः). Three of these rules apply to dhātus and are implemented in every analysis script:

- **1.3.2 — *upadeśe 'janunāsika it*** (उपदेशेऽजनुनासिक इत्): a final *anunāsika* (अनुनासिक)-marked short vowel is an *anubandha*. In the standard Pāṇinian-citation tradition, trailing short *-a* (-अ) / *-i* (-इ) / *-u* (-उ) after a consonant carries this status. The implementation strips such trailing short vowels *only when at least one other vowel remains* — preserving genuine CV-pattern roots like *ji* (जि, to conquer), *hu* (हु, to sacrifice), *sru* (स्रु, to flow), where the short vowel *is* the root vowel.

- **1.3.3 — *halantyam*** (हलन्त्यम्): a trailing single-consonant *anubandha* (the *ñit* ञित्, *ṅit* ङित्, *lit* लित्, *ṣit* षित्, *ṭit* टित्, *ḍit* डित् markers signaling ātmanepadī (आत्मनेपदी) conjugation or other grammatical properties) is stripped when it sits immediately after a vowel. The canonical case is the *kṛ* (कृ) dhātu, cited as *ḍukṛñ* (डुकृञ्, SLP1: `qukf\Y`); after the initial *ḍu* (डु) is stripped by 1.3.5 and the trailing *ñ* (ञ्) by 1.3.3, the underlying root *kṛ* (कृ) is recovered.

- **1.3.5 — *ādir ñiṭuḍavaḥ*** (आदिर्ञिटुडवः): the initial two-character sequences *ñi* (ञि, SLP1: `Ji`), *ṭu* (टु, `wu`), *ḍu* (डु, `qu`) in dhātu citation forms are *anubandhas* and are stripped from the front.

Accent markers (~, \\, ^) are stripped before structural classification — they encode the Pāṇinian *udātta* (उदात्त) / *anudātta* (अनुदात्त) / *svarita* (स्वरित) recitational distinctions, not structural phonological content. Cross-validation against the Sanskrit Heritage Platform's `parts.csv` confirms that this rule-set recovers the standard underlying roots for the vast majority of *Dhātupāṭha* entries.

A small residue of edge cases (~0.3% of the corpus) classifies as bare-vowel V-patterns after stripping — special-case Pāṇinian-citation forms such as *i* (इ, to go) and *ṛ* (ऋ, to go). These are correctly retained as 1-akṣara (अक्षर) dhātus.

---

## 5.3 The analyses

### 5.3.1 Particle-count distribution — the thermodynamic threshold

**Prediction**. An engineered atomic inventory should display: (1) a peak near the minimum particle count compatible with semantic distinction (3–4 particles, the sweet spot — pronounceable in a single beat yet acoustically distinguishable); (2) a sharp falloff beyond the single-akṣara (अक्षर) articulatory threshold (around 5 particles per syllable); (3) single-akṣara dominance — the majority of *dhātavaḥ* (धातवः) should occupy exactly one akṣara.

**Data** (across all 2,168 dhātus):

| Particles | Count | % | Common patterns | Examples |
|---|---:|---:|---|---|
| 2 (minimum) | 236 | 10.9% | CV, VC | *kṛ* कृ, *bhū* भू, *dā* दा, *jñā* ज्ञा, *pā* पा, *ji* जि, *hu* हु, *ad* अद् |
| 3 (modal) | 1,051 | 48.5% | CVC, CCV, VCV | *gam* गम्, *pat* पत्, *vac* वच्, *yam* यम्, *labh* लभ्, *sthā* स्था |
| 4 | 676 | 31.2% | CCVC, CVCC, CVCV | *svap* स्वप्, *kalp* कल्प्, *jval* ज्वल्, *bandh* बन्ध्, *granth* ग्रन्थ् |
| 5 (threshold) | 156 | 7.2% | CCVCC, CVCVC, CCVCV | *spand* स्पन्द्, *skand* स्कन्द् |
| 6+ (cliff) | 42 | 1.9% | — | — |

Akṣara count: 1 akṣara 82.8%, 2 akṣara 16.1%, 3+ akṣara 1.2%.

**Verdict — all three predictions confirmed.** Peak at 3 particles (48.5%) with mass at 4 (31.2%); cliff at 6+ (1.9%); single-akṣara dominance at 82.8%.

### 5.3.2 Varga (वर्ग) column distribution — cost × distinguishability

**Prediction**. The compression principle, applied at the column level, predicts an articulatory-simplicity gradient. C1 (unvoiced unaspirated — *k, c, ṭ, t, p*; क, च, ट, त, प) is the cheapest column to produce and should dominate. C4 (voiced aspirated — *gh, jh, ḍh, dh, bh*; घ, झ, ढ, ध, भ) is the most articulatorily expensive and should be the rarest. The order: C1 > C2 ≈ C3 > C4. C5 (nasal) sits in a separate articulatory category.

**Data** (gaṇa 1, the primary class — 1,485 varga-consonant occurrences):

| Column | Count | % |
|---|---:|---:|
| C1 (unv-unasp — *k, c, ṭ, t, p*; क, च, ट, त, प) | 555 | **37.4%** |
| C2 (unv-asp — *kh, ch, ṭh, th, ph*; ख, छ, ठ, थ, फ) | 136 | **9.2%** |
| C3 (voi-unasp — *g, j, ḍ, d, b*; ग, ज, ड, द, ब) | 382 | 25.7% |
| C4 (voi-asp — *gh, jh, ḍh, dh, bh*; घ, झ, ढ, ध, भ) | 161 | **10.8%** |
| C5 (nasal — *ṅ, ñ, ṇ, n, m*; ङ, ञ, ण, न, म) | 251 | 16.9% |

**Verdict — partially confirmed; one substantive refinement.** C1 dominance ✓ at 37.4% — confirmed. But the rarest column is **C2 (9.2%), not C4 (10.8%)**. The cost-naïve prediction expected C4 (which carries the highest articulatory cost — voicing + aspiration) to be the most suppressed, but the data places C2 below C4 by 1.6 percentage points.

**Why the refinement holds**. The naïve cost model treats aspiration as a symmetric feature: adding aspiration to *k* (क) yields *kh* (ख); adding it to *g* (ग) yields *gh* (घ); same cost both directions. Empirical perceptual phonetics says otherwise. Aspiration on a voiceless stop (*k* → *kh*; क → ख) is a *small* perceptual change — a longer puff of breath after release, easily missed in noisy listening conditions. Aspiration on a voiced stop (*g* → *gh*; ग → घ) is a *large* perceptual change — the breathy-voice / *mahāprāṇa-ghoṣavat* (महाप्राण-घोषवत्) signature is highly salient, with murmured-breath voicing during and after closure. C4 earns its place: it pays the cost but gains substantial distinguishability. C2 pays cost for negligible distinguishability gain — and the architects accordingly under-deploy it.

The framework therefore is **cost × distinguishability**, not cost alone. The chapter develops this as a load-bearing engineering principle.

### 5.3.3 Position-conditioned column distribution

**Prediction**. Distinguishability varies by position because different acoustic cues are differentially available:
- Aspiration cue is strong in initial and medial positions (released into a following vowel) but **weak in final position** (no release in connected speech).
- Voicing cue is strong in initial (pre-voicing audible) and medial; moderate in final.
- Nasal cue is strong in all positions.
- Place cue is strong in initial (burst + transitions), moderate in final.

The framework predicts column rankings per position:
- **Initial**: C1 > C5 ≈ C3 > C4 > C2 (all cues available, cost dominates; C2 pays cost for the weakest cue).
- **Medial**: C1 > C5 ≈ C3 > C4 > C2 (same as initial).
- **Final**: C1 > C5 > C3 > C4 ≈ C2 (aspirated columns lose their cue; cost not justified).

**Data** (gaṇa 1, column distribution within each position):

| Position | C1 | C2 | C3 | C4 | C5 | N |
|---|---:|---:|---:|---:|---:|---:|
| Initial | 41.5% | 4.3% | 22.2% | 14.4% | 17.6% | 653 |
| Medial | 42.4% | 10.2% | 18.5% | 6.4% | 22.6% | 314 |
| Final | 29.2% | 14.7% | 34.6% | 9.1% | 12.5% | 518 |

**Verdict — initial position confirmed; medial and final break the framework.**
- **Initial — confirmed**. C1 (41.5%) > C3 (22.2%) > C5 (17.6%) > C4 (14.4%) > C2 (4.3%). The empirical ranking matches the prediction. The "C2 at initial is rarest" finding is the cleanest single confirmation in the whole analysis.
- **Medial — one inversion**. Empirical: C1 > C5 > C3 > C2 > C4. The framework predicted C4 < C2; the data reverses this. In medial position, the C4 column drops sharply (6.4%) — apparently the high articulatory cost matters most when the consonant is intervocalic and the acoustic environment is uniform.
- **Final — predictions break down**. Empirical: C3 (34.6%) > C1 (29.2%) > C2 (14.7%) > C5 (12.5%) > C4 (9.1%). Two major divergences: (i) C3 outranks C1 in final position (voiced consonants are *preferred* as finals over voiceless), and (ii) C2 is *more* common in final than in initial (14.7% vs 4.3%) — contrary to the "weakened aspiration cue" prediction.

**What the final-position divergence reveals**. The cost × distinguishability framework assumes the architects optimize for distinguishability of the consonant *itself*. But final consonants in Sanskrit dhātus have a third role beyond standing distinguishably: they are the **bonding sites** where dhātus combine with *pratyaya* (प्रत्यय) affixes (Chapter 13) and where words combine with following words via *sandhi* (सन्धि). The architecture of *sandhi* requires a *rich, diverse final-consonant inventory* — voiced and aspirated finals participate in specific sandhi transformations that are essential to the combinatorial chemistry. The final-position richness is the engineering term we name **combinatorial load**: the bonding chemistry needs finals across the column space, and the architecture preserves them.

The framework therefore is **cost × distinguishability × combinatorial load**. The simple two-factor model holds at initial position; the three-factor model is needed at final position.

### 5.3.4 Place of articulation × position

**Prediction**. (1) All 5 places (velar, palatal, retroflex, dental, labial) should be roughly comparably represented (~20% each) — each generates a distinctive formant signature at similar baseline cost. Slight prediction: retroflex slightly under, as the tongue-tip-curl gesture is the most articulatorily demanding place. (2) Retroflex should be depleted in initial position — Sanskrit's phonotactic tradition treats retroflex consonants as *triggered* phonemes (conditioned by preceding *r* or *ṣ*). (3) Dentals + labials should be over-represented in final position — both are clean syllable-closers. (4) Palatals should be depleted in final position — palatal closure is typologically unusual as a syllable coda.

**Data** (gaṇa 1):

| Place | Count | % | Initial | Medial | Final |
|---|---:|---:|---:|---:|---:|
| Velar | 364 | 24.5% | 54.1% | 23.9% | 22.0% |
| Palatal | 220 | 14.8% | 39.1% | 15.9% | 45.0% |
| Retroflex | 226 | 15.2% | **13.7%** | 23.5% | **62.8%** |
| Dental | 311 | 20.9% | 46.0% | 21.2% | 32.8% |
| Labial | 364 | 24.5% | 53.8% | 20.1% | 26.1% |

**Verdict — predictions split**:

- **P1 — refined**. Not uniform. Three-tier structure: top (velar 24.5%, labial 24.5%), middle (dental 20.9%), bottom (palatal 14.8%, retroflex 15.2%). The top tier comprises the universally-articulated places (back, front, middle of the mouth, in all natural-language inventories). The bottom tier comprises the articulatorily-more-demanding places (palatal tongue-blade, retroflex tongue-curl).
- **P2 — strongly confirmed**. Retroflex initial share is 13.7%, vs ~50% for velar / labial. The mirror-image finding: retroflex final share is 62.8% — nearly three times what uniform deployment would predict. The retroflex column lives in final position.
- **P3 — falsified**. Dentals + labials are *not* over-represented in final position. They sit at 32.8% and 26.1% of their own occurrences in final, both below the uniform expectation. The "clean syllable-closer" prediction does not hold.
- **P4 — falsified**. Palatals are *not* depleted in final position — they sit at 45.0% (more than initial 39.1%). Sanskrit dhātus end in palatals more often than they begin with them (*vac* वच्, *yuj* युज्, *bhuj* भुज्, *muc* मुच्, *sṛj* सृज्).

**What this reveals**. Combinatorial-load analysis again. Retroflex finals participate in the *ruki* (रुकि) rule, *visarga* (विसर्ग)-conditioning, the cerebralization of *s* → *ṣ* (स → ष), and many other Sanskrit *sandhi* (सन्धि) mechanisms. The architects deployed retroflex consonants where they can do the most combinatorial work — and that's at the final position, exposed to following-word interactions. Palatals likewise: their final-position prominence reflects the sandhi mechanisms that operate on *-j* (-ज्), *-c* (-च्), *-bhuj* (-भुज्)-style dhātu finals.

### 5.3.5 Cluster analysis

**Prediction**. Initial 2-consonant clusters should be dominated by **stop + sonorant** (sonority-rising onsets — *kr-* क्र-, *tr-* त्र-, *pr-* प्र-, *dr-* द्र-, *gr-* ग्र-, *bhr-* भ्र-, *dhr-* ध्र-, *śr-* श्र-). **S + stop clusters** (*sp-* स्प-, *st-* स्त-, *sk-* स्क-, *sm-* स्म-, *sn-* स्न-) — Sanskrit's famous exception to sonority-sequencing — should be present. Three-consonant initial clusters should be rare. Final 2-consonant clusters should be dominated by nasal + stop (*-nd* -न्द्, *-nt* -न्त्, *-mb* -म्ब्, *-mp* -म्प्) — clean closures.

**Data** (gaṇa 1):
- 22.8% of dhātus have 2-consonant initial clusters; 0.6% have 3-consonant initial clusters.
- 14.1% of dhātus have 2-consonant final clusters; 0.6% have 3-consonant final clusters.

Top initial 2-consonant clusters: **tr-** (त्र-, 5.4%), **śr-** (श्र-, 4.7%), **kṣ-** (क्ष-, 4.3%), dhr-/ṣṭ-/bhr-/gl- (ध्र-/ष्ट-/भ्र-/ग्ल-, 3.9% each), kl-/kr-/dr-/dhv- (क्ल-/क्र-/द्र-/ध्व-, 3.5% each).

Top final 2-consonant clusters: **-kṣ** (-क्ष्, 20.0% — single-cluster dominance!), -rd (-र्द्, 7.5%), -ñc (-ञ्च्, 7.5%), -rb (-र्ब्, 6.9%), -rv (-र्व्, 6.9%), -ll (-ल्ल्, 6.2%).

**Verdict — partially confirmed; one striking surprise**:
- Stop + sonorant prediction ✓ (about half the top 20 initial clusters are stop + r/l/v).
- S + stop clusters ✓ present (ṣṭ- ष्ट-, sph- स्फ-, sk- स्क-, sty- स्त्य-, śv- श्व-, śl- श्ल-).
- 3-consonant clusters rare ✓ (under 1% each end).
- **Final cluster prediction wrong**: nasal + stop is not the dominant type. The dominant type is **-kṣ** (-क्ष्), a single specific cluster, accounting for 20% of all final 2-consonant clusters (*dakṣ* दक्ष्, *lakṣ* लक्ष्, *sakṣ* सक्ष्, *rakṣ* रक्ष्, *bhakṣ* भक्ष्). Nasal + stop clusters are present (*-ñc* -ञ्च्, *-mbh* -म्भ्, *-ñj* -ञ्ज्, *-lbh* -ल्भ्) but each is a small fraction.

The -kṣ (-क्ष्) over-representation is a Sanskrit signature deserving separate study. Geminate finals (-ll -ल्ल्, -ḍḍ -ड्ड्, -kk -क्क्, -ṭṭ -ट्ट्) also appear — doubling as a structural device.

### 5.3.6 Akṣara (अक्षर)-count breakdown

**Prediction**. 1-akṣara dhātus should show purer engineering preferences than 2-akṣara dhātus — the simplest atoms should display the architecture's commitments most clearly, with 2-akṣara dhātus mixing in derived forms that flatten the distribution.

**Data**:

| Akṣaras | Dhātus | C1 | C2 | C3 | C4 | C5 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 881 (77.7%) | 37.1% | 9.2% | 25.6% | 10.9% | 17.1% |
| 2 | 243 (21.4%) | 39.0% | 9.0% | 26.0% | 11.5% | 14.6% |
| 3 | 10 (0.9%) | 26.9% | 7.7% | 26.9% | 0.0% | 38.5% |

**Verdict — falsified, in a stronger direction than expected**. The 1-akṣara and 2-akṣara cohorts show **essentially identical column distributions** — every column differs by less than 2 percentage points between the two cohorts. The 1-akṣara cohort doesn't show "purer" preferences than the 2-akṣara cohort. The engineering preferences are *not* artifacts of one cohort.

This is a stronger finding than the prediction would have been. The architecture's column preferences are **structural properties of the system, not statistical artifacts of corpus composition**. Whether the engineer builds a 1-akṣara atom (cv, cvc) or a 2-akṣara atom (cvcv, ccvcv), the same column-frequency distribution applies. This is the empirical signature of a uniform underlying engineering principle.

### 5.3.7 Vowel × consonant interaction

**Prediction**. (1) /a/ (अ, the inherent vowel) should dominate — lowest cost, default. (2) /ṛ/ (ऋ, the syllabic ṛ) should cluster with specific consonants (the classic *vṛ-* वृ-, *kṛ-* कृ- root pattern). (3) Long vowels (*ā* आ, *ī* ई, *ū* ऊ) should be over-represented in compact CV / CCV dhātus where the vowel carries the entire syllable.

**Data** (gaṇa 1, 1,397 vowel occurrences):

| Rank | IAST | Count | % |
|---:|---|---:|---:|
| 1 | a | 512 | **36.6%** |
| 2 | **ṛ** | 214 | **15.3%** |
| 3 | u | 182 | 13.0% |
| 4 | i | 119 | 8.5% |
| 5 | e | 108 | 7.7% |
| 6 | ā | 87 | 6.2% |
| 7 | ī | 61 | 4.4% |
| 8 | ū | 45 | 3.2% |
| 9–13 | ai, o, ḷ, au, ṝ | (small) | <2% each |

Top consonants preceding /ṛ/ (ऋ): *v* (व, 11.2%), *k* (क, 8.9%), *ṣ* (ष, 7.9%), *ḍ* (ड, 7.5%), *p* (प, 7.0%).

**Verdict — predictions confirmed; one striking new finding**:
- /a/ (अ) dominance ✓ (36.6%).
- /ṛ/ (ऋ) pairs with specific consonants ✓ (*vṛ* वृ, *kṛ* कृ, *ṣṛ* षृ, *ḍṛ* डृ, *pṛ* पृ patterns).
- Long vowels collectively ~14% of all vowels; short vowels ~75%. The compression principle holds at the vowel level too.

**The headline new finding**: ***ṛ* (ऋ) is the second-most-common vowel in the *Dhātupāṭha* at 15.3%**. This is cross-linguistically extraordinary. The syllabic ṛ (ऋ) is a typologically rare phoneme (a syllabic-consonant vowel — most languages don't have one at all, and where it exists it's typically marginal). In Sanskrit, the architects placed ṛ as a *load-bearing vowel of the foundational atomic inventory*, used in 214 distinct primary-class dhātus: *kṛ* (कृ), *vṛ* (वृ), *dṛś* (दृश्), *mṛ* (मृ), *hṛ* (हृ), *tṛp* (तृप्), *vṛt* (वृत्), *kṛp* (कृप्), *mṛj* (मृज्), *sṛj* (सृज्), *dṛp* (दृप्), ... These dhātus generate massive vocabulary (*karma* कर्म, *manas* मनस्, *mṛtyu* मृत्यु, *mokṣa* मोक्ष, *sṛṣṭi* सृष्टि, *vṛddhi* वृद्धि, *kṛti* कृति, *prakṛti* प्रकृति, *vikṛti* विकृति, hundreds more). The architects engineered ṛ deliberately into the system because of its acoustic distinctiveness and its position in the engineering space.

### 5.3.8 Onset-coda OCP analysis (single-syllable dhātus)

**Prediction**. For single-syllable (1-akṣara) dhātus with both initial and final varga consonants, two patterns may emerge: **place harmony** (initial and final share place — *kak* कक्-style), **voicing harmony** (initial and final share voicing — *gam* गम्, *jin* जिन्-style), or **avoidance** of either. No strong directional prediction made.

**Data** (gaṇa 1, 271 single-syllable dhātus with both initial and final varga consonants):

- **Place harmony — observed 10.3%, expected 27.7%** (under independence) → **STRONG AVOIDANCE**. Only 28 out of 271 dhātus have same-place initial and final, when independence would predict ~75. This is the strongest single empirical signal in the entire analysis: ~62% below chance.
- **Voicing harmony — observed 55.7%, expected 49.4%** → modest HARMONY (~13% above chance).

**The OCP signature**. Sanskrit dhātus *avoid* having the same place of articulation flanking the vowel. The Obligatory Contour Principle (OCP) operates as a design constraint. A dhātu like *kak* (कक्) or *pap* (पप्) is suppressed; dhātus like *kap* (कप्), *gat* (गत्), *pun* (पुन्) are preferred. The architects engineered place-variation into the CVC structure for maximum acoustic distinctiveness across the syllable. This is a substantial new engineering principle that operates *across* the syllable, not within a single consonant slot.

Voicing harmony is the milder secondary effect — easier to maintain a voicing state across the syllable than to switch.

### 5.3.9 Cross-gaṇa (गण) column distribution

**Prediction**. The column distribution discovered in gaṇa 1 (the primary class) should hold across all 10 *gaṇāḥ* (गणाः), with minor variation in absolute proportions due to derivation-class differences. The C1-first pattern should be robust.

**Data** (all 10 gaṇas):

| Gaṇa | Class | Dhātus | C1 | C2 | C3 | C4 | C5 |
|---:|:---:|---:|---:|---:|---:|---:|---:|
| 1 | *bhvādi* (भ्वादि) | 1,134 | 37.4% | 9.2% | 25.7% | 10.8% | 16.9% |
| 2 | *adādi* (अदादि) | 76 | 37.3% | 1.5% | 35.8% | 3.0% | 22.4% |
| **3** | ***juhotyādi*** (**जुहोत्यादि**) | **25** | **22.7%** | **0.0%** | **22.7%** | **31.8%** | **22.7%** |
| 4 | *divādi* (दिवादि) | 151 | 36.5% | 2.4% | 22.2% | 15.6% | 23.4% |
| 5 | *svādi* (स्वादि) | 39 | 43.6% | 0.0% | 17.9% | 25.6% | 12.8% |
| 6 | *tudādi* (तुदादि) | 171 | 38.4% | 10.3% | 26.4% | 8.7% | 16.1% |
| 7 | *rudhādi* (रुधादि) | 25 | 35.0% | 2.5% | 35.0% | 12.5% | 15.0% |
| 8 | *tanādi* (तनादि) | 10 | 31.2% | 0.0% | 0.0% | 6.2% | 62.5% |
| 9 | *kryādi* (क्र्यादि) | 69 | 30.0% | 10.0% | 15.0% | 18.8% | 26.2% |
| 10 | *curādi* (चुरादि) | 468 | 47.3% | 6.0% | 24.6% | 6.9% | 15.0% |

**Verdict — robust with one substantive outlier**:
- C1-first holds in 8 of 10 gaṇas (1, 2, 4, 5, 6, 7, 9, 10).
- **Gaṇa 8 (*tanādi* तनादि, n=10)** — too small to read confidently; the C5 spike (62.5%) reflects the nasal-heavy composition of this small class.
- **Gaṇa 3 (*juhotyādi* जुहोत्यादि) — the substantive outlier**: ***C4 leads at 31.8%***. This is the reduplicating class — dhātus like *hu* (हु), *dā* (दा), *dhā* (धा), *mā* (मा) that reduplicate in present-tense formation (*juhoti* जुहोति, *dadāti* ददाति, *dadhāti* दधाति, *mimīte* मिमीते). The C4 enrichment is striking.

**Why the *juhotyādi* (जुहोत्यादि) C4 enrichment makes engineering sense**. Reduplication is itself a redundancy mechanism — the dhātu's initial consonant doubles to form the present-tense stem. For the doubled consonant to remain identifiable across the syllable boundary, the consonant must be **acoustically robust**. C4 (voiced-aspirated, breathy-voiced) is the column with the *most distinctive acoustic signature* — the same property that made C4 less-suppressed than C2 in §5.3.2. The architects engineered the most-distinguishable column into the class where its acoustic robustness pays the most. This is **functional matching**: the column that pays most in distinguishability is deployed in the structural context that needs that distinguishability most.

### 5.3.10 Feature-distance distinguishability — quantitative test

**Prediction**. If the cost × distinguishability framework holds quantitatively, then for each varga consonant: **frequency in the corpus should track engineering-value** (distinguishability divided by cost). A formal test: define feature vectors per consonant, compute mean weighted feature-distance to all other varga consonants (asymmetric-aspiration weighting per §5.3.2), compute cost, compute engineering-value, then measure rank correlation with corpus frequency.

**Implementation**. Each of the 25 varga consonants is assigned (place, voicing, aspiration, nasality). Weighted feature-distance uses: place 1.0; voicing 1.5; aspiration 0.5 (voiceless transition) or 1.5 (voiced transition); nasal 1.5. Cost = sum of marked features the consonant carries. Engineering-value = mean_weighted_distance / (1 + cost).

**Data** (Spearman rank correlations against frequency in gaṇa 1):

| Metric | ρ |
|---|---:|
| **Engineering value** (distinguishability / (1+cost)) | **+0.304** |
| Mean weighted distance (distinguishability alone) | −0.465 |
| Mean binary Hamming distance | −0.339 |
| Cost (raw) | −0.401 |

**Verdict — moderately confirmed, with a clear limitation**.
- Engineering value is the strongest positive predictor at ρ = +0.304.
- Pure distinguishability is *negatively* correlated with frequency because cost dominates — high-distinguishability consonants (nasals, voiced-aspirated) are also high-cost, and the cost penalty overwhelms the distinguishability bonus.
- The combined metric captures the trade-off correctly.

**The limitation**: ρ = +0.304 means roughly 9% of variance in frequency is explained by engineering-value. The remaining 91% is unexplained by this two-factor model. Looking at the per-cell data shows why: **specific (place × column) cells are deployed at wildly different rates** that the simple model cannot capture.

Examples within the C1 row (engineering value 2.40, all tied at the top):
- ***k*** (क, velar): 197 occurrences
- ***p*** (प, labial): 101
- ***c*** (च, palatal): 98
- ***t*** (त, dental): 83
- ***ṭ*** (ट, retroflex): 76

Same engineering value, frequencies span 197 → 76. Within the C5 row (nasals, engineering value 1.29):
- ***m*** (म, labial): 131
- ***ṇ*** (ण, retroflex): 58
- ***n*** (न, dental): 38
- ***ñ*** (ञ, palatal): 22
- ***ṅ*** (ङ, velar): **2**

*m* vs *ṅ* (म vs ङ) — a 65× difference at identical engineering-value in the two-factor model. **The architecture's cell-level preferences are real and substantial — not statistical noise.** Some cells (labial *m* म, velar *k* क, dental *d* द, dental *dh* ध, labial *bh* भ, dental *t* त, palatal *c* च) are heavily populated; others (velar *ṅ* ङ, palatal *ch* छ, retroflex *ḍh* ढ, palatal *jh* झ) are nearly empty.

The engineering, at its deepest level, deploys specific consonants at specific cells with specific frequencies — not a uniform "favor cheap + distinguishable" rule, but a *cell-by-cell engineering allocation*. The quantitative model captures the column-level direction; cell-level allocation requires additional engineering terms.

### 5.3.11 Productivity — simplest atoms generate the most

**Prediction**. If the compression principle governs the architecture, the simplest *dhātus* (CV pattern, 2 particles) should also be the *most productive* — generating the largest derivative vocabularies. The architects engineered minimum atoms because minimum atoms support maximum combinatorial reach. The corollary: the most-complex *dhātus* (CCVCC, 5 particles) should sit at the bottom of the productivity distribution. Predicted Spearman ρ between productivity and particle-count: **strongly negative**.

**Data** (curated sample of 138 *dhātus* spanning the *Dhātupāṭha*'s structural pattern space; productivity = estimated count of primary derivatives per *dhātu*, drawn from the Monier-Williams Sanskrit-English Dictionary (1899) and V. S. Apte's *Practical Sanskrit-English Dictionary* (1890); approximate ±20%, ranking is load-bearing not precise count):

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

Pattern composition of the productivity extremes:

| Pattern | Top 20 | Bottom 20 |
|---|---:|---:|
| CV | **11** | 1 |
| CVC | 7 | 3 |
| CCV | 1 | 3 |
| CCVC | 0 | 6 |
| CCVCC | 0 | 2 |
| CVCC | 0 | 2 |
| VCC | 0 | 2 |

Mean particle count, top 20 by productivity: **2.40**. Mean particle count, bottom 20: **3.50**. Bottom-to-top ratio: 1.46×.

**Verdict — strongly confirmed**. Productivity is strongly negatively correlated with particle count (ρ = −0.485). The CV pattern's mean productivity (32.6) is **2.9× higher** than the CCVCC pattern's (11.4). The top 20 productivity ranks are dominated by 2-particle CV *dhātus* (11 of 20); the bottom 20 by 4-5-particle CCVC / CCVCC / CVCC patterns (10 of 20). *Kṛ* (कृ) alone — two particles — anchors 75+ primary derivatives, more than the entire CCVCC sample combined.

**The architectural signature**. *Minimum-particle atoms support maximum combinatorial reach*. The architects did not build small atoms because small atoms were easier to inventory; they built small atoms *because small atoms generate the most vocabulary downstream*. The compression principle operates not only at the inventory-composition level (§§5.3.1–5.3.10) but at the *generative-output* level: the simplest atoms do the most semantic work.

**The natural-language inversion**.[NOTE: productivity-inversion-natural-language] In natural languages (English, Latin, Greek), the most-frequent forms tend toward *idiosyncratic irregularity* — English *be / have / do* are paradigmatically broken; Latin *esse / ire / ferre* are suppletive. The frequency-irregularity correlation is one of the most-replicated typological findings in natural-language morphology. In Sanskrit's engineered case, the correlation runs the opposite way: the highest-productivity *dhātus* are *also* the most structurally minimal *and* paradigmatically regular. There is no idiosyncrasy at the top. The engineering pays dividends across the productivity axis and the regularity axis simultaneously — a signature natural-language drift does not produce.

The reproducibility bundle's `data/dhatu_productivity.csv` lists the full 138-*dhātu* sample with derivative-count estimates and source citations; the analysis script `scripts/analyze_productivity.py` reproduces every figure in this section.

---

## 5.4 Synthesis — six engineering principles

The cumulative empirical work reveals the architecture operating at six levels:

1. **Cost × distinguishability** (per-consonant). Articulatory cost matters; perceptual distinguishability matters; the architects balance them. C1 dominates because it is cheap and clear; C4 survives because it earns its cost through distinguishability; C2 is under-deployed because it pays cost for negligible distinctiveness gain. Spearman ρ = +0.304 — moderate predictor.

2. **Cell-level allocation** (per place × column). Specific (place, column) cells are deployed at wildly different rates the two-factor model cannot capture. Labial *m* (म), dental *d* (द), labial *bh* (भ), velar *k* (क) are heavily populated; velar *ṅ* (ङ), palatal *ch* (छ), retroflex *ḍh* (ढ) are essentially empty. The architecture has cell-by-cell engineering preferences.

3. **Position-conditional preferences** (per position × column / place). Each column and each place has a position-specific signature. Retroflex consonants strongly prefer final position (62.8%); palatals favor final (45%); velars and labials favor initial; nasals are more initial than final (contrary to typological expectation). The architecture engineers specific consonants into specific functional niches.

4. **Cross-position OCP** (per *dhātu* धातु). The Obligatory Contour Principle — place-of-articulation avoidance across the syllable — operates as a 62%-below-chance suppression of same-place initial/final flanking. The architecture enforces place-diversity across the CVC structure for acoustic distinctiveness.

5. **Gaṇa (गण)-specific functional matching** (per derivational class). The *juhotyādi* (जुहोत्यादि) reduplicating class enriches C4 (the most acoustically robust column) because reduplication needs acoustic robustness. The architecture matches the most-distinguishable column to the structural context that needs distinguishability most.

6. **Productivity-from-minimum** (per *dhātu* productivity-axis). The simplest *dhātus* (2-particle CV) are the most-productive atoms in the language; the most-complex *dhātus* (5-particle CCVCC) sit at the bottom of the productivity distribution. ρ = −0.485 between productivity and particle count. The CV pattern's mean productivity is 2.9× the CCVCC pattern's. The architects engineered minimum atoms *because minimum atoms support maximum combinatorial reach* — and unlike in natural languages, the high-frequency forms in Sanskrit are *also* paradigmatically regular, not idiosyncratic.

These six principles operate simultaneously and reinforce each other. None is visible to a single-axis analysis. The architecture's depth lies in the *stack*: cost-aware, distinguishability-aware, cell-aware, position-aware, *dhātu*-aware, gaṇa-aware, and productivity-aware engineering all running together.

The compression principle stated at the chapter opening is the *governing principle*: nature and engineered systems favor compact, low-energy configurations. What the appendix shows is that the Sanskrit architecture's "compactness" is itself multi-scale. Compactness is enforced at every level — particle count, column choice, place choice, cell choice, position deployment, cross-position relations, *and the generative output that the compact atoms produce*. The architects engineered a *system of compactness*, not a single compactness rule.

---

## 5.5 Replication

The reproducibility bundle accompanying this appendix is at the repo path `analysis/dhatupatha/`. It contains:

- **`data/dhatupatha.csv`** — source data (2,168 entries) from the open-source `sanskrit/vyakarana` GitHub project. Three columns: *gaṇa* (गण)-number, position-within-*gaṇa*, *dhātu* (धातु) in SLP1 transliteration.
- **`data/derived/dhatupatha_decomposed.md`** — every *dhātu* rendered in standard Devanāgarī with *varṇa* (वर्ण)-level decomposition. Generated by `decompose_dhatupatha.py`.
- **`scripts/analyze_dhatupatha.py`** — structural classification, particle count, *akṣara* (अक्षर) count, pattern, *gaṇa* distribution. Generates the §5.3.1 figures.
- **`scripts/decompose_dhatupatha.py`** — SLP1 → Devanāgarī conversion + *varṇa*-level decomposition.
- **`scripts/analyze_varga_distribution.py [gaṇa]`** — column × position analysis. Generates §5.3.2 and §5.3.3 figures.
- **`scripts/analyze_place_distribution.py [gaṇa]`** — place × position analysis. Generates §5.3.4 figures.
- **`scripts/analyze_extensions.py [gaṇa]`** — cluster analysis, *akṣara*-count breakdown, vowel × consonant. Generates §5.3.5, §5.3.6, §5.3.7 figures.
- **`scripts/analyze_distinguishability.py`** — feature-distance scoring, onset-coda OCP analysis, cross-*gaṇa* column distribution. Generates §5.3.8, §5.3.9, §5.3.10 figures.
- **`scripts/analyze_productivity.py`** — productivity (estimated primary-derivative count from MW 1899 and Apte 1890) correlated against structural complexity. Generates §5.3.11 figures.
- **`data/dhatu_productivity.csv`** — curated productivity sample (138 *dhātus*) with derivative-count estimates and source attribution.

Requirements: Python 3.10+. No external dependencies — the scripts use only the standard library. From the bundle root: `python3 scripts/<script-name>.py [gaṇa]` (where `[gaṇa]` is an optional numerical filter from 1 to 10).

The bundle is self-contained and includes a README with full attribution, methodology notes, and a license file. Every empirical claim in Chapter 11 and in this appendix can be verified by re-running the scripts against the source CSV.

---

*End of Appendix Part 5.*
