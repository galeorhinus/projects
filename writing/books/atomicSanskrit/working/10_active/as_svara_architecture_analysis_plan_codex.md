# Svara Architecture Analysis Plan — Codex

**Status:** six research and deployment passes complete; Figures A, C, and F deployed  
**Created:** 2026-07-29  
**Primary manuscript destination:** Chapter 9, between the timing introduction and the sound-volume analysis  
**Technical destination:** dedicated source-and-evidence endnotes  
**Related chapters:** Chapters 8, 9, 15, and 16  
**Governing analytical framework:** [PASS — the Principle of Architectural Selection and Scope](as_pass_deployment_plan_codex.md)

This document remains separate from the PASS deployment plan because it owns the
phonetic and textual research. PASS supplies the common method: Contribution,
Load, Bounding Support, and Scope Judgment. The svara research must establish
the evidence before assigning any candidate Included, Restricted, Vaidika,
Lineage-Bounded, or Excluded scope.

## 1. Purpose

The manuscript analyzes the *varṇamālā* as an engineered consonant grid, but it
has not yet given the ***स्वराः (*svarāḥ*)*** the same attention. This project
will analyze Sanskrit's vowel architecture through the same questions used for
the consonants:

1. Which physically possible sounds receive reusable coordinates?
2. Which sounds remain outside the reusable inventory?
3. Which differences are encoded through vowel quality?
4. Which differences are generated through duration, pitch, nasality, or a
   specified operation?
5. What does Sanskrit gain by leaving some physically possible coordinates
   open?
6. How do the *vaidika* and *laukika* domains use the same vowel architecture
   under different permissions?

The central subject is selection. The analysis should show both what Sanskrit
includes and what it deliberately handles without creating another reusable
vowel coordinate.

**Execution record:** [Svara Architecture Evidence — Codex](as_svara_architecture_evidence_codex.md)

The evidence record completes the initial six research passes and the
three-way reconciliation of the Codex, Gemini, and Claude reports. It separates
verified findings from architectural inference, rejects unsupported physical
explanations, and records the remaining source gaps. Manuscript deployment is
the next stage.

### Evidence Order

The argument begins with the architecture itself:

1. the vowels and vowel operations already present in Vedic passages;
2. the relations among vowel quality, duration, pitch, and nasality;
3. the explanations preserved by the Prātiśākhyas and Śikṣā disciplines;
4. the contrast between the complete productive vowel system and physically
   possible sounds that receive no independent coordinate;
5. later documentation by the *vaiyākaraṇāḥ*, including Pāṇini, only where it
   helps name or verify an operation already in use.

Pāṇini is therefore evidence for the documentation of the architecture, not
the organizing figure of the analysis. The reader should be able to understand
the structural argument before any Pāṇinian rule appears.

### Existing Chapter 9 Material

The new movement must build on Chapter 9 rather than restating it:

- §§9.2–9.3 already establish the places of articulation and the relation
  between anatomy and the grid.
- §9.6 already introduces *mātrā*, pitch, and the familiar vowel list.
- §9.7 already shows the fourteen-vowel axis across the consonant grid.
- §9.8 already analyzes excluded consonant coordinates, **अ + अ → आ**, and
  *snap to grid*.

Before drafting, create a reuse map that identifies what each new section can
point back to, what must move, and what genuinely needs to be added. The same
explanation must not appear once in the consonant discussion and again in the
vowel discussion.

### Reconciled Additions

The research supplied two load-bearing examples that the first Codex pass did
not have:

1. The Mahābhāṣya explicitly reports half-*e* and half-*o* in the Sātyamugri
   and Rāṇāyanīya Sāmavedic lineages. These sounds therefore belong in the
   **Lineage-Bounded** PASS scope rather than being described as unknown to
   Sanskrit.
2. Ṛgveda 10.129 supplies three visible vowel-junction examples, including
   **न । असत् → नासद्**. The same hymn preserves pluta **आसी३त्**, which a
   normalized database had stripped from its export.

## 2. Starting Observation

The familiar vowel list is:

> **अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ**

At first glance, it appears to contain short-long pairs. A closer examination
reveals three different arrangements.

| Vowel family or quality | One *mātrā* | Two *mātrās* | Initial assessment |
|---|---:|---:|---|
| *ivarṇa* | इ | ई | paired |
| *uvarṇa* | उ | ऊ | paired |
| *ṛvarṇa* | ऋ | ॠ | paired; long member rare |
| *ḷvarṇa* | ऌ | Excluded | ॡ appears in the familiar teaching row, but no ordinary Vedic or *laukika* use was found |
| contracted *avarṇa* form | अ | Excluded | no independent long contracted counterpart |
| open *avarṇa* form | Excluded | आ | no independent short open counterpart |
| *e*-quality | half-**ए**: Lineage-Bounded | ए | no generally reusable one-*mātrā* member |
| *ai*-quality | Excluded | ऐ | no independent one-*mātrā* member |
| *o*-quality | half-**ओ**: Lineage-Bounded | ओ | no generally reusable one-*mātrā* member |
| *au*-quality | Excluded | औ | no independent one-*mātrā* member |

