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
