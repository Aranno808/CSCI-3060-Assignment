from print_error import log_constraint_error


def write_new_current_accounts(accounts, file_path):
    """
    Writes the new current bank accounts file with strict validation in the format:
    NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP_TT
    Where:
    - NNNNN is the bank account number
    - AAAAAAAAAAAAAAAAAAAA is the account holder's name
    - S is the account status - active (A) or disabled (D)
    - PPPPPPPP is the current balance of the account (in Canadian dollars)
    - TT is the account plan type (SP or NP)
    - _ is a space

    Note: As mentioned in the course Discord, we have included the account plan type
    in the current accounts file.
    """
    with open(file_path, "w") as file:
        for acc in accounts:
            # Validate account number
            if (
                not isinstance(acc["account_number"], str)
                or not acc["account_number"].isdigit()
            ):
                log_constraint_error(
                    f"Account number must be numeric string, got {acc['account_number']}",
                    file_path,
                    fatal=True,
                )
            if len(acc["account_number"]) > 5:
                log_constraint_error(
                    f"Account number exceeds 5 digits: {acc['account_number']}",
                    file_path,
                    fatal=True,
                )

            # Validate name
            if len(acc["name"]) > 20:
                log_constraint_error(
                    f"Account name exceeds 20 characters: {acc['name']}",
                    file_path,
                    fatal=True,
                )

            # Validate status
            if acc["status"] not in ("A", "D"):
                log_constraint_error(
                    f"Invalid status '{acc['status']}'. Must be 'A' or 'D'",
                    file_path,
                    fatal=True,
                )

            # Validate balance with explicit negative check
            if not isinstance(acc["balance"], (int, float)):
                log_constraint_error(
                    f"Balance must be numeric, got {type(acc['balance'])}",
                    file_path,
                    fatal=True,
                )
            if acc["balance"] < 0:
                log_constraint_error(
                    f"Negative balance detected: {acc['balance']}",
                    file_path,
                    fatal=True,
                )
            if acc["balance"] > 99999.99:
                log_constraint_error(
                    f"Balance exceeds maximum $99999.99: {acc['balance']}",
                    file_path,
                    fatal=True,
                )

            # Validate plan type
            plan = acc.get("plan", "NP")
            if plan not in ("SP", "NP"):
                log_constraint_error(
                    f"Invalid plan type '{plan}'. Must be SP or NP",
                    file_path,
                    fatal=True,
                )

            # Format fields
            acc_num = acc["account_number"].zfill(5)
            name = acc["name"].ljust(20)[:20]
            balance = f"{acc['balance']:08.2f}"

            # Write line (37 chars + plan type = 39 chars total)
            file.write(f"{acc_num} {name} {acc['status']} {balance} {plan}\n")

        # Add END_OF_FILE marker
        file.write("00000 END_OF_FILE          A 00000.00 NP\n")


def write_new_master_accounts(accounts, file_path):
    """
    Writes a new master accounts file with multiple lines of format:
    NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP_TTTT_XX
    Where:
    - NNNNN is the bank account number
    - AAAAAAAAAAAAAAAAAAAA is the account holder's name
    - S is the account status - active (A) or disabled (D)
    - PPPPPPPP is the current balance of the account (in Canadian dollars)
    - TTTT is the total number of transactions
    - XX is the account plan type (SP or NP)
    - _ is a space

    Note: As mentioned in the course Discord, we have included the account plan
    type in the master accounts file.
    """
    # The master bank accounts must be sorted by account number
    accounts = sorted(accounts, key=lambda x: x["account_number"])

    with open(file_path, "w") as f:
        for account in accounts:
            # Validate the account number
            if (
                not isinstance(account["account_number"], str)
                or not account["account_number"].isdigit()
            ):
                log_constraint_error(
                    f"Account number must be a numeric string, got {account['account_number']}",
                    file_path,
                    fatal=True,
                )
            if len(account["account_number"]) > 5:
                log_constraint_error(
                    f"Account number must be exactly 5 digits, got {account['account_number']}",
                    file_path,
                    fatal=True,
                )

            # Validate the name
            if not isinstance(account["name"], str):
                log_constraint_error(
                    f"Account name must be a string, got {type(account['name'])}",
                    file_path,
                    fatal=True,
                )
            if len(account["name"]) > 20:
                log_constraint_error(
                    f"Account name must be at most 20 characters, got {account['name']}",
                    file_path,
                    fatal=True,
                )

            # Validate the status
            if account["status"] not in ("A", "D"):
                log_constraint_error(
                    f"Invalid status '{account['status']}'. Must be 'A' or 'D'",
                    file_path,
                    fatal=True,
                )

            # Validate the balance
            if not isinstance(account["balance"], (int, float)):
                log_constraint_error(
                    f"Balance must be numeric, got {type(account['balance'])}",
                    file_path,
                    fatal=True,
                )
            if account["balance"] < 0:
                log_constraint_error(
                    f"Negative balance detected: {account['balance']}",
                    file_path,
                    fatal=True,
                )
            if account["balance"] > 99999.99:
                log_constraint_error(
                    f"Balance exceeds maximum $99999.99: {account['balance']}",
                    file_path,
                    fatal=True,
                )

            # Validate the total transactions
            if (
                not isinstance(account["total_transactions"], int)
                or account["total_transactions"] < 0
            ):
                log_constraint_error(
                    f"Total transactions must be a non-negative integer, got {account['total_transactions']}",
                    file_path,
                    fatal=True,
                )
            if account["total_transactions"] > 9999:
                log_constraint_error(
                    f"Total transactions exceeds maximum 9999: {account['total_transactions']}",
                    file_path,
                    fatal=True,
                )

            line = (
                f"{account['account_number'].zfill(5)} "
                f"{account['name'].ljust(20)} "
                f"{account['status']} "
                f"{account['balance']:08.2f} "
                f"{str(account['total_transactions']).zfill(4)} "
                f"{account['plan']}"
            )
            f.write(line + "\n")

        f.write("00000 END_OF_FILE          A 00000.00 0000 NP\n")
