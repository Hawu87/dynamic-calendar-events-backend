from datetime import date, datetime
from typing import List
from models import IPOEvent
from utils.dates import format_date_for_ics
import uuid

def generate_ics_calendar(events: List[IPOEvent]) -> str:
    """Generate .ics calendar file content from IPO events"""
    
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//IPO Calendar//IPO Events//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:IPO Calendar",
        "X-WR-CALDESC:Upcoming Initial Public Offerings"
    ]
    
    for event in events:
        if not event.ipo_date:
            continue
            
        # Generate unique ID for this event
        event_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{event.symbol or event.company}-{event.ipo_date}"))
        
        # Format date for .ics (YYYYMMDD)
        date_str = format_date_for_ics(event.ipo_date)
        
        # Create event title
        title = f"IPO: {event.company or event.symbol or 'Unknown Company'}"
        if event.symbol:
            title += f" ({event.symbol})"
        
        # Create description
        description_parts = []
        if event.exchange:
            description_parts.append(f"Exchange: {event.exchange}")
        if event.price_range:
            description_parts.append(f"Price Range: {event.price_range}")
        if event.shares:
            description_parts.append(f"Shares: {event.shares:,}")
        if event.status:
            description_parts.append(f"Status: {event.status}")
        if event.source_url:
            description_parts.append(f"More info: {event.source_url}")
        
        description_parts.append(f"Data source: {event.source}")
        description = "\\n".join(description_parts)
        
        # Add event to calendar
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{event_id}",
            f"DTSTART;VALUE=DATE:{date_str}",
            f"DTEND;VALUE=DATE:{date_str}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{description}",
            "STATUS:CONFIRMED",
            "TRANSP:TRANSPARENT",
            f"CREATED:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"LAST-MODIFIED:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            "END:VEVENT"
        ])
    
    lines.append("END:VCALENDAR")
    
    # Join with CRLF as per RFC 5545
    return "\r\n".join(lines)