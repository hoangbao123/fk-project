from kafka import KafkaProducer, KafkaConsumer
import json

producer = KafkaProducer(bootstrap_servers="34.87.20.130:9092", 
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))
data = {"hi1":"first"}
future = producer.send("fakenew", data)
meta = future.get(timeout=10)
print(meta.topic)
print(meta.partition)
print(meta.offset)