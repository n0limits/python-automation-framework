"""
Functional tests for BVNK API endpoints

These tests follow the AAA pattern:
- Arrange: Setup helper and test data
- Act: Execute API call
- Assert: Verify response/behavior
"""
import pytest
from utils.bvnk.api_validation_helper import ApiValidationHelper
from utils.bvnk.test_data import FUNCTIONAL_TEST_CASES, ERROR_STATUS_CODES
from utils.bvnk.helpers import get_wallet_balance, get_wallet_by_currency
from config.settings import settings


@pytest.mark.bvnk
@pytest.mark.functional
def test_authentication_echo(bvnk_api, print_test_header):
    """
    Test: Authentication via /echo endpoint

    Verifies:
    - Echo endpoint responds correctly
    - Token is valid
    - Request payload is echoed back
    """
    # === ARRANGE ===
    print_test_header("Authentication Echo")
    helper = ApiValidationHelper(bvnk_api)

    test_payload = {'test_key': 'test_value', 'number': 123}

    # === ACT ===
    response = helper.validate_echo_response(test_payload)

    # === ASSERT ===
    print("\n TEST PASSED: Authentication working correctly")


@pytest.mark.bvnk
@pytest.mark.functional
def test_list_all_wallets(bvnk_api, print_test_header):
    """
    Test: List all wallets

    Verifies:
    - Wallets can be listed
    - Expected number of wallets returned
    - Each wallet has required structure
    """
    # === ARRANGE ===
    print_test_header("List All Wallets")
    helper = ApiValidationHelper(bvnk_api)

    min_expected = settings.MIN_EXPECTED_WALLETS

    # === ACT ===
    wallets = helper.validate_wallet_list(min_expected)

    # === ASSERT ===
    print(f"\n TEST PASSED: Wallets listed successfully ({len(wallets)} wallets)")


@pytest.mark.bvnk
@pytest.mark.functional
def test_quote_expiry(bvnk_api, print_test_header):
    """
    Test: Quote expiry after acceptance window

    Verifies:
    - Quotes expire after waiting period
    - Expired quotes cannot be accepted
    - Correct error status code returned
    """
    # === ARRANGE ===
    print_test_header("Quote Expiry")
    helper = ApiValidationHelper(bvnk_api)

    test_case = FUNCTIONAL_TEST_CASES['quote_expiry']
    expected_statuses = ERROR_STATUS_CODES.QUOTE_EXPIRED

    # === ACT ===
    quote_uuid = helper.test_quote_expiry(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount,
        test_case.wait_time
    )

    # === ASSERT ===
    helper.verify_quote_expiry_error(quote_uuid, expected_statuses)

    print("\n TEST PASSED: Quote expiry working correctly")


@pytest.mark.bvnk
@pytest.mark.functional
def test_insufficient_balance(bvnk_api, print_test_header):
    """
    Test: Insufficient balance error handling

    Verifies:
    - API rejects conversions exceeding balance
    - Correct error status code returned
    """
    # === ARRANGE ===
    print_test_header("Insufficient Balance")
    helper = ApiValidationHelper(bvnk_api)

    test_case = FUNCTIONAL_TEST_CASES['insufficient_balance']
    expected_statuses = ERROR_STATUS_CODES.INSUFFICIENT_BALANCE

    # Get current balance
    wallets = bvnk_api.list_wallets()
    eth_wallet = get_wallet_by_currency(wallets, test_case.from_currency)
    current_balance = float(eth_wallet['balance'])

    print(f"Current {test_case.from_currency} balance: {current_balance}")

    excessive_amount = current_balance + test_case.balance_excess

    # === ACT & ASSERT ===
    helper.verify_insufficient_balance_error(
        test_case.from_currency,
        test_case.to_currency,
        excessive_amount,
        expected_statuses
    )

    print("\n TEST PASSED: Insufficient balance correctly rejected")


