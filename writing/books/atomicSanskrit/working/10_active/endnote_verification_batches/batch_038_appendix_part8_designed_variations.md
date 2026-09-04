# Endnote Verification Batch 038 — Appendix Part 8

**Audit date:** 2026-09-03  
**Scope:** All six previously unreviewed endnotes in Appendix Part 8, *Designed Variations Across the Two Domains*. Exact forms were checked against the Ṛgveda and the cited grammatical rules. The complete figure dataset and all eight generated pages were validated. No appendix prose was changed.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `vedic-vocative-sentence-accent` | P0 | Verified | RV 3.25.1 begins with accented **ágne**; RV 1.1.7 places unaccented **agne** after **upa tvā**. Whitney §314 states the sentence- and *pāda*-initial vocative rule and gives the same contrast. |
| `designed-variations-figure-sources` | P0 | Reproduced | The validators confirmed 107 figure subrows across 83 inventory rows, including 11 explicitly open subrows and 2 measured zeros. The duplicate deployment field was removed from the note. |
| `vedic-injunctive-vocam` | P0 | Strengthened | RV 1.32.1 has **pra vocam**. Kiparsky identifies the exact form as first-person aorist injunctive and gives its performative force on p. 223. The note now supplies that page locator. |
| `vedic-gerund-pitvi` | P0 | Verified | RV 3.40.7 has **pītvī somasya vāvṛdhe**. The commentary on Aṣṭādhyāyī 7.1.49 cites the same passage and contrasts **pītvī** with expected **pītvā**. |
| `vedic-infinitives-rv-1-24-8` | P0 | Verified | The RV 1.24.8 *padapāṭha* gives **anu-etavai** and **prati-dhātave**. Aṣṭādhyāyī 3.4.9 lists the Vedic infinitive endings including **-tavai** and **-tave**. |
| `vedic-participle-cikitvah` | P0 | Verified | RV 3.25.1 uses vocative **cikitvaḥ**. Whitney §462a records Rigvedic masculine vocative **-vas** beside later **-van**. The stored exact-form check finds 11 **cikitvaḥ** tokens and no exact **cikitvan** token; the appendix correctly leaves the local architectural purpose open. |

## Digital Evidence Records

The ten GRETIL *padapāṭha* files, Whitney OCR, Kiparsky article, exact Aṣṭādhyāyī rule pages, and project figure-validation records are registered in `working/40_reference/sources/as_source_registry.md` with local paths and checksums.

## Completion Tests

- Every live Appendix Part 8 marker has a reviewed endnote.
- All cited mantra numbers and forms agree with the checked primary texts.
- Aṣṭādhyāyī 3.4.9 and 7.1.49 support the two rule-level claims.
- Both figure validators pass when run in `.venv-figures`.
- No Appendix Part 8 prose change was applied.
