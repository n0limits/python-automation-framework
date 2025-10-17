from playwright.sync_api import Page, expect
from config.settings import settings

class BasePage:
    """Base page class with common methods for all pages"""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.TIMEOUT

    def navigate(self, path: str = ""):
        """Navigate to a URL"""
        url = f"{settings.BASE_URL}{path}"
        self.page.goto(url)

    def click(self, selector: str):
        """Click an element"""
        self.page.click(selector, timeout=self.timeout)

    def fill(self, selector: str, text: str):
        """Fill input field"""
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Get element text"""
        return self.page.locator(selector).inner_text()

    def wait_for_element(self, selector: str):
        """Wait for element to be visible"""
        self.page.wait_for_selector(selector, state="visible", timeout=self.timeout)

    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return self.page.locator(selector).is_visible()

    def take_screenshot(self, name: str):
        """Take screenshot"""
        self.page.screenshot(path=f"reports/screenshots/{name}.png")