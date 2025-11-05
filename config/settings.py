"""
Configuration settings for the test framework
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Centralized configuration settings for the test framework.

    Design Pattern: Configuration Object Pattern

    All settings are loaded from environment variables with sensible defaults.
    This allows easy configuration override per environment without code changes.

    Configuration Hierarchy:
    1. Environment variables (highest priority)
    2. .env file (if present)
    3. Hardcoded defaults (fallback)

    Benefits:
    - Single source of truth for all configuration
    - Easy environment-specific overrides
    - Type conversion handled centrally
    - Sensible defaults for quick setup

    Usage:
        from config.settings import settings

        base_url = settings.BVNK_API_BASE_URL
        timeout = settings.CONVERSION_TIMEOUT
    """

    # BVNK API Configuration
    """
    Base URL for BVNK API simulator.
    Override via environment variable: BVNK_API_BASE_URL=https://custom-url.com
    """
    BVNK_API_BASE_URL = os.getenv(
        'BVNK_API_BASE_URL',
        'http://bvnksimulator.pythonanywhere.com'
    )

    # E2E Test Configuration
    CONVERSION_TIMEOUT = int(os.getenv('CONVERSION_TIMEOUT', '30'))
    """
    Maximum time (seconds) to wait for conversion completion.
    Default: 30 seconds
    Increase for slower networks or complex conversions.
    """

    # Functional Test Configuration
    QUOTE_EXPIRY_WAIT_TIME = int(os.getenv('QUOTE_EXPIRY_WAIT_TIME', '22'))
    """
    Time (seconds) to wait before expecting quote expiry.
    
    API specifies quotes expire after 20 seconds.
    We use 22 seconds (20 + 2 buffer) to ensure expiry has occurred.
    """

    MIN_EXPECTED_WALLETS = int(os.getenv('MIN_EXPECTED_WALLETS', '3'))
    """
    Minimum number of wallets expected in a new account.
    Used for validation in wallet listing tests.
    """

    # Business Logic Configuration
    SERVICE_FEE_PERCENT = float(os.getenv('SERVICE_FEE_PERCENT', '0.0001'))
    """
    Service fee percentage or currency conversions.
    Service fee for all conversions/trades is 0.01%
    0.01% as decimal = 0.01 / 100 = 0.0001
    Example: For 1.0 ETH conversion, fee = 1.0 * 0.0001 = 0.0001 ETH
    """

    # Reporting Configuration
    REPORT_DIR = 'reports'
    ALLURE_RESULTS_DIR = 'reports/allure-results'


settings = Settings()