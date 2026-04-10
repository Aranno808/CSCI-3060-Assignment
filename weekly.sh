#!/bin/bash
# weekly.sh - Simulates seven days of Banking System operation.
#
# Calls daily.sh once per day, using sessions/day_1/ through sessions/day_7/
# as the session inputs. The current accounts file output from each day is
# automatically passed as input to the next day.
#
# Usage:
#   ./weekly.sh <initial_current_accounts_file> <initial_master_accounts_file> [output_dir]
#
# Arguments:
#   initial_current_accounts_file - Starting current bank accounts file (Day 1 input)
#   initial_master_accounts_file  - Starting master bank accounts file (Day 1 input)
#   output_dir                    - Directory for daily outputs (default: outputs/weekly)
#
# Session files are read from: sessions/day_1/ ... sessions/day_7/
# To customise a day's transactions, edit the .txt files in the relevant folder.

set -e

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <initial_current_accounts_file> <initial_master_accounts_file> [output_dir]"
    exit 1
fi

INITIAL_CURRENT="$1"
INITIAL_MASTER="$2"
OUTPUT_DIR="${3:-outputs/weekly}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSIONS_ROOT="$SCRIPT_DIR/sessions"

mkdir -p "$OUTPUT_DIR"

CURRENT_ACCOUNTS="$INITIAL_CURRENT"
MASTER_ACCOUNTS="$INITIAL_MASTER"

for DAY in 1 2 3 4 5 6 7; do
    echo "========================================="
    echo "  WEEKLY RUN - DAY $DAY"
    echo "========================================="

    SESSIONS_DIR="$SESSIONS_ROOT/day_${DAY}"
    DAY_OUTPUT_DIR="$OUTPUT_DIR/day_${DAY}"
    mkdir -p "$DAY_OUTPUT_DIR"

    NEW_CURRENT="$DAY_OUTPUT_DIR/current_accounts.txt"
    NEW_MASTER="$DAY_OUTPUT_DIR/master_accounts.txt"

    if [ ! -d "$SESSIONS_DIR" ]; then
        echo "Error: Sessions directory '$SESSIONS_DIR' not found."
        exit 1
    fi

    bash "$SCRIPT_DIR/daily.sh" \
        "$SESSIONS_DIR" \
        "$CURRENT_ACCOUNTS" \
        "$MASTER_ACCOUNTS" \
        "$NEW_CURRENT" \
        "$NEW_MASTER"

    echo "Day $DAY complete."
    echo "  Current accounts -> $NEW_CURRENT"
    echo "  Master accounts  -> $NEW_MASTER"
    echo ""

    # The output of the current day becomes the input for the next day
    CURRENT_ACCOUNTS="$NEW_CURRENT"
    MASTER_ACCOUNTS="$NEW_MASTER"
done

echo "========================================="
echo "  WEEKLY RUN COMPLETE"
echo "========================================="
echo "Final current accounts : $CURRENT_ACCOUNTS"
echo "Final master accounts  : $MASTER_ACCOUNTS"
