# Atomic Sanskrit — Master Figure Plan and Production Queue

**Status:** canonical figure index
**Last reconciled:** 2026-07-29
**Live numbering authority:** the current manuscript files

This document is the single index for figures that are deployed, specified,
planned, being revised, or still represented by placeholders. Detailed
research and design specifications remain in their subject plans; this file
links to them and records ownership, status, placement, reuse, and the next
production action.

The finishing plan points here as the canonical queue. Do not create another
book-wide figure plan.

## Status Key

| Status | Meaning |
|---|---|
| **Deployed** | Asset is called from the live manuscript. |
| **Revision** | Asset is deployed, but an identified change remains. |
| **Placeholder** | Plain figure placeholder remains in the live manuscript. |
| **Specified** | Detailed design specification exists; production has not begun. |
| **Source-ready** | Evidence and figure copy are ready for design. |
| **In design** | SVG, script, or design draft is being produced. |
| **Merge** | Proposed figure should be absorbed into another figure. |
| **Optional** | Produce only if layout or prose review shows a reader need. |
| **Wishlist** | Non-blocking concept retained for a later visual pass. |
| **Parked** | Valid concept without a current manuscript placement. |
| **Cut** | Removed from the live manuscript; source may remain for reference. |

## Production Rules

1. The live manuscript controls chapter and appendix numbering.
2. Use a working slug until placement is stable; assign the printed figure
   number only when the asset enters the body.
3. Keep detailed evidence in the source plan or ledger. This queue stores a
   link and a production decision rather than duplicating that material.
4. A manuscript file should contain either a deployed figure call or a
   placeholder indexed here. Detailed production notes do not belong in body
   prose.
5. Reuse an existing figure when it performs the same explanatory task.
   Create a related derivative only when another chapter needs a genuinely
   different reading.
6. Structural, tabular, and geometric figures should be reproducible SVGs,
   preferably generated from a script. Preserve the source script and source
   data beside the promoted SVG.
7. Every figure must remain legible at trade-page width and when printed in
   grayscale.
8. Before deployment, verify the title, caption, body introduction, endnote,
   asset path, grayscale derivative, and chapter cross-references.

## Current Snapshot

- **103 deployed figure references** occur in the live manuscript and reference
  files. Some intentionally reuse the same asset.
- Those references use **100 unique existing assets**; no deployed figure path
  is missing.
- **8 unresolved placeholders** remain in live manuscript prose.
- **6 svara figures** have specifications; Figures A, C, and F are deployed
  across Chapters 9 and 16.
- **6 PASS placeholders** have been reduced to two core figures plus merge,
  appendix, and optional decisions.
- Chapter 2's three language-category figures and Appendix Part 8's eight
  designed-variation figures are deployed; their older planning documents are
  source records rather than open production queues.

Validation commands:

```sh
# Deployed figure calls
rg -n '^!\[' as_*.md

# Unresolved live placeholders
rg -n '^\[FIGURE' as_*.md

# Figure specifications in active plans
find working/10_active -type f -name '*.md' -print0 |
  xargs -0 rg -n '^#{1,4} .*Figure|FIGURE PLACEHOLDER|Proposed file: figures/'
```

## P0 — Live Manuscript Placeholders

These eight entries currently print as planning text unless the build removes
them. They have first claim on figure-production time.

