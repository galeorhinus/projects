# Hexagonal-Tile *Dhātu* Visualization — Design Notes

Working notes for the *dhātu*-as-hexagonal-tile diagram system. Captures the initial design conversation so the visual vocabulary, encoding decisions, and deployment plan are all in one place when the figure-building begins. Companion to `vyanjana-duration-shiksha` endnote (the *mātrā* / millisecond ground for the duration-shape mapping).

---

## The Proposal

A hexagonal-tile visualization for *dhātus*:

- **Atomic unit = hexagon.** Every *varṇa* (vowel or consonant) becomes a hexagon, all sides equal length, all angles drawn at clean 30° / 60° / 90° increments so the shapes tessellate when placed adjacent.
- **Width encodes duration.** Three shape classes mapped to *mātrā*:
  - **½ mātrā (consonant — *vyañjana*)** → compressed hexagon
  - **1 mātrā (short vowel — *hrasva*)** → regular hexagon
  - **2 mātrās (long vowel — *dīrgha*)** → elongated hexagon
- **Assembly = edge-matching.** A *dhātu* like CVC is drawn by placing the three hexagons in sequence so an edge of each meets an edge of the next; vertical stagger (slightly above or below the central line) keeps the hexagonal geometry honest.
- **First milestone:** classify *dhātu* shapes (CV, VC, CVC, CCV, CVCC, …) with the empirical claim that **fewer than ten configurations cover ~80% of the *Dhātupāṭha*'s 2,168 entries**.
- **Forward path:** extend the same vocabulary to show *kriyā* / *śabda* formation and *upasarga* / *pratyaya* attachment — the full molecular pipeline drawable as a tessellation.

The mātrā ground for the temporal encoding lives in `vyanjana-duration-shiksha` (endnote in `as_endnotes.md`) and `hrasva-dirgha-pluta-matra` (companion vowel-duration endnote).

---

## What Works

**The temporal dimension is rendered geometric.** Width = duration. The ½:1:2 *mātrā* ratios the *Śikṣā* tradition specifies become visible at the diagram level. A reader looks at the tile and *sees* the timing. This is the engineering thesis made graphic — no prose required.

**Hexagons tessellate naturally.** Equal-length sides + clean angles means shapes interlock; the assembly looks like a built structure rather than ad-hoc concatenation. *Dhātu*-sequences look engineered, not grown. Sanskrit's *varṇa*-as-atom logic becomes the *atom-as-tile* visualization — directly equivalent to what chemistry does with structural formulas.

**Edge-matching mirrors *sandhi*.** When two hexagons meet, the meeting edges must align. That alignment is structurally what *sandhi* does at *varṇa* boundaries: not arbitrary concatenation, but a specified joining-rule. The edge geometry can be made to carry *sandhi* class — different edge styles for hard-consonant terminals (क्/ट्/त्/प्), soft-consonant terminals (ग्/द्/ब्), nasal terminals (ङ्/ण्/न्/म्), and vowel terminals (a-class / i-class / u-class). Compatible edges meet; incompatible edges visibly don't fit — the *sandhi* requirement becomes geometric.

**The "<10 configurations cover 80%" claim is empirically tractable.** The `analysis/dhatupatha/` bundle already has all 2,168 entries parsed. A short script can:

1. Extract the C/V skeleton per *dhātu* (after stripping *anubandhas* per Pāṇini 1.3.2–1.3.9 — see `as_3_05_by_the_numbers.md` §5.1 for the parser convention)
2. Tally distinct skeletons
3. Compute cumulative frequency
4. Output the Zipfian curve

Predicted top configurations: **CV** (कृ, हु, धा, भू), **CVC** (गम्, पच्, युज्), **VC** (अद्, इष्, उष्), **CCV** (श्रु, क्षि, च्यु), and **VCV / CVCV** for the more complex stems. **Verify the ratio empirically before building the diagram on top of it; the answer drives the visual budget.**

**The chemistry register stays consistent.** The book already treats *dhātus* as atoms (Ch 6, Ch 10), *gaṇāḥ* as the periodic table (Ch 11), and *upasarga* / *pratyaya* as bonding chemistry (Ch 12). A hexagonal-tile *dhātu* diagram is the structural-formula equivalent of what organic chemists draw. The visual program is internally coherent across chapters.

