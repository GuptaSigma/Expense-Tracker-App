"""
GoldAPI.io service helper — fetches the spot gold price in INR (per gram, 24K).

Endpoint: https://www.goldapi.io/api/XAU/INR
Authentication header: x-access-token: <GOLD_API_KEY>
"""

import logging
from datetime import datetime

import requests

from config import Config

logger = logging.getLogger(__name__)

# 1 troy ounce = 31.1035 grams (GoldAPI returns price per troy ounce)
_TROY_OZ_TO_GRAM = 31.1035


def fetch_gold_price_inr():
    """Fetch the current XAU/INR spot price from GoldAPI.io.

    Returns a dict::

        {
            'gold_price_24k': <float>,   # price per gram in INR (24K)
            'currency': 'INR',
            'timestamp': <str>,          # ISO timestamp from GoldAPI
            'status': 'live',
        }

    Raises:
        ValueError: when the API key is not configured or the response is
            missing the expected ``price`` field.
        requests.RequestException: on network / HTTP errors so callers can
            apply their own fallback logic.
    """
    api_key = Config.GOLD_API_KEY
    if not api_key:
        raise ValueError("GOLD_API_KEY environment variable is not set")

    url = f"{Config.GOLD_API_URL}/XAU/INR"
    headers = {"x-access-token": api_key}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    price_per_troy_oz = data.get("price")
    if price_per_troy_oz is None:
        raise ValueError(f"Unexpected GoldAPI response (missing 'price'): {data}")

    price_per_gram = round(price_per_troy_oz / _TROY_OZ_TO_GRAM, 2)

    return {
        "gold_price_24k": price_per_gram,
        "currency": "INR",
        "timestamp": data.get("timestamp") or datetime.now().isoformat(),
        "status": "live",
    }
