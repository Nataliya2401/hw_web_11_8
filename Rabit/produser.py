import pika

from datetime import datetime

import json
from bson import json_util

from faker import Faker

from Mongo.models import User

NUMBER_CONTACTS = 10
fake = Faker()


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_msg', exchange_type='direct')
channel.queue_declare(queue='task_msg_queue', durable=True)
channel.queue_bind(exchange='task_msg', queue='task_msg_queue')


def create_users():
    User.drop_collection()
    for i in range(NUMBER_CONTACTS):
        User(fullname=fake.name(), email=fake.email()).save()


def main():
    contacts = User.objects(is_sent=False)
    for contact in contacts:
        message = {
            "id": contact.id,
            "text_msg": fake.text(),
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange='task_msg',
            routing_key='task_msg_queue',
            body=json_util.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    create_users()
    main()
