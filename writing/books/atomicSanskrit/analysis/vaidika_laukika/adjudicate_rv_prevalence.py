#!/usr/bin/env python3
"""Extract morphologically annotated Rigvedic candidates for prevalence rows.

The VedaWeb TEI corpus supplies a surface form, lemma, grammatical category,
and morphological features for each annotated token. This script keeps the
annotation and the acceptance decision together so that a visible spelling is
never counted as a grammatical form without review.

The output is a research dataset, not a claim that every VedaWeb annotation is
infallible. Rows that require syntax beyond token morphology remain marked for
manual review.
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
CORPUS_VERSION = "VedaWeb TEI 6d94702e078b2d8fc04af1241aba63132c4601a3"


@dataclass(frozen=True)
class Target:
    row_id: str
    form: str
    expected: str


TARGETS = [
    Target("SG-16", "śamī", "INS.SG.F"),
    Target("SG-16", "śami", "INS.SG.F"),
    Target("SG-17", "gaurī", "LOC.SG.F"),
    Target("SG-18", "kartarī", "LOC.SG"),
    Target("SG-18", "kartari", "LOC.SG comparison"),
    Target("SG-26", "tvā", "INS.SG pronoun"),
    Target("SG-27", "asme", "DAT/LOC.PL pronoun"),
    Target("SG-27", "yuṣme", "DAT/LOC.PL pronoun"),
    Target("SG-28", "enā", "INS.SG demonstrative or adverbial"),
    Target("SG-28", "ayā", "INS.SG demonstrative or adverbial"),
    Target("SG-29", "tyā", "INS.SG.F demonstrative"),
    Target("DU-05", "śucī", "NOM/ACC/VOC.DU.N short form"),
    Target("DU-05", "mahi", "NOM/ACC/VOC.DU.N short form"),
    Target("DU-05", "hariṇī", "NOM/ACC/VOC.DU.N later-form candidate"),
    Target("DU-07", "anī", "NOM/ACC/VOC.DU.N candidate suffix"),
    Target("DU-07", "aṇī", "NOM/ACC/VOC.DU.N candidate suffix"),
    Target("PL-04", "īḥ", "NOM/ACC.PL.F candidate suffix"),
    Target("PL-04", "yaḥ", "NOM/ACC.PL.F comparison suffix"),
    Target("PL-06", "paśvaḥ", "ACC.PL source-listed form"),
    Target("PL-06", "madhvaḥ", "ACC.PL source-listed form"),
    Target("PL-06", "śucayaḥ", "ACC.PL doubtful source-listed form"),
    Target("PL-19", "imā", "NOM/ACC.PL.N demonstrative"),
    Target("PL-19", "imāni", "NOM/ACC.PL.N demonstrative"),
    Target("PL-20", "yā", "NOM/ACC.PL.N relative"),
    Target("PL-20", "yāni", "NOM/ACC.PL.N relative"),
    Target("NU-02", "trī", "NOM/ACC.PL.N numeral"),
    Target("NU-02", "trīṇi", "NOM/ACC.PL.N numeral"),
    Target("NU-04", "aṣṭa", "NOM/ACC numeral"),
    Target("NU-04", "aṣṭā", "NOM/ACC numeral"),
    Target("NU-04", "aṣṭau", "NOM/ACC numeral"),
    Target("NU-05", "pañca", "syntax review: uninflected numeral"),
    Target("NU-06", "sahasram", "syntax review: uninflected collective"),
    Target("NU-06", "śatam", "syntax review: uninflected collective"),
]


def normalize_surface(value: str) -> str:
    """Remove pitch marks while retaining ordinary IAST distinctions."""
    value = value.replace("r̥", "ṛ").replace("l̥", "ḷ")
    value = value.replace("r̥̄", "ṝ").replace("l̥̄", "ḹ")
    pitch_vowels = str.maketrans(
        {
            "á": "a",
            "à": "a",
            "â": "a",
            "í": "i",
            "ì": "i",
            "î": "i",
            "ú": "u",
            "ù": "u",
            "û": "u",
            "é": "e",
            "è": "e",
            "ê": "e",
            "ó": "o",
            "ò": "o",
            "ô": "o",
            "ŕ": "r",
        }
    )
    value = unicodedata.normalize("NFC", value).translate(pitch_vowels)
    pitch_marks = {
        "\u0300",  # grave
        "\u0301",  # acute
        "\u0302",  # circumflex
        "\u1cd0",
        "\u1cd1",
        "\u1cd2",
    }
    cleaned = "".join(char for char in value if char not in pitch_marks)
    return unicodedata.normalize("NFC", cleaned)


def get_field(fs: ET.Element, name: str) -> str:
    field = fs.find(f"./{{{TEI_NS}}}f[@name='{name}']")
    if field is None:
        return ""
    symbol = field.find(f"./{{{TEI_NS}}}symbol")
    if symbol is not None:
        return symbol.get("value", "")
    string = field.find(f"./{{{TEI_NS}}}string")
    if string is not None and string.text:
        return string.text.strip()
    return ""


def get_morphology(fs: ET.Element) -> dict[str, str]:
    values: dict[str, str] = {}
    field = fs.find(f"./{{{TEI_NS}}}f[@name='morphosyntax']")
    if field is None:
        return values
    nested = field.find(f"./{{{TEI_NS}}}fs")
    if nested is None:
        return values
    for item in nested.findall(f"./{{{TEI_NS}}}f"):
        name = item.get("name", "")
        symbol = item.find(f"./{{{TEI_NS}}}symbol")
        if name and symbol is not None:
            values[name] = symbol.get("value", "")
    return values


def reference_from_id(token_id: str) -> str:
    match = re.match(
        r"b(?P<book>\d+)_h(?P<hymn>\d+)_(?P<verse>\d+)_zur_(?P<line>[a-z]+)_(?P<token>\d+)",
        token_id,
    )
    if not match:
        return token_id
    fields = match.groupdict()
    return (
        f"RV {int(fields['book'])}.{int(fields['hymn'])}."
        f"{int(fields['verse'])}{fields['line']}"
    )


def suffix_match(surface: str, target: Target) -> bool:
    if target.form in {"anī", "aṇī", "īḥ", "yaḥ"}:
        return surface.endswith(target.form)
    return surface == target.form


def adjudicate(
    target: Target,
    lemma: str,
    gram_class: str,
    morphology: dict[str, str],
) -> tuple[str, str]:
    case = morphology.get("case", "")
    gender = morphology.get("gender", "")
    number = morphology.get("number", "")

    if target.row_id == "SG-16":
        accepted = case == "INS" and number == "SG" and gender == "F"
        return (
            ("accepted", "instrumental singular feminine")
            if accepted
            else ("rejected", "not instrumental singular feminine")
        )
    if target.row_id == "SG-17":
        accepted = case == "LOC" and number == "SG" and gender == "F"
        return (
            ("accepted", "locative singular feminine")
            if accepted
            else ("rejected", "not locative singular feminine")
        )
    if target.row_id == "SG-18":
        accepted = case == "LOC" and number == "SG"
        return (
            ("accepted", "locative singular")
            if accepted
            else ("rejected", "not locative singular")
        )
    if target.row_id == "SG-26":
        accepted = case == "INS" and number == "SG"
        return (
            ("accepted", "instrumental singular pronoun")
            if accepted
            else ("rejected", "homograph with another relation or verbal form")
        )
    if target.row_id == "SG-27":
        accepted = number == "PL" and gram_class == "pronoun"
        return (
            (
                "accepted",
                f"{case.lower()} plural pronoun" if case else "plural pronoun; relation untagged",
            )
            if accepted
            else ("rejected", "not an annotated plural pronoun")
        )
    if target.row_id == "SG-28":
        if gram_class == "adverb":
            return "accepted", "annotated as adverbial use"
        accepted = case == "INS" and number == "SG"
        return (
            ("accepted", "instrumental singular")
            if accepted
            else ("rejected", "not instrumental singular or adverbial")
        )
    if target.row_id == "SG-29":
        accepted = case == "INS" and number == "SG" and gender == "F"
        return (
            ("accepted", "instrumental singular feminine")
            if accepted
            else ("rejected", "not instrumental singular feminine")
        )
    if target.row_id in {"DU-05", "DU-07"}:
        accepted = (
            case in {"NOM", "ACC", "VOC"} and number == "DU" and gender == "N"
        )
        return (
            ("accepted", "neuter dual")
            if accepted
            else ("rejected", "suffix match outside the neuter dual")
        )
    if target.row_id == "PL-04":
        accepted = (
            normalize_surface(lemma).rstrip("-").endswith("ī")
            and case in {"NOM", "ACC"}
            and number == "PL"
            and gender == "F"
        )
        return (
            ("accepted", f"{case.lower()} plural feminine")
            if accepted
            else ("rejected", "suffix match outside nominative/accusative plural feminine")
        )
    if target.row_id == "PL-06":
        accepted = case == "ACC" and number == "PL"
        return (
            ("accepted", "accusative plural")
            if accepted
            else ("rejected", "suffix match outside the accusative plural")
        )
    if target.row_id in {"PL-19", "PL-20", "NU-02"}:
        accepted = (
            case in {"", "NOM", "ACC"} and number == "PL" and gender == "N"
        )
        return (
            ("accepted", f"{case.lower()} plural neuter")
            if accepted
            else ("rejected", "homograph outside nominative/accusative plural neuter")
        )
    if target.row_id == "NU-04":
        if normalize_surface(lemma).startswith("aṣṭ"):
            return "accepted", "annotated with the numeral lemma"
        return "rejected", "homograph belongs to another lemma"
    if target.row_id in {"NU-05", "NU-06"}:
        return "review", "token morphology cannot decide the construction"
    return "review", "no automatic rule"


def iter_tokens(tei_files: Iterable[Path]) -> Iterable[dict[str, str]]:
    for path in tei_files:
        for _, elem in ET.iterparse(path, events=("end",)):
            if elem.tag != f"{{{TEI_NS}}}fs" or elem.get("type") != "zurich_info":
                continue
            surface = get_field(elem, "surface")
            if not surface:
                elem.clear()
                continue
            morphology = get_morphology(elem)
            yield {
                "token_id": elem.get(XML_ID, ""),
                "reference": reference_from_id(elem.get(XML_ID, "")),
                "surface": surface,
                "normalized_surface": normalize_surface(surface),
                "lemma": get_field(elem, "gra_lemma"),
                "gram_class": get_field(elem, "gra_gramm"),
                "case": morphology.get("case", ""),
                "gender": morphology.get("gender", ""),
                "number": morphology.get("number", ""),
                "person": morphology.get("person", ""),
                "mood": morphology.get("mood", ""),
                "tense": morphology.get("tense", ""),
                "voice": morphology.get("voice", ""),
            }
            elem.clear()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tei-dir",
        type=Path,
        required=True,
        help="Directory containing VedaWeb rv_book_*.tei files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="CSV destination. Omit to write CSV to standard output.",
    )
    parser.add_argument(
        "--include-rejected",
        action="store_true",
        help="Include homographs and suffix matches rejected by the row rule.",
    )
    args = parser.parse_args()

    tei_files = sorted(args.tei_dir.glob("rv_book_*.tei"))
    if len(tei_files) != 10:
        parser.error(f"expected 10 rv_book_*.tei files; found {len(tei_files)}")

    rows: list[dict[str, str]] = []
    for token in iter_tokens(tei_files):
        for target in TARGETS:
            if not suffix_match(token["normalized_surface"], target):
                continue
            morphology = {
                key: token[key] for key in ("case", "gender", "number")
            }
            decision, reason = adjudicate(
                target,
                token["lemma"],
                token["gram_class"],
                morphology,
            )
            if decision == "rejected" and not args.include_rejected:
                continue
            rows.append(
                {
                    "row_id": target.row_id,
                    "target": target.form,
                    "expected": target.expected,
                    **token,
                    "decision": decision,
                    "reason": reason,
                    "source": CORPUS_VERSION,
                }
            )

    fieldnames = list(rows[0]) if rows else [
        "row_id",
        "target",
        "expected",
        "token_id",
        "reference",
        "surface",
        "normalized_surface",
        "lemma",
        "gram_class",
        "case",
        "gender",
        "number",
        "person",
        "mood",
        "tense",
        "voice",
        "decision",
        "reason",
        "source",
    ]
    destination = args.output.open("w", encoding="utf-8", newline="") if args.output else None
    stream = destination if destination is not None else __import__("sys").stdout
    try:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if destination is not None:
            destination.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
