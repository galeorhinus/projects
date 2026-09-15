# Base Meaning Audit

## First Result

The meaning-bearing source contains **2,229 entries**. This pass extracts **2,741 provisional source meaning assignments** including **3 partially enumerated entries**. Another **2 entries** have no finite meaning list and remain outside the subtotal.

These are assignments of meanings to source entries, not a finished vocabulary count. A list may use overlapping descriptions, and two entries may represent the same word and meaning. Both must be settled before these assignments become the base-word total. Unenumerated entries have a blank count, not zero. Partial entries contribute only their admitted meanings; their remaining gaps are recorded explicitly.

The book's older file has 2,168 entries and no meaning column. Its counts remain separate: this pass does not silently substitute a different inventory. No prefixes, derived bases, conjugations, or declensions have been added.

The [commentary review](meaning_review.md) resolved 33 of the initial 38 interpretation gaps. After 88 documented duplicate reductions, **2,653 provisional assignments** remain. The [identity reviews](identity_review.md) record the individual reductions and their sources. That subtotal still awaits the wider lexical-identity review.

## By Gana

| Gana | Source entries | One gloss | Enumerated | Partial | Unenumerated | Needs interpretation | Assignments |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1. भ्वादि (bhvādi) | 1156 | 944 | 208 | 2 | 2 | 0 | 1461 |
| 2. अदादि (adādi) | 76 | 62 | 14 | 0 | 0 | 0 | 101 |
| 3. जुहोत्यादि (juhotyādi) | 26 | 17 | 9 | 0 | 0 | 0 | 37 |
| 4. दिवादि (divādi) | 161 | 142 | 18 | 1 | 0 | 0 | 191 |
| 5. स्वादि (svādi) | 38 | 31 | 7 | 0 | 0 | 0 | 46 |
| 6. तुदादि (tudādi) | 174 | 148 | 26 | 0 | 0 | 0 | 212 |
| 7. रुधादि (rudhādi) | 25 | 19 | 6 | 0 | 0 | 0 | 33 |
| 8. तनादि (tanādi) | 10 | 10 | 0 | 0 | 0 | 0 | 10 |
| 9. क्र्यादि (kryādi) | 71 | 60 | 11 | 0 | 0 | 0 | 84 |
| 10. चुरादि (curādi) | 492 | 433 | 59 | 0 | 0 | 0 | 566 |

The status columns count source entries; the last counts their extracted meanings. An entry listing three meanings contributes one to 'Enumerated meanings' and three to the last column.

## What the Extraction Does

1. Keeps each source entry's identifier, citation form, original gloss, source line, URL, and checksum.
2. Keeps qualified phrases together. For example, vyaktayam vaci is one description, not two meanings.
3. Separates visible lists and explicitly annotated compounds. It does not guess the segmentation of every compound.
4. Counts sourced members of partial lists while retaining the uncounted remainder. Leaves unenumerated entries blank.
5. Counts neither English synonyms nor spellings. The assignment key is the source entry plus its meaning identifier.

The segmentations are analysis annotations. The commentary review settles the selected entries listed in its decision ledger; the rest have not received a complete independent Sanskrit review. A single listed gloss is provisionally one assignment; it may conceal finer senses that this source does not state. The complete CSV preserves the Sanskrit wording rather than introducing unverified English translations.

## Examples

