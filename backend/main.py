# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from datetime import date, timedelta
from services.ipo import get_ipos
from utils.ics import generate_ics_calendar

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware to allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/ipos")
async def ipos(
    frm: date = Query(default=date.today()),
    to: date = Query(default=(date.today()+timedelta(days=90)))
):
    events = await get_ipos(frm, to)
    return {"count": len(events), "items": [e.model_dump() for e in events]}

@app.get("/api/ipos.ics")
async def ipos_ics(
    frm: date = Query(default=date.today()),
    to: date = Query(default=(date.today()+timedelta(days=90)))
):
    events = await get_ipos(frm, to)
    ics_content = generate_ics_calendar(events)
    
    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": "attachment; filename=ipo-calendar.ics",
            "Cache-Control": "no-cache"
        }
    )
