from kafka_driver.kafka_consumer import Consumer
from text_process.preprocess import gen_triple
from graph_db.neo4j_driver import  Neo4j
from text_process.summariser import makeDefaultSummary
import json


if __name__ == "__main__":
    consumer = Consumer("baohn", "test")
    neo4j = Neo4j()
    for message in consumer.consumer:
        x = json.loads(message.value)
        if 'title' in x and x['title'] is not None :
            # text = makeDefaultSummary(x['title'], x['body'])
            triples = gen_triple(x['title'])
            neo4j.push(triples)

