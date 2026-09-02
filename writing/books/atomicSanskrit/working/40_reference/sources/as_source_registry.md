# Atomic Sanskrit Digital Source Registry

> **Purpose:** Permanent catalogue of the digital sources used to verify the
> manuscript and its endnotes. Endnotes refer to these records through hidden
> `SOURCE-RECORDS` blocks. This file and its archive paths do not enter any
> reader-facing build.

## Record Template

Copy this template for each source. The heading ID is stable and should not be
renamed after an endnote refers to it.

```markdown
### `stable-source-id`

- **Citation:** Author/editor, title, edition, publisher, year.
- **Source type:** Book / article / corpus / dataset / web page / image / audio.
- **Canonical locator:** DOI, catalogue identifier, text identifier, or edition.
- **Digital URL:** Exact URL used.
- **Archived URL:** Durable repository, DOI resolver, or web archive URL.
- **Accessed:** YYYY-MM-DD.
- **Local record:** `working/40_reference/sources/archive/...`
- **Integrity:** SHA-256; optionally repository-supplied checksum.
- **Rights/storage:** Public domain / open licence / metadata only / lawful excerpt.
- **Notes:** Version, transcription, search method, or limitations.
```

Use `Not applicable` when a field genuinely does not apply. Use `Pending
recovery` when an earlier verification pass did not preserve the information;
do not silently omit the gap.

## Registered Sources

### `gretil-yaska-nirukta-2020`

- **Citation:** Yāska, *Nirukta*, based on Lakshman Sarup's edition; electronic text entered by Munoe Tokunaga and M. Kobayashi; GRETIL TEI conversion, 2020-07-31.
- **Source type:** Primary-text electronic corpus.
- **Canonical locator:** GRETIL `sa_yAska-nirukta`; *Nirukta* 3.8.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_yAska-nirukta.htm
- **Archived URL:** https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_yAska-nirukta.xml
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/gretil-yaska-nirukta-2020/sa_yAska-nirukta.xml`
- **Integrity:** SHA-256 `94597de75a62d981f3c31f2bd6d9453c3a0b723cc9ce666f6bebf55fc4aedac7`.
- **Rights/storage:** CC BY-NC-SA 4.0 electronic text; archived locally.
- **Notes:** Used to check the Sanskrit text against Sarup's printed edition.

### `sarup-nighantu-nirukta-1920-scan`

- **Citation:** Lakshman Sarup, *The Nighaṇṭu and the Nirukta* (Oxford University Press, 1920).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `nighantuniruktao01saru`; *Nirukta* 3.8, printed p. 42.
- **Digital URL:** https://archive.org/details/nighantuniruktao01saru
- **Archived URL:** https://archive.org/details/nighantuniruktao01saru
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; durable repository record used.
- **Integrity:** Repository PDF MD5 `fc09eadcb0d5ecae7f8b9b8ff61688e6`; SHA-1 `fc7bbfd62d2ce271566242fe9d8c89d46fca6960`.
- **Rights/storage:** Public-domain scan; repository record retained instead of duplicating the 5.9 MB PDF.
- **Notes:** Printed pagination controls the citation; GRETIL supplies the searchable text.

### `suryakanta-rktantram-1933-scan`

- **Citation:** Sūrya Kānta, ed., *Ṛktantram: A Prātiśākhya of the Sāmaveda* (Mehar Chand Lachhman Das, 1933).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `ksu.rktantram0000sury`; printed p. 54, scan leaf `n81`.
- **Digital URL:** https://archive.org/details/ksu.rktantram0000sury/page/n81/mode/1up
- **Archived URL:** https://archive.org/details/ksu.rktantram0000sury
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; durable repository record used.
- **Integrity:** Repository PDF MD5 `66cf5862562c33c7dda00d21fc5600ad`; SHA-1 `1173720bba4e940e9c7e6c830c920b66bfea50c8`.
- **Rights/storage:** Public-domain scan; repository record retained instead of duplicating the 25.4 MB PDF.
- **Notes:** The cited page prints ***asurasya (= a | surasya)***.

### `sharma-samaveda-kauthuma-2000`

- **Citation:** B. R. Sharma, ed., *Sāmaveda Saṃhitā of the Kauthuma School, with Padapāṭha and the Commentaries of Mādhava, Bharatasvāmin and Sāyaṇa*, vol. 1, Harvard Oriental Series 57 (Harvard University Press, 2000).
- **Source type:** Copyrighted critical edition, digital scan consulted.
- **Canonical locator:** ISBN 0-674-00588-0; Sāmaveda 1.78, printed p. 161.
- **Digital URL:** https://www.ebharatisampat.in/pdfs/ebharati-pdf-1635578455Samavedhasamhitha2000.pdf
- **Archived URL:** Not available.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained in the repository.
- **Integrity:** SHA-256 of the consulted PDF `1dc9052a2ad890128cbb638f7b9a1d9e55daf320d6afaad9f40cbbbea87c92da`.
- **Rights/storage:** Copyrighted; metadata and checksum only.
- **Notes:** The Padapāṭha prints **असुरस्य । अ । सुरस्य**.

### `samaveda-1-78-digital`

- **Citation:** Online Sāmaveda 1.78 display containing Saṃhitāpāṭha, word separation, and audio.
- **Source type:** Web page and audio interface.
- **Canonical locator:** Sāmaveda 1.78.
- **Digital URL:** https://xn--j2b3a4c.com/samveda/78
- **Archived URL:** Not available.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/samaveda-1-78-digital/samveda-78.html`
- **Integrity:** SHA-256 `b7bf79652090ef2ebddb897388df627a87edebcd77808ec3480d934b451e05f6`.
- **Rights/storage:** Web-page research capture; audio not copied.
- **Notes:** The available audio is joined Saṃhitāpāṭha and cannot verify the Padapāṭha division.

### `vedaweb-zurich-v3`

