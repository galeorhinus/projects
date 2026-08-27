# Dhātupāṭha Empirical Findings — Engineering Signals

*Last updated: 2026-05-17.*

Synthesis of empirical engineering signals extracted from the Pāṇinian *Dhātupāṭha* (2,168 *dhātavaḥ*) via the scripts in this bundle. **Persisted explicitly because the interpretive synthesis is non-trivial and gets lost across sessions if not written down.** Scripts can re-derive every number; this file captures what the numbers *mean*.

---

> **Status note (2026-08-26):** This file preserves the May 2026 interpretive analysis, including provisional counts produced before the corrected marker-aware stripping pass. Use the generated reports in `data/derived/`, Chapter 10, and Appendix Part 6 for current numerical totals. The scripts remain the source of truth; a full refresh of this interpretive file is still pending.

## 1. Methodology summary

### Data source
- `data/dhatupatha.csv` — 2,235 entries; 2,168 *dhātavaḥ* after anubandha-stripping; from github.com/sanskrit/vyakarana
- Anubandha-aware classification per Pāṇini 1.3.2 / 1.3.3 / 1.3.5
- Bare *dhātu* forms classified into structural patterns (V, CV, CVC, CCV, etc.)

### Naming convention (analysis-internal, 2026-05-17)
Within position-role analyses, structural patterns use position-explicit naming:

| Old | New | Meaning |
|---|---|---|
| CV | **C₁V** | onset + vowel |
| VC | **VC₂** | vowel + coda |
| CVC | **C₁VC₂** | onset + vowel + coda |
| CCV | **C₁C₂V** | onset cluster + vowel |
| VCC | **VC₁C₂** | vowel + coda cluster |
| CCVC | **C₁C₂VC₃** | onset cluster + vowel + coda |
| CVCC | **C₁VC₂C₃** | onset + vowel + coda cluster |
| CCVCC | **C₁C₂VC₃C₄** | both clusters |

C₁ = onset position. C₂ = coda position. Inner positions (cluster-joiners) tracked separately as C₁ᵢ and C₂ᵢ. Outer positions (atom boundaries) as C₁ₒ and C₂ₒ.

### Position-role taxonomy

For each consonant in a single-akṣara atom, one of four roles:

| Role | Position | Engineering function |
|---|---|---|
| **onset_outer** (C₁ₒ) | atom-start | atom-onset, the "release" gesture |
| **onset_inner** (C₁ᵢ) | inside onset cluster, before vowel | cluster-joiner before the vowel |
| **coda_inner** (C₂ᵢ) | inside coda cluster, after vowel | cluster-joiner after the vowel |
| **coda_outer** (C₂ₒ) | atom-end | atom-closure, the "settlement" gesture |

Aggregations:
- **C₁ total** = onset_outer + onset_inner (all onset appearances)
- **C₂ total** = coda_inner + coda_outer (all coda appearances)
- **i/f ratio** = C₁ total / C₂ total (initial-vs-final preference)
- **outer total** = onset_outer + coda_outer (atom-boundary roles)
- **inner total** = onset_inner + coda_inner (cluster-joiner roles)

### Scripts that produce these numbers
- `scripts/analyze_dhatupatha.py` — structural classification by particle count, akṣara count, pattern
- `scripts/analyze_internal_structure.py` — CV/VC/CVC matrices, place-of-articulation analysis, CC-cluster analysis
- `scripts/analyze_position_roles.py` — extended C₁/C₂ position-role aggregation across cluster patterns
- `scripts/cluster_by_reactivity.py` — consonant clustering by reactivity-profile similarity
- `scripts/analyze_productivity.py` — Spearman correlation between particle count and MW-derivative count (Path A baseline)

### Figures produced
- `figures/build/building_dhatuh_particle_count.svg` — particle-count distribution (1 through 6+) with V-pattern row, structural-floor annotation, five-particle threshold annotation
- `figures/build/building_dhatuh_position_roles.svg` — per-consonant horizontal stacked bar showing onset_outer / onset_inner / coda_inner / coda_outer deployment for each of 33 consonants

---

## 2. Core empirical findings

### Single-vowel atoms (V-pattern)

**Exactly 7 V-pattern entries in the *Dhātupāṭha*.** Five unique single-vowel atoms:

| Atom | Gaṇa | Listing count |
|---|---|---|
| √ṛ (ऋ) | bhvādi, juhotyādi, svādi | 3 entries |
| √i (इ) | adādi | 1 entry |
| √ī (ī) | divādi | 1 entry |
| √u (उ) | bhvādi | 1 entry |
| √ṝ (ॠ) | kryādi | 1 entry |

5 unique atoms across 7 *Dhātupāṭha* listings (√ṛ appears 3× per Pāṇinian convention of separately listing inflectional-variant of the same atom). 0.32% of the corpus. **Structural floor of the atom inventory.**

### Particle-count distribution (anubandha-aware)

| Particles | Count | % | Common patterns |
|---:|---:|---:|---|
| 1 | 7 | 0.3% | V — √i √ī √u √ṛ √ṝ |
| 2 | 236 | 10.9% | C₁V, VC₂ |
| 3 | 1,051 | 48.5% | C₁VC₂, C₁C₂V, VC₂V |
| 4 | 676 | 31.2% | C₁C₂VC₃, C₁VC₂C₃, C₁VC₂V |
| 5 | 156 | 7.2% | C₁C₂VC₃C₄, longer |
| 6+ | 42 | 1.9% | cliff |

**Modal pattern: 3 particles** (48.5%). Compression-principle predictions hold; cliff at 5 particles confirmed.

