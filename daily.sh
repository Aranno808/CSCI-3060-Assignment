#!/bin/bash
# daily.sh - Simulates one day of Banking System operation.
#
# Runs the Front End once per session file in a given sessions directory,
# merges all resulting transaction files, then runs the Back End.
#
# Usage:
#   ./daily.sh <sessions_dir> <current_accounts_file> <old_master_accounts_file> \
#              [new_current_accounts_file] [new_master_accounts_file]
#
# Arguments:
#   sessions_dir              - Directory containing session input .txt files.
#                               Each .txt file is fed to the Front End as one session.
#                               Files are processed in alphabetical order.
#   current_accounts_file     - Current bank accounts file (input to Front End)
#   old_master_accounts_file  - Old master bank accounts file (input to Back End)
#   new_current_accounts_file - Output path for new current accounts file (default: outputs/daily/current_accounts.txt)
#   new_master_accounts_file  - Output path for new master accounts file  (default: outputs/daily/master_accounts.txt)

set -e

if [ "$#" -lt 3 ] || [ "$#" -gt 5 ]; then
    echo "Usage: $0 <sessions_dir> <current_accounts_file> <old_master_accounts_file> [new_current_accounts_file] [new_master_accounts_file]"
    exit 1
fi

SESSIONS_DIR="$1"
CURRENT_ACCOUNTS="$2"
OLD_MASTER="$3"
NEW_CURRENT="${4:-outputs/daily/current_accounts.txt}"
NEW_MASTER="${5:-outputs/daily/master_accounts.txt}"

if [ ! -d "$SESSIONS_DIR" ]; then
    echo "Error: Sessions directory '$SESSIONS_DIR' does not exist."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
BACKEND_DIR="$SCRIPT_DIR/backend"

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

MERGED_TRANSACTIONS="$TEMP_DIR/merged_transactions.txt"
SESSION_NUM=0

# (i) Run the Front End for each session file in the sessions directory
for SESSION_FILE in $(ls "$SESSIONS_DIR"/*.txt 2>/dev/null | sort); do
    SESSION_NUM=$((SESSION_NUM + 1))
    SESSION_TXN_FILE="$TEMP_DIR/session_${SESSION_NUM}.txt"

    echo "--- Running Front End session $SESSION_NUM: $(basename "$SESSION_FILE") ---"
    python3 "$FRONTEND_DIR/main.py" "$CURRENT_ACCOUNTS" "$SESSION_TXN_FILE" < "$SESSION_FILE"
    echo "Session $SESSION_NUM complete."
done

if [ "$SESSION_NUM" -eq 0 ]; then
    echo "Error: No session files found in '$SESSIONS_DIR'."
    exit 1
fi

# (ii) Concatenate all session transaction files into the Merged Daily Bank Account Transaction File
echo "--- Merging $SESSION_NUM transaction file(s) ---"
> "$MERGED_TRANSACTIONS"
for i in $(seq 1 $SESSION_NUM); do
    cat "$TEMP_DIR/session_${i}.txt" >> "$MERGED_TRANSACTIONS"
done

# (iii) Run the Back End with the merged transaction file
mkdir -p "$(dirname "$NEW_CURRENT")"
mkdir -p "$(dirname "$NEW_MASTER")"

echo "--- Running Back End ---"
python3 "$BACKEND_DIR/main.py" "$OLD_MASTER" "$MERGED_TRANSACTIONS" "$NEW_CURRENT" "$NEW_MASTER"

echo "--- Daily run complete ---"
echo "  New current accounts : $NEW_CURRENT"
echo "  New master accounts  : $NEW_MASTER"
