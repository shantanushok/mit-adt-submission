import asyncio
import logging
import json
from aiokafka import AIOKafkaConsumer
from app.core.config import settings

logger = logging.getLogger(__name__)

class KafkaWorker:
    consumer: AIOKafkaConsumer = None
    task: asyncio.Task = None

    @classmethod
    async def start(cls):
        try:
            cls.consumer = AIOKafkaConsumer(
                "amd-events",
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id="amd-consumer-group",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )
            await cls.consumer.start()
            logger.info("Kafka consumer started listening on 'amd-events'")
            cls.task = asyncio.create_task(cls.consume_messages())
        except Exception as e:
            logger.warning(f"Consumer could not start. Broker likely down: {e}")

    @classmethod
    async def consume_messages(cls):
        try:
            async for msg in cls.consumer:
                logger.info(f"Consumed message on topic: {msg.topic} | key: {msg.key} | value: {msg.value}")
                # We can wire this up to our database or services later
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")

    @classmethod
    async def stop(cls):
        if cls.task:
            cls.task.cancel()
            try:
                await cls.task
            except asyncio.CancelledError:
                pass
        if cls.consumer:
            await cls.consumer.stop()
            logger.info("Kafka consumer stopped.")