- **Citation:** Antje Casaretto et al., *The Morphologically Glossed Rigveda: The Zurich Annotation Corpus Revised and Extended*, version 3 (2024), hosted by VedaWeb.
- **Source type:** Open research dataset.
- **Canonical locator:** DOI 10.5281/zenodo.21527084; Zenodo record 21527084.
- **Digital URL:** https://zenodo.org/records/21527084/files/vedaweb_zurich.xlsx?download=1
- **Archived URL:** https://doi.org/10.5281/zenodo.21527084
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/datasets/vedaweb-zurich-v3/vedaweb_zurich.xlsx`
- **Integrity:** SHA-256 `5b85de05564b83e98f9a48838bdf8a841e2228e37cd719852a71e8ad6f0f7513`; repository MD5 `cafa0415fde0a8a9232069a7de234e00`.
- **Rights/storage:** Open research dataset; exact file archived locally.
- **Notes:** Used for the ***ádabdha- / dabdha-*** count and verse-level morphological checks.

### `vedaweb-tei-f9757556`

- **Citation:** VedaWeb 1.0 TEI Rigveda corpus.
- **Source type:** Open electronic corpus.
- **Canonical locator:** DOI 10.5281/zenodo.4601264; source commit `f9757556fad27b0aa927c581427643f12d352bbb`.
- **Digital URL:** https://doi.org/10.5281/zenodo.4601264
- **Archived URL:** https://zenodo.org/records/4601264
- **Accessed:** Earlier analysis; exact date pending recovery.
- **Local record:** The reproducible query script remains at `analysis/asura/count_rigvedic_deva.py`.
- **Integrity:** Source commit recorded above; local corpus checksum pending recovery.
- **Rights/storage:** Open corpus; no new duplicate created.
- **Notes:** Used by the parked `deva-sur-div-radiance-field` note for the exact ***deva*** lemma count.

### `dcs-sanskrit-repository-04e0778`

- **Citation:** Oliver Hellwig, *Sanskrit Text Repository*, local repository snapshot.
- **Source type:** Electronic Sanskrit corpus and morphological dataset.
- **Canonical locator:** Git commit `04e0778d3dc971030229179e25eea043d06ff397`.
- **Digital URL:** https://github.com/OliverHellwig/sanskrit/tree/04e0778d3dc971030229179e25eea043d06ff397
- **Archived URL:** Same immutable Git commit.
- **Accessed:** 2026-09-02.
- **Local record:** `analysis/ganah/data/raw/dcs/`
- **Integrity:** RV 6.17 file SHA-256 `5a8190f23c343ff4118bdfd9270246804aa3f1cae04905b6151a7294593eb4be`; RV 8.96 file SHA-256 `64522fd6d2ac6a127cd6290c51a622c6e90566bfa133b574ec8020fa66649162`.
- **Rights/storage:** Existing local Git snapshot; no duplicate created.
- **Notes:** Used for exact verse-level forms and local DCS metadata.

### `hale-asura-1986-scan`

- **Citation:** Wash Edward Hale, *Ásura- in Early Vedic Religion* (Motilal Banarsidass, 1986).
- **Source type:** Copyrighted monograph, digital scan consulted.
- **Canonical locator:** Internet Archive item `MXPE_asura-in-early-vedic-religion-by-wash-edward-hale-motilal-banarsidass-delhi`; ARK `ark:/13960/s2q1nrpgb05`.
- **Digital URL:** https://archive.org/details/MXPE_asura-in-early-vedic-religion-by-wash-edward-hale-motilal-banarsidass-delhi
- **Archived URL:** Same Internet Archive item.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained in the repository.
- **Integrity:** Repository PDF MD5 `9b9dbce0efba4bcce27e4b420700833d`.
- **Rights/storage:** Copyrighted monograph; metadata and repository locator only.
- **Notes:** Used at p. 24, pp. ix-xv, pp. 1-37, and for the complete occurrence survey. Taraporewala 1951 p. 123 was encountered through Hale and was not independently consulted.

### `ut-rigveda-metrically-restored`

- **Citation:** Barend A. van Nooten and Gary B. Holland, *Rig Veda: A Metrically Restored Text with an Introduction and Notes* (Harvard University Press, 1994); online edition revised by Karen Thomson and Jonathan Slocum, University of Texas Linguistics Research Center.
- **Source type:** Institutional electronic primary-text edition.
- **Canonical locator:** Harvard Oriental Series 50; Rigvedic mantra number.
- **Digital URL:** https://lrc.la.utexas.edu/books/rigveda/RV00
- **Archived URL:** Not available.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ut-rigveda-metrically-restored/`
- **Integrity:** SHA-256: RV00 `f8da518fe2bb195a3388a2d87d3af7f077a0259b34a9e269dd3ab38a8868568f`; RV01 `fef667cf7f98c91d6d32e6d312d956be2f9dee5a6d58153f70e1e9bcc4072132`; RV05 `b29ae3f130617969c8e3da0d9905de6a4f27d22a07817493f4978251f45c588f`; RV08 `e77c60e34c1cbdd516252639c0e9cc3615a4999e97cd7d5894d8dd82d118d8fa`; RV10 `1516b3413a3e20b945a461d579748c708091ad9aeef75ffa26bd8a13102e924b`.
- **Rights/storage:** Research-use HTML pages retained locally; source page states non-commercial research use.
- **Notes:** Exact book URLs are the base URL followed by `RV01`, `RV05`, `RV08`, or `RV10`.

### `jamison-brereton-rigveda-2014-dcs`

- **Citation:** Stephanie W. Jamison and Joel P. Brereton, *The Rigveda: The Earliest Religious Poetry of India*, 3 vols. (Oxford University Press, 2014).
- **Source type:** Copyrighted translation in an existing local aligned-text snapshot.
- **Canonical locator:** ISBN 9780199370184; Rigvedic mantra number.
- **Digital URL:** https://github.com/OliverHellwig/sanskrit/blob/04e0778d3dc971030229179e25eea043d06ff397/translations/RV-Jamison%2C%20Brereton.csv
- **Archived URL:** Immutable Git commit URL above.
- **Accessed:** 2026-09-02.
- **Local record:** `analysis/ganah/data/raw/dcs/translations/RV-Jamison, Brereton.csv`
- **Integrity:** SHA-256 `03742267076d9152d917a6eda712210e03dbe53c182040a1eaea4b2fba535647`.
- **Rights/storage:** Existing local research corpus; no new copy created.
- **Notes:** Used to compare translations at the exact mantra locations named in Batches 004 and 005.

### `cologne-mw-1899`

