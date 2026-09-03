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

### `vedabase-bhagavata-10-16`

- **Citation:** *Śrīmad Bhāgavata Purāṇa*, Skandha 10, chapters 16-17 and 26.12, Sanskrit text with English translation, Vedabase.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** 10.16.1, 4-6, 24-30; 10.17; 10.26.12.
- **Digital URL:** https://vedabase.io/en/library/sb/10/16/
- **Archived URL:** https://vedabase.io/en/library/sb/10/26/12/
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vedabase-bhagavata-10-16/`
- **Integrity:** SHA-256: chapter 10.16 `21730fe9b14441336926e89f6764b8cfae1bce6285959758441a4d19256b13e1`; chapter 10.17 `a439abb7b42febf4163517716fa2c024e76c38b67ee2f4a66d68b8d179394224`; 10.26.12 `ebc335bd1d842f1de3c72c2ea296cfe713949a8e3cd53410295b63b7b5666d07`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used to verify Kāliya's poisoning of the Yamunā, his removal, and the restoration of water free from poison.

### `narayaniya-mbh-12-335`

- **Citation:** *Mahābhārata*, Nārāyaṇīya, Śānti Parva 12.335.1-89, Sanskrit text with English translation, Nārāyaṇīya study edition hosted by Wisdomlib.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** Critical-edition 12.335.25-65; older-edition section 12.348.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/narayaniya-narayaneeyam/d/doc419437.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/narayaniya-mbh-12-335/page.html`
- **Integrity:** SHA-256 `b203402383a7669d791c54faedb75f8ea9215ef48382ca703431f5972e77bd5a`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for Madhu and Kaiṭabha carrying off the Vedas, Hayaśiras recovering them, and Nārāyaṇa killing the two thieves.

### `vedabase-bhagavata-8-24`

- **Citation:** *Śrīmad Bhāgavata Purāṇa*, Skandha 8, chapter 24, Sanskrit text with English translation, Vedabase.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** 8.24.8-9 and 57.
- **Digital URL:** https://vedabase.io/en/library/sb/8/24/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vedabase-bhagavata-8-24/page.html`
- **Integrity:** SHA-256 `1410937ffe62e89e306ea29b65a52209fb7696e68a533b55970729b34e77cbca`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for the Hayagrīva theft and Matsya's recovery of the Vedas.

### `vedabase-bhagavata-10-6`

- **Citation:** *Śrīmad Bhāgavata Purāṇa*, Skandha 10, chapter 6, Sanskrit text with English translation, Vedabase.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** 10.6.4-12.
- **Digital URL:** https://vedabase.io/en/library/sb/10/6/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vedabase-bhagavata-10-6/page.html`
- **Integrity:** SHA-256 `a1d1e0d3460f321a929bb122248d4c6b00fb154c5f56e187507ca611072ea8e8`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for Pūtanā's appearance, entry into Nanda's house, and poisoned breast.

### `valmiki-ramayana-aranya-42-44`

- **Citation:** Vālmīki, *Rāmāyaṇa*, Araṇya Kāṇḍa, sargas 42-44, Sanskrit Documents digital presentation with English prose translation.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** Vālmīki Rāmāyaṇa 3.42-44.
- **Digital URL:** https://sanskritdocuments.org/sites/valmikiramayan/aranya/sarga42/aranya_42_prose.htm
- **Archived URL:** https://sanskritdocuments.org/sites/valmikiramayan/aranya/sarga44/aranya_44_prose.htm
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/valmiki-ramayana-aranya-42-44/`
- **Integrity:** SHA-256: sarga 42 `ad7c12bc15bf3f59feb517c16289b830441189ddaed1a83b0122ee490fe0ed3a`; sarga 43 `e6ee21410f5a887fbf52fb5fd72efd6dab1ff2b6cb78aea8ddb9936696c138a0`; sarga 44 `38028cd8a6960d27f14256efb2b3f096c8f10dd5f5119c844f96e82f6a78dcc6`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for Mārīca's golden-deer appearance and his use of Rāma's voice.

### `adhyatma-ramayana-yuddha-7`

- **Citation:** *Adhyātma Rāmāyaṇa*, Yuddha Kāṇḍa, sarga 7, Sanskrit text with English translation.
- **Source type:** Primary-text digital edition.
- **Canonical locator:** Yuddha Kāṇḍa 7.4-20.
- **Digital URL:** https://devo-mn.monist.guru/doc/AdhyatmaRamayanaSourcepdf.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/adhyatma-ramayana-yuddha-7/source.pdf`
- **Integrity:** SHA-256 `5e60f906b1596c197a80c741eaf84e1926ac54156f18ab152584651a3ec11ba5`.
- **Rights/storage:** Public primary-text research copy.
- **Notes:** Verse 7.5 calls Kālanemi ***muniveṣadharaḥ*** and places him in a fabricated hermitage on Hanumān's route.

### `vedabase-bhagavata-10-66`

- **Citation:** *Śrīmad Bhāgavata Purāṇa*, Skandha 10, chapter 66, Sanskrit text with English translation, Vedabase.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** 10.66.1-6 and 12-21.
- **Digital URL:** https://vedabase.io/en/library/sb/10/66/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vedabase-bhagavata-10-66/page.html`
- **Integrity:** SHA-256 `f9be018b13be7d75d0699ae5666b8111010dd7feec86a174ee80d343fbf9195c`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for Pauṇḍraka's claim to the Vāsudeva identity and his imitation of Kṛṣṇa's insignia.

### `vedabase-bhagavata-10-88`

- **Citation:** *Śrīmad Bhāgavata Purāṇa*, Skandha 10, chapter 88, Sanskrit text with English translation, Vedabase.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** 10.88.13-39.
- **Digital URL:** https://vedabase.io/en/library/sb/10/88/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/vedabase-bhagavata-10-88/page.html`
- **Integrity:** SHA-256 `00ddc0d82a69f5019d59897ac99ebc31c5c0a4ff1e902ffddafb090e38a1f39a`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for Vṛka turning Śiva's boon against Śiva. The chapter does not name Bhasmāsura or Mohinī.

### `devimahatmya-ch5`

- **Citation:** *Devī Māhātmya*, chapter 5, Sanskrit text with English translation, Digital Temple of the Divine Mother.
- **Source type:** Primary-text web presentation.
- **Canonical locator:** 5.2-4 and 5.89-125; *Mārkaṇḍeya Purāṇa* 85.
- **Digital URL:** https://devimahatmya.com/book/chapter-5-the-devis-conversation-with-the-messenger/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/devimahatmya-ch5/page.html`
- **Integrity:** SHA-256 `bc942c19019eadb12c3f9e44ca8604c24fbcfbc0589f8a6034777ef734eca592`.
- **Rights/storage:** Public primary-text research capture.
- **Notes:** Used for Śumbha and Niśumbha's seizure of offices and treasures and Śumbha's attempt to take the Devī as another possession.

### `wisdomlib-shiva-purana-andhaka-42-49`

- **Citation:** *Śiva Purāṇa*, Rudra Saṃhitā, Yuddha Khaṇḍa, chapters 42-49, trans. J. L. Shastri (Motilal Banarsidass, 1950), Wisdomlib presentation.
- **Source type:** Primary-text translation web presentation.
- **Canonical locator:** Rudra Saṃhitā 5.42-49.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/shiva-purana-english/d/doc226183.html
- **Archived URL:** https://www.wisdomlib.org/hinduism/book/shiva-purana-english/d/doc226190.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/wisdomlib-shiva-purana-andhaka-42-49/`
- **Integrity:** SHA-256 manifest represented by the eight archived chapter files; first `b62360e499eddfd5e909a0b892f9ff1bf91128858ea41d4adc911c1dc5a0ae62`, last `8711af5bbb0c58f888753fcf9d37e39773d2d450ca0a8552d431403a88fa3eaa`.
- **Rights/storage:** Public translation research captures.
- **Notes:** Used for Andhaka's birth, adoption, boon, attack upon Pārvatī's protected cave, trident punishment, and later admission into Śiva's gaṇas.

### `gretil-yaska-nirukta-2020`

- **Citation:** Yāska, *Nirukta*, based on Lakshman Sarup's edition; electronic text entered by Munoe Tokunaga and M. Kobayashi; GRETIL TEI conversion, 2020-07-31.
- **Source type:** Primary-text electronic corpus.
- **Canonical locator:** GRETIL `sa_yAska-nirukta`; *Nirukta* 3.8 and 7.14.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_yAska-nirukta.htm
- **Archived URL:** https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_yAska-nirukta.xml
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/gretil-yaska-nirukta-2020/sa_yAska-nirukta.xml`
- **Integrity:** SHA-256 `94597de75a62d981f3c31f2bd6d9453c3a0b723cc9ce666f6bebf55fc4aedac7`.
- **Rights/storage:** CC BY-NC-SA 4.0 electronic text; archived locally.
- **Notes:** Used to check the Sanskrit text against Sarup's printed edition, including the two *asura* analyses at 3.8 and the analyses of **अग्नि (*agni*)** at 7.14.

### `sarup-nighantu-nirukta-1920-scan`

- **Citation:** Lakshman Sarup, *The Nighaṇṭu and the Nirukta* (Oxford University Press, 1920).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `nighantuniruktao01saru`; *Nirukta* 3.8 and 7.14.
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
- **Integrity:** RV 6.17 file SHA-256 `5a8190f23c343ff4118bdfd9270246804aa3f1cae04905b6151a7294593eb4be`; RV 8.96 file SHA-256 `64522fd6d2ac6a127cd6290c51a622c6e90566bfa133b574ec8020fa66649162`; Īśopaniṣad Kāṇva file SHA-256 `9c2155f97c072825ac641521f79e5bc88e91dc09c7a053f0b2140ca0515e7545`; Bṛhadāraṇyaka Upaniṣad Kāṇva file SHA-256 `541fa71fbf76b5460324ffe3cd2d7117c1cea19ef2020fb54b496cdbc282c283`.
- **Rights/storage:** Existing local Git snapshot; no duplicate created.
- **Notes:** Used for exact verse-level forms and local DCS metadata. Batch 007 also checked the traditional Īśopaniṣad opening invocation and its occurrence at Bṛhadāraṇyaka Upaniṣad 5.1.1 in the GRETIL texts contained in this snapshot.

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
- **Integrity:** SHA-256: RV00 `f8da518fe2bb195a3388a2d87d3af7f077a0259b34a9e269dd3ab38a8868568f`; RV01 `fef667cf7f98c91d6d32e6d312d956be2f9dee5a6d58153f70e1e9bcc4072132`; RV02 `017fb1d86c17613fa466c81ba61b34f8a0ade061c1d918f61c418cbafe34c94a`; RV03 `cc6ae519d3f5feac5cb8bab6bc529a498a19e3240254fccbb7414afd53cf826a`; RV05 `b29ae3f130617969c8e3da0d9905de6a4f27d22a07817493f4978251f45c588f`; RV06 `1b9e62ef0946bb4064a4a80223e991051e03e7430107a89c71e4751eae340b4f`; RV07 `4af631514dc06a80c1fda64fefdc539f33d4caf856a290e56ed1e0682bd31b18`; RV08 `e77c60e34c1cbdd516252639c0e9cc3615a4999e97cd7d5894d8dd82d118d8fa`; RV10 `1516b3413a3e20b945a461d579748c708091ad9aeef75ffa26bd8a13102e924b`.
- **Rights/storage:** Research-use HTML pages retained locally; source page states non-commercial research use.
- **Notes:** Exact book URLs are the base URL followed by the two-digit book number, including the locally retained `RV01`, `RV02`, `RV03`, `RV05`, `RV06`, `RV07`, `RV08`, and `RV10` pages.

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
- **Notes:** Batch 005 checked the headwords ***svar***, ***bhānu***, ***Svarbhānu***, ***lakṣmī***, and ***paśu***. Batch 007 checked ***savyasācin***, ***dhanañjaya***, ***ap***, ***payas***, ***salila***, ***pānīya***, ***jala***, ***vāri***, and ***udaka***.

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

### `american-heritage-ie-roots-guide`

- **Citation:** *The American Heritage Dictionary*, “Guide to the Indo-European Roots Appendix.”
- **Source type:** Publisher dictionary guide.
- **Canonical locator:** Indo-European Roots Appendix guide.
- **Digital URL:** https://ahdictionary.com/word/ieguide.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/american-heritage-ie-roots-guide/page.html`
- **Integrity:** SHA-256 `38697ae9b890251eca08455e8c57d12c9a410684eaeb3d157733a8abfdc2aa2f`.
- **Rights/storage:** Public publisher page; research capture retained.
- **Notes:** The guide describes the appendix as extending documentary etymology into reconstructed prehistory.

### `etymonline-about`

- **Citation:** Douglas Harper, *Online Etymology Dictionary*, “About.”
- **Source type:** Public reference site.
- **Canonical locator:** Site history, updated 2025-04-07.
- **Digital URL:** https://www.etymonline.com/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/etymonline-about/page.html`
- **Integrity:** SHA-256 `c80f17817d2c9bc26cd3d476838e8d60ff7eacd02265cc57fe2ab9fdf90f72fb`.
- **Rights/storage:** Public web page; research capture retained.
- **Notes:** The site states that Harper created the dictionary in 2001.

### `pie-reference-ecosystem-metadata`

- **Citation:** J. P. Mallory and Douglas Q. Adams, *Encyclopedia of Indo-European Culture* (1997); Helmut Rix, ed., *Lexikon der indogermanischen Verben*, 2nd ed. (2001); Michiel de Vaan, *Etymological Dictionary of Latin and the Other Italic Languages* (2008); Robert Beekes, *Etymological Dictionary of Greek* (2010).
- **Source type:** Bibliographic publication records.
- **Canonical locator:** ISBN 9781884964985; ISBN 9783895002197; DOI 10.1163/9789047421037; DOI 10.1163/9789004189629.
- **Digital URL:** https://doi.org/10.1163/9789047421037
- **Archived URL:** https://doi.org/10.1163/9789004189629
- **Accessed:** 2026-09-02.
- **Local record:** Not retained.
- **Integrity:** Not applicable; publisher and DOI metadata only.
- **Rights/storage:** Copyrighted publications; metadata only.
- **Notes:** Used only to verify publication identity and year.

### `indian-university-pie-curricula`

- **Citation:** Government of India e-PG Pathshala, “Indo-Aryan Language Family,” and official Sanskrit or linguistics curricula from Vinoba Bhave University, the Sanskrit College and University, the universities of Calicut, Delhi, and Kerala, Karnatak University, and Deccan College.
- **Source type:** Official government and university teaching materials.
- **Canonical locator:** Named modules and curricula described in `pie-indian-university-curricula`.
- **Digital URL:** https://epgp.inflibnet.ac.in/epgpdata/uploads/epgp_content/S000022LS/P001756/M023413/ET/1506322131Lings-P7-M21.pdf
- **Archived URL:** Official institution URLs retained in the endnote.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/indian-university-pie-curricula/`; `working/40_reference/sources/archive/web/indian-university-pie-curricula/`.
- **Integrity:** Aggregate SHA-256 over sorted file hashes `0de002a7e55fca6c4297c2249e46e2caf80fac7917f03bf69f9d4643cc022bfe`.
- **Rights/storage:** Official public curricula retained for research.
- **Notes:** Six official PDFs and the Vinoba Bhave University page are archived. The official e-PG PDF and University of Kerala LMS page were verified online but could not be retained during this pass.

### `ashtadhyayi-named-authorities`

- **Citation:** Pāṇini, *Aṣṭādhyāyī*, digital sūtra displays for the named-authority rules and 1.3.1 and 4.4.124.
- **Source type:** Digital primary-text and commentary pages.
- **Canonical locator:** 1.2.25, 1.3.1, 3.4.111, 4.4.124, 5.4.112, 6.1.92, 6.1.123, 6.1.130, 6.3.61, 7.1.74, 7.2.63, 7.3.99, 8.3.18, 8.3.20, 8.4.50, and 8.4.67.
- **Digital URL:** https://ashtadhyayi-lite.github.io/sutra/6.1.92.html
- **Archived URL:** Exact rule URLs follow the same stable path.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ashtadhyayi-named-authorities/`.
- **Integrity:** Aggregate SHA-256 over sorted file hashes `b3f337b3795f9c34549fe2ab78a437aeb71e9734a9504f4eadbccd1bd4778b3d`.
- **Rights/storage:** Public digital grammatical pages; research captures retained.
- **Notes:** Exact sūtra text and commentary were checked individually.

### `gita-supersite-7-14`

- **Citation:** *Bhagavad Gītā* 7.14, Gita Supersite, Indian Institute of Technology Kanpur.
- **Source type:** Institutional primary-text and commentary interface.
- **Canonical locator:** Bhagavad Gītā 7.14.
- **Digital URL:** https://www.gitasupersite.iitk.ac.in/srimad?etadi=1&etgb=1&etpurohit=1&etsiva=1&etssa=1&field_chapter_value=7&field_nsutra_value=14&language=dv
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the server rejected command-line archival requests.
- **Integrity:** Not applicable.
- **Rights/storage:** Institutional public display; metadata only.
- **Notes:** Used for **दैवी ह्येषा गुणमयी मम माया**.

### `vedantasara-two-powers`

