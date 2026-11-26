#!/usr/bin/env bash
set -euo pipefail

# Usage: tools/config_target.sh [chip] [flash_size] [partition_file]
# Defaults to esp32 @ 4MB using partitions/esp32_4MB_ota.csv

chip="${1:-esp32}"
flash="${2:-4MB}"
partition_file="${3:-}"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ptable_dir="${repo_root}/partitions"

if [[ -z "${partition_file}" ]]; then
  partition_file="${ptable_dir}/${chip}_${flash}_ota.csv"
fi

if [[ ! -f "${partition_file}" ]]; then
  echo "Partition file not found: ${partition_file}" >&2
  echo "Create one under ${ptable_dir} or pass an explicit path." >&2
  exit 1
fi

echo "Setting target=${chip}, flash=${flash}"
echo "Using partition table: ${partition_file}"

# Copy chosen partition table into the root partitions.csv the build expects
cp "${partition_file}" "${repo_root}/partitions.csv"

# Ensure IDF picks the right target and flash size
export IDF_TARGET="${chip}"
idf.py set-target "${chip}"
idf.py reconfigure -D ESPTOOLPY_FLASHSIZE="${flash}"

echo "Done. Now run: idf.py build flash (or idf.py build && idf.py -p <port> flash)"
