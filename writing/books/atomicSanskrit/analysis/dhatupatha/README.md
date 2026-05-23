# Dhātupāṭha Analysis — Reproducibility Bundle

A reproducibility bundle for the empirical claims in **Chapter 10** (*Building the Dhātuḥ*) and **Appendix Part 5** (*The Architecture by the Numbers*) of the book ***Atomic Sanskrit*** (Parag Tope).

The bundle contains:
- The machine-readable Pāṇinian *Dhātupāṭha* (2,168 verbal-root entries in SLP1 transliteration)
- A derived Devanāgarī decomposition of every entry
- Python scripts that compute the structural-classification, varga-column, place-of-articulation, cluster, akṣara-count, vowel, and distinguishability analyses cited in the book

Anyone can reproduce every empirical claim in the book by running the scripts against the source data.

---

## Structure

```
analysis/dhatupatha/
├── README.md                                ← this file
├── LICENSE                                  ← MIT for scripts; data attributions inside
├── data/
│   ├── dhatupatha.csv                       ← source (2,168 entries)
│   ├── dhatu_productivity.csv               ← curated productivity sample (138 dhātus)
│   └── derived/
│       └── dhatupatha_decomposed.md         ← Devanāgarī decomposition (generated)
└── scripts/
    ├── analyze_dhatupatha.py                ← structural classification (particle count,
    │                                          akṣara count, pattern, gaṇa distribution)
    ├── decompose_dhatupatha.py              ← SLP1 → Devanāgarī + varṇa decomposition
    ├── analyze_varga_distribution.py        ← column × position analysis
    ├── analyze_place_distribution.py        ← place-of-articulation × position
    ├── analyze_extensions.py                ← clusters, akṣara breakdown, vowel × consonant
    ├── analyze_distinguishability.py        ← feature-distance scoring,
    │                                          OCP / onset-coda analysis, cross-gaṇa
    └── analyze_productivity.py              ← productivity vs. structural complexity
                                               (MW-derivative-count proxy, Spearman ρ)
```

---

## Quick start

Requirements: **Python 3.10+**. No external dependencies — the scripts use only the standard library.

```bash
# From the bundle root:
python3 scripts/analyze_dhatupatha.py
python3 scripts/decompose_dhatupatha.py
python3 scripts/analyze_varga_distribution.py
python3 scripts/analyze_varga_distribution.py 1   # gaṇa 1 only
python3 scripts/analyze_place_distribution.py 1
python3 scripts/analyze_extensions.py 1
python3 scripts/analyze_distinguishability.py
python3 scripts/analyze_productivity.py
```

Each script prints a structured report to stdout. `decompose_dhatupatha.py` also writes a derived Devanāgarī markdown file to `data/derived/dhatupatha_decomposed.md`.

---

## What each script does

### `analyze_dhatupatha.py`
Structural classification of every dhātu in the *Dhātupāṭha*. Strips Pāṇinian *anubandhas* per *Aṣṭādhyāyī* 1.3.2, 1.3.3, 1.3.5; classifies each dhātu by phoneme count, akṣara count, and CV/CVC/CCVC/CVCC/CCVCC pattern. Reports counts by gaṇa, by akṣara count, and by structural pattern.

### `decompose_dhatupatha.py`
Converts each dhātu from SLP1 to standard Devanāgarī (with inherent /a/, vowel diacritics, and halants applied correctly), and produces a varṇa-level decomposition showing each constituent particle separately:

  कृ = क् + ऋ &nbsp; *(CV, 2 part., 1 akṣ.; SLP1 `qukf\Y`)*
  गम् = ग् + अ + म् &nbsp; *(CVC, 3 part., 1 akṣ.; SLP1 `gama~`)*
  स्कन्द् = स् + क् + अ + न् + द् &nbsp; *(CCVCC, 5 part., 1 akṣ.; SLP1 `skand`)*

Output: `data/derived/dhatupatha_decomposed.md`.

### `analyze_varga_distribution.py [gaṇa]`
For each varga consonant occurrence in the corpus, identifies its varga column (C1 unvoiced-unaspirated, C2 unvoiced-aspirated, C3 voiced-unaspirated, C4 voiced-aspirated, C5 nasal) and its position in the dhātu (initial / medial / final). Reports column × position distributions. Tests the predictions: C1 dominance, position-conditional column preferences. Optional gaṇa filter.

