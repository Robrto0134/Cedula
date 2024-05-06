import json
import pika
class Rabbit(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def produce(self, body, queue='cedula'):
        self.channel.queue_declare(queue=queue, durable=True)

        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        self.connection.close()

    def consume(self, queue='cedula'):
        self.channel.queue_declare(queue=queue, durable=True)
        method_frame, properties, body = next(self.channel.consume(queue))
        body = json.loads(body)
        self.channel.basic_ack(method_frame.delivery_tag)
        return body 