- **Citation:** Monier Monier-Williams, *A Sanskrit-English Dictionary* (Clarendon Press, 1899), Cologne Digital Sanskrit Dictionaries edition.
- **Source type:** Searchable dictionary and scanned page interface.
- **Canonical locator:** Cologne dictionary code `MW`; dictionary headword.
- **Digital URL:** https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc2/index.php
- **Archived URL:** https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/webtc/download.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/cologne-mw-1899/index.html`
- **Integrity:** SHA-256 `c89401e53d34feadc69e8f8e325e09b355259da447045e9c87e61e196ca2cc11`.
- **Rights/storage:** Search-interface capture retained; project offers the digitization under its stated terms.
- **Notes:** Batch 005 checked the headwords ***svar***, ***bhānu***, ***Svarbhānu***, ***lakṣmī***, and ***paśu***.

### `sanskritdocuments-rigveda-10`

- **Citation:** SanskritDocuments, Rigveda Maṇḍala 10 electronic text.
- **Source type:** Electronic primary-text display.
- **Canonical locator:** Rigveda Maṇḍala 10; mantra number.
- **Digital URL:** https://sanskritdocuments.org/doc_veda/r10.html
- **Archived URL:** Not available.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/sanskritdocuments-rigveda-10/r10.html`
- **Integrity:** SHA-256 `55052d4a1d2509e4228d7b90fe87e55cab1a39e7e0d9f37f94aab3bb45ad8252`.
- **Rights/storage:** Web-page research capture.
- **Notes:** Used as an additional check on RV 10.71.4 and RV 10.125.

### `ashtadhyayi-1-1-9-digital`

- **Citation:** Digital displays of the *Siddhāntakaumudī* and *Laghusiddhāntakaumudī* explanations of Aṣṭādhyāyī 1.1.9, **तुल्यास्यप्रयत्नं सवर्णम्**.
- **Source type:** Digital grammatical commentary.
- **Canonical locator:** Aṣṭādhyāyī 1.1.9.
- **Digital URL:** https://ashtadhyayi.com/sutraani/1/1/9
- **Archived URL:** https://ashtadhyayi-lite.github.io/sutra/1.1.9.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ashtadhyayi-1-1-9/`
- **Integrity:** SHA-256: ashtadhyayi.com `f762a0664e93d4ffa2ba557bfebb68bfa1f46171281352c34487cf5dfbf54a98`; static corroborating page `b1a168069f6fdb92f6ef5574399d92eb7a7b21225c1aded0061eecdba8a29b0e`.
- **Rights/storage:** Web-page research captures.
- **Notes:** Both pages display **ऋटुरषाणां मूर्धा** in the articulation list.

### `macdonell-sarvanukramani-1886-scan`

- **Citation:** Kātyāyana, *Sarvānukramaṇī of the Rigveda*, ed. A. A. Macdonell (Clarendon Press, 1886).
- **Source type:** Public-domain critical-edition scan.
- **Canonical locator:** Internet Archive item `katyayanassarvan00katy`.
- **Digital URL:** https://archive.org/details/katyayanassarvan00katy
- **Archived URL:** https://archive.org/details/katyayanassarvan00katy
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; durable repository record used.
- **Integrity:** Repository PDF MD5 `5d01917047f9cb3e68dd203e85647ff9`; SHA-1 `6ec6bf237871d5c2f5ad5adfacd24c396f87c26e`.
- **Rights/storage:** Public-domain scan; repository record retained instead of duplicating the 24.7 MB PDF.
- **Notes:** Used for the received Vāgāmbhṛṇī seer classification attached to RV 10.125.

### `rigveda-online-griffith`

- **Citation:** Ralph T. H. Griffith, *The Hymns of the Rigveda*, digital verse display.
- **Source type:** Public-domain translation interface.
- **Canonical locator:** Rigvedic mantra number.
- **Digital URL:** https://rigveda-online.github.io/
- **Archived URL:** https://github.com/rigveda-online/rigveda-online.github.io
- **Accessed:** Earlier analysis; exact date pending recovery.
- **Local record:** Not retained.
- **Integrity:** Pending source-commit recovery.
- **Rights/storage:** Public-domain translation; metadata only.
- **Notes:** Used only as a translation cross-check in `protagonist-sat-epithets`.

### `vhp-upanishads`

- **Citation:** Government of India, Vedic Heritage Portal, “Upanishads,” section “Nature of Upanishads.”
- **Source type:** Government web page.
- **Canonical locator:** Vedic Heritage Portal, Upanishads overview.
- **Digital URL:** https://vedicheritage.gov.in/upanishads/
- **Archived URL:** Not available.
- **Accessed:** 2026-09-01; availability rechecked 2026-09-02.
- **Local record:** Not retained; the host did not resolve during the archive pass.
- **Integrity:** Not applicable.
- **Rights/storage:** Government web source; exact URL retained.
- **Notes:** Used for the portal's definition of *Vedānta* as conclusion and goal and its adjacent chronological statement.

### `gita-supersite-15-15`

- **Citation:** Bhagavad Gītā 15.15, Gītā Supersite, Indian Institute of Technology Kanpur.
- **Source type:** Institutional primary-text interface.
- **Canonical locator:** Bhagavad Gītā 15.15.
- **Digital URL:** https://www.gitasupersite.iitk.ac.in/srimad?choose=1&etadi=1&etgb=1&etpurohit=1&etsiva=1&etssa=1&field_chapter_value=15&field_nsutra_value=15&language=dv&show_mool=1
- **Archived URL:** https://www.gitasupersite.iitk.ac.in/
- **Accessed:** 2026-09-01; availability rechecked 2026-09-02.
- **Local record:** Not retained; the server returned an empty response during the archive pass.
- **Integrity:** Not applicable.
- **Rights/storage:** Institutional web source; exact query URL retained.
- **Notes:** Corroborates the semantic use of ***vedānta***; it does not establish textual chronology.

### `aurobharati-devi-mahatmya-8`

- **Citation:** *Devī Māhātmya*, chapter 8, verses 41–57, AuroBharati digital presentation.
- **Source type:** Primary-text web page.
- **Canonical locator:** *Devī Māhātmya* 8.41–57; *Mārkaṇḍeya Purāṇa* 88.
- **Digital URL:** https://devimahatmyam.aurobharati.in/devimahatmyam/episode-3/chapter-8/
- **Archived URL:** Not available.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/aurobharati-devi-mahatmya-8/page.html`
- **Integrity:** SHA-256 `fe579592cce416f7d588190223afac01e2477f19dc0111bfa5d30a2072dfce76`.
- **Rights/storage:** Research-use HTML capture.
- **Notes:** Used for the Raktabīja multiplication sequence.

### `vishvasa-mahabhashya-paspashahnika`

- **Citation:** Patañjali, *Vyākaraṇa-Mahābhāṣya*, *Paspaśāhnika*, digital text based on the Kielhorn edition.
- **Source type:** Primary-text web page.
- **Canonical locator:** Kielhorn, vol. 1, p. 5, line 24 and following.
- **Digital URL:** https://vishvasa.github.io/sanskrit/vyAkaraNam/pANinIyam/mUlAni/mahA-bhAShyam/sarva-prastutiH/01_paspashAhnikam/03_nirmANa-rItiH/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vishvasa-mahabhashya-paspashahnika/page.html`
- **Integrity:** SHA-256 `5eac2aa6aabeafc351408ce271d1a797f44cab295a55db08ce005a320fc25e34`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for Bṛhaspati's thousand-divine-year word-list account and Patañjali's general-rule/exception response.

