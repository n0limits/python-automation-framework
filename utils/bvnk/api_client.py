"""
BVNK API Client for interacting with the simulator
"""
import requests
import time
from typing import Dict, Any, Optional
from config.settings import settings


class BVNKApiClient:
    """Client for BVNK API interactions"""

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

    def init_account(self) -> Dict[str, Any]:
        """
        Initialize a new simulated account and get bearer token

        Returns:
            Dict containing bearer token and account info
        """
        print("\nInitializing BVNK account...")

        # Call /init endpoint (no auth required for this endpoint)
        response = self.session.get(f"{self.base_url}/init")
        response.raise_for_status()
        data = response.json()

        print(f"Response from /init: {data}")

        # Extract access_token from response (API returns 'access_token', not 'token')
        token = data.get('access_token')

        if not token:
            raise ValueError(f"No access_token found in /init response. Response: {data}")

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
        """
        response = self.session.post(
            f"{self.base_url}/echo",
            json=payload if payload else {}
        )
        response.raise_for_status()
        return response.json()

    def list_wallets(self) -> list:
        """
        List all wallets associated with the account

        Returns:
            List of wallet dictionaries
        """
        response = self.session.get(f"{self.base_url}/api/wallet")
        response.raise_for_status()
        return response.json()

    def get_wallet(self, wallet_id: str) -> Dict[str, Any]:
        """
        Get details for a specific wallet

        Args:
            wallet_id: Wallet ID

        Returns:
            Dict containing wallet details
        """
        response = self.session.get(f"{self.base_url}/api/wallet/{wallet_id}")
        response.raise_for_status()
        return response.json()

    def create_quote(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        """
        Create a quote for currency conversion

        Args:
            from_currency: Source currency code (e.g., 'ETH')
            to_currency: Target currency code (e.g., 'TRX')
            amount: Amount to convert

        Returns:
            Dict containing quote details including UUID
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
            raise ValueError(f"Wallet not found for currency: {from_currency}")
        if not to_wallet_id:
            raise ValueError(f"Wallet not found for currency: {to_currency}")

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

        # Print error details if request fails
        if not (200 <= response.status_code < 300):
            print(f"\n Error creating quote:")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text}")

        response.raise_for_status()
        return response.json()

    def accept_quote(self, quote_uuid: str) -> Dict[str, Any]:
        """
        Accept a quote to execute the conversion

        Args:
            quote_uuid: UUID of the quote to accept

        Returns:
            Dict containing conversion result
        """
        response = self.session.put(
            f"{self.base_url}/api/v1/quote/accept/{quote_uuid}"
        )
        response.raise_for_status()
        return response.json()

    def get_quote(self, quote_uuid: str) -> Dict[str, Any]:
        """
        Get details for a specific quote

        Args:
            quote_uuid: UUID of the quote

        Returns:
            Dict containing quote details
        """
        response = self.session.get(
            f"{self.base_url}/api/v1/quote/{quote_uuid}"
        )
        response.raise_for_status()
        return response.json()

    def wait_for_quote_completion(self, quote_uuid: str, timeout: int = 30, poll_interval: int = 2) -> Dict[str, Any]:
        """
        Wait for a quote to complete processing

        Args:
            quote_uuid: UUID of the quote to wait for
            timeout: Maximum time to wait in seconds (default: 30)
            poll_interval: Time between status checks in seconds (default: 2)

        Returns:
            Final quote status dict

        Raises:
            TimeoutError: If quote doesn't complete within timeout
            ValueError: If transaction fails
        """
        start_time = time.time()
        elapsed = 0

        print(f"\nWaiting for transaction to complete (timeout: {timeout}s)...")

        while elapsed < timeout:
            quote = self.get_quote(quote_uuid)
            payment_status = quote.get('paymentStatus', '')
            quote_status = quote.get('quoteStatus', '')

            print(f"  [{int(elapsed)}s] Quote: {quote_status}, Payment: {payment_status}")

            # Check if completed - ADD 'SUCCESS' HERE
            if payment_status in ['COMPLETE', 'COMPLETED', 'PAID', 'SUCCESS']:  # ← Added 'SUCCESS'
                print(f" Transaction completed after {int(elapsed)}s!")
                return quote

            # Check if failed
            if payment_status in ['FAILED', 'CANCELLED', 'EXPIRED'] or \
                    quote_status in ['FAILED', 'CANCELLED', 'EXPIRED', 'REJECTED']:
                raise ValueError(
                    f"Transaction failed: Quote status={quote_status}, Payment status={payment_status}"
                )

            # Wait before next check
            time.sleep(poll_interval)
            elapsed = time.time() - start_time

        # Timeout reached
        raise TimeoutError(
            f"Quote {quote_uuid} did not complete within {timeout} seconds. "
            f"Last status - Quote: {quote_status}, Payment: {payment_status}"
        )

    def close(self):
        """Close the session"""
        self.session.close()