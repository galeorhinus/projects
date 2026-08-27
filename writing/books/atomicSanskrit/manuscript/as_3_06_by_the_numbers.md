# Appendix Part 6 — The Architecture by the Numbers

By the end of Chapter 10, the botanical substitute is gone and the धातुः (*dhātuḥ*) stands as an engineered semantic atom. Chapter 11 shows that atom in use. The numerical audit behind those chapters compares the size and sound structure of the atoms with the range of forms they generate.

No single number can establish engineering. The pattern has to recur at several levels. This appendix therefore examines the size and internal construction of the atoms, the positions in which their sounds appear, the procedures that activate them, and the range of words and grammatical combinations they support. The *Source and Reference Companion* preserves the tables, scripts, correction history, and replication notes. The account here presents the source, the method, and the strongest patterns in the counts.

The audit uses three related datasets, and their totals count different things. The structural baseline contains 2,168 listed entries from a digital Pāṇinian **धातुपाठ (*Dhātupāṭha*)** across the ten **गणाः (*gaṇāḥ*)**. The citation markers called **अनुबन्धाः (*anubandhāḥ*)** are removed before the sounds of each listed atom are counted.

**Path A** then compares particle count with estimated derivative counts for a selected sample of 138 atoms, using the Monier-Williams and Apte dictionaries. **Path C** examines the Digital Corpus of Sanskrit. Its parser produced 3,839 normalized verb lemmas, including derived lemmas such as causatives that are not separate entries in the धातुपाठ (*Dhātupāṭha*). For each lemma, Path C counts the distinct combinations of prefix and grammatical form-class recorded in the corpus. The 2,168 listed entries, the 138-atom sample, and the 3,839 corpus lemmas are therefore three different units.[NOTE: dcs-vs-dhatupatha-count]

Each source brings its own limitation. A dictionary sample reflects the choices made by its compilers, while a preserved corpus reflects its genres and transmission history. When the same relation appears in both, the result deserves more weight than either source could provide alone.

---

## 6.1 The Structural Baseline

The listed form of a धातुः (*dhātuḥ*) can include instructional markers that direct later grammatical operations without belonging to the pronounced atom. The *Aṣṭādhyāyī* documents how these markers function. The audit therefore removes them before counting particles; otherwise it would count grammatical notation as part of the atom.

Once those markers are removed, the compression becomes severe:

| Particles | Count | % | Common patterns | Examples |
|---|---:|---:|---|---|
| 1 | 9 | 0.4% | V, C | ऋ (*ṛ*), इ (*i*), ई (*ī*), उ (*u*) |
| 2 | 251 | 11.6% | CV, VC | कृ (*kṛ*), भू (*bhū*), दा (*dā*), जि (*ji*) |
| 3 | 1,262 | 58.2% | CVC, CCV, VCV | गम् (*gam*), पत् (*pat*), वच् (*vac*) |
| 4 | 556 | 25.6% | CCVC, CVCC, CVCV | स्वप् (*svap*), ज्वल् (*jval*), बन्ध् (*bandh*) |
| 5 | 79 | 3.6% | CCVCC, CVCVC, CCVCV | स्पन्द् (*spand*), स्कन्द् (*skand*) |
| 6+ | 11 | 0.5% | rare extended forms | — |

These rows now account for all 2,168 listed entries. When the same entries are counted by अक्षर (*akṣara*), **98.2%** contain a single अक्षर (*akṣara*). Semantic force is concentrated into small, stable forms.

Earlier provisional counts did not remove every instructional marker and therefore made the atoms appear larger. Once those markers are removed, the modal three-particle form rises to 58.2 percent, and atoms built around a single अक्षर (*akṣara*) account for 98.2 percent of the inventory. The analysis must distinguish the atom from the notation used to describe it.

---

## 6.2 Eight Engineering Principles

Eight linked principles emerge from the counts. Each one describes a different part of the same architecture.

### 1. Cost and Distinguishability

The first वर्ग (*varga*) column, formed without voicing or aspiration, occurs most often. Greater physical effort does not by itself predict rarity, however. The voiced aspirates of the fourth column require greater articulatory effort than the voiceless aspirates of the second column, yet the fourth column occurs more often. Its combination of voicing and breath also gives it a stronger acoustic signature. The distribution therefore reflects both the effort required to produce a sound and the distinctions that listeners can hear.

