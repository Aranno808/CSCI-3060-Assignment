# UML Class Diagram

This diagram uses Mermaid so it can render directly on GitHub.

Conventions used here:

* `<<module>>` represents a Python module with module-level functions.
* `<<record>>` represents the dictionary-shaped backend records used in code.
* `<<enumeration>>` represents an enum.

```mermaid
classDiagram
direction LR

namespace Frontend {
    class FrontendMain {
        <<module>>
        +main()
        +handle_login(accounts_file, transaction_output_file) Session
        +handle_logout(session)
        +handle_withdrawal(session, transaction_handler)
        +handle_transfer(session, transaction_handler)
        +handle_paybill(session, transaction_handler)
        +handle_deposit(session, transaction_handler)
        +handle_create(session, transaction_handler)
        +handle_delete(session, transaction_handler)
        +handle_disable(session, transaction_handler)
        +handle_changeplan(session, transaction_handler)
        +get_text(prompt) str
        +get_int(prompt) int
        +get_float(prompt) float
        +_print_newline_if_not_tty()
    }

    class FrontendAccountIO {
        <<module>>
        +read_accounts(filename) dict
        +write_accounts(accounts, filename)
    }

    class AccountPaymentPlan {
        <<enumeration>>
        STUDENT
        NON_STUDENT
    }

    class Account {
        +account_holder_name: str
        +account_number: int
        +balance: float
        +is_active: bool
        +account_payment_plan: AccountPaymentPlan
        +is_new: bool
        +__init__(account_holder_name, account_number, balance, is_active, account_payment_plan, is_new)
        +available_for_use: bool
    }

    class Session {
        +kind: str
        +account_holder_name: optional str
        +accounts_file: str
        +transaction_output_file: str
        +accounts: dict
        +transactions: list
        +transaction_totals: dict
        +__init__(kind, account_holder_name, accounts_file, transaction_output_file)
        +read_accounts()
        +write_transactions()
    }

    class TransactionCode {
        <<enumeration>>
        END
        WITHDRAWAL
        TRANSFER
        PAYBILL
        DEPOSIT
        CREATE
        DELETE
        DISABLE
        CHANGEPLAN
    }

    class Transaction {
        +code: TransactionCode
        +account_holder_name: str
        +account_number: int
        +amount: float
        +miscellaneous: optional value
        +__init__(code, account_holder_name, account_number, amount, miscellaneous)
    }

    class TransactionHandler {
        +session: Session
        +__init__(session)
        +withdrawal(account_holder_name, account_number, amount) Transaction
        +transfer(from_account_holder_name, from_account_number, to_account_number, amount) Transaction
        +paybill(account_holder_name, account_number, amount, company) Transaction
        +deposit(account_holder_name, account_number, amount) Transaction
        +create(account_holder_name, initial_balance) Transaction
        +delete(account_holder_name, account_number) Transaction
        +disable(account_holder_name, account_number) Transaction
        +changeplan(account_holder_name, account_number) Transaction
    }
}

namespace Backend {
    class BackendMain {
        <<module>>
        +main()
    }

    class BackendRead {
        <<module>>
        +read_old_master_accounts(file_path) list
        +read_transactions(file_path) list
    }

    class BackendWrite {
        <<module>>
        +write_new_current_accounts(accounts, file_path)
        +write_new_master_accounts(accounts, file_path)
    }

    class ErrorLogger {
        <<module>>
        +log_constraint_error(description, context, fatal=False)
    }

    class BackendTransactionCode {
        <<enumeration>>
        WITHDRAWAL
        TRANSFER
        PAYBILL
        DEPOSIT
        CREATE
        DELETE
        DISABLE
        CHANGEPLAN
    }

    class BackendAccountRecord {
        <<record>>
        +account_number: str
        +name: str
        +status: str
        +balance: float
        +total_transactions: int
        +plan: str
    }

    class BackendTransactionRecord {
        <<record>>
        +transaction_code: str
        +account_name: str
        +account_number: str
        +amount: float
        +miscellaneous: str
    }

    class BackendTransactions {
        <<module>>
        +apply_transactions(accounts, transactions)
        +handle_withdrawal(accounts, account_number, amount)
        +handle_transfer(accounts, from_account_number, to_account_number, amount)
        +handle_paybill(accounts, account_number, amount)
        +handle_deposit(accounts, account_number, amount)
        +handle_create(accounts, account_number, account_name, amount)
        +handle_changeplan(accounts, account_number)
        +handle_delete(accounts, account_number)
        +handle_disable(accounts, account_number)
        +get_account(accounts, account_number)
        +increment_transaction_count(account)
        +get_transaction_cost(account)
        +validate_balance(account_number, balance)
    }
}

FrontendMain ..> Session : creates / uses
FrontendMain ..> TransactionHandler : delegates commands
Session --> FrontendAccountIO : loads accounts
Session *-- "0..*" Account : owns
Session *-- "0..*" Transaction : stores
Session --> TransactionCode : totals keyed by
Account --> AccountPaymentPlan : uses
Transaction --> TransactionCode : uses
TransactionHandler --> Session : validates against
TransactionHandler --> Account : mutates
TransactionHandler --> Transaction : creates
TransactionHandler --> AccountPaymentPlan : changes plan

BackendMain ..> BackendRead : reads input
BackendMain ..> BackendTransactions : applies updates
BackendMain ..> BackendWrite : writes output
BackendRead ..> ErrorLogger : reports fatal issues
BackendTransactions ..> ErrorLogger : reports rule violations
BackendWrite ..> ErrorLogger : validates output
BackendRead --> BackendAccountRecord : builds
BackendRead --> BackendTransactionRecord : builds
BackendTransactions --> BackendAccountRecord : mutates
BackendTransactions --> BackendTransactionRecord : consumes
BackendTransactions --> BackendTransactionCode : dispatches by code
BackendWrite --> BackendAccountRecord : serializes
```
