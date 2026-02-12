class Session:
    def __init__(self, kind: str, account_holder_name: str | None = None):
        # Validate the session details
        if kind not in {"standard", "admin"}:
            raise ValueError("Invalid session kind. Must be 'admin' or 'standard'.")
        if kind == "admin" and account_holder_name is None:
            raise ValueError(
                "An account holder name must be provided for admin sessions."
            )

        # Initialize the session attributes
        self.kind = kind
        self.account_holder_name = account_holder_name

        # Read in the current bank accounts file
        self.read_transactions()

    def read_transactions(self):
        print(NotImplemented)

    def write_transactions(self):
        print(NotImplemented)
