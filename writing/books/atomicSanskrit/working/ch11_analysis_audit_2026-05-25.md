# Ch11 Analysis Audit — 2026-05-25

## Status

The Ch11 empirical bundle is mostly usable. One important stale item was fixed in this pass:

- `analysis/dhatupatha/scripts/analyze_racana_by_gana.py` now uses the current Ch10 top-ten *racanā* roster.
- `analysis/dhatupatha/data/derived/racana_by_gana.csv` and `.md` were regenerated.

The old working note `working/ch11_racana_gana_cross_findings.md` still contains stale interpretive tables from the pre-cleanup matrix. Use the regenerated derived files below for numbers.

## Current Data Sources

### 1. Scaffold × Gaṇa Matrix

Files:

- `analysis/dhatupatha/data/derived/racana_by_gana.csv`
- `analysis/dhatupatha/data/derived/racana_by_gana.md`
- `analysis/dhatupatha/scripts/analyze_racana_by_gana.py`

Current headline:

- Total *dhātavaḥ*: **2,168**
- Observed *racanāḥ*: **47**
- Observed *gaṇāḥ*: **10**
- Top-ten *racanāḥ* cover: **1,973 / 2,168 = 91.01%**
- Populated cells: **140 / 470**

Top-ten row totals:

| Racanā | Name | Count |
|---|---|---:|
| CV1C | *gamādi* | 926 |
| CCV1C | *spadādi* | 232 |
| CV1CC | *manthādi* | 216 |
| CV2C | *vācādi* | 214 |
| CV2 | *dhādi* | 89 |
| V1C | *iṣādi* | 70 |
| CCV2C | *hrādādi* | 65 |
| CV1 | *krādi* | 64 |
| CCV2 | *sthādi* | 49 |
| CCV1CC | *spardhādi* | 48 |

Useful Ch11 conclusions:

- *Racanā* and *gaṇa* are two axes, not one.
- The *gamādi* CV1C scaffold spans every gaṇa and remains the central corridor.
- *Bhvādi* remains the largest operational landing zone.
- The matrix is dense in a few central corridors and sparse elsewhere.
- Empty cells matter: they show which scaffold × operation pairings the system does not use.

### 2. Scaffold Deployment / Actual Use

Files:

- `analysis/ganah/data/derived/scaffold_reactivity_summary.csv`
- `analysis/ganah/data/derived/scaffold_reactivity_summary.md`
- `analysis/ganah/data/derived/dhatu_scaffold_path_c_join_canonical.csv`
- `analysis/ganah/data/derived/dhatu_scaffold_path_c_join_audit.txt`

Current headline:

- Inventory rows: **2,168**
- Canonical distinct *dhātavaḥ*: **1,518**
- DCS-visible canonical *dhātavaḥ*: **575**
- Total DCS-derived combinations after deduplication: **18,594**
- Total DCS occurrences after deduplication: **764,576**

Top-ten scaffold coverage:

- Inventory: **91.0%**
- *Dhātavaḥ* visible in actual use: **89.0%**
- Combinations: **92.5%**
- Occurrences: **93.6%**

Audit result:

- Top 20 DCS roots are matched or accounted for.
- `vartay` is accounted but not forced into the *Dhātupāṭha* scaffold inventory because DCS carries it as a corpus-derived causative/derived lemma.
- Repeated gaṇa rows do not inflate corpus usage metrics; usage is deduplicated by canonical *dhātuḥ*.

Useful Ch11 conclusion:

- The same scaffolds that dominate the inventory also dominate actual use. This belongs as the bridge from Ch10 into Ch11, but Ch11 should not re-prove the whole Ch10 deployment argument.

### 3. Path C Reactivity / Valency

Files:

