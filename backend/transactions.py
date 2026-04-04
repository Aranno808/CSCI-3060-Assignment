from enum import Enum

from print_error import log_constraint_error


class TransactionCode(Enum):
    """Represents the different types of transactions that can be performed in the banking system."""

    WITHDRAWAL = "01"
    TRANSFER = "02"
    PAYBILL = "03"
    DEPOSIT = "04"
    CREATE = "05"
    DELETE = "06"
    DISABLE = "07"
    CHANGEPLAN = "08"


def apply_transactions(accounts, transactions):
    """Applies transactions to accounts and returns the updated accounts list"""

    for transaction in transactions:
        transaction_code = transaction["transaction_code"]
        account_name = transaction["account_name"]
        account_number = transaction["account_number"]
        amount = transaction["amount"]
        miscellaneous = transaction["miscellaneous"]

        if transaction_code == TransactionCode.WITHDRAWAL.value:
            handle_withdrawal(accounts, account_number, amount)
        elif transaction_code == TransactionCode.TRANSFER.value:
            handle_transfer(
                accounts, account_number, miscellaneous, amount
            )
        elif transaction_code == TransactionCode.PAYBILL.value:
            handle_paybill(accounts, account_number, amount)
        elif transaction_code == TransactionCode.DEPOSIT.value:
            handle_deposit(accounts, account_number, amount)
        elif transaction_code == TransactionCode.CREATE.value:
            handle_create(accounts, account_number, account_name, amount)
        elif transaction_code == TransactionCode.DELETE.value:
            handle_delete(accounts, account_number)
        elif transaction_code == TransactionCode.DISABLE.value:
            handle_disable(accounts, account_number)
        elif transaction_code == TransactionCode.CHANGEPLAN.value:
            handle_changeplan(accounts, account_number)
        else:
            # This should never happen due to prior validation, but we can log an error if it does
            log_constraint_error(
                f"Invalid transaction code '{transaction_code}' in apply_transactions",
                "apply_transactions",
                fatal=False,
            )


def handle_withdrawal(accounts, account_number, amount):
    """Handles withdrawal transactions and updates the account balance accordingly."""
    # Get the account for the transaction and log an error if it doesn't exist
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for withdrawal transaction",
            f"{TransactionCode.WITHDRAWAL.name} {account_number} {amount}",
            fatal=False,
        )
        return

    # Calculate the new balance after the transaction
    transaction_cost = get_transaction_cost(account)
    new_balance = account["balance"] - (amount + transaction_cost)

    # Ensure the new balance is valid and log an error if it isn't
    if not validate_balance(account_number, new_balance):
        log_constraint_error(
            f"Invalid balance after withdrawal transaction for account '{account_number}': {new_balance}",
            f"{TransactionCode.WITHDRAWAL.name} {account_number} {amount}",
            fatal=False,
        )
        return

    # Update the account and the transaction count
    account["balance"] = new_balance
    increment_transaction_count(account)


def handle_transfer(accounts, from_account_number, to_account_number, amount):
    """Handles transfer transactions and updates account balances accordingly."""
    # Get the accounts for the transaction and log an error if either doesn't exist
    from_account = get_account(accounts, from_account_number)
    if from_account is None:
        log_constraint_error(
            f"From account number '{from_account_number}' not found for transfer transaction",
            f"{TransactionCode.TRANSFER.name} {from_account_number} {to_account_number} {amount}",
            fatal=False,
        )
        return

    to_account = get_account(accounts, to_account_number)
    if to_account is None:
        log_constraint_error(
            f"To account number '{to_account_number}' not found for transfer transaction",
            f"{TransactionCode.TRANSFER.name} {from_account_number} {to_account_number} {amount}",
            fatal=False,
        )
        return

    # Calculate the new balances after the transaction and log an error if either is invalid
    transaction_cost = get_transaction_cost(from_account)

    from_account_new_balance = from_account["balance"] - (amount + transaction_cost)
    if not validate_balance(from_account_number, from_account_new_balance):
        log_constraint_error(
            f"Invalid balance after transfer transaction for from account '{from_account_number}': {from_account_new_balance}",
            f"{TransactionCode.TRANSFER.name} {from_account_number} {to_account_number} {amount}",
            fatal=False,
        )
        return
    

    to_account_new_balance = to_account["balance"] + amount
    if not validate_balance(to_account_number, to_account_new_balance):
        log_constraint_error(
            f"Invalid balance after transfer transaction for to account '{to_account_number}': {to_account_new_balance}",
            f"{TransactionCode.TRANSFER.name} {from_account_number} {to_account_number} {amount}",
            fatal=False,
        )
        return
    
    # Update the accounts and the transaction count for the from account
    from_account["balance"] = from_account_new_balance
    to_account["balance"] = to_account_new_balance
    increment_transaction_count(from_account)


