from pathlib import Path

from enum import Enum


class AccountPaymentPlan(Enum):
    STUDENT = "SP"
    NON_STUDENT = "NP"


class Account:
    """Represents a bank account with a holder name, account number, balance, active status, and payment plan."""

    def __init__(
        self,
        account_holder_name: str,
        account_number: int,
        balance: float,
        is_active: bool = True,
        account_payment_plan: AccountPaymentPlan = AccountPaymentPlan.STUDENT,
    ):
        """Create a new account with the given holder name, account number, balance, status, and payment plan."""
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.balance = balance
        self.is_active = is_active
        self.account_payment_plan = account_payment_plan


def read_accounts() -> dict[int, Account]:
    """Load the accounts from the accounts.txt file and return a dictionary mapping account numbers to Account objects."""
    accounts = dict()

    filename = "accounts.txt"
    if not Path(filename).exists():
        return accounts

    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue

            account_holder_name = line[6:26].strip()
            if account_holder_name == "END_OF_FILE":
                break

            account_number = int(line[0:5])

            status = line[27]
            is_active = status == "A"

            balance = float(line[29:37])

            accounts[account_number] = Account(
                account_holder_name, account_number, balance, is_active
            )

    return accounts


def write_accounts(accounts: dict[int, Account]):
    """
    Write to the accounts.txt file and store a dictionary mapping account values to `Account` objects.

    NOTE: This is just for reference as accounts.txt should only be written by the backend application.
    """
    filename = "accounts.txt"
    with open(filename, "w") as f:
        for account in accounts.values():
            status = "A" if account.is_active else "D"
            balance = f"{account.balance:.2f}".zfill(8)
            line = (
                f"{account.account_number:05} "
                f"{account.account_holder_name.ljust(20)} "
                f"{status} "
                f"{balance}"
            )
            f.write(line + "\n")

        f.write("00000 END_OF_FILE           A 00000.00\n")