- `analysis/ganah/data/derived/path_c_valency.csv`
- `analysis/ganah/data/derived/path_c_with_tiers.csv`
- `analysis/ganah/data/derived/tier_distribution.txt`
- `analysis/ganah/data/derived/tier_cutoffs.txt`
- `analysis/ganah/data/derived/spearman_summary.txt`
- `analysis/ganah/FINDINGS.md`

Current headline:

- Total DCS roots: **3,839**
- Total verb tokens: **1,007,361**
- Polyvalent tier: **147 roots = 3.8%**, carrying **67.6%** of verb tokens.
- Bivalent tier: **1,059 roots = 27.6%**, carrying **30.5%** of verb tokens.
- Monovalent tier: **2,633 roots = 68.6%**, carrying **1.9%** of verb tokens.
- Canonical polyvalent set: *kṛ, bhū, sthā, gam, jñā, dā, dhā, nī, hṛ*.
- Canonical set is stable under all tested tier cutoffs.

Useful Ch11 conclusion:

- The inventory is not flat. A small hyper-reactive core carries most deployment.

### 4. Cross-Corpus Invariance

Files:

- `analysis/ganah/data/derived/cross_corpus_comparison.txt`
- `analysis/ganah/data/derived/cross_corpus_top20.csv`
- `analysis/ganah/data/derived/per_corpus_productivity.csv`
- `analysis/ganah/data/derived/per_corpus_productivity.md`

Current headline:

- Tested corpora: Ṛgveda, Atharvaveda Śaunaka, Mahābhārata, Rāmāyaṇa.
- BhG is absent from the DCS Mahābhārata range; Rāmāyaṇa substitutes as the *smriti* epic.
- Canonical nine are **9/9 attested** in every sub-corpus.
- In the *smriti* corpora, the canonical nine are **9/9 in the top 20**.
- In the *śruti* corpora, **6/9** are in the top 20, with ritual-specific atoms entering the top tier.

Useful Ch11 conclusion:

- The hyper-reactive core is not an artifact of one genre. It remains visible across different Sanskrit use-domains.

### 5. Column / Periodic-Table Axes

Files:

- `analysis/ganah/data/derived/column_axes.txt`
- `analysis/ganah/data/derived/column_axes_per_root.csv`
- `figures/ganah/fig_periodic_table.py`
- `figures/build/ganah_periodic_table.svg`

Current headline:

- The current figure positions *dhātavaḥ* by initial varga column × inherent vowel.
- Path C column-axis testing reports four candidates and deliberately does not pick a winner.
- Inherent vowel has the sharpest heterogeneity score in the report.
- Initial varga column remains visually and conceptually useful because it ties Ch11 back to the *varṇamālā* and articulatory architecture.

Drafting caution:

- Do not say the varga-column axis is the only possible periodic-table axis unless the chapter explicitly defends that choice.
- Better phrasing: the *dhātuḥ* has multiple axes of periodicity; the figure uses varga column × inherent vowel because those are visible, reproducible, and tied to the sound architecture.

### 6. Figure Refresh Status

Attempted to rerender:

- `figures/ganah/fig_periodic_table.py`
- `figures/ganah/fig_canonical_rank_trajectory.py`

Blocked by local Python environment:

```text
ImportError: cannot import name 'VisibleDeprecationWarning' from 'numpy'
```

The existing SVGs remain available:

- `figures/build/ganah_periodic_table.svg`
- `figures/build/ganah_canonical_rank_trajectory.svg`

The data feeding them has not been invalidated in this audit, but the figures were not refreshed in this pass.

## Chapter Planning Consequence

Ch11 should use this order:

1. Ch10 bridge: compact atoms are built from scaffolds.
2. Scaffold × gaṇa: construction axis and operation axis intersect.
3. Valency: operation can be measured.
4. Reactivity tiers: the inventory is not flat.
5. Hyper-reactive core: a small group carries most deployment.
6. Periodic table: visible axes arrange the reactive inventory.
7. Cross-corpus invariance: the same core persists across Sanskrit use-domains.
8. Pāṇini decoded the table.

