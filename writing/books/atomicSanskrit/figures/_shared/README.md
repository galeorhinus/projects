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

The injection of this comment is handled by a small helper
(`figures/_shared/inject_lineage_comment.py`, planned) so promoting a
stage is one command.

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