| Priority | Live ID | Working title | Placement | Status | Detailed source | Intended asset | Next action |
|---|---|---|---|---|---|---|---|
| P0 | **14.2** | Six-Layer Calibration Matrix | `as_1_14_calibration.md` §14.1 | Placeholder | Body placeholder and calibration discussion | `figures/calibration/six_layer_calibration_matrix.svg` | Convert the six layers and transversal Śikṣā role into a source-ready specification, then build. |
| P0 | **18.1** | The Architectural Test | `as_1_18_wrong_question.md` opening | **Deployed 2026-08-08** | Chapter 18 §§18.1–18.3 | `figures/wrong_question/architectural_test.svg` | Complete. Six-row comparison rendered and the body number corrected. |
| P1 | **19.7** | PIE Reconstructions and Vivimorphosis Chains | `as_1_19_pie_in_sky.md` §19.8 | Placeholder | Body placeholder; Sanskrit Radiance mapping work | `figures/pie_in_sky/pie_vivimorphosis_comparison.svg` | Reconcile with the yuj mapping method and avoid repeating Figures 19.2–19.6. |
| P1 | **20.1** | The Mitanni Sanskritic Layer | `as_1_20_life_after_pie.md` opening | Placeholder | Body placeholder | `figures/life_after_pie/mitanni_sanskritic_layer.svg` | Verify final table copy and render. |
| P2 | **20.2** | Wave 2 Catalog of Methodological Metatypy | `as_1_20_life_after_pie.md` §20.2 | Placeholder | Body placeholder | `figures/life_after_pie/wave_2_methodological_metatypy.svg` | Decide whether the evidence table needs a figure or should remain a typeset table. |
| P1 | **20.3** | Calibrant Waves and Diasporic Wave | `as_1_20_life_after_pie.md` §20.4 | Placeholder | Body placeholder and radiance plans | `figures/life_after_pie/calibrant_waves.svg` | Reframe all waves as carriers of Sanskrit's radiance, then build. |
| P2 | **A.4** | Photography and Audiography | `as_3_03_audiography.md` §3.6 | Placeholder | Body placeholder | `figures/audiography/photography_and_audiography.svg` | Produce a compact two-column engineering comparison. |
| P2 | **A.9** | Audiographic Family and Pyramid Classification | `as_3_03_audiography.md` §3.8 | Placeholder | Body table beneath placeholder | `figures/audiography/audiographic_family_classification.svg` | Decide whether a regional figure improves the existing table; otherwise remove the placeholder. |

## P1 — Architecture Figures Specified Outside the Body

### Svara Figure Family