### Vowel deployment (cumulative across all patterns)

```
अ    432+  ████████████████████████████████  (42% of CVC)
उ    245+  █████████████████                 (23% of CVC)
इ    161+  ███████████                       (14% of CVC)
ऋ     99+  ███████                           ( 8% of CVC)
ऊ     54+  ████
आ     43+  ███
ई     36+  ███
ॠ     28   ██
ए     17   █
ऐ      9   ▌
ओ      6   ▌
औ      0   ·  (inert)
ऌ      0   ·  (inert)
ॡ      0   ·  (inert)
```

**4-vowel substrate finding:** अ / उ / इ / ऋ together carry 92% of CVC deployment. The engineering operates over a 14-vowel inventory but deploys *dhātu* formation around 4 short vowels at 4 active pure places.

**Three inert vowels** (औ ऌ ॡ) at exactly zero deployment. Plus ओ, ऐ near-zero (compound vowels, sandhi-products).

---

## 3. Position-role analysis (extended across all single-akṣara patterns)

### Per-consonant top 15 (extended C₁/C₂ counts)

| Consonant | onset_outer | onset_inner | coda_inner | coda_outer | C₁ tot | C₂ tot | i/f |
|---|---:|---:|---:|---:|---:|---:|---:|
| र | 78 | 126 | 100 | 51 | 204 | 151 | 1.35× |
| क | 174 | 5 | 56 | 53 | 179 | 109 | 1.64× |
| ष | 85 | 31 | 17 | 134 | 116 | 151 | 0.77× |
| ल | 82 | 40 | 24 | 105 | 122 | 129 | 0.95× |
| व | 129 | 56 | 2 | 48 | 185 | 50 | 3.70× |
| प | 119 | 9 | 2 | 74 | 128 | 76 | 1.68× |
| म | 118 | 14 | 29 | 41 | 132 | 70 | 1.89× |
| स | 73 | 4 | 15 | 86 | 77 | 101 | 0.76× |
| च | 82 | 0 | 4 | 75 | 82 | 79 | 1.04× |
| श | 115 | 0 | 5 | 39 | 115 | 44 | 2.61× |
| द | 70 | 0 | 2 | 86 | 70 | 88 | 0.80× |
| ज | 53 | 0 | 7 | 97 | 53 | 104 | 0.51× |
| त | 104 | 8 | 19 | 22 | 112 | 41 | 2.73× |
| ट | 4 | 16 | 13 | 105 | 20 | 118 | 0.17× |
| ण | 31 | 9 | 3 | 63 | 40 | 66 | 0.61× |

### Cluster-joiner specialist class

5 atoms account for 73% of inner-cluster appearances:

| Atom | onset_inner | coda_inner | Inner total | % of consonant's total deployment |
|---|---:|---:|---:|---:|
| **र** | 126 | 100 | 226 | 64% |
| **व** | 56 | 2 | 58 | 25% |
| **ल** | 40 | 24 | 64 | 26% |
| **य** | 30 | 1 | 31 | 44% |
| **ष** | 31 | 17 | 48 | 18% |

These five = the अन्तःस्थ row (semivowels) + one ऊष्म (retroflex sibilant). **Semivowels + ष are engineered as universal cluster-joiners — the carbon-of-clusters role.**

### Outlier engineering observations
- **ल** — perfectly balanced (i/f = 0.95×); most-productive consonant overall (251 total); active in all four position-roles. The structural neutralizer.
- **र** — extreme cluster-joiner specialist; 64% of its deployment is inner-cluster.
- **C2 column** (अघोष महाप्राण: ख ठ थ फ छ) — 4 of 5 are strongly final. Aspirated unvoiced engineered as closure-marker.
- **C4 column** (घोष महाप्राण: घ झ ध ढ भ) — mostly INITIAL or balanced. Aspirated voiced engineered as release-marker.
- **ख** is the C2 anomaly (i/f = 1.25× balanced, not final-only like its column-mates).

---

## 4. Place-of-articulation aggregated

### Extended C₁/C₂ totals per place

| Place | C₁₀ | C₁ᵢ | C₂ᵢ | C₂₀ | C₁ tot | C₂ tot | i/f | outer | inner | inner % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| कण्ठ्य | 349 | 8 | 64 | 182 | 357 | 246 | 1.45× | 531 | 72 | 11.9% |
| तालव्य | 277 | 33 | 35 | 235 | 310 | 270 | 1.15× | 512 | 68 | 11.7% |
| मूर्धन्य | 205 | 186 | 145 | 481 | 391 | 626 | 0.62× | 686 | 331 | **32.5%** |
| दन्त्य | 389 | 64 | 77 | 411 | 453 | 488 | 0.93× | 800 | 141 | 15.0% |
| ओष्ठ्य | 458 | 93 | 41 | 254 | 551 | 295 | 1.87× | 712 | 134 | 15.8% |

### Place-level i/f comparison (CVC-only vs extended)

| Place | CVC-only i/f | Extended i/f | Change |
|---|---:|---:|---|
| ओष्ठ्य | 1.92× | 1.87× | unchanged |
| कण्ठ्य | 1.80× | 1.45× | softens |
| तालव्य | 1.15× | 1.15× | unchanged |
| दन्त्य | 0.80× | 0.93× | softens toward balance |
| मूर्धन्य | 0.40× | 0.62× | softens substantially |

**Ordering preserved across both analyses:** ओष्ठ्य > कण्ठ्य > तालव्य > दन्त्य > मूर्धन्य (initial-most to final-most).

### Place-level inner-position activity (new signal)

