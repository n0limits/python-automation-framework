"""
Root conftest.py - Project-level pytest configuration
Adds project root to Python path
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def pytest_configure(config):
    """
    Pytest hook - called after command line options have been parsed
    Register custom markers
    """
    config.addinivalue_line("markers", "bvnk: BVNK API tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "functional: Functional tests")
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "frontend: Frontend/UI tests")
    config.addinivalue_line("markers", "backend: Backend/API tests")
    config.addinivalue_line("markers", "mobile: Mobile web tests")
    config.addinivalue_line("markers", "mobile_app: Native mobile app tests")