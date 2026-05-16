# Appendix Part 5 — The Architecture by the Numbers

*The full empirical work behind Chapter 11. Predictions stated in engineering-method order, tested against the 2,168-entry Pāṇinian* Dhātupāṭha *with* anubandhas *stripped per* Aṣṭādhyāyī *1.3.2, 1.3.3, 1.3.5; verdicts on each prediction including the falsifications. The chapter prose carries the load-bearing findings; this appendix carries the full work so any reader can verify every claim. A reproducibility bundle accompanies the book at* `dhatupatha-analysis/` *with the source CSV, the derived Devanāgarī decomposition, and the Python scripts that produce every figure cited here.*

---

## 5.1 Introduction

Chapter 11 makes a structural claim: Sanskrit's *Dhātupāṭha* is an engineered atomic inventory whose composition follows engineering principles that can be predicted in advance and tested against the corpus. The chapter states the principles (compression, cost-versus-distinguishability, the Atomic Corollary) and cites the empirical headlines that confirm them. This appendix supplies the full demonstration.

The work proceeds in engineering-method order. For each empirical question, a prediction is stated *before* the data is consulted — what the engineering framework expects to see in the *Dhātupāṭha*. The data is then computed. The verdict on each prediction — confirmed, refined, falsified — is named in the open. Where predictions fail, the appendix names the deeper principle the failure reveals. The architecture's signature is the *pattern of confirmations and falsifications*, not any single result.

Eleven specific analyses follow, each producing its own prediction → data → verdict cycle. They cumulate into a five-principle synthesis: cost × distinguishability, place-specific deployment, position-conditional preferences, cross-position phonotactic constraints (the OCP / place-avoidance principle), and gaṇa-specific functional matching. None of these principles is visible to a feature-counting model alone; the architecture's depth requires all five.

---

## 5.2 Source data and methodology

**The source data.** The digital *Dhātupāṭha* is the `data/dhatupatha.csv` file from the open-source `sanskrit/vyakarana` project on GitHub. The CSV has three columns — *gaṇa-number*, *position-within-gaṇa*, and the *dhātu in SLP1 transliteration with Pāṇinian accent markers* (~, \\, ^). The corpus is 2,168 entries across the ten *gaṇāḥ*. This count sits within the conventional Pāṇinian range (~1,940 to ~2,200 depending on recension); the *Mādhavīya Dhātuvṛtti*, the *Siddhāntakaumudī*, and the *Kṣīrasvāmin* commentary yield comparable totals with minor recensional variation in marginal entries. The full reproducibility bundle is at the repo subdirectory `dhatupatha-analysis/`.

**The anubandha-stripping methodology.** Each Pāṇinian dhātu citation form contains *anubandha* markers — phonemes present in the citation that are not part of the underlying root, used to signal grammatical properties the *Aṣṭādhyāyī*'s rules will use downstream. The *it-saṃjñā* rules (*Aṣṭādhyāyī* 1.3.2–1.3.9) specify which phonemes in citation forms are *anubandhas*. Three of these rules apply to dhātus and are implemented in every analysis script:

- **1.3.2 — *upadeśe 'janunāsika it***: a final *anunāsika*-marked short vowel is an *anubandha*. In the standard Pāṇinian-citation tradition, trailing short *-a* / *-i* / *-u* after a consonant carries this status. The implementation strips such trailing short vowels *only when at least one other vowel remains* — preserving genuine CV-pattern roots like *ji* (to conquer), *hu* (to sacrifice), *sru* (to flow), where the short vowel *is* the root vowel.

- **1.3.3 — *halantyam***: a trailing single-consonant *anubandha* (the *ñit*, *ṅit*, *lit*, *ṣit*, *ṭit*, *ḍit* markers signaling ātmanepadī conjugation or other grammatical properties) is stripped when it sits immediately after a vowel. The canonical case is the *kṛ* dhātu, cited as *ḍukṛñ* (SLP1: `qukf\Y`); after the initial *ḍu* is stripped by 1.3.5 and the trailing *ñ* by 1.3.3, the underlying root *kṛ* is recovered.

