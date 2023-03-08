#!/usr/bin/env python
import pika
import sys


routing_key = sys.argv[1] if len(sys.argv) >= 2 else "anonymous.info"
message = " ".join(sys.argv[2:]) or "Hello World!"

with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

    channel.basic_publish(exchange="topic_logs", routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}: {message!r}")
