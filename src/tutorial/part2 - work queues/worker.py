#!/usr/bin/env python
import os
import pika
import sys
import time


def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    print(f" [x] Received {body!r}")
    for _ in range(body.count(".")):
        time.sleep(1)
        print(".", end="")
        sys.stdout.flush()
    print("")
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
        channel = connection.channel()

        channel.queue_declare(queue="task_queue", durable=True)

        # It is important that QOS is set before the callback is registered.
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(queue="task_queue", on_message_callback=callback)

        print(" [*] Waiting for messages. To exit press CTRL+C")

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
