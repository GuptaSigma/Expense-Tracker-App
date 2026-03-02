"""
Gold price service — fetches the spot gold price in INR (per gram, 24K).

Primary provider : GoldAPI.io  (https://www.goldapi.io/api/XAU/INR)
Fallback provider: MetalpriceAPI (https://api.metalpriceapi.com/v1/latest)

Both responses are normalised to the same dict shape::

    {
        'gold_price_24k': <float>,   # price per gram in INR (24K)
        'currency': 'INR',
        'timestamp': <str>,          # ISO timestamp
        'status': 'live' | 'fallback' | 'unavailable',
    }

A short TTL cache (5 minutes) is shared across both providers to reduce
rate-limit pressure.
"""

import logging
import threading
import time
from datetime import datetime

import requests

from config import Config

logger = logging.getLogger(__name__)

# 1 troy ounce = 31.1035 grams
_TROY_OZ_TO_GRAM = 31.1035

# Module-level TTL cache — survives across requests within the same process.
_CACHE_TTL = 300  # seconds (5 minutes)
_cache_data = None
_cache_time = 0.0
_cache_lock = threading.Lock()


def _get_cached():
    """Return cached gold price dict if still fresh, else None."""
    with _cache_lock:
        if _cache_data is not None and (time.time() - _cache_time) < _CACHE_TTL:
            return _cache_data
    return None


def _set_cached(data):
    """Store *data* in the module-level cache."""
    global _cache_data, _cache_time
    with _cache_lock:
        _cache_data = data
        _cache_time = time.time()


def _fetch_from_goldapi():
    """Fetch XAU/INR from GoldAPI.io.

    Raises:
        ValueError: API key missing or unexpected response shape.
        requests.RequestException: network / HTTP errors.
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


def _fetch_from_metalprice():
    """Fetch XAU/INR from MetalpriceAPI.com.

    Raises:
        ValueError: API key missing or unexpected response shape.
        requests.RequestException: network / HTTP errors.
    """
    api_key = Config.METALPRICE_API_KEY
    if not api_key:
        raise ValueError("METALPRICE_API_KEY environment variable is not set")

    url = f"{Config.METALPRICE_API_URL}/latest"
    params = {"api_key": api_key, "base": "XAU", "currencies": "INR"}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not data.get("success"):
        raise ValueError(f"MetalpriceAPI returned unsuccessful response: {data}")

    rates = data.get("rates") or {}
    price_per_troy_oz = rates.get("INR")
    if price_per_troy_oz is None:
        raise ValueError(f"MetalpriceAPI response missing INR rate: {data}")

    price_per_gram = round(price_per_troy_oz / _TROY_OZ_TO_GRAM, 2)
    timestamp = datetime.fromtimestamp(data.get("timestamp")).isoformat() if data.get("timestamp") else datetime.now().isoformat()
    return {
        "gold_price_24k": price_per_gram,
        "currency": "INR",
        "timestamp": timestamp,
        "status": "fallback",
    }


def fetch_gold_price_inr():
    """Return the current XAU/INR spot price (per gram, 24K) in INR.

    Tries GoldAPI.io first; automatically falls back to MetalpriceAPI on any
    error.  Results are cached for ``_CACHE_TTL`` seconds to reduce API calls.

    Returns a normalised dict (see module docstring).  The ``status`` field
    is ``'live'`` (GoldAPI), ``'fallback'`` (MetalpriceAPI), or
    ``'unavailable'`` (both failed, ``gold_price_24k`` will be ``None``).
    """
    cached = _get_cached()
    if cached is not None:
        return cached

    # --- Primary: GoldAPI ---
    try:
        result = _fetch_from_goldapi()
        _set_cached(result)
        return result
    except Exception as e:
        logger.warning("GoldAPI fetch failed (%s: %s); trying MetalpriceAPI", type(e).__name__, e)

    # --- Fallback: MetalpriceAPI ---
    try:
        result = _fetch_from_metalprice()
        _set_cached(result)
        return result
    except Exception as e:
        logger.warning("MetalpriceAPI fetch also failed (%s: %s); gold price unavailable", type(e).__name__, e)

    unavailable = {
        "gold_price_24k": None,
        "currency": "INR",
        "timestamp": datetime.now().isoformat(),
        "status": "unavailable",
    }
    # Do not cache the unavailable sentinel so the next request retries.
    return unavailable
