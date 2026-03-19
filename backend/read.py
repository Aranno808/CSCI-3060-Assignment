from print_error import log_constraint_error


def read_old_master_accounts(file_path):
    """Reads and validates the old master bank accounts from the given `file_path`."""
    accounts = []
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file, 1):
            clean_line = line.rstrip("\n")

            # Validate line length (now 44 chars to include plan type)
            if len(clean_line) != 45:
                log_constraint_error(
                    f"Line {line_num}: Invalid length ({len(clean_line)} chars, expected 45)",
                    file_path,
                    fatal=True,
                )
                continue

            try:
                # Extract fields with positional validation
                account_number = clean_line[0:5]
                name = clean_line[6:26].strip()
                status = clean_line[27]
                balance_str = clean_line[29:37]
                transactions_str = clean_line[38:42]
                plan_type = clean_line[43:45]

                if account_number == "00000":
                    return accounts

                # Validate account number
                if not account_number.isdigit():
                    log_constraint_error(
                        f"Line {line_num}: Account number must be 5 digits",
                        file_path,
                        fatal=True,
                    )
                    continue

                # Validate status
                if status not in ("A", "D"):
                    log_constraint_error(
                        f"Line {line_num}: Invalid status '{status}'. Must be 'A' or 'D'",
                        file_path,
                        fatal=True,
                    )
                    continue

                # Validate balance format with explicit negative check
                if balance_str[0] == "-":
                    log_constraint_error(
                        f"Line {line_num}: Negative balance detected: {balance_str}",
                        file_path,
                        fatal=True,
                    )
                    continue

                if (
                    len(balance_str) != 8
                    or balance_str[5] != "."
                    or not balance_str[:5].isdigit()
                    or not balance_str[6:].isdigit()
                ):
                    log_constraint_error(
                        f"Line {line_num}: Invalid balance format. Expected XXXXX.XX, got {balance_str}",
                        file_path,
                        fatal=True,
                    )
                    continue

                # Validate transaction count
                if not transactions_str.isdigit():
                    log_constraint_error(
                        f"Line {line_num}: Transaction count must be 4 digits",
                        file_path,
                        fatal=True,
                    )
                    continue

                # Validate plan type
                if plan_type not in ("SP", "NP"):
                    log_constraint_error(
                        f"Line {line_num}: Invalid plan type '{plan_type}'. Must be SP or NP",
                        file_path,
                        fatal=True,
                    )
                    continue

                # Convert values
                balance = float(balance_str)
                transactions = int(transactions_str)

                # Business rule validation
                if balance < 0:
                    log_constraint_error(
                        f"Line {line_num}: Negative balance detected: {balance}",
                        file_path,
                        fatal=True,
                    )
                    continue
                if transactions < 0:
                    log_constraint_error(
                        f"Line {line_num}: Negative transaction count detected: {transactions}",
                        file_path,
                        fatal=True,
                    )
                    continue

                accounts.append(
                    {
                        "account_number": account_number.lstrip("0") or "0",
                        "name": name.strip(),
                        "status": status,
                        "balance": balance,
                        "total_transactions": transactions,
                        "plan": plan_type,
                    }
                )

            except Exception as e:
                log_constraint_error(
                    f"Line {line_num}: Unexpected error - {str(e)}",
                    file_path,
                    fatal=True,
                )
                continue

    return accounts


def read_transactions(file_path):
    """
    Reads and parses transactions from the given file path. The file contains
    lines in the format:
    CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
    Where:
    - CC is a two digit transaction code
    - AAAAAAAAAAAAAAAAAAAA is the account holder's name
    - NNNNN is the bank account number
    - PPPPPPPP is the amount of funds involved in the transaction
    - MM is any additional miscellaneous information
    """
    transactions = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines, 1):
        if len(line) < 41:
            log_constraint_error(
                f"Line {i}: Invalid transaction line length ({len(line)} chars, expected at least 41)",
                file_path,
                fatal=True,
            )

        transaction_code = line[0:2]
        account_name = line[3:23].strip()
        account_number = line[24:29]
        amount = line[30:38]
        miscellaneous = line[39:].strip()

        # Return once we hit the end of transactions marker "00"
        if transaction_code == "00":
            return transactions

        if transaction_code not in ("01", "02", "03", "04", "05", "06", "07", "08"):
            log_constraint_error(
                f"Line {i}: Invalid transaction code '{transaction_code}'",
                file_path,
                fatal=True,
            )
            continue

        if not account_number.isdigit() or len(account_number) != 5:
            log_constraint_error(
                f"Line {i}: Invalid account number '{account_number}'",
                file_path,
                fatal=True,
            )
            continue
        else:
            account_number = account_number.lstrip("0") or "0"

        if amount[5] != "." or not (amount[:5] + amount[6:]).isdigit():
            log_constraint_error(
                f"Line {i}: Invalid amount format '{amount}'", file_path, fatal=True
            )
            continue
        else:
            amount = float(amount)

        transactions.append(
            {
                "transaction_code": transaction_code,
                "account_name": account_name,
                "account_number": account_number,
                "amount": amount,
                "miscellaneous": miscellaneous,
            }
        )

    return transactions
