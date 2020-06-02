import pprint
from datetime import datetime
from crawler_preprocess.parser import returnCoolHTML, parser_HTML
from mongo_driver.article import Article
from kafka_driver.kafka_producer import Producer
from mongo_driver.models import db

pp = pprint.PrettyPrinter(indent=4)
producer = Producer()


def get_cnn_news(size, from_page):
    # for i in range(18):
    url = f"https://edition.cnn.com/search?size={size}&q=us%20election&from={from_page}"
    data = parser_HTML(url)
    print(data)


if __name__ == "__main__":
    get_cnn_news(10, 1)