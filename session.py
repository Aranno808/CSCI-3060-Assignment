from account import Account, read_accounts
from transaction import Transaction, TransactionCode


class Session:
    """Represents a user session, which can be either an admin session or a standard session for a specific account holder."""

    def __init__(self, kind: str, account_holder_name: str | None = None):
        """Create a new session with the given kind and account holder name (if applicable)."""

        # Validate the session details
        if kind not in {"standard", "admin"}:
            raise ValueError("Invalid session kind. Must be 'admin' or 'standard'.")
        if kind == "standard" and account_holder_name is None:
            raise ValueError(
                "An account holder name must be provided for standard sessions."
            )

        # Initialize the session attributes
        self.kind = kind
        self.account_holder_name = account_holder_name

        # Read in the current bank accounts file
        self.accounts: dict[int, Account] = self.read_accounts()

        # Initialize the transactions list for the session
        self.transactions: list[Transaction] = []

        # Store total amounts for each transaction type for the session
        self.transaction_totals: dict[TransactionCode, float] = {
            TransactionCode.WITHDRAWAL: 0.0,
            TransactionCode.TRANSFER: 0.0,
            TransactionCode.PAYBILL: 0.0,
        }

    def read_accounts(self):
        """Read the accounts from the accounts.txt file and return a dictionary mapping account numbers to Account objects."""
        return read_accounts()

    def write_transactions(self):
        """Write the transactions from the session to the transactions.txt file."""
        with open("transactions.txt", "w") as f:
            for transaction in self.transactions:
                parts = [
                    f"{transaction.code.value:02}",
                    transaction.account_holder_name.ljust(20),
                    f"{transaction.account_number:05}",
                    f"{transaction.amount:.2f}".zfill(8),
                ]

                if transaction.miscellaneous is not None:
                    parts.append(str(transaction.miscellaneous).ljust(2))
                else:
                    parts.append("  ")

                line = " ".join(parts)
                f.write(line + "\n")

            # The sequence of transactions ends with an end of session transaction code
            f.write(
                f"{TransactionCode.END.value:02} {''.ljust(20)} {'00000'} {'00000.00'} {'  '}\n"
            )
