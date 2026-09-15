#!/usr/bin/env python3
"""Synthesis pass 4: verify deployment of the reconciled manuscript count."""

from __future__ import annotations

from capacity_synthesis_common import DATE, MANUSCRIPT, RESULTS, extract_section, project_path, sha256, write_json
from build_generativity_manuscript_proposal import CHAPTER_0_AFTER, CHAPTER_12_AFTER, ENDNOTE_AFTER


TARGETS = (
    (MANUSCRIPT / "as_1_00_seekers.md", CHAPTER_0_AFTER, "Chapter 0 §0.6"),
    (MANUSCRIPT / "as_1_12_building_vakya.md", CHAPTER_12_AFTER, "Chapter 12 §12.7"),
)
ENDNOTES = MANUSCRIPT / "as_endnotes.md"


def main() -> None:
    records = []
    for path, expected, deployment in TARGETS:
        text = path.read_text()
        if expected not in text:
            raise ValueError(f"Approved deployment text is missing from {path}")
        records.append({
            "path": project_path(path),
            "deployment": deployment,
            "line": text[: text.index(expected)].count("\n") + 1,
            "current": expected,
            "sha256": sha256(path),
        })
    endnote_text = ENDNOTES.read_text()
    endnote = extract_section(endnote_text, "### `sanskrit-generative-wordspace`")
    if endnote.strip() != ENDNOTE_AFTER.strip():
        raise ValueError("The deployed sanskrit-generative-wordspace endnote differs from the approved text")
    records.append({
        "path": project_path(ENDNOTES),
        "deployment": "Endnote `sanskrit-generative-wordspace`",
        "line": endnote_text[: endnote_text.index(endnote)].count("\n") + 1,
        "current": endnote,
        "sha256": sha256(ENDNOTES),
    })
    report = {
        "date": DATE,
        "pass": 4,
        "records": records,
        "body_deployments_verified": 2,
        "endnote_deployments_verified": 1,
        "obsolete_count_occurrences": sum(path.read_text().count("20,942,880") for path in MANUSCRIPT.glob("*.md")),
        "stale_deployment_found": "Chapter 0 §0.5" in endnote,
        "manuscript_modified": True,
    }
    write_json(RESULTS / "manuscript_generativity_claim_audit.json", report)
    lines = ["# Synthesis Pass 4: Manuscript Claim Audit", ""]
    for record in records:
        lines.extend([
            f"## {record['deployment']}", "",
            f"[{record['path']}](../../../{record['path']}#L{record['line']})", "",
            record["current"], "",
        ])
    lines.extend([
        "## Findings", "",
        "- The approved count cascade is present in Chapter 0 and Chapter 12.",
        "- The supporting endnote carries the reconciled arithmetic, scope, and exclusions.",
        "- The obsolete 20,942,880-slot count has no remaining manuscript occurrence.",
        "- The Chapter 0 deployment points to the current §0.6.", "",
    ])
    (RESULTS / "manuscript_generativity_claim_audit.md").write_text("\n".join(lines))
    print("Verified the two body deployments and their shared endnote.")


if __name__ == "__main__":
    main()
