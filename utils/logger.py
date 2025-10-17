import logging
from threading import Lock
from typing import Optional

class Logger:
    """Singleton logger"""

    _instance: Optional['Logger'] = None
    _lock: Lock = Lock()
    _logger: Optional[logging.Logger] = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._logger is None:
            self._logger = logging.getLogger("AutomationFramework")
            self._logger.setLevel(logging.DEBUG)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # File handler
            file_handler = logging.FileHandler('reports/test_execution.log')
            file_handler.setLevel(logging.DEBUG)

            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

    def get_logger(self):
        return self._logger

    def info(self, message: str):
        self._logger.info(message)

    def debug(self, message: str):
        self._logger.debug(message)

    def error(self, message: str):
        self._logger.error(message)

    def warning(self, message: str):
        self._logger.warning(message)

# Usage
logger = Logger()
logger.info("Test started")