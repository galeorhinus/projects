# Atomic Sanskrit — Endnote Verification Master

**Generated:** 2026-09-04
**Source of truth for audit results:** `working/10_active/endnote_verification_batches/`
**Generator and integrity check:** `working/tools/endnote_verification_ledger.py`

## Purpose

Track the source verification of every endnote without confusing factual verification with mechanical completeness. Batch reports preserve what was checked, which sources were used, what changed, and why. This ledger projects those results across the complete current inventory.

Do not record an endnote as **Pass** merely because it contains a plausible citation. A completed audit must compare the body claim, Short form, full note, source, locator, and every live deployment.

## Inventory

| Category | Count |
|---|---:|
| Endnote definitions | 371 |
| Unique definitions | 371 |
| Unique directly deployed notes | 341 |
| Live marker occurrences | 489 |
| Definitions without a direct manuscript marker | 30 |
| Live markers without a definition | 0 |
| Duplicate definitions | 0 |
| Entries with a structural problem | 0 |
| Missing `Deployments` field | 0 |
| Surviving verification marker | 0 |
| Unfinished Short form | 0 |

The directly deployed notes receive full source verification. Definitions without a direct manuscript marker receive a disposition review. Supporting entries should be audited with the deployed note that depends on them; parked entries need full source verification only before redeployment.

## Status Summary

| Status | Count |
|---|---:|
| Corrected | 90 |
| Corrected and applied | 3 |
| Corrected and promoted | 1 |
| Locator corrected | 1 |
| Narrowed | 24 |
| Parked | 15 |
| Partial | 1 |
| Pass | 2 |
| Qualified | 12 |
| Reconfirmed | 57 |
| Reconfirmed as continuum account | 1 |
| Reconfirmed as inference | 1 |
| Reconfirmed as synthesis | 2 |
| Reframed | 1 |
| Reproduced | 11 |
| Retired | 3 |
| Strengthened | 62 |
| Supporting | 9 |
| Verified | 65 |
| Verified and qualified | 1 |
| Verified and strengthened | 3 |
| Verified as synthesis | 5 |
| Verified; body retained | 1 |

## Status Rules

- **Pass:** the source, locator, note, and every body deployment agree.
- **Strengthened:** the claim held, but its source, locator, wording, or boundary was improved.
- **Corrected:** a factual, attribution, translation, locator, or claim-scope error was repaired.
- **Narrowed:** the available evidence required a smaller claim.
- **Blocked:** verification reached a source-access or evidence gap that remains unresolved.
- **Supporting:** no direct body marker; another deployed endnote depends on this entry.
- **Parked:** intentionally unused source material.
- **Retired:** removed from the active argument with its disposition recorded.
- **Disposition needed:** unused definition whose future status still needs a decision.
- **Queued:** assigned to the next factual audit batch but not yet verified.
- **Unreviewed:** mechanically present but not yet source-verified under this audit.

Risk is assigned during factual triage: **P0** for load-bearing or potentially damaging claims, **P1** for substantive supporting claims, and **P2** for illustrative or low-risk facts. **P?** means that triage has not yet occurred.

## Audit Protocol

Each factual batch checks:

1. source identity and bibliographic metadata;
2. an exact page, verse, rule, inscription, table, or stable section locator;
3. quotations, Sanskrit text, translations, names, dates, and numbers;
4. agreement among the manuscript claim, Short form, and full note;
5. the boundary between evidence and the book's inference;
6. every live deployment and every dependent endnote;
7. successful full and short manuscript assembly.

## Complete Ledger

