#!/bin/bash

echo "Starting Weekly Banking Simulation"

# Reset System State
cp seed_accounts.txt frontend/accounts.txt
cp seed_master.txt backend/old_master_accounts.txt

for day in {1..7}
do
    echo ""
    echo "===== DAY $day ====="

    ./day.sh sessions/day$day

done

echo ""

echo "Weekly Simulation Complete"