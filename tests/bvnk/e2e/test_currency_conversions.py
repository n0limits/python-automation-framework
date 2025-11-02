"""
End-to-End tests for BVNK currency conversions
As per assignment requirements
"""
import pytest
import time
from assertpy import assert_that
from utils.bvnk.helpers import get_wallet_balance, calculate_expected_fee
from config.settings import settings

@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.smoke
def test_convert_1_eth_to_trx(bvnk_api, wallet_balances, print_test_header):
    """
    E2E Test: Convert/trade 1 ETH for TRX
    """
    print_test_header("Convert 1 ETH to TRX")

    # Get initial balances
    initial_eth = wallet_balances['ETH']
    initial_trx = wallet_balances['TRX']

    print(f"Initial ETH balance: {initial_eth}")
    print(f"Initial TRX balance: {initial_trx}")

    # Verify sufficient balance
    assert_that(initial_eth).is_greater_than_or_equal_to(1.0)

    # Create quote
    quote = bvnk_api.create_quote(
        from_currency='ETH',
        to_currency='TRX',
        amount=1.0
    )

    print(f"\nQuote created:")
    print(f"  UUID: {quote['uuid']}")
    print(f"  Price: {quote['price']}")
    print(f"  Amount Out: {quote['amountOut']}")
    print(f"  Fee: {quote['fee']}")

    # Validate quote
    assert_that(quote).contains_key('uuid', 'from', 'to', 'amountIn', 'price')
    assert_that(quote['from']).is_equal_to('ETH')
    assert_that(quote['to']).is_equal_to('TRX')
    assert_that(float(quote['amountIn'])).is_equal_to(1.0)

# Accept quote
    accept_response = bvnk_api.accept_quote(quote['uuid'])
    print(f"\nQuote accepted: {accept_response}")

    # ADD THIS: Wait for transaction to complete
    print(f"\nWaiting for transaction to complete...")
    try:
        final_quote = bvnk_api.wait_for_quote_completion(quote['uuid'], timeout=30)
        print(f"Transaction completed!")
    except TimeoutError as e:
        print(f"⚠️ Warning: {e}")
        print("Proceeding with balance check anyway...")

    # Get final balances
    final_wallets = bvnk_api.list_wallets()
    final_eth = get_wallet_balance(final_wallets, 'ETH')
    final_trx = get_wallet_balance(final_wallets, 'TRX')

    print(f"\nFinal ETH balance: {final_eth}")
    print(f"Final TRX balance: {final_trx}")

    # Verify balances changed
    eth_change = initial_eth - final_eth
    trx_change = final_trx - initial_trx

    print(f"\nBalance changes:")
    print(f"  ETH decreased by: {eth_change}")
    print(f"  TRX increased by: {trx_change}")

    assert_that(eth_change).is_close_to(1.0, 0.0001)
    assert_that(trx_change).is_greater_than(0)

    print("\n TEST PASSED: 1 ETH successfully converted to TRX")


@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.smoke
def test_convert_420_trx_to_usdt(bvnk_api, wallet_balances, print_test_header):
    """
    E2E Test: Convert/trade 420 TRX for USDT
    """
    print_test_header("Convert 420 TRX to USDT")

    # Get initial balances
    initial_trx = wallet_balances['TRX']
    initial_usdt = wallet_balances['USDT']

    print(f"Initial TRX balance: {initial_trx}")
    print(f"Initial USDT balance: {initial_usdt}")

    # Verify sufficient balance
    assert_that(initial_trx).is_greater_than_or_equal_to(420.0)

    # Create quote
    quote = bvnk_api.create_quote(
        from_currency='TRX',
        to_currency='USDT',
        amount=420.0
    )

    print(f"\nQuote created:")
    print(f"  UUID: {quote['uuid']}")
    print(f"  Price: {quote['price']}")  # Changed from 'rate'

    # Validate quote
    assert_that(quote).contains_key('uuid', 'price')  # Changed 'rate' to 'price'
    assert_that(quote['from']).is_equal_to('TRX')
    assert_that(quote['to']).is_equal_to('USDT')

    # Accept quote
    accept_response = bvnk_api.accept_quote(quote['uuid'])
    print(f"\nQuote accepted: {accept_response}")
    # Wait for transaction to complete
    print(f"\nWaiting for transaction to complete...")
    try:
        final_quote = bvnk_api.wait_for_quote_completion(quote['uuid'], timeout=30)
        print(f"Transaction completed!")
    except TimeoutError as e:
        print(f"⚠️ Warning: {e}")
        print("Proceeding with balance check anyway...")

    # Get final balances
    final_wallets = bvnk_api.list_wallets()
    final_trx = get_wallet_balance(final_wallets, 'TRX')
    final_usdt = get_wallet_balance(final_wallets, 'USDT')

    print(f"\nFinal TRX balance: {final_trx}")
    print(f"Final USDT balance: {final_usdt}")

    # Verify balances
    trx_change = initial_trx - final_trx
    usdt_change = final_usdt - initial_usdt

    print(f"\nBalance changes:")
    print(f"  TRX decreased by: {trx_change}")
    print(f"  USDT increased by: {usdt_change}")

    assert_that(trx_change).is_close_to(420.0, 0.0001)
    assert_that(usdt_change).is_greater_than(0)

    print("\n TEST PASSED: 420 TRX successfully converted to USDT")


@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.smoke
def test_convert_987_trx_to_eth(bvnk_api, wallet_balances, print_test_header):
    """
    E2E Test: Convert/trade 987 TRX for ETH
    """
    print_test_header("Convert 987 TRX to ETH")

    # Get initial balances
    initial_trx = wallet_balances['TRX']
    initial_eth = wallet_balances['ETH']

    print(f"Initial TRX balance: {initial_trx}")
    print(f"Initial ETH balance: {initial_eth}")

    # Verify sufficient balance
    assert_that(initial_trx).is_greater_than_or_equal_to(987.0)

    # Create quote
    quote = bvnk_api.create_quote(
        from_currency='TRX',
        to_currency='ETH',
        amount=987.0
    )

    print(f"\nQuote created:")
    print(f"  UUID: {quote['uuid']}")
    print(f"  Price: {quote['price']}")  # Changed from 'rate'

    # Validate quote
    assert_that(quote).contains_key('uuid', 'price')  # Changed 'rate' to 'price'

    # Accept quote
    accept_response = bvnk_api.accept_quote(quote['uuid'])
    print(f"\nQuote accepted: {accept_response}")

    print(f"\nWaiting for transaction to complete...")
    try:
        final_quote = bvnk_api.wait_for_quote_completion(quote['uuid'], timeout=30)
        print(f"Transaction completed!")
    except TimeoutError as e:
        print(f"⚠️ Warning: {e}")
        print("Proceeding with balance check anyway...")

    # Get final balances
    final_wallets = bvnk_api.list_wallets()
    final_trx = get_wallet_balance(final_wallets, 'TRX')
    final_eth = get_wallet_balance(final_wallets, 'ETH')

    print(f"\nFinal TRX balance: {final_trx}")
    print(f"Final ETH balance: {final_eth}")

    # Verify balances
    trx_change = initial_trx - final_trx
    eth_change = final_eth - initial_eth

    print(f"\nBalance changes:")
    print(f"  TRX decreased by: {trx_change}")
    print(f"  ETH increased by: {eth_change}")

    assert_that(trx_change).is_close_to(987.0, 0.0001)
    assert_that(eth_change).is_greater_than(0)

    print("\n TEST PASSED: 987 TRX successfully converted to ETH")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])