# Svara Architecture Evidence — Codex

**Status:** six research and deployment passes complete; figure production pending  
**Created:** 2026-07-29  
**Research plan:** [Svara Architecture Analysis Plan](as_svara_architecture_analysis_plan_codex.md)  
**Analytical method:** [PASS Deployment Plan](as_pass_deployment_plan_codex.md)  
**Manuscript status:** Chapter 9 revised; endnotes and Chapter 15/16 callbacks added

## 1. Status Language

This record separates four kinds of conclusion:

- **Verified:** an internal source, exact passage, or named phoneme inventory
  directly supports the statement.
- **Supported inference:** the evidence supports the architectural reading, but
  no internal source found so far states that design rationale explicitly.
- **Unresolved:** the research has not established the claim securely.
- **Rejected:** the available evidence contradicts the claim.

The distinction is essential. Sanskrit's internal analysis gives us a strong
account of the vowel system. It does not always tell us why the architecture
selected one possibility and left another open.

## 2. Principal Findings

1. **Verified:** the familiar fourteen-character teaching row and the
   traditional vowel-realization analysis are not the same inventory.
2. **Verified:** the traditional analytical structure uses nine vowel families:
   **अ, इ, उ, ऋ, ऌ, ए, ऐ, ओ, औ**.
3. **Verified:** **अ, इ, उ, ऋ** each permit *hrasva, dīrgha,* and *pluta*
   duration. Each duration combines analytically with three pitch relations and
   two nasal states, producing eighteen realizations per family.
4. **Verified:** **ऌ** has *hrasva* and *pluta* but no regular *dīrgha* in this
   account. **ए, ऐ, ओ, औ** have *dīrgha* and *pluta* but no *hrasva*. Each
   therefore has twelve realizations.
5. **Verified:** the complete analytical count is:

   > **4 × 18 + 5 × 12 = 132**

6. **Verified:** the count represents an analytical possibility space. It does
   not prove that all 132 realizations occur in received Vedic passages.
7. **Verified:** **ॡ** does not occupy the regular two-*mātrā* position of the
   **ऌ** family in the traditional 18/12 analysis. No ordinary Vedic or
   *laukika* word containing **ॡ** was found in this pass.
8. **Verified:** short **e** and **o** are physically possible and occur as
   independent vowels in Tamil, Telugu, Kannada, Korku, Mundari, and Ho.
9. **Rejected:** Sanskrit lacks short **ए/ओ** because those sounds are
   physically impossible, require two *mātrās*, or were absent from the
   surrounding Indian sound-field.
10. **Supported inference:** Sanskrit leaves short **ए/ओ** open because its
    operations already redirect a required short substitute toward **इ/उ**.
    The two additional coordinates would therefore add less function than
    their apparent symmetry suggests.
11. **Verified:** pitch is independent of base vowel quality and duration.
    Short, long, and *pluta* vowels can all participate in accent analysis.
12. **Rejected:** *svarita* inherently requires two *mātrās*. Aṣṭādhyāyī
    1.2.32 and its commentarial analysis explicitly account for *svarita*
    within short, long, and *pluta* vowels.
13. **Verified:** *samānākṣara* and *sandhyakṣara* are internal terms, but the
    Prātiśākhya lineages do not all enumerate the first group identically.
14. **Rejected:** **इ, उ, ऋ, ऌ** form a fully symmetrical four-way junction
    architecture. **इ/उ** produce **ए/ओ** and **ऐ/औ** patterns, while the
    corresponding results for **ऋ/ऌ** are **अर्/अल्** and **आर्/आल्**.
15. **Supported inference:** the vowel system shows architectural selection.
    The strongest evidence lies in the coordinated operations and open
    positions, not in claims of anatomical necessity.
16. **Verified:** the Mahābhāṣya records that the Sātyamugri and Rāṇāyanīya
    Sāmavedic lineages recited half-*e* and half-*o*. Sanskrit's analytical
    disciplines therefore knew the shorter sounds and preserved them where a
    bounded Vedic lineage required them without adding short **ए/ओ** to the
    generally reusable vowel inventory.
17. **Verified:** Ṛgveda 10.129.5 preserves pluta **आसी३त् (*āsī3t*)** in
    accented printed editions and in the Ṛgveda-Prātiśākhya's enumeration.
    A normalized database that removes Ṛgvedic pluta marks cannot be used to
    disprove that received reading.

