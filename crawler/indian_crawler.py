import pprint
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import re
from crawler_preprocess.parser import parser_HTML
from kafka_driver.kafka_producer import Producer
from mongo_driver.article import Article
from mongo_driver.models import db

pp = pprint.PrettyPrinter(indent=4)
producer = Producer()
pool = ThreadPoolExecutor(max_workers=10)
db_name = "news"
topic = "news"


def get_cnn_news():
    for i in range(15):
        url = f"https://timesofindia.indiatimes.com/topic/Us-Election-2016/news/{i}"
        data = parser_HTML(url)
        class1 = data.find_all("li", attrs={"itemtype": "http://schema.org/ListItem"}, class_="article")
        for item in class1:
            pool.submit(get_detail_for_page, item)


def get_detail_for_page(item):
    print("processing")
    try:
        url = item.find("meta", attrs={"itemprop": "url"}).attrs['content']
        detail_data = parser_HTML(url)
        content = detail_data.find("div", class_="_3WlLe clearfix")
        if content is None:
            content = detail_data.find("div", class_="_3YYSt clearfix")
        if content is None:
            content = detail_data.find("div", class_="_1IaAp clearfix")
        if content is None:
            body = None
            print("no content")
        else:
            body = content.text
        title = item.find("meta", attrs={"itemprop": "name"}).attrs['content']
        push_to_mongo(url, title, body)
    except Exception:
        print("Exception in p")


def push_to_mongo(url, title, body):
    # print("push to mongo")
    try:
        article = Article(url)
        if title is not None:
            article.title = simple_text_process(title)
        if body is not None:
            article.body = simple_text_process(body)
        article.source = "indian"
        producer.send_message(topic, a.to_map())
        if not db[db_name].find({'url': url}).count():
            db[db_name].insert_one(article.__dict__)
            print('Inserted 1 article in db\n from thread', Thread.getName())
    except Exception:
        print("Exception in push to mongo")


def simple_text_process(text):
    return re.sub("[^0-9a-zA-Z ',.]+", "", text).strip()


if __name__ == "__main__":
    get_cnn_news()
    # print(simple_text_process())
