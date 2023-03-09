import pika


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key.upper()}: {body.decode()}")
    try:
        if method.redelivered:
            print(" [x] Already processed, acking")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        raise Exception("Something went wrong")
    except Exception as e:
        print(f" [x] Nacking {body.decode()} {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=not method.redelivered)


with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as connection:
    channel = connection.channel()
    # Read messages from exchange example1 which is of type direct
    # for all the routing keys
    channel.exchange_declare(exchange="example4", exchange_type="fanout")
    result = channel.queue_declare(queue="nack_queue", durable=False)
    queue_name = result.method.queue
    channel.queue_bind(exchange="example4", queue=queue_name)
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False
    )

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.start_consuming()