- **1.3.5 — *ādir ñiṭuḍavaḥ***: the initial two-character sequences *ñi* (SLP1: `Ji`), *ṭu* (`wu`), *ḍu* (`qu`) in dhātu citation forms are *anubandhas* and are stripped from the front.

Accent markers (~, \\, ^) are stripped before structural classification — they encode the Pāṇinian *udātta* / *anudātta* / *svarita* recitational distinctions, not structural phonological content. Cross-validation against the Sanskrit Heritage Platform's `parts.csv` confirms that this rule-set recovers the standard underlying roots for the vast majority of *Dhātupāṭha* entries.

A small residue of edge cases (~0.3% of the corpus) classifies as bare-vowel V-patterns after stripping — special-case Pāṇinian-citation forms such as *i* (इ, to go) and *ṛ* (ऋ, to go). These are correctly retained as 1-akṣara dhātus.

---

## 5.3 The analyses

### 5.3.1 Particle-count distribution — the thermodynamic threshold

**Prediction**. An engineered atomic inventory should display: (1) a peak near the minimum particle count compatible with semantic distinction (3–4 particles, the sweet spot — pronounceable in a single beat yet acoustically distinguishable); (2) a sharp falloff beyond the single-akṣara articulatory threshold (around 5 particles per syllable); (3) single-akṣara dominance — the majority of *dhātavaḥ* should occupy exactly one akṣara.

**Data** (across all 2,168 dhātus):

| Particles | Count | % | Common patterns | Examples |
|---|---:|---:|---|---|
| 2 (minimum) | 236 | 10.9% | CV, VC | *kṛ, bhū, dā, jñā, pā, ji, hu, ad* |
| 3 (modal) | 1,051 | 48.5% | CVC, CCV, VCV | *gam, pat, vac, yam, labh, sthā* |
| 4 | 676 | 31.2% | CCVC, CVCC, CVCV | *svap, kalp, jval, bandh, granth* |
| 5 (threshold) | 156 | 7.2% | CCVCC, CVCVC, CCVCV | *spand, skand* |
| 6+ (cliff) | 42 | 1.9% | — | — |

Akṣara count: 1 akṣara 82.8%, 2 akṣara 16.1%, 3+ akṣara 1.2%.

**Verdict — all three predictions confirmed.** Peak at 3 particles (48.5%) with mass at 4 (31.2%); cliff at 6+ (1.9%); single-akṣara dominance at 82.8%.

### 5.3.2 Varga column distribution — cost × distinguishability

**Prediction**. The compression principle, applied at the column level, predicts an articulatory-simplicity gradient. C1 (unvoiced unaspirated — k, c, ṭ, t, p) is the cheapest column to produce and should dominate. C4 (voiced aspirated — gh, jh, ḍh, dh, bh) is the most articulatorily expensive and should be the rarest. The order: C1 > C2 ≈ C3 > C4. C5 (nasal) sits in a separate articulatory category.

**Data** (gaṇa 1, the primary class — 1,485 varga-consonant occurrences):

| Column | Count | % |
|---|---:|---:|
| C1 (unv-unasp — k, c, ṭ, t, p) | 555 | **37.4%** |
| C2 (unv-asp — kh, ch, ṭh, th, ph) | 136 | **9.2%** |
| C3 (voi-unasp — g, j, ḍ, d, b) | 382 | 25.7% |
| C4 (voi-asp — gh, jh, ḍh, dh, bh) | 161 | **10.8%** |
| C5 (nasal — ṅ, ñ, ṇ, n, m) | 251 | 16.9% |

**Verdict — partially confirmed; one substantive refinement.** C1 dominance ✓ at 37.4% — confirmed. But the rarest column is **C2 (9.2%), not C4 (10.8%)**. The cost-naïve prediction expected C4 (which carries the highest articulatory cost — voicing + aspiration) to be the most suppressed, but the data places C2 below C4 by 1.6 percentage points.

