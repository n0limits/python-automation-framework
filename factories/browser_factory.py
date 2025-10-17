import pytest
from playwright.sync_api import Browser, sync_playwright
from config.settings import settings
from utils.logger import Logger

logger = Logger()

class BrowserFactory:
    """Factory for creating different browser instances"""

    @staticmethod
    def create_browser(browser_type: str = None) -> Browser:
        """Create browser instance based on type"""
        browser_type = browser_type or settings.BROWSER
        playwright = sync_playwright().start()

        logger.info(f"Creating {browser_type} browser")

        launch_options = {
            "headless": settings.HEADLESS,
            "slow_mo": 100 if not settings.HEADLESS else 0
        }

        if browser_type.lower() == "chrome" or browser_type.lower() == "chromium":
            browser = playwright.chromium.launch(**launch_options)

        elif browser_type.lower() == "firefox":
            browser = playwright.firefox.launch(**launch_options)

        elif browser_type.lower() == "webkit" or browser_type.lower() == "safari":
            browser = playwright.webkit.launch(**launch_options)

        elif browser_type.lower() == "edge":
            browser = playwright.chromium.launch(
                channel="msedge",
                **launch_options
            )
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")

        logger.info(f"{browser_type} browser created successfully")
        return browser

    @staticmethod
    def create_mobile_browser(device_name: str = "iPhone 12"):
        """Create browser with mobile device emulation"""
        playwright = sync_playwright().start()
        device = playwright.devices[device_name]

        browser = playwright.chromium.launch(headless=settings.HEADLESS)
        context = browser.new_context(**device)

        logger.info(f"Mobile browser created for {device_name}")
        return browser, context

# Usage in conftest.py
@pytest.fixture(scope="function")
def browser(request):
    """Browser fixture with factory"""
    browser_type = request.config.getoption("--browser", default="chromium")
    browser = BrowserFactory.create_browser(browser_type)

    yield browser

    browser.close()