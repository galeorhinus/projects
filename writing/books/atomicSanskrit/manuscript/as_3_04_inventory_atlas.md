# Appendix Part 4 — The Consonant Inventory Atlas and Additional Surveys

---

Chapter 8 compares selected language groups by placing their consonant contrasts on one shared mouth-map. Its four surveys cover 22, 20, 16, and 15 of Sanskrit's 23 base cells.

This appendix documents the method and adds seven surveys. Every comparison uses published consonant inventories, the same mouth-map, and the same Sanskrit base. Changing a language or the source used for its inventory may change the result, so each set remains a sample rather than an average for an entire region.

Together, the eleven surveys map the **subcontinental superset** introduced in Chapter 8. Each regional set contains part of that larger sound inventory; no individual language contains the whole. Sanskrit's twenty-three base cells provide the comparison target, while additional regional consonants show that the superset extends beyond Sanskrit's selected grid.

## 4.1 The Atlas Method in Depth

The atlas maps one physical fact: where the mouth produces each consonant that a language treats as an independent contrast. The shared map places that consonant at its articulatory coordinates and records which positions each language keeps as independent grid addresses. Vocabulary, descent, prestige, script, age, and the pyramid's classificatory buckets play no role in that placement.[NOTE: language-hotzones-inventory-method]

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

**Why the survey sets aside the महाप्राण (*mahāprāṇa*) rows.** Chapter 8 §8.3 defines a 23-cell Sanskrit base by setting aside the ten महाप्राण (*mahāprāṇa*) stops: **ख छ ठ थ फ** and **घ झ ढ ध भ**. The comparison can then test the consonantal base before adding the breath distinctions Sanskrit builds on top.

The generator removes the two aspirated-stop rows from every comparison language as well. It then counts coverage only across the remaining Sanskrit base addresses.[NOTE: inventory-atlas-coverage-surveys]

Chapter 8 §8.2 distinguishes sounds that speakers can produce from the contrasts their language uses to distinguish words. The atlas counts only the second kind. A sound receives its own comparison cell only when the language treats it as an independent word-making unit.

Tamil speakers, for example, produce voiced stops in ordinary speech, but Tamil does not assign those contextual sounds separate voiced-stop addresses as Sanskrit does. The same rule governs aspirated stops, neighboring sibilants, and every other inventory used here. The atlas compares reusable contrasts, not every sound that may occur during speech.

Each score reports the union of three inventories. A Sanskrit cell counts as covered when at least one language in the set uses that consonantal distinction. A score of 22 therefore means that the three languages collectively cover 22 cells; it does not mean that any one of them contains all 22.

Each score belongs to the selected set rather than to an entire region or language family. The seven additional surveys change the selections and show how the result responds.

**The source of every inventory is recorded.** The eleven surveys use phonemic inventories drawn from standard descriptions of each language. The generator `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py` places every inventory beside its reference source. Changing one inventory and rebuilding the figures immediately shows whether the totals change.

The research record also identifies the choices most likely to affect a cell: Pashto's full retroflex set, Modern Greek's lack of phonemic **h**, the shared affricate row used for distinctions in Armenian and Georgian, and one Burushaski retroflex affricate that the present row system does not classify. None changes the published coverage totals. The complete record appears in `working/40_reference/research/inventory_atlas_coverage_surveys.md` §5.

The Korku chart uses this conservative policy. Nagaraja's grammar describes a richer retroflex inventory than the atlas currently displays, including retroflex aspirates, a retroflex flap, and a retroflex lateral.[NOTE: korku-nagaraja-mouth-mind-evidence]

Adding those sounds would enrich the chart without changing the present 20-of-23 result. The महाप्राण (*mahāprāṇa*) preset removes the aspirated rows, while the retroflex flap and lateral occupy addresses outside the 23 Sanskrit base cells counted here. The appendix therefore reports the current count and records the fuller inventory separately.

## 4.2 Santali-Inclusive Forest-Belt Survey: 20 of 23