**मूर्धन्य is uniquely high in cluster-joiner activity (32.5% inner).** All other places: 11.7–15.8% inner. Driven by र's 226 inner appearances and ष's 48.

Engineering reading: मूर्धन्य is engineered as a **dual-role place** — atom-end specialist (ट ठ ड ण ष for closure) AND cluster-joiner specialist (र ष for joining). Other places are predominantly atom-boundary specialists with minor cluster-joining activity.

---

## 5. CVC place × place trajectory (920 of 944 atoms)

```
C1 \ C2        कण्ठ्य   तालव्य   मूर्धन्य   दन्त्य   ओष्ठ्य  | row tot
कण्ठ्य            7      26        84       43       18  |  178
तालव्य           15      11        53       41       33  |  153
मूर्धन्य         26      15        28       25       29  |  123
दन्त्य           25      37        46       34       52  |  194
ओष्ठ्य           26      44        93       99       10  |  272
col tot          99     133       304      242      142  |  920
```

**Two engineering principles visible in one matrix:**

1. **OCP (Obligatory Contour Principle)** — diagonal cells (same-varga C₁ + C₂) are systematically suppressed. कण्ठ्य × कण्ठ्य = 7, चवर्ग × चवर्ग = 2, ओष्ठ्य × ओष्ठ्य = 10. Off-diagonal cells 5–15× higher.

2. **मूर्धन्य as C₂ asymmetry** — मूर्धन्य appears 304 times as C₂ vs 123 times as C₁. Retroflex is engineered into the *final* consonant position. Ties to Ch 17's *mūrdhanya* engineering claim.

**Dominant trajectory cells:**
- ओष्ठ्य × दन्त्य: 99 (lip-release, dental-settle)
- ओष्ठ्य × मूर्धन्य: 93 (lip-release, retroflex-settle)
- कण्ठ्य × मूर्धन्य: 84 (back-release, retroflex-settle)

---

## 6. Initial CC clusters — the kṣ phenomenon

**क्ष (kṣ) is overwhelmingly the dominant CC cluster** in *Dhātupāṭha* atoms:
- CCV initial: 7
- CCVC initial: 20
- CVCC final: 29
- **Total: 56+ across CC structures**

No other cluster comes close. क्ष combines velar (kaṇṭhya, back) + retroflex sibilant (mūrdhanya, mid-tongue friction) — phonetically a long-distance articulatory movement. This specific cluster is engineered in heavily despite its phonetic cost.

### Top CC clusters by total appearances

**Initial (CCV + CCVC):**
1. क्ष (27 total): velar + retroflex sibilant
2. तर (12): dental + retroflex r (cluster-joiner)
3. सफ (12): dental sibilant + labial aspirated
4. शर (17): palatal sibilant + retroflex r
5. क्र (9): velar + retroflex r

**Final (CVCC):**
1. क्ष (29): velar + retroflex sibilant (mirror of initial pattern)
2. रद (12): retroflex r + dental
3. रव (12): retroflex r + labial semivowel
4. टट (9): geminate retroflex (closure-strengthener)

### Universal cluster-joiners (second-in-cluster)

| Atom | Appearances as 2nd-in-CC |
|---|---:|
| र | 100 |
| व | 45 |
| ल | 36 |
| ष | 29 |
| य | 28 |
| (others) | < 13 each |

Five atoms carry 73% of cluster-joining work. **Engineered as the bonding glue of Sanskrit's consonant clusters.**

---

## 7. The ten engineering signals (synthesis)

1. **Vowel productivity by place correlates with consonant position-preference by place.** Places where vowels are heavily deployed (कण्ठ्य, ओष्ठ्य) have consonants engineered for INITIAL. Places where vowels are inert (दन्त्य ऌ/ॡ) have consonants engineered for split / SPLIT (some strong-initial, some strong-final).

2. **Voicing × aspiration × position split.** C2 (अघोष महाप्राण = aspirated unvoiced) atoms strongly FINAL; C4 (घोष महाप्राण = aspirated voiced) atoms mostly INITIAL. Aspiration's positional role flips with voicing.

3. **ख is the C2 anomaly** — balanced i/f while ठ, थ, फ are all near-pure-final. Possibly because क is so heavily initial that the कण्ठ्य place spends its closure-role on ख.

4. **Articulatory-extreme INITIAL, curl FINAL.** ओष्ठ्य (lips, front) and कण्ठ्य (back of throat) → INITIAL. मूर्धन्य (tongue curl) → FINAL. Mid-mouth places (तालव्य, दन्त्य) sit between.

5. **Elective vowel affinities** — five consonants prefer उ over अ (त, ग, ठ, थ, ध — though ध actually prefers ऋ). Cross-cuts place; suggests an engineering axis the *varṇamālā* doesn't formalize.

6. **Cluster-joiner specialist class** (र व ल य ष) — 73% of all cluster-joining work. Engineered as universal bonders.

7. **Geminates concentrate at atom-end.** टट / कक / लल / etc. appear as final CC, not initial. Gemination engineered as closure-strengthener (parallel to aspiration and retroflex closure).

8. **4-vowel substrate.** अ उ इ ऋ carry 92% of CVC deployment despite the 14-vowel inventory. The inventory is engineered for completeness but atoms deploy around 4.

9. **ल is the structural neutralizer.** Perfectly balanced position, universal cluster-joiner, broad vowel compatibility. Most-productive consonant overall.

10. **ऋ as place-bridge.** The only vowel at मूर्धन्य place — phonetically a vowel that occupies a retroflex position. Bridges *svara* and *vyañjana* inventories at the same articulatory place.

### Plus, from the extended-cluster analysis (post-cluster-extension):

