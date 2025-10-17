"""
Framework Verification Test Suite
Tests that all components are working correctly
"""
import pytest
from playwright.sync_api import sync_playwright
import requests
from config.settings import settings


class TestFrameworkVerification:
    """Verify all framework components"""

    def test_config_loads(self):
        """Test that configuration loads correctly"""
        print('\n Testing Configuration...')
        assert settings.BASE_URL is not None
        assert settings.BROWSER is not None
        assert settings.TIMEOUT > 0
        print(f' Config BASE_URL: {settings.BASE_URL}')
        print(f' Config BROWSER: {settings.BROWSER}')
        print(f' Config TIMEOUT: {settings.TIMEOUT}')

    def test_requests_library(self):
        """Test that requests library works for API calls"""
        print('\n Testing Requests Library...')
        response = requests.get('https://httpbin.org/get')
        assert response.status_code == 200
        print(f' Requests library works! Status: {response.status_code}')

        data = response.json()
        assert 'url' in data
        print(f' JSON parsing works!')

    def test_playwright_chromium(self):
        """Test Playwright with Chromium browser"""
        print('\n Testing Playwright with Chromium...')
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto('https://example.com')

            assert 'Example Domain' in page.title()
            print(f' Chromium launched successfully')
            print(f' Page title: {page.title()}')

            heading = page.locator('h1').text_content()
            assert 'Example Domain' in heading
            print(f' Element interaction works!')

            browser.close()

    def test_playwright_firefox(self):
        """Test Playwright with Firefox browser"""
        print('\n Testing Playwright with Firefox...')
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.goto('https://example.com')

            assert page.title() is not None
            print(f' Firefox launched successfully')

            browser.close()

    def test_playwright_webkit(self):
        """Test Playwright with WebKit browser"""
        print('\n Testing Playwright with WebKit...')
        with sync_playwright() as p:
            browser = p.webkit.launch(headless=True)
            page = browser.new_page()
            page.goto('https://example.com')

            assert page.title() is not None
            print(f' WebKit launched successfully')

            browser.close()

    def test_api_call(self):
        """Test making API calls"""
        print('\n Testing API Calls...')
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

        assert response.status_code == 200
        data = response.json()
        assert 'userId' in data
        assert 'id' in data
        assert 'title' in data

        print(f' API call successful')
        print(f' Response contains expected fields')


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])