from account import Account, read_accounts


class Session:
    def __init__(self, kind: str, account_holder_name: str | None = None):
        # TODO: Remove this import.
        from transaction import Transaction

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

    def read_accounts(self):
        return read_accounts()

    def write_transactions(self):
        print(NotImplemented)
