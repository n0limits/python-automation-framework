"""
API Validation Helper
Provides reusable methods for functional API testing
"""
from typing import Dict, Any, List
from assertpy import assert_that
from config.settings import settings
import time
import requests


class ApiValidationHelper:
    """
    Helper class for functional API validation tests

    Provides methods to:
    - Validate API responses
    - Test error scenarios
    - Verify business logic (fees, expiry)
    """

    def __init__(self, bvnk_api):
        """
        Initialize API validation helper

        Args:
            bvnk_api: BVNK API client instance
        """
        self.bvnk_api = bvnk_api

    def validate_echo_response(self, test_payload: Dict = None) -> Dict[str, Any]:
        """
        Test /echo endpoint and validate response structure

        Args:
            test_payload: Optional payload to send

        Returns:
            Echo response
        """
        payload = test_payload or {'test_key': 'test_value', 'number': 123}

        print("\nCalling /echo endpoint...")
        response = self.bvnk_api.echo(payload)
        print(f"Echo response: {response}")

        # Validate response structure
        assert_that(response).contains_key('auth_token_expiry_time', 'request_payload')
        assert_that(response['request_payload']).is_equal_to(payload)

        print(" Echo response structure valid")
        print(" Payload echoed back correctly")

        return response

    def validate_wallet_list(self, expected_min_wallets: int = 3) -> List[Dict]:
        """
        Validate wallet listing response

        Args:
            expected_min_wallets: Minimum expected number of wallets

        Returns:
            List of wallets
        """
        print("\nListing wallets...")
        wallets = self.bvnk_api.list_wallets()

        print(f"Number of wallets: {len(wallets)}")

        # Validate basic structure
        assert_that(wallets).is_instance_of(list)
        assert_that(len(wallets)).is_greater_than(0)
        assert_that(len(wallets)).is_greater_than_or_equal_to(expected_min_wallets)

        # Validate each wallet has required fields
        for wallet in wallets:
            assert_that(wallet).contains_key('currency', 'balance')

            # Print wallet info
            currency_obj = wallet.get('currency', {})
            currency_code = currency_obj.get('code', 'UNKNOWN')
            balance = wallet.get('balance', '0')
            print(f"  {currency_code}: {balance}")

        print(f" All {len(wallets)} wallets have valid structure")

        return wallets

    def test_quote_expiry(
            self,
            from_currency: str = 'ETH',
            to_currency: str = 'TRX',
            amount: float = 0.1,
            wait_time: int = None
    ) -> str:
        """
        Create quote and wait for expiry

        Args:
            from_currency: Source currency
            to_currency: Target currency
            amount: Amount to convert
            wait_time: Time to wait before accepting (default: 22 seconds)

        Returns:
            Quote UUID
        """
        wait_time = wait_time or settings.QUOTE_EXPIRY_WAIT_TIME

        print(f"\nCreating quote for {amount} {from_currency} → {to_currency}...")
        quote = self.bvnk_api.create_quote(from_currency, to_currency, amount)
        quote_uuid = quote['uuid']

        print(f"Quote created: {quote_uuid}")
        print(f"Waiting {wait_time} seconds for expiry...")

        time.sleep(wait_time)

        print(" Wait complete")

        return quote_uuid

    def verify_insufficient_balance_error(
            self,
            from_currency: str,
            to_currency: str,
            excessive_amount: float,
            expected_status_codes: List[int]
    ):
        """
        Attempt conversion with insufficient balance and verify error

        Args:
            from_currency: Source currency
            to_currency: Target currency
            excessive_amount: Amount exceeding balance
            expected_status_codes: Expected error status codes
        """
        print(f"\nAttempting to convert {excessive_amount} {from_currency} (exceeds balance)...")

        try:
            quote = self.bvnk_api.create_quote(from_currency, to_currency, excessive_amount)
            self.bvnk_api.accept_quote(quote['uuid'])
            raise AssertionError("Should have rejected insufficient balance")
        except requests.exceptions.HTTPError as e:
            print(f" Correctly rejected: {e.response.status_code}")

            assert_that(e.response.status_code).described_as(
                f"Insufficient balance error should be one of {expected_status_codes}"
            ).is_in(*expected_status_codes)

            print(f" Error status code is valid: {e.response.status_code}")

    def verify_quote_expiry_error(self, quote_uuid: str, expected_status_codes: List[int]):
        """
        Attempt to accept expired quote and verify error

        Args:
            quote_uuid: UUID of expired quote
            expected_status_codes: Expected error status codes
        """
        print(f"\nAttempting to accept expired quote...")

        try:
            self.bvnk_api.accept_quote(quote_uuid)
            raise AssertionError("Expected quote to be expired, but it was accepted")
        except requests.exceptions.HTTPError as e:
            print(f"Quote correctly expired: {e}")

            assert_that(e.response.status_code).described_as(
                f"Expired quote error should be one of {expected_status_codes}"
            ).is_in(*expected_status_codes)

            print(f" Error status code is valid: {e.response.status_code}")

    def verify_service_fee(
            self,
            amount: float,
            quote: Dict[str, Any],
            expected_fee_percent: float = None
    ) -> float:
        """
        Verify service fee in quote matches expected percentage

        Args:
            amount: Conversion amount
            quote: Quote response
            expected_fee_percent: Expected fee percentage (default: from settings)

        Returns:
            Actual fee from quote
        """
        from utils.bvnk.helpers import calculate_expected_fee

        fee_percent = expected_fee_percent or settings.SERVICE_FEE_PERCENT
        expected_fee = calculate_expected_fee(amount, fee_percent)

        print(f"\nFee Verification:")
        print(f"  Amount: {amount}")
        print(f"  Fee %: {fee_percent * 100}%")
        print(f"  Expected fee: {expected_fee}")

        actual_fee = float(quote.get('fee', 0))
        print(f"  Actual fee from quote: {actual_fee}")

        assert_that(actual_fee).described_as(
            "Fee should match expected calculation"
        ).is_close_to(expected_fee, 0.00001)

        print(f" Fee matches expected amount")

        return actual_fee

    def validate_specific_wallet(self, wallet_id: int, expected_currency: str = None) -> Dict:
        """
        Validate specific wallet retrieval

        Args:
            wallet_id: Wallet ID to retrieve
            expected_currency: Optional currency code to verify

        Returns:
            Wallet details
        """
        print(f"\nRetrieving wallet {wallet_id}...")

        wallet = self.bvnk_api.get_wallet(wallet_id)

        # Validate structure
        assert_that(wallet).contains_key('id', 'currency', 'balance', 'description')
        assert_that(wallet['currency']).contains_key('code', 'name')

        currency_code = wallet['currency']['code']
        print(f" Wallet retrieved: {currency_code} (ID: {wallet['id']})")

        # Verify expected currency if provided
        if expected_currency:
            assert_that(currency_code).is_equal_to(expected_currency)
            print(f" Currency matches expected: {expected_currency}")

        return wallet
