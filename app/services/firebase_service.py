import firebase_admin
from firebase_admin import credentials
import logging
import os
from app.core.config import settings

logger = logging.getLogger(__name__)

def init_firebase():
    """Initializes Firebase Admin SDK."""
    if not firebase_admin._apps:
        try:
            if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin initialized successfully.")
            else:
                logger.warning(f"Firebase credentials not found at {settings.FIREBASE_CREDENTIALS_PATH}. Skipping initialization.")
        except Exception as e:
            logger.error(f"Error initializing Firebase: {e}")
