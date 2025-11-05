"""
Conversion Test Helper
Provides reusable methods for currency conversion testing
"""
from typing import Dict, Any, Tuple
from assertpy import assert_that
from config.settings import settings


class ConversionTestHelper:
    """
    Helper class for E2E currency conversion tests

    Provides methods to:
    - Execute complete conversion flow
    - Verify balance changes
    - Generate test reports
    """

    def __init__(self, bvnk_api, timeout: int = None):
        """
        Initialize conversion helper

        Args:
            bvnk_api: BVNK API client instance
            timeout: Timeout for conversion completion (default from settings)
        """
        self.bvnk_api = bvnk_api
        self.timeout = timeout or getattr(settings, 'CONVERSION_TIMEOUT', 20)

    def execute_conversion(
            self,
            from_currency: str,
            to_currency: str,
            amount: float
    ) -> Dict[str, Any]:
        """
        Execute complete conversion flow: create quote, accept, wait

        Args:
            from_currency: Source currency code (e.g., 'ETH')
            to_currency: Target currency code (e.g., 'TRX')
            amount: Amount to convert

        Returns:
            Dict containing quote, accept_response, and final_quote
        """
        print(f"\n{'='*70}")
        print(f"EXECUTING CONVERSION: {amount} {from_currency} → {to_currency}")
        print(f"{'='*70}")

        # Create quote
        print("\n[1/3] Creating quote...")
        quote = self.bvnk_api.create_quote(from_currency, to_currency, amount)

        print(f" Quote created:")
        print(f"  UUID: {quote['uuid']}")
        print(f"  Price: {quote['price']}")
        print(f"  Amount Out: {quote['amountOut']}")
        print(f"  Fee: {quote['fee']}")

        # Validate quote structure
        assert_that(quote).contains_key('uuid', 'from', 'to', 'amountIn', 'price')
        assert_that(quote['from']).is_equal_to(from_currency)
        assert_that(quote['to']).is_equal_to(to_currency)
        assert_that(float(quote['amountIn'])).is_equal_to(amount)

        # Accept quote
        print("\n[2/3] Accepting quote...")
        accept_response = self.bvnk_api.accept_quote(quote['uuid'])
        print(f" Quote accepted")

        # Wait for completion
        print(f"\n[3/3] Waiting for transaction to complete (timeout: {self.timeout}s)...")
        try:
            final_quote = self.bvnk_api.wait_for_quote_completion(
                quote['uuid'],
                timeout=self.timeout
            )
            print(f" Transaction completed!")
        except TimeoutError as e:
            print(f"️ Warning: {e}")
            print("Proceeding with balance verification anyway...")
            final_quote = None

        return {
            'quote': quote,
            'accept_response': accept_response,
            'final_quote': final_quote
        }

    def verify_balance_changes(
            self,
            initial_balances: Dict[str, float],
            from_currency: str,
            to_currency: str,
            amount: float
    ) -> Tuple[float, float]:
        """
        Verify that balances changed correctly after conversion

        Args:
            initial_balances: Dict of initial balances {currency: amount}
            from_currency: Source currency that should decrease
            to_currency: Target currency that should increase
            amount: Expected decrease in source currency

        Returns:
            Tuple of (from_currency_change, to_currency_change)
        """
        print(f"\n{'='*70}")
        print("VERIFYING BALANCE CHANGES")
        print(f"{'='*70}")

        # Get final balances
        from utils.bvnk.helpers import get_wallet_balance
        final_wallets = self.bvnk_api.list_wallets()
        final_from = get_wallet_balance(final_wallets, from_currency)
        final_to = get_wallet_balance(final_wallets, to_currency)

        # Calculate changes
        from_change = initial_balances[from_currency] - final_from
        to_change = final_to - initial_balances[to_currency]

        # Print results
        print(f"\n{from_currency}:")
        print(f"  Initial: {initial_balances[from_currency]}")
        print(f"  Final: {final_from}")
        print(f"  Change: -{from_change}")

        print(f"\n{to_currency}:")
        print(f"  Initial: {initial_balances[to_currency]}")
        print(f"  Final: {final_to}")
        print(f"  Change: +{to_change}")

        # Verify changes
        print(f"\n{'='*70}")
        print("ASSERTIONS")
        print(f"{'='*70}")

        assert_that(from_change).described_as(
            f"{from_currency} should decrease by {amount}"
        ).is_close_to(amount, 0.0001)
        print(f" {from_currency} decreased by expected amount")

        assert_that(to_change).described_as(
            f"{to_currency} should increase"
        ).is_greater_than(0)
        print(f" {to_currency} increased (received {to_change})")

        print(f"\n{'='*70}")
        print(f" CONVERSION VERIFIED: {amount} {from_currency} → {to_change} {to_currency}")
        print(f"{'='*70}\n")

        return from_change, to_change

    def verify_sufficient_balance(
            self,
            balances: Dict[str, float],
            currency: str,
            required_amount: float
    ):
        """
        Verify that wallet has sufficient balance for conversion

        Args:
            balances: Dict of current balances
            currency: Currency to check
            required_amount: Minimum required amount
        """
        current_balance = balances.get(currency, 0)
        assert_that(current_balance).described_as(
            f"Insufficient {currency} balance"
        ).is_greater_than_or_equal_to(required_amount)
        print(f" Sufficient {currency} balance: {current_balance} >= {required_amount}")