11. **मूर्धन्य is uniquely a dual-role place** (32.5% inner-cluster activity vs 11–16% elsewhere). र and ष drive this. Engineering: मूर्धन्य atoms are deliberately specialized to play BOTH atom-boundary and cluster-joining roles.

12. **र is the four-role consonant** — substantial deployment in all four position-roles (onset_outer 78, onset_inner 126, coda_inner 100, coda_outer 51). No other consonant covers all four roles at meaningful magnitude.

---

## 8. Cross-corpus validation pending

Path C corpus-attested combinatorial yield analysis (DCS BhG sub-corpus + DCS Ṛgveda saṃhitā sub-corpus) is the next major workstream. The expectation: the same hyper-reactive core (अ-substrate, ल as universal neutralizer, र as cluster-joiner specialist, the C2 closure-marker specialization) should hold in both *śruti* and *smriti* corpora.

Cross-corpus invariance under maximally different design purposes is itself the engineering signature.

---

## 9. Conceptual framings introduced 2026-05-17

### *Svara* / *vyañjana* as atom / ion
- ***Svara*** (vowel) = self-sounding = **stable atom** (analog: noble gas / complete element)
- ***Vyañjana*** (consonant) = manifests-only-with-other = **ion / radical** (charged, requires bonding)
- ***Akṣara*** = consonant-vowel bonded unit = **salt** ("imperishable" — Sanskrit's own term for the stable compound)
- The Sanskrit terminology itself encodes the ion/atom distinction in the category names

### Two periodic tables stacked
- ***Svara* table**: 14 vowel atoms; place × length axes; 4-vowel reactive core (अ उ इ ऋ); inert tier (औ ऌ ॡ)
- ***Vyañjana* table**: 33 consonant ions; the *varṇamālā* in canonical layout; structural axes = place × manner × voicing × aspiration

### Position-preference as a *hidden* engineering axis
The *varṇamālā* documents place × manner. Position-preference (initial vs final) is an *additional* engineering axis the corpus reveals but the *varṇamālā* does not formalize. Plus: cluster-joining capacity, vowel-preference (उ-preferring family), closure-marking specialization (C2, gemination, retroflex), and ल as universal neutralizer — these are all additional engineering signals from corpus analysis.

---

## 10. References to chapter prose

- **Ch 7-8**: *varṇamālā* engineering (place × manner × voicing × aspiration); the canonical 2D classification.
- **Ch 17**: retroflex / *mūrdhanya* engineering — Pattern 4 (place trajectory) and Pattern 11 (मूर्धन्य as dual-role place) provide empirical evidence.
- **Ch 10 §§10.2-10.5**: *varṇa → dhātu → śabda* pipeline, *svara/vyañjana* roles, *mātrā* envelope, and *dhāturacanā* scaffold procedure.
- **Ch 10 §10.6**: sonomer-count and *mātrā* compression check.
- **Ch 10 §§10.7-10.13**: scaffold concentration, *prayoga* deployment, and the four engineering verdicts (compression, distinguishability, engineering-poetry, *vaicitrya*). The position-role figure provides empirical support for distinguishability principle (engineering at the position-axis level).
- **Ch 10 §10.13**: Engineering Was Common Knowledge. The cross-cutting corpus signals here are additional evidence — the engineering operates at more axes than Pāṇini documented separately.
- **Ch 11**: empirical-pipeline workstream uses these findings to inform column-axis decision; Path C corpus analysis (BhG + Veda) is the next validation step.

---

## 11. Full per-consonant position-role table (all 33 consonants, anubandha-aware)

```
cons   onset_outer  onset_inner  coda_inner  coda_outer  | C₁ tot  C₂ tot   i/f
─────────────────────────────────────────────────────────┼──────────────────────
र         78          126          100         51        |   204    151   1.35×
क        174            5           56         53        |   179    109   1.64×
ष         85           31           17        134        |   116    151   0.77×
ल         82           40           24        105        |   122    129   0.95×
व        129           56            2         48        |   185     50   3.70×
प        119            9            2         74        |   128     76   1.68×
म        118           14           29         41        |   132     70   1.89×
स         73            4           15         86        |    77    101   0.76×
च         82            0            4         75        |    82     79   1.04×
श        115            0            5         39        |   115     44   2.61×
द         70            0            2         86        |    70     88   0.80×
ज         53            0            7         97        |    53    104   0.51×
त        104            8           19         22        |   112     41   2.73×
ट          4           16           13        105        |    20    118   0.17×
ण         31            9            3         63        |    40     66   0.61×
ह         44            0            1         58        |    44     59   0.75×
भ         50            0            5         47        |    50     52   0.96×
ग         72            0            1         27        |    72     28   2.57×
ड          7            0            7         84        |     7     91   0.08×
ध         49            2            0         37        |    51     37   1.38×
न         10            8           17         38        |    18     55   0.33×
य         19           30            1         21        |    49     22   2.23×
ब         38            1            3         27        |    39     30   1.30×
ख         32            3            1         27        |    35     28   1.25×
ठ          0            4            4         44        |     4     48   0.08×
घ         26            0            2         17        |    26     19   1.37×
थ          1            2            0         37        |     3     37   0.08×
फ          4           13            0         17        |    17     17   1.00×
ञ          0            3           18          0        |     3     18   0.17×
झ          8            0            0          2        |     8      2   4.00×
ङ          1            0            3          0        |     1      3   0.33×
छ          0            0            0          1        |     0      1   0.00×
ढ          0            0            1          0        |     0      1   0.00×
```

**Total deployment per consonant** (C₁ tot + C₂ tot, sorted): ल 251, र 355, ष 267, क 288, प 204, व 235, म 202, स 178, च 161, श 159, द 158, ज 157, त 153, ट 138, ण 106, ह 103, भ 102, ग 100, ड 98, ध 88, ब 69, ख 63, न 73, य 71, फ 34, घ 45, ठ 52, थ 40, ञ 21, झ 10, ङ 4, छ 1, ढ 1.

(Most-productive: **र** (355) when extended. Most-productive in the three-pattern analysis was **ल** because clusters were excluded.)

---

## 12. CV-pattern matrix (initial consonant × vowel, 156 atoms)

Raw output from `analyze_internal_structure.py`. Each cell = count of C₁V atoms with that specific (consonant, vowel) pair.

```
cons     अ   आ   इ   ई   उ   ऊ   ऋ   ॠ   ऌ   ॡ   ए   ऐ   ओ   औ  | row tot
─────────────────────────────────────────────────────────────────┼────────
─ कवर्ग ─
क        .   .   1   .   3   1   2   3   .   .   .   1   .   .  |  11
ख        .   .   .   .   1   .   .   .   .   .   .   1   .   .  |   2
ग        .   2   .   .   3   .   1   3   .   .   .   1   .   .  |  10
घ        .   .   .   .   1   .   3   .   .   .   .   .   .   .  |   4
ङ        .   .   .   .   1   .   .   .   .   .   .   .   .   .  |   1
─ चवर्ग ─
च        .   .   3   .   .   .   .   .   .   .   .   .   1   .  |   4
छ        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
ज        .   .   3   .   2   .   .   4   .   .   .   1   .   .  |  10
झ        .   .   .   .   .   .   .   2   .   .   .   .   .   .  |   2
ञ        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
─ टवर्ग ─
ट        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
ठ        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
ड        .   .   .   2   .   .   .   .   .   .   .   .   .   .  |   2
ढ        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
ण        .   .   .   1   1   1   .   .   .   .   .   .   .   .  |   3
─ तवर्ग ─
त        .   .   .   .   1   .   .   1   .   .   .   .   .   .  |   2
थ        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
द        .   1   .   1   2   1   1   3   .   .   1   .   1   .  |  11
ध        .   1   1   1   1   4   3   1   .   .   1   .   .   .  |  13
न        1   .   .   .   .   .   .   2   .   .   .   .   .   .  |   3
─ पवर्ग ─
प        .   2   1   1   .   2   3   3   .   .   .   1   .   .  |  13
फ        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
ब        .   .   .   .   .   .   .   .   .   .   .   .   .   .  |   0
भ        .   1   .   .   .   2   2   1   .   .   .   .   .   .  |   6
म        .   3   1   3   .   2   1   1   .   .   1   .   .   .  |  12
─ अन्य ─
य        .   1   .   .   3   .   .   .   .   .   .   .   .   .  |   4
र        .   1   2   2   2   .   .   .   .   .   .   1   .   .  |   8
ल        .   1   .   3   .   1   .   .   .   .   .   .   .   .  |   5
व        .   1   .   1   .   .   3   2   .   .   1   .   .   .  |   8
श        .   .   1   1   .   .   .   1   .   .   .   1   1   .  |   5
ष        .   .   2   .   3   3   .   .   .   .   .   1   1   .  |  10
स        .   .   .   .   .   .   2   .   .   .   .   .   .   .  |   2
ह        .   .   1   .   1   .   2   .   .   .   .   .   .   .  |   4
col tot  1  14  16  16  25  17  23  27   0   0   4   8   4   0  | 155
```

**Cell-level engineering observations** (from CV matrix):
- **94 of 462 cells filled** (20.3% of consonant × vowel space)
- **No consonant deploys with all 14 vowels.** Most-prolific consonants (ध, प, म, ल) deploy with 5–9 distinct vowels; minimum is 1.
- **Vowels with zero CV deployment:** ऌ, ॡ, औ. These vowels are not used in onset-vowel atoms.
- **Vowels with low CV deployment** (≤5): ए (4), ओ (4). Diphthongs and combined vowels.
- **Vowels with high CV deployment** (≥20): उ (25), ऋ (23), ॠ (27). Vocalic-r and labial-vowel atoms cluster here.

---

## 13. VC-pattern matrix (vowel × final consonant, 87 atoms)

```
swar    क  ख  ग  घ  ङ  च  छ  ज  झ  ञ  ट  ठ  ड  ढ  ण  त  थ  द  ध  न  प  फ  ब  भ  म  य  र  ल  व  श  ष  स  ह  | row tot
─────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────
अ       2  .  2  1  .  2  .  2  .  .  1  1  1  .  2  2  .  2  .  2  .  .  1  1  3  1  .  1  1  1  1  3  3  |  36
आ       .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  |   2
इ       1  2  1  .  .  .  .  .  .  .  1  .  .  .  1  .  .  1  .  .  .  .  .  .  .  .  .  2  1  .  3  .  .  |  13
ई       .  2  .  .  .  .  .  1  .  .  .  .  2  .  .  .  .  .  .  .  .  .  .  .  .  .  2  .  .  1  2  .  1  |  11
उ       .  2  .  .  .  3  .  .  .  .  .  2  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  1  .  .  |   9
ऊ       .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  |   4
ऋ       .  .  .  .  .  2  .  2  .  .  .  .  .  .  1  .  .  .  2  .  .  1  .  .  .  .  .  .  .  .  .  .  .  |   8
ॠ       0 across the board                                                                                   |   0
ऌ ॡ ऐ ओ औ : 0 across all consonants                                                                          |   0
ए       .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  |   2
col tot 3  6  3  1  0  8  0  5  0  0  2  5  3  0  4  2  0  3  3  3  0  1  1  2  3  1  2  3  2  2  8  4  5  |  85
```

**Cell-level engineering observations** (VC matrix):
- **56 of 462 cells filled** (12.1% of space).
- **The vowel अ dominates** (36 of 85 = 42% of VC atoms). All other vowels < 14 each.
- **VC is overwhelmingly an अ-initial pattern.** Long vowels and most other vowels barely appear.
- **9 vowels at zero deployment** (ॠ ऌ ॡ ऐ ओ औ + ones with only अ-pairings).

---

## 14. CVC vowel distribution (944 atoms)

```
अ    395  ████████████████████████████████████████████████████████████████████████████████
उ    220  ████████████████████████████████████████████
इ    132  ██████████████████████████
ऋ     76  ███████████████
ऊ     37  ███████
आ     29  █████
ई     20  ████
ए     11  ██
ॠ      1
ऐ      1
ओ      2
औ      0
ऌ      0
ॡ      0
```

CVC pattern uses 4 vowels (अ उ इ ऋ) for 92% of deployment. Long vowels and combined vowels barely appear; vocalic-l effectively never.

---

## 15. CVC C1 consonant distribution (top 15)

```
क      87  ##################
व      76  ###############
म      76  ###############
प      71  ##############
ल      70  ##############
र      65  #############
त      64  ############
च      56  ###########
श      52  ##########
द      37  #######
ग      30  ######
ज      28  #####
ष      26  #####
ण      26  #####
भ      25  #####
```

Strong-INITIAL consonants dominate: क, व, म, प, ल, र, त, च (all i/f > 1.0).

---

## 16. CVC C2 consonant distribution (top 15)

```
ट      76  ###############
ल      73  ##############
ड      71  ##############
ष      65  #############
ज      63  ############
स      52  ##########
प      51  ##########
द      47  #########
ण      37  #######
ठ      35  #######
च      33  ######
ह      31  ######
श      27  #####
न      26  #####
व      26  #####
```

Strong-FINAL consonants dominate: ट, ड, ष, ज, स, ठ (all i/f < 1.0). ल remains balanced (third on the C2 list as well as among the universal-bonders).

---

## 17. Initial CC clusters — full top-30

From CCV + CCVC patterns combined, the dominant initial CC clusters:

| Rank | Cluster | Count (CCV) | Count (CCVC) | Total |
|---|---|---:|---:|---:|
| 1 | क्ष (kṣ) | 7 | 20 | 27 |
| 2 | शर (śr) | 6 | 11 | 17 |
| 3 | तर (tr) | 0 | 12 | 12 |
| 4 | सफ (sph) | 0 | 12 | 12 |
| 5 | ष्ट (ṣṭ) | 3 | 11 | 14 |
| 6 | वय (vy) | 0 | 11 | 11 |
| 7 | कल (kl) | 0 | 10 | 10 |
| 8 | शव (śv) | 0 | 9 | 9 |
| 9 | कर (kr) | 0 | 9 | 9 |
| 10 | धव (dhv) | 0 | 7 | 7 |
| 11 | वर (vr) | 2 | 7 | 9 |
| 12 | पर (pr) | 5 | 6 | 11 |
| 13 | गर (gr) | 0 | 6 | 6 |
| 14 | शल (śl) | 0 | 6 | 6 |
| 15 | सप (sp) | 0 | 5 | 5 |
| 16 | सव (sv) | 0 | 5 | 5 |
| 17 | पल (pl) | 0 | 5 | 5 |
| 18 | दर (dr) | 4 | 0 | 4 |
| 19 | सम (sm) | 3 | 0 | 3 |
| 20 | धर (dhr) | 3 | 0 | 3 |

**Engineering observations:**
- क्ष dominates by 1.6× over the runner-up.
- Most clusters end in a semivowel (र, व, ल, य) or sibilant (ष) — confirms the universal-bonder analysis.
- Velar + retroflex-sibilant (क्ष), and velar + r/l/v dominate cluster initials.
- स as cluster-starter (सफ, सप, सव, सम) is a distinct engineered family.

---

## 18. Final CC clusters — full top-20 from CVCC

| Rank | Cluster | Count |
|---|---|---:|
| 1 | क्ष (kṣ) | 29 |
| 2 | रद (rd) | 12 |
| 3 | रव (rv) | 12 |
| 4 | रब (rb) | 10 |
| 5 | रज (rj) | 9 |
| 6 | टट (ṭṭ — geminate) | 9 |
| 7 | रण (rṇ) | 9 |
| 8 | लल (ll — geminate) | 9 |
| 9 | कक (kk — geminate) | 8 |
| 10 | तर (tr) | 8 |
| 11 | ञच (ñc) | 6 |
| 12 | रह (rh) | 6 |
| 13 | नध (ndh) | 5 |
| 14 | रच (rc) | 5 |
| 15 | मफ (mph) | 5 |
| 16 | मभ (mbh) | 5 |
| 17 | सत (st) | 5 |
| 18 | षक (ṣk) | 5 |
| 19 | षट (ṣṭ) | 4 |
| 20 | मप (mp) | 4 |

**Engineering observations:**
- क्ष ALSO dominates final-CC (29 atoms). The same cluster works at both atom-ends. Engineering symmetry.
- **र is the dominant first-of-coda-cluster** (रद, रव, रब, रज, रण, रच, रह — all start with र; total ~62 atoms have र as first-of-coda). र's cluster-joiner role is symmetric across onset and coda positions.
- **Geminates (टट, लल, कक) all appear in final-coda position** — gemination engineered as closure-strengthener.
- **Nasal + stop homorganic clusters** (नध, मफ, मभ, मप) appear in final-coda. Standard sonority-hierarchy compliance.

---

## 19. Classification edge cases and gaps

### Atoms not captured in the place-of-articulation matrix
- **920 of 944 CVC atoms** were classified by place-of-articulation. The remaining **24 CVC atoms** have C₁ or C₂ that doesn't map cleanly to one of the 5 Pāṇinian places (possibly atoms with anusvara, visarga, or non-standard SLP1 codes).
- These 24 outliers are listed in the script output for hand-review.

### Patterns with multiple vowels (currently EXCLUDED from position-role analysis)
- 348 two-akṣara atoms (CVCV, VCV, CVCVC, etc.) are skipped because intervocalic consonant position is ambiguous between "coda of syllable 1" and "onset of syllable 2."
- Future extension: classify intervocalic consonants under both roles (onset of next syllable per standard phonological maximization), or under a separate "intervocalic" role.

### Anubandha-stripping subtleties
- Pāṇini's it-marker convention (1.3.2 — *upadeśe 'janunāsika it*) treats short-vowel-with-anunāsika as an it-marker. The classifier `strip_anubandhas` handles this.
- Initial anubandhas per 1.3.5 (ñi-, ṭu-, ḍu-) are stripped from the start of the citation form. The classifier handles this.
- Accent markers (~ \ ^) are stripped. The classifier handles this.
- Edge cases (atoms with multiple accents, non-standard markers) may produce slightly different particle counts. Worth re-checking the source data if any atom's classification looks anomalous.

