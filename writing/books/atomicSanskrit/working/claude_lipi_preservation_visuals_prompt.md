# Claude Design Prompt: *Lipi*, *Smṛti*, *Śruti* Preservation Visuals

Use this prompt in Claude Design to generate visual concept pages for the preservation / calibration / aural transmission tables.

## Task

Create three HTML concept boards:

1. `preservation.html`
2. `calibration.html`
3. `aural.html`

These are not final production figures yet. They are design exploration boards. For each table assigned to a file, propose **three distinct visual design options**. There are 9 tables total, so the output should contain **27 design options**.

Each design option should be a polished static mockup rendered in HTML/CSS. The goal is to compare visual treatments, not to produce final manuscript-ready SVGs yet. But they should be readily convertible to SVG when needed.

## Palette Guidance

Choose from existing color palettes that print well in grayscale. Do not use a palette that depends on color alone for meaning.

Requirements:

- Every option must remain readable when printed in black-and-white.
- Use pattern, weight, line style, icon shape, label placement, and hierarchy in addition to color.
- Avoid low-contrast pastel-only palettes.
- Prefer palettes with strong value separation: dark ink, warm gold, stone gray, off-white, muted red/brown only for failure/capture.
- Include a short palette note for each HTML file explaining the palette and why it survives grayscale printing.

Suggested visual poles:

- **Sanskritic / calibration side**: distributed nodes, circular correction loops, living carriers, sound waves, open networks, warm light and other ideas that you may have.
- **Asuric / custody side**: vertical stacks, locked archives, stone blocks, gates, apex custody, single chokepoints, dark gray/black and other ideas you may have.

## Global Design Constraints

- Do not make ordinary data tables unless the design option explicitly argues for a table-like scorecard.
- Use visual grammar appropriate to the argument: quadrant maps, scorecards, loop diagrams, routing maps, bubble charts, capture stacks, hazard strips.
- Each design option should include:
  - design title;
  - one-sentence purpose;
  - visual mockup;
  - short note on why it works;
  - print/grayscale note.
- Use typography that feels book/editorial rather than app-dashboard.
- Avoid decorative gradient blobs or purely ornamental background shapes.
- Keep Sanskrit terms legible. Use IAST/English translation for most labels; Devanagari may appear sparingly as an accent or secondary label.
- Use icons only if they clarify: archive, manuscript, stone, mouth, ear, loop, flame, lock, gate, node, path.
- The visuals should fit the book's conceptual language: storage versus calibration, custody versus distributed correction, material durability versus living durability.

## Chapter Split

### `preservation.html` — Chapter 13: Why Preservation Needs Engineering

Place these tables here:

- Table 2 — Medium Suitability
- Table 4 — Material Durability vs Living Durability
- Table 5 — Failure-Mode Analysis
- Table 7 — Capital Cost and Capture Analysis

These belong in preservation because they explain why writing was useful but insufficient, why stone solves one problem while creating another, and why a medium must be evaluated by failure mode, capture risk, scalability, and cost.

### `calibration.html` — Chapter 14: The Calibration Matrix

Place these tables here:

- Table 1 — Form Fidelity and Durability
- Table 3 — Sanskritic vs Asuric Transmission Goals
- Table 8 — Suitability by Content Type
- Table 9 — Asuric Incentive Analysis

These belong in calibration because they compare preservation modes, distinguish content types, and expose the deeper contrast between Sanskritic distributed calibration and asuric custody.

### `aural.html` — Chapter 15: Aural Architecture

Place this table here:

- Table 6 — Correction-Loop Analysis

This belongs in the aural chapter because it makes the active correction machinery visible: reciter, teacher, listener, meter, accent, *pāṭha* redundancy, and immediate correction.

## High-Level Commentary To Preserve

Use these ideas as design constraints:

- *Lipi* should not be evaluated only as a storage technology. It must be evaluated against the goals of Sanskriti and the custody goals of the asuric pyramid.
- Sanskriti restricts the scope of *lipi* not because writing is primitive or useless, but because *lipi* is structurally easy to capture.
- The asuric pyramid loves *lipi* because *lipi* can be possessed.
- Sanskriti honors *lipi* but does not enthrone it, because the calibrant must remain harder to capture than a manuscript, archive, edict, inscription, or edition.
- Stone solves decay by creating dependence on capital. *Śruti* solves decay by creating dependence on disciplined people.
- Storage is passive. Calibration is active. A medium preserves only what its correction loop can defend.
- The pyramid asks where the text is stored. Sanskriti asks where the error is caught.
- The question is not whether writing is useful. The question is which content writing is fit to carry.

