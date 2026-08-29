# Appendix Part 4 — The Consonant Inventory Atlas and Additional Surveys

---

Chapter 8 compares selected language groups by placing their consonant contrasts on one shared mouth-map. The four body figures use a dispersed Dravidian-language set, the central forest belt, a Western Indo-European control, and a Central Asian control. Their selected sets cover 22, 20, 16, and 15 of the 23 Sanskrit base cells.

This appendix explains how the atlas was built and adds seven further surveys. The result is exploratory: coverage depends on the languages selected, the inventory source used for each language, and the decision about which reported sounds count as independent contrasts. The figures show an ordering in these samples and provide a method that can be repeated with other selections.

Together, the body and appendix map the **subcontinental superset** introduced in Chapter 8. Each regional survey captures part of that larger inventory; no individual language contains the whole. Sanskrit's twenty-three base cells provide the comparison target, while additional regional consonants demonstrate that the superset is larger than Sanskrit's selected grid.

## 4.1 The Atlas Method in Depth

The atlas asks one physical question: when a language treats a consonant as an independent contrast, where does the mouth produce it? The shared map places that consonant at its articulatory coordinates and records which positions each language keeps as independent grid addresses. It does not compare vocabulary, descent, prestige, script, age, or any of the pyramid's classificatory buckets.[NOTE: language-hotzones-inventory-method]

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

The figures abbreviate the five Sanskrit-named places as BIL, DEN, RET, PAL, and VEL. Those columns use their स्थान (*sthāna*) names; the other seven use standard labels. The five स्थान (*sthāna*) names define Sanskrit's selection from the broader anatomical space the human voice can reach.

Sanskrit's traditional categories and the comparison grid divide that space differently. Chapter 8 Figure 8.1 retains Sanskrit's own classification. The atlas compares actual pronunciation across languages. It therefore places Sanskrit **र** and **ल** with Tamil **ர** and **ல** in their shared alveolar cells. It also places Sanskrit **स** with the alveolar **s** used by Toda, Kurukh, and the forest-belt languages. This translation allows identical pronunciations to meet without altering Sanskrit's internal arrangement.

**The vertical axis contains thirteen manners.** Thirteen manner rows describe how the consonant is shaped at its place: five stop rows (voiceless unaspirated, voiceless aspirated, voiced unaspirated, voiced aspirated, ejective), two affricate rows (voiceless, voiced), two fricative rows (voiceless, voiced), and one each for nasal, lateral, tap-or-trill, and approximant / glide. Two rows contain Sanskrit's महाप्राण (*mahāprāṇa*) stops. The survey sets those rows aside for the reason explained below. The ejective row appears for languages using the Caucasian or Native American glottal-pressure system; Sanskrit does not light it.

**Why the survey sets aside the महाप्राण (*mahāprāṇa*) rows.** Chapter 8 §8.3 defines a 23-cell Sanskrit base by setting aside the ten महाप्राण (*mahāprāṇa*) stops: **ख छ ठ थ फ** and **घ झ ढ ध भ**. This does not demote Sanskrit's breath axis. It allows the comparison to test the consonantal base before adding the breath distinctions Sanskrit builds on top.

The generator removes the two aspirated-stop rows from every comparison language as well. It then counts coverage only across the remaining Sanskrit base addresses.[NOTE: inventory-atlas-coverage-surveys]

**The distinction between possible sound and assigned address keeps the comparison honest.** Chapter 8 §8.2 introduces it; the full treatment is here.

A language's *spoken sound range* includes all the sounds its speakers produce. Some arise from neighboring sounds, some vary by region, and some appear only in particular words or speaking conditions.

A ***sonomeric grid address*** is a stable inventory position assigned to an independent contrastive unit. Two sounds occupy two addresses only if the language treats them as distinct word-making units.

Tamil speakers produce voiced stop sounds in real speech, but Tamil's contrastive inventory does not assign those realizations independent voiced-stop addresses as Sanskrit does. The atlas records the inventory rather than every sound a speaker can produce.

The same rule governs aspirated stops, palatal-versus-post-alveolar distinctions, and other sounds that occur without distinguishing words independently. The atlas therefore compares contrastive inventories, matching the level at which Sanskrit selects and arranges its sonomers.

**The coverage criterion is union, not ranking.** For each three-language comparison set, a Sanskrit cell counts as *covered* if at least one of the three languages lights it. Chapter 8 examines whether the consonant inventories of the Indian subcontinent contain Sanskrit's selected base more densely than the comparison regions. Union coverage tests that proposition without turning the result into a ranking of individual languages.

