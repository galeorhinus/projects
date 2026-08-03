#!/usr/bin/env python3
"""Count exact deva-lemma tokens and mantras in the VedaWeb 1.0 TEI corpus."""

from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


DEVA_LEMMA = "#lemma_deva_4419"
TEI_NS = "{http://www.tei-c.org/ns/1.0}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def count_book(path: Path) -> tuple[int, int]:
    root = ET.parse(path).getroot()
    token_count = 0
    mantra_ids: set[str] = set()

    for stanza in root.iter(f"{TEI_NS}div"):
        if stanza.get("type") != "stanza":
            continue

        stanza_has_deva = False
        for lemma in stanza.iter(f"{TEI_NS}f"):
            if lemma.get("name") != "gra_lemma":
                continue
            for value in lemma.findall(f"{TEI_NS}string"):
                if value.get("match") == DEVA_LEMMA:
                    token_count += 1
                    stanza_has_deva = True

        if stanza_has_deva:
            mantra_ids.add(stanza.get(XML_ID, ""))

    return token_count, len(mantra_ids)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Count exact deva-lemma tokens and unique mantras by Rigvedic book."
    )
    parser.add_argument(
        "corpus_dir",
        type=Path,
        help="Directory containing the ten VedaWeb 1.0 rv_book_*.tei files.",
    )
    args = parser.parse_args()

    paths = sorted(args.corpus_dir.glob("rv_book_*.tei"))
    if len(paths) != 10:
        raise SystemExit(f"Expected 10 rv_book_*.tei files; found {len(paths)}")

    total_tokens = 0
    total_mantras = 0
    for path in paths:
        tokens, mantras = count_book(path)
        total_tokens += tokens
        total_mantras += mantras
        print(f"{path.stem}: {tokens} tokens, {mantras} mantras")

    print(f"TOTAL: {total_tokens} tokens, {total_mantras} mantras")


if __name__ == "__main__":
    main()
