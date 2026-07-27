#!/usr/bin/env python3
"""Count selected Vaidika forms in the GRETIL Rigveda Padapatha.

The script reports exact token counts. It does not infer case, gender, or
grammatical function. The prevalence ledger records which counts can safely be
treated as grammatical evidence and which remain raw spelling matches.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path


BASE_URL = (
    "https://druvx13.github.io/GRETIL-mirror/gretil/"
    "1_sanskr/1_veda/1_sam/1_rv/rvpp_{mandala:02d}u.htm"
)

# Each tuple is (row ID, Vaidika form, comparison form). Several rows have more
# than one pair because the source inventory contains distinct subclaims.
COMPARISONS = [
    ("SG-02", "manīṣā", "manīṣayā"),
    ("SG-03", "paśvā", "paśunā"),
    ("SG-06", "śiśve", "śiśave"),
    ("SG-10", "agnā", "agnau"),
    ("SG-12", "sānavi", "sānau"),
    ("SG-19", "mūrdhan", "mūrdhani"),
    ("SG-20", "mahinā", "mahimnā"),
    ("SG-21", "bhūmanā", "bhūmnā"),
    ("SG-22", "harivaḥ", "harivan"),
    ("SG-23", "cikitvaḥ", "cikitvan"),
    ("SG-24", "ojīyaḥ", "ojīyan"),
    ("SG-26", "tvā", "tvayā"),
    ("SG-27", "asme", "asmabhyam"),
    ("SG-27", "yuṣme", "yuṣmabhyam"),
    ("SG-29", "tyā", "tyayā"),
    ("DU-01", "aśvinā", "aśvinau"),
    ("DU-04", "devī", "devyau"),
    ("DU-10", "yuvabhyām", "yuvābhyām"),
    ("DU-11", "enoḥ", "enayoḥ"),
    ("PL-01", "devāsaḥ", "devāḥ"),
    ("PL-03", "devīḥ", "devyaḥ"),
    ("PL-07", "viśvā", "viśvāni"),
    ("PL-08", "śucī", "śucīni"),
    ("PL-09", "madhū", "madhūni"),
    ("PL-10", "brahma", "brahmāṇi"),
    ("PL-10", "brahmā", "brahmāṇi"),
    ("PL-12", "devebhiḥ", "devaiḥ"),
    ("PL-12", "rudrebhiḥ", "rudraiḥ"),
    ("PL-13", "yebhiḥ", "yaiḥ"),
    ("PL-17", "asmāka", "asmākam"),
    ("PL-17", "yuṣmāka", "yuṣmākam"),
    ("PL-19", "imā", "imāni"),
    ("PL-20", "yā", "yāni"),
    ("PL-21", "yebhiḥ", "yaiḥ"),
    ("NU-01", "dvā", "dvau"),
    ("NU-02", "trī", "trīṇi"),
    ("NU-03", "trīṇām", "trayāṇām"),
    ("NU-04", "aṣṭā", "aṣṭau"),
]

SINGLE_FORMS = [
    ("SG-01", "mahitvā"),
    ("SG-11", "vedī"),
    ("SG-18", "kartari"),
    ("DU-09", "yuvam"),
    ("DU-09", "yuvām"),
    ("DU-09", "yuvat"),
    ("DU-09", "yuvoḥ"),
    ("DU-12", "yoḥ"),
    ("PL-02", "vaśāsaḥ"),
    ("NU-05", "pañca"),
    ("NU-06", "sahasram"),
    ("NU-06", "śatam"),
    ("NU-04", "aṣṭa"),
]

SUFFIX_COMPARISONS = [
    ("PL-12", "-ebhiḥ", "-aiḥ"),
]


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"br", "p", "div", "pre", "li"}:
            self.parts.append("\n")

    def text(self) -> str:
        return html.unescape("".join(self.parts))


def fetch_mandala(mandala: int, cache_dir: Path) -> str:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"rvpp_{mandala:02d}.html"
    if not cache_path.exists():
        url = BASE_URL.format(mandala=mandala)
        with urllib.request.urlopen(url) as response:
            cache_path.write_bytes(response.read())
    return cache_path.read_text(encoding="utf-8")


def extract_tokens(document: str) -> list[tuple[str, str]]:
    parser = VisibleTextParser()
    parser.feed(document)
    text = parser.text()

    tokens: list[tuple[str, str]] = []
    for match in re.finditer(r"(?m)^(.+?)//\s*(RV_\d+,\d+\.\d+)\s*//", text):
        passage, reference = match.groups()
        for part in passage.split("|"):
            token = " ".join(part.split())
            if token.endswith(" iti"):
                token = token[:-4]
            if token:
                tokens.append((token, reference.replace("_", " ")))
    return tokens


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("/tmp/atomic-sanskrit-rvpp"),
        help="Directory used for downloaded GRETIL pages.",
    )
    parser.add_argument(
        "--format",
        choices=("table", "csv"),
        default="table",
        help="Output format.",
    )
    args = parser.parse_args()

    all_tokens: list[tuple[str, str]] = []
    for mandala in range(1, 11):
        all_tokens.extend(extract_tokens(fetch_mandala(mandala, args.cache_dir)))

    counts = Counter(token for token, _ in all_tokens)
    references: dict[str, list[str]] = defaultdict(list)
    for token, reference in all_tokens:
        references[token].append(reference)

    rows = []
    for row_id, vaidika, comparison in COMPARISONS:
        v_count = counts[vaidika]
        c_count = counts[comparison]
        total = v_count + c_count
        share = (100 * v_count / total) if total else None
        rows.append(
            {
                "row_id": row_id,
                "vaidika_form": vaidika,
                "vaidika_raw_count": v_count,
                "comparison_form": comparison,
                "comparison_raw_count": c_count,
                "pair_total": total,
                "vaidika_raw_share_pct": f"{share:.1f}" if share is not None else "",
                "vaidika_references": "; ".join(references[vaidika]),
                "comparison_references": "; ".join(references[comparison]),
            }
        )

    for row_id, vaidika in SINGLE_FORMS:
        rows.append(
            {
                "row_id": row_id,
                "vaidika_form": vaidika,
                "vaidika_raw_count": counts[vaidika],
                "comparison_form": "",
                "comparison_raw_count": "",
                "pair_total": "",
                "vaidika_raw_share_pct": "",
                "vaidika_references": "; ".join(references[vaidika]),
                "comparison_references": "",
            }
        )

    token_counts = Counter(token for token, _ in all_tokens)
    for row_id, vaidika_suffix, comparison_suffix in SUFFIX_COMPARISONS:
        v_count = sum(
            count
            for token, count in token_counts.items()
            if token.endswith(vaidika_suffix.removeprefix("-"))
        )
        c_count = sum(
            count
            for token, count in token_counts.items()
            if token.endswith(comparison_suffix.removeprefix("-"))
        )
        total = v_count + c_count
        share = (100 * v_count / total) if total else None
        rows.append(
            {
                "row_id": row_id,
                "vaidika_form": vaidika_suffix,
                "vaidika_raw_count": v_count,
                "comparison_form": comparison_suffix,
                "comparison_raw_count": c_count,
                "pair_total": total,
                "vaidika_raw_share_pct": f"{share:.1f}" if share is not None else "",
                "vaidika_references": "",
                "comparison_references": "",
            }
        )

    columns = list(rows[0])
    if args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
        return 0

    print(
        "| Row | Vaidika form | Raw count | Comparison | Raw count | "
        "Pair total | Raw Vaidika share |"
    )
    print("|---|---|---:|---|---:|---:|---:|")
    for row in rows:
        share = (
            f"{row['vaidika_raw_share_pct']}%"
            if row["vaidika_raw_share_pct"]
            else ""
        )
        print(
            f"| {row['row_id']} | {row['vaidika_form']} | "
            f"{row['vaidika_raw_count']} | {row['comparison_form']} | "
            f"{row['comparison_raw_count']} | {row['pair_total']} | "
            f"{share} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
