import pytest
from playwright.sync_api import Browser, sync_playwright
from config.settings import settings
from utils.logger import Logger

logger = Logger()

class BrowserFactory:
    """
    Factory Pattern for creating browser instances with different configurations.

    Design Pattern: Factory Pattern

    Provides a centralized way to create various browser types and configurations
    without exposing creation logic to tests.
    - Hides complex browser initialization
    - Supports multiple browser types (Chrome, Firefox, Safari, Edge)
    - Supports mobile device emulation
    - Consistent browser configuration across tests
    - Easy to extend with new browser types

    Supported Browsers:
    - CChrome
    - Firefox
    - Safari
    - Edge

    Example:
        browser = BrowserFactory.create_browser("chrome")
        browser, context = BrowserFactory.create_mobile_browser("iPhone 14")
    """

    @staticmethod
    def create_browser(browser_type: str = None) -> Browser:
        """
        Create a browser instance based on type.

        Factory method that encapsulates browser creation logic.
        Handles browser-specific configuration and options.

        Args:
            browser_type: Browser type ('chrome', 'firefox', 'webkit', 'edge')
                         If None, uses settings.BROWSER

        Returns:
            Initialized Playwright Browser instance

        Raises:
            ValueError: If unsupported browser type is specified
        """
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
    def create_mobile_browser(device_name: str = "iPhone 14"):
        """
        Create browser with mobile device emulation.

        Uses Playwright's device descriptor to emulate mobile devices with:
        - Correct viewport size
        - Touch events
        - User agent
        - Device pixel ratio

        Args:
            device_name: Device to emulate (e.g., "iPhone 14", "Pixel 6")
                        See Playwright documentation for full device list

        Returns:
            Tuple of (browser, context) where context has device emulation

        Example:
            browser, context = BrowserFactory.create_mobile_browser("iPhone 14")
            page = context.new_page()
        """
        playwright = sync_playwright().start()
        device = playwright.devices[device_name]

        browser = playwright.chromium.launch(headless=settings.HEADLESS)
        context = browser.new_context(**device)

        logger.info(f"Mobile browser created for {device_name}")
        return browser, context
