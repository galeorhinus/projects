#!/usr/bin/env bash
# run_pipeline.sh -- the cron entry point on amrut. Pulls fresh
# annotations, backstops tags via the LLM, installs the dashboard at
# https://secondshanti.org/as/private/dashboard/ (owner-only -- see the
# Caddyfile), and sends a digest email of what's new (silent no-op if
# nothing is). This is the one script that publishes the dashboard
# autonomously; publishing dashboard.html as a Claude Artifact instead
# (or in addition) is still available but needs an interactive Claude
# Code session and a manual republish each time.
set -euo pipefail
cd "$(dirname "$0")"

python3 pull_annotations.py
python3 auto_tagger.py
python3 build_dashboard.py --install /var/www/as/private/dashboard/index.html
python3 digest_send.py
