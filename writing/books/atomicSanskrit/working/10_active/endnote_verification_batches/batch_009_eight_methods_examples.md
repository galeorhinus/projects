# Endnote Verification Batch 009 — Eight Methods Examples

**Audit date:** 2026-09-02  
**Scope:** Ten Chapter 1 notes supporting the examples under “Withhold the light,” “Steal the foundation,” “Wear false identity,” “Turn the gift against the giver,” and “Possess the uncontainable.”

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `kaliya-yamuna-poisoning` | P1 | Strengthened | Verified the poisoning, removal, and restoration through *Bhāgavata Purāṇa* 10.16 and 10.26.12. Replaced general narrative detail with exact verse ranges. No manuscript correction required. |
| `madhu-kaitabha-vedas-theft` | P0 | Corrected | The theft is explicit in the *Mahābhārata*'s Nārāyaṇīya account, 12.335. The former note incorrectly attributed the theft to the *Devī Māhātmya* and the *Bhāgavata Purāṇa*. The manuscript's short statement remains accurate. |
| `hayagriva-asura-vedas-theft` | P0 | Corrected | *Bhāgavata Purāṇa* 8.24.8-9 names Hayagrīva as the thief and Matsya as his destroyer. The former note incorrectly joined this theft to the different Hayagrīva narrative in the *Devī Bhāgavata Purāṇa*. The manuscript's short statement remains accurate. |
| `putana-nurse-poison` | P1 | Verified | Confirmed the pleasing appearance, unopposed entry, and poisoned breast at *Bhāgavata Purāṇa* 10.6.4-12. No manuscript correction required. |
| `maricha-golden-deer` | P1 | Strengthened | Added exact locators for the command, transformation, recognition, death, and borrowed voice in Vālmīki's *Rāmāyaṇa*, Araṇya Kāṇḍa 42-44. No manuscript correction required. |
| `kalanemi-ascetic-hanuman` | P1 | Strengthened | Confirmed the episode in *Adhyātma Rāmāyaṇa*, Yuddha Kāṇḍa 7, including **मुनिवेषधरः (*muniveṣadharaḥ*)** and the fabricated hermitage. Preserved the distinction from Vālmīki's telling without chronological labels. No manuscript correction required. |
| `paundraka-vasudeva` | P1 | Verified | Confirmed Pauṇḍraka's identity claim, demand, and imitated insignia at *Bhāgavata Purāṇa* 10.66.1-21. No manuscript correction required. |
| `vrkasura-bhasmasura-boon-reversal` | P0 | Corrected | *Bhāgavata Purāṇa* 10.88 documents Vṛka and a young-brahmin appearance of Viṣṇu, not Bhasmāsura and Mohinī. The popular Bhasmāsura telling repeats the pattern, but this audit did not establish from a primary source that the two names identify one actor. A manuscript correction is proposed below. |
| `shumbha-nishumbha-devi-mahatmyam` | P1 | Strengthened | Recentered the note on the exact ownership claim in *Devī Māhātmya* 5.89-125: treasures have been seized, the Devī is classified as another treasure, and Śumbha orders her submission. No manuscript correction required. |
| `andhakasura-shiva-purana` | P1 | Strengthened | Verified Andhaka's birth, adoption, desire for Pārvatī, attack upon her protected cave, punishment, recognition, and later admission into Śiva's gaṇas across *Śiva Purāṇa*, Rudra Saṃhitā 5.42-49. No manuscript correction required. |

## Applied Manuscript Correction

### Chapter 1 §1.4 — do not present Vṛka and Bhasmāsura as two documented actors

**Current:**

> **Turn the gift against the giver.** Vṛkāsura and Bhasmāsura receive a boon and immediately turn it toward the source.[NOTE: vrkasura-bhasmasura-boon-reversal]

**Applied:**

> **Turn the gift against the giver.** Vṛkāsura receives a boon and immediately turns it against Śiva, who granted it. The popular Bhasmāsura telling repeats the same pattern.[NOTE: vrkasura-bhasmasura-boon-reversal]

**Reason:** The *Bhāgavata Purāṇa* establishes the Vṛka account. It does not name Bhasmāsura or Mohinī. The proposed wording keeps both familiar names while avoiding the unsupported implication that the note documents two independent cases.

## Digital Evidence Records

New source records:

- `vedabase-bhagavata-10-16`
- `narayaniya-mbh-12-335`
- `vedabase-bhagavata-8-24`
- `vedabase-bhagavata-10-6`
- `valmiki-ramayana-aranya-42-44`
- `adhyatma-ramayana-yuddha-7`
- `vedabase-bhagavata-10-66`
- `vedabase-bhagavata-10-88`
- `devimahatmya-ch5`
- `wisdomlib-shiva-purana-andhaka-42-49`

All ten records include exact digital URLs and local research captures with SHA-256 checksums.

## Required Completion Tests

1. Regenerate and check the master ledger.
2. Run the source-registry validator.
3. Run full and short manuscript assembly.
4. Run `git diff --check`.