---

## Refinements to Consider Before Building

### 1. Encoding voicing and aspiration on top of shape

The hexagon's *shape* carries duration. The hexagon's *fill* / *outline* can carry the 4-way *varga* column:

| | Unaspirated (*alpaprāṇa*) | Aspirated (*mahāprāṇa*) |
|---|---|---|
| **Voiceless (*aghoṣa*)** | outline-only, thin | outline-only, thick |
| **Voiced (*ghoṣa*)** | filled, light | filled, dark |

Then क ख ग घ have the same hexagon-shape (all are ½-mātrā consonants) but different fills — the four-column *varga* structure is visible at a glance. Maps directly to the VOT-by-*varga*-column table in `vyanjana-duration-shiksha`.

### 2. Articulation site (*sthāna*) on the orientation axis

Hexagons have six vertices. Rotation could encode *sthāna*:
- Top-vertex-up → *kaṇṭhya* (क-वर्ग)
- 60° clockwise → *tālavya* (च-वर्ग)
- 120° → *mūrdhanya* (ट-वर्ग)
- 180° → *dantya* (त-वर्ग)
- 240° → *oṣṭhya* (प-वर्ग)

Five articulation sites → five orientations → the *varga*-row structure encoded geometrically. **May overload the diagram on first introduction; consider saving for the second-pass figure.**

### 3. Anusvāra / visarga as marked consonant variants

Both are ½-mātrā per *Śikṣā*, so they're squished hexagons, but they carry distinct phonetic content (nasal carrier / breath terminator). A small inscribed mark inside the hexagon distinguishes them — a dot for *anusvāra* (matching the Devanagari bindu), two dots for *visarga*.

### 4. Vertical-stagger convention needs to be deterministic

"Slightly above or below" is fine for the freehand sketch, but the published figure needs a rule. Two clean options:

- **Zigzag** — alternate above/below for visual rhythm. Bonus property: amplitude could later encode pitch contour (*svara*).
- **Sandhi-driven** — the stagger direction is chosen by the *sandhi* class of the meeting edges. More information-dense but requires the *sandhi* annotation to land first.

**Recommendation:** start with the zigzag for the introductory figure (clean, readable), then introduce sandhi-driven staggering later if you want to layer it on.

### 5. *Gaṇa* membership as the outer frame

