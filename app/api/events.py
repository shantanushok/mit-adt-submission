from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from app.db.mongodb import db
from app.models.event import EventDB, EventCreate

router = APIRouter()

@router.get("/", response_description="List recent events", response_model=List[EventDB])
async def get_events(limit: int = 50):
    events = []
    if db.client is None:
        raise HTTPException(status_code=503, detail="Database not connected")
        
    cursor = db.db["events"].find().sort("timestamp", -1).limit(limit)
    async for document in cursor:
        events.append(EventDB(**document))
    return events

@router.post("/", response_description="Insert a new event via API", response_model=EventDB)
async def create_event(event: EventCreate):
    if db.client is None:
        raise HTTPException(status_code=503, detail="Database not connected")
        
    new_event = EventDB(**event.model_dump())
    result = await db.db["events"].insert_one(new_event.model_dump(by_alias=True, exclude_none=True))
    created_event = await db.db["events"].find_one({"_id": result.inserted_id})
    return EventDB(**created_event)
