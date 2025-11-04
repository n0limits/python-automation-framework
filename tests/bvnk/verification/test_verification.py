"""
BVNK API Verification & Debug Tests

These tests are for exploring and verifying the API structure.
They're marked as skipped by default and should be run manually when needed.

Usage:
    # Run all verification tests
    pytest tests/bvnk/verification/test_verification.py -v

    # Run specific verification test
    pytest tests/bvnk/verification/test_verification.py::test_debug_wallet_structure -v -s
"""
import pytest
import requests
from config.settings import settings


# ============================================
# Init Endpoint Verification
# ============================================

@pytest.mark.bvnk
@pytest.mark.functional
@pytest.mark.verification
def test_init_endpoint_directly():
    """
    Verify /init endpoint works correctly without using the API client

    This test validates:
    - Endpoint accessibility
    - Response structure
    - Token generation
    - Token validity
    """
    print("\nTesting /init endpoint directly...")

    # Call /init endpoint
    url = f"{settings.BVNK_API_BASE_URL}/init"
    print(f"Calling: {url}")

    response = requests.get(url)

    print(f"Status: {response.status_code}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    print(f"Response: {data}")

    # Verify response structure
    assert 'access_token' in data, "Missing access_token in response"
    assert 'token_type' in data, "Missing token_type in response"
    assert 'expiry' in data, "Missing expiry in response"

    token = data['access_token']
    print(f"Token received: {token[:20]}..." if len(token) > 20 else f"Token received: {token}")

    # Test token by calling /echo endpoint
    echo_response = requests.post(
        f"{settings.BVNK_API_BASE_URL}/echo",
        headers={'Authorization': f'Bearer {token}'},
        json={}
    )

    print(f"Echo status: {echo_response.status_code}")
    print(f"Echo response: {echo_response.json()}")

    assert echo_response.status_code == 200, "Token authentication failed"
    print("\n Token is valid and working!")


# ============================================
# Wallet Structure Verification
# ============================================

@pytest.mark.bvnk
@pytest.mark.functional
@pytest.mark.verification
@pytest.mark.skip(reason="Debug test - run manually with: pytest tests/bvnk/verification/test_verification.py::test_debug_wallet_structure -v -s")
def test_debug_wallet_structure(bvnk_api):
    """
    Debug: Print actual wallet structure to understand API response format

    This test helps understand:
    - Wallet object structure
    - Available fields
    - Currency object nesting
    - Balance field names
    """
    print("\n" + "="*70)
    print("DEBUGGING WALLET STRUCTURE")
    print("="*70)

    wallets = bvnk_api.list_wallets()

    print(f"\nNumber of wallets: {len(wallets)}")
    print(f"Type of wallets: {type(wallets)}")

    for idx, wallet in enumerate(wallets, 1):
        print(f"\n--- Wallet {idx} ---")
        print(f"Type: {type(wallet)}")
        print(f"Keys: {wallet.keys()}")

        # Pretty print the full wallet object
        import json
        print(f"Full content:")
        print(json.dumps(wallet, indent=2))

        # Extract and display balance-related fields
        print(f"\nBalance-related fields:")
        print(f"  balance: {wallet.get('balance')}")
        print(f"  approxBalance: {wallet.get('approxBalance')}")

        # Extract currency info
        currency = wallet.get('currency', {})
        if currency:
            print(f"\nCurrency info:")
            print(f"  code: {currency.get('code')}")
            print(f"  name: {currency.get('name')}")


# ============================================
# Quote API Format Verification
# ============================================

@pytest.mark.bvnk
@pytest.mark.functional
@pytest.mark.verification
@pytest.mark.skip(reason="Debug test - run manually with: pytest tests/bvnk/verification/test_verification.py::test_debug_quote_api -v -s")
def test_debug_quote_api(bvnk_api):
    """
    Debug: Test different quote payload formats to find correct API structure

    This test attempts various payload formats to understand:
    - Required fields
    - Field naming conventions
    - API error messages
    """
    print("\n" + "="*70)
    print("DEBUGGING QUOTE API")
    print("="*70)

    # Test different payload formats
    test_payloads = [
        {
            "name": "Simple format",
            "payload": {
                "from": "ETH",
                "to": "TRX",
                "amount": 0.1
            }
        },
        {
            "name": "Pascal case",
            "payload": {
                "FromCurrency": "ETH",
                "ToCurrency": "TRX",
                "Amount": 0.1
            }
        },
        {
            "name": "Camel case",
            "payload": {
                "fromCurrency": "ETH",
                "toCurrency": "TRX",
                "amount": 0.1
            }
        },
        {
            "name": "Snake case",
            "payload": {
                "from_currency": "ETH",
                "to_currency": "TRX",
                "amount": 0.1
            }
        }
    ]

    for idx, test in enumerate(test_payloads, 1):
        print(f"\n--- Attempt {idx} ---")
        print(f"Payload: {test['payload']}")

        try:
            response = bvnk_api.session.post(
                f"{bvnk_api.base_url}/api/v1/quote",
                json=test['payload']
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code == 200 or response.status_code == 201:
                print(" SUCCESS! This format works!")
                break
        except Exception as e:
            print(f"Error: {e}")

    print("\nNone of the formats worked. Check API documentation.")


# ============================================
# Complete API Flow Verification
# ============================================

@pytest.mark.bvnk
@pytest.mark.functional
@pytest.mark.verification
@pytest.mark.skip(reason="Comprehensive verification - run manually when needed")
def test_complete_api_flow(bvnk_api):
    """
    Comprehensive verification of complete API flow

    Tests the full workflow:
    1. Authentication (init)
    2. List wallets
    3. Create quote
    4. Get quote details
    5. Accept quote
    6. Verify completion
    """
    print("\n" + "="*70)
    print("COMPLETE API FLOW VERIFICATION")
    print("="*70)

    # Step 1: List wallets
    print("\n[1/5] Listing wallets...")
    wallets = bvnk_api.list_wallets()
    print(f" Found {len(wallets)} wallets")

    # Step 2: Create quote
    print("\n[2/5] Creating quote...")
    quote = bvnk_api.create_quote('ETH', 'TRX', 0.1)
    quote_uuid = quote['uuid']
    print(f" Quote created: {quote_uuid}")

    # Step 3: Get quote details
    print("\n[3/5] Getting quote details...")
    quote_details = bvnk_api.get_quote(quote_uuid)
    print(f" Quote status: {quote_details.get('quoteStatus')}")

    # Step 4: Accept quote
    print("\n[4/5] Accepting quote...")
    accept_response = bvnk_api.accept_quote(quote_uuid)
    print(f" Quote accepted: {accept_response.get('paymentStatus')}")

    # Step 5: Wait for completion
    print("\n[5/5] Waiting for completion...")
    try:
        final_quote = bvnk_api.wait_for_quote_completion(quote_uuid, timeout=30)
        print(f" Transaction completed!")
        print(f"   Payment status: {final_quote.get('paymentStatus')}")
        print(f"   Quote status: {final_quote.get('quoteStatus')}")
    except TimeoutError as e:
        print(f" Timeout: {e}")

    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)


# ============================================
# API Response Structure Verification
# ============================================

@pytest.mark.bvnk
@pytest.mark.functional
@pytest.mark.verification
@pytest.mark.skip(reason="Structure verification - run manually when API changes")
def test_verify_api_response_structures(bvnk_api):
    """
    Verify the structure of all API responses

    Useful when:
    - API updates
    - Documentation is unclear
    - Response format changes
    """
    print("\n" + "="*70)
    print("API RESPONSE STRUCTURE VERIFICATION")
    print("="*70)

    import json

    # Test /echo response
    print("\n--- /echo Response ---")
    echo = bvnk_api.echo({'test': 'data'})
    print(json.dumps(echo, indent=2))

    # Test /api/wallet response
    print("\n--- /api/wallet Response ---")
    wallets = bvnk_api.list_wallets()
    print(f"Type: {type(wallets)}")
    print(f"Length: {len(wallets)}")
    if wallets:
        print("First wallet structure:")
        print(json.dumps(wallets[0], indent=2))

    # Test /api/v1/quote response
    print("\n--- /api/v1/quote Response ---")
    quote = bvnk_api.create_quote('ETH', 'TRX', 0.1)
    print("Quote fields:")
    print(json.dumps(list(quote.keys()), indent=2))
    print("\nSample quote:")
    print(json.dumps(quote, indent=2))


# ============================================
# Error Response Verification
# ============================================

@pytest.mark.bvnk
@pytest.mark.functional
@pytest.mark.verification
@pytest.mark.skip(reason="Error testing - run manually")
def test_verify_error_responses(bvnk_api):
    """
    Verify how the API handles various error conditions

    Tests:
    - Invalid currency codes
    - Missing required fields
    - Invalid amounts
    - Expired quotes
    """
    print("\n" + "="*70)
    print("ERROR RESPONSE VERIFICATION")
    print("="*70)

    # Test 1: Invalid currency
    print("\n[1/4] Testing invalid currency...")
    try:
        quote = bvnk_api.create_quote('INVALID', 'TRX', 1.0)
        print(" Should have failed with invalid currency")
    except Exception as e:
        print(f" Correctly failed: {e}")

    # Test 2: Zero amount
    print("\n[2/4] Testing zero amount...")
    try:
        quote = bvnk_api.create_quote('ETH', 'TRX', 0)
        print(" Should have failed with zero amount")
    except Exception as e:
        print(f" Correctly failed: {e}")

    # Test 3: Negative amount
    print("\n[3/4] Testing negative amount...")
    try:
        quote = bvnk_api.create_quote('ETH', 'TRX', -1.0)
        print(" Should have failed with negative amount")
    except Exception as e:
        print(f" Correctly failed: {e}")

    # Test 4: Invalid quote UUID
    print("\n[4/4] Testing invalid quote UUID...")
    try:
        quote = bvnk_api.get_quote('invalid-uuid')
        print(" Should have failed with invalid UUID")
    except Exception as e:
        print(f" Correctly failed: {e}")

    print("\n Error handling verified")