# Ch7-Ch9 Current Figure Plan

Status: current production guide for the Instrument -> Field -> Grid arc.

This file supersedes the older Ch7-Ch9 figure notes in `as_figure_production_queue.md`, `inventory_atlas_figure_plan.md`, and `ch7_ch8_ch9_merge_redivide_plan.md` for these three chapters. Those files remain useful history, but the chapter filenames and figure numbering changed during the redivide.

**2026-06-08 revision:** Ch8 §8.2 was rewritten to carry the field-vs-slot distinction in prose (an English pin / spin / bin walkthrough), and the old Figure 8.1 (sound-field-vs-sound-slot schematic) was dropped. All Ch8 figures shifted down by one. The new Figure 8.1 (Sanskrit's 23-cell base before *mahaprana*) is now built and embedded.

Current chapter files:

- Ch7: `atomicSanskrit/as_1_07_adivadya.md`
- Ch8: `atomicSanskrit/as_1_08_superset.md`
- Ch9: `atomicSanskrit/as_1_09_mapping_mouth.md`

## Narrative Arc

1. **Chapter 7: Instrument.** Show the human vocal apparatus and the range of possible language selections.
2. **Chapter 8: Field.** Show the subcontinental sound-field and the coverage surveys. Introduce snap-to-grid through neighbor gaps.
3. **Chapter 9: Grid.** Show Sanskrit's selected *varnamala* as sonomeric grid, then the *sparsha* matrix and timing grid.

## Chapter 7 Figures

| Figure | Status | Current file | Purpose | Notes |
|---|---|---|---|---|
| Figure 7.1 — The Vocal Apparatus | Embedded | `figures/adivadya/vocal_tract_anatomy.svg` | Show the original instrument: lungs, larynx, vocal cords, oral cavity, tongue, lips, nasal passage, and articulating regions. | Keep. This grounds the physical body before any Sanskrit reveal. |
| Figure 7.2 — Language Hotzones Along the Vocal Tract | Embedded | `figures/adivadya/hotzones_panels.svg` | Show that different languages select different regions from the same vocal instrument. | Keep. It prepares the reader for Ch8's inventory atlas logic. |
| Figure 7.3 — The Vocal Apparatus in Sanskrit | Embedded | `figures/adivadya/vocal_apparatus_sanskrit.svg` | Show the same instrument through Sanskrit's categories: *sthana*, *prana*, *ghosa*, and *anunasika*. | Keep. This is the bridge from modern anatomy to Sanskrit terms. |

## Chapter 8 Figures

| Figure | Status | Current file / target | Purpose | Notes |
|---|---|---|---|---|
| Figure 8.1 — Sanskrit Base Before *Mahaprana* | **Embedded (2026-06-08)** | `figures/superset/sanskrit_base_before_mahaprana.svg` | Show the 23-cell survey target after holding aside the ten heavy-breath stops. Active cells in tint, mahaprana cells as faded tiles with dashed outline. | Renders at 4.5 x 6.17 in, matches App 4 typography. Caption + ref label `#fig:ch8-sanskrit-base-before-mahaprana`. |
| Figure 8.2 — Southern Survey: 20 of 23 | Embedded | `figures/superset/sk_tamil_toda_kurukh.svg` | Show Tamil + Toda + Kurukh covering nearly the whole Sanskrit base. | Keep. Primary internal survey. |
| Figure 8.3 — Forest-Belt Survey: 18 of 23 | Embedded | `figures/superset/sk_korku_mundari_ho.svg` | Show Korku + Mundari + Ho covering most of the same base without relying on Santali. | Keep. Primary central forest-belt survey. |
| Figure 8.4 — Western IE Survey: 14 of 23 | Embedded | `figures/superset/sk_english_french_greek.svg` | External control; familiar Western European languages sit farther away from Sanskrit's base than the subcontinental sets. | Keep. Caption and SVG title should stay aligned as "Survey" or "Control"; current chapter uses "Survey." |
| Figure 8.5 — Central Asian Survey: 12 of 23 | Embedded | `figures/superset/sk_tajik_kazakh_kyrgyz.svg` | Geographic control against the Central Asian corridor claimed by the racial Arya thesis. | Keep. Caption and SVG title should stay aligned as "Survey." |
| Figure 8.6 — The Gaps Are Neighbors | **Embedded (2026-06-08)** | `figures/superset/snap_to_grid_neighbor_cells.svg` | Show unfilled southern cells ल, स, श as near-neighbor regularization decisions rather than remote absences. | Rendered by Claude Design (`.from-cd.svg`) and promoted; brief at the §8.9 swap-in. |
| Figure 8.7 — *Mahaprana* as Vertical Expansion | **Embedded (2026-06-08)** | `figures/superset/mahaprana_vertical_expansion.svg` | Two side-by-side panels: base 10 stop cells (voiceless + voiced) → after-mahāprāṇa 20 stop cells with the two aspirated rows interleaved in *varṇamālā* order. Identical column heads land the "no new mouth places" point. | Rendered by Claude Design (`.from-cd.svg`) and promoted; brief at `figures/superset/mahaprana_vertical_expansion.brief.md`. Ref label `#fig:ch8-mahaprana-vertical-expansion`. |

**Note on §8.2:** The old Figure 8.1 (sound-field vs sound-slot schematic) is no longer needed. The §8.2 prose now carries the field-vs-slot distinction through an English example: *pin* / *spin* (breath contextual inside the same "p" slot) and *pin* / *bin* (separate slots), then transitions to Sanskrit *mahaprana* and Tamil voicing. If a figure ever does land in §8.2 later, it should support that walkthrough rather than re-introduce the abstract schematic.

## Chapter 9 Figures

| Figure | Status | Current file / target | Purpose | Notes |
|---|---|---|---|---|
| Figure 9.1 — *Varnamala* as Sonomer Garland | Embedded | `figures/mapping_mouth/varnamala_sonomer_garland.svg` | Show selected sonomers as an ordered garland, not a heap. | Keep. This preserves Sanskrit's own poetic and accurate term before using engineering grids. |
| Figure 9.2 — Sanskrit Extracted: The Sonomer Grid | Embedded | `figures/audiography/sanskrit_extracted_sonomer_grid.svg` | Show the finished Sanskrit-only grid after Ch8 has named snap-to-grid. | Keep. Ch9 §9.3 is now "The Finished Grid." |
| Figure 9.3 — Control-Panel View of the *Sparsha* Matrix | Embedded | `figures/mapping_mouth/control_panel.svg` | Show five mouth-stations crossed with vocal-cord vibration, breath pressure, and nasal coupling. | Keep. Text now describes this as a four-control design. |
| Figure 9.4 — Periodic-Table View of the *Sparsha* Matrix | Placeholder | `figures/mapping_mouth/sparsha_periodic_table.svg` | Show the same 25 cells as a compact engineering table. | Optional but useful if Ch9 needs another engineering visual. |
| Figure 9.5 — Matrix Table View of the *Varnamala* | Placeholder | `figures/mapping_mouth/varnamala_matrix_table.svg` | Show the full selected inventory by class: *svarah*, *sparshah*, *antasthah*, *ushmanah*, and *ayogavaha*. | Optional if the prose/table already carries enough. Useful as a reference figure. |
| Figure 9.6 — *Mahaprana* as Vertical Expansion | Placeholder | `figures/mapping_mouth/mahaprana_vertical_expansion_grid.svg` | Reprise Ch8's breath-expansion point inside the full *sparsha* matrix. | Decide whether to reuse Figure 8.7 or make a Ch9-specific matrix version. Avoid duplicate visuals unless the second one clearly adds the completed-grid context. |

## Detailed Figure Briefs

This section consolidates the design intent that was previously split across the atlas notes, the Ch7-Ch9 redivide plan, and the Ch8 rewrite plan. It is the working brief for Claude Design, Illustrator, or any future Python/SVG pass.

### Shared Visual Conventions

- Keep Ch7 figures anatomical and descriptive. They should teach the instrument, not prosecute the thesis.
- Keep Ch8 figures field-oriented. They should show available sound-material, coverage, neighbor-gaps, and *mahaprana* as a later breath layer.
- Keep Ch9 figures grid-oriented. They should show Sanskrit's selected inventory as the finished architecture.
- Use grayscale unless an existing figure family already uses a controlled accent.
- Use the book's current typographic style: large serif figure title, italic subtitle, clear labels, restrained linework.
- Use Devanagari for Sanskrit sonomers. Add IAST only when a reader needs help reading a term.
- Avoid crowding. If a figure has to teach two ideas, split it.
- Survey figures compare contrastive inventory coordinates, not every sound a speaker can physically produce.
- Ch8 survey figures should use Sanskrit as the reference shell and show the comparison languages as markers inside the Sanskrit base coordinates.
- The Ch8 base survey temporarily holds aside the ten *mahaprana* stops: ख छ ठ थ फ / घ झ ढ ध भ. This is a method choice, not a demotion of breath.

### Figure 7.1 — The Vocal Apparatus

Current file: `figures/adivadya/vocal_tract_anatomy.svg`

Chapter job:

- Establish the human vocal tract as the original instrument before Sanskrit is introduced as a grid.
- Give readers a modern anatomical map they can trust before the chapter shifts into Sanskrit categories.

What it should contain:

- Side profile of the speaking apparatus.
- Airflow source: lungs / breath path.
- Larynx and vocal cords.
- Oral cavity and nasal cavity.
- Tongue, teeth, lips, hard palate, soft palate, epiglottis.
- Place-of-articulation arc or markers for the regions needed later: glottal, pharyngeal, uvular, velar, palatal, retroflex, alveolar, dental, labiodental, bilabial.

What it should avoid:

- No Sanskrit matrix yet.
- No coverage numbers.
- No polemic labels.

Reader takeaway:

> Speech begins as anatomy: breath, vibration, cavity, tongue, lips, and nasal coupling.

### Figure 7.2 — Language Hotzones Along the Vocal Tract

Current file: `figures/adivadya/hotzones_panels.svg`

Chapter job:

- Introduce the inventory-atlas method gently.
- Show that different languages select different "hotzones" from the same instrument.

What it should contain:

- Four stacked language panels. Current chapter text names English, Arabic, Mandarin, and Zulu.
- Same lips-to-glottis axis in every panel.
- Same region labels across all panels.
- Circles or density marks showing where each language places contrastive consonants.
- Circle size proportional to number of sounds in that region, if the figure can stay readable.
- A short caption or subtitle: "different languages select different regions from the same instrument."

What it should avoid:

- No Sanskrit comparison yet. Sanskrit can wait until Ch8/Ch9.
- No ancestry claims.
- No frequency claims. These are inventory selections, not usage counts.

Reader takeaway:

> The mouth is shared; each language selects differently.

### Figure 7.3 — The Vocal Apparatus in Sanskrit

Current file: `figures/adivadya/vocal_apparatus_sanskrit.svg`

Chapter job:

- Bridge modern anatomy to Sanskrit's own technical vocabulary.
- Prepare readers for Ch8's sound-field survey and Ch9's grid.

What it should contain:

- Same underlying vocal apparatus as Figure 7.1, but with Sanskrit operating categories.
- Five Sanskrit place labels:
  - कण्ठ्य (*kaṇṭhya*)
  - तालव्य (*tālavya*)
  - मूर्धन्य (*mūrdhanya*)
  - दन्त्य (*dantya*)
  - ओष्ठ्य (*oṣṭhya*)
- Control categories:
  - स्थान (*sthāna*) = place
  - प्रयत्न (*prayatna*) = effort / manner
  - प्राण (*prāṇa*) = breath pressure
  - घोष (*ghoṣa*) = vocal-cord vibration
  - अनुनासिक (*anunāsika*) / नासिका (*nāsikā*) = nasal coupling / nasal cavity

What it should avoid:

- Do not make this a full *varnamala* table.
- Keep it anatomical, not tabular.

Reader takeaway:

> Sanskrit names the same physical controls modern speech science names: place, effort, breath, voicing, and nasal coupling.

### Figure 8.1 — Sanskrit Base Before *Mahaprana*

Current file: `figures/superset/sanskrit_base_before_mahaprana.svg`

Status: **rendered + embedded (2026-06-08).** Python source at `figures/superset/sanskrit_base_before_mahaprana.py`; reuses the auto-format pipeline from `_shared/toolkits/vocal_tract/quad_overlay.py` so the figure ships at 4.5 in wide alongside the App 4 surveys.

Chapter job:

- Make the survey target visible before the comparison begins.
- Show why the chapter tests 23 cells before bringing back *mahaprana*.

What the rendered figure carries:

- Sanskrit consonant reference shell across 6 place columns (BIL, DEN, RET, PAL, VEL, GLO) and 9 manner rows.
- Active 23-cell base with full tint (#e6e3db) and dark Devanagari (#2b2b2d):
  - क च ट त प
  - ग ज ड द ब
  - ङ ञ ण न म
  - य र ल व
  - श ष स ह
- Ten *mahaprana* stop cells held aside as faded tiles (#f0eee8) with dashed outline and gray Devanagari (#a8a39a):
  - ख छ ठ थ फ
  - घ झ ढ ध भ
- Two-chip header legend: "Base cells · 23" / "Held aside · 10."
- Title: "Sanskrit's 23-cell Base · Mahāprāṇa Rows Held Aside."
- Subtitle: "Heavy-breath stops held aside (faded) for the chapter's comparison — ख · छ · ठ · थ · फ and घ · झ · ढ · ध · भ."
- Caption: "Filled tile = lit cell · faded tile + dashed outline = held aside for §§8.6–8.8."

Reader takeaway:

> The first test asks whether the subcontinental field supplies Sanskrit's base before the breath-pressure layer is added.

### Figure 8.2 — Southern Survey: 20 of 23

Current file: `figures/superset/sk_tamil_toda_kurukh.svg`

Chapter job:

- First internal evidence figure.
- Show that Tamil + Toda + Kurukh cover nearly the whole Sanskrit base without using the north-Indian languages the orthodoxy would call "Indo-Aryan."

What it should contain:

- Sanskrit 23-cell base as shell.
- Three comparison languages marked distinctly but quietly.
- Union count: **20 / 23**.
- Missing cells called out: ल, स, श.
- A small note: "missing cells are neighbors / regularization zones."

What it should avoid:

- Do not claim these languages "are Sanskrit."
- Do not imply modern Dravidian classification is accepted as a civilizational divide. The prose handles that caveat.

Reader takeaway:

> The southern field already supplies most of Sanskrit's base; the gaps are local refinements.

### Figure 8.3 — Forest-Belt Survey: 18 of 23

Current file: `figures/superset/sk_korku_mundari_ho.svg`

Chapter job:

- Second internal evidence figure.
- Show that the central forest belt also covers most of the same Sanskrit base without relying on Santali.

What it should contain:

- Same visual grammar as Figure 8.2.
- Languages: Korku, Mundari, Ho.
- Union count: **18 / 23**.
- Missing cells listed in a small callout. Current prose names: ण, स, ष, श, ल.
- Optional note: "forest-belt selection; not a single-language ancestry claim."

What it should avoid:

- Do not overload with Santali caveats; those belong in prose/endnotes or appendix.
- Do not change the visual grammar from Figure 8.2.

Reader takeaway:

> Another non-northern subcontinental set covers most of the same base. The field is distributed.

### Figure 8.4 — Western IE Survey: 14 of 23

Current file: `figures/superset/sk_english_french_greek.svg`

Chapter job:

- External control.
- Show that familiar Western Indo-European languages cover less of Sanskrit's base than the southern and forest-belt sets.

What it should contain:

- Same Sanskrit-shell survey grammar.
- Languages: English, French, Greek.
- Union count: **14 / 23**.
- Visual tone should be neutral. The point is contrast, not ridicule.

What it should avoid:

- No detailed PIE argument here. Ch18 carries that.
- No "Europe bad" framing in the figure itself.

Reader takeaway:

> Shared human anatomy gives overlap, but the density is weaker outside the subcontinental field.

### Figure 8.5 — Central Asian Survey: 12 of 23

Current file: `figures/superset/sk_tajik_kazakh_kyrgyz.svg`

Chapter job:

- Geographic control against the Central Asian source-field implied by the racial Arya thesis.

What it should contain:

- Same Sanskrit-shell survey grammar.
- Languages: Tajik, Kazakh, Kyrgyz.
- Union count: **12 / 23**.
- Small title/subtitle should make clear this is a "Central Asian Survey," not a family-tree comparison.

What it should avoid:

- Do not imply these languages are the exact claimed source of Sanskrit. They are a corridor / geography test.

Reader takeaway:

> The Central Asian corridor does not look like a strong source-field for Sanskrit's base sound architecture.

### Figure 8.6 — The Gaps Are Neighbors

Target file: `figures/superset/snap_to_grid_neighbor_cells.svg`

Chapter job:

- Make the snap-to-grid argument visual.
- Show that the important gaps are adjacent refinements, not remote absences.

Suggested layout:

1. Left: a soft coronal / sibilant-lateral sound-zone.
   - Show continuous neighboring region, possibly with a gray band.
2. Right: selected Sanskrit coordinates.
   - Highlight ल, स, श.
   - Show nearby field positions with faint dots or ghost labels.
3. Use a restrained "snap" arrow:
   - "zone" -> "coordinate"

Required conceptual distinctions:

- **ल**: lateral regularized into Sanskrit's dental/front-coronal coordinate.
- **स**: front-coronal fricative regularized into Sanskrit's dental sibilant coordinate.
- **श**: not a simple alveolar snap; it is the palatal member of Sanskrit's three-sibilant regularization with स and ष.

Optional engineering analogy:

- A tiny CAD / Illustrator grid symbol can sit in the corner with text: "snap to grid."
- Keep this small. The figure should stay about sound.

What it should avoid:

- Do not make the missing cells look like failures.
- Do not show too many languages. This is a conceptual figure, not another survey panel.

Reader takeaway:

> The gaps reveal the engineering move: the field gives zones; Sanskrit chooses coordinates.

### Figure 8.7 — *Mahaprana* as Vertical Expansion

Target file: `figures/superset/mahaprana_vertical_expansion.svg`

Chapter job:

- Show that *mahaprana* is the second engineering move after the base field survey.
- Make clear that Sanskrit multiplies distinction through breath without crowding the place-axis.

**Scope note:** The figure shows the **stop matrix only** (5 places × stop rows). The mahāprāṇa move affects exactly the stops — the 10 stop cells (5 voiceless + 5 voiced) become 20 stop cells with the two aspirated rows added. The other 13 base cells (nasals, *antaḥstha*, *ūṣman*) are unaffected and would dilute the expansion visual. Saving them for Ch 9's grid reveal.

Layout — **two side-by-side panels with a large vertical arrow between them:**

1. **Left panel — "Base · 10 stop cells"**
   - 5 columns: BIL · DEN · RET · PAL · VEL
   - 2 rows: voiceless / voiced
   - Cells: प त ट च क (voiceless) · ब द ड ज ग (voiced)
   - All cells in active book-tint (#e6e3db) with dark Devanāgarī (#2b2b2d)

2. **Middle — large vertical arrow** with the label "+ prāṇa" and a second-line italic "(breath pressure as a new axis)"

3. **Right panel — "After mahāprāṇa · 20 stop cells"**
   - Same 5 columns: BIL · DEN · RET · PAL · VEL
   - 4 rows: voiceless / voiceless aspirated / voiced / voiced aspirated
   - Cells: प त ट च क → फ थ ठ छ ख → ब द ड ज ग → भ ध ढ झ घ
   - The two new mahāprāṇa rows (voiceless aspirated + voiced aspirated) interleaved between voiceless and voiced — matches the *varṇamālā* row order
   - The two mahāprāṇa rows visually flagged as **added by the architecture** — thin accent ring on each cell, or a small marker on the row label, but **not** styled as held-aside (this figure is the *restoration* moment after Ch 8 held them aside in §§8.6–8.8)

Required visual moves:

- The column heads (BIL · DEN · RET · PAL · VEL) must look **identical** between the two panels — the "no new mouth places" point lands by visible identity.
- The mahāprāṇa rows must read as **inserted by Sanskrit's engineering**, not as foreign material grafted on. The accent should say *new architectural row*, not *outside source*.

What it should avoid:

- Do not show the nasal, *antaḥstha*, or *ūṣman* rows. They dilute the expansion focus.
- Do not include a *visarga* forward-pointer. Ch9 §9.6 handles boundary breath.
- Do not use color accents. Grayscale only.
- Do not make *mahaprana* look imported. The accent ring is "added by Sanskrit," not "added from outside."

Reader takeaway:

> Sanskrit keeps the mouth-place grid clean and lets breath do additional structural work — same five mouth-stations, twice as many stop sonomers, no horizontal crowding.

### Figure 9.1 — *Varnamala* as Sonomer Garland

Current file: `figures/mapping_mouth/varnamala_sonomer_garland.svg`

Chapter job:

- Preserve Sanskrit's own poetic and accurate term before translating it into grids.
- Show that *varnamala* is a selected, ordered inventory, not an alphabetic heap.

What it should contain:

- Title should keep both: **वर्णमाला — The Sonomer Garland**.
- Beads or garland-like structure for sonomers.
- Legend explaining class shading and how to read the beads.
- The Oṃ / *pranava* element if retained should read as "the whole instrument in one syllable" or equivalent.

What it should avoid:

- Do not make this only a decorative necklace. It must still teach class and order.
- Do not over-explain inside the figure; Ch9 §9.1 carries the prose.

Reader takeaway:

> Sanskrit's own metaphor already says the inventory is selected, ordered, and carried.

### Figure 9.2 — Sanskrit Extracted: The Sonomer Grid

Current file: `figures/audiography/sanskrit_extracted_sonomer_grid.svg`

Chapter job:

- Show the same inventory after extraction into engineering language.
- Connect Ch9 to Appendix Part 3, where the full Sanskrit / Korean / Arabic comparison appears.

What it should contain:

- Sanskrit-only grid from the comparative matrix.
- Clean class distinctions.
- Figure title or caption should say "extracted" because the fuller comparison is in Appendix Part 3.

What it should avoid:

- No Korean / Arabic detail in the body figure.
- Do not make it look like the source of the *varnamala*. It is a modern extraction of Sanskrit's already existing sonomeric order.

Reader takeaway:

> Once isolated from the comparative chart, Sanskrit's selected inventory reveals a disciplined grid.

### Figure 9.3 — Control-Panel View of the *Sparsha* Matrix

Current file: `figures/mapping_mouth/control_panel.svg`

Chapter job:

- Make the 5x5 *sparsha* matrix feel like engineering rather than a school table.
- Show the four controls: place, voicing, breath, nasal coupling.

What it should contain:

- Five columns: velar, palatal, retroflex, dental, labial.
- Five rows:
  - voiceless light breath
  - voiceless heavy breath
  - voiced light breath
  - voiced heavy breath
  - nasal
- Visual controls for:
  - mouth-place
  - vocal-cord vibration
  - breath pressure
  - nasal opening
- Devanagari sonomers in the 25 cells.

What it should avoid:

- Do not reduce it to a table with labels only. The "control panel" metaphor needs visible controls.

Reader takeaway:

> Five mouth stations become twenty-five sonomers because Sanskrit crosses place with independent bodily controls.

### Figure 9.4 — Periodic-Table View of the *Sparsha* Matrix

Target file: `figures/mapping_mouth/sparsha_periodic_table.svg`

Status: optional.

Chapter job:

- Give a compact engineering-reference view of the same 25-cell matrix.
- Useful if the PDF needs a crisp table-like visual after the control-panel figure.

What it should contain:

- A clean 5x5 table with Sanskrit cells.
- Columns as *sthana*.
- Rows as operating modes.
- Heavy-breath and nasal rows visually distinguished.
- Possibly include both Sanskrit row names and modern equivalents.

What it should avoid:

- Do not duplicate Figure 9.3 unless the visual is clearly more compact and reference-like.

Reader takeaway:

> The matrix can be read as a periodic table of contact sonomers.

### Figure 9.5 — Matrix Table View of the *Varnamala*

Target file: `figures/mapping_mouth/varnamala_matrix_table.svg`

Status: optional reference figure.

Chapter job:

- Show the full selected inventory at one glance.
- Useful if the prose needs a reference object after the garland and extracted grid.

What it should contain:

- Four main divisions:
  - *svarah*
  - *sparshah*
  - *antasthah*
  - *ushmanah*
- Boundary category:
  - *ayogavaha* with *anusvara*, *visarga*, and related forms as appropriate.
- Optional timing note:
  - consonants = 1/2 *matra*
  - short / long / prolated vowels = 1 / 2 / 3 *matras*
  - include timing only if the figure still has room; otherwise leave timing to Ch9 §9.9.

What it should avoid:

- Do not become a dense textbook table.
- Do not conflict with the garland figure's order.

Reader takeaway:

> The whole selected inventory has class, order, and operational role.

### Figure 9.6 — *Mahaprana* as Vertical Expansion in the Finished Grid

Target file: `figures/mapping_mouth/mahaprana_vertical_expansion_grid.svg`

Status: optional; decide after Figure 8.7 exists.

Chapter job:

- Reprise the Ch8 breath expansion inside the completed *sparsha* matrix.
- Only needed if Figure 8.7 is too field-methodological and Ch9 needs a completed-grid version.

What it should contain:

- Same five place columns.
- Show light-breath and heavy-breath rows as paired layers.
- Label: "same place; added breath."

What it should avoid:

- Avoid visual duplication with Figure 8.7.
- Do not add a new conceptual claim.

Reader takeaway:

> In the finished grid, *mahaprana* is the vertical breath axis.

## Optional Heap-vs-Grid Figure

This was discussed as a possible Ch9 addition.

Suggested title: **From Sound-Field to Sonomeric Grid**

Suggested target file:

`figures/mapping_mouth/sound_field_to_sonomeric_grid.svg`

Possible layout:

1. Left panel: a natural sound-field or ordinary-language inventory as uneven dots / clusters / gaps on the same mouth-coordinate space.
2. Right panel: Sanskrit as aligned hexagons / cells in a disciplined grid.
3. Middle arrow: `selection -> regularization -> calibration`.

Placement:

- Best location: Ch9 §9.3, after the line "Chapter 8 named the move: Sanskrit snaps the field to a grid."
- Use only if the existing Figure 9.2 is not visually forceful enough by itself.

Risk:

- If the left panel uses English or Arabic, the figure can distract from the Ch8 subcontinental sound-field argument. A generic "ordinary inventory" may work better than naming a specific language in the body.

## Immediate Production Priorities

1. ~~Build Figure 8.1 — `sound_field_sound_slot.svg`.~~ Retired during the §8.2 rewrite; prose carries the field-vs-slot distinction.
2. ~~Build Figure 8.1 (new) — `sanskrit_base_before_mahaprana.svg`.~~ **Done 2026-06-08** — rendered, promoted, embedded.
3. ~~Build Figure 8.6 — `snap_to_grid_neighbor_cells.svg`.~~ **Done 2026-06-08** — rendered by Claude Design, promoted, embedded.
4. ~~Build Figure 8.7 — `mahaprana_vertical_expansion.svg`.~~ **Done 2026-06-08** — rendered by Claude Design, promoted, embedded.
5. Decide whether Ch9 needs Figure 9.4, 9.5, and 9.6 or whether the existing garland, extracted grid, and control panel are sufficient.
6. Decide whether to add optional heap-vs-grid figure after the current figures are placed and a PDF page-flow check is done.

## Notes For Claude Design

- Use grayscale only unless the existing figure family requires a specific accent.
- Keep figure titles short and aligned with chapter captions.
- Prefer the same typographic system already used in the Illustrator/Claude Design SVGs: large serif title, italic subtitle, restrained labels.
- Keep Sanskrit in Devanagari with IAST only where needed for clarity.
- Avoid crowding. Ch8 figures should teach one concept each.
- Ch8 is "field"; Ch9 is "grid." Do not reveal the complete finished grid too early in Ch8 except as the reference shell in survey figures.
