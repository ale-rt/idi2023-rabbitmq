import pika


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key.upper()}: {body.decode()}")


with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    # Read messages from exchange example1 which is of type direct
    # for all the routing keys
    channel.exchange_declare(exchange="example2", exchange_type="fanout")
    result = channel.queue_declare(queue="", auto_delete=True, durable=False)
    queue_name = result.method.queue
    channel.queue_bind(exchange="example2", queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.start_consuming()
