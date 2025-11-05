from typing import Dict, Any, Optional
import requests

from config import settings
from utils.logger import Logger

logger = Logger()

class APIRequestBuilder:
    """  Builder Pattern for constructing and executing HTTP API requests.

    Provides a fluent interface for building complex API requests step-by-step,
    making test code more readable and maintainable.

    Design Pattern: Builder Pattern
    Thread Safety: Not thread-safe (designed for single-threaded test execution)


    Example:
        response = (
            APIRequestBuilder(base_url)
            .endpoint("/users")
            .method("POST")
            .body({"name": "John"})
            .bearer_token("token123")
            .execute()
        )"""

    def __init__(self, base_url: str):
        """
        Initialize the builder with base URL and defaults.

        Args:
            base_url: Base URL for all requests (e.g., "https://api.example.com")
        """
        self._base_url = base_url
        self._endpoint = ""
        self._method = "GET"
        self._headers: Dict[str, str] = {}
        self._params: Dict[str, Any] = {}
        self._body: Optional[Dict[str, Any]] = None
        self._auth: Optional[tuple] = None
        self._timeout = 30

    def endpoint(self, path: str):
        """
        Set the API endpoint path.

        Args:
            path: Endpoint path (e.g., "/users" or "/api/v1/users")

        Returns:
            Self for method chaining
        """
        self._endpoint = path
        return self

    def method(self, method: str):
        """
        Set the HTTP method.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)

        Returns:
            Self for method chaining
        """
        self._method = method.upper()
        return self

    def header(self, key: str, value: str):
        """
        Add a single header to the request.

        Args:
            key: Header name (e.g., "Content-Type")
            value: Header value (e.g., "application/json")

        Returns:
            Self for method chaining
        """
        self._headers[key] = value
        return self

    def headers(self, headers: Dict[str, str]):
        """
        Set all headers at once (replaces existing headers).

        Args:
            headers: Dictionary of header key-value pairs

        Returns:
            Self for method chaining
        """
        self._headers = headers
        return self

    def param(self, key: str, value: Any):
        """
        Add a single query parameter.

        Args:
            key: Parameter name (e.g., "page")
            value: Parameter value (e.g., 1)

        Returns:
            Self for method chaining
        """
        self._params[key] = value
        return self

    def params(self, params: Dict[str, Any]):
        """
        Set all query parameters at once (replaces existing params).

        Args:
            params: Dictionary of parameter key-value pairs

        Returns:
            Self for method chaining
        """
        self._params = params
        return self

    def body(self, data: Dict[str, Any]):
        """
        Set the request body (automatically serialized to JSON).

        Args:
            data: Request body as dictionary

        Returns:
            Self for method chaining
        """
        self._body = data
        return self

    def auth(self, username: str, password: str):
        """
        Set HTTP Basic Authentication credentials.

        Args:
            username: Username
            password: Password

        Returns:
            Self for method chaining
        """
        self._auth = (username, password)
        return self

    def bearer_token(self, token: str):
        """
        Set Bearer token authentication (OAuth 2.0 / JWT).

        Automatically formats the Authorization header as "Bearer <token>".

        Args:
            token: Bearer token string

        Returns:
            Self for method chaining
        """
        self._headers['Authorization'] = f'Bearer {token}'
        return self

    def timeout(self, seconds: int):
        """
        Set request timeout in seconds.

        Args:
            seconds: Timeout value (default: 30)

        Returns:
            Self for method chaining
        """
        self._timeout = seconds
        return self

    def build(self) -> requests.Request:
        """
        Build the Request object without executing it.

        Useful for inspecting the request before sending or
        for advanced use cases requiring manual preparation.

        Returns:
            Prepared requests.Request object
        """
        url = f"{self._base_url}{self._endpoint}"

        request = requests.Request(
            method=self._method,
            url=url,
            headers=self._headers,
            params=self._params,
            json=self._body,
            auth=self._auth
        )

        return request

    def execute(self) -> requests.Response:
        """
        Build and execute the HTTP request.

        Automatically logs the request and response for debugging.
        Uses a new session for each request to avoid state pollution.

        Returns:
            requests.Response object with status code and body

        Raises:
            requests.RequestException: For network/connection errors
        """
        request = self.build()
        prepared = request.prepare()

        logger.info(f"{self._method} {prepared.url}")

        session = requests.Session()
        response = session.send(prepared, timeout=self._timeout)

        logger.info(f"Response: {response.status_code}")

        return response

# Usage in tests
def test_get_user_with_filters():
    response = (
        APIRequestBuilder(settings.API_BASE_URL)
        .endpoint("/users")
        .method("GET")
        .param("role", "admin")
        .param("status", "active")
        .param("limit", 10)
        .header("Accept", "application/json")
        .bearer_token("your-token-here")
        .timeout(15)
        .execute()
    )

    assert response.status_code == 200
    assert len(response.json()) <= 10

def test_create_user():
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "user"
    }

    response = (
        APIRequestBuilder(settings.API_BASE_URL)
        .endpoint("/users")
        .method("POST")
        .body(user_data)
        .header("Content-Type", "application/json")
        .bearer_token("admin-token")
        .execute()
    )

    assert response.status_code == 201