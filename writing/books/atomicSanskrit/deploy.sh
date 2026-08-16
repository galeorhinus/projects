#!/usr/bin/env bash
# deploy.sh — push the built web book to /var/www/as/ and reload Caddy.
#
# Pipeline:
#   1. (Optional) Run build_html.py to refresh build/html/.
#   2. rsync build/html/ → /var/www/as/.
#   3. Copy the updated Caddyfile to /etc/caddy/Caddyfile and reload Caddy.
#   4. Install server/invite_roster.json to /etc/secondshanti/, read-only
#      to the request-access service — see server/README.md. No service
#      restart needed; the roster is read fresh on every request.
#
# Pass --skip-build to skip the build step (use when build/html/ is already
# fresh). Pass --skip-caddy to skip Caddyfile + reload (use when only the
# rendered HTML changed). Pass --skip-roster to skip the roster install.
#
# Requires sudo for /etc/caddy/, /etc/secondshanti/, and `systemctl reload
# caddy`. /var/www/as is owned by the ubuntu user (set up at install
# time), so the rsync into it does not need sudo.

set -euo pipefail
cd "$(dirname "$0")"

SKIP_BUILD=0
SKIP_CADDY=0
SKIP_ROSTER=0
for arg in "$@"; do
	case "$arg" in
		--skip-build) SKIP_BUILD=1 ;;
		--skip-caddy) SKIP_CADDY=1 ;;
		--skip-roster) SKIP_ROSTER=1 ;;
		*) echo "Unknown arg: $arg" >&2; exit 2 ;;
	esac
done

SRC="build/html"
DST="/var/www/as"

if [ "$SKIP_BUILD" -eq 0 ]; then
	echo ">> Building HTML..."
	python3 build_html.py
fi

if [ ! -d "$SRC" ]; then
	echo "Missing $SRC — run python3 build_html.py first." >&2
	exit 1
fi

# Sanity gates: refuse to rsync if the build is partial. The rsync uses
# --delete, which means anything missing from $SRC gets removed from $DST.
# A partial build (e.g., book-only output) would silently wipe the public
# landing, essays, and private tier. These checks block that.
required_files=(
	"$SRC/index.html"
	"$SRC/book/index.html"
	"$SRC/essays/index.html"
	"$SRC/essays/style.css"
	"$SRC/private/index.html"
)
missing=0
for f in "${required_files[@]}"; do
	if [ ! -f "$f" ]; then
		echo "MISSING (would corrupt deploy): $f" >&2
		missing=1
	fi
done
file_count=$(find "$SRC" -type f | wc -l)
if [ "$file_count" -lt 20 ]; then
	echo "Build has only $file_count files — refusing to deploy a partial build." >&2
	missing=1
fi
if [ "$missing" -ne 0 ]; then
	echo "Aborting before rsync. Fix the build first (python3 build_html.py)." >&2
	exit 1
fi

echo ">> rsync $SRC/ → $DST/  (${file_count} files)"
# --exclude protects private/dashboard/ from --delete: that path is
# written directly by hypothesis/build_dashboard.py --install (run by
# amrut's cron job, hypothesis/run_pipeline.sh), not part of build/html/
# at all -- without this exclude, --delete silently wipes it on every
# deploy.sh run since rsync sees it as an extraneous destination file.
# Bit 2026-08-16: two Caddyfile-only deploys in a row deleted it, which
# looked exactly like an auth bug (404) until traced back here.
rsync -a --delete --exclude='private/dashboard/' "$SRC/" "$DST/"

if [ "$SKIP_CADDY" -eq 0 ]; then
	echo ">> Installing Caddyfile + reloading Caddy..."
	sudo install -o root -g caddy -m 640 Caddyfile /etc/caddy/Caddyfile
	sudo systemctl reload caddy
fi

if [ "$SKIP_ROSTER" -eq 0 ]; then
	if [ -f "server/invite_roster.json" ]; then
		echo ">> Installing invite roster..."
		sudo mkdir -p /etc/secondshanti
		sudo install -o www-data -g www-data -m 640 server/invite_roster.json /etc/secondshanti/invite_roster.json
	else
		echo ">> No server/invite_roster.json in the working tree — skipping roster install."
	fi
fi

echo ">> Done."
echo "   Local check: curl -sI https://secondshanti.org/as/"
echo "   (basicauth retired 2026-08-06 — /as/book/ and /as/private/ now gate via"
echo "   Google OAuth, which curl can't drive; check those in a browser instead.)"
