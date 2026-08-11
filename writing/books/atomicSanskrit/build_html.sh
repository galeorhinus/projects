#!/usr/bin/env bash
# build_html.sh — Atomic Sanskrit web book build.
# Wrapper around build_html.py. Run from anywhere; the python script resolves
# paths relative to the repo root.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 build_html.py "$@"
