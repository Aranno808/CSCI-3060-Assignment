#!/bin/bash

# Daily banking system simulation
# Runs several frontend sessions, merges transactions, then runs backend

echo "Starting Daily Banking Simulation"

# Reset System State
cp seed_accounts.txt frontend/accounts.txt
cp seed_master.txt backend/old_master_accounts.txt

# Input Files
DAY_FOLDER=$1

SESSION_INPUT1="$DAY_FOLDER/session1.txt"
SESSION_INPUT2="$DAY_FOLDER/session2.txt"
SESSION_INPUT3="$DAY_FOLDER/session3.txt"

# Accounts Files
OLD_MASTER="backend/old_master_accounts.txt"
NEW_MASTER="backend/new_master_accounts.txt"
NEW_CURRENT="frontend/accounts.txt"

# Transaction Files
SESSION1="session1_transactions.txt"
SESSION2="session2_transactions.txt"
SESSION3="session3_transactions.txt"

# Merged Transaction File
MERGED_FILE="merged_transactions.txt"

# Run frontend sessions
echo "Running Frontend Session 1..."
python frontend/main.py $NEW_CURRENT $SESSION1 < $SESSION_INPUT1

echo "Running Frontend Session 2..."
python frontend/main.py $NEW_CURRENT $SESSION2 < $SESSION_INPUT2

echo "Running Frontend Session 3..."
python frontend/main.py $NEW_CURRENT $SESSION3 < $SESSION_INPUT3

# Merge transaction files
echo "Merging Transaction Files..."
cat $SESSION1 $SESSION2 $SESSION3 > $MERGED_FILE

# Run backend
echo "Running Backend..."
python backend/main.py $OLD_MASTER $MERGED_FILE $NEW_CURRENT $NEW_MASTER

echo "Daily Processing Complete."