# Source and Reference Companion Reduction Audit

**Started:** 2026-09-06
**Scope:** The four companion-only chapters assembled before the expanded endnotes.
**Rule:** Preserve full data, calculations, tables, sources, limitations, and replication instructions. Remove internal editorial records and repeated interpretation that does not help a reader use the evidence.

**Status:** Companion reduction completed 2026-09-06. Raw companion word count fell from 12,626 to 11,477, a reduction of 1,149 words. The four chapters retain every numerical table, coordinate table, cited rule, source list, and replication instruction.

## File Map

| File | Purpose | Relationship to printed appendices | Decision |
|---|---|---|---|
| `companion/as_reference_front.md` | Explains the relation between the printed notes and their expanded records, including stable stub-names and supporting entries. | Unique navigational material. | Retain. |
| `companion/as_reference_00_where_this_argument_stands.md` | Locates the book beside Out-of-India arguments, criticism of PIE reconstruction, and formal or computational Sanskrit research. | No printed appendix performs this literature-positioning function. | Retain. Only remove repetition discovered during final continuity review. |
| `companion/as_reference_06_by_the_numbers_full.md` | Preserves the complete numerical audit behind Chapters 10–11 and printed Appendix Part 6. | Deliberately overlaps the printed appendix, which presents only the strongest results. The companion owns the full prediction-data-verdict cycles, tables, correction history needed to understand the calculations, scripts, and replication instructions. | Remove the internal `Draft notes` block. Shorten the opening roadmap and repeated synthesis language. Preserve all empirical sections and reproducibility material. |
| `companion/as_reference_08_let_coordinate_test.md` | Tests all eighteen *leṭ* person-number-*pada* coordinates against *laukika loṭ* and records the relevant Pāṇinian operations. | Printed Appendix Part 8 §8.5 gives only the result and explicitly points here for the complete test. | Preserve both coordinate tables, the semantic comparison, Vedic examples, rules, findings, and sources. Tighten only duplicated framing and conclusion language. |

## Companion Appendix 6

### Keep

- Source corpus and *anubandha* removal method.
- Four-role position taxonomy.
- Every prediction, dataset, table, numerical result, falsification, and methodological correction.
- Path A and Path C distinctions.
- Replication bundles, source files, scripts, execution order, and future Path B description.
- The eight-principle synthesis as a compact index to the full audit.

### Remove or shorten

- The dated `Draft notes (Appendix Part 6 v3)` production record. It tracks old word counts, previous baselines, sync work, typography checks, voice notes, and a planned endnote. It is useful editorial history but not part of the published technical record.
- The opening section-by-section roadmap, reduced to one paragraph because the headings already expose the structure.
- Repeated claims following the eight-principle list and the two consecutive closing hammers after the replication instructions.

## Companion Appendix 8

### Keep

- Ṛgveda 6.16.16 and 10.186.1.
- Pāṇini 3.4.6–8 and 3.4.94–98.
- Both nine-coordinate tables.
- The comparison with *loṭ*, *vidhiliṅ*, *āśīrliṅ*, and *lṛṭ*.
- The four results and the boundary between demonstrated collisions and architectural inference.

### Shorten

- Opening material that announces the result before the test begins.
- The final explanation where it repeats the four numbered findings in prose.

## Reduction Record

The complete internal draft block and all reader-facing prose removed during this pass are preserved in `as_companion_reduction_lost_and_found_codex.md`.

## Integrated Build Verification

The reduced companion was rebuilt on 2026-09-06 with:

`python3 build_book.py reference --layout a4 --progress-pages 20`

The build completed at 236 A4 pages. Visual checks covered the title page, contents, both reference-appendix openings, representative data tables, the multi-page Schleicher table, representative endnotes, and the final numbered note. All pages use the A4 media box, and no text block extends beyond it. Long inline identifiers and source paths now wrap at separators through the shared LaTeX code-span filter. The intentionally blank pages are recto separators and the final even-page pad.
