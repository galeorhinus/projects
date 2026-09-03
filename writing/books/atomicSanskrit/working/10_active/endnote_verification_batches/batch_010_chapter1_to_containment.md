# Endnote Verification Batch 010 — Chapter 1 to Containment

**Audit date:** 2026-09-02  
**Scope:** Seven remaining unaudited notes tied directly to Chapter 1, followed by three Rigvedic notes that carry the same action-over-label argument into Chapters 3 and 4.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `jalandhara-vrinda-shiva-purana` | P1 | Strengthened | Verified Jalandhara's use of Śiva's form in *Śiva Purāṇa* 5.22.37-52 and a second telling in *Padma Purāṇa* 6.13.14-51. Added exact locators and separated the Vṛndā episode from the narrower body claim. No manuscript correction required. |
| `virocana-chandogya-8-7-8-8` | P0 | Corrected | The former locator stopped at 8.8, but Indra identifies the contradiction and returns in 8.9; his instruction continues through 8.12. Corrected the locator to 8.7-8.12. No manuscript correction required. |
| `muller-bunsen-1856-priestcraft-overthrow` | P0 | Strengthened | Verified the date, recipient, and wording against Müller's letter of 25 August 1856 in the printed *Life and Letters*, vol. 1, pp. 181-183. A more exact body sentence is proposed below. |
| `pollock-sanskrit-cosmopolis-position-3` | P0 | Strengthened | Verified Pollock's culture-power frame and his statement on grammar and power at p. 188. Added his explicit qualification that the Sanskrit cosmopolis was not enforced by an imperial state or church. A more exact body sentence is proposed below. |
| `rv-1-32-vrtra` | P0 | Strengthened | Verified the containment and release sequence, exact verse locators, and the hymn's names for Vṛtra. No manuscript correction required. |
| `bhagavad-gita-16-6-daiva-asura` | P1 | Strengthened | Verified the verse and distinguished the literal “two created classes/formations” from the book's architectural rendering, “two created orders.” No manuscript correction required. |
| `compatibility-is-not-immunity` | P0 | Narrowed | Identified the central statement as the book's conceptual proposition and supplied historical evidence for the narrower colonial conversion mechanism. The body currently makes a global claim that these sources do not establish; a narrower sentence is proposed below. |
| `rigveda-7-104-18-rakshasas-night` | P1 | Strengthened | Verified the Sanskrit and compared three translations of **रिपः (*ripaḥ*)**. The body adds “peaceful,” which is not stated directly by the verse; a precise correction is proposed below. |
| `rv-vala-panis` | P1 | Strengthened | Verified RV 2.24.3 and the Saramā-Paṇi dialogue in RV 10.108, with exact verse locators. No manuscript correction required. |
| `rv-8-42-1-varuna-measures` | P0 | Strengthened | Verified the three principal verbs and the application of **असुर (*asura*)** to Varuṇa. No manuscript correction required. |

## Proposed Manuscript Corrections

These changes were approved and applied on 2026-09-02.

### Chapter 1 §1.4 — state Müller's documented words directly

**Current:**

> Max Müller privately named the goal: overthrow the authority of India's Sanskrit lineages and open the way for Christian conversion, while his public philology wore the costume of disinterested scholarship.

**Proposed:**

> Max Müller privately named the goal: use his work to overthrow what he called “Indian priestcraft” and open the way for Christian teaching, while his public philology wore the costume of disinterested scholarship.

**Reason:** This version stays close to Müller's own words and avoids substituting “the authority of India's Sanskrit lineages” for his phrase.

### Chapter 4 §4.4 — identify Pollock's power frame without claiming that he teaches hatred

**Current:**

> The asuric pyramid has now opened another front in its war against Sanskrit: readers are taught to hate the language as an instrument of elite power, although Sanskrit's calibrant architecture does the exact opposite by distributing authority.

**Proposed:**

> The asuric pyramid has now opened another front in its war against Sanskrit: readers are taught to see the language primarily as an instrument of elite power, although Sanskrit's calibrant architecture does the exact opposite by distributing authority.

The following phrase in the next sentence should change with it:

**Current:**

> this hate-driven narrative

**Proposed:**

> this power-centered narrative

**Reason:** Pollock explicitly centers culture and power. The cited book does not instruct readers to hate Sanskrit. The proposed sentence states the documented framing and leaves the book's disagreement intact.

### Chapter 1 §1.2 — narrow the historical conversion claim

**Current:**

> Across the world, the Abrahamic pyramid conquered or converted most प्राकृतिक (*prākṛtika*) societies and organized their descendants into its own architecture.

**Proposed:**

> Across large parts of the world, Abrahamic empires and missions conquered or converted प्राकृतिक (*prākṛtika*) societies and reorganized their descendants within pyramidal institutions.

**Reason:** The sources establish the recurring colonial mechanism in multiple regions. They do not establish the numerical claim “most” across the entire world.

### Chapter 3 epigraph — remove an adjective not stated directly by the verse

**Current:**

> those who bring hostility into the sacred and peaceful ceremony.

**Proposed:**

> those who bring hostility into the sacred ceremony.

**Reason:** **देवे अध्वरे (*deve adhvare*)** supports “sacred rite” or “sacred ceremony.” “Peaceful” is an interpretive addition rather than a direct part of the verse.

## Digital Evidence Records

New source records:

- `max-muller-life-letters-v1`
- `pollock-language-gods-2006`
- `gretil-chandogya-upanishad`
- `wisdomlib-jalandhara`
- `wisdomlib-rigveda-selected`
- `gretil-bhagavad-gita-16`
- `gita-supersite-16-6`
- `umich-colonialism-conversion`
- `uzh-colonial-mission-religious-change`

The existing `ut-rigveda-metrically-restored` record now includes Maṇḍala 2. Exact URLs and local SHA-256 checksums are retained wherever command-line archival capture succeeded.

## Required Completion Tests

1. Regenerate and check the master ledger.
2. Run the source-registry validator.
3. Run full and short manuscript assembly.
4. Run `git diff --check`.
