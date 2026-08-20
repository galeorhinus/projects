# Chapters 11–12 Engineering Restructure — Lost and Found

**Date:** 2026-08-17  
**Baseline commit:** `679aa4e4ce6c734f5a88636c01a4975a78809700`  
**Purpose:** Preserve and route material removed when Chapters 11 and 12 were reorganized around the sequence *dhātuḥ → kriyāpadam → śabdaḥ → padam → vākyam*.

The baseline commit preserves the complete pre-restructure text byte for byte. The entries below identify every substantive removal, its destination, and its possible future use. The five Vedic assembly figures remain in Chapter 11. No source figure or replication file was deleted.

## LF-1112-001 — Five Repeated Pāṇinian Derivations

**Source:** Former Chapter 11 §11.3, “Pāṇini's Notation Layer.”  
**Removed from body:** The second walkthrough of **इ → एति**, **अस् → अस्ति**, **यज् → यजति**, **भू → भवति**, and **राज् → राजति**, including five Pāṇinian notation figures.  
**Reason:** The body had already demonstrated the same five verbs through Vedic examples and hexes. Repeating every example through the *Aṣṭādhyāyī* changed the chapter from an engineering demonstration into a conjugation lesson.  
**Disposition:** The Vedic sequence remains in Chapter 11 §11.2. Chapter 11 §11.4 now explains Pāṇini's analytical contribution once. The five `panini_*.svg` source and promoted files remain in `figures/building_kriya/` for future appendix or teaching use. The complete removed prose remains retrievable from the baseline commit.

## LF-1112-002 — Ten *Gaṇāḥ* as the Body-Chapter Spine

**Source:** Former Chapter 11 §§11.4–11.5.  
**Removed from body:** The two operation figures, the extended explanation of ten verbal classes, and the *racanā–gaṇa* matrix discussion.  
**Reason:** The body needs to show that Vedic verbs already display recurring formation patterns. It does not need to teach the complete ten-class taxonomy.  
**Disposition:** Moved to Appendix Part 6 §6.4, “The Explicit Activation Analysis.” The appendix now contains both mechanism figures, the matrix figure, the principal counts, and the distinction between the affixes prescribed by the *Aṣṭādhyāyī* and the later umbrella term *vikaraṇa*.

## LF-1112-003 — Reactivity Methodology and Secondary Tables

**Source:** Former Chapter 11 §§11.6–11.9.  
**Removed from body:** Detailed corpus methodology, the audit-purpose table, the top-9/top-20/top-100/top-500 table, the natural-language comparison table, the extended carbon analogy, and secondary discussion of the periodic axes.  
**Reason:** The chapter needs the results that demonstrate generative reach, while the full research method belongs in the numerical appendix and endnotes.  
**Disposition:** Chapter 11 §§11.5–11.6 retain the two-source comparison, correlation, highest-reactivity atoms, tier result, size correlation, and cross-corpus result. Appendix Part 6 §§6.3–6.6 retain the methodology, numerical tests, operation analysis, periodic-axes figure, and replication trail. The `dictionary-audit-sources`, `prayoga-audit-valency`, `dcs-vs-dhatupatha-count`, `cross-corpus-invariance`, `varga-column-as-engineering-axis`, `inherent-vowel-secondary-axis`, and `cross-gana-column-distribution` endnotes retain the supporting detail.

## LF-1112-004 — Mendeleev Comparison

**Source:** Former Chapter 11 §11.10.  
**Removed from body:** The comparison between the Sanskrit analytical table and Mendeleev's 1869 periodic table.  
**Reason:** The comparison no longer closes the revised atom-to-action argument and places the modern analogy above the Sanskrit evidence.  
**Disposition:** The `mendeleev-1869-table` endnote remains intact for possible use with Appendix Part 6 or the Source and Reference Companion.

## LF-1112-005 — Full Vivimorphosis Treatise

**Source:** Former Chapter 12 §12.9, “Boundary Crossing: Apabhraṃśa = Vivimorphosis.”  
**Removed from body:** The extended four-classification table, full explanation of petrification, revivification, vivification, and vivimorphosis, and the longer application to the Radiance Thesis.  
**Reason:** The material interrupted Chapter 12's word-to-sentence demonstration and repeated arguments already developed in Chapters 2, 6, and 19.  
**Disposition:** Chapter 12 §12.9 retains a short bridge from calibrated Sanskrit formation to organic change in a receiving language. Chapter 6 remains the primary account of the four language behaviors and entropy. Chapter 19 §19.7 remains the primary application to Sanskrit's outward radiance. The full former text remains retrievable from the baseline commit.

## LF-1112-006 — Pre-Restructure Line 156

Immediately before the restructure, Chapter 11 line 156 had already been revised from “Pāṇini's own machinery proves the point” to:

> The *Aṣṭādhyāyī* documents the same principle at the sonomeric level. Its rules apply not to whole words but to *varṇāḥ* — sonomers — through classes like *ac*, *hal*, *ik*, *yaṇ*, *jhal*, and *khar*. The atom was built at the sonomeric level, and the molecule is activated at the same level, which means the *kriyā* represents the next scale of the same assembly: the measured particles stay visible when the atom becomes a verb.