- **Citation:** Sadānanda, *Vedāntasāra*, §§51–54, digital Sanskrit text with English explanation.
- **Source type:** Primary philosophical text and translation.
- **Canonical locator:** §§51–54.
- **Digital URL:** https://www.vedantahub.org/wp-content/texts/Vedantasara.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/vedantasara-swami-nikhilananda/original.pdf`
- **Integrity:** SHA-256 `026a358bab631549433023836207fa3ede7430177e716836d9fb2456849b19c2`.
- **Rights/storage:** Publicly distributed research PDF; local copy retained.
- **Notes:** §51 names concealment and projection; §§52–54 give the cloud/Sun and rope/snake examples.

### `project-generative-wordspace-calculation`

- **Citation:** *Atomic Sanskrit* schematic generative-wordspace calculation.
- **Source type:** Reproducible project calculation.
- **Canonical locator:** Script output and constants.
- **Digital URL:** Not applicable.
- **Archived URL:** Not applicable.
- **Accessed:** 2026-09-02.
- **Local record:** `analysis/generativity/generative_wordspace.py`
- **Integrity:** SHA-256 `602353a841b4912fffbd7e0a3902c34d17e1ef3654edcbad7728b9fdeb11ce74`.
- **Rights/storage:** Project source.
- **Notes:** Produces 20,942,880 formal slots and warns that the result is not a count of valid or distinct words.

### `project-path-c-analysis`

- **Citation:** *Atomic Sanskrit* Path C corpus-attested combinatorial-reach analysis.
- **Source type:** Reproducible project dataset and calculation.
- **Canonical locator:** `kṛ` row in the derived Path C files.
- **Digital URL:** Not applicable.
- **Archived URL:** Not applicable.
- **Accessed:** 2026-09-03.
- **Local record:** `analysis/ganah/data/derived/path_c_with_tiers.csv`; `analysis/ganah/data/derived/path_a_vs_path_c.csv`.
- **Integrity:** Values are reproducible from the scripts and source data documented in `analysis/ganah/README.md`.
- **Rights/storage:** Project source and derived data.
- **Notes:** Records *kṛ* at combinatorial valency 1,062 and 50,155 counted corpus uses.

### `gretil-svetasvatara-upanishad`

- **Citation:** *Śvetāśvatara Upaniṣad*, GRETIL electronic text.
- **Source type:** Primary-text electronic corpus.
- **Canonical locator:** Śvetāśvatara Upaniṣad 4.8.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/svetu_pu.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** Not retained; durable institutional corpus URL recorded.
- **Integrity:** Not applicable.
- **Rights/storage:** Public electronic text; URL retained.
- **Notes:** Confirms that Ṛgveda 1.164.39 is repeated at Śvetāśvatara Upaniṣad 4.8.

### `visigalli-gargya-2023`

- **Citation:** Paolo Visigalli, “Philosophy of Grammar in Ancient India: Reinterpreting the Gārgya Controversy in Nirukta 1.12–1.14,” *Acta Orientalia Academiae Scientiarum Hungaricae* 76.2 (2023): 169–192.
- **Source type:** Peer-reviewed research article in an institutional repository.
- **Canonical locator:** pp. 169–192.
- **Digital URL:** https://real.mtak.hu/191914/
- **Archived URL:** https://real.mtak.hu/191914/1/062-article-p169.pdf
- **Accessed:** 2026-09-03.
- **Local record:** Not retained; institutional repository record and PDF URL retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Repository copy; URL retained.
- **Notes:** Used for the Śākaṭāyana–Gārgya discussion surrounding *Nirukta* 1.12–1.14.

### `mimamsa-sutra-sandal-1923`

- **Citation:** Mohan Lal Sandal, trans., *The Mīmāṃsā Sūtras of Jaimini* (Sacred Books of the Hindus, 1923).
- **Source type:** Public-domain book scan.
- **Canonical locator:** Internet Archive item `mimamsasutra00jaimuoft`; Mīmāṃsā Sūtra 1.1.5.
- **Digital URL:** https://archive.org/details/mimamsasutra00jaimuoft
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/internet-archive-metadata/mimamsasutra00jaimuoft.json`
- **Integrity:** Metadata SHA-256 `fd286980f951bef3af645974009f7940fa1f2d106675a5e70af3cfc40da313f1`.
- **Rights/storage:** Public-domain scan; repository metadata retained.
- **Notes:** Used for the primary sūtra and historical translation.

### `sep-kumarila`

- **Citation:** John Taber, “Kumārila,” *Stanford Encyclopedia of Philosophy*.
- **Source type:** Peer-reviewed reference article.
- **Canonical locator:** Sections on Vedic testimony and Mīmāṃsā Sūtra 1.1.5.
- **Digital URL:** https://plato.stanford.edu/entries/kumaarila/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/sep-kumarila/page.html`
- **Integrity:** SHA-256 `b52d28a6a609af987850f9f867fe65282847791d0cfb1e3df5f5189b6e912bfd`.
- **Rights/storage:** Public reference page; research capture retained.
- **Notes:** Used to distinguish the sūtra's claim from later Mīmāṃsā doctrine and later Nyāya accounts of divine authorship.

### `merriam-sanskrit-loanwords`

- **Citation:** Merriam-Webster.com Dictionary, entries “guru,” “karma,” “avatar,” “mantra,” and “yoga.”
- **Source type:** Publisher-maintained dictionary pages.
- **Canonical locator:** The five named headwords.
- **Digital URL:** https://www.merriam-webster.com/dictionary/guru
- **Archived URL:** The other exact URLs replace `guru` with `karma`, `avatar`, `mantra`, or `yoga`.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the server rejected command-line archival requests.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted public dictionary pages; metadata only.
- **Notes:** Each entry identifies Sanskrit in the direct borrowing history. The record supports the five direct loans in Chapter 0 and not Chapter 19's separate reflection argument.

### `mishra-sanskrit-attributive-naming`

- **Citation:** Sampadananda Mishra, “Is Sanskrit Relevant Today?”, Sri Aurobindo Society *Renaissance*, reformatted from a TEDx talk.
- **Source type:** Public essay / talk transcript.
- **Canonical locator:** Discussion of Sanskrit words for water.
- **Digital URL:** https://renaissance.aurosociety.org/editors-note-this-is-a-slightly-reformatted-version-of-a-tedx-talk-given-by-the-author-a-reader-friendly-voice-is-still-maintained/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the server rejected command-line archival requests.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted public page; metadata only.
- **Notes:** Explicitly derives ***jalam*** from ⟪जल्⟫ (*jal*), “to harden,” through water's ability to become solid, and explains ***vāri*** through water becoming cloud and covering. The remaining four Chapter 0 derivations require separate lexical verification.

### `mishra-tedx-sanskrit-breath`

- **Citation:** Sampadananda Mishra, “Is Sanskrit, an Ancient Indian Language, Still Relevant?”, TEDxPanaji, 2018; published in reformatted form as “Is Sanskrit Relevant Today?”, Sri Aurobindo Society *Renaissance*, August 2019.
- **Source type:** Public talk and published transcript.
- **Canonical locator:** Approximately 12:30-14:30 in the talk; corresponding discussion of the stop rows, anusvāra, and visarga in the transcript.
- **Digital URL:** https://renaissance.aurosociety.org/editors-note-this-is-a-slightly-reformatted-version-of-a-tedx-talk-given-by-the-author-a-reader-friendly-voice-is-still-maintained/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the server rejected command-line archival requests.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted public page; metadata only.
- **Notes:** Supports Mishra's contemporary demonstration of alternating light and heavy breath in the stop rows, nasal resonance for anusvāra, and outward release for visarga. It does not support identifying those sounds with kumbhaka and recaka.

### `ambuda-mahabharata-3-200`

- **Citation:** *Mahābhārata*, Vana Parva 3.200, Ambuda digital Sanskrit text.
- **Source type:** Digital primary-text display.
- **Canonical locator:** 3.200.3–4.
- **Digital URL:** https://ambuda.org/texts/mahabharatam/3.200
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ambuda-mahabharata-3-200/page.html`
- **Integrity:** SHA-256 `14db15814b2a7279d1f67a29c8087d6bc6ddc1d3f377be2f8b5284db7d7fe95f`.
- **Rights/storage:** Public web-page research capture.
- **Notes:** Confirms **यद्भूतहितमत्यन्तं तत्सत्यमिति धारणा** at 3.200.4 and preserves the immediately preceding contextual verse.

### `vishnupurana-vyasa-division`

- **Citation:** *Viṣṇu Purāṇa* 3.3–4, SanskritSahitya digital Sanskrit text.
- **Source type:** Digital primary-text display.
- **Canonical locator:** 3.3.9–10; 3.4.2, 7–10.
- **Digital URL:** https://sanskritsahitya.org/vishnupuranam/3.4
- **Archived URL:** https://sanskritsahitya.org/vishnupuranam/3.3
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the server rejected command-line archival requests.
- **Integrity:** Not applicable.
- **Rights/storage:** Public digital Sanskrit display; metadata only.
- **Notes:** Confirms the recurring fourfold division, Kṛṣṇa Dvaipāyana's division of the one Veda, the four named Vedic assignments, and Romaharṣaṇa's receipt of *itihāsa-purāṇa*.

### `vhp-vedic-text-placement`

- **Citation:** Government of India, Vedic Heritage Portal, “Aitareya Aranyaka,” “Taittiriya Aranyaka,” and “Vajasaneyi Kanva Samhita, Adhyaya 40.”
- **Source type:** Institutional Vedic-text portal.
- **Canonical locator:** Aitareya Aranyaka, second division, chapters 4-6; Taittiriya Aranyaka 7-10; Vajasaneyi Kanva Samhita 40.
- **Digital URL:** https://vedicheritage.gov.in/aranyakas/aitareyaranyaka/
- **Archived URL:** https://vedicheritage.gov.in/aranyakas/taittiriya-aranyaka/ and https://vedicheritage.gov.in/hi/samhitas/yajurveda/vajasaneyi-kanva-samhita/vajasaneyi-kanva-samhita-chapter-40/
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the server was available through browser search but did not resolve from the command-line archival environment.
- **Integrity:** Not applicable.
- **Rights/storage:** Government institutional web pages; metadata and exact URLs retained.
- **Notes:** Confirms that the Aitareya Upanishad occupies chapters 4-6 of the second Aitareya Aranyaka division, Taittiriya Aranyaka 7-9 form the Taittiriya Upanishad while 10 forms the Mahanarayana Upanishad, and the Isha text occupies Vajasaneyi Kanva Samhita chapter 40.

### `mactutor-arabic-numerals`

- **Citation:** J. J. O'Connor and E. F. Robertson, “Arabic Numerals,” *MacTutor History of Mathematics Archive*, University of St Andrews.
- **Source type:** Institutional history-of-mathematics essay.
- **Canonical locator:** Sections on Indian numerals, al-Khwarizmi, and Latin transmission.
- **Digital URL:** https://mathshistory.st-andrews.ac.uk/HistTopics/Arabic_numerals/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the host did not resolve from the command-line archival environment.
- **Integrity:** Not applicable.
- **Rights/storage:** Institutional public web page; metadata only.
- **Notes:** States that Indian numerals passed through Arabic mathematical practice into Europe. It also records that al-Khwarizmi's Arabic text is lost, the Latin translation was substantially changed, and the title of the Arabic work is uncertain.

### `wisdomlib-manusmriti-8-15`

- **Citation:** *Manusmriti* 8.15 with Medhatithi's commentary and Ganganath Jha's translation, Wisdomlib digital edition.
- **Source type:** Digital primary text with commentary and translation.
- **Canonical locator:** *Manusmriti* 8.15.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/manusmriti-with-the-commentary-of-medhatithi/d/doc200908.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the host did not resolve from the command-line archival environment.
- **Integrity:** Not applicable.
- **Rights/storage:** Public digital text display; metadata and exact locator retained.
- **Notes:** Supplies the complete Sanskrit verse beginning **धर्म एव हतो हन्ति धर्मो रक्षति रक्षितः** and identifies it as 8.15.

### `sanskritdocuments-devi-mahatmya`

- **Citation:** *Devi Mahatmyam / Durga Saptashati*, Sanskrit Documents electronic text.
- **Source type:** Digital Sanskrit primary text.
- **Canonical locator:** Chapters 3 and 7-10.
- **Digital URL:** https://sanskritdocuments.org/doc_devii/durga700.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the host did not resolve from the command-line archival environment.
- **Integrity:** Not applicable.
- **Rights/storage:** Public electronic Sanskrit text; metadata and exact URL retained.
- **Notes:** Used to confirm the chapter sequence in which Devi slays Mahishasura, Chanda and Munda, Raktabija, Nishumbha, and Shumbha. It establishes those named examples, not a universal rule about the gender of every apex-claimant in the wider corpus.

### `wisdomlib-rigveda-10-22-8`

- **Citation:** *Rigveda* 10.22.8 with Sāyaṇa's commentary, Wisdomlib digital presentation.
- **Source type:** Digital primary text with traditional commentary and translation.
- **Canonical locator:** Ṛgveda 10.22.8.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc838740.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; exact URL and locator retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Public digital text display; metadata only.
- **Notes:** Sāyaṇa explains **अमानुषः (*amānuṣaḥ*)** as outside human custom and as an asuric disposition. Used with Griffith's “inhuman” rendering to avoid treating the word as a biological classification.

### `vedportal-rigveda-4-5-5`

- **Citation:** *Rigveda* 4.5.5, Ved Portal digital text with word meaning and interpretation attributed to Dr. Tulsi Ram.
- **Source type:** Digital primary-text display with modern translation.
- **Canonical locator:** Ṛgveda 4.5.5.
- **Digital URL:** https://xn--j2b3a4c.com/en/rigveda/4/5/5
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; exact URL and locator retained.
- **Integrity:** Not applicable.
- **Rights/storage:** Public digital text display; metadata only.
- **Notes:** Reads **गभीरम् पदम् (*gabhīram padam*)** as a deep state of life produced by false conduct. Jamison and Brereton instead read “deep track/profound word.” The endnote records both readings and identifies “isolation” as the book's synthesis.

### `max-muller-life-letters-v1`

- **Citation:** Georgina Adelaide Müller, ed., *The Life and Letters of the Right Honourable Friedrich Max Müller*, vol. 1 (London: Longmans, Green, 1902).
- **Source type:** Public-domain primary correspondence.
- **Canonical locator:** Letter to Chevalier Bunsen, 25 August 1856, pp. 181-183, especially p. 182.
- **Digital URL:** https://archive.org/details/lifelettersofrig01mluoft
- **Archived URL:** https://archive.org/download/lifelettersofrig01mluoft/lifelettersofrig01mluoft_djvu.txt
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/max-muller-life-letters-v1/fulltext.txt`
- **Integrity:** SHA-256 `49c0b3b9446c27ed183082155387125b48c62b2aec63c36582f15be2af049dfd`.
- **Rights/storage:** Public-domain book; full searchable text retained.
- **Notes:** The printed letter says Müller wished to join a work that would overthrow what he called “the old mischief of Indian priestcraft” and open the way for “the entrance of Christian teaching.” The date is 25 August 1856.

### `pollock-language-gods-2006`

- **Citation:** Sheldon Pollock, *The Language of the Gods in the World of Men: Sanskrit, Culture, and Power in Premodern India* (University of California Press, 2006).
- **Source type:** Copyrighted scholarly monograph made available by the author through Zenodo.
- **Canonical locator:** Introduction, pp. 5, 11-16, 30; chapter 1, pp. 39-50; chapter 4, pp. 162-188, especially p. 188.
- **Digital URL:** https://zenodo.org/records/3901953
- **Archived URL:** https://zenodo.org/records/3901953/files/Pollock%202006.pdf
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/pollock-language-gods/original.pdf`
- **Integrity:** SHA-256 `c52307a277b3a89a2f3e505e0170424dd00de36eee9f28b67acd8d2c8517f326`; DOI `10.5281/zenodo.3901953`.
- **Rights/storage:** Author-deposited copyrighted monograph; research copy retained.
- **Notes:** Pollock foregrounds Sanskrit's relation to culture, power, polity, and courtly practice, and p. 188 makes power's concern with grammar and grammar's concern with power constitutive. He also states that the Sanskrit cosmopolis had no imperial state or church enforcing its universalism; the endnote preserves that qualification.

### `gretil-chandogya-upanishad`

- **Citation:** *Chāndogya Upaniṣad*, GRETIL electronic text checked against V. P. Limaye and R. D. Vadekar, eds., *Eighteen Principal Upaniṣads*, vol. 1 (Poona, 1958), and TITUS.
- **Source type:** Electronic primary-text edition.
- **Canonical locator:** 8.7.1-8.12.6, especially 8.8.1-5 and 8.9.1-3.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/chup___u.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/gretil-chandogya/page.html`
- **Integrity:** SHA-256 `dfa72268d05eb2908694a51750ba35281a5858be2d3a51a8e0d94ad35a51c9c3`.
- **Rights/storage:** Reference-use electronic text; research capture retained.
- **Notes:** Section 8.7 begins the shared instruction. Virocana accepts the reflected body and leaves at 8.8.4-5; Indra identifies the contradiction and returns at 8.9.1-3; the successive instruction continues through 8.12.

### `wisdomlib-jalandhara`

