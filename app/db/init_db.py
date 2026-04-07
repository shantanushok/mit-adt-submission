import logging
from app.db.mongodb import db

logger = logging.getLogger(__name__)

async def setup_indexes():
    """Create indexes in MongoDB collections if they don't exist."""
    try:
        # Create unique indexes on user identification
        await db.db["users"].create_index("email", unique=True)
        await db.db["users"].create_index("firebase_uid", unique=True)
        
        # Create index on events timestamp for quick sorting and analytics queries
        await db.db["events"].create_index([("timestamp", -1)])
        
        logger.info("Database indexes successfully configured.")
    except Exception as e:
        logger.error(f"Error setting up database indexes (Ensure MongoDB is running): {e}")
