from pages.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    """Login page object"""

    # Locators (like constants in Java)
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    REMEMBER_ME_CHECKBOX = "#rememberMe"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/login"

    def open(self):
        """Navigate to login page"""
        self.navigate(self.url)
        return self

    def enter_username(self, username: str):
        """Enter username"""
        self.fill(self.USERNAME_INPUT, username)
        return self  # Fluent interface

    def enter_password(self, password: str):
        """Enter password"""
        self.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """Complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Check if error message is visible"""
        return self.is_visible(self.ERROR_MESSAGE)

    def check_remember_me(self):
        """Check remember me checkbox"""
        self.click(self.REMEMBER_ME_CHECKBOX)
        return self