import json
import pika

params = pika.URLParameters(
    'amqps://bzkwawqu:yrgbBmLP3aS4gFnRVeUZU5KFHp1XqJOZ@rattlesnake.rmq.cloudamqp.com/bzkwawqu'
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin',
                          body=json.dumps(body), properties=properties)