## 3. Pass 1 — Internal Inventory

### 3.1 Nine Families and Their Durations

| Family | Ordinary written members | *Hrasva* | *Dīrgha* | *Pluta* | Pitch × nasality per permitted duration | Analytical total |
|---|---|---:|---:|---:|---:|---:|
| **अ** | अ, आ | yes | yes | yes | 6 | **18** |
| **इ** | इ, ई | yes | yes | yes | 6 | **18** |
| **उ** | उ, ऊ | yes | yes | yes | 6 | **18** |
| **ऋ** | ऋ, ॠ | yes | yes | yes | 6 | **18** |
| **ऌ** | ऌ | yes | **open** | yes | 6 | **12** |
| **ए** | ए | **open** | yes | yes | 6 | **12** |
| **ऐ** | ऐ | **open** | yes | yes | 6 | **12** |
| **ओ** | ओ | **open** | yes | yes | 6 | **12** |
| **औ** | औ | **open** | yes | yes | 6 | **12** |

Each permitted duration has:

> **3 pitch relations × 2 nasal states = 6 realizations**

The complete matrix therefore contains twenty-two permitted duration nodes:

> **12 nodes from four three-duration families**  
> **10 nodes from five two-duration families**  
> **22 × 6 = 132 realizations**

### 3.2 Sources for the Components

The inherited disciplines document every component used in the calculation:

| Component | Internal documentation | What it establishes |
|---|---|---|
| Nasal state | Aṣṭādhyāyī 1.1.8, **मुखनासिकावचनोऽनुनासिकः** | the *anunāsika* category |
| Duration | Aṣṭādhyāyī 1.2.27, **ऊकालोऽज्झ्रस्वदीर्घप्लुतः** | one-, two-, and three-*mātrā* duration classes |
| Pitch | Aṣṭādhyāyī 1.2.29–31 | *udātta, anudātta,* and *svarita* |
| Combined analysis | Siddhāntakaumudī and later teaching under 1.2.27 | each available duration is threefold by pitch and twofold by nasality |
| Twelve-member families | commentarial discussion under 1.1.8 and 1.2.27 | **ऌ** lacks *dīrgha*; **ए/ऐ/ओ/औ** lack *hrasva* |

Useful source pages:

