# models.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class IPOEvent(BaseModel):
    source: str                               # "fmp" or "finnhub"
    symbol: Optional[str] = None
    company: Optional[str] = None
    exchange: Optional[str] = None
    ipo_date: Optional[date] = None           # expected date
    price_range: Optional[str] = None         # e.g., "$10–$12"
    shares: Optional[int] = None              # raw count if available
    status: Optional[str] = None              # e.g., "expected"/"confirmed"/"postponed"
    source_url: Optional[str] = None
