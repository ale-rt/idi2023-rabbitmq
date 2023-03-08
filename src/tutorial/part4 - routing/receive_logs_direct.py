#!/usr/bin/env python
import os
import pika
import sys


severities = sys.argv[1:] if len(sys.argv) > 1 else ["info"]


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key.upper()}: {body.decode()}")


def main():
    with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange="direct_logs", exchange_type="direct")
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        for severity in severities:
            channel.queue_bind(
                exchange="direct_logs", queue=queue_name, routing_key=severity
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
