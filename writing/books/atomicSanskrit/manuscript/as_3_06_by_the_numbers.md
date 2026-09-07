# Appendix Part 6 — The Architecture by the Numbers

Chapter 10 presents the धातुः (*dhātuḥ*) as an engineered semantic atom, and Chapter 11 shows that atom becoming a verb. This appendix tests the same architecture across the larger inventory. It examines the size and internal construction of the atoms, the positions their sounds occupy, the procedures that activate them, and the range of forms they generate.

No single number can establish engineering. The pattern must recur at several levels. The *Source and Reference Companion* preserves the complete tables, scripts, correction history, and replication instructions. The account here explains the method and presents the strongest results.

The audit uses three related datasets, and their totals count different things. The structural baseline contains 2,168 listed entries from a digital Pāṇinian **धातुपाठ (*Dhātupāṭha*)** across the ten **गणाः (*gaṇāḥ*)**. The citation markers called **अनुबन्धाः (*anubandhāḥ*)** are removed before the sounds of each listed atom are counted.

**Path A** uses the Monier-Williams and Apte dictionaries to compare particle count with estimated derivative counts for a selected sample of 138 atoms.

**Path C** examines the Digital Corpus of Sanskrit. Its parser produced 3,839 normalized verb lemmas, including causatives and other derived lemmas that do not appear as separate entries in the धातुपाठ (*Dhātupāṭha*). For each lemma, Path C counts the distinct combinations of prefix and grammatical form class recorded in the corpus.

The three totals therefore count different units: 2,168 listed धातुपाठ entries, a selected sample of 138 atoms, and 3,839 normalized corpus lemmas.[NOTE: dcs-vs-dhatupatha-count]

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

These rows account for all 2,168 listed entries. When the same entries are counted by अक्षर (*akṣara*), **98.2%** contain a single अक्षर (*akṣara*). Semantic force is concentrated into small, stable forms.

---

## 6.2 Eight Engineering Principles

Eight linked principles emerge from the counts. Each one describes a different part of the same architecture.

### 1. Cost and Distinguishability

The first वर्ग (*varga*) column, formed without voicing or aspiration, occurs most often. Greater physical effort does not by itself predict rarity, however. The voiced aspirates of the fourth column require greater articulatory effort than the voiceless aspirates of the second column, yet the fourth column occurs more often. Its combination of voicing and breath also gives it a stronger acoustic signature. The distribution therefore reflects both the effort required to produce a sound and the distinctions that listeners can hear.

The audit compares those two properties through a simple ratio: distinguishability divided by cost. Sounds with a higher ratio tend to occur more often, but the ratio explains only part of the distribution. Frequency also depends on the particular sound and its position inside the atom.

### 2. Cell-Level Allocation

Equal column value does not produce equal deployment. The labial nasal म् (*m*), for example, appears often, while the velar nasal ङ् (*ṅ*) is almost absent from the same inventory count. A column-level preference cannot explain that difference; the exact cell also affects how a sound is used.

The column identifies one property of a sound. The exact grid address identifies the complete bundle of properties that the atom can use.

### 3. Position-Conditional Preference

Position changes the physical action of a consonant. At the opening of an atom, the consonant releases into the vowel. At the end, it closes the atom and participates in later सन्धि (*sandhi*) operations. The counts reflect that difference.

Retroflex sounds occur less often before the vowel and much more often after it. Palatals also favor the closing side. Velars and labials show the opposite preference and appear more often before the vowel. The same consonant can therefore contribute differently when it opens an atom, closes it, or joins a cluster.

The following figure examines धातुपाठ (*Dhātupāṭha*) atoms built around a single अक्षर (*akṣara*) and one vowel. Each circle represents one consonant. Its position from left to right shows how often the consonant occurs before the vowel; its position from bottom to top shows how often it occurs after the vowel. The circle grows larger when the consonant appears more often inside a cluster. Colors group the consonants according to their place in the वर्णमाला (*varṇamālā*) and the mouth.

