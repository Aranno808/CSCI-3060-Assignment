from enum import Enum
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
    def __init__(self, session: Session):
        self.session = session

    def handle_withdrawal(
        self, account_holder_name: str, account_number: int, amount: int
    ) -> Transaction:

        if self.session.kind == "standard":
            if account_holder_name != self.session.account_holder_name:
                print(
                    "Bank account must be a valid account for the account holder currently logged in."
                )
                return
            if amount > 500:
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

        transaction = Transaction(
            TransactionCode.WITHDRAWAL, account_holder_name, account_number, amount
        )
        self.session.transactions.append(transaction)

        return transaction

    def handle_transfer(
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
            if amount > 1000:
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

        transaction = Transaction(
            TransactionCode.TRANSFER,
            from_account_holder_name,
            from_account_number,
            amount,
            to_account_number,
        )
        self.session.transactions.append(transaction)

        return transaction

    def check_for_admin_privileges(self) -> bool:
        if self.session.kind != "admin":
            print("You must log in as an admin to perform this transaction.")
            return False
        return True
