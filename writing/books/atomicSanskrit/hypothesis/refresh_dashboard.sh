#!/usr/bin/env bash
# refresh_dashboard.sh -- pull + tag + rebuild the live dashboard, no
# digest. Runs on its own frequent cadence (every 15 minutes via plain
# cron -- no DST-safe gating needed, unlike cron_gate.sh's fixed
# 8am/6pm slots, since "every 15 minutes" is a relative interval with
# no timezone dependency at all) so the dashboard stays close to
# real-time instead of only refreshing twice a day. digest_send.py
# stays on the existing twice-daily cadence (see cron_gate.sh) -- an
# email notification every 15 minutes would be spam, not a digest; the
# dashboard is the near-real-time view now, the email is the periodic
# summary.
#
# Also the target of the dashboard's own "Refresh now" button
# (dashboard_api.py's /refresh route) for on-demand checks between
# scheduled runs.
set -euo pipefail
cd "$(dirname "$0")"

python3 pull_annotations.py
python3 auto_tagger.py
python3 build_dashboard.py --install /var/www/as/private/dashboard/index.html