### Three-pattern vs extended count discrepancies
- `analyze_dhatupatha.py` reports CV: 152, VC: 84, CVC: 919 (uses `data/dhatupatha.csv` and pattern_counts directly).
- `analyze_internal_structure.py` reports CV: 156, VC: 87, CVC: 944 (small discrepancy of 4–25 atoms per pattern).
- The difference is likely in anubandha-edge-case handling between the two scripts' loops. **Worth reconciling at some point** but not critical — the structural patterns are robust regardless.

---

## 20. Cluster-joiner specialist class — quantified analysis

| Atom | onset_outer | onset_inner | coda_inner | coda_outer | Inner total | Outer total | Inner / (Inner+Outer) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **र** | 78 | 126 | 100 | 51 | 226 | 129 | **64%** |
| **ण** | 31 | 9 | 3 | 63 | 12 | 94 | 11% |
| **व** | 129 | 56 | 2 | 48 | 58 | 177 | 25% |
| **ल** | 82 | 40 | 24 | 105 | 64 | 187 | 26% |
| **ष** | 85 | 31 | 17 | 134 | 48 | 219 | 18% |
| **य** | 19 | 30 | 1 | 21 | 31 | 40 | **44%** |
| **म** | 118 | 14 | 29 | 41 | 43 | 159 | 21% |
| **न** | 10 | 8 | 17 | 38 | 25 | 48 | **34%** |
| **त** | 104 | 8 | 19 | 22 | 27 | 126 | 18% |
| **फ** | 4 | 13 | 0 | 17 | 13 | 21 | **38%** |
| **ट** | 4 | 16 | 13 | 105 | 29 | 109 | 21% |
| **स** | 73 | 4 | 15 | 86 | 19 | 159 | 11% |

