# Sanskrit Generativity: Bases First, Inflection Separately

Started: 2026-09-12.

**Current, 2026-09-15:** The completed [six-pass synthesis](../../analysis/generativity/results/generativity_six_pass_synthesis.md) reconciles the लौकिक grammatical branches. **4,540,848 action meanings** occupy **408,676,320** declared verb cells; **8,084,287 name meanings** occupy **194,022,888** relation-number cells; and **7,925 complete unchanging meanings** remain single cells. The resulting capacity is **602,707,133 semantic grammatical cells**. This replaces the **12,633,060 लौकिक lexical inputs** with their grammatical views rather than adding the two units. The **213,398 Vedic meanings** remain a separate lexical inventory. The [publication cascade](../../analysis/generativity/results/publication_capacity_cascade.md) follows the full path from **2,634** semantic-atom meanings through **12,846,458** bounded word-meanings to the लौकिक grammatical result. The approved wording is now deployed in Chapter 0, Chapter 12, and their [shared endnote](../../analysis/generativity/results/generativity_manuscript_proposal.md). Unrestricted recursive compounding remains outside the headline.

The [publication reporting ladder](../../analysis/generativity/results/publication_reporting_ladder.md) records how each operation enlarges the subtotal. The [stage graph](../../analysis/generativity/results/generation_stage_graph.json) stores the same sequence as machine-readable nodes and edges. It distinguishes lexical atoms, derived bases, complete indeclinables, and future inflected words so the eventual figure cannot confuse lexical capacity with grammatical cells.

Status: The counting method, source crosswalk, base-meaning reconciliation, verbal derivation layers, full engine-identifier census, ordinary and Vaidika कृदन्त layers, broad and conditioned तद्धित layers, source-demonstrated and generalized lexical स्त्रीप्रत्यय formations, the first नामधातुः layer, one bounded नञ् layer, comparative and superlative relations, one depth-limited source समास layer, one additional operation over its nominal outputs, the symbolic समास capacity model, the लौकिक कर्तरि तिङन्त capacity model, and the लौकिक नामरूप relation-number model are complete within their declared boundaries. The 12,846,458 combined result remains a bounded materialized research subtotal, not a complete Sanskrit vocabulary total or a replacement manuscript claim. Major uncounted layers remain listed in the reporting ladder.

**Current review:** The [current research count](../../analysis/generativity/results/current_research_count.md) records every approved reconciliation. The [eight-pass consolidation](../../analysis/generativity/results/eight_pass_consolidation.md) preserves the complete earlier review. The new [operation inventory](../../analysis/generativity/results/operation_inventory.md) separates a suffix identifier from a meaning-bearing operation and from base-level eligibility. Inflection does not enter any subtotal.

Read the [pilot findings](../../analysis/generativity/pilot_findings.md) and [generated example report](../../analysis/generativity/results/pilot.md). Reproduction commands are in the [analysis README](../../analysis/generativity/README.md).

## Purpose

Count the formations that Sanskrit can generate from a declared inventory of धातवः (*dhātavaḥ*) and प्रातिपदिकानि (*prātipadikāni*). Then measure the additional तिङन्तानि (*tiṅantāni*), conjugated forms, and सुबन्तानि (*subantāni*), declined forms, as separate operations.

The explanation should let a reader distinguish creating a concept from expressing its पुरुषः (*puruṣaḥ*), person; वचनम् (*vacanam*), number; विभक्तिः (*vibhaktiḥ*), case; or लकारः (*lakāraḥ*), tense or mood. The final presentation should give separate totals rather than conceal these stages inside one large multiplication.

The user has authorized this analysis, not automatic changes to manuscript prose. Leave the existing calculation, Chapter 0, Chapter 12, and their endnote unchanged until replacement findings and wording have been reviewed.

### Counting Unit: Distinct Word-Meanings

Author-approved formulation: **We count each distinct word-meaning, not each source entry.** One word with two distinct meanings contributes two entries. The same word-meaning recorded in several sources contributes one. Different words with similar meanings remain separate.

Author clarification, 2026-09-12: the primary unit is a word with a distinct lexical meaning, not a unique spelling. The earlier emphasis on deduplicating written forms was misplaced for this purpose.

