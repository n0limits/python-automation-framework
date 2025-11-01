"""
Configuration settings for the automation framework
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""

    # BVNK API Configuration
    BVNK_API_BASE_URL: str = os.getenv('BVNK_API_BASE_URL', 'http://bvnksimulator.pythonanywhere.com')
    BVNK_BEARER_TOKEN: str = os.getenv('BVNK_BEARER_TOKEN', '')

    # General Configuration
    HEADLESS: str = os.getenv('HEADLESS', 'false')
    TIMEOUT: int = int(os.getenv('TIMEOUT', '30000'))
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

    # API Settings
    SERVICE_FEE_PERCENT: float = 0.01  # 0.01% service fee
    QUOTE_EXPIRY_SECONDS: int = 20  # Quotes expire after 20 seconds


# Create a singleton instance
settings = Settings()