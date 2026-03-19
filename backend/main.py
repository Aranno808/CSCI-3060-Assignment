"""
This is the main module for the backend of the banking system. The backend takes the
merged bank account transaction file and the old master bank accounts file as inputs.
It applies the transactions to the accounts and produces two output files: the new
current bank accounts file and the new master bank accounts file.

To run this module, run: `python main.py old_master_accounts.txt merged_transactions.txt new_current_accounts.txt new_master_accounts.txt`
The backend will apply the transactions and produce the required output files.
"""

import argparse

from read import read_old_master_accounts, read_transactions
from write import write_new_current_accounts, write_new_master_accounts
from transactions import apply_transactions


def main():
    """Entry point. Reads the old master accounts and merged transactions,
    applies all transactions, and writes the updated current and master
    account files.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Banking System Back End: Processes daily transactions and updates master records."
    )

    parser.add_argument(
        "old_master_accounts_path", help="Path to the old master bank accounts file"
    )
    parser.add_argument("transactions_path", help="Path to the transactions file")
    parser.add_argument(
        "new_current_accounts_path",
        help="Output path for the new current bank accounts file",
    )
    parser.add_argument(
        "new_master_accounts_path",
        help="Output path for the new master bank accounts file",
    )

    args = parser.parse_args()

    # Read accounts and transactions, then apply transactions to accounts
    accounts = read_old_master_accounts(args.old_master_accounts_path)
    transactions = read_transactions(args.transactions_path)
    apply_transactions(accounts, transactions)

    # Write updated accounts to new current accounts file
    write_new_current_accounts(accounts, args.new_current_accounts_path)
    write_new_master_accounts(accounts, args.new_master_accounts_path)


if __name__ == "__main__":
    main()
