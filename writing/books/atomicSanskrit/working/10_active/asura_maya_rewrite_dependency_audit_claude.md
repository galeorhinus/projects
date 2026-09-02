# *Asura* → *Āsurī Māyā* — Dependency Audit for the Rewrite

**Date:** 2026-08-29 · **Scope:** whole manuscript, appendices, endnotes, glossary, figures,
reference docs, working plans · **No files were edited.** This records what depends on the old
thesis and what each passage needs. **No replacement prose is drafted here.**

## The change being audited

| | |
|---|---|
| **Old thesis** | The Ṛgveda contains **two different words** on one sound-form — *asu-ra* (life-bearing) and *a-sura* (un-shining). The word chosen tells you the alignment. |
| **Replacement** | The transmitted word *asura* **does not by itself determine alignment.** At Svarbhānu, RV 8.96.9, RV 10.124.5, RV 10.138.3 it may invite either analysis, but **the actor's actions** decide whether the power serves *sat* or *asat*. The pyramid conceals those actions and projects factional identity in their place — **āsurī māyā**: *āvaraṇa* conceals the action, *vikṣepa* projects an identity. The Vedas require **viveka**: examine purpose and action, not the label. |

**What survives untouched:** action-not-faction; *āvaraṇa*/*vikṣepa*; *viveka*; *sat*/*asat*;
*asuratva* as an operating mode; the pyramid's conflation charge; the PIE double-standard charge.

**What breaks:** any sentence asserting that the Ṛgveda *contains* two words, that the two are
*separately generated*, or that a given actor *is* an *a-sura* by word-choice rather than by deed.

**Corroborating evidence already in the repo** (from `as_asura_rigvedic_adversary_inventory.md`,
2026-08-29): *sura* has **0** RV occurrences against *asura*'s 88; the RV marks the adversary
sense with a privative on ***deva*** (RV 8.96.9 *asurā adevāḥ*) against RV 8.25.4 *devāv asurā*,
never on *sura*; the named antagonists including Svarbhānu are **आसुर (*āsura*)**, the vṛddhi
adjective built from *asura*. This audit's recommendations align with that finding.

---

## 1. Chapter 3 §3.6 — the epicenter

Everything else in the book points here. [as_1_03_strategic.md](../../manuscript/as_1_03_strategic.md)

### 1.1 Section framing