This is a provisional analytical table. It must not silently equate
traditional descriptions such as ***संवृत (*saṃvṛta*)*** and
***विवृत (*vivṛta*)*** with one fixed IPA value across every *śākhā*, region,
and period.

### 2.1 Fourteen Listed Forms, Nine Vowel Families

The fourteen familiar written forms are the reader's entry point:

> **अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ**

The internal analysis may organize them more accurately as nine vowel
families:

> **अ, इ, उ, ऋ, ऌ, ए, ऐ, ओ, औ**

Under this account, **आ, ई, ऊ,** and **ॠ** are the two-*mātrā* members of the
**अ, इ, उ,** and **ऋ** families. They do not create four additional vowel
qualities. The status of **ॡ** becomes a load-bearing research problem because
the traditional `18/12` account gives the **ऌ** family a one-*mātrā* and a
three-*mātrā* form but no ordinary two-*mātrā* member.

Each permitted duration can combine with:

- ***उदात्त (*udātta*)***, ***अनुदात्त (*anudātta*)***, or
  ***स्वरित (*svarita*)***;
- ***अनुनासिक (*anunāsika*)*** or
  ***अननुनासिक (*ananunāsika*)*** form.

Each permitted duration therefore has six forms:

> **3 pitch relations × 2 nasal states = 6**

The traditional count represented in the supplied teaching chart is:

| Vowel family | *Hrasva* | *Dīrgha* | *Pluta* | Total forms |
|---|---:|---:|---:|---:|
| अ | 6 | 6 | 6 | **18** |
| इ | 6 | 6 | 6 | **18** |
| उ | 6 | 6 | 6 | **18** |
| ऋ | 6 | 6 | 6 | **18** |
| ऌ | 6 | open | 6 | **12** |
| ए | open | 6 | 6 | **12** |
| ऐ | open | 6 | 6 | **12** |
| ओ | open | 6 | 6 | **12** |
| औ | open | 6 | 6 | **12** |

This yields **132 analytically recognized forms**:

> **4 × 18 + 5 × 12 = 132**

The number describes the analytical possibility space, not corpus frequency.
The inherited categories establish the components; *Atomic Sanskrit* supplies
the combined matrix and the total. Further passage-level research can
determine which combinations occur in received passages, which are generated
under stated conditions, and which are recognized to complete the analysis.

### 2.2 Two Layers in the Vowel Architecture

Claude's plan identifies a useful structural distinction that the evidence
program should test:

1. a simple-vowel layer organized around **अ, इ, उ, ऋ,** and **ऌ**;
2. a junction-vowel layer containing **ए, ऐ, ओ,** and **औ**.

The working internal terms are ***समानाक्षर (*samānākṣara*)*** and
***सन्ध्यक्षर (*sandhyakṣara*)***. Their exact definitions and source locations
must be verified before the body uses them as settled classifications.

The second layer should be presented through Sanskrit's own operations, not as
a historical claim that one sound evolved from another. The research must
establish:

- how the phonetic disciplines describe the simple vowels;
- how they describe the combined places ***कण्ठतालु (*kaṇṭhatālu*)*** for
  **ए/ऐ** and ***कण्ठोष्ठ (*kaṇṭhoṣṭha*)*** for **ओ/औ**;
- how *guṇa*, *vṛddhi*, and vowel junction generate these results;
- whether the familiar teaching equations accurately represent each operation
  or collapse distinct operations into one simplified diagram.

The last point is essential. **अ/आ + इ/ई → ए** and
**अ/आ + उ/ऊ → ओ** can illustrate one set of junction operations. The production
of **ऐ** and **औ** must be stated through the correct *vṛddhi* architecture,
not casually reduced to **आ + इ** and **आ + उ** unless an internal source
supports that formulation.

## 3. Terminology

The prose should not say that **इ developed from ई**, or that **ऋ is a
shortened ॠ**. That phrasing implies chronology.

Use:

- **इ and ई are the one-*mātrā* and two-*mātrā* members of *ivarṇa*.**
- **उ and ऊ are the one-*mātrā* and two-*mātrā* members of *uvarṇa*.**
- **ऋ and ॠ are the one-*mātrā* and two-*mātrā* members of *ṛvarṇa*.**
- **ऌ is the one-*mātrā* member of *ḷvarṇa*. The regular 18/12 analysis leaves
  its two-*mātrā* position open; the exact status and history of the teaching
  symbol ॡ require separate explanation.**

The phrase *missing vowel* is also imprecise. The sound may be physically
possible even though Sanskrit gives it no independent reusable coordinate.
Prefer:

- **excluded coordinate**
- **unselected coordinate**
- **physically possible sound outside the reusable vowel inventory**
- **a sound handled through another operation**

## 4. Four Independent Dimensions

The analysis must keep four dimensions separate.

### 4.1 Vowel Quality

