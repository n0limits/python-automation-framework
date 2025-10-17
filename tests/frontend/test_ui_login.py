import pytest
from assertpy import assert_that
from config.settings import settings

@pytest.mark.frontend
@pytest.mark.smoke
def test_login_success(page):
    """Test successful login"""
    # Navigate
    page.goto(f"{settings.BASE_URL}/login")

    # Interact
    page.fill("#username", "testuser")
    page.fill("#password", "password123")
    page.click("button[type='submit']")

    # Assert (like AssertJ)
    assert_that(page.url).contains("/dashboard")
    assert_that(page.locator("h1").inner_text()).is_equal_to("Welcome")

@pytest.mark.frontend
def test_login_invalid_credentials(page):
    """Test login with invalid credentials"""
    page.goto(f"{settings.BASE_URL}/login")
    page.fill("#username", "invalid")
    page.fill("#password", "wrong")
    page.click("button[type='submit']")

    error_message = page.locator(".error-message").inner_text()
    assert_that(error_message).contains("Invalid credentials")