### `joshi-roodbergen-paspashahnika-1968`

- **Citation:** S. D. Joshi and J. A. F. Roodbergen, *Patañjali's Vyākaraṇa-Mahābhāṣya: Paspaśāhnika* (University of Poona, 1968).
- **Source type:** Copyrighted scholarly book.
- **Canonical locator:** pp. 74–77.
- **Digital URL:** Pending recovery; the earlier audit did not preserve the exact licensed scan URL.
- **Archived URL:** Not available.
- **Accessed:** 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; citation metadata only.
- **Notes:** Used as a translation and interpretation check against the Kielhorn Sanskrit text.

### `vhp-rigveda-10-71`

- **Citation:** Government of India, Vedic Heritage Portal, Śākala Saṃhitā presentation of Ṛgveda 10.71.
- **Source type:** Government primary-text web page.
- **Canonical locator:** Ṛgveda 10.71.
- **Digital URL:** https://vedicheritage.gov.in/samhitas/rigveda/shakala-samhita/rigveda-shakala-samhita-mandal-10-sukta-071/
- **Archived URL:** Not available.
- **Accessed:** 2026-09-01; availability rechecked 2026-09-02.
- **Local record:** Not retained; the host did not resolve during the archive pass.
- **Integrity:** Not applicable.
- **Rights/storage:** Government web source; exact URL retained.
- **Notes:** Used for the received ṛṣi/devatā metadata and accented hymn text.

### `biblegateway-leviticus-25-nrsvue`

- **Citation:** *Leviticus* 25.44–46, New Revised Standard Version Updated Edition, BibleGateway.
- **Source type:** Copyrighted scripture translation interface.
- **Canonical locator:** Leviticus 25.44–46; NRSVUE.
- **Digital URL:** https://www.biblegateway.com/passage/?search=Leviticus+25%3A44-46&version=NRSVUE
- **Archived URL:** Not available.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/biblegateway-leviticus-25-nrsvue/page.html`
- **Integrity:** SHA-256 `25b61e140e1cd378490629c965167c1cbd513a2f3774837e3ab183c09c62f552`.
- **Rights/storage:** Narrow research-use web capture; translation remains copyrighted.
- **Notes:** Used only for the passage's acquisition, property, inheritance, and Israelite/foreigner distinction.

### `sefaria-leviticus-25-jps`

- **Citation:** *Leviticus* 25.44–46, Jewish Publication Society Tanakh, Sefaria text API.
- **Source type:** Scripture translation dataset.
- **Canonical locator:** Leviticus 25.44–46; JPS 1985.
- **Digital URL:** https://www.sefaria.org/api/v3/texts/Leviticus.25.44-46?version=primary
- **Archived URL:** https://www.sefaria.org/Leviticus.25.44-46
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/sefaria-leviticus-25/text.json`
- **Integrity:** SHA-256 `3a2c7db12380e2d312d742ea87d0f04177682ff71021411e3585a39fc70cf394`.
- **Rights/storage:** API research capture under Sefaria's stated terms.
- **Notes:** Translation cross-check for the same passage.

### `milgrom-leviticus-23-27-2001`

- **Citation:** Jacob Milgrom, *Leviticus 23–27: A New Translation with Introduction and Commentary*, Anchor Yale Bible 3B (Doubleday, 2001).
- **Source type:** Copyrighted scholarly book.
- **Canonical locator:** ISBN 9780300139419; commentary on Leviticus 25.44–46.
- **Digital URL:** https://yalebooks.yale.edu/book/9780300139419/leviticus-23-27/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; publisher metadata only.
- **Notes:** Used for the jubilee-law distinction between Israelite debt service and permanently held foreign slaves.

### `vishvasa-rigveda-pratisakhya`

- **Citation:** *Ṛgveda-Prātiśākhya*, digital presentation.
- **Source type:** Primary-text web page.
- **Canonical locator:** 1.11–12.
- **Digital URL:** https://vishvasa.github.io/sanskrit/shixA/granthAH/Rg-vedaH/prAtishAkhyam/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vishvasa-rigveda-pratisakhya/page.html`
- **Integrity:** SHA-256 `0f2ce25e958b1f9624fc76d21ad43a99282affc3073e87b15b6de28ce50d451f`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for intervocalic **ड → ळ** and **ढ → ळ्ह**, including the printed examples.

### `scharf-hyman-linguistic-encoding-sanskrit`

- **Citation:** Peter M. Scharf and Malcolm D. Hyman, *Linguistic Issues in Encoding Sanskrit* (Sanskrit Library).
- **Source type:** Open scholarly report.
- **Canonical locator:** Discussion of the complementary distribution of Ṛgvedic **ळ/ळ्ह** and **ड/ढ**.
- **Digital URL:** https://www.sanskritlibrary.org/Sanskrit/pub/lies_sl.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/scharf-hyman-linguistic-encoding-sanskrit/original.pdf`
- **Integrity:** SHA-256 `a07748c1cb729b2d37d77ca27296ac3002d87c70b7ba0c6a8c7549088266d769`.
- **Rights/storage:** Publicly distributed scholarly PDF; archived locally.
- **Notes:** Corroborating phonological description for `agnimile-rigveda-opening`.

### `sanskritdocuments-ashtadhyayi-rules`