The base vowel identifies the mouth configuration and acoustic family:
*avarṇa, ivarṇa, uvarṇa, ṛvarṇa, ḷvarṇa,* and the *sandhyakṣarāṇi*.

### 4.2 Duration

Traditional analysis distinguishes:

- ***ह्रस्व (*hrasva*)*** — one *mātrā*
- ***दीर्घ (*dīrgha*)*** — two *mātrās*
- ***प्लुत (*pluta*)*** — three *mātrās*

Duration should not be confused with vowel quality. The **अ–आ** relation is the
load-bearing test because the two sounds may differ in mouth configuration as
well as duration.

### 4.3 Pitch

Vedic recitation preserves:

- ***उदात्त (*udātta*)***
- ***अनुदात्त (*anudātta*)***
- ***स्वरित (*svarita*)***

Research must distinguish independent and dependent *svarita*, the treatment
of *pluta*, and any *śākhā*-specific pitch systems relevant to the argument.
Pitch expands the information borne by a vowel; it does not automatically
create another vowel coordinate.

### 4.4 Nasality

The analysis must distinguish oral and ***अनुनासिक (*anunāsika*)***
forms. Traditional statements that one taught vowel represents several
variants may combine quantity, pitch, and nasality. Those counts must be
reconstructed carefully rather than repeated without showing their axes.

## 5. The अ–आ Problem

This is the strongest starting point.

Traditional phonetic analysis describes short **अ** as
***संवृत (*saṃvṛta*)*** and **आ** as ***विवृत (*vivṛta*)***. If this
description applies to the actual spoken outputs, **आ** is not merely **अ held
for a second *mātrā***.

The Vedic language already uses them as one *avarṇa* family where a junction
operation requires ***सवर्णता (*savarṇatā*)***:

> **अ + अ → आ**

The investigation must proceed in this order:

1. find exact Vedic examples in which **अ + अ → आ**;
2. establish how the Prātiśākhyas and Śikṣā texts describe **अ**, **आ**,
   *saṃvṛta*, *vivṛta*, duration, and junction;
3. determine how the architecture can treat the two sounds as one functional
   family while preserving their different spoken forms;
4. use the *vaiyākaraṇa* documentation, including **तुल्यास्यप्रयत्नं
   सवर्णम्**, **अकः सवर्णे दीर्घः**, and the final **अ अ**, as later
   confirmation of the already operating relation;
5. use the Kāśikā, Mahābhāṣya, Siddhāntakaumudī,
   Laghu-Siddhāntakaumudī, and later explanations to record how the
   documentation lineage understood that relation.

### 5.1 Questions to Establish

- Exactly which internal source first states that short **अ** is *saṃvṛta*
  while **आ** is *vivṛta*?
- Does the description apply across the Vedic phonetic disciplines or only in
  specified analytical lineages?
- How do the Vedic phonetic disciplines reconcile the *saṃvṛta–vivṛta*
  difference with the Vedic **अ + अ → आ** operation?
- How does the later *vaiyākaraṇa* documentation represent that relation, and
  how do its principal commentaries explain **अ अ**?
- Which IPA approximations are defensible for the relevant recitational
  lineages?
- Is a sustained contracted vowel physically difficult, acoustically weak, or
  merely unnecessary within Sanskrit's architecture?

### 5.2 Architectural Hypothesis

Sanskrit may be separating the physical sound from the coordinate needed by
the language engine:

- the mouth produces a contracted short **अ**;
- the architecture groups **अ** with open **आ** where an operation requires one
  *avarṇa* family;
- the spoken output restores the distinction.

The selected pair leaves two inverse possibilities open:

- a two-*mātrā saṃvṛta avarṇa* that sustains the contracted quality of **अ**;
- a one-*mātrā vivṛta avarṇa* that preserves the open quality associated with
  **आ** while remaining short.

The second possibility should not be called "short **आ**." **आ** names the
selected two-*mātrā* member. The open position is a one-*mātrā vivṛta avarṇa*
that Sanskrit does not assign an independent reusable symbol.

This would provide another example of *snap to grid*. The hypothesis must be
presented as an architectural reading of Sanskrit's documented operations. No
later documenter should be made the source of the design.

## 6. The ए–ऐ–ओ–औ Problem

Sanskrit assigns no independent one-*mātrā* counterparts to **ए, ऐ, ओ,** or
**औ**.

When an *ec* vowel requires a short substitute, Sanskrit uses an *ik* vowel:

- **ए / ऐ → इ**
- **ओ / औ → उ**

The analysis should first establish this architecture through Vedic usage,
phonetic description, *guṇa*, *vṛddhi*, and junction operations. Pāṇini later
documents the shortening relation as **एच इग्घ्रस्वादेशे**, Aṣṭādhyāyī
1.1.48.

The analysis should connect the operation with:

1. the classification of **ए, ऐ, ओ, औ** as
   ***सन्ध्यक्षराणि (*sandhyakṣarāṇi*)***;
