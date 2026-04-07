from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional
from datetime import datetime

# Represents an ObjectId field in the database.
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserDB(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    firebase_uid: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class UserCreate(UserBase):
    firebase_uid: str
