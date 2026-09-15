"""Retrieve candidate evidence for the fixed remaining follow-up queue."""

import json
from pathlib import Path

from vidyut import lipi
from prepare_identity_packets import key
from read_dhatu_concordance import read_rows, source_text
from run_pilot import ARCHIVE, HERE, RESULTS


def remaining():
    first = json.loads((HERE / "reconciliation_review_01.json").read_text())["cases"]
    second = json.loads((HERE / "reconciliation_review_02.json").read_text())["cases"]
    visited = {c["id"] for c in first} | {c["prior_id"] for c in second}
    history = json.loads((RESULTS / "identity_followups.json").read_text())["groups"]
    return [g for g in history if g["id"] not in visited]


def main():
    concordance = read_rows()
    packets, urls = [], {}
    for i, g in enumerate(remaining()):
        head = lipi.transliterate(g["headword"], lipi.Scheme.Slp1, lipi.Scheme.Devanagari)
        candidates = [r for r in concordance if key(r["citation"].split(" ( ")[-1].split(" )")[0]) == key(head)]
        names = {e["source"] for e in g["evidence"]}
        for r in candidates:
            for link in r["commentaries"]:
                name = "dhatu-" + Path(link).name
                names.add(name)
                urls[name] = "https://sanskrit.uohyd.ac.in/scl/dhaatupaatha/" + link
        packets.append(dict(g, followup_batch=i // 10 + 1, candidates=candidates, sources=sorted(names)))
    (HERE / "remaining_followup_sources.json").write_text(json.dumps(urls, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "remaining_followup_packets.json").write_text(json.dumps(packets, ensure_ascii=False, indent=2) + "\n")
    for batch in range(1, 8):
        lines = [f"# Candidate Sources: Follow-up Batch {batch}", "", "Retrieval only, not identity decisions.", ""]
        for p in packets:
            if p["followup_batch"] != batch:
                continue
            lines.extend([f"## {p['id']}: {p['headword']}", "", json.dumps(p["entries"], ensure_ascii=False), "", p["remaining"], ""])
            lines.extend(json.dumps(r, ensure_ascii=False) for r in p["candidates"])
            for name in p["sources"]:
                lines.extend(["", f"### {name}", "", source_text(name) if (ARCHIVE / name).exists() else "NOT ARCHIVED", ""])
        (RESULTS / f"remaining_followup_packet_{batch:02d}.md").write_text("\n".join(lines))
    missing = [n for n in urls if not (ARCHIVE / n).exists()]
    print(f"{len(packets)} records; {len(urls)} candidate pages; {len(missing)} not yet archived.")


if __name__ == "__main__":
    main()
