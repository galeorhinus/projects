# Appendix Part 4 — The Consonant Inventory Atlas and Additional Surveys

---

Chapter 8 compares selected language groups by placing their consonant contrasts on one shared mouth-map. The four body figures use a dispersed southern-subcontinental set, the central forest belt, a Western Indo-European control, and a Central Asian control. Their selected sets cover 22, 20, 16, and 15 of the 23 Sanskrit base cells.

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

Sanskrit's traditional categories and the comparison grid divide the mouth differently. Chapter 8 Figure 8.1 retains Sanskrit's own classification, while the atlas compares how speakers actually pronounce sounds across languages. It therefore places Sanskrit **र** and **ल** with Tamil **ர** and **ல** in their shared alveolar cells. It also places Sanskrit **स** with the alveolar **s** used by Toda, Kurukh, and the forest-belt languages. This translation places matching pronunciations in the same comparison cells without altering Sanskrit's internal arrangement.

**The vertical axis contains thirteen manners.** Each row describes how a consonant is shaped at its place. Five rows contain stops: voiceless unaspirated, voiceless aspirated, voiced unaspirated, voiced aspirated, and ejective. Two rows contain affricates, two contain fricatives, and the remaining four contain nasals, laterals, taps or trills, and approximants or glides.

Two of those rows contain Sanskrit's महाप्राण (*mahāprāṇa*) stops. The survey sets them aside for the reason explained below. The ejective row records languages that use the Caucasian or Native American glottal-pressure system; Sanskrit has no sound in that row.

**Why the survey sets aside the महाप्राण (*mahāprāṇa*) rows.** Chapter 8 §8.3 defines a 23-cell Sanskrit base by setting aside the ten महाप्राण (*mahāprāṇa*) stops: **ख छ ठ थ फ** and **घ झ ढ ध भ**. This does not demote Sanskrit's breath axis. It allows the comparison to test the consonantal base before adding the breath distinctions Sanskrit builds on top.

The generator removes the two aspirated-stop rows from every comparison language as well. It then counts coverage only across the remaining Sanskrit base addresses.[NOTE: inventory-atlas-coverage-surveys]

**The comparison must distinguish a sound that speakers can produce from a sound their language uses to distinguish words.** Chapter 8 §8.2 introduces that distinction. This appendix applies it to every inventory in the atlas.

A language's *spoken sound range* includes all the sounds its speakers produce. Some arise from neighboring sounds, some vary by region, and some appear only in particular words or speaking conditions.

A ***sonomeric grid address*** is a stable inventory position assigned to an independent contrastive unit. Two sounds occupy two addresses only if the language treats them as distinct word-making units.

Tamil speakers produce voiced stop sounds in real speech, but Tamil's contrastive inventory does not assign those realizations independent voiced-stop addresses as Sanskrit does. The atlas records the inventory rather than every sound a speaker can produce.

The same rule applies to aspirated stops, palatal-versus-post-alveolar distinctions, and other sounds that occur without distinguishing words independently. The atlas therefore compares contrastive inventories, matching the level at which Sanskrit selects and arranges its sonomers.

**The coverage criterion is union, not ranking.** For each three-language comparison set, a Sanskrit cell counts as *covered* if at least one of the three languages lights it. Chapter 8 examines whether the consonant inventories of the Indian subcontinent contain Sanskrit's selected base more densely than the comparison regions. Union coverage tests that proposition without turning the result into a ranking of individual languages.

When three languages collectively cover 22 of 23 cells, no individual language needs to contain all 22. Their combined inventories match Sanskrit's base in 22 places. A language may add only three or four cells to the total, but those cells still affect the result when neither of the other languages contains them.

The selected sets create specific comparisons; they are not regional averages. Their totals test whether languages classified as *"Indo-European"* consistently cover more of Sanskrit's consonantal base than languages placed in other families. They do not. Across these eleven sets, proximity to and contact with the Indian subcontinent correspond more closely with the presence of retroflex sounds than the shared family label does.

**The source of every inventory is recorded.** The eleven surveys use phonemic inventories drawn from standard descriptions of each language. The generator `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py` places every inventory beside its reference source. Changing one inventory and rebuilding the figures immediately shows whether the totals change.

The research record also identifies the choices most likely to affect a cell: Pashto's full retroflex set, Modern Greek's lack of phonemic **h**, the shared affricate row used for distinctions in Armenian and Georgian, and one Burushaski retroflex affricate that the present row system does not classify. None changes the published coverage totals. The complete record appears in `working/40_reference/research/inventory_atlas_coverage_surveys.md` §5.

