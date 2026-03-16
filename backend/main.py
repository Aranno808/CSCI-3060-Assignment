import argparse

from read import read_old_master_accounts, read_transactions
from write import write_new_current_accounts, write_new_master_accounts
from transactions import apply_transactions


def main():

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
