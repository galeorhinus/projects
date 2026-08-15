#!/usr/bin/env bash
# run_pipeline.sh -- the cron entry point on amrut. Pulls fresh
# annotations, backstops tags via the LLM, and sends a digest email of
# what's new (silent no-op if nothing is). Deliberately does NOT run
# build_dashboard.py: publishing dashboard.html as a Claude Artifact
# needs an interactive Claude Code session (the Artifact tool), so the
# dashboard stays a manual "ask Claude to refresh and republish" step,
# not something cron can do on its own.
set -euo pipefail
cd "$(dirname "$0")"

python3 pull_annotations.py
python3 auto_tagger.py
python3 digest_send.py
