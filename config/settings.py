"""
Configuration settings for the test framework
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""

    # BVNK API Configuration
    BVNK_API_BASE_URL = os.getenv(
        'BVNK_API_BASE_URL',
        'http://bvnksimulator.pythonanywhere.com'
    )

    # E2E Test Configuration
    CONVERSION_TIMEOUT = int(os.getenv('CONVERSION_TIMEOUT', '30'))

    # Functional Test Configuration
    QUOTE_EXPIRY_WAIT_TIME = int(os.getenv('QUOTE_EXPIRY_WAIT_TIME', '22'))  # NEW - replaces QUOTE_EXPIRY_SECONDS
    MIN_EXPECTED_WALLETS = int(os.getenv('MIN_EXPECTED_WALLETS', '3'))

    # Business Logic Configuration
    SERVICE_FEE_PERCENT = float(os.getenv('SERVICE_FEE_PERCENT', '0.0001'))  # 0.01% fee

    # Reporting Configuration
    REPORT_DIR = 'reports'
    ALLURE_RESULTS_DIR = 'reports/allure-results'


settings = Settings()