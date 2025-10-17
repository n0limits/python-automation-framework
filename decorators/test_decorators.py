import functools
import time
from utils.logger import Logger

logger = Logger()

def retry(max_attempts: int = 3, delay: int = 1):
    """Retry decorator for flaky tests"""
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
                        raise
                    logger.warning(f"Attempt {attempts} failed, retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

def screenshot_on_failure(func):
    """Take screenshot if test fails"""
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
    """Log API call details"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"API Call: {func.__name__}")
        logger.debug(f"Args: {args}, Kwargs: {kwargs}")

        result = func(*args, **kwargs)

        if hasattr(result, 'status_code'):
            logger.info(f"Response Status: {result.status_code}")

        return result
    return wrapper

# Usage in tests
@retry(max_attempts=3, delay=2)
@screenshot_on_failure
@log_execution_time
def test_flaky_element(page):
    """Test that might be flaky"""
    page.goto("https://example.com")
    page.click("#sometimes-missing-button")  # Might not always be there
    assert page.url == "https://example.com/success"

@api_call_logger
def get_user(user_id: int):
    """Get user from API"""
    response = requests.get(f"{settings.API_BASE_URL}/users/{user_id}")
    return response
