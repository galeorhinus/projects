# Atomic Sanskrit Word Engine: Preliminary Implementation Plan

Started: 2026-09-15.

Status: Preliminary plan. The product name is selected; the production website stack remains open. The bounded generativity analysis is complete; application implementation has not begun.

## Selected Name

**Public name:** **Atomic Sanskrit Word Engine**

**Sanskrit identity:** **शब्दयन्त्रम् (*śabdayantram*)**

This pairing was selected on 2026-09-15. “Atomic Sanskrit” connects the application to the book and website. “Word Engine” tells a new visitor what the application does. **शब्दयन्त्रम् (*śabdayantram*)** gives the product a Sanskrit identity without requiring an unfamiliar Sanskrit term to carry the entire burden of explanation.

The Word Engine exposes Sanskrit's own word-generating architecture, derivational paths, and grammatical forms. **Language Factory** is a separate future application that will use selected phonemes from the world's languages to construct new languages modeled on the Yenpro experiment.

### Other Viable Names

1. **शब्दयन्त्रम् (*Śabdayantram*)**  
   Distinctive and structurally accurate, but less immediately intelligible to a first-time visitor.

2. **Atomic Sanskrit Explorer**  
   Accessible and expandable, but it does not identify generation as the application's central function.

3. **धातुयन्त्रम् (*Dhātuyantram*) — The Dhātu Engine**  
   Strong for forward generation from a semantic atom, but too narrow for reverse word analysis and meaning search.

4. **शब्दसृष्टिः (*Śabdasṛṣṭiḥ*) — Word Creation**  
   Memorable and expressive, but less precise about the application's analytical and audit functions.

Before publication, run a domain and trademark collision check. Use **Atomic Sanskrit Word Engine** as the public name and **AS Word Engine** as the internal shorthand.

## Product Purpose

Build a public application at `atomicsanskrit.org` that lets a reader:

1. choose a धातुः (*dhātuḥ*) meaning and follow the words generated from it;
2. enter a Sanskrit word and inspect every supported meaning and derivational path; and
3. describe a desired meaning and retrieve Sanskrit candidates supported by the released model.

The application should make Sanskrit's generative architecture inspectable. A result is useful only when the reader can see what it means, how it was formed, which operations produced it, and what evidence supports those operations.

## Starting Point

The research phase has already supplied:

- 2,634 reconciled semantic-atom meanings;
- 12,846,458 bounded शब्दार्थाः (*śabdārthāḥ*) before inflection;
- a separate boundary for 12,633,060 लौकिक (*laukika*) and 213,398 Vedic meanings;
- declared verb, noun, and unchanging-word categories;
- finite grammatical matrices yielding 602,707,133 लौकिक semantic grammatical cells;
- operation-specific ledgers, exclusions, overlaps, source records, and tests;
- a derivation-record schema;
- a product specification; and
- a pinned Vidyut 0.4.0 generation environment.

The analysis is ready, but it is not yet an application database. The records remain distributed across research ledgers. The first implementation task is therefore a release compiler, not a frontend.

## Release Boundary

Version 1 should expose the completed bounded model and nothing beyond it.

- Treat one word carrying two meanings as two शब्दार्थाः (*śabdārthāḥ*).
- Preserve alternative derivational paths instead of collapsing them.
- Keep लौकिक and Vedic records distinguishable.
- Generate supported verbal and nominal forms on demand rather than storing all 602,707,133 cells.
- Generate only the compound depths and relations admitted by the release.
- Do not require dictionary attestation when the released grammar licenses a generated meaning.
- Do not imply that a grammatically generated formation is historically common or corpus-attested.
- Reject only combinations excluded by the released rules or boundaries.
- Never present unrestricted recursive compounding as a finite inventory.

## Proposed Architecture

### 1. Research Layer

The existing analysis ledgers remain canonical and read-only. Application code must not modify them.

### 2. Release Compiler

A deterministic Python build converts the admitted ledgers into one versioned application release. It should:

- normalize every record to the derivation schema;
- assign stable word-meaning, operation, path, rule, and source identifiers;
- preserve Devanagari, IAST, and internal SLP1 forms;
- reconcile overlaps and exclusions exactly as the research reports do;
- build forward, reverse, semantic, and parent-child indexes;
- produce Parquet files for archival inspection;
- produce a portable SQLite release for local testing;
- produce import files for the production database; and
- write a manifest containing counts, boundaries, hashes, engine versions, and source versions.