The audit combines those two properties in a simple ratio: distinguishability divided by cost. That ratio has a positive correlation with frequency, but it accounts for only part of the distribution. The exact sound and its position inside the atom also affect how often it appears.

### 2. Cell-Level Allocation

Equal column value does not produce equal deployment. The labial nasal म् (*m*), for example, appears often, while the velar nasal ङ् (*ṅ*) is almost absent from the same inventory count. A column-level preference cannot explain that difference; the exact cell also affects how a sound is used.

The column identifies one property of a sound. The exact grid address identifies the complete bundle of properties that the atom can use.

### 3. Position-Conditional Preference

Position changes the physical action of a consonant. At the opening of an atom, the consonant releases into the vowel. At the end, it closes the atom and participates in later सन्धि (*sandhi*) operations. The counts reflect that difference.

Retroflex sounds occur less often before the vowel and much more often after it. Palatals also favor the closing side. Velars and labials show the opposite preference and appear more often before the vowel. The same consonant can therefore contribute differently when it opens an atom, closes it, or joins a cluster.

The following figure counts these positions across the धातुपाठ (*Dhātupāṭha*) atoms built around a single अक्षर (*akṣara*) and one vowel. Each circle represents one consonant. Its horizontal position counts uses before the vowel, its vertical position counts uses after the vowel, and its size shows how often the consonant appears inside a cluster. The colors follow the वर्णमाला (*varṇamālā*) by grouping consonants according to where the mouth produces them.