| # | ref | current | dependency | recommendation |
|---|---|---|---|---|
| A1 | [:133](../../manuscript/as_1_03_strategic.md#L133) | Heading "3.6 The असुर (*Asura*) Analysis: Action, not Faction" | **none** — this is the replacement thesis already | **keep** |
| A2 | [:135](../../manuscript/as_1_03_strategic.md#L135) | "**Two different Sanskrit words share the sound-form** असुर… The listener must examine what the actor does to distinguish *asu-ra* from *a-sura*" | **hard** — asserts two words as fact; makes *viveka* a tool for picking between words rather than for reading action | **rephrase** — the second clause already carries the replacement; the first must stop asserting two words exist in the corpus |
| A3 | [:137](../../manuscript/as_1_03_strategic.md#L137) | The **notation convention**: "the book uses असुर for the antagonist *a-sura*… says *asu-ra* explicitly" | **hard, and book-wide** — this convention is invoked by name in Ch 4 and Ch 18 | **rephrase — highest priority.** Every downstream site inherits it. Decide the replacement convention before touching anything else. |
| A4 | [:139](../../manuscript/as_1_03_strategic.md#L139) | "The architecture of containment is asuric because it withholds… The pyramid hides it by presenting protagonists and antagonists as rival factions." | **none** — this *is* the *āvaraṇa*/*vikṣepa* claim | **keep** |
| A5 | [:141](../../manuscript/as_1_03_strategic.md#L141) | The *bound*/*bounds* English homonym analogy | **hard** — the analogy exists solely to make "two words, one sound-form" intuitive | **remove or relocate.** See §5: removing it leaves A6 without a run-up. |
| A6 | [:143](../../manuscript/as_1_03_strategic.md#L143) | "The pyramid demands that the reader abandon that ordinary clarity when the word is असुर" | **hard** — "that ordinary clarity" is a back-reference to A5 | **rephrase**; cannot survive A5's removal unedited |

### 1.2 "Two Words, One Sound-Form" (subsection)

| # | ref | current | dependency | recommendation |
|---|---|---|---|---|
| B1 | [:145](../../manuscript/as_1_03_strategic.md#L145) | Subsection heading **"Two Words, One Sound-Form"** | **hard** — the heading is the old thesis | **rephrase** (heading rename; see §6 for the cross-reference cost) |
| B2 | [:147](../../manuscript/as_1_03_strategic.md#L147) | Yāska's *nāmāny ākhyātajāni*, nominal words arise from verbs | **none** — supports action-decides directly | **keep** — likely *strengthened* under the new thesis |
| B3 | [:151](../../manuscript/as_1_03_strategic.md#L151) | "Yāska explains ***asu-ra*** through असु… describes the असुराः as possessing it" | **medium** — Yāska explains *asura*, not "*asu-ra*"; the hyphenation imports the two-word claim | **rephrase** — drop the hyphenated form; the content is correct. Note: `yaska-asura-nirukta` records that Yāska gives *three* explanations, not one |
| B4 | [:152](../../manuscript/as_1_03_strategic.md#L152) | Kauthuma Padapāṭha divides *asurasya* → *a + surasya* | **none** — a real segmentation by a recitation discipline; the strongest witness and it survives | **keep** |
| B5 | [:154](../../manuscript/as_1_03_strategic.md#L154) | "These are separate witnesses. Yāska preserves the life-breath analysis. The Padapāṭha preserves the privative division." | **low** — accurate as written; only "separate witnesses **to two words**" would break | **keep**, verify surrounding framing |
| B6 | [:156](../../manuscript/as_1_03_strategic.md#L156) | *svar/sūrya/sūri/sūra* radiance family; ⟪सुर्⟫ *aiśvarya-dīptyoḥ* | **none** — supplies the field the analysis draws on | **keep** |
| B7 | [:158](../../manuscript/as_1_03_strategic.md#L158) | The **अज (*aja*)** parallel — goat vs Unborn, "Two different derivations generate one sound-form" | **hard** — a proof-by-parallel for the two-word claim | **relocate or remove.** The *aja* case is genuinely two derivations; *asura* is now asserted not to be. Keeping it adjacent implies the parallel still holds. |
| B8 | [:160](../../manuscript/as_1_03_strategic.md#L160) | The imaginary-goat joke | **medium** — depends on B7 | **remove** if B7 goes; it has no independent referent |
| B9 | [:162](../../manuscript/as_1_03_strategic.md#L162) | "***Asu-ra*** and ***a-sura*** follow the same pattern. **Two separately generated Sanskrit words converge upon one sound-form.**" | **hard — the single most load-bearing sentence in the old thesis** | **remove** |
| B10 | [:164](../../manuscript/as_1_03_strategic.md#L164) | "Two words, two etymologies, one sound-form." (hammer) | **hard** — the thesis compressed into a refrain | **remove** |

### 1.3 "The Life-Bearing *Asu-ra*" (subsection)

| # | ref | current | dependency | recommendation |
|---|---|---|---|---|
| C1 | [:166](../../manuscript/as_1_03_strategic.md#L166) | Heading "The Life-Bearing *Asu-ra*" | **hard** | **rephrase** |
| C2 | [:168–176](../../manuscript/as_1_03_strategic.md#L168) | RV 1.174.1 (Indra) and RV 1.24.14 (Varuṇa) block quotes | **none** — the mantras are evidence of *action* | **keep** |
| C3 | [:182](../../manuscript/as_1_03_strategic.md#L182) | "Indra protects… Varuṇa loosens… **In these mantras, असुर is *asu-ra***, the bearer of असु" | **hard** in its final clause; the first two sentences are pure action-reading | **rephrase** — keep the action reading, drop the word-identification |

### 1.4 "The Containing *A-sura*" (subsection)

| # | ref | current | dependency | recommendation |
|---|---|---|---|---|
| D1 | [:184](../../manuscript/as_1_03_strategic.md#L184) | Heading "The Containing *A-sura*" | **hard** | **rephrase** |
| D2 | [:186](../../manuscript/as_1_03_strategic.md#L186) | Pipru (**RV 10.138.3**), Varcin (7.99.5), Namuci (10.131.4, *āsura*), Svarbhānu (5.40.5) | **none** — and it already distinguishes असुर from आसुर correctly | **keep** — one of the four named replacement passages |
| D3 | [:188](../../manuscript/as_1_03_strategic.md#L188) | "Their names do not determine their conduct." | **none** — this is the replacement thesis in one line | **keep** |
| D4 | [:190](../../manuscript/as_1_03_strategic.md#L190) | Varcin bears *varcas*, Svarbhānu bears *svar/bhānu*; "Sanātan evaluates what a being does with that capacity." | **none — actively supports the replacement** | **keep.** Strong: radiant *names* borne by antagonists is precisely "the label does not decide" |
| D5 | [:194–202](../../manuscript/as_1_03_strategic.md#L194) | RV 5.40.5 block quote | **none** | **keep** |
| D6 | [:204](../../manuscript/as_1_03_strategic.md#L204) | "The verse uses ***आसुरः***, which Sanskrit derives from ***असुर***. The long **ā** belongs to that derivative form… **The *action* does.**" | **none — already the replacement argument** | **keep** |
| D7 | [:206](../../manuscript/as_1_03_strategic.md#L206) | Svarbhānu's deed given as **आवरण** conceals / **विक्षेप** projects | **none — this is the *āsurī māyā* frame already in place** | **keep — the anchor the rewrite builds from** |
| D8 | [:208](../../manuscript/as_1_03_strategic.md#L208) | "In what universe would anyone view Svarbhānu here as ***asu-ra***… rather than ***a-sura***?" | **hard** — the rhetorical force is "you must pick the other word" | **rephrase** — recast as "which action", not "which word" |
| D9 | [:210–212](../../manuscript/as_1_03_strategic.md#L210) | "Only inside the fertile imagination of a philology determined to hide the radiance… **Exactly like Svarbhānu.**" | **low** — depends on D8's setup, not on two-words | **keep**, verify the run-in after D8 changes |

### 1.5 "The Pyramid's Attestation Trick" (subsection)

| # | ref | current | dependency | recommendation |
|---|---|---|---|---|
| E1 | [:214](../../manuscript/as_1_03_strategic.md#L214) | Heading | none | keep |
| E2 | [:216](../../manuscript/as_1_03_strategic.md#L216) | "Because standalone सुर does not appear in the Ṛgveda, it decrees that the Veda could not possibly generate ***a-sura***" | **medium — and this is now the exposed flank.** The book concedes *sura* is absent, then argues generativity. Under the new thesis the concession is fine, but the sentence still frames the goal as certifying *a-sura* as a word | **rephrase + verify** — see §5; this is where the strongest external counter-argument lands (Taraporewala/Hale: *sura* is a post-Vedic back-formation) |
| E3 | [:218–222](../../manuscript/as_1_03_strategic.md#L218) | *a-deva* privative in RV; *a-dabdha* 48× vs *dabdha* 0× | **none** — a generativity argument, independent of two-words | **keep.** Note the inventory doc's finding makes *a-deva* doubly useful: it is the privative the RV *does* use for the adversary |
| E4 | [:226–230](../../manuscript/as_1_03_strategic.md#L226) | Attestation-committee ridicule; *adabdhāḥ* Vedas | none | keep |

### 1.6 "What the Pyramid Gains from Conflation"

| # | ref | current | dependency | recommendation |
|---|---|---|---|---|
| F1 | [:234](../../manuscript/as_1_03_strategic.md#L234) | "It therefore **refuses to recognize *asu-ra* and *a-sura* as two Sanskrit words.** Instead it installs ***h₂ḿ̥suros***" | **hard** — the charge is defined as denying two words | **rephrase** — the charge must become: it installs a reconstructed *identity* in place of the action |
| F2 | [:236](../../manuscript/as_1_03_strategic.md#L236) | PIE double standard: demands attestation, grants itself starred forms | **none** | **keep** |
| F3 | [:238](../../manuscript/as_1_03_strategic.md#L238) | "**अ + सुर, not-sovereign — becomes 'sovereign.'**" — the pyramid's incoherent derivation | **low** — attacks the pyramid's own derivation, not the book's | **keep**, verify it does not read as the book asserting *a-sura* |
| F4 | [:240](../../manuscript/as_1_03_strategic.md#L240) | Portable title for RAT | none | keep |
| F5 | [:242](../../manuscript/as_1_03_strategic.md#L242) | "They **rejected both Sanskrit words** and installed a third" | **hard** | **rephrase** |

### 1.7 "How Conflation Turns Action into Faction" · "Viveka in Every Age"

| # | ref | current | dependency | recommendation |
|---|---|---|---|---|
| G1 | [:244–246](../../manuscript/as_1_03_strategic.md#L244) | "The **invented third word** allows the pyramid to recast… factions… *sat*/*asat* disappears" | **medium** — "third word" presupposes two | **rephrase**; the faction argument itself is the replacement thesis |
| G2 | [:248](../../manuscript/as_1_03_strategic.md#L248) | "In those mantras, असुर is ***asu-ra***" | **hard** | **rephrase** |
| G3 | [:250](../../manuscript/as_1_03_strategic.md#L250) | "In those mantras, असुर is ***a-sura***, the containing antagonist" | **hard** | **rephrase** |
| G4 | [:252–256](../../manuscript/as_1_03_strategic.md#L252) | "Their *faction* does not decide… Their **actions** do." + *sat*/*asat*, swastika/pyramid | **none — the replacement thesis, already written** | **keep** |
| G5 | [:260](../../manuscript/as_1_03_strategic.md#L260) | "It cannot be a coincidence that the Vedas use the same sound-form for actors on opposite sides… the listener must examine the action" | **medium** — "same sound-form" is fine; the *design* claim ("not a coincidence") presumes deliberate two-word engineering | **rephrase** — retain the *viveka* conclusion, soften the design claim |
| G6 | [:262](../../manuscript/as_1_03_strategic.md#L262) | "collapsing **the two Sanskrit words** into one inherited title" | **hard** | **rephrase** |
| G7 | [:266](../../manuscript/as_1_03_strategic.md#L266) | "separate सत् from असत्, **the life-bearing *asu-ra* from the radiance-opposing *a-sura***, and the swastika from the pyramid" | **hard** — the triple is a refrain; the middle term breaks | **rephrase** (refrain — see §6) |
| G8 | [:268](../../manuscript/as_1_03_strategic.md#L268) | "**Sanātan evaluates the action, not the faction.**" | **none — the thesis in five words** | **keep** |

---

## 2. Downstream chapters

| # | ref | current | dependency | recommendation | connected apparatus |
|---|---|---|---|---|---|
| H1 | [as_1_00_seekers.md:77](../../manuscript/as_1_00_seekers.md#L77) | "Later chapters apply this same method to असुर, आर्य, and संस्कृत. Each word describes actions or attributes…" | **none — forward-declares action-not-faction** | **keep** | sets up the *ārya*/*dāsa* parallel |
| H2 | [as_1_01_one_oppressors_finite.md](../../manuscript/as_1_01_one_oppressors_finite.md) (6 hits) | asuric-pyramid usage | **none** — mode, not word-split | **verify** only | |
| H3 | [as_1_04_fourth_abrahamic.md:25](../../manuscript/as_1_04_fourth_abrahamic.md#L25) | "the Vedic conflict between **life-force and containment**… presented as a tribal or factional feud" | **medium** — "life-force vs containment" is the two-word pair in paraphrase | **rephrase** — the faction charge survives; the framing names the old poles | |
| H4 | [as_1_04_fourth_abrahamic.md:199](../../manuscript/as_1_04_fourth_abrahamic.md#L199) | "Chapter 3 distinguished the life-bearing ***asu-ra*** from the radiance-opposing ***a-sura***. **Following the convention established there**…" | **hard** — explicitly inherits A3's convention | **rephrase — blocked on A3** | Ch 4 §4.6 *asuratva*; glossary |
| H5 | [as_1_16_one_architecture_two_domains.md:321](../../manuscript/as_1_16_one_architecture_two_domains.md#L321) | "the two enemies introduced in Chapter 6: entropy and asuras" | **none** | keep | |
| H6 | [as_1_18_wrong_question.md:229](../../manuscript/as_1_18_wrong_question.md#L229) | "Chapter 3 §3.6 followed that distinction through **two Sanskrit words that share one sound-form**. The life-bearing *asu-ra*… The radiance-opposing *a-sura*…" | **hard** — a full restatement of the old thesis | **rephrase — blocked on §3.6** | cross-ref to §3.6 |
| H7 | [as_1_19_pie_in_sky.md:308](../../manuscript/as_1_19_pie_in_sky.md#L308) | Chain diagram line: "**असुरः (*asu-ra*, "the breath-bearer, the holder of the life-force")**" | **hard** | **rephrase** | **Figure 19.9** (`deva_asura_vivimorphosis_chains.svg`) |
| H8 | [as_1_19_pie_in_sky.md:314](../../manuscript/as_1_19_pie_in_sky.md#L314) | "it is **two words, not one**. The first is *asu-ra*, the breath-bearer…" | **hard** | **rephrase** | §19.8; `asura-standard-etymology-contested` |
| H9 | [as_1_19_pie_in_sky.md:318](../../manuscript/as_1_19_pie_in_sky.md#L318) | "The vivimorphosis at the contact-language boundary **preserves the breath-bearer, not the withholder.** Avestan *ahura*…" | **hard** — the Avestan argument is built on which of two words travelled | **verify then rephrase** — this may be the costliest single repair; the Iranian comparison needs a formulation that does not depend on selecting a word | Figure 19.9 |
| H10 | [as_2_01_epilogue.md:33,139](../../manuscript/as_2_01_epilogue.md#L33) | *samudra-manthana*; "asuras jealous of devas" | **none** — narrative, not etymological | keep | |
| H11 | [as_part_01_wrong_metaphor.md:9–17](../../manuscript/as_part_01_wrong_metaphor.md#L9) | Epigraph **Maitrāyaṇī Saṃhitā 1.9.3** — "By truth were created the radiant ones; by untruth, their opposites" | **none — and it corroborates the replacement**: alignment follows *satya*/*anṛta*, i.e. conduct | **keep** | `maitrayani-samhita-1-9-3-satya-asura` |
| H12 | [as_3_10_glossary.md:363](../../manuscript/as_3_10_glossary.md#L363) | **असुरत्व** entry — "quality of being an असुर… consolidates power, deceives, withholds light" | **none** — defined by behaviour already | **keep**; **verify** no sibling *asu-ra*/*a-sura* entries are needed or now orphaned | pairs with **आर्यत्व** |
| H13 | [as_3_03_audiography.md](../../manuscript/as_3_03_audiography.md), [as_3_05_language_factory.md](../../manuscript/as_3_05_language_factory.md), [as_1_06_apabhramsa.md](../../manuscript/as_1_06_apabhramsa.md), [as_1_10_building_dhatuh.md](../../manuscript/as_1_10_building_dhatuh.md) | incidental *asura* mentions (1–2 each) | **none** | **verify** only | |

---

## 3. Endnotes

Deployment lines inside endnotes name the sections they serve; renaming a §3.6 subsection
(B1, C1, D1) requires updating those lines too.

| # | stub | dependency | recommendation |
|---|---|---|---|
| J1 | `yaska-asura-nirukta` [:1115](../../manuscript/as_endnotes.md#L1115) | **medium** — already corrected once; records that Yāska gives *three* explanations and does **not** contain *asurāḥ suravirodhinaḥ* | **verify** — and see the separate open item: its item (3) describes "surāḥ from good, asurāḥ from evil", but the text reads *soḥ* (from *su*) / *asoḥ* (from *asu*) |
| J2 | `samaveda-padapatha-asurasya-split` [:1133](../../manuscript/as_endnotes.md#L1133) | **none** — the segmentation witness; survives intact | **keep** |
| J3 | `nanartha-homonymy` [:906](../../manuscript/as_endnotes.md#L906) | **hard** — "For *asura*, Sanskrit's analytical record preserves **two derivational routes that do not share a semantic center**" | **rephrase** — the *nānārtha* apparatus and the *aja* case stay valid in general; their application to *asura* is the claim being retired |
| J4 | `sura-dhatu-dipti` [:930](../../manuscript/as_endnotes.md#L930) | **none** — ⟪सुर्⟫ *aiśvarya-dīptyoḥ* | keep |
| J5 | `rv-1-174-1-indra-asura` [:1046](../../manuscript/as_endnotes.md#L1046) | **medium** — deployment line reads "the first of the two mantras showing the Ṛgvedic protagonist *asura* as the ***asu-ra*** breath-bearer" | **rephrase** deployment line |
| J6 | `rv-1-24-14-varuna-asura` [:1065](../../manuscript/as_endnotes.md#L1065) | medium — same pattern | rephrase |
| J7 | `rv-agni-mitra-rudra-asura` [:1084](../../manuscript/as_endnotes.md#L1084) | **hard** — "The **life-force derivation** that makes Indra and Varuṇa *asura*…" and "generalizes the ***asu-ra*** (deed-earned holder…)" | **rephrase** |
| J8 | `rigvedic-named-antagonist-asuras` [:1187](../../manuscript/as_endnotes.md#L1187) | **verify** — supports D2; likely safe | verify |
| J9 | `rigveda-5-40-5-svarbhanu-eclipse` [:11](../../manuscript/as_endnotes.md#L11) | verify — must not assert Svarbhānu *is* the *a-sura* word | **verify** |
| J10 | `svarbhanu-svar-etymology` [:35](../../manuscript/as_endnotes.md#L35) | none — supports D4 | keep |
| J11 | `asura-reconstructed-lord-account` [:1145](../../manuscript/as_endnotes.md#L1145) | **medium** — serves F1 | rephrase with F1 |
| J12 | `asura-factional-framing` [:1159](../../manuscript/as_endnotes.md#L1159) | **none — the replacement thesis's own endnote** | **keep** |
| J13 | `asura-generativity-pie-double-standard` [:1443](../../manuscript/as_endnotes.md#L1443) | none | keep |
| J14 | `rigveda-adeva-privative` [:1431](../../manuscript/as_endnotes.md#L1431) | **none — strengthened**; *a-deva* is the privative the RV actually uses | **keep** |
| J15 | `rigveda-privative-generativity` [:1419](../../manuscript/as_endnotes.md#L1419) | none — *a-dabdha* 48/0 | keep |
| J16 | `maya-concealment-projection` [:1479](../../manuscript/as_endnotes.md#L1479) | **none — the *āvaraṇa*/*vikṣepa* endnote; the rewrite's centre of gravity** | **keep**; may need **expansion** |
| J17 | `rigveda-1-11-7-maya-mayin` [:1457](../../manuscript/as_endnotes.md#L1457) | none | keep |
| J18 | `maitrayani-samhita-1-9-3-satya-asura` [:1574](../../manuscript/as_endnotes.md#L1574) | none — corroborates | keep |
| J19 | `rv-3-55-asuratvam-ekam` [:1562](../../manuscript/as_endnotes.md#L1562) | **verify** — *asuratvam* as a shared property of the devas cuts against any two-word reading; may become an asset | **verify** |
| J20 | `bhagavad-gita-16-6-daiva-asura` [:1615](../../manuscript/as_endnotes.md#L1615) | **verify** — *daiva*/*āsura* **sampad** is a classification by conduct; likely supports the replacement | verify |
| J21 | `asura-standard-etymology-contested` [:5796](../../manuscript/as_endnotes.md#L5796) | **medium** — serves H8's "two words" paragraph in §19.8 | rephrase with H8 |
| J22 | `hayagriva-asura-vedas-theft` [:1293](../../manuscript/as_endnotes.md#L1293), `vrkasura-bhasmasura-boon-reversal` [:1345](../../manuscript/as_endnotes.md#L1345), `andhakasura-shiva-purana` [:1379](../../manuscript/as_endnotes.md#L1379), `rahu-manthana-svarbhanu-layering` [:6760](../../manuscript/as_endnotes.md#L6760) | none — narrative | keep |

---

## 4. Figures, reference docs, working plans

| # | ref | dependency | recommendation |
|---|---|---|---|
| K1 | `figures/pie_in_sky/deva_asura_vivimorphosis_chains.svg` → **Figure 19.9**, [as_1_19_pie_in_sky.md:322](../../manuscript/as_1_19_pie_in_sky.md#L322) | **hard if the figure labels a chain "*asu-ra* breath-bearer"** — the figure is outlined, so text is baked to paths; changing it means editing the source and re-outlining | **verify the figure's own labels first**, then decide |
| K2 | [reference/as_thesis_summary.md:130](../../reference/as_thesis_summary.md#L130) | **hard** — Claim 39: "The Veda **generates two words on one sound-form**… Yāska preserves both readings" | **rephrase** — and Yāska-preserves-both is separately wrong (see J1) |
| K3 | [reference/as_toc_annotated.md](../../reference/as_toc_annotated.md) | **verify** — §3.6's annotation and the Claims list; the three TOC files must stay in lockstep | verify all three |
| K4 | [reference/as_second_shanti.md](../../reference/as_second_shanti.md) (12 hits) | **verify** — series planning; may propagate the old thesis into later volumes | verify |
| K5 | **CLAUDE.md** [:832](../../CLAUDE.md#L832) | **hard, and highest-leverage** — the *Asuratva* block states the two-word thesis as project doctrine and is auto-loaded every session. Also still says "Yāska preserves both the *asu* analysis and *asurāḥ suravirodhinaḥ*", which `yaska-asura-nirukta` retracted | **rephrase — do this first**; until it changes, every future drafting pass re-imports the retired thesis |
| K6 | `working/10_active/as_asura_generativity_argument_deployment_codex.md`, `..._plan_claude.md`, `as_asura_synthesis_and_plan.md`, `as_ch03_06_asura_rewrite_lost_and_found_codex.md`, `asura_rigveda_occurrence_audit_codex.md` | **hard** — these are the plans that *built* the old thesis | **relocate** to `working/90_superseded/` once the rewrite lands, or annotate at the head |
| K7 | `working/40_reference/research/as_asura_sura_asurya_vedic_survey.md` §7.2 | **none — already recommends the replacement**: "reframe *asuratva* from 'not-light' to the measuring sovereignty turned to withholding" | **keep**; use as source |

---

## 5. Passages whose removal leaves surrounding prose incomplete

These cannot simply be deleted; each leaves a hole that the surrounding sentences reference.

1. **A5 → A6.** Removing the *bound*/*bounds* analogy strands "abandon **that ordinary clarity**" at A6, which has no other antecedent. Both move together.
2. **B7 → B8 → B9.** The *aja* parallel, the goat joke, and "follow the same pattern" form one three-beat argument. B9's "**the same** pattern" points at B7. Removing B9 alone leaves B7–B8 as a parallel to nothing; removing B7 alone leaves B9 dangling. **Treat as one unit.**
3. **B1/C1/D1 headings.** The subsection titles *are* the old thesis, and the body text under C and D refers back to them ("In these mantras…", "The *action* does"). Renaming requires re-reading each subsection's first and last sentence.
4. **A3 → H4 → H6.** The notation convention is declared once and invoked by name twice. **A3 must be settled before H4 or H6 can be written.** H4 says "Following the convention established there" — it breaks the moment A3 changes.
5. **G7 and G5/G6.** The "*sat*/*asat* — *asu-ra*/*a-sura* — swastika/pyramid" triple is a **refrain** appearing in §3.6 twice (G5 area and G7) and echoed at H6. Its middle term is the retired thesis. Changing one instance without the others breaks a deliberate repetition.
6. **H9, the Avestan chain.** "Preserves the breath-bearer, not the withholder" is the *conclusion* of §19's Iranian comparison. Removing it leaves the comparison without a result. This needs a replacement claim, not a deletion — flagged as the costliest single repair outside §3.6.
7. **E2, the attestation flank.** The *sura*-is-unattested concession sets up E3's generativity argument. Under the new thesis the concession is no longer damaging, but E2's *purpose clause* ("could not possibly generate *a-sura*") must be restated or E3 answers a question no longer asked.

---

## 6. Chapter-by-chapter rewrite map

| order | file | scale | blocked on | notes |
|---|---|---|---|---|
| **0** | **CLAUDE.md** (K5) | small, highest leverage | — | Doctrine. Fix before drafting anything, or the old thesis re-enters through the always-on context. Also carries a separately retracted Yāska claim. |
| **1** | **as_1_03_strategic.md §3.6** (A1–G8) | **large — 3 headings, ~14 rephrase, ~4 removals** | CLAUDE.md | The epicentre. Settle **A3 (the notation convention)** first; everything downstream inherits it. Units: (A5+A6), (B7+B8+B9), (B1/C1/D1 headings). Note how much already survives: A1, A4, D3, D4, D6, D7, G4, G8. |
| **2** | **as_endnotes.md** (J1–J22) | medium — 6 rephrase, ~6 verify | §3.6 | Deployment lines carry section names; update with the heading renames. J3 (`nanartha-homonymy`) is the substantive one. |
| **3** | **as_1_19_pie_in_sky.md §19.8** (H7–H9) | **medium-large** | §3.6 | H9 (Avestan) needs a *new* claim, not a cut. Check Figure 19.9's baked labels (K1). |
| **4** | **as_1_18_wrong_question.md** (H6) | small | §3.6 | One paragraph; a full restatement of the old thesis. |
| **5** | **as_1_04_fourth_abrahamic.md** (H3, H4) | small | A3 | H4 explicitly invokes the convention. |
| **6** | **reference/as_thesis_summary.md** Claim 39 (K2) | small | §3.6 | Public-facing; keep in step with the Claims list. |
| **7** | **reference/as_toc_annotated.md** + `as_toc.md` + `as_toc_notes.md` (K3) | small | §3.6 | Three-file lockstep per CLAUDE.md. |
| **8** | **as_3_10_glossary.md** (H12) | small — verify | §3.6 | *Asuratva* entry likely survives; check for orphaned siblings. |
| **9** | **reference/as_second_shanti.md** (K4) | verify | — | Stop the old thesis propagating into later volumes. |
| **10** | **working plans** (K6) | housekeeping | rewrite lands | Supersede or annotate. |

**Counts:** ~48 passages examined · **hard dependency 19** · medium 11 · low/none 18 ·
**keep 21 · rephrase 18 · remove 4 · relocate 2 · verify 12** (some overlap).

**The encouraging shape:** the replacement thesis is *already written* in §3.6 — A1, A4, D3, D4,
D6, D7, G4 and G8 state action-not-faction, *āvaraṇa*/*vikṣepa*, and "their names do not
determine their conduct" in the book's own voice. The rewrite is mostly **subtraction of the
two-word scaffolding from around an argument that already stands without it**, plus one genuinely
new claim needed at H9.

## 7. Open items this audit did not settle

- **Figure 19.9's baked label text** (K1) — not inspected; text is outlined to paths.
- **`yaska-asura-nirukta` item (3)** (J1) — the *soḥ*/*asoḥ* reading vs "good/evil"; separate from this rewrite but touches the same endnote.
- **Ch 2's *āvaraṇa*/*vikṣepa* setup** — §3.6 D7 says "Chapter 2 gives the two parts of this action precise terms." Ch 2 was not audited here; the rewrite leans harder on that setup, so it should be checked for sufficiency.
- **The four named replacement passages** — RV 8.96.9 and RV 10.124.5 do **not** currently appear in Ch 3; only 10.138.3 (Pipru, D2) and 5.40.5 (Svarbhānu) do. Introducing them is new material, not a repair.