The 10 *gaṇāḥ* (Ch 11's periodic table columns) can be encoded by an outer frame or background tint around the tile cluster. A *bhvādi* *dhātu* gets one frame style; a *juhotyādi* gets another. The *dhātu*'s position in the *gaṇa* matrix stays visible without crowding the per-*varṇa* encoding.

---

## What to Save for Later Passes

- **Anubandhas / *it* markers.** Pāṇini's citation form *ḍukṛñ* has *ḍu* / *ñ* as *it*-markers, not phonological content. Strip them from the diagram (the visualization is of the underlying *dhātu*, not the citation surface). Mention the convention in the figure caption.
- **Pluta vowels (3-mātrā).** Even wider hexagons; restricted use; peripheral case. Note in caption; don't budget a separate shape class until needed.
- **Diphthongs.** *E*, *ai*, *o*, *au* are conventionally *dīrgha* (2-mātrā) → wide hexagon. *Vṛddhi* / *guṇa* distinction (*ai*/*au* vs *e*/*o*) — encode if it matters downstream; skip on the introductory figure.

---

## Where the Figure Deploys in the Manuscript

- **Ch 10 (Building the *Dhātuḥ*)** — introduce the hexagon vocabulary. First figure: the three duration shapes; second figure: 4–6 *dhātus* tiled out (कृ, गम्, हु, अद्, श्रु, युज्). Anchors the visual atoms.
- **Ch 11 (Building the *Kriyā*)** — introduce the *gaṇa*-frame encoding. Show one *dhātu* per *gaṇa* tiled with its *gaṇa* frame. Anchors the column-wise classification visually.
- **Ch 12 (Building the *Vākya*)** — full molecular pipeline. *upasarga* (left), *dhātu* (middle), *pratyaya* (right) as a single tessellation. One concrete example: **प्र + कृ + त** → *prakṛta* tiled out. The complete *padam*.

The hexagonal-tile vocabulary becomes a **reading aid across all three chapters**. Once introduced in Ch 10, the same visual grammar can carry through Ch 11 and Ch 12 without re-explanation.

---

## Structural Observation

The proposal makes the *engineering* claim visible at the diagram level. A reader who sees a *dhātu* as a tessellation of equal-edged hexagons with matching *sandhi* edges immediately understands the architecture — no prose needed, no defensive argumentation, no apology for the engineering register. **The diagram IS the polemic in compressed form.**

That is the strongest reason to build it: it does work that prose cannot, at a register the orthodoxy has spent two centuries denying.

When the design extends to *kriyā* / *śabda* / *upasarga* / *pratyaya*, the same hexagonal vocabulary supports it cleanly — just place more tiles. The framework is recursive: every layer of the Pāṇinian apparatus is drawable in the same visual language because the system itself is recursive at the *varṇa* level.

---

## Empirical Pre-Build Step

**Run the "<10 shapes cover 80%" verification first.** That one number anchors the entire visualization claim. Once it holds in the data, the figure design follows.

Script outline (drop into `analysis/dhatupatha/scripts/`):

1. Read `analysis/dhatupatha/data/dhatupatha.csv` (2,168 entries)
2. For each *dhātu*: strip *anubandhas* per *Aṣṭādhyāyī* 1.3.2 (final-vowel + nasal), 1.3.3 (final consonant after vowel), 1.3.5 (initial *ñi* / *ṭu* / *ḍu*) — parser logic from `as_3_05_by_the_numbers.md` §5.1
3. For each underlying form: map each character to C or V; concatenate into a skeleton string ("CVC", "VC", "CCV", etc.)
4. Tally skeleton frequencies
5. Sort descending; compute cumulative percentage
6. Output: top-N table + cumulative-fraction curve
7. Confirm: how many distinct skeletons account for 80% of the corpus?

If the answer is ≤10 → the visualization claim is validated and the figure budget is set. If 10–20 → consider tier-2 shapes worth dedicated visual treatment. If >20 → re-examine the encoding (the C/V skeleton may be too coarse; consider sub-classifications).

---

## Open Decisions to Make Before Drawing

- [ ] Confirm "<10 shapes cover 80%" empirically.
- [ ] Pick stagger convention (zigzag default vs sandhi-driven).
- [ ] Decide which encoding layers ship in the introductory Ch 10 figure (duration only? duration + voicing? duration + voicing + place?).
- [ ] Decide *anusvāra* / *visarga* visual marking.
- [ ] Decide whether to render *anubandhas* (recommendation: strip them).
- [ ] Pick drawing tool / format (SVG via matplotlib? Inkscape? Tikz?). Note: the project already uses Python + matplotlib for figures (see `figures/_shared/style.py`).
- [ ] Confirm the chapter sequence — Ch 10 introduction → Ch 11 *gaṇa* extension → Ch 12 affixation tessellation.

---

## Related Endnotes and Files

- **Endnote** `vyanjana-duration-shiksha` — the *Śikṣā* ½-*mātrā* specification + modern phonetics measurement + VOT-by-*varga*-column table. The temporal-encoding ground for the hexagon-shape decisions.
- **Endnote** `hrasva-dirgha-pluta-matra` — vowel-duration framework (1 / 2 / 3+ *mātrā*). Companion specification.
- **Analysis bundle** `analysis/dhatupatha/` — parsed *Dhātupāṭha*, anubandha-stripping logic, valency data, gaṇa-membership data.
- **Chapter draft** `as_1_10_building_dhatuh.md` — the introduction point for the hexagonal vocabulary.
- **Chapter draft** `as_1_11_building_kriya.md` — the *gaṇa*-frame extension point.
- **Chapter draft** `as_1_12_building_vakya.md` — the *upasarga* / *pratyaya* tessellation extension point.