- **Citation:** *Śiva Purāṇa*, Rudra Saṃhitā, Yuddha Khaṇḍa 5.22-23, and *Padma Purāṇa*, Uttara Khaṇḍa 6.13, Wisdomlib digital translations.
- **Source type:** Digital Purāṇa text and translation displays.
- **Canonical locator:** *Śiva Purāṇa* 5.22.37-52 and 5.23.2-50; *Padma Purāṇa* 6.13.14-51.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/shiva-purana-english/d/doc226163.html
- **Archived URL:** https://www.wisdomlib.org/hinduism/book/shiva-purana-english/d/doc226164.html and https://www.wisdomlib.org/hinduism/book/the-padma-purana/d/doc365444.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/wisdomlib-jalandhara/`
- **Integrity:** SHA-256: `shiva-22.html` `5b71d3ac33a0567783b86e3a624e5201258a9e801ebeb08ed89c41388f0fed24`; `shiva-23.html` `cdca72f114299e27e5804c5c95378c515f547893eb94dabcd4aa7bae97539559`; `padma-13.html` `d385ebc0f06ea3ef240077fce9e2b7733f984dddaecfe30e58370d877ad79010`.
- **Rights/storage:** Public web-page research captures.
- **Notes:** The Śiva Purāṇa passage narrates Jalandhara taking Śiva's form to approach Pārvatī. The Padma Purāṇa supplies a second telling. The accompanying Vṛndā episode is distinct and is not used as evidence for Jalandhara's disguise.

### `wisdomlib-rigveda-selected`

- **Citation:** Selected Ṛgveda mantras with Sāyaṇa's commentary and H. H. Wilson's translation, Wisdomlib digital presentation.
- **Source type:** Digital primary text with traditional commentary, word separation, grammar, and translation.
- **Canonical locator:** Ṛgveda 1.32.1, 1.32.11, 2.24.3, 7.104.18, and 8.42.1.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc829265.html
- **Archived URL:** https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc829275.html ; https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc831323.html ; https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc835457.html ; https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc836369.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/wisdomlib-rigveda-selected/`
- **Integrity:** SHA-256: RV 1.32.1 `e3988efc19fbe96751fc3349c92ac7d7e5d508be7578d074565403f40deae57d`; RV 1.32.11 `f8045259bf51cfe7a76ae8e4f9d1c742a69fe25ff58b1c81fd9a5ec9507cebfa`; RV 2.24.3 `37289d6dfcec9450ea83add87cb46959684e1f52fe8a2da5ef96eb478fee72b1`; RV 7.104.18 `1b4aa826fea67da534805341fd44fcab48f368454b2e9dbd30bba0d9d4e694ab`; RV 8.42.1 `da72bbf84313c4653f5f05b1cedcb4e877affdb45fac52646b24aa673c6bef97`.
- **Rights/storage:** Public web-page research captures.
- **Notes:** Used to cross-check exact Sanskrit forms, word separation, grammatical analysis, Sāyaṇa's interpretation, and Wilson's translations against the metrically restored text and Jamison-Brereton translation.

### `gretil-bhagavad-gita-16`

- **Citation:** *Bhagavadgītā*, chapter 16, with Sanskrit commentaries of Śrīdhara, Viśvanātha, and Baladeva, GRETIL electronic text.
- **Source type:** Electronic primary text with Sanskrit commentaries.
- **Canonical locator:** Bhagavad Gītā 16.6.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/2_epic/mbh/ext/bhg4c16u.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/gretil-bhagavad-gita-16/page.html`
- **Integrity:** SHA-256 `567e815a29734be97f781bc0fe721df4bdfd00605dee96670096ea6749432d01`.
- **Rights/storage:** Reference-use electronic text; research capture retained.
- **Notes:** Confirms the Sanskrit verse and the commentary tradition's treatment of the two **भूतसर्गौ (*bhūtasargau*)**.

### `gita-supersite-16-6`

- **Citation:** Bhagavad Gītā 16.6, Gita Supersite, Indian Institute of Technology Kanpur.
- **Source type:** Institutional primary-text and commentary interface.
- **Canonical locator:** Bhagavad Gītā 16.6.
- **Digital URL:** https://www.gitasupersite.iitk.ac.in/srimad?choose=1&ecsiva=1&etgb=1&etradi=1&etsiva=1&field_chapter_value=16&field_nsutra_value=6&language=dv
- **Archived URL:** https://www.gitasupersite.iitk.ac.in/
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the command-line request did not return the rendered verse interface.
- **Integrity:** Not applicable.
- **Rights/storage:** Institutional web source; exact query URL retained.
- **Notes:** Used as an institutional cross-check for the verse, not as the sole source for the translation.

### `umich-colonialism-conversion`

- **Citation:** William L. Clements Library, University of Michigan, “Religion & Colonialism,” Centennial Exhibit, Pair 11.
- **Source type:** University collection and exhibition essay.
- **Canonical locator:** Opening discussion of religious conversion as a goal of European colonization in the Western Hemisphere.
- **Digital URL:** https://clements.umich.edu/exhibit/centennial-exhibit/centennial-pair-11/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the page was consulted in-browser but rejected command-line archival capture.
- **Integrity:** Not applicable.
- **Rights/storage:** University public web page; exact URL retained.
- **Notes:** Supports a concrete historical example of colonization and conversion. It does not establish the book's broader conceptual proposition by itself.

### `uzh-colonial-mission-religious-change`

- **Citation:** University of Zurich, World Development, “Missionaries and Religious Change in Colonial India.”
- **Source type:** University research-project overview.
- **Canonical locator:** Overview of Christian missions, education, colonial rule, and religious change.
- **Digital URL:** https://www.worlddevelopment.uzh.ch/en/research/indcol/soctra/miss.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/colonial-conversion-sources/uzh.html`
- **Integrity:** SHA-256 `8553bacd2a6c330c2d6376e24bc50dc202e01c5908563a12d7a3453490ddd6aa`.
- **Rights/storage:** University public web-page research capture.
- **Notes:** Supports the interaction of missions, education, colonial institutions, and religious change in India. The endnote distinguishes this historical mechanism from the book's broader inference about defensive memory.

### `weber-ramayana-1873-scan`

- **Citation:** Albrecht Weber, *On the Rāmāyaṇa*, translated from the German, 1873 English printing.
- **Source type:** Public-domain book scan.
- **Canonical locator:** Printed pp. 22-24.
- **Digital URL:** https://upload.wikimedia.org/wikipedia/commons/b/b5/On_the_R%C4%81m%C4%81ya%E1%B9%87a_(IA_onramayana00webe).pdf
- **Archived URL:** Internet Archive item `onramayana00webe`.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/weber-on-ramayana-1873/original.pdf`
- **Integrity:** SHA-256 `352005a7756f585a4bd2e2fc677b208f90bd73b69ecc2a8d5a5c33a3aa0a4dbc`.
- **Rights/storage:** Public-domain scan.
- **Notes:** Printed pp. 22-23 state Weber's Homer-to-Vālmīki model; p. 24 proposes transmission following Alexander's expedition.

### `telang-ramayana-homer-1873-metadata`

- **Citation:** Kashinath Trimbak Telang, *Was the Râmâyaṇa Copied from Homer? A Reply to Professor Weber* (Bombay: Union Press, 1873).
- **Source type:** Public-domain book metadata.
- **Canonical locator:** 1873 Union Press edition, 71 pages.
- **Digital URL:** https://books.google.com/books/about/Was_the_R%C3%A2m%C3%A2ya%E1%B9%87a_Copied_from_Homer.html?id=UjbUf0BuaFEC
- **Archived URL:** https://openlibrary.org/books/OL5971044M/Was_the_Ra%CC%82ma%CC%82yan%CC%A3a_copied_from_Homer
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; bibliographic record only.
- **Integrity:** Not applicable.
- **Rights/storage:** Public bibliographic metadata.
- **Notes:** Confirms the title, author, publication place, publisher, and year of Telang's direct reply to Weber.

### `west-indo-european-poetry-myth-2007`

- **Citation:** M. L. West, *Indo-European Poetry and Myth* (Oxford University Press, 2007).
- **Source type:** Copyrighted monograph metadata and limited preview.
- **Canonical locator:** DOI 10.1093/acprof:oso/9780199280759.001.0001; pp. 12-14 and 437-438.
- **Digital URL:** https://academic.oup.com/book/10022
- **Archived URL:** https://doi.org/10.1093/acprof:oso/9780199280759.001.0001
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; metadata and exact page locators only.
- **Integrity:** Not applicable.
- **Rights/storage:** Copyrighted monograph; no local copy added.
- **Notes:** Used for the later common-inheritance frame, not as evidence for Weber's direct-borrowing claim.

### `wisdomlib-rigveda-asura-praised`

- **Citation:** Ṛgveda 1.174.1 and 1.24.14 with Sāyaṇa-based Wilson translation, word separation, and grammatical analysis, Wisdomlib.
- **Source type:** Digital primary text with traditional commentary and translation.
- **Canonical locator:** Ṛgveda 1.174.1 and 1.24.14.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc830892.html
- **Archived URL:** https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc829155.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/wisdomlib-rv-asura/`
- **Integrity:** SHA-256: RV 1.174.1 `9f9834a6d84b1a2e7ae3140a2be991307932cc0f06fe111075bddd6e3e47239b`; RV 1.24.14 `0e299207e1a0f5c09fe8512c2ec2f50bd257356dca96ccb7bcd44421f1cf3128`.
- **Rights/storage:** Public web-page research captures.
- **Notes:** Used with the University of Texas text and Jamison-Brereton translation to check the vocatives and actions in both mantras.

### `iranica-ahura-kuiper`

- **Citation:** F. B. J. Kuiper, “Ahura,” *Encyclopaedia Iranica*, vol. I, fasc. 7, pp. 683-684.
- **Source type:** Reference article.
- **Canonical locator:** Encyclopaedia Iranica, “Ahura.”
- **Digital URL:** https://www.iranicaonline.org/articles/ahura-1-type-of-deity/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** Not retained; the site rejected command-line archival capture.
- **Integrity:** Not applicable.
- **Rights/storage:** Exact public reference URL retained.
- **Notes:** Kuiper describes Rigvedic asuras as older gods, devas as younger gods, and their opposition as a process of polarization.

### `biblegateway-ephesians-6-5-9`

- **Citation:** *Ephesians* 6:5-9, New Revised Standard Version Updated Edition, Bible Gateway.
- **Source type:** Scriptural text web presentation.
- **Canonical locator:** Ephesians 6:5-9.
- **Digital URL:** https://www.biblegateway.com/passage/?search=Ephesians%206%3A5-9&version=NRSVUE
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/biblegateway-ephesians-6-5-9/page.html`
- **Integrity:** SHA-256 `270372388ae3e3c9b166104c58826a621252d94b2a958dbeb6821a80f490acc7`.
- **Rights/storage:** Public scripture-interface research capture.
- **Notes:** Confirms the instruction to slaves in verse 5 and the instruction to masters in verse 9.

### `quran-right-hands-possess`

- **Citation:** Quran 23:5-6, 70:29-30, and 4:24, with traditional commentary on 23:6, Quran.com.
- **Source type:** Scriptural text and tafsir web presentations.
- **Canonical locator:** Quran 23:5-6; 70:29-30; 4:24.
- **Digital URL:** https://legacy.quran.com/23/1-100
- **Archived URL:** https://legacy.quran.com/70/1-44 ; https://quran.com/an-nisa/24 ; https://quran.com/id/23%3A6/tafsirs/en-tafsir-maarif-ul-quran
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/quran-right-hands-possess/`
- **Integrity:** SHA-256: Quran 23 `575d406acf38e953796f804748c8f0d1c1bf64544ded4e087b9d6ff7473a620a`; Quran 70 `d40d5e5fd063b079ff5fe1ebe96edf9262af01b57de0dd5f8f70fbce2b3f8b8c`; Quran 4:24 `b127465815ab315f8f648c29d3b97dbe55d372cccadfb7fecb8749c876ce7d7c`; tafsir 23:6 `03fa39cd721dd754c48518fa3c03afcc5a0f99db16e9bc3d565a8a67715d76d3`.
- **Rights/storage:** Public scripture and commentary research captures.
- **Notes:** The verses contain the “right hands possess” formula; the commentary identifies the category as slave women or bondwomen.

### `jackson-mamluk-early-india-1990`

- **Citation:** Peter Jackson, “The Mamlūk Institution in Early Muslim India,” *Journal of the Royal Asiatic Society* 122.2 (1990), 340-358.
- **Source type:** Peer-reviewed historical article.
- **Canonical locator:** DOI 10.1017/S0035869X00108585.
- **Digital URL:** https://www.cambridge.org/core/journals/journal-of-the-royal-asiatic-society/article/abs/mamluk-institution-in-early-muslim-india/6AD31700DFD87C17F3B1DAE2EE064324
- **Archived URL:** https://doi.org/10.1017/S0035869X00108585
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/cambridge-delhi-mamluk/jackson-1990.html`
- **Integrity:** SHA-256 `7ad6d460af8984bd8692521d7f39162c8ca119b5c00bcf7f34bce6f9f0c70d9b`.
- **Rights/storage:** Public article-metadata and preview capture.
- **Notes:** The abstract and opening preview document the Ghurid introduction of the *mamlūk* military institution into Hindustan.

### `assalayana-mn93-primary`

- **Citation:** *Majjhima Nikāya* 93, *Assalāyana Sutta*; Pali Text Society edition and Ṭhānissaro Bhikkhu translation.
- **Source type:** Primary Pali text and modern translation.
- **Canonical locator:** *M* ii 149 and 153-154.
- **Digital URL:** https://www.accesstoinsight.org/tipitaka/mn/mn.093.than.html
- **Archived URL:** https://scdd.sfo2.cdn.digitaloceanspaces.com/uploads/original/2X/2/27516343af15da4af8cde92773711cf55048f1ca.pdf
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/assalayana-mn93/`
- **Integrity:** SHA-256: Pali collection PDF `5b533d207e8dca1137310f29a56df473d7ad6cb4cac05da97732db69c14e4f83`; Ṭhānissaro translation `5cd4162a7389b63e37085b209e5bfef7f20ae5d3ca1d3e02c50f2378152871e8`.
- **Rights/storage:** Public Pali research copy; translation is CC BY-NC 4.0.
- **Notes:** The checked Pali reads ***ayyo ceva dāso ca***, master and slave. ***Ayyo*** is the nominative singular of ***ayya***, a Pali form corresponding to Sanskrit **आर्य (*ārya*)**; ***dāso*** is the nominative singular of **दास (*dāsa*)**. The mule passage distinguishes human mixed parentage from a horse-donkey cross.

### `pali-english-dictionary-ayya`

- **Citation:** T. W. Rhys Davids and William Stede, *The Pali Text Society's Pali-English Dictionary* (London: Pali Text Society, 1921-1925), entries for ***ariya*** and ***ayya***.
- **Source type:** Historical Pali-English dictionary.
- **Canonical locator:** Headwords ***ariya*** and ***ayya***.
- **Digital URL:** https://theravada.vn/wp-content/uploads/2020/05/Pali-English_Dictionary_1921-25_v1.pdf
- **Archived URL:** None recorded.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/pali-english-dictionary/davids-stede-pali-english-dictionary.pdf`
- **Integrity:** SHA-256 `efbf3c20034c771e00d39965d9504ef522c179f71a9c7a0ed4acf7b6ca6cc58b`.
- **Rights/storage:** Public research copy of a historical dictionary.
- **Notes:** The dictionary identifies ***ayya*** as a Pali form of ***ariya*** and traces ***ariya*** to Vedic **आर्य (*ārya*)**. The inflected form ***ayyo*** is masculine nominative singular.

### `frankfurter-pali-grammar-ry-yy`

- **Citation:** O. Frankfurter, *Handbook of Pali: Being an Elementary Grammar, a Chrestomathy, and a Glossary* (London: Williams and Norgate, 1883), p. 14.
- **Source type:** Historical Pali grammar.
- **Canonical locator:** Phonology section, p. 14, rule 12.
- **Digital URL:** https://static.sirimangalo.org/pdf/frankfurter.pdf
- **Archived URL:** None recorded.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/pali-english-dictionary/frankfurter-handbook-of-pali.pdf`
- **Integrity:** SHA-256 `a59af9a17e756f7ca87ae1dcf44bd3963b962713a3c30efb14014ee1bf016653`.
- **Rights/storage:** Public research copy of a historical grammar.
- **Notes:** The grammar states that when Sanskrit ***r+y*** assimilates in Pali, it becomes ***yy*** rather than ***rr***, and gives Sanskrit ***ārya*** beside Pali ***ayyo*** as its example.

### `monier-williams-aravan`

