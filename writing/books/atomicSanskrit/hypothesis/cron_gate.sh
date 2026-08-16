#!/usr/bin/env bash
# cron_gate.sh -- fires digest_send.py only at 8am and 6pm America/Chicago
# wall-clock time.
#
# Exists because amrut's cron (Ubuntu's stock "cron" package, 3.0pl1 --
# the traditional Debian/Vixie fork, not cronie) does NOT honor a "TZ="
# line in the crontab for SCHEDULE interpretation, only for the executed
# job's own environment. Confirmed live 2026-08-16: a crontab entry
# "TZ=America/Chicago" + "0 8,18 * * *" fired at 08:00 and 18:00 system
# time -- and amrut's system timezone is UTC (`timedatectl`) -- so the
# "8am digest" was actually firing at 3am Chicago, silently, hours
# before the user was awake to notice, which read exactly like a
# missing/broken digest until traced back to this.
#
# `date` (unlike cron's own scheduler) DOES honor an inline TZ= prefix
# and re-reads the system's tzdata on every call, so checking real
# Chicago wall time here handles DST correctly without hardcoding a UTC
# offset that would drift twice a year. Cron itself just runs this gate
# every minute; it's silent (no output, nothing appended to cron.log)
# except in the exact target minute, when it hands off to digest_send.py.
#
# Targets digest_send.py directly, not the old run_pipeline.sh (pull +
# tag + dashboard + digest) -- since refresh_dashboard.sh separately
# runs pull + tag + dashboard every 15 minutes now (added 2026-08-17,
# so the dashboard can be a near-real-time default view instead of
# only refreshing twice a day), running that again here would just be
# a redundant, possibly-racing second pull at the same moment.
# digest_send.py reads whatever refresh_dashboard.sh's most recent
# 15-minute tick already wrote to data/annotations.json -- if that
# tick and this one land in the same minute and race, the digest is
# at worst a few minutes stale, never wrong: its own "since last
# digest" state is timestamp-based, not tick-based, so nothing gets
# silently skipped, only deferred to the next send.
set -euo pipefail
cd "$(dirname "$0")"

now=$(TZ=America/Chicago date +%H%M)
if [ "$now" = "0800" ] || [ "$now" = "1800" ]; then
    exec python3 digest_send.py
fi
