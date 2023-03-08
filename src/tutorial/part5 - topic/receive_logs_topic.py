#!/usr/bin/env python
import os
import pika
import sys


binding_keys = sys.argv[1:] or ["#"]


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}: {body.decode()}")


def main():
    with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange="topic_logs", exchange_type="topic")
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        for binding_key in binding_keys:
            channel.queue_bind(
                exchange="topic_logs", queue=queue_name, routing_key=binding_key
            )
        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )

        print(" [*] Waiting for logs. To exit press CTRL+C")

        channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
