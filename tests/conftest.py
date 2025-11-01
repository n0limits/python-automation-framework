"""
Tests conftest.py - Test fixtures and configuration
Provides fixtures for all test suites
"""
import pytest
import requests
from playwright.sync_api import sync_playwright
from config.settings import settings
from utils.bvnk.api_client import BVNKApiClient


# ============================================
# BVNK API Testing Fixtures
# ============================================

@pytest.fixture(scope="session")
def bvnk_client():
    """
    Session-scoped fixture for BVNK API client
    Initializes account once per test session
    """
    client = BVNKApiClient()

    # Initialize account and get bearer token
    init_response = client.init_account()
    print(f"\nAccount initialized. Token expires: {init_response.get('expiry', 'Unknown')}")

    yield client

    # Cleanup
    client.close()


@pytest.fixture(scope="function")
def bvnk_api():
    """
    Function-scoped fixture for BVNK API client
    Creates fresh client for each test
    """
    client = BVNKApiClient()

    # Initialize account
    init_response = client.init_account()
    print(f"\nTest account created. Token: {init_response.get('token', 'N/A')[:20]}...")

    yield client

    # Cleanup
    client.close()


@pytest.fixture
def bvnk_base_url():
    """Fixture that provides BVNK API base URL"""
    return settings.BVNK_API_BASE_URL


# ============================================
# Generic API Testing Fixtures
# ============================================

@pytest.fixture
def api_client():
    """
    Generic API client fixture using requests
    For testing non-BVNK APIs
    """
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })

    yield session

    session.close()


# ============================================
# Web Testing Fixtures (Playwright)
# ============================================

@pytest.fixture(scope="function")
def browser():
    """Fixture that provides a Playwright browser instance"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=settings.HEADLESS == 'true'
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Fixture that provides a browser context"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Fixture that provides a Playwright page"""
    page = context.new_page()
    yield page
    page.close()


# ============================================
# Test Data Fixtures
# ============================================

@pytest.fixture
def test_user_data():
    """Fixture that provides static test user data"""
    return {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'Test123!@#'
    }


@pytest.fixture
def random_user_data(faker):
    """Fixture that provides random user data using Faker"""
    return {
        'name': faker.name(),
        'email': faker.email(),
        'username': faker.user_name(),
        'password': faker.password()
    }


# ============================================
# Pytest Hooks
# ============================================

def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results
    Can be used for custom reporting or screenshots on failure
    """
    if call.when == "call":
        if call.excinfo is not None:
            # Test failed
            print(f"\nTest failed: {item.name}")


def pytest_collection_modifyitems(config, items):
    """
    Hook to modify test items after collection
    Can be used to add markers, reorder tests, etc.
    """
    # Example: Run smoke tests first
    items.sort(key=lambda item: 0 if "smoke" in item.keywords else 1)