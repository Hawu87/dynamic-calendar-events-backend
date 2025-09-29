# providers/finnhub.py
import os
from datetime import date
from typing import List
from models import IPOEvent
from utils.http import get_json
from utils.dates import parse_date

FINNHUB_BASE = "https://finnhub.io/api/v1/calendar/ipo"

def _fmt(d: date) -> str:
    return d.isoformat()

async def fetch_finnhub_ipos(dt_from: date, dt_to: date) -> List[IPOEvent]:
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    params = {"from": _fmt(dt_from), "to": _fmt(dt_to), "token": finnhub_key}
    payload = await get_json(FINNHUB_BASE, params=params)
    # Finnhub returns { "ipoCalendar": [ { date, symbol, name, exchange, price, numberOfShares, ... } ] }
    rows = (payload or {}).get("ipoCalendar", [])
    events: List[IPOEvent] = []
    for item in rows:
        # Convert price fields (e.g., "10-12") into a range string for consistency
        price_range = item.get("price") or item.get("priceRange")
        events.append(IPOEvent(
            source="finnhub",
            symbol=item.get("symbol"),
            company=item.get("name"),
            exchange=item.get("exchange"),
            ipo_date=parse_date(item.get("date")),
            price_range=str(price_range) if price_range else None,
            shares=(item.get("numberOfShares") or item.get("shares")),
            status=None,
            source_url=None,   # Add if provider supplies
        ))
    return events
