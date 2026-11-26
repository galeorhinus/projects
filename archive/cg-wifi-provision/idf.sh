#!/bin/bash

# A script to chain idf.py commands based on a single argument.
# e: erase-flash
# b: build
# f: flash
# m: monitor

set -e

# Source the ESP-IDF environment script to set up the correct paths and python environment.
if [ -f "$HOME/esp/esp-idf/export.sh" ]; then
    source "$HOME/esp/esp-idf/export.sh"
fi

if [ -z "$1" ]; then
    echo "Usage: $0 <sequence>"
    echo "  e: erase-flash"
    echo "  b: build"
    echo "  f: flash"
    echo "  m: monitor"
    echo "Example: $0 ebfm"
    exit 1
fi

SEQUENCE=$1
COMMANDS=()

for (( i=0; i<${#SEQUENCE}; i++ )); do
  char="${SEQUENCE:$i:1}"
  case "$char" in
    e) COMMANDS+=("idf.py erase-flash") ;;
    b) COMMANDS+=("idf.py build") ;;
    f) COMMANDS+=("idf.py flash") ;;
    m) COMMANDS+=("idf.py monitor") ;;
    *)
      echo "Error: Unknown command character '$char' in sequence."
      exit 1
      ;;
  esac
done

FULL_COMMAND=$(IFS=' && '; echo "${COMMANDS[*]}")

echo "Executing: $FULL_COMMAND"
eval "$FULL_COMMAND"