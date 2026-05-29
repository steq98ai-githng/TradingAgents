from confluent_kafka import Producer
import json
import logging
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

logger = logging.getLogger(__name__)

class FuturesProducer:
    def __init__(self):
        conf = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}
        self.producer = Producer(**conf)

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def send_data(self, topic, data):
        try:
            self.producer.produce(
                topic,
                key=data.get("symbol", "unknown"),
                value=json.dumps(data),
                callback=self.delivery_report
            )
            self.producer.poll(0)
        except Exception as e:
            logger.error(f"Error sending data to Kafka: {e}")

    def flush(self):
        self.producer.flush()

producer = FuturesProducer()
