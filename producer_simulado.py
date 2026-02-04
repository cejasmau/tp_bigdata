import time
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    api_version=(2, 8, 1),
    value_serializer=lambda v: v.encode("utf-8")
)

tickers = ["AAPL", "MSFT", "GOOG"]
prices = {
    "AAPL": 187.0,
    "MSFT": 412.0,
    "GOOG": 140.0
}

print("Productor Kafka iniciado...")

while True:
    ticker = random.choice(tickers)
    prices[ticker] += random.uniform(-0.5, 0.5)

    event_time = datetime.utcnow().isoformat()
    price = round(prices[ticker], 2)

    message = f"{ticker},{event_time},{price}"
    producer.send("market-data", message)

    print("Enviado:", message)
    time.sleep(2)