2. their places of articulation;
3. ***गुण (*guṇa*)*** and ***वृद्धि (*vṛddhi*)*** operations;
4. their fixed two-*mātrā* status in ordinary Sanskrit analysis;
5. Vedic recitational forms and any specified shortening;
6. the decision to redirect shortening toward **इ** or **उ** rather than
   creating short **ए, ऐ, ओ,** or **औ**.

### 6.1 Architectural Hypothesis

The architecture may treat these vowels as generated junction results rather
than simple vowels needing complete short-long rows. When shortening is
required, Sanskrit returns to the nearest simple reusable coordinate.

This may demonstrate economy without loss of function: four physically
possible short coordinates remain open because existing simple vowels already
perform the required grammatical work.

Short **e** and **o** occur in other languages, including languages already
used in the manuscript's subcontinental sound-field comparison. Their
pronounceability therefore cannot explain their absence from Sanskrit's
reusable inventory. The research must instead compare the contribution of
those coordinates with the architectural load they would add.

### 6.2 One Source, Different Operations

The vowel and consonant sides of the *varṇamālā* meet most clearly around the
***इक् (*ik*)*** vowels:

- before another vowel, **इ, उ, ऋ,** and **ऌ** can yield the corresponding
  ***यण् (*yaṇ*)*** sounds **य, व, र,** and **ल**;
- in other operations, **इ/ई** and **उ/ऊ** participate in the architecture
  that yields **ए/ऐ** and **ओ/औ**.

This is a promising unification, but it is not a four-way symmetry. **ऋ** and
**ऌ** do not produce a parallel pair of junction vowels corresponding to
**ए/ऐ** and **ओ/औ**. Their *guṇa* and *vṛddhi* results must be shown accurately
as **अर्/आर्** and **अल्/आल्**, where applicable.

The body can therefore place a secure pair side by side:

> **इ + अ → य**  
> **अ/आ + इ/ई → ए**

and then explain that Sanskrit assigns different operations according to
position and scope. The larger claim should be that the vowel-consonant
boundary is operational, not that all four *ik* vowels produce identical
two-sided families.

## 7. The ऌ–ॡ Boundary Case

The status of **ॡ** must be handled carefully.

Research must establish:

- whether **ॡ** occurs in any received Vedic passage;
- whether it occurs in any ordinary Sanskrit lexeme;
- whether it appears only as a formally required long counterpart;
- how Vedic passages, the Prātiśākhyas, and the Śikṣā texts treat it;
- how the later *vaiyākaraṇa* and commentarial lineages document it;
- whether its inclusion demonstrates inventory symmetry, operational
  completeness, or an actual productive sound.

If **ॡ** is formally recognized without ordinary lexical use, it may provide an
important control. Sanskrit can recognize a coordinate conceptually without
deploying it freely. That would complicate any simple claim that every listed
vowel was selected because the surrounding speech field used it frequently.

## 8. Vedic Pitch and the Vowel Matrix

The Vedic pitch system should receive its own analysis rather than being added
as a footnote to vowel length.

### 8.1 Questions

- Which vowels can receive each of the three principal pitch relations?
- How do pitch and duration combine?
- How does *svarita* alter the realized pitch contour of a short, long, or
  *pluta* vowel?
- Does pitch ever preserve a distinction that would otherwise collide?
- Which grammatical relations are carried or clarified by pitch?
- How do the different *śākhās* realize and notate pitch?
- Which parts of the pitch system belong to Sanskrit-wide architecture, and
  which belong to a particular received passage or lineage?

### 8.2 Working Conclusion

Pitch is probably not the reason short **ए** or long contracted **अ** failed to
become independent vowels. It is an orthogonal information layer. Its
importance may lie elsewhere: Sanskrit keeps the base vowel inventory compact
while Vedic pitch, duration, and nasality multiply the acoustic information
that each selected vowel can bear.

## 9. The Coordinate Test for a Svara

Chapter 9 already asks what a consonant must do before it earns a sonomeric
coordinate. This project should develop a parallel test for vowels.

A candidate vowel coordinate should be tested for:

1. **Articulatory identity:** Can the mouth produce it consistently?
2. **Acoustic distinguishability:** Can listeners reliably distinguish it from
   neighboring vowels?
3. **Molecular productivity:** Can it combine with consonants across the
   reusable sonomer grid?
4. **Grammatical function:** Does it add a distinction that Sanskrit needs?
5. **Operational necessity:** Can an existing vowel or specified operation
   perform the same work?
6. **Domain suitability:** Does the sound belong in unrestricted *laukika*
   generation, a specified Sanskrit-wide operation, or only a fixed Vedic
   passage?
7. **Entropy cost:** Would another coordinate improve expression or merely
   create avoidable overlap?

This test remains provisional until the internal phonetic sources show which
questions the Hindu analytical continuum itself asked.

### 9.1 Candidate Reasons for an Excluded Coordinate

Claude's three-part classification is useful as a research device, but its
causal claims are not yet established. Test each excluded coordinate against these
three possible explanations:

