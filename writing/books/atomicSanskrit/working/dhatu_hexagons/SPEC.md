# Hexagon Visual Grammar — Specification

The decoding scheme for the *dhātu* hexagon visualization. What each visual property of a hexagon means; how adjacent hexagons tile; how to read a generated SVG.

This document is the single source of truth for the visual encoding. The code (`dhatu_hexagon.py`) implements it; the README explains how to invoke it; this file says **what the rendering means**.

Design rationale and pre-build decisions live in `../as_dhatu_hexagon_design_notes.md`. Empirical / temporal grounding (½ : 1 : 2 *mātrā* ratios) lives in `../../concepts/vyanjana_timing.md` and the endnote `vyanjana-duration-shiksha`.

---

## 1. Geometry

Every hexagon is **flat-top**, **constant height**, **variable width**. Each one is built from:

- **Four slanted edges**, all the same length `e` (the slanted-edge unit), placed at ±60° from horizontal. These edges are the "matchable" sides — the geometry that abuts adjacent hexagons. Their length is invariant across all *varṇas*.
- **Two horizontal edges** (top and bottom), of length `w` that varies by *mātrā* class. These are the "encoding" edges — width carries duration.

The hexagon's full height is therefore constant:

> `h = e · √3 ≈ 1.732 · e`

In the current implementation, `e = 40 px`, so `h ≈ 69.3 px`.

The six vertices of a hexagon centered at `(cx, cy)` with top edge length `w`, in clockwise order from top-left:

| Vertex | Coordinates | Role |
|---|---|---|
| P1 (top-left) | `(cx − w/2, cy − h/2)` | end of top-left slanted edge |
| P2 (top-right) | `(cx + w/2, cy − h/2)` | start of top-right slanted edge |
| P3 (right) | `(cx + w/2 + e/2, cy)` | rightmost point; meets next hex's P6 |
| P4 (bottom-right) | `(cx + w/2, cy + h/2)` | end of bottom-right slanted edge |
| P5 (bottom-left) | `(cx − w/2, cy + h/2)` | start of bottom-left slanted edge |
| P6 (left) | `(cx − w/2 − e/2, cy)` | leftmost point; meets previous hex's P3 |

The top edge runs from P1 to P2; the bottom edge from P5 to P4. The four slanted edges (P2→P3, P3→P4, P5→P6, P6→P1) are all length `e`.

---

## 2. Encoding channels

Six visual properties carry information about each *varṇa*. They map to the Indic phonetic categories the *Pāṇinīya Śikṣā* and the *varṇamālā* specify.

### 2.1 Width (top / bottom edge length) → ***mātrā* duration**

The top and bottom edges' length encodes how long the *varṇa* takes to articulate, in *mātrā* units (per *Śikṣā*).

| Class | *Mātrā* | Edge width | Examples |
|---|---|---|---|
| **C** (*vyañjana*) | ½ | `w = e / 2` | consonants — क ख ग ट प य र ल व श ष स ह etc. |
| **V1** (*hrasva*) | 1 | `w = e` | short vowels — अ इ उ ऋ ऌ |
| **V2** (*dīrgha*) | 2 | `w = 2 · e` | long vowels and diphthongs — आ ई ऊ ॠ ए ऐ ओ औ |

A consonant hexagon is narrow; a short-vowel hexagon is medium; a long-vowel hexagon is wide. The width ratio is exactly the duration ratio (½ : 1 : 2). *Pluta* (3 *mātrās*) is reserved for future extension — the framework supports a "V3" class with `w = 3 · e` but it is not currently in the *varṇa* table.

### 2.2 Fill color → ***sthāna*** (place of articulation)

The hexagon's fill hue encodes the articulator site. The palette maps the five canonical *sthāna* of the *varṇamālā* (and three compound sites for diphthongs and *v*) to distinct colors:

| *Sthāna* | Devanagari class | Color | Hex |
|---|---|---|---|
| ***kaṇṭhya*** | guttural — back of mouth / throat | red | `#e85d5d` |
| ***tālavya*** | palatal — hard palate | orange | `#f59f3a` |
| ***mūrdhanya*** | retroflex — hard palate roof / front | yellow | `#e8c547` |
| ***dantya*** | dental — back of teeth | green | `#65c97e` |
| ***oṣṭhya*** | labial — lips | blue | `#5da8e8` |
| ***kaṇṭha-tālavya*** | compound (ए ऐ) | pink | `#f06fb8` |
| ***kaṇṭha-oṣṭhya*** | compound (ओ औ) | purple | `#9f7be8` |
| ***danta-oṣṭhya*** | dento-labial (व) | light blue | `#6fbcd9` |
| *default* | fallback (anusvāra, visarga) | grey | `#bcbcbc` |

