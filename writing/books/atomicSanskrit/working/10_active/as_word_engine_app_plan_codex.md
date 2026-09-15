# Atomic Sanskrit Word Engine: Application Plan

Started: 2026-09-14.

Status: Planned for later development. The bounded generativity analysis is complete. No application implementation has begun.

The bounded analysis is now complete. The [preliminary implementation plan](as_word_engine_preliminary_implementation_plan_codex.md) defines the path from the research ledgers to a versioned release compiler, query service, and public interface. The selected public name is **Atomic Sanskrit Word Engine**, with **शब्दयन्त्रम् (*śabdayantram*)** as its Sanskrit identity.

## Purpose

Build a public application for `atomicsanskrit.org` that exposes the bounded generative model developed for *Atomic Sanskrit*. The application will present every materialized word in a named release and generate supported compound branches on demand within that release's operations and depth. It will not claim to enumerate unrestricted Sanskrit recursion.

The application has three principal uses:

1. Select a धातुः (*dhātuḥ*) and explore every word-meaning descended from it within the current model.
2. Enter a Sanskrit word and inspect every supported derivational path, meaning, and grammatical analysis.
3. Enter a requested meaning and receive candidate Sanskrit words whose recorded or compositionally generated meanings address it.

## Governing Boundary

“All possible words” means every materialized word and every requested formal compound supported by the operations and maximum depth declared by the current Atomic Sanskrit model release.

The application must never silently continue a derivation beyond that release boundary. Results outside the model may be presented only in a separately labeled experimental mode. Public totals must distinguish materialized lexical records from formal compound-capacity slots. Every displayed path must reconcile either to a released ledger row or to a deterministic compound derivation under the released relation model.

## Canonical Research Records

The application plan links to these records rather than duplicating their contents:

| Application requirement | Canonical record |
|---|---|
| Research method, current subtotal, and remaining passes | [Generativity analysis plan](as_generativity_count_analysis_codex.md) |
| Reproduction commands and artifact index | [Generativity README](../../analysis/generativity/README.md) |
| Admission, exclusion, and counting rules | [Admission standard](../../analysis/generativity/admission_standard.md) |
| Incremental operations and counts | [Publication reporting ladder](../../analysis/generativity/results/publication_reporting_ladder.md) |
| Machine-readable stage sequence | [Generation stage graph](../../analysis/generativity/results/generation_stage_graph.json) |
| Latest plain तद्धित source pass | [Plain तद्धित six-pass report](../../analysis/generativity/results/plain_taddhita_six_pass_summary.md) |
| Symbolic compound capacity and depth boundary | [Twelve-pass समास capacity report](../../analysis/generativity/results/samasa_capacity_twelve_pass_summary.md) |
| Verbal citation and person-number capacity | [Twelve-pass तिङन्त capacity report](../../analysis/generativity/results/tinanta_twelve_pass_summary.md) |
| Name-form citation and relation-number capacity | [Twelve-pass नामरूप capacity report](../../analysis/generativity/results/subanta_twelve_pass_summary.md) |
| Reader-facing lexical and grammatical partition | [Sanskrit word-space graph](../../analysis/generativity/results/wordspace_category_graph.md) |
| Digital sources, URLs, checksums, and local archives | [Source registry](../40_reference/sources/as_source_registry.md) |
| Sanskrit-first grammatical terminology | [Grammar terms](../../analysis/generativity/grammar_terms.md) |
| Required application record structure | [Derivation record schema](../../analysis/generativity/derivation_record_schema.md) |
| Screens, interactions, and result language | [Product specification](as_word_engine_product_spec_codex.md) |

## Product Modes

### 1. Generate From an Atom

The user chooses a धातुः meaning, domain, permitted operation families, and maximum depth. The application traverses the released derivation graph and displays all matching descendants. Large families require filters, pagination, summaries by operation, and an expandable derivation tree.

### 2. Decode a Word

The user enters Devanagari, IAST, or another supported transliteration. The application normalizes the input, finds matching forms, and returns every supported word-meaning and path. Identical spellings with different meanings or derivations remain separate results.

### 3. Find Words for a Meaning

The user describes a desired meaning. The application searches source glosses, semantic tags, and generated meaning descriptions; identifies possible atoms and operations; and ranks candidate words. Grammatical generation validates forms. A semantic search match alone cannot establish grammatical validity.

## Meaning Evidence

Every displayed meaning must carry one of these labels:

1. **Source-defined:** stated by a grammatical source or commentary used in the analysis.
2. **Compositionally generated:** calculated from an admitted source meaning and licensed operations.
3. **Context-dependent:** several supported analyses remain possible.
4. **Experimental:** outside the released count and clearly separated from ordinary results.

The application must not force one interpretation when the ledger contains several.

## Development Sequence