- **Citation:** Monier Monier-Williams, *A Sanskrit-English Dictionary* (Oxford, 1899), s.v. ***arāvan***, University of Hyderabad digital mirror.
- **Source type:** Searchable dictionary web page.
- **Canonical locator:** Headword ***arāvan***.
- **Digital URL:** https://sanskrit.uohyd.ac.in/SKT/MW/17.html
- **Archived URL:** https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/MWScanpdf/mw0087-aratni.pdf
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/monier-williams-aravan/page.html`
- **Integrity:** SHA-256 `131c3a2abcbc5c2c5b594ebe74485ae39124a7f91937c001eb6dba9e50ddbe2f`.
- **Rights/storage:** Public dictionary research capture.
- **Notes:** The entry prints ***a-rāvan*** and gives “not liberal,” envious, and hostile.

### `etymonline-liberal-etymology`

- **Citation:** Online Etymology Dictionary, “liberal.”
- **Source type:** Etymological dictionary web page.
- **Canonical locator:** Headword “liberal.”
- **Digital URL:** https://www.etymonline.com/word/liberal
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/monier-williams-aravan/etymonline-liberal.html`
- **Integrity:** SHA-256 `fbc0bcdb8e6bc6fe121e453f77faf937c2ccf8770d5a65b031787c4d4b199007`.
- **Rights/storage:** Public dictionary research capture.
- **Notes:** Records English *liberal* through Latin ***liberalis*** and ***liber*** and includes the generosity/open-handedness sense history.

### `gretil-maitrayani-samhita`

- **Citation:** *Maitrāyaṇī Saṃhitā*, electronic text from TITUS, based on Leopold von Schroeder's edition, GRETIL analytic presentation.
- **Source type:** Electronic Vedic primary text.
- **Canonical locator:** MS 1.9.3.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/1_sam/maitrs_au.htm
- **Archived URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/1_sam/maitrs_pu.htm
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/gretil-maitrayani-samhita/maitrs_au.htm`
- **Integrity:** SHA-256 `0ab4eedb96b2dcba8c0b0b8687dd222e36caee98c72a68ea712521eb63db1a70`.
- **Rights/storage:** Reference-use electronic text; research capture retained.
- **Notes:** MS 1.9.3 contains ***satyena devān asṛjatānṛtenāsurān, te devāḥ satyam abhavan, anṛtam asurāḥ***.

### `becker-heavenly-city-1932`

- **Citation:** Carl L. Becker, *The Heavenly City of the Eighteenth-Century Philosophers* (Yale University Press, 1932; 70th-anniversary edition, 2003).
- **Source type:** Copyrighted monograph, searchable limited preview.
- **Canonical locator:** Lectures III-IV; 2003 edition, especially pp. 31 and 139-155.
- **Digital URL:** https://books.google.com/books?id=XjfPR77yihIC
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-secular-eschatology/becker-google-books/`
- **Integrity:** SHA-256: metadata `e6e5201d2855ecad2ca1675cdeae3b522b6b1be6b08fe831c2165d58c7d851bb`; “heavenly city” results `d174d25559ce3cba12431d68381cc9cac647a21955d2470bf69b8ffae1c43905`; “religion of humanity” results `8d31b1d08aaaf740c479781a40cde4ad4f7ce650a18525f43b1addf1a32f3825`.
- **Rights/storage:** Search-result extracts and public bibliographic metadata retained for research.
- **Notes:** Confirms Becker's comparison between Augustine's heavenly city and the philosophes' secular reconstruction, including posterity and the “religion of humanity.” It does not establish that Becker invented the broader continuity thesis.

### `chapter4-scriptural-architecture`

- **Citation:** Deuteronomy 7:6; Isaiah 11; Matthew 28:19-20; Revelation 20-21; Quran 3:110 and 75.
- **Source type:** Primary scriptural texts in public digital presentations.
- **Canonical locator:** The passages listed above.
- **Digital URL:** https://www.biblegateway.com/passage/?search=Deuteronomy%207%3A6%3BIsaiah%2011%3BMatthew%2028%3A19-20%3BRevelation%2020-21&version=KJV ; https://quran.com/3/110 ; https://quran.com/75
- **Archived URL:** Same as the digital URLs.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-secular-eschatology/scriptural-mapping/`
- **Integrity:** SHA-256: Deuteronomy 7:6 `3f16b38ac12f624a272727e337b7f67fd49fc0aad062ab13811f85f46bc0ae30`; Isaiah 11 `3bbb8bf783668c8045e49ecaa4829148bb8b5c63bc20f0700d41e5eeeb2c65b2`; Matthew 28:19-20 `cf4e7453c76fad8af6bb3172d445a968d997a43aa3e9b653303a4c103094fe87`; Revelation 20 `d2007180a034f779a04df07bb7b3d8cd73305074da688180e94eb2ea6f7e7990`; Revelation 21 `fc622f0da2937b5e40eef54759abeedb2a23609af0e5f385cdedbcd4e875f005`; Quran 3:110 `26ae635714d42a221be18e6a3816506e0250df1354f7b155ef155fd259564d74`; Quran 75 `afd8d4876e595e28b8f8dbd143e650ca9258ae4f04a915788824844f27bd4d7a`.
- **Rights/storage:** Public-domain Bible text and public Quran API research captures.
- **Notes:** The passages anchor the chosen-community, Christian-mission, and eschatology columns in Figures 4.1a-b. Judaism's covenantal boundary is not a universal conversion command.

### `lemaitre-hawking-cosmology-creation`

- **Citation:** Georges Lemaître, “The Beginning of the World from the Point of View of Quantum Theory,” *Nature* 127 (1931), 706; Stephen Hawking, *A Brief History of Time* (Bantam, 1988), Chapter 8 and Conclusion; UCLouvain Archives, “Commencement ou Création?”
- **Source type:** Scientific primary source, published monograph, and institutional archive.
- **Canonical locator:** Lemaître 1931, p. 706; Hawking, Chapter 8 and Conclusion; UCLouvain sections “Commencement ou Création?” and “Pie XII et le discours Un'Ora.”
- **Digital URL:** https://doi.org/10.1038/127706b0 ; https://archives.uclouvain.be/exhibits/show/georges-lemaitre/commencement-ou-creation
- **Archived URL:** Same as the digital URLs.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch4-secular-eschatology/lemaitre/lemaitre-1931.pdf`; `working/40_reference/sources/archive/web/ch4-secular-eschatology/ucl-lemaitre/commencement-creation.html`; `working/40_reference/sources/archive/web/ch4-secular-eschatology/hawking/brief-history.html`.
- **Integrity:** SHA-256: Lemaître PDF `ad92901fe343f989b6d10eaecdecd0ca328c76bcaad846059d0aa11b90206164`; UCLouvain capture `e7efdaa21f9b67e0718b8a99c21e05fbcefe9a91e2ced05858ba3e98873f3b06`; searchable Hawking guide `23b0d975c63713f6271f8349d34f28f2dedac473ece3fcc336b0d8ab192d192f`.
- **Rights/storage:** Scientific article and public institutional web captures retained for research; Hawking book cited bibliographically rather than archived.
- **Notes:** Lemaître distinguished a physical beginning from theological creation and objected when the two were conflated. Hawking's “mind of God” is used for complete physical law. The archived Hawking web page is an independent searchable guide, not an official estate publication.

### `fukuyama-end-history-1989`

- **Citation:** Francis Fukuyama, “The End of History?” *The National Interest* 16 (Summer 1989), 3-18.
- **Source type:** Published political essay.
- **Canonical locator:** p. 4; discussion of Hegel and Kojève throughout pp. 3-6.
- **Digital URL:** https://www.jstor.org/stable/24027184
- **Archived URL:** Internet Archive research scan.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch4-secular-eschatology/fukuyama/fukuyama-1989.pdf`
- **Integrity:** SHA-256 `ae67afc11037ecb49bf506dabd1f7aeb6a744f487808106def4f9df20f0645e0`.
- **Rights/storage:** Research copy retained; citation points to the stable JSTOR record.
- **Notes:** Fukuyama calls Western liberal democracy the endpoint of ideological evolution and the final form of human government. He does not call the argument a secularized Abrahamic eschatology; that genealogy is supplied by the book and by Gray.

### `voegelin-new-science-politics-1952`

- **Citation:** Eric Voegelin, *The New Science of Politics: An Introduction* (University of Chicago Press, 1952).
- **Source type:** Published political-theory monograph.
- **Canonical locator:** “Gnosticism: The Nature of Modernity,” pp. 107-132, especially 119-121 and 126-132.
- **Digital URL:** https://archive.org/details/newscienceofpoli0000voeg
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch4-secular-eschatology/voegelin/voegelin-new-science-politics.pdf`; searchable OCR in the same directory.
- **Integrity:** SHA-256: PDF `41ec3818259fc3bbd8ba306d353427293c5b053d5409d9dbbbd7b7e59522289b`; OCR `d0cbcd806e51c9ec282aa0196935a6782b52f1a5d78d3f3b9a909cf66e780b11`.
- **Rights/storage:** Borrowable/archive research copy and derived OCR retained for verification.
- **Notes:** Voegelin explicitly identifies progressivism, utopianism, and revolutionary activism as forms of immanentization and describes progressivism, positivism, and scientism traveling as Westernization and the development of “backward countries.”

### `gray-black-mass-2007`

- **Citation:** John Gray, *Black Mass: Apocalyptic Religion and the Death of Utopia* (Allen Lane, 2007).
- **Source type:** Copyrighted monograph, searchable limited preview.
- **Canonical locator:** Chapter 1; discussion of Fukuyama at preview locations PT11 and PT161-163.
- **Digital URL:** https://books.google.com/books?id=Ba7hNX9x-fwC
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-secular-eschatology/gray-google-books/`
- **Integrity:** SHA-256: metadata `6452f4225ad47317e3525a9199fadbf6a60ed5ca0b36db0b49cdbc3fb03f7b39`; Fukuyama results `edcb618704b2c554ff31320bd8afadcbea098a3fc60757a066f8bbe978d7d421`; end-of-history results `32db40a2202c0f5612815fbef6dcce9292fe8e6f142f80eba1354a36756af150`; utopian-thinking results `7e9fce5c2c3da712240c5967b2651351aae1fc0ade46b7101c1ad0e9cf0aea5b`.
- **Rights/storage:** Search-result extracts and public bibliographic metadata retained for research.
- **Notes:** Gray links modern political utopias and Fukuyama's teleology to Christian apocalyptic forms. The climate application belongs to a separate endnote.

### `laird-climate-narrative-2022`

- **Citation:** Frank N. Laird, “The ‘Save the Earth!’ Narrative Creates a Narrative Trap for Climate Advocates,” *Frontiers in Climate* 4 (2022), article 900672.
- **Source type:** Peer-reviewed open-access article.
- **Canonical locator:** DOI 10.3389/fclim.2022.900672; sections “The Narrative Trap” and “A Different Narrative.”
- **Digital URL:** https://doi.org/10.3389/fclim.2022.900672
- **Archived URL:** https://www.frontiersin.org/journals/climate/articles/10.3389/fclim.2022.900672/full
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-secular-eschatology/climate-apocalypse/save-earth-narrative.html`
- **Integrity:** SHA-256 `75984d3be1a59ff0016af0600e7113696414820c1ad2d5d5db5bc3d91a3e13f3`.
- **Rights/storage:** CC BY open-access article capture.
- **Notes:** Documents the linked “save the earth,” “no choice,” and “political will” claims and locates them within apocalyptic environmentalism.

### `tope-gawd-climate-2012`

- **Citation:** Parag Tope, “A Fart Tax and a Pink Revolution Can ‘Save the World’,” *Quick Take*, December 6, 2012.
- **Source type:** Author's earlier public essay.
- **Canonical locator:** Complete post.
- **Digital URL:** https://quicktake.wordpress.com/2012/12/06/indias-pink-revolution-can-save-the-world/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-secular-eschatology/tope-climate/post.html`
- **Integrity:** SHA-256 `918bf155943c7eb6e29753a9ffa55f477f275734bd743182f7aa893418698a30`.
- **Rights/storage:** Author's own public essay retained for research.
- **Notes:** Establishes the author's prior use of the doomsday-cult analogy and the ***GaWD*** coinage. It is not used as independent evidence for the broader pattern.

### `ambedkar-pakistan-close-corporation`

- **Citation:** B. R. Ambedkar, *Pakistan, or the Partition of India*, in *Dr. Babasaheb Ambedkar: Writings and Speeches*, vol. 8 (Government of Maharashtra, 1990).
- **Source type:** Government-collected edition of the 1945 book.
- **Canonical locator:** Chapter XII, “National Frustration,” pp. 330-331.
- **Digital URL:** https://archive.org/details/PARI.dr-babasaheb-ambedkar-vol-8-pakistan-or-the-partition-of-india
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch4-secular-eschatology/ambedkar/baws-vol8.pdf`; searchable OCR in the same directory.
- **Integrity:** SHA-256: PDF `469182b118d1125d55f2c58cb883dea06cf207145a43b171794dd856e6edf99e`; OCR `5adb4a558cfdd22d6d02739732d23e87d337ced3976041adfe612c322f7285fb`.
- **Rights/storage:** Government edition and searchable OCR retained for verification.
- **Notes:** The quoted “close corporation” passage is on pp. 330-331. The previous endnote incorrectly assigned it to Chapter X and pp. 330-332.

### `rostow-stages-growth-1960`

- **Citation:** W. W. Rostow, *The Stages of Economic Growth: A Non-Communist Manifesto* (Cambridge University Press, 1960).
- **Source type:** Published economics monograph.
- **Canonical locator:** Introduction, pp. 1-3; Chapter 2, pp. 4-16.
- **Digital URL:** https://archive.org/details/dli.ernet.507775
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch4-secular-eschatology/rostow/rostow-1960.pdf`; searchable OCR in the same directory.
- **Integrity:** SHA-256: PDF `c87bacfb2b71e9db73590429212e5d38b7512e9cca48afa3046b7d11e930c532`; OCR `53d3857bf3bdd09851b1b8e91898c952be4bece117cc9e9f0442a713a783fffa`.
- **Rights/storage:** Public archive research copy and OCR retained for verification.
- **Notes:** Rostow lists the five categories in Chapter 2. In the introduction he calls the scheme “arbitrary and limited” and denies that it is correct in any absolute sense. This source does not by itself establish a direct institutional chain to the World Bank or the Sustainable Development Goals.

### `tope-missionaries-progress-2011`

- **Citation:** Parag Tope, “Missionaries of 'Progress',” *Quick Take*, October 29, 2011.
- **Source type:** Author's earlier public essay.
- **Canonical locator:** Complete post.
- **Digital URL:** https://quicktake.wordpress.com/2011/10/29/missionaries-of-progress/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-completion/missionaries-progress/page.html`.
- **Integrity:** SHA-256 `7e5c7ba019e6b4d01d21b3435a7a6b6b0947728968a6760b0657732f374b73cf`.
- **Rights/storage:** Author's own public essay retained for research.
- **Notes:** Establishes the author's prior use of *missionaries of progress* for NGOs exporting Western ideas of progress as universal. It is not independent evidence for Chapter 4's larger claim.

### `popular-pie-public-syntheses`

- **Citation:** David W. Anthony, *The Horse, the Wheel, and Language* (Princeton University Press, 2007); David Reich, *Who We Are and How We Got Here* (Pantheon, 2018); Tony Joseph, *Early Indians* (Juggernaut, 2018); Laura Spinney, *Proto* (William Collins / Bloomsbury, 2025).
- **Source type:** Public-facing books and publisher descriptions.
- **Canonical locator:** Anthony, publisher description and chapters 13-16; Reich, Chapter 6; Joseph, publisher description; Spinney, publisher description.
- **Digital URL:** https://www.jstor.org/stable/j.ctt7sjpn
- **Archived URL:** https://www.penguinrandomhouse.com/books/247850/who-we-are-and-how-we-got-here-by-david-reich/ ; https://www.juggernaut.in/products/early-indians-the-story-of-our-ancestors-and-where-we-came-from ; https://books.google.com/books?id=nZoZEQAAQBAJ
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-completion/popular-pie/`; Reich research copy at `working/40_reference/sources/archive/documents/ch4-completion/popular-pie/reich.pdf`.
- **Integrity:** SHA-256: Anthony Princeton catalogue `0e5c6ef82afa3f094f785678ee0ebfa753db4ebb064289ea9e5e42e44942916b`; Reich publisher page `53fae249737e1c251216c8a2bdf10dd209c3e3c104f970da0beb89986ca2281b`; Reich research PDF `0731321195058faf0319e12ec9637f1337360ab2bdaeb0ca38902939df6855a7`; Joseph publisher page `43ac17280bc5f76c1cffa318b44ccbe4c927660241899c8574e2f5aa8e0e79fa`; Spinney Google Books page `be163ea630d0ec159386a80108192c6a890f349c9337f17d34b863d72a76e2ef`.
- **Rights/storage:** Public publisher pages, publisher catalogue, bibliographic page, and a research copy retained for verification.
- **Notes:** The records verify that the four books carry complementary parts of the PIE-steppe account to general readers. The description of that role as *missionaries of progress* is Chapter 4's analysis.

### `harvard-murty-library-2010`

- **Citation:** “Murty family gift establishes Murty Classical Library of India series,” *Harvard Gazette*, April 29, 2010.
- **Source type:** Official university announcement.
- **Canonical locator:** Complete announcement, especially the funding, editorial, and publication details.
- **Digital URL:** https://news.harvard.edu/gazette/story/2010/04/murty-family-gift-establishes-murty-classical-library-of-india-series/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-completion/murty-library/harvard-gazette.html`.
- **Integrity:** SHA-256 `11db7d12eabdcbdffe63d87f494794451d979fd6b3b01a1805357b06d45524f9`.
- **Rights/storage:** Public institutional announcement retained for research.
- **Notes:** Confirms the $5.2 million gift, Harvard University Press series, Sheldon Pollock's general editorship, editorial board, and facing-page format. It does not describe the project as circulating Pollock's culture-and-power thesis.

