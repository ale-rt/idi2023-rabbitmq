#!/usr/bin/env python
import pika
import sys


message = " ".join(sys.argv[1:]) or "info: Hello World!"

with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    channel.exchange_declare(exchange="logs", exchange_type="fanout")
    channel.basic_publish(exchange="logs", routing_key="", body=message)
    print(f" [x] Sent {message!r}")
