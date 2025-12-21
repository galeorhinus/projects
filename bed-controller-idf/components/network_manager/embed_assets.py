#!/usr/bin/env python3
"""
Minimal asset pipeline: minify and gzip HTML/JS/CSS/JSON assets for embedding.
Inputs are read from the project-level "data" folder. Outputs (.gz) are written
to OUT_DIR (default: ./embedded under this component).
"""
import gzip
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]  # project root
DATA_DIR = ROOT / "data"

FILES = [
    "index.html",
    "app.js",
    "bed-visualizer.js",
    "style.css",
    "sw.js",
    "branding.json",
    "favicon.png",
]

UI_BUILD_TAG = os.environ.get("UI_BUILD_TAG", "UI_BUILD_DEV")
UI_ROLE = os.environ.get("UI_ROLE", "bed")
UI_ROLES = os.environ.get("UI_ROLES", UI_ROLE)


def minify_js(text: str) -> str:
    text = re.sub(r"/\\*.*?\\*/", "", text, flags=re.S)  # block comments
    text = re.sub(r"//.*", "", text)  # line comments
    text = re.sub(r"\\s+", " ", text)
    return text.strip()


def minify_css(text: str) -> str:
    text = re.sub(r"/\\*.*?\\*/", "", text, flags=re.S)
    text = re.sub(r"\\s+", " ", text)
    text = re.sub(r" ?([{}:;,]) ?", r"\\1", text)
    text = text.replace(";}", "}")
    return text.strip()


def minify_html(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r">\\s+<", "><", text)
    text = re.sub(r"\\s+", " ", text)
    return text.strip()


def minify_json(text: str) -> str:
    text = re.sub(r"\\s+", " ", text)
    return text.strip()


# Disable minification for now to avoid breaking JS; still gzip compress.
MINIFIERS = {}


def main():
    out_dir = pathlib.Path(os.environ.get("OUT_DIR", pathlib.Path(__file__).parent / "embedded"))
    out_dir.mkdir(parents=True, exist_ok=True)

    for rel in FILES:
        src = DATA_DIR / rel
        if not src.exists():
            print(f"Missing asset: {src}", file=sys.stderr)
            sys.exit(1)
        suffix = src.suffix.lower()
        minify = MINIFIERS.get(suffix)
        if rel == "app.js":
            text = src.read_text(encoding="utf-8")
            text = text.replace("__UI_BUILD_TAG__", UI_BUILD_TAG)
            text = text.replace("__UI_ROLE__", UI_ROLE)
            text = text.replace("__UI_ROLES__", UI_ROLES)
            raw = text.encode("utf-8")
        elif minify:
            raw = minify(src.read_text(encoding="utf-8")).encode("utf-8")
        else:
            raw = src.read_bytes()
        gz_path = out_dir / f"{src.name}.gz"
        with gzip.open(gz_path, "wb", compresslevel=9) as f:
            f.write(raw)
        print(f"Wrote {gz_path} ({len(raw)} bytes raw)")


if __name__ == "__main__":
    main()
