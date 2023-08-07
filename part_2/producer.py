from random import choice
import pika
from faker import Faker
from models import Contact
import Mongo_connect
from RabitMQ_connect import channel, connection

fake = Faker()
notification_options = ['sms', 'email']


channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

contacts = []
for i in range(20):
    contacts.append({
        "fullname": fake.name(),
        "company": fake.company(),
        "email": fake.email(),
        "phone_number": fake.msisdn(),
        "choice_for_message": choice(notification_options),
        "send_email": False,
        "send_sms": False
    })

for contact_data in contacts:
    contact = Contact(**contact_data)
    contact.save()

    if contact.choice_for_message == 'email' and not contact.send_email:
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id).encode())

    if contact.choice_for_message == 'sms' and not contact.send_sms:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=str(contact.id).encode())

print("Contacts and messages sent to queues")

connection.close()
