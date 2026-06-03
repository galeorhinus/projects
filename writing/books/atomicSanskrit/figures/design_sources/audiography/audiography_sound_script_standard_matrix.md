# Comparative Phonology Figure — Design Brief (v2)

*A companion figure to "Varṇamāla — The Sonomer Garland." This figure compares Sanskrit, Korean, and Arabic phonological inventories using a unified speech-science framework, with Sanskrit as the visual anchor.*

---

## Project context

You are designing a figure for the *Atomic Sanskrit* book project. The book argues that Sanskrit's phonological inventory (the *varṇamāla*) is **engineered** — deliberately designed, structurally complete, and uniquely so among the world's languages. The existing "Sonomer Garland" figure visualizes Sanskrit's *varṇamāla* internally. This new figure extends the argument by comparing three phonologies side by side.

### The engineering / standardization asymmetry

The figure makes a three-way structural distinction visible:

| Language | Phonology | Script |
|---|---|---|
| **Sanskrit** | **Engineered** | **Engineered** (Brāhmī family) |
| **Korean** | Standardized (natural language formally documented) | **Engineered** (Hangul by Sejong, 1443 CE) |
| **Arabic** | Standardized (natural language formally documented; Sibawayh's *Al-Kitāb*) | Standardized / adapted (from Aramaic) |

Sanskrit is the only case where the phonology itself is engineered. Korean and Arabic phonologies developed naturally and were standardized after the fact; Korean additionally received an engineered SCRIPT centuries after the language was already in use; Arabic's script was adapted (not engineered) from a related Semitic source.

### The argument the figure should make visible without text

1. Sanskrit's hexagonal markers fill a contiguous middle region densely and symmetrically — the visual signature of an engineered phonology.
2. Arabic's circular markers extend to pharyngeal and uvular depths Sanskrit doesn't reach, and add a pharyngealized series no other language has — wide place coverage, sparse density.
3. Korean's square markers stack at fewer places with multi-axis depth (plain / aspirated / tense) — narrow place coverage, layered features.
4. A small "universal core" of phonemes is shared by all three languages — the floor humans naturally converge on regardless of engineering tradition.
5. Sanskrit serves as the visual anchor: multi-language cells show the Sanskrit hex at full size with other languages as smaller satellite markers connected by lines. This makes the engineered-center / standardized-periphery structure visible in every shared cell.

---

## Visual reference: the companion figure

This figure should sit alongside the existing "Varṇamāla — The Sonomer Garland" figure in the same book. Match its aesthetic conventions:

- **Vertical orientation, A4 / book-page aspect** (~3:4 height:width)
- **Greyscale palette** — light backgrounds, charcoal and black foregrounds, no full-saturation colors
- **Serif typography** — same family as the Sonomer Garland
- **Left-side legend panel** running the full height of the figure
- **Main matrix on the right** taking ~75% of the canvas width
- **Title and subtitle at the top** in the same style as "वर्णमाला — The Sonomer Garland"

---

## Title

```
       Engineered and Standardized
        Sanskrit · Korean · Arabic
```

**Subtitle (italic serif, smaller, immediately below the title):**

> *one engineered phonology · two standardized phonologies (one with engineered script)*

(Order: Sanskrit first, Korean middle, Arabic last — left-to-right gradient from maximum engineering to maximum standardization.)

---

## Overall composition

Four regions, organized like the existing figure:

1. **Top:** Title + subtitle strip
2. **Below title:** Anatomical ruler showing position from lips (mm) — proportional tick marks aligned with the matrix below
3. **Left ~25%:** Legend / key panel (manner classes, shape key, position diagram)
4. **Right ~75%:** Main consonant matrix — 12 columns × 18 rows of cells

No vowel sub-panel. The consonant matrix is the only data area. The ruler is a thin horizontal strip immediately above row 1 of the matrix.

---

## Column specification (12 places of articulation)

Order: back of mouth → front of mouth (left to right), strictly monotonic by anatomical position. Pure speech-science terminology. No Sanskrit metalanguage.

**All 12 columns are uniform width.** The non-uniform anatomical spacing is communicated through the proportional ruler at the top of the matrix (see next section), NOT through column-width variation.

| # | Column header (top of column) | mm from lips | Filled by |
|---|---|---:|---|
| 1 | **Glottal** | 180 | Sk + Ar + Ko |
| 2 | **Pharyngeal** | 150 | Arabic only |
| 3 | **Uvular** | 120 | Arabic only |
| 4 | **Velar** | 95 | Sk + Ar + Ko |
| 5 | **Palatal** | 65 | Sk + Ko (y) |
| 6 | **Retroflex** | 50 | Sanskrit only |
| 7 | **Post-alveolar** | 38 | Ar + Ko |
| 8 | **Alveolar** | 28 | Ar + Ko |
| 9 | **Dental** | 18 | Sk + Ar |
| 10 | **Interdental** | 10 | Arabic only |
| 11 | **Labio-dental** | 5 | Arabic only |
| 12 | **Bilabial** | 0 | Sk + Ar + Ko |

Column headers sit at the top of each column, set in small caps or a clean uppercase serif.

---

## Anatomical ruler (NEW in v3)

A horizontal ruler sits immediately below the column headers and above the first row of the matrix. The ruler shows the position of each place of articulation **measured in millimeters from the lips** in an average adult vocal tract (~180 mm total length).

### Why proportional spacing

The ruler tick marks are positioned to reflect the TRUE anatomical distances between places of articulation. The matrix columns are uniform width, but the ruler is "warped" — ticks cluster densely at the back of the mouth (where many places of articulation are anatomically distant — pharyngeal, uvular, velar are spread across ~85 mm) and spread sparsely at the front (where the bilabial → post-alveolar range fits in only ~38 mm but occupies the right-hand 6 columns of the matrix).

The visual effect: reader sees the matrix structure cleanly (uniform columns, easy to scan) AND learns the anatomical truth (back-of-mouth distances are larger than front-of-mouth distances, but the column system normalizes this).

### Tick mark positions

Ticks at every 10 mm from 0 to 180. Positions measured in column-units (matrix is 12 column-units wide, left edge = 0, right edge = 12):

| mm value | Visual position (column-units from left) | Label? |
|---:|---:|---|
| 180 | 0.5 | yes (major) |
| 170 | 0.83 | no (minor) |
| 160 | 1.17 | yes (major) |
| 150 | 1.5 | no (minor) |
| 140 | 1.83 | yes (major) |
| 130 | 2.17 | no (minor) |
| 120 | 2.5 | yes (major) |
| 110 | 2.9 | no (minor) |
| 100 | 3.3 | yes (major) |
| 90 | 3.67 | no (minor) |
| 80 | 4.0 | yes (major) |
| 70 | 4.33 | no (minor) |
| 60 | 4.83 | yes (major) |
| 50 | 5.5 | no (minor) |
| 40 | 6.33 | yes (major) |
| 30 | 7.3 | no (minor) |
| 20 | 8.3 | yes (major) |
| 10 | 9.5 | no (minor) |
| 0 | 11.5 | yes (major) |

**Labeling strategy:** label every 20 mm (the major ticks at 0, 20, 40, 60, 80, 100, 120, 140, 160, 180); leave the 10s in between as minor unlabeled ticks. This avoids label crowding at the back of the chart where ticks are densely packed.

### Ruler style

- Horizontal line: thin charcoal (#2A2A2A), ~0.5pt
- Major tick marks: extend down ~6pt from the line, charcoal
- Minor tick marks: extend down ~3pt from the line, lighter grey
- Label text: serif, small (8–10pt), charcoal, positioned just above the line
- Subtitle below the ruler line, small italic serif (7–8pt), grey:
  > *position from lips (mm) · average adult vocal tract*

### Visual effect

The reader sees that the back of the chart (left side) has tick marks crowded together — many millimeters compressed into one column-width — while the front of the chart (right side) has tick marks spread out — few millimeters across one column-width. The chart's uniform-width columns compress the anatomy at the back and stretch it at the front; the ruler shows the truth.

Alongside the structural argument the matrix makes about phonological inventories, the ruler makes a complementary anatomical argument: **the back of the human vocal tract is where engineering distinctions get packed into small spatial regions**. This visually anchors the abstract column system in physical reality.

---

## Row specification (18 manner-feature rows)

Each row label sits on the left, just inside the matrix area. Standard IPA / speech-science terminology only.

| Row # | Row label |
|---|---|
| 1 | Plosive — voiceless, unaspirated |
| 2 | Plosive — voiceless, aspirated |
| 3 | Plosive — voiceless, tense (fortis) |
| 4 | Plosive — voiceless, pharyngealized |
| 5 | Plosive — voiced, unaspirated |
| 6 | Plosive — voiced, breathy |
| 7 | Plosive — voiced, pharyngealized |
| 8 | Affricate — voiceless, unaspirated |
| 9 | Affricate — voiceless, aspirated |
| 10 | Affricate — voiceless, tense |
| 11 | Affricate — voiced |
| 12 | Nasal |
| 13 | Liquid (trill, tap, lateral) |
| 14 | Glide / Semivowel (palatal, labio-velar) |
| 15 | Fricative — voiceless |
| 16 | Fricative — voiced |
| 17 | Fricative — pharyngealized |
| 18 | Fricative — tense |

**Manner-class groupings and dividers:**

- **Stops** (rows 1–11): plosives + affricates — most-constricted manners
- **Sonorants** (rows 12–14): nasal + liquid + glide — voiced, vowel-adjacent manners
- **Fricatives** (rows 15–18): continuous turbulent constriction

Use horizontal dividers after rows 7 (plosives → affricates), 11 (affricates → nasal), 14 (sonorants → fricatives), and 18 (matrix end). Optionally a lighter divider after row 12 (within the sonorant block, separating nasal from liquid).

The flow groups all sonorants (nasal, liquid, glide) together as a coherent block between the stops and the fricatives — matching standard IPA chart conventions where trill/tap precede fricatives.

**Note on row 13 (Liquid):** This row consolidates what were previously three separate rows (trill, tap/flap, lateral approximant) since these all share the "consonantal sonorant" character and only collectively occupy a sparse region of the matrix. The alveolar cell in this row is the densest cell in the matrix — it contains Sanskrit र (tap), Arabic ر (trill), Arabic ل (lateral), and Korean ㄹ (tap/lateral allophone). See the Sanskrit-centric satellite layout instructions for handling this 4-phoneme cell — Sanskrit hex centered at full size with three satellites (two Arabic circles + one Korean square).

**Note on row 14 (Glide / Semivowel):** Consolidates the palatal and labio-velar approximant rows. Glides are sonorants at vowel-like places — phonetically intermediate between consonants and vowels.

---

## Shape system

| Language | Shape | Fill | Border |
|---|---|---|---|
| **Sanskrit** | Hexagon (regular, 6-sided, point-up) | Solid light grey (#D4D4D4) | Thin charcoal border (~1pt) |
| **Arabic** | Circle | Solid medium grey (#A8A8A8) | Thin charcoal border |
| **Korean** | Square (slightly rounded corners, 2–3px radius) | Solid darker grey (#888888) | Thin charcoal border |

**Each shape contains its language's script character — no IPA symbols anywhere in the figure.**

- Sanskrit hexagons contain Devanagari letters
- Arabic circles contain Arabic letters (naskh font with full diacritical dots — see Typography section)
- Korean squares contain Hangul jamo

---

## Multi-language cell treatment — Sanskrit-centric satellite layout

When a cell contains Sanskrit AND one or more other languages, the Sanskrit hexagon stays at its **full original size**, centered in the cell. The other language markers are drawn as **smaller satellites** placed at the side of the cell, connected to the central hex by a thin line.

**Layout per cell composition:**

| Cell composition | Layout |
|---|---|
| **Sanskrit only** | Hex centered in cell at full size. Standard treatment. |
| **Sanskrit + Arabic** | Sanskrit hex at full size, centered. Arabic circle as satellite (~45–50% of hex size) placed to the right side of the cell (or slightly extending beyond the cell boundary). Thin charcoal line connects the right edge of the hex to the left edge of the circle. |
| **Sanskrit + Korean** | Sanskrit hex at full size, centered. Korean square as satellite (~45–50% of hex size) placed to the right side of the cell. Thin line connects hex edge to square edge. |
| **Sanskrit + Arabic + Korean** (universal core) | Sanskrit hex at full size, centered. Arabic circle satellite on the LEFT side; Korean square satellite on the RIGHT side. Two thin connecting lines from the hex edges to each satellite. |
| **Arabic + Korean only (no Sanskrit)** | Both markers at standard cell-fitting size, placed side-by-side within the cell (Arabic left, Korean right). NO connecting line — no Sanskrit center to anchor to. |
| **Arabic alone** or **Korean alone** | Single marker centered in cell at standard size. |

**Connecting line specification:**

- Stroke: 0.5pt charcoal (#2A2A2A)
- Connects from the perimeter of the hex to the perimeter of the satellite marker
- Lines should not intersect any script character

**Why this layout:** Sanskrit becomes the visual anchor of every multi-language cell. The reader sees "Sanskrit is the engineered center; other languages have phonemes connected to (but smaller than) the Sanskrit reference point." This enacts the book's central argument geometrically.

**Sanskrit hex is the same size in every cell** — whether the cell is Sanskrit-only or Sanskrit + others. The satellite markers are smaller than the central hex but legible.

---

## Devanagari typographic adjustment

Devanagari characters have a *shirorekhā* (top header bar) and the visual weight of the character sits BELOW its mathematical center. Mathematically centered Devanagari appears top-heavy in a hexagonal frame.

**Adjustment:** shift Devanagari characters DOWN within the hex by approximately 8–12% of the hex's vertical extent. The goal is **optical centering** (visual balance) rather than geometric centering.

This applies to all Devanagari characters inside Sanskrit hexagons. Arabic letters in circles and Hangul in squares do not have the same top-line weighting issue and should remain at standard optical centering.

---

## Classification methodology

Each language's phonemes are placed in the matrix according to **that language's own engineered classification system**, not by IPA articulation alone. This is a deliberate design choice that aligns the comparative figure with the book's central argument.

### How each language's classification is honored

- **Sanskrit:** Pāṇinian classification (the *varṇamāla*'s own structural assignment). Sanskrit र is placed at Retroflex (मूर्धन्य), Sanskrit स at Dental (दन्त्य), Sanskrit ह at Velar (कण्ठ्य), Sanskrit व at Bilabial (ओष्ठ्य) — matching the Sonomer Garland figure.
- **Arabic:** standard Arabic phonetic classification (the *makhārij* tradition + IPA mapping). Most Arabic phonemes have unambiguous IPA-aligned placement.
- **Korean:** standard Korean phonological classification matching modern phonetic analysis.

### Why this matters

The book argues that each engineering tradition classifies its phonemes through its own internal logic. If the figure imposed IPA classification universally, it would implicitly claim "IPA's articulation chart is the truth and each language's classification is a quirk." That undercuts the engineering thesis.

Following each language's own classification creates cells where the same column may contain phonemes that are phonetically slightly different across languages. For example, the Velar column contains:
- Sanskrit ह (Pāṇinian kaṇṭhya; phonetically /h/ or /ɦ/, glottal in IPA)
- Sanskrit क ख ग घ ङ (Pāṇinian kaṇṭhya; phonetically velar /k/, /kʰ/, /g/, /gʱ/, /ŋ/)
- Arabic ك خ غ (phonetically velar /k/, /x/, /ɣ/)
- Korean ㄱ ㅋ ㄲ ㅇ (phonetically velar)

These don't all sound identical, but each language has independently classified its phoneme at this position within its own framework. The figure visualizes the *classification convergence*, not the *acoustic convergence*.

### Where Sanskrit's classification diverges from IPA

Four Sanskrit phonemes are placed by Pāṇinian rather than IPA classification. Each is marked with footnote ⁴:

| Phoneme | Column (Pāṇinian) | IPA would place at |
|---|---|---|
| **र** | Retroflex (मूर्धन्य) | Alveolar (tap [ɾ]) |
| **स** | Dental (दन्त्य) | Alveolar (sibilant [s]) |
| **ह** | Velar (कण्ठ्य) | Glottal (fricative [h]) |
| **व** | Bilabial (ओष्ठ्य) | Labio-dental (approximant [ʋ]) |

### Trade-off acknowledged

This design choice reduces the "universal-core" count from 5 to 3 cells (see Universal-core section). Two cells where IPA convergence WOULD exist (s and h) no longer appear as shared because Sanskrit places these sounds elsewhere. The reduction is itself part of the argument: cross-linguistic phonetic identity is not the same as cross-linguistic classification identity. Languages that "share a sound" by IPA standards may still file that sound in different structural positions within their own engineered phonologies.

---

## Cell-by-cell content map

Every cell with content. Empty cells (most of the matrix) show nothing.

| Row | Column | Sanskrit (hex) | Arabic (circle) | Korean (square) |
|---|---|---|---|---|
| 1 | Velar | क | ك | ㄱ |
| 1 | Dental | त | ت | — |
| 1 | Alveolar | — | — | ㄷ |
| 1 | Retroflex | ट | — | — |
| 1 | Palatal | च | — | — |
| 1 | Bilabial | प | — | ㅂ |
| 1 | Uvular | — | ق | — |
| 1 | Glottal | — | ء | — |
| 2 | Velar | ख | — | ㅋ |
| 2 | Dental | थ | — | — |
| 2 | Alveolar | — | — | ㅌ |
| 2 | Retroflex | ठ | — | — |
| 2 | Palatal | छ | — | — |
| 2 | Bilabial | फ | — | ㅍ |
| 3 | Velar | — | — | ㄲ |
| 3 | Alveolar | — | — | ㄸ |
| 3 | Bilabial | — | — | ㅃ |
| 4 | Dental | — | ط | — |
| 5 | Velar | ग | — | — |
| 5 | Dental | द | د | — |
| 5 | Retroflex | ड | — | — |
| 5 | Palatal | ज | — | — |
| 5 | Bilabial | ब | ب | — |
| 6 | Velar | घ | — | — |
| 6 | Dental | ध | — | — |
| 6 | Retroflex | ढ | — | — |
| 6 | Palatal | झ | — | — |
| 6 | Bilabial | भ | — | — |
| 7 | Dental | — | ض | — |
| 8 | Post-alveolar | — | — | ㅈ |
| 9 | Post-alveolar | — | — | ㅊ |
| 10 | Post-alveolar | — | — | ㅉ |
| 11 | Post-alveolar | — | ج | — |
| 12 | Velar | ङ | — | ㅇ¹ |
| 12 | Palatal | ञ | — | — |
| 12 | Retroflex | ण | — | — |
| 12 | Alveolar | — | ن | ㄴ |
| 12 | Dental | न | — | — |
| 12 | Bilabial | म | م | ㅁ |
| 13 | Dental | ल | — | — |
| 13 | Retroflex | र² | — | — |
| 13 | Alveolar | — | ر · ل | ㄹ¹ |
| 14 | Palatal | य | ي | y¹ |
| 14 | Bilabial | व² | و | w¹ |
| 15 | Velar | ह² | خ | — |
| 15 | Pharyngeal | — | ح | — |
| 15 | Glottal | — | ه | ㅎ |
| 15 | Palatal | श | — | — |
| 15 | Post-alveolar | — | ش | — |
| 15 | Retroflex | ष | — | — |
| 15 | Dental | स² | — | — |
| 15 | Alveolar | — | س | ㅅ |
| 15 | Interdental | — | ث | — |
| 15 | Labio-dental | — | ف | — |
| 16 | Velar | — | غ | — |
| 16 | Pharyngeal | — | ع | — |
| 16 | Alveolar | — | ز | — |
| 16 | Interdental | — | ذ | — |
| 17 | Alveolar | — | ص | — |
| 17 | Interdental | — | ظ | — |
| 18 | Alveolar | — | — | ㅆ |

**Footnotes — two consolidated notes** (place small superscript marks at the relevant cells, with the two notes below the figure):

- **¹** Korean: ㅇ is velar nasal syllable-finally only (initial is null); ㄹ is [ɾ] (tap) or [l] (lateral) by position; w and y appear only as glides in diphthongs.
- **²** Sanskrit is placed by Pāṇinian classification, not IPA: र = *mūrdhanya* (retroflex), स = *dantya* (dental), ह = *kaṇṭhya* (velar), व = *oṣṭhya* (labial). Each engineered tradition files its sounds under its own system.

**Cell marker assignments:**

| Cell | Marker |
|---|---|
| Korean ㅇ (row 12 Velar) | ¹ |
| Korean ㄹ (row 13 Alveolar — Liquid) | ¹ |
| Korean y (row 14 Palatal — Glide) | ¹ |
| Korean w (row 14 Bilabial — Glide) | ¹ |
| Sanskrit र (row 13 Retroflex — Liquid) | ² |
| Sanskrit व (row 14 Bilabial — Glide) | ² |
| Sanskrit ह (row 15 Velar — Fricative voiceless) | ² |
| Sanskrit स (row 15 Dental — Fricative voiceless) | ² |

Note: this is a **v3.6 consolidation** from the original four-footnote scheme (¹ ² ³ ⁴) due to space constraints in the legend panel. Note ¹ now covers all Korean-specific behaviors; Note ² covers the Pāṇinian classification framework.

---

## Universal-core cells (the convergence)

Three cells contain phonemes from all three languages where each language's own classification places them in the same column. These are the universal-core cells where the Sanskrit hex appears at full size with both Arabic circle (left satellite) and Korean square (right satellite):

| Row | Column (#) | Phonemes |
|---|---|---|
| 1 | Velar (col 4) | क · ك · ㄱ |
| 12 | Bilabial (col 12) | म · م · ㅁ |
| 14 | Palatal (col 5) | य · ي · y |

A subtle background tint (very faint warm color, ~5–8% opacity) behind these three cells makes the universal-core pattern visible at the matrix level. Alternatively, a thin warm-tinted border around the cells.

**Note on the reduced universal-core (down from 5 in v2):** In earlier versions, the universal-core also included Row 15 Alveolar (स · س · ㅅ) and Row 15 Glottal (ह · ه · ㅎ). With v3.5 adopting Pāṇinian classification for Sanskrit phonemes, Sanskrit places स at Dental (दन्त्य) and ह at Velar (कण्ठ्य) — even though phonetically /s/ is alveolar and /h/ is glottal in IPA terms. The reduction from 5 to 3 universal-core cells is informative: it shows that even where languages share *phonetic* outputs (the /s/ sound, the /h/ sound), they often classify them at different *structural positions* within their own engineering systems. The three remaining universal-core cells are positions where all three traditions converge in classification as well as phonetic output.

---

## Empty-cell treatment

Empty cells display nothing — just background. To preserve the column/row structure visually:

- **Faint grid lines** between cells (very light grey, ~10% opacity)
- **Slightly tinted backgrounds** for rows belonging to the same manner-class group (alternating bands, very subtle — financial-table style)

The matrix should read as mostly-empty with the markers forming visible clusters / patterns.

---

## Legend panel (left side, full height)

Structure from top to bottom:

```
┌─────────────────────────┐
│ How to Read the Matrix  │
│ three phonologies,      │
│ one chart               │
├─────────────────────────┤
│ SHAPE KEY               │
│                         │
│   ⬡  Sanskrit           │
│   ○  Arabic             │
│   □  Korean             │
├─────────────────────────┤
│ MULTI-LANGUAGE CELLS    │
│                         │
│ [diagram: Sanskrit hex  │
│  centered, Arabic circle│
│  satellite on left,     │
│  Korean square satellite│
│  on right, thin lines   │
│  connecting]            │
│                         │
│ Sanskrit stays full-    │
│ size as the central     │
│ phoneme; other          │
│ languages appear as     │
│ smaller satellites      │
│ connected by lines.     │
├─────────────────────────┤
│ MANNER CLASSES          │
│                         │
│ Plosive                 │
│   complete oral         │
│   closure with release  │
│                         │
│ Affricate               │
│   closure released as   │
│   fricative             │
│                         │
│ Nasal                   │
│   oral closure with     │
│   nasal release         │
│                         │
│ Liquid                  │
│   trill, tap, lateral — │
│   consonantal sonorants │
│                         │
│ Glide / Semivowel       │
│   palatal y, labio-velar│
│   w — sonorants at      │
│   vowel-like places     │
│                         │
│ Fricative               │
│   narrow constriction,  │
│   turbulence            │
├─────────────────────────┤
│ FEATURE AXES            │
│   voiceless · voiced    │
│   unaspirated · aspirated│
│   plain · tense         │
│   pharyngealized ·      │
│   breathy               │
└─────────────────────────┘
```

The "MULTI-LANGUAGE CELLS" diagram should be a small visual showing a Sanskrit hex at the center with Arabic circle and Korean square as satellites connected by lines — a single example from the universal-core (e.g., velar /k/ with क, ك, ㄱ) — so the reader understands the convention at a glance.

Use the same serif typography as the Sonomer Garland figure's legend panel. NO Sanskrit terminology anywhere in this panel — pure speech-science only.

---

## Optional caption (beneath the figure)

A short italicized caption at the bottom of the figure could name the visible pattern explicitly:

> *Sanskrit's hexagons fill a contiguous middle region. Arabic's circles spread to pharyngeal and uvular depths and add a pharyngealized series. Korean's squares stack at fewer places with multi-axis depth. Five cells — the universal core — carry phonemes shared by all three traditions.*

---

## Typography

- Title and headers: serif (matching the Sonomer Garland)
- Subtitle: serif italic
- Column labels: serif small caps or uppercase, condensed
- Row labels: serif, sentence case
- Script characters inside markers: native typefaces — Devanagari, Arabic, Hangul — sized to fit comfortably inside the shape with margin
- Legend text: serif, light weight

**CRITICAL — Arabic font requirement:**

Use a standard Arabic naskh font with full diacritical dots: **Amiri**, **Noto Naskh Arabic**, or **Scheherazade New**. Calligraphic / rasm / kufic styles that omit dots are NOT acceptable. The dots are what distinguish ت from ب from ث from ن, ج from ح from خ, ف from ق, etc. Without them, the Arabic characters become unreadable.

Verify at print resolution that every Arabic letter is unambiguously identifiable to an Arabic reader.

**Devanagari positioning:** shift Devanagari characters DOWN within the hex by ~8–12% of the hex's vertical extent for optical centering (see Devanagari typographic adjustment section above).

---

## Color palette

Greyscale only. Suggested values:

- Background: warm off-white (#FAFAFA)
- Light grey (Sanskrit hexagon fill): #D4D4D4
- Medium grey (Arabic circle fill): #A8A8A8
- Dark grey (Korean square fill): #888888
- Charcoal (borders, text, connecting lines): #2A2A2A
- Faint grid lines: #E5E5E5
- Universal-core cell tint: very faint warm color (~5–8% opacity)

The three-greys-for-three-languages convention makes shape AND fill carry the language identity, useful when script characters are too small to read at print resolution.

---

## Output format

- **SVG (vector)** — primary deliverable, for clean print rendering
- **Dimensions:** sized for a full-page figure in a 6×9 trade paperback (so ~5" × 7" usable area)
- **Self-contained:** all fonts embedded; no external dependencies

---

## What NOT to include

To preserve the chart's neutrality and visual structure:

- ❌ NO IPA symbols anywhere in the figure
- ❌ NO Sanskrit metalinguistic terminology (no *sthāna*, *prayatna*, *prāṇa*, *ghoṣa*, *anunāsika*, *kaṇṭhya*, *tālavya*, *mūrdhanya*, *dantya*, *oṣṭhya*, *sparśa*, *ūṣman*, *antaḥstha*, *svara*, *praṇava*, *anusvāra*)
- ❌ NO Devanagari labels in column or row headers (Devanagari appears only inside Sanskrit hexagon markers)
- ❌ NO Om symbol
- ❌ NO vowel sub-panel — removed in v2
- ❌ NO "beads" — use plain shape markers
- ❌ NO triangular-cluster layout — replaced by the Sanskrit-centric satellite layout in v2
- ❌ NO Arabic rasm / dotless font — must use naskh with full dots
- ❌ NO sub-grids within individual cells
- ❌ NO varying column widths (all 12 columns are uniform width in v3 — the proportional ruler at the top communicates anatomical spacing instead)
- ❌ NO non-monotonic column ordering (columns must run strictly from deepest place at left to shallowest at right; no skipping or jumping)

---

## Consistency notes with the companion figure

The Sonomer Garland figure (existing) shows the Sanskrit phonology in its own internal terms. This figure (the comparative matrix) shows the same Sanskrit content as the engineered center of a comparative chart that includes two standardized phonologies.

The two figures should:

- Share the same typography and color palette
- Sit side-by-side in the book (probably in Ch 8 or as a paired figure)
- Read as companion pieces: one is "the *varṇamāla* from inside" (Sonomer Garland), the other is "the *varṇamāla* against the world" (this matrix — engineered Sanskrit anchor with standardized Korean and Arabic as connected peripheries)
- The Sanskrit hexagons in this figure should look stylistically related to the Sanskrit beads in the Sonomer Garland — same Sanskrit, different visual treatment

The reader who has just looked at the Sonomer Garland will recognize the Sanskrit content in this comparative figure as familiar territory, now placed in a wider phonological context where Sanskrit serves as the engineered visual anchor for two standardized peer systems.