| Source entry | Original meaning description | Extracted meanings |
|---|---|---|
| 01.1074: `pA\` | पाने (pāne) | पाने (pāne) |
| 02.0051: `pA\` | रक्षणे (rakṣaṇe) | रक्षणे (rakṣaṇe) |
| 06.0022: `fca~` | स्तुतौ दीप्तौ च (stutau dīptau ca) | स्तुतौ (stutau); दीप्तौ (dīptau) |
| 01.0978: `hula~` | गतौ हिंसायां संवरणे च (gatau hiṃsāyāṃ saṃvaraṇe ca) | गतौ (gatau); हिंसायां (hiṃsāyāṃ); संवरणे (saṃvaraṇe) |
| 01.1165: `wuo~Svi` | गतिवृद्ध्योः (gativṛddhyoḥ) | गतौ (gatau); वृद्धौ (vṛddhau) |
| 01.0951: `vanu~` | अनेकार्थत्वे (anekārthatve) | Unresolved; no invented count |

The two pa entries retain drinking and protecting separately. The rc entry retains praise and shining separately. The hula entry lists movement, harming, and covering. The van entry says multiple meanings without supplying an enumeration.

## Identity Review

The exact-citation check flags **223 groups**, covering **487 source entries**. The ledger distinguishes groups with repeated glosses from groups with different descriptions. The commentary review establishes 81 same-identity groups; their repeated assignments are consolidated without deleting either source record. The remaining groups have not been automatically merged. A different citation form can also represent the same word; this exact-form check is a first diagnostic, not the complete identity review.

In the old-to-new comparison, 1,773 entries match in code and citation, 41 have a unique same-class citation candidate elsewhere, four have several candidates, and 350 have no exact candidate. Fifty local entries share a selected target with another local entry. The reconciliation table now shows both the proposed target and the newer source's entry at the old code. Candidate matches remain candidates; no ambiguous meanings have been copied into the old inventory.

## Files

- [Full source-entry ledger](base_meanings.csv)
- [One row per extracted meaning](base_meaning_assignments.csv)
- [Counts by gana](base_meanings_by_gana.csv)
- [Repeated-citation review](base_identity_review.csv)
- [Old-to-new reconciliation](base_local_reconciliation.csv)
- [Excluded placeholder rows](base_placeholders.csv)
- [Analysis rules and explicit segmentations](../meaning_analysis.json)
- [Commentary decisions and source links](meaning_review.md)

## Source

[Pinned Vidyut Dhatupatha](https://raw.githubusercontent.com/ambuda-org/vidyut/f3ba4167d40eebc4b3023d24e66867aa6a8cdb32/vidyut-prakriya/data/dhatupatha.tsv), archived locally with its source manifest. This is a digital transcription, not a new collation of printed editions.
SHA-256: `bb2013ead0ea536dc7f887164c385c703cb0014ccf6e5af35b87e6d3049ba380`.

## Next Work

Continue lexical-identity review, carrying the specific meaning gaps below alongside it. Reconcile the older inventory before assigning it a meaning total. After that, apply named derivational operations to admitted base meanings. Conjugation and declension remain a later, separate operation.

## Interpretation Queue

Repeated descriptions are grouped here; the CSV retains every affected source entry.

| Source entries | Original gloss | What needs checking |
|---|---|---|
| 01.0365 | मर्दने विमर्दने (mardane vimardane) | Locate commentary on prud to determine whether the second description adds a distinct meaning. The two transcriptions differ (vimardana versus pramardana); the one admitted assignment does not settle that difference. |
| 01.0900 | अनेकार्थाः (anekārthāḥ) | The commentary records general action and many meanings as explanations of the unspecified entry. Neither supplies a list of distinct lexical meanings. Keep the entry outside the numerical subtotal, with a blank count rather than zero. |
| 01.0951 | अनेकार्थत्वे (anekārthatve) | The commentary refers back to kage and distinguishes this van entry from other same-looking entries. It supplies no finite list of meanings. Keep this entry outside the numerical subtotal; do not import the meanings of another van merely from shared spelling. |
| 01.1158 | बीजसन्ताने गर्भाधाने छेदने बीजतन्तुसन्ताने मुण्डबीजोप्त्योः वपने घर्षणे तन्तुनिर्माणे च (bījasantāne garbhādhāne chedane bījatantusantāne muṇḍabījoptyoḥ vapane gharṣaṇe tantunirmāṇe ca) | The pinned inventory also names rubbing and thread-making and combines bija/tantu descriptions. The three inspected commentaries do not locate those additions. Keep them in the original gloss and seek their source; do not claim that this three-meaning subtotal exhausts vap. |
| 04.0077 | वृद्धिसिद्धिद्रोहदैवपर्यालोचनादिषु च (vṛddhisiddhidrohadaivaparyālocanādiṣu ca) | The pinned gloss ends in adi and does not enumerate the rest. Further meanings are not assigned a number. Retain the disagreement with Kshiratarangini about the fourth-class use beyond growth for the eligibility stage. |
