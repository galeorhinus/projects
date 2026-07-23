# Atomic Sanskrit Readability Review

This directory is the active decision workspace for the Codex readability audit.

The manuscript contains no Codex review comments. The completed audit under `working/10_active/manuscript_readability_audit_codex/` remains an unchanged historical record. All decisions are made here before any manuscript prose is changed.

## Application Status

The decisions selected in review files 01–22 were processed on 2026-07-23. Seventy-three revisions were applied, two original passages were explicitly retained, and one Part I proposal was superseded without being applied. The accepted second-pass refinements in file 30 were incorporated at the same time.

The complete decision-to-manuscript map is in [31_application_manifest.md](./31_application_manifest.md).

All substantive material removed by an audit revision must also appear in the central [Manuscript Readability Audit — Lost and Found](../../40_reference/source_material/manuscript_readability_audit_lost_and_found.md). The ledger is an application gate, not an optional cleanup record.

## Decision Workflow

Each review block contains the exact current manuscript text and a proposed replacement or structural treatment.

Each block must also classify its effect as `REPHRASE — NO SUBSTANTIVE CUT`, `CUT`, `CONDENSE`, or `MOVE`. A block classified as `CUT`, `CONDENSE`, or `MOVE` requires a Lost and Found ID before application.

Mark one decision:

- `ACCEPT PROPOSED` - apply the proposed text exactly.
- `KEEP ORIGINAL` - close the item without changing the manuscript.
- `USE AUTHOR REVISION` - apply the text written in the Author Revision field.
- `REVISE AGAIN` - Codex prepares another proposal from the comments.
- `DEFER` - leave the item open for a later pass.

When reviewed blocks are processed, Codex applies only accepted or author-revised text. The block status then becomes `APPLIED` or `CLOSED`, with the application date and resulting manuscript location recorded in the same review file.

## Status Summary

| Review file | Unit | Status |
|---|---|---|
| `01_about_series.md` | About the Series | READY |
| `02_preface.md` | Preface | READY |
| `03_overture.md` | Overture | READY |
| `04_ch00.md` | Chapter 0 | READY |
| `05_ch01.md` | Chapter 1 | READY |
| `06_part01.md` | Part I opener | READY |
| `07_ch02.md` | Chapter 2 | READY |
| `08_ch03.md` | Chapter 3 | READY |
| `09_ch04.md` | Chapter 4 | READY |
| `10_ch05.md` | Chapter 5 | READY |
| `11_ch06.md` | Chapter 6 | READY |
| `12_ch07.md` | Chapter 7 | READY |
| `13_ch08.md` | Chapter 8 | READY |
| `14_ch09.md` | Chapter 9 | READY |
| `15_ch10.md` | Chapter 10 | READY |
| `16_ch11.md` | Chapter 11 | READY |
| `17_ch12.md` | Chapter 12 | READY |
| `18_ch13.md` | Chapter 13 | READY |
| `19_ch14.md` | Chapter 14 | READY |
| `20_ch15.md` | Chapter 15 | READY |
| `21_ch16.md` | Chapter 16 | READY |
| `22_ch17.md` | Chapter 17 | READY |
| `23_ch18.md` | Chapter 18 | READY |
| `24_ch19.md` | Chapter 19 | READY |
| `25_epilogue.md` | Epilogue | READY |
| `26_parts_front_back.md` | Remaining Part openers, Acknowledgments, Note on Notes | READY |
| `27_appendices.md` | Appendices 1-9 | READY |
| `28_endnotes_figures_global.md` | Endnotes, captions, and global decisions | READY |
| `29_work_hold_lexical_sweep.md` | Contextual sweep for `question`, `answer`, `work`, and `hold` | PLANNED |

## Block Format

````markdown
## EXAMPLE-001 - Short description

**Source:** clickable manuscript location  
**Action:** REPLACE / INSERT / DELETE / MOVE / STRUCTURE  
**Cut impact:** REPHRASE — NO SUBSTANTIVE CUT / CUT / CONDENSE / MOVE  
**Lost and Found:** NONE / LAF-R-###  
**Status:** OPEN  
### Original

> Exact current manuscript text.

### Proposed

Proposed replacement text or structural treatment.

### Decision

- [ ] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [ ] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text
Write replacement prose here when selecting USE AUTHOR REVISION.
````

### Comments

Write comments or revision instructions here.
```

## Processing Rules

1. The exact original is refreshed if the manuscript changes before a decision is applied.
2. A block with more than one affected paragraph contains the complete original and complete proposed replacement.
3. Structural blocks show the existing heading sequence and the proposed sequence. They are never applied automatically.
4. Codex does not infer acceptance from casual edits. Select a decision explicitly.
5. Every substantive sentence, clause, claim, example, qualification, citation, heading, figure, caption, or argumentative beat that disappears is copied into Lost and Found before the manuscript changes. The rule is not limited to material Codex considers important.
6. An accepted block marked `CUT`, `CONDENSE`, or `MOVE` cannot be applied without a Lost and Found ID. A move must also record its destination.
7. Pure rephrasing must be marked `REPHRASE — NO SUBSTANTIVE CUT`; when the classification is uncertain, log the material.
8. The historical audit documents are not modified as decisions are made.