Color choice runs front-of-mouth to back-of-mouth in the spectrum: red (back) → orange → yellow → green → blue (front). The spatial order on the mouth is encoded in the spectral order on the page. *Varga*-row identification at a glance: all *k*-varga letters are red, all *p*-varga letters are blue, etc.

### 2.3 Fill saturation → **voicing class**

The base color (from sthāna) is *lightened* toward white by an amount that depends on the voicing class. Voiced sounds carry near-full saturation; voiceless sounds carry visibly lighter fill.

| Voicing class | Lightening | Visual effect | Examples |
|---|---|---|---|
| ***ghoṣa*** (voiced) | 0.05 | full saturation | ग ज ड द ब |
| ***anunāsika*** (nasal) | 0.20 | slight lightening | ङ ञ ण न म |
| ***antaḥstha*** (semivowel) | 0.30 | medium | य र ल व |
| *vowel* | 0.35 | medium | अ आ इ ई etc. |
| ***ūṣman*** (fricative) | 0.45 | light | श ष स ह |
| ***aghoṣa*** (voiceless) | 0.55 | light | क च ट त प |
| ***anusvāra*** | 0.60 | very light | ं |
| ***visarga*** | 0.60 | very light | ः |

Lightening is computed by linearly interpolating the base color toward white. *Amount* = 0 means no change; *amount* = 1 means full white. The amounts above are chosen so a voiced stop reads as "saturated colored hex" and a voiceless stop as "pale tinted hex" against the same sthāna hue.

### 2.4 Stroke weight → **aspiration**

The hexagon outline's stroke weight encodes whether the *varṇa* is aspirated.

| Aspiration class | Stroke width | Examples |
|---|---|---|
| ***mahāprāṇa*** (aspirated) | 3.5 px | ख घ छ झ ठ ढ थ ध फ भ |
| ***alpaprāṇa*** (unaspirated) | 1.5 px | क ग च ज ट ड त द प ब, all semivowels, all nasals |
| n/a (vowels, anusvāra, visarga) | 1.5 px | all vowels |

Note: ***ūṣman*** (fricatives — श ष स ह) are tagged `mahāprāṇa` in the *varṇa* table because they carry continuous aspirated airflow phonetically. So sibilants render with thick stroke. This is consistent with the Pāṇinian classification.

### 2.5 Inscribed marks → **special phonetic carriers**

Three categories of *varṇa* carry extra marks beyond the hexagon shape itself:

- ***Anunāsika*** (nasals — ङ ञ ण न म): a small black bindu (dot) floats **above** the top edge of the hexagon, ~5 px above the top. Echoes the Devanagari nasal-indicating bindu visually.
- ***Anusvāra*** (ं): a single bindu **inside** the hexagon, slightly below center.
- ***Visarga*** (ः): two bindus **inside** the hexagon, left and right of center, mirroring the Devanagari visarga's two-dot character.

These marks are additive on top of the hexagon's shape + color + stroke. A nasal हexagon is still a full ½-*mātrā* consonant hex in shape; the bindu above just signals "nasal."

### 2.6 Labels (text content)

Each hexagon carries two text labels:

- **Devanagari label**, centered, slightly above the hexagon's vertical center. Font: Devanagari (with fallback chain `Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Arial Unicode MS, sans-serif`). Size: 22 pt, weight 500. **Pure consonants carry the *halant*** (्); vowels render bare; *anusvāra* (ं) and *visarga* (ः) themselves are diacritics and render bare. So क becomes क्, ग becomes ग्, but अ stays अ and ं stays ं.
- **IAST label**, centered, below the Devanagari. Font: serif (`Charter, Georgia, Times, serif`), 11 pt, italic. Size and italics chosen to read as a subordinate gloss to the primary Devanagari label.

---

## 3. Tiling

A *dhātu* is rendered as a horizontal strip of hexagons that share slanted edges with their neighbors. The sharing pattern is a **strict zigzag**.

### 3.1 The zigzag

Hexagon centers alternate between two y-coordinates:

> `cy_even = −h/4` (above the midline)
> `cy_odd = +h/4` (below the midline)