**Why the refinement holds**. The naïve cost model treats aspiration as a symmetric feature: adding aspiration to k yields kh; adding it to g yields gh; same cost both directions. Empirical perceptual phonetics says otherwise. Aspiration on a voiceless stop (k → kh) is a *small* perceptual change — a longer puff of breath after release, easily missed in noisy listening conditions. Aspiration on a voiced stop (g → gh) is a *large* perceptual change — the breathy-voice / *mahāprāṇa-ghoṣavat* signature is highly salient, with murmured-breath voicing during and after closure. C4 earns its place: it pays the cost but gains substantial distinguishability. C2 pays cost for negligible distinguishability gain — and the architects accordingly under-deploy it.

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

**What the final-position divergence reveals**. The cost × distinguishability framework assumes the architects optimize for distinguishability of the consonant *itself*. But final consonants in Sanskrit dhātus have a third role beyond standing distinguishably: they are the **bonding sites** where dhātus combine with *pratyaya* affixes (Chapter 13) and where words combine with following words via *sandhi*. The architecture of *sandhi* requires a *rich, diverse final-consonant inventory* — voiced and aspirated finals participate in specific sandhi transformations that are essential to the combinatorial chemistry. The final-position richness is the engineering term we name **combinatorial load**: the bonding chemistry needs finals across the column space, and the architecture preserves them.

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
- **P4 — falsified**. Palatals are *not* depleted in final position — they sit at 45.0% (more than initial 39.1%). Sanskrit dhātus end in palatals more often than they begin with them (*vac, yuj, bhuj, muc, sṛj*).

**What this reveals**. Combinatorial-load analysis again. Retroflex finals participate in the *ruki* rule, *visarga*-conditioning, the cerebralization of *s* → *ṣ*, and many other Sanskrit sandhi mechanisms. The architects deployed retroflex consonants where they can do the most combinatorial work — and that's at the final position, exposed to following-word interactions. Palatals likewise: their final-position prominence reflects the sandhi mechanisms that operate on *-j, -c, -bhuj*-style dhātu finals.

### 5.3.5 Cluster analysis

**Prediction**. Initial 2-consonant clusters should be dominated by **stop + sonorant** (sonority-rising onsets — *kr-, tr-, pr-, dr-, gr-, bhr-, dhr-, śr-*). **S + stop clusters** (*sp-, st-, sk-, sm-, sn-*) — Sanskrit's famous exception to sonority-sequencing — should be present. Three-consonant initial clusters should be rare. Final 2-consonant clusters should be dominated by nasal + stop (*-nd, -nt, -mb, -mp*) — clean closures.

**Data** (gaṇa 1):
- 22.8% of dhātus have 2-consonant initial clusters; 0.6% have 3-consonant initial clusters.
- 14.1% of dhātus have 2-consonant final clusters; 0.6% have 3-consonant final clusters.

Top initial 2-consonant clusters: **tr-** (5.4%), **śr-** (4.7%), **kṣ-** (4.3%), dhr-/ṣṭ-/bhr-/gl- (3.9% each), kl-/kr-/dr-/dhv- (3.5% each).

Top final 2-consonant clusters: **-kṣ** (20.0% — single-cluster dominance!), -rd (7.5%), -ñc (7.5%), -rb (6.9%), -rv (6.9%), -ll (6.2%).

**Verdict — partially confirmed; one striking surprise**:
- Stop + sonorant prediction ✓ (about half the top 20 initial clusters are stop + r/l/v).
- S + stop clusters ✓ present (ṣṭ-, sph-, sk-, sty-, śv-, śl-).
- 3-consonant clusters rare ✓ (under 1% each end).
- **Final cluster prediction wrong**: nasal + stop is not the dominant type. The dominant type is **-kṣ**, a single specific cluster, accounting for 20% of all final 2-consonant clusters (*dakṣ, lakṣ, sakṣ, rakṣ, bhakṣ*). Nasal + stop clusters are present (*-ñc, -mbh, -ñj, -lbh*) but each is a small fraction.