Keep separate meanings of the same written form as separate entries. Two synonyms in a gloss do not automatically establish two meanings; nor does each contextual use create another entry. Each meaning distinction needs a source or an explicit grammatical derivation. Different words expressing a similar meaning also remain distinct words.

Count these meaning-bearing entries before inflection. Then count the applicable person-number and case-number combinations separately, preserving different grammatical functions even when their written forms coincide. Spelling comparisons are internal diagnostics only; they must not reduce either the semantic count or the grammatical-cell count.

For alternative readings, retain each distinct meaning with the source that records it. If one reading lists affection and protection and another lists affection and living, affection contributes once: three candidate word-meanings, not four. This research inventory does not imply that every commentator accepted every reading. Keep explicitly prefixed meanings for the prefix stage. A partial list can contribute its supported members without assigning a number to an unspecified remainder.

## What We Have Now

The existing script, `analysis/generativity/generative_wordspace.py`, reproduces:

| Grid | Calculation | Slots |
|---|---|---:|
| Finite verbs | 2,168 x 23 x 10 x 9 x 2 | 8,975,520 |
| Nominals | 2,168 x 23 x 10 x 24 | 11,967,360 |
| Combined | Sum of the two grids | 20,942,880 |

The ten nominal derivations are unnamed placeholders. The prefix axis counts 22 printed labels plus an unprefixed state, including conditioned forms of the same underlying prefix. The calculation does not test the admissibility of each combination, deduplicate the results, or enumerate successive derivations.

Preserve this script as the reproducible record behind the existing endnote. Build the new analysis alongside it.

## Initial Inventory Audit

Run from the book root:

```sh
python3 analysis/generativity/audit_inventory.py
python3 -m unittest discover -s tests -p 'test_generative_inventory.py'
```

Source: `analysis/dhatupatha/data/dhatupatha.csv`.

Source SHA-256: `e491d6cd8c68e3fe455f57098ba6d6ad2762cf0882a74dd585aa45e636eb9d86`.

| Measurement | Count |
|---|---:|
| Active source entries with individual identifiers | 2,168 |
| Commented rows, excluded by the existing analysis | 67 |
| Distinct citation spellings among active entries | 1,910 |
| Distinct spellings after the existing normalization | 1,518 |

These measure different things. The familiar 2,168 is the active-entry count, not the number of distinct normalized spellings. Multiple entries may share a spelling while differing in meaning, conjugational class, or other grammatical properties. Conversely, different entries may ultimately represent the same lexical base. Neither decision can be made by comparing spellings alone.

The current CSV provides class, position, and citation form. It does not supply the full meaning and applicability information required for the new count. Enrich entries from identified sources; retain the original identifier throughout. The existing normalization was designed for structural analysis. It can help locate candidate matches, but must not determine lexical or semantic identity.

The audit prints both input and normalizer checksums so these measurements can be reproduced after future changes.

## Four Separate Results

### 1. धातवः (*Dhātavaḥ*): Verbal Bases

Start with source entries, resolve lexical identities where the evidence permits, and report unresolved identities separately. Count धातवः (*dhātavaḥ*) without an उपसर्गः (*upasargaḥ*) first, then valid formations with an उपसर्गः (*upasargaḥ*), followed by derived verbal formations.

Include णिजन्त (*ṇijanta*), causative; सन्नन्त (*sannanta*), desiderative; यङन्त (*yaṅanta*), repeated or intensive; and नामधातुः (*nāmadhātuḥ*), noun-derived verbal, operations in separate subtotals. These are operation families, not multipliers that automatically apply to every धातुः (*dhātuḥ*). Record the order of उपसर्गाः (*upasargāḥ*) and the rule-defined order of derivation. Count a meaning-bearing धातुः (*dhātuḥ*) once even when its conjugation uses several different stems.

For the initial bounded run, allow no prefix or one underlying prefix and at most one named verbal-derivation operation. Evaluate combinations in their appropriate grammatical order. Later runs can extend prefix sequences and derivational depth, with separate results for each expansion.

### 2. प्रातिपदिकानि (*Prātipadikāni*): Nominal Bases

Replace the ten placeholders with an explicit inventory of प्रत्ययाः (*pratyayāḥ*), affixes, and their meanings, applicability conditions, and rule references.