def handle_paybill(accounts, account_number, amount):
    """Handles paybill transactions and updates the account balance accordingly."""
    # Get the account for the transaction and log an error if it doesn't exist
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for paybill transaction",
            f"{TransactionCode.PAYBILL.name} {account_number} {amount}",
            fatal=False,
        )
        return


    # Calculate the new balance after the transaction
    transaction_cost = get_transaction_cost(account)
    new_balance = account["balance"] - (amount + transaction_cost)

    # Ensure the new balance is valid and log an error if it isn't
    if not validate_balance(account_number, new_balance):
        log_constraint_error(
            f"Invalid balance after paybill transaction for account '{account_number}': {new_balance}",
            f"{TransactionCode.PAYBILL.name} {account_number} {amount}",
            fatal=False,
        )
        return

    # Update the account and the transaction count
    account["balance"] = new_balance
    increment_transaction_count(account)



def handle_deposit(accounts, account_number, amount):
    """Handles deposit transactions and updates the account balance accordingly."""
    # Get the account for the transaction and log an error if it doesn't exist
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for deposit transaction",
            f"{TransactionCode.DEPOSIT.name} {account_number} {amount}",
            fatal=False,
        )
        return


    # Calculate the new balance after the transaction
    transaction_cost = get_transaction_cost(account)
    new_balance = account["balance"] + amount - transaction_cost

    # Ensure the new balance is valid and log an error if it isn't
    if not validate_balance(account_number, new_balance):
        log_constraint_error(
            f"Invalid balance after deposit transaction for account '{account_number}': {new_balance}",
            f"{TransactionCode.DEPOSIT.name} {account_number} {amount}",
            fatal=False,
        )
        return
    
    # Update the account and the transaction count
    account["balance"] = new_balance
    increment_transaction_count(account)



def handle_create(accounts, account_number, account_name, amount):
    """Handles create transactions and adds a new account to the accounts list."""
    # A newly created account must have a unique account number
    if get_account(accounts, account_number) is not None:
        log_constraint_error(
            f"Account number '{account_number}' already exists for create transaction",
            f"{TransactionCode.CREATE.name} {account_number} {account_name} {amount}",
            fatal=False,
        )
        return

    # Create a new account and add it to the accounts list
    account = {
        "account_number": account_number,
        "name": account_name,
        "status": "A",
        "balance": amount,
        "total_transactions": 0,
        "plan": "SP",
    }
    accounts.append(account)


def handle_changeplan(accounts, account_number):
    """Handles change plan transactions and updates the account plan type."""
    # Get the account for the transaction and log an error if it doesn't exist
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for change plan transaction",
            f"{TransactionCode.CHANGEPLAN.name} {account_number}",
            fatal=False,
        )
        return

    # Calculate the new balance after the transaction
    transaction_cost = get_transaction_cost(account)
    new_balance = account["balance"] - transaction_cost

    # Ensure the new balance is valid and log an error if it isn't
    if not validate_balance(account_number, new_balance):
        log_constraint_error(
            f"Invalid balance after change plan transaction for account '{account_number}': {new_balance}",
            f"{TransactionCode.CHANGEPLAN.name} {account_number}",
            fatal=False,
        )
        return

    # Update the account and the transaction count
    account["plan"] = "NP"
    account["balance"] = new_balance
    increment_transaction_count(account)


def handle_delete(accounts, account_number):
    """Handles delete transactions and removes an account from the accounts list."""
    # Get the account for the transaction and log an error if it doesn't exist
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for delete transaction",
            f"{TransactionCode.DELETE.name} {account_number}",
            fatal=False,
        )
        return

    # Remove the account from the accounts list
    accounts.remove(account)


def handle_disable(accounts, account_number):
    """Handles disable transactions and updates the account status to 'D'."""
    # Get the account for the transaction and log an error if it doesn't exist
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for disable transaction",
            f"{TransactionCode.DISABLE.name} {account_number}",
            fatal=False,
        )
        return

    # Calculate the new balance after the transaction
    transaction_cost = get_transaction_cost(account)
    new_balance = account["balance"] - transaction_cost

    # Ensure the new balance is valid and log an error if it isn't
    if not validate_balance(account_number, new_balance):
        log_constraint_error(
            f"Invalid balance after disable transaction for account '{account_number}': {new_balance}",
            f"{TransactionCode.DISABLE.name} {account_number}",
            fatal=False,
        )
        return

    # Update the account and the transaction count
    account["status"] = "D"
    account["balance"] = new_balance
    increment_transaction_count(account)


def get_account(accounts, account_number) -> dict | None:
    """Helper function to retrieve an account by account number."""
    for account in accounts:
        if account["account_number"] == account_number:
            return account
    return None


def increment_transaction_count(account):
    """Increments the total transaction count for an account."""
    account["total_transactions"] += 1


def get_transaction_cost(account):
    """Returns the transaction cost for an account based on its plan type."""
    if account["plan"] == "SP":
        return 0.05
    else:
        return 0.10


def validate_balance(account_number, balance):
    """Validates that the balance is within the allowed range and logs an error if not."""
    # No bank account should ever have a negative balance
    if balance < 0:
        return False
    # No bank account should ever have a balance greater than $99,999.99
    if balance > 99999.99:
        return False
    return True
