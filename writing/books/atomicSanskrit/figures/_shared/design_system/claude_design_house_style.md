# atomic_sanskrit — book illustration design system

**v1.0  —  2026-06-03**

Persistent house style for every illustration and figure-table in the *Atomic Sanskrit* book. One project in claude design; multiple chats, one per figure category. All chats read this file and the companion `book-assets.css` at the project level.

**Don't invent new fonts, greys, sizes, or filenames per figure.** Pull from the shared tokens. When a figure category genuinely needs something the tokens don't cover, extend the system in this file and `book-assets.css` first; don't fork conventions silently inside a single chat.

---

## 1. Workflow

- **Project root** holds the shared assets: this `CLAUDE.md`, `book-assets.css`, and any other cross-category resources.
- **One chat per figure category** (audiography, sonomer-garland, dhātu-architecture, scaffold-icons, analysis-charts, etc.). New categories open a new chat; existing categories continue in their dedicated chat.
- **Per-figure design briefs** live in the manuscript repo at `figures/design_sources/<category>/<filename>.md`, paired with their rendered SVG of the same name. Briefs are uploaded to the relevant chat when work begins.
- **Preserve existing figures untouched** when starting new work. New file, new entry — never silently overwrite a previous render.

---

## 2. Typography (two families only)

- **Latin (English headings, labels, IAST transliteration) → Gentium Book Plus** (italic for IAST).
- **Devanāgarī → Adobe Devanagari.**
- Weights used: **regular, italic, semibold, bold**. Never mix more than these two families.
- Preserve IAST diacritics cleanly: *ā ī ū ṛ ṝ ḷ ḹ ṭ ḍ ṇ ñ ṅ ś ṣ ṁ ṃ ḥ ē ō* etc.
- **Banned faces:** Arial, Helvetica, Inter, Roboto, system sans-serif, decorative or default presentation fonts.

**Font stacks — use these strings verbatim** (single quotes inside double-quoted SVG attributes):

```
Latin / IAST : 'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif
Devanāgarī   : 'Adobe Devanagari', 'Noto Serif Devanagari', 'Kohinoor Devanagari', 'Devanagari MT', serif
```

**Why these:**

- **Gentium Book Plus** is the canonical face: open-source (SIL OFL), full IAST diacritic coverage, matches the rendered `audiography_sound_script_standard_matrix.svg`.
- **Charter** is the print-pipeline fallback (Bitstream Charter / TeX Charter).
- **Charis SIL** is the open-source web fallback when Gentium isn't available.
- **Adobe Devanagari** is the book's house Devanāgarī (print path).
- **Noto Serif Devanagari** is the open-source serif fallback — deliberately **serif** (not Sans) so HTML preview stays visually consistent with the serif Latin face.

For zero-font-dependency deliverables, export with text **converted to outlines**.

---

## 3. Page and sizing math (critical for print)

- **Live width per figure: 4.5 in** (book is 6 × 9 trade paperback).
- Portrait figures typically ~6.25 in tall. Width is the cross-category constant; height varies.
- Figures use **SVG with a 1120-unit-wide viewBox** mapped to 4.5 in.
- Conversion: **1 pt ≈ 3.46 units**; **8 pt ≈ 28 units**.
- **Minimum text size: 8 pt (≈ 28 u).** Nothing in a legend, table, or caption may be smaller.
- Headings land around **10–11 pt (≈ 35–38 u)**.
- Quote real point sizes when discussing type — units are an internal coordinate space, not a typographic measure.

When exporting SVG, set `width="4.5in"` and the matching height (e.g. `height="6.253in"`) so the file places at true size in the manuscript.

---

## 4. Greyscale system

The book is printed black-and-white. **Grey carries meaning.** Each figure category has both shared invariants and a category-specific palette. Pull tokens from `book-assets.css`.

### Shared invariants (Tier 1)

| Role | Hex | Brightness |
|---|---|---|
| Background field | `#f4f4f3` | warm off-white |
| Ink — dark (on light fills) | `#2b2b2d` | — |
| Ink — light (on dark fills) | `#f3f2ef` | — |
| Faint grid lines | `#e5e5e5` | — |
| Manner-class group dividers | `#cccccc` | — |

**Text contrast rule:** light text (`#f3f2ef`) once a fill's luminance < ~0.66 (i.e., from the 150-grey downward); dark text (`#2b2b2d`) above that.

### Category palette: Sonomer Garland (manner-class gradient)

Light → dark gradient toward ॐ. Each varṇa bead picks its grey based on manner class.

| Role | Hex | Value |
|---|---|---|
| Stops (sparśa) | `#c8c8c8` | 200 |
| Sibilants (ūṣman) | `#969696` | 150 |
| Semivowels (antaḥstha) | `#646464` | 100 |
| Vowels (svara) | `#323232` | 50 |
| ॐ / deepest | `#000000` | 0 |

Garland connecting string: 150 grey, ~1 pt. Leader lines (when shown): 100 grey, ~1 pt, dashed. Often hidden — grey-coding usually carries the legend-to-figure mapping on its own.