## Table Contents and Design Requests

### Table 1 — Form Fidelity and Durability

Assigned file: `calibration.html`

Table content:

| | Millennial Durability | Fragile Duration |
|---|---|---|
| Exact-form preservation | **Śruti / Auditure**: exact sound preserved through recitation, meter, accent, redundancy, trained correction, and lineage. Also **śilālekha** for durable written marks, though it preserves marks rather than sound. | **Lipi / ordinary writing**: exact visible marks can be stored, but the physical medium can decay, burn, be altered, or be centrally controlled. |
| Pattern preservation | **Smṛti / Mnemoniture**: story, category, dharma, and civilizational pattern survive through retelling, translation, adaptation, and memory, but not exact phonetic form. | **Hearsay / rumor / ephemeral speech**: neither exact form nor pattern is structurally protected. |

High-level commentary:

- This is the cleanest core figure.
- The rare quadrant is *śruti*: exact form plus millennial durability.
- *Smṛti* is not careless; it preserves pattern rather than exact phonetic form.
- *Śilālekha* should be shown as durable marks, not living sound.

Create three design options:

1. A clean 2x2 quadrant map with *Śruti* as the luminous top-right quadrant.
2. A landscape axis chart with icons and annotations for each quadrant.
3. A more editorial full-page spread that contrasts "living sound" with "material mark."

### Table 2 — Medium Suitability

Assigned file: `preservation.html`

Table content:

| Parameter | Lipi | Śilālekha | Smṛti | Śruti |
|---|---|---|---|---|
| Form Fidelity | High for visible marks; weak for sound | High for visible marks; weak for sound | Low for exact wording; high for pattern | Highest for sound-form |
| Durability | Medium to low; depends on medium | High | High | High |
| Scalability | Medium; depends on literacy and materials | Low; monumental and fixed | High | High but training-intensive |
| Fragility | Medium/high: decay, fire, copying errors | Low physical fragility; high contextual fragility | Low; retellings regenerate | Low if lineages remain active |
| Institutional Capture | High: archives, scribes, editions, access | High: rulers commission and locate it | Medium/low: distributed storytellers | Low/medium: lineages are distributed but require discipline |
| Correction Mechanism | Copy comparison, commentary, editorial control | Visual inspection, but no living correction | Community memory, narrative coherence | Recitation, meter, accent, trained audience |
| Medium Dependence | High | High | Low | Low |
| Portability | Medium | Low | High | High |
| Access Barrier | Literacy/material access | Physical access to site | Broad, through story/song | Trained participation |
| Sound Preservation | Weak unless paired with a prior sound-system | Weak | Weak | Highest |

High-level commentary:

- This table explains why writing was insufficient.
- It should be compact and immediately comparable.
- *Śilālekha* fixes decay but intensifies capital dependence and capture.

Create three design options:

1. Economist-style heatmap / scorecard with filled, half-filled, and hollow symbols.
2. Radar / profile comparison cards for each medium.
3. Compact matrix with icon-coded strengths and risks, optimized for print.

### Table 3 — Sanskritic vs Asuric Transmission Goals

Assigned file: `calibration.html`

Table content:

| Parameter | Sanskritic Preference | Asuric Preference | Why *Lipi* Attracts the Pyramid |
|---|---|---|---|
| Custody | Distributed across trained persons and lineages | Centralized in archive, canon, institution | Written objects can be owned, seized, hidden, edited, burned |
| Correction | Live correction by reciter, teacher, listener, meter | Editorial correction by authorized office | The apex decides the "correct text" |
| Access | Embodied training; many carriers | Credentialed access; few gatekeepers | Literacy, manuscripts, libraries, editions create gates |
| Authority | Authority lives in calibrated practice | Authority lives in document custody | Whoever controls the document controls doctrine |
| Scalability | Scales through people and practice | Scales through copies and administration | Copies are useful for empire, law, bureaucracy |
| Fragility | Avoids single-point failure | Creates controllable chokepoints | A captured archive captures memory |
| Transmission Object | Sound, pattern, practice, correction | Text, record, decree, inscription | The visible mark becomes the "evidence" |
| Durability Type | Living durability | Material durability | Stone survives, but it freezes context |
| Interpretation | Disciplined continuity within *paramparā* | Authorized interpretation from above | Text without living calibration invites priest, editor, judge |
| Civilizational Effect | Keeps power distributed | Concentrates power | *Lipi* is easy to turn into custody |

