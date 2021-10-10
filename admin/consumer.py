import json
import pika
import django

django.setup()
params = pika.URLParameters(
    'amqps://bzkwawqu:yrgbBmLP3aS4gFnRVeUZU5KFHp1XqJOZ@rattlesnake.rmq.cloudamqp.com/bzkwawqu'
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    from products.models import Product

    print(" [x] Received in admin %r" % body)
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print('Product likes incremented.')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print('Started consuming')

channel.start_consuming()

channel.close()
