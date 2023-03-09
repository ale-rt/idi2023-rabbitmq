import pika


def callback(ch, method, properties, body):
    try:
        retry_count = properties.headers.get("x-delivery-count", 0)
    except AttributeError:
        retry_count = 0
    print(f" [x] {method.routing_key.upper()}: {body.decode()}")
    print(f" [x] Nacking {body.decode()} / Retry: {retry_count}")
    requeue = retry_count < 10
    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=requeue)


with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    channel.queue_bind(exchange="example5", queue="quorum_queue")
    channel.basic_consume(
        queue="quorum_queue", on_message_callback=callback, auto_ack=False
    )

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.start_consuming()
