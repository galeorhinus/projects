# Bounded सनादि (sanādi) Eligibility Pass

This pass applies one सनादिप्रत्ययः (sanādipratyayaḥ) at a time, without an उपसर्गः (upasargaḥ), to every धातुः (dhātuḥ) entry in the pinned engine's Dhātupāṭha. It records generated candidates. It does not add them to the Sanskrit word count.

## Inputs

The engine tested **2229 source entries**. The reconciled ledger contains **2634 provisional base word-meanings** across **2739 lexical assignment rows**. Three source entries have no admitted lexical meaning: `01.0900` and `01.0951` retain unenumerated meaning lists, while `01.0930` is classified as grammatical metadata.

## धातुः (Dhātuḥ) Results

| Operation | Engine entries with output | Zero output | Base meanings represented | Candidate derived word-meanings | Distinct spellings | Admitted |
|---|---:|---:|---:|---:|---:|---:|
| णिजन्त (ṇijanta), causative (`Ric`) | 2229 | 0 | 2634 | 2634 | 1550 | 0 |
| सन्नन्त (sannanta), desiderative (`san`) | 2229 | 0 | 2634 | 2634 | 2145 | 0 |
| यङन्त (yaṅanta), intensive (`yaN`) | 1775 | 454 | 2099 | 2099 | 1380 | 0 |
| यङ्लुगन्त (yaṅluganta), intensive with luk (`yaNluk`) | 1775 | 454 | 2099 | 2099 | 1609 | 0 |

A candidate derived word-meaning combines one operation with one reconciled base meaning. Two meanings carried by the same spelling remain separate. Alternative surface forms produced for the same derivation remain attached to that candidate and do not multiply it. The spelling column is only a diagnostic.

The णिजन्त (*ṇijanta*), causative, and सन्नन्त (*sannanta*), desiderative, operations produced at least one output for every engine entry. The यङन्त (*yaṅanta*) and यङ्लुगन्त (*yaṅluganta*) operations produced output for 1,775 entries and no output for 454. The primary rule restricts यङन्त (*yaṅanta*) to a one-vowel, consonant-initial धातुः (*dhātuḥ*) and to repeated or intense action; the present report does not assume that every generated रूपम् (*rūpam*), form, satisfies the intended meaning in actual use.

One checked example proves why generation and eligibility must remain separate. The Kāśikā commentary under 3.1.22 says that the general यङन्त (*yaṅanta*) formation is not used for *śobhate* and *rocate* because of *anabhidhāna*. Vidyut nevertheless returns `SoSuBya` / `SoSuB` and `rorucya` / `roruc` for the corresponding entries. The engine has completed a formal derivation; the semantic witness has not admitted the resulting word-meaning.

## Deferred प्रातिपदिकम् (Prātipadikam) Inputs

The engine also exposes `kAmyac`, `kyaN`, and `kyac`, which create a नामधातुः (*nāmadhātuḥ*) from a प्रातिपदिकम् (*prātipadikam*). They are not applied here because the project has not yet fixed the प्रातिपदिकम् (*prātipadikam*) input inventory. Adding a few familiar examples would not establish a count.

## Next Eligibility Decision

Review the four धातुः (*dhātuḥ*) relations in this order: णिजन्त (*ṇijanta*), सन्नन्त (*sannanta*), यङन्त (*yaṅanta*), and यङ्लुगन्त (*yaṅluganta*). For each one, determine whether the grammatical condition licenses a productive word-meaning for every represented base meaning or whether lexical exclusions require a narrower set. Only approved rows can move from `candidate` to `admitted`.

Row-level records are in `sanadi_engine_results.csv` and `sanadi_candidate_meanings.csv`. The JSON report stores the scope, sources, checksums, and exact summary counts.
