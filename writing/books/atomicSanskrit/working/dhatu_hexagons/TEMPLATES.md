# *Dhātu-Racanā* — The Template Catalog

The catalog of abstract *varṇa*-sequence templates that *dhātus* fill. Each template — call it a **रचना (*racanā*)** in the Sanskrit register — specifies a particle count and an ordered sequence of consonant, short-vowel, and long-vowel slots. Specific *dhātus* are *fillings* of these templates.

This document is the catalog. Companion files:

- `SPEC.md` — visual grammar of the hexagon rendering (geometry, encoding channels, tiling).
- `dhatu_hexagon.py` — implementation. v1 takes bare *varṇa* lists; v2 will take template + filling.
- `../as_dhatu_hexagon_design_notes.md` — pre-build design rationale.
- `../../concepts/vyanjana_timing.md` — the ½-*mātrā* / 1-*mātrā* / 2-*mātrā* temporal grounding the template widths encode.

---

## 1. The concept

The visualization tool currently takes a specific *varṇa* sequence — e.g., `g, a, m` for गम् — and renders three hexagons. **The shape of the rendering is independent of the specific *varṇas*.** गम् (*gam*) and नम् (*nam*) and पच् (*pac*) all render with the same hexagon arrangement: narrow + medium + narrow, zigzagged. Only the colors, labels, and saturation differ.

The shape itself is the **template**. The *varṇas* are the **filling**.

A ***dhātu-racanā*** (***धातुरचना***) is a repeatable construction-template: a particle count plus an ordered sequence of consonant, short-vowel, and long-vowel slots. **CV1C** is a *racanā*. **CCV1C** is a *racanā*. Specific *dhātavaḥ* fill that template with particular *varṇas*: गम् (*gam*), नम् (*nam*), पच् (*pac*), वद् (*vad*).

The visualization can be decomposed:

- **Template** (*racanā*) = particle count + C / V1 / V2 sequence (e.g., CV1C, CCV2, V1CC). Determines layout.
- **Filling** = specific *varṇas* in each slot (e.g., {g, a, m} for the CV1C template). Determines colors, labels, and other within-hexagon encoding.

Two *dhātus* in the same *racanā* are structurally analogous — same temporal envelope, same articulatory shape, same metrical contribution. **The *dhātu-racanā* is the template. The *dhātuḥ* is the filled construction.**

### Why ***racanā***

***रचना (racanā)*** carries the right register for the book's engineering frame: it means *construction*, *composition*, *arrangement*, *formation*. The verb-stem **रच् (*rac*)** means to make, to construct, to compose. Sanskrit is not merely *shaped*; it is *constructed*. The *racanā* is the construction-template; specific *dhātus* are constructions that fill it.

The term avoids the modern-Sanskrit electron-shell connotation of ***kakṣyā*** (कक्ष्या) and avoids overloading the *vyākaraṇa* term ***ākṛti*** (आकृति) which already carries form-type connotations adjacent to but not identical to the construction-template sense.

---

## 2. The template catalog

Each template is named by its particle sequence using these tokens:

- **C** — any consonant (*vyañjana*, ½ *mātrā*)
- **V1** — any short vowel (*hrasva*, 1 *mātrā* — *a*, *i*, *u*, *ṛ*, *ḷ*)
- **V2** — any long vowel (*dīrgha*, 2 *mātrā* — *ā*, *ī*, *ū*, *ṝ*, *e*, *ai*, *o*, *au*)

A canonical Devanagari exemplar — a real *dhātu* from the *Dhātupāṭha* — anchors each template as a memorable label.

### 2.1 Two-particle templates (4 total)

| Template | Pattern | Exemplar | IAST | Gloss | Gaṇa |
|---|---|---|---|---|---|
| **CV1** | C + short V | **कृ** | *kṛ* | to do, to make | 8 |
| **CV2** | C + long V | **धा** | *dhā* | to put, to place | 3 |
| **V1C** | short V + C | **इष्** | *iṣ* | to wish, desire | 6 |
| **V2C** | long V + C | **आप्** | *āp* | to obtain | 5 |

