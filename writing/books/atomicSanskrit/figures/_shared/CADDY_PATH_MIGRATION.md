# Caddy path-migration notes (2026-06-07)

Every artifact previously at `atomicSanskrit/figures/build/<filename>.svg`
has moved.  Two new directories provide the new locations:

| Old path                                                  | New location                                                      |
|-----------------------------------------------------------|-------------------------------------------------------------------|
| `figures/build/<chapter>_<fig>.svg`                       | `figures/<chapter>/<fig>.svg`                                     |
| `figures/build/vocal_tract/overlay_*.svg`                 | `figures/_shared/toolkits/vocal_tract/output/overlay_*.svg`       |
| `figures/build/vocal_tract/scatter_*.svg`                 | `figures/_shared/toolkits/vocal_tract/output/scatter_*.svg`       |
| `figures/build/vocal_tract/example_vargas.svg`            | `figures/_shared/toolkits/vocal_tract/output/example_vargas.svg`  |
| `figures/icons/scaffold_*.svg`                            | `figures/_shared/icons/scaffold_*.svg`                            |
| `figures/build/about_series/*.svg`                        | `figures/about_series/<name>.svg`                                 |
| `figures/build/adivadya_*.svg`                            | `figures/adivadya/<name>.svg`                                     |
| `figures/build/audiography_*.svg`                         | `figures/audiography/<name>.svg`                                  |
| `figures/build/apabhramsa_*.svg`                          | `figures/apabhramsa/<name>.svg`                                   |
| `figures/build/fourth_abrahamic_*.svg`                    | `figures/fourth_abrahamic/<name>.svg`                             |
| `figures/build/siddha_grammar_*.svg`                      | `figures/siddha_grammar/<name>.svg`                               |
| `figures/build/strategic_*.svg`                           | `figures/strategic/<name>.svg`                                    |
| `figures/build/pie_in_sky_*.svg`                          | `figures/pie_in_sky/<name>.svg`                                   |
| `figures/build/building_dhatuh_*.svg`                     | `figures/building_dhatuh/<name>.svg`                              |
| `figures/build/building_kriya_*.svg`                      | `figures/building_kriya/<name>.svg`                               |
| `figures/build/building_vakya_*.svg`                      | `figures/building_vakya/<name>.svg`                               |
| `figures/build/ch11_valency_*.svg`                        | `figures/building_kriya/valency_*.svg`                            |
| `figures/build/ganah_*.svg`                               | `figures/ganah/<name>.svg`                                        |
| `figures/build/mapping_mouth_*.svg`                       | `figures/mapping_mouth/<name>.svg`                                |
| `figures/build/preface_*.svg`                             | `figures/preface_modes/<name>.svg`                                |

Rule of thumb: the chapter prefix in the filename dropped, and the file
moved into the chapter folder.  The PDF companions (where they exist)
travel alongside the SVG with the same basename.

If Caddy was serving any URL whose path traced to
`atomicSanskrit/figures/build/...`, those URLs need to be updated to
the new layout — either as direct path rewrites, or as Caddy
`handle_path` blocks that map the old prefix to the new chapter folder.
