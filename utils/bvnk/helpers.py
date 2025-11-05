"""
Helper functions for BVNK API testing
"""
from typing import List, Dict, Any, Optional


def get_wallet_balance(wallets: List[Dict], currency: str) -> float:
    """
    Get balance for a specific currency from wallet list

    Args:
        wallets: List of wallet dictionaries from API
        currency: Currency code (e.g., 'ETH', 'TRX')

    Returns:
        Balance as float, or 0.0 if not found
    """
    for wallet in wallets:
        # Currency is nested inside a 'currency' object
        currency_obj = wallet.get('currency', {})
        wallet_code = currency_obj.get('code', '')

        if wallet_code == currency:
            # Balance is a string, need to convert to float
            balance_str = wallet.get('balance', '0')
            try:
                return float(balance_str)
            except (ValueError, TypeError):
                return 0.0

    return 0.0


def get_wallet_by_currency(wallets: List[Dict], currency: str) -> Optional[Dict]:
    """
    Get wallet object for a specific currency

    Args:
        wallets: List of wallet dictionaries
        currency: Currency code

    Returns:
        Wallet dict or None if not found
    """
    for wallet in wallets:
        # Currency is nested inside a 'currency' object
        currency_obj = wallet.get('currency', {})
        wallet_code = currency_obj.get('code', '')

        if wallet_code == currency:
            return wallet

    return None


def calculate_expected_fee(amount: float, fee_percent: float = 0.0001) -> float:
    """
    Calculate expected service fee

    Service fee for all conversions/trades is 0.01%

    Args:
        amount: Amount to calculate fee for
        fee_percent: Fee percentage as decimal (0.0001 = 0.01%)

    Returns:
        Fee amount

    Example:
        calculate_expected_fee(100, 0.0001) = 0.01  (0.01% of 100)
        calculate_expected_fee(1.0, 0.0001) = 0.0001  (0.01% of 1.0)
    """
    return amount * fee_percent


def calculate_net_amount(gross_amount: float, fee_percent: float = 0.0001) -> float:
    """
    Calculate net amount after fee deduction

    Service fee for all conversions/trades is 0.01%

    Args:
        gross_amount: Gross amount before fee
        fee_percent: Fee percentage as decimal (0.0001 = 0.01%)

    Returns:
        Net amount after fee

    Example:
        calculate_net_amount(100, 0.0001) = 99.99  (100 - 0.01% fee)
    """
    fee = calculate_expected_fee(gross_amount, fee_percent)
    return gross_amount - fee


def validate_quote_response(quote: Dict[str, Any]) -> bool:
    """
    Validate quote response has required fields

    Args:
        quote: Quote response dictionary

    Returns:
        True if valid, False otherwise
    """
    required_fields = ['uuid', 'from', 'to', 'amountIn', 'price']
    return all(field in quote for field in required_fields)