# Appendix Part 4 — The Consonant Inventory Atlas and Control Surveys

---

Chapter 8 compares selected language groups by placing their consonant contrasts on one shared mouth-map. The four body figures show the southern subcontinent, the central forest belt, a Western Indo-European control, and a Central Asian control. Their selected sets cover 22, 20, 16, and 15 of the 23 Sanskrit base cells.

This appendix explains how the atlas was built and adds seven further surveys. The result is exploratory: coverage depends on the languages selected, the inventory source used for each language, and the decision about which reported sounds count as independent contrasts. The figures show an ordering in these samples and provide a method that can be repeated with other selections.

Together, the body and appendix map the **subcontinental superset** introduced in Chapter 8. Each regional survey captures part of that larger inventory; no individual language contains the whole. Sanskrit's twenty-three base cells provide the comparison target, while additional regional consonants demonstrate that the superset is larger than Sanskrit's selected grid.

## 4.1 The Atlas Method in Depth

The atlas asks one physical question: when a language treats a consonant as an independent contrast, where do that sound's articulatory coordinates place it on a shared mouth-map? The atlas records which of those positions each language keeps as independent grid addresses. It does not compare vocabulary, descent, prestige, script, age, or any of the pyramid's classificatory buckets.[NOTE: language-hotzones-inventory-method]

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

The five Sanskrit-named places (BIL, DEN, RET, PAL, VEL) use their स्थान (*sthāna*) names. The seven other columns use standard labels. The five स्थान (*sthāna*) names define Sanskrit's selection from the broader anatomical space the human voice can reach.

Sanskrit's traditional categories and the comparison grid divide that space differently. Chapter 8 Figure 8.1 retains Sanskrit's own classification. The atlas compares actual pronunciation across languages. It therefore places Sanskrit **र** and **ल** with Tamil **ர** and **ல** in their shared alveolar cells. It also places Sanskrit **स** with the alveolar **s** used by Toda, Kurukh, and the forest-belt languages. This translation allows identical pronunciations to meet without altering Sanskrit's internal arrangement.

**The vertical axis contains thirteen manners.** Thirteen manner rows describe how the consonant is shaped at its place: five stop rows (voiceless unaspirated, voiceless aspirated, voiced unaspirated, voiced aspirated, ejective), two affricate rows (voiceless, voiced), two fricative rows (voiceless, voiced), and one each for nasal, lateral, tap-or-trill, and approximant / glide. The two aspirated stop rows are Sanskrit's महाप्राण (*mahāprāṇa*) row pair, set apart by the strip preset described below. The ejective row appears for languages using the Caucasian or Native American glottal-pressure system; Sanskrit does not light it.

**The strip preset built on महाप्राण (*mahāprāṇa*) isolates the base inventory.** Chapter 8 §8.3 defines a 23-cell Sanskrit base by setting aside the ten महाप्राण (*mahāprāṇa*) stop cells—**ख छ ठ थ फ** and **घ झ ढ ध भ**—running a sensitivity check rather than executing a demotion. Sanskrit's vertical breath axis remains structural, while Chapter 8 needs the base inventory isolated from the breath layer Sanskrit stacks on top. Before comparison, the preset removes manner rows 1 (voiceless aspirated) and 3 (voiced aspirated) from every language's harmonized cell set, systematically removing aspirated stops in any comparison language too. The atlas then measures coverage across the rows Sanskrit's base lights rather than across all manner rows.[NOTE: inventory-atlas-coverage-surveys]

**The distinction between possible sound and assigned address keeps the comparison honest.** Chapter 8 §8.2 introduces it; the full treatment is here.

A *spoken sound-field* is the set of acoustic realizations a language's speakers can and do produce. It includes allophonic variation, contextual realization, dialect-level variation, and the long tail of phonetic detail a careful phonetician would record.

A ***sonomeric grid address*** is a stable inventory position assigned to an independent contrastive unit. Two sounds occupy two addresses only if the language treats them as distinct word-making units.

While Tamil speakers produce voiced stop sounds in real speech, Tamil's contrastive inventory does not assign those voiced realizations independent voiced-stop addresses the way Sanskrit does. The atlas records the inventory rather than every sound a speaker can produce. The same caution governs aspirated stops, palatal-versus-post-alveolar distinctions, and any other case where a language permits sounds that its contrastive inventory does not treat as independent. The atlas records contrastive inventories, matching the level at which Sanskrit selects and arranges its sonomers.

