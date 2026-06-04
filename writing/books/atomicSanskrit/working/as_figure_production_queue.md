# Atomic Sanskrit — Figure Production Queue

Created 2026-05-31 during the Draft 2 structural-read cleanup. This file tracks reader-facing figure placeholders that still appear in the assembled manuscript.

Validation command:

```sh
rg -n "\[FIGURE|FIGURE [0-9A-Z.]" atomicSanskrit/build/atomic_sanskrit.md
```

Status key: `[ ]` open · `[~]` in progress · `[x]` rendered and inserted · `[-]` cut / replaced by prose or table

## Production Principles

- Prioritize figures that carry the architecture spine before conceptual illustrations.
- Prefer repo-native SVGs generated from scripts when the figure is structural, tabular, or geometric.
- Use the existing Ch10-Ch12 visual language where applicable: hexagonal sonomer/atom/molecule vocabulary, restrained grayscale, Devanagari + IAST where the reader needs both.
- If a placeholder is really a table, either render it as a clean table in markdown or generate a simple SVG table; do not over-illustrate.
- Optional placeholders should either become real figures or be cut before reader builds.

## P0 — Architecture Spine Blockers

These figures support the book's central calibration argument and should be produced first.

| Status | Figure | Source | Purpose | Production Note |
|---|---|---|---|---|
| `[ ]` | Figure 14.1 — The Four Preservation Modes | `as_1_14_calibration.md` | Make Scripture / Mnemoniture / Flexture / Auditure visible as distinct preservation technologies. | Likely a clean matrix/table figure: medium, human capacity, content category, Indic counterpart. |
| `[ ]` | Figure 14.2 — The Six-Layer Calibration Matrix | `as_1_14_calibration.md` | Make the Vedas / Prātiśākhya / Vyākaraṇam / Dhātupāṭha / Varṇamālā / Chandas calibration stack visible, with Śikṣā as transversal pedagogy. | Highest-priority figure. Could be nested layers with Śikṣā as an overlay band or vertical brace. |

## P1 — Polemic Frame And Sound-Field

These figures make the antagonist frame and the subcontinental sound-field legible.

| Status | Figure | Source | Purpose | Production Note |
|---|---|---|---|---|
| `[ ]` | Figure 2.1 — Linear Progress vs. Kālacakra | `as_1_02_strategic.md` | Show the incompatibility between linear-progress teleology and cyclic time. | Two-panel conceptual SVG: upward arrow vs wave/wheel. |
| `[ ]` | Figure 2.2 — Three Pillars and Containment | `as_1_02_strategic.md` | Compress AIT / Noachian chronology / linear-progress teleology into one containment architecture. | Structural diagram with two cracked pillars and one intact pillar supporting botanical metaphor. |
| `[ ]` | Figure 3.1 — Structural Template of the Four Abrahamic Religions | `as_1_03_fourth_abrahamic.md` | Show progressivism as structurally homologous to the three Abrahamic religions. | Table figure may be enough. Keep direct, not ornamental. |
| `[ ]` | Figure 3.2 — Pyramid and Swastika | `as_1_03_fourth_abrahamic.md` | Show pyramidal authorization vs rotational-distributed transmission. | Can reuse visual language from `figures/build/about_series/` swastika/pyramid experiments. |
| `[ ]` | Figure 9.1 — Subcontinental Sound-Field | `as_1_09_superset.md` | Show the regional sound-field, retroflex distribution, aspirated series, and eastern boundary. | Map-like schematic; if a real map is too time-consuming, use a stylized subcontinent field diagram. |
| `[ ]` | Figure 9.2 — Selection From the Superset | `as_1_09_superset.md` | Show outer subcontinental sound possibilities and inner selected varṇamālā grid. | Two-layer field/grid visualization. |

## P2 — Supporting Architecture Figures

These figures are valuable, but the prose can survive longer without them.

