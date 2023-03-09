import pika
import sys


routing_key = sys.argv[1]


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}: {body.decode()}")


with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    # Read messages from exchange example3 which is of type topic
    # for routing keys that matched the routing_key variable
    channel.exchange_declare(exchange="example3", exchange_type="topic")
    result = channel.queue_declare(queue="")
    queue_name = result.method.queue
    channel.queue_bind(exchange="example3", queue=queue_name, routing_key=routing_key)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.start_consuming()
