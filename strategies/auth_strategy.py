from abc import ABC, abstractmethod

import pytest
import requests
from typing import Dict, Any

from config import settings


class AuthStrategy(ABC):
    """
    Abstract base class for authentication strategies (Strategy Pattern).
    Use Case: APIs with different authentication methods

    The Strategy Pattern allows selecting authentication algorithm at runtime:
    - Defines a family of authentication algorithms
    - Encapsulates each algorithm in a separate class
    - Makes algorithms interchangeable
    - Client code doesn't need to know authentication details
    - Easy to add new authentication methods without changing client code
    - Test different auth methods by swapping strategy
    - Separate authentication logic from API client logic
    - Follow Open/Closed Principle (open for extension, closed for modification)

    Supported Strategies:
    - BasicAuthStrategy: HTTP Basic Authentication
    - BearerTokenStrategy: Bearer Token (OAuth 2.0, JWT)
    - OAuth2Strategy: OAuth 2.0 Client Credentials Flow
    - APIKeyStrategy: API Key in header

    Usage Pattern:
        1. Choose authentication strategy
        2. Create strategy instance with credentials
        3. Pass strategy to APIClient
        4. APIClient uses strategy to authenticate all requests

    Example:
        # Select strategy based on environment
        if env == "dev":
            auth = BasicAuthStrategy("user", "pass")
        elif env == "prod":
            auth = BearerTokenStrategy(token)

        # Use same client code regardless of auth method
        client = APIClient(base_url, auth)
        response = client.get("/users")
    """

    @abstractmethod
    def authenticate(self, session: requests.Session) -> None:
        """
        Authenticate the requests session.
        Each strategy implements its specific authentication mechanism.
        Args:
            session: Requests session to authenticate
        Implementations should modify session object in-place by:
        - Setting session.auth for HTTP Basic/Digest
        - Setting session.headers for token-based auth
        - Setting session.cookies for cookie-based auth
        """
        pass

class BasicAuthStrategy(AuthStrategy):
    """
    HTTP Basic Authentication strategy.

    Sends credentials as Base64-encoded "username:password" in Authorization header.
    Format: "Authorization: Basic base64(username:password)"

    Use When:
    - API uses HTTP Basic Authentication
    - Simple username/password authentication
    - Internal APIs or development environments

    Security Notes:
    - MUST use HTTPS in production (credentials are Base64, not encrypted)
    - Base64 is encoding, not encryption
    - Easy to decode if intercepted over HTTP

    Args:
        username: Username for authentication
        password: Password for authentication

    Example:
        auth = BasicAuthStrategy("admin", "secretpassword")
        client = APIClient("https://api.example.com", auth)

        # All requests will include:
        # Authorization: Basic YWRtaW46c2VjcmV0cGFzc3dvcmQ=
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def authenticate(self, session: requests.Session) -> None:
        session.auth = (self.username, self.password)

class BearerTokenStrategy(AuthStrategy):
    """
    Bearer Token authentication strategy.

    Authentication Method: RFC 6750 Bearer Token Usage
    Sends pre-obtained token in Authorization header.
    Format: "Authorization: Bearer <token>"
    Use When:
    - API uses OAuth 2.0 Bearer Tokens
    - API uses JWT (JSON Web Tokens)
    - Token obtained from separate authentication endpoint
    - Single-tenant API with long-lived tokens

    Args:
        token: Pre-obtained bearer token string

    Example:
        # Token obtained from login endpoint
        login_response = requests.post("/login", json={"user": "admin", "pass": "secret"})
        token = login_response.json()["access_token"]
    """
    def __init__(self, token: str):
        self.token = token

    def authenticate(self, session: requests.Session) -> None:
        """
        Set Bearer token in Authorization header.

        Token is sent as-is (no additional encoding).
        """
        session.headers.update({
            'Authorization': f'Bearer {self.token}'
        })

class OAuth2Strategy(AuthStrategy):
    """
    OAuth 2.0 Client Credentials Flow authentication strategy.

    Implements server-to-server authentication where:
    1. Client sends credentials to token endpoint
    2. Authorization server returns access token
    3. Access token used for API requests - Microservices authentication

    OAuth 2.0 Flow:
        POST /token
        grant_type=client_credentials
        client_id=<your_id>
        client_secret=<your_secret>
        Response:
        {
            "access_token": "eyJhbGc...",
            "token_type": "Bearer",
            "expires_in": 3600
        }
    Security:
    - Client credentials are like username/password - keep secure
    - Access tokens are short-lived (typically 1 hour)
    - Tokens automatically refresh on expiration (if implemented)
    """

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
    """
    API Key authentication strategy.
    Sends API key in a custom header (X-API-Key).
    """

    def __init__(self, api_key: str, header_name: str = 'X-API-Key'):
        self.api_key = api_key
        self.header_name = header_name

    def authenticate(self, session: requests.Session) -> None:
        session.headers.update({
            self.header_name: self.api_key
        })

class APIClient:
    """
    Generic API client that uses authentication strategies.
    - Write client code once, use with any auth method
    - Easy to test with different auth configurations
    - Add new auth methods without changing client

    Args:
        base_url: API base URL
        auth_strategy: Authentication strategy instance

    Example:
        # Same client code, different auth
        basic_client = APIClient(url, BasicAuthStrategy("user", "pass"))
        token_client = APIClient(url, BearerTokenStrategy(token))
        oauth_client = APIClient(url, OAuth2Strategy(id, secret, token_url))

        # All work the same way
        basic_client.get("/users")
        token_client.get("/users")
        oauth_client.get("/users")
    """
    def __init__(self, base_url: str, auth_strategy: AuthStrategy):
        self.base_url = base_url
        self.session = requests.Session()
        auth_strategy.authenticate(self.session)

    def get(self, endpoint: str, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", **kwargs)
