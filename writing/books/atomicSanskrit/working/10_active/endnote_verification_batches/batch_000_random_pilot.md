# Endnote Verification Batch 000 — Random Pilot

**Audit date:** 2026-09-01

## Purpose

Audit ten endnotes deployed in ten different chapters. The test is not whether every interpretation is uncontested. It is whether the cited source says what the note attributes to it, whether the manuscript states only what that evidence can carry, and whether a reader can follow the citation to the relevant passage.

Reproducibility seed: `endnote-audit-2026-09-01`

The sample was fixed before source review. No note was replaced after a weakness was found.

## Tests

Each note was checked for:

1. a unique note definition and at least one live manuscript marker;
2. agreement between the body claim, the short note, and the full note;
3. a primary source or an authoritative scholarly source with a usable locator;
4. accurate quotation, paraphrase, names, dates, verse numbers, rule numbers, and technical terminology;
5. a clear boundary between what the source establishes and what the book infers;
6. the absence of `[VERIFY]` and `[TBD]` placeholders;
7. successful assembly in both full-endnote and short-endnote modes.

## Sample And Results

| Chapter | Endnote | Risk | Result | Finding and action |
|---|---|:---:|---|---|
| 0 | `vedanta-anta-chronology-capture` | P1 | Strengthened | Removed a weaker secondary example. The revised note now relies on the Government of India's Vedic Heritage Portal, which defines *Vedānta* as conclusion and goal and then immediately makes a chronological claim. The note separates structural position, purpose, and chronology. |
| 1 | `raktabija-multiplication` | P2 | Strengthened | Replaced the loose “clone” description with the text's claim that each fallen drop produces another asura of Raktabīja's size and power. Added *Devī Māhātmya* 8.41, 8.43–48, and 8.53–57. |
| 2 | `paspashahnika-brihaspati-indra-word-list` | P0 | Pass | The Sanskrit text, translation, thousand-divine-year claim, and the move from word-by-word enumeration to general rule and exception agree with the *Mahābhāṣya*, *Paspaśāhnika*, Kielhorn vol. I, p. 5. No revision was needed. |
| 3 | `leviticus-slavery-25-44-46` | P1 | Strengthened | Replaced a long translation-dependent quotation with a precise paraphrase. The note now limits itself to acquisition from surrounding nations and resident-alien families, property, inheritance, and the separate rule for fellow Israelites. |
| 9 | `agnimile-rigveda-opening` | P1 | Locator strengthened | Ṛgveda 1.1.1 and the received **ईळे (*īḷe*)** form were correct. Added the exact *Ṛgveda-Prātiśākhya* locator, 1.11–12, for intervocalic **ड → ळ** and **ढ → ळ्ह**. |
| 13 | `juhotyadibhyah-shluh-dadhati` | P1 | Corrected | The old prose assigned replacement, reduplication, and ending attachment to 2.4.75. The revision states that 2.4.75 replaces **शप् (*śap*)** with **श्लु (*ślu*)**, while 6.1.10 requires reduplication. The apparent Ṛgveda locator conflict was resolved: standard ṛc numbering gives 1.66.2d; a half-line index gives 1.66.4. |
| 14 | `chandas-laghu-guru-virahanka-sequence` | P1 | Strengthened | Distinguished Piṅgala's earlier prosodic-combinatorial framework from the first explicit additive recurrence attributed to Virahāṅka. Added Parmanand Singh's exact discussion at pp. 233–235. |
| 15 | `nambudiri-vedic-recitation-isolation` | P0 | Corrected | Removed an unsupported claim that fieldwork had demonstrated sound-by-sound agreement across separated Vedic lineages. The revised note establishes what the sources document: named traditions in several regions, branch-specific preservation, the 1957 Nambūdiri recordings, and the limits of that evidence. Two dependent notes were corrected for consistency. |
| 18 | `retroflex-substrate-standard-account` | P0 | Corrected | The old note treated the central grid position of the retroflex row as evidence against contact and described the standard account too uniformly. The revision accurately presents contact, internal change, and mixed accounts, then states the boundary: full architectural integration requires explanation but cannot by itself date the row or disprove contact. |
| 19 | `asura-standard-etymology-contested` | P0 | Corrected | Removed a `[VERIFY]` marker and corrected two attribution errors. Monier-Williams does not give the two derivations in one *asura* entry as the old note claimed. Yāska does not use the phrase *asurāḥ suravirodhinaḥ* attributed to him in a linked note. *Nirukta* 3.8 supplies the life-breath analysis; the Kauthuma Sāmaveda Padapāṭha supplies the explicit *a + surasya* division. The Mayrhofer reconstruction and gloss were also corrected. |

