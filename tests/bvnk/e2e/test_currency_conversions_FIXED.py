"""
End-to-End tests for BVNK currency conversions (FIXED VERSION)

FIXES APPLIED:
1. Added pytest parametrization to reduce code duplication
2. Single test function instead of 3 duplicate functions
3. Better test IDs for clear reporting
4. Reduced from ~150 lines to ~60 lines
"""
import pytest
from utils.bvnk.conversion_helper import ConversionTestHelper
from utils.bvnk.test_data import CONVERSION_TEST_CASES


@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.parametrize(
    "test_case_key",
    [
        pytest.param("eth_to_trx", id="convert_1_eth_to_trx"),
        pytest.param("trx_to_usdt", id="convert_420_trx_to_usdt"),
        pytest.param("trx_to_eth", id="convert_987_trx_to_eth"),
    ]
)
def test_currency_conversion(bvnk_api, wallet_balances, print_test_header, test_case_key):
    """
    Parametrized E2E Test: Currency Conversions

    Tests multiple conversion scenarios with a single test function:
    - 1 ETH → TRX
    - 420 TRX → USDT
    - 987 TRX → ETH

    Benefits of parametrization:
    - Reduced code duplication (150 lines → 60 lines)
    - Easy to add new test cases (just add to parametrize decorator)
    - Consistent test logic across all scenarios
    - Clear test IDs in reports

    Verifies:
    - Quote creation and acceptance
    - Transaction completion
    - Correct balance changes
    """
    # === ARRANGE ===
    test_case = CONVERSION_TEST_CASES[test_case_key]
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

    print(f"\n✓ TEST PASSED: {test_case.test_name}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