### `juvenal-satire6-custodes`

- **Citation:** Juvenal, *Satires* 6.346-348; G. G. Ramsay edition and translation (Loeb Classical Library 91, 1918).
- **Source type:** Latin primary text and public-domain edition.
- **Canonical locator:** Satire 6.346-348 and the parallel at Oxford fragment O 29-34.
- **Digital URL:** https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A2007.01.0093%3Abook%3D2%3Apoem%3D6
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-completion/juvenal/perseus-satire6.html`.
- **Integrity:** SHA-256 `ada471230a5fd724c5072d6d3b0f9b1f8c388362c016d1d7adab2e0ef43991f3`.
- **Rights/storage:** Public-domain classical text retained for research.
- **Notes:** Confirms the phrase and its immediate context: guards imposed upon a wife are themselves corruptible. Ramsay's apparatus records a longer parallel in the Oxford fragment; editions differ over placement and textual history.

### `mahabharata-ashtavakra-bandin`

- **Citation:** *Mahābhārata*, *Vana Parva*, sections 132-134, trans. Kisari Mohan Ganguli.
- **Source type:** Itihāsa primary narrative in a public-domain English translation.
- **Canonical locator:** Section 132 for Kahoḍa and Aṣṭāvakra's arrival; section 133 for the doorkeeper; section 134 for the debate and return from Varuṇa's sacrifice.
- **Digital URL:** https://getgnosis.app/read/mahabharata/447/
- **Archived URL:** https://getgnosis.app/read/mahabharata/448/ ; https://getgnosis.app/read/mahabharata/449/
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-completion/ashtavakra-bandin/`.
- **Integrity:** SHA-256: section 132 `11651db99a46d9a5c40ebb9a169feae123bcd5bc12b9a48f919cb33ede5c7acc`; section 133 `207321565040c4ba4e235fe991d82015b87683acdf0e4c38c6da85b073d0b694`; section 134 `e2397dee1f65368cccec380a40fa560eb8acfd3f59b287f8e29e485a50fb985a`.
- **Rights/storage:** Public-domain translation retained for research.
- **Notes:** The doorkeeper excludes Aṣṭāvakra because he is young, not because of bodily deformity. The text says the defeated Brahmins attended Varuṇa's sacrifice, not that nāgas detained them.

### `rigveda-9-63-5-translations`

- **Citation:** Ṛgveda 9.63.5 in H. H. Wilson, Ralph T. H. Griffith, and Stephanie W. Jamison and Joel P. Brereton.
- **Source type:** Vedic primary text, padapāṭha, and three published translations.
- **Canonical locator:** Ṛgveda 9.63.5; Jamison and Brereton, vol. 3, pp. 1286-1287.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc837811.html
- **Archived URL:** https://rigveda-online.github.io/9/63.html ; https://wiswo.org/books/_resources/book-reference-pdfs/Jamison-Brereton-2014-The%20Rigveda-The%20Earliest%20Poetry%20of%20India%20all%203%20Volume%20Sets.pdf
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch4-completion/rigveda-9635/`; Jamison-Brereton research copy at `working/40_reference/sources/archive/documents/rigveda-9635/jamison-brereton-rigveda.pdf`.
- **Integrity:** SHA-256: Wilson display `cfadad01e6f8ed0b06c084561e0b096de8143e0c2c7b533c7a81c91625ed8b24`; Griffith display `6f0235fe035bfabb101c9761a0f15247b112b80a82faba218c35a4261d0c98f4`; Jamison-Brereton PDF `0ab278d9696f584ea0fbbb4720ea20dcbf6c33ae69f886a6580ac4667bfc36ab`.
- **Rights/storage:** Public web presentations and a research copy retained for verification.
- **Notes:** Confirms the Sanskrit and padapāṭha, Wilson's “all our acts prosperous” and “withholders (of oblations),” Griffith's “every noble work” and “godless ones,” and Jamison-Brereton's “making it all Ārya” and “non-givers.” The translation comparison establishes the changed content, not the translators' private motive.
### `kielhorn-mahabhashya-v1`

- **Citation:** F. Kielhorn, ed., *The Vyākaraṇa-Mahābhāṣya of Patañjali*, volume 1 (Bombay: Government Central Book Depot, 1880).
- **Source type:** Public-domain critical edition.
- **Canonical locator:** *Paspaśāhnika*, especially printed pp. 1-6.
- **Digital URL:** https://archive.org/details/india.history.resource.78451
- **Archived URL:** https://archive.org/download/india.history.resource.78451/78451.pdf
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch5-verification/kielhorn-mahabhashya-v1/`.
- **Integrity:** Aggregate SHA-256 over the archived PDF, OCR text, and scan metadata: `23be5c284984efd213ab9e4bcd9e7c02f7f0abab6a04e40b613c0773488e1cf2`.
- **Rights/storage:** Public-domain edition retained for research.
- **Notes:** Primary edition used to check the *Paspaśāhnika* sequence and printed locators.

### `vishvasa-paspashahnika-full`

- **Citation:** Patañjali, *Vyākaraṇa-Mahābhāṣya*, *Paspaśāhnika*, digital Sanskrit presentation based on the Kielhorn edition.
- **Source type:** Searchable primary-text transcription with visibly marked editorial annotations.
- **Canonical locator:** Complete *Paspaśāhnika*; files 1-12.
- **Digital URL:** https://vishvasa.github.io/sanskrit/vyAkaraNam/pANinIyam/mUlAni/mahA-bhAShyam/sarva-prastutiH/01_paspashAhnikam/
- **Archived URL:** https://github.com/vishvAsa/sanskrit/tree/content/vyAkaraNam/pANinIyam/mUlAni/mahA-bhAShyam/sarva-prastutiH/01_paspashAhnikam
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch5-verification/vishvasa-paspashahnika/`.
- **Integrity:** Aggregate SHA-256 over thirteen Markdown source files: `adcad232e534c23f40bc709367d9857d610722f3e84ce2ba43c048f3462cc03e`.
- **Rights/storage:** Public digital text retained for research.
- **Notes:** Original text and modern annotations are typographically distinguishable. Checks use the original Sanskrit and confirm it against Kielhorn.

### `subramanya-sastri-mahabhashya-lectures-v1`

- **Citation:** P. S. Subrahmanya Sastri, *Lectures on Patañjali's Mahābhāṣya*, volume 1.
- **Source type:** Public-domain translation and commentary.
- **Canonical locator:** *Paspaśāhnika*, pp. 19-24 for the purposes of grammar and pp. 49-60 for Kātyāyana's first *vārttika* and Patañjali's discussion.
- **Digital URL:** https://archive.org/details/LecturesOnPatanjalisVyakaranaMahabhashya1
- **Archived URL:** https://archive.org/download/LecturesOnPatanjalisVyakaranaMahabhashya1/LecturesMahabhasya_djvu.txt
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch5-verification/subramanya-sastri-lectures/LecturesMahabhasya_djvu.txt`.
- **Integrity:** SHA-256 `d0af718431c545f200104406f4bec80857bed9199346e6ccb06c9d95c0949e7d`.
- **Rights/storage:** Public-domain OCR retained for research.
- **Notes:** Used as a translation check. The OCR is imperfect, so Sanskrit readings are checked against Kielhorn and the Vishvasa transcription.

### `monier-williams-vyakarana-entries`

- **Citation:** Monier Monier-Williams, *A Sanskrit-English Dictionary* (1899), entries ***vy-ā-√kṛ***, ***vyākaraṇa***, and ***vaiyākaraṇa***, Cologne Digital Sanskrit Lexicon.
- **Source type:** Digital historical lexicon.
- **Canonical locator:** Printed pp. 1024 and 1035; Cologne record IDs 207425-207427 and 209443-209451.
- **Digital URL:** https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc/indexcaller.php
- **Archived URL:** Exact entry responses retained locally.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch5-verification/monier-williams/`.
- **Integrity:** Aggregate SHA-256 over three HTML entry records: `91108bf4ae5fcd915333ed98459d60bdf978744fa6734629226e17ba04381b74`.
- **Rights/storage:** Public historical dictionary entries retained for research.
- **Notes:** The verb means to undo, divide, separate, expound, or explain. In the grammatical domain, the noun means grammatical analysis or grammar; the agent noun means grammarian. “Decoder” is the book's architectural description of the demonstrated work, not the dictionary's literal gloss of the title.

### `ashtadhyayi-open-close`

- **Citation:** Pāṇini, *Aṣṭādhyāyī* 1.1.1 and 8.4.68, digital sūtra displays.
- **Source type:** Digital primary-text and commentary pages.
- **Canonical locator:** 1.1.1 **वृद्धिरादैच्** and 8.4.68 **अ अ**.
- **Digital URL:** https://ashtadhyayi-lite.github.io/sutra/1.1.1.html
- **Archived URL:** https://ashtadhyayi-lite.github.io/sutra/8.4.68.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch5-verification/ashtadhyayi-open-close/`.
- **Integrity:** Aggregate SHA-256 over the two HTML records: `649e8dc369e85dc46563bcab90dd37632a811e4d4da5bf02831ce548f81fbd35`.
- **Rights/storage:** Public digital grammatical pages retained for research.
- **Notes:** Supports the narrow observation that the received *sūtrapāṭha* begins directly with 1.1.1 and ends with 8.4.68.

### `macdonell-shakalya-padapatha`

- **Citation:** Arthur A. Macdonell, *A History of Sanskrit Literature* (London: William Heinemann, 1900), pp. 50-51.
- **Source type:** Public-domain secondary history.
- **Canonical locator:** Chapter 3, account of the Ṛgvedic *Pada* text and its attribution to Śākalya.
- **Digital URL:** https://www.gutenberg.org/ebooks/41563
- **Archived URL:** https://archive.org/details/ahistoryofsanskr41563gut
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch5-verification/macdonell-history-sanskrit-literature.html`.
- **Integrity:** SHA-256 `1ca606171dd15d20c4ff9aad16e2ccad01e331d13c7b5c17303cbae1fe3886e4`.
- **Rights/storage:** Public-domain book retained for research.
- **Notes:** Records the traditional attribution of the Ṛgvedic *Padapāṭha* to Śākalya and describes the text as an analysis that presents words independently. It does not say that the *Padapāṭha* supplies grammatical case and number.

### `ashtadhyayi-shakalya-rules`

- **Citation:** Pāṇini, *Aṣṭādhyāyī* 1.1.16, 6.1.127, and 8.4.51, with *Kāśikā* and modern explanatory material, Aṣṭādhyāyī Lite.
- **Source type:** Digital primary-text and commentary pages.
- **Canonical locator:** 1.1.16 **सम्बुद्धौ शाकल्यस्येतावनार्षे**; 6.1.127 **इकोऽसवर्णे शाकल्यस्य ह्रस्वश्च**; 8.4.51 **सर्वत्र शाकल्यस्य**.
- **Digital URL:** https://ashtadhyayi-lite.github.io/sutra/1.1.16.html
- **Archived URL:** https://ashtadhyayi-lite.github.io/sutra/6.1.127.html ; https://ashtadhyayi-lite.github.io/sutra/8.4.51.html
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch5-verification/shakalya-rules/`.
- **Integrity:** Aggregate SHA-256 over the three HTML records: `51126ff64ba6ff9ada40a7079f0e08e4c5a9e8a79bea73c61415bae04e220f59`.
- **Rights/storage:** Public digital grammatical pages retained for research.
- **Notes:** These rules concern optional *pragṛhya* treatment, word-final *ik* before a dissimilar vowel, and the prohibition of consonant doubling in Śākalya's analysis. They do not concern compound boundaries, *visarga*, or *anusvāra*. Rule 8.3.18 names Śākaṭāyana, not Śākalya.

### `unesco-angkor-advisory-1992`

- **Citation:** UNESCO, *Angkor: World Heritage List Advisory Body Evaluation* (1992).
- **Source type:** Official heritage evaluation.
- **Canonical locator:** pp. 14-15, vegetation and structural damage.
- **Digital URL:** https://whc.unesco.org/archive/advisory_body_evaluation/668.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch6-verification/unesco-angkor-evaluation.pdf`.
- **Integrity:** SHA-256 `2bd5fba5cc9f0db4ec7da5abcaa775d3c34a924e94ed981335ba58cff2fcb320`.
- **Rights/storage:** Public institutional document retained for research.
- **Notes:** Documents vegetation and root damage at Angkor; used for the Ta Prohm entropy analogy.

### `census-central-india-1911-caste`

- **Citation:** C. E. Luard, *Central India State Census Series, Volume III: Census of India, 1911* (1913).
- **Source type:** Official colonial census report.
- **Canonical locator:** vol. 1, pp. 218-221, caste classification and social precedence.
- **Digital URL:** https://censusindia.gov.in/nada/index.php/catalog/28385
- **Archived URL:** https://censusindia.gov.in/nada/index.php/catalog/28385/download/31567/THE_CENTRALINDIA_STATE_CENSUS_SERIES_VOLUME_111_1911.pdf
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch6-verification/census/central-india-census-1911.pdf`.
- **Integrity:** SHA-256 `f74a87bd4ddc1d9ddea3a40ca10b8956c14a68f959e233bcc3550f7c56ebc801`.
- **Rights/storage:** Official historical census scan retained for research.
- **Notes:** Records the 1901 social-precedence classification, its disputes, and the controlled index of caste names.

### `rosa-law-public-law-111-256`

- **Citation:** Rosa's Law, Public Law 111-256, 124 Stat. 2643-2645 (2010).
- **Source type:** Official United States statute.
- **Canonical locator:** §§2-8, 124 Stat. 2643-2645.
- **Digital URL:** https://www.congress.gov/111/plaws/publ256/PLAW-111publ256.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch6-verification/rosa-law-public-law-111-256.pdf`.
- **Integrity:** SHA-256 `0d9f66f4376f47cc7e867e6a4faa6589ef21ef76f7abb8d61c0139d8e1f2a7ca`.
- **Rights/storage:** Public government document retained for research.
- **Notes:** Establishes the statutory terminology substitutions used in the endnote.

### `apa-dsm5-terminology-change`

- **Citation:** American Psychiatric Association, *Highlights of Changes from DSM-IV-TR to DSM-5* (2013).
- **Source type:** Official professional-association guide.
- **Canonical locator:** p. 1, “Intellectual Disability (Intellectual Developmental Disorder).”
- **Digital URL:** https://www.psychiatry.org/File%20Library/Psychiatrists/Practice/DSM/APA_DSM_Changes_from_DSM-IV-TR_-to_DSM-5.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch6-verification/apa-dsm5-changes.pdf`.
- **Integrity:** SHA-256 `a48f54ded6664b7aeea4d71e485b5a83e7c10d017a03e2ade8a187ef12704ec6`.
- **Rights/storage:** Public institutional guide retained for research.
- **Notes:** Confirms the change from the DSM-IV term to *intellectual disability* in DSM-5.

### `pinker-game-of-name-1994`

- **Citation:** Steven Pinker, “The Game of the Name,” *The New York Times*, April 5, 1994, p. A21.
- **Source type:** Newspaper essay by the person who introduced the phrase used by the chapter.
- **Canonical locator:** Complete article, especially the paragraph naming the “euphemism treadmill.”
- **Digital URL:** https://stevenpinker.com/files/pinker/files/1994_04_03_newyorktimes.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch6-verification/pinker-1994-euphemism-treadmill.pdf`.
- **Integrity:** SHA-256 `3661be064df72ad23bfcf64f802af0999089b49aad5758f4ad7cce248540b7c6`.
- **Rights/storage:** Research copy retained for verification.
- **Notes:** Supports the name and example of the euphemism treadmill, not the chapter's larger calibrant interpretation.

### `akademio-esperanto-fundamento`

- **Citation:** Akademio de Esperanto, *Akademia Vortaro: Klarigoj*.
- **Source type:** Official Esperanto language-institution record.
- **Canonical locator:** Count of 2,768 foundational elements.
- **Digital URL:** https://www.akademio-de-esperanto.org/akademia_vortaro/klarigoj.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch6-verification/esperanto-akademia-vortaro.html`.
- **Integrity:** SHA-256 `cd42ef5fe3413cd3b808471b3aef2c8fd4ba9338f0e6605f74b7aaa50b8ccca3`.
- **Rights/storage:** Public institutional page retained for research.
- **Notes:** Supplies the official inventory count used in the Esperanto comparison.

### `akademio-esperanto-oficialaj-aldonoj`

- **Citation:** Akademio de Esperanto, *Oficialaj Aldonoj*.
- **Source type:** Official Esperanto language-institution record.
- **Canonical locator:** First Official Addition in 1909 and later additions.
- **Digital URL:** https://www.akademio-de-esperanto.org/verkoj/oficialaj_aldonoj.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch6-verification/esperanto-oficialaj-aldonoj.html`.
- **Integrity:** SHA-256 `134d3660358959c0e6b531601ae78ebc3cba44d0113dae23404e8f9c6325a26c`.
- **Rights/storage:** Public institutional page retained for research.
- **Notes:** Documents official additions after publication of the *Fundamento*.

