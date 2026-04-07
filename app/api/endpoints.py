from fastapi import APIRouter
import logging
from app.db.mongodb import db
from app.db.mongodb import db
from app.services.kafka_service import KafkaService
from app.api import auth, upload, ws

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(upload.router, prefix="/upload", tags=["Uploads"])
router.include_router(ws.router, prefix="/ws", tags=["WebSockets"])
logger = logging.getLogger(__name__)

@router.get("/status")
async def api_status():
    """Checks the status of the various external services"""
    status = {
        "mongodb": "disconnected",
        "kafka": "disconnected"
    }
    
    # Check Mongo
    try:
        if db.client is not None:
            await db.client.admin.command('ping')
            status["mongodb"] = "connected"
    except Exception as e:
        logger.warning(f"MongoDB ping failed: {e}")
        
    # Check Kafka
    if KafkaService.producer is not None:
         status["kafka"] = "connected"
         
    return status

@router.post("/events")
async def send_event(event_type: str, data: dict):
    """Sends a mock event to Kafka"""
    if KafkaService.producer:
        await KafkaService.send_message("amd-events", {"type": event_type, "data": data})
        return {"status": "Event sent to topic 'amd-events'"}
    return {"status": "Kafka not connected, event dropped"}
