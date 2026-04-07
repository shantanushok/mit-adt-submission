from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.core import PyObjectId

class EventBase(BaseModel):
    event_type: str
    metadata: dict = {}

class EventDB(EventBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    timestamp: datetime = Field(default_factory=datetime.now)

class EventCreate(EventBase):
    pass
