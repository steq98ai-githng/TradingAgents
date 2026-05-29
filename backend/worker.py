import asyncio
import json
import logging
from confluent_kafka import Consumer, KafkaError
from backend.database import AsyncSessionLocal, MNQCandle
from datetime import datetime
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_CANDLES = "mnq_candles"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_candles():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'backend_worker',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(**conf)
    consumer.subscribe([TOPIC_CANDLES])

    logger.info(f"Started consuming from {TOPIC_CANDLES}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                await asyncio.sleep(0.1)
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                    break

            data = json.loads(msg.value().decode('utf-8'))
            logger.info(f"Received candle: {data}")

            async with AsyncSessionLocal() as session:
                candle = MNQCandle(
                    symbol=data["symbol"],
                    timestamp=datetime.fromisoformat(data["timestamp"]),
                    open=data["open"],
                    high=data["high"],
                    low=data["low"],
                    close=data["close"],
                    volume=data["volume"],
                    interval=data["interval"]
                )
                session.add(candle)
                await session.commit()
    except Exception as e:
        logger.error(f"Worker error: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    asyncio.run(consume_candles())

async def run_worker():
    # This would combine the Kafka consumer and signal broadcasting
    # For now, we'll mock the broadcast to WebSocket
    pass
