# IPO Calendar Backend (V0)

A FastAPI backend that generates dynamic IPO calendar events from financial data providers.

## Features (V0)

- ✅ **JSON API**: Get IPO events as JSON from `/api/ipos`
- ✅ **Calendar Export**: Download .ics calendar file from `/api/ipos.ics`
- ✅ **Finnhub Data Source**: Live IPO data from Finnhub API
- ✅ **Date Range Filtering**: Query IPOs within specific date ranges
- ✅ **Deduplication**: Ready for multiple sources when available

## Data Sources Status

- ✅ **Finnhub**: Active and working
- ❌ **FMP**: Discontinued IPO endpoints as of Aug 31, 2025 (need paid upgrade)
- 🔍 **Future**: Will add alternative providers (NASDAQ, SEC filings, etc.)

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** (optional - will return empty results without keys):
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Start the server**:
   ```bash
   uvicorn main:app --reload --port 8001
   ```

4. **Test the endpoints**:
   - JSON API: http://localhost:8001/api/ipos
   - Calendar file: http://localhost:8001/api/ipos.ics

## API Endpoints

### GET `/api/ipos`
Returns IPO events as JSON.

**Query Parameters:**
- `frm` (date): Start date (default: today)
- `to` (date): End date (default: today + 90 days)

**Example:**
```bash
curl "http://localhost:8001/api/ipos?frm=2024-01-01&to=2024-12-31"
```

### GET `/api/ipos.ics`
Returns IPO events as downloadable .ics calendar file.

**Query Parameters:** Same as `/api/ipos`

**Example:**
```bash
curl "http://localhost:8001/api/ipos.ics" -o ipo-calendar.ics
```

## Testing

Run the test script to verify functionality with mock data:
```bash
python3 test_ipo_calendar.py
```

This generates a `test_ipo_calendar.ics` file you can import into any calendar app.

## API Keys Setup

Get API keys from:
- **FMP**: https://financialmodelingprep.com/developer/docs
- **Finnhub**: https://finnhub.io/

Add them to your `.env` file:
```
FMP_API_KEY=your_fmp_key_here
FINNHUB_API_KEY=your_finnhub_key_here
```

## V0 Goal ✅

**Achieved**: Basic website where users can download a static IPO calendar (.ics) generated via reliable financial sources. Users can import into Apple/Google Calendar manually.