All four 2-particle templates are populated; this is the simplest layer of the architecture. कृ is chosen as the CV1 exemplar because it is arguably the most foundational *dhātu* in Sanskrit (action / making itself, named in the *saṃskṛtam* etymology).

### 2.2 Three-particle templates (up to 6 main + variants)

| Template | Pattern | Exemplar | IAST | Gloss | Gaṇa |
|---|---|---|---|---|---|
| **CV1C** | C + short V + C | **गम्** | *gam* | to go | 1 |
| **CV2C** | C + long V + C | **वाच्** | *vāc* | to speak | 2 |
| **CCV1** | CC + short V | **श्रु** | *śru* | to hear | 5 |
| **CCV2** | CC + long V | **स्था** | *sthā* | to stand | 1 |
| **V1CC** | short V + CC | **अर्च्** | *arc* | to honor / worship | 1 |
| **V2CC** | long V + CC | **ईक्ष्** | *īkṣ* | to see | 1 |

The four main 3-particle templates (CV1C, CV2C, CCV1, CCV2) are heavily populated. V1CC and V2CC are sparser; ईक्ष् is a canonical V2CC if one counts क्ष as two *varṇas* (k + ṣ).

### 2.3 Four-particle templates

| Template | Pattern | Exemplar | IAST | Gloss | Gaṇa |
|---|---|---|---|---|---|
| **CV1CC** | C + short V + CC | **कल्प्** | *kalp* | to be fit | 1 |
| **CCV1C** | CC + short V + C | **स्मर्** | *smar* | to remember | 1 |
| **CV2CV1** | C + long V + C + short V | **बाधृ** | *bādhṛ* | to molest, oppose | 1 |
| **CV1CV2** | C + short V + C + long V | **चिती** | *citī* | to perceive | 1 |
| **CV2CC** | C + long V + CC | (rare; verify) | — | — | — |
| **CCV2C** | CC + long V + C | (rare; verify) | — | — | — |

CV1CC, CCV1C, and the disyllabic CV2CV1 are all heavily populated (see §2.5 empirical results). The two-syllable templates (CV2CV1, CV1CV2, CV1CV1, CV2CV2) emerged as a major family that the original catalog did not anticipate.

### 2.4 Total template count

- 2-particle: **4 templates**, all populated.
- 3-particle: **6 templates**, four heavily populated, two sparser.
- 4-particle: **8+ templates**, including the disyllabic CV2CV1 / CV1CV2 family.

Estimated total realistic templates: **~15–20**. The Zipfian distribution should land such that the top ~10 templates cover the majority of the *Dhātupāṭha*.

---

## 2.5 Empirical results — 2,168-entry *Dhātupāṭha* analysis (2026-05-23)

The template-classifier was run against the full *Dhātupāṭha* (`analysis/dhatupatha/scripts/analyze_shells.py`). Full results in [`analysis/dhatupatha/data/derived/template_distribution.csv`](../../analysis/dhatupatha/data/derived/template_distribution.csv) and [`template_distribution.md`](../../analysis/dhatupatha/data/derived/template_distribution.md). (The script filename retains the old `shell` dev term; the prose, reasoning, and generated outputs use *racanā* / template.)

### Headline numbers

- **Total entries:** 2,168 (after anubandha-stripping)
- **Distinct templates observed:** 69
- **The "<10 templates cover 80%" prediction:** **validated exactly** — 10 templates reach 81.27% of the corpus

### Cumulative thresholds

| Coverage | # of templates | Last template added | Reached at |
|---:|---:|---|---:|
| 50% | 3 | **CV1CC** | 56.78% |
| 75% | 8 | **CV1** | 76.34% |
| **80%** | **10** | **CCV2** | **81.27%** |
| 90% | 16 | **CV2CC** | 90.54% |
| 95% | 22 | **CV1CCV2** | 95.16% |
| 99% | 48 | **V2CCV2CV2** | 99.03% |