### `analyze_place_distribution.py [gaṇa]`
Identifies the place of articulation (sthāna) of each varga consonant: velar / palatal / retroflex / dental / labial. Computes place × position distribution, the full 5 × 5 varga grid, and top-frequency specific consonants. Tests predictions about place uniformity and position preferences (e.g., retroflex initial avoidance).

### `analyze_extensions.py [gaṇa]`
Three deeper analyses:
1. **Cluster analysis** — top initial and final 2-consonant clusters, revealing phonotactic preferences in dhātu construction (stop + sonorant onsets, geminate finals, etc.).
2. **Akṣara-count breakdown** — column and place distribution filtered by akṣara count, testing whether the simplest atoms show purest engineering preferences.
3. **Vowel × consonant interaction** — vowel frequency distribution and consonant-vowel co-occurrence patterns (e.g., the prominence of the syllabic /ṛ/).

### `analyze_distinguishability.py`
Quantitative implementation of the cost × distinguishability framework:
1. For each varga consonant, compute mean weighted feature-distance to all other varga consonants (binary Hamming + asymmetric-aspiration-weighted) and articulatory cost. Engineering value = distinguishability / (1 + cost). Compute Spearman rank correlation with corpus frequency.
2. **Onset-coda co-occurrence** — for single-syllable dhātus, test place harmony (the OCP / Obligatory Contour Principle) and voicing harmony.
3. **Cross-gaṇa column distribution** — does the column pattern hold across all 10 *gaṇāḥ*? Identifies gaṇa-specific signatures (e.g., the *juhotyādi* C4 enrichment).

### `analyze_productivity.py`
Tests the compression-principle prediction that the *simplest dhātus generate the most vocabulary*. Loads `data/dhatu_productivity.csv` — a curated sample of 138 dhātus spanning the structural pattern space (CV, VC, CVC, CCV, CCVC, CVCC, CCVCC), with productivity scores estimated from the Monier-Williams Sanskrit-English Dictionary (1899) and V. S. Apte's *Practical Sanskrit-English Dictionary* (1890). Productivity is operationalized as the count of *primary derivatives* per dhātu (kṛdanta nominals, upasarga-prefixed verbs and their nominals, agentive / instrumental / abstract nominal derivatives). The script computes Spearman rank correlations between productivity and structural features, stratifies productivity by particle count and by pattern, and contrasts the pattern composition of the top-20 vs. bottom-20 by productivity. Documented prediction: ρ(productivity, particle-count) is strongly negative; CV-pattern *dhātus* dominate the top of the productivity ranking. The data sourcing is approximate (±20%), and the ranking — not the precise count — is the load-bearing claim.

---

## The Pāṇinian anubandha-stripping methodology

Each script applies three *it-saṃjñā* rules from Pāṇini's *Aṣṭādhyāyī* before structural classification, to recover the underlying root form from the canonical citation form:

1. **1.3.2 — *upadeśe 'janunāsika it***. In the citation form (*upadeśa*), a final *anunāsika*-marked short vowel is an *anubandha*. The trailing short *-a* / *-i* / *-u* after a consonant is stripped — provided that at least one other vowel remains in the form. The "vowel-survival" condition prevents over-stripping of genuine CV-pattern roots like *ji* जि (to conquer), *hu* हु (to sacrifice), *sru* स्रु (to flow).

2. **1.3.3 — *halantyam***. A trailing single-consonant *anubandha* (the *ñit*, *ṅit*, *lit*, *ṣit*, *ṭit*, *ḍit* markers signaling grammatical properties like ātmanepadī conjugation) is stripped when it sits immediately after a vowel. The canonical case: the *kṛ* dhātu's citation form is *ḍukṛñ* (SLP1: `qukf\Y`); the initial *ḍu* is stripped by 1.3.5, the trailing *ñ* by 1.3.3, leaving the bare root *kṛ*.

3. **1.3.5 — *ādir ñiṭuḍavaḥ***. The initial two-character sequences *ñi* (SLP1: `Yi`), *ṭu* (`wu`), *ḍu* (`qu`) in dhātu citation forms are *anubandhas* and are stripped from the front.

Accent markers (~, \\, ^) in the SLP1 encoding indicate *udātta*, *anudātta*, *svarita* respectively and are stripped before structural classification.

