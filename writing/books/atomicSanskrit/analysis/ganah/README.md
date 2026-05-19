# Path C — Corpus-Attested Combinatorial Valency for Sanskrit *Dhātavaḥ*

*Empirical-analysis bundle for the Ch 11 / Appendix Part 5 next-generation workstream. Self-contained; reproducible.*

## What is in this bundle

This directory holds the Path C empirical analysis: a corpus-attested combinatorial-valency measure for the 2,168-entry Pāṇinian *Dhātupāṭha*. The measure operationalizes valency as the **count of distinct (*upasarga*, *pratyaya*) pairs that produce attested forms** in a reference Sanskrit corpus. The result is a per-*dhātu* number that quantifies the atom's *operational combinatorial reach* — what the architecture actually deploys, not what the lexicographers compiled.

Path C complements two prior measures:

- **Path A** (`analysis/dhatupatha/` companion bundle) — MW-derivative count. Proxy-grade; uses Monier-Williams 1899 and Apte 1890 dictionary derivative-counts. Retained as baseline; documents lexicographer compilation, not corpus-attested deployment.
- **Path B** (future work) — *Aṣṭādhyāyī* affix-licensing count. Documents what Pāṇini's rules license; deferred to future research.
- **Path C** (this bundle) — corpus-attested combinatorial yield. Documents what the architecture actually deploys in the canonical corpus.

The chapter prose (Ch 11) operationalizes valency via Path C; this bundle is the reproducibility backbone.

## Corpus choice

See `STATUS.md` for the corpus actually used by this run and the rationale for the choice. Candidates considered in decision-tree order:

1. **DCS — Digital Corpus of Sanskrit** (Hellwig). Lemmatized, covers Vedic + classical + post-classical, includes BhG and *Ṛgveda saṃhitā* sub-corpora. Available via the open-source `OliverHellwig/sanskrit` GitHub mirror.
2. **GRETIL** — Göttingen Register of Electronic Texts in Indian Languages. Larger but inconsistently tagged.
3. **Whitney 1885** — *The Roots, Verb-Forms, and Primary Derivatives of the Sanskrit Language*. Public-domain fallback if both above are unavailable.

The bundle's analysis is corpus-agnostic — any corpus that yields a (*dhātu*, *upasarga*, *pratyaya*) attestation index feeds the same scripts.

## Methodology

Path C valency per *dhātu*:

```
v(dhātu) = | { (upasarga, pratyaya) : there exists an attested form of dhātu
              with this upasarga prefix and this pratyaya suffix in the corpus } |
```

Notes:

- *Upasarga* — set of 22 canonical Sanskrit prefixes (*pra, parā, apa, sam, anu, ava, nis, niḥ, dus, duḥ, vi, ā, ni, adhi, api, ati, su, ud, abhi, prati, pari, upa*). Bare-stem (no prefix) counted as one valency-slot.
- *Pratyaya* — set of Sanskrit suffixes. Two cuts available: (a) all *kṛt-pratyayas* + finite-verb endings (*tiṅ*) — the full apparatus; (b) the productive subset (the ~40–60 most-deployed suffixes across the corpus). Default: (a); (b) available via flag.
- Attestation cut-off: a form counts if it appears at least once in the reference corpus. (Token-frequency-weighted variant available via flag for sensitivity analysis.)

## Layout

```
analysis/ganah/
├── README.md          (this file)
├── STATUS.md          (live status log; morning handoff)
├── data/
│   ├── raw/           (downloaded corpus files; not committed if large)
│   └── derived/       (computed attestation indices, valency tables)
├── scripts/           (Python analysis scripts; stdlib only)
└── figures/           (SVG figures produced)
```

## Reproducing the analysis

```bash
cd analysis/ganah/
python3 scripts/acquire_corpus.py        # Phase 2: download / verify corpus
python3 scripts/build_attestation.py     # Phase 3: parse → (dhātu, upasarga, pratyaya) index
python3 scripts/compute_valency.py       # Phase 4: per-dhātu Path C valency
python3 scripts/spearman_baseline.py     # Phase 5: Path A vs Path C correlation
python3 scripts/tier_cutoffs.py          # Phase 6: tier-assignment sensitivity
python3 scripts/tier_distribution.py     # Phase 7: tier-distribution across full DP
python3 scripts/cross_corpus.py          # Phase 8: BhG vs Ṛgveda comparison
python3 scripts/column_axis_test.py      # Phase 9: 4-candidate axis test
python3 scripts/cross_gana_extension.py  # Phase 10: per-gaṇa column distribution
```

Each script reads / writes from `data/derived/`. Requirements: Python 3.10+, standard library only (the bundle deliberately avoids external dependencies for reproducibility).

## Author + Provenance

Author: Parag Tope (book-side author). Analysis scripts and methodology drafted during the autonomous night session of 2026-05-18 under the brief in `working/as_todo.md` CURRENT FOCUS — *Path C autonomous-night-session kickoff*.

The reproducibility bundle is structured for public release alongside the book and the companion dossier; nothing in this directory depends on private resources.

## License

The scripts and methodology documentation in this bundle are released under the same terms as the book's repository. The corpus data files in `data/raw/` carry the upstream corpus's own license (DCS / GRETIL / Whitney 1885 — public domain as applicable).