### Top 10 templates (the spine of the architecture)

| Rank | Template | Particles | Count | % of corpus | Cum % | Class name (dhātu) |
|---:|---|---:|---:|---:|---:|---|
| 1 | **CV1C** | 3 | 819 | 37.78 | 37.78 | ***gamādi*** (गम्) |
| 2 | **CCV1C** | 4 | 209 | 9.64 | 47.42 | ***smarādi*** (स्मर्) |
| 3 | **CV1CC** | 4 | 203 | 9.36 | 56.78 | ***kalpādi*** (कल्प्) |
| 4 | **CV2CV1** | 4 | 105 | 4.84 | 61.62 | ***bādhrādi*** (बाधृ) |
| 5 | **CV2C** | 3 | 101 | 4.66 | 66.28 | ***vācādi*** (वाच्) |
| 6 | **CV2** | 2 | 88 | 4.06 | 70.34 | ***dhādi*** (धा) |
| 7 | **V1C** | 2 | 65 | 3.00 | 73.34 | ***iṣādi*** (इष्) |
| 8 | **CV1** | 2 | 65 | 3.00 | 76.34 | ***krādi*** (कृ) |
| 9 | **CV1CV2** | 4 | 58 | 2.68 | 79.01 | ***cityādi*** (चिती) |
| 10 | **CCV2** | 3 | 49 | 2.26 | 81.27 | ***sthādi*** (स्था) |

The *-ādi* class-naming convention is documented in §2.6 below.

### Key empirical observations

**(a) CV1C dominates massively.** The canonical 3-particle CVC template (with a *short* vowel) accounts for **37.78%** of all *dhātus* on its own. This is the workhorse construction of the Sanskrit verbal architecture — गम्, पच्, वद्, भिद्, युज्, and roughly 800 others share this *racanā*.

**(b) Disyllabic templates emerged as a major family not anticipated in the original catalog.** CV2CV1 (rank 4, 105 entries) and CV1CV2 (rank 9, 58 entries) are *disyllabic* 4-particle templates — *dhātus* like बाधृ (*b-ā-dh-ṛ*), गाधृ, नाधृ, नाथृ, etc. These are not (consonant cluster + simple syllable) but (full syllable + full syllable). The original catalog focused on consonant-cluster variations of monosyllabic *dhātus*; the corpus shows that **a sixth of all *dhātus* are disyllabic** (CV2CV1 + CV1CV2 + CV1CV1 + CV2CV2 together cover ~9% of the corpus).

**(c) Short vowels dominate long vowels in most positions.** The V1 (*hrasva*) templates (CV1C, CV1CC, CCV1C, CV1, V1C) collectively dominate the corresponding V2 (*dīrgha*) templates. This confirms the prediction; the magnitude of dominance is striking — short-vowel templates outnumber long-vowel templates by roughly 4:1 across the top 20.

**(d) The long tail is real and informative.** 69 distinct templates exist, but the top 22 already reach 95.16%, leaving the remaining 47 templates to carry less than 5% of the corpus. The architecture is highly selective; most theoretical combinations are sparsely populated or empty.

**(e) The 1-particle templates exist.** Five *dhātus* are bare V1 (ऋ, उ, इ — "to go") and two are bare V2 (ई, ॠ). Pure-vowel *dhātus* are rare but not absent — the architecture allows single-*varṇa* constructions, though it does not lean on them.

**(f) The long-tail audit remains useful.** The `Yi` correction removes false *ñi* monsters; one 9-particle singleton (CCV2CCV2CCV2 = ट्वोस्फूर्जा) and several 6–7 particle singleton templates remain. These should be verified as bare *dhātus*, augmented citation forms, or residual parser edge cases before publication.

### What this means for the engineering thesis

The empirical distribution sharpens the architecture-as-engineered claim:

- **Selectivity confirmed.** Of the combinatorial possibilities the *varṇa* inventory admits, the architecture populates only 69 distinct templates in 2,168 *dhātus*. The vast majority of theoretical combinations are not used. The empty cells are not gaps; they are design selections.
- **Compactness confirmed.** ~14.5% of the distinct templates (10 of 69) carry 80% of the corpus. This is the Zipfian signature of an engineered system; a natural-language inventory would have a less concentrated distribution.
- **The top templates are the spine.** CV1C, CCV1C, CV1CC, CV2CV1, CV2C, CV2, V1C, CV1, CV1CV2, CCV2 — these ten templates are the architectural spine. Every chapter that argues "Sanskrit is built from a discrete inventory of constructions" can ground that claim in this list.
- **The disyllabic templates deserve their own treatment.** The catalog above (§2.1–2.4) focuses on monosyllabic templates with consonant-cluster variations. The empirical data shows that ~9% of *dhātus* are disyllabic. Future revisions should expand the catalog to include the CV2CV1, CV1CV2, CV1CV1, CV2CV2 family as a distinct category.

---

## 2.6 Class names — the *-ādi* convention

Each of the top 10 templates carries a canonical class name following Pāṇini's own *gaṇa*-naming pattern (***bhvādi***, ***adādi***, ***juhotyādi***, ***divādi***, ***svādi***, ***tudādi***, ***rudhādi***, ***tanādi***, ***kryādi***, ***curādi*** — each *gaṇa* named after its canonical *dhātu* suffixed with ***-ādi***, "starting with X / the X-class"). The template class names follow the same convention: identify the canonical *dhātu*, apply Pāṇinian sandhi where the *dhātu* ends in a vowel, suffix *-ādi*.

| Rank | Template | Class name | Devanagari | Canonical *dhātu* | Sandhi rule |
|---:|---|---|---|---|---|
| 1 | CV1C | ***gamādi*** | गमादि | गम् (*gam*, to go; gaṇa 1) | consonant-final stem; no vowel sandhi |
| 2 | CCV1C | ***smarādi*** | स्मरादि | स्मर् (*smar*, to remember; gaṇa 1) | consonant-final stem; no vowel sandhi |
| 3 | CV1CC | ***kalpādi*** | कल्पादि | कल्प् (*kalp*, to be fit; gaṇa 1) | consonant-final stem; no vowel sandhi |
| 4 | CV2CV1 | ***bādhrādi*** | बाध्रादि | बाधृ (*bādhṛ*, to oppose; gaṇa 1) | ṛ → r before vowel (*iko yaṇ aci*, 6.1.77) |
| 5 | CV2C | ***vācādi*** | वाचादि | वाच् (*vāc*, to speak; gaṇa 2) | consonant-final stem; no vowel sandhi |
| 6 | CV2 | ***dhādi*** | धादि | धा (*dhā*, to put, place; gaṇa 3) | ā + ā → ā (savarṇa-dīrgha, 6.1.101) |
| 7 | V1C | ***iṣādi*** | इषादि | इष् (*iṣ*, to wish, desire; gaṇa 6) | consonant-final stem; no vowel sandhi |
| 8 | CV1 | ***krādi*** | क्रादि | कृ (*kṛ*, to do, make; gaṇa 8) | ṛ → r before vowel (*iko yaṇ aci*, 6.1.77) |
| 9 | CV1CV2 | ***cityādi*** | चित्यादि | चिती (*citī*, to perceive; gaṇa 1) | ī → y before vowel (*iko yaṇ aci*, 6.1.77) |
| 10 | CCV2 | ***sthādi*** | स्थादि | स्था (*sthā*, to stand; gaṇa 1) | ā + ā → ā (savarṇa-dīrgha, 6.1.101) |

### Avoiding clashes with Pāṇini's *gaṇa* names

Three obvious canonical *dhātus* are deliberately *not* used because their *-ādi* forms collide with established *gaṇa* names:

- ***bhū*** → *bhvādi* collides with *gaṇa* 1 (the *bhū*-class). CV2 takes ***dhādi*** instead.
- ***ad*** → *adādi* collides with *gaṇa* 2 (the *ad*-class). V1C takes ***iṣādi*** instead.
- ***krī*** → *kryādi* collides with *gaṇa* 9 (the *krī*-class). CCV2 takes ***sthādi*** instead — though *krī* is itself CCV2 by particle count, the *kryādi* name is reserved for the *gaṇa*.

Other Pāṇinian *gaṇa* names — *juhotyādi*, *divādi*, *svādi*, *tudādi*, *rudhādi*, *tanādi*, *curādi* — do not collide with any canonical-*dhātu* candidate for the top 10 templates, so no further avoidance is required. The convention reads cleanly without ambiguity against Pāṇini's existing names.

### Two-layer naming — *gaṇa* and *racanā*

A *dhātu* like *vāc* belongs to *gaṇa* 2 (***adādi***, the inflectional class) *and* sits in the ***vācādi*** template (CV2C, the phonological class). The same *dhātu* carries two classifications at two different layers — one morphological / inflectional, one phonological / shape-based. The two layers are independent; a *dhātu* can be classified under both without contradiction.

Where the canonical *dhātus* of the two layers happen to be the same (would have been *adādi* for both *gaṇa* 2 and V1C; *bhvādi* for both *gaṇa* 1 and CV2; *kryādi* for both *gaṇa* 9 and CCV2), the *gaṇa* name takes precedence — Pāṇini established it first — and the template takes the next-most-canonical *dhātu* as its name. This is the avoidance described above. The naming convention is consistent across both layers; only the canonical-*dhātu* exemplars differ where needed.

### Why ***-ādi***

The *-ādi* convention does three things at once:

1. **Anchors the template in the corpus.** Each class name encodes its canonical *dhātu*. A reader who knows the *dhātu* knows the template's shape.
2. **Imports Pāṇini's grammatical register.** The convention is the *paramparā*'s own classificatory grammar; using it for templates places the catalog inside the tradition's vocabulary rather than alongside it.
3. **Scales cleanly.** New templates discovered in expanded corpora (Gītā / Vedic subsets, see `working/as_author_tasks.md`) can be named on the same pattern: identify the canonical *dhātu*, apply sandhi, suffix *-ādi*.

The ten class names above are the catalog's anchors; additional templates beyond the top 10 follow the same convention.

---

## 3. Empty templates — the architectural signal

The combinatorial possibilities not represented above are themselves analytically interesting. Sanskrit's *sandhi* system prevents adjacent vowels in continuous text; no bare *dhātu* has a V1V1, V1V2, V2V1, or V2V2 sequence at the surface. The templates V1V1, V1V2, CV1V1, CV2V2, V1CV1, V1CV2, V2CV1, V2CV2, etc. are all **structurally empty** — not because the corpus happens to lack examples, but because the architecture's *sandhi* rules disallow them.

**Sandhi is a template selector.** It restricts which combinatorial possibilities the architecture allows. The empty cells in the template catalog map directly onto the cells *sandhi* forbids.

A natural language would populate the combinatorial space roughly evenly, with some patterns more or less common but no large structural gaps. An engineered language *selects* a subset of templates consistent with its design constraints (timing balance, articulatory accessibility, sandhi rules, semantic-load distribution) and ignores the rest.

The empty cells are not failures of analysis. They are the architecture's selections made visible by negative space.

This is the same logic as the *varṇamālā*'s exclusion of the alveolar row (Ch 9): the architecture *could* include it; it chooses not to, because the inclusion would compromise acoustic distinguishability. The template catalog's empty cells are the same engineering decision at a different layer — what configurations of *varṇas* the architecture is willing to construct into a *dhātu*.

---

## 4. How the statistical analysis shifts

The original "<10 shapes cover 80% of *Dhātupāṭha*" claim used the basic C / V skeleton without distinguishing V1 / V2. With V1 / V2 split, the analysis changes in three ways:

### 4.1 More bins, finer Zipfian

