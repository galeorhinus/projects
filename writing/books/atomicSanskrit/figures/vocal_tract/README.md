# Vocal Tract Consonant Atlases — Analysis and Chart Reference

> Twenty-four-language cross-comparison of consonant inventories rendered as scatter overlays on a vocal-tract ribbon. Used in *Atomic Sanskrit* Appendix Part 3 (*Audiography*). This document covers the analytical framework, the chart-reading conventions, the inventory sources, and the technical reference for the script and configs.

---

## Table of contents

- [1. The analysis](#1-the-analysis)
- [2. Reading a chart](#2-reading-a-chart)
- [3. The 12-place axis](#3-the-12-place-axis)
- [4. The anatomical angular distribution](#4-the-anatomical-angular-distribution)
- [5. The row layout](#5-the-row-layout)
- [6. Leader lines and the number legend](#6-leader-lines-and-the-number-legend)
- [7. The 24-language atlas](#7-the-24-language-atlas)
- [8. Comparative observations](#8-comparative-observations)
- [9. Sources](#9-sources)
- [10. Technical reference](#10-technical-reference)
- [11. Files in this directory](#11-files-in-this-directory)

---

## 1. The analysis

Each chart is one language's consonant phoneme inventory plotted onto a shared coordinate system that mirrors the vocal tract. The shared coordinate system makes consonant inventories visually comparable across languages — same axes, same column meanings, same number-to-place mapping — so the eye can scan from chart to chart and pick up the structural differences without re-learning the layout each time.

What the analysis lets a reader see at a glance:

- **Which places of articulation a language uses** — sparse columns mean only some places are recruited; dense columns mean the place is heavily exploited.
- **The depth of contrast at each place** — a tall stack at one column means many manner-of-articulation distinctions there (Sanskrit's 4-row stop matrix at five places); a single dot means only one phoneme at that place.
- **The shape of the inventory** — symmetric (Tamil's 6×2 stop/nasal grid), front-heavy (English clustering at alveolar), spread-across-all-12 (Arabic's pharyngeal-to-bilabial occupation), or sparse (Nahuatl, Korku).

The deliberate analytical move is to use a *shared place axis* and let each language's *rows* vary — so place-of-articulation can be compared across languages, while manner stays a within-language axis. This trades total expressiveness (a fully-typed phonetic-feature space would have manner standardised too) for cross-language readability.

The atlas was built for *Atomic Sanskrit*'s Appendix Part 3, which compares Sanskrit, Arabic, and Korean as a starting set of three. Twelve additional languages were added to widen the comparison: a sweep across European, East Asian, Iranian, African, American, southern subcontinental, and central-eastern subcontinental inventories.

---

## 2. Reading a chart

Every chart has the same elements:

```
┌──────────────────────────────────────────────┐
│           ╭─────────────────╮                │   ← base ribbon
│         ⊙ ⊙ ⊙   ⊙   ⊙ ⊙ ⊙ ⊙                  │   ← outer row
│         ⊙ ⊙ ⊙   ⊙   ⊙ ⊙ ⊙ ⊙                  │   ← row beneath
│         ⊙ ⊙ ⊙   ⊙       ⊙                    │   ← circles = phonemes
│         ⊙ ⊙ ⊙                                │   ← innermost row
│         │ │ │   │   │ │ │ │                  │   ← radial leader segments
│         │ │ │   │   │ │ │ │                  │
│         │ │ │   │   │ │ │ │                  │   ← vertical leader segments
│         1 4 5   7   8 9   12                 │   ← number callouts
└──────────────────────────────────────────────┘
```

**The base ribbon** is a thin elliptical arc that serves as a visual anchor for the mouth — it spans 90° of arc (from 150° to 240° in the script's angle convention, with 180° at the visual top), representing the inside of the vocal tract from the lips (left) to the throat (right).

**Each circle is one phoneme.** Its position encodes two things:

- **Angular position** (where along the arc) = the *place of articulation*. The 12 columns are positioned along the arc; columns 1–6 are toward the front of the mouth (left side of the chart), columns 7–12 toward the back (right side).
- **Radial position** (how far from the chart's centre) = the *manner row*. Rows are language-specific — Sanskrit's row 0 is voiceless unaspirated stops, Arabic's row 0 is voiceless plain stops, Tamil's row 0 is just "stops" because Tamil doesn't distinguish voicing phonemically. Read what each row means by looking at the cells inside that row.

**Orientation: the mouth runs left-to-right at the top of the chart.** Lips at the left (column 1, bilabial, at angular position 150°), throat at the right (column 12, glottal, at angular position 240°). This matches the physical anatomy of a head viewed in cross-section facing right.

**The leader lines** come off the *innermost* (most-central-on-chart) filled circle in each column, run radially inward, then turn straight down. Only columns that have at least one filled circle get a leader. The number at the bottom of each leader identifies which place-of-articulation column it points to — the same number mapping is used across every chart.

The fact that only filled columns get leaders means the *set of numbers visible* is itself a quick summary: a chart showing numbers 1, 4, 5, 7, 8, 9 is using six places; one showing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 is using all twelve.

---

## 3. The 12-place axis

The columns are a standardised place-of-articulation axis. Each language's matrix is cast onto these twelve columns so the same number always means the same place.

| # | Place of articulation | Articulator | Examples |
|---:|---|---|---|
| 1 | Bilabial | both lips | /p, b, m, w/ |
| 2 | Labio-dental | lower lip + upper teeth | /f, v/ |
| 3 | Interdental | tongue between teeth | /θ, ð/ (English *th*) |
| 4 | Dental | tongue tip + upper teeth | /t̪, d̪, n̪/ (Tamil த, Sanskrit त) |
| 5 | Alveolar | tongue tip + alveolar ridge | /t, d, s, n, l, r/ (English most) |
| 6 | Post-alveolar | tongue **blade** + behind ridge | /ʃ, ʒ, tʃ, dʒ/ (English *sh*, *ch*) |
| 7 | Retroflex | tongue **tip curled back** | /ʈ, ɖ, ɳ, ʂ, ʐ/ (Sanskrit ट, Tamil ட, Mandarin tʂ) |
| 8 | Palatal | tongue body + hard palate | /c, ɟ, ɲ, j/ (Sanskrit च, Tamil ச) |
| 9 | Velar | tongue back + soft palate | /k, g, ŋ, x, ɣ/ |
| 10 | Uvular | tongue back + uvula | /q, ʁ/ (Arabic ق, French *r*) |
| 11 | Pharyngeal | tongue root + pharynx | /ħ, ʕ/ (Arabic ح, ع) |
| 12 | Glottal | vocal folds | /ʔ, h/ |

**The split between columns 6 and 7** — post-alveolar vs retroflex — is worth flagging. They share approximately the same place of contact (the area just behind the alveolar ridge), but the *articulator* differs:

- **Post-alveolar (6)** uses the tongue *blade* — the flat front portion. English /ʃ/ and /ʒ/ are post-alveolar.
- **Retroflex (7)** uses the tongue *tip*, curled backward and pointing up. Sanskrit's mūrdhanya (ट ठ ड ढ ण ष), Tamil's ட ண ள ழ, and Mandarin's tʂ-series are retroflex.

The earlier version of the chart collapsed these into one column. The current 12-column scheme keeps them distinct so that languages making the contrast (Tamil — which has both /tʃ/-like palatal ச and retroflex ட — or Hindi if it were in the set) can show it.

---

## 4. The anatomical angular distribution

The 12 columns are *not* evenly spaced around the arc. They are positioned in proportion to the actual distance from the lips to each place of articulation in the vocal tract.

The vocal tract from lips to glottis is about 17 cm (6.7 in) on average for an adult. The 12 columns are anchored at the following approximate distances:

| # | Place | Distance from lips | Angular position (°) |
|---:|---|---:|---:|
| 1 | Bilabial | 0.0 cm | 150.00° |
| 2 | Labio-dental | 0.5 cm | 152.65° |
| 3 | Interdental | 1.0 cm | 155.29° |
| 4 | Dental | 1.5 cm | 157.94° |
| 5 | Alveolar | 2.5 cm | 163.24° |
| 6 | Post-alveolar | 3.5 cm | 168.53° |
| 7 | Retroflex | 3.8 cm | 170.12° |
| 8 | Palatal | 5.5 cm | 179.12° |
| 9 | Velar | 9.0 cm | 197.65° |
| 10 | Uvular | 11.5 cm | 210.88° |
| 11 | Pharyngeal | 13.5 cm | 221.47° |
| 12 | Glottal | 17.0 cm | 240.00° |

Mapping formula: `θ = 150° + (distance_cm / 17 cm) × 90°`.

The deliberate consequence is that the front of the mouth (columns 1–7, lip through retroflex) is *compressed* into the first 20° of arc, while the back of the mouth (columns 8–12, palatal through glottal) is *stretched* across the remaining 70°. This is faithful to anatomy: phonetic distinctions in the front of the mouth genuinely happen in millimetres (lip–teeth–ridge are all within a few centimetres of each other), while distinctions in the back of the mouth happen across centimetres (the velar–uvular–pharyngeal–glottal series spans 8 cm).

A reader noticing that the front-of-mouth columns crowd together is reading a real anatomical fact, not a layout flaw.

The script also supports two other distribution modes — `uniform` (equal angular spacing) and `sqrt` (square-root warped, midway between uniform and anatomical). The 16 production charts use **anatomical** mode; the other modes are available via `--angular-mode` for experimentation.

---

## 5. The row layout

Rows are anchored at the chart's *innermost* radius and grow *outward*. The configuration parameter is `rows.r_inner = 2.0`, meaning the innermost (last-index) row sits at radius 2.0 from the chart's center. Each earlier row steps outward by `delta_r = 0.1`.

For a language with N rows:

- Row 0 (outermost, drawn furthest from chart center) sits at radius `2.0 + (N − 1) × 0.1`
- Row N−1 (innermost, drawn closest to chart center) sits at radius 2.0

Tamil has 5 rows, so its outermost row is at r=2.4. Sanskrit has 7 rows, outermost at r=2.6. Santali has 9 rows, outermost at r=2.8. Arabic has 12 rows, outermost at r=3.1.

**Row meanings are language-specific.** There is no enforced "row 0 = stops, row 1 = aspirated, row 2 = voiced" convention across languages — each chart's row structure is dictated by the manner-of-articulation contrasts the language actually makes. Sanskrit's seven rows are: voiceless unaspirated stops, voiceless aspirated stops, voiced unaspirated stops, voiced aspirated stops, nasals, semivowels, sibilants — the canonical varga ordering. Tamil's five rows are: voiceless stops, nasals, laterals, taps/approximants, glides. Quechua's nine rows distinguish plain, aspirated, and ejective stops at each place. Read the row labels by looking at the inventory inside each row.

**Why outward growth.** Earlier versions of the chart anchored rows at the *center* of the ribbon (each row spreading inward and outward from the centerline). The outward-from-r=2.0 anchor places dots on a clean, compact arc-band above the leader lines, leaves the chart's inner area free for the leader lines and the bottom number row, and gives every chart a consistent visual "base" regardless of how many rows the language needs.

---

## 6. Leader lines and the number legend

Each filled column (any column that has at least one circle) gets a two-segment leader line:

1. **Radial segment**: from `(innermost filled cell's r − 0.1)` along the column's theta, running radially inward to `r = 1.9`.
2. **Vertical segment**: from the radial endpoint, straight down (constant x), to a y-coordinate placed so that the leader's bottom endpoint sits approximately 0.5 inches above the canvas bottom edge.

A number callout is then placed about 0.05 inches below the leader's bottom endpoint. The number is the column index + 1 — that is, 1 for bilabial, 2 for labio-dental, …, 12 for glottal.

**The number is the legend key.** The mapping is consistent across every chart in the atlas: if you look at one chart and see numbers 1, 4, 5, 7, 8, 9, you know — without re-reading per-chart labels — that this language uses bilabial, dental, alveolar, retroflex, palatal, and velar places (and only those).

Languages with sparse inventories have only a few numbers visible; languages with dense inventories show many. The number set itself becomes a fingerprint.

**Empty columns are silent.** A column without any filled cells gets no leader and no number — which itself is informative. Tamil's chart shows no 6 (post-alveolar), no 10 (uvular), no 11 (pharyngeal), no 12 (glottal) — those absences are the inventory's structural shape.

---

## 7. The 24-language atlas

The atlas covers four broad regions of inventory shape. Within each region, languages were selected to illustrate distinctive structural patterns rather than to make a representative sample.

### 7.1 Sanskrit, Tamil — engineered and symmetric

**Sanskrit** ([scatter_sanskrit.svg](build/scatter_sanskrit.svg)) — the Pāṇinian inventory. 7 rows × 5 occupied columns. The defining feature is the five-varga structure: voiceless unaspirated, voiceless aspirated, voiced unaspirated, voiced aspirated, and nasal, all matched at five places (bilabial, dental, retroflex, palatal, velar) — a 4×5 stop matrix that no other language in the set replicates with this completeness. Cells: 33. Columns lit: 1, 4, 7, 8, 9.

**Tamil** ([scatter_tamil.svg](build/scatter_tamil.svg)) — the symmetric southern subcontinental inventory. 5 rows × 6 occupied columns. One voiceless stop per place across six places (bilabial, dental, alveolar, retroflex, palatal, velar) and one nasal per place. Voicing is allophonic rather than phonemic — Tamil's inventory does not encode a voicing distinction in writing, even though voiced realisations occur. Unique: the retroflex approximant ழ /ɻ/ (the *zha* of *Tamiḻ*). Cells: 18. Columns lit: 1, 4, 5, 7, 8, 9.

### 7.2 Mundari, Korku, Santali — three Munda inventories

Three languages of the Munda people of the Chotanagpur plateau and surrounding regions in eastern subcontinent. Sister languages within the group include Ho and Sora. The three charts show what happens to a shared base inventory under different intensities of contact with Sanskritic / Indic languages.

**Korku** ([scatter_korku.svg](build/scatter_korku.svg)) — Satpura range and Mahadeo hills (Madhya Pradesh, Maharashtra). The most conservative of the three. 5-place voiceless/voiced stop pairs, four matched nasals, /s, h, l, r, w, j/. No phonemic glottal stop, no integrated aspirated stops. Cells: 20. Columns lit: 1, 4, 5, 7, 8, 9, 12.

**Mundari** ([scatter_mundari.svg](build/scatter_mundari.svg)) — Jharkhand, Odisha, West Bengal. Adds the phonemic glottal stop /ʔ/ at column 12 to the Korku baseline. Otherwise structurally identical to Korku. Cells: 21. Columns lit: same as Korku.

**Santali** ([scatter_santali.svg](build/scatter_santali.svg)) — the most widely spoken language of the Munda people, written in its own Ol Chiki script as well as Devanagari, Bengali, and Roman. The most contact-influenced of the three: integrates the full four-way Sanskrit-style stop matrix (voiceless / voiceless-aspirated / voiced / voiced-aspirated) across all five stop places, plus the retroflex flap /ɽ/. Cells: 31. Columns lit: same 7 as Korku and Mundari — what differs is the *row depth*.

Side-by-side, the three Munda charts make the contact-history visible: same set of columns lit, very different row depths.

### 7.3 The IPA-compact set — eight reference inventories

These eight follow standard published phonemic analyses of each language. They serve as anchors against which the more structurally distinctive charts (Sanskrit, Tamil, the Munda set, Arabic, the Bantu pair, the Americas pair) can be read.

**English** ([scatter_english.svg](build/scatter_english.svg)) — General-American/Received-Pronunciation phoneme inventory. Cluster-heavy at alveolar (5) and adjacent columns. The two interdental fricatives /θ, ð/ at column 3 are an unusual feature among the world's languages — only a handful retain them. Cells: 24.

**French** ([scatter_french.svg](build/scatter_french.svg)) — Metropolitan standard. The signature is the uvular /ʁ/ at column 10 (the French *r*) — no other European language in the set uses column 10. No interdental fricatives, no /h/. Cells: 21.

**Japanese** ([scatter_japanese.svg](build/scatter_japanese.svg)) — Standard (Tokyo) Japanese. Compact inventory; the lone /ɸ/ (the *fu* of *Fuji*) is a marker. No phonemic /l/–/r/ distinction (the famously single liquid). Cells: 21.

**Korean** ([scatter_korean.svg](build/scatter_korean.svg)) — Standard Seoul. Three-way stop contrast (plain, aspirated, tensed) at three places (bilabial, dental, velar) — a typologically rare pattern. The post-alveolar affricate column carries the same three-way contrast (ㅈ, ㅊ, ㅉ). Cells: 21.

**Mandarin** ([scatter_mandarin.svg](build/scatter_mandarin.svg)) — Standard (Beijing-based) Mandarin. Distinctive three-way affricate contrast at three different places: alveolar (ts, tsʰ), retroflex (tʂ, tʂʰ), and palatal (tɕ, tɕʰ). No voiced stops, no fricative voicing pairs. Cells: 24.

**Farsi** ([scatter_farsi.svg](build/scatter_farsi.svg)) — Modern Persian. Retains the uvular column (q, x, ɣ) under Arabic influence; rich fricative inventory across alveolar, post-alveolar, labio-dental. Cells: 25.

**Arabic** ([scatter_arabic.svg](build/scatter_arabic.svg)) — Modern Standard Arabic. The widest place-of-articulation spread in the set — 11 of 12 columns populated (only column 7 / retroflex is unused), including the pharyngeals (ح ع at column 11) that almost no other language uses. The emphatic ("pharyngealised") consonants are not shown as a separate row but live among the regular cells. Cells: 28.

### 7.4 Swahili, Zulu — two Bantu inventories

**Swahili** ([scatter_swahili.svg](build/scatter_swahili.svg)) — the East African lingua franca. Standard Bantu shape: voiceless / voiced stop pairs, four nasals, the velar fricative ɣ, palatal nasal ɲ. The interdental fricatives θ ð (rendered as ث ذ in Arabic-script-source loanwords) and labio-dental fricatives /f, v/ enter through Arabic-source vocabulary. Cells: 23.

**Zulu** ([scatter_zulu.svg](build/scatter_zulu.svg)) — southern African (KwaZulu-Natal and surrounding). The defining feature: three click consonants (ǀ dental click, ǁ lateral-alveolar click, ǃ post-alveolar click) — no other language in the set uses click consonants. The current placement of the clicks in the matrix is being revisited (the lateral and post-alveolar clicks need to land on their phonetically-correct columns 5/6 rather than the columns they are currently rendered at). Ejective fricatives, breathy-voiced stops, the bilabial implosive ɓ are additional distinctive markers. Cells: 32.

### 7.5 Quechua, Nahuatl — two American inventories

**Quechua** ([scatter_quechua.svg](build/scatter_quechua.svg)) — Cuzco–Bolivian Quechua. The defining feature: a three-way stop contrast (plain / aspirated / ejective) at four places — bilabial (p, pʰ, pʼ), dental (t, tʰ, tʼ), velar (k, kʰ, kʼ), and uvular (q, qʰ, qʼ) — three rows tall across columns 1, 4, 9, 10. Palatal nasal /ɲ/ and palatal lateral /ʎ/. Cells: 24.

**Nahuatl** ([scatter_nahuatl.svg](build/scatter_nahuatl.svg)) — Classical Nahuatl (the language of the Mexica). The defining feature: *no voiced stops anywhere* — a striking absence visible as a missing row. The lateral affricate /tɬ/ in the alveolar column is uniquely Mesoamerican; labialised velar /kʷ/ in the velar column. One of the sparsest inventories in the set. Cells: 16.

### 7.6 Southern and central-subcontinent set — Gondi, Kui, Kuvi, Kolami, Kurukh, Telugu, Malayalam, Brahui

Eight languages of the southern subcontinent, central-eastern forest belt, and the geographic outlier in Balochistan. The orthodoxy classifies all eight under a single family-tree label ("Dravidian"); the atlas treats them as languages of overlapping regions and lets the inventories speak. Read side-by-side, the eight charts make visible how much of the family-tree's perceived unity is regional and how much is a discipline-internal classification artifact.

**Gondi** ([scatter_gondi.svg](build/scatter_gondi.svg)) — spoken by the Gondi people of the central forest belt (Madhya Pradesh, Chhattisgarh, Maharashtra, Telangana, and neighbouring states). One of the most widely-spoken languages of the central-subcontinent forest-belt communities. Five-place voiceless/voiced stop matrix, five matched nasals, alveolar /l/ + retroflex /ɭ/ laterals, trill /r/, /s/, /h/, glides /w, j/. Native inventory; aspirates appear in Sanskritic loanwords and are not separate phonemes here. Cells: 22. Columns lit: 1, 4, 5, 7, 8, 9, 12.

**Kui** ([scatter_kui.svg](build/scatter_kui.svg)) — spoken by the Kondh people of Odisha (Kandhamal district and surrounding). Five-place voiceless/voiced stops, four nasals (no palatal nasal /ɲ/), both laterals, trill, /s/, /h/, glides. Cells: 21. Columns lit: 1, 4, 5, 7, 8, 9, 12.

**Kuvi** ([scatter_kuvi.svg](build/scatter_kuvi.svg)) — spoken by the Kondh people of the Odisha–Andhra Pradesh border. The closest sister language to Kui — the closeness is the point, and the chart shows it visually. Same column-set and same row-depth as Kui. Cells: 21. Columns lit: identical to Kui.

**Kolami** ([scatter_kolami.svg](build/scatter_kolami.svg)) — spoken by the Kolami people of the Adilabad / Yavatmal region (Telangana–Maharashtra border); a relatively small speech community. The sparsest of the central-forest-belt charts: no retroflex lateral, no /h/. Cells: 19. Columns lit: 1, 4, 5, 7, 8, 9.

**Kurukh** ([scatter_kurukh.svg](build/scatter_kurukh.svg)) — spoken by the Oraon people of Jharkhand and surrounding areas (Bihar, West Bengal, parts of Chhattisgarh). Adds the retroflex flap /ɽ/ that the southern-subcontinent languages don't typically include. Cells: 22. Columns lit: 1, 4, 5, 7, 8, 9, 12.

**Telugu** ([scatter_telugu.svg](build/scatter_telugu.svg)) — the largest non-Indo-European language of the subcontinent by speaker count (Andhra Pradesh, Telangana, and diaspora). Heavy absorption of Sanskritic vocabulary has integrated the full four-way stop voicing × aspiration contrast — structurally identical to Sanskrit's 4-row stop matrix but built from absorption rather than native engineering (the same pattern Santali shows). Three sibilants (/s, ʃ, ʂ/), five nasals, glottal /h/, both laterals, trill, glides. Cells: 34. Columns lit: 1, 4, 5, 6, 7, 8, 9, 12.

**Malayalam** ([scatter_malayalam.svg](build/scatter_malayalam.svg)) — spoken in Kerala. Among the densest retroflex inventories anywhere: phonemic retroflex stop /ʈ ɖ/, nasal /ɳ/, sibilant /ʂ/, lateral /ɭ/, and flap /ɽ/ — five retroflex consonants, more than any other language shown. Full 4-row stop matrix from Sanskritic absorption. Labio-dental approximant /ʋ/ instead of /w/. Cells: 35 — the densest single-language chart in the entire set. Columns lit: 1, 2, 4, 5, 6, 7, 8, 9, 12.

**Brahui** ([scatter_brahui.svg](build/scatter_brahui.svg)) — spoken by the Brahui people of Balochistan (Pakistan); a geographically isolated speech community far from the southern-subcontinent languages it is grouped with by the orthodoxy. Heavy Persian / Balochi / Arabic contact has reshaped the inventory: uvular /q/, uvular fricatives /x, ɣ/, pharyngeal /ħ/, the glottal stop /ʔ/, and labio-dental /f/. None of these appear in Gondi, Kui, Kuvi, Kolami, Kolami, or Kurukh. The chart's inventory shape resembles Farsi more than the central-forest-belt languages — a polemic point in itself about what the orthodoxy's family-tree classification holds together. Cells: 28. Columns lit: 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12.

---

## 8. Comparative observations

When the charts are placed side-by-side, several patterns become visible. None of these is asserted as a finding *of* the atlas — the atlas is the visualization; the patterns are what the visualization makes legible.

### 8.1 The Indic-cluster density spectrum

| Language | Cells | Columns lit | Row depth |
|---|---:|---|---|
| Korku | 20 | 1, 4, 5, 7, 8, 9, 12 | shallow (7 rows) |
| Mundari | 21 | same as Korku | shallow (7 rows) |
| Tamil | 18 | 1, 4, 5, 7, 8, 9 | shallowest (5 rows) |
| Santali | 31 | same as Korku | deeper (9 rows) |
| Sanskrit | 33 | 1, 4, 7, 8, 9 | deep (7 rows) |

Tamil and the Munda languages share the *outline* of the inventory (which places are used) but vary in *depth*. Santali's deep stop matrix mirrors Sanskrit's deep stop matrix — built from absorption rather than native engineering, but visually congruent.

### 8.2 Column-12 (glottal) occupancy

A small but informative diagnostic. The chart lights up column 12 when a language has a phonemic glottal stop /ʔ/ or a phonemic /h/. The pattern:

- Lit (has /h/ or /ʔ/): Mundari, Korku, Santali (all have /h/; Mundari adds /ʔ/), English, Farsi, Arabic (has both), Swahili (has /h/), Zulu, Quechua, Nahuatl, Mandarin (has /h/), Japanese (has /h/), Korean (has /h/)
- Dark: Sanskrit, Tamil, French

Sanskrit's apparent column-12 absence in the current atlas is a *data placement* of ह at column 9 (velar) rather than column 12 (glottal). The Sanskrit grammarian tradition classifies ह as *kaṇṭhya* (throat / velar area) — in standardised IPA terms ह is glottal /ɦ/, column 12. The placement reflects the Pāṇinian classification rather than the IPA classification. (This is a known reading-of-the-source choice rather than a bug; it can be moved if the IPA standard takes precedence for a particular use of the chart.)

### 8.3 The widest and narrowest spreads

- **Widest** — Arabic, 11 of 12 columns populated (column 7 / retroflex is the one place Arabic does not use). The pharyngeal column (11) is essentially Arabic-exclusive in the set.
- **Narrowest** — Tamil at 6 columns; Sanskrit, Nahuatl at 5 columns each. The *narrowness* doesn't mean impoverished — Sanskrit fills its five columns with up to four rows each.

### 8.4 Structurally unique markers

| Marker | Language |
|---|---|
| Click consonants (currently at columns 3, 4, 9 in the chart — placements may be revisited per standard IPA classification of clicks at dental, lateral-alveolar, and post-alveolar) | Zulu |
| Three-way ejective contrast at 4 places (bilabial, dental, velar, uvular) | Quechua |
| Three-way affricate contrast at columns 5, 7, 8 (alveolar, retroflex, palatal) | Mandarin |
| Pharyngeals at column 11 (sole language in the set using column 11) | Arabic |
| Uvular /ʁ/ at column 10 (sole occupant in the European inventories shown) | French |
| Lateral affricate /tɬ/ at column 5 | Nahuatl |
| Retroflex approximant /ɻ/ at column 7 | Tamil (ழ) |
| Three-way plain/aspirated/tensed stop contrast at 3 places (bilabial, dental, velar) | Korean |
| Interdental fricatives at column 3 | English (θ, ð); Arabic (ث, ذ, ظ); Swahili (loanword θ, ð) |
| No phonemic voiced stops | Nahuatl, Mandarin |
| Full 4-way voicing × aspiration matrix | Sanskrit (engineered), Santali (absorbed) |

---

## 9. Sources

### 9.1 Sanskrit

Inventory and matrix structure follow the Pāṇinian *varga* organisation as documented in the *Aṣṭādhyāyī* and its standard commentaries. The 5×7 matrix (5 *vargas* across 7 manner rows) is the table appearing in *Atomic Sanskrit* Appendix Part 3 §3.1 — voiceless unaspirated / voiceless aspirated / voiced unaspirated / voiced aspirated / nasal across bilabial / dental / retroflex / palatal / velar, plus the semivowel row (y, r, l, v) and the sibilant row (s, ṣ, ś, h). This is the canonical reference for the Sanskrit chart.

The placement of ह at column 9 in the current chart reflects the Pāṇinian *kaṇṭhya* (throat/velar) classification. In IPA terms ह is glottal /ɦ/ at column 12. Either placement is defensible; the chart currently follows the Pāṇinian convention.

### 9.2 Tamil, Telugu, Malayalam, Gondi, Kui, Kuvi, Kolami, Kurukh, Brahui

Tamil consonants follow the traditional Tamil grammatical organisation (the *meyyeḻuttu* — pure consonants). The five rows shown — stops, nasals, laterals, tap + retroflex approximant, glides — are the standard analytical groupings used in Tamil phonology references (e.g., the descriptions in Schiffman's *Reference Grammar of Spoken Tamil*, Cambridge 1999, and standard Tamil phonology summaries).

The 6-place symmetric stop/nasal grid is universally recognised as Tamil's defining structural feature; the inclusion of ழ /ɻ/ as a unique retroflex approximant is similarly universal in Tamil phonology references.

Telugu, Malayalam, Gondi, Kui, Kuvi, Kolami, Kurukh, and Brahui inventories follow standard published phonemic analyses, with Krishnamurti's *The Dravidian Languages* (Cambridge Language Surveys, 2003) as the primary reference for the smaller languages of the central forest belt (Gondi, Kui, Kuvi, Kolami, Kurukh) and the geographic outlier (Brahui). Steever (ed.), *The Dravidian Languages* (Routledge Language Family Series, 1998) and Andronov's grammars cover the larger languages (Tamil, Telugu, Malayalam) in additional detail. Asher and Kumari, *Malayalam* (Routledge Descriptive Grammars, 1997) provides the Malayalam analysis used here; Krishnamurti and Gwynn, *A Grammar of Modern Telugu* (Oxford, 1985) provides the Telugu one.

The atlas labels these languages by name and regional anchor — the family-tree taxonomy ("Dravidian") that the orthodoxy applies to them is rejected per the project's conventions. Calling Brahui (spoken in Balochistan, in heavy Persian / Arabic / Balochi contact) a sister of Tamil (spoken 2,500 km away with no comparable contact pressures) on the basis of regular sound correspondences is the orthodoxy's claim; the atlas neither endorses nor enforces it. The charts simply show what each language's inventory actually looks like.

### 9.3 Mundari, Korku, Santali

The three Munda inventories follow standard published phonemic analyses:

- General reference for the lineage: G. D. S. Anderson (ed.), *The Munda Languages* (Routledge Language Family Series, 2008).
- Santali: L. Neukom, *A Grammar of Santali* (Lincom Studies in Asian Linguistics, 2001).
- Mundari: T. Osada, *A Reference Grammar of Mundari* (Institute for the Study of Languages and Cultures of Asia and Africa, 1992); Anderson and Osada, "Mundari," in Anderson 2008.
- Korku: N. H. Zide, "Korku," in Anderson 2008; A. R. K. Zide and N. H. Zide, "Proto-Munda cultural vocabulary," in *Austroasiatic Studies* (1976).

The famous "checked" (glottalised) word-final stop allophones of the lineage are documented in all three primary sources; the atlas does not show them as separate phonemes because their phonemic status is debated — they are typically analysed as positional allophones of the regular stops rather than independent phonemes.

The aspirate row in the Santali chart reflects Neukom's treatment of aspirates as integrated phonemes; aspirates in Mundari and Korku are more restricted (loanword-confined) and are not shown as separate rows in those charts.

### 9.4 European, East Asian, Iranian, African, American inventories

These follow widely-published standard phonemic analyses:

- **English** (General American / Received Pronunciation): standard IPA phonemic descriptions as documented in Roach, *English Phonetics and Phonology* (Cambridge); Ladefoged and Johnson, *A Course in Phonetics*.
- **French** (Metropolitan): Tranel, *The Sounds of French* (Cambridge); Fougeron and Smith, "French" in the *Journal of the International Phonetic Association* Illustration series.
- **Japanese** (Standard Tokyo): Vance, *The Sounds of Japanese* (Cambridge); the *JIPA* Illustration entry for Japanese.
- **Korean** (Standard Seoul): Sohn, *The Korean Language* (Cambridge); Lee and Ramsey, *The Korean Language* (SUNY Press).
- **Mandarin** (Standard Beijing): Duanmu, *The Phonology of Standard Chinese* (Oxford); the *JIPA* Illustration entry for Standard Chinese.
- **Farsi** (Modern Persian): Mahootian, *Persian* (Routledge); Windfuhr, *Persian Grammar* (Mouton).
- **Arabic** (Modern Standard): Watson, *The Phonology and Morphology of Arabic* (Oxford); Holes, *Modern Arabic* (Georgetown).
- **Swahili**: Hyman, "Bantu Phonology" in *The Cambridge Handbook of Phonology*; standard Swahili grammar references.
- **Zulu**: Doke, *Textbook of Zulu Grammar*; the *JIPA* Illustration entry for Zulu; standard Bantu click-language references.
- **Quechua** (Cuzco–Bolivian): Cusihuamán, *Diccionario Quechua: Cuzco–Collao*; standard Quechua phonology references.
- **Nahuatl** (Classical): Andrews, *Introduction to Classical Nahuatl* (University of Oklahoma); standard Mesoamerican linguistics references.

These references are the standard sources for the phonemic inventories shown; the matrix structure for each chart casts the published inventory onto the shared 12-column place axis.

### 9.5 Vocal tract distances

The lip-to-place distances used for the anatomical angular distribution (the table in §4) are approximate adult-male averages drawn from standard articulatory-phonetics references — Ladefoged and Maddieson, *The Sounds of the World's Languages* (Blackwell, 1996); Stevens, *Acoustic Phonetics* (MIT Press, 1998); and the standard IPA articulator-position diagrams. Individual measurements vary by speaker (adult-female vocal tract length is closer to 14–15 cm); the 17 cm anchor and the table values are representative rather than exact.

---

## 10. Technical reference

### 10.1 File structure

The figure pipeline is three Python files plus per-language JSON configs:

- [vocal_tract_schematics.py](vocal_tract_schematics.py) — the geometry primitives (`point_at`, `tangent_at`, `outward_normal_at`, `build_ribbon_path_d`, `elliptical_ribbon_svg`). The angle convention used everywhere: 0° at the 6 o'clock position, increasing clockwise (so 90° is 9 o'clock, 180° is 12 o'clock, 270° is 3 o'clock).
- [vocal_tract_regions.py](vocal_tract_regions.py) — composer for ribbon-arc atlases with optional region bands and labels. Used for region-of-articulation overview figures (not the scatter atlases).
- [vocal_tract_scatter.py](vocal_tract_scatter.py) — the scatter-overlay renderer used for all 16 language atlases. Imports from `vocal_tract_schematics.py`.

The script depends only on Python's standard library — no numpy, matplotlib, or external SVG libraries. SVG is emitted directly as text.

### 10.2 Geometry parameters

All 16 production configs use the same geometry:

```json
"geometry": {
  "r1": 2.25,     // ellipse semi-major axis (inches)
  "r2": 2.25,     // ellipse semi-minor axis (inches) — equal to r1 = circular ribbon
  "w": 0.35       // ribbon width (inches)
},
"canvas": {
  "width": 4.5,   // canvas width (inches)
  "height": 3.0   // canvas height (inches)
}
```

The base ribbon is the arc from `t1=150°` to `t2=240°` on this geometry. Stroke is `#bbbbbb` at 0.01 in width, opacity 0.7.

### 10.3 Scatter parameters

```json
"scatter": {
  "mode": "grid",                          // grid (deterministic) or jitter (randomised within cell)
  "angular_range": {
    "mode": "anatomical",                  // or "uniform" or "sqrt"
    "center": 195,                         // angular midpoint of the chart
    "half_width_deg": 45,                  // ±45° around center = 150° to 240°
    "distances": [0.0, 0.5, 1.0, 1.5, 2.5, 3.5, 3.8, 5.5, 9.0, 11.5, 13.5, 17.0]
  },
  "rows": {
    "delta_r": 0.1,                        // row spacing (inches)
    "r_inner": 2.0                         // innermost row radius (inches)
  },
  "circle_radius": 0.05,                   // dot radius (inches)
  "fill_color": "#666666",
  "opacity": 0.5,
  "matrix": [ ... ]                        // n_rows × 12 array of consonant labels
}
```

The matrix is row-major. Empty strings (`""`) mean no phoneme at that (row, column) cell — these produce no dot. Non-empty strings (Devanagari, IPA, Tamil script, etc.) are rendered as the dot's label is *not* used (the script renders dots without per-dot text — the visible content of each dot is just the circle).

### 10.4 Place label parameters

```json
"place_labels": {
  "labels": [
    "bilabial", "labio-d.", "interdent.", "dental", "alveolar",
    "post-alv.", "retroflex", "palatal", "velar", "uvular",
    "pharyngeal", "glottal"
  ],                                       // documentation / legend source
  "show_numbers": true,                    // render col_idx + 1 as the callout
  "leader_inner_r": 1.9,                   // radial endpoint of the leader segment
  "leader_gap": 0.1,                       // gap from innermost dot to leader start
  "leader_stroke_color": "#888888",
  "leader_stroke_width": 0.005,
  "font_size": 0.1528,                     // 11pt at 1 user unit = 1 inch
  "color": "#222222",
  "label_gap": 0.05,                       // gap between leader endpoint and text top
  "bottom_margin": 0.5                     // distance from leader endpoint to canvas bottom
}
```

The `y_label` field (leader bottom y) is derived dynamically by default — computed so the leader endpoint sits `bottom_margin` inches above the auto-centred canvas bottom regardless of how many rows the chart has. Set `y_label` explicitly to override.

### 10.5 CLI usage

```bash
# Generate the standard SVG for a language:
python3 vocal_tract_scatter.py configs/scatter_sanskrit.json

# Override the dot mode (grid is default):
python3 vocal_tract_scatter.py configs/scatter_sanskrit.json --mode jitter

# Override the angular distribution:
python3 vocal_tract_scatter.py configs/scatter_sanskrit.json --angular-mode uniform
python3 vocal_tract_scatter.py configs/scatter_sanskrit.json --angular-mode sqrt

# Custom output path:
python3 vocal_tract_scatter.py configs/scatter_sanskrit.json -o /tmp/sanskrit.svg
```

Default output path is `../build/vocal_tract/<name>.svg` (relative to the script). When `--mode` or `--angular-mode` is set to a non-default value, the value is appended to the output filename (e.g., `scatter_sanskrit_uniform.svg`).

### 10.6 Adding a new language

1. Create `configs/scatter_<lang>.json`, copying the structure of an existing config.
2. Fill in `description` with the regional anchor, sister languages (if any), and the distinguishing inventory features.
3. Pick a unique `jitter.seed` value (existing seeds are visible in the configs; the values are prime numbers for ease).
4. Replace the `matrix` with the language's inventory cast onto the 12 columns. Use IPA symbols, native script, or romanisation as appropriate; the matrix cell text is documentation — the rendered chart shows only circles and numbers.
5. Run `python3 vocal_tract_scatter.py configs/scatter_<lang>.json` to generate the SVG.
6. Add the language entry to §7 of this README.

---

## 11. Files in this directory

### Scripts

- `vocal_tract_schematics.py` — geometry primitives
- `vocal_tract_regions.py` — ribbon-arc atlas composer (regions / labels)
- `vocal_tract_scatter.py` — scatter-overlay renderer (this atlas)

### Configs

The 16 language configs in `configs/`:

| Config | Language | Cells | Columns lit |
|---|---|---:|---|
| [scatter_sanskrit.json](configs/scatter_sanskrit.json) | Sanskrit | 33 | 1, 4, 7, 8, 9 |
| [scatter_tamil.json](configs/scatter_tamil.json) | Tamil | 18 | 1, 4, 5, 7, 8, 9 |
| [scatter_telugu.json](configs/scatter_telugu.json) | Telugu | 34 | 1, 4, 5, 6, 7, 8, 9, 12 |
| [scatter_malayalam.json](configs/scatter_malayalam.json) | Malayalam | 35 | 1, 2, 4, 5, 6, 7, 8, 9, 12 |
| [scatter_gondi.json](configs/scatter_gondi.json) | Gondi | 22 | 1, 4, 5, 7, 8, 9, 12 |
| [scatter_kui.json](configs/scatter_kui.json) | Kui | 21 | 1, 4, 5, 7, 8, 9, 12 |
| [scatter_kuvi.json](configs/scatter_kuvi.json) | Kuvi | 21 | 1, 4, 5, 7, 8, 9, 12 |
| [scatter_kolami.json](configs/scatter_kolami.json) | Kolami | 19 | 1, 4, 5, 7, 8, 9 |
| [scatter_kurukh.json](configs/scatter_kurukh.json) | Kurukh | 22 | 1, 4, 5, 7, 8, 9, 12 |
| [scatter_brahui.json](configs/scatter_brahui.json) | Brahui | 28 | 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| [scatter_mundari.json](configs/scatter_mundari.json) | Mundari | 21 | 1, 4, 5, 7, 8, 9, 12 |
| [scatter_korku.json](configs/scatter_korku.json) | Korku | 20 | 1, 4, 5, 7, 8, 9, 12 |
| [scatter_santali.json](configs/scatter_santali.json) | Santali | 31 | 1, 4, 5, 7, 8, 9, 12 |
| [scatter_english.json](configs/scatter_english.json) | English | 24 | 1, 2, 3, 4, 5, 6, 8, 9, 12 |
| [scatter_french.json](configs/scatter_french.json) | French | 21 | 1, 2, 4, 5, 6, 8, 9, 10 |
| [scatter_japanese.json](configs/scatter_japanese.json) | Japanese | 21 | 1, 4, 5, 6, 8, 9, 12 |
| [scatter_korean.json](configs/scatter_korean.json) | Korean | 21 | 1, 4, 6, 8, 9, 12 |
| [scatter_mandarin.json](configs/scatter_mandarin.json) | Mandarin | 24 | 1, 2, 5, 7, 8, 9, 12 |
| [scatter_farsi.json](configs/scatter_farsi.json) | Farsi | 25 | 1, 2, 4, 5, 6, 8, 9, 10, 12 |
| [scatter_arabic.json](configs/scatter_arabic.json) | Arabic | 28 | 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12 |
| [scatter_swahili.json](configs/scatter_swahili.json) | Swahili | 23 | 1, 2, 3, 4, 5, 6, 8, 9, 12 |
| [scatter_zulu.json](configs/scatter_zulu.json) | Zulu | 32 | 1, 2, 3, 4, 5, 6, 8, 9, 12 |
| [scatter_quechua.json](configs/scatter_quechua.json) | Quechua | 24 | 1, 4, 5, 6, 8, 9, 10, 12 |
| [scatter_nahuatl.json](configs/scatter_nahuatl.json) | Nahuatl | 16 | 1, 4, 5, 6, 8, 9, 12 |

### Build output

Generated SVGs in `../build/vocal_tract/scatter_<lang>.svg`. Regenerate any chart by running the script against its config.

### Other figures

- `example_vargas.json` / `example_vargas.svg` — a demonstration of the regions atlas (the Sanskrit varga places shown as labelled ribbon bands without the scatter overlay).

---

*Last updated alongside commit `9a7e857` (Korku + Santali atlases). Atlas authored as part of *Atomic Sanskrit* Appendix Part 3 (*Audiography*).*