The -kṣ over-representation is a Sanskrit signature deserving separate study. Geminate finals (-ll, -ḍḍ, -kk, -ṭṭ) also appear — doubling as a structural device.

### 5.3.6 Akṣara-count breakdown

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

**Prediction**. (1) /a/ (the inherent vowel) should dominate — lowest cost, default. (2) /ṛ/ (the syllabic ṛ) should cluster with specific consonants (the classic *vṛ-, kṛ-* root pattern). (3) Long vowels (ā, ī, ū) should be over-represented in compact CV / CCV dhātus where the vowel carries the entire syllable.

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

Top consonants preceding /ṛ/: v (11.2%), k (8.9%), ṣ (7.9%), ḍ (7.5%), p (7.0%).

**Verdict — predictions confirmed; one striking new finding**:
- /a/ dominance ✓ (36.6%).
- /ṛ/ pairs with specific consonants ✓ (*vṛ, kṛ, ṣṛ, ḍṛ, pṛ* patterns).
- Long vowels collectively ~14% of all vowels; short vowels ~75%. The compression principle holds at the vowel level too.

**The headline new finding**: ***ṛ* is the second-most-common vowel in the *Dhātupāṭha* at 15.3%**. This is cross-linguistically extraordinary. The syllabic ṛ is a typologically rare phoneme (a syllabic-consonant vowel — most languages don't have one at all, and where it exists it's typically marginal). In Sanskrit, the architects placed ṛ as a *load-bearing vowel of the foundational atomic inventory*, used in 214 distinct primary-class dhātus: *kṛ, vṛ, dṛś, mṛ, hṛ, tṛp, vṛt, kṛp, mṛj, sṛj, dṛp, ...* These dhātus generate massive vocabulary (*karma, manas, mṛtyu, mokṣa, sṛṣṭi, vṛddhi, kṛti, prakṛti, vikṛti*, hundreds more). The architects engineered ṛ deliberately into the system because of its acoustic distinctiveness and its position in the engineering space.

### 5.3.8 Onset-coda OCP analysis (single-syllable dhātus)

**Prediction**. For single-syllable (1-akṣara) dhātus with both initial and final varga consonants, two patterns may emerge: **place harmony** (initial and final share place — *kak*-style), **voicing harmony** (initial and final share voicing — *gam, jin*-style), or **avoidance** of either. No strong directional prediction made.

**Data** (gaṇa 1, 271 single-syllable dhātus with both initial and final varga consonants):

- **Place harmony — observed 10.3%, expected 27.7%** (under independence) → **STRONG AVOIDANCE**. Only 28 out of 271 dhātus have same-place initial and final, when independence would predict ~75. This is the strongest single empirical signal in the entire analysis: ~62% below chance.
- **Voicing harmony — observed 55.7%, expected 49.4%** → modest HARMONY (~13% above chance).

**The OCP signature**. Sanskrit dhātus *avoid* having the same place of articulation flanking the vowel. The Obligatory Contour Principle (OCP) operates as a design constraint. A dhātu like *kak* or *pap* is suppressed; dhātus like *kap, gat, pun* are preferred. The architects engineered place-variation into the CVC structure for maximum acoustic distinctiveness across the syllable. This is a substantial new engineering principle that operates *across* the syllable, not within a single consonant slot.

Voicing harmony is the milder secondary effect — easier to maintain a voicing state across the syllable than to switch.

### 5.3.9 Cross-gaṇa column distribution

**Prediction**. The column distribution discovered in gaṇa 1 (the primary class) should hold across all 10 *gaṇāḥ*, with minor variation in absolute proportions due to derivation-class differences. The C1-first pattern should be robust.

**Data** (all 10 gaṇas):

