from threading import Lock
from typing import Optional, Dict, Any
import json

class ConfigManager:
    """
    Singleton Pattern for managing test configuration across the framework.

    Ensures only one configuration instance exists throughout the test execution,
    preventing inconsistent configuration state and unnecessary file reads.

    Design Pattern: Singleton Pattern
    Thread Safety: Thread-safe (uses double-checked locking)

    Implementation Details:
    - Uses __new__ to control instance creation
    - Double-checked locking pattern for thread safety
    - Config loaded once and cached in memory

    Example:
        config = ConfigManager()  # Always returns same instance
        base_url = config.get('base_url')
        env_config = config.get_env_config('staging')
    """
    _instance: Optional['ConfigManager'] = None
    _lock: Lock = Lock()
    _config: Optional[Dict[str, Any]] = None

    def __new__(cls):
        """
        Control instance creation to ensure only one exists (Singleton pattern).

        Uses double-checked locking:
        1. First check: Quick check without locking
        2. Acquire lock if no instance exists
        3. Second check: Verify no other thread created instance while waiting
        4. Create instance if still None

        Thread-safe fro parallel test execution.

        Returns:
            The single ConfigManager instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = "config/test_config.json"):
        """
        Initialize configuration (once - singleton).

        Args:
            config_path: Path to JSON configuration file

        Note: __init__ may be called multiple times (once per ConfigManager()),
        but the check ensures config is loaded only once.
        """
        if self._config is None:
            with open(config_path, 'r') as f:
                self._config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Configuration key (e.g., 'base_url')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def get_env_config(self, env: str) -> Dict[str, Any]:
        """
        Get environment-specific configuration.
        (dev, staging, production).
        Expects config structure:
        {
            "environments": {
                "dev": { ... },
                "staging": { ... },
                "production": { ... }
            }
        }

        Args:
            env: Environment name (e.g., 'staging')

        Returns:
            Environment-specific configuration dictionary
        """
        return self._config.get('environments', {}).get(env, {})

    def set(self, key: str, value: Any):
        """
        Set/update configuration value at runtime.

        Useful for dynamic configuration changes during test execution.
        Changes are not persisted to file (memory only).

        Args:
            key: Configuration key
            value: New value
        """
        self._config[key] = value

# Usage
config = ConfigManager()
base_url = config.get('base_url')