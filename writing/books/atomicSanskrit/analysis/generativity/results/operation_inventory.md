# Formation Operation Inventory

This is a census of the derivational identifiers exposed by the pinned Vidyut 0.4.0 engine. It is not a Sanskrit vocabulary total. An identifier enters a future count only after its meaning, input conditions, and base-level eligibility are established.

## Boundary

The engine exposes **304 identifiers**: **7 sanadi**, **122 ordinary krt**, and **175 taddhita**. The existing pilot contains **35 semantic-operation rows**. Twenty-eight name an affix; the other **7** describe identity, prefixing, feminine formation, inflection, or compounding.

The curated pilot touches **25 distinct engine identifiers**. The remaining **279 identifiers** are inventoried but semantically unclassified. All 304 rows therefore remain `not_admitted`; no multiplier has been applied to the 2,634 provisional base meanings.

A suffix identifier is not always one semantic operation. The pilot already records three meanings for `lyu~w`: action, instrument, and location. Conversely, a grammatical operation can surface through a replacement while the engine request retains the original identifier, as with prefixed `ktvA` producing the `lyap` form. The next pass must therefore classify meaning-bearing operations, not merely suffix names.

## Family Architecture

| Family | Role | Current boundary |
|---|---|---|
| Source धातुः (dhātuḥ) | base_count | 2634 provisional base meanings |
| उपसर्गः (upasargaḥ) | derived_base | 1103907 admitted word-meanings across the one-prefix and two-prefix layers |
| सनादिप्रत्ययः (sanādipratyayaḥ) from a धातुः (dhātuḥ) | derived_base | 263084 admitted word-meanings across unprefixed and one-prefix layers |
| नामधातुः (nāmadhātuḥ) from a प्रातिपदिकम् (prātipadikam) | derived_base | 3176352 admitted derived verbal meanings from the first 794078-meaning nominal inventory |
| कृदन्तम् (kṛdantam) | derived_word | 801942 laukika after known Vedic-base restrictions; 204738 admitted through Vaidika-specific operations |
| तद्धितान्तम् (taddhitāntam) | derived_word | 3971627 admitted word-meanings |
| स्त्रीप्रत्ययः (strīpratyayaḥ) | derived_word | 50 source-demonstrated word-meanings |
| समासः (samāsaḥ) | derived_word | 113 source-demonstrated compound meanings; 958 one-operation descendants from the 96 nominal compounds |
| नञ्-समासः (nañ-samāsaḥ) | derived_word | 3177340 admitted word-meanings; combined bounded subtotal 11116406 |
| तिङन्तम् (tiṅantam) | inflection | present active pilot only |
| सुबन्तम् (subantam) | inflection | masculine pacaka pilot only |

## Engine Census

| Family | Identifiers | Seeded by pilot | Pending semantic classification |
|---|---:|---:|---:|
| sanadi | 7 | 7 | 0 |
| krt | 122 | 13 | 109 |
| taddhita | 175 | 5 | 170 |

## What Comes Next

1. Split identifiers that carry several semantic relations into separate meaning-bearing operations.
2. For each operation, state the eligible input class and record exclusions, required prefixes, and construction conditions.
3. Test those rules against a bounded sample of the current 2,634 base meanings.
4. Enumerate derived verbal, nominal, and indeclinable meanings separately. Inflection follows only after those base inventories are fixed.

The full row-level census is in `operation_inventory.csv`; `operation_inventory.json` carries the same rows with source URLs, checksums, and input hashes.
