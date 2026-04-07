import asyncio
import random
import logging
from datetime import datetime
from app.api.ws import manager

logger = logging.getLogger(__name__)

class MockTelemetryTask:
    task: asyncio.Task = None
    running: bool = False

    @classmethod
    async def run_simulation(cls):
        cls.running = True
        logger.info("Mock Telemetry generator starting...")
        
        kafka_count = 1205
        db_count = 54030
        
        while cls.running:
            try:
                # Add slight random variations
                kafka_count += random.randint(1, 15)
                db_count += random.randint(0, 5)
                
                payload = {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "cpu": round(random.uniform(20.0, 95.0), 1),
                    "memory": round(random.uniform(40.0, 80.0), 1),
                    "kafka_events": kafka_count,
                    "db_documents": db_count,
                    "last_event": random.choice(["USER_LOGIN", "DATA_SYNC", "SYSTEM_SCAN", "DB_CLEANUP", "API_REQUEST"])
                }
                
                await manager.broadcast(payload)
                await asyncio.sleep(random.uniform(0.8, 2.5))  # Stream data randomly between 0.8s and 2.5s
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Mock telemetry error: {e}")
                await asyncio.sleep(2)

    @classmethod
    def start(cls):
        if not cls.running:
            cls.task = asyncio.create_task(cls.run_simulation())

    @classmethod
    def stop(cls):
        cls.running = False
        if cls.task:
            cls.task.cancel()
        logger.info("Mock Telemetry stopped.")