The first hexagon sits at `cy_even` (above the midline). The second drops to `cy_odd`. The third returns to `cy_even`. Etc. The overall strip's midline is at `y = 0`; the zigzag amplitude is `h/4` above and below.

The vertical offset between adjacent hexagons is therefore `h/2` (the difference between `cy_even` and `cy_odd`). This is precisely the offset required for two hexagons of equal height to share a slanted edge.

### 3.2 Horizontal advancement

Given a hexagon `i` of top-edge width `w_i` placed at `cx_i`, the next hexagon `i+1` of width `w_{i+1}` is placed at:

> `cx_{i+1} = cx_i + (w_i + w_{i+1}) / 2 + e / 2`

The `(w_i + w_{i+1}) / 2` term accounts for half of each hexagon's top edge. The `e / 2` term accounts for the horizontal projection of the slanted edge that separates them.

Result: hexagon `i`'s right vertex (`P3`) at `(cx_i + w_i/2 + e/2, cy_i)` coincides with hexagon `i+1`'s top-left vertex (`P1`) at `(cx_{i+1} − w_{i+1}/2, cy_{i+1} − h/2)` *or* its bottom-left vertex (`P5`) at `(cx_{i+1} − w_{i+1}/2, cy_{i+1} + h/2)` — depending on whether the zigzag step goes down or up.

The slanted edge between adjacent hexagons is shared: hexagon `i`'s bottom-right edge (P3→P4) is the same segment as hexagon `i+1`'s top-left edge (P1→P6), traversed in opposite directions. Geometrically, the strip is one continuous tessellation.

### 3.3 Why this matters

Edge-sharing makes the *dhātu* read as a *built* object rather than a sequence of independent shapes. Adjacent *varṇas* are bonded at a specific geometric site — the shared slanted edge — which is the visual analogue of *sandhi*. The convention is uniform across all *dhātus*; the visualization itself encodes the bondability of adjacent *varṇas* without requiring additional annotation.

---

## 4. The *varṇa* table

The full mapping from IAST label → (Devanagari, class, *sthāna*, voicing, aspiration) lives in `dhatu_hexagon.py` as the `VARNAS` dictionary. It contains 47 entries covering:

- **All 13 vowels** (अ आ इ ई उ ऊ ऋ ॠ ऌ ए ऐ ओ औ)
- **25 *sparśa* consonants** (the five *vargas* of five consonants each)
- **4 *antaḥstha*** (य र ल व)
- **4 *ūṣman*** (श ष स ह)
- **2 ayogavāha** (ं ः)

Each entry has six fields:

```python
"k":  {"deva": "क", "iast": "k", "class": "C", "sthana": "kanthya",
       "voicing": "aghosha", "aspiration": "alpaprana"}
```

To extend the framework to a new *varṇa* category (e.g., the Vedic ळ retroflex lateral), add an entry to `VARNAS` with the appropriate metadata; no other changes are needed. The renderer reads all visual properties from the table.

---

## 5. Reading a generated SVG

Given an SVG produced by the tool, a reader can decode every *varṇa* from its visual properties:

1. **Width of the hexagon** says: ½ mātrā (narrow), 1 mātrā (medium), or 2 mātrā (wide).
2. **Color** says: which row of the *varṇamālā* (red kaṇṭhya, orange tālavya, yellow mūrdhanya, green dantya, blue oṣṭhya, or a compound site).
3. **Saturation** (light vs full) says: voiceless (light), voiced (full), or one of the intermediate classes.
4. **Stroke** (thin vs thick) says: unaspirated (thin) or aspirated (thick).
5. **Bindu above the hexagon**: this is a nasal (anunāsika).
6. **Bindu(s) inside**: anusvāra (one) or visarga (two).
7. **Labels** confirm the identification — the Devanagari character (with halant for consonants) and the IAST gloss.

The geometric arrangement says: this is *one dhātu*, with adjacent *varṇas* bonded at shared slanted edges (the *sandhi* sites), zigzagged in the temporal sequence the reciter would speak.

---

## 6. Open extensions (not yet encoded)

The current implementation captures the structural axes (place, manner, voicing, aspiration, duration) but does not yet encode several features that the design notes flag as future passes:

- ***Gaṇa* membership** — the 10 *gaṇāḥ* of the *Dhātupāṭha*. Could be encoded as an outer frame or background tint around the entire *dhātu* tile-cluster. Currently absent.
- ***Sandhi* class on shared edges** — the meeting-edge geometry currently uses uniform slope. A richer pass could vary the edge style (color, dash pattern, marker glyph) per *sandhi* class so the bondability becomes explicit rather than implicit. Currently uniform.
- **Articulation site via orientation** — the design notes propose rotating the hexagon to encode *sthāna*. The current implementation uses color for this (which works better with edge-matching, since rotation breaks the slanted-edge geometry). Rotation-as-encoding is therefore deferred indefinitely.
- ***Pluta*** vowels (3 *mātrās*) — the framework supports a `V3` class with `w = 3e` but no *pluta* entries are currently in the table.
- ***Upasarga*** prefixes and ***pratyaya*** suffixes — the morphology chemistry (Ch 12) extends the *dhātu* into a complete *padam*. The hexagonal grammar supports this (just add more tiles), but `dhatu_hexagon.py` v1 takes only a bare *varṇa* list.
- ***Guru* / *laghu* metrical overlay** — the *Chandas* per-syllable weight (developed in `concepts/vyanjana_timing.md`) is a Level-2 layer on top of the per-*varṇa* hexagons. Could be added as a frame around each syllable's hex cluster (1-mātrā frame = *laghu*, 2-mātrā frame = *guru*). Not yet encoded.
- **Visarga as half-hexagon with breath-fade right edge** — replace the current full-hexagon-with-two-bindus rendering of visarga (ः) with a 5-vertex half-shape:
  - Start with a V1 (1-*mātrā*) hexagon shape and cut it vertically through its center.
  - Keep the **left half** — 5 vertices: top-left (`P1`), top-midpoint (`(cx, cy − h/2)`), bottom-midpoint (`(cx, cy + h/2)`), bottom-left (`P5`), and left vertex (`P6`).
  - The **right edge** is a straight vertical line from top-midpoint to bottom-midpoint.
  - **Top edge length is `e/2`** — preserves the ½-*mātrā* temporal encoding (consonants and visarga are both ½ *mātrā* per *Śikṣā*, so they should share top-edge width).
  - **Total width is `e`** — narrower than the current C hexagon (which is `3e/2` wide). The asymmetry of the half-shape itself is the distinguishing geometric signature; visarga becomes the only *varṇa* in the strip with a straight vertical edge.

  **Phonetic rationale.** Visarga is a voiceless breath release — the previous vowel's voicing fading into open breath, with no closing articulator gesture. A half-hexagon-ending-in-line captures the gestural quality visually: bounded articulation on the left (the opening), unbounded breath fade on the right (no closing). The shape encodes what the phoneme *does* — a sound that has an articulated start and a non-articulated end.

  **Implementation note.** The half-shape replaces the current `<polygon>` + inscribed-bindus rendering for visarga. The geometric signature is unmistakable — no full hexagon has a vertical edge, so the visarga half-shape cannot be mistaken for any other *varṇa*. The fill color stays neutral grey (`default` palette entry) consistent with current treatment.

  **Tiling note.** The visarga's vertical right edge can still abut the next hexagon's left slanted edge in the zigzag — the next hexagon's left vertex (`P6`) sits at the same x-coordinate as the visarga's right edge, and the zigzag y-offset still applies. Edge-matching geometry is preserved; only the visarga's *shape* changes, not its *position* in the strip.

  **Parallel open question for anusvāra (ं).** Phonetically, anusvāra is the voiced-nasal continuation of the previous vowel — comparable in "fade-out" character to visarga but with voicing and nasalization retained. A possible parallel design: half-hexagon with a curved or dotted right edge (vs visarga's straight line), encoding "nasal hum continues" vs "breath fades out." Or: anusvāra keeps the current bindu-inside-full-hexagon treatment while visarga moves to the half-shape, making the two ayogavāha visually distinct categories rather than parallel variants. Held open for design iteration; the visarga half-shape can land independently of the anusvāra decision.

Each of these is a v2+ addition. The v1 spec above is stable: nothing in v2 should re-encode any v1 property.

---

## 7. Versioning

- **v1** (this document): geometry + width-mātrā + color-sthāna + saturation-voicing + stroke-aspiration + bindu-marks + halant + zigzag. As implemented in `dhatu_hexagon.py`.
- v2 (planned): + *gaṇa* frame, JSON input.
- v3 (planned): + *upasarga* / *pratyaya* attachment, + *guru* / *laghu* overlay.
- v4 (speculative): + sandhi-edge encoding, + ṛddhi / guṇa transformations.

Any future revision should keep this document in lockstep with the code. The spec is the authority; the code implements it.
