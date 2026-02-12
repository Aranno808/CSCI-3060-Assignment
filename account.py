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
    print("Simulating account loading...")
    return {
        10000: Account("Alice", 10000, 1000.00),
        10001: Account("Bob", 10001, 500.00),
        10002: Account("Charlie", 10002, 200.00),
    }
