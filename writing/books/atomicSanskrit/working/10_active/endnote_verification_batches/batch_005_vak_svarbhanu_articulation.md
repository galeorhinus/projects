# Endnote Verification Batch 005 — Vāk, Svarbhānu, and Articulation

**Audit date:** 2026-09-02  
**Scope:** Ten Vedic and grammatical notes supporting the Svarbhānu arc, the Vāk sequence, Vāk Ambhṛṇī, and Chapter 17's articulation epigraph.

## Results

| Endnote | Risk | Result | Finding and action |
|---|:---:|---|---|
| `svarbhanu-svar-etymology` | P1 | Strengthened | Confirmed **स्वर्भानु (*Svarbhānu*)** as ***svar-bhānu*** and documented the light/heaven and light/ray senses of the two members. Marked the name-irony as the book's observation rather than a dictionary gloss. |
| `rigveda-5-40-atri-clearing` | P1 | Corrected | Checked RV 5.40.6. Replaced the unexplained "fourth *brahman*" with "fourth sacred formulation," distinguished the mantra's plural ***māyāḥ*** from the later expression ***āsurī māyā***, and added both live deployments. |
| `rigveda-5-40-9-atris-find-sun` | P1 | Strengthened | Confirmed the plural **अत्रयः (*atrayaḥ*)** and **नहि अन्ये अशक्नुवन् (*nahi anye aśaknuvan*)**, "no others were able." Added the locked source basis and repaired the structural field name. |
| `rigveda-10-71-2-sieve-vak` | P1 | Corrected | Confirmed the sieve, mental formation, and ***akrata*** clauses. Corrected **तितउना (*titaunā*)** in Chapter 18. Marked "auspicious radiance" as the book's interpretive rendering of the beauty-and-luster range of ***lakṣmī*** rather than the only lexical translation. |
| `rigveda-10-71-3-path-vak` | P1 | Strengthened | Confirmed the path, entry into the ṛṣis, distribution, and seven-singer clauses. Marked the connection to the *varṇamālā* as Chapter 9's architectural inference rather than language used by the mantra. |
| `rigveda-8-100-11-vak-blessing` | P1 | Corrected | **पशवः (*paśavaḥ*)** means animals or livestock. Replaced "all beings" with "animals of every form" in the Epilogue and the note. |
| `rigveda-10-71-4-vach` | P0 | Corrected | The padapāṭha reads **शृण्वन् । न । शृणोति । एनाम्**, not ***aśṛṇoti***. Corrected the word division, sandhi explanation, table, and translation. The body keeps the continuous saṃhitā form; the note now explains why its written division can be misleading. |
| `rigveda-1-164-45-four-quarters-vak` | P1 | Strengthened | Confirmed the four quarters, three hidden, and one humanly spoken. Added the locked source basis and identified "in the cave" as the concrete traditional rendering of ***guhā***, "in hiding / in secret." |
| `rigveda-10-125-vak-ambhrini` | P0 | Corrected | Removed the false claim that the seer wrote the mantra down, corrected ***juṣṭam*** from the adverb "joyfully" to the participle "cherished," and separated the hymn's cosmic scope from the later Mīmāṃsā doctrine of *apauruṣeyatva*. Replaced an unsupported argument from silence with the positive evidence of the received seer classification. |
| `rturasanam-murdha-shiksha` | P0 | Corrected | The line **ऋटुरषाणां मूर्धा** is found in the *Siddhāntakaumudī* explanation of Aṣṭādhyāyī 1.1.9, not in the *Pāṇinīya Śikṣā* as previously credited. Corrected Chapter 17, replaced the false padapāṭha framing with a grammatical breakdown, and repaired the compound-ending explanation. |

## Approved Body Corrections

1. Chapter 18: ***titauṇā*** → ***titaunā***.
2. Epilogue: "all beings, in many forms" → "animals of every form."
3. Chapter 17: *Pāṇinīya Śikṣā* attribution → *Siddhāntakaumudī*, on Aṣṭādhyāyī 1.1.9; two corresponding prose references changed.
4. Chapter 20: "fourth formulation of disciplined speech" → "fourth sacred formulation."

No other manuscript-body prose was changed in this batch.

## Principal Sources Checked

- Barend A. van Nooten and Gary B. Holland, *Rig Veda: A Metrically Restored Text with an Introduction and Notes* (Harvard University Press, 1994), RV 1.164.45, 5.40.6 and 5.40.9, 8.100.11, 10.71.2–4, and 10.125.
- Stephanie W. Jamison and Joel P. Brereton, *The Rigveda: The Earliest Religious Poetry of India* (Oxford University Press, 2014), the same mantra locations.
- Monier Monier-Williams, *A Sanskrit-English Dictionary* (Oxford, 1899), entries for ***svar***, ***bhānu***, ***Svarbhānu***, ***lakṣmī***, and ***paśu***.
- *Siddhāntakaumudī*, explanation of Aṣṭādhyāyī 1.1.9, **तुल्यास्यप्रयत्नं सवर्णम्**; corroborated by the *Laghusiddhāntakaumudī* articulation list.
- Kātyāyana, *Sarvānukramaṇī of the Rigveda*, ed. A. A. Macdonell (Oxford, 1886), for the Vāgāmbhṛṇī seer tradition.

## Digital Evidence Records

The exact URLs, archive identifiers, local paths, and checksums are registered
in [the digital source registry](../../40_reference/sources/as_source_registry.md)
under these stable IDs:

- `ut-rigveda-metrically-restored`
- `jamison-brereton-rigveda-2014-dcs`
- `cologne-mw-1899`
- `sanskritdocuments-rigveda-10`
- `ashtadhyayi-1-1-9-digital`
- `macdonell-sarvanukramani-1886-scan`

The exact UT Rigveda pages, SanskritDocuments page, Cologne dictionary
interface, and grammatical-commentary pages are retained as local HTML
captures. The Jamison-Brereton comparison points to an immutable commit of the
existing local DCS-aligned file. The public-domain *Sarvānukramaṇī* scan remains
at the Internet Archive under its stable item identifier.

## Outcome

The Svarbhānu and Vāk sequences remain available for the book's architectural argument, but the notes now distinguish mantra text from the book's later application. The batch removed three especially important errors: an incorrect Vedic word division, a written-transmission claim imposed on an oral corpus, and a false source attribution for Chapter 17's articulation line.

## Required Completion Tests

1. Regenerate and check the master ledger.
2. Verify all ten entries retain a Short and Deployments field.
3. Confirm the four approved body corrections and the absence of the replaced forms.
4. Run `python3 working/tools/source_registry_check.py`.
5. Run `git diff --check`.
