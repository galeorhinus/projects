# Icon Design Brief — *Atomic Sanskrit*

A request for a coherent icon set for the book's core engineering concepts
(*sonomer*, *dhātuḥ*, *kriyā*, and the rest of the scale-chain). This brief gives
the context, the existing visual system to harmonize with, the concept list, the
format requirements, and a set of starting ideas. **The starting ideas are
springboards, not specifications — propose better ones.**

---

## 1. What the book is (one paragraph)

*Atomic Sanskrit* argues that Sanskrit is **engineered**, not grown — a precisely
calibrated architecture of sound and meaning, the way a chemistry is an
architecture of matter. The book's signature analytical idiom is **chemical /
engineering**: sound-*particles* combine into *atoms*, atoms fill *scaffolds* and
bond into *molecules*, molecules assemble into sentences. The visual language must
feel **manufactured and exact** — blueprint, schematic, precision instrument —
never organic, hand-drawn, or decorative. (The book reserves the organic/decaying
aesthetic for the *opposing* thesis it dismantles; Sanskrit's side is the
engineered side.)

---

## 2. The existing visual system (harmonize with this)

The book already has a hexagon-based visual grammar and a live icon family. New
icons must read as members of the same family.

**The hexagon is the book's visual atom.** A single *flat-top* hexagon (points
left and right) is one unit of measured sound. Units stagger on two rails (an
upper rail and a lower rail) and interlock left-to-right into strips — this is how
the book draws *dhātavaḥ*, words, and verb-assembly.

**The existing scaffold icons** (`figures/_shared/icons/scaffold_*.svg`) render
the *dhāturacanā* (scaffold) shapes — e.g. `CV1C`, `CCV1C` — as clusters of
flat-top hexagons:

- **fill-only** (no stroke), one flat color per icon;
- ship in two inks: **gray `#888888`** (default — body text and chart labels) and
  **black `#1a1a1a`** (isolated against white at small size);
- tight `viewBox`, `preserveAspectRatio="xMidYMid meet"`, with `role="img"`,
  `<title>`, and `aria-label`;
- used inline at `height:1em; vertical-align:-0.2em`, and larger in figures.

**Warm palette** (the book's print/figure colours, from
`figures/_shared/matra_style.py`) — provide a warm variant of each icon in
addition to gray/black:

| Token | Hex | Use |
|---|---|---|
| background | `#ffffff` | page |
| tan (light) | `#d8c7a3` | the light element (vowel / atom centre) |
| dark brown | `#4a3a28` | the heavy element (consonant / sonomer) |
| outline | `#5c4830` | strokes where used |
| gold | `#a8842c` | the result / transformed / highlighted element |
| mid brown | `#6b563a` | secondary |

**Eclipse note:** the book also has a *narrative* icon system (Sūrya / Svarbhānu /
Rāhu — the eclipse spine). These technical icons are a **separate** system; do not
borrow sun/eclipse motifs here.

---

## 3. The icons needed

Grouped by the layer of the architecture. Each is named with its English gloss,
its Sanskrit term (Devanagari + IAST), and what it means in the book. Devanagari
letterforms may *inspire* a mark, but each icon must read for someone who cannot
read the script.

### Sound layer
- **Sonomer** — **वर्ण (*varṇa*)** — the atomic *particle* of measured sound. The
  book coins "sonomer" (sound + *-mer*, as in *monomer*). The smallest unit. **Not
  a "letter"** — the book actively displaces the letter/alphabet framing.
- **Akṣara** — **अक्षर (*akṣara*)** — the **imperishable** sound-unit (syllable).
  *a-kṣara* = non-perishing. The distinctive idea is *permanence / indestructible
  form* — a unit engineered not to decay.
- **Varṇamālā** — **वर्णमाला (*varṇamālā*)** — the full inventory / "garland" of
  sonomers, organized as a 5×5 *varga* grid. The periodic table of Sanskrit sound.

### Structure layer
- **Dhātuḥ** — **धातुः (*dhātuḥ*)** — the **semantic atom**: the constituent that
  *holds* identity (the same word names the surviving metal in metallurgy and the
  structural tissue in Āyurveda). Has *valency* — it bonds. **Not a "root"** (the
  book displaces the botanical framing).
- **Dhāturacanā / Racanā** — **रचना (*racanā*)** — the **scaffold**: the abstract
  slot-template a *dhātuḥ* fills. **ICONS ALREADY EXIST** (the `scaffold_*` set) —
  listed here only so the new icons stay compatible. A *dhātuḥ* should look like it
  could *fill* a *racanā*.
- **Śabda** — **शब्द (*śabda*)** — the **lexical molecule**: a word, built by
  bonding atoms with affixes.
- **Kriyā / Kriyāpada** — **क्रिया / क्रियापद (*kriyā*)** — the **verb / action**:
  the molecule assembled from a *dhātuḥ* + activation sonomers + ending. Carries
  *motion* — it is the action-word.

