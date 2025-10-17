"""
Quick Verification - Fast smoke test
"""


def test_imports():
    """Quick test that everything imports correctly"""
    print('\n Testing Imports...')

    import pytest
    print(f' pytest {pytest.__version__}')

    import playwright
    print(' playwright installed')

    import requests
    print(f' requests {requests.__version__}')

    from dotenv import load_dotenv
    print(' python-dotenv installed')

    from config.settings import settings
    print(f' config loaded: {settings.BASE_URL}')

    print('\n All imports successful!')


def test_basic_assertion():
    """Test that pytest assertions work"""
    print('\n Testing Assertions...')
    assert 1 + 1 == 2
    assert "hello".upper() == "HELLO"
    print(' Assertions work!')


if __name__ == '__main__':
    test_imports()
    test_basic_assertion()