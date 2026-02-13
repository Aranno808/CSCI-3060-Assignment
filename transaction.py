from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from session import Session


class TransactionCode(Enum):
    END = 0
    WITHDRAWAL = 1
    TRANSFER = 2
    PAYBILL = 3
    DEPOSIT = 4
    CREATE = 5
    DELETE = 6
    DISABLE = 7
    CHANGEPLAN = 8


class Transaction:
    def __init__(
        self,
        code: TransactionCode,
        account_holder_name: str,
        account_number: int,
        amount: float,
        miscellaneous: str | float | None = None,
    ):
        self.code = code
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.amount = amount
        self.miscellaneous = miscellaneous


class TransactionHandler:
    def __init__(self, session: "Session"):
        self.session = session

    def withdrawal(
        self, account_holder_name: str, account_number: int, amount: int
    ) -> Transaction:

        if self.session.kind == "standard":
            if account_holder_name != self.session.account_holder_name:
                print(
                    "Bank account must be a valid account for the account holder currently logged in."
                )
                return

            current_total = self.session.transaction_totals[TransactionCode.WITHDRAWAL]
            if current_total + amount > 500:
                print(
                    "Maximum amount that can be withdrawn in current session is $500.00 in standard mode."
                )
                return

        account = self.session.accounts.get(account_number)
        if account is None:
            print(
                "Bank account must be a valid account for the account holder currently logged in."
            )
            return

        new_balance = account.balance - amount
        if new_balance < 0:
            print("Account balance must be at least $0.00 after withdrawal.")
            return

        account.balance = new_balance

        self.session.transaction_totals[TransactionCode.WITHDRAWAL] += amount

        transaction = Transaction(
            TransactionCode.WITHDRAWAL, account_holder_name, account_number, amount
        )
        self.session.transactions.append(transaction)

        return transaction

    def transfer(
        self,
        from_account_holder_name: str,
        from_account_number: int,
        to_account_number: int,
        amount: int,
    ) -> Transaction:

        if self.session.kind == "standard":
            if from_account_holder_name != self.session.account_holder_name:
                print(
                    "Bank account must be a valid account for the account holder currently logged in."
                )
                return

            current_total = self.session.transaction_totals[TransactionCode.TRANSFER]
            if current_total + amount > 1000:
                print(
                    "Maximum amount that can be transferred in current session is $1000.00 in standard mode."
                )
                return

        from_account = self.session.accounts.get(from_account_number)
        if from_account is None:
            print("From account number must be a valid account.")
            return

        to_account = self.session.accounts.get(to_account_number)
        if to_account is None:
            print("Destination account number must be a valid account.")
            return

        from_new_balance = from_account.balance - amount
        to_new_balance = to_account.balance + amount

        if (from_new_balance < 0) or (to_new_balance < 0):
            print(
                "Account balance of both accounts must be at least $0.00 after transfer"
            )
            return

        from_account.balance = from_new_balance
        to_account.balance = to_new_balance

        self.session.transaction_totals[TransactionCode.TRANSFER] += amount

        transaction = Transaction(
            TransactionCode.TRANSFER,
            from_account_holder_name,
            from_account_number,
            amount,
            to_account_number,
        )
        self.session.transactions.append(transaction)

        return transaction

    def paybill(
        self, account_holder_name: str, account_number: int, amount: int, company: str
    ) -> Transaction:
        if self.session.kind == "standard":
            if account_holder_name != self.session.account_holder_name:
                print(
                    "Bank account must be a valid account for the account holder currently logged in."
                )
                return

            current_total = self.session.transaction_totals[TransactionCode.PAYBILL]
            if current_total + amount > 2000:
                print(
                    "Maximum amount that can be paid in current session is $2000.00 in standard mode."
                )
                return

        account = self.session.accounts.get(account_number)
        if account is None:
            print(
                "Bank account must be a valid account for the account holder currently logged in."
            )
            return

        new_balance = account.balance - amount
        if new_balance < 0:
            print("Account balance must be at least $0.00 after payment.")
            return

        account.balance = new_balance

        self.session.transaction_totals[TransactionCode.PAYBILL] += amount

        transaction = Transaction(
            TransactionCode.PAYBILL,
            account_holder_name,
            account_number,
            amount,
            company,
        )
        self.session.transactions.append(transaction)

        return transaction

    def deposit(
        self, account_holder_name: str, account_number: int, amount: int
    ) -> Transaction:
        if self.session.kind == "standard":
            if account_holder_name != self.session.account_holder_name:
                print(
                    "Bank account must be a valid account for the account holder currently logged in."
                )
                return

        account = self.session.accounts.get(account_number)
        if account is None:
            print(
                "Bank account must be a valid account for the account holder currently logged in."
            )
            return

        # Deposited funds should not be available for use in this session
        new_balance = account.balance + amount
        if new_balance < 0:
            print("Account balance must be at least $0.00 after deposit.")
            return

        transaction = Transaction(
            TransactionCode.DEPOSIT,
            account_holder_name,
            account_number,
            amount,
        )
        self.session.transactions.append(transaction)

        return transaction

    def create(self, account_holder_name: str, initial_balance: float) -> Transaction:
        if self.session.kind != "admin":
            print("You must log in as an admin to perform this transaction.")
            return

        # Generate a new, unique account number
        account_number = max(self.session.accounts.keys(), default=10000) + 1

        transaction = Transaction(
            TransactionCode.CREATE,
            account_holder_name,
            account_number,
            initial_balance,
        )
        self.session.transactions.append(transaction)

        return transaction

    def delete(self, account_holder_name: str, account_number: int) -> Transaction:
        if self.session.kind != "admin":
            print("You must log in as an admin to perform this transaction.")
            return

        account = self.session.accounts.get(account_number)
        if account is None:
            print("Account number must be a valid account.")
            return

        if account.account_holder_name != account_holder_name:
            print("Account holder's name must match the account number.")
            return

        # No further transactions should be accepted on a deleted account
        self.session.accounts.pop(account_number)

        transaction = Transaction(
            TransactionCode.DELETE,
            account_holder_name,
            account_number,
            0.0,
        )
        self.session.transactions.append(transaction)

        return transaction

    def disable(self, account_holder_name: str, account_number: int) -> Transaction:
        if self.session.kind != "admin":
            print("You must log in as an admin to perform this transaction.")
            return

        account = self.session.accounts.get(account_number)
        if account is None:
            print("Account number must be a valid account.")
            return

        if account.account_holder_name != account_holder_name:
            print("Account holder's name must match the account number.")
            return

        # No further transactions should be accepted on a disabled account
        account.is_active = False

        transaction = Transaction(
            TransactionCode.DISABLE,
            account_holder_name,
            account_number,
            0.0,
        )
        self.session.transactions.append(transaction)

        return transaction

    def changeplan(self, account_holder_name: str, account_number: int) -> Transaction:
        if self.session.kind != "admin":
            print("You must log in as an admin to perform this transaction.")
            return

        account = self.session.accounts.get(account_number)
        if account is None:
            print("Account number must be a valid account.")
            return

        if account.account_holder_name != account_holder_name:
            print("Account holder's name must match the account number.")
            return

        # Change the account's payment plan to non-student
        account.account_payment_plan = account.account_payment_plan.NON_STUDENT

        transaction = Transaction(
            TransactionCode.CHANGEPLAN,
            account_holder_name,
            account_number,
            0.0,
        )
        self.session.transactions.append(transaction)

        return transaction

    def check_for_admin_privileges(self) -> bool:
        if self.session.kind != "admin":
            print("You must log in as an admin to perform this transaction.")
            return False
        return True
