import pika
import random
import time


# Add a roughly every second to the exchange with a random routing key

routing_keys = ["info", "warning", "error"]

with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    channel.exchange_declare(exchange="example1", exchange_type="direct")
    idx = 0
    while True:
        idx += 1
        message = f"Message {idx}"
        channel.basic_publish(
            exchange="example1", routing_key=random.choice(routing_keys), body=message
        )
        print(f" [x] Sent: {message!r}")
        time.sleep(1)
