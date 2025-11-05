from playwright.sync_api import Page, expect
from config.settings import settings

class BasePage:
    """
    Base Page Object Model class with common methods for all page objects.

    Design Pattern: Page Object Model (POM) for UI/Browser testing with Playwright

    All page-specific classes should inherit from BasePage:
        class LoginPage(BasePage):
            # Page-specific methods

    Example:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("user", "pass")
    """

    def __init__(self, page: Page):
        """
        Initialize base page with Playwright page instance.
        """
        self.page = page
        self.timeout = settings.TIMEOUT

    def navigate(self, path: str = ""):
        """
        Navigate to a URL constructed from base URL and path.

        Combines settings.BASE_URL with provided path to create full URL.
        Useful for navigating to different pages of the same application.

        Args:
            path: Relative path to append to base URL (e.g., "/login", "/dashboard")
                 If empty, navigates to base URL

        Example:
            # settings.BASE_URL = "https://bvnk.com"
            self.navigate("/login")  # Goes to https://bvnk.com/login
            self.navigate()          # Goes to https://bvnk.com
        """
        url = f"{settings.BASE_URL}{path}"
        self.page.goto(url)

    def click(self, selector: str):
        """
        Click an element using CSS selector.
        Waits for element to be clickable before clicking.
        Uses default timeout from settings.
        Args:
            selector: CSS selector (e.g., "#login-button", ".submit-btn")
        Raises:
            TimeoutError: If element not found/clickable within timeout
        """
        self.page.click(selector, timeout=self.timeout)

    def fill(self, selector: str, text: str):
        """
        Fill input field with text.
        Clears existing text and types new text into input field.
        Waits for element to be visible and enabled.
        Args:
            selector: CSS selector for input field
            text: Text to enter into the field
        Example:
            self.fill("#username", "john_doe")
            self.fill("input[name='email']", "john@example.com")
        """
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """
        Get visible text content of an element.
        Returns the text content visible to users
        Args:
            selector: CSS selector for the element
        Example:
            error_msg = self.get_text(".error-message")
            assert "Invalid credentials" in error_msg
        """
        return self.page.locator(selector).inner_text()

    def wait_for_element(self, selector: str):
        """
        Explicitly waits for element to appear and be visible.
        Args:
            selector: CSS selector for the element
        Example:
            # Wait for success message after form submission
            self.wait_for_element(".success-message")
        """
        self.page.wait_for_selector(selector, state="visible", timeout=self.timeout)

    def is_visible(self, selector: str) -> bool:
        """
        Check if element is currently visible (non-blocking).
        Does not wait - returns immediate True/False.
        Use for conditional logic in tests.
        Args:
            selector: CSS selector for the element
        Returns:
            True if element is visible, False otherwise
        Example:
            if self.is_visible(".error-message"):
                error_text = self.get_text(".error-message")
                logger.error(f"Error displayed: {error_text}")
        """
        return self.page.locator(selector).is_visible()

    def take_screenshot(self, name: str):
        """Take screenshot"""
        self.page.screenshot(path=f"reports/screenshots/{name}.png")