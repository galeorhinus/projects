# Appendix Part 4 — The Subcontinental Sound-Field: Inventory Atlas and Control Surveys

---

Chapter 8 surveys the subcontinental sound-field through four figures: the deep-south Southern Survey, the Santali-free Forest-Belt Survey, the Western IE control, and the Central Asian control. The polemic ladder lands cleanly at four step-points (20, 18, 14, 12 of 23 Sanskrit base coordinates).

This appendix carries the empirical material the body's four-step ladder rests on: the atlas methodology in depth, the seven control surveys the body could not fit, and the eleven-survey coverage cascade.

## 4.1 The Atlas Method in Depth

The atlas asks one physical question: when a language treats a consonant as a contrastive coordinate, where does that consonant sit on a shared mouth-map? It measures the body-anchored coordinates each language treats as independent contrastive slots — not vocabulary, descent, prestige, script, age, or any of the pyramid's classificatory buckets.[NOTE: language-hotzones-inventory-method]

**The horizontal axis carries twelve places.** Each language's consonants land on a 12-column axis that runs from lips to glottis along the human vocal tract:

| Col | Sanskrit anchor | Standard label | Body location |
|---:|---|---|---|
| 0 | **ओष्ठ्य** (*oṣṭhya*) | bilabial | both lips meeting |
| 1 | — | labio-dental | lower lip to upper teeth |
| 2 | — | interdental | tongue tip between teeth |
| 3 | **दन्त्य** (*dantya*) | dental | tongue against upper teeth |
| 4 | — | alveolar | tongue against alveolar ridge |
| 5 | — | post-alveolar | tongue blade behind alveolar ridge |
| 6 | **मूर्धन्य** (*mūrdhanya*) | retroflex | tongue tip curled toward palate ridge |
| 7 | **तालव्य** (*tālavya*) | palatal | tongue body toward hard palate |
| 8 | **कण्ठ्य** (*kaṇṭhya*) | velar | tongue back toward soft palate |
| 9 | — | uvular | tongue back against uvula |
| 10 | — | pharyngeal | tongue root toward pharynx wall |
| 11 | — | glottal | vocal folds |

The five Sanskrit-named places (BIL, DEN, RET, PAL, VEL) carry their *sthāna* names. The seven other columns carry standard labels — Sanskrit's grid does not stop there. The five *sthāna* names define Sanskrit's selection from the broader anatomical space the human voice can reach.

**The vertical axis carries thirteen manners.** Thirteen manner rows describe how the consonant is shaped at its place: five stop rows (voiceless unaspirated, voiceless aspirated, voiced unaspirated, voiced aspirated, ejective), two affricate rows (voiceless, voiced), two fricative rows (voiceless, voiced), and one each for nasal, lateral, tap-or-trill, and approximant / glide. The two aspirated stop rows are Sanskrit's *mahāprāṇa* row pair, set apart by the strip preset described below. The ejective row appears for languages carrying the Caucasian or Native American glottal-pressure system; Sanskrit does not light it.

**The mahāprāṇa-strip preset isolates the base field.** Chapter 8 §8.3 defines a 23-cell Sanskrit base by holding aside the ten *mahāprāṇa* stop cells: **ख छ ठ थ फ** and **घ झ ढ ध भ**. Sensitivity check, not demotion. Sanskrit's vertical breath axis remains structural; Chapter 8 needs the base field isolated from the breath layer Sanskrit stacks on top. The preset removes manner rows 1 (voiceless aspirated) and 3 (voiced aspirated) from every language's harmonized cell set before comparison. Aspirated stops in any comparison language are removed too. The atlas then measures coverage across the rows Sanskrit's base lights, not across all manner rows.[NOTE: inventory-atlas-coverage-surveys]

**The field-versus-coordinate distinction keeps the comparison honest.** Chapter 8 §8.2 introduces it; the full depth lands here.

A *spoken sound-field* is the set of acoustic realizations a language's speakers can and do produce. It includes allophonic variation, contextual realization, dialect-level variation, and the long tail of phonetic detail a careful field-phonetician would record.

