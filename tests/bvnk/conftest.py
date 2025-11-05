"""
BVNK-specific test fixtures
Provides helper fixtures for BVNK API testing
"""
import pytest
import requests

from utils.bvnk.api_client import BVNKApiClient
from utils.bvnk.helpers import get_wallet_balance, calculate_expected_fee
from config.settings import settings


# ============================================
# BVNK Helper Fixtures
# ============================================

@pytest.fixture
def wallet_balances(bvnk_api):
    """
    Fixture that provides initial wallet balances.

    Retrieves balances at start of test for before/after comparison.

    Usage:
        def test_conversion(bvnk_api, wallet_balances):
            initial_eth = wallet_balances['ETH']
            # ... do conversion ...
            # verify balance changed

    Returns:
        Dict with currency codes as keys and balances as values
        Example: {'ETH': 10.0, 'TRX': 50000.0, 'USDT': 1000.0}
    """
    wallets = bvnk_api.list_wallets()
    balances = {}

    for wallet in wallets:
        currency_obj = wallet.get('currency', {})
        currency_code = currency_obj.get('code', '')

        if currency_code:
            balance_str = wallet.get('balance', '0')
            balances[currency_code] = float(balance_str)

    print(f"\nInitial wallet balances: {balances}")
    return balances


@pytest.fixture
def create_and_accept_quote(bvnk_api):
    """
    Fixture factory for creating and accepting quotes.

    Simplifies E2E conversion tests by handling quote workflow.

    Usage:
        def test_conversion(bvnk_api, create_and_accept_quote):
            quote, result = create_and_accept_quote('ETH', 'TRX', 1.0)
            assert result['status'] == 'success'

    Returns:
        Function that creates and accepts quotes
    """
    def _create_and_accept(from_currency, to_currency, amount):
        """
        Create and accept a quote

        Args:
            from_currency: Source currency (e.g., 'ETH')
            to_currency: Target currency (e.g., 'TRX')
            amount: Amount to convert

        Returns:
            Tuple of (quote_response, accept_response)
        """
        print(f"\nCreating quote: {amount} {from_currency} -> {to_currency}")

        # Create quote
        quote = bvnk_api.create_quote(from_currency, to_currency, amount)
        print(f"Quote created: UUID={quote['uuid']}, Price={quote.get('price', 'N/A')}")

        # Accept quote
        accept_response = bvnk_api.accept_quote(quote['uuid'])
        print(f"Quote accepted: {accept_response}")

        return quote, accept_response

    return _create_and_accept


@pytest.fixture
def verify_balance_change(bvnk_api):
    """
    Fixture that provides a function to verify balance changes.

    Compares current balances with initial balances and expected changes.

    Usage:
        def test_conversion(bvnk_api, wallet_balances, verify_balance_change):
            # ... do conversion ...
            verify_balance_change(wallet_balances, {'ETH': -1.0, 'TRX': 50000.0})

    Returns:
        Function to verify balance changes
    """
    def _verify(initial_balances, expected_changes, tolerance=0.001):
        """
        Verify that wallet balances changed as expected

        Args:
            initial_balances: Dict of initial balances {currency: amount}
            expected_changes: Dict of expected changes {currency: change_amount}
            tolerance: Allowed difference for floating point comparison
        """
        current_wallets = bvnk_api.list_wallets()

        print("\n" + "="*60)
        print("BALANCE VERIFICATION")
        print("="*60)

        for currency, expected_change in expected_changes.items():
            initial = initial_balances.get(currency, 0)
            current = get_wallet_balance(current_wallets, currency)
            actual_change = current - initial

            print(f"\n{currency}:")
            print(f"  Initial balance: {initial}")
            print(f"  Current balance: {current}")
            print(f"  Expected change: {expected_change}")
            print(f"  Actual change:   {actual_change}")
            print(f"  Difference:      {abs(actual_change - expected_change)}")

            # Verify within tolerance
            assert abs(actual_change - expected_change) < tolerance, \
                f"{currency} balance change mismatch: expected {expected_change}, got {actual_change}"

            print(f"  Status: PASS ✓")

    return _verify


