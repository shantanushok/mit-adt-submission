from fastapi import APIRouter, Depends, HTTPException, status, Header
from firebase_admin import auth
from app.db.mongodb import db
from app.models.core import UserDB, UserCreate
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def verify_firebase_token(authorization: str = Header(None)):
    """Dependency to extract and verify Firebase IdToken."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid auth header")
        token = authorization.split("Bearer ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logger.error(f"Firebase auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@router.post("/login", response_description="Login or register user via Firebase")
async def login_user(firebase_user: dict = Depends(verify_firebase_token)):
    uid = firebase_user.get("uid")
    email = firebase_user.get("email")
    name = firebase_user.get("name")
    
    # Check if user exists in MongoDB
    user_doc = await db.db["users"].find_one({"firebase_uid": uid})
    
    if user_doc:
        return {"status": "success", "message": "User logged in", "user_id": str(user_doc["_id"])}

    # Create new user
    new_user = UserCreate(email=email, name=name, firebase_uid=uid)
    result = await db.db["users"].insert_one(new_user.model_dump(by_alias=True, exclude_none=True))
    
    return {"status": "success", "message": "User registered", "user_id": str(result.inserted_id)}