High-level commentary:

- This is the main civilizational contrast.
- It should not feel like a spreadsheet.
- The visual should show two opposed transmission architectures.

Create three design options:

1. Split-screen: distributed Sanskritic field on left, pyramid archive on right.
2. Two-column architecture diagram with matched rows and crossing tension lines.
3. Central "transmission goal" spine with Sanskritic branches and asuric branches.

### Table 4 — Material Durability vs Living Durability

Assigned file: `preservation.html`

Table content:

| Medium | Durability | Scalability | Capture Risk |
|---|---|---|---|
| Palm-leaf / paper *lipi* | Low to medium | Medium | High |
| Śilālekha | High | Low: major inscriptional projects require capital, labor, authority, site control, and political sponsorship | Very high |
| Smṛti | High for pattern | Very high | Low to medium |
| Śruti | High for exact sound | High through trained lineages | Low when distributed |

High-level commentary:

- Material durability is not the same as civilizational durability.
- Stone is durable, but it is not scalable.
- *Śruti* is expensive through discipline, not through capital.

Create three design options:

1. Capture-risk / scalability plane.
2. Four medium cards with durability, scalability, and capture-risk gauges.
3. "Material vs living durability" comparison ladder, with stone and *śruti* as opposed endpoints.

### Table 5 — Failure-Mode Analysis

Assigned file: `preservation.html`

Table content:

| Medium | Primary Failure Modes | What the Medium Is Good At | What It Cannot Guarantee |
|---|---|---|---|
| Palm-leaf / paper *lipi* | Decay, fire, seizure, copying error, edition capture, archive custody | Portable records, commentary, teaching, legal and administrative memory | Millennial survival without material continuity and custody protection |
| Śilālekha | Capital dependence, site capture, political authorship, frozen context, limited update path | Public announcement, royal order, durable memory of patronage or event | Scalable distributed transmission or living correction |
| Smṛti | Narrative drift, regional variation, motif expansion, selective emphasis | Civilizational story-pattern, category memory, dharmic imagination across languages | Exact phonetic or verbal form |
| Śruti | Lineage break, training collapse, loss of disciplined auditors, social abandonment of recitation | Exact sound-form across generations through living discipline | Survival without living practitioners |

High-level commentary:

- This table prevents *śruti* from sounding magical.
- Every medium fails differently.
- *Śruti* is engineered against failure modes that matter for exact phonetic preservation.

Create three design options:

1. Four horizontal failure-mode lanes with hazard icons.
2. "How it fails / what survives" strip with end-state markers.
3. Risk-map cards showing threat clusters and defenses for each medium.

### Table 6 — Correction-Loop Analysis

Assigned file: `aural.html`

Table content:

| Medium | Error Detected By | Correction Loop | Who Holds Authority |
|---|---|---|---|
| Palm-leaf / paper *lipi* | Scribe, editor, archive comparison, commentator | Copy comparison, collation, commentary, authorized edition | Whoever controls the copy-chain, archive, or edition |
| Śilālekha | Visual inspection, public reading, later epigraphic comparison | Minimal living correction after inscription; the text is fixed into the medium | Patron, ruler, temple, court, state, site custodian |
| Smṛti | Community memory, narrative coherence, performer-audience feedback | Retelling, correction by received pattern, adjustment across context | Distributed storytellers, households, teachers, communities |
| Śruti | Reciter, teacher, listener, meter, accent, *pāṭha* redundancy | Immediate oral correction, metrical check, accent check, recitation cross-check, lineage discipline | Calibrated practice itself, distributed through trained lineages |

High-level commentary:

- This is likely the strongest technical visual.
- The question is not only where information is stored. The question is where error is found and corrected.
- *Śruti* should look like a closed, live, multi-node correction loop.
- *Śilālekha* should look almost one-way.

Create three design options:

1. Four correction-loop mini-diagrams.
2. A single large comparative loop diagram, with *śruti* as the complete loop.
3. "Where is the error caught?" process diagram from storage to calibration.

Caption candidate:

> Storage asks where the text is kept. Calibration asks where the error is caught.

### Table 7 — Capital Cost and Capture Analysis

Assigned file: `preservation.html`

Table content:

