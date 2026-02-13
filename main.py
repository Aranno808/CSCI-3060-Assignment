from session import Session
from transaction import TransactionHandler


def main():

    session = None

    print("Banking System")
    while True:
        command = input("> ").strip()

        # No transaction other than login should be accepted if there is no active session
        if session is None and command != "login":
            print("Please log in to perform transactions.")
            continue

        # No subsequent login should be accepted if there is already an active session
        if session is not None and command == "login":
            print("You are already logged in. Please log out before logging in again.")
            continue

        transaction_handler = TransactionHandler(session)

        if command == "login":
            session = handle_login()
        elif command == "logout":
            session = handle_logout(session)
        elif command == "withdrawal":
            handle_withdrawal(session, transaction_handler)
        elif command == "transfer":
            handle_transfer(session, transaction_handler)
        elif command == "paybill":
            handle_paybill(session, transaction_handler)
        elif command == "deposit":
            handle_deposit(session, transaction_handler)
        elif command == "create":
            handle_create(session, transaction_handler)
        elif command == "delete":
            handle_delete(session, transaction_handler)
        elif command == "disable":
            handle_disable(session, transaction_handler)
        elif command == "changeplan":
            handle_changeplan(session, transaction_handler)
        else:
            print("Invalid command.")


def handle_login():
    # Get the session kind from the user
    while True:
        kind = get_text("Enter session kind (admin/standard): ")
        if kind not in ["admin", "standard"]:
            print("Invalid session kind. Please enter 'admin' or 'standard'.")
            continue
        else:
            break

    # Get the account holder name if the session kind is standard
    account_holder_name = None
    if kind == "standard":
        account_holder_name = get_text("Enter account holder name: ")

    # Create a new session
    session = Session(kind, account_holder_name)

    return session


def handle_logout(session: Session):
    # Write the current session's transactions to the file
    session.write_transactions()
    return None


def handle_withdrawal(session: Session, transaction_handler: TransactionHandler):
    """Withdraw money from an account."""

    # Ask for the account holder's name, account number, and amount to withdraw
    if session.kind == "admin":
        account_holder_name = input("Enter account holder name: ").strip()
    else:
        account_holder_name = session.account_holder_name

    account_number = get_int("Enter account number: ")

    amount = get_float("Enter amount to withdraw: ")

    transaction_handler.withdrawal(account_holder_name, account_number, amount)


def handle_transfer(session: Session, transaction_handler: TransactionHandler):
    """Transfer money from one account to another."""

    # Ask for the account holder's name (if logged in as admin)
    if session.kind == "admin":
        from_account_holder_name = input("Enter account holder name: ").strip()
    else:
        from_account_holder_name = session.account_holder_name

    # Ask for the account number that the money will be transferred from
    from_account_number = get_int("Enter account number to transfer from: ")

    # Ask for the account number that the money will be transferred to
    to_account_number = get_int("Enter account number to transfer to: ")

    # Ask for the amount to transfer
    amount = get_float("Enter amount to transfer: ")

    transaction_handler.transfer(
        from_account_holder_name, from_account_number, to_account_number, amount
    )


def handle_paybill(session: Session, transaction_handler: TransactionHandler):
    """Pay a bill with money from an account."""

    # Ask for the account holder's name (if logged in as admin)
    if session.kind == "admin":
        account_holder_name = get_text("Enter account holder name: ")
    else:
        account_holder_name = session.account_holder_name

    # Ask for the account number
    account_number = get_int("Enter account number: ")

    # Ask for the company to whom the bill is being paid
    company = get_text("Enter company name: ")
    if company not in {
        "The Bright Light Electric Company (EC)",
        "Credit Card Company Q (CQ)",
        "Fast Internet, Inc. (FI)",
    }:
        print("Invalid company name. Please enter a valid company name.")
        return

    # Ask for the amount to pay
    amount = get_float("Enter amount to pay: ")

    transaction_handler.paybill(account_holder_name, account_number, amount, company)


def handle_deposit(session: Session, transaction_handler: TransactionHandler):
    """Deposit money into an account."""

    # Ask for the account holder's name (if logged in as admin)
    if session.kind == "admin":
        account_holder_name = get_text("Enter account holder name: ")
    else:
        account_holder_name = session.account_holder_name

    # Ask for the account number
    account_number = get_int("Enter account number: ")

    # Ask for the amount to deposit
    amount = get_float("Enter amount to deposit: ")

    transaction_handler.deposit(account_holder_name, account_number, amount)


def handle_create(session: Session, transaction_handler: TransactionHandler):
    """Create a new account."""

    # Ask for the account holder's name
    account_holder_name = get_text("Enter account holder name: ")

    # Ask for the initial balance
    initial_balance = get_float("Enter initial balance: ")

    transaction_handler.create(account_holder_name, initial_balance)


def handle_delete(session: Session, transaction_handler: TransactionHandler):
    """Delete an account."""

    # Ask for the account holder's name
    account_holder_name = get_text("Enter account holder name: ")

    # Ask for the account number
    account_number = get_int("Enter account number: ")

    transaction_handler.delete(account_holder_name, account_number)


def handle_disable(session: Session, transaction_handler: TransactionHandler):
    """Disable an account."""

    # Ask for the account holder's name
    account_holder_name = get_text("Enter account holder name: ")

    # Ask for the account number
    account_number = get_int("Enter account number: ")

    transaction_handler.disable(account_holder_name, account_number)


def handle_changeplan(session: Session, transaction_handler: TransactionHandler):
    """Change the payment plan of an account."""

    # Ask for the account holder's name
    account_holder_name = get_text("Enter account holder name: ")

    # Ask for the account number
    account_number = get_int("Enter account number: ")

    transaction_handler.changeplan(account_holder_name, account_number)


def get_text(prompt: str) -> str:
    while True:
        text = input(prompt).strip()
        if text:
            return text


def get_int(prompt: str) -> int:
    while True:
        text = input(prompt).strip()
        if text.isdigit():
            return int(text)
        else:
            print("Please enter a valid integer.")


def get_float(prompt: str) -> float:
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