1. **Existing coordinate:** Sanskrit already handles the required sound or
   function through a neighboring coordinate, so a new one would add load
   without adding enough expressive range.
2. **Generated result:** the sound belongs to a specified operation whose output
   already has a defined quality and duration. A separate reusable coordinate
   might duplicate or collide with that output.
3. **Shared functional family:** the architecture groups distinct spoken
   forms into one operational family, as the **अ/आ** investigation may
   establish.

These are candidate explanations, not three conclusions that every open vowel
must fit. PASS will supply the final Contribution, Load, Bounding Support, and
Scope Judgment for each case.

## 10. Evidence Program

### Pass 1 — Internal Inventory

Create a source table for each of the nine vowel families and map the fourteen
familiar written forms onto it. Record:

- Devanāgarī
- IAST
- traditional family
- *sthāna*
- internal *prayatna*
- one-, two-, and three-*mātrā* forms
- oral and nasal forms
- pitch forms
- Vedic examples
- laukika examples
- grammatical operations
- source and exact section

For each family, calculate and verify:

- permitted duration classes;
- the six pitch-and-nasality forms within each permitted duration;
- the traditional total of eighteen or twelve;
- actual examples from received passages;
- whether a cell is found, condition-generated, analytically recognized, excluded, or still
  unverified.

### Pass 2 — अ–आ Structural Audit

Begin with:

- exact Vedic instances of **अ + अ → आ**;
- relevant Prātiśākhya and Śikṣā passages
- descriptions of *saṃvṛta*, *vivṛta*, *hrasva*, and *dīrgha*;
- evidence for how the sound is actually transmitted.

After the structural account is clear, collect the later documentation:
Aṣṭādhyāyī 1.1.9, 6.1.101, and 8.4.68; relevant Vārttikas and Mahābhāṣya
passages; and the principal commentaries. Separate what each source states from
later interpretation.

### Pass 3 — Sandhyakṣara Audit

Analyze **ए, ऐ, ओ, औ** through:

- exact Vedic forms and junctions
- Prātiśākhya and Śikṣā descriptions
- the source and exact meaning of *samānākṣara* and *sandhyakṣara*
- the source for *kaṇṭhatālu* and *kaṇṭhoṣṭha*
- *guṇa* and *vṛddhi*
- *sandhi*
- shortening operations
- Vedic and laukika examples
- short **e/o** in Tamil, Telugu, Kannada, Prākrit, and any other relevant
  comparison language
- the paired operations **इ + अ → य** and **अ/आ + इ/ई → ए**
- the non-parallel treatment of **ऋ** and **ऌ**

Use Aṣṭādhyāyī 1.1.48 only after the architecture is visible, as the later
documentation of how Sanskrit handles shortening.

### Pass 4 — Pitch Matrix

Map vowel quality × duration × pitch × nasality. Mark:

- combinations recognized by the analytical system;
- combinations found in exact passages;
- combinations generated under stated conditions;
- combinations that are physically possible but unused;
- combinations whose status remains unknown.

This pass must also test, rather than assume:

- whether a *svarita* requires two *mātrās*;
- whether short **e/o** would create any special pitch difficulty;
- whether the *saṃvṛta/vivṛta* distinction has a documented error-detection
  function;
- whether pitch helps bound particular grammatical collisions while remaining
  independent of the vowel-quality inventory.

The default working position remains that pitch is an additional information
channel. It should not be used to explain an open vowel coordinate without
specific evidence.

### Pass 5 — Subcontinental Sound-Field Comparison

Compare the excluded coordinates with the same language groups already used in
Chapter 8:

- Tamil
- Telugu
- Kannada
- Korku
- Mundari
- Ho

The comparison must use native vocabulary and secure phoneme inventories.
Urban pronunciation of borrowed English words cannot establish the inherited
sound field.

Questions:

- Do these languages use a phonemic long central or contracted vowel?
- Do they distinguish short open **a** from long open **ā**?
- Do they use phonemic short **e** and **o**?
- If they do, why did Sanskrit leave those coordinates open?
- Does Sanskrit's selection follow the field, or does grammatical economy
  override field frequency?

### Pass 6 — Architectural Analysis

For each excluded coordinate, compare competing explanations:

1. insufficient acoustic distinguishability;
2. no independent grammatical function;
3. an existing vowel already performs the work;
4. a specified operation generates the sound when needed;
5. the candidate cannot combine productively across the complete grid;
6. the sound belongs only to a fixed or lineage-restricted Vedic setting;
7. the additional coordinate would raise entropy without adding useful range.

### Pass 7 — Manuscript Deployment

Write the body explanation in classroom prose:

1. show the familiar vowel list;
2. show the simple-vowel and junction-vowel layers;
3. reorganize the inventory by quality and duration;
4. let the reader see the excluded coordinates;
5. explain **अ–आ**;
6. explain **ए–ऐ–ओ–औ** through their actual operations;
7. place **इ + अ → य** beside **अ/आ + इ/ई → ए**;
8. add pitch, duration, and nasality as separate dimensions;
9. apply PASS to each Included, Restricted, Vaidika, Lineage-Bounded, or
   Excluded coordinate;