### `zamenhof-fundamento-antauparolo`

- **Citation:** L. L. Zamenhof, *Fundamento de Esperanto*, *Antaŭparolo* (1905).
- **Source type:** Primary Esperanto programmatic text.
- **Canonical locator:** Passage permitting new words for ideas not conveniently expressed by the existing stock.
- **Digital URL:** https://www.akademio-de-esperanto.org/fundamento/antauparolo.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch6-verification/esperanto-fundamento-antauparolo.html`.
- **Integrity:** SHA-256 `29cb7e2ccce770f04217b9cd8280a5d66bac9ecb265d3e63009c943299f2dab6`.
- **Rights/storage:** Public historical text retained for research.
- **Notes:** Establishes that use could introduce and settle additional vocabulary.

### `macdonell-vedic-grammar-1916`

- **Citation:** Arthur A. Macdonell, *A Vedic Grammar for Students* (Oxford, 1916).
- **Source type:** Public-domain historical grammar.
- **Canonical locator:** Preface, printed pp. v-vi.
- **Digital URL:** https://archive.org/details/vedicgrammar00macd
- **Archived URL:** Same collection; OCR retained locally.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch5-verification/macdonell-vedic-grammar/vedicgrammar00macd_djvu.txt`.
- **Integrity:** SHA-256 `88a2ff7c27b908fd09dc2fde20cc8f2be332c938a2c4f3d6576ffd9d637be5bd`.
- **Rights/storage:** Public-domain OCR retained for research.
- **Notes:** Used to verify the explicit chronological framing of Vedic and later Sanskrit.

### `witzel-vedic-canon-1997`

- **Citation:** Michael Witzel, “The Development of the Vedic Canon and its Schools,” in *Inside the Texts, Beyond the Texts* (Harvard Oriental Series, Opera Minora 2, 1997), pp. 257-345.
- **Source type:** Scholarly chapter presenting an internal chronology of Vedic texts.
- **Canonical locator:** pp. 257-345, especially the linguistic levels and concluding sequence.
- **Digital URL:** https://michaelwitzel.org/wp-content/uploads/2014/06/canon.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch6-verification/witzel/vedic-canon-1997.pdf`.
- **Integrity:** SHA-256 `40c26122cc34adc94ecd84543de5436e04a570970465eb25a7111da8541d1532`.
- **Rights/storage:** Research copy retained for verification.
- **Notes:** Documents the chronological inference that Chapter 6 disputes.

### `dales-mythical-massacre-1964`

- **Citation:** George F. Dales, “The Mythical Massacre at Mohenjo-Daro,” *Expedition* 6.3 (1964), pp. 36-43.
- **Source type:** Archaeological reassessment.
- **Canonical locator:** Complete article, especially the review of the thirty-seven skeletons and Room 74 group.
- **Digital URL:** https://www.penn.museum/sites/expedition/the-mythical-massacre-at-mohenjo-daro/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch6-verification/dales-mythical-massacre.html`.
- **Integrity:** SHA-256 `08a3fb41263597d32205fb04401f2e649bef3bada8349f3fa0b9ea9fa3337f31`.
- **Rights/storage:** Public museum article retained for research.
- **Notes:** Corrects the chapter note's former conflation of a fourteen-skeleton group with a separate six-skeleton group.

### `gosvami-human-voice-1957`

- **Citation:** O. Gosvami, *The Story of Indian Music: Its Growth and Synthesis* (Asia Publishing House, 1957).
- **Source type:** Historical survey of Indian music.
- **Canonical locator:** Chapter 12, “The Human Voice in Music.”
- **Digital URL:** https://openlibrary.org/books/OL31956449M/The_story_of_Indian_music
- **Archived URL:** https://archive.org/details/storyofindianmus0000unse
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch7-verification/gosvami-human-voice-1957.pdf`.
- **Integrity:** SHA-256 `f179479cd6532cc2f10d5ee8f96ef6e2ecc35f5a6a184f1c2b587a763bd981c5`.
- **Rights/storage:** Research copy retained for verification.
- **Notes:** Supports the priority given to vocal music; it does not attest the compound **ādi-vādya** as an ancient title.

### `allen-phonetics-ancient-india-1953`

- **Citation:** W. Sidney Allen, *Phonetics in Ancient India* (Oxford University Press, 1953).
- **Source type:** Modern phonetic study of Sanskrit source traditions.
- **Canonical locator:** Printed pp. 17-23 and 33-36.
- **Digital URL:** https://archive.org/download/in.gov.ignca.7855/7855.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch7-verification/allen-phonetics-in-ancient-india.pdf` and `.txt`.
- **Integrity:** PDF SHA-256 `c7691a863277648dc305a2999760d208bac3ebe3bcf180df62e5c10b73a9aa42`; OCR SHA-256 `feb5fc3aa0b577ad9ae6dbf5d8f0abe8b3e14228d3ba75cb1caeb1928893314c`.
- **Rights/storage:** Public archive copy retained for research.
- **Notes:** Used as a secondary cross-check for *sthāna*, *karaṇa*, internal and external *prayatna*, breath, voice, and voiced aspiration.

### `laghukaumudi-prayatna`

- **Citation:** *Laghu-siddhānta-kaumudī*, *Saṃjñā-prakaraṇam*, explanation of **तुल्यास्यप्रयत्नं सवर्णम्**.
- **Source type:** Digital Sanskrit grammatical text.
- **Canonical locator:** Passage beginning **आद्यः पञ्चधा** and the following list beginning **बाह्यप्रयत्नस्त्वेकादशधा**.
- **Digital URL:** https://ashtadhyayi.com/laghukaumudi/1
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/primary/laghukaumudi-samjna.html`.
- **Integrity:** SHA-256 `f762a0664e93d4ffa2ba557bfebb68bfa1f46171281352c34487cf5dfbf54a98`.
- **Rights/storage:** Public digital text retained for research.
- **Notes:** Gives five internal efforts and eleven external efforts directly.

### `yajnavalkya-shiksha-duration`

- **Citation:** *Yājñavalkya Śikṣā* 13.
- **Source type:** Digital Sanskrit primary text.
- **Canonical locator:** Verse 13, beginning **एकमात्रो भवेद्ध्रस्वः**.
- **Digital URL:** https://sanskritdocuments.org/doc_veda/yajnavalkyashiksha.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/primary/yajnavalkya-shiksha.html`.
- **Integrity:** SHA-256 `46d1b7295e55242e2cdf4f41f78ccbe68607d92a514c183659f131190bff3432`.
- **Rights/storage:** Public digital text retained for research.
- **Notes:** States the 1:2:3 vowel-duration relation and the consonant's half-*mātrā*.

### `ma-rao-tabla-bol-pedagogy-2018`

- **Citation:** Rohit M. A. and Preeti Rao, “Acoustic-Prosodic Features of Tabla Bol Recitation and Correspondence with the Tabla Imitation,” *Interspeech 2018*, pp. 1229-1233.
- **Source type:** Peer-reviewed conference paper.
- **Canonical locator:** Abstract and §1.
- **Digital URL:** https://www.isca-archive.org/interspeech_2018/ma18_interspeech.html
- **Archived URL:** https://www.isca-archive.org/interspeech_2018/ma18_interspeech.pdf
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/instruments/tabla-bol-pedagogy.html`.
- **Integrity:** SHA-256 `6af2a6d54fd50ad7a40f20bfee616665578402f7e0807cee91e2a87790a938322`.
- **Rights/storage:** Public conference record retained for research.
- **Notes:** Establishes that strokes are named by bols and that bol recitation conveys a composition's basic score in oral pedagogy.

### `met-sarangi-503204`

- **Citation:** Metropolitan Museum of Art, “Sarangi,” collection no. 1982.143.2.
- **Source type:** Museum collection record.
- **Canonical locator:** Object description.
- **Digital URL:** https://www.metmuseum.org/art/collection/search/503204
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** URL and quoted description retained in the batch report; the site rejected the automated local archive request.
- **Integrity:** Not available for a local file.
- **Rights/storage:** Public museum record cited by URL.
- **Notes:** Describes the sarangi's close proximity to the melodic flexibility of the human voice.

### `ghosh-natyashastra-ch28`

- **Citation:** Bharata, *Nāṭyaśāstra* 28.1-2, trans. Manomohan Ghosh.
- **Source type:** Primary Sanskrit treatise in published translation.
- **Canonical locator:** Chapter 28, verses 1-2.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/the-natyashastra/d/doc210187.html
- **Archived URL:** https://archive.org/details/in.ernet.dli.2015.48979
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/primary/natyashastra-ch28.html`; PDF at `working/40_reference/sources/archive/documents/ch7-verification/natyashastra/ghosh-natyashastra-v2.pdf`.
- **Integrity:** HTML SHA-256 `6b9e307bc6f1d25860b8db9a58ba11c00acd9ed83fba2fd9bf38efbf11c0ff2b`; PDF SHA-256 `511d370e4868f5f3399ffc71f6ff7ff38c120541684f8373e94d66c244c8f44c`.
- **Rights/storage:** Public digital presentation and research scan retained for verification.
- **Notes:** Gives the exact four classes and representative mechanisms without the later examples formerly added by the endnote.

### `gretil-mandukya-upanishad`

- **Citation:** *Māṇḍūkya Upaniṣad*, GRETIL digital text.
- **Source type:** Digital Sanskrit primary text.
- **Canonical locator:** Verses 1 and 8-12.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/mand_upu.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/primary/mandukya-upanishad.html`.
- **Integrity:** SHA-256 `fd0e0c409296bbbf8a66122c2ae6505fb45f41aa72436899625b94dfe5fc8281`.
- **Rights/storage:** Public digital Sanskrit text retained for research.
- **Notes:** Supplies the Oṃ formula and its analysis into the three measures and the fourth.

### `gretil-taittiriya-upanishad`

- **Citation:** *Taittirīya Upaniṣad* 1.8.1 with Śaṃkara's commentary, GRETIL digital text.
- **Source type:** Digital Sanskrit primary text and commentary.
- **Canonical locator:** 1.8.1.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_taittirIyopaniSad-zaMkarabhASya.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/primary/taittiriya-upanishad-bhasya.html`.
- **Integrity:** SHA-256 `af74378cd2cd383856d23109ff15d10aa9996c41f0f9a62a6c16c004b7d47c5b`.
- **Rights/storage:** Public digital Sanskrit text retained for research.
- **Notes:** Confirms **om iti brahma, om itīdaṃ sarvam** and the recitational contexts listed in the note.

### `gretil-katha-upanishad`

- **Citation:** *Kaṭha Upaniṣad*, GRETIL digital text.
- **Source type:** Digital Sanskrit primary text.
- **Canonical locator:** GRETIL 2.15-17, conventionally numbered 1.2.15-17.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/kathop_u.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/primary/katha-upanishad.html`.
- **Integrity:** SHA-256 `e62789ce5dc2c715f838f24f41c2d3fc210e88a850b7daf9703c394a752225b8`.
- **Rights/storage:** Public digital Sanskrit text retained for research.
- **Notes:** Confirms the passage that condenses the Vedic goal into Oṃ.

### `gretil-yoga-sutra`

- **Citation:** Patañjali, *Yoga Sūtra* 1.27, GRETIL digital text.
- **Source type:** Digital Sanskrit primary text.
- **Canonical locator:** 1.27, **तस्य वाचकः प्रणवः**.
- **Digital URL:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/3_phil/yoga/yogasutu.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/primary/yoga-sutra.html`.
- **Integrity:** SHA-256 `ccd7f4da9d4b2dbebea762d39d33a7eb9bccb8216bcf840a861a7dcf843e1395`.
- **Rights/storage:** Public digital Sanskrit text retained for research.
- **Notes:** Confirms the designation of the *praṇava* as the verbal designator in Yoga Sūtra 1.27.

### `ghosh-natyashastra-ch33`

- **Citation:** Bharata, *Nāṭyaśāstra* 33.31-35, translated by Manomohan Ghosh, *The Nāṭyaśāstra*, vol. 2 (Calcutta: Asiatic Society, 1961), pp. 873-74.
- **Source type:** Primary Sanskrit treatise in translation.
- **Canonical locator:** Chapter 33, verses 31-35; printed pp. 873-74.
- **Digital URL:** https://archive.org/details/in.ernet.dli.2015.48979
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch7-verification/natyashastra/ghosh-natyashastra-v2.pdf` and `.txt`.
- **Integrity:** Shares the archived volume and checksums recorded under `ghosh-natyashastra-ch28`.
- **Rights/storage:** Public archive copy retained for research.
- **Notes:** Describes the human body as a vīṇā, says notes arise first from the body and then pass to wooden and other instruments, and directs instruments to reproduce the singer's notes. It does not use the compound **ādi-vādya**.

### `octaves-aadi-vadya`

- **Citation:** Octaves Online, “Sound, Spirit, and Song: The Significance of Music in Hindustani Vocal,” section “The Voice as the Aadi Vadya (The Original Instrument).”
- **Source type:** Contemporary Indian music instruction.
- **Canonical locator:** Section headed “The Voice as the Aadi Vadya (The Original Instrument).”
- **Digital URL:** https://www.octavesonline.com/post/sound-spirit-and-song-the-significance-of-music-in-hindustani-vocal
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/web/ch7-verification/contemporary/octaves-aadi-vadya.html`.
- **Integrity:** SHA-256 `79aad04ba37bb1c5e5272fd2877ddcb0c7c27bb0554faf687fb49d7dd15ad85d`.
- **Rights/storage:** Public webpage retained for research verification.
- **Notes:** Establishes current use of **Aadi Vadya** for the human voice. The older architectural support comes separately from *Nāṭyaśāstra* 33.31-35.

### `lsi-tamil-nadu-2019`

- **Citation:** Office of the Registrar General, India, *Linguistic Survey of India: Tamil Nadu* (Language Division, 2019).
- **Source type:** Government linguistic survey.
- **Canonical locator:** Tamil phonology, printed pp. 61-65; Toda phonology, printed pp. 642-43.
- **Digital URL:** https://censusindia.gov.in/nada/index.php/catalog/45244/download/48951/LSI_TAMIL_NADU.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/lsi-tamil-nadu.pdf`.
- **Integrity:** SHA-256 `19e6a463c7ae8bc190c622c6f53fc9c7d970dd9f58546410aac05902daa320dd`.
- **Rights/storage:** Public government survey retained for research.
- **Notes:** Supports Tamil's lack of contrastive aspiration, its contextual stop voicing, and the recorded Tamil and Toda inventories used in the atlas audit.

### `lsi-jharkhand-2020`

- **Citation:** Office of the Registrar General, India, *Linguistic Survey of India: Jharkhand* (Language Division, 2020).
- **Source type:** Government linguistic survey.
- **Canonical locator:** Kurukh inventory, printed pp. 213-14; Ho inventory, printed pp. 349-50; Ho morphophonemics, printed p. 382.
- **Digital URL:** https://censusindia.gov.in/nada/index.php/catalog/34832/download/38520/LSI_JHARKHAND.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/lsi-jharkhand.pdf`.
- **Integrity:** SHA-256 `e371d2d617ad3caefd3df7e5ee7a977fa9b359afd2b94b61e0e86678ca6a2222`.
- **Rights/storage:** Public government survey retained for research.
- **Notes:** Supplies the Kurukh and Ho phonemic inventories and documents movement of the Ho checked-vowel feature in inflection.

### `lsi-west-bengal-part1-2020`

- **Citation:** Office of the Registrar General, India, *Linguistic Survey of India: West Bengal, Part I* (Language Division, 2020).
- **Source type:** Government linguistic survey.
- **Canonical locator:** Mundari inventory, printed p. 399; Mundari morphophonemics, printed p. 406.
- **Digital URL:** https://censusindia.gov.in/nada/index.php/catalog/34826/download/38514/LSI_WB_PART_I.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/lsi-west-bengal-part1.pdf`.
- **Integrity:** SHA-256 `d3d1f935612bad52cb79699c07702aa4efafd26a872163d8998782fde4639a63`.
- **Rights/storage:** Public government survey retained for research.
- **Notes:** Includes a glottal stop in Mundari's consonant inventory and records regular glottal-stop alternations.

### `deeney-ho-grammar`

- **Citation:** John Deeney, *Ho Grammar* (Chaibasa: Xavier Ho Publications, 1975).
- **Source type:** Descriptive grammar.
- **Canonical locator:** Printed pp. 7-9, “Checked and unchecked vowels.”
- **Digital URL:** https://michaelyorke.org/wp-content/uploads/2023/08/Ho-Grammar-by-J-Deeney.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/deeney-ho-grammar.pdf`.
- **Integrity:** SHA-256 `00669d3b6558994d7c4ba277a3ef786799fbf39a51d08cebe4d912464b1ecf2d`.
- **Rights/storage:** Public research copy retained for verification.
- **Notes:** Defines the Ho checked vowel as interrupted by a glottal catch and supplies meaning-changing checked/unchecked pairs.

### `arsenault-retroflexion-south-asia-2017`

