import logging
import time
from confluent_kafka import Consumer

# Set up structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'event_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['events'])

logging.info("Consumer started. Listening to 'events' topic...")

while True:
    try:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error(f"Consumer error: {msg.error()}")
            continue

        logging.info(f"Received message: {msg.value().decode('utf-8')}")

    except Exception as e:
        logging.exception("Unexpected error occurred while consuming. Retrying in 3 seconds...")
        time.sleep(3)
