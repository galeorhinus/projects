# *Varṇamālā* Analysis — Reproducibility Bundle

A reproducibility bundle for the empirical claims in **Chapter 7** (*ॐ (Oṃ): The Anatomy of Sound*), **Chapter 8** (*Mapping the Mouth: The Sonomeric Grid*), and **Appendix Part 3** (*The Sonomer Beneath the Audiograph*) of ***Atomic Sanskrit*** (Parag Tope).

The bundle counts *varṇāḥ* in the Rigveda Saṃhitā *padapāṭha* and aggregates the counts by category (*svara* / *vyañjana* / *ayogavāha*), by *sthāna* (place of articulation), and by individual *varṇa*. The output is the empirical anchor for the engineering claims about the *varṇamālā*'s deployment in the *śruti* corpus.

Anyone can reproduce every count by running the script against the source data.

---

## Structure

```
analysis/varnamala/
├── README.md                              ← this file
├── data/
│   └── derived/
│       ├── varna_counts.csv               ← per-varṇa token counts (generated)
│       ├── category_summary.csv           ← svara / vyañjana / ayogavāha totals (generated)
│       └── place_summary.csv              ← per-sthāna totals for vyañjanāni (generated)
└── scripts/
    └── count_varnas_rigveda.py            ← tokenizer + classifier + aggregator
```

Source data lives in the companion *gaṇāḥ* bundle and is read directly: `analysis/ganah/data/raw/dcs/dcs/data/rigveda/pada-and-analysis.dat`.

---

## Quick start

Requirements: **Python 3.10+**. No external dependencies — standard library only.

```bash
# From the bundle root:
python3 scripts/count_varnas_rigveda.py
```

The script prints a structured report to stdout and writes the three derived CSVs to `data/derived/`.

---

## What the script does

### `count_varnas_rigveda.py`

Reads the DCS Rigveda *padapāṭha* (tab-separated; the relevant column is the IAST text of each *pada*) and performs four operations:

1. **Greedy IAST tokenization.** Splits each *pada* into a sequence of *varṇāḥ*. Digraphs (`kh`, `gh`, `ch`, `jh`, `ṭh`, `ḍh`, `th`, `dh`, `ph`, `bh`, `ai`, `au`) are recognized as single *varṇāḥ* rather than two-character sequences. Anusvāra accepts both common IAST encodings (`ṁ` U+1E41 and `ṃ` U+1E43) and normalizes to `ṃ` internally.
2. ***Anusvāra* resolution — Pāṇini 8.4.58 (*parasavarṇa*).** Anusvāra before a stop or nasal resolves to the homorganic nasal of the following consonant's *sthāna* (*kaṇṭhya* → ङ, *tālavya* → ञ, *mūrdhanya* → ण, *dantya* → न, *oṣṭhya* → म). Anusvāra before semivowels, sibilants, *h*, or at word-final position remains as *ayogavāha*. This recovers the underlying *varṇa* sequence the *padapāṭha* form leaves implicit.
3. **Classification.** Each *varṇa* is tagged with its category (*svara* / *vyañjana* / *ayogavāha*), and *vyañjanāni* are further tagged with their *sthāna* (*kaṇṭhya* / *tālavya* / *mūrdhanya* / *dantya* / *oṣṭhya*) and class (*stop-voiced-unasp*, *stop-voiced-asp*, *stop-unvoiced-unasp*, *stop-unvoiced-asp*, *nasal*, *antaḥstha*, *ūṣman*).
4. **Aggregation.** Token counts are summed per *varṇa*, per category, and per *sthāna*; written to three derived CSVs.

---

## Output schemas

### `data/derived/varna_counts.csv`

| column | meaning |
|---|---|
| `varna` | the IAST *varṇa* (single character or digraph) |
| `category` | `svara`, `vyañjana`, or `ayogavāha` |
| `place` | *sthāna* — for *vyañjanāni* only |
| `class` | functional class — for *vyañjanāni* only |
| `count` | token frequency in the corpus |
| `share_of_total` | count / total *varṇa* tokens |

Rows are sorted by descending `count`.

### `data/derived/category_summary.csv`

| column | meaning |
|---|---|
| `category` | `svara`, `vyañjana`, `ayogavāha` |
| `count` | total token count for the category |
| `share_of_total` | category fraction of all *varṇa* tokens |

### `data/derived/place_summary.csv`

| column | meaning |
|---|---|
| `place` | *sthāna* — *kaṇṭhya*, *tālavya*, *mūrdhanya*, *dantya*, *oṣṭhya* |
| `vyanjana_count` | total *vyañjana* tokens at that *sthāna* |
| `share_of_vyanjanas` | place fraction of all *vyañjana* tokens |

---

## Headline findings (current run)

Total token count: ~909,000 *varṇāḥ* across the Rigveda Saṃhitā *padapāṭha*.