The Korku chart uses this conservative policy. Nagaraja's grammar describes a richer retroflex inventory than the atlas currently displays, including retroflex aspirates, a retroflex flap, and a retroflex lateral.[NOTE: korku-nagaraja-mouth-mind-evidence]

Adding those sounds would enrich the chart without changing the present 20-of-23 result. The महाप्राण (*mahāprāṇa*) preset removes the aspirated rows, while the retroflex flap and lateral occupy addresses outside the 23 Sanskrit base cells counted here. The appendix therefore reports the current count and records the fuller inventory separately.

The method is narrow and reproducible. It turns Chapter 8's comparison into numbers the reader can audit.

## 4.2 Santali-Inclusive Forest-Belt Survey: 20 of 23

The body's Forest-Belt Survey used Korku, Mundari, and Ho. This alternate set replaces Ho with Santali and tests whether that choice changes the result. It does not: Korku, Mundari, and Santali cover the same 20 of 23 cells.

The unfilled letters match the body set too: **ण · ष · श**.

![Figure A.4.1 — Korku-Mundari-Santali Survey: 20 of 23 Sanskrit base cells. Korku, Mundari, and Santali cover the same 20 cells the body's Forest-Belt Survey covers, with the same unfilled set (ण · ष · श).](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=100%}

Including Santali does not increase the count. Both sampled forest-belt sets cover 20 of Sanskrit's 23 base cells and leave the same retroflex nasal and two sibilants unfilled.

## 4.3 Santali-Free Mixed Survey: 21 of 23

The Mixed Survey replaces Santali with Burushaski, a language isolate spoken in the Hunza Valley, and pairs it with Korku and Mundari.

The count rises to 21 of 23. The unfilled set contracts to **ण · श**. Burushaski's retroflex inventory adds **ष**, while the three languages already cover Sanskrit's alveolar **र**, **ल**, and **स**.

This comparison crosses the pyramid's family boundaries without using Santali. Korku and Mundari come from the central forest belt, while Burushaski comes from the north-western frontier. Together, their inventories cover 21 cells.

![Figure A.4.2 — Mixed Survey: 21 of 23 Sanskrit base cells. Korku, Mundari, and Burushaski leave only ण and श unfilled.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=100% height=80%}

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 18 of 23

The machinery places the languages it calls *"Munda"* alongside two other branches under the label *"Austro-Asiatic"*: Khasian in the Meghalaya highlands and Nicobaric on the Nicobar Islands. These branches are spoken in widely separated regions of the subcontinent.

The Dispersed Survey picks one representative from each branch: Sora (which the machinery classifies as *"South Munda,"* Eastern Ghats and Rushikulya basin), Khasi (Meghalaya highlands), and Nicobarese (Car Nicobar). Coverage falls to 18 of 23. The unfilled set expands to **ट · ड · ण · ष · श** — five cells, two more than the Korku-Mundari-Santali Forest-Belt set the body uses.

The single pyramid label *"Austro-Asiatic"* places these three languages in one family, but the selected inventories have sharply different shapes. Sora's inventory lacks the retroflex stops found in Korku, Mundari, and Santali; Khasi uses voiceless-aspirated stops; Nicobarese uses neither retroflex nor aspirated stops in the inventory selected here. Their union covers less of Sanskrit's base than the forest-belt samples built from Korku, Mundari, and either Ho or Santali.

In these samples, the family label does not predict how much of Sanskrit's base each regional selection covers. A larger comparison would be needed to separate the effects of branch history, geography, and contact.

![Figure A.4.3 — Dispersed Survey: 18 of 23 Sanskrit base cells. Sora, Khasi, and Nicobarese — three languages the machinery classifies under one *"Austro-Asiatic"* umbrella across three remote subcontinental poles — cover two fewer cells than the Korku-Mundari-Santali Forest-Belt Survey.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=100%}

## 4.5 Northwest Frontier Survey: 22 of 23

Three north-western contact-zone languages — Pashto (*"Iranian"* by the pyramid's label, Afghanistan and the north-western Indian subcontinent), Nuristani (a separate IE branch spoken in the Hindu Kush valleys), and Burushaski (the Hunza Valley isolate) — cover 22 of 23, tying the highest result in the survey. Like the body's Southern Survey, they leave only **श** unfilled.

The north-western frontier set and the body's widely dispersed Tamil + Toda + Kurukh set deliver the same count and leave the same single cell unfilled. Both draw from languages that use retroflex distinctions found across the Indian subcontinent, and both contain nearly the whole base Sanskrit selected.

The pyramid assigns the three languages to different categories. It classifies Pashto as *"Iranian"*, Nuristani as a separate IE branch that is neither Indic nor Iranian, and Burushaski as a language isolate. Despite those different labels, the selected frontier set ties the Southern Survey because its inventories include retroflex contrasts found across the broad subcontinental sound range.

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

The Slavic and Caucasus IE Survey compares three languages classified as Indo-European and spoken along the steppe corridor: the East Slavic languages Russian and Ukrainian, and the Caucasian Iranian language Ossetian. Together they cover 14 of Sanskrit's 23 base cells, only one more than the lowest result in the atlas.

All three languages share the pyramid's "Indo-European" label that supposedly makes them Sanskrit's relatives. East Slavic and Caucasian Iranian together cover less of Sanskrit's base than the body's Western IE Survey at 16/23 and the Central Asian Tajik + Kazakh + Kyrgyz set at 15/23. Across the selected IE-classified sets, coverage ranges from 14/23 to 22/23 and rises in the sets drawn closer to the subcontinental contact zone.

The selected steppe-corridor languages — drawn from the region where the pyramid places its Aryan migration — cover fewer of Sanskrit's base cells than the selected languages from the Indian subcontinent and its north-western frontier.

![Figure A.4.7 — Slavic & Caucasus IE Survey: 14 of 23 Sanskrit base cells. Three IE-classified languages along the steppe corridor cover only one cell more than the Caucasus floor and less than the body's Western IE and Central Asian sets.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=100% height=80%}

## 4.9 The Coverage Cascade

The eleven surveys — four in the body and seven in this appendix — produce the following sample ordering. Sets drawn from the Indian subcontinent and its north-western contact zone occupy the higher rows, while the selected Caucasus and steppe sets occupy the lower rows. These eleven sets do not establish a universal geographic law. They show a repeatable pattern that can now be tested against more languages.

![Figure A.4.8 — The Coverage Cascade. Eleven three-language surveys ranked by how many of Sanskrit's 23 base sonomers their combined inventories cover. Filled pips show covered cells; hollow pips show unfilled cells.](figures/superset/superset_coverage_cascade_pips.svg){#fig:app4-coverage-cascade width=86%}

**The selected sets closer to the Indian subcontinent show higher coverage.** The Tamil + Toda + Kurukh set and the north-western Pashto + Nuristani + Burushaski set both reach 22/23 and leave only **श** unfilled. The first combines languages spoken in widely separated parts of the subcontinent; the second combines languages from the north-western frontier. The selected Caucasus set produces the lowest result at 13/23.

**The pyramid's "Indo-European" classification does not explain the variation within these samples.** The selected sets containing IE-classified languages range from 14/23 to 22/23. Two members of the high-coverage frontier set, Pashto and Nuristani, carry the same broad IE label as Russian, Ukrainian, and Ossetian in the low-coverage set. Their locations and histories of contact with the Indian subcontinent differ.

**The selected Iranian languages divide along the contact axis.** Pashto and Balochi, inside the north-western subcontinental contact zone, use retroflex contrasts and contribute to the higher coverage there. Farsi, Kurdish, and Talysh, outside that zone, deliver 15/23 in the selected set. Their shared Iranian label does not account for that difference.

**The *"Austro-Asiatic"* samples also vary by geography and branch.** Korku, Mundari, and Santali inside the central forest belt deliver 20/23, while the dispersed Sora + Khasi + Nicobarese set delivers 18/23. The broad family label does not remove the differences among their sound inventories.

**The four surveys in Chapter 8 also appear in this larger comparison.** Their results descend from the Southern Survey (22) to the Forest-Belt Survey (20), the Western IE Survey (16), and the Central Asian Survey (15). The seven additional surveys reproduce parts of that order with different languages. They also show how the result changes when the selected languages or their inventory descriptions change.

Across these samples, Sanskrit's base grid addresses receive their highest coverage from the southern, central forest-belt, and north-western regions of the Indian subcontinent. The machinery sorts those languages into different families, yet the selected inventories repeatedly recover much of the same Sanskrit base. The atlas therefore gives the transported-cargo story a reproducible test: expand the inventories, alter the language sets, and see whether the geographic pattern survives.
