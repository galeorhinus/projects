# Atomic Sanskrit Word Engine: Product Specification

Started: 2026-09-14.

Status: Initial product definition. The bounded analysis is complete; implementation begins with the release schema and compiler described in the [preliminary implementation plan](as_word_engine_preliminary_implementation_plan_codex.md).

## Audience

- A reader curious about what Sanskrit can generate from a धातुः.
- A Sanskrit student trying to understand how a known word was formed.
- A writer seeking candidate Sanskrit words for a meaning.
- A grammarian or reviewer auditing the rule and evidence behind a result.

The default interface must remain readable for an intelligent non-specialist. Sanskrit grammatical names should appear after a plain description of what the operation does.

## Home Screen

The first screen is the working application, not a marketing page. It presents three modes as tabs or a segmented control:

1. **Generate from a धातुः**
2. **Decode a word**
3. **Find a word for a meaning**

The current model version and analytical boundary remain available without dominating the workspace.

## Generate From a धातुः

### Inputs

- धातुः search by Devanagari, IAST, or meaning.
- Meaning selector when one atom has several meanings.
- Domain selector.
- Operation-family filters.
- Maximum depth up to the released model boundary.

### Results

- Total descendants within the selected boundary.
- Counts grouped by operation and form class.
- Searchable and paginated word list.
- Expandable derivation tree.
- Familiar and less familiar examples near the top.
- Complete path, meaning evidence, rules, and source links in a detail panel.

## Decode a Word

### Input

A Sanskrit form in Devanagari or a supported transliteration.

### Results

- Normalized form.
- Every matching word-meaning.
- Every supported derivational path.
- Source atom and meaning.
- Ordered operations and intermediate forms.
- Grammatical analysis for complete inflected forms.
- Clear notice when the result is ambiguous, outside the released depth, or unsupported.

## Find a Word for a Meaning

### Input

A short description such as “one who desires knowledge,” “absence of agency,” or “made predominantly from food.”

### Process

1. Search recorded source glosses and semantic tags.
2. Identify candidate atoms or nominal bases.
3. Identify requested relations such as agent, desire, causation, possession, state, descent, material, comparison, or negation.
4. Retrieve materialized candidates from the released derivation graph or construct a supported compound under the released relation and depth boundary.
5. Rank exact source meanings above compositional and context-dependent estimates.

### Results

- Candidate Sanskrit words.
- Literal compositional meaning.
- Why each candidate matches.
- Full derivation path.
- Meaning-evidence label.
- Alternatives when several constructions express related ideas.

### Deterministic and AI-Assisted Search

The ordinary meaning search must work without AI through searchable glosses, semantic tags, and selectors for relations such as agent, instrument, desire, causation, possession, state, descent, material, comparison, and negation.

An optional natural-language layer may translate an unrestricted request into a structured search containing core concepts, requested relations, and desired form class. It may then rank materialized candidates or request virtual compounds from the released deterministic relation model. It may not create or validate Sanskrit words.

The interface must show this structured interpretation so that a reader can correct, for example, “agent” to “instrument” or “desire” to “obligation.” If the AI service is unavailable, the structured search controls and all other application modes must continue to work.

## Result Language

Use Devanagari first and IAST as fallback. Show the internal SLP1 form only in an audit or developer view. Explain operations in ordinary language before giving technical labels.

Avoid claiming that a generated word was historically used merely because the grammar licenses it. Dictionary or corpus evidence may be displayed as additional information but is not the admission gate for the released generative inventory.

## Performance Requirements

- Never load the full dataset in the browser.
- Paginate large result families.
- Return the first useful results quickly while aggregate counts and deeper branches load separately.
- Cache common atoms and searches.
- Preserve stable result URLs for review and citation.

## Runtime Trust Boundary

The following are pregenerated before release:

- materialized Sanskrit forms and word-meanings;
- complete or reconstructible derivational paths;
- source and rule references;
- grammatical classifications;
- compositional meaning estimates;
- semantic tags and search indexes;
- optional embeddings used for similarity search.

The release also includes the canonical compound-member, verbal, and name-meaning inventories, supported relation and inflection definitions, depth limits, capacity formulas, and verified fixtures. It does not materialize trillions of formal compound slots, 408 million verbal cells, or 194 million name-form cells. Supported compounds and paradigms are generated deterministically on demand through the pinned engine, with their parent meanings, grammatical coordinates, and rule paths retained or reconstructed. The current compound model permits depth one and a bounded depth two; it does not expose unrestricted recursion. The current verbal model covers ten लौकिक लकाराः in कर्तरि प्रयोग and keeps वैदिक लेट् separate. The current name-form model covers eight relations and three number values, treats gender as an output attribute, and keeps agreement-driven additional genders separate.

Forward धातुः exploration, Sanskrit word decoding, derivation display, filters, structured meaning search, and on-demand compound generation are deterministic operations.

Runtime AI is an optional interface assistant. It may interpret, translate, explain, or rank a request. Every Sanskrit result must still resolve to a released record with a verifiable path. AI output that does not resolve to such a record must not appear as a Sanskrit candidate.

## Provenance View

Every result must expose:

- model release;
- count status;
- source and parent identities;
- ordered operations;
- rule references;
- verification status;
- source-defined or estimated meaning status.

For an on-demand compound, the view must also identify its relation, both parent meanings, compound depth, and whether the form is materialized or virtual. A virtual result must not be presented as dictionary-attested merely because the grammar generates it.

The default reader view may summarize this information. The audit view must retain it completely.

## First Implementable Release

The first application release should provide the forward धातुः explorer and exact word lookup against a frozen analytical model. Meaning-to-word search follows after the semantic tags and confidence ranking have been tested. This order tests the data architecture before introducing the least deterministic feature.
