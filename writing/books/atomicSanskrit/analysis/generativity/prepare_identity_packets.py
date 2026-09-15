"""Build research packets; candidate concordance matches never decide identity."""

import json
from pathlib import Path

from vidyut import lipi
from read_dhatu_concordance import read_rows, source_text
from run_pilot import ARCHIVE, HERE, RESULTS


def key(text):
    text = lipi.transliterate(text, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)
    # Loose retrieval only: normalize spelling variants without assigning identity.
    return text.replace("z", "s").replace("R", "n").replace("b", "v").replace("m", "n")


def packets():
    rows = read_rows()
    result = []
    for item in json.loads((HERE / "identity_packets.json").read_text()):
        matches = [row for row in rows if key(row["citation"].split(" ( ")[-1].split(" )")[0]) == key(item["headword"])]
        selected = []
        for row in matches:
            preferred = [name for name in row["commentaries"] if "/mA" in name]
            selected.extend(preferred or row["commentaries"][:1])
        result.append({**item, "concordance_candidates": matches,
                       "commentaries": sorted({Path(name).stem for name in selected})})
    return result


def main():
    result = packets()
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "identity_packets.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for batch in sorted({item["batch"] for item in result}):
        lines = [f"# Research Packet: Batch {batch}", "", "Retrieval candidates only; no identity decision is inferred.", ""]
        for item in result:
            if item["batch"] != batch:
                continue
            lines += [f"## {item['id']}: {item['headword']}", "", json.dumps(item["entries"], ensure_ascii=False), ""]
            lines += [json.dumps(row, ensure_ascii=False) for row in item["concordance_candidates"]]
            for code in item["commentaries"]:
                filename = f"dhatu-{code}.html"
                lines += ["", f"### {code}", "", source_text(filename) if (ARCHIVE / filename).exists() else "NOT ARCHIVED", ""]
        (RESULTS / f"identity_packet_{batch:02d}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(sorted({code for item in result for code in item["commentaries"]})))


if __name__ == "__main__":
    main()
