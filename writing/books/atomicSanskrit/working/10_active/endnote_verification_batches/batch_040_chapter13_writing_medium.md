# Endnote Verification Batch 040 — Chapter 13 Writing as Medium

**Audit date:** 2026-09-04  
**Scope:** The new Chapter 13 §13.3 endnote supporting the claim that लिपि (*lipi*) is useful but cannot serve as a reliable primary calibrant. The audit checked the body claim, short note, full note, source locators, local records, and live deployment.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `writing-medium-fire-and-authority` | P0 | Pass | The Nalanda claim is tied to the Archaeological Survey of India and UNESCO nomination dossier; the Alexandria wording is limited to written collections destroyed by fire and is supported by Plutarch, Cassius Dio, and the Open University synthesis; the order to burn other Qur'anic materials follows *Ṣaḥīḥ al-Bukhārī* 4987. The different causes remain distinct while supporting the shared medium-risk argument. |

## Digital Evidence Records

The Nalanda dossier excerpt and the public-domain Plutarch and Cassius Dio pages are archived with checksums. The Open University and *Ṣaḥīḥ al-Bukhārī* URLs are registered even though their servers rejected automated capture. All five records appear in `working/40_reference/sources/as_source_registry.md` and are linked from the endnote's hidden `SOURCE-RECORDS` block.

## Completion Tests

- The new Chapter 13 marker resolves to one endnote.
- Each hidden source ID resolves to one registry entry.
- The body carries the architectural conclusion; historical qualifications remain in the endnote.
- The source archive remains outside the reader-facing manuscript build.