This uncommitted intermediate wording is preserved here because it does not appear in the baseline commit. Its central point survives in revised Chapter 11: the *Aṣṭādhyāyī* documents the analytical procedure rather than creating the Vedic forms.

## LF-1112-007 — Quoting Apparatus in Chapter 11 §11.2

**Source:** Chapter 11 §11.2, opening paragraphs.
**Removed from body:** The explanation of why the examples quote the *padapāṭha* rather than the connected recitation, and the naming of **प्रथमपुरुष-एकवचनम् (*prathama-puruṣa-ekavacanam*)** for the shared **ति** ending.
**Reason:** Author direction, 2026-08-17: the section's purpose is to show that Vedic forms already demonstrate atoms becoming molecules. Explaining the quoting method in the body turned that demonstration into a methodological preamble. The endnote `rigvedic-kriya-examples` already carried the same explanation twice — "the excerpts are presented in pada-separated form so the inspected verbal molecule remains distinct before *saṃhitā* sandhi recombines the line," and "the *padapāṭha* rather than the continuous *saṃhitā* line is quoted because the separated pada form isolates the molecule under inspection" — so the body text was duplicating its own note. The endnote also already carried "not offered as a full conjugational lesson," which the body was restating.
**Disposition:** Nothing lost. The *padapāṭha* rationale remains in `rigvedic-kriya-examples` in the two sentences quoted above. The grammatical term was added to that endnote, together with the detail that the two traditions count persons from opposite ends — the *vyākaraṇa* discipline's *first* person is English grammar's third. The body now states the ending's function plainly: it "marks a single doer: *he*, *she*, or *it*."

**Secondary note.** Before this cut, the body sentence had been revised twice for clarity — the second version read "The examples below quote the **पदपाठ (*padapāṭha*)**, the recitation that separates a line into its individual words. Each completed verb can therefore be examined on its own, before *sandhi* fuses it with the words on either side in connected recitation." That revision fixed a real defect: the original used **संहिता (*saṃhitā*)** to mean the connected recitation mode, a sense the body never teaches, while every earlier use in the manuscript means the text division (Saṃhitā / Brāhmaṇa / Āraṇyaka / Upaniṣad). The sentence has since been removed entirely rather than kept in improved form. If any version is ever restored to the body, restore the revised wording, not the original.

## LF-1112-008 — Baseline Before the Vedic-Breadth Rewrite

**Date:** 2026-08-20
**Purpose:** Preserve the complete Chapters 11 and 12 that existed immediately before the rewrite planned in `as_ch11_ch12_vedic_engineering_rewrite_plan_codex.md`.

Exact snapshots:

- `working/40_reference/source_material/ch11_pre_vedic_breadth_rewrite_2026-08-20.md`
- `working/40_reference/source_material/ch12_pre_vedic_breadth_rewrite_2026-08-20.md`

The Chapter 11 snapshot has SHA-256 `7f70adda632f1091b9a802a3962738a6b2d785f93adbf52f20c13989cd1bafb4`.

The Chapter 12 snapshot has SHA-256 `225d6b8aef952ddf95c539319fd6d3fa425727aa85edc7fced7f6d9945d67a38`.

These snapshots include every paragraph, figure deployment, note marker, and author revision present at the Pass 2 review gate. Later passes may move or replace material, but nothing from this baseline will depend on memory or an uncommitted diff for recovery.

## LF-1112-009 — Chapter 11 Numerical Spine Removed from the Body

**Source:** The Pass 2 snapshot of Chapter 11, especially the sections on corpus counts, reactivity tiers, periodic axes, and numerical comparisons.
**Removed from body:** The numerical argument that had become the principal structure of Chapter 11.
**Reason:** Chapter 11 now has one purpose: demonstrate how Sanskrit extends Vedic *dhātavaḥ* into completed verbs. The numerical analysis supports that demonstration but should not interrupt it.
**Disposition:** Appendix Part 6 remains the primary destination. The exact pre-rewrite chapter is preserved in `ch11_pre_vedic_breadth_rewrite_2026-08-20.md`. Passes 7 and 8 will compare the removed material against Appendix Part 6 and move only material that the appendix does not already contain.

## LF-1112-010 — Chapter 11 Examples Reallocated

**Source:** The Pass 2 snapshot of Chapter 11.
**Removed or reduced in the body:** The former detailed sequence centered on **अस्ति, यजति,** and **राजति**, together with figures that repeated the same formation argument.
**Reason:** The new body uses five examples that demonstrate five visibly different procedures: vowel change, vowel change with insertion, repetition, nasal insertion, and nasal extension.
**Disposition:** **अस्ति** and the **यजति / यजते** pair remain in the compact breadth section. **राजति** remains in Chapter 12 as a short sentence example. The old figures remain in `figures/building_kriya/`; no source figure was deleted. The full old prose remains in the Chapter 11 snapshot.

## LF-1112-011 — Chapter 12 Material Removed from the Sentence Spine

