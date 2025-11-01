"""
Framework Verification Tests
Tests that all framework components are properly installed and configured
"""
import pytest
import requests
from playwright.sync_api import sync_playwright
from config.settings import settings


class TestFrameworkVerification:
    """Comprehensive framework verification tests"""

    def test_imports(self):
        """Verify all required packages are installed"""
        print('\n' + '='*60)
        print('Testing Package Imports')
        print('='*60)

        # Test pytest
        import pytest
        print(f'pytest {pytest.__version__}')

        # Test playwright
        import playwright
        print(f'playwright installed')

        # Test requests
        import requests
        print(f'requests {requests.__version__}')

        # Test dotenv
        from dotenv import load_dotenv
        print(f'python-dotenv installed')

        # Test assertpy
        from assertpy import assert_that
        print(f'assertpy installed')

        # Test faker
        from faker import Faker
        print(f'faker installed')

        print('\nAll imports successful!')

    def test_basic_assertions(self):
        """Test that pytest assertions work"""
        print('\n' + '='*60)
        print('Testing Basic Assertions')
        print('='*60)

        assert 1 + 1 == 2
        assert "hello".upper() == "HELLO"
        assert [1, 2, 3] == [1, 2, 3]

        print('Basic assertions work!')

    def test_assertpy_assertions(self):
        """Test assertpy fluent assertions"""
        print('\n' + '='*60)
        print('Testing Assertpy (Fluent Assertions)')
        print('='*60)

        from assertpy import assert_that

        assert_that(5).is_greater_than(3)
        assert_that("hello").starts_with("he")
        assert_that([1, 2, 3]).contains(2)

        print('Assertpy fluent assertions work!')

    def test_config_loads(self):
        """Test that configuration loads correctly"""
    print('\n' + '='*60)
    print('Testing Configuration Loading')
    print('='*60)

    # Check which attributes exist
    print('Available configuration:')

    if hasattr(settings, 'BASE_URL'):
        print(f'BASE_URL: {settings.BASE_URL}')

    if hasattr(settings, 'API_BASE_URL'):
        print(f'API_BASE_URL: {settings.API_BASE_URL}')

    if hasattr(settings, 'BVNK_API_BASE_URL'):
        assert settings.BVNK_API_BASE_URL is not None
        print(f'BVNK_API_BASE_URL: {settings.BVNK_API_BASE_URL}')

    if hasattr(settings, 'BROWSER'):
        print(f'BROWSER: {settings.BROWSER}')

    if hasattr(settings, 'HEADLESS'):
        assert settings.HEADLESS is not None
        print(f'HEADLESS: {settings.HEADLESS}')

    if hasattr(settings, 'TIMEOUT'):
        assert settings.TIMEOUT > 0
        print(f'TIMEOUT: {settings.TIMEOUT}')

    if hasattr(settings, 'SERVICE_FEE_PERCENT'):
        print(f'SERVICE_FEE_PERCENT: {settings.SERVICE_FEE_PERCENT}%')

    print('\nConfiguration loads correctly!')

    def test_requests_library(self):
        """Test that requests library works for API calls"""
        print('\n' + '='*60)
        print('Testing Requests Library')
        print('='*60)

        response = requests.get('https://httpbin.org/get')
        assert response.status_code == 200
        print(f'GET request successful: Status {response.status_code}')

        data = response.json()
        assert 'url' in data
        print(f'JSON parsing works!')

        # Test POST
        response = requests.post('https://httpbin.org/post', json={'test': 'data'})
        assert response.status_code == 200
        print(f'POST request works!')

        print('\nRequests library fully functional!')

    def test_faker_data_generation(self):
        """Test Faker for test data generation"""
        print('\n' + '='*60)
        print('Testing Faker (Test Data Generation)')
        print('='*60)

        from faker import Faker
        fake = Faker()

        name = fake.name()
        email = fake.email()
        address = fake.address()

        assert len(name) > 0
        assert '@' in email
        assert len(address) > 0

        print(f'Generated name: {name}')
        print(f'Generated email: {email}')
        print(f'Faker working correctly!')

    def test_playwright_chromium(self):
        """Test Playwright with Chromium browser"""
        print('\n' + '='*60)
        print('Testing Playwright - Chromium')
        print('='*60)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto('https://example.com')

            assert 'Example Domain' in page.title()
            print(f'Page loaded: {page.title()}')

            heading = page.locator('h1').text_content()
            assert 'Example Domain' in heading
            print(f'Element interaction works: {heading}')

            browser.close()
            print('\nChromium browser works!')

    def test_playwright_firefox(self):
        """Test Playwright with Firefox browser"""
        print('\n' + '='*60)
        print('Testing Playwright - Firefox')
        print('='*60)

        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.goto('https://example.com')

            assert page.title() is not None
            print(f'Firefox loaded: {page.title()}')

            browser.close()
            print('\nFirefox browser works!')

    def test_playwright_webkit(self):
        """Test Playwright with WebKit (Safari)"""
        print('\n' + '='*60)
        print('Testing Playwright - WebKit')
        print('='*60)

        with sync_playwright() as p:
            browser = p.webkit.launch(headless=True)
            page = browser.new_page()
            page.goto('https://example.com')

            assert page.title() is not None
            print(f'WebKit loaded: {page.title()}')

            browser.close()
            print('\nWebKit browser works!')

    def test_api_json_placeholder(self):
        """Test API calls with JSONPlaceholder"""
        print('\n' + '='*60)
        print('Testing API Calls')
        print('='*60)

        # GET request
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        assert response.status_code == 200

        data = response.json()
        assert 'userId' in data
        assert 'id' in data
        assert 'title' in data
        assert 'body' in data

        print(f'GET request successful')
        print(f'Post ID: {data["id"]}')
        print(f'Post Title: {data["title"][:50]}...')

        print('\nAPI calls working correctly!')


# Optional: Quick standalone tests (not in class)
def test_quick_smoke():
    """Quick smoke test - runs first"""
    print('\nQUICK SMOKE TEST')
    assert 1 + 1 == 2
    print('Framework is alive!')


if __name__ == '__main__':
    print('\n' + '='*70)
    print('FRAMEWORK VERIFICATION TEST SUITE')
    print('='*70)
    print('\nRunning all verification tests...\n')

    pytest.main([__file__, '-v', '-s'])