- **Citation:** Paul Arsenault, “Retroflexion in South Asia: Typological, Genetic, and Areal Patterns,” *Journal of South Asian Languages and Linguistics* 4.1 (2017), pp. 1-53.
- **Source type:** Peer-reviewed typological survey; archived author manuscript.
- **Canonical locator:** Abstract, §§3-5, and distribution maps; doi:10.1515/jsall-2017-0001.
- **Digital URL:** https://digitalcollections.tyndale.ca/bitstreams/ecd929b8-d841-4fd8-8d93-cf8d291999ec/download
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-02.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/arsenault-retroflexion-south-asia-2017.pdf`.
- **Integrity:** SHA-256 `d91512bfc0cb8e71b2889773d3ef2b2dc643f759326c25165834b2299f4468b0`.
- **Rights/storage:** Author manuscript retained for research verification.
- **Notes:** Finds retroflexion characteristic of South Asia and most retroflex-system distributions more geographic than genealogical; does not support global-exclusivity claims.

### `nagaraja-korku-1999`

- **Citation:** K. S. Nagaraja, *Korku Language: Grammar, Texts and Vocabulary* (Tokyo: Institute for the Study of Languages and Cultures of Asia and Africa, Tokyo University of Foreign Studies, 1999).
- **Source type:** Descriptive grammar.
- **Canonical locator:** Chapter I, §1.1, “Inventory of Phonemes,” printed p. 5.
- **Digital URL:** https://dokumen.pub/korku-language-grammar-texts-and-vocabulary.html
- **Archived URL:** https://books.google.com/books?id=qXgOAAAAYAAJ
- **Accessed:** 2026-09-03.
- **Local record:** Metadata and indexed text only; the public host rejected automated archival retrieval.
- **Integrity:** Not available for a local file.
- **Rights/storage:** Bibliographic record and public indexed text retained by URL.
- **Notes:** Supplies the fuller Korku inventory used by the atlas. The aspirated rows are removed by the Chapter 8 comparison before its 23-cell coverage calculation.

### `zide-korku-syllables`

- **Citation:** Norman H. Zide, “Korku Syllables and Syllable Stress,” in *Papers in Southeast Asian Linguistics No. 3*, ed. David Thomas (Canberra: Australian National University, 1973), pp. 161-75.
- **Source type:** Descriptive phonological article.
- **Canonical locator:** Printed p. 162, “The Korku Phonemes” and footnotes 1-3.
- **Digital URL:** https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/e0717b76-a183-4912-9765-d9fad7b36200/content
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/korku-syllables-zide.pdf`.
- **Integrity:** SHA-256 `bfad94646519a33c1ccdbebcfc3818ed1607c7ab1fe2428f9086e00d016fdb1a`.
- **Rights/storage:** Public repository copy retained for research verification.
- **Notes:** Records the older compact analysis and treats voiceless and voiced aspiration as vowel accompaniments. Used to document the analytical difference from Nagaraja rather than to blend the two inventories.

### `zide-review-nagaraja-korku-2009`

- **Citation:** Norman H. Zide, review of K. S. Nagaraja, *Korku Language: Grammar, Texts and Vocabulary*, *Mon-Khmer Studies* 39 (2009), pp. 177-92.
- **Source type:** Scholarly review.
- **Canonical locator:** Printed pp. 179-81.
- **Digital URL:** https://sealang.net/archives/mksj/pdf/MKSJ-39.177.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/korku-nagaraja-review-zide-2009.pdf`.
- **Integrity:** SHA-256 `96d71705ca0b4ffbba14f943410cc5e9a483af0271de4c00fa6494812230e5dc`.
- **Rights/storage:** Public journal copy retained for research verification.
- **Notes:** Documents the difference between Nagaraja's two-speaker description and Zide's earlier analysis, including the role of Hindi contact.

### `roach-british-rp-2004`

- **Citation:** Peter Roach, “British English: Received Pronunciation,” *Journal of the International Phonetic Association* 34.2 (2004), pp. 239-45.
- **Source type:** Peer-reviewed IPA illustration.
- **Canonical locator:** Consonant table, printed p. 241.
- **Digital URL:** https://www.cambridge.org/core/services/aop-cambridge-core/content/view/D4AFF0A7118E7081ACF7C7586FF87590/S0025100304001768a.pdf/british_english_received_pronunciation.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/external/roach-british-rp-2004.pdf`.
- **Integrity:** SHA-256 `206c5b912100ad4c70900507c03ec32e81a272ef3278888b176892aefbefff6b`.
- **Rights/storage:** Public journal copy retained for research verification.
- **Notes:** Correctly places English **t, d, n, l** in the alveolar column and **θ, ð** in the dental column.

### `fougeron-smith-french-1993`

- **Citation:** Cécile Fougeron and Caroline L. Smith, “French,” *Journal of the International Phonetic Association* 23.2 (1993), pp. 73-76.
- **Source type:** Peer-reviewed IPA illustration.
- **Canonical locator:** Consonant table, printed p. 79 in the *Handbook of the International Phonetic Association* reprint.
- **Digital URL:** https://wwwhomes.uni-bielefeld.de/gibbon/2019-Mannheim-Summer-School/Languages/French.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/external/fougeron-smith-french-1993.pdf`.
- **Integrity:** SHA-256 `8cae37ea210e3a6a206580e3eca82e3e863f9d4929f7d59e35c72afac5bb9e4d`.
- **Rights/storage:** Public teaching copy retained for research verification.
- **Notes:** Supplies the Metropolitan French consonant table used by the atlas.

### `holton-mackridge-philippaki-greek-2012`

