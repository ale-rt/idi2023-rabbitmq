import pika
import random
import time


# Add a roughly every second to the exchange with a random routing key composed
# of three parts: log level, actor, and domain.

log_levels = ["info", "warning", "error"]
actor = ["user", "system"]
domain = ["login", "logout", ""]

with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    channel.exchange_declare(exchange="example3", exchange_type="topic")
    idx = 0
    while True:
        idx += 1
        # If domain is an empty string, we don't want a trailing dot.
        routing_key = ".".join(
            [
                random.choice(log_levels),
                random.choice(actor),
                random.choice(domain),
            ]
        ).rstrip(".")
        message = f"Message {idx}"
        channel.basic_publish(
            exchange="example3", routing_key=routing_key, body=message
        )
        print(f" [x] {routing_key!r} {message!r}")
        time.sleep(1)