@pytest.fixture
def get_balances_for_currencies(bvnk_api):
    """
    Fixture that provides a function to get balances for specific currencies.

    Convenient way to get multiple balances at once.

    Usage:
        def test_something(bvnk_api, get_balances_for_currencies):
            eth, trx = get_balances_for_currencies(['ETH', 'TRX'])

    Returns:
        Function to get balances for list of currencies
    """
    def _get_balances(currencies):
        """
        Get balances for specific currencies

        Args:
            currencies: List of currency codes

        Returns:
            List of balances in the same order as currencies
        """
        wallets = bvnk_api.list_wallets()
        return [get_wallet_balance(wallets, curr) for curr in currencies]

    return _get_balances


@pytest.fixture
def calculate_conversion_with_fee():
    """
    Fixture that calculates expected conversion amounts including fee.

    Uses service fee from settings (0.01% = 0.0001).

    Usage:
        def test_conversion(calculate_conversion_with_fee):
            gross, fee, net = calculate_conversion_with_fee(1.0, 50000.5)

    Returns:
        Function to calculate conversion
    """
    def _calculate(amount, rate):
        """
        Calculate conversion with service fee

        Args:
            amount: Amount to convert
            rate: Exchange rate

        Returns:
            Tuple of (gross_received, fee, net_received)
        """
        gross = amount * rate
        fee = calculate_expected_fee(gross, settings.SERVICE_FEE_PERCENT)
        net = gross - fee

        return gross, fee, net

    return _calculate


@pytest.fixture
def print_test_header():
    """
    Fixture that prints a formatted test header.

    Makes test output more readable.

    Usage:
        def test_something(print_test_header):
            print_test_header("My Test Name")
    """
    def _print_header(test_name):
        """Print formatted test header"""
        print("\n" + "="*70)
        print(f"TEST: {test_name}")
        print("="*70 + "\n")

    return _print_header


# ============================================
# BVNK Test Configuration Hooks
# ============================================

def pytest_configure(config):
    """
    Configure BVNK-specific pytest markers.

    Adds custom markers for better test organization.
    """
    config.addinivalue_line(
        "markers",
        "conversion: Tests related to currency conversion"
    )
    config.addinivalue_line(
        "markers",
        "quote: Tests related to quote operations"
    )
    config.addinivalue_line(
        "markers",
        "wallet: Tests related to wallet operations"
    )
    config.addinivalue_line(
        "markers",
        "authentication: Tests related to authentication"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection for BVNK tests.

    Runs E2E tests before functional tests for logical flow.
    """
    def sort_key(item):
        if "e2e" in item.keywords:
            return 0
        elif "functional" in item.keywords:
            return 1
        else:
            return 2

    items.sort(key=sort_key)


def pytest_sessionstart(session):
    """
    Pytest hook - runs BEFORE test collection

    Performs automatic health check to verify API availability.
    Aborts entire test session if API is not ready.

    This ensures we fail fast and don't waste time running tests
    against an unavailable or unhealthy API.
    """
    health_url = f"{settings.BVNK_API_BASE_URL}/health"

    print("\n" + "="*70)
    print("PRE-SESSION HEALTH CHECK")
    print("="*70)
    print(f"Verifying BVNK API is ready...")
    print(f"Health URL: {health_url}")

    try:
        response = requests.get(health_url, timeout=10)

        if response.status_code != 200:
            print(f"\n API HEALTH CHECK FAILED!")
            print(f"Status Code: {response.status_code}")
            pytest.exit(
                f"\nCannot proceed - API is not healthy!\n"
                f"Please check the API server and try again.\n",
                returncode=1
            )

        health_data = response.json()

        print(f"\n✓ API HEALTH CHECK PASSED")
        print(f"├─ Uptime: {health_data.get('uptime', 'N/A')}")
        print(f"├─ DB Size: {health_data.get('approximate_db_size', 'N/A')}")
        print(f"└─ Total Requests: {health_data.get('total_authenticated_requests', 0)}")
        print("="*70)
        print("Proceeding with test execution...\n")

    except requests.exceptions.RequestException as e:
        print(f"\n API HEALTH CHECK FAILED!")
        print(f"Error: {str(e)}")
        pytest.exit(
            f"\nCannot connect to API at {health_url}\n"
            f"Please check:\n"
            f"  1. API server is running\n"
            f"  2. Network connectivity\n"
            f"  3. Firewall settings\n"
            f"  4. Base URL in settings: {settings.BVNK_API_BASE_URL}\n",
            returncode=1
        )