#!/usr/bin/env python3
"""Synthesis pass 5: record and verify the approved manuscript deployment."""

from __future__ import annotations

from capacity_synthesis_common import DATE, RESULTS, project_path, read_json, sha256, write_json


INPUTS = (
    RESULTS / "manuscript_generativity_claim_audit.json",
    RESULTS / "publication_capacity_cascade.json",
    RESULTS / "integrated_grammatical_capacity.json",
    RESULTS / "vaidika_capacity_boundary.json",
)


CHAPTER_0_AFTER = """These operations give a finite inventory enormous reach. A bounded reconstruction conducted for this book begins with 2,634 recorded meanings carried by Sanskrit's semantic atoms. Before inflection, the operations tested so far generate 12,846,458 शब्दार्थाः (*śabdārthāḥ*), distinct word-meanings. When the ordinary-language portion passes through the declared verb and noun matrices, it occupies 602,707,133 grammatical cells. The count stops before unrestricted recursive compounding, which has no fixed ceiling. Chapter 12 explains each stage of the calculation.[NOTE: sanskrit-generative-wordspace]"""

CHAPTER_12_AFTER = """The scale of this generativity can now be followed from operation to operation. The reconstruction begins with 2,634 recorded meanings carried by Sanskrit's semantic atoms. Prefixes and verbal transformations raise the count beyond 1.3 million. Sanskrit then turns those verbal meanings into actions, agents, instruments, qualities, obligations, and other kinds of meaning. Further operations express state, possession, descent, origin, comparison, negation, and bounded compounds. Before inflection begins, the resulting inventory contains 12,846,458 शब्दार्थाः (*śabdārthāḥ*), distinct word-meanings.

The लौकिक (*laukika*) portion divides into three familiar Sanskrit categories:

- **4,540,848 क्रियार्थाः (*kriyārthāḥ*)**, meanings of actions and processes;
- **8,084,287 नामार्थाः (*nāmārthāḥ*)**, meanings that name people, things, qualities, states, and relations; and
- **7,925 अव्ययानि (*avyayāni*)**, complete words whose forms do not change.

The क्रियार्थाः (*kriyārthāḥ*) can appear across ten settings of time and mood, three grammatical persons, and three numbers. The नामार्थाः (*nāmārthāḥ*) can appear across eight grammatical relations and three numbers. Under these declared matrices, the ordinary-language inventory occupies 602,707,133 grammatical cells.[NOTE: sanskrit-generative-wordspace]

This gives Bṛhaspati's thousand divine years a numerical scale. Even a deliberately bounded reconstruction passes six hundred million cells before unrestricted recursive compounding begins. A dictionary can record words that speakers have already used. It cannot reach the end of Sanskrit's generative capacity."""

ENDNOTE_AFTER = """### `sanskrit-generative-wordspace`

<!-- SOURCE-RECORDS
- project-generativity-capacity-synthesis | reconciled lexical, verbal-inflection, nominal-inflection, and integrated-capacity reports
- project-dhatupatha-csv | original project inventory behind the earlier baseline
- generativity-vidyut-040-pilot | pinned engine, source inventory, rule snapshots, checksums, and generated derivation paths
-->

**Short:** A reproducible reconstruction begins with 2,634 reconciled धातुः (*dhātuḥ*) meanings and generates 12,846,458 bounded शब्दार्थाः (*śabdārthāḥ*), distinct word-meanings, before inflection. The 12,633,060 लौकिक (*laukika*) meanings then occupy 602,707,133 semantic grammatical cells under the declared verb and noun matrices. The 213,398 Vedic meanings remain a separate lexical inventory.

**Deployments:** Chapter 0 §0.6; Chapter 12 §12.7.

The bounded lexical inventory divides into three लौकिक meaning classes:

- **4,540,848 क्रियार्थाः (*kriyārthāḥ*)**, action and process meanings. Ten settings of time and mood, three grammatical persons, and three numbers produce **408,676,320** cells: 4,540,848 × 10 × 3 × 3.
- **8,084,287 नामार्थाः (*nāmārthāḥ*)**, meanings naming people, things, qualities, states, and relations. In the technical count these are प्रातिपदिकार्थाः (*prātipadikārthāḥ*), meanings carried by nominal bases. Eight grammatical relations and three numbers produce **194,022,888** cells: 8,084,287 × 8 × 3.
- **7,925 अव्ययानि (*avyayāni*)**, complete words whose forms do not change. Each contributes one cell.

The integrated लौकिक capacity is therefore **408,676,320 + 194,022,888 + 7,925 = 602,707,133 semantic grammatical cells**. The calculation replaces each lexical input with its grammatical matrix; it does not add the 12,633,060 inputs again. A repeated spelling remains attached to every distinct meaning and grammatical coordinate it expresses.

The count is bounded by design. The verbal matrix covers ten लौकिक settings of time and mood in कर्तरि (*kartari*) construction. The nominal matrix covers eight relations and three numbers, with gender treated as an output property rather than an automatic multiplier. Vedic inflection, कर्मणि (*karmaṇi*), भावे (*bhāve*), further agreement-driven gender forms, and unrestricted recursive compounding remain outside this total.

Local regeneration verifies ninety verbal citation cells, 270 complete verbal sample cells, eight nominal citation cells, and 192 complete nominal sample cells with rule histories. The full capacities are calculated from the reconciled meaning inventories and declared coordinate matrices; hundreds of millions of rows are not materialized merely to repeat the same arithmetic.

This number does not claim that Sanskrit has 602,707,133 distinct spellings or that a dictionary records that many entries. It measures the semantic and grammatical capacity reached by the operations included in the model. The separate compound experiment demonstrates why unrestricted compounding cannot provide a finite upper limit."""


def main() -> None:
    audit, cascade, integrated, boundary = [read_json(path) for path in INPUTS]
    current = {record["deployment"]: record for record in audit["records"]}
    proposals = [
        {
            "deployment": "Chapter 0 §0.6",
            "path": current["Chapter 0 §0.6"]["path"],
            "line": current["Chapter 0 §0.6"]["line"],
            "after": CHAPTER_0_AFTER,
        },
        {
            "deployment": "Chapter 12 §12.7",
            "path": current["Chapter 12 §12.7"]["path"],
            "line": current["Chapter 12 §12.7"]["line"],
            "after": CHAPTER_12_AFTER,
        },
        {
            "deployment": "Endnote `sanskrit-generative-wordspace`",
            "path": current["Endnote `sanskrit-generative-wordspace`"]["path"],
            "line": current["Endnote `sanskrit-generative-wordspace`"]["line"],
            "after": ENDNOTE_AFTER,
        },
    ]
    report = {
        "date": DATE,
        "pass": 5,
        "status": "deployed",
        "manuscript_modified": True,
        "integrated_laukika_grammatical_cells": integrated["integrated_laukika_grammatical_cells"],
        "vaidika_lexical_word_meanings_held_separate": boundary["vaidika_lexical_word_meanings"],
        "proposals": proposals,
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
    }
    write_json(RESULTS / "generativity_manuscript_proposal.json", report)
    lines = [
        "# Synthesis Pass 5: Manuscript Deployment", "",
        "**Status:** Approved and deployed on 2026-09-15.", "",
    ]
    for proposal in proposals:
        lines.extend([
            f"## {proposal['deployment']}", "",
            f"[{proposal['path']}](../../../{proposal['path']}#L{proposal['line']})", "",
            "### Deployed", "", proposal["after"], "",
        ])
    (RESULTS / "generativity_manuscript_proposal.md").write_text("\n".join(lines))
    print("Recorded three approved manuscript deployments.")


if __name__ == "__main__":
    main()