Separate कृदन्तानि (*kṛdantāni*), primary formations from धातवः (*dhātavaḥ*); तद्धितान्तानि (*taddhitāntāni*), secondary formations from प्रातिपदिकानि (*prātipadikāni*); and the source nominal inventory. A noun such as a personal name cannot appear as an input merely because its derived form is familiar: its source must be recorded.

Keep nouns, adjectives, and participial uses identifiable. Count separately established lexical meanings even when their forms coincide. A grammatical role or a different English gloss alone does not establish a new lexical meaning. Report a combined nominal-entry total alongside any noun-only subtotal.

This is where the formations discussed with the author belong: action and agent nouns, offspring names, abstract qualities expressed through प्रत्ययाः (*pratyayāḥ*) such as *tva*, and relational adjectives. A स्त्रीप्रत्ययः (*strīpratyayaḥ*) is another recorded operation. It does not authorize an automatic count across all three लिङ्गानि (*liṅgāni*), genders, for every noun.

For the initial run, enumerate one कृदन्तम् (*kṛdantam*) from each admitted धातुः (*dhātuḥ*); separately enumerate one तद्धितान्तम् (*taddhitāntam*) from a fixed, sourced set of प्रातिपदिकानि (*prātipadikāni*). Test selected कृदन्त-to-तद्धितान्त chains in a later, explicitly bounded run.

### 3. अव्ययानि (*Avyayāni*): Indeclinable Derived Forms

Give formations such as ktva, lyap, and tumun their own count. They derive from verbal bases but do not receive the noun case-number expansion. Record applicable replacements and environments rather than counting alternative grammatical labels as independent outputs by default.

### 4. तिङन्तानि and सुबन्तानि (*Tiṅantāni and Subantāni*): Inflected Forms

Only after establishing the admitted bases, generate तिङन्तानि (*tiṅantāni*) and सुबन्तानि (*subantāni*).

For तिङन्तानि (*tiṅantāni*), record लकारः (*lakāraḥ*), tense or mood; पुरुषः (*puruṣaḥ*), person; वचनम् (*vacanam*), number; पदम् (*padam*); and प्रयोगः (*prayogaḥ*), construction. Distinguish कर्तरि (*kartari*), कर्मणि (*karmaṇi*), and भावे (*bhāve*) प्रयोगाः (*prayogāḥ*) from the परस्मैपदम् (*parasmaipadam*) and आत्मनेपदम् (*ātmanepadam*) series. Do not count every tense stem as a new lexical verb.

For सुबन्तानि (*subantāni*), record permitted लिङ्गम् (*liṅgam*), gender; declensional behavior; वचनम् (*vacanam*), number; and विभक्तिः (*vibhaktiḥ*), case. The familiar 24-cell teaching table includes सम्बोधनम् (*sambodhanam*), the vocative, alongside the seven case series. Count its grammatical cells separately from distinct output spellings: several cells can share one spelling. Inherently plural, gender-restricted, and other restricted bases need their own applicability records.

The main results should show the number of meaning-bearing verbal and nominal entries, followed by their grammatical expansions. Distinct-spelling measurements may remain in technical diagnostics but are not a measure of vocabulary. Do not collapse grammatical cells because their spellings match, or add the base count to its inflected expansion as though they were independent populations.

## Counting Rules

1. **Declare the scope.** Start with a bounded laukika run. Keep Vedic-only formations and accent-sensitive distinctions in a separately specified extension. A bounded run is not a census of everything Sanskrit can ever express.
2. **Retain meaning where a rule requires it.** Record an operation's intended relation, such as offspring, possession, or causation. An affix list alone is insufficient input.
3. **Count distinct word-meanings, not source entries or spellings.** Preserve word, meaning, and source identifiers through derivation. One word with two distinct meanings contributes two entries. Several sources documenting the same word-meaning contribute one. Different words with similar meanings remain separate. String equality and English-gloss equality cannot settle lexical identity.
4. **Separate rules from software coverage.** A generator returning no result may indicate an unsupported operation rather than a prohibited formation. Distinguish generated, source-verified, rule-excluded, unsupported, and unresolved cases.
5. **Do not multiply by variants blindly.** Optional outputs and conditioned substitutions retain their relationship to the same input and meaning. A spelling variant alone does not create a new meaning-bearing entry.
6. **Bound recursion.** Each run states its prefix inventory, maximum prefix sequence length, permitted derivation chains, and nominal-input inventory. Compounding belongs in its own bounded experiment. Otherwise the nominal inventory has no declared stopping point.
7. **Preserve the evidence.** Each accepted formation needs its input identity, operation, semantic condition, output, rule trail or source locator, and verification status. Store source URLs and snapshots using the existing source-registry workflow.
8. **Do not call the existing grid a lower bound.** Omitting some operations does not compensate for including invalid combinations. A future minimum must be built from individually supported, deduplicated results under the declared counting unit.