The template count grows from ~5 basic shapes to ~15–20 populated templates (or 69 distinct templates total, including the long tail — see §2.5). The Zipfian distribution persists at the finer granularity: a small number of templates dominate; the rest are sparse-to-empty. The "top N covers 80%" threshold lands at 10 templates (validated empirically in §2.5).

### 4.2 V1 dominates V2 in most positions

Short vowels are more frequent than long vowels in the *Dhātupāṭha*. Most *dhātu* constructions use V1 (specifically *a*, *i*, *u*, *ṛ*) as their main vowel; V2 vowels appear most often in monosyllabic stems (धा, स्था, भू, सू) and some specific patterns. Confirmed empirically (§2.5) — short-vowel templates outnumber long-vowel templates by roughly 4:1 across the top 20.

### 4.3 Empty templates are quantitatively analyzable

The negative-space argument (§3) becomes a measurable claim: count the empty / near-empty templates, characterize *why* they are empty (sandhi forbids, articulatory difficulty, no semantic precedent, etc.), and present the structural reasons. This is appendix-grade material.

---

## 5. The visualization tool — v2 refactor

`dhatu_hexagon.py` v1 takes a bare *varṇa* list and renders. v2 should split the input into template + filling:

```python
# v2 input model
TEMPLATES = {
    "CV1":  {"pattern": "CV1",  "exemplar": "कृ",   "iast": "kṛ",   "gana": 8},
    "CV2":  {"pattern": "CV2",  "exemplar": "धा",   "iast": "dhā",  "gana": 3},
    "V1C":  {"pattern": "V1C",  "exemplar": "अद्",  "iast": "ad",   "gana": 2},
    # ... etc.
}

def classify(particles):
    """Return the template name for a varṇa list (or 'UNKNOWN' for templates not in catalog)."""
    pattern = "".join("C" if p["class"] == "C" else p["class"] for p in particles)
    return pattern_to_template_name(pattern)

def render(template_name, filling):
    """Render the named template filled with specific varṇas."""
    template = TEMPLATES[template_name]
    return apply_layout(template, filling)
```

This refactor enables:

- **Template-based catalogs.** A page showing the "periodic table of *racanās*" — all populated templates with their canonical exemplars, organized by particle count and pattern. High-value figure for the manuscript appendix.
- **Template-filling visualization.** Pick a *racanā* and show 5–10 *dhātus* that fill it, demonstrating how the same template carries different specific *varṇas*. Useful for chapter prose ("these all have the same construction; only the content varies").
- **Empty-template visualization.** A template rendered with a placeholder + a note "no *dhātu* fills this template because *sandhi* forbids V1V2 sequences." Makes the negative-space argument visible.

The template-catalog page is the strongest single visualization the tool can produce. It compresses the architecture's selection rules into one image.

---

## 6. Empirical verification — methodology

(Now executed — see §2.5 for results. This section documents the method.)

The analysis runs against `../../analysis/dhatupatha/data/dhatupatha.csv`:

1. **For each *dhātu*:** strip *anubandhas* per *Aṣṭādhyāyī* 1.3.2, 1.3.3, 1.3.5 (the same parser logic `as_3_05_by_the_numbers.md` §5.1 uses).
2. **For each underlying form:** classify each *varṇa* as C / V1 / V2 using the IAST → category map (vowels long-or-short by their IAST diacritic; consonants are C).
3. **Build the template label:** concatenate the per-*varṇa* classifications (e.g., `CV1C` for *gam*).
4. **Tally:** count *dhātus* per template across all 2,168 entries.
5. **Sort:** descending by count.
6. **Cumulative:** compute cumulative percentage; identify the threshold (top N templates covering 80% / 90% / 95%).
7. **Empty cells:** enumerate the theoretical combinatorial templates (2-particle: 4; 3-particle: 18 = 2 × 3 × 3; 4-particle: many) and identify which are unpopulated.
8. **Per-*gaṇa* breakdown:** does each *gaṇa* show distinctive template distributions? (Some *gaṇas* may be heavily CV1 / CV2C, others CCV1, etc.)

