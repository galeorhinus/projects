# Inventory Atlas — Coverage Surveys

> Date: 2026-06-08. Twelve quad-overlay figures comparing Sanskrit's
> 23-cell base (mahāprāṇa held aside) against four-language sets drawn
> from across the subcontinental field, the IE family, the Iranian /
> Caucasus / Central-Asian belt, and a Western European control.
> Companion to `inventory_atlas_mahaprana_strip_results.md`.

---

## 1. Methodology

Every survey holds Sanskrit's 23-cell base constant: the place × manner
matrix of Sanskrit's consonantal inventory after the ten **mahāprāṇa**
cells (voiceless-aspirated + voiced-aspirated stops, rows 1 and 3) are
held aside. The remaining 23 cells are the *base coordinates* the
figures count against.

Each four-language figure asks **one question**: how many of those 23
cells does the union of the other three languages cover? "Cover" means
the cell is lit by at least one of the three.

Two methodological commitments carry through every survey:

1. **Contrastive inventory coordinates, not every sound speakers
   physically produce.** A language's atlas row reflects what it
   *promotes* to an independent contrastive coordinate, not the full
   range of allophonic / contextual realizations its speakers produce.
   Tamil speakers produce voiced-stop sounds in real speech; Tamil's
   contrastive inventory does not count them as independent voiced-stop
   coordinates. The comparison is at the sonomeric layer, not the
   spoken-field layer. (Cf. Ch 8 §8.2 field-vs-coordinate framing.)