- **Citation:** David Holton, Peter Mackridge, Irene Philippaki-Warburton, and Vassilios Spyropoulos, *Greek: A Comprehensive Grammar of the Modern Language*, 2nd ed. (Routledge, 2012).
- **Source type:** Descriptive grammar.
- **Canonical locator:** Chapter 1, §§1.1 and 1.1.1.3, printed pp. 3 and 9.
- **Digital URL:** https://api.pageplace.de/preview/DT0400.9781136626401_A23858615/preview-9781136626401_A23858615.pdf
- **Archived URL:** https://doi.org/10.4324/9780203802380
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/external/holton-mackridge-philippaki-greek-preview.pdf`.
- **Integrity:** SHA-256 `620be73c573d04df2bf6360042ce5ceecadd04b4228855fa2d3339eabdeb2d6d`.
- **Rights/storage:** Publisher preview retained for research verification.
- **Notes:** Distinguishes the core phonemes from the wider chart of consonantal sounds and contextual realizations used by the pronunciation atlas.

### `perry-tajik-2005`

- **Citation:** John R. Perry, *A Tajik Persian Reference Grammar* (Leiden: Brill, 2005).
- **Source type:** Descriptive grammar.
- **Canonical locator:** §1.5 and Figure 1.5, printed pp. 22-24.
- **Digital URL:** https://www.slideshare.net/slideshow/a-tajik-persian-reference-grammar-bilingual-john-r-perry/279821442
- **Archived URL:** https://openlibrary.org/books/OL3393232M/A_Tajik_Persian_reference_grammar
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch8-verification/inventories/tajik-perry-slideshare.html`.
- **Integrity:** SHA-256 `32ed63159c77e21ee19ca1b9aa3213ccf0218eb59539560b132a8e68ef0e18ea`.
- **Rights/storage:** Public presentation record retained for research verification.
- **Notes:** Gives twenty-four consonant phonemes and explicitly treats **[w]** as an allophone of **/v/** in the standard language.

### `mccollum-chen-kazakh-2020`

- **Citation:** Adam G. McCollum and Si Chen, “Kazakh,” *Journal of the International Phonetic Association* 51.2 (2021), pp. 276-98; first published online 26 February 2020.
- **Source type:** Peer-reviewed IPA illustration.
- **Canonical locator:** Consonant table and discussion, printed pp. 277-78; doi:10.1017/S0025100319000185.
- **Digital URL:** https://www.cambridge.org/core/services/aop-cambridge-core/content/view/353A10BD35418B48B5A6370D9F7D8CE0/S0025100319000185a.pdf/div-class-title-kazakh-div.pdf
- **Archived URL:** https://doi.org/10.1017/S0025100319000185
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch8-verification/external/mccollum-chen-kazakh-2020.pdf`.
- **Integrity:** SHA-256 `bf4c5d7fe54505e8e9a42c0e51d492f967ded3be7c7e9e21623da2d3f9baec70`.
- **Rights/storage:** Open-access journal article retained for research verification.
- **Notes:** Supplies the twenty-consonant core inventory. Variable loan sounds **[f, v, h]** are discussed separately and excluded from the core configuration.

### `phoible-kyrgyz-standard-2382`

- **Citation:** Steven Moran and Daniel McCloy, eds., PHOIBLE 2.0, “Kyrgyz (Standard),” inventory EA 2382, source Kara 2003.
- **Source type:** Curated phonological inventory database.
- **Canonical locator:** Inventory 2382, segment list.
- **Digital URL:** https://phoible.org/inventories/view/2382
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch8-verification/inventories/kyrgyz-phoible.html`.
- **Integrity:** SHA-256 `51d709ae753c7f3e270d15db2a4a5e33971ba879f6257942e5fec2275e33955e`.
- **Rights/storage:** CC BY-SA database record retained for research verification.
- **Notes:** The linked segment list, rather than every empty symbol displayed by the generic IPA chart, supplies the standard Kyrgyz configuration.

### `story-bunton-stop-model-2017`

- **Citation:** Brad H. Story and Kate Bunton, “An Acoustically Driven Vocal Tract Model for Stop Consonant Production,” *Speech Communication* 87 (2017), pp. 1-17.
- **Source type:** Peer-reviewed acoustic and MRI-based modeling study.
- **Canonical locator:** Figures 2, 4, and 5 and discussion on printed pp. 5 and 8-11; doi:10.1016/j.specom.2016.12.005.
- **Digital URL:** https://bpb-us-e2.wpmucdn.com/sites.arizona.edu/dist/f/80/files/2023/10/StoryBunton_SpeechComm2017-1.pdf
- **Archived URL:** https://doi.org/10.1016/j.specom.2016.12.005
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch9-verification/story-bunton-stop-model-2017.pdf`.
- **Integrity:** SHA-256 `ef8bce288cacd2046cd2fb69719ee72b0a81ed0520cfa0578a71d79d9bc4ae83`.
- **Rights/storage:** Public author copy retained for research verification.
- **Notes:** Provides a 17.5-centimeter MRI-derived adult vocal-tract scale and modeled bilabial, alveolar, and velar closure locations. Used to replace the manuscript's former values, which mixed glottis-based and lip-based coordinates.

### `ghosh-natyashastra-ch9`

- **Citation:** Bharata, *Nāṭyaśāstra*, chapter 9, translated by Manomohan Ghosh.
- **Source type:** Primary-text translation web presentation.
- **Canonical locator:** Chapter 9, gestures of the major limbs and hand gestures.
- **Digital URL:** https://www.wisdomlib.org/hinduism/book/the-natyashastra/d/doc209706.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/natyashastra-ch9.html`.
- **Integrity:** SHA-256 `fadf738013e5a6d7cdd6a0953e01f8729c0e250f99482c7b629e279aea0896b5`.
- **Rights/storage:** Public research capture of a translated primary text.
- **Notes:** Documents bodily gesture and twenty-four single-hand gestures in this *Nāṭyaśāstra* recension. The separate 28/23 enumeration cited in the endnote belongs to the *Abhinaya Darpaṇa*.

### `unesco-vedic-chanting`

- **Citation:** UNESCO, “Tradition of Vedic Chanting,” Representative List of the Intangible Cultural Heritage of Humanity, nomination 00062.
- **Source type:** Institutional heritage record.
- **Canonical locator:** Nomination 00062; inscribed 2008, originally proclaimed 2003.
- **Digital URL:** https://ich.unesco.org/en/RL/vedic-chanting-00062
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/unesco-vedic-chanting.html`.
- **Integrity:** SHA-256 `05c3c3383105856b69afb33d2e0f4778d1e15ad824d1a192c0693fd370d7f95b`.
- **Rights/storage:** Public institutional web record retained for research verification.
- **Notes:** Supports exact sound, accent, pronunciation, and recitation-technique claims. Its evolutionary chronology and statement that Vedic language derives from Classical Sanskrit are not adopted by the manuscript.

### `alhaidary-gap-detection-2019`

- **Citation:** A. A. Alhaidary et al., “Auditory Temporal Resolution in Adaptive Tasks: Gap Detection Investigation,” *Saudi Medical Journal* 40.1 (2019), 52-58.
- **Source type:** Peer-reviewed experimental article.
- **Canonical locator:** Results; doi:10.15537/smj.2019.1.23814; PMCID PMC6452600.
- **Digital URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6452600/
- **Archived URL:** https://doi.org/10.15537/smj.2019.1.23814
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/alhaidary-gap-detection-2019.html`.
- **Integrity:** SHA-256 `6d89d74424a66bb77bb60deb4ffe7035609e6dd88896ec7e6342f9ed17c495d5`.
- **Rights/storage:** Open-access article retained for research verification.
- **Notes:** Reports a mean 3.19 ms broadband-noise gap-detection threshold for 27 normal-hearing young adults.

### `moore-auditory-processes-2008`

- **Citation:** Brian C. J. Moore, “Basic Auditory Processes Involved in the Analysis of Speech Sounds,” *Philosophical Transactions of the Royal Society B* 363.1493 (2008), 947-963.
- **Source type:** Peer-reviewed review article.
- **Canonical locator:** §6(a); doi:10.1098/rstb.2007.2152; PMCID PMC2606789.
- **Digital URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC2606789/
- **Archived URL:** https://doi.org/10.1098/rstb.2007.2152
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/moore-auditory-processes-2008.html`.
- **Integrity:** SHA-256 `6caeefefd8e20a78e2cf3bc980747a86767d92476f5616ed6d5172adb8642908`.
- **Rights/storage:** Open-access article retained for research verification.
- **Notes:** Gives a typical broadband-noise gap threshold of 2-3 ms and explains the dependence on stimulus conditions.

### `yasui-song-error-detection-2009`

- **Citation:** Takao Yasui, Kimitaka Kaga, and Kuniyoshi L. Sakai, “Language and Music: Differential Hemispheric Dominance in Detecting Unexpected Errors in the Lyrics and Melody of Memorized Songs,” *Human Brain Mapping* 30.2 (2009), 588-601.
- **Source type:** Peer-reviewed experimental article.
- **Canonical locator:** Experiments 1 and 3; doi:10.1002/hbm.20529; PMCID PMC6870715.
- **Digital URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6870715/
- **Archived URL:** https://doi.org/10.1002/hbm.20529
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/yasui-song-error-detection-2009.html`.
- **Integrity:** SHA-256 `3f1981c7a9400f0df1639ae8b7aa7311b3f38907ccf4f457c9365fcbcff729b6`.
- **Rights/storage:** Open-access article retained for research verification.
- **Notes:** Supports detection of unexpected lyric and melody deviations in memorized songs; it does not establish a universal advantage for sung learning.

### `aleppo-codex-masorah`

- **Citation:** The Aleppo Codex project, “The Masoretes and the Masorah.”
- **Source type:** Institutional manuscript and textual-history presentation.
- **Canonical locator:** §§2.1-2.5, especially consonantal text, vocalization, accents, and Masoretic notes.
- **Digital URL:** https://www.aleppocodex.org/2.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/aleppo-codex-masorah.html`.
- **Integrity:** SHA-256 `6d73cf4d201df04860512b15779f9120d0f1d9a27eaf94f357ad2cd7808980a4`.
- **Rights/storage:** Public institutional web record retained for research verification.
- **Notes:** Documents the addition of vowel signs, cantillation marks, and Masoretic notes to preserve the received reading tradition. It also acknowledges textual variation before stabilization.

### `nasser-quran-canonizations`

- **Citation:** Shady H. Nasser, “The Canonizations of the Qurʾān: Political Decrees or Community Practices?”
- **Source type:** Scholarly article made available by the author.
- **Canonical locator:** Opening synthesis and discussion of Ibn Mujāhid and Ibn al-Jazarī.
- **Digital URL:** https://scholar.harvard.edu/files/shadynasser/files/8_nasser_the_canonizations_of_the_quran_political_decrees_or_community_practices.pdf
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** Metadata and indexed text only; the host rejected automated retrieval.
- **Integrity:** No local file.
- **Rights/storage:** Bibliographic record and public author URL retained.
- **Notes:** Documents successive canonizations, Ibn Mujāhid's seven readings, Ibn al-Jazarī's extension to ten, and the role of politico-religious authority.

### `ideo-cairo-quran-1924`

- **Citation:** Dominican Institute for Oriental Studies, “The Cairo Edition of the Qurʾān 1924: Texts, Histories & Challenges,” conference description, 2021.
- **Source type:** Institutional research-program page.
- **Canonical locator:** Presentation and “History of institutions” sections.
- **Digital URL:** https://www.ideo-cairo.org/en/conference-en/call-for-papers-the-cairo-edition-of-the-qur%CA%BEan-1924/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/ideo-cairo-quran-1924.html`.
- **Integrity:** SHA-256 `ac6d33ced895731ec506b69162ece8d40a12ae3a7ff20c14d9534494c89f3a2c`.
- **Rights/storage:** Public institutional web record retained for research verification.
- **Notes:** Identifies the 1924 edition with King Fuad, the al-Azhar committee, the Ministry of Education, and its later importance as a liturgical and academic reference.

### `alazhar-mushaf-committee`

- **Citation:** Al-Azhar Islamic Research Academy, “What Do You Know About the Muṣḥaf Revision Committee at Al-Azhar Al-Sharif?” 10 September 2021.
- **Source type:** Official institutional web page.
- **Canonical locator:** Committee mandate and publication/circulation permissions.
- **Digital URL:** https://azhar.eg/magmaa-e/Articles/ArtMID/11236/ArticleID/56332/What-do-you-know-about-the-Mu%E1%B9%A3%E1%B8%A5af-Revision-Committee-at-Al-Azhar-Al-Sharif
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/alazhar-mushaf-committee.html`.
- **Integrity:** SHA-256 `6d6e70cc080302f3cec4630a169ee61db3e8c85faf4fd3b989fee3c67b20f384`.
- **Rights/storage:** Public official web record retained for research verification.
- **Notes:** The committee states that it grants permissions to publish and circulate muṣḥafs in Egypt and abroad.

### `egypt-quran-law-102-1985`

- **Citation:** Supreme Constitutional Court of Egypt, Case 64 of Judicial Year 41, quoting Law 102 of 1985 on printing the Quran and prophetic traditions.
- **Source type:** Official court decision and statutory quotation.
- **Canonical locator:** Law 102 of 1985, articles 1-2, as quoted in the judgment.
- **Digital URL:** https://www.sccourt.gov.eg/SCC/faces/Rules_Html/11747_41_64_1_2.html?timestamp=1695751655766
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/egypt-quran-law-102-1985.html`.
- **Integrity:** SHA-256 `99bcb4ff7641c106971dc284e977c9334004b1e85703366d655ff6eb467cd1a2`.
- **Rights/storage:** Public official court record retained for research verification.
- **Notes:** Records prosecution for unlicensed circulation and quotes penalties including imprisonment, fines, and confiscation.

### `vatican-nova-vulgata-1979`

- **Citation:** John Paul II, *Scripturarum Thesaurus*, Apostolic Constitution promulgating the *Nova Vulgata*, 25 April 1979.
- **Source type:** Official church document.
- **Canonical locator:** Promulgation of the *Nova Vulgata* as the *editio typica*.
- **Digital URL:** https://www.vatican.va/content/john-paul-ii/en/apost_constitutions/documents/hf_jp-ii_apc_19790425_scripturarum-thesaurus.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch13-14-verification/vatican-nova-vulgata-1979.html`.
- **Integrity:** SHA-256 `20db9b617f7d050a68695b2e74eb8bde8db0f9cc2d744a20415c8051c2adcd0f`.
- **Rights/storage:** Public official web record retained for research verification.
- **Notes:** Confirms the institutional promulgation and revision of the Latin text; it does not document medieval copying practice.

### `iyer-vikrtis-vedic-recitation-1978`

- **Citation:** S. Venkitasubramonia Iyer, “Vikṛtis in Vedic Recitation,” in *Kṛtyaratnāvalī* (Bhandarkar Oriental Research Institute, 1978), pp. 1–7 of the article.
- **Source type:** Scholarly article quoting and explaining the received recitation classification.
- **Canonical locator:** Opening classification; *Vikṛtivallī* kārikā 5; descriptions of *jaṭā* through *ghana*.
- **Digital URL:** https://archive.org/details/vrox_krtya-ratnavali-vikritis-vedic-recitation-by-s-venkitasubramonia-iyer-engli
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch15-verification/iyer-krtya-ratnavali-vikritis-1978.txt`; page map at `working/40_reference/sources/archive/documents/ch15-verification/iyer-page-numbers.json`; metadata at `working/40_reference/sources/archive/web/internet-archive-metadata/vrox_krtya-ratnavali-vikritis-vedic-recitation-by-s-venkitasubramonia-iyer-engli.json`.
- **Integrity:** SHA-256 `fffc0141b2028a5e7d617c829aae62ee14a733cb5b382a6cda21cf47c7fbf08a` (OCR), `cdc568bd1d9faa683aeeb688e4e267c14334b2cf4df9b5a740deef12abb3a930` (page map), and `0961f9a3bfd6f1b7a5bcc755d9c5f285186c7562b72b376983a03469d1c3ad5b` (metadata).
- **Rights/storage:** Public-domain scan retained for research verification.
- **Notes:** Explicitly classifies *Saṃhitā, Pada,* and *Krama* as the three *prakṛti* modes and *Jaṭā, Mālā, Śikhā, Rekhā, Dhvaja, Daṇḍa, Ratha,* and *Ghana* as the eight *vikṛtis*.

### `staal-nambudiri-veda-recitation-1961`

- **Citation:** Frits Staal, *Nambudiri Veda Recitation* (The Hague: Mouton, 1961), *Disputationes Rheno-Trajectinae* 5.
- **Source type:** Monograph based on field recordings made in South India in 1957.
- **Canonical locator:** Preface on recordings; §3, “Vikṛtis of the Tamil Ṛgveda and Yajurveda Recitation.”
- **Digital URL:** https://archive.org/details/staal-nambudiri
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch15-verification/staal-nambudiri-veda-recitation-1961.txt`; metadata at `working/40_reference/sources/archive/web/internet-archive-metadata/staal-nambudiri.json`.
- **Integrity:** SHA-256 `0f4653ecb2b99e48ef6466e2439c59c8481b7d9a14133e8f01782f1590a262d8` (OCR) and `cbb07daa74221f6c4eabf9a446146f0b7544a6e77fa2b4903ac01035227e7250` (metadata).
- **Rights/storage:** Public research scan and metadata retained for verification.
- **Notes:** Records living *krama, jaṭā,* and *ghana* patterns and states that a person who masters *ghana* and the preceding forms is called *ghanapathikal*.

### `staal-agni-fire-altar-1983`

- **Citation:** Frits Staal, with C. V. Somayajipad and M. Itti Ravi Nambudiri, *Agni: The Vedic Ritual of the Fire Altar*, 2 vols. (Berkeley: Asian Humanities Press, 1983), vol. I.
- **Source type:** Documentary monograph arising from the 1975 Nambūdiri Agnicayana performance.
- **Canonical locator:** Vol. I title page, contents, and preface p. xxi.
- **Digital URL:** https://archive.org/details/frits-staal-agni-the-vedic-ritual-of-the-fire-altar.-1-asian-humanities-press-1983
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch15-verification/staal-agni-vol1-1983.txt`; metadata at `working/40_reference/sources/archive/web/internet-archive-metadata/frits-staal-agni-vol1-1983.json`.
- **Integrity:** SHA-256 `e55f217d35a5296bb8c276ba601ac622657da40380e528e51e391292b3e4a761` (OCR) and `b36d0ecce50b7e7627f5da53afdff1f2aa9921abd8b0ae81466f4acec2fab844` (metadata).
- **Rights/storage:** Research-access scan and metadata retained for verification.
- **Notes:** The preface directly states that the twelve-day ceremony was performed from 12 to 24 April 1975 so that it could be filmed and recorded; the volume also contains extensive photographic documentation.

### `shiksha-samgraha-tripathi`

- **Citation:** Rāma Prasāda Tripāṭhī, ed., *Śikṣā Saṃgraha of Yājñavalkya and Others* (Sampurnanand Sanskrit University collection).
- **Source type:** Sanskrit source collection with editorial introduction.
- **Canonical locator:** Contents and introduction, especially descriptions of *Yājñavalkya Śikṣā* and *Vāsiṣṭhī Śikṣā*.
- **Digital URL:** https://archive.org/details/shikshasamgraha
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch15-verification/shiksha-samgraha-djvu.txt`; metadata at `working/40_reference/sources/archive/web/internet-archive-metadata/shikshasamgraha.json`.
- **Integrity:** SHA-256 `ea79ffd6dfb9362c3164f0da000b5fdd8946910200033492f74e5eaa5291b150` (OCR) and `2acbe8e06112934b3077a1fc0dd631d4780bb3d48728ca22a13fc4829a558804` (metadata).
- **Rights/storage:** Public research scan and metadata retained for verification.
- **Notes:** Corrects the earlier description of *Vāsiṣṭhī Śikṣā*: the introduction associates it with counting the *ṛcs* and *yajus* of the Śukla Yajurveda Saṃhitā, not with a Sāmavedic recitation framework.

### `pillai-apisaliya-shiksha-1971`

- **Citation:** K. Raghavan Pillai, ed., “Āpiśalīyaśikṣā,” *Journal of the Kerala University Oriental Research Institute and Manuscripts Library* 18.2–3 (1971): 199–204.
- **Source type:** Direct Sanskrit text edition.
- **Canonical locator:** Entire six-page edition.
- **Digital URL:** https://archive.org/details/Apisaliyasiksa
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch15-verification/apisaliya-shiksha-1971.pdf`; metadata at `working/40_reference/sources/archive/web/internet-archive-metadata/Apisaliyasiksa.json`.
- **Integrity:** SHA-256 `5230f89c3be48c29e5b5bc32d828a61774760296ab880d2a5cc2a1f131723d30` (PDF) and `9fb29a7e34c235f7e648adeefc796e70680d0c74bec0ec86c7822bf916c7ed7a` (metadata).
- **Rights/storage:** Public research scan retained for verification.
- **Notes:** Establishes the received text titled *Āpiśalīyaśikṣā*; the title alone does not establish the date of the surviving text.

### `bharadvaja-shiksha-edition`

- **Citation:** *Bhāradvāja Śikṣā*, ed. Rāmachandra Dikshitar, V. R. Sundaram Ayyar, and P. S. BORI edition.
- **Source type:** Direct Sanskrit text edition.
- **Canonical locator:** Title and edited text.
- **Digital URL:** https://archive.org/details/bharadvajasiksaramachandradikshitarv.r.sundaramayyarp.s.bori_129_H
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch15-verification/bharadvaja-shiksha.pdf`; metadata at `working/40_reference/sources/archive/web/internet-archive-metadata/bharadvajasiksa.json`.
- **Integrity:** SHA-256 `10d54663edefc507b9408d14975ea64452c9227643593085766283f87aaf4f6d` (PDF) and `ac887b30eda4104138979136b836441eab798d2dc0ce4abaf48b5a0e0dc2110a` (metadata).
- **Rights/storage:** Public research scan retained for verification.
- **Notes:** Establishes the received text titled *Bhāradvāja Śikṣā*.

### `sanskritdocuments-mundaka`

- **Citation:** *Muṇḍaka Upaniṣad* 1.1.5, SanskritDocuments transcription.
- **Source type:** Direct Sanskrit text transcription.
- **Canonical locator:** 1.1.5, **शिक्षा कल्पो व्याकरणं निरुक्तं छन्दो ज्योतिषमिति**.
- **Digital URL:** https://www.sanskritdocuments.org/doc_upanishhat/mundaka.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch15-verification/mundaka-upanishad.html`.
- **Integrity:** SHA-256 `faccc12c0508a95200bdc7d371bd2bdaf8898b30f4cfc6db601eec164278d03d`.
- **Rights/storage:** Public Sanskrit transcription retained for verification.
- **Notes:** Directly supports a six-Vedāṅga enumeration beginning with *Śikṣā*; it does not state an architectural reason for the order.

### `nist-crc-glossary`

- **Citation:** National Institute of Standards and Technology, Computer Security Resource Center, “cyclic redundancy check (CRC).”
- **Source type:** Official technical glossary.
- **Canonical locator:** Definition.
- **Digital URL:** https://csrc.nist.gov/glossary/term/cyclic_redundancy_check
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch15-verification/nist-crc-glossary.html`.
- **Integrity:** SHA-256 `44536ee21f88ca5c5c354d419568feb564caad22fe546959e3b7ac3835ba5c25`.
- **Rights/storage:** Public US government record retained for verification.
- **Notes:** Defines CRC as a checksum algorithm used to provide data integrity against accidental changes.

### `nist-crc-dads`

- **Citation:** Paul E. Black, “cyclic redundancy check,” *NIST Dictionary of Algorithms and Data Structures*, revised 19 July 2021.
- **Source type:** Official technical dictionary entry.
- **Canonical locator:** Definition and explanation of recalculation and comparison.
- **Digital URL:** https://xlinux.nist.gov/dads/HTML/cyclicRedundancyCheck.html
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch15-verification/nist-crc-dads.html`.
- **Integrity:** SHA-256 `a7373edc05a97a35899c398396341885ac54b61353c1da9254312b29c0ba02cf`.
- **Rights/storage:** Public US government record retained for verification.
- **Notes:** Explains that the receiver recalculates and compares the CRC to detect transmission errors.

### `sanskritdocuments-ashtadhyayi-ch16-rules`

- **Citation:** Pāṇini, *Aṣṭādhyāyī*, with the *Kāśikāvṛtti* and other commentarial material in the SanskritDocuments rule pages.
- **Source type:** Electronic Sanskrit primary text with traditional commentary.
- **Canonical locator:** Rules 1.4.80–82; 3.2.107–108; 3.4.7, 3.4.92, 3.4.94–98; 6.3.113; 7.1.9, 7.1.39, 7.1.46; 7.3.93; 7.4.74; 8.2.61; and 8.3.37.
- **Digital URL:** https://sanskritdocuments.org/learning_tools/ashtadhyayi/
- **Archived URL:** Same as the digital URL; individual rule pages use `vyakhya/{adhyāya}/{rule}.htm`.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch16-verification/ashtadhyayi-*.html`.
- **Integrity:** Combined SHA-256 over the sorted checksums of the twenty retained rule pages: `13812325442235a92147cc102d15c185445e6af631e32823ee610868f72c0027`.
- **Rights/storage:** Public Sanskrit text and commentary pages retained for research verification.
- **Notes:** Used to verify the scope rules and examples cited in Chapter 16. The standalone SanskritDocuments *sūtrapāṭha* confirms the standard numbering where a commentarial page contains an inconsistent displayed link number.

### `titus-aitareya-brahmana-5-11`

- **Citation:** *Aitareya Brāhmaṇa*, TITUS electronic text, based on Theodor Aufrecht's 1879 edition; electronic entry by Fco. Javier Martínez García and TITUS edition by Jost Gippert.
- **Source type:** Institutional electronic primary-text edition.
- **Canonical locator:** 5.11.2, TITUS page `ab164.htm`, sentence anchor `RV_AB_5_11_2`.
- **Digital URL:** https://titus.uni-frankfurt.de/texte/etcs/ind/aind/ved/rv/ab/ab164.htm
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch16-verification/titus-aitareya-brahmana-5-11.html`.
- **Integrity:** SHA-256 `47d5ff1ed913ed57ff830411673495d42bbd0e7fbf4e6bb3cc3b7dc1766e6dac`.
- **Rights/storage:** Public institutional electronic text retained for research verification.
- **Notes:** Verifies the separated *upasargas* in the passage containing **ā ... dviṣato vasu datte** and **nir enam ... nudate**.

### `aitareya-brahmana-sastri-1942`

- **Citation:** Anantakrishna Sastri, ed., *Aitareya Brahmana* (1942).
- **Source type:** Scanned printed Sanskrit edition and OCR.
- **Canonical locator:** Aitareya Brāhmaṇa 5.11.
- **Digital URL:** https://archive.org/details/aitareyabrahmana014460mbp
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/documents/ch16-verification/aitareya-brahmana-sastri-1942.txt`; metadata at `working/40_reference/sources/archive/web/internet-archive-metadata/aitareyabrahmana014460mbp.json`.
- **Integrity:** SHA-256 `8989b3b92be885ee7fe09f74ba37453e4b3f10e451ee3f68c071b9279890d9fb` (OCR).
- **Rights/storage:** Public research scan metadata and OCR retained for verification.
- **Notes:** Consulted as a second printed witness for the Aitareya passage; the exact searchable locator is supplied by the TITUS record.

### `vedic-heritage-introduction`

- **Citation:** Vedic Heritage Portal, Government of India, “Introduction.”
- **Source type:** Government institutional reference page.
- **Canonical locator:** “Classification of the Vedic Literature.”
- **Digital URL:** https://vedicheritage.gov.in/introduction/
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** Not retained; the host failed DNS resolution during the local archive attempt.
- **Integrity:** No local file.
- **Rights/storage:** Exact public institutional URL retained.
- **Notes:** Used only for the portal's enumeration of the four Vedas, their textual classes, and the six Vedāṅgas.

### `kripacharyulu-sayana-madhava-1986`

- **Citation:** Munuganti Kripacharyulu, *Sāyaṇa and Mādhava-Vidyāraṇya: A Study of Their Lives and Letters* (Rajyalakshmi Publications, 1986).
- **Source type:** Bibliographic record for a printed scholarly monograph.
- **Canonical locator:** Book record and the work survey cited in the endnote.
- **Digital URL:** https://books.google.com/books?id=WmQqAAAAYAAJ
- **Archived URL:** Same as the digital URL.
- **Accessed:** 2026-09-03.
- **Local record:** `working/40_reference/sources/archive/web/ch16-verification/google-books-kripacharyulu-sayana-madhava-1986.html`.
- **Integrity:** SHA-256 `dba7dc55f7bb8f0925add9d9ee65a454fa974c418614239f23738d3a2930d23a`.
- **Rights/storage:** Copyrighted monograph; bibliographic page only retained.
- **Notes:** Supports the historical case involving the Sāyaṇa-Mādhava household and its range of Vedic and other Sanskrit work. The endnote retains the attribution caveat.
