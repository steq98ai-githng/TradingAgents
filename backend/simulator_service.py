import asyncio
import logging
from tradingagents.dataflows.futures_simulator import MNQSimulator
from backend.kafka_producer import producer
import os

TOPIC_CANDLES = "mnq_candles"
logger = logging.getLogger(__name__)

async def run_simulator():
    sim = MNQSimulator()
    logger.info("MNQ Simulator started")
    while True:
        try:
            candle = sim.generate_candle()
            producer.send_data(TOPIC_CANDLES, candle)
            logger.info(f"Published candle: {candle['timestamp']} - {candle['close']}")
            # Simulate 1-minute candles, but run faster for testing if needed
            await asyncio.sleep(10) # 10 seconds for demo purposes
        except Exception as e:
            logger.error(f"Simulator error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_simulator())
