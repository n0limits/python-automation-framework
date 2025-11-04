"""
End-to-End tests for BVNK currency conversions

These tests follow the AAA pattern:
- Arrange: Setup test data and helper
- Act: Execute conversion
- Assert: Verify balance changes
"""
import pytest
from utils.bvnk.conversion_helper import ConversionTestHelper
from utils.bvnk.test_data import CONVERSION_TEST_CASES


@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.smoke
def test_convert_1_eth_to_trx(bvnk_api, wallet_balances, print_test_header):
    """
    E2E Test: Convert 1 ETH to TRX

    Verifies:
    - Quote creation and acceptance
    - Transaction completion
    - Correct balance changes
    """
    # === ARRANGE ===
    test_case = CONVERSION_TEST_CASES['eth_to_trx']
    print_test_header(test_case.test_name)

    helper = ConversionTestHelper(bvnk_api)

    print(f"Initial {test_case.from_currency} balance: {wallet_balances[test_case.from_currency]}")
    print(f"Initial {test_case.to_currency} balance: {wallet_balances[test_case.to_currency]}")

    helper.verify_sufficient_balance(
        wallet_balances,
        test_case.from_currency,
        test_case.amount
    )

    # === ACT ===
    conversion_result = helper.execute_conversion(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    # === ASSERT ===
    helper.verify_balance_changes(
        wallet_balances,
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    print(f"\n TEST PASSED: {test_case.test_name}")


@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.smoke
def test_convert_420_trx_to_usdt(bvnk_api, wallet_balances, print_test_header):
    """
    E2E Test: Convert 420 TRX to USDT

    Verifies:
    - Quote creation and acceptance
    - Transaction completion
    - Correct balance changes
    """
    # === ARRANGE ===
    test_case = CONVERSION_TEST_CASES['trx_to_usdt']
    print_test_header(test_case.test_name)

    helper = ConversionTestHelper(bvnk_api)

    print(f"Initial {test_case.from_currency} balance: {wallet_balances[test_case.from_currency]}")
    print(f"Initial {test_case.to_currency} balance: {wallet_balances[test_case.to_currency]}")

    helper.verify_sufficient_balance(
        wallet_balances,
        test_case.from_currency,
        test_case.amount
    )

    # === ACT ===
    conversion_result = helper.execute_conversion(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    # === ASSERT ===
    helper.verify_balance_changes(
        wallet_balances,
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    print(f"\n TEST PASSED: {test_case.test_name}")


@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.smoke
def test_convert_987_trx_to_eth(bvnk_api, wallet_balances, print_test_header):
    """
    E2E Test: Convert 987 TRX to ETH

    Verifies:
    - Quote creation and acceptance
    - Transaction completion
    - Correct balance changes
    """
    # === ARRANGE ===
    test_case = CONVERSION_TEST_CASES['trx_to_eth']
    print_test_header(test_case.test_name)

    helper = ConversionTestHelper(bvnk_api)

    print(f"Initial {test_case.from_currency} balance: {wallet_balances[test_case.from_currency]}")
    print(f"Initial {test_case.to_currency} balance: {wallet_balances[test_case.to_currency]}")

    helper.verify_sufficient_balance(
        wallet_balances,
        test_case.from_currency,
        test_case.amount
    )

    # === ACT ===
    conversion_result = helper.execute_conversion(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    # === ASSERT ===
    helper.verify_balance_changes(
        wallet_balances,
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    print(f"\n TEST PASSED: {test_case.test_name}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])