The stripping is implemented identically in every script that uses it (the function is duplicated for self-containedness). Cross-checking against the Sanskrit Heritage Platform's `parts.csv` (https://github.com/sanskrit/data/blob/master/sanskrit-heritage-site/parts.csv, ~11,570 verb stems) confirms that this rule-set recovers the standard underlying roots for the vast majority of *Dhātupāṭha* entries — including canonical cases like *kṛ* (ḍukṛñ → kṛ), *brū* (brūñ → brū), *śri* (śriñ → śri).

---

## Source data attribution

The source CSV at `data/dhatupatha.csv` is taken verbatim from the open-source `sanskrit/vyakarana` project:

- **Source**: <https://github.com/sanskrit/vyakarana>
- **File**: `data/dhatupatha.csv` in that repository
- **Format**: three columns — *gaṇa-number*, *position-within-gaṇa*, *dhātu in SLP1 transliteration with Pāṇinian accent markers*

The `sanskrit/vyakarana` repository did not have an explicit LICENSE file at the time of this bundle's preparation. Users who want to redistribute the source CSV should check the upstream repository's current licensing status. The underlying *Dhātupāṭha* itself is an ancient Sanskrit canonical text in the public domain.

The 2,168-entry count in this CSV sits within the conventional Pāṇinian range (~1,940 to ~2,200 depending on recension). Other published *Dhātupāṭha* recensions — Bhattoji Dīkṣita's *Siddhāntakaumudī*, the *Mādhavīya Dhātuvṛtti*, the *Kṣīrasvāmin* commentary — yield comparable totals with minor recensional variation in marginal entries.

---

## How the findings cross-reference the book

The empirical claims in **Chapter 10** of *Atomic Sanskrit* are the load-bearing distillation; the full work (predictions, data tables, verdicts including falsifications) is in **Appendix Part 5**.

| Book location | Reproduced by |
|---|---|
| Ch 10 §10.4 (atomic-layer structural patterns) | `analyze_dhatupatha.py` |
| Ch 10 §10.5 (thermodynamic-threshold distribution) | `analyze_dhatupatha.py` |
| Ch 10 §10.6 (cost × distinguishability; OCP; /ṛ/ prominence; cell-level allocation) | `analyze_varga_distribution.py`, `analyze_distinguishability.py`, `analyze_extensions.py` |
| Ch 10 §10.7 (productivity — simplest atoms generate the most) | `analyze_productivity.py` |
| Ch 10 §10.8 (engineering enables poetry — *varṇa-vāda* synthesis) | (synthesis section; data from all scripts) |
| Ch 10 §10.10 (juhotyādi C4 teaser → Ch 11) | `analyze_distinguishability.py` |
| Appendix Part 5 (full empirical work) | All scripts |

The findings the scripts produce should match those cited in the book, modulo any minor numerical drift if the upstream source CSV is updated.

---

## Methodology notes for future work

Two methodological refinements are out of scope for this bundle but flagged for future contributors:

1. **Anubandha-stripping completeness**. The current implementation applies *Aṣṭādhyāyī* 1.3.2, 1.3.3, and 1.3.5. The further rules *cuṭū* (1.3.7) and *laśakvataddhite* (1.3.8) govern initial-consonant *anubandhas* in *pratyaya*s; they do not affect dhātu citation specifically. Their inclusion would slightly affect *pratyaya* analysis but not dhātu structure.

2. **Asymmetric aspiration weighting**. The `weighted_distance` function in `analyze_distinguishability.py` uses **0.5** for voiceless-aspirated transitions (kh ↔ k) and **1.5** for voiced-aspirated transitions (gh ↔ g). These weights reflect cross-linguistic perceptual-phonetics evidence that breathy voice (the C4 column) is more perceptually salient than the puff-of-aspiration alone (the C2 column). Different weight choices would produce different distinguishability rankings and different Spearman correlations; the bundle's weight choice is documented in the script for reproducibility.

---

## Citing this bundle

If you use this bundle in research:

> Parag Tope, *Dhātupāṭha Analysis — Reproducibility Bundle* (2026), accompanying *Atomic Sanskrit* (Vol. 1 of *Second Shanti*), Chapter 10 and Appendix Part 5.

Underlying source data: `sanskrit/vyakarana` project on GitHub.

---

## License

See `LICENSE`. The scripts are MIT-licensed; the source CSV preserves its upstream attribution.
