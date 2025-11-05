import functools
import time

import requests

from config import settings
from utils.logger import Logger

logger = Logger()

def retry(max_attempts: int = 3, delay: int = 1):
    """
    Decorator Pattern for automatic retry of flaky test operations.

    Design Pattern: Decorator Pattern
    Use Case: Network calls, UI interactions, timing-dependent operations

    Automatically retries a function if it raises an exception, useful for:
    - Flaky API calls due to network issues
    - UI elements that load slowly or inconsistently
    - Database operations that might temporarily fail
    - Any operation with transient failures

    Modify the delay parameter between attempts

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
                     Total executions = max_attempts (includes initial attempt)
        delay: Time in seconds to wait between retries (default: 1)

    Returns:
        Decorated function that will retry on failure

    Behavior:
    - On success: Returns result immediately
    - On failure: Waits 'delay' seconds and retries
    - After max_attempts: Re-raises the last exception
    - Logs each retry attempt for debugging

    Example:
        @retry(max_attempts=3, delay=2)
        def test_flaky_api():
            response = requests.get("URL)
            assert response.status_code == 200

        # Will retry up to 3 times with 2 second delay between attempts
        # Total max time: 3 attempts × 2 seconds = 6 seconds (plus execution time)

    Warning:
        - Not suitable for operations that should fail immediately
        - Can mask real issues if overused
        - Increases test execution time on failures
        - Use sparingly and only for genuinely flaky operations
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {str(e)}")
                        raise # Re-raise original exception after all retries exhausted
                    logger.warning(f"Attempt {attempts} failed, retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

def screenshot_on_failure(func):
    """
    Decorator for automatic screenshot capture on test failure.
    Use Case: UI/Browser testing with Playwright or Selenium

    Requirements:
    - Test function must have a 'page' attribute in its arguments
    - Page object must have screenshot() method (Playwright/Selenium)
    - reports/screenshots/ directory must exist

    Args:
        func: Test function to decorate

    Note:
        - Only works with browser-based tests
        - Screenshot shows browser state at failure moment
        - Useful for debugging flaky UI tests
        - Can increase test execution time slightly
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Try to get page object from args
            for arg in args:
                if hasattr(arg, 'page'):
                    page = arg.page
                    screenshot_name = f"failure_{func.__name__}_{int(time.time())}"
                    page.screenshot(path=f"reports/screenshots/{screenshot_name}.png")
                    logger.error(f"Screenshot saved: {screenshot_name}.png")
                    break
            raise
    return wrapper

def log_execution_time(func):
    """Log function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Starting: {func.__name__}")

        result = func(*args, **kwargs)

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Finished: {func.__name__} in {execution_time:.2f}s")

        return result
    return wrapper

def api_call_logger(func):
    """
    Decorator for detailed API call logging.

    Automatically logs detailed information about API calls, including:
    - Function name (identifies which API endpoint is being called)
    - Request arguments and keyword arguments
    - HTTP response status code (if response object returned)

    Requirements:
    - Function must return a requests.Response object (or object with status_code)
    - If return value has no status_code, only input logging occurs

    Example:
        @api_call_logger
        def get_user(user_id: int):
            response = requests.get(f"{settings.API_BASE_URL}/users/{user_id}")
            return response

        # Call the function
        user = get_user(123)

    Security Note:
        Be cautious with DEBUG level logging in production:
        - May log sensitive data (passwords, tokens, PII)
        - Consider sanitizing kwargs before logging
        - Use only in test/dev environments

    Best Practice - Combine with Retry:
        @retry(max_attempts=3)
        @api_call_logger
        def get_user(user_id: int):
            # Both decorators work together
            # Logs each retry attempt
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"API Call: {func.__name__}")
        logger.debug(f"Args: {args}, Kwargs: {kwargs}")

        result = func(*args, **kwargs)

        if hasattr(result, 'status_code'):
            logger.info(f"Response Status: {result.status_code}")

        return result
    return wrapper