1. Freeze the derivation record schema before the remaining analytical layers are generated.
2. Require every remaining pass to preserve parent identifiers, ordered operations, intermediate forms, meanings, rule references, and verification status.
3. Write a release exporter that normalizes all admitted ledgers into application tables.
4. Generate `analysis/generativity/results/generativity_release_manifest.json` from code. It must contain the model version, schema version, operation boundaries, ledger hashes, source manifests, engine version, counts, and exclusions.
5. Validate that exported totals exactly match the research subtotal and that sampled paths regenerate.
6. Build the forward धातुः explorer.
7. Build reverse word decoding from the same graph.
8. Add meaning-to-word search after semantic tags and confidence labels are stable.
9. Perform desktop and mobile usability, accessibility, performance, and provenance testing.
10. Publish a versioned release at `atomicsanskrit.org`.

## Storage and Serving Direction

The research ledgers remain canonical. The application consumes an exported release and never edits the analysis.

Use columnar files such as Parquet for reproducible release artifacts and local audits. Use a query database or search service for production. The final choice depends on the existing `atomicsanskrit.org` infrastructure and the size of the completed ledgers. Eleven million or more materialized word-meaning paths require server-side search, pagination, and indexes; they should not be shipped to a browser as one dataset. The database stores this million-scale lexical inventory, not the trillions of formal compound slots. Compound requests use the released member inventory and relation rules, run deterministically through the pinned engine, and may be cached after generation.

## Pregeneration and Runtime AI

The linguistic system must not depend on AI at runtime. Every ordinary Sanskrit result must come from the versioned and verified release, either as a pregenerated lexical record or as a deterministic compound generated under its declared rules.

Pregenerate:

- every admitted materialized word-meaning;
- Devanagari, IAST, and normalized forms;
- derivational operations, parent records, and intermediate forms;
- rule and source references;
- grammatical classifications;
- source-defined and compositionally estimated meanings;
- semantic tags, aggregate counts, and search indexes;
- alternative analyses and paths;
- semantic embeddings, if the chosen search design uses them.

Do not pregenerate every formal compound or inflectional slot. Pregenerate the canonical member inventories, relation and inflection definitions, capacity formulas, validation fixtures, and search metadata. Generate a requested compound, verbal paradigm, or name-form paradigm deterministically at runtime, preserve its parents and grammatical coordinates, retain the engine rule path, and cache the result when useful. A generated compound is a formal semantic possibility under an intended relation; the interface must not imply that it is already used, independently useful without context, or recorded in a dictionary.

Forward generation from a धातुः, Sanskrit word decoding, derivation-tree browsing, filtering, and exact or tagged meaning search must work without AI.

Runtime AI is optional. Its permitted role is limited to:

1. converting an unrestricted meaning request into structured concepts and operations;
2. translating a query from a supported modern language;
3. explaining an existing derivation in simpler language; and
4. ranking released candidates against the wording of the request.

AI may not invent, validate, admit, or silently alter a Sanskrit form or meaning. It may return only materialized candidates from the released ledger or virtual compounds produced by the released deterministic relation model. The application must display the structured interpretation used for a natural-language search and allow the user to correct it before or after retrieval.

If the AI service is unavailable, the application must retain all core functions through exact search, semantic tags, relation selectors, and deterministic graph traversal.

## Required Release Tables

1. Word-meanings.
2. Surface forms and transliterations.
3. Derivational operations and compound relation definitions.
4. Parent-child derivation edges.
5. Complete ordered derivation paths or deterministic instructions for reconstructing virtual compound paths.
6. Semantic tags and searchable glosses.
7. Materialized grammatical forms and deterministic specifications for virtual paradigms, kept distinct from lexical word-meanings.
8. Rules and source records.
9. Model releases and artifact hashes.

## Acceptance Criteria

- Every ordinary result belongs to a named model release.
- Every counted result has a complete path back to a source धातुः or declared nominal input.
- Every path records ordered operations and governing rules.
- Every public count reconciles exactly to the release manifest.
- Same spelling with different meanings remains separate.
- Alternative paths remain visible rather than being arbitrarily collapsed.
- Complete indeclinables, derived bases, conjugated forms, and declined forms remain distinguishable.
- Meaning evidence and confidence are visible.
- Forward generation, word decoding, and structured meaning search work without runtime AI.
- Runtime AI remains optional and outside the grammatical trust boundary.
- AI-assisted searches return only released candidates and expose their structured interpretation.
- No lack of dictionary attestation is treated as grammatical rejection.
- Unsupported or out-of-depth requests are reported honestly.
- The application can be rebuilt from archived sources and pinned software versions.

## Deferred Decisions

- Website repository and deployment platform.
- Production database and search engine.
- Whether semantic search begins with exact multilingual glosses, embeddings, or both.
- Which Indian languages accompany English in the first public release.
- Whether an experimental live generator should ever be exposed beside the fixed released corpus.

These decisions do not block the remaining analysis. The immediate requirement is to preserve derivational lineage in every new ledger.
