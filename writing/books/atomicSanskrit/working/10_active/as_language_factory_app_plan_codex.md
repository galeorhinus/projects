# Language Factory: Preliminary Application Plan

Started: 2026-09-15.

Status: Separate future product. The Yenpro appendix supplies the proof of concept; product analysis and implementation have not begun.

## Purpose

The **Language Factory** will let users create constructed languages similar to Yenpro by combining a selected sound inventory with a released set of Sanskrit's generative operations.

The application is distinct from the **Atomic Sanskrit Word Engine**:

- The **Word Engine** explores Sanskrit words, meanings, derivations, and grammatical forms.
- The **Language Factory** creates a new language by running a declared generative architecture through a different set of phonemes.

The Word Engine is analytical. The Language Factory is constructive.

## Core Experience

A user should be able to:

1. choose a known language's phoneme inventory or assemble one from phonemes used around the world;
2. map those phonemes to the sound distinctions required by the selected generative model;
3. declare permissible syllable shapes and adaptations for difficult sound sequences;
4. generate a starter vocabulary from selected semantic atoms and operations;
5. inspect how every generated word was formed;
6. adjust the sound map and regenerate the language consistently;
7. generate selected grammatical paradigms and sample sentences; and
8. save, version, export, and share the resulting language.

Yenpro should become the first complete example project and the principal test fixture.

## Product Boundary

The Language Factory must not mix constructed-language records with Sanskrit records.

- Every generated language belongs to its own project and version.
- Every project records the phoneme inventory, mapping, phonotactic adjustments, grammatical operations, and generation depth it uses.
- Generated forms do not enter the Sanskrit Word Engine's inventory or counts.
- A generated form is not presented as historically attested in any natural language.
- Selecting phonemes from a natural language does not claim that the resulting constructed language descends from, represents, or reconstructs that language.
- Users may alter pronunciation and surface form, but every result must retain a reproducible path through the selected architecture.

## Relationship to the Word Engine

The two applications may share infrastructure without sharing their records.

Reusable components include:

- the versioned operation and rule registry;
- derivation-path rendering;
- Devanagari, IAST, IPA, and internal normalization utilities;
- deterministic generation services;
- source and provenance display;
- model manifests and checksums; and
- graph, search, export, and audit components.

The Language Factory should consume a stable operation-model release through an explicit interface. It should not read the Word Engine's internal database tables directly or modify its research release.

## Project Manifest

Every constructed language needs a machine-readable manifest containing:

- project name and version;
- parent operation-model release;
- selected source phoneme inventories;
- complete working phoneme inventory;
- phoneme-to-sonomer mapping;
- permitted mergers, substitutions, and unresolved distinctions;
- syllable and scaffold rules;
- sound-sequence repair rules;
- selected semantic atoms and meanings;
- enabled derivational and grammatical operations;
- generation and compound-depth boundaries;
- script or transliteration choices;
- generated-record counts; and
- hashes of all inputs and outputs.

Changing the map or rules creates a new project version rather than silently changing existing words.

## Creation Workflow

### 1. Select Sounds

Begin with one of three routes:

- select the phoneme inventory associated with a documented language;
- combine phonemes from several documented inventories; or
- construct an inventory manually from the global catalog.

The interface should group sounds by place, manner, breath, voicing, nasality, and vowel properties. It should make gaps and mergers visible before generation begins.

### 2. Map the Architecture

Assign selected phonemes to the distinctions required by the operation model. The application should identify:

- distinctions with a direct match;
- distinctions represented through an approximation;
- several distinctions merged into one output;
- selected phonemes that remain unused; and
- required distinctions with no output yet assigned.

The user must resolve or explicitly accept every gap before producing a stable release.

### 3. Define Surface Rules

Specify what happens when generated sequences are difficult or prohibited in the selected sound system. Yenpuro's adaptation of Yenpro supplies the first model for this stage.

Rules must be ordered, deterministic, reversible where possible, and visible in each derivation.

### 4. Generate the Lexicon

Choose semantic atoms and operation families, then generate a bounded vocabulary. Begin with useful groups such as:

- movement and location;
- perception and knowledge;
- making and changing;
- people and relationships;
- objects and materials;
- qualities and states;
- time and number; and
- common particles and complete unchanging words.

Every entry should show its meaning, source atom, operations, intermediate forms, sound mapping, surface adjustments, and final form.

### 5. Generate Grammar and Sentences

Apply selected person, number, time, mood, and relation systems to the generated vocabulary. The application should then produce controlled sample sentences whose derivations remain fully inspectable.

### 6. Test and Publish

Run collision, pronounceability, ambiguity, coverage, and regeneration checks. Publish only when every output can be reproduced from the project manifest.

## Preliminary Architecture

Use a shared deterministic core with two isolated data domains:

1. **Operation-model releases:** read-only definitions inherited from the Sanskrit analysis.
2. **Constructed-language projects:** user-owned mappings, rules, generated records, and versions.

The application will also require:

- a curated global phoneme catalog;
- a visual sound-inventory editor;
- a mapping validator;
- an ordered surface-transformation engine;
- a bounded vocabulary generator;
- a collision and ambiguity analyzer;
- a project database and versioning layer; and
- export formats for lexicons, paradigms, manifests, and derivation graphs.

## AI Boundary

Language creation should remain deterministic. AI may suggest a phoneme inventory, propose semantic domains, explain a collision, or help a user name a generated concept. It may not silently change a phoneme map, grammatical operation, surface rule, or generated form.

Every published language must regenerate without AI from its project manifest and pinned operation model.

## First Implementable Release

The first release should reproduce Yenpro from a checked-in manifest. It should allow a user to:

1. inspect Yenpro's source sound inventory and mapping;
2. change one mapping;
3. regenerate a small controlled vocabulary;
4. compare the old and new forms;
5. inspect the complete path for each form; and
6. save the result as a new project version.

This establishes the product's central claim before adding a full global phoneme catalog or unrestricted user projects.

## Development Sequence

1. Convert the Yenpro appendix into a complete machine-readable reference manifest.
2. Identify which Word Engine operation definitions can become a stable shared library.
3. Define the constructed-language project schema and versioning rules.
4. Build the phoneme mapping and coverage validator.
5. Reproduce Yenpro deterministically from the manifest.
6. Add surface-sequence adaptation and comparison views.
7. Add bounded vocabulary and paradigm generation.
8. Add the global phoneme catalog and visual selector.
9. Add project persistence, export, sharing, and publication.
10. Test a second language configuration to prove that the implementation is not hard-coded to Yenpro.

## Acceptance Criteria

- Yenpro regenerates exactly from its checked-in manifest.
- Every generated word retains its source meaning and complete operation path.
- Every surface change identifies the rule that caused it.
- Mapping gaps and mergers remain visible.
- Project versions are immutable after publication.
- Constructed-language records never enter Sanskrit inventories or counts.
- A project can be rebuilt from its manifest without AI.
- A second sound inventory can use the same architecture without Yenpro-specific code.

## Supporting Records

- [Language Factory appendix](../../manuscript/as_3_05_language_factory.md)
- [Atomic Sanskrit Word Engine plan](as_word_engine_app_plan_codex.md)
- [Word Engine implementation plan](as_word_engine_preliminary_implementation_plan_codex.md)
- [Derivation record schema](../../analysis/generativity/derivation_record_schema.md)

## Resume Point

Begin by encoding Yenpro as a project manifest. Do not build the visual phoneme selector until that manifest regenerates the appendix's vocabulary and transformation paths exactly.
