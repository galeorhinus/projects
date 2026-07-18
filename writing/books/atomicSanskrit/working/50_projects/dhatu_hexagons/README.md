# Dhātu Hexagon Visualizer

Standalone Python script that renders Sanskrit *dhātus* as hexagonal-tile SVGs. v1.

Design notes: see `../as_dhatu_hexagon_design_notes.md`.

## Encoding

| Property | Visual channel |
|---|---|
| **Mātrā duration** (½ / 1 / 2) | Hexagon width (top/bottom edge length) |
| **Sthāna** (place of articulation) | Fill color — kaṇṭhya red, tālavya orange, mūrdhanya yellow, dantya green, oṣṭhya blue, plus compound sites |
| **Voicing class** (aghoṣa / ghoṣa / anunāsika / ūṣman / antaḥstha / vowel) | Fill saturation (lighter = voiceless, darker = voiced) |
| **Aspiration** (alpaprāṇa / mahāprāṇa) | Stroke weight (thin / thick) |
| **Anunāsika** (nasal consonants) | Ordinary consonant tile; no extra dot |
| **Anusvāra ं** | Lower-rail concave-left release socket with one large dot |
| **Visarga ः** | Lower-rail concave-left release socket with two colon-like dots |

Geometry: flat-top hexagons, constant height (all four slanted edges length `e`, at ±60°), variable top/bottom edge length. Vyañjanas ride the upper articulation rail; svaras and ayogavāha ride the lower rail. Adjacent cross-rail units share a slanted edge; same-rail units advance to the next vertex.

## Usage

```bash
python dhatu_hexagon.py "g,a,m" -o output/gam.svg          # गम्
python dhatu_hexagon.py "k,R" -o output/kr.svg             # कृ  (R = ṛ)
python dhatu_hexagon.py "bh,U" -o output/bhu.svg           # भू  (U = ū)
python dhatu_hexagon.py "j,v,a,l" -o output/jval.svg       # ज्वल्
python dhatu_hexagon.py "s,n,i,h" -o output/snih.svg       # स्निह्
```

Each particle is looked up in the built-in `VARNAS` table (Devanagari + IAST + class + sthāna + voicing + aspiration). Class is auto-detected; use `label:CLASS` to override (`C`, `V1`, `V2`).

### ASCII aliases (Harvard-Kyoto)

For terminal convenience when typing IAST diacritics is awkward:

```
A = ā    I = ī    U = ū    R = ṛ    RR = ṝ    lR = ḷ
T = ṭ    Th = ṭh  D = ḍ    Dh = ḍh  N = ṇ
G = ṅ    J = ñ    S = ṣ    z = ś
M = ṃ    H = ḥ
```

Direct IAST also works (e.g., `ṛ`, `ṣ`).

## Files

- `dhatu_hexagon.py` — the script
- `output/` — generated SVGs (run-time output)
- `README.md` — this file

## Future Work

Per `../as_dhatu_hexagon_design_notes.md`:

- JSON input format (replacing the CLI string when complexity grows)
- *Upasarga* attachment (left of *dhātu*)
- *Pratyaya* attachment (right of *dhātu*)
- *Gaṇa* modifications (vikaraṇa augmentation, dhātu reshaping)
- *Kriyā* (verb form) and *śabda* (noun form) full pipelines
- Sandhi-driven edge styling on top of the articulation rails
- Empirical "<10 shapes cover 80%" verification against the *Dhātupāṭha*