@pytest.mark.bvnk
@pytest.mark.functional
def test_service_fee_calculation(bvnk_api, print_test_header):
    """
    Test: Service fee calculation (0.01%)

    Verifies:
    - Fee is correctly calculated from quote
    - Fee matches expected percentage
    - Amount deducted equals conversion amount
    """
    # === ARRANGE ===
    print_test_header("Service Fee Calculation")
    helper = ApiValidationHelper(bvnk_api)

    test_case = FUNCTIONAL_TEST_CASES['fee_calculation']

    # Get initial balance
    wallets = bvnk_api.list_wallets()
    initial_balance = get_wallet_balance(wallets, test_case.from_currency)

    print(f"Converting {test_case.amount} {test_case.from_currency}")

    # === ACT ===
    # Create quote
    quote = bvnk_api.create_quote(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    # Verify fee in quote
    actual_fee = helper.verify_service_fee(test_case.amount, quote)

    # Accept and wait for completion
    bvnk_api.accept_quote(quote['uuid'])

    print(f"\nWaiting for transaction to complete...")
    try:
        bvnk_api.wait_for_quote_completion(quote['uuid'], timeout=30)
    except TimeoutError:
        print(" Timeout waiting for completion")

    # Get final balance
    final_wallets = bvnk_api.list_wallets()
    final_balance = get_wallet_balance(final_wallets, test_case.from_currency)

    # === ASSERT ===
    actual_deducted = initial_balance - final_balance
    print(f"\nBalance Verification:")
    print(f"  Initial: {initial_balance}")
    print(f"  Final: {final_balance}")
    print(f"  Actually deducted: {actual_deducted}")

    from assertpy import assert_that
    assert_that(actual_deducted).is_close_to(test_case.amount, 0.001)

    print(f"\n TEST PASSED: Service fee calculation correct")

@pytest.mark.bvnk
@pytest.mark.functional
def test_get_specific_wallet(bvnk_api, print_test_header):
    """
    Test: Get specific wallet by ID

    Verifies:
    - Individual wallet can be retrieved by ID
    - Wallet details match the list response
    - All required fields are present
    """
    # === ARRANGE ===
    print_test_header("Get Specific Wallet")

    # First, get all wallets to find a valid wallet ID
    wallets = bvnk_api.list_wallets()

    from assertpy import assert_that
    assert_that(wallets).is_not_empty()

    # Get the first wallet's ID
    first_wallet = wallets[0]
    wallet_id = first_wallet['id']

    print(f"\nTesting with wallet ID: {wallet_id}")
    print(f"Expected currency: {first_wallet['currency']['code']}")

    # === ACT ===
    # Get specific wallet details
    specific_wallet = bvnk_api.get_wallet(wallet_id)

    print(f"\nRetrieved wallet details:")
    print(f"  ID: {specific_wallet['id']}")
    print(f"  Currency: {specific_wallet['currency']['code']}")
    print(f"  Balance: {specific_wallet['balance']}")

    # === ASSERT ===
    # Verify wallet structure
    assert_that(specific_wallet).contains_key('id', 'currency', 'balance', 'description')
    assert_that(specific_wallet['currency']).contains_key('code', 'name')

    # Verify it matches the wallet from list
    assert_that(specific_wallet['id']).is_equal_to(first_wallet['id'])
    assert_that(specific_wallet['currency']['code']).is_equal_to(first_wallet['currency']['code'])
    assert_that(specific_wallet['balance']).is_equal_to(first_wallet['balance'])

    print(f"\n TEST PASSED: Specific wallet retrieved successfully")

# @pytest.mark.bvnk
# @pytest.mark.functional
# def test_get_specific_wallet(bvnk_api, print_test_header):
#     """
#     Test: Get specific wallet by ID
#
#     Verifies:
#     - Individual wallet can be retrieved by ID
#     - Wallet details are complete and valid
#     - Wallet matches expected structure
#     """
#     # === ARRANGE ===
#     print_test_header("Get Specific Wallet")
#     helper = ApiValidationHelper(bvnk_api)
#
#     # First get all wallets to find a valid ID
#     all_wallets = bvnk_api.list_wallets()
#
#     from assertpy import assert_that
#     assert_that(all_wallets).is_not_empty()
#
#     # Use first wallet's ID for testing
#     test_wallet_from_list = all_wallets[0]
#     wallet_id = test_wallet_from_list['id']
#     expected_currency = test_wallet_from_list['currency']['code']
#
#     print(f"\nTesting with wallet ID: {wallet_id}")
#     print(f"Expected currency: {expected_currency}")
#
#     # === ACT ===
#     specific_wallet = helper.validate_specific_wallet(wallet_id, expected_currency)
#
#     # === ASSERT ===
#     # Verify it matches the wallet from list endpoint
#     assert_that(specific_wallet['id']).is_equal_to(test_wallet_from_list['id'])
#     assert_that(specific_wallet['currency']['code']).is_equal_to(test_wallet_from_list['currency']['code'])
#     assert_that(specific_wallet['balance']).is_equal_to(test_wallet_from_list['balance'])
#
#     print(f"\n TEST PASSED: Specific wallet retrieved and validated")

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
