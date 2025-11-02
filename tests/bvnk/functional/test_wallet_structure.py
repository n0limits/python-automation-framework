"""
Debug test to understand wallet structure
"""
import pytest
from assertpy import assert_that


@pytest.mark.bvnk
@pytest.mark.functional
def test_debug_wallet_structure(bvnk_api):
    """Debug: Print actual wallet structure"""
    print("\n" + "="*70)
    print("DEBUGGING WALLET STRUCTURE")
    print("="*70)

    wallets = bvnk_api.list_wallets()

    print(f"\nNumber of wallets: {len(wallets)}")
    print(f"Type of wallets: {type(wallets)}")

    for i, wallet in enumerate(wallets):
        print(f"\n--- Wallet {i+1} ---")
        print(f"Type: {type(wallet)}")
        print(f"Keys: {wallet.keys() if isinstance(wallet, dict) else 'Not a dict'}")
        print(f"Full content:")

        # Pretty print the wallet
        import json
        print(json.dumps(wallet, indent=2))

        # Check for balance fields
        print(f"\nBalance-related fields:")
        for key in wallet.keys():
            if 'balance' in key.lower() or 'amount' in key.lower() or 'value' in key.lower():
                print(f"  {key}: {wallet[key]}")

    assert_that(wallets).is_not_empty()


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])