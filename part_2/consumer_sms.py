import time
from models import Contact
from RabitMQ_connect import channel
import Mongo_connect

channel.queue_declare(queue='sms_queue')


def send_sms(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending SMS to {contact.phone_number}")
    time.sleep(1)
    contact.send_sms = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_sms(contact_id)


channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print("Waiting for SMS messages. To exit press CTRL+C")
channel.start_consuming()