| Status | Figure | Source | Purpose | Production Note |
|---|---|---|---|---|
| `[x]` | Figure 4.1 — Long Memory of Sanskrit Grammar | `as_1_04_siddha.md` | Make pre-Pāṇinian decoding lineage and Trimuni stack visible. | Rendered as `figures/build/siddha_grammar_lineage_stack.svg`. |
| `[ ]` | Figure 5.1 — *Gauḥ* and Four *Apabhraṃśas* | `as_1_05_apabhramsa.md` | Show one engineered form with many fallings-away. | Radial node diagram. |
| `[ ]` | Figure 5.2 — Drift, Codification, Calibration | `as_1_05_apabhramsa.md` | Visualize the three-frame standardization model. | Table figure; may become markdown table instead. |
| `[ ]` | Figure 5.3 — Calibrant Envelope | `as_1_05_apabhramsa.md` | Show Sanskrit as calibrant, calibrant-anchored regional languages, and uncalibrated drift. | Three-tier horizontal axis. |
| `[ ]` | Figure 6.1 — *Dhātuḥ* Across Indic Sciences | `as_1_06_dhatuh.md` | Show one technical term carrying one architectural function across domains. | Table figure. |
| `[ ]` | Figure 6.2 — Saptadhātu Cascade | `as_1_06_dhatuh.md` | Show constitutive body-layer cascade. | Simple vertical cascade. |
| `[ ]` | Figure 7.1 — Vocal Apparatus | `as_1_07_adivadya.md` | Ground the mouth as instrument. | Cross-section schematic; likely needs a clean custom SVG or licensed/public-domain base redrawn. |
| `[x]` | Figure 7.2 — Modern Speech-Science Mouth Map | `as_1_07_adivadya.md` | Show the English speech-science articulation regions along a reusable vocal-tract arc. | Rendered as `figures/build/mapping_mouth_modern_speech_map.svg`; source script at `figures/mapping_mouth/fig_modern_mouth_map.py`. |
| `[ ]` | Figure 7.3 — Vocal Apparatus in Sanskrit | `as_1_07_adivadya.md` | Show Sanskrit labels on the instrument. | Derivative of Figure 7.1 / 7.2. |
| `[ ]` | Figure 7.4 — Language Hotzones Along Vocal Tract | `as_1_07_adivadya.md` | Contrast language inventories along the vocal tract before Sanskrit selection. | Horizontal vocal-tract axis. |
| `[x]` | Figure 8.1 — Sonomeric Garland | `as_1_08_mapping_mouth.md` | Show the *varṇamālā* as a literal ordered *mālā* of selected sonomers. | Illustrator SVG at `figures/mapping_mouth/sonomericGarlandB106.svg`. |
| `[x]` | Figure 8.2 — Sanskrit Extracted: The Sonomer Grid | `as_1_08_mapping_mouth.md` | Isolate Sanskrit hexagons from the comparative articulatory matrix so the sonomer-grid selection is visible in the main body. | Rendered as `figures/build/audiography_sanskrit_extracted_sonomer_grid.svg`; reused as Figure A.6. |
| `[x]` | Figure 8.3 — Control Panel | `as_1_08_mapping_mouth.md` | Show the 5x5 varṇamālā as instrument board. | Rendered as `figures/build/mapping_mouth_control_panel.svg`; source script at `figures/mapping_mouth/fig_control_panel.py`. |
| `[ ]` | Figure 8.4 — Periodic-Table Style | `as_1_08_mapping_mouth.md` | Make Staal's structural comparison visible without importing his inference. | 25-cell periodic-style grid. |
| `[ ]` | Figure 8.5 — Matrix Table | `as_1_08_mapping_mouth.md` | Plain reference view of the 5x5 grid. | Could be markdown table if SVG adds no value. |

## P3 — Prosecution / Remedy Exhibits

These can be produced after the core architecture visuals are stable.

| Status | Figure | Source | Purpose | Production Note |
|---|---|---|---|---|
| `[ ]` | Figure 17.1 — The Architectural Test | `as_1_17_wrong_question.md` | Summarize what a valid model must explain. | Six-row table figure. |
| `[ ]` | Figure 18.1 — PIE vs Vivimorphosis Chains | `as_1_18_pie_in_sky.md` | Contrast standard PIE reconstructions with book's vivimorphosis chains. | Side-by-side chain diagram. |
| `[ ]` | Figure 18.2 — One Sanskrit *Dhātuḥ*, Multiple PIE Roots | `as_1_18_pie_in_sky.md` | Show *dṛś* unity vs PIE splitting. | Split-table or branching diagram. |
| `[ ]` | Figure 19.1 — Mitanni Sanskritic Layer | `as_1_19_life_after_pie.md` | Make treaty / horse-training / throne-name evidence scannable. | Evidence table figure. |
| `[ ]` | Figure 19.2 — Wave 2 Methodological Metatypy | `as_1_19_life_after_pie.md` | Summarize transmission cases. | Table figure. |
| `[ ]` | Figure 19.3 — Calibrant Waves and Diasporic Wave | `as_1_19_life_after_pie.md` | Show Wave 1 / Wave 2 / Wave 3 / Diasporic Wave. | Timeline/layer diagram. |
| `[ ]` | Figure A.4 — Photography and Audiography | `as_3_03_audiography.md` | Parallel engineered capture of light and sound. | Two-column analogy diagram. |
| `[x]` | Figure A.5 — Sound, Script, Standard | `as_3_03_audiography.md` | Place Sanskrit, Arabic, and Korean on one place-and-manner matrix. | Rendered as `figures/build/audiography_sound_script_standard_matrix.svg`; Sanskrit hexagons, Arabic circles, Korean squares. |
| `[x]` | Figure A.6 — Sanskrit Extracted: The Sonomer Grid | `as_3_03_audiography.md` | Show Sanskrit as engineered sound-grid. | Rendered as `figures/build/audiography_sanskrit_extracted_sonomer_grid.svg`; reused from Figure 8.2. |
| `[x]` | Figure A.7 — Arabic Extracted: Codified Sound Tradition | `as_3_03_audiography.md` | Show Arabic as inherited phonology stabilized by codified tradition. | Rendered as `figures/build/audiography_arabic_extracted_codified_sound_tradition.svg`. |
| `[x]` | Figure A.8 — Korean Extracted: Engineered Script, Existing Sound | `as_3_03_audiography.md` | Show Korean as existing phonology served by engineered Hangul script. | Rendered as `figures/build/audiography_korean_extracted_engineered_script.svg`. |
| `[ ]` | Figure A.9 — Audiographic Family and Orthodox Classification | `as_3_03_audiography.md` | Show Indic scripts and orthodox labels. | Regional table or map-table hybrid. |

## Optional / Cut Candidates

| Status | Figure | Source | Decision Needed |
|---|---|---|---|
| `[ ]` | Figure 6.3 — Botanical Root vs Architectural *Dhātuḥ* | `as_1_06_dhatuh.md` | Placeholder itself says optional. Keep only if it adds more than the Ch1 tree metaphor and Ch10 atom diagrams already add. |

## Validation Notes

- Ch10-Ch12 already use rendered SVGs and do not appear in this queue.
- Production output should contain 29 reader-facing figure placeholders after the next assemble run.
- Draft-note figure mentions in source files are ignored because the build strips draft-note blocks.
