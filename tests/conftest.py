"""
Root test fixtures - Base fixtures for all test suites
"""
import pytest
from utils.bvnk.api_client import BVNKApiClient


# ============================================
# BVNK API Testing Fixtures
# ============================================

@pytest.fixture(scope="session")
def bvnk_client():
    """
    Session-scoped BVNK API client.

    Creates one client for entire test session.
    Reuses same account/token across tests (faster but less isolated).

    Usage:
        def test_something(bvnk_client):
            wallets = bvnk_client.list_wallets()
    """
    print("\n" + "="*70)
    print("Creating session BVNK API client...")
    print("="*70)

    client = BVNKApiClient()
    init_response = client.init_account()

    print(f"\nSession account initialized. Token expires: {init_response.get('expiry', 'Unknown')}")
    print("="*70)

    yield client

    client.close()


@pytest.fixture(scope="function")
def bvnk_api():
    """
    Function-scoped BVNK API client.

    Creates fresh client with new account for EACH test.
    Use this for tests that modify wallet balances (E2E tests).

    Usage:
        def test_conversion(bvnk_api):
            quote = bvnk_api.create_quote('ETH', 'TRX', 1.0)
    """
    print("\n" + "="*70)
    print("Creating new BVNK API client...")
    print("="*70)

    client = BVNKApiClient()
    init_response = client.init_account()

    print(f"\nAccount setup complete!")
    print(f"Token expires: {init_response.get('expiry', 'Unknown')}")
    print("="*70)

    yield client

    client.close()


@pytest.fixture
def bvnk_base_url():
    """Provides BVNK API base URL from settings"""
    from config.settings import settings
    return settings.BVNK_API_BASE_URL


# ============================================
# Pytest Hooks
# ============================================

def pytest_collection_modifyitems(config, items):
    """
    Hook to modify test collection.
    Runs smoke tests first for faster feedback.
    """
    items.sort(key=lambda item: 0 if "smoke" in item.keywords else 1)