"""
Debug test for quote API
"""
import pytest
import requests
from config.settings import settings


@pytest.mark.bvnk
@pytest.mark.functional
def test_debug_quote_api(bvnk_api):
    """Debug: Test different quote payload formats"""
    print("\n" + "="*70)
    print("DEBUGGING QUOTE API")
    print("="*70)

    # Try different payload formats
    payloads = [
        # Format 1: as in API client
        {
            'from': 'ETH',
            'to': 'TRX',
            'amount': 0.1
        },
        # Format 2: with "FromCurrency" and "ToCurrency"
        {
            'FromCurrency': 'ETH',
            'ToCurrency': 'TRX',
            'Amount': 0.1
        },
        # Format 3: lowercase
        {
            'fromCurrency': 'ETH',
            'toCurrency': 'TRX',
            'amount': 0.1
        },
        # Format 4: with "from_currency"
        {
            'from_currency': 'ETH',
            'to_currency': 'TRX',
            'amount': 0.1
        }
    ]

    for i, payload in enumerate(payloads, 1):
        print(f"\n--- Attempt {i} ---")
        print(f"Payload: {payload}")

        try:
            response = bvnk_api.session.post(
                f"{settings.BVNK_API_BASE_URL}/api/v1/quote",
                json=payload
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code == 200:
                print(" THIS FORMAT WORKS!")
                print(f"Quote: {response.json()}")
                return  # Stop once we find working format

        except Exception as e:
            print(f"Error: {e}")

    print("\nNone of the formats worked. Check API documentation.")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])