# Derivation Record Schema

Status: Application-facing contract proposed 2026-09-14. Apply it to new analytical layers and use the eventual exporter to normalize earlier ledgers.

## Principle

The identity being counted is a word-meaning, not a spelling. A form may carry several meanings, and one meaning may have alternative derivational paths. The schema must preserve both situations.

## Required Word-Meaning Fields

| Field | Purpose |
|---|---|
| `word_meaning_id` | Stable identity for one word and one meaning |
| `form_slp1` | Internal normalized form |
| `form_devanagari` | Primary displayed Sanskrit form |
| `form_iast` | Fallback transliteration |
| `meaning` | Concise meaning carried by this record |
| `semantic_tags` | Searchable concepts and operation relations |
| `form_class` | Verbal base, nominal base, indeclinable, conjugated form, declined form, or compound |
| `domain` | लौकिक, वैदिक, or another explicitly declared scope |
| `meaning_evidence` | Source-defined, compositionally generated, context-dependent, or experimental |
| `model_release` | First released model containing the record |
| `count_status` | Admitted, overlap, excluded, unresolved, or experimental |
| `materialization_status` | Materialized lexical record or virtual compound generated on demand |

## Required Derivation Fields

| Field | Purpose |
|---|---|
| `derivation_id` | Stable identity for one derivational path |
| `word_meaning_id` | Result produced by the path |
| `parent_word_meaning_ids` | One parent for ordinary derivation; several for compounds |
| `source_atom_ids` | Ultimate धातुः or declared source inputs |
| `ordered_operations` | Operations applied in grammatical order |
| `intermediate_forms` | Forms produced between source and result |
| `rule_refs` | Governing grammatical rules |
| `source_record_ids` | Archived evidence records supplying meanings or restrictions |
| `engine_name` | Generator or verifier used |
| `engine_version` | Pinned version and commit |
| `verification_status` | Exact, partial variant coverage, independently implemented, unresolved, or mismatch |
| `derivational_depth` | Number of counted operations from the declared source input |

## Required Virtual-Compound Fields

| Field | Purpose |
|---|---|
| `compound_relation_id` | Released semantic relation joining the members |
| `member_word_meaning_ids` | Ordered or unordered parent meanings, as required by the relation |
| `compound_depth` | Compound depth under the released recursion boundary |
| `meaning_template` | Compositional relation used to estimate the result's meaning |
| `generation_instruction` | Deterministic engine request sufficient to reconstruct the form and rule path |
| `cache_status` | Never generated, generated for this request, or retained in the application cache |

## Required Virtual-Inflection Fields

| Field | Purpose |
|---|---|
| `lexical_word_meaning_id` | Verbal or nominal meaning receiving the grammatical coordinate |
| `inflection_family` | Verbal or nominal grammatical expansion |
| `lakara_id` | Tense-or-mood coordinate for a verbal form; empty for a nominal form |
| `purusha` | प्रथम, मध्यम, or उत्तम grammatical person; empty for a nominal form |
| `vibhakti_id` | Relation coordinate for a nominal form; empty for a verbal form |
| `vacana` | Singular, dual, or plural number |
| `prayoga` | कर्तरि, कर्मणि, or भावे construction within the released verbal scope |
| `linga` | Lexical or contextually selected gender used to generate a nominal output |
| `pada_outputs` | Generated परस्मैपदम् and आत्मनेपदम् alternatives attached to a verbal cell |
| `generation_instruction` | Deterministic engine request sufficient to reconstruct every output and rule path |

## Path Rules

1. Never merge records merely because their spellings coincide.
2. Never multiply a meaning merely because an operation produces optional forms.
3. Preserve alternative paths to the same word-meaning as separate derivations attached to one identity.
4. Preserve different meanings of the same form as separate word-meaning identities.
5. Keep grammatical inflection separate from lexical derivation.
6. Record every model boundary needed to explain why a further possible operation was not followed.
7. Store source locators and hashes through stable source-record identifiers rather than repeating long citations in every row.
8. Do not require every formal compound slot to exist as a stored word-meaning row. A virtual compound must still preserve its released relation, parent meanings, depth, generated form, and complete reconstruction path.
9. Count an inflectional semantic cell once for its lexical meaning and grammatical coordinates. Optional outputs, पद alternatives, and repeated spellings remain attached to the cell unless a separately established semantic distinction requires another record.

## Release Manifest

The future exporter must generate `results/generativity_release_manifest.json` with:

- schema and model versions;
- included domains, operations, and maximum depths;
- excluded and unresolved operation families;
- row counts by form class and stage;
- separate materialized lexical totals and symbolic compound-capacity totals;
- supported compound relations, member-inventory hash, and maximum compound depth;
- canonical ledger paths and SHA-256 hashes;
- source-manifest paths and hashes;
- Vidyut version and commit;
- exporter version and test result.

The application may display only records covered by a valid release manifest unless it labels them experimental.
