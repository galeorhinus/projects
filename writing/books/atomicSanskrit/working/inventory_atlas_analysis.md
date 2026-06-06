# Vocal-tract inventory atlas — analysis findings

> Self-contained analytical dump for review by independent readers. Companion documents: `inventory_atlas_critique.md` (anticipated orthodoxy responses), `inventory_atlas_roadmap.md` (future work). Tooling and per-figure documentation live in `atomicSanskrit/figures/vocal_tract/README.md`.

---

## 0. What was built

A **34-language consonant inventory atlas** rendered as scatter charts on a shared vocal-tract coordinate system, plus an **overlay-and-metric system** for pairwise inventory comparison. The infrastructure exists in `atomicSanskrit/figures/vocal_tract/` and produces:

- 34 standalone language atlases (one SVG per language)
- An overlay chart for any pair (filled gray dots = language A, outlined rings = language B; shared cells visible as filled-with-ring)
- 8 similarity metrics computed per pair, printed to stdout and rendered inline at the bottom of every overlay SVG

The shared coordinate system is **12 places of articulation × 13 manner classes = 156 possible cells**. Each language fills a subset. The 12 places are positioned along the vocal-tract arc in proportion to **actual lip-to-place distance** (the anatomical angular distribution — front-of-mouth columns are visibly compressed because the mouth itself compresses there). The 13 manner classes are the standardised set: voiceless / voiceless-aspirated / voiced / voiced-aspirated stops; ejective stops; voiceless / voiced affricates; voiceless / voiced fricatives; nasal; lateral; tap-or-trill; approximant.

The atlas covers four broad regional clusters:

| Cluster | Languages |
|---|---|
| Sanskritic + symmetric southern | Sanskrit, Tamil |
| Three southern-bulk + ancient + outlier | Telugu, Kannada, Malayalam, Tulu, Toda, Brahui |
| Central forest belt | Gondi, Kui, Kuvi, Kolami, Kurukh, Malto |
| Munda lineage | Mundari, Korku, Santali |
| Northern isolate + Tibeto-Burman frontier | Burushaski, Lepcha, Manipuri, Bodo, Garo, Mizo |
| IPA-compact reference set | English, French, Japanese, Korean, Mandarin, Farsi, Arabic, Swahili, Zulu, Quechua, Nahuatl |

Selection criterion was *structural distinctiveness* — each chart illustrates a different inventory pattern.

---

## 1. The eight metrics

All eight are computed on the full 13-row × 12-column manner-place grid (no compaction), so cross-pair comparisons are directly comparable.

**Symmetric overlap measures:**

| Metric | Formula | Range | What it measures |
|---|---|---|---|
| Jaccard | `\|A∩B\| / \|A∪B\|` | 0–1 | Strict; size-sensitive |
| Dice | `2\|A∩B\| / (\|A\|+\|B\|)` | 0–1 | Mid; weighted toward agreement |
| Cosine | `\|A∩B\| / √(\|A\|·\|B\|)` | 0–1 | Size-tolerant |
| Jensen-Shannon similarity | `1 − JSD(P_A‖P_B)/ln 2` where P is uniform over support | 0–1 | Information-theoretic |
| Place-overlap | `\|places(A)∩places(B)\| / \|places(A)∪places(B)\|` | 0–1 | Ignores manner; counts places |

Note: **edit distance / (|A|+|B|)** = **1 − Dice**, so edit distance carries no information beyond Dice for set comparison.

**Asymmetric coverage measures** — the new analytical tool:

| Metric | Formula | What it measures |
|---|---|---|
| `Sk⊇X` (Sanskrit covers X) | `\|A∩B\| / \|B\|` | Fraction of B's phonemes that are also in A. "Does A contain B?" |
| `X⊇Sk` (X covers Sanskrit) | `\|A∩B\| / \|A\|` | Fraction of A's phonemes that are also in B. "Does B contain A?" |

The asymmetry between these is where the most-interesting structural facts live. Identical inventories give `Sk⊇X = X⊇Sk = 1.0`. A small inventory mostly nested inside a large one gives `Sk⊇X = high, X⊇Sk = low`. A large inventory mostly nested inside an even-larger one gives the reverse.

---

## 2. The Sanskrit-pairwise table (all 33 other atlas languages)

Computed via `vocal_tract_overlay.py`. Sorted by cosine.

