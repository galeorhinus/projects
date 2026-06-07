# `figures/_shared/` — cross-chapter figure resources

This directory holds anything used by figures in more than one chapter:

- `icons/` — small SVG icons re-used as inline marks throughout the book
  (the ten *dhāturacanā* scaffold-shape icons live here; see CLAUDE.md §
  "Scaffold-icon deployment in body text" for the deployment rules).
- `toolkits/` — Python modules (importable) that several chapter scripts
  call into. Each toolkit is one subdirectory, e.g. `toolkits/vocal_tract/`,
  carrying its geometry helpers, renderers, and per-figure config JSON.
- `style.py` — shared typography helpers used by every figure script.

Chapter-specific figures live in `figures/<chapter_slug>/`, not here.

---

## Naming convention (applies to every chapter folder, not just `_shared/`)

Each illustration has a stable `<base>` name. Variants are tracked by a
**`.from-<chain>`** suffix that encodes the pipeline lineage:

```
<base>.py                            # Python source (if any)
<base>.from-py.svg                   # Python's raw output
<base>.from-py-cd.svg                # → Claude Design
<base>.from-py-cd-edit.svg           # → CD → manual edit
<base>.from-hand.svg                 # hand-drawn, no Python
<base>.from-hand-cd.svg              # hand → CD
<base>.svg                           # CANONICAL — what the manuscript references
                                     #   (a copy of whichever from-* is shipping)
```

**Stage tokens:**

| Token | Meaning |
|---|---|
| `py` | Python-script generated |
| `cd` | Passed through Claude Design |
| `edit` | Manually edited (vector tool) |
| `hand` | Hand-drawn from scratch |

The chain reads left-to-right: `from-py-cd-edit` means "started as Python,
then Claude Design, then a manual touch-up."

The bare `<base>.svg` is the **canonical** — it's a copy (not a symlink)
of whichever `from-*` variant is shipping. To advance which stage is
canonical, just `cp <base>.from-<chosen>.svg <base>.svg`.

## Canonical SVG self-documenting header

Every canonical `<base>.svg` carries an XML comment at the top recording
its lineage:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- lineage: py → cd
     canonical-source: <base>.from-py-cd.svg
     updated: YYYY-MM-DD -->
<svg xmlns="http://www.w3.org/2000/svg" ...>
```

## The `_shared/lineage` helper

The lineage comment is injected (and verified) by `_shared/lineage.py`,
invokable as a module from the `figures/` directory:

    # Promote a from-* variant to canonical — injects the lineage comment
    python3 -m _shared.lineage promote <chapter>/<base>.from-<chain>.svg

    # Show lineage of every canonical in a chapter folder
    python3 -m _shared.lineage list <chapter>/

    # Verify that a canonical's content still matches its recorded source
    python3 -m _shared.lineage verify <chapter>/<base>.svg

Promote is what you run after advancing a stage (e.g. when Claude Design
returns a refined SVG and you've saved it as `<base>.from-py-cd.svg`).
List is useful before a build to confirm what's shipping. Verify is the
safety net — if someone edits a canonical by hand instead of through a
proper stage, verify will flag the drift.

The helper writes today's date by default (`datetime.date.today()`).
Pass `--date YYYY-MM-DD` to override (e.g., to reproduce the canonical
exactly from a past commit).

## Why a `_shared/` folder rather than scattering helpers

Two reasons:

1. **Discoverability.** When a chapter script imports a helper, the path
   `from _shared.toolkits.vocal_tract import schematics` makes the
   shared-vs-chapter distinction obvious without grepping.
2. **Cleanup invariant.** When a chapter is archived or rewritten,
   `figures/<chapter_slug>/` can be deleted wholesale without worrying
   about cross-chapter breakage. Anything in `_shared/` is, by definition,
   not chapter-disposable.

---

*Convention adopted 2026-06-07. Full migration is being staged across
~9 commits; see the active TODO list or `git log -- atomicSanskrit/figures/`
for the running history.*