A *sonomeric coordinate* is a contrastive unit the language promotes into its inventory as an independent slot. Two sounds occupy two coordinates only if the language treats them as distinct word-making units.

Tamil speakers produce voiced stop sounds in real speech. Tamil's contrastive inventory does not promote those voiced realizations to independent voiced-stop coordinates the way Sanskrit does. The atlas records the latter, not the former. The same caution governs aspirated stops, palatal-versus-post-alveolar distinctions, and any other case where a language's spoken field contains material its inventory does not formally credit. The atlas operates at the inventory layer because Sanskrit's engineering operates at the inventory layer.

**The coverage criterion is union, not ranking.** For each three-language comparison set, a Sanskrit cell counts as *covered* if at least one of the three languages lights it. Chapter 8 asks whether the subcontinental field — or some other region — supplies enough material to make Sanskrit's base recoverable. Union coverage answers that question without conflating it with per-language ranking.

Three languages collectively covering 20 of 23 cells does not mean each language carries 20 of those cells; it means the union of their three inventories intersects Sanskrit's base in 20 places. A language that contributes three or four cells can still be load-bearing if those cells are otherwise unfilled.

**Inventory provenance is open.** The eleven surveys are computed against a harmonized set of phonemic inventories drawn from standard linguistic descriptions per language. The Python generator `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py` carries every inventory in one place alongside its reference work — Padgett (2003) and Yanushevskaya & Bunčić (2015) for Russian; Tegey & Robson (1996) and Bečka (1969) for Pashto; Schulze (2000), Stilo (2008), and Pirejko (1976) for Talysh; and so on for each comparison language. Anyone who wants to test an alternative inventory choice can edit the file, regenerate the JSON, and rebuild the figure. The reproducibility bundle ships with the figure pipeline.

The inventory choices are conservative and editorial. Verification flags live in `working/inventory_atlas_coverage_surveys.md` §5: Pashto's full retroflex set, Greek's lack of phonemic /h/, the aspirated/ejective affricate collapse Armenian and Georgian carry, the single Burushaski symbol (ʈʂ) the harmonizer's manner taxonomy does not have a row for. The data trail is visible to any reader who wants it.

The method is narrow and reproducible. It makes Chapter 8's question answerable in numbers the reader can audit.

## 4.2 Santali-Inclusive Munda Control: 18 of 23

The body's Forest-Belt Survey held Santali aside because the machinery treats Santali as Indic-influenced. The substitution costs nothing: Korku, Mundari, and Santali cover the same 18 of 23 cells Korku + Mundari + Ho covers.

The unfilled letters match the body set too: **ण · स · ष · श · ल**. The *dantya* / *tālavya* line where Sanskrit's place-coding decisions diverge from the broader subcontinental alveolar / post-alveolar placement is the same set of cells.