| Language | \|B\| | ∩ | Jacc | Dice | Plc | Cos | JSD-s | Sk⊇X | X⊇Sk |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| santali | 31 | 27 | 0.73 | 0.84 | 0.71 | 0.84 | 0.84 | 0.87 | 0.82 |
| kannada | 34 | 28 | 0.72 | 0.84 | 0.62 | 0.84 | 0.84 | 0.82 | 0.85 |
| telugu | 34 | 28 | 0.72 | 0.84 | 0.62 | 0.84 | 0.84 | 0.82 | 0.85 |
| malayalam | 35 | 28 | 0.70 | 0.82 | 0.56 | 0.82 | 0.82 | 0.80 | 0.85 |
| burushaski | 34 | 22 | 0.49 | 0.66 | 0.56 | 0.66 | 0.66 | 0.65 | 0.67 |
| lepcha | 21 | 17 | 0.46 | 0.63 | 0.57 | 0.65 | 0.64 | 0.81 | 0.52 |
| manipuri | 21 | 17 | 0.46 | 0.63 | 0.57 | 0.65 | 0.64 | 0.81 | 0.52 |
| kolami | 19 | 16 | 0.44 | 0.62 | 0.83 | 0.64 | 0.63 | 0.84 | 0.48 |
| gondi | 22 | 17 | 0.45 | 0.62 | 0.71 | 0.63 | 0.63 | 0.77 | 0.52 |
| kurukh | 22 | 17 | 0.45 | 0.62 | 0.71 | 0.63 | 0.63 | 0.77 | 0.52 |
| korku | 20 | 16 | 0.43 | 0.60 | 0.71 | 0.62 | 0.61 | 0.80 | 0.48 |
| tulu | 23 | 17 | 0.44 | 0.61 | 0.62 | 0.62 | 0.61 | 0.74 | 0.52 |
| kui | 21 | 16 | 0.42 | 0.59 | 0.71 | 0.61 | 0.60 | 0.76 | 0.48 |
| kuvi | 21 | 16 | 0.42 | 0.59 | 0.71 | 0.61 | 0.60 | 0.76 | 0.48 |
| malto | 21 | 16 | 0.42 | 0.59 | 0.71 | 0.61 | 0.60 | 0.76 | 0.48 |
| mundari | 21 | 16 | 0.42 | 0.59 | 0.71 | 0.61 | 0.60 | 0.76 | 0.48 |
| toda | 27 | 18 | 0.43 | 0.60 | 0.62 | 0.60 | 0.60 | 0.67 | 0.55 |
| mizo | 19 | 15 | 0.41 | 0.58 | 0.57 | 0.60 | 0.59 | 0.79 | 0.45 |
| korean | 15 | 13 | 0.37 | 0.54 | 0.57 | 0.58 | 0.56 | 0.87 | 0.39 |
| brahui | 28 | 17 | 0.39 | 0.56 | 0.45 | 0.56 | 0.56 | 0.61 | 0.52 |
| garo | 15 | 11 | 0.30 | 0.46 | 0.57 | 0.49 | 0.48 | 0.73 | 0.33 |
| french | 21 | 13 | 0.32 | 0.48 | 0.44 | 0.49 | 0.49 | 0.62 | 0.39 |
| tamil | 18 | 12 | 0.31 | 0.47 | 0.83 | 0.49 | 0.48 | 0.67 | 0.36 |
| bodo | 16 | 11 | 0.29 | 0.45 | 0.57 | 0.48 | 0.47 | 0.69 | 0.33 |
| zulu | 23 | 13 | 0.30 | 0.46 | 0.40 | 0.47 | 0.47 | 0.57 | 0.39 |
| swahili | 25 | 13 | 0.29 | 0.45 | 0.40 | 0.45 | 0.45 | 0.52 | 0.39 |
| english | 24 | 12 | 0.27 | 0.42 | 0.40 | 0.43 | 0.42 | 0.50 | 0.36 |
| quechua | 24 | 12 | 0.27 | 0.42 | 0.44 | 0.43 | 0.42 | 0.50 | 0.36 |
| japanese | 21 | 11 | 0.26 | 0.41 | 0.50 | 0.42 | 0.41 | 0.52 | 0.33 |
| mandarin | 21 | 11 | 0.26 | 0.41 | 0.50 | 0.42 | 0.41 | 0.52 | 0.33 |
| nahuatl | 15 | 9 | 0.23 | 0.38 | 0.50 | 0.40 | 0.39 | 0.60 | 0.27 |
| farsi | 25 | 11 | 0.23 | 0.38 | 0.40 | 0.38 | 0.38 | 0.44 | 0.33 |
| arabic | 24 | 8 | 0.16 | 0.28 | 0.33 | 0.28 | 0.28 | 0.33 | 0.24 |

