#!/usr/bin/env python3
"""One-shot generator for the 13 new language scatter configs.

Drafts conservative phonemic inventories from standard linguistic
descriptions and writes the JSON files in the configs/ directory.
Inventories follow the standardized 12-column place axis used by
the other vocal_tract scatter configs.

Reviewability rationale: keeping all 13 inventories in one Python
data structure lets you scan + correct in one place, rather than
opening 13 separate JSON files.  After review, regenerate with
``python3 _generate_new_configs.py``.

Sources (in capsule form — long enough that the choices are
defensible, short enough to fit on one screen each):

 - russian      Padgett (2003); Yanushevskaya & Bunčić (2015)
 - ukrainian    Pugh & Press (1999); Buk et al. (2008)
 - ossetian     Abaev (1964); Erschler (2009)
 - tajik        Perry (2005); Ido (2014)
 - kazakh       Kornfilt (1997); Vajda (1994)
 - kyrgyz       Hebert & Poppe (1963); Imart (1981)
 - pashto       Tegey & Robson (1996); Bečka (1969)
 - nuristani    Strand (2010); Grjunberg (1971)
 - kurdish      MacKenzie (1961); Thackston (2006) — Kurmanji
 - balochi      Jahani & Korn (2009)
 - armenian     Vaux (1998); Dum-Tragut (2009) — Eastern Armenian
 - georgian     Hewitt (1995); Aronson (1990)
 - greek        Holton, Mackridge & Philippaki-Warburton (2012) — Modern
"""
from __future__ import annotations

import json
from pathlib import Path


# -- shared boilerplate parts -----------------------------------------------

CONFIGS_DIR = Path(__file__).resolve().parent

GEOMETRY = {"r1": 2.25, "r2": 2.25, "w": 0.35}
CANVAS = {"width": 4.5, "height": 3.0}
BASE_RIBBON = {
    "t1": 150, "t2": 240,
    "stroke_color": "#bbbbbb", "stroke_size": 0.01,
    "fill_color": "none", "opacity": 0.7,
}
PLACE_LABELS = {
    "labels": [
        "bilabial", "labio-d.", "interdent.", "dental", "alveolar",
        "post-alv.", "retroflex", "palatal", "velar", "uvular",
        "pharyngeal", "glottal",
    ],
    "show_numbers": True,
    "leader_inner_r": 1.9, "leader_gap": 0.1,
    "leader_stroke_color": "#888888", "leader_stroke_width": 0.005,
    "font_size": 0.1528, "color": "#222222",
    "label_gap": 0.05, "bottom_margin": 0.5,
}
ANGULAR_RANGE = {
    "mode": "anatomical",
    "center": 195, "half_width_deg": 45,
    "distances": [0.0, 0.5, 1.0, 1.5, 2.5, 3.5, 3.8, 5.5, 9.0, 11.5, 13.5, 17.0],
}
ROWS_CFG = {"delta_r": 0.1, "r_inner": 2.0}


# -- per-language inventory data --------------------------------------------
# Each entry: (description, seed, matrix-rows).
# Matrix columns are the standard 12 places.

# Column indexes for readability:
# 0  bilabial    1 labio-d.   2 interdent.  3 dental
# 4  alveolar    5 post-alv.  6 retroflex   7 palatal
# 8  velar       9 uvular    10 pharyngeal 11 glottal

