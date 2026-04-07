from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.init_db import setup_indexes
from app.services.kafka_service import KafkaService
from app.services.firebase_service import init_firebase
from app.services.imagekit_service import init_imagekit
from app.worker.kafka_consumer import KafkaWorker
from app.worker.mock_generator import MockTelemetryTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Events
    logger.info("Initializing services...")
    init_firebase()
    init_imagekit()
    await connect_to_mongo()
    await setup_indexes()
    await KafkaService.connect()
    await KafkaWorker.start()
    MockTelemetryTask.start()
    yield
    # Shutdown Events
    logger.info("Shutting down services...")
    await close_mongo_connection()
    await KafkaService.disconnect()
    await KafkaWorker.stop()
    MockTelemetryTask.stop()

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="AMD Backend connecting to MongoDB, Kafka, Firebase, and ImageKit.",
    lifespan=lifespan
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}. System is ready for integration."
    }

@app.get("/api/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

# API routes
from app.api.endpoints import router as api_router
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
