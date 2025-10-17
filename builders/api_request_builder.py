from typing import Dict, Any, Optional
import requests
from utils.logger import Logger

logger = Logger()

class APIRequestBuilder:
    """Builder for constructing API requests"""

    def __init__(self, base_url: str):
        self._base_url = base_url
        self._endpoint = ""
        self._method = "GET"
        self._headers: Dict[str, str] = {}
        self._params: Dict[str, Any] = {}
        self._body: Optional[Dict[str, Any]] = None
        self._auth: Optional[tuple] = None
        self._timeout = 30

    def endpoint(self, path: str):
        """Set endpoint"""
        self._endpoint = path
        return self

    def method(self, method: str):
        """Set HTTP method"""
        self._method = method.upper()
        return self

    def header(self, key: str, value: str):
        """Add a header"""
        self._headers[key] = value
        return self

    def headers(self, headers: Dict[str, str]):
        """Set all headers"""
        self._headers = headers
        return self

    def param(self, key: str, value: Any):
        """Add query parameter"""
        self._params[key] = value
        return self

    def params(self, params: Dict[str, Any]):
        """Set all query parameters"""
        self._params = params
        return self

    def body(self, data: Dict[str, Any]):
        """Set request body"""
        self._body = data
        return self

    def auth(self, username: str, password: str):
        """Set basic auth"""
        self._auth = (username, password)
        return self

    def bearer_token(self, token: str):
        """Set bearer token"""
        self._headers['Authorization'] = f'Bearer {token}'
        return self

    def timeout(self, seconds: int):
        """Set timeout"""
        self._timeout = seconds
        return self

    def build(self) -> requests.Request:
        """Build the request"""
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
        """Build and execute the request"""
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