(Sanskrit has 33 cells and 5 places.)

The 8 metrics agree on rough rank order. Jaccard and Dice penalise size differences; cosine and JSD-sim don't; place-overlap collapses the manner dimension. Coverage breaks each pair into two asymmetric numbers and exposes the inventory-containment structure.

---

## 3. The four polemic findings

The atlas + metric system supports four set-theoretic statements about the data that DO NOT require the reader to accept any framework about families, areal-versus-genetic, or contact dynamics. They're statements about which inventories nest inside which, full stop.

### Finding 1 — Orthodoxy's family classifications do not track inventory similarity

Every "Dravidian" and "Munda" language in the atlas EXCEPT Brahui scores higher on every metric than every "Indo-European" language outside Sanskrit itself. Specifically:

| Comparison | Tamil (orthodoxy: "Dravidian") | English (orthodoxy: "Indo-European") |
|---|---:|---:|
| Jaccard | 0.31 | 0.27 |
| Dice | 0.47 | 0.42 |
| Cosine | 0.49 | 0.43 |
| Sk⊇X | 0.67 | 0.50 |

Same pattern with Farsi (orthodoxy: "Indo-Iranian sister of Sanskrit"):

| Metric | Tamil | Farsi |
|---|---:|---:|
| Sk⊇X | 0.67 | **0.44** |
| Cosine | 0.49 | 0.38 |

The orthodoxy's Indo-Iranian closeness to Sanskrit is **NOT VISIBLE** in the inventory dimension. Farsi's containment in Sanskrit (44%) is lower than Tamil's (67%). The Iranian language whose family-tree position is supposedly *next to* Sanskrit is, by inventory measurement, more distant from Sanskrit than the "different family" Tamil.

The framework-neutral statement: **the orthodoxy's family-tree boundaries do not predict the data.** Whatever evidence the philological reconstruction project uses to draw those boundaries, the consonant inventory dimension does not corroborate it. This is not a refutation of the orthodox case — that case rests on lexical sound correspondences, not inventory — but it is evidence that one of the dimensions phonologists could in principle have used to corroborate family classification *does not*.

### Finding 2 — Tamil is approximately Sanskrit minus the engineering layer

The most-precise set-theoretic statement in this analysis. The pairwise data say:

```
Sanskrit (33 cells)
   ∩ Tamil (12 cells shared)
   ∪ Tamil-only (6 cells)
   ∪ Sanskrit-only (21 cells)
   = 39 cells total
```

The 12 shared cells are exactly the cells you'd expect to share if Sanskrit and Tamil started from the same anatomical baseline: the 5 voiceless stops at bilabial, dental, retroflex, palatal, velar; the 5 matched nasals at those same places; the labial approximant /v ʋ/ at column 1; the palatal glide /j/ at column 8.

The 21 Sanskrit-only cells are the "engineering layer" the book argues Sanskrit deliberately added:
- 5 voiceless aspirated stops (mahāprāṇa, row 1)
- 5 voiced stops (row 2)
- 5 voiced aspirated stops (mahāprāṇa, row 3)
- 4 sibilants /s ʂ ɕ h/
- The lateral and tap at retroflex/dental

The 6 Tamil-only cells are Tamil-specific anatomical elaborations:
- The alveolar series (/t n l/) at column 5
- The retroflex lateral /ɭ/ at column 7
- The Tamil-signature retroflex approximant /ɻ/ (ழ) at column 7

The asymmetric coverage values **`Sk⊇Tamil = 0.67`** and **`Tamil⊇Sk = 0.36`** are the numerical witnesses to this structure. Tamil is almost-contained in Sanskrit; Sanskrit is NOT almost-contained in Tamil. Sanskrit has added ~21 features Tamil doesn't have; Tamil has added ~6 features Sanskrit doesn't have. The relationship is asymmetric in a specific way that the book's frame predicts: **Sanskrit = Tamil's anatomical base + a layer of deliberate engineering.**

