import json
import pika

from main import Post, db

params = pika.URLParameters('amqps://knveduol:J6Drcdy-Np6n-1o44HhTOiHqhkMnaC8L@baboon.rmq.cloudamqp.com/knveduol')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main application')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'post_created':
        post = Post(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(post)
        db.session.commit()
        print('Post created in main app')

    elif properties.content_type == 'post_updated':
        post = Post.query.get(data['id'])
        post.title = data['title']
        post.image = data['image']
        db.session.commit()
        print('Post updated in main app')

    elif properties.content_type == 'post_deleted':
        post = Post.query.get(data)
        db.session.delete(post)
        db.session.commit()
        print('Post deleted in main app')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
