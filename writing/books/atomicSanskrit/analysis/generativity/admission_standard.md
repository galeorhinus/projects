# Generative Admission Standard

Approved by the author on 2026-09-13 as Pass 2 of the verbal-derivation census.

## What Enters the Ledger

A derived word-meaning enters the research ledger when all of the following conditions hold:

1. A declared grammatical rule positively licenses the operation and its meaning.
2. The input is an admitted base word-meaning in the current reconciled ledger.
3. The input satisfies the rule's structural and semantic conditions.
4. The pinned engine produces at least one form through the relevant operation. If its public API does not expose that operation, a direct implementation of the cited rules must reproduce pinned source examples before it can generate a ledger.
5. No explicit rule, **अनभिधानम् (*anabhidhānam*)**, or documented lexical restriction excludes the formation.

A bounded source-example pass can also admit a directly demonstrated derived word-meaning when its source supplies the input, semantic relation, operation, and expected output, and the pinned engine reproduces that output. In that route, the source input does not automatically enter the base inventory, and the example does not authorize multiplication across other inputs. The conditioned तद्धित and स्त्रीप्रत्यय passes use this narrower route.

Dictionary or corpus attestation is not required when a productive grammatical rule licenses the formation. Sanskrit's generative architecture does not require every valid word to have been collected in a dictionary. Attestation can strengthen a record or resolve an exception, but absence from a dictionary does not erase a rule-licensed word.

For an उपसर्गः (*upasargaḥ*), Aṣṭādhyāyī 1.4.58 identifies the प्रादि forms and 1.4.59 authorizes their उपसर्ग operation when they connect with an action. A successfully constructed उपसर्ग-धातु pair therefore enters the generative ledger even when its exact conventional gloss has not yet been recorded. Such a row carries an open meaning, not a rejected meaning. Established usage can supply its gloss or add further distinct meanings later.

## What Vidyut Establishes

Vidyut establishes that its pinned implementation can construct a form from the declared input and operation. It does not establish the intended meaning, decide whether an operation is productive in that semantic environment, or override an explicit exclusion in the grammatical sources.

The rule supplies semantic authority. The engine normally supplies a reproducible construction. The bounded नञ् pass records the one present exception: Vidyut implements compounds internally but does not expose their construction through its Python API, so the pass implements the three cited rules directly and verifies both surface outcomes against five tests from the same pinned Vidyut revision.

## Counting Rules

- Count a distinct word or a distinct meaning, not a distinct spelling.
- The same spelling with two meanings contributes two word-meanings.
- Alternative surface forms of one derivation remain attached to one word-meaning unless evidence establishes that they are different words.
- A productive semantic branch contributes once for each admitted base word-meaning that satisfies its conditions.
- A class-forming operation does not become a new derived word merely because the engine uses the same प्रत्ययः (*pratyayaḥ*) that another rule uses derivationally.
- Inflected तिङन्तानि (*tiṅantāni*) and सुबन्तानि (*subantāni*) remain outside the lexical subtotal.
- Each ledger declares its own operation depth. The completed verbal ledgers separately count one सनादिप्रत्ययः, one उपसर्गः, one उपसर्गः plus one सनादिप्रत्ययः, a true चरादिगण causative, and exactly two ordered उपसर्गाः. The final layer is a computational bound, not a claim that the grammar limits a stack to two.
- The one-उपसर्गः and two-उपसर्गः ledgers begin with original base धातु meanings. The stacked उपसर्गः + सनादि ledger begins with the admitted one-सनादि semantic branches.
- An उपसर्ग-धातु pair is removed only for an explicit grammatical conflict, an unmet structural condition, or failure of the pinned engine to construct a form. Missing attestation is not an exclusion.
- A धातुपाठः meaning limited to a named उपसर्गः is inherited only when that उपसर्गः stands directly before the धातुः. An outer उपसर्गः may precede it in the two-prefix ledger. A meaning marked अनुपसर्ग is not inherited by any prefixed formation, even when the engine can construct its surface form.
- A source clause can add a prefixed meaning that the unprefixed base does not carry. Such an enrichment adds a word-meaning only in the prefix environment licensed by that clause.
- The completed कृदन्त ledgers apply fourteen classified laukika semantic operations directly to the 2,634 original धातु meanings, to admitted one-उपसर्गः meanings, and to admitted one-सनादि meanings and true चरादिगणः causatives.
- Three laukika अव्यय operations and ten selected root-conditioned कृदन्त operations have separate ledgers. Classification never admits a word by itself; each counted operation still requires an explicit meaning and source rule.
- The bounded तद्धित pilot starts from five declared nominal inputs. It does not extrapolate those examples across the 175 identifiers exposed by the engine.
- Nineteen engine-metadata Vedic-domain कृत्प्रत्यय identifiers, plus क्वसु recovered from the source-level domain review, map to seven semantic operations. The completed Vedic-mode ledgers count only operations for which the source condition and engine output are both available; unsupported operations remain explicit and uncounted.

## Current Consequences

