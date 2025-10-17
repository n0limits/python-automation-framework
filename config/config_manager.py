from threading import Lock
from typing import Optional, Dict, Any
import json

class ConfigManager:
    """Singleton configuration manager"""

    _instance: Optional['ConfigManager'] = None
    _lock: Lock = Lock()
    _config: Optional[Dict[str, Any]] = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = "config/test_config.json"):
        if self._config is None:
            with open(config_path, 'r') as f:
                self._config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)

    def get_env_config(self, env: str) -> Dict[str, Any]:
        """Get environment-specific config"""
        return self._config.get('environments', {}).get(env, {})

    def set(self, key: str, value: Any):
        """Set configuration value"""
        self._config[key] = value

# Usage
config = ConfigManager()
base_url = config.get('base_url')