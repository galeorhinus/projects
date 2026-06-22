# De-AI Pass Tracker

Tracks the humanize / de-AI sweep across the manuscript. **The author sequences** (which file, when); **Claude tracks** status here and updates after every chunk.

The de-AI rules live in the user-memory note `feedback_deai_humanize_prose.md` and (for the tense rule + voice) in `CLAUDE.md`.

## Workflow

1. **Sweep in chunks** of ~100 physical lines, snapped to the nearest blank-line / section boundary (never split a paragraph across a chunk).
2. **Double, don't replace.** For every paragraph changed, the verbatim original is kept directly above the rewrite, wrapped in a strippable HTML comment:

   ```
   <!-- AISWEEP-OLD
   {verbatim original paragraph(s)}
   AISWEEP-END -->
   {new paragraph(s)}
   ```

   The wrapper renders nothing in a build and shows greyed in the editor — original above, rewrite below.
3. **Change report.** Each chunk ends with `file:line` links + a one-line rationale per change, plus which line-ranges were skipped as mechanical (figure-demos, data tables, captions).
4. **Review** in the editor (or via the checkpoint-commit git diff).
5. **Strip** approved blocks: `python3 working/deai_strip.py <file>` (or `--check` to count). Then commit the clean version.

## Status legend

- ⬜ not started
- 🟡 swept — doubled, awaiting review (chunk progress noted)
- 🟢 reviewed & stripped — final
- ➖ mechanical / minimal-prose — light or no sweep needed
- ✅ done (note method)

## Ledger

| # | File | Title / role | Lines | Status |
|---|---|---|--:|---|
| — | as_0_00_about_series | About the series | 17 | ⬜ |
| — | as_0_01_preface | Preface | 102 | ⬜ |
| — | as_0_02_acknowledgements | Acknowledgements | 14 | ➖ |
| — | as_0_04_note_on_notes | Note on the Notes | 9 | ➖ |
| — | as_part_00_overture_shankha | Overture — *The Śaṅkha* | 33 | ⬜ |
| **I** | as_part_01_wrong_metaphor | Part I opener | 59 | ⬜ |
| 0 | as_1_00_seekers | Seekers | 197 | ⬜ |
| 1 | as_1_01_one_oppressors_finite | One / Oppressors / Finite | 115 | ⬜ |
| 2 | as_1_02_botanical | The Botanical Metaphor | 159 | ⬜ |
| 3 | as_1_03_strategic | Strategic | 97 | ⬜ |
| **II** | as_part_02_sanskrit_self_conception | Part II opener | 15 | ➖ |
| 4 | as_1_04_fourth_abrahamic | Fourth Abrahamic | 180 | ⬜ |
| 5 | as_1_05_siddha | Siddha | 129 | ⬜ |
| 6a | as_1_06_apabhramsa | Apabhraṃśa | 139 | ⬜ |
| 6b | as_1_06_dhatuh | The *dhātuḥ* | 112 | ⬜ |
| **III** | as_part_03_sound_field | Part III opener | 15 | ➖ |
| 7 | as_1_07_adivadya | Ādivādya | 149 | ⬜ |
| 8 | as_1_08_superset | The Superset | 274 | ⬜ |
| 9 | as_1_09_mapping_mouth | Mapping the Mouth | 253 | ⬜ |
| **IV** | as_part_04_atomic_architecture | Part IV opener | 15 | ➖ |
| 10 | as_1_10_building_dhatuh | Building the *dhātuḥ* | 443 | ⬜ |
| 11 | as_1_11_building_kriya | Building the *kriyā* | 324 | ✅ done (replace-mode, committed ff89667) + breathing-pass review: no new changes needed — the replace-mode sweep already de-uniformized (fused staccato chains, killed stacked-negative cluster, broke anaphora); remaining signpost candidates borderline, left |
| 12 | as_1_12_building_vakya | Building the *vākya* | 278 | 🟢 STRIPPED — final. De-AI + chunk-1 rescan + breathing pass + RV 1.164.39 epigraph promotion & akṣara reading. 23 redlines stripped & committed |
| 13 | as_1_13_preservation | Preservation | 163 | 🟢 STRIPPED — final. 3 metadiscourse fixes + 4 signpost cuts (Gemini review); deliberate hammers/triads PROTECTED. 7 redlines stripped |
| **V** | as_part_05_anti_entropy_practice | Part V opener | 15 | ➖ |
| 14 | as_1_14_calibration | Calibration | 204 | 🟢 STRIPPED — final. 4 sweep fixes + 2 breathing; deliberate triads protected. 6 redlines stripped |
| 15 | as_1_15_aural | Aural | 101 | ⬜ |
| 16 | as_1_16_retroflex | Retroflex | 173 | ⬜ |
| **VI** | as_part_06_killing_pie | Part VI opener | 15 | ➖ |
| 17 | as_1_17_wrong_question | The Wrong Question | 209 | ⬜ |
| 18 | as_1_18_pie_in_sky | PIE in the Sky | 291 | ⬜ |
| **VII** | as_part_07_life_after_pie | Part VII opener | 15 | ➖ |
| 19 | as_1_19_life_after_pie | Life After PIE | 129 | ⬜ |
| E | as_2_01_epilogue | Epilogue | 200 | ⬜ |
| A1 | as_3_01_baking | App — Baking | 303 | ⬜ |
| A2 | as_3_02_encyclopaedic | App — Encyclopaedic | 317 | ⬜ |
| A3 | as_3_03_audiography | App — Audiography | 324 | ➖ data-heavy |
| A4 | as_3_04_inventory_atlas | App — Inventory Atlas | 183 | ➖ data-heavy |
| A5 | as_3_05_language_factory | App — Language Factory | 302 | ⬜ |
| A6 | as_3_06_by_the_numbers | App — By the Numbers | 724 | ➖ data-heavy |
| A7 | as_3_07_vedic_carrier | App — Vedic Carrier | 293 | ⬜ |
| A8 | as_3_08_codification_story | App — Codification Story | 530 | ⬜ |
| A9 | as_3_09_glossary | Glossary | 389 | ➖ reference |

_Last updated: 2026-06-22 (tracker created; Ch 11 complete in replace-mode)._
