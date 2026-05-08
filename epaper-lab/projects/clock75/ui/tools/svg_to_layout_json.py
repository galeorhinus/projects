#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"


def strip_ns(tag: str) -> str:
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def parse_style(root: ET.Element) -> str:
    for defs in root.findall(f"{{{SVG_NS}}}defs"):
        for style in defs.findall(f"{{{SVG_NS}}}style"):
            return style.text or ""
    return ""


def parse_elements(root: ET.Element):
    elements = []
    for elem in root.iter():
        tag = strip_ns(elem.tag)
        if tag in {"svg", "defs", "style"}:
            continue
        attrs = {k: v for k, v in elem.attrib.items()}
        text = (elem.text or "").strip() if tag == "text" else ""
        elements.append({"tag": tag, "attrs": attrs, "text": text})
    return elements


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("in_svg")
    ap.add_argument("out_json")
    args = ap.parse_args()

    tree = ET.parse(args.in_svg)
    root = tree.getroot()

    layout = {
        "width": int(root.attrib.get("width", "800")),
        "height": int(root.attrib.get("height", "480")),
        "viewBox": root.attrib.get("viewBox", "0 0 800 480"),
        "style": parse_style(root),
        "elements": parse_elements(root),
    }

    Path(args.out_json).write_text(json.dumps(layout, indent=2), encoding="ascii")


if __name__ == "__main__":
    main()