Detailed specification:
[Svara Architecture Analysis Plan, §11](as_svara_architecture_analysis_plan_codex.md#11-proposed-figures)

| Working slug | Working title | Placement | Status | Reuse / ownership | Next action |
|---|---|---|---|---|---|
| `svara_form_matrix` | The Svara Form Matrix | Chapter 9 after the 132 calculation | **Deployed** | Chapter 9 owns the 162-position / 132-selected / 30-Excluded arithmetic. | Reproducible source and promoted SVG are in `figures/mapping_mouth/`. |
| `svara_two_domains` | One Svara Architecture, Two Domains | Chapter 16 | **Deployed** | Derivative of the Chapter 9 visual language, not a duplicate of its complete matrix. | Reproducible source and promoted SVG are in `figures/vaidika_laukika/`. |
| `svara_selected_excluded_forms` | Selected and Excluded Vowel Forms | Chapter 9 §9.10 | **Deployed** | Combines the **अ/आ** quality-duration selection with the one-*mātrā* **ए/ओ** exclusions. | Reproducible source and promoted SVG are in `figures/mapping_mouth/`. |

### PASS Figure Family

Detailed specification:
[PASS Deployment Plan, §8](as_pass_deployment_plan_codex.md#8-figure-options)

| Working slug | Working title | Placement | Status | Disposition | Next action |
|---|---|---|---|---|---|
| `pass_selection_and_scope` | The Principle of Architectural Selection and Scope | Chapter 9 §9.10 | **Deployed** | The only dedicated PASS figure in the body: Contribution → Load → Bounding Support → Scope, followed by the two paired sound cases. | Reproducible source and promoted SVG are in `figures/calibration/`. |
| `pass_scope_matrix` | Selection and Scope Matrix | Appendix Part 8 | **Optional** | Appendix evidence summary, not a second body figure. | Build only if it communicates the settled classifications more clearly than a table. |
| `pass_open_coordinates` | Two Excluded Coordinates | Chapter 9 | **Merge** | Existing Figure 9.6 and §9.10 already carry the argument. | Do not create separately unless Figure 9.6 is redesigned. |
| `pass_svara_scope` | PASS Across the Svara Architecture | Chapter 9 | **Merge** | Merge into `svara_form_matrix`. | Remove as an independent production item. |
| `pass_two_domains_profile` | PASS Across the Two Domains | Chapter 16 | **Merge** | Merge into `svara_two_domains` or the broader two-domain figure. | Decide during Chapter 16 layout. |
| `pass_let_profile` | Why Leṭ Remains Vaidika | Appendix Part 8 | **Optional** | Appendix-supporting. | Produce only if the collision table remains difficult to scan. |
| `pass_evidence_matrix` | PASS Evidence Matrix | Source and Reference Companion | **Optional** | Technical evidence figure. | Hold until evidence states are locked. |

### Other Active Figure Families

| Working slug / family | Working title | Placement | Status | Detailed source | Next action |
|---|---|---|---|---|---|
| `figure_0_2_revision` | Sanātana Time | Chapter 0 | **Revision** | [Author tasks](as_author_tasks.md) and asura synthesis plan | Add the structural meaning of *Vedānta* without implying a chronological period; preserve the unknown beginning of the Veda. |
| `one_veda_four_functions` | The One Veda and Its Four Functions | Chapter 0 or sequel | **Needs reconciliation** | [Asura synthesis plan](as_asura_synthesis_and_plan.md#51-illustration-1--the-one-veda-and-its-four-the-establishing-image) | Reconcile the old *anādi* claim with the manuscript's current statement that the Veda has an unknown beginning. Decide whether revised Figure 0.2 already performs this work. |
| `vyasa_vibhaga` | The Vyāsa-vibhāga | Chapter 0 or sequel | **Needs reconciliation** | [Asura synthesis plan](as_asura_synthesis_and_plan.md#52-illustration-2--the-vyāsa-vibhāga-the-one-divides-into-four-a-fifth-crosses-into-the-laukika) | Reconcile with deployed Figure 0.2 and current chronology language before production. |
| `language_categories` | Four Language Categories | Chapter 2 | **Deployed** | [Language Categories and Processes Plan](language_categories_and_processes_figure_plan.md) | Source plan is complete; no open production action. |
| `language_movements` | Languages and Movements | Chapter 2 | **Deployed** | Same plan | Source plan is complete; no open production action. |
| `language_misclassification` | The Misclassification of Sanskrit | Chapter 2 | **Deployed** | Same plan | Source plan is complete; no open production action. |
| `language_layers_over_time` | Language Categories Across Time | Chapter 2, 6, or 12 | **Specified** | [Four Language Behaviors plan](four_language_behaviors_codex_plan.md#figure-possibility) and `as_todo.md` | Reconcile the older layers-vs-time proposal with the three deployed Chapter 2 figures; merge if the existing process figure already carries the movement. |
| `language_behavior_icons` | Four Language-Behavior Icons | Shared visual vocabulary | **Optional** | `as_todo.md` figure task | Choose or generate only if later figures need a stable icon family. |
| `calibrant_envelope` | Orbit and Calibrant Envelope | Chapter 6 | **Parked** | Existing queue history; Orbit and Radiance plan | Re-specify before returning to the body. |
| `upasarga_radiance` | Upasarga Architecture and Receiving Fields | Chapter 12, 19, or appendix | **Specified** | [Upasarga Mapping Plan, §9](as_sanskrit_radiance_upasarga_mapping_plan.md#9-figure-concept) | Finish the Sanskrit/Greek/Latin evidence record before assigning placement. |
| `upasarga_architecture_fragment` | Complete Architecture and Receiving Fragments | Appendix or project proposal | **Specified** | Same plan | Hold until the primary upasarga figure is resolved. |
| `designed_variations` | Eight Designed-Variation Figures | Appendix Part 8 | **Deployed** | [Figure source data](as_vaidika_laukika_declensional_figure_source_data.md) | Preserve source data and regenerate after evidence corrections. |
| `two_domain_four_function_overview` | Four Functions of Designed Vedic Variation | Chapter 16 | **Optional** | [Chapter 16 ownership ledger](as_ch16_appendix_split_ownership_codex.md#figures) | Add only if the chapter's prose hierarchy does not make the four functions clear. |
| `ganah_reactivity_matrix` | Matrix of Elemental Reactivity | Chapter 11 or reference | **Needs reconciliation** | `as_todo.md` empirical figure tasks | Compare the requested tier × *gaṇa* grid with deployed `racana_gana_matrix.svg`, `reactivity_tiers.svg`, and `periodic_table.svg`; specify only the missing view. |
| `ganah_cross_corpus` | Comparative-Corpus View | Chapter 11 or reference | **Needs reconciliation** | `as_todo.md` empirical figure tasks | Decide whether deployed `canonical_rank_trajectory.svg` performs the requested comparison or whether a new overlap/bar figure remains necessary. |

## P2 — Existing Deployed Figure Register

This register is grouped by manuscript owner. It confirms coverage without
duplicating every caption. The live figure calls remain the detailed register.

| Owner | Deployed references | Figure family / asset location | Notes |
|---|---:|---|---|
| Preface, overture, Parts I–VII, epilogue, Ch0–1 | 12 eclipse-spine references | `figures/eclipse_spine/` | E.1–E.12; intentionally repeated narrative spine. |
| Chapter 0 | 2 chapter figures | `figures/seekers/` | Figures 0.1–0.2; Figure 0.2 has an author revision task. |
| Chapter 2 | 3 | `figures/botanical/` | Categories, movements, and misclassification. |
| Chapter 3 | 1 | `figures/strategic/` | Three Pillars and Containment. |
| Chapter 4 | 3 | `figures/fourth_abrahamic/` | Figures 4.1a, 4.1b, and 4.2. |
| Chapter 5 | 1 | `figures/siddha_grammar/` | Figure 5.1. |
| Chapter 6 | 1 | `figures/apabhramsa/` | Figure 6.1. |
| Chapter 7 | 3 | `figures/adivadya/` | Figures 7.1–7.3. |
| Chapter 8 | 7 | `figures/superset/` | Figures 8.1–8.7. |
| Chapter 9 | 8 | `figures/mapping_mouth/`, `figures/audiography/`, `figures/calibration/` | Figures 9.1–9.8; Figure 9.7 introduces PASS and Figure 9.8 presents the selected/excluded vowel forms. |
| Chapter 10 | 7 | `figures/building_dhatuh/` | Atom architecture and distributions. |
| Chapter 11 | 14 | `figures/building_kriya/`, `figures/ganah/` | Vedic/Pāṇinian assemblies plus statistical architecture. |
| Chapter 12 | 9 | `figures/building_vakya/` | Complete sonomer-to-sentence visual sequence. |
| Chapter 13 | 1 | `figures/preservation/` | Asuric Custody Stack. |
| Chapter 14 | 2 | `figures/calibration/` | Figures 14.1 and 14.3; Figure 14.2 remains a placeholder. |
| Chapter 16 | 1 | `figures/vaidika_laukika/` | Figure 16.1 shows the shared svara architecture under two domain permissions. |
| Chapter 17 | 1 | `figures/adivadya/` | Mūrdhanya flex. |
| Chapter 19 | 7 | `figures/pie_in_sky/` | Figures 19.1–19.7; Figure 19.8 remains a placeholder. Figure 19.6 presents the complete Radiance mechanism. |
| Chapter 20 | 2 | `figures/life_after_pie/` | Figures 20.2 and 20.3 summarize analytical routes and the four transmission waves; Figure 20.1 remains a placeholder. |
| Appendix Part 3 | 4 | `figures/audiography/` | Figures A.5–A.8; A.4 and A.9 remain placeholders. |
| Appendix Part 4 | 7 | `figures/superset/` | Figures A.4.1–A.4.7. |
| Appendix Part 8 | 8 | `figures/vaidika_laukika/` | Designed-variation figure series. |
| Reference Part 6 | 3 | `figures/building_dhatuh/`, `figures/ganah/` | Intentional reuse of statistical figures. |

Total deployed references in this reconciliation: **106**.

## P3 — Parked or Cut Historical Concepts

| Concept | Status | Reason / return condition |
|---|---|---|
| Former Figure 6.2 — Drift, Codification, Calibration | **Cut** | Chapter 2's four-category sequence supersedes it. |
| Botanical Root vs Architectural Dhātuḥ | **Parked** | Return only if it adds more than Chapters 2, 10, and 12 already show. |
| Dhātuḥ Across Indic Sciences | **Parked** | The standalone dhātuḥ chapter was dissolved. |
| Saptadhātu Cascade | **Parked** | No current body owner. |

## Figure Wishlist — Non-Blocking

These concepts do not block the manuscript or the current figure-production
sequence. They remain available if a later reader or layout review identifies
a clear visual need.

| Working slug | Working title | Possible placement | Status | Return condition |
|---|---|---|---|---|
| `svara_four_dimensions` | Four Dimensions of a Vowel | Chapter 9 or endnote | **Wishlist** | Return only if Figure 9.5 does not make quality, duration, pitch, and nasality clear enough. |
| `svara_shortening` | Shortening Without New Coordinates | Chapter 9 or endnote | **Wishlist** | Return only if the **ए/ऐ → इ** and **ओ/औ → उ** prose needs a visual aid. |
| `svara_operations` | One Source, Different Operations | Chapter 9 or endnote | **Wishlist** | Return only if the paired equations remain difficult to follow. |

## Numbering and Ownership Corrections

1. **Resolved 2026-08-08:** the placeholder inside
   `as_1_18_wrong_question.md` incorrectly said **Figure 17.1**. The deployed
   asset is **Figure 18.1**, `figures/wrong_question/architectural_test.svg`.
2. The former queue's proposed Figures 19.2 and 19.3 are obsolete. Those
   numbers now belong to deployed PIE-tree and orbit/radiance figures. The
   remaining comparison placeholder is **Figure 19.8**.
3. Appendix figure labels must preserve the appendix-part hierarchy. Do not
   collapse Figure A.4 in Appendix Part 3 into the A.4.1–A.4.7 family owned by
   Appendix Part 4.
4. Chapter 9 owns the complete 132-form matrix. Chapter 16 owns the
   two-domain derivative. Neither should reuse the other figure unchanged.

## Production Sequence

1. **Complete:** build `svara_form_matrix` and deploy it in Chapter 9.
2. **Complete:** build the related `svara_two_domains` figure and deploy it in Chapter 16.
3. Produce the PASS Decision Path or merge its explanation into one of those
   two figures if the final layouts already make PASS visible.
4. Resolve live placeholder Figure 14.2.
5. Resolve the Chapter 18 numbering error and build the Architectural Test.
6. Produce or deliberately replace Figures 19.7 and 20.1–20.3.
7. Decide whether Appendix Figures A.4 and A.9 add more than their current
   prose and tables.
8. Reconcile the two older Veda/Vyāsa figure proposals with deployed Figure
   0.2 before commissioning either.

## Completion Checklist

- [ ] Every live `[FIGURE ...]` placeholder is replaced by a deployed asset or
      deliberately removed after its content is preserved.
- [ ] Every active topic-plan figure appears in this index.
- [ ] Every deployed figure has an existing asset.
- [ ] Every generated figure records its script and source data.
- [ ] Every caption agrees with the current chapter argument and terminology.
- [ ] Every reused asset has one clear primary owner.
- [ ] All figures render legibly at trade width.
- [ ] All figures remain intelligible in grayscale.
- [ ] Final figure numbers and cross-references survive a clean book build.
