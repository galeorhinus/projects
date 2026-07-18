# Register Reduction Audit

Purpose: reduce casual use of `register` / `registers` / `registered` / `registering` across the manuscript and guidance files. Keep the word only where it is genuinely the best technical word. Prefer `voice`, `mode`, `style`, `domain`, `idiom`, `language`, `layer`, `listed`, `recorded`, `surfaces`, or `appears` where the local meaning is clearer.

Counting pattern:

```sh
\bregister(s|ed|ing)?\b
```

## Baseline

Date: 2026-06-09

| Scope | Count | Notes |
|---|---:|---|
| Assembled book files | 216 | All files listed in `as_book.yaml`, including appendices and endnotes. |
| Reading-flow files | 70 | Front matter, part openers, Chapters 0-19, Epilogue, Acknowledgments. |
| Appendices + endnotes | 146 | Appendix files and `as_endnotes.md`. |
| Guidance files | 61 | `CLAUDE.md` + `STYLE.md`; tracked separately because these rules shape future edits. |

## Pass Log

| Pass | Scope | Before | After | Delta | Notes |
|---|---|---:|---:|---:|---|
| 0 | Baseline count | 216 | 216 | 0 | No manuscript changes. |
| 1 | Guidance files | 61 | 2 | -59 | Updated `CLAUDE.md` and `STYLE.md`; `register` now survives only in the explicit exception rule. Assembled book count unchanged at 216. |
| 2 | Reading-flow files | 70 | 0 | -70 | Replaced loose uses across Chapters 0-19 and the Epilogue with `voice`, `idiom`, `language`, `mode`, `standard`, `discipline`, `style`, `vocabulary`, or `posture`. Also renamed one endnote key touched by Ch16. Assembled book count now 142. |
| 3 | Appendices + endnotes | 142 | 0 | -142 | Replaced appendix and endnote uses with `mode`, `form`, `layer`, `domain`, `usage`, `speech-field`, `idiom`, `discipline`, `listed`, or `marks` depending on context. Assembled book count now 0. |

## Final Counts

Date: 2026-06-09

| Scope | Count | Notes |
|---|---:|---|
| Assembled book files | 0 | All files listed in `as_book.yaml`. |
| Reading-flow files | 0 | Front matter, part openers, Chapters 0-19, Epilogue, Acknowledgments. |
| Appendices + endnotes | 0 | Appendix files and `as_endnotes.md`. |
| Guidance files | 2 | Both occurrences are in the explicit `CLAUDE.md` exception rule that tells future edits to avoid the word by default. |