The analysis bundle `analysis/dhatupatha/` has the parser + 2,168-entry corpus + the new template-classifier script.

### 6.1 Additional parameters to track

The template count is only the first pass. Before this analysis is promoted into Ch 10 prose or an appendix figure, track the following parameters so the *racanā* claim remains architectural rather than merely descriptive:

1. **Particle count.** Keep the existing 1 / 2 / 3 / 4 / 5+ particle distribution. This is the compression axis: how many sound-particles the atom requires.
2. ***Mātrā* envelope.** Convert each template into timing weight using C = ½ *mātrā*, V1 = 1 *mātrā*, V2 = 2 *mātrās*. CV1C and V2 are both small by particle count, but they do not have the same temporal profile.
3. ***Akṣara* count.** Separate monosyllabic templates from disyllabic and longer templates. The empirical data shows CV2CV1 / CV1CV2 / CV1CV1 / CV2CV2 form a real disyllabic family; do not collapse them into generic 4-particle forms.
4. **Vowel nucleus.** Track the actual vowel occupying the V1 / V2 slot, not only the length class. The four-vowel reactive core (*a, i, u, ṛ*) is a separate architectural signal, with *ṛ* needing its own treatment.
5. **Onset / coda / inner-cluster roles.** For each template, classify consonant positions as release, closure, and bonding positions. This connects the *racanā* catalog to Ch 10's position-role / subatomic-periodicity analysis.
6. **Place-of-articulation path.** Track the movement through *sthāna* across the template: same-place repetition, front-to-back movement, back-to-front movement, retroflex involvement, and compound-site participation. This is where the same-place suppression argument should live inside the template analysis.
7. **Cluster topology.** Distinguish CC-before-vowel, CC-after-vowel, CCC clusters, *kṣa* clusters, semivowel-bonded clusters, and nasal clusters. The raw template label says "CC"; the architecture may treat different CC types differently.
8. **Empty and near-empty templates.** Record which theoretical templates are unpopulated or almost unpopulated, then classify why: *sandhi* exclusion, articulatory crowding, acoustic indistinguishability, semantic redundancy, or likely parser / anubandha issue. Negative space is part of the evidence.
9. **Per-*gaṇa* distribution.** Track which *racanāḥ* each *gaṇa* favors. If the ten *gaṇāḥ* carry distinctive template profiles, then Pāṇini's inflectional classes preserve phonological-shape information as well as conjugational behavior.
10. **Productivity by template.** Join template class to derivative productivity. The key question: do compact templates generate more *śabdāḥ*, or do certain longer templates carry specialized high-value functions?
11. **Cross-corpus usage.** Compare the *Dhātupāṭha* inventory against actual deployment in the Vedas, *Bhagavad Gītā*, *Rāmāyaṇa*, and later corpora. Inventory selection and usage selection may not be identical.
12. **Cross-recension stability.** Compare template distributions across *Dhātupāṭha* recensions where available. Stable distributions across recension variance would strengthen the claim that the templates reflect architecture, not editorial accident.
13. ***Anubandha* audit.** Initial *ñi* / *ṭu* / *ḍu* stripping is standardized as `Yi`, `wu`, `qu` (2026-05-23). Keep all scripts on the same table; the remaining audit target is the long-tail edge cases and any non-1.3.5 *it*-marker behavior.

---

## 7. Open questions

