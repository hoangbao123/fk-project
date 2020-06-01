from kafka import KafkaConsumer
import json


class Consumer:
    def __init__(self, topic, group_id):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=['34.87.20.130:9092'],
                                      auto_offset_reset='earliest',
                                      enable_auto_commit=True,
                                      group_id=group_id,
                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')))


if __name__ == '__main__':
    consumer = Consumer('app-log', 'update-score')
    print("Consuming")
    for mess in consumer.consumer:
        print(mess.value)