The first **नञ्-समासः (*nañ-samāsaḥ*)** pass is complete. It expresses one relation, “not X” or “absence of X,” over the current bounded nominal inventory. The surface alternation between अ- and अन्- belongs to generation and does not create two multipliers. Other traditional नञ् meanings remain outside the count unless their eligibility can be established as separate operations.

## Execution Passes

| Pass | Work | Deliverable | Status |
|---|---|---|---|
| 1 | Define units and audit existing data | This document and reproducible inventory audit | Complete for the declared base inventory; separately scoped lexical questions remain recorded |
| 2 | Inventory derivations and source inputs | Named operation tables, source crosswalk, eligibility fields | Full 304-identifier engine census complete; all 175 तद्धित identifiers now carry a later-pass disposition; narrower semantic eligibility remains where required |
| 3 | Validate a representative pilot | Small reviewed derivation set covering each operation family and known restrictions | 28 form checks pass; author accepted the 28-entry semantic sample; deferred families and wider eligibility testing remain |
| 4 | Enumerate bases within the declared scope | Separate verb, nominal, and indeclinable counts with coverage report | Materialized lexical layers complete at 12,846,458 word-meanings; symbolic समास capacity complete at depths one and two without adding those slots to the subtotal |
| 5 | Generate inflections from admitted bases | Separate conjugation and declension counts; repeated-spelling analysis | लौकिक कर्तरि तिङन्त and नामरूप 8 × 3 capacities complete within their declared boundaries |
| 6 | Prepare publication findings | Reproducible report and proposed Chapter 0/12/endnote replacements | Pending author review |

The pilot should include regular and irregular bases, identical spellings with different source entries, one-pada and two-pada cases, prefix-conditioned behavior, blocked combinations, nominal gender restrictions, and optional outputs. Familiar examples such as gam, kr, pac, Kunti-to-Kaunteya, and abstract tva formations are starting tests, not a sufficient test suite by themselves.

## Implementation Direction

Evaluate an established grammatical generator before writing new derivational logic. Vidyut is a candidate: its official repository provides Sanskrit word generation and Python bindings. Its coverage and handling of semantic conditions must be tested against the pilot; this document does not assume complete grammatical coverage.

Record a pinned version or commit, data checksums, run configuration, and coverage gaps. Keep generated results in `analysis/generativity/`, with scripts producing the summary tables from detailed records. Vidyut 0.4.0 is installed in an isolated build environment; its corresponding source snapshot and input data are archived. The Python nominal-derivation constructors do not expose semantic-condition arguments, so the broad तद्धित pass admits inputs through separately sourced semantic-operation records before asking the engine to construct their forms.