| Gaṇa | Class | Dhātus | C1 | C2 | C3 | C4 | C5 |
|---:|:---:|---:|---:|---:|---:|---:|---:|
| 1 | bhvādi | 1,134 | 37.4% | 9.2% | 25.7% | 10.8% | 16.9% |
| 2 | adādi | 76 | 37.3% | 1.5% | 35.8% | 3.0% | 22.4% |
| **3** | **juhotyādi** | **25** | **22.7%** | **0.0%** | **22.7%** | **31.8%** | **22.7%** |
| 4 | divādi | 151 | 36.5% | 2.4% | 22.2% | 15.6% | 23.4% |
| 5 | svādi | 39 | 43.6% | 0.0% | 17.9% | 25.6% | 12.8% |
| 6 | tudādi | 171 | 38.4% | 10.3% | 26.4% | 8.7% | 16.1% |
| 7 | rudhādi | 25 | 35.0% | 2.5% | 35.0% | 12.5% | 15.0% |
| 8 | tanādi | 10 | 31.2% | 0.0% | 0.0% | 6.2% | 62.5% |
| 9 | kryādi | 69 | 30.0% | 10.0% | 15.0% | 18.8% | 26.2% |
| 10 | curādi | 468 | 47.3% | 6.0% | 24.6% | 6.9% | 15.0% |

**Verdict — robust with one substantive outlier**:
- C1-first holds in 8 of 10 gaṇas (1, 2, 4, 5, 6, 7, 9, 10).
- **Gaṇa 8 (tanādi, n=10)** — too small to read confidently; the C5 spike (62.5%) reflects the nasal-heavy composition of this small class.
- **Gaṇa 3 (juhotyādi) — the substantive outlier**: ***C4 leads at 31.8%***. This is the reduplicating class — dhātus like *hu, dā, dhā, mā* that reduplicate in present-tense formation (*juhoti, dadāti, dadhāti, mimīte*). The C4 enrichment is striking.

**Why the *juhotyādi* C4 enrichment makes engineering sense**. Reduplication is itself a redundancy mechanism — the dhātu's initial consonant doubles to form the present-tense stem. For the doubled consonant to remain identifiable across the syllable boundary, the consonant must be **acoustically robust**. C4 (voiced-aspirated, breathy-voiced) is the column with the *most distinctive acoustic signature* — the same property that made C4 less-suppressed than C2 in §5.3.2. The architects engineered the most-distinguishable column into the class where its acoustic robustness pays the most. This is **functional matching**: the column that pays most in distinguishability is deployed in the structural context that needs that distinguishability most.

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
- **k** (velar): 197 occurrences
- **p** (labial): 101
- **c** (palatal): 98
- **t** (dental): 83
- **ṭ** (retroflex): 76

Same engineering value, frequencies span 197 → 76. Within the C5 row (nasals, engineering value 1.29):
- **m** (labial): 131
- **ṇ** (retroflex): 58
- **n** (dental): 38
- **ñ** (palatal): 22
- **ṅ** (velar): **2**

m vs ṅ — a 65× difference at identical engineering-value in the two-factor model. **The architecture's cell-level preferences are real and substantial — not statistical noise.** Some cells (labial m, velar k, dental d, dental dh, labial bh, dental t, palatal c) are heavily populated; others (velar ṅ, palatal ch, retroflex ḍh, palatal jh) are nearly empty.

The engineering, at its deepest level, deploys specific consonants at specific cells with specific frequencies — not a uniform "favor cheap + distinguishable" rule, but a *cell-by-cell engineering allocation*. The quantitative model captures the column-level direction; cell-level allocation requires additional engineering terms.

---

## 5.4 Synthesis — five engineering principles

The cumulative empirical work reveals the architecture operating at five levels:

