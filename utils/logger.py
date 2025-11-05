import logging
from threading import Lock
from typing import Optional

class Logger:
    """
    Singleton Pattern for centralized logging throughout the framework.
    - Single configuration point for all logging

    Log Levels:
    - DEBUG: Detailed diagnostic information
    - INFO: General information about test execution
    - WARNING: Warning messages (test should still pass)
    - ERROR: Error messages (test failures, exceptions)

    Output:
    - Console: INFO and above (for real-time monitoring)
    - File: DEBUG and above (for detailed post-execution analysis)

    Example:
        logger = Logger()  # Always returns same instance
        logger.info("Test started")
        logger.debug("Detailed debug info")
        logger.error("Test failed")
    """

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
        """
        Initialize logger only once with console and file handlers.
        Configuration:
        - Logger name: "AutomationFramework"
        - Console: INFO level (shows important messages during test run)
        - File: DEBUG level (captures everything for debugging)
        - Format: timestamp - name - level - message
        """
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