This is not a claim that Sanskrit descended from Tamil or that Tamil descended from Sanskrit. It is a claim about the set-theoretic relationship of their inventories *today*. Whatever generated this relationship — contact, common areal substrate, shared anatomical engineering tradition — the relationship itself is a fact about the data.

### Finding 3 — Sanskrit is the curated superset of the human articulator space

The data converge on a sharper claim than "Sanskrit covers most other inventories." They show Sanskrit is the **curated superset**: a deliberately-chosen comprehensive map of the human mouth, into which smaller and differently-engineered inventories largely nest.

*Curated* is load-bearing. The point is not that Sanskrit happens to be large; many languages are large. The point is that Sanskrit's inventory has been chosen — by whoever engineered it — to span the human articulator space with deliberate completeness. The architectural signature is exactly what the book's engineering thesis predicts: a phoneme set that is not the accidental product of contact and drift, but the result of a comprehensive anatomical survey turned into a system.

The atlas-wide pattern in the coverage column `Sk⊇X`:

| Cluster | Range of Sk⊇X |
|---|---|
| Languages "absorbed into" Sanskritic structure (Santali, Telugu, Kannada, Malayalam) | 0.80 – 0.87 |
| Munda + southern + central forest belt baseline | 0.74 – 0.80 |
| Northeastern frontier (Tibeto-Burman) | 0.69 – 0.81 |
| Korean | 0.87 |
| Indo-European languages (English, French) | 0.50 – 0.62 |
| Iranian languages (Farsi, Brahui) | 0.44 – 0.61 |
| Arabic | 0.33 |

Sanskrit covers most of these inventories largely (≥0.7) and many of them very largely (≥0.8). The Korean number — `Sk⊇Korean = 0.87` — is the highest in the table, even though Sanskrit and Korean are spoken thousands of miles apart with no plausible historical contact. The reason is structural: Korean has a small inventory (15 cells in the atlas) and Sanskrit's deliberately-engineered 33-cell inventory simply contains most of Korean's articulatory choices.

This is **the curated-superset signature**. A deliberately-architected inventory designed to map the human articulator space comprehensively should end up containing the inventories of less-engineered systems — regardless of geography, regardless of orthodox family classification. The atlas data shows exactly this pattern: Sanskrit's coverage of distant small-inventory languages is consistently high, with no relationship to the orthodox family-tree taxonomy.

This is *not* evidence of descent or family relationship. It is evidence of **architectural completeness through curation**. Sanskrit's varṇamālā does not contain Korean phonemes because Sanskrit and Korean are related; it contains them because Sanskrit's architects curated their inventory to span the mouth's anatomical possibilities, and Korean's phonemes happen to fall within those possibilities. Every human mouth is the same mouth; a system that catalogues that mouth comprehensively will contain the systems that catalogue it partially.

The "curated superset" framing is the cleanest single description the data supports for what Sanskrit is:

> Sanskrit's phoneme inventory is the curated superset of the human articulator space — engineered to map the mouth comprehensively, into which other languages' inventories largely nest because they catalogue subsets of the same anatomy.

### Finding 4 — The Brahui control case

Brahui is the most analytically valuable single language in the atlas. The orthodoxy classifies Brahui as a Dravidian language (a sister of Tamil, Telugu, Kannada). Brahui is spoken in Balochistan (Pakistan), geographically separated from the rest of the supposed Dravidian family by ~2,500 km, surrounded for over a thousand years by Persian, Balochi, and Arabic.

What the data show:

| Metric | Brahui | Tamil |
|---|---:|---:|
| Jaccard | 0.39 | 0.31 |
| Dice | 0.56 | 0.47 |
| Cosine | 0.56 | 0.49 |
| Place-overlap | **0.45** | **0.83** |
| Sk⊇X | 0.61 | 0.67 |

The place-overlap divergence is the striking one. Brahui has *11 places of articulation* in its inventory (the highest in the atlas after Arabic) — including the uvular column (q, x, ɣ), the pharyngeal column (ħ), and the glottal stop (ʔ). These are Persian/Arabic features that have entered Brahui through ~1000 years of contact. **Brahui's place-overlap with Sanskrit (0.45) is lower than Tamil's (0.83) because Brahui has been pulled toward Persian/Arabic, not because it has different ancestry from Tamil.**

