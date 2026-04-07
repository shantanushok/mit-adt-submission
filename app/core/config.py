from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AMD Internal Dashboard API"
    
    # CORS setup: allows frontend on standard dev ports
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500", # Usually for Live Server
    ]

    # MongoDB Config
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "amd_database"

    # Kafka Config
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    # ImageKit Config
    IMAGEKIT_PUBLIC_KEY: str = ""
    IMAGEKIT_PRIVATE_KEY: str = ""
    IMAGEKIT_URL_ENDPOINT: str = ""

    # Firebase details
    FIREBASE_CREDENTIALS_PATH: str = "firebase-adminsdk.json"

    class Config:
        env_file = ".env"

settings = Settings()