Official source consulted 2026-09-12: [Ambuda's Vidyut repository](https://github.com/ambuda-org/vidyut). This URL supports the implementation candidate, not any linguistic total. Archive the exact implementation and documentation version when selected.

Existing input provenance: [sanskrit/vyakarana](https://github.com/sanskrit/vyakarana), as documented in `analysis/dhatupatha/README.md`. The local checksum above identifies the input actually audited; no fresh equivalence with the current remote data is claimed.

## Current Boundary

The identity-reconciliation review is complete at **2,634** provisional base-meaning assignments. A separate current dataset preserves all 2,741 source-assignment rows; one grammatical-metadata row and one unsupported source-reading row remain available outside the lexical subtotal. The full engine census contains 304 derivational identifiers. Every identifier remains outside a count until its meaning and eligibility have been established; the completed ledgers admit only classified operations with explicit meanings.

The first bounded verbal ledger contributes **15,156** meanings including the original bases. Source-level prefix restrictions and enrichments yield **52,567** one-prefix meanings. One prefix plus one सनादि adds **250,040**; the second णिच् adds **522** true चरादिगण causatives; and the declared two-position उपसर्ग experiment adds **1,051,340**. Aṣṭādhyāyī 1.4.80 places the prefixes before the धातुः in लौकिक use, and 6.4.96 expressly recognizes a two-prefix environment. The experiment does not turn two into the grammar's maximum. The first six passes then add **29,996** direct कृदन्त meanings, producing **1,399,621**.

The second six passes add **7,902** अव्यय meanings; classify all 87 deferred ordinary कृत्प्रत्यय identifiers without counting the classification itself; add **25,703** selected conditioned कृदन्त meanings; add **598,606** कृदन्त meanings from one-उपसर्गः inputs; add **142,882** from admitted सनादि-derived inputs; and add a seven-entry तद्धित pilot. The [twelve-pass report](../../analysis/generativity/results/twelve_pass_expansion_summary.md) reconciles **2,174,721 word-meanings under laukika generation mode**. No row is removed merely because a dictionary or corpus lacks it.

Eleven meanings in the shared base inventory are documented as Vedic-only. Their 8,660 base-and-descendant rows do not mix with other sources, so the [domain audit](../../analysis/generativity/results/domain_boundary_audit.md) moves them cleanly to the Vaidika side and reports **2,166,061** as the bounded laukika subtotal before broad nominal expansion. The completed `is_chandasi=True` passes add 204,738 Vaidika-specific word-meanings, producing a bounded Vaidika subtotal of **213,398** and an intermediate combined subtotal of **2,379,459**.

The next six passes derive a 794,078-meaning लौकिक nominal input inventory from the completed कृदन्त ledgers and five declared pilot nouns. All 175 pinned तद्धित identifiers receive a disposition, but only त्व and तल् for state or defining quality, मतुप् for possession, and three named ढक् descent examples enter the count. The resulting ledger contains **2,382,237** तद्धित word-meanings. Seven already belonged to the pilot, so the new layer adds **2,382,230** and raises the [combined bounded subtotal](../../analysis/generativity/results/taddhita_reconciliation.md) to **4,761,689**.

The next conditioned pass reads literal meaning-bearing examples from the eight pinned Kāśikā test files covering Aṣṭādhyāyī 4.1-5.4. It extracts 1,047 positive assertions, collapses them into 1,010 unique base-context-suffix relations, and verifies 975 through the unrestricted Python binding. The 35 mismatches remain outside the count. The [six-pass conditioned report](../../analysis/generativity/results/conditioned_taddhita_six_pass_summary.md) raises the combined bounded subtotal to **4,762,664** without treating the conditioned suffixes as universal multipliers.

The स्त्रीप्रत्यय pass inventories seven suffix identifiers and extracts 66 active assertions from the pinned Kāśikā 4.1 tests. These collapse to 65 nominal inputs. Vidyut's generic Python path verifies 50 actual suffix-bearing feminine derivations; five already-feminine inputs merely decline, and ten source constructions require metadata that the generic constructor loses. The [six-pass स्त्रीप्रत्यय report](../../analysis/generativity/results/stri_six_pass_summary.md) therefore adds 50 word-meanings and raises the combined bounded subtotal to **4,762,714**. It does not multiply grammatical gender across the nominal inventory.

The नामधातुः pass separates four productive relations under 3.1.8-3.1.11 from the named and conditioned relations under 3.1.12-3.1.21. The productive layer adds **3,176,312** meanings, while forty active source-demonstrated relations add another **40**. All candidates generate through pinned Vidyut 0.4.0, raising the [combined bounded subtotal](../../analysis/generativity/results/namadhatu_reconciliation.md) to **7,939,066**. Every new row is a derived verbal base; finite तिङन्त forms remain outside the count.

The नञ् pass applies one negative relation to the current nominal inventory: **ज्ञान (jñāna)** can become **अज्ञान (ajñāna)**, while **कर्तृत्व (kartṛtva)** can become **अकर्तृत्व (akartṛtva)**. The 794,078 earlier nominal meanings, 2,382,237 broad तद्धित meanings, 975 conditioned तद्धित meanings, and 50 feminine meanings provide **3,177,340** eligible inputs. One new meaning per input raises the [combined bounded subtotal](../../analysis/generativity/results/nan_reconciliation.md) to **11,116,406**. The two surface outcomes, अ- before a consonant and अन्- before a vowel, do not double the count. Recursive negation, other compounds, and inflection remain outside it.

The suffix-operation pass then groups all 175 तद्धित identifiers by their semantic work and distinguishes grammatical operations from the endings visible in finished words. It recovers 24 meaning-conditioned relations encoded through local source helpers or constructed inputs and verifies all 24 through Vidyut 0.4.0. Two relations reproduce one source-recorded output but not a second optional variant; each still contributes one verified word-meaning. The [six-pass suffix report](../../analysis/generativity/results/suffix_operation_six_pass_summary.md) raises the combined bounded subtotal to **11,116,430**.

The next pass returns the 292 positive plain source assertions to their governing rules. Forty-four occur only in ignored tests and remain outside the count. The 248 active assertions produce 249 semantic rows because **मूल्य (mūlya)** carries two rule-defined meanings. Four repeated assertions collapse, leaving 245 relations; Vidyut reproduces every one. Nine already occur in earlier तद्धित ledgers. The [plain तद्धित source report](../../analysis/generativity/results/plain_taddhita_six_pass_summary.md) therefore adds **236 word-meanings**: 197 nominal bases and 39 complete indeclinables. The combined bounded subtotal becomes **11,116,666**.

The next six passes classify all 57 recovered तद्धित semantic families by whether the present nominal metadata can satisfy their governing conditions. Comparative and superlative proceed through the two securely general paths. Rules 5.3.55 and 5.3.57 admit तमप् and तरप् across all 794,078 declared nominal meanings when comparison is intended. Rule 5.3.58 limits इष्ठन् and ईयसुन् to गुणवचन inputs; the present English semantic labels do not independently establish that traditional category, so those paths remain deferred. Vidyut generates all **1,588,156** eligible तमप् and तरप् relations. One already occurs in the plain-source ledger, so the [comparative and superlative report](../../analysis/generativity/results/taddhita_generalization_six_pass_summary.md) adds **1,588,155 word-meanings** and raises the combined bounded subtotal to **12,704,821**. The other recovered families remain source-bounded until their required input classes can be identified independently. Thirty of the planned thirty-six passes remain.

The following six passes return to स्त्रीप्रत्यय with the semantic classes now available. Four source operations already denote agents: ण्वुल् and तृच् agent nouns, the conditioned अच् agent, and the blessing-specific वुन् agent. Their source ledgers retain the धातुः code, कृदन्त suffix, उपसर्गः, and सनादि stack, allowing every candidate to be reconstructed rather than inferred from spelling. Vidyut generates all **140,568** lexical feminine relations through टाप् or ङीप्. Two कर्तृ/कर्त्री and हर्तृ/हर्त्री relations overlap the earlier source-example set. Four other coincident spellings are not merged because spelling does not establish meaning. The [lexical स्त्रीप्रत्यय report](../../analysis/generativity/results/stri_generalization_six_pass_summary.md) therefore adds **140,566 word-meanings** and raises the combined bounded subtotal to **12,845,387**. Participles, verbal adjectives, and other agreement-driven feminine forms remain outside the lexical count. Twenty-four planned passes remain.

The next six passes establish a deliberately narrow समास boundary. They inventory all eight compound types exposed by pinned Vidyut 0.4.0 and extract 167 regression assertions from its Kāśikā tests. Thirty-five ignored assertions and twelve active assertions whose members are constructed inside test helpers remain outside eligibility. Seven repeated assertions collapse, leaving **113 unique active source relations** whose members and outputs are stated directly. Each relation contributes one compound word-meaning at derivational depth one. The [bounded समास report](../../analysis/generativity/results/samasa_six_pass_summary.md) raises the combined subtotal to **12,845,500**. It does not infer that every nominal pair forms a meaningful compound, count recursive compounds, or treat output variants as additional meanings. Eighteen planned passes remain.

The following six passes test one further operation after those source compounds. Seventeen अव्ययीभाव compounds remain complete indeclinables; the other **96** enter as nominal bases. Five established तद्धित relations add 480 nominal meanings. Four established नामधातुः relations add 384 verbal meanings. One nonrecursive नञ् relation adds 94 nominal meanings after excluding two compounds that are already negative. Vidyut generates all 864 तद्धित and नामधातुः relations, while the previously source-tested नञ् rules generate the remaining 94; a separate verification pass reproduces every output set. The [compound-input stack report](../../analysis/generativity/results/compound_stack_six_pass_summary.md) adds **958 word-meanings** and raises the subtotal to **12,846,458**. It stops at derivational depth two.

The final twelve समास passes replace the 113-example fixture with a formal capacity model while retaining those examples as verification evidence. A virtual inventory reconciles **8,083,621 compoundable nominal word-meanings** without copying them into another ledger. Four broadly available relations then yield **196,034,769,247,681 depth-one semantic slots** when a speaker intends the named relation. Applying one of ten post-compound operations under its declared semantic reading yields **1,960,347,692,476,810 formal slots**. At depth two, exactly one depth-one compound may join one original nominal member; two depth-one compounds and unrestricted recursion remain excluded. That boundary yields **9,508,024,664,524,249,997,406 slots**. The pinned local Rust verifier regenerates all 113 source fixtures, sixteen depth-one samples, and six recursive samples with complete rule histories. The [twelve-pass report](../../analysis/generativity/results/samasa_capacity_twelve_pass_summary.md) keeps every capacity outside the materialized lexical subtotal. No समास capacity passes remain; तिङन्त analysis is next.

The twelve तिङन्त passes assemble a virtual inventory of **4,540,848 लौकिक verbal word-meanings** from eight provenance-rich source layers. Ten लौकिक लकाराः yield **45,408,480 third-person singular citation cells**. Expanding each coordinate across three पुरुषाः and three वचनानि yields **408,676,320 कर्तरि grammatical cells**. The citation cells are a subset of the full matrix. परस्मैपदम् and आत्मनेपदम् outputs remain attached to one semantic cell rather than supplying an automatic two-series multiplier. Vidyut regenerates all ninety citation samples and all 270 cells in the भू-कृ-एध् paradigm sample with complete rule paths. Thirteen repeated spellings in that sample retain every grammatical coordinate. The [twelve-pass report](../../analysis/generativity/results/tinanta_twelve_pass_summary.md) keeps all grammatical cells outside the lexical subtotal. No तिङन्त passes remain.

The twelve नामरूप passes first replace the compound-oriented nominal view with an exact lexical-class reconciliation. The current subtotal contains **8,084,287 लौकिक name, object, quality, state, and relation meanings**, plus **7,925 complete unchanging meanings** that do not enter declension. One citation coordinate supplies 8,084,287 cells. Eight relation coordinates across one, two, and more than two supply **194,022,888 grammatical cells**. Gender determines the output within a cell but does not automatically triple either lexical meanings or grammatical coordinates. Vidyut regenerates all eight citation samples and all 192 cells in eight complete paradigms with rule histories. Forty-six sample spellings recur across coordinates; no coordinates are merged. The [twelve-pass report](../../analysis/generativity/results/subanta_twelve_pass_summary.md) keeps both capacities outside the lexical subtotal. Agreement-driven additional genders and Vedic-domain nominal inflection remain separate.

Verification covers source hashes, exact evidence anchors, all original fields, applied/proposed count separation, the 304-row operation census, all ordinary and Vaidika कृत्प्रत्यय classifications, all 175 तद्धित identifier dispositions, all seven स्त्रीप्रत्यय identifiers, the नामधातुः classification and ledger, every completed engine run, each restriction and enrichment, row-count reconciliation, stable IDs, and cross-domain arithmetic. The integrated test count is recorded in the analysis README after each completed run. The manuscript, companion, covers, and published calculation remain unchanged by this analysis.

### Historical Sequence

The following paragraphs record the earlier state of the work. Their open queues and proposed subtotals are superseded by the eight-pass consolidation above.

**Current, 2026-09-13:** The first reconciliation was approved and applied in a separate normalization layer: [current research count, 2,649](../../analysis/generativity/results/current_research_count.md). All 2,741 original assignment rows and fields remain; one is classified as grammatical metadata, while three additional consolidations use shared keys. The ay headword correction is applied without assuming identity with the other ay entry. The earlier nine batches retain their historical 2,653 endpoint.

The [second ten-case report](../../analysis/generativity/results/reconciliation_review_02.md) is now ready for author review. It proposes mergers for bhram, dhvan, and jharjh, plus removing the unsupported binding assignment under dhri-ng from the admitted subtotal while preserving it as an unresolved source reading. Proposed subtotal: 2,645; not applied. Six cases retain their counts, including unresolved ay. Bhu's heading and mixing example are clarified; alternative readings for dhup and ghat remain attributed rather than being added automatically. Across the two targeted passes, 19 of 84 historical follow-up records have been revisited, with 65 still untouched. Three partial lists and two unenumerated entries remain additional work.

The [first ten-case reconciliation](../../analysis/generativity/results/reconciliation_review_01.md) remains available as the historical before/after proposal record. Do not rewrite the archived source or old batch decisions when applying later approvals. Use `normalized_*` fields and exclude grammatical metadata in subsequent enumeration.

The author authorized all remaining exact-citation passes, and Batches 4-9 are complete. Review their [combined report](../../analysis/generativity/results/identity_passes_complete.md), then address the [recorded follow-ups](../../analysis/generativity/results/identity_followups.md), prioritizing reading differences that affect the base count. The six batch subtotals are 2,708, 2,701, 2,691, 2,678, 2,663, and 2,653. Do not confuse an exhausted review queue with a final vocabulary count. Cross-spelling identities, finer senses, affix eligibility, and enumeration remain separate work.

Keep three open identity groups from batch 1 in the queue: bhram (movement versus not remaining settled), dhri-ng (binding/destruction versus remaining), and dhvan (the ghatadi repetition). Also retain the meaning-expansion follow-ups for bhu's avakalkana reading and dhup's alternative shining reading. They were recorded, not silently added to this identity batch's count.

Batch 2 adds two unmerged open groups: ghri (sprinkling versus flowing, with shining retained) and nat (competing performance, dance, movement, and bending readings). Jharjh's shared speaking meaning is consolidated, but tarjana versus bhartsana still needs review. The ledger also records the source variants for ghat/nad's speech-or-shining group, ghush's declaration/non-declaration conditions, shik's marshana/amarshana wording, and khud's citation/pada alignment. These follow-ups do not authorize automatic count changes.

The latest meaning pass added 29 assignments: the subtotal after the two existing duplicate reductions rose from 2,710 to 2,739. Carry three partial-list gaps alongside identity work: prud's second description, vap's longer source list, and radh's unspecified remainder. The kage and van entries remain outside the numerical subtotal because their sources do not enumerate their meanings. Every source row and original description remains available. None of these subtotals includes a prefix or inflection multiplier.

Batch 3 adds eight unmerged open groups: shrath, shubh, shumbh, svid, arj, brih, bukk, and chan. They have specific citation or meaning questions recorded beside the evidence. The third arha assignment remains provisional despite the supported merger of its first two assignments. The two shrana atoms remain separate because the commentary explicitly calls them different atoms, even with the same giving gloss. Other within-entry meaning and alternative-reading checks remain visible in the ledger.

The exact-citation diagnostic identified 223 groups covering 487 entries in the richer source. All have now been examined. The earlier jval and gadi consolidations remain, as do all decisions from Batches 1-3. Batches 4-9 add 61 partly or fully consolidated groups, 86 groups retaining different listed meanings, and 24 wholly open groups. Across the entire review, 37 groups remain wholly open; another 47 contain a recorded follow-up despite a decision on part of the group. Additional meanings remain independent. The old-to-new reconciliation also retains the 354 entries without an unambiguous exact candidate and all shared target mappings. No source meanings have been automatically transferred into the old inventory.

Carry the new eligibility notes into the next stage: meaning-conditioned pada use, the nitya-sananta entry, a required AN prefix, Vedic-only entries, and nominal-derived inputs already present in the base file. Counting those nominal-derived inputs again as newly created bases would duplicate the same formation.

Then expand affix-level coverage and establish semantic eligibility before broad enumeration. In the separate inflection stage, all applicable grammatical cells remain counted regardless of repeated spelling. The manuscript remains unchanged.
