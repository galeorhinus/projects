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

## Canonical SVG self-documenting header — the injected XML comment

Every canonical `<base>.svg` carries an XML comment at the top recording
its lineage.  The comment is **injected automatically** by `_shared/lineage.py`
during `promote`; do not hand-write it.

### What gets injected

Concretely — `figures/adivadya/hotzones_panels.svg` opens with:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- lineage: py → cd
     canonical-source: hotzones_panels.from-py-cd.svg
     updated: 2026-06-07 -->
<svg xmlns="http://www.w3.org/2000/svg" width="4.5000in" height="5.2830in" ...>
  ...
</svg>
```

Three fields, fixed format:

| Field | What it records | Where it comes from |
|---|---|---|
| `lineage:` | The stage chain, joined by ` → ` | parsed from the `from-<chain>` part of the source filename (hyphens → arrows) |
| `canonical-source:` | The exact `from-*.svg` filename the canonical was copied from | the source argument to `promote` |
| `updated:` | ISO date | `datetime.date.today()` by default; `--date YYYY-MM-DD` to override |

### Where it goes in the file

Immediately after the `<?xml … ?>` declaration, before the `<svg>` root.
If the source has no XML declaration, the comment is prepended to the
file.

### Idempotent

If the canonical already has a lineage comment in that position when
`promote` runs again, the existing comment is **replaced**, not stacked.
This means re-promoting the same source twice produces byte-identical
output (apart from the `updated:` date if the day rolled over).

---

## Promote / verify roundtrip — worked example

Imagine a freshly Python-generated figure that's now coming back from
Claude Design.  Walking through the full lifecycle:

```bash
# Starting state — only Python's output exists.
$ ls figures/adivadya/
hotzones_panels.from-py.svg
hotzones_panels.py

# 1. First promote — make Python output the canonical.
$ cd figures
$ python3 -m _shared.lineage promote adivadya/hotzones_panels.from-py.svg
  → wrote adivadya/hotzones_panels.svg

# Canonical now exists with `lineage: py`.
$ python3 -m _shared.lineage list adivadya/
  canonical             lineage  source                          (updated)
  --------------------  -------  ------------------------------  ---------
  hotzones_panels.svg   py       hotzones_panels.from-py.svg     (2026-06-07)

# 2. Send hotzones_panels.from-py.svg to Claude Design.  Save the
#    returned SVG under the chapter folder with the .from-py-cd.svg
#    suffix (this is the chain advance — `py` becomes `py-cd`).
$ ls figures/adivadya/
hotzones_panels.from-py-cd.svg     ← new, from Claude Design
hotzones_panels.from-py.svg
hotzones_panels.py
hotzones_panels.svg

# 3. Promote the new variant.  The canonical is overwritten and the
#    XML comment records the new lineage.
$ python3 -m _shared.lineage promote adivadya/hotzones_panels.from-py-cd.svg
  → wrote adivadya/hotzones_panels.svg

$ python3 -m _shared.lineage list adivadya/
  canonical             lineage  source                            (updated)
  --------------------  -------  --------------------------------  ---------
  hotzones_panels.svg   py → cd  hotzones_panels.from-py-cd.svg    (2026-06-07)

# 4. Verify — confirm the canonical's content (stripped of its lineage
#    comment) still byte-matches the recorded canonical-source file.
$ python3 -m _shared.lineage verify adivadya/hotzones_panels.svg
  ✓ hotzones_panels.svg: matches hotzones_panels.from-py-cd.svg
```

The two earlier stage variants (`.py` and `.from-py.svg`) are still on
disk — they're never deleted by `promote`.  If you decide tomorrow that
Claude Design's pass made things worse, you can re-promote the Python
variant to roll back:

```bash
$ python3 -m _shared.lineage promote adivadya/hotzones_panels.from-py.svg
  → wrote adivadya/hotzones_panels.svg
```

The canonical is back to `lineage: py` and the CD stage file is still
there for a future do-over.

### When `verify` finds drift

The verify command exists for one reason: someone (often a human, but
sometimes a script) edits the canonical `.svg` directly instead of
editing a `from-*` variant and re-promoting.  That breaks the
convention's "canonical = exact copy of recorded source + lineage
comment" invariant.

If verify flags drift, the fix is one of:

- The edit was small and you want it preserved: copy the canonical
  back over the source variant (`cp <base>.svg <base>.from-<chain>.svg`),
  then re-promote to refresh the comment.
- The edit was a mistake: re-promote from the recorded source to
  clobber the drift.

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
