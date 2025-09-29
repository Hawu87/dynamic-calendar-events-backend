# utils/http.py
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Dict, Any, Optional

DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=8))
async def _get_json_with_retry(url: str, params: dict | None = None, headers: dict | None = None):
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        r = await client.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

async def get_json(url: str, params: Optional[Dict[str, Any]] = None, headers: dict | None = None) -> Optional[Dict[str, Any]]:
    """Fetch JSON data from URL with optional query parameters"""
    try:
        return await _get_json_with_retry(url, params, headers)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None