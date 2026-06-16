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
| `[ ]` | Figure 4.1a/b — Structural Template of the Four Abrahamic Religions | `as_1_03_fourth_abrahamic.md` | Show progressivism as structurally homologous to the three Abrahamic religions. | Active chapter now uses paired SVGs for named religions and progressivism. |
| `[ ]` | Figure 4.2 — Pyramid and Swastika | `as_1_03_fourth_abrahamic.md` | Show pyramidal authorization vs rotational-distributed transmission. | Can reuse visual language from `figures/about_series/` swastika/pyramid experiments. |
| `[x]` | Figure 8.1 — Sanskrit's 23-cell Base before *mahāprāṇa* | `as_1_08_superset.md` | Show the Sanskrit comparison target after the ten heavy-breath cells are temporarily held aside. | Rendered as `figures/superset/sanskrit_base_before_mahaprana.svg`. |
| `[x]` | Figure 8.2 — Southern Survey | `as_1_08_superset.md` | Show Tamil, Toda, and Kurukh covering 20 of 23 Sanskrit base coordinates. | Rendered as `figures/superset/sk_tamil_toda_kurukh.svg`. |
| `[x]` | Figure 8.3 — Forest-Belt Survey | `as_1_08_superset.md` | Show Korku, Mundari, and Ho covering 18 of 23 Sanskrit base coordinates without relying on Santali. | Rendered as `figures/superset/sk_korku_mundari_ho.svg`. |
| `[x]` | Figure 8.4 — Western IE Survey | `as_1_08_superset.md` | Use English, French, and Greek as an external control. | Rendered as `figures/superset/sk_english_french_greek.svg`. |
| `[x]` | Figure 8.5 — Central Asian Survey | `as_1_08_superset.md` | Use Tajik, Kazakh, and Kyrgyz as a geographic control against the Central Asian source-field claim. | Rendered as `figures/superset/sk_tajik_kazakh_kyrgyz.svg`. |
| `[x]` | Figure 8.6 — The Gaps Are Neighbors | `as_1_08_superset.md` | Show ल, स, and श as near-neighbor snap-to-grid choices rather than field absences. | Rendered as `figures/superset/snap_to_grid_neighbor_cells.svg`. |
| `[x]` | Figure 8.7 — *Mahāprāṇa* as Vertical Expansion | `as_1_08_superset.md` | Show breath pressure as a vertical expansion of the stop grid rather than a new horizontal mouth-place. | Rendered as `figures/superset/mahaprana_vertical_expansion.svg`. |

## P2 — Supporting Architecture Figures

These figures are valuable, but the prose can survive longer without them.

| Status | Figure | Source | Purpose | Production Note |
|---|---|---|---|---|
| `[x]` | Figure 5.1 — Long Memory of Sanskrit Grammar | `as_1_04_siddha.md` | Make pre-Pāṇinian decoding lineage and Trimuni stack visible. | Rendered as `figures/siddha_grammar/lineage_stack.svg`. |
| `[x]` | Figure 6.1 — *Gauḥ* and Four *Apabhraṃśas* | `as_1_05_apabhramsa.md` | Show one calibrated form with many fallings-away. | Rendered as `figures/apabhramsa/gauh_four_apabhramsas.svg`. |
| `[x]` | Figure 6.2 — Drift, Codification, Calibration | `as_1_05_apabhramsa.md` | Visualize the three-category standardization model. | Rendered as `figures/apabhramsa/drift_codification_calibration.svg`. |
| `[ ]` | Figure 6.3 — Calibrant Envelope | `as_1_05_apabhramsa.md` | Show Sanskrit as calibrant, calibrant-anchored regional languages, and uncalibrated drift. | Three-tier horizontal axis. |
| `[ ]` | PARKED — *Dhātuḥ* Across Indic Sciences | `as_1_06_dhatuh.md` | Show one technical term carrying one architectural function across domains. | Standalone *dhātuḥ* chapter is dissolved; renumber or relocate during the Ch 10 fold. |
| `[ ]` | PARKED — Saptadhātu Cascade | `as_1_06_dhatuh.md` | Show constitutive body-layer cascade. | Standalone *dhātuḥ* chapter is dissolved; renumber or relocate during the Ch 10 fold. |
| `[x]` | Figure 7.1 — Vocal Apparatus | `as_1_07_adivadya.md` | Ground the mouth as instrument and show the articulating regions. | Rendered as `figures/adivadya/vocal_tract_anatomy.svg`; replaces the separate modern speech-science mouth map. |
| `[x]` | Figure 7.2 — Language Hotzones Along Vocal Tract | `as_1_07_adivadya.md` | Contrast language inventories along the vocal tract before Sanskrit selection. | Rendered as `figures/adivadya/hotzones_panels.svg`; generated by `figures/adivadya/hotzones_panels.py`. |
| `[x]` | Figure 7.3 — Vocal Apparatus in Sanskrit | `as_1_07_adivadya.md` | Show Sanskrit labels on the instrument. | Rendered as `figures/adivadya/vocal_apparatus_sanskrit.svg`. |
| `[x]` | Figure 9.1 — Vedic Sieve | `as_1_09_mapping_mouth.md` | Show sound-grains being sifted into selected sonomers before the garland is woven. | Rendered as `figures/mapping_mouth/vedic_sieve_sonomer_garland.svg`. |
| `[x]` | Figure 9.2 — Sonomer Garland | `as_1_09_mapping_mouth.md` | Show the *varṇamālā* as a literal ordered *mālā* of selected sonomers. | Rendered as `figures/mapping_mouth/varnamala_sonomer_garland.svg`. |
| `[x]` | Figure 9.3 — Sanskrit Extracted: The Sonomer Grid | `as_1_09_mapping_mouth.md` | Isolate Sanskrit hexagons from the comparative articulatory matrix so the sonomer-grid selection is visible in the main body. | Rendered as `figures/audiography/sanskrit_extracted_sonomer_grid.svg`; reused as Figure A.6. |
| `[x]` | Figure 9.4 — Control Panel | `as_1_09_mapping_mouth.md` | Re-read the 5×5 *sparśa* table as a mouth-control panel. | Rendered as `figures/mapping_mouth/control_panel.svg`. |
| `[x]` | Figure 9.5 — The Sound Volume | `as_1_09_mapping_mouth.md` | Show the 5×7 consonant plane extended through the 14-vowel axis, with two empty consonant cells passing through the full vowel dimension and one lit क fiber. | Rendered as `figures/mapping_mouth/sound_volume.svg`. |