**The coverage criterion is union, not ranking.** For each three-language comparison set, a Sanskrit cell counts as *covered* if at least one of the three languages lights it. Chapter 8 asks whether the subcontinental sound-field — or some other region — supplies enough material to make Sanskrit's base recoverable. Union coverage tests that proposition without conflating it with per-language ranking.

Three languages collectively covering 22 of 23 cells does not mean each language contains 22 of those cells; it means the union of their three inventories intersects Sanskrit's base in 22 places. A language that contributes three or four cells can still carry weight if those cells are otherwise unfilled.

**Inventory provenance is open.** The eleven surveys are computed against a harmonized set of phonemic inventories drawn from standard linguistic descriptions per language. The Python generator `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py` stores every inventory in one place alongside its reference work — Padgett (2003) and Yanushevskaya & Bunčić (2015) for Russian; Tegey & Robson (1996) and Bečka (1969) for Pashto; Schulze (2000), Stilo (2008), and Pirejko (1976) for Talysh; and so on for each comparison language. Anyone who wants to test an alternative inventory choice can edit the file, regenerate the JSON, and rebuild the figure. The reproducibility bundle ships with the figure pipeline.

The inventory choices are conservative and editorial. Verification flags live in `working/40_reference/research/inventory_atlas_coverage_surveys.md` §5: Pashto's full retroflex set, Greek's lack of phonemic /h/, the aspirated/ejective affricate collapse found in Armenian and Georgian, the single Burushaski symbol (ʈʂ) the harmonizer's manner taxonomy does not have a row for. The data trail is visible to any reader who wants it.

The Korku chart uses this conservative policy. Nagaraja's grammar describes a richer retroflex inventory than the atlas currently displays, including retroflex aspirates, a retroflex flap, and a retroflex lateral.[NOTE: korku-nagaraja-mouth-mind-evidence] Adding those sounds would enrich the Korku chart, but it would not change the present 20-of-23 base-coverage result: the महाप्राण (*mahāprāṇa*) preset removes the aspirated rows, while the added retroflex flap and lateral occupy addresses outside the 23 Sanskrit base cells counted here. The appendix therefore reports the current count and separately records the fuller inventory.

The method is narrow and reproducible. It turns Chapter 8's comparison into numbers the reader can audit.

## 4.2 Santali-Inclusive Munda Control: 20 of 23

The body's Forest-Belt Survey set Santali aside because the machinery treats Santali as Indic-influenced. The substitution costs nothing: Korku, Mundari, and Santali cover the same 20 of 23 cells Korku + Mundari + Ho covers.

The unfilled letters match the body set too: **ण · ष · श**.

