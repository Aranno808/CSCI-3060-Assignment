from session import Session


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

        if command == "login":
            session = handle_login()
        elif command == "logout":
            session = handle_logout(session)


def handle_login():
    # Get the session kind from the user
    while True:
        kind = input("Enter session kind (admin/standard): ").strip().lower()
        if kind not in ["admin", "standard"]:
            print("Invalid session kind. Please enter 'admin' or 'standard'.")
            continue
        else:
            break

    # Get the account holder name if the session kind is admin
    account_holder_name = None
    if kind == "admin":
        while True:
            account_holder_name = input("Enter account holder name: ").strip()
            if not account_holder_name:
                print("Account holder name cannot be empty. Please enter a valid name.")
                continue
            else:
                break

    # Create a new session
    session = Session(kind, account_holder_name)

    return session


def handle_logout(session: Session):
    # Write the current session's transactions to the file
    session.write_transactions()
    return None


if __name__ == "__main__":
    main()