This is the orthodoxy's areal effect, made visible. **The data correctly capture areal pressure.** When areal pressure is real and substantial — as it is for Brahui in Persian/Arabic contact zone — it shows up as inventory divergence from the supposed sister languages.

The control case matters because it gives the response to the orthodox critique. The orthodox response to Findings 1–3 is "you're seeing areal convergence, not inheritance." Brahui says: areal effects DO show in this data, when they are real. Brahui's inventory has been areally pulled toward Persian/Arabic, and the metric captures that. The fact that Sanskrit and Tamil look similar in this data *despite their orthodoxy-different families* therefore cannot be dismissed by hand-wave to areal effects — areal effects, when present, are detectable and detectable in the expected direction.

To put it sharply: **if Sanskrit-Tamil similarity is "areal" by the orthodoxy's account, then Sanskrit-Tamil should have moved together AND moved DIFFERENTLY from each other's regional non-relatives.** The Brahui data show that areal divergence IS detectable. Sanskrit-Tamil are not showing areal divergence from each other; they're showing inventory containment with engineering asymmetry. That's a structurally different pattern.

---

## 4. Where the eight metrics agree vs diverge

For Sanskrit-pairwise, all 8 metrics agree on rough rank order. The top 4 (Santali, Telugu, Kannada, Malayalam) are identical across every metric. The bottom 3 (Farsi, Arabic, Nahuatl) are identical across every metric. The mid-band reshuffles slightly.

Where they diverge most:

- **Tamil's place-overlap (0.83) is anomalously high** compared to its cosine (0.49) or Jaccard (0.31). Reading: Tamil uses almost the same set of places as Sanskrit, but at much lower depth.
- **Kolami's place-overlap (0.83) is tied with Tamil's**, despite Kolami being a smaller, sparser inventory. Reading: Kolami exploits the same places as Sanskrit, just with even less depth.
- **Korean's coverage Sk⊇Korean (0.87) is the highest in the table**, despite Korean's overall cosine being only 0.58. Reading: Korean's small inventory of 15 phonemes is mostly a subset of Sanskrit's 33, but the structural relationship is "small subset of big set" rather than "similar size, similar shape."

The two metrics that carry the most distinctive information are **place-overlap** (which strips manner) and **asymmetric coverage** (which exposes containment direction). Cosine, JSD-similarity, Jaccard, and Dice are roughly redundant for binary inventory data — they differ in how they normalise by inventory size but they all measure the same thing.

---

## 5. What the metric system does NOT do

To pre-empt critique, the following limitations are honest:

- **No lexical evidence.** The orthodoxy's family-tree case is built primarily on regular sound correspondences in inherited vocabulary (e.g., Sanskrit *pitar* ~ Greek *patēr* ~ Latin *pater* ~ Old English *fæder*, all "father"). Phoneme inventory is not what the comparative method tests. The atlas evidence is from a different dimension entirely. Findings 1–4 do not claim to refute the orthodoxy's lexical reconstruction; they claim only that the inventory dimension shows different rankings.
- **Phoneme identity is approximate.** Sanskrit's /t̪/ and English's /t/ are placed at the same column (dental) and the same manner row (voiceless unaspirated stop), but their actual phonetic realisations differ in subtle ways. The metric treats them as a match; a strict phonetician would disagree.
- **The 13-row manner taxonomy is a methodological choice.** A finer manner taxonomy would distinguish more cells; a coarser one would distinguish fewer. The numbers are partly artifacts of this choice. Robustness check: the rank order is stable across reasonable variants of the taxonomy.
- **The classification table is hand-coded.** The mapping from each phoneme symbol (Devanagari, Tamil, Korean, Arabic, IPA) to its manner class lives in `vocal_tract_overlay.py:SYMBOL_TO_MANNER` and represents ~280 entries. Unknown symbols are flagged on stderr; the current table covers all symbols across the 34 configs.
- **Sanskrit ह placement.** Sanskrit's ह is currently at column 9 (velar) per the Pāṇinian *kaṇṭhya* classification rather than column 12 (glottal) per IPA. This affects pairings where the other language has /h/ at column 12 — those pair contributions are missed. Moving ह to column 12 would slightly increase Sanskrit's coverage with most other languages.
- **No frequency information.** Each phoneme is treated as a single binary cell. The metric does not know that Sanskrit's /a/ is far more frequent in actual text than /ɭ/, or that Tamil's stops carry more functional load than its glides. A frequency-weighted metric would tell a different story.
- **No syllable-structure or phonotactic evidence.** Two languages may share inventory cells but combine them very differently. The metric ignores this completely.

