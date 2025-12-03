"""
Base Test Class for BVNK API Tests (NEW FILE)

ADDRESSES FEEDBACK:
- Provides centralized test setup/teardown
- Common assertion methods
- Shared test utilities
- Consistent error handling
- Base logging configuration

USAGE:
Tests can inherit from this class to get shared functionality,
or continue using function-based tests with fixtures (both are valid).

Example:
    class TestConversions(BaseBVNKTest):
        def test_eth_conversion(self):
            # Can use self.assert_balance_changed(), etc.
            pass
"""
import pytest
from typing import Dict, List, Any
from assertpy import assert_that
from utils.logger import logger
from utils.bvnk.helpers import get_wallet_balance, get_wallet_by_currency


class BaseBVNKTest:
    """
    Base class for BVNK API tests providing shared functionality

    Benefits:
    - Centralized setup/teardown
    - Common assertion methods
    - Consistent logging
    - Reusable helper methods
    - Test isolation

    Note: This is optional - tests can still use function-based approach with fixtures.
    This class is provided to address feedback about lacking base class.
    """

    # ============================================
    # SETUP & TEARDOWN
    # ============================================

    @pytest.fixture(autouse=True)
    def base_setup(self, bvnk_api):
        """
        Automatic setup for all tests inheriting from this class

        Sets up:
        - API client reference
        - Initial state capture
        - Test logging

        Runs before each test method automatically.
        """
        self.api = bvnk_api
        self.test_name = self._get_test_name()

        logger.info(f"{'=' * 70}")
        logger.info(f"Starting test: {self.test_name}")
        logger.info(f"{'=' * 70}")

        # Capture initial state for comparison
        self.initial_wallets = self._get_all_wallets()

        yield  # Test runs here

        # Teardown
        logger.info(f"Completed test: {self.test_name}")
        logger.info(f"{'=' * 70}\n")

    # ============================================
    # HELPER METHODS
    # ============================================

    def _get_test_name(self) -> str:
        """Get current test method name"""
        import inspect
        return inspect.currentframe().f_back.f_back.f_code.co_name

    def _get_all_wallets(self) -> List[Dict[str, Any]]:
        """Get all wallets for the account"""
        try:
            return self.api.list_wallets()
        except Exception as e:
            logger.error(f"Failed to retrieve wallets: {e}")
            return []

    def _get_wallet_balances(self) -> Dict[str, float]:
        """
        Get current balances for all wallets

        Returns:
            Dict mapping currency code to balance
        """
        wallets = self._get_all_wallets()
        balances = {}

        for wallet in wallets:
            currency_code = wallet.get('currency', {}).get('code', '')
            if currency_code:
                balances[currency_code] = float(wallet.get('balance', 0))

        return balances

    # ============================================
    # ASSERTION METHODS
    # ============================================

    def assert_wallet_exists(self, currency: str):
        """
        Assert that a wallet exists for the given currency

        Args:
            currency: Currency code (e.g., 'ETH')

        Raises:
            AssertionError: If wallet doesn't exist
        """
        wallets = self._get_all_wallets()
        wallet = get_wallet_by_currency(wallets, currency)

        assert_that(wallet).is_not_none()
        logger.debug(f"✓ Wallet exists for {currency}")

    def assert_balance_changed(
        self,
        currency: str,
        initial_balance: float,
        expected_change: float,
        tolerance: float = 0.001
    ):
        """
        Assert that balance changed by expected amount

        Args:
            currency: Currency code
            initial_balance: Balance before operation
            expected_change: Expected change (negative for decrease)
            tolerance: Allowed difference for floating point comparison

        Raises:
            AssertionError: If balance change doesn't match expected
        """
        wallets = self._get_all_wallets()
        current_balance = get_wallet_balance(wallets, currency)
        actual_change = current_balance - initial_balance

        logger.info(f"{currency} balance change: {initial_balance} -> {current_balance} (Δ {actual_change})")

        assert_that(abs(actual_change - expected_change)).is_less_than(tolerance)
        logger.debug(f"✓ Balance change verified within tolerance")

    def assert_balance_decreased(self, currency: str, initial_balance: float):
        """
        Assert that balance decreased (for any amount)

        Args:
            currency: Currency code
            initial_balance: Balance before operation
        """
        current_balance = get_wallet_balance(self._get_all_wallets(), currency)

        assert_that(current_balance).is_less_than(initial_balance)
        logger.debug(f"✓ {currency} balance decreased: {initial_balance} -> {current_balance}")

    def assert_balance_increased(self, currency: str, initial_balance: float):
        """
        Assert that balance increased (for any amount)

        Args:
            currency: Currency code
            initial_balance: Balance before operation
        """
        current_balance = get_wallet_balance(self._get_all_wallets(), currency)

        assert_that(current_balance).is_greater_than(initial_balance)
        logger.debug(f"✓ {currency} balance increased: {initial_balance} -> {current_balance}")

    def assert_sufficient_balance(self, currency: str, required_amount: float):
        """
        Assert that wallet has sufficient balance

        Args:
            currency: Currency code
            required_amount: Required amount

        Raises:
            AssertionError: If balance is insufficient
        """
        current_balance = get_wallet_balance(self._get_all_wallets(), currency)

        assert_that(current_balance).is_greater_than_or_equal_to(required_amount)
        logger.debug(f"✓ Sufficient {currency} balance: {current_balance} >= {required_amount}")

    def assert_quote_valid(self, quote: Dict[str, Any]):
        """
        Assert that quote response has valid structure

        Args:
            quote: Quote response dict

        Raises:
            AssertionError: If quote structure is invalid
        """
        assert_that(quote).contains_key('uuid', 'price', 'from', 'to')
        logger.debug(f"✓ Quote structure valid: {quote.get('uuid')}")

    # ============================================
    # CONVENIENCE METHODS
    # ============================================

    def get_balance(self, currency: str) -> float:
        """
        Get current balance for a currency

        Args:
            currency: Currency code

        Returns:
            Current balance as float
        """
        return get_wallet_balance(self._get_all_wallets(), currency)

    def create_conversion_quote(
        self,
        from_currency: str,
        to_currency: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        Create a conversion quote

        Args:
            from_currency: Source currency
            to_currency: Target currency
            amount: Amount to convert

        Returns:
            Quote response dict
        """
        logger.info(f"Creating quote: {amount} {from_currency} -> {to_currency}")
        quote = self.api.create_quote(from_currency, to_currency, amount)
        logger.debug(f"Quote created: {quote.get('uuid')}")
        return quote

    def execute_conversion(
        self,
        from_currency: str,
        to_currency: str,
        amount: float,
        wait_for_completion: bool = True,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Execute a complete conversion workflow

        Args:
            from_currency: Source currency
            to_currency: Target currency
            amount: Amount to convert
            wait_for_completion: Whether to wait for completion
            timeout: Timeout for completion wait

        Returns:
            Final quote dict
        """
        quote = self.create_conversion_quote(from_currency, to_currency, amount)

        logger.info(f"Accepting quote: {quote['uuid']}")
        self.api.accept_quote(quote['uuid'])

        if wait_for_completion:
            logger.info(f"Waiting for conversion to complete (timeout: {timeout}s)")
            final_quote = self.api.wait_for_quote_completion(quote['uuid'], timeout=timeout)
            logger.info("Conversion completed successfully")
            return final_quote
        else:
            return quote


# ============================================
# EXAMPLE USAGE
# ============================================

class TestConversionExample(BaseBVNKTest):
    """
    Example test class using BaseBVNKTest

    Shows how to use inherited functionality
    """

    @pytest.mark.skip(reason="Example only")
    def test_eth_to_trx_conversion(self):
        """Example: Test ETH to TRX conversion using base class"""

        # Use inherited methods
        initial_eth = self.get_balance('ETH')
        initial_trx = self.get_balance('TRX')

        # Use assertion method
        self.assert_sufficient_balance('ETH', 1.0)

        # Use convenience method
        final_quote = self.execute_conversion('ETH', 'TRX', 1.0)

        # Use assertion methods
        self.assert_balance_decreased('ETH', initial_eth)
        self.assert_balance_increased('TRX', initial_trx)
        self.assert_balance_changed('ETH', initial_eth, -1.0, tolerance=0.01)
