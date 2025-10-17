import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_URL = os.getenv('BASE_URL', 'https://default-url.com')
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.default.com')
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    TIMEOUT = int(os.getenv('TIMEOUT', '30000'))

settings = Settings()