# Mouth Cross-Section Base — Design Brief

*Working reference for the shared sagittal-cross-section illustration used as the base for Chapter 7 (Ādivādya: The Anatomy of Sound) and downstream Ch 8 / Appendix Part 3 phonetic figures.*

**Status:** brief — base SVG not yet produced.
**Source for the base:** drawn in Illustrator, exported as SVG to `figures/build/`.
**Companion stock references:** three Shutterstock images in this folder, used as visual guidance only (not as the base itself).

---

## Purpose

The book's Ch 7 / Ch 8 / App Part 3 sequence treats the vocal apparatus as the instrument out of which Sanskrit's *varṇamālā* selects its phonemes. Several figures in those chapters need to overlay arrows, highlights, vowel-position tongue redraws, and Sanskrit place-of-articulation labels onto an anatomically faithful sagittal cross-section.

This brief identifies what the shared base needs to contain so that every derived figure (Om sweep, five-sthāna map, vowel-space figure, visarga/anusvāra breath gesture, prāṇāyāma figure, etc.) can pull from the same source without redrawing the anatomy.

---

## Reference images in this folder

Three Shutterstock-licensed images downloaded as visual references:

| Filename | What it shows | Use as |
|---|---|---|
| `stock-vector-throat-anatomy-in-sagittal-view-infographic-poster-pharynx-larynx-nasal-and-oral-cavities-2644659117.jpg` | Black-silhouette head profile; cavities color-blocked (nasal pharynx, oral pharynx, laryngeal pharynx, nasal cavity, oral cavity, larynx) | **Skip.** Too abstract. Color zones are exactly what overlays will need to add — having them baked into the base leaves no room for differentiation. |
| `stock-vector-upper-respiratory-tract-anatomy-nose-throat-mouth-respiratory-system-1578586936.jpg` | Highly detailed medical illustration in browns/tans — bone texture, conchae, sinuses, vertebrae, hyoid, thyroid cartilage, etc. | **Anatomical accuracy reference.** Use to verify structure positions and shapes; do NOT redraw at this level of detail. |
| `stock-vector-vocal-cords-the-human-voice-1609371985.jpg` | Mid-detail sagittal view with browns/tans, plus inset circles showing vocal cords open/closed | **Style and detail-level target.** The closest match to the level of complexity the book figure needs. |

---

## Recommendation

**Redraw the base in Illustrator using Image 3 (`stock-vector-vocal-cords...`) as the style and detail-level target. Use Image 2 (`stock-vector-upper-respiratory-tract...`) as the anatomical accuracy reference. Ignore Image 1.**

Image 3 sits at the sweet spot: enough specificity that the reader recognizes anatomy at a glance, not so much that overlays compete with the base.

---

## What Image 3 covers

| Element | Status in Image 3 |
|---|---|
| Head profile / face outline | ✓ rendered |
| Oral cavity (as a space) | ✓ shown |
| Nasal cavity (as a space) | ✓ shown |
| Pharynx | ✓ shown as a single zone |
| Tongue | ✓ shown as a single mass |
| Vocal cords | ✓ shown and labeled |
| Epiglottis | ✓ shown and labeled |
| Trachea | ✓ shown |
| Hard palate (roof) | ✓ visible (but undifferentiated from soft palate) |

That's nine of the ~25 named structures the base needs. Image 3 is a solid foundation but incomplete.

---

## Critical missing elements — must add when redrawing

These are anatomical structures derived figures will require, and which Image 3 either omits or doesn't make distinct.

| Element | Why the book needs it | Reference image |
|---|---|---|
| **Upper lip + lower lip as distinct shapes** | Bilabial (*oṣṭhya*) articulation, Om's `m` closure, rounded vowel positions for `u`. Image 3 shows a closed mouth profile, not separable lips. | Image 2 has them defined |
| **Hard palate vs. soft palate (velum) — visible boundary** | *Tālavya* (palatal) vs. *kaṇṭhya* (velar) — the key Pāṇinian distinction. Image 3 renders them as a continuous brown band. | Image 2 distinguishes them clearly |
| **Soft palate as a hinged / movable structure** | Nasal coupling — the velum drops for nasals and *anusvāra*, rises to seal for non-nasals. Needs to be a visible structure that can be redrawn in two positions across figures. | Image 2 |
| **Uvula** | Visible anatomical landmark; hangs from the soft palate; helps the reader locate the velar zone instantly. | Image 2 |
| **Alveolar ridge** (the bony ridge behind upper teeth) | Retroflex / dental contact zone (*mūrdhanya* / *dantya* boundary). Image 3 has nothing where this should be. | Image 2 has it implicit between teeth and palate |
| **Tongue subdivisions** — tip, blade, body, root as faint internal lines | Vowel-position figures redraw the tongue's high point at different locations. Without internal subdivision marks, the figures can't show "tongue body high-back for *u*" vs. "tongue body low-central for *a*". | Neither stock image subdivides — add this yourself |
| **Nasal coupling point** (where nasal cavity opens into oropharynx behind the velum) | *Anusvāra* figures show air diverting upward through this opening. Currently invisible in Image 3. | Image 2 hints at it; Image 1 actually shows the nasopharynx zone |

