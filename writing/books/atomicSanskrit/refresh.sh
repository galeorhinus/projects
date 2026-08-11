#!/bin/bash
set -e
git pull --ff-only
./build_html.sh
./deploy.sh
echo "✓ Refreshed at $(date)"

