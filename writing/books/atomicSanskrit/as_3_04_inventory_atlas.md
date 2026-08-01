# Appendix Part 4 — The Subcontinental Sound-Field: Inventory Atlas and Control Surveys

---

Chapter 8 compares selected language groups by placing their consonant contrasts on one shared mouth-map. The four body figures show the southern subcontinent, the central forest belt, a Western Indo-European control, and a Central Asian control. Their selected sets cover 20, 18, 14, and 12 of the 23 Sanskrit base coordinates.

This appendix explains how the atlas was built and adds seven further surveys. The result is exploratory: coverage depends on the languages selected, the inventory source used for each language, and the decision about which reported sounds count as independent contrasts. The figures show an ordering in these samples and provide a method that can be repeated with other selections.

## 4.1 The Atlas Method in Depth

The atlas asks one physical question: when a language treats a consonant as a contrastive coordinate, where does that consonant sit on a shared mouth-map? It measures the body-anchored coordinates each language treats as independent contrastive slots — not vocabulary, descent, prestige, script, age, or any of the pyramid's classificatory buckets.[NOTE: language-hotzones-inventory-method]

**The horizontal axis contains twelve places.** Each language's consonants fall on a 12-column axis that runs from lips to glottis along the human vocal tract:

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

The five Sanskrit-named places (BIL, DEN, RET, PAL, VEL) use their *sthāna* names. The seven other columns use standard labels — Sanskrit's grid does not stop there. The five *sthāna* names define Sanskrit's selection from the broader anatomical space the human voice can reach.

**The vertical axis contains thirteen manners.** Thirteen manner rows describe how the consonant is shaped at its place: five stop rows (voiceless unaspirated, voiceless aspirated, voiced unaspirated, voiced aspirated, ejective), two affricate rows (voiceless, voiced), two fricative rows (voiceless, voiced), and one each for nasal, lateral, tap-or-trill, and approximant / glide. The two aspirated stop rows are Sanskrit's *mahāprāṇa* row pair, set apart by the strip preset described below. The ejective row appears for languages using the Caucasian or Native American glottal-pressure system; Sanskrit does not light it.

**The *mahāprāṇa*-strip preset isolates the base field.** Chapter 8 §8.3 defines a 23-cell Sanskrit base by setting aside the ten *mahāprāṇa* stop cells—**ख छ ठ थ फ** and **घ झ ढ ध भ**—running a sensitivity check rather than executing a demotion. Sanskrit's vertical breath axis remains structural, while Chapter 8 needs the base field isolated from the breath layer Sanskrit stacks on top. Before comparison, the preset removes manner rows 1 (voiceless aspirated) and 3 (voiced aspirated) from every language's harmonized cell set, systematically removing aspirated stops in any comparison language too. The atlas then measures coverage across the rows Sanskrit's base lights rather than across all manner rows.[NOTE: inventory-atlas-coverage-surveys]

**The field-versus-coordinate distinction keeps the comparison honest.** Chapter 8 §8.2 introduces it; the full treatment is here.

A *spoken sound-field* is the set of acoustic realizations a language's speakers can and do produce. It includes allophonic variation, contextual realization, dialect-level variation, and the long tail of phonetic detail a careful field-phonetician would record.

A *sonomeric coordinate* is a contrastive unit the language promotes into its inventory as an independent slot. Two sounds occupy two coordinates only if the language treats them as distinct word-making units.

While Tamil speakers produce voiced stop sounds in real speech, Tamil's contrastive inventory does not promote those voiced realizations to independent voiced-stop coordinates the way Sanskrit does. The atlas strictly records the latter rather than the former. The same caution governs aspirated stops, palatal-versus-post-alveolar distinctions, and any other case where a language's spoken field contains material its inventory does not formally credit. The atlas operates at the inventory layer, mirroring how Sanskrit's engineering itself operates at the inventory layer.

**The coverage criterion is union, not ranking.** For each three-language comparison set, a Sanskrit cell counts as *covered* if at least one of the three languages lights it. Chapter 8 asks whether the subcontinental field — or some other region — supplies enough material to make Sanskrit's base recoverable. Union coverage tests that proposition without conflating it with per-language ranking.

