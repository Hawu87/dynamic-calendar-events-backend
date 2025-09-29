# providers/fmp.py
import os
from datetime import date
from typing import List
from models import IPOEvent
from utils.http import get_json
from utils.dates import parse_date

FMP_BASE = "https://financialmodelingprep.com/api/v3/ipo-calendar"

def _fmt(d: date) -> str:
    return d.isoformat()

async def fetch_fmp_ipos(dt_from: date, dt_to: date) -> List[IPOEvent]:
    # NOTE: FMP discontinued IPO calendar endpoints as of Aug 31, 2025
    # Returning empty list until alternative endpoint is found
    print("FMP IPO calendar endpoint discontinued - returning empty results")
    return []
    
    # Original code (disabled):
    # fmp_key = os.getenv("FMP_API_KEY")
    # params = {"from": _fmt(dt_from), "to": _fmt(dt_to), "apikey": fmp_key}
    # data = await get_json(FMP_BASE, params=params)

    events: List[IPOEvent] = []
    # FMP fields vary by plan; common ones include: date, symbol, company, exchange, priceRange, numberOfShares, status, link/prospectus
    for item in data or []:
        events.append(IPOEvent(
            source="fmp",
            symbol=item.get("symbol"),
            company=item.get("company") or item.get("companyName"),
            exchange=item.get("exchange"),
            ipo_date=parse_date(item.get("date")),
            price_range=item.get("priceRange"),
            shares=(item.get("numberOfShares") or item.get("shares")),
            status=item.get("status"),
            source_url=item.get("link") or item.get("prospectus") or item.get("url"),
        ))
    return events
