import os
import json
import pika
from main import Product, db

params = pika.URLParameters(os.environ['CLOUDAMQP_URL'])


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print(" [x] Received in admin %r" % body)
    data = json.loads(body)
    print(data)


    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print('Started consuming')

channel.start_consuming()

channel.close()
