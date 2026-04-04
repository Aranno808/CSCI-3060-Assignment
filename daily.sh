#!/bin/bash

# Daily banking system simulation
# Runs several frontend sessions, merges transactions, then runs backend

# -------- CONFIG --------
FRONTEND=frontend/main.py
BACKEND=backend/main.py

CURRENT_ACCOUNTS=frontend/accounts.txt
OLD_MASTER=backend/old_master_accounts.txt
NEW_MASTER=backend/new_master_accounts.txt
MERGED_FILE=merged_transactions.txt
OUTPUT_FILE="transaction_output.txt"

# Reset System State
cp seed_accounts.txt $CURRENT_ACCOUNTS
cp seed_master.txt $OLD_MASTER

# List of session files
DAY_FOLDER=$1

SESSIONS=("$DAY_FOLDER/session1.txt" "$DAY_FOLDER/session2.txt" "$DAY_FOLDER/session3.txt")

# Clean old merged file
> $MERGED_FILE

echo "Starting Daily Banking Simulation"

# Run Front End for each session
for SESSION in "${SESSIONS[@]}"
do
    echo "Processing $SESSION..."

    python $FRONTEND $CURRENT_ACCOUNTS $OUTPUT_FILE < $SESSION

    # Append to merged file and remove '00' lines
    grep -v '^00' "$OUTPUT_FILE" >> "$MERGED_FILE"
done

# Add terminator line
echo "00                      00000 00000.00  " >> "$MERGED_FILE"

# Run Back end
echo "Running Back End..."

python $BACKEND $OLD_MASTER $MERGED_FILE $CURRENT_ACCOUNTS $NEW_MASTER

echo "Daily Processing Complete."