The compiler must fail if its totals do not reconcile to the published analysis.

### 3. Production Data Store

Use PostgreSQL as the initial production assumption because the released inventory contains millions of word-meaning records and requires indexed filtering, pagination, and joins across derivational paths. Keep this choice provisional until the existing `atomicsanskrit.org` infrastructure is inspected.

Suggested indexes:

- exact Devanagari, IAST, and normalized-form lookup;
- धातुः and parent-record lookup;
- operation family and derivational depth;
- semantic tags and normalized gloss text;
- release, domain, evidence class, and count status; and
- compound members and grammatical coordinates.

### 4. Deterministic Generation Service

Use the pinned grammatical engine for operations that should be computed on request:

- verbal paradigms;
- noun relation-number paradigms;
- admitted bounded compounds; and
- regeneration of a stored derivational path for verification.

Every runtime result must identify the model release, inputs, operation sequence, grammatical coordinates, and rule path. Frequently requested results may be cached, but the cache is never canonical.

### 5. API

The first API should support:

- release metadata and boundaries;
- धातुः search and selection by meaning;
- descendants of a selected semantic atom;
- exact and normalized word lookup;
- retrieval of every meaning and path for one form;
- derivation-tree expansion;
- deterministic paradigm generation;
- filtered and paginated result families; and
- source and rule retrieval.

Meaning-to-word search can enter the API after the exact and structural paths are stable.

### 6. Frontend

The first screen should be the application workspace with three modes:

1. **Build from a धातुः**
2. **Decode a word**
3. **Find a word for a meaning**

Version 1 can launch with the first two modes. Each result should show Devanagari first, IAST as fallback, a plain-language meaning, and a compact derivational path. A detail view should expose the complete audit record.

## Implementation Phases

### Phase 0 — Repository and Infrastructure Audit

- Locate the source repository and deployment path for `atomicsanskrit.org`.
- Record its frontend framework, hosting platform, database access, authentication model, and release process.
- Decide whether the app lives in that repository or as a separately deployed service.
- Confirm that the selected public name has no material domain or trademark collision.

**Exit:** an architecture decision record identifies the repositories, deployment boundary, and chosen stack.

### Phase 1 — Freeze Release Schema 1

- Reconcile the current derivation schema with every ledger family.
- Define stable identifier rules.
- Define the release manifest and semantic-tag schemas.
- Mark fields that can be absent in historical ledgers.
- Add schema fixtures for homonyms, alternative paths, Vedic records, indeclinables, compounds, and excluded combinations.

**Exit:** schema validation passes against representative records from every operation family.

### Phase 2 — Build the Release Compiler

- Normalize the ledgers.
- Emit Parquet, SQLite, and production-import artifacts.
- Build indexes and aggregate counts.
- Generate a signed or hashed release manifest.
- Reconcile every published subtotal.
- Regenerate a sample from each operation family through Vidyut.

**Exit:** one command builds a complete, internally consistent release from the archived analysis.

### Phase 3 — Build a Local Query Prototype

- Implement command-line queries for धातुः descendants, word decoding, and path inspection.
- Test response shape and pagination before building an HTTP service.
- Measure index size, query latency, and memory requirements with the complete release.

**Exit:** the two primary workflows work locally against the full inventory.

### Phase 4 — Build the Read-Only API

- Add versioned endpoints.
- Enforce release boundaries in every query.
- Add deterministic paradigm and bounded-compound generation.
- Add caching, rate limits, structured errors, and stable result URLs.
- Expose source and rule provenance.

**Exit:** API tests reproduce the local query results and reject unsupported depth or operations explicitly.

### Phase 5 — Build the First Public Interface

- Implement **Build from a धातुः**.
- Implement **Decode a word**.
- Add the derivation tree and audit panel.
- Add filters for meaning, domain, operation family, evidence class, and depth.
- Test large families without loading the full result set into the browser.
- Verify desktop and mobile layouts with browser screenshots.

