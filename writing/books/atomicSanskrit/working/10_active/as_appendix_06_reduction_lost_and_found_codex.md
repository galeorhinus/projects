# Appendix Part 6 Reduction — Lost and Found

This file preserves passages removed or consolidated during the 2026-09 reduction of Appendix Part 6. The revised appendix retains all eight engineering principles, all principal measurements, and the figures required to interpret them. The periodic-axes figure and its accompanying prose moved to the full *Source and Reference Companion* rather than being discarded. Rephrased sentences can also be recovered through Git.

## LF-AP6-001 — Corrected-Count Repetition

**Recorded:** 2026-09-06
**Source:** Appendix Part 6 §6.1, “The Structural Baseline”
**Disposition:** Removed as repetition. The preceding method paragraph still explains the removal of instructional markers, and the table retains the corrected 58.2-percent and 98.2-percent results. The full correction history remains in the companion.

### Superseded Text

> Earlier provisional counts did not remove every instructional marker and therefore made the atoms appear larger. Once those markers are removed, the modal three-particle form rises to 58.2 percent, and atoms built around a single अक्षर (*akṣara*) account for 98.2 percent of the inventory. The analysis must distinguish the atom from the notation used to describe it.

## LF-AP6-002 — Repeated Cluster-Joiner Explanation

**Recorded:** 2026-09-06
**Source:** Appendix Part 6 §6.2, Principle 4
**Disposition:** Consolidated into one paragraph. The revised paragraph retains the measured contrast between र् (*r*) and ल् (*l*) and the joining role of the अन्तःस्थाः (*antaḥsthāḥ*).

### Superseded Text

> The largest circle belongs to **र् (*r*)**. It appears frequently on both sides of the vowel and joins more consonant clusters than any other sonomer in this count. This range allows **र् (*r*)** to connect sounds throughout a धातुः (*dhātuḥ*).
>
> The circle for **ल् (*l*)** lies much closer to the dashed line. It appears before and after the vowel in a more balanced proportion. The category therefore describes a function rather than an ornament. These sounds join one consonant to another, while other sounds appear more often at the boundaries.

## LF-AP6-003 — Natural-Language Detour

**Recorded:** 2026-09-06
**Source:** Appendix Part 6 §6.2, Principle 8
**Disposition:** Removed from the body. The endnote remains attached to the conclusion in §6.3 and preserves the comparison with frequent irregular verbs in natural languages.

### Superseded Text

> English places irregular forms such as *be*, *have*, and *do* among its most frequent verbs; Latin and Greek offer comparable examples. The current audit examines a different Sanskrit relation: the atoms with the greatest generative reach are concentrated among the smaller forms. A complete comparison of paradigm irregularity would require a separate audit, but the observed concentration already shows that Sanskrit keeps many of its busiest atoms compact and reusable.[NOTE: generative-reach-inversion-natural-language]

## LF-AP6-004 — Repeated Definitions of Reach

**Recorded:** 2026-09-06
**Source:** Appendix Part 6 §§6.2–6.3
**Disposition:** Consolidated. The revised text defines Path A and Path C once, retains the 121-atom overlap, and explains the +0.66 correlation.

### Superseded Text

> Path A and Path C calculate two different kinds of reach. Path A estimates how many primary derivatives each atom generates. The appendix calls this its **generative reach**. Path C counts the combinations in which each atom appears across the corpus. The appendix calls this its **combinatorial reach**.
>
> Both forms of reach tend to fall as particle count rises. Smaller atoms therefore tend to generate more derivatives and appear in more recorded combinations.
>
> Path A and Path C calculate different kinds of reach. The dictionary sample counts how many words lexicographers connect with a selected धातुः (*dhātuḥ*). The corpus audit counts how many combinations of prefix and grammatical form-class actually occur with that atom in the parsed texts.[NOTE: dictionary-audit-sources][NOTE: prayoga-audit-valency]
>
> The two measurements agree often enough to identify the same high-reach center. Across the atoms found in both records, their correlation is **+0.66**. A result of +1.00 would mean that their rankings matched perfectly. A result close to zero would mean that one record provided no indication of the other. The observed result shows substantial agreement without pretending that a dictionary and a corpus count the same thing.

