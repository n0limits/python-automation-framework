"""
Helper functions for BVNK API testing
"""
from typing import Dict, Any, List


def get_wallet_balance(wallets: List[Dict], currency: str) -> float:
    """
    Get balance for a specific currency from wallet list

    Args:
        wallets: List of wallet dictionaries
        currency: Currency code to find

    Returns:
        Balance as float, or 0.0 if not found
    """
    for wallet in wallets:
        if wallet.get('currency') == currency:
            return float(wallet.get('balance', 0.0))
    return 0.0


def calculate_expected_fee(amount: float, fee_percent: float = 0.01) -> float:
    """
    Calculate expected service fee

    Args:
        amount: Transaction amount
        fee_percent: Fee percentage (default 0.01%)

    Returns:
        Fee amount
    """
    return amount * (fee_percent / 100)


def calculate_net_amount(gross_amount: float, fee_percent: float = 0.01) -> float:
    """
    Calculate net amount after fee

    Args:
        gross_amount: Amount before fee
        fee_percent: Fee percentage

    Returns:
        Net amount after fee
    """
    fee = calculate_expected_fee(gross_amount, fee_percent)
    return gross_amount - fee


def validate_quote_response(quote: Dict[str, Any]) -> bool:
    """
    Validate that quote response contains required fields

    Args:
        quote: Quote response dictionary

    Returns:
        True if valid, False otherwise
    """
    required_fields = ['uuid', 'from', 'to', 'amount', 'rate', 'expiry']
    return all(field in quote for field in required_fields)