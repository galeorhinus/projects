# Endnote Verification Batch 004 — Asura and Māyā Evidence Lock

**Audit date:** 2026-09-02  
**Scope:** The primary-source chain supporting the revised Chapter 3 §3.6 distinction between lexical possibility, contextual action, and evidentiary uncertainty.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `yaska-asura-nirukta` | P0 | Corrected | Checked *Nirukta* 3.8 in Lakshman Sarup, p. 42, and against the GRETIL text. Yāska quotes the oppositional RV 10.53.4 passage and then offers the **असु (*asu*)**, breath, analysis. Removed the false attribution ***asurāḥ suravirodhinaḥ*** and made the evidentiary consequence explicit. |
| `samaveda-padapatha-asurasya-split` | P0 | Partial | Checked Sūrya Kānta's *Ṛktantram*, p. 54, and B. R. Sharma's Kauthuma edition, printed p. 161. Both record ***asurasya*** as ***a + surasya*** for Sāmaveda 1.78, corresponding to the praised *asura* of RV 7.6.1. The available online audio is Samhitapatha and cannot reveal the division. A direct Kauthuma Padapatha recitation is now logged in `as_verification_todo.md`; until then the claim must remain explicitly about the printed Padapatha. |
| `rigveda-privative-generativity` | P0 | Corrected | Reproduced the count against VedaWeb's Zurich annotation corpus, version 3: 48 rows under lemma ***ádabdha-*** and none under ***dabdha-***. Narrowed the claim to the positive participial stem because **⟪दभ्⟫** occurs elsewhere in other forms. Recorded the dataset version and matching file checksum. |
| `rigveda-adeva-privative` | P1 | Strengthened | Confirmed RV 6.17.8 in the VedaWeb v3 text: ***ádevo yád abhy aúhiṣṭa devā́n***. Added RV 8.96.9 from the local DCS text: ***asurā adevāḥ*** marks the opponents separately as ***a-devāḥ*** while leaving *asura* undivided. |
| `asura-generativity-pie-double-standard` | P0 | Strengthened | Located the recorded-*sura* objection in Wash Edward Hale, p. 24, where he endorses I. J. S. Taraporewala's account, and in the Sanskrit commentary on Sāmaveda 1.78. Reframed the body around the objection actually made: ***a-sura*** is treated as a later reanalysis because independent ***sura*** is absent from the Vedic corpus. |
| `rigvedic-named-antagonist-asuras` | P1 | Corrected | Checked the hostile and praised ranges against the VedaWeb data and Hale's occurrence study. Retained the action evidence for Pipru, Varcin, Namuci, and Svarbhānu while removing any implication that hostile context proves a privative lexical division. |
| `asura-academic-industry` | P1 | Verified | Counted the named positions in Hale's contents and checked the additional reviewers and etymologists in Chapter 1. The defensible floor is 42 distinct earlier scholars within Hale's survey. The body uses "more than forty" and the endnote states that this is a lower bound, not a total count. |
| `protagonist-sat-epithets` | P1 | Corrected | Removed the inference that Indra's praised RV 1.174.1 occurrence must be ***asu-ra***. The verse establishes that *asura* can describe an actor aligned with **सत् (*sat*)**; it does not determine the lexical division. |
| `deva-sur-div-radiance-field` | P2 | Parked | Its radiance evidence remains available, but the revised Chapter 3 no longer cites the note directly. Removed the stale deployment rather than forcing the evidence back into the body. |

## Principal Sources Checked

- Yāska, *Nirukta* 3.8, in Lakshman Sarup, *The Nighaṇṭu and the Nirukta* (Oxford University Press, 1920), p. 42; GRETIL electronic text.
- Sūrya Kānta, ed., *Ṛktantram: A Prātiśākhya of the Sāmaveda* (1933), p. 54, scanned edition at the Internet Archive.
- Antje Casaretto et al., *The morphologically glossed Rigveda — The Zurich annotation corpus revised and extended*, version 3 (2024), Zenodo record 21527084; `vedaweb_zurich.xlsx`, MD5 `cafa0415fde0a8a9232069a7de234e00`.
- Wash Edward Hale, *Ásura- in Early Vedic Religion* (Motilal Banarsidass, 1986), p. 24 and the complete Rigvedic occurrence survey.
- I. J. S. Taraporewala, "Some Vedic Words Viewed in the Light of the Gathas and Other Avesta Texts," *Journal of the Bombay Branch of the Royal Asiatic Society* 26 (1951), p. 123, as cited by Hale.

## Digital Evidence Records

The exact URLs, archive identifiers, local paths, and checksums are registered
in [the digital source registry](../../40_reference/sources/as_source_registry.md)
under these stable IDs:

- `gretil-yaska-nirukta-2020`
- `sarup-nighantu-nirukta-1920-scan`
- `suryakanta-rktantram-1933-scan`
- `sharma-samaveda-kauthuma-2000`
- `samaveda-1-78-digital`
- `vedaweb-zurich-v3`
- `vedaweb-tei-f9757556`
- `dcs-sanskrit-repository-04e0778`
- `hale-asura-1986-scan`
- `jamison-brereton-rigveda-2014-dcs`
- `rigveda-online-griffith`

The VedaWeb v3 dataset and GRETIL XML are retained locally. Large scans held by
the Internet Archive are represented by durable item identifiers and repository
checksums rather than duplicated in Git. The Taraporewala article was not
consulted directly; the batch encountered it through Hale, and the registry
records that limit instead of assigning it an unverified digital URL.

## Outcome

The evidence sustains two analyses but does not permit them to be assigned by moral role. Yāska's life-breath analysis appears beside an oppositional passage, while the Kauthuma privative division appears beside a praised passage. Chapter 3 now states that limit directly. The privative-generativity evidence establishes that ***a-sura*** remains possible even though independent ***sura*** is absent; it does not claim to prove the lexical identity of any Rigvedic occurrence.

## Required Completion Tests

1. Regenerate and check the master ledger.
2. Verify all live Chapter 3 markers have definitions.
3. Run the manuscript terminology audit for categorical ***asu-ra / a-sura*** assignments.
4. Run `python3 working/tools/source_registry_check.py`.
5. Run `git diff --check`.
