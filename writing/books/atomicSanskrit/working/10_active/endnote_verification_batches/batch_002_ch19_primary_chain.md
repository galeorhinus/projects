# Endnote Verification Batch 002 — Chapter 19 Primary Chain

**Audit date:** 2026-09-01  
**Scope:** Six notes in Chapter 19 that still contain explicit verification markers. Together they support the chapter's reconstruction of the path from Sanskrit forms to starred PIE ancestry.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `s-mobile-root-extension-confessions` | P0 | Strengthened | Replaced the claim that *s-mobile* has "no source, no rule, no conditioning environment, and no meaning" with what the literature supports: its distribution was not accurately predictable, several origins have been proposed, and no explanation has won agreement. Distinguished that uncertainty from the separate objection that reconstructed root extensions often lack an identifiable function. |
| `sut-agama-visarga-s` | P1 | Corrected | Corrected 6.1.137 from two preceding forms to three: *sam*, *pari*, and *upa*. Removed the claim that *suṭ* appears before ⟪कृ⟫ alone and removed unrelated visarga examples incorrectly assigned to 8.3.46. Rewrote the body paragraph around the verified rule-cluster. |
| `jan-dhatupatha-double-entry` | P0 | Strengthened | Confirmed both entries in the project's machine-readable Dhātupāṭha and in the Kāśikā on 7.3.79. Clarified that 3.25 and 4.44 are project base-index numbers rather than universal printed locators. Removed an unnecessary, unverified list of modern-language spellings. |
| `chambers-1872-king-kin` | P0 | Locator corrected | Verified the title page and both entries against page-images. *Kin* is on p. 281 and *king* on p. 282; the old note assigned both to p. 281. The quotations and unstarred Sanskrit termini are otherwise accurate. |
| `skeat-aryan-roots-and-edition-drift` | P0 | Corrected | Compared the 1882 and 1910 page-images. The heading, authority, Sanskrit-alphabet, GENUS, and CURT changes are real. Corrected the later beget-root from **KN** to **GEN**, removed unneeded unverified examples, and added exact entry and appendix pages. |
| `muller-1863-janaka-king` | P0 | Corrected | The lectures were delivered in 1863 but published in 1864. Corrected the bibliography and the first *king / janaka* passage from the old pp. 242–43 locator to p. 218. Verified the remaining passages at pp. 193 and 255–56. |

## Principal Sources Checked

- Kenneth Shields Jr., "Indo-European S-Mobile and Indo-European Morphology," *Emerita* 64.2 (1996), pp. 249–54.
- James Clackson, *Indo-European Linguistics: An Introduction* (Cambridge University Press, 2007), pp. 67–70.
- Julius Pokorny, *Indogermanisches etymologisches Wörterbuch* (Francke, 1959), pp. 938–45.
- *Aṣṭādhyāyī* 6.1.135 and 6.1.137–39 with the Kāśikā; 8.3.46 checked as the excluded rule.
- The project's `analysis/dhatupatha/data/dhatupatha.csv`; Kāśikā on *Aṣṭādhyāyī* 7.3.79.
- James Donald, ed., *Chambers's Etymological Dictionary of the English Language* (1872), title page and pp. 281–82.
- Walter W. Skeat, *An Etymological Dictionary of the English Language* (1882), pp. 172, 255, 729–45; new and revised edition (1910), pp. 150, 287–88, 751–58.
- Friedrich Max Müller, *Lectures on the Science of Language*, Second Series (1864), title page and pp. 193, 218, 255–56.

## Digital Evidence Records

The exact URLs, local dataset checksum, Internet Archive item records, and
repository checksums are registered in [the digital source registry](../../40_reference/sources/as_source_registry.md)
under these stable IDs:

- `shields-s-mobile-1996`
- `clackson-ie-linguistics-2007`
- `pokorny-iew-1959-vol1`
- `ashtadhyayi-rule-cluster-digital`
- `project-dhatupatha-csv`
- `chambers-etymological-dictionary-1872-scan`
- `skeat-etymological-dictionary-1882-scan`
- `skeat-etymological-dictionary-1910-scan`
- `muller-science-language-second-series-1864-scan`

The open *Emerita* article is archived locally. The four large dictionary and
lecture scans remain in the Internet Archive; their item metadata and supplied
checksums are retained locally instead of duplicating several hundred
megabytes in Git.

## Outcome

All six explicit verification markers were discharged. Every correction was carried into the Short form and the Chapter 19 deployment. The batch found four factual or locator errors, one overstatement, and one note that needed clearer edition-numbering boundaries.

## Required Completion Tests

1. Replace or discharge every `[VERIFY]` marker in the six full notes.
2. Add exact page, entry, rule, or edition locators.
3. Compare each note against the Chapter 19 claim and all appendix deployments.
4. Update each Short form after any correction or narrowing.
5. Record source-access limits rather than treating an inaccessible scan as verification.
6. Complete full and short manuscript assemblies.
