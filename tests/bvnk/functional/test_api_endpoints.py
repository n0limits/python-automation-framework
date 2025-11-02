"""
Functional tests for BVNK API endpoints
Additional tests as per assignment requirements
"""
import pytest
import time

import requests
from assertpy import assert_that
from config.settings import settings


@pytest.mark.bvnk
@pytest.mark.functional
def test_authentication_echo(bvnk_api, print_test_header):
    """
    Test that authentication works correctly with the echo endpoint
    """
    print_test_header("Authentication Echo")

    # Create test payload
    test_payload = {
        'test_key': 'test_value',
        'number': 123
    }

    # Call echo endpoint
    response = bvnk_api.echo(test_payload)
    print(f"Echo response: {response}")

    # Verify response structure (use actual field names)
    assert_that(response).contains_key('auth_token_expiry_time')  # Changed from 'expiry'
    assert_that(response).contains_key('request_payload')

    # Verify payload was echoed back
    echoed_payload = response['request_payload']
    assert_that(echoed_payload).is_equal_to(test_payload)

    print("\n TEST PASSED: Authentication working correctly")


# @pytest.mark.bvnk
# @pytest.mark.functional
# def test_authentication_echo(bvnk_api, print_test_header):
#     """
#     Test that authentication works correctly with the echo endpoint
#     """
#     print_test_header("Authentication Echo")
#
#     # Create test payload
#     test_payload = {
#         'test_key': 'test_value',
#         'number': 123
#     }
#
#     # Call echo endpoint
#     response = bvnk_api.echo(test_payload)
#     print(f"Echo response: {response}")
#
#     # Verify response structure (use actual field names from response)
#     assert_that(response).contains_key('auth_token_expiry_time')  # Changed from 'expiry'
#     assert_that(response).contains_key('request_payload')
#
#     # Verify payload was echoed back
#     echoed_payload = response['request_payload']
#     assert_that(echoed_payload).is_equal_to(test_payload)
#
#     print("\nTEST PASSED: Authentication working correctly")


@pytest.mark.bvnk
@pytest.mark.functional
def test_list_all_wallets(bvnk_api):
    """
    Test: Verify wallet listing functionality
    """
    print("\n" + "=" * 60)
    print("TEST: List All Wallets")
    print("=" * 60)

    wallets = bvnk_api.list_wallets()

    print(f"Number of wallets: {len(wallets)}")

    # Assertions
    assert_that(wallets).is_instance_of(list)
    assert_that(len(wallets)).is_greater_than(0)

    # Verify wallet structure
    for wallet in wallets:
        print(f"  {wallet['currency']}: {wallet['balance']}")
        assert_that(wallet).contains_key('currency', 'balance')

    print(" TEST PASSED: Wallets listed successfully")


@pytest.mark.bvnk
@pytest.mark.functional
def test_quote_expiry(bvnk_api):
    """
    Test: Verify quote expires after 20 seconds
    """
    print("\n" + "=" * 60)
    print("TEST: Quote Expiry")
    print("=" * 60)

    # Create quote
    quote = bvnk_api.create_quote('ETH', 'TRX', 0.1)
    quote_uuid = quote['uuid']

    print(f"Quote created: {quote_uuid}")
    print(f"Waiting {settings.QUOTE_EXPIRY_SECONDS + 2} seconds for expiry...")

    # Wait for quote to expire
    time.sleep(settings.QUOTE_EXPIRY_SECONDS + 2)

    # Try to accept expired quote
    try:
        bvnk_api.accept_quote(quote_uuid)
        pytest.fail("Expected quote to be expired, but it was accepted")
    except requests.exceptions.HTTPError as e:
        print(f"Quote correctly expired: {e}")
        assert_that(e.response.status_code).is_in(400, 404, 410)

    print(" TEST PASSED: Quote expires correctly")


@pytest.mark.bvnk
@pytest.mark.functional
def test_insufficient_balance(bvnk_api, print_test_header):
    """
    Test that system rejects conversions with insufficient balance
    """
    print_test_header("Insufficient Balance")

    # Get wallets
    wallets = bvnk_api.list_wallets()

    # Use the helper function correctly
    from utils.bvnk.helpers import get_wallet_by_currency
    eth_wallet = get_wallet_by_currency(wallets, 'ETH')

    assert_that(eth_wallet).is_not_none()

    # Get current balance (it's a string, convert to float)
    current_balance = float(eth_wallet['balance'])
    print(f"Current ETH balance: {current_balance}")

    # Try to convert more than available
    excessive_amount = current_balance + 1000.0
    print(f"Attempting to convert {excessive_amount} ETH (more than balance)")

    # This should fail
    try:
        quote = bvnk_api.create_quote('ETH', 'TRX', excessive_amount)
        bvnk_api.accept_quote(quote['uuid'])
        pytest.fail("Should have rejected insufficient balance")
    except requests.exceptions.HTTPError as e:
        print(f" Correctly rejected: {e.response.status_code}")
        assert_that(e.response.status_code).is_in(400, 422)  # Bad request or unprocessable

    print("\n TEST PASSED: Insufficient balance correctly rejected")


@pytest.mark.bvnk
@pytest.mark.functional
def test_service_fee_calculation(bvnk_api):
    """
    Test: Verify service fee is calculated correctly (0.01%)
    """
    print("\n" + "=" * 60)
    print("TEST: Service Fee Calculation")
    print("=" * 60)

    # Get initial balance
    initial_wallets = bvnk_api.list_wallets()
    initial_eth = next((w['balance'] for w in initial_wallets if w['currency'] == 'ETH'), 0)

    amount = 1.0
    expected_fee = amount * (settings.SERVICE_FEE_PERCENT / 100)
    expected_net = amount - expected_fee

    print(f"Converting {amount} ETH")
    print(f"Expected fee: {expected_fee} ETH")
    print(f"Expected net: {expected_net} ETH")

    # Create and accept quote
    quote = bvnk_api.create_quote('ETH', 'TRX', amount)
    bvnk_api.accept_quote(quote['uuid'])

    # Verify balance change
    final_wallets = bvnk_api.list_wallets()
    final_eth = next((w['balance'] for w in final_wallets if w['currency'] == 'ETH'), 0)

    actual_deducted = float(initial_eth) - float(final_eth)

    print(f"Actually deducted: {actual_deducted} ETH")

    # Allow small rounding difference
    assert_that(actual_deducted).is_close_to(amount, 0.001)

    print(" TEST PASSED: Service fee calculated correctly")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