![Where consonants appear around the vowel in atoms built around a single अक्षर (*akṣara*).](figures/building_dhatuh/role_map_color.svg){#fig:appendix-numbers-dhatuh-role-map width=100%}

The dashed line marks equal use before and after the vowel. **क, व, प,** and **श** sit farther to the right because they occur more often before the vowel. **ष, ज, स, ट,** and **ड** sit higher because they occur more often after it.

### 4. Cluster-Joiner Specialization

Consonant clusters do not use every sound in the same way. Most of the joining is performed by a small class whose major members are the **अन्तःस्थाः (*antaḥsthāḥ*)**: य्, र्, ल्, व् (*y, r, l, v*). In the वर्णमाला (*varṇamālā*), these sounds stand between the stop rows and the **ऊष्माणः (*ūṣmāṇaḥ*)**. The count shows them performing a corresponding connecting role inside the atoms, with र् (*r*) doing so most often.

The largest circle belongs to **र् (*r*)**. It appears frequently on both sides of the vowel and joins more consonant clusters than any other sonomer in this count. **ल् (*l*)** appears less often and is distributed more evenly before and after the vowel. Together, the अन्तःस्थाः (*antaḥsthāḥ*) perform much of the joining inside Sanskrit's compact atoms.

### 5. मूर्धन्य (*Mūrdhanya*) Dual-Role Engineering

The **मूर्धन्य (*mūrdhanya*)** anatomical coordinate performs several important functions. Sounds made there appear frequently at the ends of atoms, join many consonant clusters, and participate in the ऋ (*ṛ*) / र् (*r*) relation. The usual story treats this position as marginal, but the counts place it near the center of Sanskrit's atomic construction.

The relationship between **ऋ (*ṛ*)** and **र् (*r*)** extends this pattern across the vowel and consonant systems. Sanskrit places both at the मूर्धन्य (*mūrdhanya*) position. **ऋ (*ṛ*)** can occupy the vowel-center of an अक्षर (*akṣara*), while **र् (*r*)** can connect with sounds on either side of that center. When **ऋ (*ṛ*)** appears before another vowel, ***यण्-सन्धि (*yaṇ-sandhi*)*** replaces it with **र् (*r*)**. Sanskrit thus treats them as the vowel and consonant forms of closely related movements at the same place in the mouth.

The pyramid describes retroflexion as late, local, marginal, or borrowed. None of those labels explains why the retroflex position carries linked duties across Sanskrit's vowel system, consonant grid, atomic construction, and junction rules. The position bears substantial architectural load.

### 6. Contrast Across the Vowel

The audit contains 355 atoms built around a single अक्षर (*akṣara*), with a वर्ग (*varga*) consonant on both sides of the vowel. Only 35, or **9.9%**, use the same place of articulation on both sides. If the opening and closing places occurred independently, the expected share would be about **26.5%**. The atoms therefore favor a change of place across the vowel. A *kak*-style repetition occurs much less often than the distribution of the individual sounds would predict.[NOTE: dhatupatha-empirical-distribution]

Modern linguistics calls this kind of repeated-feature avoidance the **Obligatory Contour Principle (OCP)**. The Sanskrit result can be stated without the technical term: even inside a very small atom, the opening and closing consonants usually come from different places in the mouth.

### 7. गण (*Gaṇa*)-Specific Functional Matching

The ten गणाः (*gaṇāḥ*) have different sound profiles. The जुहोत्यादि (*juhotyādi*) class, which uses reduplication, contains an unusually high share of voiced aspirates. The inventory share is 33.3 percent, and the share rises to 42.9 percent when the count is limited to entries recorded in Path C.[NOTE: cross-gana-column-distribution]

The association is clear, but the count does not by itself establish the reason. The book proposes an architectural explanation: reduplication repeats material inside a verbal form, and the fourth column gives that repeated material a strong acoustic signature.

### 8. Generative Reach From Minimum

Two independent audits test whether compact atoms have greater reach. Path A estimates the size of the derivative family generated by each atom. Path C counts the prefix-and-form-class combinations recorded for it in the corpus. Both forms of reach fall as particle count rises. Section 6.3 presents the results.

---

## 6.3 How Far Compact Atoms Reach

The dictionary sample and the corpus now test the eighth principle separately. If compactness supports reuse, smaller atoms should produce larger word families and enter more recorded combinations.

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

The dictionary sample and the corpus audit count different forms of reach, yet both associate compact atoms with wider use. A botanical account cannot explain why the most reusable parts of the inventory are also among its smallest. The book identifies this pattern as compression designed for controlled expansion.[NOTE: generative-reach-inversion-natural-language]

### Two Records Identify the Same High-Reach Atoms

Of the 138 atoms in Path A, 121 also appear in Path C.[NOTE: dictionary-audit-sources][NOTE: prayoga-audit-valency] Their rankings have a correlation of **+0.66**. A result of +1.00 would mean that the rankings matched perfectly; a result close to zero would mean that one record provided no indication of the other. The result shows substantial agreement between two different measurements.

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

The 2,633 specialist lemmas preserve distinctions that occur less often. The corpus therefore combines a compact core used repeatedly with a much larger inventory available for narrower meanings.

### The Same Core Across Four Corpora

The corpus audit also compares the **ऋग्वेद (*Ṛgveda*)**, the **अथर्ववेद (*Atharvaveda*) Śaunaka**, the **महाभारत (*Mahābhārata*)**, and the **रामायण (*Rāmāyaṇa*)**. The first two belong to श्रुति (*śruti*). The latter two belong to स्मृति (*smṛti*), specifically इतिहास (*itihāsa*). Their subjects and styles differ.

Nine reference atoms appear in every one of the four: **⟪कृ⟫ (*kṛ*)**, **⟪भू⟫ (*bhū*)**, **⟪स्था⟫ (*sthā*)**, **⟪गम्⟫ (*gam*)**, **⟪ज्ञा⟫ (*jñā*)**, **⟪दा⟫ (*dā*)**, **⟪धा⟫ (*dhā*)**, **⟪नी⟫ (*nī*)**, and **⟪हृ⟫ (*hṛ*)**.[NOTE: cross-corpus-invariance]

![Rank trajectories of nine high-reach धातवः (*dhātavaḥ*) across four Sanskrit corpora.](figures/ganah/canonical_rank_trajectory.svg){#fig:appendix-numbers-canonical-rank-trajectory width=100%}

The Vedic corpora give greater prominence to atoms suited to their subjects, while the epics distribute the same core through narrative action. Their exact rankings differ because the works use language for different purposes. All nine remain in use across the four corpora, carrying a compact core through both Vedic and लौकिक (*laukika*) expression.

---

## 6.4 How Atomic Shape Relates to Activation

The reach analysis counts how widely an atom extends. The next analysis compares the atom's internal construction with the procedure that turns it into a completed verb. Chapter 11 demonstrates those procedures through Vedic examples.

The grammatical tradition recorded in the *Aṣṭādhyāyī* and धातुपाठ (*Dhātupāṭha*) groups together धातवः (*dhātavaḥ*) that behave alike. It then states the operations associated with each group.

The tradition teaches ten verbal **गणाः (*gaṇāḥ*)**. Each gathers धातवः (*dhātavaḥ*) that undergo a recurring operation before receiving the personal ending. Some take an inserted element. Some change internally. Some repeat part of the atom. The *Aṣṭādhyāyī* specifies these operations rule by rule, and later grammatical teaching commonly gathers the intervening elements under the term **विकरणम् (*vikaraṇam*)**.[NOTE: vikarana-as-column-signature]

The first figure groups five classes by four broad mechanisms: thematic activation, direct activation, reduplication, and infixation. The second presents five forms of suffixal extension.

![Four mechanisms and five activation classes, with their signatures and worked examples.](figures/building_kriya/gana_mechanisms_activation.svg){#fig:appendix-numbers-gana-mechanisms-activation width=100%}

![Five classes that append an element between the atom and its ending.](figures/building_kriya/gana_mechanisms_suffixal_extension.svg){#fig:appendix-numbers-gana-mechanisms-suffixal-extension width=100%}

The classification becomes numerically useful when it is compared with the रचना (*racanā*), the sonomeric construction of the atom. One axis records how the atom is built. The other records the activation group in which the grammatical tradition places it.

After instructional markers are removed, the 2,168-entry धातुपाठ (*Dhātupāṭha*) contains 47 observed रचना (*racanā*) scaffolds. The ten most frequent scaffolds contain 1,973 entries, or **91.01%** of the inventory. Of the 470 possible scaffold-by-class cells, 140 contain listed atoms.[NOTE: racana-gana-matrix]

![The ten most frequent रचनाः (*racanāḥ*) across the ten verbal classes.](figures/ganah/racana_gana_matrix.svg){#fig:appendix-numbers-racana-gana-matrix width=100%}

The filled and empty cells show that an atom's construction affects how it becomes a verb, but does not determine the procedure by itself. Some scaffolds occur across nearly every class; others appear mainly within a few.

---

## 6.5 What the Numbers Show

The measurements converge on one organization. Sanskrit concentrates meaning in compact atoms, gives sounds different duties at different positions, and relies on a small group of sonomers for much of the joining inside clusters. Its activation groups have their own sound profiles. Both the dictionary sample and the corpus then show wider reach among smaller atoms.

Alongside that compact center stands a long tail of rare scaffolds and specialized shapes. This is **वैचित्र्य (*vaicitrya*)**: structured variety around strong recurring forms. The architecture combines economical defaults with the specialized atoms needed for narrower meanings.

The same engineering pattern therefore recurs across sound, atomic construction, verbal activation, and recorded use.

---

## 6.6 Replication

The *Source and Reference Companion* identifies the datasets and scripts behind every result in this appendix. It also preserves the correction history and the command sequence needed to reproduce each table. Readers can inspect the source data, rerun Path A against the dictionary sample, and rerun Path C against forms recorded in the corpus.

Across both paths, the धातुपाठ (*Dhātupāṭha*) behaves as an atomic inventory organized for compression, distinction, and generative reach. That recurring organization is the numerical signature of its engineering.