- **Citation:** Pāṇini, *Aṣṭādhyāyī*, SanskritDocuments explanatory displays with Kāśikā and Nyāsa material.
- **Source type:** Digital primary text and commentary.
- **Canonical locator:** 2.4.75 and 6.1.10.
- **Digital URL:** https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya/2/2.4.75.htm
- **Archived URL:** https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya/6/6.1.10.htm
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/sanskritdocuments-ashtadhyayi-rules/`
- **Integrity:** SHA-256: 2.4.75 `6caf94353423a732cc33818279fc04949115050d8e39df86968ee5f88d5738b6`; 6.1.10 `2591a5c285f13096544ec2c14ac2217c5a48ceeeafed83c8704ebc317a5ea03a`.
- **Rights/storage:** Web-page research captures.
- **Notes:** Separates the **śap → ślu** replacement from reduplication.

### `vishvasa-vedic-concordance`

- **Citation:** Digital Vedic word concordance, Vishvasa Sanskrit repository.
- **Source type:** Primary-text concordance web page.
- **Canonical locator:** Ṛgveda 1.66.2d, alternatively indexed as half-verse 1.66.4.
- **Digital URL:** https://vishvasa.github.io/vedAH/vaidika-padAnukrama-koshaH/08/10_8.10/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vishvasa-vedic-concordance/page.html`
- **Integrity:** SHA-256 `19d18528f30e6c76797f8985a13d11086395e8db03c4606d69ff0d3c45b78ff8`.
- **Rights/storage:** Web-page research capture.
- **Notes:** Resolves the two numbering conventions for the **dadhāti** line.

### `singh-fibonacci-1985`

- **Citation:** Parmanand Singh, “The So-called Fibonacci Numbers in Ancient and Medieval India,” *Historia Mathematica* 12.3 (1985): 229–244.
- **Source type:** Scholarly article PDF.
- **Canonical locator:** pp. 233–235.
- **Digital URL:** https://www.cs.cornell.edu/courses/JavaAndDS/files/Singh-so-called-Fibs.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/singh-fibonacci-1985/original.pdf`
- **Integrity:** SHA-256 `f6de76859b37d68f7ba38fd0974721d95e8d23ece88325851ab255a23c414ad0`.
- **Rights/storage:** Publicly distributed research PDF; archived locally.
- **Notes:** Used to distinguish Piṅgala's combinatorial frame from Virahāṅka's explicit additive recurrence.

### `plofker-mathematics-india-2009`

- **Citation:** Kim Plofker, *Mathematics in India* (Princeton University Press, 2009).
- **Source type:** Copyrighted scholarly book.
- **Canonical locator:** ISBN 9780691120676; JSTOR book ID `j.ctt7s03d`.
- **Digital URL:** https://www.jstor.org/stable/j.ctt7s03d
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; stable catalogue/full-text platform record only.
- **Notes:** Corroborating source for Sanskrit prosody and combinatorics.

### `gray-nambudiri-recitation-1959`

- **Citation:** J. E. B. Gray, “An Analysis of Nambudiri Ṛgvedic Recitation and the Nature of the Vedic Accent,” *Bulletin of the School of Oriental and African Studies* 22.3 (1959): 499–530.
- **Source type:** Copyrighted scholarly article.
- **Canonical locator:** DOI 10.1017/S0041977X00065551.
- **Digital URL:** https://doi.org/10.1017/S0041977X00065551
- **Archived URL:** Same DOI.
- **Accessed:** 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; DOI metadata only.
- **Notes:** Used for the 1957 Nambūdiri recordings and analysis, not for cross-lineage identity.

### `neelakandhan-veda-kerala`

- **Citation:** C. M. Neelakandhan, “Oral and Textual Traditions of Veda in Kerala,” Vedic Heritage Portal.
- **Source type:** Government-hosted scholarly PDF.
- **Canonical locator:** Kerala Vedic traditions survey.
- **Digital URL:** https://vedicheritage.gov.in/pdf/Oral_Textual_Traditions_Veda_Kerala.pdf
- **Archived URL:** Not available.
- **Accessed:** 2026-09-01; availability rechecked 2026-09-02.
- **Local record:** Not retained; the host did not resolve during the archive pass.
- **Integrity:** Pending recovery.
- **Rights/storage:** Government-hosted source; exact URL retained.
- **Notes:** Used for named branch-specific oral and textual traditions in Kerala.

### `ignca-oral-tradition-vedas`

- **Citation:** Indira Gandhi National Centre for the Arts, *Oral Tradition of the Vedas*, Ministry of Culture UNESCO-submission catalogue.
- **Source type:** Government institutional PDF.
- **Canonical locator:** catalogue pp. 1–2.
- **Digital URL:** https://ignca.gov.in/wp-content/uploads/2015/10/media_centre_dvds.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ignca-oral-tradition-vedas/original.pdf`
- **Integrity:** SHA-256 `fcf5bd1e67d0eeaa2799a450a2fc1a812ad89b1754348ce3ecc2d87e714984c3`.
- **Rights/storage:** Government publication; archived locally.
- **Notes:** Records the geographic and branch range of Vedic recitation traditions.

### `emeneau-india-linguistic-area-1956`