## P3 — Prosecution / Remedy Exhibits

These can be produced after the core architecture visuals are stable.

| Status | Figure | Source | Purpose | Production Note |
|---|---|---|---|---|
| `[ ]` | Figure 17.1 — The Architectural Test | `as_1_17_wrong_question.md` | Summarize what a valid model must explain. | Six-row table figure. |
| `[x]` | Figure 18.1 — PIE Keeps Returning to Sanskrit | `as_1_18_pie_in_sky.md` | Show the reconstructed ancestor moving away from Sanskrit and then reloading Sanskrit-like material. | Rendered as `figures/pie_in_sky/sanskrit_containment_trajectory.svg`. |
| `[ ]` | Figure 18.2 — PIE vs Vivimorphosis Chains | `as_1_18_pie_in_sky.md` | Contrast standard PIE reconstructions with book's vivimorphosis chains. | Side-by-side chain diagram. |
| `[ ]` | Figure 18.3 — One Sanskrit *Dhātuḥ*, Multiple PIE Roots | `as_1_18_pie_in_sky.md` | Show *dṛś* unity vs PIE splitting. | Split-table or branching diagram. |
| `[ ]` | Figure 19.1 — Mitanni Sanskritic Layer | `as_1_19_life_after_pie.md` | Make treaty / horse-training / throne-name evidence scannable. | Evidence table figure. |
| `[ ]` | Figure 19.2 — Wave 2 Methodological Metatypy | `as_1_19_life_after_pie.md` | Summarize transmission cases. | Table figure. |
| `[ ]` | Figure 19.3 — Calibrant Waves and Diasporic Wave | `as_1_19_life_after_pie.md` | Show Wave 1 / Wave 2 / Wave 3 / Diasporic Wave. | Timeline/layer diagram. |
| `[ ]` | Figure A.4 — Photography and Audiography | `as_3_03_audiography.md` | Parallel engineered capture of light and sound. | Two-column analogy diagram. |
| `[x]` | Figure A.5 — Sound, Script, Standard | `as_3_03_audiography.md` | Place Sanskrit, Arabic, and Korean on one place-and-manner matrix. | Rendered as `figures/audiography/sound_script_standard_matrix.svg`; Sanskrit hexagons, Arabic circles, Korean squares. |
| `[x]` | Figure A.6 — Sanskrit Extracted: The Sonomer Grid | `as_3_03_audiography.md` | Show Sanskrit as engineered sound-grid. | Rendered as `figures/audiography/sanskrit_extracted_sonomer_grid.svg`; reused from Figure 9.3. |
| `[x]` | Figure A.7 — Arabic Extracted: Codified Sound Tradition | `as_3_03_audiography.md` | Show Arabic as inherited phonology stabilized by codified tradition. | Rendered as `figures/audiography/arabic_extracted_codified_sound_tradition.svg`. |
| `[x]` | Figure A.8 — Korean Extracted: Engineered Script, Existing Sound | `as_3_03_audiography.md` | Show Korean as existing phonology served by engineered Hangul script. | Rendered as `figures/audiography/korean_extracted_engineered_script.svg`. |
| `[ ]` | Figure A.9 — Audiographic Family and Orthodox Classification | `as_3_03_audiography.md` | Show Indic scripts and orthodox labels. | Regional table or map-table hybrid. |

## Optional / Cut Candidates

| Status | Figure | Source | Decision Needed |
|---|---|---|---|
| `[ ]` | PARKED — Botanical Root vs Architectural *Dhātuḥ* | `as_1_06_dhatuh.md` | Candidate for Ch10 only if it adds more than the Ch2 tree metaphor and Ch10 atom diagrams already add. |

## Validation Notes

- Ch10-Ch12 already use rendered SVGs and do not appear in this queue.
- Production output should contain 29 reader-facing figure placeholders after the next assemble run.
- Draft-note figure mentions in source files are ignored because the build strips draft-note blocks.