1. **Cost × distinguishability** (per-consonant). Articulatory cost matters; perceptual distinguishability matters; the architects balance them. C1 dominates because it is cheap and clear; C4 survives because it earns its cost through distinguishability; C2 is under-deployed because it pays cost for negligible distinctiveness gain. Spearman ρ = +0.304 — moderate predictor.

2. **Cell-level allocation** (per place × column). Specific (place, column) cells are deployed at wildly different rates the two-factor model cannot capture. Labial m, dental d, labial bh, velar k are heavily populated; velar ṅ, palatal ch, retroflex ḍh are essentially empty. The architecture has cell-by-cell engineering preferences.

3. **Position-conditional preferences** (per position × column / place). Each column and each place has a position-specific signature. Retroflex consonants strongly prefer final position (62.8%); palatals favor final (45%); velars and labials favor initial; nasals are more initial than final (contrary to typological expectation). The architecture engineers specific consonants into specific functional niches.

4. **Cross-position OCP** (per dhātu). The Obligatory Contour Principle — place-of-articulation avoidance across the syllable — operates as a 62%-below-chance suppression of same-place initial/final flanking. The architecture enforces place-diversity across the CVC structure for acoustic distinctiveness.

5. **Gaṇa-specific functional matching** (per derivational class). The *juhotyādi* reduplicating class enriches C4 (the most acoustically robust column) because reduplication needs acoustic robustness. The architecture matches the most-distinguishable column to the structural context that needs distinguishability most.

These five principles operate simultaneously and reinforce each other. None is visible to a single-axis analysis. The architecture's depth lies in the *stack*: cost-aware, distinguishability-aware, cell-aware, position-aware, dhātu-aware, and gaṇa-aware engineering all running together.

The compression principle stated at the chapter opening is the *governing principle*: nature and engineered systems favor compact, low-energy configurations. What the appendix shows is that the Sanskrit architecture's "compactness" is itself multi-scale. Compactness is enforced at every level — particle count, column choice, place choice, cell choice, position deployment, and cross-position relations — each adding to the others. The architects engineered a *system of compactness*, not a single compactness rule.

---

## 5.5 Replication

The reproducibility bundle accompanying this appendix is at the repo path `dhatupatha-analysis/`. It contains:

- **`data/dhatupatha.csv`** — source data (2,168 entries) from the open-source `sanskrit/vyakarana` GitHub project. Three columns: gaṇa-number, position-within-gaṇa, dhātu in SLP1 transliteration.
- **`data/derived/dhatupatha_decomposed.md`** — every dhātu rendered in standard Devanāgarī with varṇa-level decomposition. Generated by `decompose_dhatupatha.py`.
- **`scripts/analyze_dhatupatha.py`** — structural classification, particle count, akṣara count, pattern, gaṇa distribution. Generates the §5.3.1 figures.
- **`scripts/decompose_dhatupatha.py`** — SLP1 → Devanāgarī conversion + varṇa-level decomposition.
- **`scripts/analyze_varga_distribution.py [gaṇa]`** — column × position analysis. Generates §5.3.2 and §5.3.3 figures.
- **`scripts/analyze_place_distribution.py [gaṇa]`** — place × position analysis. Generates §5.3.4 figures.
- **`scripts/analyze_extensions.py [gaṇa]`** — cluster analysis, akṣara-count breakdown, vowel × consonant. Generates §5.3.5, §5.3.6, §5.3.7 figures.
- **`scripts/analyze_distinguishability.py`** — feature-distance scoring, onset-coda OCP analysis, cross-gaṇa column distribution. Generates §5.3.8, §5.3.9, §5.3.10 figures.

Requirements: Python 3.10+. No external dependencies — the scripts use only the standard library. From the bundle root: `python3 scripts/<script-name>.py [gaṇa]` (where `[gaṇa]` is an optional numerical filter from 1 to 10).

The bundle is self-contained and includes a README with full attribution, methodology notes, and a license file. Every empirical claim in Chapter 11 and in this appendix can be verified by re-running the scripts against the source CSV.

---

*End of Appendix Part 5.*