- **Citation:** Murray B. Emeneau, “India as a Linguistic Area,” *Language* 32.1 (1956): 3–16.
- **Source type:** Scholarly article PDF.
- **Canonical locator:** pp. 5–6; JSTOR stable ID 410649.
- **Digital URL:** https://eemaata.com/books/India%20as%20a%20Linguistic%20Area%20-%20Emeneau.pdf
- **Archived URL:** https://www.jstor.org/stable/410649
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/emeneau-india-linguistic-area-1956/original.pdf`
- **Integrity:** SHA-256 `3a8a229cfe40a5ba0bd68b4e1d2b614b8f580dae3b72eeae162bd2b534e35515`.
- **Rights/storage:** Narrow research copy of a publicly distributed PDF.
- **Notes:** Used to state the classic linguistic-area account of retroflexion.

### `hock-substratum-rigvedic-sanskrit-1975`

- **Citation:** Hans Henrich Hock, “Substratum Influence on (Rig-Vedic) Sanskrit?” *Studies in the Linguistic Sciences* 5.2 (1975): 76–125.
- **Source type:** Institutional-repository article record.
- **Canonical locator:** Illinois IDEALS item 26708.
- **Digital URL:** https://www.ideals.illinois.edu/items/26708
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-01; archive attempted 2026-09-02.
- **Local record:** Not retained; the repository denied the automated capture.
- **Integrity:** Not applicable.
- **Rights/storage:** Institutional repository record; no copied article.
- **Notes:** Used for alternatives to a single uniform retroflex-substrate account.

### `kuiper-aryans-rigveda-1991`

- **Citation:** F. B. J. Kuiper, *Aryans in the Rigveda*, Leiden Studies in Indo-European 1 (Rodopi, 1991).
- **Source type:** Copyrighted scholarly book.
- **Canonical locator:** ISBN 9789051833072; eISBN 9789401200226.
- **Digital URL:** https://www.degruyterbrill.com/document/isbn/9789401200226/html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; publisher metadata only.
- **Notes:** One representative source for contact/substrate explanations; the endnote does not treat it as the only account.

### `mayrhofer-ewaia-1992-vol1`

- **Citation:** Manfred Mayrhofer, *Etymologisches Wörterbuch des Altindoarischen*, vol. 1 (Carl Winter, 1992).
- **Source type:** Copyrighted scholarly dictionary.
- **Canonical locator:** pp. 147–148, s.v. ***ásura-***; ISBN 9783533038269.
- **Digital URL:** Pending recovery; the earlier audit did not preserve the exact consulted scan URL.
- **Archived URL:** https://glottolog.org/resource/reference/id/471451
- **Accessed:** 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; catalogue metadata only.
- **Notes:** The audit recorded Mayrhofer's lord/king proposal and kept it separate from Sanskrit's internal analyses.

### `schleicher-fable-1868-jstor`

- **Citation:** August Schleicher, “Eine Fabel in indogermanischer Ursprache,” *Beiträge zur vergleichenden Sprachforschung* 5.2 (1868): 206–208.
- **Source type:** Public-domain journal article in a stable scan repository.
- **Canonical locator:** JSTOR stable ID 23458804.
- **Digital URL:** https://www.jstor.org/stable/23458804
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-01.
- **Local record:** Not retained; stable repository page images used.
- **Integrity:** Not available from the repository interface.
- **Rights/storage:** Public-domain text; repository locator retained rather than copying page images.
- **Notes:** The original typography confirms that the forms in the connected text are not each preceded by an asterisk.

### `robins-history-linguistics-1997`

- **Citation:** R. H. Robins, *A Short History of Linguistics*, 4th ed. (Longman, 1997).
- **Source type:** Copyrighted scholarly book.
- **Canonical locator:** p. 179; ISBN 9780582249943.
- **Digital URL:** https://www.routledge.com/A-Short-History-of-Linguistics/Robins/p/book/9780582249943
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02; text consulted in the earlier audit on 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; publisher metadata only.
- **Notes:** The exact licensed file URL used to inspect p. 179 was not preserved; the page credits Schleicher with initiating the asterisk practice.

### `morpurgo-davies-nineteenth-century-1998`

- **Citation:** Anna Morpurgo Davies, *Nineteenth-Century Linguistics*, vol. 4 of *History of Linguistics* (Longman, 1998).
- **Source type:** Copyrighted scholarly book.
- **Canonical locator:** pp. 167 and 185; ISBN 9780582294783.
- **Digital URL:** https://www.routledge.com/History-of-Linguistics-Volume-IV-Nineteenth-Century-Linguistics/Davies-Lepschy/p/book/9780582294783
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02; text consulted in the earlier audit on 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; publisher metadata only.
- **Notes:** The exact licensed file URL was not preserved. The cited pages document the conventional Schleicher attribution and earlier uses by Pott, Gabelentz, and Loebe.

### `shields-s-mobile-1996`

- **Citation:** Kenneth Shields Jr., “Indo-European S-Mobile and Indo-European Morphology,” *Emerita* 64.2 (1996): 250–254.
- **Source type:** Open-access scholarly article.
- **Canonical locator:** DOI 10.3989/emerita.1996.v64.i2.227.
- **Digital URL:** https://emerita.revistas.csic.es/index.php/emerita/article/download/227/228
- **Archived URL:** https://doi.org/10.3989/emerita.1996.v64.i2.227
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/shields-s-mobile-1996/original.pdf`
- **Integrity:** SHA-256 `ebc96aa42619774120ef1d0d1545a9984214fc645e838904b52d5e379d65d01a`.
- **Rights/storage:** CC BY 4.0 publisher PDF; archived locally.
- **Notes:** Used at pp. 249–250 and 253 in the journal pagination.

### `clackson-ie-linguistics-2007`

- **Citation:** James Clackson, *Indo-European Linguistics: An Introduction* (Cambridge University Press, 2007).
- **Source type:** Copyrighted scholarly book.
- **Canonical locator:** pp. 67–70; ISBN 9780521653671.
- **Digital URL:** https://books.google.com/books?id=DJDjNp6wODoC
- **Archived URL:** https://assets.cambridge.org/97805216/53138/frontmatter/9780521653138_frontmatter.pdf
- **Accessed:** 2026-09-02; text consulted in the earlier audit on 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; bibliographic and preview records only.
- **Notes:** Used for the objection that reconstructed root extensions often have no identifiable function.

### `pokorny-iew-1959-vol1`

- **Citation:** Julius Pokorny, *Indogermanisches etymologisches Wörterbuch*, vol. 1 (Francke, 1959).
- **Source type:** Book scan in a durable repository.
- **Canonical locator:** Internet Archive item `indogermanisches01pokouoft`; pp. 938–945.
- **Digital URL:** https://archive.org/details/indogermanisches01pokouoft
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/internet-archive-metadata/indogermanisches01pokouoft.json`
- **Integrity:** Repository PDF MD5 `c3d513a2bb5e2a8f554ba8979fb39a8d`; SHA-1 `cc5bcdbdfdd4b91ce4ea30045f3e72d9cc5fa5a4`.
- **Rights/storage:** Repository scan; metadata retained instead of duplicating the 33 MB PDF.
- **Notes:** Used for the *(s)ker-* family and extended forms.

### `ashtadhyayi-rule-cluster-digital`

- **Citation:** Pāṇini, *Aṣṭādhyāyī*, digital sūtra and Dhātupāṭha displays at Ashtadhyayi.com.
- **Source type:** Digital primary-text and commentary interface.
- **Canonical locator:** 1.4.14; 6.1.135, 6.1.137–139; 7.3.79; Dhātupāṭha 6.66.
- **Digital URL:** https://ashtadhyayi.com/sutraani/6/1/135
- **Archived URL:** https://ashtadhyayi.com/dhatu/06.0066
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ashtadhyayi-rule-cluster/`
- **Integrity:** All captured routes returned the same application shell, SHA-256 `f762a0664e93d4ffa2ba557bfebb68bfa1f46171281352c34487cf5dfbf54a98`.
- **Rights/storage:** Web-interface captures.
- **Notes:** Exact route URLs identify each rule. Because the local files contain only the shared application shell, they do not replace the live route or the independent SanskritDocuments/local-data checks.

### `project-dhatupatha-csv`

