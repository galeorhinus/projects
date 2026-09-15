# Generativity Pilot: Findings and Next Work

Date: 2026-09-12. Scope: the named-operation inventory and a small generator pilot. No manuscript or endnote prose was changed.

## What Is Ready

The initial [operation inventory](operations.csv) contains 34 entries covering base identity, prefixing, verbal derivation, primary and secondary nominal derivation, feminine formation, indeclinables, inflection, and compounding. Fourteen operation entries are explicitly deferred. This is a working inventory, not a claim to have listed every Sanskrit affix. The later [engine census](results/operation_inventory.md) records all 304 derivational identifiers exposed by the pinned software without treating them as eligible formations or as a multiplier.

The [pilot report](results/pilot.md) contains 28 expectation checks. All match after the two input corrections documented below. These are example checks, including controls, not 28 independent words or a general proof of the generator's completeness.

Every generated example retains its source entry where applicable, intended meaning, requested operation, exact input, expected and actual output, and derivation history in [the detailed results](results/pilot.json). Source snapshots, URLs, retrieval dates, and SHA-256 checksums are retained in the evidence archive's manifest.

## The Counting Separation Works

Author clarification after the first pilot: **the primary count is of words distinguished by lexical meaning, not of unique spellings.** The earlier report's emphasis on the 18 spellings was misplaced. That measurement remains a technical observation, not a reduction of the word count.

One पाचक (*pācaka*) base in its agent meaning, used in the masculine, fills all **24 case-number cells** in the pilot. All 24 belong in the separate grammatical expansion. Their 18 distinct spellings do not erase the grammatical distinctions represented by the other cells. Additional lexical meanings, where established, would be recorded separately before inflection.

One भू (*bhū*) base produces **nine present-tense parasmaipada forms** in the separate conjugation sample. They remain forms of one lexical verb in this analysis.

The pilot also keeps कृत्वा (*kṛtvā*), प्रकृत्य (*prakṛtya*), and कर्तुम् (*kartum*) outside the noun-declension count. Their derivation is recorded without attaching case-number endings.

## Source Identity Matters

Two entries share the citation spelling `pA\` but carry different meanings and belong to different classes:

| Source code | Meaning | Present form |
|---|---|---|
| 01.1074 | Drinking | पिबति (*pibati*) |
| 02.0051 | Protecting | पाति (*pāti*) |

Merging those inputs by spelling would erase a meaningful distinction. Conversely, retaining every source row without reconciliation can preserve duplicate records. Keep the source identity until the entries have been compared.

The pinned Vidyut loader returns 2,229 entries. The book's input has 2,168 active entries. The pilot uses the pinned engine's entries directly and does not replace the book's input inventory with them.

The [candidate crosswalk](results/source_crosswalk.csv) accounts for all 2,168 local entries:

| Match category | Local entries |
|---|---:|
| Same identifier and citation form | 1,773 |
| Unique same-class citation candidate at another identifier | 41 |
| Multiple same-class citation candidates without an exact identifier match | 4 |
| No exact same-class citation candidate | 350 |

Fifty rows share a selected target with another local row. These are flagged, not merged. Even the strongest match category is a source-alignment candidate, not a completed audit of meanings. The 350 unmatched rows are not evidence of nonexistent or invalid Sanskrit bases; citation conventions and inventory differences must be examined.

## Two Pilot Corrections

1. The initial expected desiderative base was `cikIrz`. The generator returns `cikIrza`, retaining the suffix vowel. Inspection of the derivation and the separate चिकीर्षति (*cikīrṣati*) check support that representation. The fixture now records the returned base, with a note explaining the vowel. This is a correction to the pilot's expectation, not a change to a linguistic claim in the book.
2. The initial कुन्ती (*Kuntī*) input was an untyped nominal string. It produced no output for ढक् (*ḍhak*). Declaring its feminine-derived status using the engine's `nyap` constructor produces कौन्तेय (*kaunteya*). The commentary to 4.1.120 explicitly refers to feminine-suffix-bearing bases; the pinned implementation's examples use the same metadata for विनता (*Vinatā*). Both typed and untyped cases are retained, so the missing metadata remains a visible control.

The second correction is particularly important: an empty output can mean that the input is incomplete. It cannot automatically mean that Sanskrit disallows the formation.

## Rule Checks and Software Limits

The archived primary commentary was consulted for the principal meanings and conditions of the pilot: causation (3.1.26), desire (3.1.7), nominal desire (3.1.8-9), repeated or intense action (3.1.22), agency (3.1.133), action nouns (3.3.18 and 3.3.115), prior action (3.4.21), purpose (3.3.10), offspring formation (4.1.120), and abstract quality (5.1.119). The source pages sometimes give the exact familiar example and sometimes establish the general operation. The report does not label every generated example as independently quoted from a source.

The Sanskrit Documents compilation has some inconsistent numeric headings. For example, the page reached through `1.4.59.htm` contains the commentary for 1.4.60, and the abstract-quality page mixes 5.1.118 and 5.1.119 headings. Preserve the snapshots unchanged. Identify a passage by its actual sutra wording and commentary, and use the separately archived `sutrapatha.tsv` for the engine's rule-code mapping. Before publication, reconcile any locator used in a citation; a filename is not sufficient verification.

The installed Python interface accepts a base and an affix for primary and secondary nominal derivation, but exposes no `artha` argument on those two constructors. That prevents this pilot from selecting a specific semantic relation through those calls. The intended relation is currently recorded and checked externally for the selected examples. This limitation must be addressed before running general secondary derivation, where the same suffix can serve different relations.

The engine also returns both करोति (*karoti*) and कुरुते (*kurute*) when no pada is specified for the chosen कृ (*kṛ*) entry. That establishes two generated forms, not free interchangeability in every sentence. Their applicability conditions still matter.

## Evidence and Reproducibility

- Python package: `vidyut==0.4.0`, installed only in `build/generativity-venv`.
- Matching source tag: `py-0.4.0`, commit `f3ba4167d40eebc4b3023d24e66867aa6a8cdb32`.
- Archive: `working/40_reference/sources/archive/documents/generativity-pilot/`.
- Archive manifest: 45 snapshots, comprising eight software/data documents and 37 primary grammar pages. Downloaded pages for deferred operations are retained for later review, not marked fully verified.
- Regression suite: nine tests pass, including all 28 pilot cases, spelling deduplication, independent inflection counts, homonym preservation, and crosswalk integrity.
- Existing `generative_wordspace.py` and the manuscript's 20,942,880-slot illustration remain untouched.

## Next Work

1. Review the unmatched and ambiguous source entries and shared targets. Distinguish citation changes from different lexical entries before importing meanings.
2. Establish the full named-affix list for the first enumeration. The initial family inventory must expand into affix-by-affix applicability records, including replacements, optionality, and output gender where relevant.
3. Evaluate an interface that exposes semantic conditions for nominal derivation, or implement an explicitly reviewed eligibility layer around the pinned generator. Do not bypass this by multiplying all bases by all suffixes.
4. Expand the pilot to deferred families and negative cases. Then enumerate the agreed bounded set of verbal, nominal, and indeclinable formations, followed by a separate inflection run.

No new grand total should enter the book until these counts have been produced and reviewed.
