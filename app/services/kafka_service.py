import logging
import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

logger = logging.getLogger(__name__)

class KafkaService:
    producer: AIOKafkaProducer = None

    @classmethod
    async def connect(cls):
        logger.info("Connecting to Kafka...")
        try:
            cls.producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await cls.producer.start()
            logger.info("Kafka producer connected.")
        except Exception as e:
            logger.warning(f"Kafka warning: Could not connect to {settings.KAFKA_BOOTSTRAP_SERVERS}: {e}")

    @classmethod
    async def disconnect(cls):
        logger.info("Disconnecting from Kafka...")
        if cls.producer:
            await cls.producer.stop()
            logger.info("Kafka producer disconnected.")

    @classmethod
    async def send_message(cls, topic: str, message: dict):
        if not cls.producer:
            logger.warning("Kafka producer not active. Message dropped.")
            return
        await cls.producer.send_and_wait(topic, message)
