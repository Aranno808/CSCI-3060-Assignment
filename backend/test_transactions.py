import pytest
from unittest.mock import patch

from transactions import apply_transactions, TransactionCode


# TC1: Empty list (0 iterations)
def test_apply_transactions_empty():
    accounts = {}
    apply_transactions(accounts, [])
    assert accounts == {}


# TC2: Withdrawal branch
@patch("transactions.handle_withdrawal")
def test_apply_transactions_withdrawal(mock_withdrawal):
    transactions = [
        {
            "transaction_code": TransactionCode.WITHDRAWAL.value,
            "account_name": "A",
            "account_number": "123",
            "amount": 100,
            "miscellaneous": "",
        }
    ]

    apply_transactions({}, transactions)

    mock_withdrawal.assert_called_once()


# TC3: All valid branches
@patch("transactions.handle_withdrawal")
@patch("transactions.handle_transfer")
@patch("transactions.handle_paybill")
@patch("transactions.handle_deposit")
@patch("transactions.handle_create")
@patch("transactions.handle_delete")
@patch("transactions.handle_disable")
@patch("transactions.handle_changeplan")
def test_apply_transactions_all_branches(
    mock_changeplan,
    mock_disable,
    mock_delete,
    mock_create,
    mock_deposit,
    mock_paybill,
    mock_transfer,
    mock_withdrawal,
):
    transactions = [
        {"transaction_code": TransactionCode.DEPOSIT.value, "account_name": "A", "account_number": "1", "amount": 10, "miscellaneous": ""},
        {"transaction_code": TransactionCode.TRANSFER.value, "account_name": "A", "account_number": "1", "amount": 10, "miscellaneous": "002"},
        {"transaction_code": TransactionCode.PAYBILL.value, "account_name": "A", "account_number": "1", "amount": 10, "miscellaneous": ""},
        {"transaction_code": TransactionCode.CREATE.value, "account_name": "A", "account_number": "1", "amount": 10, "miscellaneous": ""},
        {"transaction_code": TransactionCode.DELETE.value, "account_name": "A", "account_number": "1", "amount": 0, "miscellaneous": ""},
        {"transaction_code": TransactionCode.DISABLE.value, "account_name": "A", "account_number": "1", "amount": 0, "miscellaneous": ""},
        {"transaction_code": TransactionCode.CHANGEPLAN.value, "account_name": "A", "account_number": "1", "amount": 0, "miscellaneous": ""},
    ]

    apply_transactions({}, transactions)

    # Check each branch was triggered
    assert mock_deposit.called
    assert mock_transfer.called
    assert mock_paybill.called
    assert mock_create.called
    assert mock_delete.called
    assert mock_disable.called
    assert mock_changeplan.called


# TC4: Invalid branch
@patch("transactions.log_constraint_error")
def test_apply_transactions_invalid(mock_log):
    transactions = [
        {
            "transaction_code": "INVALID",
            "account_name": "A",
            "account_number": "123",
            "amount": 0,
            "miscellaneous": "",
        }
    ]

    apply_transactions({}, transactions)

    mock_log.assert_called_once()