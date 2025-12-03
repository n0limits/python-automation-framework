"""
Negative tests for BVNK API
"""
import pytest
import requests
from utils.bvnk.helpers import get_wallet_by_currency
from utils.bvnk.test_data import ERROR_STATUS_CODES
from utils.bvnk.api_client import BVNKResourceNotFoundError, BVNKValidationError


@pytest.mark.bvnk
@pytest.mark.negative
def test_get_nonexistent_wallet(bvnk_api, print_test_header):
    """
    Test: Retrieve a wallet that doesn't exist
    Verifies:
    - API returns 404 for nonexistent wallet
    """
    print_test_header("Get Nonexistent Wallet")

    wallet_id = 999999  # non-existent
    print(f"Retrieving wallet {wallet_id}...")

    try:
        bvnk_api.get_wallet(wallet_id)
        raise AssertionError("API should reject nonexistent wallet")
    except BVNKResourceNotFoundError as e:
        print(f"Correctly rejected nonexistent wallet: {e.status_code}")
        assert e.status_code == 404

    print("\n TEST PASSED: Nonexistent wallet request correctly rejected")


# TODO why does it accept negative amounts?

@pytest.mark.bvnk
@pytest.mark.negative
@pytest.mark.xfail(reason="API currently allows negative amounts")
def test_create_quote_negative_amount(bvnk_api, print_test_header):
    """
    Test: Create a quote with a negative amount
    Verifies:
    - API should reject negative amounts
    """
    print_test_header("Create Quote with Negative Amount")

    # Get wallets
    wallets = bvnk_api.list_wallets()
    from_wallet = get_wallet_by_currency(wallets, 'ETH')
    to_wallet = get_wallet_by_currency(wallets, 'TRX')

    negative_amount = -10.0
    print(f"Creating quote:\n  From: ETH (wallet ID: {from_wallet['id']})\n"
          f"  To: TRX (wallet ID: {to_wallet['id']})\n  Amount: {negative_amount}")

    try:
        bvnk_api.create_quote('ETH', 'TRX', negative_amount)
        raise AssertionError("API should reject negative amount")
    except BVNKValidationError as e:
        print(f"Correctly rejected negative amount: {e.status_code}")
        assert e.status_code in [400, 422]


@pytest.mark.bvnk
@pytest.mark.negative
def test_accept_invalid_quote_uuid(bvnk_api, print_test_header):
    """
    Test: Accept a quote using an invalid UUID
    Verifies:
    - API rejects invalid UUID
    - Returns correct error status (422 included)
    """
    print_test_header("Accept Invalid Quote UUID")

    invalid_uuid = "invalid-uuid-1234"
    expected_statuses = [400, 404, 410, 412, 422]  # include 422

    try:
        bvnk_api.accept_quote(invalid_uuid)
        raise AssertionError("API should reject invalid quote UUID")
    except BVNKValidationError as e:
        print(f"Correctly rejected invalid UUID: {e.status_code}")
        assert e.status_code in expected_statuses

    print("\n TEST PASSED: Invalid quote UUID correctly rejected")
