#!/usr/bin/env bash
# refresh_dashboard_fast.sh -- pull + rebuild ONLY, no tagging. Used by
# the dashboard's own "Refresh now" button (dashboard_api.py's /refresh
# route) for a fast, reliable response.
#
# auto_tagger.py's LLM calls (one per untagged annotation, each ~1-2s
# plus a courtesy sleep between calls) can push a full refresh past a
# minute when there's a tagging backlog -- confirmed live 2026-08-16:
# this made the button feel erratic, and a long-running fetch() is
# fragile on top of that (a backgrounded tab or a locked phone can kill
# it silently mid-wait, with no error shown and no reload -- exactly
# "no callback, had to refresh manually to see it actually worked").
#
# Tagging still happens reliably regardless of this button -- it's
# refresh_dashboard.sh's own job, unaffected, on its normal 15-minute
# cron cycle. New comments show up here immediately, un-tagged until
# that next cycle catches up -- an acceptable tradeoff for a fast,
# reliable "show me what's new right now" button.
set -euo pipefail
cd "$(dirname "$0")"

python3 pull_annotations.py
python3 build_dashboard.py --install /var/www/as/private/dashboard/index.html \
    --readers /var/lib/secondshanti/dashboard_readers