Three languages collectively covering 22 of 23 cells does not mean each language contains 22 of those cells; it means the union of their three inventories intersects Sanskrit's base in 22 places. A language that contributes three or four cells can still carry weight if those cells are otherwise unfilled.

The selected sets are deliberate comparisons, not regional averages. The totals cannot determine language ancestry by themselves. They test a narrower question: do the selected languages carrying the *"Indo-European"* label consistently cover more of Sanskrit's consonantal base? They do not. Within these eleven sets, location and contact with the Indian subcontinent correspond more closely to the retroflex contribution than the shared family label does.

**The source of every inventory is recorded.** The eleven surveys use phonemic inventories drawn from standard descriptions of each language. The generator `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py` places every inventory beside its reference source. Changing one inventory and rebuilding the figures immediately shows whether the totals change.

The research record also identifies the choices most likely to affect a cell: Pashto's full retroflex set, Modern Greek's lack of phonemic **h**, the shared affricate row used for distinctions in Armenian and Georgian, and one Burushaski retroflex affricate that the present row system does not classify. None changes the published coverage totals. The complete record appears in `working/40_reference/research/inventory_atlas_coverage_surveys.md` §5.

The Korku chart uses this conservative policy. Nagaraja's grammar describes a richer retroflex inventory than the atlas currently displays, including retroflex aspirates, a retroflex flap, and a retroflex lateral.[NOTE: korku-nagaraja-mouth-mind-evidence]

Adding those sounds would enrich the chart without changing the present 20-of-23 result. The महाप्राण (*mahāprāṇa*) preset removes the aspirated rows, while the retroflex flap and lateral occupy addresses outside the 23 Sanskrit base cells counted here. The appendix therefore reports the current count and records the fuller inventory separately.

The method is narrow and reproducible. It turns Chapter 8's comparison into numbers the reader can audit.

## 4.2 Santali-Inclusive Munda Survey: 20 of 23

The body's Forest-Belt Survey used Korku, Mundari, and Ho. This alternate set replaces Ho with Santali and tests whether that choice changes the result. It does not: Korku, Mundari, and Santali cover the same 20 of 23 cells.

The unfilled letters match the body set too: **ण · ष · श**.