10. close with the engineering revealed by selection and scope.

Technical disputes, source variants, IPA qualifications, and corpus counts
belong in endnotes or the appendix.

## 11. Proposed Figures

### Figure A — The Svara Form Matrix

**Primary placement:** Chapter 9  
**Status:** deployed as `figures/mapping_mouth/svara_form_matrix.svg`  

The figure should make the derivation of **132** visible without requiring the
reader to reconstruct the arithmetic from prose.

Use nine rows for the vowel families:

> **अ, इ, उ, ऋ, ऌ, ए, ऐ, ओ, औ**

Use nine principal columns arranged as three groups:

- one *mātrā* × three pitch relations;
- two *mātrās* × three pitch relations;
- three *mātrās* × three pitch relations.

Within each duration group, label the three columns:

- ***उदात्त (*udātta*)***
- ***अनुदात्त (*anudātta*)***
- ***स्वरित (*svarita*)***

Split every cell into two equal halves:

- oral, or ***अननुनासिक (*ananunāsika*)***;
- nasal, or ***अनुनासिक (*anunāsika*)***.

This produces **162 visible half-cells**:

> **9 vowel families × 9 duration-and-pitch columns × 2 nasal states = 162**

Mark **132 half-cells as selected analytical forms**. Leave thirty
half-cells visibly Excluded:

- the two-*mātrā* position of **ऌ** removes
  **1 family × 3 pitches × 2 nasal states = 6**;
- the one-*mātrā* positions of **ए, ऐ, ओ,** and **औ** remove
  **4 families × 3 pitches × 2 nasal states = 24**;
- **6 + 24 = 30 Excluded**;
- **162 − 30 = 132 selected analytical forms**.

Use the following visual treatment:

- selected half-cells use the figure's ordinary fill;
- Excluded half-cells remain unfilled and receive a restrained diagonal mark;
- the complete three-*mātrā* column group uses a subtle pattern or border to
  identify *pluta* as Restricted;
- half-**ए** and half-**ओ** appear in a separate side callout marked
  Lineage-Bounded because they are preserved by named Sāmavedic lineages but
  do not enter the regular 132-form matrix.

Print **18** at the end of the **अ, इ, उ,** and **ऋ** rows. Print **12** at
the end of the **ऌ, ए, ऐ, ओ,** and **औ** rows. Add a final arithmetic band:

> **162 possible positions − 30 Excluded = 132 selected forms**

Checked or filled cells mean **analytically selected**, not “found in a
surviving passage.” Passage-level evidence and unresolved corpus coverage
belong in the endnote rather than in this figure.

### Figure B — Four Dimensions of a Vowel

**Status:** Figure wishlist; non-blocking  

Start with one vowel coordinate and show four independent controls:

- quality
- duration
- pitch
- nasality

This figure should prevent readers from treating every audible difference as a
new vowel.

### Figure C — Selected and Excluded Vowel Forms

**Primary placement:** Chapter 9 §9.10  
**Status:** deployed as `figures/mapping_mouth/svara_selected_excluded_forms.svg`

Show:

- spoken short **अ** as *saṃvṛta*;
- spoken long **आ** as *vivṛta*;
- the Excluded two-*mātrā saṃvṛta* position;
- the Excluded one-*mātrā vivṛta* position;
- the generally Excluded one-*mātrā* **ए** and **ओ** positions;
- the selected two-*mātrā* **ए** and **ओ** forms;
- the Lineage-Bounded half-**ए** and half-**ओ** as a separate callout.

The adjacent prose supplies the functional alignment of **अ/आ** as one
*savarṇa* family, **अ + अ → आ**, and the later *vaiyākaraṇa* explanation.

### Figure D — Shortening Without New Coordinates

**Status:** Figure wishlist; non-blocking  

Show:

- **ए / ऐ → इ**
- **ओ / औ → उ**

Explain the structural decision first: the architecture redirects shortening
instead of creating four short *sandhyakṣara* coordinates. A small source note
may state that Pāṇini later documented this operation in Aṣṭādhyāyī 1.1.48.

### Figure E — One Source, Different Operations

**Status:** Figure wishlist; non-blocking  

Use a small paired diagram:

- **इ + अ → य** on the consonant or glide side;
- **अ/आ + इ/ई → ए** on the junction-vowel side.

The figure should explain position and operation without claiming a complete
four-vowel symmetry. A technical note can add the corresponding **उ/व/ओ**
relation and the different **ऋ/ऌ** outputs.

### Figure F — One Svara Architecture, Two Domains

**Primary placement:** Chapter 16  
**Status:** deployed as `figures/vaidika_laukika/svara_two_domains.svg`  
**Relationship to Figure A:** use the same visual vocabulary, but do not repeat
the complete 162-position matrix.

Figure A explains how the 132 analytical forms arise. Figure F explains
how the two Sanskrit domains use the shared svara architecture under different
permissions. Keeping these purposes separate prevents the arithmetic figure
from becoming overloaded with domain information.

