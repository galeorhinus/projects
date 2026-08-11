#!/usr/bin/env bash
# deploy.sh — push the built web book to /var/www/as/ and reload Caddy.
#
# Pipeline:
#   1. (Optional) Run build_html.py to refresh build/html/.
#   2. rsync build/html/ → /var/www/as/.
#   3. Copy the updated Caddyfile to /etc/caddy/Caddyfile and reload Caddy.
#
# Pass --skip-build to skip the build step (use when build/html/ is already
# fresh). Pass --skip-caddy to skip Caddyfile + reload (use when only the
# rendered HTML changed).
#
# Requires sudo for /etc/caddy/ and `systemctl reload caddy`. /var/www/as
# is owned by the ubuntu user (set up at install time), so the rsync into
# it does not need sudo.

set -euo pipefail
cd "$(dirname "$0")"

SKIP_BUILD=0
SKIP_CADDY=0
for arg in "$@"; do
	case "$arg" in
		--skip-build) SKIP_BUILD=1 ;;
		--skip-caddy) SKIP_CADDY=1 ;;
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
rsync -a --delete "$SRC/" "$DST/"

if [ "$SKIP_CADDY" -eq 0 ]; then
	echo ">> Installing Caddyfile + reloading Caddy..."
	sudo install -o root -g caddy -m 640 Caddyfile /etc/caddy/Caddyfile
	sudo systemctl reload caddy
fi

echo ">> Done."
echo "   Local check: curl -sI -u reader:PASSWORD https://secondshanti.org/as/"