| Medium | Material Cost | Training Cost | Capture Risk | Capture Mechanism |
|---|---|---|---|---|
| Palm-leaf / paper *lipi* | Low to medium | Literacy and scribal training | High | Archive control, manuscript custody, scribal gatekeeping, edition authority |
| Śilālekha | High | Specialist craft plus political commission | Very high | Patronage, site control, royal command, temple/court/state custody |
| Smṛti | Low | Cultural participation, story memory, performer skill | Low to medium | Prestige control, narrative framing, selective retelling |
| Śruti | Low material cost | Very high discipline cost | Low when distributed | Capture requires capture or collapse of lineages, teachers, auditors, and practice |

High-level commentary:

- Stone inscription is elite-sponsored durability.
- Stone solves decay by creating dependence on capital.
- *Śruti* has high discipline cost but low material cost.

Create three design options:

1. Cost vs capture bubble chart, with bubble size as training cost.
2. Four cost/capture cards with material-cost and training-cost bars.
3. Two-axis "capital vs discipline" map showing how costs distribute or centralize authority.

### Table 8 — Suitability by Content Type

Assigned file: `calibration.html`

Table content:

| Content Type | Best Medium | Why |
|---|---|---|
| Accounts, administration, law, teaching aids, letters, records | *Lipi* | These require visible reference, portability, copying, and practical retrieval |
| Public royal announcement, grant, boundary, victory, patronage memory | *Śilālekha*, *śāsanam*, *praśasti*, *tāmraśāsanam* | These require public durability, visible authority, and institutional recognition |
| Civilizational story-pattern, ethical narrative, dharmic imagination | *Smṛti* | The content must travel across languages, regions, households, performance forms, and generations |
| Exact phonetic calibrant, Vedic sound-form, accent, meter, recitation architecture | *Śruti* | The content is sound itself and must be preserved as sound, not merely as meaning or marks |

High-level commentary:

- This table prevents the anti-writing misunderstanding.
- Sanskriti did not reject *lipi*. It assigned *lipi* to domains where writing is excellent.
- The argument is about fit between content and carrier.

Create three design options:

1. Routing map from content types to preservation media.
2. Decision tree: "What needs to be preserved?" leading to the proper medium.
3. Subway-map style with four lines: records, public authority, story-pattern, exact sound.

### Table 9 — Asuric Incentive Analysis

Assigned file: `calibration.html`

Table content:

| The Pyramid Wants | Medium That Serves It | Why |
|---|---|---|
| Ownable object | *Lipi* | Manuscripts, books, archives, and editions can be possessed |
| Authorized edition | *Lipi* | A central institution can declare one copy or edition normative |
| Monumental legitimacy | *Śilālekha* | Stone gives authority a public, durable, capital-intensive body |
| Priest / editor / judge class | Written canon | Interpretation can be routed through credentialed gatekeepers |
| Centralized archive | *Lipi* | Storage can be gathered, catalogued, restricted, confiscated, or destroyed |
| Controllable interpretation | Written text severed from living calibration | The document becomes a field for institutional commentary and adjudication |
| Chronology capture | Inscriptional dating and manuscript dating | The interface can be dated and then falsely made to date the architecture |

High-level commentary:

- This is the most polemical visual.
- It should show why the pyramid loves *lipi*: not merely precision, but custody.
- The apex label can be **Custody**.

Create three design options:

1. Pyramid capture stack with layers corresponding to the table rows.
2. Lock-and-archive system diagram showing how *lipi* becomes custody.
3. "Asuric incentive board" with cards feeding into an apex labeled Custody.

## Deliverables

Create exactly these files:

1. `preservation.html`
2. `calibration.html`
3. `aural.html`

Each file should:

- contain only the tables assigned to that chapter;
- include 3 design options per table;
- include each table's high-level commentary before its design options;
- include the table content in a compact reference block, but the visual options should be the main focus;
- use responsive HTML/CSS that can be viewed in a browser;
- avoid external network dependencies;
- use embedded CSS;
- use simple inline SVG icons or CSS shapes where useful;
- be printable on letter paper and readable in grayscale.

## Do Not Do Yet

- Do not finalize SVG production files.
- Do not choose a winner for the author.
- Do not simplify the conceptual language.
- Do not remove Sanskrit terms.
- Do not make the visuals look like generic business dashboards.

At the end of each HTML file, add a short "Design Recommendation" section that ranks the 3 options for that chapter's use case, with a one-sentence reason for each ranking.
