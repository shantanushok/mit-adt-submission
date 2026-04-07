from imagekitio import ImageKit
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

imagekit_client = None

def init_imagekit():
    global imagekit_client
    try:
        if settings.IMAGEKIT_PUBLIC_KEY and settings.IMAGEKIT_PRIVATE_KEY:
            imagekit_client = ImageKit(
                private_key=settings.IMAGEKIT_PRIVATE_KEY,
                public_key=settings.IMAGEKIT_PUBLIC_KEY,
                url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
            )
            logger.info("ImageKit client initialized.")
        else:
            logger.warning("ImageKit credentials missing. Client not initialized.")
    except Exception as e:
        logger.error(f"Error initializing ImageKit: {e}")
