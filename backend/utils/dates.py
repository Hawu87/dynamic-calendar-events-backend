from datetime import date, datetime
from typing import Optional

def parse_date(date_str: Optional[str]) -> Optional[date]:
    """Parse date string in various formats to date object"""
    if not date_str:
        return None
    
    try:
        # Try ISO format first (YYYY-MM-DD)
        return datetime.fromisoformat(date_str).date()
    except ValueError:
        pass
    
    # Add other date format parsing if needed
    try:
        # Try MM/DD/YYYY format
        return datetime.strptime(date_str, "%m/%d/%Y").date()
    except ValueError:
        pass
    
    try:
        # Try YYYY-MM-DD format explicitly
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass
    
    return None

def format_date_for_ics(dt: date) -> str:
    """Format date for .ics file (YYYYMMDD format)"""
    return dt.strftime("%Y%m%d")