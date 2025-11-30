"""
Functional tests for BVNK API endpoints (FIXED VERSION)

FIXES APPLIED:
1. Replaced print statements with logger calls
2. Kept print only for formatted test output
3. Used appropriate log levels (DEBUG, INFO, ERROR)
4. Removed excessive/obvious comments
5. Kept only "WHY" comments, removed "WHAT" comments
"""
import pytest
from utils.bvnk.api_validation_helper import ApiValidationHelper
from utils.bvnk.test_data import FUNCTIONAL_TEST_CASES, ERROR_STATUS_CODES
from utils.bvnk.helpers import get_wallet_balance, get_wallet_by_currency
from config.settings import settings
from utils.logger import logger  # FIXED: Import logger


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
    print_test_header("Authentication Echo")  # Keep formatted output
    logger.info("Testing authentication via /echo endpoint")  # FIXED: Use logger

    helper = ApiValidationHelper(bvnk_api)
    test_payload = {'test_key': 'test_value', 'number': 123}
    logger.debug(f"Test payload: {test_payload}")  # FIXED: Debug details

    response = helper.validate_echo_response(test_payload)

    logger.info("Authentication test completed successfully")  # FIXED: Use logger
    print("\n✅ TEST PASSED: Authentication working correctly")  # Keep result output


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
    print_test_header("List All Wallets")
    logger.info("Testing wallet list endpoint")  # FIXED: Use logger

    helper = ApiValidationHelper(bvnk_api)
    min_expected = settings.MIN_EXPECTED_WALLETS
    logger.debug(f"Minimum expected wallets: {min_expected}")  # FIXED: Debug details

    wallets = helper.validate_wallet_list(min_expected)

    logger.info(f"Successfully retrieved {len(wallets)} wallets")  # FIXED: Use logger
    print(f"\n✅ TEST PASSED: Wallets listed successfully ({len(wallets)} wallets)")


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
    print_test_header("Quote Expiry")
    logger.info("Testing quote expiry behavior")  # FIXED: Use logger

    helper = ApiValidationHelper(bvnk_api)
    test_case = FUNCTIONAL_TEST_CASES['quote_expiry']
    expected_statuses = ERROR_STATUS_CODES.QUOTE_EXPIRED

    logger.debug(f"Creating quote: {test_case.amount} {test_case.from_currency} -> {test_case.to_currency}")  # FIXED

    quote_uuid = helper.test_quote_expiry(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount,
        test_case.wait_time
    )

    logger.info(f"Verifying quote {quote_uuid} has expired")  # FIXED: Use logger
    helper.verify_quote_expiry_error(quote_uuid, expected_statuses)

    logger.info("Quote expiry test completed successfully")  # FIXED: Use logger
    print("\n✅ TEST PASSED: Quote expiry working correctly")