**Exit:** a reviewer can trace a familiar word and an unfamiliar generated word back to their semantic atoms and sources.

### Phase 6 — Add Meaning-to-Word Search

- Normalize and tag source and generated meanings.
- Build deterministic concept and relation filters.
- Add full-text search and evaluate optional semantic embeddings.
- Add an optional AI query interpreter only after deterministic search works.
- Restrict AI output to released candidates or deterministically generated bounded compounds.

**Exit:** a natural-language request returns explainable Sanskrit candidates without placing AI inside the grammatical trust boundary.

### Phase 7 — Production Hardening and Release

- Run count, determinism, regression, load, accessibility, and security tests.
- Publish release notes and model boundaries.
- Provide a downloadable release manifest and citation link.
- Add monitoring, backups, and rollback procedures.
- Deploy the versioned application at `atomicsanskrit.org`.

**Exit:** the public release can be reconstructed from its archived inputs and pinned software.

## Testing Strategy

The application needs five independent test layers:

1. **Research reconciliation:** exported totals equal the accepted analysis totals.
2. **Schema validation:** every admitted record satisfies its form-class requirements.
3. **Derivational verification:** sampled paths regenerate through the pinned engine.
4. **Query correctness:** forward and reverse queries preserve meanings, homonyms, and alternative paths.
5. **Product verification:** browser tests confirm pagination, filters, stable URLs, responsive layout, and readable Devanagari.

Golden fixtures should include familiar formations such as **चन्द्रयान (*Candrayāna*)** alongside less familiar formations that demonstrate the same operations.

## AI Boundary

The core application must work without AI. Pregenerate forms, paths, meanings, tags, indexes, and optional embeddings. Use deterministic code at runtime for database retrieval, graph traversal, bounded compounds, and grammatical paradigms.

AI may later interpret a user's unrestricted meaning request, translate it into structured concepts, explain an existing path, or rank released candidates. It may not invent or validate a Sanskrit result. If AI is unavailable, all exact, structural, and filtered searches must continue to work.

## Principal Risks

- Earlier ledgers may not all carry the complete derivation schema and will need deterministic normalization.
- A single surface form can represent several meanings and paths; careless deduplication would corrupt the model.
- The 602,707,133 grammatical cells are a capacity, not a table to materialize.
- Compound recursion can create misleading totals unless every request carries a visible depth boundary.
- Meaning search can overstate certainty unless source-defined, generated, context-dependent, and experimental meanings remain distinct.
- Devanagari normalization and transliteration variants require dedicated test fixtures.
- A public interface can make a generated form look attested unless evidence labels remain visible.

## First Development Milestone

Do not begin with screens. Build a command that produces a versioned release directory containing:

```text
release/<version>/
  manifest.json
  word_meanings.parquet
  forms.parquet
  derivation_edges.parquet
  operations.parquet
  rules.parquet
  sources.parquet
  semantic_tags.parquet
  atomic_sanskrit.sqlite
  checksums.sha256
```

Then prove three queries against the complete release:

1. list every released descendant of one selected धातुः meaning;
2. return every supported meaning and derivation for one entered Sanskrit form; and
3. regenerate and explain one selected path through the pinned engine.

Once those three operations work, the frontend becomes a controlled presentation problem rather than a second attempt to organize the research.

## Canonical Supporting Documents

- [Word Engine application plan](as_word_engine_app_plan_codex.md)
- [Word Engine product specification](as_word_engine_product_spec_codex.md)
- [Separate Language Factory plan](as_language_factory_app_plan_codex.md)
- [Derivation record schema](../../analysis/generativity/derivation_record_schema.md)
- [Generativity analysis](../../analysis/generativity/README.md)
- [Admission standard](../../analysis/generativity/admission_standard.md)
- [Six-pass capacity synthesis](../../analysis/generativity/results/generativity_six_pass_synthesis.md)
- [Publication count cascade](../../analysis/generativity/results/publication_capacity_cascade.md)
- [Language Factory appendix](../../manuscript/as_3_05_language_factory.md)

## Resume Point

When development begins, start with Phase 0 and Phase 1. The first code artifact should be the release-schema validator, followed by the release compiler. Do not begin runtime generation or interface work until the compiler reproduces all accepted totals from the current ledgers.