| Endnote | Direct deployments | Uses | Risk | Status | Batch | Checked | Structure |
|---|---|---:|:---:|---|---|---|---|
| `rigveda-5-40-5-svarbhanu-eclipse` | Prologue — The Eclipse L19; Chapter 1 L129; Chapter 3 L185 | 3 | P1 | Strengthened | [B003](endnote_verification_batches/batch_003_explicit_verify_markers.md) | 2026-09-01 | OK |
| `svarbhanu-svar-etymology` | Part I L29 | 1 | P1 | Strengthened | [B005](endnote_verification_batches/batch_005_vak_svarbhanu_articulation.md) | 2026-09-02 | OK |
| `rigveda-5-40-atri-clearing` | Chapter 3 L215; Chapter 20 L185 | 2 | P1 | Reconfirmed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `rigveda-5-40-9-atris-find-sun` | Epilogue — The Atris Find the Sun L13 | 1 | P1 | Reconfirmed | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `rigveda-10-71-2-sieve-vak` | Chapter 9 L13; Chapter 18 L257 | 2 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `rigveda-10-71-3-path-vak` | Chapter 9 L477; Chapter 18 L267 | 2 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `rigveda-8-100-11-vak-blessing` | Epilogue — The Atris Find the Sun L257 | 1 | P1 | Reconfirmed | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `rigveda-10-71-4-vach` | Chapter 13 L11; Chapter 18 L277 | 2 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `rigveda-1-164-45-four-quarters-vak` | Chapter 8 L11 | 1 | P0 | Verified | [B017](endnote_verification_batches/batch_017_chapter8_sound_superset.md) | 2026-09-03 | OK |
| `rigveda-10-125-vak-ambhrini` | Chapter 0 L119; Chapter 18 L287 | 2 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `rturasanam-murdha-shiksha` | Chapter 17 L9 (2 uses) | 2 | P0 | Reconfirmed | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `samskrtam-morphology` | Prologue — The Eclipse L43; Chapter 2 L155 | 2 | P1 | Corrected | [B006](endnote_verification_batches/batch_006_high_risk_architecture.md) | 2026-09-02 | OK |
| `temples-two-enemies-ta-prohm` | Chapter 6 L28 | 1 | P1 | Strengthened | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `paspashahnika-brihaspati-indra-word-list` | Chapter 2 L97; Chapter 10 L258 | 2 | P0 | Reconfirmed | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `paspashahnika-apabhramsa-passage` | Chapter 6 L11 (3 uses) | 3 | P0 | Corrected | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `gavi-source-form-reversal` | Chapter 6 L82 | 1 | P1 | Reconfirmed | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `pre-pie-dictionary-shift` | Chapter 1 L109 (2 uses); Chapter 19 L8 (2 uses) | 4 | P1 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `schleicher-1868-fable` | Chapter 19 L30; Appendix Part 1 — Baking the Mother Tongue L87 (2 uses); Appendix Part 5 — The Language Factory L194 | 4 | P0 | Reconfirmed | [B036](endnote_verification_batches/batch_036_appendix_part5_language_factory.md) | 2026-09-03 | OK |
| `jakobson-1959-nursery-words` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `pie-cementing-recent-decades` | Chapter 1 L109 (2 uses); Chapter 4 L133; Chapter 19 L108 | 4 | P0 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `pie-indian-university-curricula` | Chapter 3 L39; Chapter 4 L137 (3 uses); Appendix Part 2 — The Encyclopaedic Confirmation L182 (2 uses) | 6 | P1 | Reconfirmed | [B033](endnote_verification_batches/batch_033_appendix_part2_encyclopaedic.md) | 2026-09-03 | OK |
| `missionaries-of-progress-precedent` | Chapter 4 L157 | 1 | P2 | Strengthened | [B013](endnote_verification_batches/batch_013_chapter4_completion.md) | 2026-09-02 | OK |
| `popular-pie-missionaries` | Chapter 4 L159 | 1 | P1 | Strengthened | [B013](endnote_verification_batches/batch_013_chapter4_completion.md) | 2026-09-02 | OK |
| `devi-mahatmya-goddess-undoes-male-apex` | Chapter 1 L25 | 1 | P0 | Narrowed | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `pollock-sanskrit-cosmopolis-position-3` | Chapter 1 L141; Chapter 4 L175 | 2 | P0 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `murty-library-gift-gate` | Chapter 4 L175 | 1 | P0 | Verified; body retained | [B013](endnote_verification_batches/batch_013_chapter4_completion.md) | 2026-09-02 | OK |
| `fourth-abrahamic-eschatology-precedent` | Chapter 4 L69 | 1 | P0 | Strengthened | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `brahmi-devanagari-structural-identity` | Chapter 13 L93; Appendix Part 3 — The Sonomer and the Audiograph: Sound Engineering, Pun Intended L83 (2 uses) | 3 | P1 | Pass | [B041](endnote_verification_batches/batch_041_audiography_script_entropy.md) | 2026-09-04 | OK |
| `durable-script-archive-selection` | Chapter 13 L111; Appendix Part 3 — The Sonomer and the Audiograph: Sound Engineering, Pun Intended L115 | 2 | P1 | Verified | [B034](endnote_verification_batches/batch_034_appendix_part3_audiography.md) | 2026-09-03 | OK |
| `writing-medium-fire-and-authority` | Chapter 13 L101 | 1 | P0 | Pass | [B040](endnote_verification_batches/batch_040_chapter13_writing_medium.md) | 2026-09-04 | OK |
| `daniels-abjad-abugida-typology` | Appendix Part 3 — The Sonomer and the Audiograph: Sound Engineering, Pun Intended L137 (2 uses) | 2 | P1 | Strengthened | [B034](endnote_verification_batches/batch_034_appendix_part3_audiography.md) | 2026-09-03 | OK |
| `aksara-imperishable-name` | Chapter 9 L164 | 1 | P1 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `chronology-asymmetry-rationale` | Prologue — The Eclipse L65 | 1 | P0 | Corrected | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `vedanta-anta-chronology-capture` | Chapter 0 L153 | 1 | P1 | Strengthened | [B000](endnote_verification_batches/batch_000_random_pilot.md) | 2026-09-01 | OK |
| `vedanta-textual-placement` | Chapter 0 L149 | 1 | P1 | Verified | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `ramayana-homer-chronology-capture` | Chapter 3 L95 | 1 | P0 | Strengthened | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `indo-european-narrative-inheritance` | Chapter 19 L68 | 1 | P1 | Verified | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `satyam-bhutahitam-mahabharata` | Chapter 0 L276; Epilogue — The Atris Find the Sun L123; Part I L31 | 3 | P1 | Reconfirmed | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `nanartha-homonymy` | No direct manuscript marker | 0 | P1 | Corrected | [B003](endnote_verification_batches/batch_003_explicit_verify_markers.md) | 2026-09-01 | OK |
| `sura-dhatu-dipti` | Chapter 3 L143 | 1 | P0 | Corrected | [B003](endnote_verification_batches/batch_003_explicit_verify_markers.md) | 2026-09-01 | OK |
| `s-mobile-root-extension-confessions` | Chapter 19 L134 | 1 | P0 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `krt-dhatupatha-chedane` | Chapter 19 L142 | 1 | P0 | Verified | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `krt-upasarga-corpus` | Chapter 19 L146 | 1 | P0 | Corrected | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `sut-agama-visarga-s` | Chapter 19 L146 | 1 | P1 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `jan-dhatupatha-double-entry` | Chapter 19 L178 (2 uses); Appendix Part 1 — Baking the Mother Tongue L179 | 3 | P0 | Reconfirmed | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `chambers-1872-king-kin` | Chapter 19 L166 | 1 | P0 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `skeat-aryan-roots-and-edition-drift` | Chapter 19 L170 | 1 | P0 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `muller-1863-janaka-king` | Chapter 19 L172 | 1 | P0 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `rv-1-174-1-indra-asura` | Chapter 3 L161 | 1 | P0 | Corrected | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `rv-1-24-14-varuna-asura` | Chapter 3 L161 | 1 | P0 | Corrected | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `rv-agni-mitra-rudra-asura` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `nirukta-nominal-words-from-actions` | No direct manuscript marker | 0 | P0 | Strengthened | [B003](endnote_verification_batches/batch_003_explicit_verify_markers.md) | 2026-09-01 | OK |
| `yaska-asura-nirukta` | Chapter 3 L145 | 1 | P0 | Corrected | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `samaveda-padapatha-asurasya-split` | Chapter 3 L145 | 1 | P0 | Partial | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `asura-reconstructed-lord-account` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `asura-factional-framing` | Chapter 3 L157 | 1 | P1 | Strengthened | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `asura-academic-industry` | Chapter 3 L149 | 1 | P1 | Verified | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `deva-sur-div-radiance-field` | No direct manuscript marker | 0 | P2 | Parked | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `rigvedic-named-antagonist-asuras` | Chapter 3 L161 | 1 | P1 | Corrected | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `mayin-concealment-cluster` | Chapter 1 L153; Chapter 18 L13 (2 uses) | 3 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `avrata-vow-less-blockade` | Chapter 1 L155 | 1 | P0 | Corrected | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `rv-4-5-5-gabhiram-padam-isolation` | Chapter 1 L162 | 1 | P0 | Reframed | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `apad-ahastah-vrtra-enclosure` | Chapter 1 L164 | 1 | P1 | Narrowed | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `aradhas-panis-hoarders` | Chapter 1 L164 | 1 | P1 | Narrowed | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `kaliya-yamuna-poisoning` | Chapter 1 L129 | 1 | P1 | Strengthened | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `madhu-kaitabha-vedas-theft` | Chapter 1 L131 | 1 | P0 | Corrected | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `hayagriva-asura-vedas-theft` | Chapter 1 L131 | 1 | P0 | Corrected | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `putana-nurse-poison` | Chapter 1 L133 | 1 | P1 | Verified | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `maricha-golden-deer` | Chapter 1 L133 | 1 | P1 | Strengthened | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `kalanemi-ascetic-hanuman` | Chapter 1 L133 | 1 | P1 | Strengthened | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `paundraka-vasudeva` | Chapter 1 L133 | 1 | P1 | Verified | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `vrkasura-bhasmasura-boon-reversal` | Chapter 1 L135 | 1 | P0 | Corrected | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `raktabija-multiplication` | Chapter 1 L137 | 1 | P2 | Strengthened | [B000](endnote_verification_batches/batch_000_random_pilot.md) | 2026-09-01 | OK |
| `shumbha-nishumbha-devi-mahatmyam` | Chapter 1 L139 | 1 | P1 | Strengthened | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `andhakasura-shiva-purana` | Chapter 1 L139 | 1 | P1 | Strengthened | [B009](endnote_verification_batches/batch_009_eight_methods_examples.md) | 2026-09-02 | OK |
| `jalandhara-vrinda-shiva-purana` | Chapter 1 L139 | 1 | P1 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `virocana-chandogya-8-7-8-8` | Chapter 1 L141 | 1 | P0 | Corrected | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `muller-bunsen-1856-priestcraft-overthrow` | Chapter 1 L133 | 1 | P0 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `rigveda-privative-generativity` | Chapter 3 L169 | 1 | P0 | Corrected | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `rigveda-adeva-privative` | Chapter 3 L169 | 1 | P1 | Strengthened | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `asura-generativity-pie-double-standard` | Chapter 3 L169 | 1 | P0 | Strengthened | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `rigveda-1-11-7-maya-mayin` | Chapter 2 L13 (2 uses); Chapter 3 L137 | 3 | P1 | Strengthened | [B006](endnote_verification_batches/batch_006_high_risk_architecture.md) | 2026-09-02 | OK |
| `maya-concealment-projection` | Chapter 1 L153; Chapter 2 L231; Chapter 3 L67 (2 uses); Chapter 4 L33; Chapter 18 L102; Chapter 19 L264; Chapter 20 L185 | 8 | P0 | Reconfirmed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `rigveda-7-104-18-rakshasas-night` | Chapter 3 L13 | 1 | P1 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `rv-1-32-vrtra` | Chapter 1 L129; Chapter 3 L211; Chapter 4 L13 | 3 | P0 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `rv-vala-panis` | Chapter 3 L213 | 1 | P1 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `rv-8-42-1-varuna-measures` | Chapter 3 L221 | 1 | P0 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `rv-3-55-asuratvam-ekam` | Chapter 3 L223 | 1 | P1 | Strengthened | [B003](endnote_verification_batches/batch_003_explicit_verify_markers.md) | 2026-09-01 | OK |
| `maitrayani-samhita-1-9-3-satya-asura` | Part I L17 | 1 | P0 | Strengthened | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `bhagavad-gita-1-2-citation` | Preface — Beyond the Red Lotus L49 | 1 | P1 | Strengthened | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `bhagavad-gita-16-6-daiva-asura` | Chapter 1 L13 | 1 | P1 | Strengthened | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `compatibility-is-not-immunity` | Chapter 1 L93; Chapter 4 L37 | 2 | P0 | Narrowed | [B010](endnote_verification_batches/batch_010_chapter1_to_containment.md) | 2026-09-02 | OK |
| `parampara-vyakaranam-bhartrhari-position-1` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `modern-sanskrit-lineage-roles` | Chapter 20 L179 | 1 | P1 | Strengthened | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `dayananda-rgvedadi-bhashya` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `aurobindo-kapali-sastry-mishra-vedic-lineage` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `ojha-vedic-architecture-corpus` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `kak-vedic-structural-architecture` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `kapoor-text-and-interpretation` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `malhotra-battle-for-sanskrit-pollock-prosecution` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `briggs-1985-ai-magazine` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `kak-paninian-algorithmic` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `staal-formal-systems` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `patanjali-siddhe-shabdarthasambandhe` | Chapter 5 L11 (2 uses) | 2 | P0 | Corrected and promoted | [B014](endnote_verification_batches/batch_014_chapter5_grammar_before_panini.md) | 2026-09-02 | OK |
| `eleven-pathas` | Chapter 18 L317 | 1 | P0 | Strengthened | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `english-sanskrit-loanwords` | Chapter 0 L65 | 1 | P1 | Corrected | [B007](endnote_verification_batches/batch_007_chapter0_foundations.md) | 2026-09-02 | OK |
| `sanskrit-names-as-attributes` | Chapter 0 L71 (2 uses) | 2 | P0 | Verified and strengthened | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `yaska-deva-derivation` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `veda-vyasa-division` | Chapter 0 L157; Chapter 18 L317 | 2 | P1 | Reconfirmed as continuum account | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `sanskrit-generative-wordspace` | Chapter 0 L181; Chapter 12 L205 | 2 | P0 | Reproduced | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `place-value-arabic-transmission` | Chapter 0 L171 | 1 | P1 | Corrected | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `protagonist-sat-epithets` | Chapter 0 L258 | 1 | P1 | Corrected | [B004](endnote_verification_batches/batch_004_asura_maya_evidence_lock.md) | 2026-09-02 | OK |
| `rv-10-72-2-sat-born-from-asat` | Chapter 0 L207; Chapter 18 L237 | 2 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `rv-10-190-1-rta-satya-cocreated` | Chapter 0 L218 | 1 | P1 | Strengthened | [B007](endnote_verification_batches/batch_007_chapter0_foundations.md) | 2026-09-02 | OK |
| `sat-rta-cosmogonic-sequence-inference` | Chapter 0 L226; Chapter 18 L237 | 2 | P1 | Reconfirmed as inference | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `rv-7-104-12-13-sat-asat-vrjina-soma` | Chapter 0 L246 (2 uses) | 2 | P0 | Corrected | [B007](endnote_verification_batches/batch_007_chapter0_foundations.md) | 2026-09-02 | OK |
| `rv-5-51-15-svasti-panthanam` | Chapter 0 L268 | 1 | P1 | Narrowed | [B007](endnote_verification_batches/batch_007_chapter0_foundations.md) | 2026-09-02 | OK |
| `kaplan-zero-erasure` | Appendix Part 3 — The Sonomer and the Audiograph: Sound Engineering, Pun Intended L166 | 1 | P0 | Corrected | [B034](endnote_verification_batches/batch_034_appendix_part3_audiography.md) | 2026-09-03 | OK |
| `sound-script-standard-matrix` | Appendix Part 3 — The Sonomer and the Audiograph: Sound Engineering, Pun Intended L174 (2 uses) | 2 | P1 | Strengthened | [B034](endnote_verification_batches/batch_034_appendix_part3_audiography.md) | 2026-09-03 | OK |
| `siddham-east-asia-sonomeric-field` | Appendix Part 3 — The Sonomer and the Audiograph: Sound Engineering, Pun Intended L198 (2 uses); Appendix Part 5 — The Language Factory L46 | 3 | P0 | Reconfirmed | [B036](endnote_verification_batches/batch_036_appendix_part5_language_factory.md) | 2026-09-03 | OK |
| `ishopanishad-invocation` | Chapter 0 L15 (2 uses) | 2 | P1 | Strengthened | [B007](endnote_verification_batches/batch_007_chapter0_foundations.md) | 2026-09-02 | OK |
| `schleicher-stammbaumtheorie` | Chapter 2 L145 | 1 | P1 | Corrected and applied | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `hlafweard-etymology` | Chapter 2 L143 | 1 | P1 | Corrected and applied | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `dhatu-pre-panini-vedic` | Chapter 2 L159 | 1 | P1 | Corrected | [B006](endnote_verification_batches/batch_006_high_risk_architecture.md) | 2026-09-02 | OK |
| `leviticus-slavery-25-44-46` | Chapter 3 L59 | 1 | P1 | Strengthened | [B000](endnote_verification_batches/batch_000_random_pilot.md) | 2026-09-01 | OK |
| `ephesians-slavery-6-5` | Chapter 3 L59 | 1 | P0 | Narrowed | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `quran-slavery-citations` | Chapter 3 L59 | 1 | P0 | Narrowed | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `delhi-sultanate-mamluk` | Chapter 3 L59 | 1 | P0 | Narrowed | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `assalayana-sutta` | Chapter 3 L61 | 1 | P0 | Corrected | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `caste-colonial-census-hardening` | Chapter 6 L198 | 1 | P0 | Strengthened | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `liber-aravan-etymology` | Chapter 3 L99 | 1 | P1 | Strengthened | [B011](endnote_verification_batches/batch_011_chapter3_order_and_faction.md) | 2026-09-02 | OK |
| `rosa-law-2013` | Chapter 6 L186 | 1 | P1 | Corrected | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `pinker-euphemism-treadmill` | Chapter 6 L186 | 1 | P1 | Strengthened | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `rasashastra-chemistry-anticipation` | Chapter 10 L48 | 1 | P0 | Corrected | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `saptadhatu-standard` | Chapter 10 L48 | 1 | P1 | Narrowed | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `dhatu-cross-linguistic-analogues` | Chapter 10 L54 | 1 | P1 | Qualified | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `dhatupatha-count-and-ganas` | Chapter 10 L52 | 1 | P0 | Corrected | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `retroflex-substrate-standard-account` | Chapter 18 L80 | 1 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `secular-packaging-three-transformations` | Chapter 4 L31 | 1 | P1 | Strengthened | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `four-iterations-architectural-mapping` | Chapter 4 L35 | 1 | P0 | Narrowed | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `genesis-big-bang-god-as-law` | Chapter 4 L63 | 1 | P0 | Corrected | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `heavenly-city-becker` | Chapter 4 L41 | 1 | P1 | Strengthened | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `end-of-history-fukuyama` | Chapter 4 L63 | 1 | P1 | Corrected | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `voegelin-gnosticism` | Chapter 4 L65 | 1 | P1 | Corrected | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `black-mass-gray` | Chapter 4 L67 | 1 | P1 | Narrowed | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `ambedkar-pakistan-partition-1945` | Chapter 4 L81 | 1 | P0 | Locator corrected | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `rostow-modernization-theory` | Chapter 4 L157 | 1 | P0 | Narrowed | [B012](endnote_verification_batches/batch_012_chapter4_secular_eschatology.md) | 2026-09-02 | OK |
| `juvenal-quis-custodiet` | Chapter 4 L185 | 1 | P1 | Corrected | [B013](endnote_verification_batches/batch_013_chapter4_completion.md) | 2026-09-02 | OK |
| `ashtavakra-bandin-mahabharata` | Chapter 4 L193 | 1 | P0 | Corrected and applied | [B013](endnote_verification_batches/batch_013_chapter4_completion.md) | 2026-09-02 | OK |
| `shakalya-padapatha` | Chapter 5 L33 | 1 | P0 | Corrected | [B014](endnote_verification_batches/batch_014_chapter5_grammar_before_panini.md) | 2026-09-02 | OK |
| `panini-cites-pre-paninian-vaiyakaranas` | Chapter 5 L31 | 1 | P1 | Reconfirmed | [B014](endnote_verification_batches/batch_014_chapter5_grammar_before_panini.md) | 2026-09-02 | OK |
| `apauruseya-mimamsa-sutra-1-1-5` | Chapter 17 L163; Chapter 18 L291 | 2 | P0 | Reconfirmed | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `adi-vadya-voice-as-original-instrument` | Chapter 7 L37 | 1 | P1 | Strengthened | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `vocal-tract-cm-modeling` | Chapter 7 L45 | 1 | P1 | Corrected | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `sanskrit-allophone-architecture-comparison` | Chapter 8 L59 | 1 | P1 | Qualified | [B017](endnote_verification_batches/batch_017_chapter8_sound_superset.md) | 2026-09-03 | OK |
| `language-hotzones-inventory-method` | Chapter 7 L93; Chapter 8 L71; Appendix Part 4 — The Consonant Inventory Atlas and Additional Surveys L13 | 3 | P0 | Reconfirmed | [B035](endnote_verification_batches/batch_035_appendix_part4_inventory_atlas.md) | 2026-09-03 | OK |
| `inventory-atlas-coverage-surveys` | Chapter 8 L83; Chapter 9 L88; Appendix Part 4 — The Consonant Inventory Atlas and Additional Surveys L42 | 3 | P0 | Reproduced | [B035](endnote_verification_batches/batch_035_appendix_part4_inventory_atlas.md) | 2026-09-03 | OK |
| `tabla-bols-mouth-to-drum` | Chapter 7 L67 | 1 | P1 | Corrected | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `sarangi-closest-to-human-voice` | Chapter 7 L77 | 1 | P2 | Narrowed | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `nadyashastra-four-instrument-taxonomy` | Chapter 7 L107 | 1 | P1 | Corrected | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `place-of-articulation-sanskrit-terms` | Chapter 7 L113; Chapter 9 L84 | 2 | P0 | Reconfirmed | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `karana-active-articulator` | Chapter 7 L115 | 1 | P0 | Corrected | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `allen-1953-phonetics-ancient-india` | Chapter 7 L107 | 1 | P1 | Strengthened | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `sprista-isatsprista-isatsamvrta-vivrta-constriction` | Chapter 7 L125 | 1 | P0 | Corrected | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `abhyantara-bahya-prayatna` | Chapter 7 L147 | 1 | P0 | Corrected | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `svasa-nada-vivrta-samvrta-phonation` | Chapter 7 L147 | 1 | P0 | Corrected | [B016](endnote_verification_batches/batch_016_chapter7_sound_anatomy.md) | 2026-09-02 | OK |
| `ayogavaha-category-pratisakhya` | Chapter 9 L78 | 1 | P0 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `visarga-anusvara-articulation` | Chapter 8 L202; Chapter 9 L78 | 2 | P0 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `mishra-breath-pedagogy` | Chapter 9 L150 | 1 | P1 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `visarga-cognate-shadow` | Chapter 9 L156 | 1 | P0 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `varnamala-grid-geometry` | Chapter 9 L129 | 1 | P0 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `om-vocal-tract-macro-gesture` | Chapter 7 L11 (3 uses); Chapter 10 L380 | 4 | P0 | Reconfirmed | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `sandhi-anusvara-assimilation` | Chapter 9 L152 | 1 | P0 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `pre-panini-pratisakhya-classification` | Chapter 9 L53 (2 uses) | 2 | P0 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `staal-mendeleev-varga-comparison` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `architecture-not-analysis-pratisakhya` | Chapter 9 L131 | 1 | P1 | Narrowed | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `western-linguistic-encounter-sanskrit-1786-1879` | Chapter 20 L77 | 1 | P0 | Corrected | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `early-19c-comparative-philology-bopp-pott` | Chapter 19 L38; Chapter 20 L81 | 2 | P0 | Reconfirmed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `jones-1786-third-anniversary-discourse` | No direct manuscript marker | 0 | — | Supporting | — | — | OK |
| `ipa-1886-1900-chart` | Chapter 20 L83 | 1 | P0 | Corrected | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `history-of-linguistics-sanskrit-influence` | Chapter 20 L77 | 1 | P0 | Narrowed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `formants-source-filter-theory` | Chapter 9 L131 | 1 | P1 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `hrasva-dirgha-pluta-matra` | Chapter 7 L73; Chapter 9 L170 | 2 | P0 | Reconfirmed | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `vyanjana-duration-shiksha` | Chapter 9 L170; Chapter 15 L21 | 2 | P0 | Reconfirmed | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `vedic-svara-system` | Chapter 9 L206; Chapter 16 L119 | 2 | P0 | Reconfirmed | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `svara-nine-families-132` | Chapter 9 L218 | 1 | P0 | Qualified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `pass-selection-scope-principle` | Chapter 9 L290 | 1 | P1 | Qualified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `vedic-half-e-half-o` | Chapter 9 L200 | 1 | P0 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `svara-restricted-and-lineage-bounded-use` | Chapter 9 L194 | 1 | P1 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `svara-avarna-operation` | Chapter 9 L378 | 1 | P0 | Qualified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `snap-to-grid-pragrihya-exception` | Chapter 9 L324 | 1 | P0 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `sound-volume-two-open-coordinates` | Chapter 9 L338 | 1 | P0 | Qualified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `agnimile-rigveda-opening` | Chapter 9 L392; Chapter 16 L151 | 2 | P0 | Reconfirmed | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `muller-eic-rigveda` | Chapter 18 L157 | 1 | P0 | Corrected | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `savarkar-ratnagiri-mleccha` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `samarth-ramdas-mleccha-verse` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `south-indian-mahaprana-loan-only` | Chapter 8 L79 | 1 | P0 | Corrected | [B017](endnote_verification_batches/batch_017_chapter8_sound_superset.md) | 2026-09-03 | OK |
| `bengali-va-ba-merger` | No direct manuscript marker | 0 | — | Retired | — | — | OK |
| `sindhi-implosives-inventory` | Chapter 9 L412 | 1 | P1 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `tamil-zha-retroflex-approximant` | Chapter 9 L412 | 1 | P1 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `tamil-alveolar-trill` | Chapter 9 L412 | 1 | P1 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `ho-mundari-checked-consonants` | Chapter 8 L131; Chapter 9 L412 | 2 | P0 | Reconfirmed | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `urdu-persian-arabic-loan-phonemes` | Chapter 9 L412 | 1 | P1 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `punjabi-tonal-development` | No direct manuscript marker | 0 | — | Retired | — | — | OK |
| `pahari-tonal-features` | No direct manuscript marker | 0 | — | Retired | — | — | OK |
| `retroflex-global-distribution` | Chapter 8 L180; Chapter 9 L102 | 2 | P0 | Corrected | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `kailasa-temple-ellora-engineering` | Chapter 18 L33 | 1 | P0 | Corrected | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `smrti-as-mnemoniture` | Chapter 14 L40 | 1 | P1 | Corrected | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `flexture-natyashastra-dance` | Chapter 14 L42 | 1 | P1 | Narrowed | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `shruti-as-auditure` | Chapter 14 L44 | 1 | P0 | Corrected | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `auditory-temporal-gap-resolution` | Chapter 14 L66 | 1 | P0 | Verified | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `metered-verbal-pattern-error-detection` | Chapter 14 L74 | 1 | P1 | Verified | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `masoretic-engineered-preservation` | Chapter 14 L149; Appendix Part 2 — The Encyclopaedic Confirmation L91 | 2 | P0 | Reconfirmed | [B033](endnote_verification_batches/batch_033_appendix_part2_encyclopaedic.md) | 2026-09-03 | OK |
| `quranic-engineered-preservation` | Chapter 2 L53; Chapter 14 L151; Appendix Part 2 — The Encyclopaedic Confirmation L93 | 3 | P0 | Reconfirmed | [B033](endnote_verification_batches/batch_033_appendix_part2_encyclopaedic.md) | 2026-09-03 | OK |
| `arabic-religio-political-authority` | Chapter 2 L27 (4 uses); Chapter 13 L149; Chapter 14 L143 (2 uses) | 7 | P0 | Reconfirmed | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `latin-vulgate-engineered-preservation` | Chapter 14 L153 | 1 | P0 | Corrected | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `shiksha-texts-standard-list` | Chapter 15 L19 | 1 | P0 | Corrected | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `shiksha-first-vedanga-priority` | Chapter 15 L29 | 1 | P1 | Qualified | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `eleven-pathas-full-list` | Chapter 15 L35 | 1 | P0 | Corrected | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `ghanapathi-title-recognition` | Chapter 15 L45 | 1 | P1 | Narrowed | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `six-vikrti-pathas-pattern-list` | Chapter 15 L47 | 1 | P0 | Corrected | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `crc-error-detection-analogy` | Chapter 15 L57 | 1 | P1 | Verified | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `combinatorial-redundancy-comparative` | Chapter 15 L67 | 1 | P0 | Narrowed | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `nambudiri-vedic-recitation-isolation` | Chapter 15 L75 (2 uses) | 2 | P0 | Reconfirmed | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `staal-agni-nambudiri-recording` | Chapter 15 L77 | 1 | P1 | Corrected | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `cross-shakha-verification-fieldwork` | Chapter 15 L77 | 1 | P0 | Narrowed | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `masoretic-codification-timing` | Chapter 15 L93 | 1 | P0 | Corrected | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `quran-recitation-vs-pathas-comparison` | Chapter 15 L93 | 1 | P0 | Corrected | [B024](endnote_verification_batches/batch_024_chapter15_aural.md) | 2026-09-03 | OK |
| `conlangs-tolkien-okrand` | Chapter 2 L93 | 1 | P1 | Qualified | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `pie-term-history` | Chapter 19 L104 | 1 | P0 | Corrected | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `thomason-kaufman-1988` | Chapter 19 L203 | 1 | P0 | Corrected | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `ross-metatypy-takia` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `as-bhu-being-paradigm` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `vyutpatti-fivefold-method` | Appendix Part 1 — Baking the Mother Tongue L145 | 1 | P0 | Verified | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `yuj-bhr-radiance-method` | Chapter 19 L293; Appendix Part 1 — Baking the Mother Tongue L159 (2 uses) | 3 | P0 | Corrected | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `upasarga-radiance-apa` | Chapter 19 L312; Appendix Part 1 — Baking the Mother Tongue L275 | 2 | P0 | Reconfirmed | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `agastya-sources` | Chapter 20 L23 | 1 | P0 | Corrected | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `mitanni-sanskritic-evidence` | Chapter 20 L29 (2 uses) | 2 | P0 | Corrected | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `behistun-inscription` | Chapter 20 L39 | 1 | P0 | Strengthened | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `dionysius-thrax-techne` | Chapter 20 L115 | 1 | P0 | Corrected | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `donatus-priscian-grammars` | Chapter 20 L109 | 1 | P0 | Corrected | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `thonmi-sambhota-tibetan-grammars` | Chapter 20 L103 | 1 | P0 | Narrowed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `buddhist-asia-radiance` | Chapter 19 L201; Chapter 20 L65 (5 uses) | 6 | P0 | Reconfirmed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `sibawayh-al-kitab` | Chapter 2 L27; Chapter 20 L117 | 2 | P1 | Reconfirmed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `medieval-hebrew-grammarians` | Chapter 20 L111 | 1 | P0 | Corrected | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `romani-diaspora-evidence` | Chapter 20 L143 | 1 | P0 | Strengthened | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `jones-1786-anniversary-address` | Appendix Part 1 — Baking the Mother Tongue L29 | 1 | P1 | Verified | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `boden-chair-1832-evangelical-purpose` | Chapter 1 L127; Appendix Part 1 — Baking the Mother Tongue L29 | 2 | P0 | Reconfirmed | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `indian-epic-critical-editions` | Appendix Part 2 — The Encyclopaedic Confirmation L23 | 1 | P1 | Verified | [B033](endnote_verification_batches/batch_033_appendix_part2_encyclopaedic.md) | 2026-09-03 | OK |
| `grierson-lsi-classification` | Appendix Part 2 — The Encyclopaedic Confirmation L25 | 1 | P1 | Verified | [B033](endnote_verification_batches/batch_033_appendix_part2_encyclopaedic.md) | 2026-09-03 | OK |
| `deccan-dictionary-project-method` | Appendix Part 2 — The Encyclopaedic Confirmation L61 (2 uses) | 2 | P0 | Strengthened | [B033](endnote_verification_batches/batch_033_appendix_part2_encyclopaedic.md) | 2026-09-03 | OK |
| `jya-trijya-mathematical-terms` | Appendix Part 2 — The Encyclopaedic Confirmation L121 | 1 | P1 | Verified | [B033](endnote_verification_batches/batch_033_appendix_part2_encyclopaedic.md) | 2026-09-03 | OK |
| `appendix-dhatu-case-sources` | Appendix Part 1 — Baking the Mother Tongue L202 (4 uses) | 4 | P1 | Verified | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `deccan-college-founding-arc` | Appendix Part 1 — Baking the Mother Tongue L31 | 1 | P0 | Corrected | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `shabdakalpadruma-deb-1858` | Appendix Part 1 — Baking the Mother Tongue L53 | 1 | P1 | Corrected | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `vacaspatyam-taranatha-1873` | Appendix Part 1 — Baking the Mother Tongue L53 | 1 | P1 | Corrected | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `rg-bhandarkar-honors` | Appendix Part 1 — Baking the Mother Tongue L61 | 1 | P0 | Corrected | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `bopp-1816-conjugationssystem` | Appendix Part 1 — Baking the Mother Tongue L83; Appendix Part 5 — The Language Factory L194 | 2 | P1 | Reconfirmed | [B036](endnote_verification_batches/batch_036_appendix_part5_language_factory.md) | 2026-09-03 | OK |
| `schleicher-1861-compendium` | Chapter 19 L34; Appendix Part 1 — Baking the Mother Tongue L87; Appendix Part 5 — The Language Factory L194 | 3 | P0 | Reconfirmed | [B036](endnote_verification_batches/batch_036_appendix_part5_language_factory.md) | 2026-09-03 | OK |
| `brugmann-grundriss-1886` | Appendix Part 1 — Baking the Mother Tongue L105 | 1 | P1 | Verified | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `pac-pakva-ashtadhyayi-8-2-52` | Appendix Part 5 — The Language Factory L134 | 1 | P0 | Verified | [B036](endnote_verification_batches/batch_036_appendix_part5_language_factory.md) | 2026-09-03 | OK |
| `japanese-loanword-phonotactic-adaptation` | Appendix Part 5 — The Language Factory L151 | 1 | P1 | Strengthened | [B036](endnote_verification_batches/batch_036_appendix_part5_language_factory.md) | 2026-09-03 | OK |
| `dhatupatha-empirical-distribution` | Chapter 10 L174; Appendix Part 6 — The Architecture by the Numbers L88 | 2 | P0 | Reproduced | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `panini-adi-naming-convention` | Chapter 10 L127 | 1 | P2 | Verified | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `zipf-rank-frequency` | Chapter 10 L176 | 1 | P1 | Verified | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `scaffold-distinguishability-by-matra` | Chapter 10 L202 | 1 | P0 | Reproduced | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `vaicitrya-racana-tail` | Chapter 10 L188 | 1 | P1 | Reproduced | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `yaska-agni-nirukta-7-14` | Chapter 10 L308 | 1 | P0 | Strengthened | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `scaffold-deployment-join` | Chapter 10 L268 | 1 | P0 | Reproduced | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `rigvedic-kriya-examples` | Chapter 11 L21 | 1 | P0 | Verified | [B020](endnote_verification_batches/batch_020_chapter11_building_kriya.md) | 2026-09-02 | OK |
| `rigvedic-kriya-breadth` | Chapter 11 L139 | 1 | P0 | Verified | [B020](endnote_verification_batches/batch_020_chapter11_building_kriya.md) | 2026-09-02 | OK |
| `vedic-kr-derived-family` | Chapter 12 L41 | 1 | P0 | Verified | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `rigveda-5-76-2-samskrtam` | Chapter 12 L53 | 1 | P0 | Verified | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `rigveda-5-25-4-word-order` | Chapter 12 L69 | 1 | P0 | Verified | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `rigveda-2-23-1-vakya` | Chapter 12 L121 | 1 | P0 | Verified | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `vedic-kriyapadas-before-panini` | Chapter 11 L17 | 1 | P0 | Verified | [B020](endnote_verification_batches/batch_020_chapter11_building_kriya.md) | 2026-09-02 | OK |
| `apadam-constraint` | Chapter 11 L5; Chapter 12 L61 | 2 | P0 | Reconfirmed | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `juhotyadibhyah-shluh-dadhati` | Chapter 13 L189 | 1 | P0 | Verified | [B022](endnote_verification_batches/batch_022_chapter13_preservation.md) | 2026-09-03 | OK |
| `racana-gana-matrix` | Appendix Part 6 — The Architecture by the Numbers L186 | 1 | P1 | Reproduced | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `vyakarana-etymology` | Chapter 5 L25 | 1 | P0 | Verified and strengthened | [B014](endnote_verification_batches/batch_014_chapter5_grammar_before_panini.md) | 2026-09-02 | OK |
| `vaiyakarana-role-title` | Chapter 5 L25 | 1 | P0 | Verified and strengthened | [B014](endnote_verification_batches/batch_014_chapter5_grammar_before_panini.md) | 2026-09-02 | OK |
| `panini-no-preface` | Chapter 5 L73 | 1 | P1 | Verified | [B014](endnote_verification_batches/batch_014_chapter5_grammar_before_panini.md) | 2026-09-02 | OK |
| `prayojanani-paspashahnika` | Chapter 5 L61 | 1 | P0 | Corrected | [B014](endnote_verification_batches/batch_014_chapter5_grammar_before_panini.md) | 2026-09-02 | OK |
| `varnavada-presupposes-engineering` | Chapter 10 L234 | 1 | P0 | Verified | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `generative-reach-inversion-natural-language` | Appendix Part 6 — The Architecture by the Numbers L104 | 1 | P1 | Strengthened | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `deva-pie-etymology` | Chapter 19 L245 | 1 | P0 | Narrowed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `dhatu-endowment-families` | Chapter 19 L247 | 1 | P0 | Strengthened | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `asura-standard-etymology-contested` | Chapter 19 L318 | 1 | P0 | Reconfirmed | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `bakers-story-category-theft` | Preface — Beyond the Red Lotus L90; Chapter 2 L25 | 2 | P0 | Corrected | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `tolkappiyam-grammar-and-tamil-change` | Chapter 2 L29 (2 uses); Chapter 14 L143 | 3 | P0 | Verified | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `tamil-sanskrit-distributed-grammar` | Chapter 2 L69; Chapter 17 L193 | 2 | P1 | Reconfirmed as synthesis | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `1858-religious-neutrality-after-war` | Preface — Beyond the Red Lotus L3; Chapter 2 L211 | 2 | P0 | Strengthened | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `language-origin-standardization-form` | Chapter 2 L83 | 1 | P1 | Strengthened | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `botanical-drift-prestige-memory` | Chapter 14 L171 | 1 | P1 | Verified and qualified | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `petrified-bounded-forms` | Chapter 2 L59 (2 uses); Chapter 13 L151 (2 uses); Chapter 14 L159 (2 uses) | 6 | P1 | Qualified | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `esperanto-engineered-botanical-transition` | Chapter 2 L105; Chapter 6 L114; Chapter 20 L81 | 3 | P1 | Reconfirmed | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `vedic-variation-eight-claims` | Chapter 6 L158 | 1 | P0 | Corrected | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `chandasi-bhashayam-mode-markers` | Chapter 2 L183; Chapter 17 L167 | 2 | P1 | Strengthened | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `laukika-only-scope-examples` | Chapter 16 L273; Appendix Part 8 — Designed Variations Across the Two Domains L279 | 2 | P0 | Verified | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `three-deployments-framework` | Chapter 20 L163 | 1 | P1 | Verified as synthesis | [B030](endnote_verification_batches/batch_030_chapter20_life_after_pie.md) | 2026-09-03 | OK |
| `dictionary-audit-sources` | Appendix Part 6 — The Architecture by the Numbers L130 | 1 | P0 | Qualified | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `prayoga-audit-valency` | Appendix Part 6 — The Architecture by the Numbers L130 | 1 | P0 | Reproduced | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `mendeleev-1869-table` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `vikarana-as-column-signature` | Chapter 11 L165; Appendix Part 6 — The Architecture by the Numbers L176 | 2 | P1 | Verified | [B020](endnote_verification_batches/batch_020_chapter11_building_kriya.md) | 2026-09-02 | OK |
| `varga-column-as-engineering-axis` | Appendix Part 6 — The Architecture by the Numbers L192 | 1 | P1 | Reproduced | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `inherent-vowel-secondary-axis` | Appendix Part 6 — The Architecture by the Numbers L192 | 1 | P1 | Corrected | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `dcs-vs-dhatupatha-count` | Appendix Part 6 — The Architecture by the Numbers L15 | 1 | P0 | Reproduced | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `cross-corpus-invariance` | Appendix Part 6 — The Architecture by the Numbers L162 | 1 | P0 | Narrowed | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `nasadiya-sukta` | No direct manuscript marker | 0 | P0 | Corrected | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `migration-trap-movement-not-authorship` | Preface — Beyond the Red Lotus L94; Chapter 18 L173 (4 uses) | 5 | P0 | Corrected | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `migration-trap-displacement-routes` | Chapter 18 L185 (4 uses) | 4 | P0 | Corrected | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `migration-trap-india-absorption` | Chapter 18 L207 (2 uses) | 2 | P0 | Verified | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `calibration-hierarchy` | Chapter 2 L137; Chapter 18 L114 | 2 | P1 | Reconfirmed as synthesis | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `vedic-classical-circular-dating` | Appendix Part 9 — Testing the Codification Myth L25 | 1 | P0 | Strengthened | [B039](endnote_verification_batches/batch_039_appendix_part9_codification_myth.md) | 2026-09-03 | OK |
| `calibration-audit-gap` | Appendix Part 9 — Testing the Codification Myth L53 | 1 | P0 | Narrowed | [B039](endnote_verification_batches/batch_039_appendix_part9_codification_myth.md) | 2026-09-03 | OK |
| `mitanni-indic-technical-vocabulary` | Appendix Part 9 — Testing the Codification Myth L75 | 1 | P0 | Strengthened | [B039](endnote_verification_batches/batch_039_appendix_part9_codification_myth.md) | 2026-09-03 | OK |
| `speculation-theory-asuric-certainty` | Chapter 18 L118 | 1 | P1 | Corrected | [B027](endnote_verification_batches/batch_027_chapter18_wrong_question.md) | 2026-09-03 | OK |
| `cross-gana-column-distribution` | Appendix Part 6 — The Architecture by the Numbers L94 | 1 | P0 | Narrowed | [B037](endnote_verification_batches/batch_037_appendix_part6_by_numbers.md) | 2026-09-03 | OK |
| `sutra-laksana-six-criteria` | Chapter 10 L13 | 1 | P0 | Verified | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `yoga-sutra-1-2` | Chapter 10 L368 | 1 | P1 | Verified | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `nyaya-sutra-pramana-1-1-3` | Chapter 10 L370 | 1 | P1 | Verified | [B019](endnote_verification_batches/batch_019_chapter10_building_dhatu.md) | 2026-09-02 | OK |
| `varnamala-comparative-sound-inventories` | Chapter 9 L96 | 1 | P1 | Qualified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `chandas-laghu-guru-virahanka-sequence` | Chapter 14 L110 | 1 | P1 | Reconfirmed | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `whole-language-sutra-discipline-comparator` | Chapter 14 L120 | 1 | P1 | Verified as synthesis | [B023](endnote_verification_batches/batch_023_chapter14_calibration.md) | 2026-09-03 | OK |
| `rigveda-1-164-39-akshara-assembly` | Chapter 12 L21 | 1 | P0 | Corrected | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `nirukta-namany-akhyatajani` | Chapter 12 L31 | 1 | P0 | Verified | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `kr-bonding-examples` | Chapter 12 L199 | 1 | P1 | Verified | [B021](endnote_verification_batches/batch_021_chapter12_building_vakya.md) | 2026-09-03 | OK |
| `hlad-contrast-atom` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `apabhramsa-vivimorphosis-boundary` | Chapter 19 L213 | 1 | P1 | Verified as synthesis | [B029](endnote_verification_batches/batch_029_chapter19_pie_in_sky.md) | 2026-09-03 | OK |
| `vedic-reduplication-abhyasa-examples` | Chapter 17 L69 | 1 | P0 | Verified | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `ahamkara-ego-management` | Chapter 17 L77 | 1 | P1 | Corrected | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `vedic-receiver-sampradana-examples` | Chapter 17 L83 | 1 | P0 | Verified | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `karmani-bhave-karta-demotion` | Chapter 17 L97 | 1 | P0 | Corrected | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `vedic-folded-action-ktva-lyap-examples` | Chapter 17 L119 | 1 | P0 | Verified | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `gerund-coreference-default-not-gate` | Chapter 17 L125 | 1 | P0 | Corrected | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `phillips-harrison-mundari-mimetic-reduplication` | Chapter 17 L55 | 1 | P0 | Verified | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `korku-nagaraja-mouth-mind-evidence` | Chapter 17 L49 (4 uses); Appendix Part 4 — The Consonant Inventory Atlas and Additional Surveys L64 | 5 | P0 | Reconfirmed | [B035](endnote_verification_batches/batch_035_appendix_part4_inventory_atlas.md) | 2026-09-03 | OK |
| `nimitta-chariot` | Chapter 17 L183 | 1 | P0 | Corrected | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `borrowing-model-substrate-areal-claims` | Chapter 17 L147 | 1 | P0 | Strengthened | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `avestan-retroflex-absence` | Chapter 17 L153 | 1 | P0 | Corrected | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `rigveda-five-feature-cluster` | Chapter 17 L159 | 1 | P0 | Verified | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `madhyandina-kanva-branch-shapes` | Chapter 17 L169 | 1 | P0 | Corrected | [B026](endnote_verification_batches/batch_026_chapter17_subcontinental_mouth_mind_order.md) | 2026-09-03 | OK |
| `rigveda-9635-wilson-griffith` | Chapter 1 L129; Chapter 4 L179; Epilogue — The Atris Find the Sun L153 | 3 | P0 | Reconfirmed | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `orl-three-apex-nexus` | Preface — Beyond the Red Lotus L3; Chapter 2 L211; Appendix Part 1 — Baking the Mother Tongue L25 | 3 | P0 | Reconfirmed | [B032](endnote_verification_batches/batch_032_appendix_part1_baking.md) | 2026-09-03 | OK |
| `dharmo-rakshati-rakshitah` | Chapter 0 L298 | 1 | P1 | Verified | [B008](endnote_verification_batches/batch_008_opening_architecture.md) | 2026-09-02 | OK |
| `samudra-manthana-source-anchor` | Epilogue — The Atris Find the Sun L33 | 1 | P1 | Reconfirmed | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `wheeler-mohenjo-daro-overreach` | Chapter 6 L160 | 1 | P0 | Corrected | [B015](endnote_verification_batches/batch_015_chapter6_entropy.md) | 2026-09-02 | OK |
| `rahu-manthana-svarbhanu-layering` | Epilogue — The Atris Find the Sun L41 | 1 | P0 | Strengthened | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `amrta-anti-entropy-principles` | Epilogue — The Atris Find the Sun L49 | 1 | P1 | Reconfirmed | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `colonial-sanskrit-institutes` | Epilogue — The Atris Find the Sun L35 | 1 | P1 | Reconfirmed | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `konkani-marathi-language-pressure` | Epilogue — The Atris Find the Sun L203 | 1 | P0 | Verified | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `rgveda-floating-upasarga-meter` | Chapter 16 L179 | 1 | P0 | Verified | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `aitareya-brahmana-separated-upasargas` | Chapter 16 L181; Appendix Part 8 — Designed Variations Across the Two Domains L138 | 2 | P0 | Verified | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `vedic-functional-range-linguistic-calibrant` | Chapter 16 L239 | 1 | P1 | Verified as synthesis | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `vedic-akaranta-instrumental-plural-range` | Chapter 16 L135; Appendix Part 8 — Designed Variations Across the Two Domains L150 | 2 | P0 | Strengthened | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `vedic-vocative-sentence-accent` | Appendix Part 8 — Designed Variations Across the Two Domains L110 | 1 | P0 | Verified | [B038](endnote_verification_batches/batch_038_appendix_part8_designed_variations.md) | 2026-09-03 | OK |
| `vedic-personal-ending-imasi` | Chapter 16 L131; Appendix Part 8 — Designed Variations Across the Two Domains L120 | 2 | P0 | Verified | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `vedic-jihvamuliya-upadhmaniya-pair` | Chapter 16 L155; Appendix Part 8 — Designed Variations Across the Two Domains L62 | 2 | P0 | Verified | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `designed-variations-figure-sources` | Appendix Part 8 — Designed Variations Across the Two Domains L283 | 1 | P0 | Reproduced | [B038](endnote_verification_batches/batch_038_appendix_part8_designed_variations.md) | 2026-09-03 | OK |
| `vedic-pluta-rv-10-129-5` | Chapter 9 L224; Appendix Part 8 — Designed Variations Across the Two Domains L90 | 2 | P0 | Verified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `vedic-social-sound-calibrant` | Chapter 9 L230 | 1 | P1 | Qualified | [B018](endnote_verification_batches/batch_018_chapter9_sonomeric_grid.md) | 2026-09-03 | OK |
| `vedic-let-bravani-tarisat` | Chapter 16 L206; Appendix Part 8 — Designed Variations Across the Two Domains L196 | 2 | P0 | Verified | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `vedic-injunctive-vocam` | Appendix Part 8 — Designed Variations Across the Two Domains L224 | 1 | P0 | Strengthened | [B038](endnote_verification_batches/batch_038_appendix_part8_designed_variations.md) | 2026-09-03 | OK |
| `vedic-gerund-pitvi` | Appendix Part 8 — Designed Variations Across the Two Domains L240 | 1 | P0 | Verified | [B038](endnote_verification_batches/batch_038_appendix_part8_designed_variations.md) | 2026-09-03 | OK |
| `vedic-infinitives-rv-1-24-8` | Appendix Part 8 — Designed Variations Across the Two Domains L256 | 1 | P0 | Verified | [B038](endnote_verification_batches/batch_038_appendix_part8_designed_variations.md) | 2026-09-03 | OK |
| `vedic-participle-cikitvah` | Appendix Part 8 — Designed Variations Across the Two Domains L262 | 1 | P0 | Verified | [B038](endnote_verification_batches/batch_038_appendix_part8_designed_variations.md) | 2026-09-03 | OK |
| `vaidika-laukika-household-responsibility-cases` | Chapter 16 L323; Appendix Part 8 — Designed Variations Across the Two Domains L311 | 2 | P1 | Corrected | [B025](endnote_verification_batches/batch_025_chapter16_two_domains.md) | 2026-09-03 | OK |
| `english-empire-layered-pyramid` | Chapter 1 L87 | 1 | P1 | Verified as synthesis | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
| `bhiksha-calibrant-architecture` | Epilogue — The Atris Find the Sun L185 (2 uses) | 2 | P1 | Strengthened | [B031](endnote_verification_batches/batch_031_epilogue.md) | 2026-09-03 | OK |
| `where-this-argument-stands` | No direct manuscript marker | 0 | — | Parked | — | — | OK |
| `anti-sanskrit-progress-parliament` | Chapter 1 L107 | 1 | P0 | Strengthened | [B028](endnote_verification_batches/batch_028_preface_chapter3_completion.md) | 2026-09-03 | OK |