**Source:** The Pass 2 snapshot of Chapter 12.
**Removed from the body:** The extended ⟪कृ⟫ / ⟪ह्लाद्⟫ comparison, the twenty-million-form estimate, repeated explanations of head-bonds and tail-bonds, the full vivimorphosis treatment, and figures that repeated those arguments.
**Reason:** Chapter 12 now follows one continuous construction from *dhātuḥ* to derived word, from word to *padam*, and from *padam* to Vedic sentence. The removed material either duplicates that construction or belongs to another chapter.
**Disposition:** The compact ⟪कृ⟫ family and bonding matrix remain in Chapter 12. Vivimorphosis is reduced to a forward pointer, with Chapter 19 §19.7 as its primary body location. Numerical and comparative material remains available for Appendix Part 6 or the reference notes. Every removed paragraph and figure deployment remains in `ch12_pre_vedic_breadth_rewrite_2026-08-20.md`; no source figure was deleted.

## LF-1112-012 — Domain-Consistency Baseline and Vedic-Only Examples

**Date:** 2026-08-20
**Purpose:** Preserve the complete Pass 6 chapters immediately before the examples were restricted to grammar shared by the *vaidika* and *laukika* domains.

Exact snapshots:

- `working/40_reference/source_material/ch11_pass6_before_domain_consistency_2026-08-20.md`
- `working/40_reference/source_material/ch12_pass6_before_domain_consistency_2026-08-20.md`

The Chapter 11 snapshot has SHA-256 `57964c51ff4ee418c25f60ae45b215d9608ba952ce136625b6179ca0bcafa439`.

The Chapter 12 snapshot has SHA-256 `53866e6fe8d12c0d7b15681503e8b19290d1c3433610d9dcdd87441ed9fe49e7`.

**Removed or rerouted from the body:** **ईळे (*īḷe*)**, the Vedic **ळ** sound, **कृणोति / कृणोषि** and related nasal extensions from ⟪कृ⟫, **भवाति (*bhavāti*)** as a *leṭ* example, **कर्त्वम् (*kartvam*)**, the separated *upasargāḥ* in RV 1.164.39, and the Vedic-only forms analyzed through RV 7.81.4.

**Reason:** Chapters 11 and 12 establish the Vedas as the grammatical and pronunciation calibrant for *laukika* Sanskrit. Their principal examples must therefore demonstrate operations that a student can carry from the Vedas into *laukika* composition. The designed differences between the domains require a separate argument.

**Disposition:** Chapter 16 and Appendix Part 8 remain the primary locations for Vedic-only sounds, endings, verbal forms, and floating *upasargāḥ*. Appendix Part 7 may retain complete passage parsing where useful. The two snapshots above preserve every removed paragraph and table row exactly as it stood before rerouting.

## LF-1112-013 — Pass 7 Reallocation

**Date:** 2026-08-20
**Purpose:** Record where the material removed from Chapters 11 and 12 now resides.

**Chapter 11 numerical material:** Appendix Part 6 now contains the agreement between the dictionary and corpus records, the three reach tiers, and the comparison across the *Ṛgveda*, *Atharvaveda*, *Mahābhārata*, and *Rāmāyaṇa*. The size correlations and research method were already present there, so Pass 7 did not duplicate them. The source remains preserved in `ch11_pre_vedic_breadth_rewrite_2026-08-20.md`.

**Chapter 11 and 12 Vedic evidence:** Appendix Part 7 now records the five verbal preparation procedures used in Chapter 11, the full person-and-number table, the time-command-possibility table, four forms generated from ⟪कृ⟫, and the three sentence examples used in Chapter 12. The appendix retains its three additional passage analyses after this concordance. The Pass 6 snapshots preserve the Vedic-only examples that were rerouted to Chapter 16 and Appendix Part 8.

**Vivimorphosis:** Chapter 12 retains only a forward pointer. Chapter 19 §19.7 now owns the two-sided boundary description: *apabhraṃśa* from Sanskrit's side and vivimorphosis from the receiving language's side. It also owns the movement from *śabda* through *bīja* to *apaśabda*. The former Chapter 12 prose remains preserved in `ch12_pre_vedic_breadth_rewrite_2026-08-20.md`.

**Figures:** No source figure was deleted. The older `figures/building_vakya/vivimorphosis.svg` remains available but is not deployed because Chapter 19 already uses `figures/pie_in_sky/stha_vivimorphosis.svg`. Appendix Part 6 now deploys the existing reactivity-tier and cross-corpus rank figures under appendix-specific figure identifiers.

## LF-1112-014 — Compact Person-and-Number Demonstration

**Source:** Chapter 11 §11.3 after Pass 7.
**Removed from the body:** The three-by-three table that used several Vedic atoms to display singular, dual, and plural forms for the speaker, the person addressed, and the person described.
**Reason:** The body now uses six singular and plural forms generated from ⟪इ⟫. Keeping one atom constant makes the engineering easier to see, while omitting the dual keeps the first demonstration compact.
**Disposition:** The complete nine-position Vedic concordance remains in Appendix Part 7 §7.2 with all nine passage references. The removed body table therefore remains present in the manuscript as supporting evidence rather than disappearing.
