#!/usr/bin/env python3
"""
Minimal asset pipeline: minify and gzip HTML/JS/CSS/JSON assets for embedding.
Inputs are read from the project-level "data" folder. Outputs (.gz) are written
to OUT_DIR (default: ./embedded under this component).
"""
import gzip
import os
import pathlib
import random
import re
import sys
import time
import shutil

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

UI_BUILD_TAG_FILE = os.environ.get("UI_BUILD_TAG_FILE")
UI_BUILD_TAG = os.environ.get("UI_BUILD_TAG")
if not UI_BUILD_TAG and UI_BUILD_TAG_FILE and pathlib.Path(UI_BUILD_TAG_FILE).exists():
    UI_BUILD_TAG = pathlib.Path(UI_BUILD_TAG_FILE).read_text(encoding="utf-8").strip()
if not UI_BUILD_TAG:
    suffix = "".join(random.choice("0123456789ABCDEF") for _ in range(6))
    UI_BUILD_TAG = time.strftime("UI_BUILD_%Y-%m-%d_%H%M%S") + "_" + suffix
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
    tag_path = pathlib.Path(UI_BUILD_TAG_FILE) if UI_BUILD_TAG_FILE else (out_dir / "ui_build_tag.txt")
    tag_path.parent.mkdir(parents=True, exist_ok=True)
    tag_path.write_text(UI_BUILD_TAG, encoding="utf-8")
    print(f"Wrote build tag {UI_BUILD_TAG} -> {tag_path}")

    generated = []
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
        generated.append(gz_path)

    # Touch a stamp file so CMake rebuilds embedded assets even with a stale build dir
    stamp_path = out_dir / "assets.stamp"
    stamp_path.write_text(str(time.time()), encoding="utf-8")
    print(f"Updated stamp {stamp_path}")

    # Opportunistically copy fresh assets into build output (avoids stale gz when build dir already exists)
    build_dir = ROOT / "build"
    if build_dir.exists():
        # Default IDF layout for the component
        targets = [build_dir / "esp-idf" / "network_manager" / "embedded"]
        copied_any = False
        for dest in targets:
            if not dest.exists():
                # Only copy if the component has already been configured
                continue
            dest.mkdir(parents=True, exist_ok=True)
            for gz in generated:
                dest_path = dest / gz.name
                if gz.resolve() == dest_path.resolve():
                    continue  # already writing directly to the build output
                shutil.copy2(gz, dest_path)
            dest_stamp = dest / stamp_path.name
            if stamp_path.resolve() != dest_stamp.resolve():
                shutil.copy2(stamp_path, dest_stamp)
            copied_any = True
            print(f"Copied assets to {dest}")
        if not copied_any:
            print("Build dir present but no network_manager/embedded folder yet; skipping copy.")
    else:
        print("Build dir not found; skipping copy into build output.")


if __name__ == "__main__":
    main()