### Measure & system layer
- **Mātrā** — **मात्रा (*mātrā*)** — the unit of **timing / measure** (light =
  *laghu* = 1 beat; heavy = *guru* = 2 beats). The book scans it with pipe marks
  (`|` and `||`) and draws it as a ruler under the hex strips.
- **Sūtra** — **सूत्र (*sūtra*)** — the **thread**: a maximally compressed rule
  (*alpākṣaram*, "few-syllabled"); dense, exact, load-bearing. Literally "thread."
- **Calibration matrix** — the multi-axis grid that holds the whole system in fixed
  measure across generations (*dhruva-māna*, "fixed measure"). The architecture
  itself.
- *(optional)* **Vākya** — **वाक्य (*vākya*)** — the **sentence**: molecules linked
  into a chain.
- *(optional)* **Mukha** — the **mouth / vocal apparatus**: where sound is
  articulated; the origin of the chain. The book maps five places of articulation.

---

## 4. Format & technical requirements

- **SVG**, hand-optimizable, minimal nodes. One concept per file.
- **Three colour variants** per icon: gray `#888888`, black `#1a1a1a`, and a warm
  variant (use tan/dark-brown/gold per §2). Match the `scaffold_<slug>_<ink>.svg`
  naming pattern.
- **Reads at 1em (~16 px) inline AND scales up** in headers/figures. So: bold
  silhouette, generous negative space, ≤2 distinct elements per icon, no hairline
  detail that vanishes at 16 px.
- **Square-ish or tight bounding box**, centred, `preserveAspectRatio` meet;
  include `<title>` + `aria-label`.
- **One flat colour per icon** by default (so it can be tinted via `currentColor`
  or recoloured), matching the fill-only scaffold icons. A two-tone warm variant
  is welcome where it clarifies (e.g. a gold "result" element).
- **Consistent line weight, corner treatment, and level of abstraction** across the
  whole set — they must look designed *together*.

---

## 5. Avoid

- Speech bubbles, ABC blocks, quill pens, books, scrolls, "language" clichés.
- Generic Western-academic or religious iconography.
- Over-ornate "ethnic" decoration (no kitsch mandalas, no paisley). The aesthetic
  is **precision-engineered**, not folkloric.
- Anything that reads as organic, growing, hand-drawn, or decaying — that is the
  visual register of the thesis the book *opposes*.
- Sun / eclipse / Rāhu motifs (reserved for the separate narrative system).
- Detail that only survives at large size.

---

## 6. Proposed organizing principle (a starting idea)

**Make the set an assembly progression, with the hexagon as the shared atom.**
The book's whole argument is scale-recurring assembly: *particle → atom → scaffold
→ molecule → sentence*. The icon set can *be* that progression, so the family
reads as one story and each icon differs from its neighbour by exactly one move:

| Concept | Starting idea (riff freely) |
|---|---|
| **Sonomer (varṇa)** | a single flat-top hexagon with one minimal internal mark — a dot, or a short sound-ripple — the irreducible sound-particle. |
| **Akṣara** | the sonomer-hex *sealed* — enclosed in a thin ring, or drawn with one unbroken continuous contour — to read as *imperishable*. |
| **Varṇamālā** | a compact grid of small hexes (the 5×5 inventory), or a closed loop/garland of them. |
| **Dhātuḥ** | a single **solid** hexagon with a clear **nucleus** and small **bond-stubs** on its edges (valency) — visibly an *atom that combines*, and visibly able to *fill* a scaffold outline. |
| **Racanā** | *(exists)* the staggered hex-cluster silhouette. |
| **Śabda** | two–three hexes **bonded** into a balanced, static cluster — a molecule at rest. |
| **Kriyā / kriyāpada** | a bonded hex-cluster **plus a motion cue** — a forward arrow or a small activation spark — the molecule in *action*. (Differs from *śabda* only by the motion mark.) |
| **Mātrā** | a short ruler segment with one long + one short tick, echoing *guru/laghu* (`||` / `|`). The measure, not a hex. |
| **Sūtra** | a single taut thread with one knot, or a tightly-wound coil — *thread* + *compression*. |
| **Calibration matrix** | a small grid with two crossing axes / crosshair — measurement space. |

A second axis that could help differentiate at a glance: **sound-side** concepts
(*varṇa, akṣara, varṇamālā*) carry a wave/ripple cue; **structure-side** concepts
(*dhātuḥ, śabda, kriyā*) carry the chemistry/hex cue; **measure** (*mātrā, matrix*)
carries the ruler/grid cue. The unifying constant is the flat-top hexagon and a
single consistent line weight.

---

## 7. Deliverables

- One SVG per concept, in three inks (gray / black / warm), named to match the
  existing `scaffold_<slug>_<ink>.svg` convention.
- A single contact sheet showing the full set at 16 px and at large size, so the
  family coherence and small-size legibility can both be judged.
- Editable source (the construction geometry) so the set can be regenerated /
  extended, matching how `build_scaffold_icons.py` generates the scaffold set.
