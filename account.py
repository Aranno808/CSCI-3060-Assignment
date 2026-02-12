from pathlib import Path

from enum import Enum


class AccountPaymentPlan(Enum):
    STUDENT = "SP"
    NON_STUDENT = "NP"


class Account:
    def __init__(
        self,
        account_holder_name: str,
        account_number: int,
        balance: float,
        is_active: bool = True,
        account_payment_plan: AccountPaymentPlan = AccountPaymentPlan.STUDENT,
    ):
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.balance = balance
        self.is_active = is_active
        self.account_payment_plan = account_payment_plan


def read_accounts() -> dict[int, Account]:
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