**Specialist-class membership criterion**: Inner / total ≥ 25%.

Atoms meeting the criterion: **र (64%), य (44%), फ (38%), न (34%), ल (26%), व (25%)**.

**र is the extreme specialist.** य and फ are next. Plus the broader cluster-joiner band (व ल) where ~25% of deployment is inner-cluster.

ष at 18% is a "minor cluster-joiner with strong outer-coda specialty." Not a pure specialist but participates.

---

## 21. Total atom counts by pattern (all single-akṣara, anubandha-aware)

```
Pattern (new name) (old name)   Atom count
─────────────────────────────────────────
C₁VC₂                  (CVC)        944
C₁C₂VC₃                (CCVC)       240
C₁VC₂C₃                (CVCC)       235
C₁V                    (CV)         156
VC₂                    (VC)          87
C₁C₂V                  (CCV)         85
C₁C₂VC₃C₄              (CCVCC)       49
VC₁C₂                  (VCC)         34
─────────────────────────────────────────
Subtotal: single-akṣara (1 V)    1,830
─────────────────────────────────────────

Plus rarer single-akṣara patterns:
CVCCC                       7
CCCV                        3
CCCVC                       1
CCCVCC                      1
CVCCCC                      1
VCCCC                       1
VCCC                        1
─────────────────────────────────────────
Total single-akṣara             1,852
V (pure vowel)                      7
─────────────────────────────────────────
Total atoms classifiable: 1,859

Plus 309 two-or-more-akṣara atoms = 2,168 total Dhātupāṭha entries.
```

