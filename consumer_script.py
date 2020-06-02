from kafka_driver.kafka_consumer import Consumer
from text_process.preprocess import gen_triple
from graph_db.neo4j_driver import  Neo4j
from crawler.indian_crawler import simple_text_process
from text_process.summariser import makeDefaultSummary
import json


if __name__ == "__main__":
    consumer = Consumer("news", "test")
    neo4j = Neo4j()
    print("Start consuming")
    for message in consumer.consumer:
        print("consuming  message")
        x = message.value
        try:
            if 'title' in x and x['title'] is not None:
                if x['body'] is None:
                    x['body'] = ""
                text = makeDefaultSummary(x['title'], x['body'])
                triples = gen_triple(x['title'])
                neo4j.push(triples)
        except:
            print("Xu ly ko dc")

