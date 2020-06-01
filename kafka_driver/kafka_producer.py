from kafka import KafkaProducer
import json
import time


class Producer:
    producer = None

    def __init__(self):
        if Producer.producer is None:
            print("Construct Producer")
            Producer.producer = KafkaProducer(
                bootstrap_servers=['34.87.20.130:9092'],
                value_serializer=lambda x:
                json.dumps(x).encode('utf-8'))

    def send_message(self, topic, value):
        print("Send_mess to {} with value {}".format(topic, value))
        self.producer.send(topic, value=value)


