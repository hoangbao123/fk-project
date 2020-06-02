from datetime import datetime

from crawler_preprocess.parser import returnCoolHTML, returnCoolXML
from mongo_driver.article import Article
from mongo_driver.models import db
from kafka_driver.kafka_producer import Producer

db_name = "news"
topic = "news"
producer = Producer()

def fetchUSElectionIndependent():
    for i in range(280, 631):
        print("==========================")
        print(i)
        data = returnCoolHTML("https://www.independent.co.uk/search/site/us%2520election?page=" + str(i))
        for headline in data.find_all("h2"):
            if headline.find("a"):
                url = headline.find("a")["href"]
                print(url)
                if not db[db_name].find({'url': url}).count():
                    a = Article(url)
                    page = returnCoolHTML(url)
                    if page.find('time') and page.find('time').has_attr('data-microtimes'):
                        a.datePublished = datetime.fromtimestamp(
                            float(eval(page.find('time')['data-microtimes'])['published'][0:10]))
                        print(a.datePublished)
                    if page.find('h1') and len(str(page.find('h1'))) <= 200:  # , {"class":"headline article-width"}):
                        a.title = page.find('h1').get_text().strip()
                        print(a.title)
                    if page.find(class_="text-wrapper"):
                        body = ""
                        for paragraph in page.find(class_="text-wrapper").find_all('p'):
                            if paragraph.parent.name == "div":
                                body += paragraph.get_text().strip() + " "
                        a.body = body
                    a.source = "The Independent"
                    producer.send_message(topic, a.to_map())
                    out = db[db_name].insert_one(a.__dict__)
                    print(out)


# Fetch articles from The Independent
def getIndependentNews():
    data = returnCoolXML('http://www.independent.co.uk/news/uk/politics/rss')
    for article in data.find_all("item"):
        url = article.find("link").get_text()
        print(url)
        if not db[db_name].find({'url': url}).count():
            a = Article(article.find("link").get_text())
            page = returnCoolHTML(article.find("link").get_text())
            if page.find('time') and page.find('time').has_attr('data-microtimes'):
                a.datePublished = datetime.fromtimestamp(
                    float(eval(page.find('time')['data-microtimes'])['published'][0:10]))
            # print(a.datePublished)
            if page.find('h1'):
                a.title = page.find('h1').get_text().strip()
            # print(a.title)
            if page.find(class_="text-wrapper"):
                body = ""
                for paragraph in page.find(class_="text-wrapper").find_all('p'):
                    if paragraph.parent.name == "div":
                        body += paragraph.get_text().strip() + " "
                a.body = body
            a.source = "The Independent"
            producer.send_message(topic, a.to_map())
            out = db[db_name].insert_one(a.__dict__)
            print('Inserted 1 article in db\n')
