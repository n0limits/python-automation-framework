import pytest
from assertpy import assert_that
from config.settings import settings

@pytest.mark.backend
@pytest.mark.smoke
def test_get_user_by_id(api_client):
    """Test GET user endpoint"""
    response = api_client.get(f"{settings.API_BASE_URL}/users/1")

    # Assert status code
    assert_that(response.status_code).is_equal_to(200)

    # Assert response body
    data = response.json()
    assert_that(data).contains_key("id", "name", "email")
    assert_that(data["id"]).is_equal_to(1)
    assert_that(data["email"]).contains("@")

@pytest.mark.backend
def test_create_user(api_client):
    """Test POST create user"""
    payload = {
        "name": "John Doe",
        "email": "john@example.com"
    }

    response = api_client.post(
        f"{settings.API_BASE_URL}/users",
        json=payload
    )

    assert_that(response.status_code).is_equal_to(201)

    data = response.json()
    assert_that(data["name"]).is_equal_to("John Doe")
    assert_that(data).has_id()