![Where consonants appear around the vowel in atoms built around a single अक्षर (*akṣara*).](figures/building_dhatuh/role_map_color.svg){#fig:appendix-numbers-dhatuh-role-map width=100%}

The dashed line marks equal use before and after the vowel. **क, व, प,** and **श** sit farther to the right because they occur more often before the vowel. **ष, ज, स, ट,** and **ड** sit higher because they occur more often after it.

### 4. Cluster-Joiner Specialization

Consonant clusters do not use every sound in the same way. Most of the joining falls to a small class whose major members are the **अन्तःस्थाः (*antaḥsthāḥ*)** — य्, र्, ल्, व् (*y, r, l, v*). The Sanskrit term describes sounds that stand between the stop rows and the **ऊष्माणः (*ūṣmāṇaḥ*)**. Their placement in the वर्णमाला (*varṇamālā*) matches the connecting role that the count reveals, with र् (*r*) performing that role most often.

The largest circle belongs to **र् (*r*)**. It appears frequently on both sides of the vowel and joins more consonant clusters than any other sonomer in this count. This range allows **र् (*r*)** to connect sounds throughout a धातुः (*dhātuḥ*).

The circle for **ल् (*l*)** lies much closer to the dashed line. It appears before and after the vowel in a more balanced proportion. The category therefore describes a function rather than an ornament. These sounds join one consonant to another, while other sounds appear more often at the boundaries.

### 5. मूर्धन्य (*Mūrdhanya*) Dual-Role Engineering

The **मूर्धन्य (*mūrdhanya*)** anatomical coordinate bears unusual load. It appears frequently at the ends of atoms, participates heavily in cluster-joining, and connects with the ऋ (*ṛ*) / र् (*r*) bridge. The counts place a coordinate treated as marginal by the usual story near the center of Sanskrit's atomic construction.

The relationship between **ऋ (*ṛ*)** and **र् (*r*)** extends this pattern across the vowel and consonant systems. Sanskrit places both at the मूर्धन्य (*mūrdhanya*) position. **ऋ (*ṛ*)** can occupy the vowel-center of an अक्षर (*akṣara*), while **र् (*r*)** can connect with sounds on either side of that center. When **ऋ (*ṛ*)** appears before another vowel, ***यण्-सन्धि (*yaṇ-sandhi*)*** replaces it with **र् (*r*)**. Sanskrit thus treats them as the vowel and consonant forms of closely related movements at the same place in the mouth.

The pyramid describes retroflexion as late, local, marginal, or borrowed. None of those labels explains why the retroflex position carries linked duties across Sanskrit's vowel system, consonant grid, atomic construction, and junction rules. The position bears substantial architectural load.

### 6. Contrast Across the Vowel

The audit contains 355 atoms built around a single अक्षर (*akṣara*), with a वर्ग (*varga*) consonant on both sides of the vowel. Only 35, or **9.9%**, use the same place of articulation on both sides. If the opening and closing places occurred independently, the expected share would be about **26.5%**. The atoms therefore favor a change of place across the vowel. A *kak*-style repetition occurs much less often than the distribution of the individual sounds would predict.[NOTE: dhatupatha-empirical-distribution]

Modern linguistics calls this kind of repeated-feature avoidance the **Obligatory Contour Principle (OCP)**. The Sanskrit result can be stated without the technical term: even inside a very small atom, the opening and closing consonants usually come from different places in the mouth.

### 7. गण (*Gaṇa*)-Specific Functional Matching

The ten गणाः (*gaṇāḥ*) have different sound profiles. The जुहोत्यादि (*juhotyādi*) class, which uses reduplication, contains an unusually high share of voiced aspirates. The inventory share is 33.3 percent, and the share rises to 42.9 percent when the count is limited to entries recorded in Path C.[NOTE: cross-gana-column-distribution]

The association is clear, but the count does not by itself establish the reason. The book proposes an architectural explanation: reduplication repeats material inside a verbal form, and the fourth column gives that repeated material a strong acoustic signature.

### 8. Generative Reach From Minimum

Path A and Path C calculate two different kinds of reach. Path A estimates the number of primary derivatives generated by each atom; this is its **generative reach**. Path C counts the combinations in which each atom appears across the corpus; this is its **combinatorial reach**. As particle count rises, both forms of reach tend to fall. Smaller atoms therefore tend to generate more derivatives and appear in more recorded combinations.

English places irregular forms such as *be*, *have*, and *do* among its most frequent verbs; Latin and Greek offer comparable examples. The current audit examines a different Sanskrit relation: the atoms with the greatest generative reach are concentrated among the smaller forms. A complete comparison of paradigm irregularity would require a separate audit, but the observed concentration already shows that Sanskrit keeps many of its busiest atoms compact and reusable.[NOTE: generative-reach-inversion-natural-language]

---

## 6.3 How Far Compact Atoms Reach

The eighth principle requires a closer examination. If Sanskrit keeps its most reusable atoms compact, smaller atoms should generate larger word families and enter more grammatical combinations. The dictionary and corpus records test those two expectations separately.

| Particles | n | Mean generative reach | Median | Max |
|---:|---:|---:|---:|---:|
| 1 | 1 | 30.0 | 30.0 | 30 |
| 2 | 26 | **30.1** | 30.0 | 75 |
| 3 | 72 | 20.5 | 18.0 | 55 |
| 4 | 31 | 13.5 | 12.0 | 30 |
| 5 | 8 | 11.4 | 12.0 | 18 |

The table contains all 138 atoms in the selected Path A sample. The mean falls from 30.1 derivatives among two-particle atoms to 11.4 among five-particle atoms. Spearman's rank correlation summarizes that direction: a negative value means that larger particle counts tend to accompany lower generative reach. Path A gives ρ = **−0.485**.

Path C uses a different calculation and a much larger set. It counts the distinct prefix-and-form-class combinations recorded for each of 3,839 normalized DCS verb lemmas. Its correlation between particle count and combinatorial valency is also negative, at ρ = **−0.4334**. The dictionary sample and the corpus analysis therefore point in the same direction.

The high-reach group contains familiar compact atoms: कृ (*kṛ*), भू (*bhū*), दा (*dā*), धा (*dhā*), हृ (*hṛ*), गम् (*gam*), स्था (*sthā*), and ज्ञा (*jñā*). Across the sample, smaller atoms produce larger word families on average.

The botanical metaphor cannot explain this recurring relation. The dictionary sample and the corpus audit count different forms of reach, yet both associate compact atoms with wider use. The book identifies that pattern as compression designed for controlled expansion.

### Two Records Identify the Same High-Reach Atoms

Path A and Path C calculate different kinds of reach. The dictionary sample counts how many words lexicographers connect with a selected धातुः (*dhātuḥ*). The corpus audit counts how many combinations of prefix and grammatical form-class actually occur with that atom in the parsed texts.[NOTE: dictionary-audit-sources][NOTE: prayoga-audit-valency]

The two measurements agree often enough to identify the same high-reach center. Across the atoms found in both records, their correlation is **+0.66**. A result of +1.00 would mean that their rankings matched perfectly. A result close to zero would mean that one record provided no indication of the other. The observed result shows substantial agreement without pretending that a dictionary and a corpus count the same thing.

The corpus gives the following recorded combination counts for five familiar atoms:

| धातुः (*Dhātuḥ*) | **⟪कृ⟫ (*kṛ*)** | **⟪भू⟫ (*bhū*)** | **⟪धा⟫ (*dhā*)** | **⟪हृ⟫ (*hṛ*)** | **⟪गम्⟫ (*gam*)** |
|:--|--:|--:|--:|--:|--:|
| Recorded combinations | 1,062 | 504 | 386 | 368 | 291 |

The 1,062 combinations beside ⟪कृ⟫ do not assign greater importance to its meaning. The number records how many combinations of prefix and grammatical form-class the corpus contains for forms built from that atom. A compact atom meaning *to do* or *to make* can participate in an unusually wide range of Sanskrit expression.

### Three Reach Tiers

The full corpus divides its 3,839 normalized verb lemmas into three broad tiers:

| Tier | Recorded combinations | Normalized verb lemmas | Share of recorded verb use |
|---|---:|---:|---:|
| High reach | 50+ | 147 (**3.8%**) | **67.6%** |
| Middle reach | 5–49 | 1,059 (**27.6%**) | **30.5%** |
| Specialist | 1–4 | 2,633 (**68.6%**) | **1.9%** |

![Reach tiers by verb-lemma share and recorded Sanskrit use.](figures/ganah/reactivity_tiers.svg){#fig:appendix-numbers-reactivity-tiers width=100%}

Only 147 lemmas belong to the high-reach tier, yet their forms account for more than two-thirds of the recorded verb use. The 2,633 specialist lemmas account for less than two percent.

The specialist tier is not unused or unnecessary. Its members record distinctions that occur less often. The corpus combines a compact core used repeatedly with a much larger inventory available for narrower meanings.

### The Same Core Across Four Corpora

The corpus audit also compares the **ऋग्वेद (*Ṛgveda*)**, the **अथर्ववेद (*Atharvaveda*) Śaunaka**, the **महाभारत (*Mahābhārata*)**, and the **रामायण (*Rāmāyaṇa*)**. The first two belong to श्रुति (*śruti*). The latter two belong to स्मृति (*smṛti*), specifically इतिहास (*itihāsa*). Their subjects and styles differ.

Nine reference atoms appear in every one of the four: **⟪कृ⟫ (*kṛ*)**, **⟪भू⟫ (*bhū*)**, **⟪स्था⟫ (*sthā*)**, **⟪गम्⟫ (*gam*)**, **⟪ज्ञा⟫ (*jñā*)**, **⟪दा⟫ (*dā*)**, **⟪धा⟫ (*dhā*)**, **⟪नी⟫ (*nī*)**, and **⟪हृ⟫ (*hṛ*)**.[NOTE: cross-corpus-invariance]

![Rank trajectories of nine high-reach धातवः (*dhātavaḥ*) across four Sanskrit corpora.](figures/ganah/canonical_rank_trajectory.svg){#fig:appendix-numbers-canonical-rank-trajectory width=100%}

The Vedic corpora give greater prominence to atoms suited to their subjects, while the epics distribute the same core through narrative action. Their exact rankings differ because the texts use language for different purposes. All nine remain in use across the four corpora. The comparison shows a compact core extending through both Vedic and लौकिक (*laukika*) expression; it does not claim that the four texts use that core in identical proportions.

---

## 6.4 How Atomic Shape Relates to Activation

The reach analysis counts how widely an atom extends. A second analysis asks how the atom's internal construction relates to the procedure that turns it into a completed verb. Chapter 11 demonstrates those procedures through Vedic verbs. The grammatical analysis preserved with the *Aṣṭādhyāyī* and धातुपाठ (*Dhātupāṭha*) groups धातवः (*dhātavaḥ*) that behave alike and states the operations associated with those groups.

The tradition teaches ten verbal **गणाः (*gaṇāḥ*)**. Each gathers धातवः (*dhātavaḥ*) that undergo a recurring operation before receiving the personal ending. Some take an inserted element. Some change internally. Some repeat part of the atom. The *Aṣṭādhyāyī* specifies these operations rule by rule, and later grammatical teaching commonly gathers the intervening elements under the term **विकरणम् (*vikaraṇam*)**.[NOTE: vikarana-as-column-signature]

The first figure groups five classes by four broad mechanisms: thematic activation, direct activation, reduplication, and infixation. The second presents five forms of suffixal extension.

![Four mechanisms and five activation classes, with their signatures and worked examples.](figures/building_kriya/gana_mechanisms_activation.svg){#fig:appendix-numbers-gana-mechanisms-activation width=100%}

![Five classes that append an element between the atom and its ending.](figures/building_kriya/gana_mechanisms_suffixal_extension.svg){#fig:appendix-numbers-gana-mechanisms-suffixal-extension width=100%}

The classification becomes numerically useful when it is compared with the रचना (*racanā*), the sonomeric construction of the atom. One axis records how the atom is built. The other records the activation group in which the grammatical tradition places it.

After instructional markers are removed, the 2,168-entry धातुपाठ (*Dhātupāṭha*) contains 47 observed रचना (*racanā*) scaffolds. The ten most frequent scaffolds contain 1,973 entries, or **91.01%** of the inventory. Of the 470 possible scaffold-by-class cells, 140 contain listed atoms.[NOTE: racana-gana-matrix]

![The ten most frequent रचनाः (*racanāḥ*) across the ten verbal classes.](figures/ganah/racana_gana_matrix.svg){#fig:appendix-numbers-racana-gana-matrix width=100%}

The filled and empty cells show that atomic construction and verbal activation are related without being identical. Some scaffolds occur across nearly every class. Others concentrate within a few operations. This analysis belongs in the technical appendix because it tests the classification numerically; the body chapter needs only the simpler conclusion that different atoms follow recurring activation patterns.

The periodic-axes figure tests a second arrangement. It places the धातवः (*dhātavaḥ*) recorded in the corpus by the वर्ग (*varga*) column of their first consonant and by their inherent vowel, then uses marker size and color to show combinatorial reach.[NOTE: varga-column-as-engineering-axis][NOTE: inherent-vowel-secondary-axis]

![धातवः (*Dhātavaḥ*) recorded in the corpus, arranged by initial वर्ग (*varga*) column and inherent vowel.](figures/ganah/periodic_table.svg){#fig:appendix-numbers-periodic-axes width=100%}

The figure uses chemical periodicity as an analytical analogy. It asks whether properties already present inside an atom help predict how widely that atom enters verbal combinations. The numerical results and replication files allow that interpretation to be tested independently.

---

## 6.5 What the Numbers Show

Several independent counts reveal the same organization. Sanskrit concentrates meaning in compact atoms. It places sounds differently at the opening and closing positions of those atoms. A small set of sounds performs most of the joining inside clusters. The activation groups also have different sound profiles. Finally, both the dictionary sample and the corpus analysis show greater reach among smaller atoms.

The inventory also contains a long tail of rare scaffolds and specialized shapes. That range is **वैचित्र्य (*vaicitrya*)**: structured variety around strong modal forms. The book's engineering claim rests on both features together, because a generative architecture needs compact defaults as well as specialized forms.

These patterns recur across the sound inventory, atomic construction, verbal activation, and recorded use. Together they provide the numerical evidence for the engineering demonstrated through words and sentences in Chapters 10, 11, and 12.

---

## 6.6 Replication

The *Source and Reference Companion* preserves the replication trail:

- the complete Path A tables from `analysis/dhatupatha/`;
- the complete Path C corpus audit from `analysis/ganah/`;
- the stripping-rule correction history;
- the questions tested, the data used, and the resulting conclusions;
- the जुहोत्यादि (*juhotyādi*) C4 correction from 31.8% to 33.3%, and the Path C sharpening to 42.9%;
- the complete script-to-output map for reproducing each table.

The code bundles are already organized for public audit. The structural baseline counts the listed धातुपाठ (*Dhātupāṭha*). Path A estimates generative reach from a selected dictionary sample. Path C counts combinatorial reach from forms recorded in the corpus. A future Path B can calculate the formal bonding space documented by the *Aṣṭādhyāyī* itself: what its rules make available beyond what dictionaries list or corpora preserve.

The printed book presents the result, while the companion preserves the audit trail for readers who want to rerun the tests. Across these analyses, the धातुपाठ (*Dhātupāṭha*) behaves as an atomic inventory organized for compression, distinction, and generative reach. The book identifies that recurring organization as engineering.