### Category palette: Audiography (language markers)

Three uniform greys for the three language traditions in the comparative + extracted matrix family. Each language uses one shape + one fill consistently across all figures in the family.

| Language | Shape | Fill | Value |
|---|---|---|---|
| Sanskrit | hexagon | `#d4d4d4` | 212 |
| Arabic | circle | `#a8a8a8` | 168 |
| Korean | square | `#888888` | 136 |

**Universal-core cell tint:** `rgba(212, 151, 74, 0.08)` — a very faint warm overlay marking cells where all three languages converge in both phonetics and classification.

### Future category palettes

When a new figure category requires shared color tokens beyond Tier 1, extend `book-assets.css` (Tier 2 section) with the new palette and document it here. Don't invent fills inside a single chat.

---

## 5. File naming

Snake_case throughout. Filenames follow the manuscript convention:

```
<chapter_slug>_<descriptive_name>[_variant].<ext>
```

Examples (all real files in the project):

```
audiography_sound_script_standard_matrix.svg
audiography_sanskrit_extracted_sonomer_grid.svg
audiography_korean_extracted_engineered_script.svg
audiography_arabic_extracted_codified_sound_tradition.svg
mapping_mouth_varnamala_sonomer_garland.svg
mapping_mouth_varnamala_sonomer_garland_no_leaders.svg
```

**Chapter slugs — complete catalog of valid prefixes:**

The slug is the third segment of the manuscript filename (`as_<zone>_<seq>_<slug>.md`). Match it exactly when naming any figure for that chapter.

**Front matter** (zone 0):

| Slug | Manuscript file | What it covers |
|---|---|---|
| `about_series` | `as_0_00_about_series.md` | Series front-matter / volume positioning |
| `preface` | `as_0_01_preface.md` | Preface |
| `acknowledgements` | `as_0_02_acknowledgements.md` | Acknowledgments |
| `prologue` | `as_0_03_prologue.md` | Prologue (*The Prosecution*) |
| `note_on_notes` | `as_0_04_note_on_notes.md` | Note on endnotes / companion |

**Body chapters** (zone 1):

| Slug | Manuscript file | What it covers |
|---|---|---|
| `seekers` | `as_1_00_seekers.md` | Chapter 0 — *Seekers* |
| `botanical` | `as_1_01_botanical.md` | Chapter 1 — botanical metaphor dismantled |
| `strategic` | `as_1_02_strategic.md` | Chapter 2 — *Why the Pyramid Needs the Tree* |
| `fourth_abrahamic` | `as_1_03_fourth_abrahamic.md` | Chapter 3 — *The Fourth Abrahamic Religion* |
| `siddha` | `as_1_04_siddha.md` | Chapter 4 — *siddha* / *kārya* |
| `apabhramsa` | `as_1_05_apabhramsa.md` | Chapter 5 — *apabhraṃśa* |
| `dhatuh` | `as_1_06_dhatuh.md` | Chapter 6 — *dhātuḥ* reclaimed |
| `adivadya` | `as_1_07_adivadya.md` | Chapter 7 — *Oṃ: The Anatomy of Sound* |
| `superset` | `as_1_08_superset.md` | Chapter 8 — *The Subcontinental Sound-Field* |
| `mapping_mouth` | `as_1_09_mapping_mouth.md` | Chapter 9 — *The Varṇamālā: The Sonomeric Grid* |
| `building_dhatuh` | `as_1_10_building_dhatuh.md` | Chapter 10 — *Building the Dhātuḥ* |
| `building_kriya` | `as_1_11_building_kriya.md` | Chapter 11 — *Building the Kriyā* |
| `building_vakya` | `as_1_12_building_vakya.md` | Chapter 12 — *Building the Vākya* |
| `preservation` | `as_1_13_preservation.md` | Chapter 13 — *Why Preservation Needs Engineering* |
| `calibration` | `as_1_14_calibration.md` | Chapter 14 — *The Calibration Matrix* |
| `aural` | `as_1_15_aural.md` | Chapter 15 — *Aural Architecture* |
| `retroflex` | `as_1_17_retroflex.md` | Chapter 17 — retroflex / *āryatva* |
| `wrong_question` | `as_1_18_wrong_question.md` | Chapter 18 — *The Wrong Question* |
| `pie_in_sky` | `as_1_19_pie_in_sky.md` | Chapter 19 — *PIE in the Sky* (prosecution close) |
| `life_after_pie` | `as_1_20_life_after_pie.md` | Chapter 20 — *Life After PIE* |

**End matter** (zone 2):

| Slug | Manuscript file | What it covers |
|---|---|---|
| `epilogue` | `as_2_01_epilogue.md` | Epilogue — *Make the World Ārya* |

**Appendix parts** (zone 3):

