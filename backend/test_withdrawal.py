import pytest
from unittest.mock import patch

from transactions import handle_withdrawal


# TC1: Account not found
@patch("transactions.get_account", return_value=None)
@patch("transactions.log_constraint_error")
def test_withdrawal_account_not_found(mock_log, mock_get_account):
    handle_withdrawal({}, "123", 100)
    mock_log.assert_called_once()


# TC2: Invalid balance
@patch("transactions.increment_transaction_count")
@patch("transactions.validate_balance", return_value=False)
@patch("transactions.get_transaction_cost", return_value=5)
@patch("transactions.get_account", return_value={"balance": 100})
@patch("transactions.log_constraint_error")
def test_withdrawal_invalid_balance(
    mock_log, mock_get_account, mock_cost, mock_validate, mock_increment
):
    handle_withdrawal({}, "123", 200)

    mock_log.assert_called_once()
    mock_increment.assert_not_called()


# TC3: Success
@patch("transactions.increment_transaction_count")
@patch("transactions.validate_balance", return_value=True)
@patch("transactions.get_transaction_cost", return_value=5)
def test_withdrawal_success(mock_cost, mock_validate, mock_increment):
    account = {"balance": 200}

    with patch("transactions.get_account", return_value=account):
        handle_withdrawal({}, "123", 50)

    assert account["balance"] == 145
    mock_increment.assert_called_once()