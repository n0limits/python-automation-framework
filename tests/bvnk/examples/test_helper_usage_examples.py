"""
Examples of using ConversionTestHelper in different scenarios

These are example tests showing various ways to use the helper.
Uncomment and modify as needed for your use cases.
"""
import pytest
from utils.bvnk.conversion_helper import ConversionTestHelper
from utils.bvnk.test_data import CONVERSION_TEST_CASES


@pytest.mark.bvnk
@pytest.mark.examples
@pytest.mark.skip(reason="Example test - uncomment to use")
def test_multiple_conversions_sequence(bvnk_api, wallet_balances):
    """
    Example: Execute multiple conversions in sequence

    Demonstrates using ConversionTestHelper for
    testing sequential conversion flows
    """
    helper = ConversionTestHelper(bvnk_api, timeout=60)

    # First conversion
    print("\n[Conversion 1/3] ETH → TRX")
    result1 = helper.execute_conversion('ETH', 'TRX', 0.1)

    # Second conversion
    print("\n[Conversion 2/3] TRX → USDT")
    result2 = helper.execute_conversion('TRX', 'USDT', 100)

    # Third conversion
    print("\n[Conversion 3/3] USDT → ETH")
    result3 = helper.execute_conversion('USDT', 'ETH', 50)

    print("\n All 3 conversions completed successfully")

    # Verify all conversions succeeded
    assert result1['final_quote'] is not None
    assert result2['final_quote'] is not None
    assert result3['final_quote'] is not None


@pytest.mark.bvnk
@pytest.mark.examples
@pytest.mark.skip(reason="Example test - uncomment to use")
def test_conversion_with_custom_timeout(bvnk_api, wallet_balances):
    """
    Example: Test conversion with extended timeout
    """
    # Use longer timeout for this test (2 minutes)
    helper = ConversionTestHelper(bvnk_api, timeout=120)

    result = helper.execute_conversion('ETH', 'TRX', 0.5)

    assert result['final_quote'] is not None
    print("\n Conversion completed within extended timeout")


@pytest.mark.bvnk
@pytest.mark.examples
@pytest.mark.skip(reason="Example test - uncomment to use")
def test_using_test_data_dynamically(bvnk_api, wallet_balances):
    """
    Example: Use test data dynamically based on conditions
    """
    helper = ConversionTestHelper(bvnk_api)

    # Choose test case based on balance
    eth_balance = wallet_balances['ETH']

    if eth_balance >= 1.0:
        test_case = CONVERSION_TEST_CASES['eth_to_trx']
    else:
        test_case = CONVERSION_TEST_CASES['trx_to_usdt']

    print(f"\nExecuting: {test_case.test_name}")
    print(f"Reason: ETH balance is {eth_balance}")

    result = helper.execute_conversion(
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )

    helper.verify_balance_changes(
        wallet_balances,
        test_case.from_currency,
        test_case.to_currency,
        test_case.amount
    )


@pytest.mark.bvnk
@pytest.mark.examples
@pytest.mark.skip(reason="Example test - uncomment to use")
def test_verify_balance_only(bvnk_api, wallet_balances):
    """
    Example: Use helper just for balance verification

    Useful when you want manual control over conversion
    but still want consistent balance verification
    """
    helper = ConversionTestHelper(bvnk_api)

    # Do conversion manually (for testing specific scenarios)
    quote = bvnk_api.create_quote('ETH', 'TRX', 0.1)
    print(f"Manual quote created: {quote['uuid']}")

    bvnk_api.accept_quote(quote['uuid'])
    print("Manual quote accepted")

    bvnk_api.wait_for_quote_completion(quote['uuid'])
    print("Manual wait completed")

    # Use helper just for verification
    helper.verify_balance_changes(
        wallet_balances,
        'ETH',
        'TRX',
        0.1
    )

    print("\n Manual conversion verified using helper")


@pytest.mark.bvnk
@pytest.mark.examples
@pytest.mark.skip(reason="Example test - uncomment to use")
def test_conversion_chain(bvnk_api, wallet_balances):
    """
    Example: Chain of conversions (round trip)

    ETH → TRX → USDT → ETH
    """
    helper = ConversionTestHelper(bvnk_api, timeout=60)

    initial_eth = wallet_balances['ETH']
    print(f"\nStarting ETH balance: {initial_eth}")

    # Step 1: ETH → TRX
    print("\n[Step 1/3] ETH → TRX")
    helper.execute_conversion('ETH', 'TRX', 0.1)

    # Step 2: TRX → USDT
    print("\n[Step 2/3] TRX → USDT")
    helper.execute_conversion('TRX', 'USDT', 500)

    # Step 3: USDT → ETH (back to ETH)
    print("\n[Step 3/3] USDT → ETH")
    helper.execute_conversion('USDT', 'ETH', 100)

    # Check final ETH balance
    from utils.bvnk.helpers import get_wallet_balance
    final_wallets = bvnk_api.list_wallets()
    final_eth = get_wallet_balance(final_wallets, 'ETH')

    print(f"\nFinal ETH balance: {final_eth}")
    print(f"Net change: {final_eth - initial_eth} ETH")

    print("\n Round trip conversion completed")