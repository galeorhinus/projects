# Figure Font-Size Audit

Audit and width-feasibility pass only. No manuscript files or figure files were changed.

## Assumptions

- Layout basis: `trade` text width assumed as **4.50 in**.
- Minimum target for print labels: **6.0 pt**.
- Comfortable target for print labels: **7.0 pt**.
- Current markdown percentage widths are converted against that text width.
- Effective font size is calculated as `svg_font_size * proposed_width_in * 72 / viewBox_width`.
- The audit measures only live SVG text with `font-size` declarations.
- Figures whose text has been converted to paths are marked as outlined/path text.

## Summary

- SVG figure references scanned: **38**
- Unique SVG files referenced: **36**
- Unique SVGs with live measurable text: **34**
- Unique SVGs with outlined/path text: **2**
- Missing SVG files: **0**
- References with measurable effective font sizes: **36**

Flags:
- contains 6-7pt text: 1
- contains <6pt text: 34
- outlined/path text: 2

Width-only feasibility:
- current width clears target: 2
- manual visual check: 2
- needs redraw or font-size bump: 29
- width-only fix possible: 5

## Audit Table

| Figure | Source | Current width | Proposed width | SVG viewBox | SVG font sizes | Effective print sizes | Flag |
|---|---:|---:|---:|---:|---:|---:|---|
| `fig:preface-domains-modes-matrix` | `as_0_01_preface.md:74` | `80%` | 3.60 in | 720×470 | 11.00–24.00 | 3.96–8.64 pt | contains <6pt text |
| `fig:preface-orthodoxy-flattening` | `as_0_01_preface.md:78` | `80%` | 3.60 in | 780×420 | 11.00–21.00 | 3.66–6.98 pt | contains <6pt text |
| `fig:mapping-mouth-modern-speech-map` | `as_1_07_adivadya.md:59` | `90%` | 4.05 in | 690×660 | 12.00–22.00 | 5.07–9.30 pt | contains <6pt text |
| `fig:mapping-mouth-sonomeric-garland` | `as_1_08_mapping_mouth.md:25` | `100%` | 4.50 in | 1240×1723 | 31.00–96.00 | 8.10–25.08 pt |  |
| `fig:mapping-mouth-control-panel` | `as_1_08_mapping_mouth.md:159` | `100%` | 4.50 in | 1040×870 | 10.50–26.00 | 3.27–8.10 pt | contains <6pt text |
| `fig:building-dhatuh-matra-envelope` | `as_1_10_building_dhatuh.md:121` | `95%` | 4.28 in | 840×790 | 9.00–22.00 | 3.30–8.06 pt | contains <6pt text |
| `fig:building-dhatuh-racana-scaffold` | `as_1_10_building_dhatuh.md:133` | `85%` | 3.83 in | 900×540 | 11.00–22.00 | 3.37–6.73 pt | contains <6pt text |
| `fig:building-dhatuh-particle-count` | `as_1_10_building_dhatuh.md:166` | `80%` | 3.60 in | 334×197 | 9.00 | 6.99 pt | contains 6-7pt text |
| `fig:building-dhatuh-matra-distribution` | `as_1_10_building_dhatuh.md:172` | `85%` | 3.83 in | 391×204 | — | — pt | outlined/path text |
| `fig:building-dhatuh-top-ten-racanas` | `as_1_10_building_dhatuh.md:188` | `95%` | 4.28 in | 870×681 | 16.00–20.00 | 5.66–7.07 pt | contains <6pt text |
| `fig:building-dhatuh-scaffold-deployment` | `as_1_10_building_dhatuh.md:294` | `95%` | 4.28 in | 920×360 | 13.00–16.00 | 4.35–5.35 pt | contains <6pt text |
| `fig:building-dhatuh-role-map` | `as_1_10_building_dhatuh.md:367` | `95%` | 4.28 in | 800×620 | 11.00–32.00 | 4.23–12.31 pt | contains <6pt text |
| `fig:building-kriya-vedic-eti` | `as_1_11_building_kriya.md:33` | `75%` | 3.38 in | 488×490 | 11.00–22.00 | 5.48–10.95 pt | contains <6pt text |
| `fig:building-kriya-vedic-asti` | `as_1_11_building_kriya.md:47` | `75%` | 3.38 in | 478×421 | 9.00–22.00 | 4.58–11.18 pt | contains <6pt text |
| `fig:building-kriya-vedic-yajati` | `as_1_11_building_kriya.md:61` | `75%` | 3.38 in | 548×421 | 11.00–22.00 | 4.88–9.76 pt | contains <6pt text |
| `fig:building-kriya-vedic-bhavati` | `as_1_11_building_kriya.md:75` | `75%` | 3.38 in | 578×421 | 11.00–22.00 | 4.62–9.25 pt | contains <6pt text |
| `fig:building-kriya-vedic-rajati` | `as_1_11_building_kriya.md:89` | `75%` | 3.38 in | 608×421 | 11.00–22.00 | 4.40–8.79 pt | contains <6pt text |
| `fig:building-kriya-panini-eti` | `as_1_11_building_kriya.md:146` | `75%` | 3.38 in | 578×569 | 11.00–22.00 | 4.62–9.25 pt | contains <6pt text |
| `fig:building-kriya-panini-asti` | `as_1_11_building_kriya.md:150` | `75%` | 3.38 in | 583×569 | 9.00–22.00 | 3.75–9.17 pt | contains <6pt text |
| `fig:building-kriya-panini-yajati` | `as_1_11_building_kriya.md:154` | `75%` | 3.38 in | 630×569 | 11.00–22.00 | 4.24–8.49 pt | contains <6pt text |
| `fig:building-kriya-panini-bhavati` | `as_1_11_building_kriya.md:158` | `75%` | 3.38 in | 660×569 | 11.00–22.00 | 4.05–8.10 pt | contains <6pt text |
| `fig:building-kriya-panini-rajati` | `as_1_11_building_kriya.md:162` | `75%` | 3.38 in | 690×569 | 11.00–22.00 | 3.87–7.75 pt | contains <6pt text |
| `fig:ganah-racana-gana-matrix` | `as_1_11_building_kriya.md:211` | `100%` | 4.50 in | 994×572 | 11.00–22.00 | 3.59–7.17 pt | contains <6pt text |
| `fig:ganah-reactivity-tiers` | `as_1_11_building_kriya.md:262` | `88%` | 3.96 in | 920×290 | 14.00–16.00 | 4.34–4.96 pt | contains <6pt text |
| `fig:ganah-periodic-axes` | `as_1_11_building_kriya.md:326` | `100%` | 4.50 in | 780×531 | 7.00–11.00 | 2.91–4.57 pt | contains <6pt text |
| `fig:ganah-canonical-rank-trajectory` | `as_1_11_building_kriya.md:348` | `90%` | 4.05 in | 600×362 | 8.00–11.00 | 3.89–5.35 pt | contains <6pt text |
| `fig:building-vakya-pipeline` | `as_1_12_building_vakya.md:35` | `90%` | 4.05 in | 900×330 | 10.00–24.00 | 3.24–7.78 pt | contains <6pt text |
| `fig:building-vakya-visual-key` | `as_1_12_building_vakya.md:57` | `85%` | 3.83 in | 760×430 | 10.00–24.00 | 3.62–8.70 pt | contains <6pt text |
| `fig:building-vakya-kr-hlad` | `as_1_12_building_vakya.md:89` | `80%` | 3.60 in | 740×310 | 10.00–24.00 | 3.50–8.41 pt | contains <6pt text |
| `fig:building-vakya-head-bonds` | `as_1_12_building_vakya.md:107` | `95%` | 4.28 in | 940×515 | 9.00–24.00 | 2.95–7.86 pt | contains <6pt text |
| `fig:building-vakya-tail-bonds` | `as_1_12_building_vakya.md:130` | `95%` | 4.28 in | 1000×845 | 9.00–24.00 | 2.77–7.39 pt | contains <6pt text |
| `fig:building-vakya-kr-bonding-matrix` | `as_1_12_building_vakya.md:153` | `95%` | 4.28 in | 980×500 | 12.00–24.00 | 3.77–7.54 pt | contains <6pt text |
| `fig:building-vakya-rca-role-marker` | `as_1_12_building_vakya.md:177` | `85%` | 3.83 in | 840×250 | 11.00–34.00 | 3.61–11.15 pt | contains <6pt text |
| `fig:building-vakya-sentence-full-hex` | `as_1_12_building_vakya.md:213` | `100%` | 4.50 in | 1736×335 | 10.00–27.00 | 1.87–5.04 pt | contains <6pt text |
| `fig:building-vakya-vivimorphosis` | `as_1_12_building_vakya.md:235` | `95%` | 4.28 in | 1080×310 | 11.00–24.00 | 3.14–6.84 pt | contains <6pt text |
| `fig:app5-position-roles` | `as_3_05_by_the_numbers.md:173` | `95%` | 4.28 in | 456×619 | — | — pt | outlined/path text |
| `fig:app5-reactivity-tiers` | `as_3_05_by_the_numbers.md:483` | `88%` | 3.96 in | 920×290 | 14.00–16.00 | 4.34–4.96 pt | contains <6pt text |
| `fig:app5-canonical-rank-trajectory` | `as_3_05_by_the_numbers.md:504` | `90%` | 4.05 in | 600×362 | 8.00–11.00 | 3.89–5.35 pt | contains <6pt text |

