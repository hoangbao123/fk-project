import pprint
import json
from datetime import datetime
from mongo_driver.article import Article
from kafka_driver.kafka_producer import Producer
from mongo_driver.models import db
from crawler_preprocess.parser import returnCoolHTML, returnCoolXML

pp = pprint.PrettyPrinter(indent=4)
producer = Producer()
db_name = "my_db"


# Fetch articles from BBC News
def getGuardianNews():
    data = returnCoolXML('https://www.theguardian.com/politics/rss')
    count = 0
    for article in data.find_all("item"):
        url = article.find("link").get_text()
        print(url)
        if not db[db_name].find({'url': url}).count():
            a = Article(article.find("link").get_text())
            page = returnCoolHTML(article.find("link").get_text())
            if page.find('time') and page.find('time').has_attr('data-timestamp'):
                a.datePublished = datetime.fromtimestamp(float(page.find('time')['data-timestamp'][0:10]))
            # print(a.datePublished)
            if page.find(class_="content__headline"):
                a.title = page.find(class_="content__headline").get_text().strip()
            if page.find(class_="content__article-body"):
                body = ""
                for paragraph in page.find(class_="content__article-body").find_all('p'):
                    body += paragraph.get_text().strip() + " "
                a.body = body
            a.source = "The Guardian"
            producer.send_message("baohn", json.dumps(a.to_map()))
            print(a.to_map())
            out = db[db_name].insert_one(a.__dict__)
            print('Inserted 1 article in db\n')


if __name__ == "__main__":
    getGuardianNews()