- **Citation:** *Atomic Sanskrit* machine-readable Dhātupāṭha base inventory.
- **Source type:** Project dataset.
- **Canonical locator:** base indices 03.0025, 04.0044, and 06.0066.
- **Digital URL:** Not applicable.
- **Archived URL:** Not applicable.
- **Accessed:** 2026-09-02.
- **Local record:** `analysis/dhatupatha/data/dhatupatha.csv`
- **Integrity:** SHA-256 `e491d6cd8c68e3fe455f57098ba6d6ad2762cf0882a74dd585aa45e636eb9d86`.
- **Rights/storage:** Project research dataset.
- **Notes:** The base indices are project identifiers, not universal printed-entry numbers.

### `chambers-etymological-dictionary-1872-scan`

- **Citation:** James Donald, ed., *Chambers's Etymological Dictionary of the English Language* (W. & R. Chambers, 1872).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `chamberssetymolo00donarich`; title page and pp. 281–282.
- **Digital URL:** https://archive.org/details/chamberssetymolo00donarich
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/internet-archive-metadata/chamberssetymolo00donarich.json`
- **Integrity:** Repository PDF MD5 `fe9f1d94e945e674654c392697e5234e`; SHA-1 `9eda00807fd22ad700761ae2eddcc8db567d4f96`.
- **Rights/storage:** Public-domain scan; repository metadata retained instead of duplicating the 81 MB PDF.
- **Notes:** Used for the *kin* and *king* entries and their unstarred Sanskrit termini.

### `skeat-etymological-dictionary-1882-scan`

- **Citation:** Walter W. Skeat, *An Etymological Dictionary of the English Language* (Clarendon Press, 1882).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `in.ernet.dli.2015.83588`; pp. 172, 255, and 729–745.
- **Digital URL:** https://archive.org/details/in.ernet.dli.2015.83588
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/internet-archive-metadata/in.ernet.dli.2015.83588.json`
- **Integrity:** Repository PDF MD5 `130af7a59c6f4e640cb6a96bb72c3e2b`; SHA-1 `a8fd6590a06a1b700ee590fd04b3b94dbd5bfef5`.
- **Rights/storage:** Public-domain scan; repository metadata retained instead of duplicating the 234 MB PDF.
- **Notes:** Used for the first-edition GENUS/CURT entries and “List of Aryan Roots.”

### `skeat-etymological-dictionary-1910-scan`

- **Citation:** Walter W. Skeat, *An Etymological Dictionary of the English Language*, new and revised ed. (Clarendon Press, 1910 printing).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `in.ernet.dli.2015.15880`; pp. 150, 287–288, and 751–758.
- **Digital URL:** https://archive.org/details/in.ernet.dli.2015.15880
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/internet-archive-metadata/in.ernet.dli.2015.15880.json`
- **Integrity:** Repository PDF MD5 `daab4cc1f0d23e581388b1689a98666d`; SHA-1 `91e1feeb3cc52870d8a5f0d16f8155f01ac81fbd`.
- **Rights/storage:** Public-domain scan; repository metadata retained instead of duplicating the 154 MB PDF.
- **Notes:** Used for the revised GENUS/CURT entries and “List of Indogermanic Roots.”

### `muller-science-language-second-series-1864-scan`

- **Citation:** Friedrich Max Müller, *Lectures on the Science of Language*, Second Series (Longman, Green, Longman, Roberts, & Green, 1864).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `s2lecturesonscie02mluoft`; title page and pp. 193, 218, 255–256.
- **Digital URL:** https://archive.org/details/s2lecturesonscie02mluoft
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/internet-archive-metadata/s2lecturesonscie02mluoft.json`
- **Integrity:** Repository PDF MD5 `2644b25756e29e07794434fadc9e64e2`; SHA-1 `377ee51f2015eb9b11e90ff062707c12a86f2cc4`.
- **Rights/storage:** Public-domain scan; repository metadata retained instead of duplicating the 47 MB PDF.
- **Notes:** The lectures were delivered in 1863 and published in 1864.

### `grassmann-rigveda-dictionary-1873`

- **Citation:** Hermann Grassmann, *Wörterbuch zum Rig-Veda* (F. A. Brockhaus, 1873).
- **Source type:** Public-domain dictionary digitization.
- **Canonical locator:** s.v. ***aja***, p. 19; s.v. ***asuratvá***, p. 156; BSB digital object `bsb11159221`.
- **Digital URL:** https://www.sanskrit-lexicon.uni-koeln.de/scans/GRAScan/2020/web/webtc/download.html
- **Archived URL:** https://www.digitale-sammlungen.de/en/details/bsb11159221
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/datasets/grassmann-rigveda-dictionary-1873/gratxt.zip`
- **Integrity:** SHA-256 `40d1a5bb434e194f11ec98e86e6be0d5419e81b7036e48b68eb8ea866a3b7c91`.
- **Rights/storage:** Cologne digitization archive; local text package retained.
- **Notes:** Used for the *aja* entries and the 24/22 ***asuratvá*** occurrence check.

### `aussant-homonymy-polysemy-2015`

- **Citation:** Émilie Aussant, “Sanskrit Theories on Homonymy and Polysemy,” *Bulletin d'Études Indiennes* 32 (2015): 13–36.
- **Source type:** Copyrighted scholarly article; author-uploaded record.
- **Canonical locator:** pp. 13–36.
- **Digital URL:** https://www.researchgate.net/publication/308359847_Sanskrit_Theories_on_Homonymy_and_Polysemy
- **Archived URL:** Not available.
- **Accessed:** 2026-09-02; text consulted in the earlier audit on 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; metadata only.
- **Notes:** Used for the ***ekaśabdadarśana / anekaśabdadarśana*** distinction.

### `eggeling-satapatha-vol44-1900`

- **Citation:** Julius Eggeling, trans., *The Śatapatha-Brāhmaṇa*, part 5, *Sacred Books of the East* 44 (Oxford University Press, 1900).
- **Source type:** Public-domain translation.
- **Canonical locator:** Śatapatha Brāhmaṇa 11.1.6.7–8; printed pp. 13–14.
- **Digital URL:** https://www.sacred-texts.com/hin/sbr/sbe44/sbe4405.htm
- **Archived URL:** https://archive.org/details/satapathabrahman02egge
- **Accessed:** 2026-09-01; availability rechecked 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/internet-archive-metadata/satapathabrahman02egge.json`
- **Integrity:** Repository PDF MD5 `0705f9f9bcbe58e8a10f012d73d529bb`; SHA-1 `2cf7b993df2af2084873ddec9747938af9debd9c`.
- **Rights/storage:** Public-domain scan; repository metadata retained instead of duplicating the 30 MB PDF.
- **Notes:** Supplies the later breath/light and darkness contrast, not a division of a Rigvedic word.

