import pika
import time


# Add a roughly every second to the exchange

with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    channel.exchange_declare(exchange="example5", exchange_type="fanout")
    idx = 0
    while True:
        idx += 1
        message = f"Message {idx}"
        channel.basic_publish(exchange="example5", body=message, routing_key="")
        print(f" [x] Sent: {message!r}")
        time.sleep(1)
