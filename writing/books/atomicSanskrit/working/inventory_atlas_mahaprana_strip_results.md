# Inventory Atlas — Mahaprana-Strip Sensitivity Check

Date: 2026-06-06

This check compares the normal Sanskrit consonant inventory against every
language in the vocal-tract atlas, then compares the same languages against
Sanskrit with the two mahaprana stop rows removed:

- voiceless aspirated stops: ख छ ठ थ फ
- voiced aspirated stops: घ झ ढ ध भ

The point is not to publish this as a final theorem. The point is to test
whether Sanskrit's aspirated stop layer behaves like an engineering layer
above a more widely shared subcontinental base.

## Result

The test supports the expected direction.

Removing Sanskrit's mahaprana rows raises Jaccard similarity for the central
and southern base inventories: Korku, Gondi, Kurukh, Kolami, Kui, Kuvi, Malto,
Mundari, Tulu, Toda, and Tamil all move upward. It sharply lowers the heavily
Sanskritic-absorbed inventories: Santali, Telugu, Kannada, and Malayalam.

That is the useful Ch9 claim: the aspirated layer is not invisible noise. It
acts like a detachable engineering layer in the atlas.

## Full Table

`normal_jaccard` uses the current Sanskrit atlas with ह placed at the glottal
column. `stripped_jaccard` removes Sanskrit's mahaprana stop rows only.

| Language | Normal Jaccard | Stripped Jaccard | Delta | Normal coverage | Stripped coverage |
|---|---:|---:|---:|---:|---:|
| Korku | 0.472 | 0.654 | +0.182 | 0.850 | 0.850 |
| Gondi | 0.486 | 0.667 | +0.180 | 0.818 | 0.818 |
| Kurukh | 0.486 | 0.667 | +0.180 | 0.818 | 0.818 |
| Kolami | 0.444 | 0.615 | +0.171 | 0.842 | 0.842 |
| Kui | 0.459 | 0.630 | +0.170 | 0.810 | 0.810 |
| Kuvi | 0.459 | 0.630 | +0.170 | 0.810 | 0.810 |
| Malto | 0.459 | 0.630 | +0.170 | 0.810 | 0.810 |
| Mundari | 0.459 | 0.630 | +0.170 | 0.810 | 0.810 |
| Tulu | 0.474 | 0.643 | +0.169 | 0.783 | 0.783 |
| Toda | 0.463 | 0.613 | +0.149 | 0.704 | 0.704 |
| Garo | 0.333 | 0.462 | +0.128 | 0.800 | 0.800 |
| Bodo | 0.324 | 0.444 | +0.120 | 0.750 | 0.750 |
| Brahui | 0.386 | 0.500 | +0.114 | 0.607 | 0.607 |
| Tamil | 0.308 | 0.414 | +0.106 | 0.667 | 0.667 |
| Zulu | 0.333 | 0.438 | +0.104 | 0.609 | 0.609 |
| French | 0.317 | 0.419 | +0.102 | 0.619 | 0.619 |
| Nahuatl | 0.263 | 0.357 | +0.094 | 0.667 | 0.667 |
| Swahili | 0.318 | 0.412 | +0.094 | 0.560 | 0.560 |
| Japanese | 0.286 | 0.375 | +0.089 | 0.571 | 0.571 |
| English | 0.295 | 0.382 | +0.087 | 0.542 | 0.542 |
| Farsi | 0.261 | 0.333 | +0.072 | 0.480 | 0.480 |
| Arabic | 0.163 | 0.205 | +0.042 | 0.333 | 0.333 |
| Mandarin | 0.256 | 0.257 | +0.001 | 0.524 | 0.429 |
| Korean | 0.412 | 0.407 | -0.004 | 0.933 | 0.733 |
| Quechua | 0.295 | 0.270 | -0.025 | 0.542 | 0.417 |
| Lepcha | 0.500 | 0.467 | -0.033 | 0.857 | 0.667 |
| Manipuri | 0.500 | 0.467 | -0.033 | 0.857 | 0.667 |
| Mizo | 0.444 | 0.400 | -0.044 | 0.842 | 0.632 |
| Burushaski | 0.489 | 0.425 | -0.064 | 0.647 | 0.500 |
| Malayalam | 0.744 | 0.487 | -0.256 | 0.829 | 0.543 |
| Kannada | 0.763 | 0.500 | -0.263 | 0.853 | 0.559 |
| Telugu | 0.763 | 0.500 | -0.263 | 0.853 | 0.559 |
| Santali | 0.778 | 0.500 | -0.278 | 0.903 | 0.581 |

## Reading the Coverage Column

Coverage here means: how much of the comparison language's inventory is also
present in Sanskrit. It is asymmetric. Tamil stays at 0.667 in both runs
because removing Sanskrit's mahaprana rows does not remove any Tamil-matching
cells. Tamil's Jaccard rises because the Sanskrit-side non-shared layer got
smaller.

## Reproducibility

Single comparison:

```bash
cd atomicSanskrit/figures/vocal_tract
python3 vocal_tract_overlay.py configs/scatter_sanskrit.json \
  configs/scatter_tamil.json \
  --label-a Sanskrit \
  --label-b Tamil \
  --strip-a mahaprana
```

The batch table above was computed by applying the same `--strip-a mahaprana`
logic to every `scatter_*.json` config except Sanskrit.
