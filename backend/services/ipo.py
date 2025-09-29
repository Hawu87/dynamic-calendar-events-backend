# services/ipo.py
from datetime import date
from typing import List
from models import IPOEvent
from providers.fmp import fetch_fmp_ipos
from providers.finnhub import fetch_finnhub_ipos

def _key(e: IPOEvent) -> tuple:
    # (symbol, date) works well; fall back to (company, date)
    return (e.symbol or e.company or "").upper(), e.ipo_date

def _prefer(a: IPOEvent, b: IPOEvent) -> IPOEvent:
    # Simple preference rule: keep FMP if it has prospectus/price_range, else Finnhub
    if a.source == "fmp" and (a.price_range or a.source_url):
        return a
    if b.source == "fmp" and (b.price_range or b.source_url):
        return b
    # Fallback: first non-null wins
    merged = IPOEvent(
        source=f"{a.source}+{b.source}",
        symbol=a.symbol or b.symbol,
        company=a.company or b.company,
        exchange=a.exchange or b.exchange,
        ipo_date=a.ipo_date or b.ipo_date,
        price_range=a.price_range or b.price_range,
        shares=a.shares or b.shares,
        status=a.status or b.status,
        source_url=a.source_url or b.source_url,
    )
    return merged

async def get_ipos(dt_from: date, dt_to: date) -> List[IPOEvent]:
    import asyncio
    # gather concurrently:
    fmp, fin = await asyncio.gather(
        fetch_fmp_ipos(dt_from, dt_to), 
        fetch_finnhub_ipos(dt_from, dt_to)
    )

    by_key: dict[tuple, IPOEvent] = {}
    for ev in [*fmp, *fin]:
        k = _key(ev)
        if k in by_key:
            by_key[k] = _prefer(by_key[k], ev)
        else:
            by_key[k] = ev
    return list(by_key.values())
