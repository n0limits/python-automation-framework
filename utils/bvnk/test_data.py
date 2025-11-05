"""
Test Data for BVNK Currency Conversions
Centralized configuration for E2E conversion tests
"""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class ConversionTestCase:
    """
    Test case configuration for currency conversion

    Attributes:
        from_currency: Source currency code
        to_currency: Target currency code
        amount: Amount to convert
        test_name: Descriptive test name
        timeout: Optional custom timeout (uses default if None)
        description: Optional test description
    """
    from_currency: str
    to_currency: str
    amount: float
    test_name: str
    timeout: Optional[int] = None
    description: Optional[str] = None

    def __str__(self):
        return f"{self.test_name}: {self.amount} {self.from_currency} → {self.to_currency}"


# Test data for E2E conversion tests
CONVERSION_TEST_CASES = {
    'eth_to_trx': ConversionTestCase(
        from_currency='ETH',
        to_currency='TRX',
        amount=1.0,
        test_name='Convert 1 ETH to TRX',
        description='E2E test for ETH to TRX conversion'
    ),
    'trx_to_usdt': ConversionTestCase(
        from_currency='TRX',
        to_currency='USDT',
        amount=420.0,
        test_name='Convert 420 TRX to USDT',
        description='E2E test for TRX to USDT conversion'
    ),
    'trx_to_eth': ConversionTestCase(
        from_currency='TRX',
        to_currency='ETH',
        amount=987.0,
        test_name='Convert 987 TRX to ETH',
        description='E2E test for TRX to ETH conversion'
    )
}

# ============================================
# Functional Test Data
# ============================================

@dataclass
class ErrorStatusCodes:
    """Expected error status codes for different scenarios"""
    QUOTE_EXPIRED: List[int] = field(default_factory=lambda: [400, 404, 410, 412])
    INSUFFICIENT_BALANCE: List[int] = field(default_factory=lambda: [400, 412, 422])


@dataclass
class QuoteExpiryTestCase:
    """Test case for quote expiry validation"""
    from_currency: str = 'ETH'
    to_currency: str = 'TRX'
    amount: float = 0.1
    wait_time: Optional[int] = None  # Uses settings default if None
    test_name: str = 'Quote Expiry'


@dataclass
class InsufficientBalanceTestCase:
    """Test case for insufficient balance validation"""
    from_currency: str = 'ETH'
    to_currency: str = 'TRX'
    balance_excess: float = 1000.0  # How much to exceed balance by
    test_name: str = 'Insufficient Balance'


@dataclass
class FeeCalculationTestCase:
    """Test case for fee calculation"""
    from_currency: str = 'ETH'
    to_currency: str = 'TRX'
    amount: float = 1.0
    test_name: str = 'Service Fee Calculation'


# Test configuration instances
ERROR_STATUS_CODES = ErrorStatusCodes()

FUNCTIONAL_TEST_CASES = {
    'quote_expiry': QuoteExpiryTestCase(),
    'insufficient_balance': InsufficientBalanceTestCase(),
    'fee_calculation': FeeCalculationTestCase()
}


def get_test_case(key: str) -> ConversionTestCase:
    """
    Get test case by key

    Args:
        key: Test case key (e.g., 'eth_to_trx')

    Returns:
        ConversionTestCase instance
    """
    return CONVERSION_TEST_CASES[key]