The body's Forest-Belt Survey used Korku, Mundari, and Ho. This alternate replaces Ho with Santali to test whether excluding Santali affected the result. Korku, Mundari, and Santali still cover 20 of 23 cells and leave **ण · ष · श** unfilled.

![Figure A.4.1 — Korku-Mundari-Santali Survey: 20 of 23 Sanskrit base cells. Korku, Mundari, and Santali cover the same 20 cells the body's Forest-Belt Survey covers, with the same unfilled set (ण · ष · श).](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=100%}

## 4.3 Santali-Free Mixed Survey: 21 of 23

The Mixed Survey pairs Korku and Mundari with Burushaski, a language isolate spoken in the Hunza Valley. Their combined inventories cover 21 of 23 cells and leave only **ण · श** unfilled. Burushaski supplies **ष**, while the three languages together already cover Sanskrit's alveolar **र**, **ल**, and **स**.

The survey therefore reaches 21 cells without Santali by combining languages that the pyramid places in separate families.

![Figure A.4.2 — Mixed Survey: 21 of 23 Sanskrit base cells. Korku, Mundari, and Burushaski leave only ण and श unfilled.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=100% height=80%}

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 18 of 23

The machinery places the languages it calls *"Munda"* alongside two other branches under the label *"Austro-Asiatic"*: Khasian in the Meghalaya highlands and Nicobaric on the Nicobar Islands. These branches are spoken in widely separated regions of the subcontinent.

The Dispersed Survey picks one representative from each branch: Sora (which the machinery classifies as *"South Munda,"* Eastern Ghats and Rushikulya basin), Khasi (Meghalaya highlands), and Nicobarese (Car Nicobar). Coverage falls to 18 of 23. The unfilled set expands to **ट · ड · ण · ष · श** — five cells, two more than the Korku-Mundari-Santali Forest-Belt set the body uses.

The single pyramid label *"Austro-Asiatic"* places these three languages in one family, but the selected inventories have sharply different shapes. Sora's inventory lacks the retroflex stops found in Korku, Mundari, and Santali; Khasi uses voiceless-aspirated stops; Nicobarese uses neither retroflex nor aspirated stops in the inventory selected here. Their union covers less of Sanskrit's base than the forest-belt samples built from Korku, Mundari, and either Ho or Santali.

![Figure A.4.3 — Dispersed Survey: 18 of 23 Sanskrit base cells. Sora, Khasi, and Nicobarese — three languages the machinery classifies under one *"Austro-Asiatic"* umbrella across three remote subcontinental poles — cover two fewer cells than the Korku-Mundari-Santali Forest-Belt Survey.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=100%}

## 4.5 Northwest Frontier Survey: 22 of 23

Pashto, Nuristani, and Burushaski cover 22 of 23 cells and leave only **श** unfilled. This north-western frontier set ties the body's widely dispersed Tamil + Toda + Kurukh survey.

The pyramid assigns the three languages to separate categories: Pashto is *"Iranian,"* Nuristani belongs to another Indo-European branch, and Burushaski is an isolate. Their combined inventories reach 22 cells because they contain retroflex distinctions distributed across the north-western subcontinental contact zone.

![Figure A.4.4 — Northwest Frontier Survey: 22 of 23 Sanskrit base cells. Pashto, Nuristani, and Burushaski cover the same 22 cells as the body's Tamil + Toda + Kurukh set. Both leave only श unfilled.](figures/superset/sk_pashto_nuristani_burushaski.svg){#fig:app4-nw-frontier-survey width=100% height=80%}

## 4.6 Iranian Survey Outside the Subcontinental Retroflex Zone: 15 of 23

Farsi, Kurdish Kurmanji, and Talysh are spoken outside the north-western subcontinental contact zone. Together they cover 15 of 23 cells and leave **ट · च · ड · ज · ण · ञ · ष · श** unfilled. That is seven fewer cells than the Northwest Frontier set, even though the pyramid classifies all three languages here within Sanskrit's *"Iranian sister branch."*

Replacing Caspian-littoral Talysh with Balochi, an Iranian language inside the contact zone, raises coverage from 15 to 17. Balochi supplies the retroflex addresses **ट** and **ड**. The shared Iranian label remains the same; the location and history of contact change.

![Figure A.4.5 — Iranian Survey: 15 of 23 Sanskrit base cells. Three Iranian languages outside the north-western subcontinental contact zone leave most of Sanskrit's retroflex column unfilled.](figures/superset/sk_farsi_kurdish_talysh.svg){#fig:app4-iranian-survey width=100% height=80%}

## 4.7 Caucasus Survey: 13 of 23

Armenian, Georgian, and Ossetian are all spoken in the Caucasus, but the pyramid places them in three different categories. Armenian belongs to a separate Indo-European branch. Georgian belongs to the Kartvelian family outside the Indo-European classification, while Ossetian is classified as Iranian. Together they cover 13 of 23 cells, the lowest result in the eleven-survey set. The ten unfilled cells are **ट · च · ड · ज · ण · ञ · ङ · ष · श · व**, the largest unfilled set in the atlas.

![Figure A.4.6 — Caucasus Survey: 13 of 23 Sanskrit base cells. Three pyramid classifications meet in one geographic region, and this selected set produces the lowest coverage among the eleven surveys.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=100% height=80%}

## 4.8 Slavic & Caucasus IE Survey: 14 of 23

Russian, Ukrainian, and Ossetian are three Indo-European-classified languages spoken along the steppe corridor. Together they cover 14 of Sanskrit's 23 base cells, only one more than the Caucasus floor.

The selected languages from the region through which the pyramid places its Aryan migration cover fewer cells than the selected languages of the Indian subcontinent and its north-western frontier.

![Figure A.4.7 — Slavic & Caucasus IE Survey: 14 of 23 Sanskrit base cells. Three IE-classified languages along the steppe corridor cover only one cell more than the Caucasus floor and less than the body's Western IE and Central Asian sets.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=100% height=80%}

## 4.9 The Coverage Cascade

The cascade places all eleven surveys on one scale. Sets drawn from the Indian subcontinent and its north-western contact zone occupy the higher rows, while the selected Caucasus and steppe sets occupy the lower rows.

![Figure A.4.8 — The Coverage Cascade. Eleven three-language surveys ranked by how many of Sanskrit's 23 base sonomers their combined inventories cover. Filled pips show covered cells; hollow pips show unfilled cells.](figures/superset/superset_coverage_cascade_pips.svg){#fig:app4-coverage-cascade width=86%}

The Tamil + Toda + Kurukh set and the north-western Pashto + Nuristani + Burushaski set both reach 22/23 and leave only **श** unfilled. The first combines languages spoken in widely separated parts of the subcontinent; the second combines languages from the north-western frontier. The selected Caucasus set produces the lowest result at 13/23.

The pyramid's *"Indo-European"* classification spans results from 14/23 to 22/23. Pashto and Nuristani in the high-coverage frontier set carry the same broad label as Russian, Ukrainian, and Ossetian in the low-coverage set. Their locations and histories of contact with the Indian subcontinent differ.

The Iranian comparison shows what the broad family label misses. Pashto and Balochi use retroflex distinctions inside the north-western subcontinental contact zone. The selected Farsi, Kurdish, and Talysh set outside that zone delivers 15/23. All five languages carry the Iranian label.

The *"Austro-Asiatic"* label conceals a similar difference. Korku, Mundari, and Santali inside the central forest belt deliver 20/23, while the dispersed Sora + Khasi + Nicobarese set delivers 18/23.

The highest scores in these samples come from the southern, central forest-belt, and north-western regions of the Indian subcontinent. The machinery sorts those languages into different families, yet their inventories repeatedly recover much of the same Sanskrit base.

The atlas gives the transported-cargo story a reproducible test. Other researchers can expand the inventories, alter the language sets, and see whether the geographic ordering survives.
