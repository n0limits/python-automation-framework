"""
Test the /init endpoint to verify token retrieval
"""
import pytest
import requests
from assertpy import assert_that
from config.settings import settings


@pytest.mark.bvnk
@pytest.mark.functional
def test_init_endpoint_directly():
    """
    Test that /init endpoint returns a valid token
    This test doesn't use the fixture to verify the endpoint works
    """
    print("\nTesting /init endpoint directly...")

    # Call /init endpoint directly
    url = f"{settings.BVNK_API_BASE_URL}/init"
    print(f"Calling: {url}")

    response = requests.get(url)

    # Verify response
    assert_that(response.status_code).is_equal_to(200)
    print(f"Status: {response.status_code}")

    data = response.json()
    print(f"Response: {data}")

    # Check for token (try different possible field names)
    token = None
    if 'token' in data:
        token = data['token']
    elif 'bearer_token' in data:
        token = data['bearer_token']
    elif 'access_token' in data:
        token = data['access_token']

    assert_that(token).is_not_none()
    assert_that(token).is_not_empty()

    print(f"Token received: {token[:20]}...")

    # Test that token works by calling /echo
    echo_url = f"{settings.BVNK_API_BASE_URL}/echo"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    echo_response = requests.post(echo_url, headers=headers, json={})
    print(f"Echo status: {echo_response.status_code}")
    print(f"Echo response: {echo_response.json()}")

    assert_that(echo_response.status_code).is_equal_to(200)

    print("\nToken is valid and working!")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])