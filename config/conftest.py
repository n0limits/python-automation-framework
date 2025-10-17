import pytest
from playwright.sync_api import sync_playwright
from config.settings import settings

@pytest.fixture(scope="session")
def browser():
    """Browser fixture - runs once per session"""
    with sync_playwright() as p:
        if settings.BROWSER == "firefox":
            browser = p.firefox.launch(headless=settings.HEADLESS)
        elif settings.BROWSER == "webkit":
            browser = p.webkit.launch(headless=settings.HEADLESS)
        else:
            browser = p.chromium.launch(headless=settings.HEADLESS)

        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """Page fixture - new page for each test"""
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(settings.TIMEOUT)

    yield page

    context.close()

@pytest.fixture(scope="session")
def api_client():
    """API client fixture"""
    import requests
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})

    yield session

    session.close()