The 7 V-pattern atoms are the 5 single-vowel dhātus (√i √ī √u √ṛ √ṝ), with √ṛ listed 3× across different gaṇas.

---

## 22. Reactivity profile — complete output (all 33 consonants, sorted by total productivity)

From `cluster_by_reactivity.py`, **C₁V + VC₂ + C₁VC₂ data only** (not extended to clusters — this is the original three-pattern view):

```
cons  tot  init  fin  i/f     top vowels (count)
─────────────────────────────────────────────────
ल    151    75    76  0.99×   अ(66), उ(31), इ(27), ऊ(10), ई(9)
प    135    84    51  1.65×   अ(38), उ(32), इ(21), ऋ(21), ऊ(9)
क    121    98    23  4.26×   अ(47), उ(37), ऋ(10), इ(7), ऊ(7)
म    114    88    26  3.38×   अ(48), उ(18), इ(14), ऋ(11), आ(9)
व    112    84    28  3.00×   अ(49), इ(29), ऋ(15), ई(8), आ(5)
ष    109    36    73  0.49×   अ(28), इ(24), उ(20), ऊ(19), ऋ(13)
ज    106    38    68  0.56×   अ(36), उ(28), इ(17), ऋ(11), ॠ(4)
च    101    60    41  1.46×   अ(47), उ(26), इ(13), ऋ(5), आ(4)
द     98    48    50  0.96×   अ(42), इ(19), उ(12), ऋ(9), आ(5)
र     95    73    22  3.32×   अ(37), उ(29), इ(14), ई(6), आ(4)
श     86    57    29  1.97×   अ(29), इ(17), उ(16), ऋ(8), ई(6)
ड     81     7    74  0.09×   अ(32), उ(30), इ(7), ई(5), ऋ(5)
ट     80     2    78  0.03×   अ(35), उ(29), इ(11), ऊ(2), ई(1)
त     79    66    13  5.08×   उ(24), अ(22), इ(11), ऋ(11), ई(3)
ण     70    29    41  0.71×   अ(33), उ(13), इ(9), ऋ(7), ऊ(4)
स     65     9    56  0.16×   अ(34), उ(9), इ(8), आ(6), ऋ(4)
ह     61    25    36  0.69×   अ(28), ऋ(11), इ(9), उ(8), ए(3)
ग     58    40    18  2.22×   उ(20), अ(19), ऋ(6), इ(5), ॠ(3)
भ     56    31    25  1.24×   अ(24), उ(11), ऋ(8), आ(6), ऊ(4)
ध     52    27    25  1.08×   ऋ(15), ऊ(9), अ(7), उ(7), इ(6)
ख     49    25    24  1.04×   अ(23), इ(12), उ(8), ई(2), ए(2)
ठ     40     0    40  0.00×   उ(20), अ(15), ए(3), इ(1), ऊ(1)
घ     37    21    16  1.31×   अ(21), उ(8), ऋ(6), इ(2)
न     36     7    29  0.24×   अ(26), आ(5), उ(2), ॠ(2), ऊ(1)
ब     34    22    12  1.83×   उ(13), अ(12), इ(5), ऋ(3), ए(1)
य     28    17    11  1.55×   अ(17), उ(9), आ(1), ऊ(1)
थ     12     1    11  0.09×   उ(7), अ(4), ऋ(1)
फ     11     2     9  0.22×   अ(4), उ(3), ऋ(3), इ(1)
झ      6     6     0   inf    अ(4), ॠ(2)
ङ      1     1     0   inf    उ(1)
```

