from fastapi import APIRouter, HTTPException
from typing import List
from app.db.mongodb import db
from app.models.core import UserDB

router = APIRouter()

@router.get("/", response_description="List all users", response_model=List[UserDB])
async def get_users(limit: int = 100):
    users = []
    if db.client is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    cursor = db.db["users"].find().limit(limit)
    async for document in cursor:
        users.append(UserDB(**document))
    return users

@router.get("/{uid}", response_description="Get a single user by firebase UID", response_model=UserDB)
async def get_user_by_uid(uid: str):
    if db.client is None:
        raise HTTPException(status_code=503, detail="Database not connected")
        
    if (user := await db.db["users"].find_one({"firebase_uid": uid})) is not None:
        return UserDB(**user)
    raise HTTPException(status_code=404, detail=f"User {uid} not found")