- General यङन्त (*yaṅanta*) produces separate repetition and intensity meanings.
- Rule 3.1.23 replaces those two meanings with crooked movement when the धातुः (*dhātuḥ*) itself expresses movement.
- Rule 3.1.24 replaces them with disparagement of the action for its listed धातवः (*dhātavaḥ*).
- यङ्लुगन्त (*yaṅluganta*) is a separate derived verbal word that inherits the licensed यङन्त meaning.
- The known *śobhate* and *rocate* exclusions remain outside both यङन्त and यङ्लुगन्त.
- For a चरादिगणः (*curādigaṇaḥ*) base, the first णिच् (*ṇic*) supplied under 3.1.25 is class-forming. The completed true-causative pass adds a second णिच् under 3.1.26.
- The root-specific उपसर्ग sweep records 134 one-prefix exclusions from seven explicit धातुपाठः conditions. It also supplies 21 additional one-prefix meanings. The same conditions produce 2,680 exclusions and 420 enrichments in the ordered two-prefix layer.
- The कृदन्त classification treats ल्युट् action, instrument, and location as three meanings even when the same generated form carries all three. It keeps alternative surface forms of one operation/base relation together.
- The twelve-pass engine run contains 2,174,721 word-meanings under laukika generation mode. Eleven base meanings in the shared inventory are already documented as Vedic-only; removing their 8,660 base-and-descendant rows gives a current known laukika subtotal of 2,166,061. Neither is a complete Sanskrit vocabulary total, and neither has been deployed in the manuscript.
- The Vaidika passes add 204,738 word-meanings through Vaidika-specific operations. Together with the 8,660 base-and-descendant rows moved across the known domain boundary, the bounded Vaidika subtotal is 213,398 and the combined bounded subtotal is 2,379,459. The 5,280 candidates attached to unsupported Vaidika suffix families remain outside that count.
- The first broad तद्धित expansion begins with 794,078 declared लौकिक nominal word-meanings. Three general relations and three bounded descent examples generate 2,382,237 तद्धित word-meanings. Seven were already present in the pilot, so 2,382,230 are new and the current combined bounded subtotal becomes 4,761,689.
- The conditioned तद्धित source-example pass adds 975 relations whose nominal base, semantic context, suffix, rule-located test, and expected form are explicit. Thirty-five relations that the unrestricted Python constructor does not reproduce remain outside the subtotal. The current combined bounded subtotal is 4,762,664.
- The स्त्रीप्रत्यय source-example pass inventories all seven pinned suffix identifiers and admits 50 feminine word-meanings. Five already-feminine bases that merely decline in स्त्रीलिङ्ग and ten generic-constructor mismatches remain outside the lexical count. The current combined bounded subtotal is 4,762,714.
- The नामधातुः pass applies four productive relations from rules 3.1.8-3.1.11 to the first 794,078-meaning nominal inventory: two self-related desire formations, treatment of an object by comparison, and conduct of an agent by comparison. Rules 3.1.12-3.1.21 remain source-conditioned. Forty active narrower relations are admitted; ten relations from an ignored engine test remain outside the count. The pass adds 3,176,352 derived verbal meanings and raises the current combined bounded subtotal to 7,939,066.
- The bounded नञ् pass applies one negative relation to the current 3,177,340-meaning nominal inventory. Aṣṭādhyāyī 2.2.6 licenses the compound; 6.3.73-74 determine the अ-/अन्- surface outcome. Those two outcomes are not separate semantic multipliers. The pass admits one negative word-meaning per source meaning and raises the combined subtotal to 11,116,406. It does not require dictionary attestation, apply negation recursively, count additional interpretations of नञ्, or inflect the resulting compounds.
- A नामधातुः row is a derived verbal base, not a finite तिङन्त word. The source examples' present-tense forms verify their operations but are not counted as additional lexical meanings.
- The comparative and superlative generalization pass reads 5.3.55 and 5.3.57 as general semantic operations under an intended comparison. तमप् and तरप् therefore apply to all 794,078 declared लौकिक nominal meanings. Rule 5.3.58 restricts इष्ठन् and ईयसुन् to गुणवचन inputs. English semantic labels such as fitness, capacity, or disposition do not independently establish that traditional category, so those two operations remain deferred. All 1,588,156 eligible तमप् and तरप् relations generate; one already occurs in the plain-source ledger, so 1,588,155 are added and the combined bounded subtotal becomes 12,704,821.
- The broader स्त्रीप्रत्यय pass admits only nominal meanings already classified as lexical agents. It reconstructs four source operations from their original grammatical metadata and requires Vidyut to insert a स्त्रीप्रत्यय. Participial and adjectival agreement is not another lexical meaning. All 140,568 candidates generate; two confirmed agent-feminine relations already occur in the earlier source set, so 140,566 are added and the combined bounded subtotal becomes 12,845,387. Coincident spelling without established semantic identity does not create an overlap.
- The first broader समास pass admits only unique active relations stated directly in the pinned Kāśikā regression tests. Every retained assertion must expose its members, compound type, and expected output without reconstructing a test-local member. The 113 admitted relations remain at derivational depth one. They do not license every pair of nominal meanings or recursive reuse of their outputs. The combined bounded subtotal becomes 12,845,500.
- The first compound-input stack treats 96 source-demonstrated compounds as nominal bases and leaves 17 अव्ययीभाव compounds as complete indeclinables. Nine previously established nominal operations apply to those 96 bases. The नञ् operation applies to 94, excluding two compounds that are already negative. Every one of the 958 depth-two relations must reproduce a form; no further recursion is admitted. The combined bounded subtotal becomes 12,846,458.
