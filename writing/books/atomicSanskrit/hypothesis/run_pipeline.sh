#!/usr/bin/env bash
# run_pipeline.sh -- manual full-refresh convenience: pull + tag +
# rebuild the dashboard + send the digest, all four steps, in one call.
#
# NOT cron's entry point anymore (was, until 2026-08-17) -- cron now
# runs the two halves on their own separate cadences instead:
#   refresh_dashboard.sh  -- pull + tag + dashboard, every 15 minutes
#   cron_gate.sh           -- digest_send.py only, at 8am/6pm Chicago
# splitting them out let the dashboard become a near-real-time default
# view without also firing an email notification every 15 minutes.
# This script still runs the old all-in-one sequence, useful when
# testing changes or wanting everything caught up immediately by hand.
set -euo pipefail
cd "$(dirname "$0")"

python3 pull_annotations.py
python3 auto_tagger.py
python3 build_dashboard.py --install /var/www/as/private/dashboard/index.html \
    --readers /var/lib/secondshanti/dashboard_readers
python3 digest_send.py