## LF-AP6-005 — Defensive Qualifications

**Recorded:** 2026-09-06
**Source:** Appendix Part 6 §§6.3–6.4
**Disposition:** Removed. The retained prose already states that the four corpora give the atoms different rankings and that atomic construction does not determine activation by itself.

### Removed Sentences

> The comparison shows a compact core extending through both Vedic and लौकिक (*laukika*) expression; it does not claim that the four texts use that core in identical proportions.
>
> The technical appendix tests that relationship numerically. The body chapter needs only the simpler conclusion that different atoms follow recurring activation patterns.

## LF-AP6-006 — Periodic Axes

**Recorded:** 2026-09-06
**Source:** Appendix Part 6 §6.4
**Disposition:** Moved with both endnote markers and the figure to `companion/as_reference_06_by_the_numbers_full.md`, after the Path C analysis. The material remains in the full reference edition.

### Moved Text

> The periodic-axes figure tests a second arrangement. It places the धातवः (*dhātavaḥ*) recorded in the corpus by the वर्ग (*varga*) column of their first consonant and by their inherent vowel, then uses marker size and color to show combinatorial reach.[NOTE: varga-column-as-engineering-axis][NOTE: inherent-vowel-secondary-axis]
>
> ![धातवः (*Dhātavaḥ*) recorded in the corpus, arranged by initial वर्ग (*varga*) column and inherent vowel.](figures/ganah/periodic_table.svg){#fig:appendix-numbers-periodic-axes width=100%}
>
> The figure uses chemical periodicity as an analytical analogy. It asks whether properties already present inside an atom help predict how widely that atom enters verbal combinations. The numerical results and replication files allow that interpretation to be tested independently.

## LF-AP6-007 — Repeated Synthesis and Replication Inventory

**Recorded:** 2026-09-06
**Source:** Appendix Part 6 §§6.5–6.6
**Disposition:** Consolidated. The revised close retains the recurring patterns, वैचित्र्य (*vaicitrya*), the location of the replication bundle, and the distinction between Path A and Path C. The future Path B description remains in the full companion.

### Superseded Text

> Several independent counts reveal the same organization. Sanskrit concentrates meaning in compact atoms. It places sounds differently at the opening and closing positions of those atoms. A small set of sounds performs most of the joining inside clusters. The activation groups also have different sound profiles. Finally, both the dictionary sample and the corpus analysis show greater reach among smaller atoms.
>
> The inventory also contains a long tail of rare scaffolds and specialized shapes. That range is **वैचित्र्य (*vaicitrya*)**: structured variety around strong modal forms. The book's engineering claim rests on both features together, because a generative architecture needs compact defaults as well as specialized forms.
>
> These patterns recur across the sound inventory, atomic construction, verbal activation, and recorded use. Together they provide the numerical evidence for the engineering demonstrated through words and sentences in Chapters 10, 11, and 12.
>
> The *Source and Reference Companion* preserves the replication trail:
>
> - the complete Path A tables from `analysis/dhatupatha/`;
> - the complete Path C corpus audit from `analysis/ganah/`;
> - the stripping-rule correction history;
> - the questions tested, the data used, and the resulting conclusions;
> - the जुहोत्यादि (*juhotyādi*) C4 correction from 31.8% to 33.3%, and the Path C sharpening to 42.9%;
> - the complete script-to-output map for reproducing each table.
>
> The code bundles are already organized for public audit. The structural baseline counts entries listed in the धातुपाठ (*Dhātupāṭha*). Path A estimates generative reach from a selected dictionary sample, while Path C counts combinatorial reach from forms recorded in the corpus.
>
> A future Path B can calculate the complete set of combinations made possible by the *Aṣṭādhyāyī*. It would examine what the rules allow beyond the forms that dictionaries list or the corpus records.
>
> The printed book presents the result, while the companion preserves the audit trail for readers who want to rerun the tests. Across these analyses, the धातुपाठ (*Dhātupāṭha*) behaves as an atomic inventory organized for compression, distinction, and generative reach. The book identifies that recurring organization as engineering.