---

## Useful additions — recommended

| Element | Why | Reference image |
|---|---|---|
| **Upper teeth (incisors) clearly in cross-section** | Dental (*dantya*) articulation; visible landmark at the front of the mouth. | Image 2 |
| **Lower teeth + mandible (jaw)** | Visual anchor for the lower face; the jaw moves in articulation. | Image 2 |
| **Glottis as a visible gap between the vocal cords** | *Visarga* figures show the glottis opening; voicing figures show it vibrating. Image 3's main view draws the cords as a solid bar; its inset shows the gap correctly. | Image 2 / Image 3 inset |
| **Larynx outline as distinct from surrounding tissue** | Houses the vocal cords; useful labeled anchor. | Image 2 |
| **Lungs (small inset or arrow at bottom)** | Breath-source figures (*prāṇa*, *prāṇāyāma*, Om's continuous airstream) need a clear source. Image 3 ends at the trachea. | Add yourself — small lungs inset bottom-left of the cross-section, or an upward arrow at the trachea labeled *prāṇa* · प्राण |

---

## Skip these — not needed for phonetics

| Element | Why skip |
|---|---|
| Esophagus | In Image 3; not phonetics-relevant. Omit. |
| Vertebrae / spine | In Image 2; visual noise. Omit. |
| Sinuses (frontal, sphenoidal) | In Image 2; not phonetics-relevant. Omit. |
| Conchae (superior, middle, inferior) | In Image 2; not phonetics-relevant. Omit. |
| Tonsils (pharyngeal, palatine, lingual) | In Image 2; not phonetics-relevant. Omit. |
| Auditory tube, sella turcica | In Image 2; not phonetics-relevant. Omit. |
| Hyoid bone, thyroid cartilage | In Image 2; not needed unless specifically required for medical accuracy in the larynx area. Optional. |

---

## Complete anatomical completeness checklist

When the Illustrator base is finished, every structure below should exist as its own named layer (the name becomes the SVG `<g id="...">` group ID after export). Hidden layers stay in the SVG as named groups but are invisible in the rendered base — claude design can still reference them for positional anchoring.

### Visible layers

- [ ] `face-profile` (outer outline)
- [ ] `lips-upper` *(distinct from lower)*
- [ ] `lips-lower`
- [ ] `teeth-upper` *(visible incisors in section)*
- [ ] `teeth-lower`
- [ ] `mandible` *(jaw outline)*
- [ ] `alveolar-ridge` *(small bump behind upper teeth)*
- [ ] `hard-palate`
- [ ] `soft-palate-velum` *(distinct from hard palate)*
- [ ] `uvula` *(hanging at end of soft palate)*
- [ ] `nasal-cavity`
- [ ] `nasal-passage-opening` *(the coupling point behind velum)*
- [ ] `tongue-tip`
- [ ] `tongue-blade`
- [ ] `tongue-body`
- [ ] `tongue-root`
- [ ] `tongue-outline` *(overall shape)*
- [ ] `oropharynx` *(behind tongue, above larynx)*
- [ ] `epiglottis`
- [ ] `larynx-outline`
- [ ] `vocal-cords` *(two folds)*
- [ ] `glottis-gap` *(the space between them)*
- [ ] `trachea`
- [ ] `lungs-inset` *(optional, bottom corner)*

### Hidden zone-of-articulation layers (for claude design's positional reference)

- [ ] `zone-kanthya-velar`
- [ ] `zone-talavya-palatal`
- [ ] `zone-murdhanya-retroflex`
- [ ] `zone-dantya-dental`
- [ ] `zone-osthya-labial`

Set fill-opacity to 0 (or layer to invisible) before SVG export — the groups stay in the SVG as named anchors; the rendered base shows nothing where they sit.

---

## Style notes for the final base

Think of it as **"Image 3 anatomy, in the book's grayscale palette, with Image 2's anatomical landmarks correctly placed."**

| Style choice | Value |
|---|---|
| Base outline strokes | ~1 pt charcoal `#2b2b2d` |
| Anatomy fills | Light grey `#d4d4d4` (matches `--g-sanskrit` token in `book-assets.css`) |
| Internal subdivisions (tongue parts, palate boundary) | Very faint hairlines, ~0.25 pt at `#cccccc` |
| Textures, shading gradients, stippling | None — clean line work only |
| Color | Greyscale only; no full-saturation colors anywhere in the base |
| Background | `#f4f4f3` (book canonical warm off-white) |
| Optional zone overlays in Illustrator | Drawn in faint warm tints for the artist's positioning reference only; **invisible in exported SVG** |

The base should read as a **quiet, anatomically faithful reference**. Each derived figure adds its own contrasting overlays (colored zones, arrows, labels) that pop against the muted base.

---

## Suggested derived figures (what the base will support)

| Figure | What overlays add to the base |
|---|---|
| `adivadya_om_sweep.svg` | Three-phase arrow (a → u → m) showing the sweep through the tract; phase labels in Devanāgarī + IAST; active organs highlighted at each phase |
| `adivadya_five_sthana.svg` | The five Pāṇinian places (*kaṇṭhya* / *tālavya* / *mūrdhanya* / *dantya* / *oṣṭhya*) labeled at their anatomical positions, anchored to the zone-of-articulation hidden layers |
| `adivadya_vowel_space.svg` | Tongue body redrawn in three positions (low-central for *a*, high-back for *u*, high-front for *i*); lips at three rounding states |
| `adivadya_visarga_anusvara.svg` | Two breath-gesture diagrams: visarga (glottis open, outward release) and anusvāra (velum dropped, inward nasal resonance) |
| `adivadya_prana_flow.svg` | Prāṇa pathway — lungs → vocal cords → cavity → exit; airflow arrows through the tract |
| `adivadya_manner_classes.svg` | Sparśa / ūṣman / antaḥstha / svara as contact types at different positions; visual differentiation of each manner |
| `adivadya_vocal_cord_states.svg` | Larynx detail figure (a separate sub-figure, modeled on Image 3's circular inset) showing vocal cords closed / open / vibrating |

The vocal-cord-state figure is the one case where a separate inset-style illustration is needed rather than an overlay on the main base.

---

## Export bundle (next steps)

When the base illustration is complete:

1. Export from Illustrator as SVG with these settings:
   - Styling: Internal CSS
   - Font: Convert to Outlines (if any text is in the base — likely none)
   - Images: Embed
   - **Object IDs: Layer Names** (critical — keeps the named-layer structure)
   - Decimal Places: 2
   - Minify: unchecked
   - Responsive: unchecked

2. Save to:
   - `figures/build/adivadya_mouth_cross_section.svg` (canonical base — referenced by all derived figures)

3. Optionally also save:
   - A labeled reference version (with anatomy labels visible) at `figures/design_sources/claude_design/adivadya_mouth_cross_section_LABELED.svg` — for the artist's working reference only, not used in the book
   - A high-resolution PNG (~2400 px wide) for visual verification at `figures/design_sources/claude_design/adivadya_mouth_cross_section.png`

4. Keep the `.ai` source outside the repo (or in a non-tracked location).

5. Upload the SVG base, the labeled reference, and this brief to claude design at the project level. Each Ch 7 figure chat will then:
   - Inherit `CLAUDE.md` and `book-assets.css` from the project root
   - Load the base SVG and this brief
   - Generate overlay-only SVG for one specific derived figure
   - Output to `figures/build/`

---

## Cross-chapter reuse

This base may also serve:

- **Ch 8 (*Mapping the Mouth: The Sonomeric Grid*)** — the *varṇamālā* introduction; the five-place grid is the central object. The same cross-section base supports figures showing where each *sparśa-varga* row sits anatomically.
- **Appendix Part 3 (*The Sonomer and the Audiograph*)** — appendix-grade figures developing the sonomer-first-audiograph-second argument. May reuse the base for any anatomy-anchored argument.

Naming convention for cross-chapter use: when the base appears in a Ch 8 or App Part 3 figure, the OUTPUT filename uses that chapter's slug (`mapping_mouth_*.svg`, `audiography_*.svg`), but the underlying base reference stays `adivadya_mouth_cross_section.svg` — one canonical asset, many derived figures.
