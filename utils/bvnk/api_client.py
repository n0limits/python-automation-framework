"""
BVNK API Client for interacting with the simulator
"""
import requests
from typing import Dict, Any, Optional
from config.settings import settings


class BVNKApiClient:
    """Client for BVNK API interactions"""

    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize BVNK API Client

        Args:
            bearer_token: Bearer token for authentication
        """
        self.base_url = settings.BVNK_API_BASE_URL
        self.bearer_token = bearer_token or settings.BVNK_BEARER_TOKEN
        self.session = requests.Session()

        if self.bearer_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.bearer_token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })

    def init_account(self) -> Dict[str, Any]:
        """
        Initialize a new simulated account

        Returns:
            Dict containing bearer token and account info
        """
        response = self.session.get(f"{self.base_url}/init")
        response.raise_for_status()
        data = response.json()

        # Update bearer token
        if 'token' in data:
            self.bearer_token = data['token']
            self.session.headers.update({
                'Authorization': f'Bearer {self.bearer_token}'
            })

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

    def list_wallets(self) -> Dict[str, Any]:
        """
        List all wallets associated with the account

        Returns:
            Dict containing list of wallets
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
        payload = {
            'from': from_currency,
            'to': to_currency,
            'amount': amount
        }
        response = self.session.post(
            f"{self.base_url}/api/v1/quote",
            json=payload
        )
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

    def close(self):
        """Close the session"""
        self.session.close()