LANGS: dict[str, dict] = {
    "russian": {
        "description": (
            "Russian — East Slavic, written in Cyrillic. Standardized "
            "phonemic inventory on the 12-column place axis, with "
            "palatalization (Russian's distinctive 'soft' series — pʲ, "
            "tʲ, kʲ, etc.) NOT represented as separate cells because the "
            "atlas indexes place x manner, not secondary articulation. "
            "Voiceless / voiced stop pairs at 3 places (bilabial, dental, "
            "velar). Two matched nasals (m, n). Voiceless fricatives "
            "f, s, ʃ, x and voiced v, z, ʒ. Affricates ts (alveolar), "
            "tʃ (post-alveolar). Lateral /l/, trill /r/, palatal glide "
            "/j/. Conservative inventory drawn from Padgett (2003) and "
            "Yanushevskaya & Bunčić (2015)."
        ),
        "seed": 180,
        "matrix": [
            # voiceless stops
            ["p", "", "", "t", "",  "",  "", "", "k", "", "", ""],
            # voiced stops
            ["b", "", "", "d", "",  "",  "", "", "g", "", "", ""],
            # nasals
            ["m", "", "", "n", "",  "",  "", "", "",  "", "", ""],
            # voiceless fricatives
            ["",  "f","", "",  "s", "ʃ", "", "", "x", "", "", ""],
            # voiced fricatives
            ["",  "v","", "",  "z", "ʒ", "", "", "",  "", "", ""],
            # affricates
            ["",  "", "", "",  "ts","tʃ","", "", "",  "", "", ""],
            # lateral
            ["",  "", "", "",  "l", "",  "", "", "",  "", "", ""],
            # trill
            ["",  "", "", "",  "r", "",  "", "", "",  "", "", ""],
            # approximants
            ["",  "", "", "",  "",  "",  "", "j","",  "", "", ""],
        ],
    },

    "ukrainian": {
        "description": (
            "Ukrainian — East Slavic, written in Cyrillic. Phonemic "
            "inventory on the standardized 12-column place axis. "
            "Distinctive from Russian primarily in carrying voiced "
            "glottal /ɦ/ where Russian has velar /x/. Stop and nasal "
            "structure matches Russian (no /q/, no retroflex, no "
            "pharyngeal). Fricatives f/v, s/z, ʃ/ʒ, x, ɦ. Affricates "
            "ts, tʃ. Lateral /l/, trill /r/. Bilabial approximant "
            "/w/ alongside palatal /j/. Conservative inventory drawn "
            "from Pugh & Press (1999) and Buk et al. (2008)."
        ),
        "seed": 181,
        "matrix": [
            ["p", "", "", "t", "",  "",  "", "", "k", "", "", ""],
            ["b", "", "", "d", "",  "",  "", "", "g", "", "", ""],
            ["m", "", "", "n", "",  "",  "", "", "",  "", "", ""],
            ["",  "f","", "",  "s", "ʃ", "", "", "x", "", "", ""],
            ["",  "v","", "",  "z", "ʒ", "", "", "",  "", "", "ɦ"],
            ["",  "", "", "",  "ts","tʃ","", "", "",  "", "", ""],
            ["",  "", "", "",  "l", "",  "", "", "",  "", "", ""],
            ["",  "", "", "",  "r", "",  "", "", "",  "", "", ""],
            ["w", "", "", "",  "",  "",  "", "j","",  "", "", ""],
        ],
    },

    "ossetian": {
        "description": (
            "Ossetian — an Iranian language of the central Caucasus "
            "(North Ossetia / South Ossetia), written in Cyrillic. "
            "The defining structural feature is the three-way stop "
            "contrast — voiceless, ejective, voiced — at 4 places "
            "(bilabial, dental, velar, uvular). The ejective row is a "
            "Caucasian areal feature; no other Iranian language carries "
            "it. Two nasals (m, n). Voiceless fricatives f, s, ʃ, x, h; "
            "voiced v, z, ʒ, ɣ. Affricates ts, tʃ (also ejective "
            "counterparts tsʼ, tʃʼ which collapse onto the voiceless-"
            "affricate row on this atlas). Lateral /l/, trill /r/. "
            "Inventory drawn from Abaev (1964) and Erschler (2009)."
        ),
        "seed": 182,
        "matrix": [
            ["p",  "", "", "t",  "",   "",   "", "", "k",  "q",  "", ""],
            ["pʼ", "", "", "tʼ", "",   "",   "", "", "kʼ", "qʼ", "", ""],
            ["b",  "", "", "d",  "",   "",   "", "", "g",  "",   "", ""],
            ["m",  "", "", "n",  "",   "",   "", "", "",   "",   "", ""],
            ["",   "f","", "",   "s",  "ʃ",  "", "", "x",  "",   "", "h"],
            ["",   "v","", "",   "z",  "ʒ",  "", "", "ɣ",  "",   "", ""],
            ["",   "", "", "",   "ts", "tʃ", "", "", "",   "",   "", ""],
            ["",   "", "", "",   "tsʼ","tʃʼ","", "", "",   "",   "", ""],
            ["",   "", "", "",   "l",  "",   "", "", "",   "",   "", ""],
            ["",   "", "", "",   "r",  "",   "", "", "",   "",   "", ""],
            ["",   "", "", "",   "",   "",   "", "j","",   "",   "", ""],
        ],
    },

    "tajik": {
        "description": (
            "Tajik — an Iranian language of Tajikistan (and adjacent "
            "Afghanistan and Uzbekistan), written in Cyrillic; the "
            "Central Asian variety of the broader Persian "
            "(Farsi / Dari / Tajik) continuum. Phonemic inventory on "
            "the standardized 12-column place axis. Voiceless stops at "
            "5 places (bilabial, dental, velar, uvular, glottal); "
            "voiced at 3 (bilabial, dental, velar). Two nasals. "
            "Voiceless fricatives f, s, ʃ, x, h; voiced v, z, ʒ, ɣ. "
            "Affricates tʃ, dʒ (no /ts/). Lateral /l/, trill /r/. "
            "Inventory drawn from Perry (2005) and Ido (2014)."
        ),
        "seed": 183,
        "matrix": [
            ["p", "", "", "t", "",  "",  "", "", "k", "q", "", "ʔ"],
            ["b", "", "", "d", "",  "",  "", "", "g", "",  "", ""],
            ["m", "", "", "n", "",  "",  "", "", "",  "",  "", ""],
            ["",  "f","", "",  "s", "ʃ", "", "", "x", "",  "", "h"],
            ["",  "v","", "",  "z", "ʒ", "", "", "ɣ", "",  "", ""],
            ["",  "", "", "",  "",  "tʃ","", "", "",  "",  "", ""],
            ["",  "", "", "",  "",  "dʒ","", "", "",  "",  "", ""],
            ["",  "", "", "",  "l", "",  "", "", "",  "",  "", ""],
            ["",  "", "", "",  "r", "",  "", "", "",  "",  "", ""],
            ["w", "", "", "",  "",  "",  "", "j","",  "",  "", ""],
        ],
    },

    "kazakh": {
        "description": (
            "Kazakh — a Turkic language of Kazakhstan (and adjacent "
            "regions of China, Mongolia, Russia, Uzbekistan), written "
            "in Cyrillic (transitioning to Latin). Phonemic inventory "
            "on the standardized 12-column place axis. Voiceless stops "
            "at 4 places (bilabial, dental, velar, uvular). Voiced at "
            "3 (bilabial, dental, velar). Three nasals (m, n, ŋ). "
            "Voiceless fricatives s, ʃ, h; voiced z, ʒ, ɣ. Single "
            "affricate tʃ. Lateral /l/, trill /r/. Bilabial /w/ and "
            "palatal /j/ glides. Inventory drawn from Kornfilt (1997) "
            "and Vajda (1994)."
        ),
        "seed": 184,
        "matrix": [
            ["p", "", "", "t", "",  "",  "", "", "k", "q",  "", ""],
            ["b", "", "", "d", "",  "",  "", "", "g", "",   "", ""],
            ["m", "", "", "n", "",  "",  "", "", "ŋ", "",   "", ""],
            ["",  "", "", "",  "s", "ʃ", "", "", "",  "",   "", "h"],
            ["",  "", "", "",  "z", "ʒ", "", "", "",  "ɣ",  "", ""],
            ["",  "", "", "",  "",  "tʃ","", "", "",  "",   "", ""],
            ["",  "", "", "",  "l", "",  "", "", "",  "",   "", ""],
            ["",  "", "", "",  "r", "",  "", "", "",  "",   "", ""],
            ["w", "", "", "",  "",  "",  "", "j","",  "",   "", ""],
        ],
    },

    "kyrgyz": {
        "description": (
            "Kyrgyz — a Turkic language of Kyrgyzstan (and adjacent "
            "regions of China and Tajikistan), written in Cyrillic. "
            "Phonemic inventory on the standardized 12-column place "
            "axis. Voiceless stops at 3 places (bilabial, dental, "
            "velar); voiced at 3. Three nasals (m, n, ŋ). Voiceless "
            "fricatives s, ʃ, h; voiced z, ʒ. Two affricates tʃ, dʒ. "
            "Lateral /l/, trill /r/. Bilabial /w/ and palatal /j/ "
            "glides. Lighter inventory than Kazakh (no native /q ɣ/). "
            "Inventory drawn from Hebert & Poppe (1963) and Imart (1981)."
        ),
        "seed": 185,
        "matrix": [
            ["p", "", "", "t", "",  "",  "", "", "k", "",  "", ""],
            ["b", "", "", "d", "",  "",  "", "", "g", "",  "", ""],
            ["m", "", "", "n", "",  "",  "", "", "ŋ", "",  "", ""],
            ["",  "", "", "",  "s", "ʃ", "", "", "",  "",  "", "h"],
            ["",  "", "", "",  "z", "ʒ", "", "", "",  "",  "", ""],
            ["",  "", "", "",  "",  "tʃ","", "", "",  "",  "", ""],
            ["",  "", "", "",  "",  "dʒ","", "", "",  "",  "", ""],
            ["",  "", "", "",  "l", "",  "", "", "",  "",  "", ""],
            ["",  "", "", "",  "r", "",  "", "", "",  "",  "", ""],
            ["w", "", "", "",  "",  "",  "", "j","",  "",  "", ""],
        ],
    },

    "pashto": {
        "description": (
            "Pashto — an Iranian language of Afghanistan and "
            "north-western Pakistan, written in a Perso-Arabic-derived "
            "script. The defining structural feature on this atlas is "
            "the FULL RETROFLEX column — Pashto carries retroflex "
            "stops (ʈ, ɖ), retroflex nasal (ɳ), retroflex fricatives "
            "(ʂ, ʐ), retroflex flap (ɽ) and retroflex lateral (ɭ), the "
            "complete subcontinental retroflex set acquired via the "
            "north-western contact zone. Voiceless stops at 5 places "
            "(bilabial, dental, retroflex, velar, uvular). Voiced at "
            "4. Nasals m, n, ɳ. Voiceless fricatives f, s, ʃ, ʂ, x, "
            "h; voiced z, ʒ, ʐ, ɣ. Affricates ts, dz, tʃ, dʒ. "
            "Inventory drawn from Tegey & Robson (1996) and Bečka (1969)."
        ),
        "seed": 186,
        "matrix": [
            ["p", "", "", "t", "",  "",   "ʈ", "", "k", "q", "", ""],
            ["b", "", "", "d", "",  "",   "ɖ", "", "g", "",  "", ""],
            ["m", "", "", "n", "",  "",   "ɳ", "", "",  "",  "", ""],
            ["",  "f","", "",  "s", "ʃ",  "ʂ", "", "x", "",  "", "h"],
            ["",  "", "", "",  "z", "ʒ",  "ʐ", "", "ɣ", "",  "", ""],
            ["",  "", "", "",  "ts","tʃ", "",  "", "",  "",  "", ""],
            ["",  "", "", "",  "dz","dʒ", "",  "", "",  "",  "", ""],
            ["",  "", "", "",  "l", "",   "ɭ", "", "",  "",  "", ""],
            ["",  "", "", "",  "r", "",   "ɽ", "", "",  "",  "", ""],
            ["w", "", "", "",  "",  "",   "",  "j","",  "",  "", ""],
        ],
    },

    "nuristani": {
        "description": (
            "Nuristani — the Nuristani languages of eastern Afghanistan "
            "(Kati, Waigali, Ashkun, Prasun, Kalasha-ala); represented "
            "here by a conservative Kati-leaning inventory.  Orthodoxy-"
            "classified as a separate branch of 'Indo-European' "
            "alongside Indic and Iranian.  Carries retroflex stops, "
            "nasal, fricative, and flap (ʈ, ɖ, ɳ, ʂ, ɽ) as a partial "
            "subcontinental match.  Voiceless stops at 5 places "
            "(bilabial, dental, retroflex, palatal, velar); voiced at "
            "5. Four-place nasal series (m, n, ɳ, ɲ). Voiceless "
            "fricatives s, ʃ, ʂ, x, h; voiced z, ʒ, ɣ. Two affricates "
            "tʃ, dʒ. Lateral /l/, trill /r/, retroflex flap /ɽ/. "
            "Inventory drawn from Strand (2010) and Grjunberg (1971)."
        ),
        "seed": 187,
        "matrix": [
            ["p", "", "", "t", "",  "",   "ʈ", "c", "k", "", "", ""],
            ["b", "", "", "d", "",  "",   "ɖ", "ɟ", "g", "", "", ""],
            ["m", "", "", "n", "",  "",   "ɳ", "ɲ", "",  "", "", ""],
            ["",  "", "", "",  "s", "ʃ",  "ʂ", "",  "x", "", "", "h"],
            ["",  "", "", "",  "z", "ʒ",  "",  "",  "ɣ", "", "", ""],
            ["",  "", "", "",  "",  "tʃ", "",  "",  "",  "", "", ""],
            ["",  "", "", "",  "",  "dʒ", "",  "",  "",  "", "", ""],
            ["",  "", "", "",  "l", "",   "",  "",  "",  "", "", ""],
            ["",  "", "", "",  "r", "",   "ɽ", "",  "",  "", "", ""],
            ["w", "", "", "",  "",  "",   "",  "j", "",  "", "", ""],
        ],
    },

    "kurdish": {
        "description": (
            "Kurdish — Kurmanji (Northern Kurdish) inventory; an "
            "Iranian language of eastern Turkey, northern Syria, "
            "northern Iraq, and north-western Iran, written in Latin "
            "(Hawar) or Perso-Arabic-derived script. Phonemic inventory "
            "on the standardized 12-column place axis. Voiceless stops "
            "at 4 places (bilabial, dental, velar, uvular). Voiced at "
            "3. Two nasals. Voiceless fricatives f, s, ʃ, x, ħ, h; "
            "voiced v, z, ʒ, ɣ, ʕ — the pharyngeal pair ħ/ʕ is the "
            "Semitic-contact feature distinguishing Kurdish from its "
            "Iranian cousins further east. Two affricates tʃ, dʒ. "
            "Lateral /l/, trill /r/. Inventory drawn from MacKenzie "
            "(1961) and Thackston (2006)."
        ),
        "seed": 188,
        "matrix": [
            ["p", "", "", "t", "",  "",  "", "", "k", "q", "",  ""],
            ["b", "", "", "d", "",  "",  "", "", "g", "",  "",  ""],
            ["m", "", "", "n", "",  "",  "", "", "",  "",  "",  ""],
            ["",  "f","", "",  "s", "ʃ", "", "", "x", "",  "ħ", "h"],
            ["",  "v","", "",  "z", "ʒ", "", "", "ɣ", "",  "ʕ", ""],
            ["",  "", "", "",  "",  "tʃ","", "", "",  "",  "",  ""],
            ["",  "", "", "",  "",  "dʒ","", "", "",  "",  "",  ""],
            ["",  "", "", "",  "l", "",  "", "", "",  "",  "",  ""],
            ["",  "", "", "",  "r", "",  "", "", "",  "",  "",  ""],
            ["w", "", "", "",  "",  "",  "", "j","",  "",  "",  ""],
        ],
    },

    "balochi": {
        "description": (
            "Balochi — an Iranian language of south-western Pakistan, "
            "south-eastern Iran, and southern Afghanistan, written in "
            "Perso-Arabic-derived script. Like Pashto, Balochi has "
            "acquired the subcontinental retroflex set via the north-"
            "western contact zone — retroflex stops (ʈ, ɖ) and the "
            "retroflex flap (ɽ), though without the full retroflex "
            "fricative / nasal / lateral complement Pashto carries. "
            "Voiceless stops at 4 places (bilabial, dental, retroflex, "
            "velar). Voiced at 4. Two nasals. Voiceless fricatives f, "
            "s, ʃ, h; voiced z, ʒ. Two affricates tʃ, dʒ. Lateral /l/, "
            "trill /r/, retroflex flap /ɽ/. Inventory drawn from "
            "Jahani & Korn (2009)."
        ),
        "seed": 189,
        "matrix": [
            ["p", "", "", "t", "",  "",  "ʈ", "", "k", "", "", ""],
            ["b", "", "", "d", "",  "",  "ɖ", "", "g", "", "", ""],
            ["m", "", "", "n", "",  "",  "",  "", "",  "", "", ""],
            ["",  "f","", "",  "s", "ʃ", "",  "", "",  "", "", "h"],
            ["",  "", "", "",  "z", "ʒ", "",  "", "",  "", "", ""],
            ["",  "", "", "",  "",  "tʃ","",  "", "",  "", "", ""],
            ["",  "", "", "",  "",  "dʒ","",  "", "",  "", "", ""],
            ["",  "", "", "",  "l", "",  "",  "", "",  "", "", ""],
            ["",  "", "", "",  "r", "",  "ɽ", "", "",  "", "", ""],
            ["w", "", "", "",  "",  "",  "",  "j","",  "", "", ""],
        ],
    },

    "armenian": {
        "description": (
            "Armenian — Eastern Armenian variety, written in the "
            "Armenian alphabet. The defining structural feature is the "
            "three-way stop and affricate contrast — voiceless, "
            "voiceless aspirated, voiced — across bilabial, dental, "
            "and velar places, and across the alveolar and post-"
            "alveolar affricate places. The aspirated row is the "
            "feature that places Armenian close to Sanskrit's mahāprāṇa "
            "system, though Armenian's pattern is independent (not a "
            "subcontinental borrowing). Two nasals. Voiceless fricatives "
            "f, s, ʃ, x, h; voiced v, z, ʒ, ɣ. Lateral /l/, trill "
            "/r/. Inventory drawn from Vaux (1998) and Dum-Tragut (2009). "
            "Note: aspirated affricates (tsʰ, tʃʰ) collapse onto the "
            "voiceless-affricate row on this atlas, which lacks a "
            "dedicated aspirated-affricate manner."
        ),
        "seed": 190,
        "matrix": [
            ["p",   "", "", "t",   "",   "",   "", "", "k",   "", "", ""],
            ["pʰ",  "", "", "tʰ",  "",   "",   "", "", "kʰ",  "", "", ""],
            ["b",   "", "", "d",   "",   "",   "", "", "g",   "", "", ""],
            ["m",   "", "", "n",   "",   "",   "", "", "",    "", "", ""],
            ["",    "f","", "",    "s",  "ʃ",  "", "", "x",   "", "", "h"],
            ["",    "v","", "",    "z",  "ʒ",  "", "", "ɣ",   "", "", ""],
            ["",    "", "", "",    "ts", "tʃ", "", "", "",    "", "", ""],
            ["",    "", "", "",    "tsʰ","tʃʰ","", "", "",    "", "", ""],
            ["",    "", "", "",    "dz", "dʒ", "", "", "",    "", "", ""],
            ["",    "", "", "",    "l",  "",   "", "", "",    "", "", ""],
            ["",    "", "", "",    "r",  "",   "", "", "",    "", "", ""],
            ["",    "", "", "",    "",   "",   "", "j","",    "", "", ""],
        ],
    },

    "georgian": {
        "description": (
            "Georgian — a Kartvelian (South Caucasian) language of "
            "Georgia, written in the Georgian (Mkhedruli) script. "
            "Kartvelian is NOT classified by the orthodoxy as part of "
            "the 'Indo-European' family — Georgian is here as a "
            "Caucasus-region control. The structural signature is the "
            "three-way stop and affricate contrast — voiceless, "
            "ejective, voiced — across 4 stop places (bilabial, dental, "
            "velar, uvular). Two nasals. Voiceless fricatives v, s, ʃ, "
            "x, h (note Georgian has /v/ classed as a fricative, not "
            "/f/); voiced z, ʒ, ɣ. Lateral /l/, trill /r/. No phonemic "
            "glides. Inventory drawn from Hewitt (1995) and Aronson "
            "(1990). Ejective affricates (tsʼ, tʃʼ) collapse onto the "
            "voiceless-affricate row on this atlas."
        ),
        "seed": 191,
        "matrix": [
            ["p",   "", "", "t",   "",    "",    "", "", "k",  "q",  "", ""],
            ["pʼ",  "", "", "tʼ",  "",    "",    "", "", "kʼ", "qʼ", "", ""],
            ["b",   "", "", "d",   "",    "",    "", "", "g",  "",   "", ""],
            ["m",   "", "", "n",   "",    "",    "", "", "",   "",   "", ""],
            ["",    "v","", "",    "s",   "ʃ",   "", "", "x",  "",   "", "h"],
            ["",    "", "", "",    "z",   "ʒ",   "", "", "ɣ",  "",   "", ""],
            ["",    "", "", "",    "ts",  "tʃ",  "", "", "",   "",   "", ""],
            ["",    "", "", "",    "tsʼ", "tʃʼ", "", "", "",   "",   "", ""],
            ["",    "", "", "",    "dz",  "dʒ",  "", "", "",   "",   "", ""],
            ["",    "", "", "",    "l",   "",    "", "", "",   "",   "", ""],
            ["",    "", "", "",    "r",   "",    "", "", "",   "",   "", ""],
        ],
    },

    "greek": {
        "description": (
            "Greek — Modern Standard Greek, written in the Greek "
            "alphabet. Phonemic inventory on the standardized 12-column "
            "place axis. The distinctive feature on this atlas is the "
            "interdental fricative pair (θ, ð) — preserved from "
            "Ancient Greek in the same column where most other "
            "comparison languages are empty. Voiceless and voiced stop "
            "pairs at 3 places (bilabial, dental, velar). Two nasals. "
            "Voiceless fricatives f, θ, s, x; voiced v, ð, z, ɣ. "
            "Affricates ts, dz (alveolar; no post-alveolar /tʃ dʒ/ — "
            "Modern Greek lacks the post-alveolar series most other IE "
            "comparison languages have). Lateral /l/, trill /r/, "
            "palatal /j/. Inventory drawn from Holton, Mackridge & "
            "Philippaki-Warburton (2012)."
        ),
        "seed": 192,
        "matrix": [
            ["p", "", "", "t", "",  "", "", "", "k", "", "", ""],
            ["b", "", "", "d", "",  "", "", "", "g", "", "", ""],
            ["m", "", "", "n", "",  "", "", "", "",  "", "", ""],
            ["",  "f","θ","",  "s", "", "", "", "x", "", "", ""],
            ["",  "v","ð","",  "z", "", "", "", "ɣ", "", "", ""],
            ["",  "", "", "",  "ts","", "", "", "",  "", "", ""],
            ["",  "", "", "",  "dz","", "", "", "",  "", "", ""],
            ["",  "", "", "",  "l", "", "", "", "",  "", "", ""],
            ["",  "", "", "",  "r", "", "", "", "",  "", "", ""],
            ["",  "", "", "",  "",  "", "", "j","",  "", "", ""],
        ],
    },
}


def build_config(slug: str, entry: dict) -> dict:
    return {
        "name": f"scatter_{slug}",
        "description": entry["description"],
        "geometry": GEOMETRY,
        "canvas": CANVAS,
        "base_ribbon": BASE_RIBBON,
        "scatter": {
            "mode": "grid",
            "angular_range": ANGULAR_RANGE,
            "rows": ROWS_CFG,
            "jitter": {"theta_deg": 2.0, "r": 0.03, "seed": entry["seed"]},
            "circle_radius": 0.05,
            "fill_color": "#666666",
            "opacity": 0.5,
            "place_labels": PLACE_LABELS,
            "matrix": entry["matrix"],
        },
    }


def main() -> int:
    for slug, entry in LANGS.items():
        cfg = build_config(slug, entry)
        out = CONFIGS_DIR / f"scatter_{slug}.json"
        out.write_text(
            json.dumps(cfg, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  wrote {out.name}")
    print(f"\n{len(LANGS)} configs written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
