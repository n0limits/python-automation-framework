from abc import ABC, abstractmethod
import requests
from typing import Dict, Any

class AuthStrategy(ABC):
    """Abstract authentication strategy"""

    @abstractmethod
    def authenticate(self, session: requests.Session) -> None:
        """Authenticate the session"""
        pass

class BasicAuthStrategy(AuthStrategy):
    """Basic authentication"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def authenticate(self, session: requests.Session) -> None:
        session.auth = (self.username, self.password)

class BearerTokenStrategy(AuthStrategy):
    """Bearer token authentication"""

    def __init__(self, token: str):
        self.token = token

    def authenticate(self, session: requests.Session) -> None:
        session.headers.update({
            'Authorization': f'Bearer {self.token}'
        })

class OAuth2Strategy(AuthStrategy):
    """OAuth2 authentication"""

    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

    def authenticate(self, session: requests.Session) -> None:
        # Get access token
        response = requests.post(
            self.token_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
        )
        token = response.json()['access_token']
        session.headers.update({
            'Authorization': f'Bearer {token}'
        })

class APIKeyStrategy(AuthStrategy):
    """API Key authentication"""

    def __init__(self, api_key: str, header_name: str = 'X-API-Key'):
        self.api_key = api_key
        self.header_name = header_name

    def authenticate(self, session: requests.Session) -> None:
        session.headers.update({
            self.header_name: self.api_key
        })

class APIClient:
    """API client using strategy pattern"""

    def __init__(self, base_url: str, auth_strategy: AuthStrategy):
        self.base_url = base_url
        self.session = requests.Session()
        auth_strategy.authenticate(self.session)

    def get(self, endpoint: str, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", **kwargs)

# Usage in conftest.py or tests
@pytest.fixture
def api_client_basic():
    """API client with basic auth"""
    auth = BasicAuthStrategy("user", "password")
    return APIClient(settings.API_BASE_URL, auth)

@pytest.fixture
def api_client_token():
    """API client with bearer token"""
    auth = BearerTokenStrategy("your-token-here")
    return APIClient(settings.API_BASE_URL, auth)

@pytest.fixture
def api_client_oauth():
    """API client with OAuth2"""
    auth = OAuth2Strategy(
        client_id="your-client-id",
        client_secret="your-secret",
        token_url="https://auth.example.com/token"
    )
    return APIClient(settings.API_BASE_URL, auth)

# Test using different auth strategies
def test_with_basic_auth(api_client_basic):
    response = api_client_basic.get("/users")
    assert response.status_code == 200

def test_with_token_auth(api_client_token):
    response = api_client_token.get("/users")
    assert response.status_code == 200