| Slug | Manuscript file | What it covers |
|---|---|---|
| `baking` | `as_3_01_baking.md` | App Part 1 — *Baking the Mother Tongue* |
| `encyclopaedic` | `as_3_02_encyclopaedic.md` | App Part 2 — *The Encyclopaedic Confirmation* |
| `audiography` | `as_3_03_audiography.md` | App Part 3 — *The Sonomer Beneath the Audiograph* |
| `language_factory` | `as_3_04_language_factory.md` | App Part 4 — language factory |
| `by_the_numbers` | `as_3_05_by_the_numbers.md` | App Part 5 — *Dhātupāṭha by the Numbers* |
| `vedic_carrier` | `as_3_06_vedic_carrier.md` | App Part 6 — Vedic carrier |
| `codification_myth` | `as_3_09_codification_myth.md` | Appendix Part 9 — *Testing the Codification Myth* |
| `glossary` | `as_3_08_glossary.md` | App Part 8 — Glossary |

**Cross-chapter analysis slugs** (figures derived from `analysis/` bundles, may appear in multiple chapters):

| Slug | Source bundle | Used in |
|---|---|---|
| `ganah` | `analysis/ganah/` | Chapter 11, App Part 5 |
| `preface_modes` | (Preface chapter analysis) | Preface |

A new figure category — whether a new chapter or a new cross-chapter analysis — gets a new slug. Match the manuscript's existing `figures/<slug>/` subdirectory naming when one exists. If the slug is brand-new, mirror the manuscript filename's slug segment exactly.

**Deliverable formats:**

- **SVG** — primary (vector, sharpest for print). Always required.
- **PNG** — optional (state DPI; 4.5 in × 200 DPI ≈ 924 px wide).
- **PDF** — optional, on request.
- **HTML** — keep the editable source HTML named to match the figure (e.g., `audiography_sound_script_standard_matrix.html` → `.svg`).

---

## 6. SVG output requirements (critical)

The book builds via pandoc + xelatex. **External CSS does not propagate to the PDF.** Every rendered SVG must be self-contained.

1. **Inline the resolved font-family on every `<text>` element** (or in an internal `<style>` block at the top of the SVG):

   ```xml
   font-family="'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"
   ```

   For Devanāgarī text:

   ```xml
   font-family="'Adobe Devanagari', 'Noto Serif Devanagari', serif"
   ```

2. **Inline the resolved fill colors** as hex values on each `<path>` / `<rect>` / `<circle>` / `<polygon>`. Don't rely on external CSS variables; the LaTeX pipeline strips them.

3. **SVG width/height attributes** must specify physical units (`width="4.5in" height="6.253in"`), not just viewBox.

4. **Devanāgarī positioning:** shift Devanāgarī characters DOWN by approximately 8–12% of the marker height for optical centering. The *shirorekhā* top-bar puts the character's visual weight below its mathematical center; without the shift, Devanāgarī inside a hexagon or square looks top-heavy.

5. **Arabic font must be naskh with full diacritical dots** (Amiri / Noto Naskh Arabic / Scheherazade New). Rasm / kufic / dotless calligraphic styles collapse ت / ب / ث / ن into the same dotless skeleton (ٮ) and are unreadable.

6. **No IPA symbols inside phonology figures.** The audiography family uses native scripts only (Devanāgarī, Arabic naskh, Hangul jamo). IPA appears in surrounding prose; the matrix cells stay in each language's own script.

---

## 7. Working conventions

- **Build figures as self-contained HTML that renders inline SVG.** The HTML is the canonical editable source; the SVG is its compiled output. The same source exports cleanly to SVG / PNG / PDF.
- **Toggleable extras** (e.g., leader lines, footnote markers, varga-block highlights) should be a single boolean flag near the top of the render function, not scattered edits throughout the SVG.
- **Variant renders** use the `_<variant>` filename suffix: `..._no_leaders.svg`, `..._with_frequency.svg`, etc.
- **Per-figure design briefs** in `figures/design_sources/<category>/` are the source of truth for what a figure should contain. Update the brief whenever a design decision changes; don't rely on chat memory.
- **When extending the design system** (new font, new palette, new sizing convention), update both this file AND `book-assets.css`, bump versions, and note in the changelog which chats need to re-render against the new tokens.

---

## 8. Companion file

`book-assets.css` in this same directory is the machine-readable form of these tokens. HTML previews import it; SVGs inline the resolved values. The CSS comments mirror this CLAUDE.md's structure (Tier 1 invariants / Tier 2 category palettes / Tier 3 utility classes).

When the two files conflict, **this CLAUDE.md is the authoritative spec**. Update the CSS to match, not the other way around. The CSS is the compiled output of the conventions documented here.

---

## Changelog

- **v1.0 (2026-06-03)** — Initial book-wide design system. Reconciles the original `mapping_mouth` chapter-scoped CLAUDE.md with the audiography figure family and the rendered `audiography_sound_script_standard_matrix.svg`. Primary font: Gentium Book Plus. viewBox: 1120u for 4.5 in. Devanagari fallback: Noto Serif Devanagari. File naming: per-chapter slugs. Greyscale: shared invariants + category-specific palettes (Sonomer Garland gradient + audiography language markers).
