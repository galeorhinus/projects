# Claude Design Illustration Workflow

Use Claude Design by **illustration family**, not by individual figure.

## Core Rule

Create one Claude Design project for each reusable visual system.

Do not create a separate project for every figure if several figures share the same geometry, scale, labels, or visual language. Build one master, then create variants from it.

## Project Type

For static book figures, use:

1. **Template** — best default for reusable figure families.
2. **Slide deck** — use only when a sequence of related figures needs a repeated slide-like layout.
3. **Prototype** — use only for interactive or web-first visuals.
4. **Other** — use only if Claude Design does not offer a better fit.

For most Atomic Sanskrit manuscript figures, choose **Template**.

## Recommended Structure

Mirror the Claude Design organization in the repository:

```text
atomicSanskrit/
  figures/
    design_sources/
      mouth_map/
        brief.md
        style_notes.md
        mouth_map_master.svg
        variants/
          mouth_full_modern_regions.svg
          mouth_sanskrit_selected_regions.svg
          mouth_varnamala_five_sthanas.svg
          mouth_retroflex_focus.svg
          mouth_om_sweep.svg
        exports/
          svg/
          pdf/
          png/
    build/
      mapping_mouth_modern_regions.svg
      mapping_mouth_sanskrit_selection.svg
```

`figures/design_sources/` holds design-source material and variants. `figures/build/` holds final manuscript-ready outputs.

## Figure Family Example

Project: **Mouth Map / Articulation Field**

Use one master base geometry for all of these:

- `mouth_full_modern_regions`
- `mouth_sanskrit_selected_regions`
- `mouth_varnamala_five_sthanas`
- `mouth_retroflex_focus`
- `mouth_om_sweep`
- `mouth_sonomer_grid_link`

The full modern-region figure and the Sanskrit-selection figure should live in the same Claude Design project. The second should be a variant of the first, with non-selected regions faded or de-emphasized, not a new drawing.

## Reuse Rules

1. Create a master base geometry first.
2. Never redraw variants from scratch.
3. Keep the same canvas size across variants in a family.
4. Keep the same coordinate system across variants.
5. Keep the same label style, stroke weight, grayscale palette, and spacing logic.
6. Export final manuscript-ready SVG/PDF into `figures/build`.
7. Keep Claude/Illustrator source material separate from final build files.

## Naming Rules

Use descriptive, chapter-aware names for build outputs:

```text
mapping_mouth_modern_regions.svg
mapping_mouth_sanskrit_selection.svg
mapping_mouth_varnamala_five_sthanas.svg
mapping_mouth_retroflex_focus.svg
mapping_mouth_om_sweep.svg
```

Use shorter internal names inside design-source folders when useful, but final build filenames should make manuscript placement obvious.

## Design Consistency Principle

Visual consistency is part of the argument. If two figures compare stages of the same architecture, they should share the same geometry and visual grammar. The reader should see continuity before reading the caption.

