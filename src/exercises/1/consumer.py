import pika
import sys


routing_keys = sys.argv[1:] if len(sys.argv) > 1 else ["info"]


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key.upper()}: {body.decode()}")


with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    # Read messages from exchange example1 which is of type direct
    # for all the routing keys
    channel.exchange_declare(exchange="example1", exchange_type="direct")
    result = channel.queue_declare(queue="queue1")
    queue_name = result.method.queue
    for routing_key in routing_keys:
        channel.queue_bind(
            exchange="example1", queue=queue_name, routing_key=routing_key
        )
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.start_consuming()