![Figure A.4.1 — Munda Survey: 20 of 23 Sanskrit base cells. Korku, Mundari, and Santali cover the same 20 cells the body's Forest-Belt Survey covers, with the same unfilled set (ण · ष · श).](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=100%}

Santali's heavier Indic absorption does not move the count in this substitution. Both sampled forest-belt sets cover 20 of Sanskrit's 23 base cells and leave the same retroflex nasal and two sibilants unfilled.

## 4.3 Santali-Free Mixed Control: 21 of 23

The Mixed Control swaps Santali for Burushaski — the Hunza Valley language-isolate sitting outside every family tree assigned within the subcontinent — and pairs it with Korku and Mundari.

![Figure A.4.2 — Mixed Control: 21 of 23 Sanskrit base cells. Korku, Mundari, and Burushaski leave only ण and श unfilled.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=100% height=80%}

The count rises to 21 of 23. The unfilled set contracts to **ण · श**. Burushaski's retroflex inventory adds **ष**, while the three languages already cover Sanskrit's alveolar **र**, **ल**, and **स**.

The substitution forecloses two of the pyramid's deflections at once. Santali is excluded, so Indic absorption cannot explain the coverage. The all-Munda framing is also broken. Three languages drawn from different pyramid classifications, all sitting in or adjacent to the central forest belt and the north-western frontier, cover 21 cells.

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 18 of 23

The machinery classifies Munda alongside two other branches under the umbrella *"Austro-Asiatic"*: a Khasian branch in the Meghalaya highlands and a Nicobaric branch on the Nicobar Islands. The three branches sit at geographically remote subcontinental poles.

The Dispersed Survey picks one representative from each branch: Sora (South Munda, Eastern Ghats and Rushikulya basin), Khasi (Meghalaya highlands), and Nicobarese (Car Nicobar). Coverage falls to 18 of 23. The unfilled set expands to **ट · ड · ण · ष · श** — five cells, two more than the Munda-pure Forest-Belt set the body uses.

![Figure A.4.3 — Dispersed Survey: 18 of 23 Sanskrit base cells. Sora, Khasi, and Nicobarese — three languages the machinery classifies under one *"Austro-Asiatic"* umbrella across three remote subcontinental poles — cover two fewer cells than the all-Munda Forest-Belt Survey.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=100%}

The single pyramid label *"Austro-Asiatic"* places these three languages in one family, but the selected inventories have sharply different shapes. Sora's South Munda inventory lacks the retroflex stops found in North Munda; Khasi uses voiceless-aspirated stops; Nicobarese uses neither retroflex nor aspirated stops in the inventory selected here. Their union covers less of Sanskrit's base than the all-Munda forest-belt samples.

In these samples, the family label does not describe the shared inventory shape. The three languages also come from remote regions of the subcontinent, so family and geography cannot be separated without a larger controlled sample.

## 4.5 Northwest Frontier Survey: 22 of 23

Three north-western contact-zone languages — Pashto (*"Iranian"* by the pyramid's label, Afghanistan and Pakistan tribal belt), Nuristani (a separate IE branch isolated in the Hindu Kush valleys), and Burushaski (the Hunza Valley isolate) — cover 22 of 23, tying the deepest result in the survey. Like the body's Southern Survey, they leave only **श** unfilled.

![Figure A.4.4 — Northwest Frontier Survey: 22 of 23 Sanskrit base cells. Pashto, Nuristani, and Burushaski cover the same 22 cells the deep-south Tamil + Toda + Kurukh set covers. Both leave only श unfilled.](figures/superset/sk_pashto_nuristani_burushaski.svg){#fig:app4-nw-frontier-survey width=100% height=80%}

Two geographically opposite sets — deep south and north-western frontier — deliver the same count and leave the same single cell unfilled. Both regions sit inside the subcontinental retroflex contact zone; both contain nearly the whole base Sanskrit selected.

The set presents a taxonomically mixed profile. The pyramid's label classifies Pashto as *"Iranian"*, the machinery classifies Nuristani as a separate IE branch neither Indic nor Iranian, and Burushaski stands as a language-isolate. Despite those different labels, the selected frontier set ties the southern set. Its inventories use retroflex contrasts associated with the same broad subcontinental contact zone that the deep-south languages preserve.

## 4.6 Iranian Survey: 15 of 23 (Non-Contact Zone)

Three Iranian languages outside the north-western contact zone — Farsi (Iran), Kurdish Kurmanji (northern Iraq, Syria, eastern Turkey), and Talysh (Caspian littoral, Azerbaijan and northern Iran) — cover 15 of 23, the geographic mirror image of the Northwest Frontier Survey. The unfilled set runs **ट · च · ड · ज · ण · ञ · ष · श**: eight cells, including most of the retroflex column.

![Figure A.4.5 — Iranian Survey: 15 of 23 Sanskrit base cells. Three Iranian languages outside the north-western subcontinental contact zone leave most of Sanskrit's retroflex column unfilled.](figures/superset/sk_farsi_kurdish_talysh.svg){#fig:app4-iranian-survey width=100% height=80%}

The selected languages that the pyramid classifies as Sanskrit's "Iranian sister branch" cover seven fewer cells than the mixed Northwest Frontier set.

The contact / non-contact comparison explains the two-cell change in this pair of samples. Swapping Talysh for Balochi — a north-western frontier Iranian language that uses retroflex contrasts from the subcontinental contact zone — moves coverage from 15 to 17. The increase comes from the retroflex grid addresses **ट** and **ड** that Balochi uses and Caspian-littoral Talysh does not. The shared "Iranian" classification alone does not explain the difference.

## 4.7 Caucasus Survey: 13 of 23

Three languages from three different pyramid classifications, all from the Caucasus region — Armenian (a separate IE branch), Georgian (Kartvelian / South Caucasian, outside the IE classification altogether), and Ossetian (Iranian, north Caucasus) — fall to 13 of 23, the floor of the eleven-survey set. The unfilled list runs **ट · च · ड · ज · ण · ञ · ङ · ष · श · व**: ten cells, the largest unfilled list of any survey.

![Figure A.4.6 — Caucasus Survey: 13 of 23 Sanskrit base cells. Three pyramid classifications meet in one geographic region, and this selected set produces the lowest coverage among the eleven surveys.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=100% height=80%}

Three pyramid classifications meet inside one geographic region, yet the selected set reaches only 13 of 23. This is the lowest coverage among the eleven samples.

## 4.8 Slavic & Caucasus IE Survey: 14 of 23

The Slavic & Caucasus IE Survey runs three IE-classified languages along the steppe corridor: Russian and Ukrainian from East Slavic, Ossetian from Caucasian Iranian. Coverage reaches 14 of 23, one cell above the Caucasus floor.

![Figure A.4.7 — Slavic & Caucasus IE Survey: 14 of 23 Sanskrit base cells. Three IE-classified languages along the steppe corridor cover only one cell more than the Caucasus floor and less than the body's Western IE and Central Asian sets.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=100% height=80%}

All three languages share the pyramid's "Indo-European" label that supposedly makes them Sanskrit's relatives. East Slavic and Caucasian Iranian together cover less of Sanskrit's base than the body's Western IE Survey at 16/23 and the Central Asian Tajik + Kazakh + Kyrgyz set at 15/23. Across the selected IE-classified sets, coverage ranges from 14/23 to 22/23 and rises in the sets drawn closer to the subcontinental contact zone.

The steppe corridor — which the pyramid's Aryan-migration story frequently cites as the source region — supplies less of Sanskrit's base material than the deep south, the central forest belt, or the north-western frontier.

## 4.9 The Coverage Cascade

The eleven surveys — four in the body and seven in this appendix — produce the following sample ordering. Sets drawn from the subcontinent and its north-western contact zone occupy the higher rows, while the selected Caucasus and steppe sets occupy the lower rows. A larger preregistered sample would be needed to establish that ordering as a general geographic pattern.

| Coverage | Set | Languages | Source |
|---:|---|---|---|
| **22 / 23** | Southern Survey | Tamil + Toda + Kurukh | body (Ch 8 §8.4) |
| **22 / 23** | Northwest Frontier | Pashto + Nuristani + Burushaski | App 4 §4.5 |
| 21 / 23 | Mixed Control | Korku + Mundari + Burushaski | App 4 §4.3 |
| 20 / 23 | Forest-Belt Survey | Korku + Mundari + Ho | body (Ch 8 §8.4) |
| 20 / 23 | Munda Survey | Korku + Mundari + Santali | App 4 §4.2 |
| 18 / 23 | Dispersed *"Austro-Asiatic"* | Sora + Khasi + Nicobarese | App 4 §4.4 |
| 16 / 23 | Western IE Survey | English + French + Greek | body (Ch 8 §8.4) |
| 15 / 23 | Iranian Survey (non-contact) | Farsi + Kurdish + Talysh | App 4 §4.6 |
| 15 / 23 | Central Asian Survey | Tajik + Kazakh + Kyrgyz | body (Ch 8 §8.4) |
| 14 / 23 | Slavic & Caucasus IE | Russian + Ukrainian + Ossetian | App 4 §4.8 |
| **13 / 23** | Caucasus Survey | Armenian + Georgian + Ossetian | App 4 §4.7 |

**The selected sets closer to the subcontinent show higher coverage.** The two 22/23 results appear at geographically opposite poles — the deep-south Tamil + Toda + Kurukh set and the north-western Pashto + Nuristani + Burushaski set. Both sit inside the subcontinental retroflex contact zone, cover the same 22 cells, and leave only **श** unfilled. The selected Caucasus set produces the lowest result at 13/23.

**The pyramid's "Indo-European" classification does not explain the variation within these samples.** The IE-classified sets range from 14/23 to 22/23. Pashto + Nuristani at the high end carry the same broad IE label as Russian + Ukrainian + Ossetian at the low end, while their positions relative to the subcontinental contact zone differ.

**The selected Iranian languages divide along the contact axis.** Pashto and Balochi, inside the north-western subcontinental contact zone, use retroflex contrasts and contribute to the higher coverage there. Farsi, Kurdish, and Talysh, outside that zone, deliver 15/23 in the selected set. The shared Iranian label does not explain that difference by itself.

**The *"Austro-Asiatic"* samples also vary by geography and branch.** Munda languages inside the central forest belt deliver 20/23, while the dispersed Sora + Khasi + Nicobarese set delivers 18/23. The broad family label does not remove the differences among their sound inventories.

**The body's four figures occupy four points in the larger sample ordering.** Southern Survey (22), Forest-Belt Survey (20), Western IE Survey (16), and Central Asian Survey (15) form the sequence used in Chapter 8. The seven appendix surveys show that several alternate selections reproduce parts of that ordering, while also showing how much the result depends on the chosen languages and inventory descriptions.

Across these samples, Sanskrit's base grid addresses receive their highest coverage from the southern, central forest-belt, and north-western regions of the subcontinent. The machinery sorts those languages into different families, yet the selected inventories repeatedly recover much of the same Sanskrit base. This exploratory result is consistent with the engineering thesis and creates a reproducible test for the transported-cargo story.
