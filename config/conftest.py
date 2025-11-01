"""
Pytest configuration and fixtures for all tests
"""
import pytest
import requests
from playwright.sync_api import sync_playwright
from config.settings import settings


# ============================================
# API Testing Fixtures
# ============================================

@pytest.fixture
def api_client():
    """
    Fixture that provides a requests session for API testing
    with automatic header setup and cleanup
    """
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })

    # Add authentication if needed
    if hasattr(settings, 'API_KEY') and settings.API_KEY:
        session.headers.update({
            'Authorization': f'Bearer {settings.API_KEY}'
        })

    yield session

    # Cleanup
    session.close()


@pytest.fixture
def api_base_url():
    """Fixture that provides the API base URL"""
    return settings.API_BASE_URL


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
    """Fixture that provides test user data"""
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
# Configuration Hooks
# ============================================

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "frontend: Desktop web tests")
    config.addinivalue_line("markers", "backend: Backend/API tests")
    config.addinivalue_line("markers", "mobile: Mobile web tests")
    config.addinivalue_line("markers", "mobile_app: Native mobile app tests")
    config.addinivalue_line("markers", "android: Android specific tests")
    config.addinivalue_line("markers", "ios: iOS specific tests")
    config.addinivalue_line("markers", "slow: Slow running tests")