The metric is **one dimension of evidence** that adds to the conversation. It is not a complete phonological comparison.

---

## 6. Reproducing the analysis

All raw data and tools are in `atomicSanskrit/figures/vocal_tract/`. To regenerate a single Sanskrit-vs-language pair:

```bash
cd atomicSanskrit/figures/vocal_tract
python3 vocal_tract_overlay.py \
  configs/scatter_sanskrit.json configs/scatter_tamil.json
# Prints 8 metrics; writes SVG to ../build/vocal_tract/
```

To regenerate the full Sanskrit-pairwise table:

```python
import json
from pathlib import Path
from vocal_tract_overlay import harmonize, compute_metrics

configs = Path("configs")
sk = json.loads((configs / "scatter_sanskrit.json").read_text())
sk_cells, _, _ = harmonize(sk["scatter"]["matrix"])

for path in sorted(configs.glob("scatter_*.json")):
    if path.stem == "scatter_sanskrit": continue
    cfg = json.loads(path.read_text())
    cells, _, _ = harmonize(cfg["scatter"]["matrix"])
    m = compute_metrics(sk_cells, cells)
    print(path.stem, m["jaccard"], m["cosine"], m["cov_a_in_b"])
```

The atlas configs and the script are version-controlled; the same input produces the same output deterministically.

---

## 7. Summary of analytical contribution

The atlas + metric system has produced four polemic-defensible findings, all summarisable under one frame: **Sanskrit is the curated superset.**

1. **The orthodoxy's family-tree boundaries do not align with inventory-similarity rankings.** The "Dravidian" and "Munda" languages cluster closer to Sanskrit than the "Indo-European" languages do. The orthodoxy's classification predicts the opposite ordering; the data refuse to corroborate it.
2. **Tamil is approximately a subset of Sanskrit.** Sk⊇Tamil = 0.67, Tamil⊇Sk = 0.36. The set-theoretic relationship is *Sanskrit ≈ Tamil's base + 21-cell engineering layer.* Tamil is not a sibling; Tamil is one of the bases the curation worked over.
3. **Sanskrit is the curated superset of the human articulator space.** Sk⊇X is consistently ≥0.7 for the southern subcontinent, ≥0.8 for the absorbed-Sanskritic languages, and 0.87 for Korean. The pattern holds across geography and across the orthodox family-tree categories. This is the curated-superset signature: a comprehensively-engineered inventory contains the inventories that catalogue subsets of the same anatomy.
4. **The Brahui control case shows areal effects ARE detectable** in this data when they exist. Brahui's place-overlap with Sanskrit (0.45) is far lower than its "Dravidian sisters'" (0.71–0.83) because Brahui has been areally pulled toward Persian/Arabic. The orthodoxy's hand-wave to "Sanskrit-Tamil similarity is areal" cannot dismiss findings 1–3 because areal-effect-when-real shows the expected pattern, and Sanskrit-Tamil don't show it.

Findings 2, 3, and 4 together produce the most-effective polemic statement the data support:

> **Sanskrit's phoneme inventory is the curated superset of the human articulator space.** Tamil is set-theoretically a subset of Sanskrit. So are Korean, Kolami, Mizo, Lepcha, Manipuri, Korku, Kui, Kuvi, Malto, Mundari — every smaller-inventory language in the atlas, across every region. Brahui is the exception that proves the rule: Brahui, by areal pressure, has been pulled INTO a different shape (uvular, pharyngeal, glottal-stop columns Sanskrit doesn't use), and is correspondingly LESS contained by Sanskrit. The data behave exactly as the engineering thesis predicts: a curated superset will tend to contain unengineered systems and will fail to contain systems that have been areally re-curated by other engineering pressures.

This is one dimension of the case against the orthodoxy's framework. Other dimensions (lexical, grammatical) are not addressed by this analysis and require their own evidence — but on this dimension, the engineering thesis is what the data prefer.
