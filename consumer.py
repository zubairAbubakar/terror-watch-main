import pika

params = pika.URLParameters('amqps://knveduol:J6Drcdy-Np6n-1o44HhTOiHqhkMnaC8L@baboon.rmq.cloudamqp.com/knveduol')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    print(body)


channel.basic_consume(queue='main', on_message_callback=callback)

print('Started Consuming')

channel.start_consuming()

channel.close()