Organize Figure F around five feature-level scope judgments:

| Feature | Vaidika | Laukika | Scope |
|---|:---:|:---:|---|
| Ordinary vowel-family and duration core | ✓ | ✓ | Shared |
| Vedic pitch layer | ✓ |  | Vaidika |
| Exact lineage-preserved form | ✓ |  | Lineage-Bounded |
| New composition through the shared sound system |  | ✓ | Laukika |
| *Pluta* under stated conditions | ◐ | ◐ | Restricted |

The table is a design skeleton rather than final figure copy. The finished
illustration should make three points visible:

1. The domains share the ordinary vowel-family and duration architecture.
2. The *vaidika* domain adds pitch, exact received form, and
   lineage-preserved forms.
3. The *laukika* domain adds permission to use the shared architecture in new
   composition; it does not require a separate vowel inventory.

Use three check treatments only at the feature level:

- **Vaidika only**
- **Laukika only**
- **Vaidika and Laukika**

Use a separate half-check or patterned mark for **Restricted** features.
Lineage-Bounded features should receive a small lineage marker rather than
being presented as Vaidika-wide.

The figure should not classify all 132 forms as Vaidika-only,
Laukika-only, or shared. Pitch, duration, nasality, lineage, and compositional
permission do not divide along identical domain boundaries. Figure F therefore
shows the domain allocation of architectural features rather than assigning a
domain check to every acoustic half-cell.

Suggested title:

> **One Svara Architecture, Two Domains**

Suggested subtitle:

> *How Vaidika preservation and Laukika composition use the same vowel system*

## 12. Manuscript Placement

### Preferred Body Location

Chapter 9 should contain the core analysis because that chapter already
explains how a sound earns a reusable coordinate. The consonant and vowel
analyses would then support one conclusion: Sanskrit's engineering appears in
selection as much as in inventory.

Proposed Chapter 9 structure:

1. retain the existing consonant-coordinate test in §9.8;
2. add **§9.9 The Svaras Are Built, Not Listed**;
3. add **§9.10 Three Ways a Vowel Coordinate Is Excluded**;
4. add **§9.11 Where the Garland Unfolds**;
5. let the current **Engineered Margin** become the joint conclusion for the
   consonant and vowel selections;
6. renumber the current §§9.9–9.11 as §§9.12–9.14;
7. update every affected pointer in the same manuscript change.

The three-section structure is provisional until the evidence review shows
that each section has enough reader-facing substance. If the evidence supports
only one or two movements, combine them rather than padding the chapter.

### Chapter 15 Callback

Chapter 15 can refer back to the pitch-duration-nasality matrix when explaining
how exact recitation preserves more information than unaccented writing.

### Chapter 16 Callback

Chapter 16 can use the vowel analysis as another example of different
permissions:

- the *laukika* domain receives a compact reusable vowel inventory;
- the *vaidika* domain preserves pitch, duration, nasality, and
  lineage-restricted forms at their fixed positions.

## 13. Guardrails

1. Do not organize the structural analysis around Pāṇini.
2. Do not describe Pāṇini as creating, correcting, completing, or improving the
   vowel architecture.
3. Establish the operation in the Vedas and the phonetic disciplines before
   introducing later *vaiyākaraṇa* documentation.
4. Do not turn stylistic or *śākhā*-specific variation into chronology.
5. Do not equate one traditional phonetic term with one universal IPA symbol
   without evidence.
6. Do not call an unselected coordinate anatomically impossible.
7. Do not claim that pitch caused the excluded coordinates unless a source or a
   complete architectural argument establishes that relation.
8. Do not call **अ + अ → आ** literal acoustic addition. It is an architectural
   operation that requires explanation.
9. Keep script, sound, coordinate, grammatical family, and recitational output
   separate.
10. Preserve unresolved evidence as unresolved.
11. Present architectural purpose as this book's inference unless an internal
    source states the purpose directly.

## 14. Inputs from Other Research Passes

### Gemini

**Current file:** `as_pass_deployment_plan_gemini.md`

Useful leads:

- treat the absent short **e/o** and the **अ/आ** asymmetry as architectural
  problems rather than accidents;
- test whether mouth geometry adds a second distinction beyond duration;
- test interactions among vowel quality, duration, and pitch.

Claims retained only as hypotheses:

- short **e/o** cannot be physically produced in one *mātrā*;
- a *svarita* requires two *mātrās*;
- the absence of short **e/o** prevents vocal-tract overload;
- the *saṃvṛta/vivṛta* distinction was explicitly designed as an
  error-correction device.

Other languages produce short **e/o**, so physical impossibility cannot carry
the argument. The pitch claims also require exact internal evidence before
they enter either body prose or endnotes.

### Claude

**Current file:** `as_svara_architecture_analysis_plan_claude.md`

Adopted into this plan:

- audit and reuse the existing Chapter 9 material;
- test the simple-vowel and junction-vowel layers;
- verify the combined place descriptions for **ए/ऐ** and **ओ/औ**;
- organize the body as three connected movements in §§9.9–9.11;
- use a paired **इ + अ → य / अ/आ + इ/ई → ए** diagram;
- keep pitch and nasality separate from the vowel-quality explanation;
- place source-heavy documentation in endnotes;
- perform a complete cross-reference sweep after renumbering.

Qualified or corrected:

- the generation of **ऐ/औ** must use the correct *vṛddhi* account;
- **ऋ/ऌ** do not complete the same compound-vowel symmetry as **इ/उ**;
- **ॡ** must not be called a phantom or symmetry-only coordinate before the
  corpus and internal-source audit establishes its status;
- the proposed three causes of an excluded coordinate remain analytical
  hypotheses until the evidence program verifies them.

### Codex

**Current file:** `as_svara_architecture_analysis_plan_codex.md`

Codex will compare all three records, classify agreements and conflicts,
verify load-bearing claims, and produce a consolidated evidence plan before
any manuscript prose changes.

## 15. Required Deliverables

- [x] Exact internal-source table for all fourteen listed vowels. The evidence
      pass establishes that the fourteen-character teaching row is not
      identical to the regular internal duration inventory; **ॡ** is retained
      as a formal teaching completion whose ordinary textual use remains
      unverified.
- [x] Nine-family map connecting the fourteen familiar written forms to
      duration, pitch, and nasality.
- [x] Internal sources for every component of the `18/12` classification.
      *Atomic Sanskrit* combines those established components and introduces
      the complete **132-form matrix** as its own analytical synthesis.
- [~] Cell-level status matrix distinguishing passage evidence, condition-generated
      form, analytical recognition, excluded coordinates, and unresolved
      combinations. The analytical matrix is complete; passage-level coverage
      remains incomplete.
- [~] Source-backed account of *saṃvṛta* **अ** and *vivṛta* **आ**. The
      commentarial account is secure; the earliest phonetic-discipline source
      remains open.
- [x] Vedic and phonetic-discipline account of the **अ–आ** architecture.
      Ṛgveda 10.129.1 supplies **न । असत् → नासद्**, with two further
      junctions in the same hymn.
- [x] Vedic and phonetic-discipline account of the **ए–ऐ–ओ–औ** architecture.
      The operations and classifications are secure, and the Mahābhāṣya
      supplies the bounded half-*e/half-o* evidence.
- [x] Short supporting note on the later *vaiyākaraṇa* documentation.
- [x] Status report for **ॠ, ऌ,** and **ॡ**.
- [x] Complete analytical pitch × duration × nasality matrix.
- [x] Vedic examples for the important combinations needed by the body.
- [x] Subcontinental screening comparison using the existing Chapter 8
      language set.
- [x] Tested explanations for every excluded coordinate.
- [x] Body figure plan.
- [x] Technical appendix or endnote plan.
- [x] Chapter 9 deployment proposal.
- [x] Chapter 9 reuse and deduplication map.
- [x] Verified definitions and sources for *samānākṣara*,
      *sandhyakṣara*, *kaṇṭhatālu*, and *kaṇṭhoṣṭha*, with lineage
      qualifications.
- [x] Correct operation map for *guṇa*, *vṛddhi*, vowel junction, and *yaṇ*.
- [x] Explicit disposition of the Gemini pitch and physical-impossibility
      hypotheses.
- [x] Complete cross-reference map for the Chapter 9 renumbering.
- [x] Chapter 15 and Chapter 16 callbacks.
- [x] Lost and Found record for displaced prose.

## 16. Six-Pass Deployment Sequence

- [x] **Pass 1 — Reconcile evidence.** Compare the Codex, Gemini, and Claude
      records; resolve conflicts; preserve source limitations.
- [x] **Pass 2 — Correct the research record.** Add the half-*e/half-o*
      evidence, restore the documented Ṛgvedic pluta, and close the
      **अ + अ → आ** example gap.
- [x] **Pass 3 — Audit Chapter 9.** Map existing explanations, identify
      duplication, and distinguish the fourteen-form teaching axis from the
      nine-family analytical structure.
- [x] **Pass 4 — Rebuild the section architecture.** Place the svara analysis
      where it follows naturally from *mātrā* and precedes the sound-volume
      calculation.
- [x] **Pass 5 — Draft the body.** Use explanatory classroom prose, Sanskrit
      terminology on first use, concrete examples before abstractions, and no
      figure changes.
- [x] **Pass 6 — Integrate the result.** Add source-heavy endnotes, PASS scope
      judgments, Chapter 15 and Chapter 16 callbacks, cross-reference updates,
      and a Lost and Found record for any displaced prose.

## 17. Hammer

> Sanskrit's vowel architecture reveals engineering in two places: in the
> sounds it selects as reusable coordinates, and in the sounds it knows how to
> produce without adding them to the grid.

Chapter 9 expresses the same conclusion more compactly after the consonant and
vowel cases: **This is engineering by exclusion.**