- [Aṣṭādhyāyī 1.2.27 with commentaries](https://ashtadhyayi.com/sutraani/1/2/27?expand=sutra-commentary-nyaas-region&focus=sutra-commentary-nyaas-region&highlight=%E0%A4%B2%E0%A4%AD%E0%A5%8D%E0%A4%AF)
- [Aṣṭādhyāyī 1.1.8 with commentarial search](https://ashtadhyayi.com/sutraani/1/1/8)
- [Sanskrit Documents presentation of 1.2.27](https://sanskritdocuments.org/~sanskrit/learning_tools/sarvanisutrani/1.2.27.htm)

**Source judgment:** *Atomic Sanskrit* combines these inherited distinctions
into the complete **132-realization matrix**. The matrix is this book's
analytical synthesis; its components belong to the older grammatical and
phonetic disciplines.

### 3.3 Internal Inventory Is Scope-Sensitive

Ṛgveda-Prātiśākhya 1.11 states:

> **अष्टौ समानाक्षराण्यादितस्ततश्चत्वारि सन्ध्यक्षराण्युत्तराणि ।**

It counts eight initial *samānākṣarāṇi* followed by four
*sandhyakṣarāṇi*. The eight are **अ आ इ ई उ ऊ ऋ ॠ**; the four are
**ए ऐ ओ औ**. The received Ṛgvedic classification does not insert **ऌ** merely
to make a five-family diagram.

The Taittirīya-Prātiśākhya uses a different count:

> **अथ नवादितस्समानाक्षराणि**

This difference supplies a guardrail for the manuscript:

- *samānākṣara* and *sandhyakṣara* are valid internal terms;
- their exact inventory must be attributed to a lineage;
- the book should not flatten every Prātiśākhya into one universal list.

Sources:

- [Ṛgveda-Prātiśākhya text, Chapter 1](https://advocatetanmoy.com/rigveda-pratisakhyam-by-sounak/)
- [Taittirīya-Prātiśākhya scan](https://commons.wikimedia.org/wiki/File%3AThe_Taittiriya_Pratisakhya_%28IA_in.ernet.dli.2015.61160%29.pdf)

### 3.4 Place of Articulation

The internal articulatory classification gives the following broad map:

| Family | Traditional place |
|---|---|
| **अ** | ***कण्ठ (*kaṇṭha*)*** |
| **इ** | ***तालु (*tālu*)*** |
| **उ** | ***ओष्ठ (*oṣṭha*)*** |
| **ऋ** | ***मूर्धन् (*mūrdhan*)*** |
| **ऌ** | ***दन्त (*danta*)*** |
| **ए/ऐ** | ***कण्ठतालु (*kaṇṭhatālu*)*** |
| **ओ/औ** | ***कण्ठोष्ठ (*kaṇṭhoṣṭha*)*** |

The Pāṇinīya-Śikṣā tradition preserves:

> **ए ऐ तु कण्ठतालव्यौ ओ औ कण्ठोष्ठजौ स्मृतौ**

It also describes the relative throat element within **ए/ओ** and **ऐ/औ**.
This supports an articulatory relation among the simple and junction vowels.
The description does not by itself establish every simplified classroom
equation used for *guṇa* and *vṛddhi*.

Source:

- [Pāṇinīya Śikṣā, edition and translation](https://ignca.gov.in/Asi_data/8226.pdf)

### 3.5 The Status of ॡ

**Finding:** **ॡ** should not currently be presented as an ordinary two-*mātrā*
member parallel to **आ, ई, ऊ, ॠ**.

Evidence:

1. the 18/12 analysis gives the **ऌ** family no *dīrgha* node;
2. commentarial discussion of **अकः सवर्णे दीर्घः** explicitly encounters
   the absence of a long **ऌ** output;
3. no received Vedic passage or ordinary Sanskrit word containing **ॡ** was
   found in this pass;
4. modern reference works commonly describe it as a formal or theoretical
   completion of the written row.

Source:

- [Kāśikā and related commentary under 6.1.101](https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya/6/6.1.101.htm)

**Unresolved:** when **ॡ** entered particular teaching alphabets, which internal
text first wrote it as an independent symbol, and whether any lineage gives it
a narrowly restricted use.

## 4. Pass 2 — The अ–आ Structural Audit

### 4.1 What Is Secure

The short and long members of *avarṇa* are not described as duration-only
duplicates in the later internal analysis:

- actual short **अ** is ***संवृत (*saṃvṛta*)***;
- **आ** is ***विवृत (*vivṛta*)***;
- grammatical operations nevertheless treat **अ/आ** as one functional family
  where *savarṇa* identity is required.

Aṣṭādhyāyī 1.1.9 defines *savarṇa*:

> **तुल्यास्यप्रयत्नं सवर्णम् ।**

Aṣṭādhyāyī 6.1.101 states:

> **अकः सवर्णे दीर्घः ।**

The final rule, 8.4.68:

> **अ अ ।**

is interpreted by the commentarial lineage as restoring the contracted
realization of short **अ** after the grammatical analysis has treated it as
open where required for operations.

Sources:

- [Aṣṭādhyāyī 1.1.9 and *savarṇa* explanation](https://www.learnsanskrit.org/vyakarana/sounds/savarna-sounds/)
- [Aṣṭādhyāyī 6.1.101 with Kāśikā](https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya/6/6.1.101.htm)
- [Aṣṭādhyāyī 8.4.68](https://ashtadhyayi.github.io/suutra/8.4/?transliteration_target=gurmukhi)

### 4.2 What This Does and Does Not Establish

**Verified:** Sanskrit's analysis separates spoken realization from functional
family membership.

**Supported inference:** this is a form of *snap to grid*. The architecture
uses one *avarṇa* family for grammatical operations even though the transmitted
short and long outputs differ in mouth configuration.

**Unresolved:** whether this arrangement was selected specifically for
error-detection, acoustic projection, or another physical reason.

**Rejected:** short **अ** is simply **आ** pronounced for half as long.

### 4.3 Vedic Evidence Gap

The operation **अ + अ → आ** is secure in Sanskrit and is documented by the
internal analytical lineage. This pass did not locate a sufficiently secure
Ṛgvedic *saṃhitāpāṭha/padapāṭha* pair that can be cited as the body example
without further source work.

**Status:** exact Vedic passage example still required before deployment.

## 5. Pass 3 — The Sandhyakṣara Audit

### 5.1 Secure Operations

The vowel architecture uses several different operations. They should not be
collapsed into one supposed short-to-long ladder.

| Operation | Documentation | Secure pattern |
|---|---|---|
| *yaṇ* | 6.1.77 **इको यणचि** | **इ/उ/ऋ/ऌ → य/व/र/ल** before a vowel |
| *guṇa* junction | 6.1.87 **आद्गुणः** | **अ/आ + इ/ई → ए**, **अ/आ + उ/ऊ → ओ**, **ऋ/ॠ → अर्**, **ऌ → अल्** |
| *vṛddhi* junction | 6.1.88 **वृद्धिरेचि** | **अ/आ + ए/ऐ → ऐ**, **अ/आ + ओ/औ → औ** |
| *ec* before a vowel | 6.1.78 **एचोऽयवायावः** | **ए/ऐ/ओ/औ → अय्/आय्/अव्/आव्** |
| same-family junction | 6.1.101 **अकः सवर्णे दीर्घः** | one long substitute for adjacent members of the same family |
| short substitute | 1.1.48 **एच इग्घ्रस्वादेशे** | **ए/ऐ → इ**, **ओ/औ → उ** when a short substitute is required |

### 5.2 The Useful Classroom Pair

The clearest paired demonstration is:

> **इ + अ → य**  
> **अ/आ + इ/ई → ए**

The same **इ** family participates in different operations according to its
position and the operation being performed. The architecture therefore joins
the vowel and consonant sides of the *varṇamālā* without making them identical.

### 5.3 Symmetry Limit

The following claim must not enter the manuscript:

> **इ, उ, ऋ, ऌ each generates a parallel pair of junction vowels.**

That symmetry does not exist. **इ/उ** participate in the **ए/ऐ** and **ओ/औ**
architecture. **ऋ/ऌ** instead produce sequences containing **र्/ल्**:
**अर्/अल्** and **आर्/आल्**.

This limit improves the argument. Sanskrit's grid is organized, but the
organization follows function rather than visual symmetry.

### 5.4 Why Short ए/ओ Are Excluded

**Verified:**

- Sanskrit gives **ए/ओ** no ordinary one-*mātrā* coordinate.
- Sanskrit knows how to request a short substitute.
- when that operation is required, **ए/ऐ** return to **इ**, and **ओ/औ** return
  to **उ**.

**Supported inference:** the architecture does not need separate short **ए/ओ**
coordinates because the simple **इ/उ** coordinates already perform the
required shortening function.

**Unresolved:** whether an internal source explicitly gives economy,
distinguishability, collision, or entropy as the reason.

## 6. Pass 4 — Pitch, Duration, and Nasality Matrix

### 6.1 Matrix Structure

The matrix should contain:

- **nine rows:** अ, इ, उ, ऋ, ऌ, ए, ऐ, ओ, औ;
- **nine principal columns:** three durations × three pitch relations;
- **two halves within each permitted cell:** oral and nasal.

The following symbols are recommended for the evidence figure:

- **Recognized:** the internal analytical system defines the realization;
- **Passage:** an exact received example has been located;
- **Restricted:** a stated operation produces or requires it;
- **Excluded:** the architecture provides no independent coordinate;
- **Unresolved:** source or usage remains unverified.

The figure must not use a filled cell to imply corpus frequency.

### 6.2 Matrix by Family

| Family | One *mātrā* | Two *mātrās* | Three *mātrās* |
|---|---|---|---|
| **अ** | recognized: 3 pitch × 2 nasal | recognized: 3 × 2 | recognized: 3 × 2 |
| **इ** | recognized: 3 × 2 | recognized: 3 × 2 | recognized: 3 × 2 |
| **उ** | recognized: 3 × 2 | recognized: 3 × 2 | recognized: 3 × 2 |
| **ऋ** | recognized: 3 × 2 | recognized: 3 × 2 | recognized: 3 × 2 |
| **ऌ** | recognized: 3 × 2 | **open** | recognized: 3 × 2 |
| **ए** | **open** | recognized: 3 × 2 | recognized: 3 × 2 |
| **ऐ** | **open** | recognized: 3 × 2 | recognized: 3 × 2 |
| **ओ** | **open** | recognized: 3 × 2 | recognized: 3 × 2 |
| **औ** | **open** | recognized: 3 × 2 | recognized: 3 × 2 |

### 6.3 Svarita Does Not Require Two Mātrās

Aṣṭādhyāyī 1.2.32 states:

> **तस्यादित उदात्तमर्धह्रस्वम् ।**

Its commentarial analysis apportions the initial high portion of *svarita*
according to the duration of a short, long, or *pluta* vowel. A short vowel can
therefore carry *svarita*. The contour does not require a two-*mātrā* vowel.

Sources:

- [Aṣṭādhyāyī 1.2.32](https://ashtadhyayi.com/sutraani/1/2/32?expand=sutra-commentary-balamanorama-region&focus=sutra-commentary-balamanorama-region&highlight=%E0%A4%B0%E0%A4%B5%E0%A4%A3)
- [Śabdakaustubha discussion](https://www.jainqq.org/booktext/Shabda_Kaustubh_Part_02/023084)

### 6.4 Pluta Is a Duration, Not a New Vowel

Ṛgveda 10.129.5 preserves:

> **अधः स्विदासी३दुपरि स्विदासी३त्**
>
> *adhaḥ svid āsī3d upari svid āsī3t*

The numeral marks *pluta* duration. The vowel quality remains **ई**; duration
adds another acoustic dimension.

Sources:

- [Ṛgveda 10.129.5](https://vedsearch.org/rigved/10/129/5)
- [Technical Vedic phonology presentation](https://spw.uni-goettingen.de/projects/aig/doc/VED-PHO-003.pdf)

The often-repeated count of three Ṛgvedic and fifteen Atharvavedic *pluta*
occurrences remains a secondary report in this pass. It should not enter the
manuscript until checked against the cited specialist source or a corpus count.

### 6.5 Pitch and Excluded Vowel Coordinates

**Verified:** pitch multiplies the information available on a selected vowel.

**Supported inference:** pitch helps keep the reusable vowel inventory compact
while permitting greater information density in Vedic transmission.

**Rejected:** pitch explains why Sanskrit lacks short **ए/ओ** or a long
contracted **अ**. The pitch system operates across available durations and does
not make those vowel qualities physically impossible.

## 7. Pass 5 — Subcontinental Sound-Field Comparison

### 7.1 Short e and o

The PHOIBLE inventories checked give the following results:

| Language | Short **e** | Long **e** | Short **o** | Long **o** | Source status |
|---|---:|---:|---:|---:|---|
| Tamil | yes | yes | yes | yes | PHOIBLE RA 1788 |
| Telugu | yes | yes | yes | yes | PHOIBLE RA 1791 |
| Kannada | yes | yes | yes | yes | PHOIBLE RA 1734 |
| Korku | yes | not in selected inventory | yes | not in selected inventory | PHOIBLE RA 1749, citing Zide 1960 |
| Mundari | yes | yes | yes | yes | PHOIBLE RA 1770, citing Sinha 1974 and Osada 1992 |
| Ho | yes | yes | yes | yes | PHOIBLE RA 1729 |

Sources:

- [Tamil inventory](https://phoible.org/inventories/view/1788)
- [Telugu inventory](https://phoible.org/inventories/view/1791)
- [Kannada inventory](https://phoible.org/inventories/view/1734)
- [Korku inventory](https://phoible.org/inventories/view/1749)
- [Mundari inventory](https://phoible.org/inventories/view/1770)
- [Ho inventory](https://phoible.org/inventories/view/1729)

### 7.2 Consequence

The comparison establishes:

- short **e/o** existed within the same broad Indian sound-field used by the
  manuscript;
- their absence from Sanskrit cannot be explained by an inability of Indian
  mouths to produce them;
- Sanskrit's selection does not merely copy every recurring regional vowel.

This is stronger evidence for engineering than a claim of regional absence
would have been. The architecture encountered or could accommodate the sounds,
yet did not need them as independent reusable coordinates.

### 7.3 Remaining Field Questions

The PHOIBLE comparison is a secure screening result, not the final citation
layer. Before manuscript deployment:

- secure grammar-page citations for each inventory where possible;
- add native word pairs demonstrating short and long **e/o** in Tamil, Telugu,
  Kannada, Mundari, and Ho;
- verify Korku against Nagaraja rather than relying only on Zide/PHOIBLE;
- test central-vowel contrasts separately from the short **e/o** question.

No claim about long contracted **अ** can yet be made from this table.

## 8. Pass 6 — PASS Profiles

### 8.1 Short ए and ओ

- **Candidate:** independent one-*mātrā* **ए/ओ** coordinates.
- **Physical possibility:** strong; all six comparison languages use short
  **e/o**.
- **Contribution:** moderate. They could add two vowel-quality distinctions.
- **Load:** moderate. Sanskrit already redirects a required short *ec*
  substitute to **इ/उ**, so the added coordinates would overlap with an
  existing operation.
- **Bounding support:** unnecessary because the architecture already has a
  stable substitute.
- **Scope judgment:** **Excluded** in Sanskrit's reusable vowel inventory.
- **Evidence status of rationale:** supported inference.

### 8.2 Short ऐ and औ

- **Candidate:** independent one-*mātrā* **ऐ/औ**.
- **Physical possibility:** not in doubt as brief diphthongal outputs, but exact
  Indian inventory comparisons remain to be assembled.
- **Contribution:** slight to moderate.
- **Load:** strong duplication. The shortening rule already returns **ऐ** to
  **इ** and **औ** to **उ**.
- **Scope judgment:** **Excluded**.
- **Evidence status of rationale:** supported inference.

### 8.3 Long ऌ / ॡ

- **Candidate:** ordinary two-*mātrā* member of the **ऌ** family.
- **Physical possibility:** plausible.
- **Contribution:** unresolved; no ordinary lexical or received Vedic use was
  found.
- **Load:** unresolved.
- **Bounding support:** the analytical system can discuss the family without
  filling the two-*mātrā* position.
- **Scope judgment:** **Excluded or analytically unresolved**, pending exact source
  history for **ॡ**.
- **Evidence status:** unresolved. Do not classify it as Included.

### 8.4 A Sustained Contracted अ

- **Candidate:** a two-*mātrā* central or contracted vowel that preserves the
  short **अ** quality rather than opening toward **आ**.
- **Physical possibility:** strong; comparable central vowels exist in human
  languages.
- **Contribution:** unresolved. Sanskrit already uses **आ** as the two-*mātrā*
  member of *avarṇa*.
- **Load:** likely overlap inside the operational *avarṇa* family.
- **Bounding support:** Sanskrit's analysis groups **अ/आ** where an operation
  requires *savarṇatā* and restores the transmitted short realization
  afterward.
- **Scope judgment:** **Excluded** as an independent reusable Sanskrit coordinate.
- **Evidence status of rationale:** supported inference; physical explanation
  still unresolved.

### 8.5 An Excluded One-Mātrā Vivṛta Avarṇa

- **Candidate:** a one-*mātrā vivṛta avarṇa* that preserves the open quality
  associated with **आ** while remaining short.
- **Physical possibility:** strong; human languages use short open *a*.
- **Contribution:** unresolved. Sanskrit already selects contracted **अ** for
  the one-*mātrā* position.
- **Load:** it would place two quality distinctions inside the one-*mātrā*
  position of one operational family.
- **Bounding support:** no bounded Sanskrit use has been located.
- **Scope judgment:** **Excluded** as an independent reusable Sanskrit coordinate.
- **Evidence status:** the excluded coordinate is structurally visible; the reason
  for leaving it open remains an architectural inference.

### 8.6 Pitch

- **Candidate:** *udātta, anudātta,* and *svarita*.
- **Contribution:** strong. Pitch carries additional Vedic information and is
  integral to exact transmission.
- **Load:** substantial training and lineage dependence.
- **Bounding support:** exact passage, recitational lineage, notation,
  transmitted sequence, and the Prātiśākhya/Śikṣā disciplines.
- **Scope judgment:** **Lineage-Bounded** for the exact received pitch pattern.
- **Evidence status:** verified.

### 8.7 Pluta

- **Candidate:** three-*mātrā* duration.
- **Contribution:** clear in specified uses such as interrogation, calling, or
  other stated conditions; exact function must be shown passage by passage.
- **Load:** slight when explicitly marked or transmitted.
- **Bounding support:** stated condition, notation, passage, and recitation.
- **Scope judgment:** **Restricted**, with received Vedic examples.
- **Evidence status:** verified for existence and duration; corpus prevalence
  remains incomplete.

### 8.8 Oral and Nasal Realizations

- **Candidate:** *anunāsika* and *ananunāsika* realization.
- **Contribution:** verified as an analytical distinction.
- **Load:** exact phonological and corpus distribution not yet mapped.
- **Bounding support:** phonetic environment and received recitation.
- **Scope judgment:** **Restricted** pending a more exact distribution study.
- **Evidence status:** the category is verified; the full 132-cell corpus
  realization is not.

## 9. Proposed Chapter 9 Consequences

The research supports three connected movements in Chapter 9. The deployment
places the vowel-family and realization analysis before the sound volume, then
applies PASS to consonant and vowel coordinates in one combined section.

### 9.1 The Vowel List Conceals a Larger Architecture

Begin with the familiar written row, then reorganize it as:

- nine vowel families;
- twenty-two permitted duration nodes;
- three pitch relations;
- two nasal states;
- 132 analytically recognized realizations.

The prose must say clearly that 132 is an analytical count, not 132 ordinary
written vowels and not 132 forms proven to occur in the corpus.

### 9.2 What Earns a Vowel Coordinate

Use PASS on:

- short **ए/ओ**;
- short **ऐ/औ**;
- long **ऌ/ॡ**;
- a sustained contracted **अ**;
- a one-*mātrā vivṛta avarṇa*.

The strongest classroom reveal is that short **e/o** occur throughout the
comparison field. Sanskrit leaves those positions open because its architecture
routes the required operation through **इ/उ**, not because the mouth cannot
produce them.

The Mahābhāṣya's report of half-*e* and half-*o* in two Sāmavedic lineages
sharpens the point. The architecture did not overlook these sounds. It
preserved them within the lineage where they belonged while keeping them
outside the generally reusable inventory. This is a direct example of PASS
assigning a sound to Lineage-Bounded scope.

### 9.3 Where the Vowel and Consonant Architectures Meet

Place these operations beside one another:

> **इ + अ → य**  
> **अ/आ + इ/ई → ए**

Then show:

- *yaṇ*;
- *guṇa*;
- *vṛddhi*;
- *ec* substitution;
- the non-parallel treatment of **ऋ/ऌ**.

This movement should explain operations rather than present a false geometric
symmetry.

## 10. Figure Consequences

### 10.1 Svara Realization Matrix

Proceed with the proposed 9-row matrix, but use evidence states rather than
simple filled/empty cells.

Required legend:

- analytically recognized;
- exact passage located;
- specified by a stated operation;
- open;
- unresolved.

### 10.2 The Existing Fourteen-Vowel Axis

Chapter 9 currently uses fourteen vowels as a generative axis. This research
creates a direct audit requirement:

- determine whether **ॡ** belongs in that reusable axis;
- distinguish a written teaching inventory from the regular operational
  inventory;
- recalculate any totals that depend on fourteen productive vowel choices;
- preserve fourteen only if the text explains exactly what the count means.

This affects the current 5 × 7 × 14 and related sonomer-address totals.

### 10.3 Suggested Figure Set

1. **Nine Families, 132 Realizations** — the complete duration/pitch/nasality
   matrix.
2. **Written Forms and Operational Families** — fourteen familiar symbols
   mapped onto nine families, with **ॡ** marked unresolved rather than silently
   productive.
3. **What Earns a Vowel Coordinate** — PASS profiles for short **ए/ओ**, long
   **ऌ**, sustained contracted **अ**, and one-*mātrā vivṛta avarṇa*.
4. **One Family, Different Operations** — *yaṇ, guṇa, vṛddhi,* and short
   substitution without false four-way symmetry.

## 11. Claims to Remove from the Working Hypothesis

The following claims should not survive into manuscript drafting:

1. short **e/o** are absent from the Indian sound-field;
2. a junction vowel is physically incapable of one-*mātrā* duration;
3. *svarita* requires at least two *mātrās*;
4. **इ, उ, ऋ, ऌ** each produce a parallel junction-vowel pair;
5. **ॡ** is an ordinary long vowel merely because the familiar teaching row
   prints it;
6. the complete 132-cell matrix is fully instantiated in the Vedic corpus;
7. pitch caused the open vowel coordinates;
8. Pāṇini created any of these relations.

## 12. Remaining Research After Reconciliation

The following questions can remain in the technical record without delaying
the body prose:

1. Establish the earliest secure phonetic-discipline source for
   *saṃvṛta* short **अ** and *vivṛta* **आ**. The commentarial account itself is
   secure.
2. Trace **ॡ** through internal teaching and script history. No ordinary Vedic
   or *laukika* use has been found.
3. Build passage-level examples across more of the 132-cell analytical matrix.
   The body must not imply that every analytical cell has already been found in
   a received passage.
4. Verify any numerical claim about the total frequency of *pluta* across the
   Vedic corpus before printing a corpus-wide count. The existence of pluta in
   Ṛgveda 10.129.5 is secure.
5. Replace inventory-database screening for Korku, Mundari, Ho, Tamil, Telugu,
   and Kannada with page-level grammar citations before those six languages
   carry a source-heavy endnote.

The earlier request for a Vedic **अ + अ → आ** example is now satisfied by
Ṛgveda 10.129.1: the *padapāṭha* preserves **न । असत्**, while the
*saṃhitāpāṭha* gives **नासद्**. The same hymn also supplies **न । आसीत् →
नासीत्** and **स्वधा । अवस्तात् → स्वधावस्तात्**.

The Chapter 9 count audit remains a deployment task rather than a research
gap. Fourteen can describe the familiar written teaching row; it must not be
presented as fourteen equally productive or equally evidenced vowel
coordinates.

## 13. Reconciliation of the Gemini and Claude Audits

### 13.1 Evidence Added from Gemini

The Mahābhāṣya records:

> **ननु च भोश्छन्दोगानां सात्यमुग्रिराणायनीया अर्धमेकारमर्धमोकारं चाधीयते ।**
>
> *nanu ca bhoś chandogānāṃ sātyamugrirāṇāyanīyāḥ ardham ekāram
> ardham okāraṃ cādhīyate*

The Sātyamugri and Rāṇāyanīya lineages of the Sāmaveda recite a half-*e* and a
half-*o*. This evidence is stronger than the comparison-language argument
alone because it establishes internal awareness and bounded Vedic use.

Gemini also confirms the Kāśikā explanation attached to the final
*Aṣṭādhyāyī* rule:

> **अकारो विवृतोपदिष्टः संवृतप्रत्यापत्त्यर्थं प्रयुज्यते ।**

The short **अ** had been treated as *vivṛta* for the relevant operations; the
final instruction restores its *saṃvṛta* realization.

### 13.2 Evidence Retained from Claude

Claude located useful Vedic junction examples:

- **न । असत् → नासद्** in Ṛgveda 10.129.1;
- **न । आसीत् → नासीत्** in the same verse;
- **स्वधा । अवस्तात् → स्वधावस्तात्** in Ṛgveda 10.129.5.

Claude also correctly emphasizes that the 132 total is an analytical
possibility space and that normalized corpus exports cannot prove the pitch
and nasality of every cell.

### 13.3 Correction to Claude's Pluta Verdict

Claude's report rejects **आसी३त् (*āsī3t*)** in Ṛgveda 10.129.5 because the
Digital Corpus of Sanskrit prints unmarked **आसीत्**. The report also states
that this database strips Ṛgvedic pluta notation. Those two observations
cannot support the rejection.

Accented printed editions preserve:

> **अधः स्विदासी३दुपरि स्विदासी३त्**
>
> *adhaḥ svid āsī3d upari svid āsī3t*

The Ṛgveda-Prātiśākhya also includes the passage when it identifies the rare
Ṛgvedic pluta forms. The manuscript may therefore retain this example while
avoiding an unsourced corpus-wide total.

## 14. Research Judgment

The six passes support a strong but narrower thesis than the initial
hypothesis.

Sanskrit's vowel engineering does not lie in avoiding sounds that Indian mouths
could not produce. The comparison field proves the opposite for short
**e/o**. The architecture selects a compact reusable inventory, generates
additional outputs through specified operations, and adds duration, pitch, and
nasality without turning every physically possible sound into another base
coordinate.

What Sanskrit leaves open is therefore as informative as what it selects.