- **Canonical exemplar selection.** The tables above pick one exemplar per template. The empirical analysis (§2.5) confirms the predicted exemplars for the top-populated templates; some sparser templates still need exemplar verification.
- **Boundary cases.** क्ष (kṣa) — one *varṇa* or two? Pāṇinian analysis treats it as two; some traditions as one. The C / V tokenization settles this for the parser as two *varṇas* (k + ṣ), consistent with the engineering thesis's atomicity argument.
- **Three-consonant clusters (CCC).** Bare *dhātu* CCC patterns are rare but exist. Verify whether the remaining long-tail cluster templates are bare *dhātus* or augmented citation forms with un-stripped *it*-markers.
- **Halant-bearing dhātus.** Many *Dhātupāṭha* entries cite the *dhātu* in citation form (with *it*-markers / *anubandhas*). The template classification operates on the *stripped* form. The parser strips per Pāṇini 1.3.2 / 1.3.3 / 1.3.5; the corrected long tail still suggests some edge cases may need additional handling.
- **Per-*gaṇa* template distributions.** Do certain *gaṇas* favor certain templates? The per-*gaṇa* breakdown in `template_distribution.md` shows that yes — gaṇa 1 (*bhvādi*) is dominated by CV1C; gaṇa 10 (*curādi*) shows a different distribution. Worth a dedicated analysis.
- **Cross-*śākhā* invariance.** If different *Dhātupāṭha* recensions list slightly different *dhātus* (Mādhavīya vs Siddhānta-Kaumudī vs Kṣīrasvāmin), do the template distributions remain stable? Stability would confirm that the template catalog reflects an underlying architecture rather than a recension-specific quirk.
- **Gītā / Vedic subset analysis.** Run the same template-classifier against the ~500 *dhātus* listed for the *Bhagavad Gītā* and the *Vedas* (queued in `working/as_author_tasks.md`). Compare distributions: does usage match the inventory, or does the inventory exceed actual usage?

---

## 8. Why this catalog matters

The template catalog gives the engineering thesis a quantitative spine at the *dhātu* layer. Three claims become testable, and all three are confirmed by the empirical results in §2.5:

1. **The architecture is selective.** Empty templates exist; *sandhi* and other rules forbid certain combinations. The corpus inhabits 69 of the theoretically infinite combinatorial templates, with a heavy concentration in the top 10.
2. **The architecture is compact.** 10 of the 69 templates carry 80% of the corpus. The selection is not arbitrary — the populated cells obey the engineering constraints (timing, articulation, sandhi).
3. **The templates abstract over content.** Two *dhātus* in the same *racanā* are structurally analogous — same temporal envelope, same articulatory shape, same metrical contribution. The template, not the specific *varṇa* content, is what the metrical and grammatical systems operate on.

Each of these is appendix-grade material. §2.5 gives the empirical numbers; the catalog tables (§2.1–2.4) give the conceptual framework.

---

## 9. Cross-references

- **`SPEC.md`** — visual grammar of the hexagon rendering. The template-as-layout-template observation lives here as a future v2 deployment.
- **`dhatu_hexagon.py`** — the implementation. v1 takes bare *varṇa* lists; v2 will take template + filling.
- **`../as_dhatu_hexagon_design_notes.md`** — pre-build design rationale that flagged the "<10 shapes cover 80%" claim. This document refines that claim with the V1 / V2 distinction and confirms it empirically.
- **`../../concepts/vyanjana_timing.md`** — the ½-*mātrā* / 1-*mātrā* / 2-*mātrā* temporal grounding. The templates encode these durations in their width pattern.
- **`../../analysis/dhatupatha/`** — the corpus and parser bundle that the empirical verification (§2.5) draws on. Script: `scripts/analyze_shells.py`. Output: `data/derived/template_distribution.csv` and `data/derived/template_distribution.md`. (The script filename retains the old `shell` dev term; the generated outputs use *racanā* / template.)
- **`../../as_3_05_by_the_numbers.md`** — Appendix Part 5; the existing numerical analysis of the *Dhātupāṭha*. The template-distribution analysis extends this with the V1 / V2 axis.
- **Manuscript chapters** Ch 10 (*Building the Dhātuḥ*) and Ch 11 (*Periodic Table of Gaṇāḥ*) — natural deployment sites for the template-catalog figure when the empirical work matures.

---

*Last updated: 2026-05-23. Terminology shift from "shell" / "ākṛti" to "template" / "racanā" applied this revision. Open for refinement as exemplars are verified and the disyllabic family is catalogued.*