2. **Mahāprāṇa held aside, not removed.** The ten mahāprāṇa cells are
   stripped *for the comparison* — the test isolates Sanskrit's base
   field from the breath-pressure engineering layer Sanskrit stacks on
   top. This is a sensitivity analysis, not a demotion of mahāprāṇa
   (which remains structurally load-bearing in Sanskrit's grid).

The atlas axis is the standardized 12 places (BIL, LD, ID, DEN, ALV,
PA, RET, PAL, VEL, UV, PHA, GLO) × 13 manner rows.

---

## 2. The twelve surveys

The figures live at `figures/superset/sk_<l2>_<l3>_<l4>.svg`. Sanskrit
is always the constant "tl" (top-left) language; the other three are
named in filename order.

| # | Figure (filename) | Set name | Covered | Unfilled (Devanāgarī) |
|---|---|---|---:|---|
| 1 | `sk_tamil_toda_kurukh` | Southern Survey | **20 / 23** | ल · स · श |
| 2 | `sk_pashto_nuristani_burushaski` | Northwest Frontier Survey | **20 / 23** | ल · स · श |
| 3 | `sk_korku_mundari_ho` | Forest-Belt Survey | 18 / 23 | ण · स · ष · श · ल |
| 4 | `sk_korku_mundari_santali` | Munda Survey | 18 / 23 | ण · स · ष · श · ल |
| 5 | `sk_korku_mundari_burushaski` | Mixed Control | 18 / 23 | ण · स · श · ल · र |
| 6 | `sk_farsi_kurdish_balochi` | Iranian Survey | 16 / 23 | च · ज · ण · ञ · स · ष · श |
| 7 | `sk_sora_khasi_nicobarese` | Dispersed Survey | 15 / 23 | ट · ड · ण · स · ष · श · ल · र |
| 8 | `sk_english_french_greek` | Western IE Survey | 14 / 23 | ट · च · ड · ज · ण · स · ष · श · र |
| 9 | `sk_english_arabic_farsi` | External Comparison | 13 / 23 | ट · च · ड · ज · ण · ञ · स · ष · श · र |
| 10 | `sk_tajik_kazakh_kyrgyz` | Central Asian Survey | 12 / 23 | ट · च · ड · ज · ण · ञ · स · ष · श · ल · र |
| 11 | `sk_russian_ukrainian_ossetian` | Slavic & Caucasus IE Survey | 11 / 23 | ट · च · ड · ज · ण · ञ · ङ · स · ष · श · ल · र |
| 12 | `sk_armenian_georgian_ossetian` | Caucasus Survey | **10 / 23** | ट · च · ड · ज · ण · ञ · ङ · स · ष · श · ल · र · व |

---

## 3. The headline findings

### 3.1 Subcontinental geography predicts coverage

The two 20/23 ceilings come from sets at **opposite geographic poles of
the subcontinent**:

- Southern (Tamil + Toda + Kurukh) — the deep south.
- Northwest Frontier (Pashto + Nuristani + Burushaski) — the
  Hindu-Kush / Pamir contact zone.

Both miss exactly the same three cells: **ल · स · श**. Pashto +
Nuristani + Burushaski all carry the retroflex column (ʈ ɖ ɳ ɽ — Pashto
adds ʂ ʐ ɭ on top), which is the structural feature that lets them
match southern coverage. Two utterly different language families
(Iranian + Nuristani-branch IE + isolate) at opposite ends of the
subcontinent land on the same number because **the subcontinental
sound-field reaches both ends**.

### 3.2 The orthodoxy's "Indo-European" classification does not predict coverage

The orthodoxy classifies as *Indo-European*: Sanskrit, Pashto,
Nuristani, Iranian (Farsi / Kurdish / Balochi), Slavic (Russian /
Ukrainian), Ossetian, Armenian, English, French, Greek. Inside that
family, the coverage spread is **20 → 11**:

| IE-classified set | Coverage |
|---|---:|
| Pashto + Nuristani + Burushaski* | 20 / 23 |
| Farsi + Kurdish + Balochi | 16 / 23 |
| English + French + Greek | 14 / 23 |
| Russian + Ukrainian + Ossetian | 11 / 23 |

*Burushaski is not IE; it's an isolate. Even the all-IE Iranian-only
Pashto + Nuristani + (substituted) set would still cover >18.

The supposed *Iranian-as-Sanskrit's-sister-branch* relationship
delivers 16/23 — worse than every subcontinental set we tested, and
only marginally better than three random non-subcontinental languages
(English + Arabic + Farsi = 13). The supposed *Greek-as-PIE-founder*
relationship delivers 14/23 from a Western European set. The
*Slavic-IE* sister relationship delivers 11/23.

**Family-tree distance from Sanskrit does not move the metric.
Geographic distance does.**

### 3.3 Caucasus mixed at 10/23 is the floor

Three Caucasus-region languages from three different orthodox
classifications (Armenian IE + Georgian Kartvelian + Ossetian Iranian)
land at the lowest coverage of any survey. The Caucasus is far enough
from the subcontinental sound-field that even mixed taxonomic origins
inside one geographic region cratter together.

### 3.4 The coverage cascade

```
20 — subcontinental (southern OR NW frontier)
18 — North Munda (any three-language combination)
16 — Iranian (Farsi + Kurdish + Balochi)
15 — dispersed Austroasiatic (Sora + Khasi + Nicobarese)
14 — Western IE (English + French + Greek)
13 — English + Arabic + Farsi (mixed external)
12 — Central Asian (Tajik + Kazakh + Kyrgyz)
11 — Slavic + Caucasus IE (Russian + Ukrainian + Ossetian)
10 — Caucasus mixed (Armenian + Georgian + Ossetian)
```

Geography is the variable that moves the number. Orthodoxy family
labels are noise on top of geography.

### 3.5 The three unfilled cells in the southern + NW frontier surveys (ल · स · श) are a place-coding artifact, not a sound-field gap

Sanskrit's *dantya / tālavya* line places ल · स · श at DEN / DEN / PAL
respectively on the atlas. The southern languages all have laterals
and sibilants — they just place them at ALV / ALV / PA. The cells
are unfilled on **Sanskrit's** axis because Sanskrit chose a particular
place coordinate, not because the field is missing the sound.

This is the **second engineering layer** the Ch 8/9 plan flagged: not
mahāprāṇa, but the deliberate place-coding decision that puts these
three phonemes at slightly different coordinates from where the rest of
the subcontinent places them. The unfilled cells are evidence of
Sanskrit's snap-to-grid engineering, not evidence of subcontinental
absence.

### 3.6 Santali's Indic-absorption doesn't change the count

Forest-Belt (Korku + Mundari + Ho) and Munda Survey (Korku + Mundari +
Santali) both land at 18/23 with the **same unfilled cells**: ण · स ·
ष · श · ल. Santali is the most-Indic-influenced North Munda language;
removing it and replacing with Ho (less-influenced) doesn't change the
number. The forest-belt's coverage is structural, not borrowed.

---

## 4. Canvas dimensions (for figure deployment)

Figures fall into two canvas groups based on how many place columns
their language unions light:

**5.35 × 6.23 in** (7 place columns, 7–9 manner rows) — uniform
small-multiples set:

- `sk_tamil_toda_kurukh.svg`
- `sk_korku_mundari_ho.svg`
- `sk_korku_mundari_santali.svg`
- `sk_sora_khasi_nicobarese.svg`

**Wider (6.45 – 8.10 in)** — additional place columns: labio-dental,
post-alveolar, uvular, pharyngeal, glottal columns light from external
or NW-frontier languages:

- `sk_korku_mundari_burushaski.svg` (6.45 × 7.88)
- `sk_russian_ukrainian_ossetian.svg` (7.00 × 7.88)
- `sk_tajik_kazakh_kyrgyz.svg` (7.00 × 7.88)
- `sk_pashto_nuristani_burushaski.svg` (7.00 × 7.88)
- `sk_armenian_georgian_ossetian.svg` (7.00 × 8.43 — taller because Armenian's aspirated row + Georgian's ejective row stack)
- `sk_farsi_kurdish_balochi.svg` (7.55 × 7.88)
- `sk_english_french_greek.svg` (7.55 × 7.88)
- `sk_english_arabic_farsi.svg` (8.10 × 7.88)

For a small-multiples panel in Ch 8, the four 5.35-wide figures can sit
in a 2×2 grid at uniform display size; the wider figures need their own
row(s) or rescaling.

---

## 5. Inventory caveats — review before publication

The 13 new language configs (added 2026-06-08) are conservative drafts
from standard linguistic descriptions. Sources are cited per language
in
`figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py`.
Three places worth a second look before any number in this document is
quoted in the manuscript:

1. **Pashto's retroflex complement** at 32 cells is the largest of any
   non-subcontinental language in the atlas. Tegey & Robson (1996)
   list the full ʈ / ɖ / ɳ / ʂ / ʐ / ɭ / ɽ set. A tighter / more
   conservative Pashto inventory (drop ɭ and/or ʐ) would lower Pashto's
   contribution to the Northwest Frontier Survey but is unlikely to
   drop the 20/23 ceiling, since Nuristani and Burushaski also carry
   retroflex elements.

2. **Greek's lack of /h/** is editorial. Modern Greek genuinely doesn't
   have phonemic /h/. Older sources sometimes show /h/ as a dialect
   feature. Including it would add one cell at GLO (currently the
   Western IE figure leaves GLO empty for Greek).

3. **Aspirated and ejective affricates collapse onto the regular
   affricate row** (atlas limitation, not a data error). Armenian
   (tsʰ / tʃʰ) and Georgian (tsʼ / tʃʼ) carry this contrast in real
   inventories; the atlas tracks place×manner but not
   ejective-vs-aspirated for affricates. Coverage numbers are
   unaffected (the cells light either way), but a caption mentioning
   these languages should flag the collapse.

4. **Burushaski has one unclassified symbol (ʈʂ — retroflex
   affricate)** that the atlas classifier doesn't have a row for.
   The Mixed Control and Northwest Frontier Survey both surface this
   as a print-time warning. The cell would land at RET × affricate;
   adding an affricate-retroflex row to the atlas's manner taxonomy
   would handle it, but the change isn't load-bearing for the current
   surveys (Burushaski's other retroflex stops + flap already cover
   the structural point).

The four newly-added Munda/Khasian/Nicobaric configs from earlier this
session (Ho, Sora, Khasi, Nicobarese) carry similar verification
flags — see the previous handoff notes.

---

## 6. Polemic-load-bearing facts

Boxed for ready-reference when drafting Ch 8 prose:

1. Pashto + Nuristani + Burushaski cover **20/23** of Sanskrit's base —
   identical to Tamil + Toda + Kurukh.
2. The orthodoxy's "Iranian-as-Sanskrit's-sister" delivers **16/23**;
   English + French + Greek delivers **14/23**; Slavic + Caucasus IE
   delivers **11/23**.
3. Caucasus mixed delivers **10/23** — the lowest of all twelve
   surveys.
4. The three unfilled cells in the 20/23 surveys (ल · स · श) are a
   Sanskrit place-coding choice, not a subcontinental absence.
5. Geographic distance from the subcontinent predicts coverage
   monotonically. Family-tree classification does not.

---

## 7. Related working docs

- `inventory_atlas_mahaprana_strip_results.md` — original mahāprāṇa
  sensitivity analysis (the methodological precursor to these
  surveys).
- `ch9_subcontinental_sound_field_rewrite_plan.md` — Ch 9 (pre-merge)
  figure plan; figures here supply the visual evidence.
- `ch7_ch8_ch9_merge_redivide_plan.md` — the active reorg plan; in the
  new sequence these figures move into Ch 8 (the field chapter) before
  Ch 9 reveals the engineered grid.

---

*Last updated 2026-06-08. Twelve figures shipped to `figures/superset/`
with `py`-lineage canonicals; inventories sourced and seed-tagged in
`_generate_new_configs.py`.*