## Principal Sources Checked

- Government of India, Vedic Heritage Portal, “Upanishads.”
- *Devī Māhātmya* 8.41–57.
- Patañjali, *Vyākaraṇa-Mahābhāṣya*, *Paspaśāhnika*, Kielhorn vol. I, p. 5.
- *Leviticus* 25:44–46, NRSVUE and JPS; Jacob Milgrom, *Leviticus 23–27*.
- Ṛgveda 1.1.1 and *Ṛgveda-Prātiśākhya* 1.11–12.
- *Aṣṭādhyāyī* 2.4.75 and 6.1.10; Ṛgveda 1.66.2d.
- Parmanand Singh, “The So-called Fibonacci Numbers in Ancient and Medieval India,” pp. 233–235.
- J. E. B. Gray, “An Analysis of Nambudiri Ṛgvedic Recitation and the Nature of the Vedic Accent”; Vedic Heritage Portal and IGNCA surveys.
- Murray B. Emeneau, “India as a Linguistic Area,” pp. 5–6; Hans Henrich Hock, “Substratum Influence on (Rig-Vedic) Sanskrit?”
- Manfred Mayrhofer, *Etymologisches Wörterbuch des Altindoarischen*, vol. I, pp. 147–148; Monier-Williams, entries *asura* and *sura*; Yāska, *Nirukta* 3.8; Sūrya Kānta, ed., *Ṛktantra*, p. 54.

## Digital Evidence Records

The exact URLs, archive paths, repository identifiers, and checksums are
registered in [the digital source registry](../../40_reference/sources/as_source_registry.md)
under these stable IDs:

- `vhp-upanishads`
- `gita-supersite-15-15`
- `aurobharati-devi-mahatmya-8`
- `vishvasa-mahabhashya-paspashahnika`
- `joshi-roodbergen-paspashahnika-1968`
- `vhp-rigveda-10-71`
- `biblegateway-leviticus-25-nrsvue`
- `sefaria-leviticus-25-jps`
- `milgrom-leviticus-23-27-2001`
- `ut-rigveda-metrically-restored`
- `vishvasa-rigveda-pratisakhya`
- `scharf-hyman-linguistic-encoding-sanskrit`
- `sanskritdocuments-ashtadhyayi-rules`
- `vishvasa-vedic-concordance`
- `dcs-sanskrit-repository-04e0778`
- `singh-fibonacci-1985`
- `plofker-mathematics-india-2009`
- `gray-nambudiri-recitation-1959`
- `neelakandhan-veda-kerala`
- `ignca-oral-tradition-vedas`
- `emeneau-india-linguistic-area-1956`
- `hock-substratum-rigvedic-sanskrit-1975`
- `kuiper-aryans-rigveda-1991`
- `mayrhofer-ewaia-1992-vol1`
- `cologne-mw-1899`
- `gretil-yaska-nirukta-2020`
- `sarup-nighantu-nirukta-1920-scan`
- `suryakanta-rktantram-1933-scan`

Open sources are retained locally when practical. Large scans use durable
repository identifiers and repository checksums. The registry marks the two
older licensed-book paths that could not be recovered rather than substituting
a catalogue page for the file actually inspected.

## Verification Outcome

All ten sampled notes now have one definition, at least one live deployment, no unresolved verification placeholder, and a source path that supports the attributed claim. Both full and short endnote assemblies completed successfully.

This audit also found an important secondary lesson: a note can remain technically sourced while the manuscript draws a stronger conclusion than the source permits. The Chapter 15 and Chapter 18 corrections came from checking the body claim and the note together rather than inspecting the bibliography alone.

## Files Revised

- `manuscript/as_1_00_seekers.md`
- `manuscript/as_1_03_strategic.md`
- `manuscript/as_1_13_preservation.md`
- `manuscript/as_1_15_aural.md`
- `manuscript/as_1_18_wrong_question.md`
- `manuscript/as_1_19_pie_in_sky.md`
- `manuscript/as_endnotes.md`

The pre-existing changes in `as_book.yaml` were not part of this audit.