Three languages collectively covering 20 of 23 cells does not mean each language contains 20 of those cells; it means the union of their three inventories intersects Sanskrit's base in 20 places. A language that contributes three or four cells can still carry weight if those cells are otherwise unfilled.

**Inventory provenance is open.** The eleven surveys are computed against a harmonized set of phonemic inventories drawn from standard linguistic descriptions per language. The Python generator `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py` stores every inventory in one place alongside its reference work — Padgett (2003) and Yanushevskaya & Bunčić (2015) for Russian; Tegey & Robson (1996) and Bečka (1969) for Pashto; Schulze (2000), Stilo (2008), and Pirejko (1976) for Talysh; and so on for each comparison language. Anyone who wants to test an alternative inventory choice can edit the file, regenerate the JSON, and rebuild the figure. The reproducibility bundle ships with the figure pipeline.

The inventory choices are conservative and editorial. Verification flags live in `working/40_reference/research/inventory_atlas_coverage_surveys.md` §5: Pashto's full retroflex set, Greek's lack of phonemic /h/, the aspirated/ejective affricate collapse found in Armenian and Georgian, the single Burushaski symbol (ʈʂ) the harmonizer's manner taxonomy does not have a row for. The data trail is visible to any reader who wants it.

The Korku chart uses this conservative policy. Nagaraja's grammar describes a richer retroflex inventory than the atlas currently displays, including retroflex aspirates, a retroflex flap, and a retroflex lateral.[NOTE: korku-nagaraja-mouth-mind-evidence] Adding those sounds would enrich the Korku chart, but it would not change the present 18-of-23 base-coverage result: the *mahāprāṇa* preset removes the aspirated rows, while the added retroflex flap and lateral occupy coordinates outside the 23 Sanskrit base cells counted here. The appendix therefore reports the current count while making the fuller inventory visible.

The method is narrow and reproducible. It turns Chapter 8's comparison into numbers the reader can audit.

## 4.2 Santali-Inclusive Munda Control: 18 of 23

The body's Forest-Belt Survey set Santali aside because the machinery treats Santali as Indic-influenced. The substitution costs nothing: Korku, Mundari, and Santali cover the same 18 of 23 cells Korku + Mundari + Ho covers.

The unfilled letters match the body set too: **ण · स · ष · श · ल**. The *dantya* / *tālavya* line where Sanskrit's place-coding decisions diverge from the broader subcontinental alveolar / post-alveolar placement is the same set of cells.