![Figure A.4.1 — Munda Survey: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Santali cover the same 18 cells the body's Forest-Belt Survey covers, with the same unfilled set (ण · स · ष · श · ल).](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=100%}

Santali's heavier Indic absorption does not move the count. The unfilled cells are not what Santali borrowed from Sanskrit; they are what Sanskrit chose to place differently from the broader subcontinental field. Switching Ho for Santali leaves the geographic verdict intact. The forest belt carries 18 of Sanskrit's 23 base coordinates regardless of which three forest-belt languages are sampled.

## 4.3 Santali-Free Mixed Control: 18 of 23

The Mixed Control swaps Santali for Burushaski — the Hunza Valley language-isolate sitting outside every family tree the subcontinent carries — and pairs it with Korku and Mundari.

![Figure A.4.2 — Mixed Control: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Burushaski reach the same 18-cell coverage as the all-Munda control; Burushaski's retroflex inventory exchanges one unfilled cell for another but does not move the count.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=100%}

The count holds at 18 of 23. The unfilled set shifts: **ण · स · श · ल · र**. Burushaski's retroflex inventory covers cells the all-Munda set leaves open, but trades the gain against the alveolar tap / trill र, which Burushaski places at a different coordinate.

The substitution forecloses two of the pyramid's deflections at once. Santali is excluded — Indic absorption cannot explain the coverage. The all-Munda framing is broken — family resemblance cannot explain it either. The geographic explanation survives: three languages drawn from three different pyramid classifications, all sitting in or adjacent to the central forest belt and the north-western frontier, cover the same 18 cells the Forest-Belt and Munda Surveys cover.

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 15 of 23

The machinery classifies Munda alongside two other branches under the umbrella *"Austro-Asiatic"*: a Khasian branch in the Meghalaya highlands and a Nicobaric branch on the Nicobar Islands. The three branches sit at geographically remote subcontinental poles.

The Dispersed Survey picks one representative from each branch: Sora (South Munda, Eastern Ghats and Rushikulya basin), Khasi (Meghalaya highlands), and Nicobarese (Car Nicobar). Coverage falls to 15 of 23. The unfilled set expands to **ट · ड · ण · स · ष · श · ल · र** — eight cells, three more than the Munda-pure Forest-Belt set the body uses.

![Figure A.4.3 — Dispersed Survey: 15 of 23 Sanskrit base coordinates. Sora, Khasi, and Nicobarese — three languages the machinery classifies under one *"Austro-Asiatic"* umbrella across three remote subcontinental poles — cover three fewer cells than the all-Munda Forest-Belt Survey.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=100%}

The single pyramid label *"Austro-Asiatic"* predicts that these three languages should share structural sound-field properties. They do not. Sora's South Munda inventory lacks the retroflex stops North Munda carries; Khasi runs voiceless-aspirated stops as the Mon-Khmer signature; Nicobarese carries neither retroflex nor aspirated stops. Three languages under one manufactured umbrella deliver three different inventory shapes, and their union covers less of Sanskrit's base than any all-subcontinental control.

The family label is not structural. Geography is structural — and inside the *"Austro-Asiatic"* umbrella the geography is dispersed across three remote regions of the subcontinent.

## 4.5 Northwest Frontier Survey: 20 of 23

This is the deepest result in the appendix.

Three north-western contact-zone languages — Pashto (*"Iranian"* by the pyramid's label, Afghanistan and Pakistan tribal belt), Nuristani (a separate IE branch isolated in the Hindu Kush valleys), and Burushaski (the Hunza Valley isolate) — cover 20 of 23. The unfilled cells are exactly the three the body's Southern Survey (Tamil + Toda + Kurukh) leaves unfilled: **ल · स · श**.

![Figure A.4.4 — Northwest Frontier Survey: 20 of 23 Sanskrit base coordinates. Pashto, Nuristani, and Burushaski cover the same 20 cells the deep-south Tamil + Toda + Kurukh set covers, with the same unfilled triple (ल · स · श). Two geographically opposite ends of the subcontinent deliver the same count.](figures/superset/sk_pashto_nuristani_burushaski.svg){#fig:app4-nw-frontier-survey width=100%}

Two geographically opposite sets — deep south and north-western frontier — deliver the same count with the same unfilled list. Both regions sit inside the subcontinental retroflex contact zone; both carry the cells Sanskrit's base lights.

The set is taxonomically mixed. Pashto is *"Iranian"* by the pyramid's label; Nuristani is a separate IE branch the machinery classifies neither as Indic nor as Iranian; Burushaski is a language-isolate. The three pyramid classifications collide inside one geographic outcome — and the outcome ties the southern set. The frontier inventories acquired the retroflex column from the same subcontinental contact zone the deep-south languages preserve. The geography predicts the count; the classifications do not.

## 4.6 Iranian Survey: 13 of 23 (Non-Contact Zone)

The Iranian Survey is the Northwest Frontier Survey's geographic mirror image.

Three Iranian languages outside the north-western contact zone — Farsi (Iran), Kurdish Kurmanji (northern Iraq, Syria, eastern Turkey), and Talysh (Caspian littoral, Azerbaijan and northern Iran) — cover only 13 of 23. The unfilled set runs **ट · च · ड · ज · ण · ञ · स · ष · श · र**: ten cells, including the entire retroflex column.

![Figure A.4.5 — Iranian Survey: 13 of 23 Sanskrit base coordinates. Three Iranian languages outside the north-western subcontinental contact zone cover the same number of Sanskrit's base cells as three random external languages. The retroflex column the Northwest Frontier Survey lit is here entirely unfilled.](figures/superset/sk_farsi_kurdish_talysh.svg){#fig:app4-iranian-survey width=100%}

The 13/23 number is the same coverage a random external English + Arabic + Farsi mix delivers. Three languages the pyramid classifies as Sanskrit's "Iranian sister branch" cousins cover no more of Sanskrit's base than three external languages do.

The contact / non-contact axis carries the explanation. Swapping Talysh for Balochi — a north-western frontier Iranian language that did acquire retroflex from the subcontinental contact zone — moves coverage from 13 to 16. The exact 3-cell jump is the retroflex column **ट · ड · र** Balochi carries and Caspian-littoral Iranian does not. The "Iranian" classification predicts nothing once contact is held constant.

## 4.7 Caucasus Survey: 10 of 23

Caucasus Survey: floor of the eleven-survey set.

Three languages from three different pyramid classifications, all from the Caucasus region: Armenian (a separate IE branch), Georgian (Kartvelian / South Caucasian, outside the IE classification altogether), and Ossetian (Iranian, north Caucasus). Coverage falls to 10 of 23 — lower than any other survey in the set. The unfilled list runs **ट · च · ड · ज · ण · ञ · ङ · स · ष · श · ल · र · व**: thirteen cells, the largest unfilled list of any survey.

![Figure A.4.6 — Caucasus Survey: 10 of 23 Sanskrit base coordinates. Three pyramid classifications collide in one geographic region — and the floor coverage of all eleven surveys appears at exactly that point. Geographic distance from the subcontinent is what moves the number.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=100%}

Three pyramid classifications collide inside one geographic region. None rescues the coverage. The Caucasus sits far enough from the subcontinent that geographic distance dominates. The floor lands here.

## 4.8 Slavic & Caucasus IE Survey: 11 of 23

The Slavic & Caucasus IE Survey runs three IE-classified languages along the steppe corridor: Russian and Ukrainian from East Slavic, Ossetian from Caucasian Iranian. Coverage reaches 11 of 23, one cell above the Caucasus floor.

![Figure A.4.7 — Slavic & Caucasus IE Survey: 11 of 23 Sanskrit base coordinates. Three IE-classified languages along the steppe corridor cover only one cell more than the Caucasus floor — and considerably less than the body's Western IE and Central Asian sets.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=100%}

All three languages share the pyramid's "Indo-European" label that supposedly makes them Sanskrit's relatives. East Slavic and Caucasian Iranian together cover less of Sanskrit's base than the body's Western IE Survey at 14/23, and considerably less than the Central Asian Tajik + Kazakh + Kyrgyz at 12/23 — itself classified as a mix the pyramid classifies as "Iranian" and "Turkic". The IE-classified sets span 11/23 to 20/23 depending only on which IE languages sat geographically close to the subcontinental contact zone.

The steppe corridor — frequently cited as the source field in the pyramid's Aryan-migration story — supplies less of Sanskrit's base material than the deep south, the central forest belt, or the north-western frontier.

## 4.9 The Coverage Cascade

The eleven surveys — four in the body, seven in this appendix — stack into a monotone cascade. Geography produces the signal. Family-tree classification produces noise on top of it.

| Coverage | Set | Languages | Source |
|---:|---|---|---|
| **20 / 23** | Southern Survey | Tamil + Toda + Kurukh | body (Ch 8 §8.6) |
| **20 / 23** | Northwest Frontier | Pashto + Nuristani + Burushaski | App 4 §4.5 |
| 18 / 23 | Forest-Belt Survey | Korku + Mundari + Ho | body (Ch 8 §8.7) |
| 18 / 23 | Munda Survey | Korku + Mundari + Santali | App 4 §4.2 |
| 18 / 23 | Mixed Control | Korku + Mundari + Burushaski | App 4 §4.3 |
| 15 / 23 | Dispersed *"Austro-Asiatic"* | Sora + Khasi + Nicobarese | App 4 §4.4 |
| 14 / 23 | Western IE Survey | English + French + Greek | body (Ch 8 §8.8) |
| 13 / 23 | Iranian Survey (non-contact) | Farsi + Kurdish + Talysh | App 4 §4.6 |
| 12 / 23 | Central Asian Survey | Tajik + Kazakh + Kyrgyz | body (Ch 8 §8.8) |
| 11 / 23 | Slavic & Caucasus IE | Russian + Ukrainian + Ossetian | App 4 §4.8 |
| **10 / 23** | Caucasus Survey | Armenian + Georgian + Ossetian | App 4 §4.7 |

**Geographic distance from the subcontinent predicts coverage.** The two 20/23 ceilings appear at geographically opposite poles — the deep-south Tamil + Toda + Kurukh set and the north-western Pashto + Nuristani + Burushaski set. Both sit inside the subcontinental retroflex contact zone. Both cover the same 20 cells with the same three unfilled letters (**ल · स · श**). At the other end, the Caucasus Survey delivers 10/23 — the lowest of the eleven — because the Caucasus is far enough from the subcontinent that no classification rescues the coverage.

**The pyramid's "Indo-European" classification does not predict coverage.** Inside the IE-classified set the spread is 11/23 to 20/23 — a nine-cell range driven entirely by geography. Pashto + Nuristani at the high end carry the same IE label as Russian + Ukrainian + Ossetian at the low end. The classification is structurally inert.

**The pyramid's "Iranian sister branch" claim collapses on the contact axis.** Pashto and Balochi — Iranian languages inside the north-western subcontinental contact zone — carry the retroflex column and contribute heavily to the 20/23 NW Frontier ceiling. Farsi, Kurdish, and Talysh — Iranian languages outside the contact zone — deliver 13/23, the same coverage three random external languages do. The Iranian classification predicts nothing once contact is held constant.

**The *"Austro-Asiatic"* family label fails the same test.** Munda inside the central forest belt delivers 18/23. The same family label across dispersed subcontinental geography (Sora + Khasi + Nicobarese) delivers 15/23. The label flattens three different sound-fields.

**The body's four-step ladder hits the cascade at four step-points.** Southern Survey (20), Forest-Belt Survey (18), Western IE Survey (14), Central Asian Survey (12) — each step is a measurable falling-off from the subcontinental ceiling. The seven appendix controls confirm that each step is real, is not driven by which three languages a survey set happens to use, and persists across alternate language choices the pyramid might insist on.

Sanskrit's base coordinates are subcontinental. They live in the subcontinental mouth — south, central, north-western — across languages the machinery sorts into three different family classifications, and across languages the pyramid denies any classificatory relationship to. The classifications do not move the count. The geography does. The engineering thesis is consistent with the field. The transported-cargo story is not.

---

## Draft notes (Appendix Part 4 v1 — first complete draft, 2026-06-08)

**Purpose:** field-level supplement to Chapter 8. The body chapter runs a four-step polemic ladder (Southern, Forest-Belt, Western IE, Central Asian); this appendix carries the seven controls and the deep methodology so the body chapter can stay compact without losing the empirical backbone.

**Section spine:**

- §4.1 atlas method in depth
- §§4.2–4.8 seven control surveys, one figure each
- §4.9 coverage cascade with the four polemic conclusions (geographic monotone; IE classification inert; Iranian contact-vs-non-contact; AA family label inert)

**Cross-references:** Chapter 8 §8.7 promises this appendix. §4.5 (NW Frontier 20/23) and §4.6 (non-contact Iranian 13/23) feed Chapter 16's retroflex-fingerprint argument.

**Figures:** all 11 surveys at `figures/superset/sk_*.svg`; generator and per-language sources at `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py`.

**Working trail:** `working/inventory_atlas_coverage_surveys.md` — per-figure metadata, verification queue, canvas-dimension table.

**Pending verifications** (carried in the working doc §5):

- Pashto's full retroflex set — Tegey & Robson; conservative drop of ɭ / ʐ unlikely to budge the 20/23 ceiling
- Greek's lack of phonemic /h/ — would add 1 cell at GLO if restored
- Burushaski's unclassified ʈʂ — atlas manner taxonomy has no retroflex-affricate row
- Aspirated / ejective affricate collapse in Armenian and Georgian — atlas tracks place × manner but not ejective-vs-aspirated for affricates
