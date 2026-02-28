#!/usr/bin/env bash
# CSCI 3060U Phase 3 - Automated Test Runner and Validator
set -euo pipefail

ACCOUNTS_FILE="accounts.txt"
EXPECTED_DIR="expected"
mkdir -p outputs

shopt -s nullglob
inputs=(inputs/*.txt)

for infile in "${inputs[@]}"; do
  base=$(basename "$infile" .txt)
  echo "-----------------------------------"
  echo "Running Test: $base"

  # Run program
  python main.py "$ACCOUNTS_FILE" "outputs/${base}.atf" < "$infile" > "outputs/${base}.out"

  # Validate transactions
  echo "Checking Transaction File..."
  if diff "outputs/${base}.atf" "$EXPECTED_DIR/${base}.etf" > /dev/null; then
    echo "  [PASS] Transactions match."
  else
    echo "  [FAIL] Transactions differ!"
  fi

  # Validate terminal log
  echo "Checking Terminal Log..."
  if diff "outputs/${base}.out" "$EXPECTED_DIR/${base}.out" > /dev/null; then
    echo "  [PASS] Terminal output matches."
  else
    echo "  [FAIL] Terminal output differs!"
  fi
done

echo "-----------------------------------"
echo "Testing Complete. Check results and update your Failure Table."