![Figure A.4.1 — Munda Survey: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Santali cover the same 18 cells the body's Forest-Belt Survey covers, with the same unfilled set (ण · स · ष · श · ल).](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=100%}

Santali's heavier Indic absorption does not move the count in this substitution. The unfilled cells are not what Santali borrowed from Sanskrit; they are what Sanskrit chose to place differently from the broader subcontinental field. Both sampled forest-belt sets cover 18 of Sanskrit's 23 base coordinates.

## 4.3 Santali-Free Mixed Control: 18 of 23

The Mixed Control swaps Santali for Burushaski — the Hunza Valley language-isolate sitting outside every family tree assigned within the subcontinent — and pairs it with Korku and Mundari.

![Figure A.4.2 — Mixed Control: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Burushaski reach the same 18-cell coverage as the all-Munda control; Burushaski's retroflex inventory exchanges one unfilled cell for another but does not move the count.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=100% height=80%}

The count remains 18 of 23. The unfilled set shifts: **ण · स · श · ल · र**. Burushaski's retroflex inventory covers cells the all-Munda set leaves open, but trades the gain against the alveolar tap / trill र, which Burushaski places at a different coordinate.

The substitution forecloses two of the pyramid's deflections at once. Santali is excluded — Indic absorption cannot explain the coverage. The all-Munda framing is broken — family resemblance cannot explain it either. The geographic explanation survives: three languages drawn from three different pyramid classifications, all sitting in or adjacent to the central forest belt and the north-western frontier, cover the same 18 cells the Forest-Belt and Munda Surveys cover.

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 15 of 23

The machinery classifies Munda alongside two other branches under the umbrella *"Austro-Asiatic"*: a Khasian branch in the Meghalaya highlands and a Nicobaric branch on the Nicobar Islands. The three branches sit at geographically remote subcontinental poles.

The Dispersed Survey picks one representative from each branch: Sora (South Munda, Eastern Ghats and Rushikulya basin), Khasi (Meghalaya highlands), and Nicobarese (Car Nicobar). Coverage falls to 15 of 23. The unfilled set expands to **ट · ड · ण · स · ष · श · ल · र** — eight cells, three more than the Munda-pure Forest-Belt set the body uses.

![Figure A.4.3 — Dispersed Survey: 15 of 23 Sanskrit base coordinates. Sora, Khasi, and Nicobarese — three languages the machinery classifies under one *"Austro-Asiatic"* umbrella across three remote subcontinental poles — cover three fewer cells than the all-Munda Forest-Belt Survey.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=100%}

The single pyramid label *"Austro-Asiatic"* places these three languages in one family, but the selected inventories have sharply different shapes. Sora's South Munda inventory lacks the retroflex stops found in North Munda; Khasi uses voiceless-aspirated stops; Nicobarese uses neither retroflex nor aspirated stops in the inventory selected here. Their union covers less of Sanskrit's base than the all-Munda forest-belt samples.

In these samples, the family label does not describe the shared inventory shape. The three languages also come from remote regions of the subcontinent, so family and geography cannot be separated without a larger controlled sample.

## 4.5 Northwest Frontier Survey: 20 of 23

Three north-western contact-zone languages — Pashto (*"Iranian"* by the pyramid's label, Afghanistan and Pakistan tribal belt), Nuristani (a separate IE branch isolated in the Hindu Kush valleys), and Burushaski (the Hunza Valley isolate) — cover 20 of 23, the deepest result in the survey. The unfilled cells are exactly the three the body's Southern Survey (Tamil + Toda + Kurukh) leaves unfilled: **ल · स · श**.

![Figure A.4.4 — Northwest Frontier Survey: 20 of 23 Sanskrit base coordinates. Pashto, Nuristani, and Burushaski cover the same 20 cells the deep-south Tamil + Toda + Kurukh set covers, with the same unfilled triple (ल · स · श). Two geographically opposite ends of the subcontinent deliver the same count.](figures/superset/sk_pashto_nuristani_burushaski.svg){#fig:app4-nw-frontier-survey width=100% height=80%}

Two geographically opposite sets — deep south and north-western frontier — deliver the same count with the same unfilled list. Both regions sit inside the subcontinental retroflex contact zone; both contain the cells Sanskrit's base lights.

The set presents a taxonomically mixed profile. The pyramid's label classifies Pashto as *"Iranian"*, the machinery classifies Nuristani as a separate IE branch neither Indic nor Iranian, and Burushaski stands as a language-isolate. Despite those different labels, the selected frontier set ties the southern set. Its inventories use retroflex contrasts associated with the same broad subcontinental contact zone that the deep-south languages preserve.

## 4.6 Iranian Survey: 13 of 23 (Non-Contact Zone)

Three Iranian languages outside the north-western contact zone — Farsi (Iran), Kurdish Kurmanji (northern Iraq, Syria, eastern Turkey), and Talysh (Caspian littoral, Azerbaijan and northern Iran) — cover only 13 of 23, the geographic mirror image of the Northwest Frontier Survey. The unfilled set runs **ट · च · ड · ज · ण · ञ · स · ष · श · र**: ten cells, including the entire retroflex column.

![Figure A.4.5 — Iranian Survey: 13 of 23 Sanskrit base coordinates. Three Iranian languages outside the north-western subcontinental contact zone cover the same number of Sanskrit's base cells as three random external languages. The retroflex column the Northwest Frontier Survey lit is here entirely unfilled.](figures/superset/sk_farsi_kurdish_talysh.svg){#fig:app4-iranian-survey width=100% height=80%}

The 13/23 number is the same coverage a random external English + Arabic + Farsi mix delivers. Three languages the pyramid classifies as Sanskrit's "Iranian sister branch" cousins cover no more of Sanskrit's base than three external languages do.

The contact / non-contact comparison explains the three-cell change in this pair of samples. Swapping Talysh for Balochi — a north-western frontier Iranian language that uses retroflex contrasts from the subcontinental contact zone — moves coverage from 13 to 16. The exact increase comes from the retroflex coordinates **ट · ड · र** that Balochi uses and Caspian-littoral Talysh does not. The shared "Iranian" classification alone does not explain the difference.

## 4.7 Caucasus Survey: 10 of 23

Three languages from three different pyramid classifications, all from the Caucasus region — Armenian (a separate IE branch), Georgian (Kartvelian / South Caucasian, outside the IE classification altogether), and Ossetian (Iranian, north Caucasus) — fall to 10 of 23, the floor of the eleven-survey set. The unfilled list runs **ट · च · ड · ज · ण · ञ · ङ · स · ष · श · ल · र · व**: thirteen cells, the largest unfilled list of any survey.

![Figure A.4.6 — Caucasus Survey: 10 of 23 Sanskrit base coordinates. Three pyramid classifications meet in one geographic region, and this selected set produces the lowest coverage among the eleven surveys.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=100% height=80%}

Three pyramid classifications meet inside one geographic region, yet the selected set reaches only 10 of 23. This is the lowest coverage among the eleven samples.

## 4.8 Slavic & Caucasus IE Survey: 11 of 23

The Slavic & Caucasus IE Survey runs three IE-classified languages along the steppe corridor: Russian and Ukrainian from East Slavic, Ossetian from Caucasian Iranian. Coverage reaches 11 of 23, one cell above the Caucasus floor.

![Figure A.4.7 — Slavic & Caucasus IE Survey: 11 of 23 Sanskrit base coordinates. Three IE-classified languages along the steppe corridor cover only one cell more than the Caucasus floor — and considerably less than the body's Western IE and Central Asian sets.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=100% height=80%}

All three languages share the pyramid's "Indo-European" label that supposedly makes them Sanskrit's relatives. East Slavic and Caucasian Iranian together cover less of Sanskrit's base than the body's Western IE Survey at 14/23 and the Central Asian Tajik + Kazakh + Kyrgyz set at 12/23. Across the selected IE-classified sets, coverage ranges from 11/23 to 20/23 and rises in the sets drawn closer to the subcontinental contact zone.

The steppe corridor — which the pyramid's Aryan-migration story frequently cites as the source field — supplies less of Sanskrit's base material than the deep south, the central forest belt, or the north-western frontier.

## 4.9 The Coverage Cascade

The eleven surveys — four in the body and seven in this appendix — produce the following sample ordering. Sets drawn from the subcontinent and its north-western contact zone occupy the higher rows, while the selected Caucasus and steppe sets occupy the lower rows. A larger preregistered sample would be needed to establish that ordering as a general geographic pattern.

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

**The selected sets closer to the subcontinent show higher coverage.** The two 20/23 results appear at geographically opposite poles — the deep-south Tamil + Toda + Kurukh set and the north-western Pashto + Nuristani + Burushaski set. Both sit inside the subcontinental retroflex contact zone and cover the same 20 cells, with the same three unfilled letters (**ल · स · श**). The selected Caucasus set produces the lowest result at 10/23.

**The pyramid's "Indo-European" classification does not explain the variation within these samples.** The IE-classified sets range from 11/23 to 20/23. Pashto + Nuristani at the high end carry the same broad IE label as Russian + Ukrainian + Ossetian at the low end, while their positions relative to the subcontinental contact zone differ.

**The selected Iranian languages divide along the contact axis.** Pashto and Balochi, inside the north-western subcontinental contact zone, use retroflex contrasts and contribute to the higher coverage there. Farsi, Kurdish, and Talysh, outside that zone, deliver 13/23 in the selected set. The shared Iranian label does not explain that difference by itself.

**The *"Austro-Asiatic"* samples also vary by geography and branch.** Munda languages inside the central forest belt deliver 18/23, while the dispersed Sora + Khasi + Nicobarese set delivers 15/23. The broad family label does not remove the differences among their sound-fields.

**The body's four figures occupy four points in the larger sample ordering.** Southern Survey (20), Forest-Belt Survey (18), Western IE Survey (14), and Central Asian Survey (12) form the sequence used in Chapter 8. The seven appendix surveys show that several alternate selections reproduce parts of that ordering, while also showing how much the result depends on the chosen languages and inventory descriptions.

Across these samples, Sanskrit's base coordinates receive their highest coverage from the southern, central forest-belt, and north-western fields of the subcontinent. The machinery sorts those languages into different families, yet the selected inventories repeatedly recover much of the same Sanskrit base. This exploratory result is consistent with the engineering thesis and creates a reproducible test for the transported-cargo story.