| Category | Share |
|---|---:|
| *vyañjana* | 51.7% |
| *svara* | 43.3% |
| *ayogavāha* | 5.0% |

*Sthāna* distribution among *vyañjanāni*:

| Place | Share |
|---|---:|
| *dantya* | 36.2% |
| *oṣṭhya* | 27.9% |
| *tālavya* | 14.6% |
| *mūrdhanya* | 13.8% |
| *kaṇṭhya* | 7.4% |

The two front *sthāna*s (*dantya* + *oṣṭhya*) account for ~64% of all consonant tokens; the deepest position (*kaṇṭhya*) is the rarest *vyañjana* place by a clear margin. The corpus deploys the engineered grid asymmetrically — the same grid the *Prātiśākhya* discipline documents and Pāṇini's *Aṣṭādhyāyī* operates over.

Top individual *varṇāḥ* by token frequency: *a* (21.0%), *ā* (6.6%), *t* (6.1%), *i* (5.7%), *m* (5.6%), *v* (5.4%), *ḥ* (4.8%), *r* (4.8%), *n* (4.7%), *y* (4.1%), *s* (4.0%).

---

## Source data attribution

The Rigveda Saṃhitā *padapāṭha* file is read from the companion *gaṇāḥ* bundle:

- **File**: `analysis/ganah/data/raw/dcs/dcs/data/rigveda/pada-and-analysis.dat`
- **Source corpus**: Digital Corpus of Sanskrit (DCS), Oliver Hellwig, distributed via the `OliverHellwig/sanskrit` GitHub repository.
- **Format**: TSV with columns `book`, `hymn`, `stanza`, `pada`, `text`, `lemmata`, `lexids`, `refids`. The script reads only the `text` column, which carries the IAST *padapāṭha* text of each *pada*, without accent marks.

The *padapāṭha* form is the word-segmented citation form of the Rigveda preserved across the *paramparā*; it gives one *varṇa* sequence per *pada* without the *saṃhitā*-form *sandhi* fusions. That is the right input for *varṇa* counts: it shows what the engineered architecture actually deploys, not the surface *saṃhitā* concatenations.

The underlying Rigveda corpus is an ancient Sanskrit canonical text in the public domain. The DCS preparation carries its own attribution; users redistributing the source `.dat` should check the upstream repository.

---

## How the findings cross-reference the book

| Book location | Reproduced by |
|---|---|
| Chapter 7 §§7.6–7.8 (the *varṇamālā* mapped to the speaking instrument) | `count_varnas_rigveda.py` — category, *sthāna* totals |
| Chapter 8 §8.2 (the *varṇamālā* as engineered selection) | `count_varnas_rigveda.py` — per-*varṇa* token counts |
| Chapter 8 §8.4 (snap-to-grid; *sthāna* sampling) | `place_summary.csv` |
| Chapter 8 §8.6 (the engineering precedes Pāṇini — the deployment is *in* the corpus) | `varna_counts.csv`, `category_summary.csv` |
| Appendix Part 3 (the sonomer beneath the audiograph) | All outputs |

The book's empirical claims about *varṇamālā* deployment in the *śruti* corpus should match the counts produced here, modulo any minor numerical drift if the upstream DCS *padapāṭha* is updated.

---

## Methodology notes for future work

1. **Anusvāra in word-final position.** The current implementation leaves word-final anusvāra as *ayogavāha* on the assumption that the next-token lookahead in the *padapāṭha* stream is unreliable across word boundaries. A *saṃhitā*-aware variant could resolve more anusvāras at the cost of importing *sandhi* surface effects the *padapāṭha* form deliberately undoes.
2. **Visarga inventory split.** The script counts all visarga occurrences as a single *ayogavāha* class. A finer cut would distinguish *jihvāmūlīya*, *upadhmānīya*, and the unmarked visarga the *Prātiśākhya* tradition documents separately. The DCS text does not preserve those distinctions, so the split would require a phonologically-informed re-derivation.
3. **Token-frequency vs. type-frequency.** The current outputs are token counts. A type-frequency variant (counting one occurrence per distinct *pada*) would test whether the *sthāna* asymmetry holds at the lexical level or whether it is amplified by high-frequency function words.
4. **Other *śruti* corpora.** Extending to the Atharvaveda, Sāmaveda, and Yajurveda *padapāṭhas* (when DCS coverage allows) would test whether the *varṇamālā* deployment signature is Rigveda-specific or a stable *śruti*-wide pattern.

---

## Citing this bundle

If you use this bundle in research:

> Parag Tope, *Varṇamālā Analysis — Reproducibility Bundle* (2026), accompanying *Atomic Sanskrit* (Vol. 1 of *Second Shanti*), Chapters 7–8 and Appendix Part 3.

Underlying source data: Digital Corpus of Sanskrit (DCS), `OliverHellwig/sanskrit` GitHub repository.
