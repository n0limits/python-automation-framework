"""
Functional tests for BVNK API endpoints
Additional tests as per assignment requirements
"""
import pytest
import time

import requests
from assertpy import assert_that
from config.settings import settings
from utils.bvnk.helpers import calculate_expected_fee, get_wallet_balance


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
        assert_that(e.response.status_code).is_in(400, 404, 410, 412)

        print(f"\n TEST PASSED: Quote expiry working correctly")


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
        print(f"✅ Correctly rejected: {e.response.status_code}")
        assert_that(e.response.status_code).is_in(400, 412, 422)  # Bad request or unprocessable

    print("\n TEST PASSED: Insufficient balance correctly rejected")

@pytest.mark.bvnk
@pytest.mark.functional
def test_service_fee_calculation(bvnk_api, print_test_header):
    """
    Test that service fee is calculated correctly (0.01%)
    """
    print_test_header("Service Fee Calculation")

    amount = 1.0
    print(f"Converting {amount} ETH")

    # Calculate expected fee
    expected_fee = calculate_expected_fee(amount, settings.SERVICE_FEE_PERCENT)
    expected_net = amount - expected_fee

    print(f"Expected fee: {expected_fee} ETH")
    print(f"Expected net: {expected_net} ETH")

    # Get initial balance
    wallets = bvnk_api.list_wallets()
    initial_eth = get_wallet_balance(wallets, 'ETH')

    # Create quote
    quote = bvnk_api.create_quote('ETH', 'TRX', amount)

    # Get the fee from quote response
    actual_fee = float(quote.get('fee', 0))
    print(f"Actual fee from quote: {actual_fee} ETH")

    # Verify fee is correct
    assert_that(actual_fee).is_close_to(expected_fee, 0.00001)

    # Accept and wait for completion
    bvnk_api.accept_quote(quote['uuid'])

    print(f"\nWaiting for transaction to complete...")
    try:
        bvnk_api.wait_for_quote_completion(quote['uuid'], timeout=30)
    except TimeoutError:
        print("⚠️ Timeout waiting for completion")

    # Get final balance
    final_wallets = bvnk_api.list_wallets()
    final_eth = get_wallet_balance(final_wallets, 'ETH')

    # Calculate actual deduction
    actual_deducted = initial_eth - final_eth
    print(f"Actually deducted: {actual_deducted} ETH")

    # Verify the full amount was deducted (fee is taken from received amount, not sent amount)
    assert_that(actual_deducted).is_close_to(amount, 0.001)

    print(f"\n TEST PASSED: Service fee calculation correct")

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