![Figure A.4.1 — Munda Survey: 20 of 23 Sanskrit base cells. Korku, Mundari, and Santali cover the same 20 cells the body's Forest-Belt Survey covers, with the same unfilled set (ण · ष · श).](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=100%}

Including Santali does not increase the count. Both sampled forest-belt sets cover 20 of Sanskrit's 23 base cells and leave the same retroflex nasal and two sibilants unfilled.

## 4.3 Santali-Free Mixed Survey: 21 of 23

The Mixed Survey swaps Santali for Burushaski, the language-isolate of the Hunza Valley, and pairs it with Korku and Mundari.

The count rises to 21 of 23. The unfilled set contracts to **ण · श**. Burushaski's retroflex inventory adds **ष**, while the three languages already cover Sanskrit's alveolar **र**, **ल**, and **स**.

This comparison crosses the pyramid's family boundaries without using Santali. Korku and Mundari come from the central forest belt, while Burushaski comes from the north-western frontier. Together, their inventories cover 21 cells.

![Figure A.4.2 — Mixed Survey: 21 of 23 Sanskrit base cells. Korku, Mundari, and Burushaski leave only ण and श unfilled.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=100% height=80%}

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 18 of 23

The machinery classifies Munda alongside two other branches under the umbrella *"Austro-Asiatic"*: a Khasian branch in the Meghalaya highlands and a Nicobaric branch on the Nicobar Islands. The three branches sit at geographically remote subcontinental poles.

The Dispersed Survey picks one representative from each branch: Sora (South Munda, Eastern Ghats and Rushikulya basin), Khasi (Meghalaya highlands), and Nicobarese (Car Nicobar). Coverage falls to 18 of 23. The unfilled set expands to **ट · ड · ण · ष · श** — five cells, two more than the Munda-pure Forest-Belt set the body uses.

The single pyramid label *"Austro-Asiatic"* places these three languages in one family, but the selected inventories have sharply different shapes. Sora's South Munda inventory lacks the retroflex stops found in North Munda; Khasi uses voiceless-aspirated stops; Nicobarese uses neither retroflex nor aspirated stops in the inventory selected here. Their union covers less of Sanskrit's base than the all-Munda forest-belt samples.

In these samples, the family label does not predict how much of Sanskrit's base each regional selection covers. A larger comparison would be needed to separate the effects of branch history, geography, and contact.

![Figure A.4.3 — Dispersed Survey: 18 of 23 Sanskrit base cells. Sora, Khasi, and Nicobarese — three languages the machinery classifies under one *"Austro-Asiatic"* umbrella across three remote subcontinental poles — cover two fewer cells than the all-Munda Forest-Belt Survey.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=100%}

## 4.5 Northwest Frontier Survey: 22 of 23

Three north-western contact-zone languages — Pashto (*"Iranian"* by the pyramid's label, Afghanistan and the north-western Indian subcontinent), Nuristani (a separate IE branch spoken in the Hindu Kush valleys), and Burushaski (the Hunza Valley isolate) — cover 22 of 23, tying the highest result in the survey. Like the body's Southern Survey, they leave only **श** unfilled.

The north-western frontier set and the body's widely dispersed Tamil + Toda + Kurukh set deliver the same count and leave the same single cell unfilled. Both draw from languages that use retroflex distinctions found across the Indian subcontinent, and both contain nearly the whole base Sanskrit selected.

The set presents a taxonomically mixed profile. The pyramid's label classifies Pashto as *"Iranian"*, the machinery classifies Nuristani as a separate IE branch neither Indic nor Iranian, and Burushaski stands as a language-isolate. Despite those different labels, the selected frontier set ties the Southern Survey. Its inventories use retroflex contrasts associated with the broad subcontinental sound range.

![Figure A.4.4 — Northwest Frontier Survey: 22 of 23 Sanskrit base cells. Pashto, Nuristani, and Burushaski cover the same 22 cells as the body's Tamil + Toda + Kurukh set. Both leave only श unfilled.](figures/superset/sk_pashto_nuristani_burushaski.svg){#fig:app4-nw-frontier-survey width=100% height=80%}

## 4.6 Iranian Survey Outside the Subcontinental Retroflex Zone: 15 of 23

Three Iranian languages outside the north-western contact zone — Farsi (Iran), Kurdish Kurmanji (northern Iraq, Syria, eastern Turkey), and Talysh (Caspian littoral, Azerbaijan and northern Iran) — create a direct comparison with the Northwest Frontier Survey. They cover 15 of 23. The unfilled set runs **ट · च · ड · ज · ण · ञ · ष · श**: eight cells, including most of the retroflex column.

The selected languages that the pyramid classifies as Sanskrit's "Iranian sister branch" cover seven fewer cells than the mixed Northwest Frontier set.

The contact comparison clarifies the two-cell difference. Replacing Talysh with Balochi — a north-western frontier Iranian language that uses retroflex contrasts within the subcontinental contact zone — moves coverage from 15 to 17.

Balochi contributes the retroflex grid addresses **ट** and **ड** that Caspian-littoral Talysh does not. Their shared *Iranian* classification does not explain the difference; their locations and histories of contact with the Indian subcontinent correspond to it.

![Figure A.4.5 — Iranian Survey: 15 of 23 Sanskrit base cells. Three Iranian languages outside the north-western subcontinental contact zone leave most of Sanskrit's retroflex column unfilled.](figures/superset/sk_farsi_kurdish_talysh.svg){#fig:app4-iranian-survey width=100% height=80%}

## 4.7 Caucasus Survey: 13 of 23

Three languages from three different pyramid classifications, all from the Caucasus region — Armenian (a separate IE branch), Georgian (Kartvelian / South Caucasian, outside the IE classification altogether), and Ossetian (Iranian, north Caucasus) — fall to 13 of 23, the floor of the eleven-survey set. The unfilled list runs **ट · च · ड · ज · ण · ञ · ङ · ष · श · व**: ten cells, the largest unfilled list of any survey.

Three pyramid classifications meet inside one geographic region, yet the selected set reaches only 13 of 23. This is the lowest coverage among the eleven samples.

![Figure A.4.6 — Caucasus Survey: 13 of 23 Sanskrit base cells. Three pyramid classifications meet in one geographic region, and this selected set produces the lowest coverage among the eleven surveys.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=100% height=80%}

## 4.8 Slavic & Caucasus IE Survey: 14 of 23

The Slavic & Caucasus IE Survey runs three IE-classified languages along the steppe corridor: Russian and Ukrainian from East Slavic, Ossetian from Caucasian Iranian. Coverage reaches 14 of 23, one cell above the Caucasus floor.

All three languages share the pyramid's "Indo-European" label that supposedly makes them Sanskrit's relatives. East Slavic and Caucasian Iranian together cover less of Sanskrit's base than the body's Western IE Survey at 16/23 and the Central Asian Tajik + Kazakh + Kyrgyz set at 15/23. Across the selected IE-classified sets, coverage ranges from 14/23 to 22/23 and rises in the sets drawn closer to the subcontinental contact zone.

The selected steppe-corridor languages — drawn from the region where the pyramid places its Aryan migration — cover fewer of Sanskrit's base cells than the selected languages from the Indian subcontinent and its north-western frontier.

![Figure A.4.7 — Slavic & Caucasus IE Survey: 14 of 23 Sanskrit base cells. Three IE-classified languages along the steppe corridor cover only one cell more than the Caucasus floor and less than the body's Western IE and Central Asian sets.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=100% height=80%}

## 4.9 The Coverage Cascade

The eleven surveys — four in the body and seven in this appendix — produce the following sample ordering. Sets drawn from the Indian subcontinent and its north-western contact zone occupy the higher rows, while the selected Caucasus and steppe sets occupy the lower rows. These eleven sets do not establish a universal geographic law. They show a repeatable pattern that can now be tested against more languages.

| Coverage | Set | Languages | Source |
|---:|---|---|---|
| **22 / 23** | Southern Survey | Tamil + Toda + Kurukh | body (Ch 8 §8.4) |
| **22 / 23** | Northwest Frontier | Pashto + Nuristani + Burushaski | App 4 §4.5 |
| 21 / 23 | Mixed Survey | Korku + Mundari + Burushaski | App 4 §4.3 |
| 20 / 23 | Forest-Belt Survey | Korku + Mundari + Ho | body (Ch 8 §8.4) |
| 20 / 23 | Munda Survey | Korku + Mundari + Santali | App 4 §4.2 |
| 18 / 23 | Dispersed *"Austro-Asiatic"* | Sora + Khasi + Nicobarese | App 4 §4.4 |
| 16 / 23 | Western IE Survey | English + French + Greek | body (Ch 8 §8.4) |
| 15 / 23 | Iranian Survey (outside the retroflex zone) | Farsi + Kurdish + Talysh | App 4 §4.6 |
| 15 / 23 | Central Asian Survey | Tajik + Kazakh + Kyrgyz | body (Ch 8 §8.4) |
| 14 / 23 | Slavic & Caucasus IE | Russian + Ukrainian + Ossetian | App 4 §4.8 |
| **13 / 23** | Caucasus Survey | Armenian + Georgian + Ossetian | App 4 §4.7 |

**The selected sets closer to the Indian subcontinent show higher coverage.** The Tamil + Toda + Kurukh set and the north-western Pashto + Nuristani + Burushaski set both reach 22/23 and leave only **श** unfilled. The first combines languages spoken in widely separated parts of the subcontinent; the second combines languages from the north-western frontier. The selected Caucasus set produces the lowest result at 13/23.

**The pyramid's "Indo-European" classification does not explain the variation within these samples.** The selected sets containing IE-classified languages range from 14/23 to 22/23. Two members of the high-coverage frontier set, Pashto and Nuristani, carry the same broad IE label as Russian, Ukrainian, and Ossetian in the low-coverage set. Their locations and histories of contact with the Indian subcontinent differ.

**The selected Iranian languages divide along the contact axis.** Pashto and Balochi, inside the north-western subcontinental contact zone, use retroflex contrasts and contribute to the higher coverage there. Farsi, Kurdish, and Talysh, outside that zone, deliver 15/23 in the selected set. Their shared Iranian label does not account for that difference.

**The *"Austro-Asiatic"* samples also vary by geography and branch.** Munda languages inside the central forest belt deliver 20/23, while the dispersed Sora + Khasi + Nicobarese set delivers 18/23. The broad family label does not remove the differences among their sound inventories.

**The body's four figures occupy four points in the larger sample ordering.** Southern Survey (22), Forest-Belt Survey (20), Western IE Survey (16), and Central Asian Survey (15) form the sequence used in Chapter 8. The seven appendix surveys show that several alternate selections reproduce parts of that ordering, while also showing how much the result depends on the chosen languages and inventory descriptions.

Across these samples, Sanskrit's base grid addresses receive their highest coverage from the southern, central forest-belt, and north-western regions of the Indian subcontinent. The machinery sorts those languages into different families, yet the selected inventories repeatedly recover much of the same Sanskrit base. The atlas therefore gives the transported-cargo story a reproducible test: expand the inventories, alter the language sets, and see whether the geographic pattern survives.
