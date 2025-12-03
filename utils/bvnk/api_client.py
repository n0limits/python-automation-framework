"""
BVNK API Client

Error Handling Features:
1. Custom error handling classes
2. Content-type validation before JSON parsing
3. Handles 204 No Content gracefully
4. Contextual error messages
5. Centralized error handling
6. Proper exception hierarchy
"""
import requests
import time
from typing import Dict, Any, Optional
from config.settings import settings


# ============================================
# CUSTOM ERROR HANDLING CLASSES
# ============================================

class BVNKApiError(Exception):
    """Base exception for all BVNK API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)

    def __str__(self):
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.response_body:
            parts.append(f"Response: {self.response_body[:200]}")  # Limit response length
        return " | ".join(parts)


class BVNKAuthenticationError(BVNKApiError):
    """Authentication failed (401)"""
    pass


class BVNKResourceNotFoundError(BVNKApiError):
    """Resource not found (404)"""
    pass


class BVNKValidationError(BVNKApiError):
    """Request validation failed (400, 422)"""
    pass


class BVNKQuoteExpiredError(BVNKApiError):
    """Quote has expired (410, 412)"""
    pass


class BVNKInsufficientBalanceError(BVNKApiError):
    """Insufficient balance for operation (412, 422)"""
    pass


class BVNKServerError(BVNKApiError):
    """Server error (500, 502, 503, 504)"""
    pass


class BVNKInvalidResponseError(BVNKApiError):
    """Response is not valid JSON or has unexpected content-type"""
    pass


# ============================================
# API CLIENT
# ============================================

class BVNKApiClient:
    """Client for BVNK API interactions with proper error handling"""

    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize BVNK API Client

        Args:
            bearer_token: Bearer token for authentication (optional, will be obtained from /init)
        """
        self.base_url = settings.BVNK_API_BASE_URL
        self.bearer_token = bearer_token
        self.session = requests.Session()

        # Set default headers (without auth initially)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

        # Only add auth header if token is provided
        if self.bearer_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.bearer_token}'
            })

    # ============================================
    # CENTRALIZED ERROR HANDLING
    # ============================================

    def _handle_response(self, response: requests.Response, endpoint: str = "") -> Dict[str, Any]:
        """
        Centralized response handling with proper error checking

        Features:
        - Content-type validation before JSON parsing
        - Handles 204 No Content gracefully
        - Custom exceptions with context
        - Handles HTML error pages

        Args:
            response: Response object from requests
            endpoint: API endpoint being called (for error context)

        Returns:
            Parsed JSON response or empty dict for 204

        Raises:
            BVNKAuthenticationError: For 401 errors
            BVNKResourceNotFoundError: For 404 errors
            BVNKValidationError: For 400, 422 errors
            BVNKQuoteExpiredError: For 410, 412 errors (quote-specific)
            BVNKServerError: For 5xx errors
            BVNKInvalidResponseError: For invalid JSON or content-type
        """
        # Handle HTTP errors first
        if not response.ok:
            error_body = response.text[:500]  # Limit error body size

            if response.status_code == 401:
                raise BVNKAuthenticationError(
                    f"Authentication failed for {endpoint}",
                    status_code=401,
                    response_body=error_body
                )
            elif response.status_code == 404:
                raise BVNKResourceNotFoundError(
                    f"Resource not found: {endpoint}",
                    status_code=404,
                    response_body=error_body
                )
            elif response.status_code == 400:
                raise BVNKValidationError(
                    f"Bad request to {endpoint}",
                    status_code=400,
                    response_body=error_body
                )
            elif response.status_code == 422:
                # Could be validation or insufficient balance
                if 'balance' in error_body.lower() or 'insufficient' in error_body.lower():
                    raise BVNKInsufficientBalanceError(
                        f"Insufficient balance for {endpoint}",
                        status_code=422,
                        response_body=error_body
                    )
                else:
                    raise BVNKValidationError(
                        f"Validation failed for {endpoint}",
                        status_code=422,
                        response_body=error_body
                    )
            elif response.status_code in [410, 412]:
                # Check if it's insufficient balance (similar to 422 handling)
                if 'balance' in error_body.lower() or 'insufficient' in error_body.lower():
                    raise BVNKInsufficientBalanceError(
                        f"Insufficient balance for {endpoint}",
                        status_code=response.status_code,
                        response_body=error_body
                    )
                else:
                    # Quote-specific errors
                    raise BVNKQuoteExpiredError(
                        f"Quote expired or invalid for {endpoint}",
                        status_code=response.status_code,
                        response_body=error_body
                    )
            elif response.status_code >= 500:
                raise BVNKServerError(
                    f"Server error for {endpoint}",
                    status_code=response.status_code,
                    response_body=error_body
                )
            else:
                # Generic HTTP error
                raise BVNKApiError(
                    f"HTTP {response.status_code} for {endpoint}",
                    status_code=response.status_code,
                    response_body=error_body
                )

        # Handle successful responses
        # Check for 204 No Content
        if response.status_code == 204:
            return {}  # No content, return empty dict

        # Validate content-type before parsing JSON
        content_type = response.headers.get('Content-Type', '')

        if 'application/json' not in content_type:
            raise BVNKInvalidResponseError(
                f"Expected JSON response from {endpoint}, got {content_type}",
                status_code=response.status_code,
                response_body=response.text[:500]
            )

        # Safely parse JSON with error handling
        try:
            return response.json()
        except ValueError as e:
            raise BVNKInvalidResponseError(
                f"Invalid JSON in response from {endpoint}: {str(e)}",
                status_code=response.status_code,
                response_body=response.text[:500]
            ) from e

    # ============================================
    # API METHODS
    # ============================================

    def init_account(self) -> Dict[str, Any]:
        """
        Initialize a new simulated account and get bearer token

        Returns:
            Dict containing bearer token and account info

        Raises:
            BVNKApiError: If initialization fails
        """
        print("\nInitializing BVNK account...")

        response = self.session.get(f"{self.base_url}/init")
        data = self._handle_response(response, endpoint="/init")

        print(f"Response from /init: {data}")

        # Extract access_token from response
        token = data.get('access_token')

        if not token:
            raise BVNKApiError(f"No access_token found in /init response. Response: {data}")

        # Store token
        self.bearer_token = token

        # Update session headers with authentication
        self.session.headers.update({
            'Authorization': f'Bearer {self.bearer_token}'
        })

        print(f" Account initialized successfully!")
        print(f"Token: {self.bearer_token[:20]}..." if len(self.bearer_token) > 20 else f"Token: {self.bearer_token}")
        print(f"Token expiry (timestamp): {data.get('expiry', 'Not provided')}")

        return data

    def echo(self, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Test authentication endpoint

        Args:
            payload: Optional request body to echo back

        Returns:
            Dict containing token expiry and echoed content

        Raises:
            BVNKAuthenticationError: If authentication fails
        """
        response = self.session.post(
            f"{self.base_url}/echo",
            json=payload if payload else {}
        )
        return self._handle_response(response, endpoint="/echo")

    def list_wallets(self) -> list:
        """
        List all wallets associated with the account

        Returns:
            List of wallet dictionaries

        Raises:
            BVNKAuthenticationError: If not authenticated
        """
        response = self.session.get(f"{self.base_url}/api/wallet")
        return self._handle_response(response, endpoint="/api/wallet")

    def get_wallet(self, wallet_id: int) -> Dict[str, Any]:
        """
        Get specific wallet details by ID

        Args:
            wallet_id: Wallet ID to retrieve

        Returns:
            Wallet details dictionary

        Raises:
            BVNKResourceNotFoundError: If wallet doesn't exist
        """
        print(f"\nGetting wallet {wallet_id}...")

        response = self.session.get(f"{self.base_url}/api/wallet/{wallet_id}")
        wallet = self._handle_response(response, endpoint=f"/api/wallet/{wallet_id}")

        print(f" Wallet retrieved: {wallet['currency']['code']}")

        return wallet

    def create_quote(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        """
        Create a quote for currency conversion

        Args:
            from_currency: Source currency code (e.g., 'ETH')
            to_currency: Target currency code (e.g., 'TRX')
            amount: Amount to convert

        Returns:
            Dict containing quote details including UUID

        Raises:
            BVNKValidationError: If validation fails
            BVNKInsufficientBalanceError: If insufficient balance
        """
        # First, get wallets to find wallet IDs
        wallets = self.list_wallets()

        # Find wallet IDs for the currencies
        from_wallet_id = None
        to_wallet_id = None

        for wallet in wallets:
            currency_obj = wallet.get('currency', {})
            code = currency_obj.get('code', '')

            if code == from_currency:
                from_wallet_id = wallet.get('id')
            elif code == to_currency:
                to_wallet_id = wallet.get('id')

        if not from_wallet_id:
            raise BVNKValidationError(f"Wallet not found for currency: {from_currency}")
        if not to_wallet_id:
            raise BVNKValidationError(f"Wallet not found for currency: {to_currency}")

        print(f"\nCreating quote:")
        print(f"  From: {from_currency} (wallet ID: {from_wallet_id})")
        print(f"  To: {to_currency} (wallet ID: {to_wallet_id})")
        print(f"  Amount: {amount}")

        # Build payload according to API schema
        payload = {
            'from': from_currency,
            'to': to_currency,
            'fromWallet': from_wallet_id,
            'toWallet': to_wallet_id,
            'useMaximum': False,
            'useMinimum': False,
            'reference': f'conversion-{from_currency}-to-{to_currency}',
            'amountIn': amount,
            'amountOut': 0,
            'payInMethod': 'balance',
            'payOutMethod': 'balance'
        }

        print(f"Payload: {payload}")

        response = self.session.post(
            f"{self.base_url}/api/v1/quote",
            json=payload
        )

        return self._handle_response(response, endpoint="/api/v1/quote")

    def accept_quote(self, quote_uuid: str) -> Dict[str, Any]:
        """
        Accept a quote to execute the conversion

        Args:
            quote_uuid: UUID of the quote to accept

        Returns:
            Dict containing conversion result

        Raises:
            BVNKQuoteExpiredError: If quote has expired
            BVNKResourceNotFoundError: If quote doesn't exist
        """
        response = self.session.put(
            f"{self.base_url}/api/v1/quote/accept/{quote_uuid}"
        )
        return self._handle_response(response, endpoint=f"/api/v1/quote/accept/{quote_uuid}")

    def get_quote(self, quote_uuid: str) -> Dict[str, Any]:
        """
        Get details for a specific quote

        Args:
            quote_uuid: UUID of the quote

        Returns:
            Dict containing quote details

        Raises:
            BVNKResourceNotFoundError: If quote doesn't exist
        """
        response = self.session.get(
            f"{self.base_url}/api/v1/quote/{quote_uuid}"
        )
        return self._handle_response(response, endpoint=f"/api/v1/quote/{quote_uuid}")

    def wait_for_quote_completion(self, quote_uuid: str, timeout: int = 20, initial_poll_interval: float = 0.5) -> Dict[str, Any]:
        """
        Wait for a quote to complete processing with exponential backoff

        Args:
            quote_uuid: UUID of the quote to wait for
            timeout: Maximum time to wait in seconds (default: 20)
            initial_poll_interval: Starting interval in seconds (default: 0.5)

        Returns:
            Final quote status dict

        Raises:
            TimeoutError: If quote doesn't complete within timeout
            BVNKApiError: If quote fails
        """
        start_time = time.time()
        elapsed = 0
        poll_interval = initial_poll_interval
        max_poll_interval = 3.0

        print(f"\nWaiting for transaction to complete (timeout: {timeout}s)...")

        while elapsed < timeout:
            quote = self.get_quote(quote_uuid)
            payment_status = quote.get('paymentStatus', '')
            quote_status = quote.get('quoteStatus', '')

            print(f"  [{int(elapsed)}s] Quote: {quote_status}, Payment: {payment_status}")

            # Check if completed
            if payment_status in ['COMPLETE', 'COMPLETED', 'PAID', 'SUCCESS']:
                print(f" Transaction completed after {int(elapsed)}s!")
                return quote

            # Check if failed
            if payment_status in ['FAILED', 'CANCELLED', 'EXPIRED'] or \
                    quote_status in ['FAILED', 'CANCELLED', 'EXPIRED', 'REJECTED']:
                raise BVNKApiError(
                    f"Transaction failed: Quote status={quote_status}, Payment status={payment_status}"
                )

            # Wait with exponential backoff
            time.sleep(poll_interval)
            elapsed = time.time() - start_time

            # Increase poll interval (exponential backoff)
            poll_interval = min(poll_interval * 1.5, max_poll_interval)

        raise TimeoutError(
            f"Quote {quote_uuid} did not complete within {timeout} seconds. "
            f"Last status - Quote: {quote_status}, Payment: {payment_status}"
        )

    def close(self):
        """Close the session"""
        self.session.close()