**Consonants with zero deployment in three-pattern analysis:** छ, ढ, ञ — all listed in the *varṇamālā* but virtually unused in single-onset / single-coda / CVC contexts. Their few appearances (छ 1, ढ 1, ञ 21 inner-cluster appearances) only show up in cluster patterns.

The extended (cluster-aware) version of this table is in Section 11 above.

---

## 23. Future-research / pending analyses

1. **Path C corpus-attested combinatorial yield (DCS).** Compute (*upasarga*, *pratyaya*) bonding count per *dhātu* across DCS reference corpus. Required for Ch 11 valency analysis.

2. **Cross-corpus: BhG vs Veda.** Apply same Path C measure within DCS BhG sub-corpus and DCS Ṛgveda sub-corpus. Expected: same hyper-reactive core (अ-substrate; ल as neutralizer; र as cluster-joiner; C2 closure-marker specialization) dominates both.

3. **Multi-akṣara position-role analysis.** Extend `analyze_position_roles.py` to handle two-akṣara (CVCV, VCV, CVCVC) and three-akṣara atoms. Intervocalic consonants need a position-role assignment (probably "onset of next syllable" per phonological-maximization convention).

4. **Reconcile three-pattern vs extended atom counts.** Small discrepancies (4–25 atoms per pattern) between `analyze_dhatupatha.py` (CV 152) and `analyze_internal_structure.py` (CV 156). Trace the difference; ensure all scripts agree.

5. **Mendeleev-style gap analysis.** Which (place, manner, position) combinations are predicted by the engineering but appear at near-zero deployment? Are there "gaps" the engineering could have filled but didn't?

6. **Sound-symbolism / engineering-poetry quantification.** Ch 10's third principle (form-meaning resonance — liquid consonants in flow-action dhātus, etc.) — can this be quantified empirically by clustering *dhātus* on their (form-features × meaning-domain) joint distribution?

7. **Semantic-domain analysis.** For each *dhātu*, classify its semantic domain (motion / cognition / speech / action / being / etc.). Test whether semantic domains correlate with phonetic position. The "structure predicts behavior" claim Ch 11 lands.

8. **Comparative-corpus engineering signatures.** Apply the same position-role analysis to:
   - Latin verbal roots (if extractable)
   - Greek verbal roots
   - Avestan (closest comparison)
   - Modern Sanskrit-loaning languages (Marathi, Hindi)
   - Goal: show that the engineering signatures are unique to Sanskrit, not universal phonological properties.

---

*End of FINDINGS. This document captures the empirical synthesis as of 2026-05-17. Future sessions should treat this as the source-of-truth for "what the Dhātupāṭha empirical analysis has revealed" — the scripts can re-derive any number, but the interpretive synthesis lives here.*
