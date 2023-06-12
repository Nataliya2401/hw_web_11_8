import pika

import json
from bson import json_util

# sys.path.insert(1, os.path.join(sys.path[0], '../cd'))

from Mongo.models import User

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_msg_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    message = json_util.loads(body.decode())

    user = User.objects(id=message['id'])
    user.update(is_sent=True)

    print(f" [x] Received {message}")
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_msg_queue', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()
