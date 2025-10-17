import pytest
from playwright.sync_api import sync_playwright
from config.settings import settings

def test_playwright_chromium():
    '''Test Playwright with Chromium'''
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://example.com')
        assert 'Example Domain' in page.title()
        print('✅ Chromium test passed!')
        browser.close()

def test_config_loads():
    '''Test that config settings load correctly'''
    assert settings.BASE_URL is not None
    print(f'✅ Config loaded: BASE_URL = {settings.BASE_URL}')

def test_requests_works():
    '''Test that requests library works'''
    import requests
    response = requests.get('https://httpbin.org/get')
    assert response.status_code == 200
    print('✅ Requests library works!')

if __name__ == '__main__':
    print('\n=== Running Verification Tests ===\n')
    test_config_loads()
    test_requests_works()
    test_playwright_chromium()
    print('\n🎉 All verification tests passed!\n')