@pytest.mark.bvnk
@pytest.mark.functional
def test_insufficient_balance(bvnk_api, print_test_header):
    """
    Test: Insufficient balance error handling

    Verifies:
    - API rejects conversions exceeding balance
    - Correct error status code returned
    """
    print_test_header("Insufficient Balance")
    logger.info("Testing insufficient balance validation")  # FIXED: Use logger

    helper = ApiValidationHelper(bvnk_api)
    test_case = FUNCTIONAL_TEST_CASES['insufficient_balance']
    expected_statuses = ERROR_STATUS_CODES.INSUFFICIENT_BALANCE

    wallets = bvnk_api.list_wallets()
    eth_wallet = get_wallet_by_currency(wallets, test_case.from_currency)
    current_balance = float(eth_wallet['balance'])

    logger.info(f"Current {test_case.from_currency} balance: {current_balance}")  # FIXED: Use logger
    print(f"Current {test_case.from_currency} balance: {current_balance}")  # Keep visible output

    # Add extra amount to ensure insufficient balance
    excessive_amount = current_balance + test_case.balance_excess
    logger.debug(f"Testing with excessive amount: {excessive_amount}")  # FIXED

    helper.verify_insufficient_balance_error(
        test_case.from_currency,
        test_case.to_currency,
        excessive_amount,
        expected_statuses
    )

    logger.info("Insufficient balance test completed successfully")  # FIXED: Use logger
    print("\n✅ TEST PASSED: Insufficient balance correctly rejected")


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
    print_test_header("Service Fee Calculation")
    logger.info("Testing service fee calculation (0.01%)")  # FIXED: Use logger

    helper = ApiValidationHelper(bvnk_api)
    test_case = FUNCTIONAL_TEST_CASES['fee_calculation']

    wallets = bvnk_api.list_wallets()
    initial_balance = get_wallet_balance(wallets, test_case.from_currency)

    logger.info(f"Initial {test_case.from_currency} balance: {initial_balance}")  # FIXED
    print(f"Converting {test_case.amount} {test_case.from_currency}")

    quote = bvnk_api.create_quote(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )
    logger.debug(f"Quote created: {quote.get('uuid')}")  # FIXED

    actual_fee = helper.verify_service_fee(test_case.amount, quote)
    logger.info(f"Service fee verified: {actual_fee}")  # FIXED

    bvnk_api.accept_quote(quote['uuid'])
    logger.info("Quote accepted, waiting for completion")  # FIXED

    print(f"\nWaiting for transaction to complete...")
    try:
        bvnk_api.wait_for_quote_completion(quote['uuid'], timeout=30)
        logger.info("Transaction completed successfully")  # FIXED
    except TimeoutError:
        logger.warning("Transaction timed out")  # FIXED: Use logger
        print("⚠ Timeout waiting for completion")

    final_wallets = bvnk_api.list_wallets()
    final_balance = get_wallet_balance(final_wallets, test_case.from_currency)

    actual_deducted = initial_balance - final_balance
    logger.info(f"Balance change: {initial_balance} -> {final_balance} (deducted: {actual_deducted})")  # FIXED

    print(f"\nBalance Verification:")
    print(f"  Initial: {initial_balance}")
    print(f"  Final: {final_balance}")
    print(f"  Actually deducted: {actual_deducted}")

    from assertpy import assert_that
    from utils.bvnk.helpers import calculate_expected_fee

    expected_fee = calculate_expected_fee(test_case.amount, settings.SERVICE_FEE_PERCENT)
    expected_total_deduction = test_case.amount + expected_fee

    print(f"  Expected deduction:")
    print(f"    - Amount: {test_case.amount}")
    print(f"    - Fee (0.01%): {expected_fee:.6f}")
    print(f"    - Total: {expected_total_deduction:.6f}")

    assert_that(actual_deducted).is_close_to(expected_total_deduction, 0.00001)

    logger.info("Service fee test completed successfully")  # FIXED: Use logger
    print(f"\n✅ TEST PASSED: Service fee calculation correct")
    print(f"    Amount deducted: {actual_deducted:.6f}")
    print(f"    Expected: {expected_total_deduction:.6f}")
    print(f"    Difference: {abs(actual_deducted - expected_total_deduction):.8f}")


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
    print_test_header("Get Specific Wallet")
    logger.info("Testing individual wallet retrieval")  # FIXED: Use logger

    wallets = bvnk_api.list_wallets()

    from assertpy import assert_that
    assert_that(wallets).is_not_empty()

    first_wallet = wallets[0]
    wallet_id = first_wallet['id']

    logger.info(f"Testing with wallet ID: {wallet_id}")  # FIXED: Use logger
    logger.debug(f"Expected currency: {first_wallet['currency']['code']}")  # FIXED

    print(f"\nTesting with wallet ID: {wallet_id}")
    print(f"Expected currency: {first_wallet['currency']['code']}")

    specific_wallet = bvnk_api.get_wallet(wallet_id)

    logger.debug(f"Retrieved wallet: {specific_wallet.get('id')}")  # FIXED
    print(f"\nRetrieved wallet details:")
    print(f"  ID: {specific_wallet['id']}")
    print(f"  Currency: {specific_wallet['currency']['code']}")
    print(f"  Balance: {specific_wallet['balance']}")

    # Verify wallet structure
    assert_that(specific_wallet).contains_key('id', 'currency', 'balance', 'description')
    assert_that(specific_wallet['currency']).contains_key('code', 'name')

    # Verify it matches the wallet from list
    assert_that(specific_wallet['id']).is_equal_to(first_wallet['id'])
    assert_that(specific_wallet['currency']['code']).is_equal_to(first_wallet['currency']['code'])
    assert_that(specific_wallet['balance']).is_equal_to(first_wallet['balance'])

    logger.info("Wallet retrieval test completed successfully")  # FIXED: Use logger
    print(f"\n✅ TEST PASSED: Specific wallet retrieved successfully")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