### `turner-cdial-1962`

- **Citation:** Ralph Lilley Turner, *A Comparative Dictionary of the Indo-Aryan Languages* (Oxford University Press, 1962–1966), Digital South Asia Library edition.
- **Source type:** Copyrighted searchable dictionary.
- **Canonical locator:** entry 4147, printed p. 222.
- **Digital URL:** https://dsal.uchicago.edu/dictionaries/soas/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/turner-cdial-1962/index.html`
- **Integrity:** SHA-256 `880dde21f7954f9e932ae275fe8f9943622c1771660d8c5b046cabbf90f53b4e`.
- **Rights/storage:** Interface capture only; dictionary text remains copyrighted.
- **Notes:** Used for Turner's historical placement of ***gāvī*** and the modern forms under entry 4147.

### `joshi-apadam-constraint-2009`

- **Citation:** Prasad P. Joshi, “A Glimpse into the Apadam-Constraint in the Tradition of Sanskrit Grammar,” in Gérard Huet, Amba Kulkarni, and Peter Scharf, eds., *Sanskrit Computational Linguistics* (Springer, 2009), 278–286.
- **Source type:** Copyrighted conference paper.
- **Canonical locator:** DOI 10.1007/978-3-642-00155-0_12.
- **Digital URL:** https://doi.org/10.1007/978-3-642-00155-0_12
- **Archived URL:** https://link.springer.com/chapter/10.1007/978-3-642-00155-0_12
- **Accessed:** 2026-09-02.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; DOI and publisher metadata only.
- **Notes:** Used for the later disciplinary formulation **अपदं न प्रयुञ्जीत**; the body claim rests on Aṣṭādhyāyī 1.4.14.

### `bhagavata-canto8-sanskrit`

- **Citation:** *Śrīmad Bhāgavata Purāṇa*, Skandha 8, Sanskrit electronic text.
- **Source type:** Primary-text web page.
- **Canonical locator:** 8.7.1–43, 8.8.33–46, and 8.9.19–26.
- **Digital URL:** https://srimadbhagavatam.org/downloads/SB-Sanskrit/SB-Sanskrit8.html
- **Archived URL:** https://vedabase.io/en/library/sb/8/
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/bhagavata-canto8-sanskrit/canto8.html`
- **Integrity:** SHA-256 `63d27ed146a02b55203f2cc5fb1c605a3171d7fc3e6665a0e2f8bc9e5fa4a072`.
- **Rights/storage:** Primary-text research capture.
- **Notes:** Used for the Epilogue's single-source *samudra-manthana* sequence and poison-name variants.

### `aurobindo-secret-veda-1971`

- **Citation:** Sri Aurobindo, *The Secret of the Veda*, Sri Aurobindo Birth Centenary Library 10 (Sri Aurobindo Ashram, 1971).
- **Source type:** Authorized digital book presentation.
- **Canonical locator:** pp. 62–63 and 71 in the 1971 SABCL edition.
- **Digital URL:** https://www.motherandsriaurobindo.in/Sri-Aurobindo/books/sabcl/the-secret-of-the-veda/
- **Archived URL:** https://www.sriaurobindoashram.org/sriaurobindo/downloadpdf.php?id=30
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/aurobindo-secret-veda-1971/index.html`
- **Integrity:** SHA-256 `d18cf45749594d83a290bf4623e228a71eee7f457bca3e4c8da49c75fb3c4b1a`.
- **Rights/storage:** Authorized web presentation archived for research; no unofficial scan added.
- **Notes:** The local page identifies the 1971 volume and exposes its text. The later Ashram PDF is an authorized edition but does not control the cited 1971 pagination.

### `colonial-sanskrit-institution-histories`

- **Citation:** Official histories of Sampurnanand Sanskrit Vishwavidyalaya, the Maharashtra State Gazetteer, and The Sanskrit College and University.
- **Source type:** Government and institutional web pages.
- **Canonical locator:** Benares 1791; Poona 1821; Calcutta 1824.
- **Digital URL:** https://ssvv.ac.in/about-us
- **Archived URL:** https://www.sanskritcollegeanduniversity.ac.in/history.php
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/colonial-sanskrit-institutions/`
- **Integrity:** SHA-256: SSVV `8cb4fc7449155001275f77604870df1f76e3f5f616f51fc13b1a7e6ae678d421`; Poona Gazetteer `d7b75694be02c49d643ef07339f01562ff2a68834e055016a82fd4de363440da`; Sanskrit College Kolkata `a68eb543c83a5552fbc73501ee11d33560446f3d15e163ab9deb2285d7755191`.
- **Rights/storage:** Government/institutional research captures.
- **Notes:** Poona source URL: https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Poona%20District/instruction.html

### `hatcher-pandit-2005`

- **Citation:** Brian A. Hatcher, “What's Become of the Pandit? Rethinking the History of Sanskrit Scholars in Colonial Bengal,” *Modern Asian Studies* 39.3 (2005): 683–723.
- **Source type:** Copyrighted scholarly article.
- **Canonical locator:** DOI 10.1017/S0026749X04001672.
- **Digital URL:** https://doi.org/10.1017/S0026749X04001672
- **Archived URL:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/whats-become-of-the-pandit-rethinking-the-history-of-sanskrit-scholars-in-colonial-bengal/8638AD8E0E28FE42E3A7862D3A58301F
- **Accessed:** 2026-09-02; text consulted in the earlier audit on 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; DOI/repository metadata only.
- **Notes:** Used for the roles of Sanskrit paṇḍits in colonial scholarly institutions.

### `dodson-pandits-2002`

- **Citation:** Michael S. Dodson, “Re-Presented for the Pandits: James Ballantyne, ‘Useful Knowledge,’ and Sanskrit Scholarship in Benares College during the Mid-Nineteenth Century,” *Modern Asian Studies* 36.2 (2002): 257–298.
- **Source type:** Copyrighted scholarly article.
- **Canonical locator:** DOI 10.1017/S0026749X02002019.
- **Digital URL:** https://doi.org/10.1017/S0026749X02002019
- **Archived URL:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/represented-for-the-pandits-james-ballantyne-useful-knowledge-and-sanskrit-scholarship-in-benares-college-during-the-midnineteenth-century/F985ABCC4B23961752B08811F825DFC2
- **Accessed:** 2026-09-02; text consulted in the earlier audit on 2026-09-01.
- **Local record:** Not retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted; DOI/publisher metadata only.
- **Notes:** Used for the work of Indian scholars within Benares College's colonial knowledge system.