## Width-Only Feasibility

| Figure | Current proposed width | Smallest current print text | Width for target | Width for comfort | Verdict |
|---|---:|---:|---:|---:|---|
| `fig:preface-domains-modes-matrix` | 3.60 in | 3.96 pt | 5.45 in | 6.36 in | needs redraw or font-size bump |
| `fig:preface-orthodoxy-flattening` | 3.60 in | 3.66 pt | 5.91 in | 6.89 in | needs redraw or font-size bump |
| `fig:mapping-mouth-modern-speech-map` | 4.05 in | 5.07 pt | 4.79 in | 5.59 in | needs redraw or font-size bump |
| `fig:mapping-mouth-sonomeric-garland` | 4.50 in | 8.10 pt | 3.33 in | 3.89 in | current width clears target |
| `fig:mapping-mouth-control-panel` | 4.50 in | 3.27 pt | 8.25 in | 9.63 in | needs redraw or font-size bump |
| `fig:building-dhatuh-matra-envelope` | 4.28 in | 3.30 pt | 7.78 in | 9.07 in | needs redraw or font-size bump |
| `fig:building-dhatuh-racana-scaffold` | 3.83 in | 3.37 pt | 6.82 in | 7.95 in | needs redraw or font-size bump |
| `fig:building-dhatuh-particle-count` | 3.60 in | 6.99 pt | 3.09 in | 3.61 in | current width clears target |
| `fig:building-dhatuh-matra-distribution` | 3.83 in | — | — | — | manual visual check |
| `fig:building-dhatuh-top-ten-racanas` | 4.28 in | 5.66 pt | 4.53 in | 5.29 in | needs redraw or font-size bump |
| `fig:building-dhatuh-scaffold-deployment` | 4.28 in | 4.35 pt | 5.90 in | 6.88 in | needs redraw or font-size bump |
| `fig:building-dhatuh-role-map` | 4.28 in | 4.23 pt | 6.06 in | 7.07 in | needs redraw or font-size bump |
| `fig:building-kriya-vedic-eti` | 3.38 in | 5.48 pt | 3.70 in | 4.31 in | width-only fix possible |
| `fig:building-kriya-vedic-asti` | 3.38 in | 4.58 pt | 4.43 in | 5.16 in | width-only fix possible |
| `fig:building-kriya-vedic-yajati` | 3.38 in | 4.88 pt | 4.15 in | 4.84 in | width-only fix possible |
| `fig:building-kriya-vedic-bhavati` | 3.38 in | 4.62 pt | 4.38 in | 5.11 in | width-only fix possible |
| `fig:building-kriya-vedic-rajati` | 3.38 in | 4.40 pt | 4.61 in | 5.37 in | needs redraw or font-size bump |
| `fig:building-kriya-panini-eti` | 3.38 in | 4.62 pt | 4.38 in | 5.11 in | width-only fix possible |
| `fig:building-kriya-panini-asti` | 3.38 in | 3.75 pt | 5.40 in | 6.30 in | needs redraw or font-size bump |
| `fig:building-kriya-panini-yajati` | 3.38 in | 4.24 pt | 4.77 in | 5.57 in | needs redraw or font-size bump |
| `fig:building-kriya-panini-bhavati` | 3.38 in | 4.05 pt | 5.00 in | 5.83 in | needs redraw or font-size bump |
| `fig:building-kriya-panini-rajati` | 3.38 in | 3.87 pt | 5.23 in | 6.10 in | needs redraw or font-size bump |
| `fig:ganah-racana-gana-matrix` | 4.50 in | 3.59 pt | 7.53 in | 8.79 in | needs redraw or font-size bump |
| `fig:ganah-reactivity-tiers` | 3.96 in | 4.34 pt | 5.48 in | 6.39 in | needs redraw or font-size bump |
| `fig:ganah-periodic-axes` | 4.50 in | 2.91 pt | 9.28 in | 10.83 in | needs redraw or font-size bump |
| `fig:ganah-canonical-rank-trajectory` | 4.05 in | 3.89 pt | 6.25 in | 7.29 in | needs redraw or font-size bump |
| `fig:building-vakya-pipeline` | 4.05 in | 3.24 pt | 7.50 in | 8.75 in | needs redraw or font-size bump |
| `fig:building-vakya-visual-key` | 3.83 in | 3.62 pt | 6.33 in | 7.39 in | needs redraw or font-size bump |
| `fig:building-vakya-kr-hlad` | 3.60 in | 3.50 pt | 6.17 in | 7.19 in | needs redraw or font-size bump |
| `fig:building-vakya-head-bonds` | 4.28 in | 2.95 pt | 8.70 in | 10.15 in | needs redraw or font-size bump |
| `fig:building-vakya-tail-bonds` | 4.28 in | 2.77 pt | 9.26 in | 10.80 in | needs redraw or font-size bump |
| `fig:building-vakya-kr-bonding-matrix` | 4.28 in | 3.77 pt | 6.81 in | 7.94 in | needs redraw or font-size bump |
| `fig:building-vakya-rca-role-marker` | 3.83 in | 3.61 pt | 6.36 in | 7.42 in | needs redraw or font-size bump |
| `fig:building-vakya-sentence-full-hex` | 4.50 in | 1.87 pt | 14.47 in | 16.88 in | needs redraw or font-size bump |
| `fig:building-vakya-vivimorphosis` | 4.28 in | 3.14 pt | 8.18 in | 9.55 in | needs redraw or font-size bump |
| `fig:app5-position-roles` | 4.28 in | — | — | — | manual visual check |
| `fig:app5-reactivity-tiers` | 3.96 in | 4.34 pt | 5.48 in | 6.39 in | needs redraw or font-size bump |
| `fig:app5-canonical-rank-trajectory` | 4.05 in | 3.89 pt | 6.25 in | 7.29 in | needs redraw or font-size bump |

## Duplicate Figure References

- `figures/build/ganah_canonical_rank_trajectory.svg`: `as_1_11_building_kriya.md:348` (`90%`), `as_3_05_by_the_numbers.md:504` (`90%`)
- `figures/build/ganah_reactivity_tiers.svg`: `as_1_11_building_kriya.md:262` (`88%`), `as_3_05_by_the_numbers.md:483` (`88%`)

## Next Pass

1. Review figures marked `needs redraw or font-size bump`.
2. For figures marked `width-only fix possible`, decide whether the wider figure fits the page.
3. Convert selected markdown width attributes from percentages to inches.
4. Re-render figures where the required width exceeds the text block.
