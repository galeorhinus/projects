# यङन्त (Yaṅanta) Semantic Review

This pass decides what must be reviewed before यङन्त (*yaṅanta*) and यङ्लुगन्त (*yaṅluganta*) can enter the generativity count. It changes no count and no manuscript claim.

## What the Rules Distinguish

Aṣṭādhyāyī 3.1.22 supplies the general यङन्त (*yaṅanta*) operation. The Kāśikā explains its semantic field through **पौनःपुन्यम् (*paunaḥpunyam*)**, repetition, and **भृशार्थः (*bhṛśārthaḥ*)**, intensity. Under this project's counting rule, those are two different meanings even when one derived form can carry either one.

Two following rules narrow that general field. Rule 3.1.23 assigns movement-denoting धातुः (*dhātuḥ*) meanings to crooked movement and excludes the general repetition/intensity reading there. Rule 3.1.24 assigns its listed धातवः (*dhātavaḥ*) to disparagement of the action itself; criticism of the agent or instrument does not satisfy the condition.

The same commentary also supplies a lexical control. It rejects the general यङन्त (*yaṅanta*) use of *śobhate* and *rocate* through **अनभिधानम् (*anabhidhānam*)**, although Vidyut produces formal outputs for the corresponding entries. A derivation engine can show that a form is constructible. It cannot by itself show that speakers use the resulting word with the proposed meaning.

## What the Engine Covers

| Engine path | Source entries | Reconciled base meanings | Treatment |
|---|---:|---:|---|
| 3.1.22 general path | 1754 | 2072 | repetition/intensity review |
| Vārttika 3.1.22.1 shape path | 9 | 12 | same semantic review; special form |
| 3.1.24 disparaged action | 12 | 15 | exclusive semantic branch |
| No engine output | 454 | 559 | unresolved, not admitted |

The pinned Vidyut 0.4.0 module has no separate 3.1.23 selection path. Its ordinary formal path therefore includes possible movement meanings without determining whether crooked movement is intended. The broad source-gloss screen places **312 base meanings** in a review queue. Those rows are retrieval candidates, not 3.1.23 decisions and not countable results.

## यङ्लुगन्त (Yaṅluganta)

Aṣṭādhyāyī 2.4.74 applies **लुक् (*luk*)** to यङ् (*yaṅ*) in the stated environment. The commentary retains consequences of the deleted प्रत्ययः (*pratyayaḥ*) through **प्रत्ययलक्षणम् (*pratyayalakṣaṇam*)**, and the pinned implementation assigns the resulting धातुः (*dhātuḥ*) to अदादिगणः (*adādigaṇaḥ*). The operation therefore creates a distinct derived verbal word and paradigm. It does not independently create a new meaning: the यङ्लुगन्त (*yaṅluganta*) inherits whichever repetition, intensity, crooked-movement, or disparaged-action branch licensed the corresponding यङन्त (*yaṅanta*).

## Decisions Proposed

- **YAN-P1 — pending:** Represent repetition and intensity as two different meanings under general 3.1.22 eligibility. Do not assume that both are lexically available for every generated base meaning.
- **YAN-P2 — pending:** For movement-denoting base meanings governed by 3.1.23, use one crooked-movement relation instead of the two general 3.1.22 relations.
- **YAN-P3 — pending:** For base meanings governed by 3.1.24, use one disparaged-action relation instead of the two general 3.1.22 relations.
- **YAN-P4 — pending:** Apply attested anabhidhana exclusions before admission. Exclude the known shubh and ruc controls from the general yan candidate set unless contrary lexical evidence is found.
- **YAN-P5 — pending:** Treat a licensed yaN-luk formation as a separate derived verbal word because its formation and paradigm differ, but let it inherit the corresponding yaN semantic branch. Luk does not create another meaning multiplier.

## Count Status

No यङन्त (*yaṅanta*) or यङ्लुगन्त (*yaṅluganta*) candidate is admitted. Exact totals require approval of the semantic model, manual classification of the 3.1.23 queue, and a wider lexical-exclusion check. The current published and research totals remain unchanged.

The row-level movement queue is `yan_movement_candidates.csv`. The JSON report preserves source URLs, retrieval records, hashes, engine-path counts, and all pending proposals.
